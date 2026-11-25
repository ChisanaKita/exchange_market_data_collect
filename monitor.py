"""Alert when a configured (exchange, market_type, symbol) stream stops producing market data.

The writer records the monotonic time of the last successful write per (exchange, market_type, symbol). Every
`check_interval` seconds the monitor lists the streams that have been silent for `stale_after` seconds and sends one
alert when a stream goes stale and one when it recovers. It alerts on state changes only, so a stream that stays down
does not repeat. This also catches a full disk, because the writer then fails every write.
"""
import asyncio
import logging
import time
from typing import Dict, Iterable, List, Set, Tuple

from app_logging import ALERT

logger = logging.getLogger("DataFreshnessMonitor")

Stream = Tuple[str, str, str]  # (exchange, market_type, symbol)


def _describe(streams: Iterable[Stream]) -> str:
    by_exchange: Dict[str, List[str]] = {}
    for exchange, market_type, symbol in sorted(streams):
        by_exchange.setdefault(exchange, []).append(f"{symbol} ({market_type})")
    return "\n".join(f"- {exchange}: {', '.join(symbols)}" for exchange, symbols in by_exchange.items())


class DataFreshnessMonitor:
    def __init__(self, writer, expected: Iterable[Stream], stale_after: float, check_interval: float = 60):
        self.writer = writer
        self.expected: List[Stream] = list(dict.fromkeys(expected))
        self.stale_after = stale_after
        self.check_interval = check_interval
        self.started_at = time.monotonic()
        self.stale: Set[Stream] = set()
        self.task = None

    async def start(self):
        self.started_at = time.monotonic()  # streams get a full grace period after startup
        self.task = asyncio.create_task(self._run())
        logger.info(f"Monitoring {len(self.expected)} symbols; alert after {self.stale_after / 60:.0f} min without data.")

    async def stop(self):
        if self.task:
            self.task.cancel()
            await asyncio.gather(self.task, return_exceptions=True)

    async def _run(self):
        while True:
            await asyncio.sleep(self.check_interval)
            try:
                self.check()
            except Exception as e:
                logger.error(f"Freshness check failed: {e!r}", exc_info=True)

    def check(self, now: float = None):
        now = time.monotonic() if now is None else now
        last_write = self.writer.last_write
        stale = {
            stream for stream in self.expected
            if now - last_write.get(stream, self.started_at) >= self.stale_after
        }

        newly_stale = stale - self.stale
        recovered = self.stale - stale
        self.stale = stale

        if newly_stale:
            logger.error(
                f"No market data for {self.stale_after / 60:.0f}+ min ({len(stale)}/{len(self.expected)} symbols down):\n"
                f"{_describe(newly_stale)}",
                extra=ALERT,
            )
        if recovered:
            logger.info(f"Market data resumed:\n{_describe(recovered)}", extra=ALERT)
