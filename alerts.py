"""Telegram alerts, delivered as a loguru sink.

Which records are sent (see `should_alert`):
- any record logged with `extra=ALERT` (stdlib) / bound with `alert=True` (loguru), at any level;
- every CRITICAL record;
- ERROR records, except from exchange collectors. Collector errors are mostly transient (a WebSocket reconnect
  that recovers in seconds); missing data is reported by the freshness monitor instead (monitor.py).

The sink runs on loguru's queue thread (`enqueue=True`), so the blocking HTTP call never stalls the event loop.
See docs/adr/0007-telegram-alerts.md.
"""
import json
import logging
import re
import socket
import time
import urllib.error
import urllib.request
from datetime import timezone

from loguru import logger

_log = logging.getLogger("TelegramAlerts")

TELEGRAM_MAX_MESSAGE_CHARS = 4096
_DIGITS = re.compile(r"\d+")


def should_alert(record) -> bool:
    if record["extra"].get("alert"):
        return True
    level = record["level"].no
    if level >= logger.level("CRITICAL").no:
        return True
    return level >= logger.level("ERROR").no and not str(record["extra"].get("logger_name", "")).endswith("Collector")


class TelegramAlertSink:
    """Send log records to one Telegram chat, with de-duplication and an hourly cap.

    Records whose logger and message are equal once digits are ignored (so "free 4.1 GB" and "free 3.9 GB" match)
    are sent at most once per `cooldown_seconds`. At most `max_per_hour` messages are sent per hour; after that
    one notice is sent and the rest of the hour is dropped (it is still in the log files).
    """

    def __init__(self, token: str, chat_id: str, instance_name: str, cooldown_seconds: float, max_per_hour: int = 30):
        self._url = f"https://api.telegram.org/bot{token}/sendMessage"
        self._chat_id = chat_id
        self._instance_name = instance_name
        self._cooldown_seconds = cooldown_seconds
        self._max_per_hour = max_per_hour
        self._last_sent: dict[tuple, float] = {}
        self._hour_start = 0.0
        self._sent_this_hour = 0
        self._muted_notice_sent = False

    def __call__(self, message) -> None:
        record = message.record
        now = time.monotonic()

        key = (record["extra"].get("logger_name"), record["level"].name, _DIGITS.sub("#", record["message"]))
        last = self._last_sent.get(key)
        if last is not None and now - last < self._cooldown_seconds:
            return

        if now - self._hour_start >= 3600:
            self._hour_start, self._sent_this_hour, self._muted_notice_sent = now, 0, False
        if self._sent_this_hour >= self._max_per_hour:
            if not self._muted_notice_sent:
                self._muted_notice_sent = True
                self._send(f"[{self._instance_name}] Alert limit of {self._max_per_hour}/hour reached. "
                           "Further alerts this hour are only in the log files.")
            return

        self._last_sent[key] = now
        self._sent_this_hour += 1
        self._send(self._format(record))

    def _format(self, record) -> str:
        time_str = record["time"].astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        lines = [
            f"[{self._instance_name}] {record['level'].name}",
            f"{record['extra'].get('logger_name', 'app')} at {time_str}",
            "",
            record["message"],
        ]
        exception = record["exception"]
        if exception is not None and exception.type is not None:
            lines.append(f"{exception.type.__name__}: {exception.value}")
        text = "\n".join(lines)
        if len(text) > TELEGRAM_MAX_MESSAGE_CHARS:
            text = text[: TELEGRAM_MAX_MESSAGE_CHARS - 20] + "\n...(truncated)"
        return text

    def _send(self, text: str) -> None:
        """POST to the Bot API. Never raises: a failed alert must not break logging."""
        body = json.dumps({"chat_id": self._chat_id, "text": text, "disable_web_page_preview": True}).encode()
        for attempt in range(2):
            request = urllib.request.Request(self._url, data=body, headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(request, timeout=10):
                    return
            except urllib.error.HTTPError as e:
                retry_after = 0
                try:
                    retry_after = json.loads(e.read()).get("parameters", {}).get("retry_after", 0)
                except Exception:
                    pass
                if e.code == 429 and attempt == 0 and retry_after:
                    time.sleep(min(retry_after, 30))
                    continue
                self._report_failure(f"HTTP {e.code}")
                return
            except Exception as e:
                if attempt == 0:
                    time.sleep(2)
                    continue
                self._report_failure(repr(e))
                return

    @staticmethod
    def _report_failure(reason: str) -> None:
        # The sink's filter drops "TelegramAlerts" records, so this goes to the log files only. The URL holds the
        # token, so only the reason is logged.
        logger.bind(logger_name="TelegramAlerts").warning(f"Could not send Telegram alert: {reason}")


def add_telegram_sink(token: str, chat_id: str, instance_name: str = "", cooldown_minutes: float = 60) -> bool:
    """Attach the Telegram sink if a token and chat id are configured. Returns whether alerts are enabled."""
    if not (token and chat_id):
        _log.warning("Telegram alerts disabled: set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to enable them.")
        return False

    sink = TelegramAlertSink(token, chat_id, instance_name or socket.gethostname(), cooldown_minutes * 60)
    # Filter out the sink's own failure reports so a Telegram outage cannot loop
    logger.add(
        sink,
        level="DEBUG",
        filter=lambda r: r["extra"].get("logger_name") != "TelegramAlerts" and should_alert(r),
        enqueue=True,
        catch=True,
    )
    return True
