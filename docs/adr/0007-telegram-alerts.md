# 0007. Telegram alerts from the log stream, plus a data freshness monitor

- Status: Accepted
- Date: 2026-11-16

## Context

Completed days stayed in `local_cache` until the disk filled, and market data was lost before anyone noticed.
ADR 0006 made the cause visible in log files, but someone still has to read them. The owner wants failures pushed to
Telegram.

## Decision

- **Alerts are a loguru sink** (`alerts.py`), not separate notify calls spread through the code. Any log line can
  become an alert, and the uploader thread, the event loop and crash hooks all use the same path. The sink uses
  `enqueue=True`, so the blocking Bot API request runs on loguru's worker thread, never on the event loop.
- **What is sent.** Records marked `extra=ALERT`, every CRITICAL, and ERROR from anything except the exchange
  collectors. Collector ERRORs are mostly transient (a WebSocket reconnect, a REST timeout) and would flood the
  chat. We rejected forwarding them, and rejected only rate-limiting them.
- **Impact over cause: `monitor.py`.** The writer records the last successful write per (exchange, symbol). Every
  minute the monitor sends one alert when configured symbols have been silent for `STALE_DATA_ALERT_MINUTES` (5),
  and one when they resume. Because it measures data actually written, it also catches a full disk, a dead
  subscription or a hung collector, none of which produce a specific error line.
- **Positive confirmation.** Each archived day sends a message. A missing message after UTC midnight means the
  upload did not succeed, even if the failure itself was never logged (for example a hang).
- **Noise control.** The same alert, compared with digits ignored, is sent at most once per
  `TELEGRAM_ALERT_COOLDOWN_MINUTES` (60). At most 30 alerts go out per hour, then one notice. Failed sends are
  logged locally and never retried through Telegram, so an API outage cannot loop.
- Plain text, no `parse_mode`, so log text never needs Markdown escaping. stdlib `urllib`, so there is no new
  dependency.
- Configured only through `.env` (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`). Alerts are off when either is missing.
  The token is never committed.

## Consequences

- A Bot API outage or a blocked egress only loses alerts; collection and logging continue.
- Per-symbol freshness assumes every configured symbol writes at least once per threshold. That holds today
  because REST order book polling writes every 200 ms. A symbol that is delisted or misnamed alerts once at startup
  and stays quiet afterwards.
- Alerts are only sent while the process runs. If the container or instance dies without SIGTERM, no message
  arrives. Silence is detected only by noticing the missing daily "archived" message. An external heartbeat would be
  the next step if that is not enough.
