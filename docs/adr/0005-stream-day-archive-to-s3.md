# 0005. Stream the daily archive to S3 instead of staging a zip on disk

- Status: Accepted
- Date: 2026-11-03

## Context

From 2026-10-29 completed days stopped being deleted from `local_cache` and the 50 GB EC2 volume filled.
`uploader.py` has not changed since July, so the trigger was on the server (S3 access, network, or a
failed upload), not a code change. But the design made any failure permanent: `_process_day_upload` wrote
the whole day's zip next to the data before uploading. On a nearly full disk that zip could not be
written, so the upload failed on every hourly retry and the data that needed freeing was never freed.

## Decision

- The day directory is zipped on a thread straight into an OS pipe, and `upload_fileobj` reads the pipe
  as a multipart upload (64 MB parts). No temporary zip is written, so the upload needs no free disk.
- Same S3 key and same archive layout as before (`<prefix>/YYYY/MM/DD/YYYYMMDD.zip`, rooted at the day folder).
- The local day directory is deleted only after `head_object` reports exactly the bytes the zip writer
  produced. If the zip writer fails midway, the reader raises at end of stream, so a truncated archive is
  never completed as an S3 object.
- Failures are logged with a traceback (previously only the message), days are processed oldest first,
  and every hourly pass logs free disk and the completed days still waiting to be uploaded (ERROR when
  free space is under 15% with a backlog).

- Zips that earlier versions left in the cache (`YYYYMMDD.zip` whose day directory still exists) are
  deleted best effort at the start of each pass. A relaunch log on 2026-11-03 showed the old code failing
  on `Permission denied: 'local_cache/20261029.zip'`, a stale zip it could not overwrite, which left that
  day (and its disk space) stuck. If another user owns the zip it is reported with the `sudo rm` to run.

## Consequences

- A full disk no longer blocks cleanup; the first failing step is visible in the log.
- Data is still never deleted without a verified upload, so a persistent S3 problem (credentials, IAM,
  bucket, network) still leaves days on disk; the new log lines make that obvious instead of silent.
- A retry re-zips and re-uploads the day from scratch (as before).
