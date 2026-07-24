import asyncio
import logging
import aiohttp
from typing import List, Dict, Any
from writer import MarketDataWriter

logger = logging.getLogger("BaseExchangeCollector")


class AsyncRateLimiter:
    """Non-blocking rate limiter to throttle requests to a safe rate."""
    def __init__(self, rps: float):
        self.rps = rps
        self.time_between_requests = 1.0 / rps if rps > 0 else 0.0
        self.last_request_time = 0.0
        self.lock = asyncio.Lock()

    async def acquire(self):
        if self.rps <= 0:
            return
        async with self.lock:
            now = asyncio.get_event_loop().time()
            elapsed = now - self.last_request_time
            if elapsed < self.time_between_requests:
                sleep_time = self.time_between_requests - elapsed
                await asyncio.sleep(sleep_time)
            self.last_request_time = asyncio.get_event_loop().time()


class BaseExchangeCollector:
    exchange_name: str = "base"

    def __init__(
        self,
        writer: MarketDataWriter,
        target_symbols: List[str],
        rest_rate_limit_rps: float,
        rest_poll_interval_ms: int
    ):
        self.writer = writer
        self.target_symbols = target_symbols
        self.rest_rate_limit_rps = rest_rate_limit_rps
        self.rest_poll_interval_ms = rest_poll_interval_ms
        self.session = None
        self.running = False
        self.tasks: List[asyncio.Task] = []
        self.rate_limiter = AsyncRateLimiter(rest_rate_limit_rps)
        self.global_backoff_until = 0.0
        self.logger = logging.getLogger(self.__class__.__name__)

    async def start(self):
        """Start the collector services."""
        self.running = True
        self.session = aiohttp.ClientSession()

        # Start WebSocket loop(s)
        ws_tasks = self._start_ws_tasks()
        self.tasks.extend(ws_tasks)

        # Start REST polling loop for each symbol
        for symbol in self.target_symbols:
            self.tasks.append(asyncio.create_task(self._run_rest_polling(symbol)))

        self.logger.info(f"{self.exchange_name.capitalize()} Collector successfully started.")

    async def stop(self):
        """Stop the collector gracefully."""
        self.running = False
        # Cancel all background tasks
        for task in self.tasks:
            task.cancel()
        
        # Wait for all tasks to be completed / cancelled
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
            self.tasks.clear()

        # Close aiohttp session
        if self.session:
            await self.session.close()
            self.session = None

        self.logger.info(f"{self.exchange_name.capitalize()} Collector stopped.")

    def _start_ws_tasks(self) -> List[asyncio.Task]:
        """Override in subclass to define which WebSocket loops to run."""
        raise NotImplementedError

    async def _run_ws_loop(self, ws_url: str, subscribe_func, heartbeat_func, message_handler_func):
        """WebSocket manager with exponential backoff on connection failure."""
        import websockets
        backoff = 1
        while self.running:
            try:
                self.logger.info(f"Connecting to {self.exchange_name.capitalize()} WS at {ws_url}...")
                async with websockets.connect(ws_url, ping_interval=20, ping_timeout=10) as ws:
                    backoff = 1  # Reset backoff on successful connection
                    self.logger.info(f"Successfully connected to {self.exchange_name.capitalize()} WebSocket.")

                    # Start heartbeat task if provided
                    heartbeat_task = None
                    if heartbeat_func:
                        heartbeat_task = asyncio.create_task(heartbeat_func(ws))
                    
                    try:
                        # Subscribe to streams
                        await subscribe_func(ws)

                        # Main receive loop
                        async for message in ws:
                            if not self.running:
                                break
                            await message_handler_func(message)
                    finally:
                        if heartbeat_task:
                            heartbeat_task.cancel()

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"{self.exchange_name.capitalize()} WS connection error: {e}. Reconnecting in {backoff} seconds...")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 60)

    async def _run_rest_polling(self, symbol: str):
        """Generic REST poller loop with custom rate limiter and global 429 backoff."""
        poll_interval_sec = self.rest_poll_interval_ms / 1000.0

        while self.running:
            start_time = asyncio.get_event_loop().time()

            # Apply global backoff if active
            now = asyncio.get_event_loop().time()
            if now < self.global_backoff_until:
                sleep_duration = self.global_backoff_until - now
                self.logger.debug(f"REST Poller for {symbol} sleeping during active global backoff: {sleep_duration:.1f}s")
                await asyncio.sleep(sleep_duration)
                continue

            try:
                # Acquire slot from rate limiter
                await self.rate_limiter.acquire()

                # Perform fetch
                await self._fetch_and_write_rest_orderbook(symbol)

            except asyncio.CancelledError:
                break
            except aiohttp.ClientResponseError as cre:
                if cre.status == 429:
                    self.logger.warning(f"REST orderbook polling hit HTTP 429 (Too Many Requests). Setting global backoff for 60 seconds...")
                    self.global_backoff_until = asyncio.get_event_loop().time() + 60.0
                else:
                    self.logger.error(f"HTTP error fetching REST orderbook for {symbol}: status={cre.status}, msg={cre.message}")
            except Exception as e:
                self.logger.error(f"Error polling REST orderbook for {symbol}: {e}")

            # Space out consecutive requests of the same poller task
            elapsed = asyncio.get_event_loop().time() - start_time
            sleep_time = max(0.01, poll_interval_sec - elapsed)
            await asyncio.sleep(sleep_time)

    async def _fetch_and_write_rest_orderbook(self, symbol: str):
        """Fetch REST orderbook snapshot and write it. Must be implemented in subclass."""
        raise NotImplementedError
