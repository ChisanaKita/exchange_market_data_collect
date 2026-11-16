"""Application logging built on loguru.

Every module keeps using the standard `logging.getLogger(name)` API. `setup_logging()` routes those records into
loguru, which writes them to stdout (picked up by `docker logs`) and to daily log files under `LOG_DIR` that are
kept for `LOG_RETENTION_DAYS` days. See docs/adr/0006-persistent-application-log-with-loguru.md.
"""
import logging
import os
import sys
import threading
import time
from datetime import timezone
from pathlib import Path

from loguru import logger

LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS!UTC} [{level}] {extra[logger_name]}: {message}"

# Chatty third-party libraries are capped at WARNING
_QUIET_LIBRARIES = ("websockets", "urllib3", "botocore", "boto3", "s3transfer", "asyncio")


class _InterceptHandler(logging.Handler):
    """Forward standard-library log records to loguru, keeping the original logger name and caller."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Walk past the logging module's own frames so loguru reports the real caller
        frame, depth = logging.currentframe(), 0
        while frame is not None and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.bind(logger_name=record.name).opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class _DailyOrSizeRotation:
    """Start a new file at each UTC midnight, or earlier once the current file would exceed `max_bytes`.

    The size cap keeps a log flood (e.g. a reconnect loop) from filling the same disk that holds the market data.
    """

    def __init__(self, max_bytes: int):
        self.max_bytes = max_bytes
        self.day = None

    def __call__(self, message, file) -> bool:
        day = message.record["time"].astimezone(timezone.utc).date()
        if self.day is None:
            self.day = day
        if day != self.day:
            self.day = day
            return True
        return file.tell() + len(message) > self.max_bytes


class _AgeAndTotalSizeRetention:
    """Delete log files older than `max_age_days`, then the oldest files until all together fit in `max_total_bytes`.

    loguru calls this on each rotation, after closing the current file and before opening the next one, with every
    file that matches the log name pattern.
    """

    def __init__(self, max_age_days: int, max_total_bytes: int):
        self.max_age_seconds = max_age_days * 86400
        self.max_total_bytes = max_total_bytes

    def __call__(self, logs) -> None:
        cutoff = time.time() - self.max_age_seconds
        kept = []
        for log in logs:
            stat = os.stat(log)
            if stat.st_mtime <= cutoff:
                os.remove(log)
            else:
                kept.append((stat.st_mtime, stat.st_size, log))

        kept.sort(reverse=True)  # newest first
        total = 0
        for _, size, log in kept:
            total += size
            if total > self.max_total_bytes:
                os.remove(log)


def setup_logging(
    log_dir: str,
    level: str = "INFO",
    retention_days: int = 30,
    max_file_mb: int = 100,
    max_total_mb: int = 2000,
) -> Path:
    """Configure stdout and rotating file logging. Returns the log directory."""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    logger.remove()
    logger.configure(extra={"logger_name": "app"})

    # diagnose=False: loguru's variable dump in tracebacks could write API secrets into the log
    logger.add(sys.stdout, level=level, format=LOG_FORMAT, backtrace=False, diagnose=False)
    logger.add(
        log_path / "app_{time:YYYY-MM-DD!UTC}.log",
        level=level,
        format=LOG_FORMAT,
        rotation=_DailyOrSizeRotation(max_file_mb * 1024 * 1024),
        retention=_AgeAndTotalSizeRetention(retention_days, max_total_mb * 1024 * 1024),
        encoding="utf-8",
        backtrace=False,
        diagnose=False,
    )

    logging.basicConfig(handlers=[_InterceptHandler()], level=0, force=True)
    for name in _QUIET_LIBRARIES:
        logging.getLogger(name).setLevel(logging.WARNING)

    # Errors that would otherwise go only to stderr
    def _log_uncaught(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_tb)
            return
        logger.bind(logger_name="Main").opt(exception=(exc_type, exc_value, exc_tb)).critical("Uncaught exception")

    def _log_thread_exception(args):
        logger.bind(logger_name=f"Thread:{args.thread.name if args.thread else '?'}").opt(
            exception=(args.exc_type, args.exc_value, args.exc_traceback)
        ).error("Uncaught exception in thread")

    sys.excepthook = _log_uncaught
    threading.excepthook = _log_thread_exception

    return log_path
