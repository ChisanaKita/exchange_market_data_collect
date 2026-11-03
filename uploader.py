import os
import shutil
import logging
import asyncio
import threading
import zipfile
from datetime import datetime, timezone
from pathlib import Path
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from config import (
    LOCAL_DATA_DIR,
    S3_BUCKET_NAME,
    S3_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    S3_PREFIX,
    UPLOAD_DELAY_MINUTES
)

logger = logging.getLogger("MarketDataUploader")

# Multipart part size for the streamed upload (a stream has no known size, and S3 allows at most 10000 parts)
UPLOAD_PART_SIZE = 64 * 1024 * 1024


class _CountingWriter:
    """Write-only (non-seekable) file object that counts the bytes written through it."""

    def __init__(self, fileobj):
        self._fileobj = fileobj
        self.bytes_written = 0

    def write(self, data):
        self.bytes_written += len(data)
        return self._fileobj.write(data)

    def flush(self):
        self._fileobj.flush()


class _PipeReader:
    """Read end of the zip pipe. If the zip producer failed, reaching EOF raises instead of looking like a clean
    end of stream, so a truncated zip can never be uploaded as if it were complete."""

    def __init__(self, fileobj, state: dict):
        self._fileobj = fileobj
        self._state = state

    def read(self, size=-1):
        data = self._fileobj.read(size)  # buffered: returns `size` bytes unless the stream has ended
        if (size is None or size < 0 or len(data) < size) and self._state.get("error"):
            raise RuntimeError(f"zip producer failed: {self._state['error']!r}")
        return data

    def close(self):
        self._fileobj.close()


