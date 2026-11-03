import asyncio
import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from collectors.base import BaseExchangeCollector
from writer import MarketDataWriter

# PantherTrade production endpoints. UAT uses web-api-uat / ws-api-uat.panthertrade.com with separate credentials.
PANTHER_WS_URL = "wss://ws-api.panthertrade.com/v1"
PANTHER_REST_URL = "https://web-api.panthertrade.com"

PANTHER_BOOK_DEPTH = 20  # maximum depth the book channel and REST orderbook offer
PANTHER_KLINE_INTERVAL = "1m"
PANTHER_KLINE_LOOKBACK_MINUTES = 3  # re-request recent closed candles so a late one is picked up next minute
PANTHER_HEARTBEAT_SECONDS = 30  # doc suggests 30-45s; the server drops connections idle for 60s
PANTHER_LOGIN_TIMEOUT_SECONDS = 10  # the server closes unauthenticated connections after 10s
PANTHER_LOGIN_FAILURE_PAUSE_SECONDS = 30  # avoid hammering the handshake limit (3/s/IP) with bad credentials


def _to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _now_ms() -> int:
    return int(time.time() * 1000)


def sign_message(message: str, api_secret: str) -> str:
    """HMAC-SHA256 over `message` with the API secret, base64 encoded (REST and WebSocket login)."""
    digest = hmac.new(api_secret.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def _level_parts(level: Any) -> tuple:
    """Return (price, quantity) from a level that is either {"price", "qty"/"quantity"/"size"} or [price, qty]."""
    if isinstance(level, dict):
        qty = level.get("qty", level.get("quantity", level.get("size")))
        return level.get("price"), qty
    if isinstance(level, (list, tuple)) and len(level) >= 2:
        return level[0], level[1]
    return None, None


def _parse_levels(levels: Any) -> List[List[float]]:
    parsed = []
    for level in levels or []:
        price, qty = _level_parts(level)
        if price is not None and qty is not None:
            parsed.append([_to_float(price), _to_float(qty)])
    return parsed


class LocalBook:
    """One symbol's order book rebuilt from the `book` channel snapshot + incremental updates.

    Prices are kept as the server's strings so equal prices always collide on the same key.
    """

    def __init__(self):
        self.bids: Dict[str, str] = {}
        self.asks: Dict[str, str] = {}
        self.seq_id: Optional[int] = None

    @staticmethod
    def _apply(side: Dict[str, str], levels: Any):
        for level in levels or []:
            price, qty = _level_parts(level)
            if price is None or qty is None:
                continue
            if _to_float(qty) == 0.0:
                side.pop(str(price), None)
            else:
                side[str(price)] = str(qty)

    def apply_snapshot(self, data: Dict[str, Any]):
        self.bids.clear()
        self.asks.clear()
        self._apply(self.bids, data.get("bids"))
        self._apply(self.asks, data.get("asks"))
        self.seq_id = _seq(data.get("seq_id"))

    def apply_update(self, data: Dict[str, Any]) -> bool:
        """Apply a delta. Returns False (and leaves the book untouched) when the sequence chain is broken."""
        prev = _seq(data.get("prev_seq_id", data.get("pre_seq_id")))
        if self.seq_id is None or prev != self.seq_id:
            return False
        self._apply(self.bids, data.get("bids"))
        self._apply(self.asks, data.get("asks"))
        self.seq_id = _seq(data.get("seq_id"))
        return True

    def top(self, depth: int = PANTHER_BOOK_DEPTH):
        bids = sorted(self.bids.items(), key=lambda kv: float(kv[0]), reverse=True)[:depth]
        asks = sorted(self.asks.items(), key=lambda kv: float(kv[0]))[:depth]
        return (
            [[float(p), float(q)] for p, q in bids],
            [[float(p), float(q)] for p, q in asks],
        )


def _seq(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


class PantherCollector(BaseExchangeCollector):
    """PantherTrade spot market data. Unlike the other exchanges every connection and request is authenticated."""

    exchange_name: str = "panther"

    def __init__(
        self,
        writer: MarketDataWriter,
        target_symbols: List[str],
        api_key: str,
        api_secret: str,
        passphrase: str,
        ws_url: str = PANTHER_WS_URL,
        rest_url: str = PANTHER_REST_URL,
        rest_rate_limit_rps: float = 1.5,
        rest_poll_interval_ms: int = 200
    ):
        super().__init__(writer, target_symbols, rest_rate_limit_rps, rest_poll_interval_ms)
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.ws_url = ws_url
        self.rest_url = rest_url.rstrip("/")
        self._ws = None
        self._books: Dict[str, LocalBook] = {}
        # Per symbol: the last minute (epoch minutes) for which klines were requested, and candles already written.
        self._kline_minute: Dict[str, int] = {}
        self._kline_written: Dict[str, set] = {}

    @staticmethod
    def get_market_type(symbol: str) -> str:
        return "spot"

    # ------------------------------------------------------------------ WebSocket

    def _start_ws_tasks(self) -> List[asyncio.Task]:
        return [
            asyncio.create_task(
                self._run_ws_loop(
                    ws_url=self.ws_url,
                    subscribe_func=self._login_and_subscribe,
                    heartbeat_func=self._run_ws_heartbeat,
                    message_handler_func=self._handle_ws_message
                )
            )
        ]

    async def _run_ws_heartbeat(self, ws):
        """Application-level heartbeat. It starts after the login window, since an unauthenticated heartbeat is fatal."""
        try:
            while self.running:
                await asyncio.sleep(PANTHER_HEARTBEAT_SECONDS)
                ts = _now_ms()
                await ws.send(json.dumps({"id": f"hb_{ts}", "method": "heartbeat", "timestamp": ts}))
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f"Error sending Panther WS heartbeat: {e}")

    async def _login_and_subscribe(self, ws):
        self._ws = ws
        self._books = {symbol: LocalBook() for symbol in self.target_symbols}
        await self._login(ws)
        await self._subscribe(ws)

    async def _login(self, ws):
        ts = _now_ms()
        await ws.send(json.dumps({
            "method": "login",
            "params": {
                "api_key": self.api_key,
                "timestamp": ts,
                "signature": sign_message(f"{ts}GET/login", self.api_secret),
                "passphrase": self.passphrase
            },
            "timestamp": ts
        }))
        try:
            ack = json.loads(await asyncio.wait_for(ws.recv(), PANTHER_LOGIN_TIMEOUT_SECONDS))
        except asyncio.TimeoutError:
            raise RuntimeError("Panther WS login timed out")
        if ack.get("method") == "login_ack" and (ack.get("data") or {}).get("status") == "success":
            self.logger.info(f"Panther WS login succeeded (connections left: {(ack.get('data') or {}).get('conn_limit')})")
            return
        self.logger.error(f"Panther WS login failed: {ack}")
        await asyncio.sleep(PANTHER_LOGIN_FAILURE_PAUSE_SECONDS)
        raise RuntimeError(f"Panther WS login failed: {ack.get('message') or ack}")

    async def _subscribe(self, ws):
        """One request per channel; each carries every target symbol."""
        self.logger.info(f"Subscribing Panther WS streams for symbols: {self.target_symbols}")
        requests = [
            ("ticker", {"product_symbol": self.target_symbols}),
            ("trade", {"product_symbol": self.target_symbols}),
            ("book", {"product_symbol": self.target_symbols, "depth": PANTHER_BOOK_DEPTH}),
        ]
        for channel, params in requests:
            await ws.send(json.dumps({
                "method": "subscribe",
                "channel": channel,
                "params": params,
                "timestamp": _now_ms()
            }))

    async def _resync(self, symbol: str, data: Dict[str, Any]):
        """A broken sequence chain means the local book is wrong; reconnect to get a fresh snapshot."""
        self.logger.warning(
            f"Panther book sequence gap for {symbol}: have seq_id={self._books[symbol].seq_id}, "
            f"update prev_seq_id={data.get('prev_seq_id', data.get('pre_seq_id'))}. Reconnecting for a new snapshot."
        )
        if self._ws is not None:
            await self._ws.close()

    async def _handle_ws_message(self, raw_message: str):
        """Parse a WebSocket message and persist it."""
        try:
            msg = json.loads(raw_message)
            method = msg.get("method")
            if method in ("heartbeat_ack", "login_ack"):
                return
            if method == "subscription_ack":
                self.logger.info(f"Panther WS subscribed: {msg.get('channel')} {msg.get('data')}")
                return
            if method == "error":
                self.logger.error(f"Panther WS error message: {msg}")
                return

            channel = msg.get("channel")
            symbol = msg.get("product_symbol")
            data = msg.get("data")
            if not channel or not isinstance(data, dict) or symbol not in self.target_symbols:
                return

            market_type = self.get_market_type(symbol)

            if channel == "ticker":
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=symbol,
                    market_type=market_type,
                    category="bbo",
                    record={
                        # The ticker has no event time of its own (last_trade_time is the last trade), so use receipt time.
                        "timestamp": _now_ms(),
                        "bid_price": _to_float(data.get("best_bid_price")),
                        "bid_quantity": _to_float(data.get("best_bid_quantity")),
                        "ask_price": _to_float(data.get("best_ask_price")),
                        "ask_quantity": _to_float(data.get("best_ask_quantity")),
                        "last_price": _to_float(data.get("last_trade_price", data.get("last_price"))),
                        "raw": msg
                    }
                )
            elif channel in ("trade", "trades"):
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=symbol,
                    market_type=market_type,
                    category="trades",
                    record={
                        "timestamp": int(data.get("time") or _now_ms()),
                        "price": _to_float(data.get("price")),
                        "quantity": _to_float(data.get("quantity")),
                        "side": data.get("taker_side"),
                        "trade_id": str(data.get("public_trade_id")),
                        "raw": msg
                    }
                )
            elif channel == "book":
                book = self._books[symbol]
                if msg.get("type") == "snapshot":
                    book.apply_snapshot(data)
                elif not book.apply_update(data):
                    await self._resync(symbol, data)
                    return
                bids, asks = book.top()
                await self.writer.write(
                    exchange=self.exchange_name,
                    symbol=symbol,
                    market_type=market_type,
                    category="depth",
                    record={
                        "timestamp": int(data.get("time") or _now_ms()),
                        "bids": bids,
                        "asks": asks,
                        "version": str(book.seq_id if book.seq_id is not None else ""),
                        "raw": msg
                    }
                )
            else:
                self.logger.debug(f"Ignoring Panther WS message on unhandled channel '{channel}'")

        except Exception as e:
            self.logger.error(f"Error handling Panther WS message: {e}", exc_info=True)

    # ------------------------------------------------------------------ REST

    async def _get_json(self, path: str, params: Dict[str, Any]) -> Any:
        """Signed GET. The query string is part of the signed request path (unverified, see ADR 0004)."""
        request_path = f"{path}?{urlencode(params)}" if params else path
        ts = str(int(time.time()))
        headers = {
            "PT-ACCESS-KEY": self.api_key,
            "PT-SIGNATURE": sign_message(f"{ts}GET{request_path}", self.api_secret),
            "PT-TIMESTAMP": ts,
            "PT-Passphrase": self.passphrase,
        }
        async with self.session.get(f"{self.rest_url}{request_path}", headers=headers, timeout=5) as response:
            response.raise_for_status()
            return await response.json(content_type=None)

    async def _fetch_and_write_rest(self, symbol: str):
        """Poll the REST order book every cycle and the closed 1m candles once per minute.

        Both calls draw from the same 2 rps/IP budget, so the kline call takes its own rate limiter slot.
        """
        await self._fetch_orderbook(symbol)

        minute = int(time.time() // 60)
        if minute > self._kline_minute.get(symbol, 0):
            await self.rate_limiter.acquire()
            await self._fetch_klines(symbol, minute)
            self._kline_minute[symbol] = minute  # only after success, so a failed request is retried next cycle

    async def _fetch_orderbook(self, symbol: str):
        raw_data = await self._get_json(f"/v1/products/{symbol}/orderbook", {"depth": PANTHER_BOOK_DEPTH})
        if not isinstance(raw_data, dict) or "bids" not in raw_data or "asks" not in raw_data:
            raise ValueError(f"Panther orderbook request for {symbol} failed: {raw_data}")

        await self.writer.write(
            exchange=self.exchange_name,
            symbol=symbol,
            market_type=self.get_market_type(symbol),
            category="orderbook_rest",
            record={
                "timestamp": int(raw_data.get("time") or _now_ms()),
                "bids": _parse_levels(raw_data.get("bids")),
                "asks": _parse_levels(raw_data.get("asks")),
                "version": str(raw_data.get("sequence") or ""),
                "raw": raw_data
            }
        )

    async def _fetch_klines(self, symbol: str, minute: int):
        """Write closed 1m candles of the last few minutes that have not been written yet."""
        end_ms = minute * 60_000  # the start of the current minute: everything before it is closed
        start_ms = end_ms - PANTHER_KLINE_LOOKBACK_MINUTES * 60_000
        raw_data = await self._get_json(
            f"/v1/products/{symbol}/ohlc",
            {"interval": PANTHER_KLINE_INTERVAL, "start_time": start_ms, "end_time": end_ms}
        )
        if not isinstance(raw_data, list):
            raise ValueError(f"Panther ohlc request for {symbol} failed: {raw_data}")

        written = self._kline_written.setdefault(symbol, set())
        for candle in raw_data:
            open_time = int(candle["open_time"])
            close_time = int(candle["close_time"])
            if open_time in written or close_time > end_ms:
                continue  # already stored, or the still-open candle
            written.add(open_time)
            await self.writer.write(
                exchange=self.exchange_name,
                symbol=symbol,
                market_type=self.get_market_type(symbol),
                category="kline_1m_rest",
                record={
                    "timestamp": open_time,
                    "open_time": open_time,
                    "close_time": close_time,
                    "open": _to_float(candle.get("open")),
                    "high": _to_float(candle.get("high")),
                    "low": _to_float(candle.get("low")),
                    "close": _to_float(candle.get("close")),
                    "volume": _to_float(candle.get("volume")),
                    "raw": candle
                }
            )
        written.intersection_update({t for t in written if t >= start_ms})
