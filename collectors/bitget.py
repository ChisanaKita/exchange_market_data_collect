"""Bitget spot and perpetual collector.

One instance collects one market (`market="spot"` or `market="perp"`); main.py runs one of each, both writing
under exchange "bitget" with market_type "spot" or "futures". Perpetuals are routed by their native symbol
(ADR 0009):

- `..._CM` (e.g. `BTCUSD_CM`) is coin-margined. The v2 WebSocket no longer lists it, so it uses the v3 WebSocket.
- `...PERP` (e.g. `HYPEPERP`) is USDC-margined (USDC-FUTURES on the v2 WebSocket).
- anything else is USDT-margined (USDT-FUTURES on the v2 WebSocket).

REST depth for every market comes from the v3 orderbook endpoint.
"""
import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import partial
from typing import Any, Dict, List

from collectors.base import BaseExchangeCollector
from writer import MarketDataWriter

# Default configurations
BITGET_WS_URL = "wss://ws.bitget.com/v2/ws/public"
BITGET_V3_WS_URL = "wss://ws.bitget.com/v3/ws/public"
BITGET_REST_URL = "https://api.bitget.com"

SPOT = "spot"
PERP = "perp"

# Each symbol takes 4 channels; Bitget advises fewer than 50 channels per connection
WS_SYMBOLS_PER_CONNECTION = 12


@dataclass(frozen=True)
class BitgetRoute:
    ws_version: str  # "v2" or "v3"
    ws_inst_type: str  # instType sent in WebSocket subscriptions
    rest_category: str  # category for GET /api/v3/market/orderbook


def route_for(market: str, symbol: str) -> BitgetRoute:
    """Pick the WebSocket protocol, instType and REST category for a native Bitget symbol."""
    if market == SPOT:
        return BitgetRoute("v2", "SPOT", "SPOT")
    if symbol.endswith("_CM"):
        return BitgetRoute("v3", "coin-futures", "COIN-FUTURES")
    if symbol.endswith("PERP"):
        return BitgetRoute("v2", "USDC-FUTURES", "USDC-FUTURES")
    return BitgetRoute("v2", "USDT-FUTURES", "USDT-FUTURES")


def _chunks(items: List[str], size: int) -> List[List[str]]:
    return [items[i:i + size] for i in range(0, len(items), size)]


