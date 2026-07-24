import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from collectors.base import BaseExchangeCollector
from writer import MarketDataWriter

# Default configurations
GATE_USDT_WS_URL = "wss://fx-ws.gateio.ws/v4/ws/usdt"
GATE_BTC_WS_URL = "wss://fx-ws.gateio.ws/v4/ws/btc"
GATE_REST_URL = "https://fx-api.gateio.ws/api/v4"


class GateCollector(BaseExchangeCollector):
    exchange_name: str = "gate"

    # Map unified symbols to Gate.io symbols
    UNIFIED_TO_EXCHANGE = {
        "BTCUSDT-PERPETUAL": "BTC_USDT",
        "ETHUSDT-PERPETUAL": "ETH_USDT",
        "BTCUSD-PERPETUAL": "BTC_USD"
    }
    EXCHANGE_TO_UNIFIED = {v: k for k, v in UNIFIED_TO_EXCHANGE.items()}

    def __init__(
        self,
        writer: MarketDataWriter,
        target_symbols: List[str],
        rest_rate_limit_rps: float = 2.0,
        rest_poll_interval_ms: int = 200,
        usdt_ws_url: str = GATE_USDT_WS_URL,
        btc_ws_url: str = GATE_BTC_WS_URL,
        rest_url: str = GATE_REST_URL
    ):
        self.mapped_symbols = [self.UNIFIED_TO_EXCHANGE[s] for s in target_symbols if s in self.UNIFIED_TO_EXCHANGE]
        super().__init__(writer, self.mapped_symbols, rest_rate_limit_rps, rest_poll_interval_ms)
        self.usdt_ws_url = usdt_ws_url
        self.btc_ws_url = btc_ws_url
        self.rest_url = rest_url

    def to_unified_symbol(self, exchange_symbol: str) -> str:
        """Convert exchange symbol back to unified symbol."""
        return self.EXCHANGE_TO_UNIFIED.get(exchange_symbol, exchange_symbol)

    def get_settle(self, symbol: str) -> str:
        """Determine settlement currency for REST / WS routing."""
        return "btc" if symbol == "BTC_USD" else "usdt"

    def _start_ws_tasks(self) -> List[asyncio.Task]:
        """Start separate WebSocket loops for USDT and BTC settled futures."""
        tasks = []
        
        # Split symbols by settlement
        usdt_symbols = [s for s in self.target_symbols if self.get_settle(s) == "usdt"]
        btc_symbols = [s for s in self.target_symbols if self.get_settle(s) == "btc"]

        if usdt_symbols:
            tasks.append(
                asyncio.create_task(
                    self._run_ws_loop(
                        ws_url=self.usdt_ws_url,
                        subscribe_func=lambda ws: self._subscribe_ws_streams(ws, usdt_symbols),
                        heartbeat_func=self._run_ws_heartbeat,
                        message_handler_func=self._handle_ws_message
                    )
                )
            )

        if btc_symbols:
            tasks.append(
                asyncio.create_task(
                    self._run_ws_loop(
                        ws_url=self.btc_ws_url,
                        subscribe_func=lambda ws: self._subscribe_ws_streams(ws, btc_symbols),
                        heartbeat_func=self._run_ws_heartbeat,
                        message_handler_func=self._handle_ws_message
                    )
                )
            )

        return tasks

    async def _run_ws_heartbeat(self, ws):
        """Periodic heartbeat sender required by Gate.io."""
        try:
            while self.running:
                await asyncio.sleep(25)
                ping_payload = {"time": int(datetime.now(timezone.utc).timestamp()), "channel": "futures.ping"}
                await ws.send(json.dumps(ping_payload))
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f"Error sending Gate.io WS heartbeat: {e}")

    async def _subscribe_ws_streams(self, ws, symbols: List[str]):
        """Send subscription payloads for target symbols."""
        for symbol in symbols:
            # Subscribe to 4 required public data streams
            subscriptions = [
                {
                    "time": int(datetime.now(timezone.utc).timestamp()),
                    "channel": "futures.candlesticks",
                    "event": "subscribe",
                    "payload": ["1m", symbol]
                },
                {
                    "time": int(datetime.now(timezone.utc).timestamp()),
                    "channel": "futures.trades",
                    "event": "subscribe",
                    "payload": [symbol]
                },
                {
                    "time": int(datetime.now(timezone.utc).timestamp()),
                    "channel": "futures.order_book",
                    "event": "subscribe",
                    "payload": [symbol, "20", "0"]  # up to 20 levels, 0 update interval (realtime)
                },
                {
                    "time": int(datetime.now(timezone.utc).timestamp()),
                    "channel": "futures.book_ticker",
                    "event": "subscribe",
                    "payload": [symbol]
                }
            ]
            for sub in subscriptions:
                self.logger.debug(f"Subscribing: {sub}")
                await ws.send(json.dumps(sub))

    def _parse_bids_asks(self, bids_or_asks_list: Any) -> List[List[float]]:
        """Helper to robustly parse lists of bids or asks from Gate.io."""
        parsed = []
        if not bids_or_asks_list:
            return parsed
        for item in bids_or_asks_list:
            try:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    parsed.append([float(item[0]), float(item[1])])
                elif isinstance(item, dict):
                    # Gate.io WebSocket orderbook format: {"p": "...", "s": ...}
                    p = item.get("p") or item.get("price")
                    s = item.get("s") or item.get("size") or item.get("quantity")
                    if p is not None and s is not None:
                        parsed.append([float(p), float(s)])
            except (ValueError, TypeError) as e:
                self.logger.warning(f"Error parsing Gate.io orderbook item {item}: {e}")
        return parsed

    async def _handle_ws_message(self, raw_message: str):
        """Parse, normalize, and write WebSocket payloads."""
        try:
            msg = json.loads(raw_message)
            
            channel = msg.get("channel")
            event = msg.get("event")
            
            # Silently handle ping/pong response or subscription feedback
            if channel == "futures.pong" or event == "pong":
                return
            if event == "subscribe":
                self.logger.info(f"Gate.io WS Subscribed successfully: {msg}")
                return

            result = msg.get("result")
            if not channel or not result:
                return

            # 1. Handle Klines (futures.candlesticks)
            if channel == "futures.candlesticks":
                items = result if isinstance(result, list) else [result]
                for candle in items:
                    exchange_symbol = candle.get("n") or candle.get("s") or candle.get("contract")
                    if not exchange_symbol:
                        continue
                    
                    # Candlestick channel symbol is in format "1m_ETH_USDT", we need to strip the interval prefix
                    if "_" in exchange_symbol:
                        parts = exchange_symbol.split("_", 1)
                        if len(parts) > 1 and parts[0] in ["1s", "10s", "1m", "5m", "15m", "30m", "1h", "4h", "1d"]:
                            exchange_symbol = parts[1]

                    unified_symbol = self.to_unified_symbol(exchange_symbol)
                    ts = int(candle.get("t", 0)) * 1000
                    await self.writer.write(
                        exchange=self.exchange_name,
                        symbol=unified_symbol,
                        market_type="futures",
                        category="kline_1m",
                        record={
                            "timestamp": ts,
                            "open_time": ts,
                            "close_time": ts + 59999,
                            "open": float(candle.get("o", 0.0)),
                            "high": float(candle.get("h", 0.0)),
                            "low": float(candle.get("l", 0.0)),
                            "close": float(candle.get("c", 0.0)),
                            "volume": float(candle.get("v", 0.0)),
                            "raw": msg
                        }
                    )

            # 2. Handle Trades (futures.trades)
            elif channel == "futures.trades":
                items = result if isinstance(result, list) else [result]
                for trade in items:
                    exchange_symbol = trade.get("contract") or trade.get("s") or trade.get("n")
                    if not exchange_symbol:
                        continue
                    unified_symbol = self.to_unified_symbol(exchange_symbol)
                    ts = int(trade.get("create_time_ms") or (trade.get("create_time", 0) * 1000))
                    
                    # Gate size sign indicates trade direction:
                    # Positive size is buy (taker buys); Negative is sell (taker sells)
                    size = float(trade.get("size", 0.0))
                    side = "buy" if size > 0 else "sell"
                    qty = abs(size)

                    await self.writer.write(
                        exchange=self.exchange_name,
                        symbol=unified_symbol,
                        market_type="futures",
                        category="trades",
                        record={
                            "timestamp": ts,
                            "price": float(trade.get("price", 0.0)),
                            "quantity": qty,
                            "side": side,
                            "trade_id": str(trade.get("id")),
                            "raw": msg
                        }
                    )

            # 3. Handle Depth (futures.order_book)
            elif channel == "futures.order_book":
                exchange_symbol = result.get("contract") or result.get("s") or result.get("n")
                if not exchange_symbol:
                    return
                unified_symbol = self.to_unified_symbol(exchange_symbol)
                ts = result.get("t") or int(msg.get("time_ms", 0))
                
                bids = self._parse_bids_asks(result.get("bids", []))
                asks = self._parse_bids_asks(result.get("asks", []))
                
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=unified_symbol,
                    market_type="futures",
                    category="depth",
                    record={
                        "timestamp": ts,
                        "bids": bids,
                        "asks": asks,
                        "version": str(result.get("id") or ""),
                        "raw": msg
                    }
                )

            # 4. Handle BBO (futures.book_ticker)
            elif channel == "futures.book_ticker":
                exchange_symbol = result.get("contract") or result.get("s") or result.get("n")
                if not exchange_symbol:
                    return
                unified_symbol = self.to_unified_symbol(exchange_symbol)
                ts = result.get("t") or int(msg.get("time_ms", 0))
                
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=unified_symbol,
                    market_type="futures",
                    category="bbo",
                    record={
                        "timestamp": ts,
                        "bid_price": float(result.get("b", 0.0)),
                        "bid_quantity": float(result.get("B", 0.0)),
                        "ask_price": float(result.get("a", 0.0)),
                        "ask_quantity": float(result.get("A", 0.0)),
                        "version": str(result.get("t")),
                        "raw": msg
                    }
                )

        except Exception as e:
            self.logger.error(f"Error parsing Gate.io WS message: {e}", exc_info=True)

    async def _fetch_and_write_rest_orderbook(self, symbol: str):
        """Fetch depth from Gate.io REST API and write to storage."""
        settle = self.get_settle(symbol)
        unified_symbol = self.to_unified_symbol(symbol)
        
        # Endpoint: GET /futures/{settle}/order_book
        depth_url = f"{self.rest_url}/futures/{settle}/order_book"
        params = {
            "contract": symbol,
            "limit": "20"
        }

        async with self.session.get(depth_url, params=params, timeout=5) as response:
            raw_data = await response.json()
            
            bids = self._parse_bids_asks(raw_data.get("bids", []))
            asks = self._parse_bids_asks(raw_data.get("asks", []))
            # Gate.io REST returns current server timestamp in response header 'current-time'
            # or we use the local time as fallback
            ts_sec = float(response.headers.get("current-time", datetime.now(timezone.utc).timestamp()))
            ts = int(ts_sec * 1000)

            await self.writer.write(
                exchange=self.exchange_name,
                symbol=unified_symbol,
                market_type="futures",
                category="orderbook_rest",
                record={
                    "timestamp": ts,
                    "bids": bids,
                    "asks": asks,
                    "raw": raw_data
                }
            )