class MarketDataUploader:
    def __init__(self, base_dir: str = LOCAL_DATA_DIR):
        self.base_dir = Path(base_dir)
        self.running = False
        self.task = None

        # Configure global AWS region environment variables so that any internal clients 
        # created by botocore (e.g. for credential refreshing) have a default region.
        import os
        if S3_REGION:
            os.environ.setdefault("AWS_DEFAULT_REGION", S3_REGION)
            os.environ.setdefault("AWS_REGION", S3_REGION)

        # Initialize boto3 Session and S3 client
        # If credentials are not specified, boto3 automatically searches local env variables, 
        # AWS shared credentials file, or IAM instance profile.
        session_kwargs = {}
        if S3_REGION:
            session_kwargs["region_name"] = S3_REGION
            
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            session_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
            session_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
            logger.info("Initializing S3 client with configured credentials.")
        else:
            logger.info("Initializing S3 client using IAM Instance Profile or system environment.")
            
        self.session = boto3.Session(**session_kwargs)
        self.s3_client = self.session.client("s3")

    async def start(self):
        """Start the background uploader task."""
        self.running = True
        self.task = asyncio.create_task(self._run_uploader_loop())
        logger.info("Market Data Uploader successfully started.")

    async def stop(self):
        """Stop the background uploader gracefully."""
        self.running = False
        if self.task:
            self.task.cancel()
        logger.info("Market Data Uploader stopped.")

    async def _run_uploader_loop(self):
        """Periodically checks if there is completed day data that needs to be zipped and uploaded."""
        while self.running:
            try:
                # Run the upload check on startup and then every hour
                await self.check_and_upload_completed_days()
            except Exception as e:
                logger.error(f"Error in uploader loop iteration: {e}")
            
            # Sleep for 1 hour before checking again
            await asyncio.sleep(3600)

    async def check_and_upload_completed_days(self):
        """Scan the local cache directory for folders representing past UTC days, zip, and upload them."""
        # Current day in UTC
        today_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        
        # Scan local directory
        if not self.base_dir.exists():
            return

        self._log_disk_status(today_str)

        for path in sorted(self.base_dir.iterdir()):
            if not path.is_dir():
                continue

            dir_name = path.name
            # Check if directory is named YYYYMMDD (length 8 and is numeric)
            if len(dir_name) == 8 and dir_name.isdigit():
                # If directory represents a completed day (older than today)
                if dir_name < today_str:
                    # Double-check: Make sure we are at least UPLOAD_DELAY_MINUTES past midnight UTC
                    # so that all late writers are completely finished and handles are closed.
                    now_utc = datetime.now(timezone.utc)
                    midnight_utc = datetime.combine(now_utc.date(), datetime.min.time(), tzinfo=timezone.utc)
                    minutes_since_midnight = (now_utc - midnight_utc).total_seconds() / 60.0
                    
                    if minutes_since_midnight < UPLOAD_DELAY_MINUTES:
                        logger.info(f"Day {dir_name} is completed, but waiting for {UPLOAD_DELAY_MINUTES} minutes past midnight UTC buffer. (Current minutes: {minutes_since_midnight:.1f})")
                        continue

                    logger.info(f"Found completed day directory ready for S3 upload: {dir_name}")
                    # Run CPU-bound zipping and S3 uploading in executors to prevent blocking event loop
                    await asyncio.to_thread(self._process_day_upload, path)

    def _log_disk_status(self, today_str: str):
        """Report free disk and any days still waiting to be uploaded, so a stuck uploader shows up in the logs."""
        usage = shutil.disk_usage(self.base_dir)
        pending = sorted(
            p.name for p in self.base_dir.iterdir()
            if p.is_dir() and len(p.name) == 8 and p.name.isdigit() and p.name < today_str
        )
        message = f"Disk: {usage.free / 1e9:.1f} GB free of {usage.total / 1e9:.1f} GB. Completed days waiting for upload: {pending or 'none'}"
        if pending and usage.free / usage.total < 0.15:
            logger.error(f"{message}. Disk is nearly full; uploads must succeed to free space.")
        else:
            logger.info(message)

    def _stream_zip_to_s3(self, day_dir: Path, s3_key: str):
        """Zip `day_dir` straight into an S3 multipart upload through a pipe, with no temporary zip on disk.

        The previous implementation wrote the whole day's zip next to the data first, which needs free disk
        space; on a full disk that failed forever and the cache could never be cleaned up.
        """
        read_fd, write_fd = os.pipe()
        state = {"error": None, "bytes": 0}

        def produce():
            try:
                with os.fdopen(write_fd, "wb") as write_end:
                    counter = _CountingWriter(write_end)
                    with zipfile.ZipFile(counter, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as archive:
                        for file_path in sorted(p for p in day_dir.rglob("*") if p.is_file()):
                            # The day directory is the archive root (e.g. 20260616/hashkey/...)
                            archive.write(file_path, arcname=file_path.relative_to(day_dir.parent).as_posix())
                    state["bytes"] = counter.bytes_written
            except BaseException as e:
                state["error"] = e

        producer = threading.Thread(target=produce, name=f"zip-{day_dir.name}", daemon=True)
        producer.start()
        reader = _PipeReader(os.fdopen(read_fd, "rb"), state)
        try:
            self.s3_client.upload_fileobj(
                reader,
                Bucket=S3_BUCKET_NAME,
                Key=s3_key,
                Config=TransferConfig(multipart_chunksize=UPLOAD_PART_SIZE)
            )
        finally:
            reader.close()  # unblocks the producer (broken pipe) if the upload stopped early
            producer.join()

        if state["error"]:
            raise state["error"]

        # Never delete local data unless S3 holds exactly the bytes we produced
        remote_size = self.s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=s3_key)["ContentLength"]
        if remote_size != state["bytes"]:
            raise RuntimeError(f"S3 object size {remote_size} != zip size {state['bytes']} for {s3_key}")
        return state["bytes"]

    def _process_day_upload(self, day_dir: Path):
        """Zip and upload a completed day, then delete it locally only after the upload is verified."""
        day_str = day_dir.name
        year = day_str[0:4]
        month = day_str[4:6]
        day = day_str[6:8]

        # Calculate S3 target key: e.g. crypto-market-data/2026/06/16/20260616.zip
        s3_key = f"{S3_PREFIX}{year}/{month}/{day}/{day_str}.zip"

        try:
            logger.info(f"Zipping {day_dir} and streaming it to s3://{S3_BUCKET_NAME}/{s3_key}...")
            size = self._stream_zip_to_s3(day_dir, s3_key)
            logger.info(f"S3 upload successful for {day_str} ({size / 1e6:.1f} MB zipped).")

            # On success, clean up the local day directory to save space
            shutil.rmtree(day_dir)
            logger.info(f"Cleanup finished. Day {day_str} successfully archived to S3.")

        except (NoCredentialsError, PartialCredentialsError) as cred_err:
            logger.error(f"S3 Upload failed due to credentials error: {cred_err}. Leaving files local.")
        except Exception as e:
            logger.error(f"Failed to process and upload {day_str}: {e!r}. Leaving files local.", exc_info=True)
