import asyncio
from datetime import datetime, timezone
from typing import List

import aiohttp

from collectors.hashkey import HashkeyCollector
from writer import MarketDataWriter

# Since 2026-06-16 HashKey MENA (UAE) is served from the HashKey HK platform hosts.
# The MENA market is selected via the `site=MENA` parameter on every public
# market-data request / WS subscription (defaults to HK if omitted).
HASHKEY_MENA_WS_URL = "wss://stream-pro.hashkey.com/quote/ws/v2"
HASHKEY_MENA_REST_URL = "https://api-pro.hashkey.com"


class HashkeyMenaCollector(HashkeyCollector):
    exchange_name: str = "hashkey_mena"

    # MENA listings as of 2026-09: USDT perpetuals (crypto + tokenised equities/ETFs)
    # plus USD/USDT/AED spot pairs.
    UNIFIED_TO_EXCHANGE = {
        "BTCUSDT-PERPETUAL": "BTCUSDT-PERPETUAL",
        "ETHUSDT-PERPETUAL": "ETHUSDT-PERPETUAL",
        "SKHYNIXUSDT-PERPETUAL": "SKHYNIXUSDT-PERPETUAL",
        "QQQUSDT-PERPETUAL": "QQQUSDT-PERPETUAL",
        "SPCXUSDT-PERPETUAL": "SPCXUSDT-PERPETUAL",
        "SOXLUSDT-PERPETUAL": "SOXLUSDT-PERPETUAL",
        "USDTUSDC": "USDTUSDC"
    }

    WS_SUBSCRIBE_EXTRA = {"site": "MENA"}
    REST_EXTRA_PARAMS = {"site": "MENA"}

    def __init__(
        self,
        writer: MarketDataWriter,
        target_symbols: List[str],
        rest_rate_limit_rps: float = 1.5,
        rest_poll_interval_ms: int = 200,
        funding_rate_delay_ms: int = 500,
        ws_url: str = HASHKEY_MENA_WS_URL,
        rest_url: str = HASHKEY_MENA_REST_URL
    ):
        super().__init__(
            writer,
            target_symbols,
            rest_rate_limit_rps=rest_rate_limit_rps,
            rest_poll_interval_ms=rest_poll_interval_ms,
            ws_url=ws_url,
            rest_url=rest_url
        )
        self.funding_rate_delay_ms = funding_rate_delay_ms
        # Funding rate only exists for perpetual contracts
        self.funding_rate_symbols = [s for s in self.target_symbols if self.get_market_type(s) == "futures"]

    async def start(self):
        await super().start()
        if self.funding_rate_symbols:
            self.tasks.append(asyncio.create_task(self._run_funding_rate_polling()))

    async def _run_funding_rate_polling(self):
        """Query funding rate for each perpetual sequentially, pausing between queries."""
        delay_sec = self.funding_rate_delay_ms / 1000.0

        while self.running:
            for symbol in self.funding_rate_symbols:
                if not self.running:
                    break

                # Honour the global backoff shared with the REST depth pollers
                now = asyncio.get_event_loop().time()
                if now < self.global_backoff_until:
                    await asyncio.sleep(self.global_backoff_until - now)
                    continue

                try:
                    await self._fetch_and_write_funding_rate(symbol)
                except asyncio.CancelledError:
                    return
                except aiohttp.ClientResponseError as cre:
                    if cre.status == 429:
                        self.logger.warning("Funding rate polling hit HTTP 429 (Too Many Requests). Setting global backoff for 60 seconds...")
                        self.global_backoff_until = asyncio.get_event_loop().time() + 60.0
                    else:
                        self.logger.error(f"HTTP error fetching funding rate for {symbol}: status={cre.status}, msg={cre.message}")
                except Exception as e:
                    self.logger.error(f"Error polling funding rate for {symbol}: {e}")

                await asyncio.sleep(delay_sec)

    async def _fetch_and_write_funding_rate(self, symbol: str):
        """Fetch current funding rate from REST API and write to storage."""
        url = f"{self.rest_url}/api/v2/futures/fundingRate"
        query_ts = int(datetime.now(timezone.utc).timestamp() * 1000)
        params = {"symbol": symbol, "state": "current", "timestamp": str(query_ts), **self.REST_EXTRA_PARAMS}
        async with self.session.get(url, params=params, timeout=5) as response:
            response.raise_for_status()
            raw_data = await response.json()

            # Response is a list; empty when the symbol is unknown
            if not isinstance(raw_data, list) or not raw_data:
                self.logger.warning(f"Empty funding rate response for {symbol}: {raw_data}")
                return

            for entry in raw_data:
                next_funding_time = entry.get("nextFundingTime")
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=entry.get("symbol", symbol),
                    market_type="futures",
                    category="funding_rate",
                    record={
                        "timestamp": query_ts,
                        "rate": float(entry.get("rate", 0.0)),
                        "next_funding_time": int(next_funding_time) if next_funding_time else None,
                        "raw": entry
                    }
                )
