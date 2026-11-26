import asyncio
import logging
import sys
import signal

from writer import MarketDataWriter
from uploader import MarketDataUploader
from collectors.bitget import SPOT as BITGET_SPOT, PERP as BITGET_PERP
from collectors import (
    HashkeyGlobalCollector,
    HashkeyHkCollector,
    HashkeyMenaCollector,
    BitgetCollector,
    GateCollector,
    OSLCollector,
    PantherCollector
)
from config import (
    HASHKEY_GLOBAL_TARGET_SYMBOLS,
    HASHKEY_HK_TARGET_SYMBOLS,
    HASHKEY_MENA_TARGET_SYMBOLS,
    BITGET_SPOT_TARGET_SYMBOLS,
    BITGET_PERP_TARGET_SYMBOLS,
    IGNORED_SYMBOL_ENV_VARS,
    GATE_TARGET_SYMBOLS,
    OSL_TARGET_SYMBOLS,
    PANTHER_TARGET_SYMBOLS,
    HASHKEY_GLOBAL_WS_URL,
    HASHKEY_GLOBAL_REST_URL,
    HASHKEY_GLOBAL_REST_POLL_INTERVAL_MS,
    HASHKEY_GLOBAL_REST_RATE_LIMIT_RPS,
    HASHKEY_HK_WS_URL,
    HASHKEY_HK_REST_URL,
    HASHKEY_HK_REST_POLL_INTERVAL_MS,
    HASHKEY_HK_REST_RATE_LIMIT_RPS,
    HASHKEY_MENA_WS_URL,
    HASHKEY_MENA_REST_URL,
    HASHKEY_MENA_REST_POLL_INTERVAL_MS,
    HASHKEY_MENA_REST_RATE_LIMIT_RPS,
    HASHKEY_MENA_FUNDING_RATE_DELAY_MS,
    BITGET_WS_URL,
    BITGET_V3_WS_URL,
    BITGET_REST_URL,
    BITGET_REST_POLL_INTERVAL_MS,
    BITGET_REST_RATE_LIMIT_RPS,
    GATE_USDT_WS_URL,
    GATE_BTC_WS_URL,
    GATE_REST_URL,
    GATE_REST_POLL_INTERVAL_MS,
    GATE_REST_RATE_LIMIT_RPS,
    OSL_REST_URL,
    OSL_WS_URL,
    OSL_REST_POLL_INTERVAL_MS,
    OSL_REST_RATE_LIMIT_RPS,
    PANTHER_WS_URL,
    PANTHER_REST_URL,
    PANTHER_API_KEY,
    PANTHER_API_SECRET,
    PANTHER_PASSPHRASE,
    PANTHER_REST_POLL_INTERVAL_MS,
    PANTHER_REST_RATE_LIMIT_RPS,
    LOG_DIR,
    LOG_LEVEL,
    LOG_RETENTION_DAYS,
    LOG_MAX_FILE_MB,
    LOG_MAX_TOTAL_MB,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    ALERT_INSTANCE_NAME,
    TELEGRAM_ALERT_COOLDOWN_MINUTES,
    STALE_DATA_ALERT_MINUTES
)
from app_logging import setup_logging, ALERT
from alerts import add_telegram_sink
from monitor import DataFreshnessMonitor


# stdout plus daily log files kept for LOG_RETENTION_DAYS (docker logs alone are capped and lost on recreate)
log_path = setup_logging(LOG_DIR, LOG_LEVEL, LOG_RETENTION_DAYS, LOG_MAX_FILE_MB, LOG_MAX_TOTAL_MB)

logger = logging.getLogger("Main")
logger.info(f"Writing application logs to {log_path.resolve()} (kept {LOG_RETENTION_DAYS} days).")
add_telegram_sink(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ALERT_INSTANCE_NAME, TELEGRAM_ALERT_COOLDOWN_MINUTES)


