import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from collectors.base import BaseExchangeCollector
from writer import MarketDataWriter

# Default configurations
BITGET_WS_URL = "wss://ws.bitget.com/v2/ws/public"
BITGET_REST_URL = "https://api.bitget.com"


class BitgetCollector(BaseExchangeCollector):
    exchange_name: str = "bitget"

    # Map unified symbols to Bitget symbols
    UNIFIED_TO_EXCHANGE = {
        "BTCUSDT-PERPETUAL": "BTCUSDT",
        "ETHUSDT-PERPETUAL": "ETHUSDT",
        "BTCUSD-PERPETUAL": "BTCUSD"
    }
    EXCHANGE_TO_UNIFIED = {v: k for k, v in UNIFIED_TO_EXCHANGE.items()}

    def __init__(
        self,
        writer: MarketDataWriter,
        target_symbols: List[str],
        rest_rate_limit_rps: float = 2.0,
        rest_poll_interval_ms: int = 200,
        ws_url: str = BITGET_WS_URL,
        rest_url: str = BITGET_REST_URL
    ):
        self.mapped_symbols = [self.UNIFIED_TO_EXCHANGE[s] for s in target_symbols if s in self.UNIFIED_TO_EXCHANGE]
        super().__init__(writer, self.mapped_symbols, rest_rate_limit_rps, rest_poll_interval_ms)
        self.ws_url = ws_url
        self.rest_url = rest_url

    def to_unified_symbol(self, exchange_symbol: str) -> str:
        """Convert exchange symbol back to unified symbol."""
        return self.EXCHANGE_TO_UNIFIED.get(exchange_symbol, exchange_symbol)

    def get_inst_type(self, symbol: str) -> str:
        """Determine Bitget instType for WebSocket."""
        return "COIN-FUTURES" if symbol == "BTCUSD" else "USDT-FUTURES"

    def get_product_type(self, symbol: str) -> str:
        """Determine Bitget productType for REST."""
        return "coin-futures" if symbol == "BTCUSD" else "usdt-futures"

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
        """Periodic heartbeat sender required by Bitget."""
        try:
            while self.running:
                await asyncio.sleep(25)
                await ws.send("ping")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f"Error sending Bitget WS heartbeat: {e}")

    async def _subscribe_ws_streams(self, ws):
        """Send subscription payloads for target symbols."""
        args = []
        for symbol in self.target_symbols:
            inst_type = self.get_inst_type(symbol)
            args.extend([
                {"instType": inst_type, "channel": "candle1m", "instId": symbol},
                {"instType": inst_type, "channel": "trade", "instId": symbol},
                {"instType": inst_type, "channel": "books", "instId": symbol},
                {"instType": inst_type, "channel": "books1", "instId": symbol}
            ])
        
        # Batch subscription
        sub_payload = {
            "op": "subscribe",
            "args": args
        }
        self.logger.info(f"Subscribing to Bitget WS: {len(args)} channels")
        await ws.send(json.dumps(sub_payload))

    def _parse_bids_asks(self, bids_or_asks_list: Any) -> List[List[float]]:
        """Helper to robustly parse lists of bids or asks."""
        parsed = []
        if not bids_or_asks_list:
            return parsed
        for item in bids_or_asks_list:
            try:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    parsed.append([float(item[0]), float(item[1])])
            except (ValueError, TypeError) as e:
                self.logger.warning(f"Error parsing Bitget orderbook item {item}: {e}")
        return parsed

    async def _handle_ws_message(self, raw_message: str):
        """Parse, normalize, and write WebSocket payloads."""
        try:
            # Handle text ping/pong frames
            if raw_message == "pong" or raw_message == "ping":
                return

            msg = json.loads(raw_message)
            
            # Check for subscription confirmation
            if msg.get("event") == "subscribe":
                self.logger.info(f"Bitget subscribed successfully to channels: {msg.get('arg')}")
                return
            if msg.get("event") == "error":
                self.logger.error(f"Bitget WS error message: {msg}")
                return

            arg = msg.get("arg")
            data = msg.get("data")
            if not arg or not data:
                return

            channel = arg.get("channel")
            exchange_symbol = arg.get("instId")
            unified_symbol = self.to_unified_symbol(exchange_symbol)
            push_ts = msg.get("ts") or int(datetime.now(timezone.utc).timestamp() * 1000)

            # 1. Handle Klines (candle1m)
            if channel == "candle1m":
                for candle in data:
                    # Format: [ts, open, high, low, close, volume, quote_volume, close_time]
                    ts = int(candle[0])
                    await self.writer.write(
                        exchange=self.exchange_name,
                        symbol=unified_symbol,
                        market_type="futures",
                        category="kline_1m",
                        record={
                            "timestamp": ts,
                            "open_time": ts,
                            "close_time": int(float(candle[7])) if len(candle) >= 8 else ts + 59999,
                            "open": float(candle[1]),
                            "high": float(candle[2]),
                            "low": float(candle[3]),
                            "close": float(candle[4]),
                            "volume": float(candle[5]),
                            "raw": msg
                        }
                    )

            # 2. Handle Trades (trade)
            elif channel == "trade":
                for trade in data:
                    # Format: {"ts": "...", "price": "...", "size": "...", "side": "buy/sell", "tradeId": "..."}
                    ts = int(trade.get("ts"))
                    await self.writer.write(
                        exchange=self.exchange_name,
                        symbol=unified_symbol,
                        market_type="futures",
                        category="trades",
                        record={
                            "timestamp": ts,
                            "price": float(trade.get("price", 0.0)),
                            "quantity": float(trade.get("size", 0.0)),
                            "side": trade.get("side", "sell"),
                            "trade_id": str(trade.get("tradeId")),
                            "raw": msg
                        }
                    )

            # 3. Handle Depth (books)
            elif channel == "books":
                for depth in data:
                    bids = self._parse_bids_asks(depth.get("bids", []))
                    asks = self._parse_bids_asks(depth.get("asks", []))
                    ts = int(depth.get("ts") or push_ts)
                    await self.writer.write(
                        exchange=self.exchange_name,
                        symbol=unified_symbol,
                        market_type="futures",
                        category="depth",
                        record={
                            "timestamp": ts,
                            "bids": bids,
                            "asks": asks,
                            "version": str(depth.get("seqNum") or ""),
                            "raw": msg
                        }
                    )

            # 4. Handle BBO (books1)
            elif channel == "books1":
                for bbo in data:
                    bids = bbo.get("bids", [])
                    asks = bbo.get("asks", [])
                    
                    bid_p = float(bids[0][0]) if bids and len(bids[0]) >= 2 else 0.0
                    bid_q = float(bids[0][1]) if bids and len(bids[0]) >= 2 else 0.0
                    ask_p = float(asks[0][0]) if asks and len(asks[0]) >= 2 else 0.0
                    ask_q = float(asks[0][1]) if asks and len(asks[0]) >= 2 else 0.0

                    ts = int(bbo.get("ts") or push_ts)
                    await self.writer.write(
                        exchange=self.exchange_name,
                        symbol=unified_symbol,
                        market_type="futures",
                        category="bbo",
                        record={
                            "timestamp": ts,
                            "bid_price": bid_p,
                            "bid_quantity": bid_q,
                            "ask_price": ask_p,
                            "ask_quantity": ask_q,
                            "version": str(bbo.get("seqNum") or ""),
                            "raw": msg
                        }
                    )

        except Exception as e:
            self.logger.error(f"Error parsing Bitget WS message: {e}", exc_info=True)

    async def _fetch_and_write_rest_orderbook(self, symbol: str):
        """Fetch depth from Bitget REST API and write to storage."""
        # Endpoint: GET /api/v2/mix/market/depth
        depth_url = f"{self.rest_url}/api/v2/mix/market/depth"
        product_type = self.get_product_type(symbol)
        unified_symbol = self.to_unified_symbol(symbol)

        params = {
            "symbol": symbol,
            "productType": product_type,
            "limit": "20"
        }

        async with self.session.get(depth_url, params=params, timeout=5) as response:
            raw_data = await response.json()
            
            # Bitget REST API V2 structure:
            # {"code":"00000","msg":"success","requestTime":...,"data":{"bids":[...],"asks":[...],"ts":"...","seqNum":...}}
            data = raw_data.get("data") or {}
            bids = self._parse_bids_asks(data.get("bids", []))
            asks = self._parse_bids_asks(data.get("asks", []))
            ts = int(data.get("ts") or int(datetime.now(timezone.utc).timestamp() * 1000))

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