class BitgetCollector(BaseExchangeCollector):
    exchange_name: str = "bitget"

    def __init__(
        self,
        writer: MarketDataWriter,
        target_symbols: List[str],
        market: str,
        rest_rate_limit_rps: float = 5.0,
        rest_poll_interval_ms: int = 200,
        ws_url: str = BITGET_WS_URL,
        v3_ws_url: str = BITGET_V3_WS_URL,
        rest_url: str = BITGET_REST_URL
    ):
        if market not in (SPOT, PERP):
            raise ValueError(f"Bitget market must be '{SPOT}' or '{PERP}', got {market!r}")
        super().__init__(writer, target_symbols, rest_rate_limit_rps, rest_poll_interval_ms)
        self.market = market
        self.market_type = "spot" if market == SPOT else "futures"
        self.routes: Dict[str, BitgetRoute] = {symbol: route_for(market, symbol) for symbol in target_symbols}
        self.ws_url = ws_url
        self.v3_ws_url = v3_ws_url
        self.rest_url = rest_url
        # Must end with "Collector": alerts.py treats ERRORs from collector loggers as transient
        self.logger = logging.getLogger(f"Bitget{market.capitalize()}Collector")

    def get_market_type(self, symbol: str) -> str:
        return self.market_type

    # ------------------------------------------------------------------ WebSocket

    def _start_ws_tasks(self) -> List[asyncio.Task]:
        """Start one WebSocket loop per protocol and chunk of symbols."""
        tasks = []
        for version, url, subscribe, handler in (
            ("v2", self.ws_url, self._subscribe_v2, self._handle_ws_message),
            ("v3", self.v3_ws_url, self._subscribe_v3, self._handle_v3_ws_message),
        ):
            symbols = [symbol for symbol, route in self.routes.items() if route.ws_version == version]
            for chunk in _chunks(symbols, WS_SYMBOLS_PER_CONNECTION):
                tasks.append(
                    asyncio.create_task(
                        self._run_ws_loop(
                            ws_url=url,
                            subscribe_func=partial(subscribe, chunk),
                            heartbeat_func=self._run_ws_heartbeat,
                            message_handler_func=handler
                        )
                    )
                )
        return tasks

    async def _run_ws_heartbeat(self, ws):
        """Periodic text ping required by Bitget (v2 and v3 both answer "pong")."""
        try:
            while self.running:
                await asyncio.sleep(25)
                await ws.send("ping")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f"Error sending Bitget WS heartbeat: {e!r}")

    async def _subscribe_v2(self, symbols: List[str], ws):
        args = []
        for symbol in symbols:
            inst_type = self.routes[symbol].ws_inst_type
            args.extend([
                {"instType": inst_type, "channel": "candle1m", "instId": symbol},
                {"instType": inst_type, "channel": "trade", "instId": symbol},
                {"instType": inst_type, "channel": "books", "instId": symbol},
                {"instType": inst_type, "channel": "books1", "instId": symbol}
            ])
        self.logger.info(f"Subscribing to Bitget v2 WS: {len(args)} channels")
        await ws.send(json.dumps({"op": "subscribe", "args": args}))

    async def _subscribe_v3(self, symbols: List[str], ws):
        args = []
        for symbol in symbols:
            inst_type = self.routes[symbol].ws_inst_type
            args.extend([
                {"instType": inst_type, "topic": "kline", "symbol": symbol, "interval": "1m"},
                {"instType": inst_type, "topic": "publicTrade", "symbol": symbol},
                {"instType": inst_type, "topic": "books", "symbol": symbol},
                {"instType": inst_type, "topic": "books1", "symbol": symbol}
            ])
        self.logger.info(f"Subscribing to Bitget v3 WS: {len(args)} channels")
        await ws.send(json.dumps({"op": "subscribe", "args": args}))

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

    def _control_message(self, raw_message: str):
        """Return the decoded message, or None for pong frames and subscribe/error events (logged here)."""
        if raw_message in ("pong", "ping"):
            return None
        msg = json.loads(raw_message)
        if msg.get("event") == "subscribe":
            self.logger.info(f"Bitget subscribed successfully to channel: {msg.get('arg')}")
            return None
        if msg.get("event") == "error":
            self.logger.error(f"Bitget WS error message: {msg}")
            return None
        if not msg.get("arg") or not msg.get("data"):
            return None
        return msg

    async def _handle_ws_message(self, raw_message: str):
        """Parse and write a v2 WebSocket payload."""
        try:
            msg = self._control_message(raw_message)
            if msg is None:
                return
            channel = msg["arg"].get("channel")
            symbol = msg["arg"].get("instId")
            data = msg["data"]
            push_ts = msg.get("ts") or int(datetime.now(timezone.utc).timestamp() * 1000)

            if channel == "candle1m":
                # [start, open, high, low, close, base volume, quote volume, USDT volume]
                for candle in data:
                    await self._write_kline(symbol, int(candle[0]), candle[1], candle[2], candle[3], candle[4],
                                            candle[5], msg)
            elif channel == "trade":
                for trade in data:
                    await self._write_trade(symbol, int(trade.get("ts")), trade.get("price", 0.0),
                                            trade.get("size", 0.0), trade.get("side", "sell"),
                                            trade.get("tradeId"), msg)
            elif channel == "books":
                for depth in data:
                    await self._write_depth(symbol, int(depth.get("ts") or push_ts), depth.get("bids", []),
                                            depth.get("asks", []), depth.get("seq"), msg)
            elif channel == "books1":
                for bbo in data:
                    await self._write_bbo(symbol, int(bbo.get("ts") or push_ts), bbo.get("bids", []),
                                          bbo.get("asks", []), bbo.get("seq"), msg)
        except Exception as e:
            self.logger.error(f"Error parsing Bitget WS message: {e}", exc_info=True)

    async def _handle_v3_ws_message(self, raw_message: str):
        """Parse and write a v3 WebSocket payload (short field names, `topic`/`symbol` in `arg`)."""
        try:
            msg = self._control_message(raw_message)
            if msg is None:
                return
            topic = msg["arg"].get("topic")
            symbol = msg["arg"].get("symbol")
            data = msg["data"]
            push_ts = msg.get("ts") or int(datetime.now(timezone.utc).timestamp() * 1000)

            if topic == "kline":
                # {"start", "open", "close", "high", "low", "volume", "turnover"}
                for candle in data:
                    await self._write_kline(symbol, int(candle["start"]), candle["open"], candle["high"],
                                            candle["low"], candle["close"], candle["volume"], msg)
            elif topic == "publicTrade":
                # {"i": trade id, "p": price, "v": size, "S": side, "T": trade time}
                for trade in data:
                    await self._write_trade(symbol, int(trade.get("T") or push_ts), trade.get("p", 0.0),
                                            trade.get("v", 0.0), trade.get("S", "sell"), trade.get("i"), msg)
            elif topic == "books":
                for depth in data:
                    await self._write_depth(symbol, int(depth.get("ts") or push_ts), depth.get("b", []),
                                            depth.get("a", []), depth.get("seq"), msg)
            elif topic == "books1":
                for bbo in data:
                    await self._write_bbo(symbol, int(bbo.get("ts") or push_ts), bbo.get("b", []),
                                          bbo.get("a", []), bbo.get("seq"), msg)
        except Exception as e:
            self.logger.error(f"Error parsing Bitget v3 WS message: {e}", exc_info=True)

    async def _write_kline(self, symbol, open_time, open_, high, low, close, volume, msg):
        await self.writer.write(
            exchange=self.exchange_name,
            symbol=symbol,
            market_type=self.market_type,
            category="kline_1m",
            record={
                "timestamp": open_time,
                "open_time": open_time,
                "close_time": open_time + 59999,
                "open": float(open_),
                "high": float(high),
                "low": float(low),
                "close": float(close),
                "volume": float(volume),
                "raw": msg
            }
        )

    async def _write_trade(self, symbol, ts, price, quantity, side, trade_id, msg):
        await self.writer.write(
            exchange=self.exchange_name,
            symbol=symbol,
            market_type=self.market_type,
            category="trades",
            record={
                "timestamp": ts,
                "price": float(price),
                "quantity": float(quantity),
                "side": side,
                "trade_id": str(trade_id),
                "raw": msg
            }
        )

    async def _write_depth(self, symbol, ts, bids, asks, seq, msg):
        await self.writer.write(
            exchange=self.exchange_name,
            symbol=symbol,
            market_type=self.market_type,
            category="depth",
            record={
                "timestamp": ts,
                "bids": self._parse_bids_asks(bids),
                "asks": self._parse_bids_asks(asks),
                "version": str(seq or ""),
                "raw": msg
            }
        )

    async def _write_bbo(self, symbol, ts, bids, asks, seq, msg):
        bid = bids[0] if bids and len(bids[0]) >= 2 else (0.0, 0.0)
        ask = asks[0] if asks and len(asks[0]) >= 2 else (0.0, 0.0)
        await self.writer.write(
            exchange=self.exchange_name,
            symbol=symbol,
            market_type=self.market_type,
            category="bbo",
            record={
                "timestamp": ts,
                "bid_price": float(bid[0]),
                "bid_quantity": float(bid[1]),
                "ask_price": float(ask[0]),
                "ask_quantity": float(ask[1]),
                "version": str(seq or ""),
                "raw": msg
            }
        )

    # ------------------------------------------------------------------ REST

    async def _fetch_and_write_rest(self, symbol: str):
        """Fetch depth from Bitget REST API and write to storage."""
        # Endpoint: GET /api/v3/market/orderbook (20 req/s/IP)
        depth_url = f"{self.rest_url}/api/v3/market/orderbook"
        params = {
            "category": self.routes[symbol].rest_category,
            "symbol": symbol,
            "limit": "20"
        }

        async with self.session.get(depth_url, params=params, timeout=5) as response:
            raw_data = await response.json(content_type=None)

        # Bitget REST API V3 structure (asks under "a", bids under "b", both ascending/descending by price):
        # {"code":"00000","msg":"success","requestTime":...,"data":{"a":[[price,size],...],"b":[[price,size],...],"ts":"..."}}
        # Errors carry a non-"00000" code (e.g. 25100 "Trading pair ... does not exist") and `data: null`.
        if raw_data.get("code") != "00000":
            raise ValueError(f"Bitget orderbook request for {symbol} failed: {raw_data}")

        data = raw_data.get("data") or {}
        bids = self._parse_bids_asks(data.get("b", []))
        asks = self._parse_bids_asks(data.get("a", []))
        ts = int(data.get("ts") or int(datetime.now(timezone.utc).timestamp() * 1000))

        await self.writer.write(
            exchange=self.exchange_name,
            symbol=symbol,
            market_type=self.market_type,
            category="orderbook_rest",
            record={
                "timestamp": ts,
                "bids": bids,
                "asks": asks,
                "raw": raw_data
            }
        )