class Application:
    def __init__(self):
        self.writer = None
        self.collectors = []
        self.uploader = None
        self.monitor = None
        self.shutdown_event = asyncio.Event()

    async def run(self):
        """Main orchestrator for the application."""
        logger.info("Initializing Multi-Exchange Market Data Collector...")
        
        # 1. Initialize Writer & Uploader
        self.writer = MarketDataWriter()
        self.uploader = MarketDataUploader()
        
        # 2. Initialize all Exchange Collectors
        self.collectors = [
            HashkeyGlobalCollector(
                writer=self.writer,
                target_symbols=HASHKEY_GLOBAL_TARGET_SYMBOLS,
                rest_rate_limit_rps=HASHKEY_GLOBAL_REST_RATE_LIMIT_RPS,
                rest_poll_interval_ms=HASHKEY_GLOBAL_REST_POLL_INTERVAL_MS,
                ws_url=HASHKEY_GLOBAL_WS_URL,
                rest_url=HASHKEY_GLOBAL_REST_URL
            ),
            HashkeyHkCollector(
                writer=self.writer,
                target_symbols=HASHKEY_HK_TARGET_SYMBOLS,
                rest_rate_limit_rps=HASHKEY_HK_REST_RATE_LIMIT_RPS,
                rest_poll_interval_ms=HASHKEY_HK_REST_POLL_INTERVAL_MS,
                ws_url=HASHKEY_HK_WS_URL,
                rest_url=HASHKEY_HK_REST_URL
            ),
            HashkeyMenaCollector(
                writer=self.writer,
                target_symbols=HASHKEY_MENA_TARGET_SYMBOLS,
                rest_rate_limit_rps=HASHKEY_MENA_REST_RATE_LIMIT_RPS,
                rest_poll_interval_ms=HASHKEY_MENA_REST_POLL_INTERVAL_MS,
                funding_rate_delay_ms=HASHKEY_MENA_FUNDING_RATE_DELAY_MS,
                ws_url=HASHKEY_MENA_WS_URL,
                rest_url=HASHKEY_MENA_REST_URL
            ),
            *(
                BitgetCollector(
                    writer=self.writer,
                    target_symbols=symbols,
                    market=market,
                    rest_rate_limit_rps=BITGET_REST_RATE_LIMIT_RPS,
                    rest_poll_interval_ms=BITGET_REST_POLL_INTERVAL_MS,
                    ws_url=BITGET_WS_URL,
                    v3_ws_url=BITGET_V3_WS_URL,
                    rest_url=BITGET_REST_URL
                )
                for market, symbols in (
                    (BITGET_SPOT, BITGET_SPOT_TARGET_SYMBOLS),
                    (BITGET_PERP, BITGET_PERP_TARGET_SYMBOLS),
                )
                if symbols
            ),
            GateCollector(
                writer=self.writer,
                target_symbols=GATE_TARGET_SYMBOLS,
                rest_rate_limit_rps=GATE_REST_RATE_LIMIT_RPS,
                rest_poll_interval_ms=GATE_REST_POLL_INTERVAL_MS,
                usdt_ws_url=GATE_USDT_WS_URL,
                btc_ws_url=GATE_BTC_WS_URL,
                rest_url=GATE_REST_URL
            ),
            OSLCollector(
                writer=self.writer,
                target_symbols=OSL_TARGET_SYMBOLS,
                ws_url=OSL_WS_URL,
                rest_url=OSL_REST_URL,
                rest_rate_limit_rps=OSL_REST_RATE_LIMIT_RPS,
                rest_poll_interval_ms=OSL_REST_POLL_INTERVAL_MS
            )
        ]

        # Panther needs credentials for every connection; without them skip it so the other exchanges still run
        if PANTHER_API_KEY and PANTHER_API_SECRET and PANTHER_PASSPHRASE:
            self.collectors.append(
                PantherCollector(
                    writer=self.writer,
                    target_symbols=PANTHER_TARGET_SYMBOLS,
                    api_key=PANTHER_API_KEY,
                    api_secret=PANTHER_API_SECRET,
                    passphrase=PANTHER_PASSPHRASE,
                    ws_url=PANTHER_WS_URL,
                    rest_url=PANTHER_REST_URL,
                    rest_rate_limit_rps=PANTHER_REST_RATE_LIMIT_RPS,
                    rest_poll_interval_ms=PANTHER_REST_POLL_INTERVAL_MS
                )
            )
        else:
            logger.warning(
                "Panther collector disabled: set PANTHER_API_KEY, PANTHER_API_SECRET and PANTHER_PASSPHRASE to enable it."
            )

        if IGNORED_SYMBOL_ENV_VARS:
            logger.warning(
                f"Ignoring {', '.join(IGNORED_SYMBOL_ENV_VARS)}: symbols are set only in config.py. "
                "Remove these from the environment / .env.",
                extra=ALERT
            )

        # 3. Setup Graceful Shutdown Signal Handlers
        self._setup_signal_handlers()

        # 4. Start uploader
        await self.uploader.start()

        # 5. Start all exchange collectors
        for collector in self.collectors:
            await collector.start()

        # 6. Alert when any configured symbol stops producing data
        self.monitor = DataFreshnessMonitor(
            self.writer,
            [stream for collector in self.collectors for stream in collector.monitored_streams()],
            stale_after=STALE_DATA_ALERT_MINUTES * 60
        )
        await self.monitor.start()

        # Bitget runs one collector per market, so count distinct exchange names
        exchanges = list(dict.fromkeys(collector.exchange_name for collector in self.collectors))
        logger.info(
            f"Collector started: {len(exchanges)} exchanges active ({', '.join(exchanges)}).",
            extra=ALERT
        )
        
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
        logger.warning(f"Received termination signal {sig.name}. Shutting down; market data collection stops.", extra=ALERT)
        self.shutdown_event.set()

    async def _shutdown(self):
        """Orchestrate multi-step shutdown of all services."""
        logger.info("Stopping collectors and flushing files...")
        
        if self.monitor:
            await self.monitor.stop()

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
