import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from typing import List, Dict, Any

from collectors.base import BaseExchangeCollector
from writer import MarketDataWriter

OSL_WS_URL = "wss://stream-api.osl.com/openapi/v1/ws"


class OSLCollector(BaseExchangeCollector):
    exchange_name: str = "osl"

    UNIFIED_TO_EXCHANGE = {
        "BTCUSDT-PERPETUAL": "BTCUSDC",
        "BTCUSD-PERPETUAL": "BTCUSDC",
        "BTC-PERP": "BTCUSDC",
        "BTCUSDC": "BTCUSDC",
        "USDTUSD": "USDTUSD"
    }
    EXCHANGE_TO_UNIFIED = {
        "BTCUSDC": "BTC-PERP",
        "USDTUSD": "USDTUSD"
    }

    def __init__(
        self,
        writer: MarketDataWriter,
        target_symbols: List[str],
        api_key: str = "",
        api_secret: str = "",
        ws_url: str = OSL_WS_URL,
        rest_url: str = "https://api.osl.com",
        rest_rate_limit_rps: float = 2.0,
        rest_poll_interval_ms: int = 200
    ):
        # Exclusively restrict OSL collector to BTC-PERP (BTCUSDC) and USDTUSD spot
        target_osl_symbols = ["BTCUSDC", "USDTUSD"]
        super().__init__(writer, target_osl_symbols, rest_rate_limit_rps, rest_poll_interval_ms)
        self.api_key = api_key
        self.api_secret = api_secret
        self.ws_url = ws_url
        self.rest_url = rest_url

    def to_unified_symbol(self, exchange_symbol: str) -> str:
        return self.EXCHANGE_TO_UNIFIED.get(exchange_symbol, exchange_symbol)

    def get_market_type(self, symbol: str) -> str:
        unified = self.to_unified_symbol(symbol)
        if "PERP" in symbol or "PERPETUAL" in symbol or "PERP" in unified or "PERPETUAL" in unified or symbol == "BTCUSDC":
            return "futures"
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
        """Send WebSocket ping frame or JSON ping every 20 seconds."""
        try:
            while self.running:
                await asyncio.sleep(20)
                await ws.send("ping")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f"Error sending OSL WS heartbeat: {e}")

    async def _subscribe_ws_streams(self, ws):
        """Subscribe to Binance-style streams for target symbols."""
        params = []
        for symbol in self.target_symbols:
            s = symbol.lower()
            params.extend([
                f"{s}@bookTicker",
                f"{s}@depth",
                f"{s}@trade",
                f"{s}@kline_1m"
            ])

        sub_payload = {
            "method": "SUBSCRIBE",
            "params": params,
            "id": 1
        }
        self.logger.info(f"Subscribing OSL WS streams for symbols: {self.target_symbols}")
        await ws.send(json.dumps(sub_payload))

    async def _handle_ws_message(self, raw_message: str):
        """Parse WebSocket message and persist to MarketDataWriter."""
        try:
            if raw_message == "pong":
                return

            msg = json.loads(raw_message)

            # Handle subscription ACK
            if "result" in msg and "id" in msg:
                self.logger.info(f"OSL WS subscription ACK: {msg}")
                return

            event_type = msg.get("eventType")
            param = msg.get("param", "")
            data = msg.get("data")

            # Extract symbol from param e.g. "btcusdc@depth" -> "BTCUSDC"
            if not param or "@" not in param:
                return

            symbol_raw = param.split("@")[0].upper()
            if symbol_raw not in self.target_symbols:
                return

            unified_symbol = self.to_unified_symbol(symbol_raw)
            market_type = self.get_market_type(symbol_raw)
            ts = msg.get("eventTime") or int(datetime.now(timezone.utc).timestamp() * 1000)

            if event_type in ("bookTicker", "ticker"):
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=unified_symbol,
                    market_type=market_type,
                    category="bbo",
                    record={
                        "timestamp": ts,
                        "raw": msg
                    }
                )
            elif event_type in ("depthUpdate", "depth"):
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=unified_symbol,
                    market_type=market_type,
                    category="depth",
                    record={
                        "timestamp": ts,
                        "raw": msg
                    }
                )
            elif event_type in ("trade", "trades"):
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=unified_symbol,
                    market_type=market_type,
                    category="trades",
                    record={
                        "timestamp": ts,
                        "raw": msg
                    }
                )
            elif event_type in ("kline", "kline_1m"):
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=unified_symbol,
                    market_type=market_type,
                    category="kline_1m",
                    record={
                        "timestamp": ts,
                        "raw": msg
                    }
                )

        except Exception as e:
            self.logger.error(f"Error handling OSL WS message: {e}", exc_info=True)

    async def _fetch_and_write_rest_orderbook(self, symbol: str):
        """Fetch depth from OSL REST API and write to storage."""
        depth_url = f"{self.rest_url}/openapi/v1/depth"
        params = {"symbol": symbol}
        headers = {"User-Agent": "Mozilla/5.0"}
        async with self.session.get(depth_url, params=params, headers=headers, timeout=5) as response:
            raw_data = await response.json(content_type=None)
            
            bids = [[float(p), float(q)] for p, q in raw_data.get("bids", [])]
            asks = [[float(p), float(q)] for p, q in raw_data.get("asks", [])]

            unified_symbol = self.to_unified_symbol(symbol)
            market_type = self.get_market_type(symbol)
            ts = raw_data.get("time")
            if ts is not None:
                ts = int(ts)
            else:
                ts = int(datetime.now(timezone.utc).timestamp() * 1000)

            await self.writer.write(
                exchange=self.exchange_name,
                symbol=unified_symbol,
                market_type=market_type,
                category="orderbook_rest",
                record={
                    "timestamp": ts,
                    "bids": bids,
                    "asks": asks,
                    "raw": raw_data
                }
            )