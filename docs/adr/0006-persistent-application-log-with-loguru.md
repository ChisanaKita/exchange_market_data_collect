# 0006. Persistent application log with loguru, kept 30 days

- Status: Accepted
- Date: 2026-11-16

## Context

After ADR 0005 shipped, completed days in `local_cache` were still not uploaded and the EC2 disk filled
again. The uploader logs every failure with a traceback, but those lines went only to stdout. Docker's
`json-file` driver keeps 5 x 10 MB, so a day of collector output can push out the midnight upload attempt, and
`docker compose up --build` or `down` removes the container's log entirely. We could not see why the uploads failed.

## Decision

- `app_logging.setup_logging()` sets up loguru with two sinks: stdout (so `docker logs` still works) and
  `LOG_DIR/app_YYYY-MM-DD.log`.
- Existing modules keep using `logging.getLogger(name)`. An intercept handler sends standard-library records
  (including boto3 and asyncio warnings) to loguru with the original logger name. We did not rewrite every module
  to import loguru.
- Rotation happens at UTC midnight, or earlier when a file would pass `LOG_MAX_FILE_MB` (default 100). The size cap
  matters because the log shares the disk with the market data, so a log flood must not cause the next disk-full.
- Retention is `LOG_RETENTION_DAYS` (default 30), measured from file modification time. On top of that, the
  oldest files are deleted once all log files together pass `LOG_MAX_TOTAL_MB` (default 2000). Loguru applies
  retention when it rotates, so it runs at the first log line after UTC midnight and at every size split, not at startup.
- `diagnose=False`, because loguru's variable dump in tracebacks would write Panther API secrets into the file.
- Uncaught exceptions in the main thread and in worker threads (such as the zip producer) are logged, not just
  printed to stderr.
- Docker compose bind-mounts `./logs` to `/app/logs`, so logs survive container rebuilds.
- loguru is pinned to 0.7.3. 0.8.0 was released on 2026-11-11, too recently to trust on the production collector.

## Consequences

- The uploader's hourly `Disk:` line and any `Failed to process and upload` traceback are on the host for 30 days.
- Log disk use is bounded by `LOG_MAX_TOTAL_MB` plus one file (`LOG_MAX_FILE_MB`). At normal volume it is a few MB
  per day, so the 30-day limit is the one that applies. During a flood the total cap applies, so fewer than 30 days are kept.
- Log writes are synchronous (no `enqueue`), so the last lines before a crash are on disk. The cost is a
  small blocking write on the event loop per line, which is acceptable at this volume.
