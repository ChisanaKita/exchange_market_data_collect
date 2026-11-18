# 0008. Never overwrite an uploaded day archive

- Status: Accepted
- Date: 2026-11-18

## Context

On 2026-11-18 the uploader streamed `20261117.zip` (2900.8 MB) to S3 and verified its size. Then
`shutil.rmtree` failed partway with `PermissionError` on `local_cache/20261117/okx/ETHUSDT/futures`. Those
files belonged to root: a Docker container started in June with the first version of the collector was
still running and writing OKX data into the same `local_cache`. By then most of the day folder had already
been deleted.

The leftover folder still had an 8-digit name, so each hourly pass treated it as a pending day. The pass
zipped the remaining 512 MB and uploaded it to the same key, replacing the full archive. Bucket versioning
was off, so about 2.4 GB of 17 November data was lost.

The stale `local_cache/20261029.zip` that ADR 0005 could not delete (`Permission denied`) was probably
written by the same container.

## Decision

- After a verified upload, the day folder is renamed to `.uploaded-YYYYMMDD` before it is deleted. The scan
  only matches 8-digit names, so leftovers from a failed delete are never uploaded again. Each pass retries
  deleting `.uploaded-*` folders and logs an ERROR with the `sudo chown` fix while it cannot.
- Before uploading, the uploader sends HEAD for the S3 key. If the object already exists, it refuses to
  upload, logs an ERROR (which goes to Telegram) and leaves the day local for a person to resolve.
- If HEAD cannot answer (any error other than 404, for example 403 when the role has no `s3:ListBucket`),
  the upload is refused too. The design fails closed: it never uploads over an archive it could not rule out.
- The deployment guide now lists `s3:ListBucket` as required and recommends bucket versioning.

## Rejected alternatives

- **Upload to a new key when the key exists** (for example `20261117-2.zip`). This never loses data, but it
  silently creates partial duplicates that whoever processes the archives has to reconcile. A refusal with
  an alert puts a person in the loop for what should be a rare event.
- **Rename to `.uploading-YYYYMMDD` before the upload.** A crash during the upload would then hide a day
  that was never archived.

## Consequences

- A partial delete costs only disk space until permissions are fixed. It no longer costs data.
- If the process dies between the verified upload and the rename (a window of milliseconds), the next pass
  finds the archive in S3 and refuses to upload. A person then has to check the archive and delete the local
  folder.
- An instance role without `s3:ListBucket` stops uploading, with an ERROR that names the missing permission.
- `tests/test_uploader.py` covers these cases with an in-memory S3 fake and a real permission failure. Run
  `uv run --group test pytest`. These are the first tests in the repo.
