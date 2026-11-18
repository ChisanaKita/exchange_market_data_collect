"""Uploader safety tests: a day archive in S3 must never be replaced by a smaller, partial one.

Regression for 2026-11-18: after a verified upload of 20261117, `shutil.rmtree` failed partway on a folder owned
by another user. The half-deleted day folder still looked like a pending day, so the next pass zipped what was
left and overwrote the full 2.9 GB archive with a 512 MB one.
"""
import asyncio
import io
import os
import stat

import pytest
from botocore.exceptions import ClientError

import uploader
from uploader import MarketDataUploader

DAY = "20000101"  # always in the past, so the uploader treats it as a completed day


class FakeS3:
    """In-memory stand-in for the boto3 S3 client calls the uploader makes."""

    def __init__(self, head_error_code="404"):
        self.objects = {}
        self.put_count = 0
        self.head_error_code = head_error_code  # what HEAD on a missing key returns (403 without s3:ListBucket)

    def upload_fileobj(self, fileobj, Bucket, Key, Config=None):
        buffer = io.BytesIO()
        while chunk := fileobj.read(1024 * 1024):
            buffer.write(chunk)
        self.objects[Key] = buffer.getvalue()
        self.put_count += 1

    def head_object(self, Bucket, Key):
        if Key not in self.objects:
            raise ClientError({"Error": {"Code": self.head_error_code, "Message": "Not Found"}}, "HeadObject")
        return {"ContentLength": len(self.objects[Key])}


def make_day(base, files):
    for relative, content in files.items():
        path = base / DAY / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def s3_key():
    return f"{uploader.S3_PREFIX}2000/01/01/{DAY}.zip"


@pytest.fixture
def cache(tmp_path, monkeypatch):
    monkeypatch.setattr(uploader, "UPLOAD_DELAY_MINUTES", 0)
    base = tmp_path / "local_cache"
    base.mkdir()
    yield base
    # Restore write permission so pytest can clean up read-only folders created by a test
    for root, dirs, _ in os.walk(base):
        for name in dirs:
            os.chmod(os.path.join(root, name), stat.S_IRWXU)


def make_uploader(base, s3):
    up = MarketDataUploader(base_dir=str(base))
    up.s3_client = s3
    return up


def run_pass(up):
    asyncio.run(up.check_and_upload_completed_days())


def lock_folder(path):
    """Make a folder's entries undeletable for this user, like a folder owned by root with mode 755."""
    os.chmod(path, stat.S_IRUSR | stat.S_IXUSR)


def test_verified_upload_removes_day_folder(cache):
    make_day(cache, {"gate/BTC_USDT/futures/trades.jsonl": "x" * 100})
    s3 = FakeS3()

    run_pass(make_uploader(cache, s3))

    assert s3.put_count == 1
    assert s3_key() in s3.objects
    assert list(cache.iterdir()) == []


def test_failed_local_delete_never_reuploads_the_day(cache):
    make_day(cache, {
        "gate/BTC_USDT/futures/trades.jsonl": "x" * 10_000,
        "okx/ETHUSDT/futures/liquidations.jsonl": "y" * 100,
    })
    lock_folder(cache / DAY / "okx" / "ETHUSDT")
    s3 = FakeS3()
    up = make_uploader(cache, s3)

    run_pass(up)
    full_archive = s3.objects[s3_key()]
    run_pass(up)
    run_pass(up)

    assert s3.put_count == 1
    assert s3.objects[s3_key()] == full_archive


def test_failed_local_delete_is_retried_once_permissions_are_fixed(cache):
    make_day(cache, {"okx/ETHUSDT/futures/liquidations.jsonl": "y" * 100})
    lock_folder(cache / DAY / "okx" / "ETHUSDT")
    s3 = FakeS3()
    up = make_uploader(cache, s3)

    run_pass(up)
    leftovers = [p for p in cache.iterdir()]
    assert leftovers, "the undeletable files should still be on disk"
    for root, dirs, _ in os.walk(cache):
        for name in dirs:
            os.chmod(os.path.join(root, name), stat.S_IRWXU)
    run_pass(up)

    assert list(cache.iterdir()) == []
    assert s3.put_count == 1


def test_existing_s3_archive_is_never_overwritten(cache):
    make_day(cache, {"gate/BTC_USDT/futures/trades.jsonl": "partial"})
    s3 = FakeS3()
    s3.objects[s3_key()] = b"the full archive uploaded earlier"

    run_pass(make_uploader(cache, s3))

    assert s3.put_count == 0
    assert s3.objects[s3_key()] == b"the full archive uploaded earlier"
    assert (cache / DAY / "gate/BTC_USDT/futures/trades.jsonl").exists()


def test_upload_is_refused_when_s3_cannot_say_whether_the_archive_exists(cache):
    # Without s3:ListBucket, HEAD on a missing key returns 403 instead of 404
    make_day(cache, {"gate/BTC_USDT/futures/trades.jsonl": "x"})
    s3 = FakeS3(head_error_code="403")

    run_pass(make_uploader(cache, s3))

    assert s3.put_count == 0
    assert (cache / DAY / "gate/BTC_USDT/futures/trades.jsonl").exists()
