import asyncio
import json
from datetime import datetime, timezone
from typing import Any, List

from collectors.base import BaseExchangeCollector
from writer import MarketDataWriter

# OSL API v5 public market data (no authentication required).
OSL_WS_URL = "wss://stream-hk.osl.com/ws/v5/public"
OSL_REST_URL = "https://trade-hk.osl.com/api/v5"

OSL_INST_TYPE = "SPOT"
OSL_DEPTH_CHANNEL = "books15"  # "books5" pushes 5 levels, "books15" pushes up to 15
OSL_KLINE_INTERVAL = "1m"
OSL_HEARTBEAT_SECONDS = 30  # server drops idle connections after 60s


def _to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _parse_levels(levels: Any) -> List[List[float]]:
    return [[_to_float(level[0]), _to_float(level[1])] for level in (levels or []) if len(level) >= 2]


class OSLCollector(BaseExchangeCollector):
    exchange_name: str = "osl"

    def __init__(
        self,
        writer: MarketDataWriter,
        target_symbols: List[str],
        api_key: str = "",
        api_secret: str = "",
        ws_url: str = OSL_WS_URL,
        rest_url: str = OSL_REST_URL,
        rest_rate_limit_rps: float = 2.0,
        rest_poll_interval_ms: int = 200
    ):
        super().__init__(writer, target_symbols, rest_rate_limit_rps, rest_poll_interval_ms)
        # Public endpoints only; credentials are reserved for private channels.
        self.api_key = api_key
        self.api_secret = api_secret
        self.ws_url = ws_url
        self.rest_url = rest_url

    @staticmethod
    def get_market_type(symbol: str) -> str:
        return "spot"

    def _start_ws_tasks(self) -> List[asyncio.Task]:
        """Start the WebSocket loop."""
        return [
            asyncio.create_task(
                self._run_ws_loop(
                    ws_url=self.ws_url,
                    subscribe_func=self._subscribe_ws_streams,
                    heartbeat_func=self._run_ws_heartbeat,
                    message_handler_func=self._handle_ws_message
                )
            )
        ]

    async def _run_ws_heartbeat(self, ws):
        """Send the plain-text `ping` OSL expects; it answers with `pong`."""
        try:
            while self.running:
                await asyncio.sleep(OSL_HEARTBEAT_SECONDS)
                await ws.send("ping")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f"Error sending OSL WS heartbeat: {e}")

    async def _subscribe_ws_streams(self, ws):
        """Subscribe to ticker, depth and trade channels, one request per symbol."""
        self.logger.info(f"Subscribing OSL WS streams for symbols: {self.target_symbols}")
        for symbol in self.target_symbols:
            args = [
                {"instType": OSL_INST_TYPE, "channel": channel, "instId": symbol}
                for channel in ("ticker", OSL_DEPTH_CHANNEL, "trade")
            ]
            await ws.send(json.dumps({"op": "subscribe", "args": args}))

    async def _handle_ws_message(self, raw_message: str):
        """Parse WebSocket message and persist to MarketDataWriter."""
        try:
            if raw_message == "pong":
                return

            msg = json.loads(raw_message)

            event = msg.get("event")
            if event == "subscribe":
                self.logger.info(f"OSL WS subscribed: {msg.get('arg')}")
                return
            if event == "error":
                self.logger.error(f"OSL WS error message: {msg}")
                return

            arg = msg.get("arg") or {}
            data = msg.get("data")
            channel = arg.get("channel")
            symbol = arg.get("instId")
            if not channel or not data or symbol not in self.target_symbols:
                return

            market_type = self.get_market_type(symbol)
            push_ts = msg.get("ts") or int(datetime.now(timezone.utc).timestamp() * 1000)

            for entry in data:
                if channel == "ticker":
                    await self.writer.write(
                        exchange=self.exchange_name,
                        symbol=symbol,
                        market_type=market_type,
                        category="bbo",
                        record={
                            "timestamp": int(entry.get("ts") or push_ts),
                            "bid_price": _to_float(entry.get("bidPr")),
                            "bid_quantity": _to_float(entry.get("bidSz")),
                            "ask_price": _to_float(entry.get("askPr")),
                            "ask_quantity": _to_float(entry.get("askSz")),
                            "last_price": _to_float(entry.get("lastPr")),
                            "raw": msg
                        }
                    )
                elif channel in ("books5", "books15"):
                    await self.writer.write(
                        exchange=self.exchange_name,
                        symbol=symbol,
                        market_type=market_type,
                        category="depth",
                        record={
                            "timestamp": int(entry.get("ts") or push_ts),
                            "bids": _parse_levels(entry.get("bids")),
                            "asks": _parse_levels(entry.get("asks")),
                            "raw": msg
                        }
                    )
                elif channel == "trade":
                    await self.writer.write(
                        exchange=self.exchange_name,
                        symbol=symbol,
                        market_type=market_type,
                        category="trades",
                        record={
                            "timestamp": int(entry.get("ts") or push_ts),
                            "price": _to_float(entry.get("price")),
                            "quantity": _to_float(entry.get("size")),
                            "side": entry.get("side"),
                            "trade_id": str(entry.get("tradeId")),
                            "raw": entry
                        }
                    )
                else:
                    self.logger.debug(f"Ignoring OSL WS message on unhandled channel '{channel}'")
                    return

        except Exception as e:
            self.logger.error(f"Error handling OSL WS message: {e}", exc_info=True)

    async def _fetch_and_write_rest(self, symbol: str):
        """Fetch the latest kline from the OSL v5 REST API and write it to storage."""
        url = f"{self.rest_url}/kline"
        params = {"symbol": symbol, "interval": OSL_KLINE_INTERVAL, "limit": "1"}
        headers = {"User-Agent": "Mozilla/5.0"}
        async with self.session.get(url, params=params, headers=headers, timeout=5) as response:
            response.raise_for_status()
            raw_data = await response.json(content_type=None)

        # Errors come back as HTTP 200 with a JSON object, e.g. {"code": -1107, "msg": "symbol not exist"}
        if not isinstance(raw_data, list):
            raise ValueError(f"OSL kline request for {symbol} failed: {raw_data}")

        for candle in raw_data:
            # [openTime, open, high, low, close, volume, closeTime, quoteVolume, numTrades, takerBuyBase, takerBuyQuote]
            await self.writer.write(
                exchange=self.exchange_name,
                symbol=symbol,
                market_type=self.get_market_type(symbol),
                category="kline_1m_rest",
                record={
                    "timestamp": int(candle[0]),
                    "open_time": int(candle[0]),
                    "close_time": int(candle[6]),
                    "open": _to_float(candle[1]),
                    "high": _to_float(candle[2]),
                    "low": _to_float(candle[3]),
                    "close": _to_float(candle[4]),
                    "volume": _to_float(candle[5]),
                    "quote_volume": _to_float(candle[7]),
                    "trades": int(candle[8]),
                    "raw": candle
                }
            )
