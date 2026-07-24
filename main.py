import asyncio
import logging
import sys
import signal

from writer import MarketDataWriter
from uploader import MarketDataUploader
from collectors import (
    HashkeyCollector,
    BitgetCollector,
    GateCollector,
    OSLCollector
)
from config import (
    TARGET_SYMBOLS,
    HASHKEY_WS_URL,
    HASHKEY_REST_URL,
    HASHKEY_REST_POLL_INTERVAL_MS,
    HASHKEY_REST_RATE_LIMIT_RPS,
    BITGET_WS_URL,
    BITGET_REST_URL,
    BITGET_REST_POLL_INTERVAL_MS,
    BITGET_REST_RATE_LIMIT_RPS,
    GATE_USDT_WS_URL,
    GATE_BTC_WS_URL,
    GATE_REST_URL,
    GATE_REST_POLL_INTERVAL_MS,
    GATE_REST_RATE_LIMIT_RPS,
    OSL_API_KEY,
    OSL_API_SECRET,
    OSL_REST_URL,
    OSL_WS_URL,
    OSL_REST_POLL_INTERVAL_MS,
    OSL_REST_RATE_LIMIT_RPS
)


# Configure logging with a clean, detailed, and human-readable format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
# Reduce verbose logging from third party libraries
logging.getLogger("websockets").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)

logger = logging.getLogger("Main")


class Application:
    def __init__(self):
        self.writer = None
        self.collectors = []
        self.uploader = None
        self.shutdown_event = asyncio.Event()

    async def run(self):
        """Main orchestrator for the application."""
        logger.info("Initializing Multi-Exchange Market Data Collector...")
        
        # 1. Initialize Writer & Uploader
        self.writer = MarketDataWriter()
        self.uploader = MarketDataUploader()
        
        # 2. Initialize all Exchange Collectors
        self.collectors = [
            HashkeyCollector(
                writer=self.writer,
                target_symbols=TARGET_SYMBOLS,
                rest_rate_limit_rps=HASHKEY_REST_RATE_LIMIT_RPS,
                rest_poll_interval_ms=HASHKEY_REST_POLL_INTERVAL_MS,
                ws_url=HASHKEY_WS_URL,
                rest_url=HASHKEY_REST_URL
            ),
            BitgetCollector(
                writer=self.writer,
                target_symbols=TARGET_SYMBOLS,
                rest_rate_limit_rps=BITGET_REST_RATE_LIMIT_RPS,
                rest_poll_interval_ms=BITGET_REST_POLL_INTERVAL_MS,
                ws_url=BITGET_WS_URL,
                rest_url=BITGET_REST_URL
            ),
            GateCollector(
                writer=self.writer,
                target_symbols=TARGET_SYMBOLS,
                rest_rate_limit_rps=GATE_REST_RATE_LIMIT_RPS,
                rest_poll_interval_ms=GATE_REST_POLL_INTERVAL_MS,
                usdt_ws_url=GATE_USDT_WS_URL,
                btc_ws_url=GATE_BTC_WS_URL,
                rest_url=GATE_REST_URL
            ),
            OSLCollector(
                writer=self.writer,
                target_symbols=TARGET_SYMBOLS,
                api_key=OSL_API_KEY,
                api_secret=OSL_API_SECRET,
                ws_url=OSL_WS_URL,
                rest_url=OSL_REST_URL,
                rest_rate_limit_rps=OSL_REST_RATE_LIMIT_RPS,
                rest_poll_interval_ms=OSL_REST_POLL_INTERVAL_MS
            )
        ]

        # 3. Setup Graceful Shutdown Signal Handlers
        self._setup_signal_handlers()

        # 4. Start uploader
        await self.uploader.start()

        # 5. Start all exchange collectors
        for collector in self.collectors:
            await collector.start()

        logger.info(f"All {len(self.collectors)} exchange collectors are active. Collection running. Press Ctrl+C to stop.")
        
        # Keep running until shutdown signal is received
        await self.shutdown_event.wait()
        
        # Graceful shutdown process
        await self._shutdown()

    def _setup_signal_handlers(self):
        """Bind SIGINT and SIGTERM to trigger graceful shutdown."""
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self._handle_shutdown_signal, sig)
            except NotImplementedError:
                # Fallback for platforms where add_signal_handler is not implemented (e.g. Windows)
                pass

    def _handle_shutdown_signal(self, sig):
        logger.info(f"Received termination signal {sig.name}. Initiating graceful shutdown...")
        self.shutdown_event.set()

    async def _shutdown(self):
        """Orchestrate multi-step shutdown of all services."""
        logger.info("Stopping collectors and flushing files...")
        
        # Stop all collectors concurrently
        if self.collectors:
            logger.info("Stopping exchange collectors...")
            stop_tasks = [collector.stop() for collector in self.collectors]
            await asyncio.gather(*stop_tasks, return_exceptions=True)

        # Stop S3 Uploader background loop
        if self.uploader:
            try:
                await self.uploader.stop()
            except Exception as e:
                logger.error(f"Error stopping S3 uploader: {e}")

        # Final write handles flush and close
        if self.writer:
            try:
                await self.writer.close()
            except Exception as e:
                logger.error(f"Error closing market data writer: {e}")

        logger.info("Shutdown sequence completed. Exiting.")


if __name__ == "__main__":
    app = Application()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        logger.info("Program terminated via KeyboardInterrupt.")
    except Exception as e:
        logger.critical(f"Unhandled exception in main execution loop: {e}", exc_info=True)
        sys.exit(1)
