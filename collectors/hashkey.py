import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import List

from collectors.base import BaseExchangeCollector
from writer import MarketDataWriter

# Default configurations if not overridden in constructor
HASHKEY_WS_URL = "wss://stream-glb.hashkey.com/quote/ws/v2"
HASHKEY_REST_URL = "https://api-glb.hashkey.com"


class HashkeyCollector(BaseExchangeCollector):
    exchange_name: str = "hashkey"

    UNIFIED_TO_EXCHANGE = {
        "BTCUSDT-PERPETUAL": "BTCUSDT-PERPETUAL",
        "ETHUSDT-PERPETUAL": "ETHUSDT-PERPETUAL",
        "BTCUSD-PERPETUAL": "BTCUSD-PERPETUAL"
    }

    def __init__(
        self,
        writer: MarketDataWriter,
        target_symbols: List[str],
        rest_rate_limit_rps: float = 1.5,
        rest_poll_interval_ms: int = 200,
        ws_url: str = HASHKEY_WS_URL,
        rest_url: str = HASHKEY_REST_URL
    ):
        self.mapped_symbols = [self.UNIFIED_TO_EXCHANGE[s] for s in target_symbols if s in self.UNIFIED_TO_EXCHANGE]
        super().__init__(writer, self.mapped_symbols, rest_rate_limit_rps, rest_poll_interval_ms)
        self.ws_url = ws_url
        self.rest_url = rest_url

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
        """Periodic heartbeat sender required by Hashkey Global."""
        try:
            while self.running:
                await asyncio.sleep(10)
                ping_payload = {"ping": int(datetime.now(timezone.utc).timestamp() * 1000)}
                await ws.send(json.dumps(ping_payload))
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f"Error sending Hashkey WS heartbeat: {e}")

    async def _subscribe_ws_streams(self, ws):
        """Send subscription payloads for target symbols."""
        for symbol in self.target_symbols:
            subscriptions = [
                {"topic": "kline", "event": "sub", "params": {"symbol": symbol, "klineType": "1m"}},
                {"topic": "trade", "event": "sub", "params": {"symbol": symbol}},
                {"topic": "depth", "event": "sub", "params": {"symbol": symbol}},
                {"topic": "bbo", "event": "sub", "params": {"symbol": symbol}}
            ]
            for sub in subscriptions:
                self.logger.debug(f"Subscribing: {sub}")
                await ws.send(json.dumps(sub))

    async def _handle_ws_message(self, raw_message: str):
        """Parse, normalize, and write WebSocket payloads."""
        try:
            msg = json.loads(raw_message)
            
            # Handle pong replies silently
            if "pong" in msg:
                return

            # Check for error or confirmation codes
            if "code" in msg:
                code = msg.get("code")
                if code == "0":
                    self.logger.info(f"Subscription success: {msg.get('topic')} -> {msg.get('params', {})}")
                else:
                    self.logger.error(f"WS subscription failure: {msg}")
                return

            topic = msg.get("topic")
            data = msg.get("data")
            if not topic or not data:
                return

            symbol = msg.get("params", {}).get("symbol") or data.get("s")
            if not symbol or symbol not in self.target_symbols:
                return

            # 1. Handle Klines
            if topic == "kline":
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=symbol,
                    market_type="futures",
                    category="kline_1m",
                    record={
                        "timestamp": data.get("t"),
                        "open_time": data.get("t"),
                        "close_time": data.get("t") + 59999 if data.get("t") else None,
                        "open": float(data.get("o", 0.0)),
                        "high": float(data.get("h", 0.0)),
                        "low": float(data.get("l", 0.0)),
                        "close": float(data.get("c", 0.0)),
                        "volume": float(data.get("v", 0.0)),
                        "raw": msg
                    }
                )

            # 2. Handle Trades
            elif topic == "trade":
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=symbol,
                    market_type="futures",
                    category="trades",
                    record={
                        "timestamp": data.get("t"),
                        "price": float(data.get("p", 0.0)),
                        "quantity": float(data.get("q", 0.0)),
                        "side": "sell" if data.get("m") else "buy",
                        "trade_id": str(data.get("v")),
                        "raw": msg
                    }
                )

            # 3. Handle Depth
            elif topic == "depth":
                bids = [[float(p), float(q)] for p, q in data.get("b", [])]
                asks = [[float(p), float(q)] for p, q in data.get("a", [])]
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=symbol,
                    market_type="futures",
                    category="depth",
                    record={
                        "timestamp": data.get("t"),
                        "bids": bids,
                        "asks": asks,
                        "version": data.get("v"),
                        "raw": msg
                    }
                )

            # 4. Handle BBO
            elif topic == "bbo":
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=symbol,
                    market_type="futures",
                    category="bbo",
                    record={
                        "timestamp": data.get("t"),
                        "bid_price": float(data.get("b", 0.0)) if data.get("b") else 0.0,
                        "bid_quantity": float(data.get("bz", 0.0)) if data.get("bz") else 0.0,
                        "ask_price": float(data.get("a", 0.0)) if data.get("a") else 0.0,
                        "ask_quantity": float(data.get("az", 0.0)) if data.get("az") else 0.0,
                        "version": data.get("v"),
                        "raw": msg
                    }
                )

        except Exception as e:
            self.logger.error(f"Error parsing WS message: {e}", exc_info=True)

    async def _fetch_and_write_rest_orderbook(self, symbol: str):
        """Fetch depth from REST API and write to storage."""
        depth_url = f"{self.rest_url}/quote/v1/depth"
        params = {"symbol": symbol, "limit": "20"}
        async with self.session.get(depth_url, params=params, timeout=5) as response:
            raw_data = await response.json()
            
            bids = [[float(p), float(q)] for p, q in raw_data.get("b", [])]
            asks = [[float(p), float(q)] for p, q in raw_data.get("a", [])]

            await self.writer.write(
                exchange=self.exchange_name,
                symbol=symbol,
                market_type="futures",
                category="orderbook_rest",
                record={
                    "timestamp": raw_data.get("t"),
                    "bids": bids,
                    "asks": asks,
                    "raw": raw_data
                }
            )
