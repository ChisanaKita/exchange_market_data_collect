import json
import logging
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any
from collections import OrderedDict

from config import LOCAL_DATA_DIR

logger = logging.getLogger("MarketDataWriter")

class MarketDataWriter:
    def __init__(self, base_dir: str = LOCAL_DATA_DIR):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.file_handles: OrderedDict[str, Any] = OrderedDict()
        self.max_handles = 800  # Safe limit under standard 1024 OS descriptor limit
        self.lock = asyncio.Lock()
        self.current_day_utc = self._get_current_day_utc()

    def _get_current_day_utc(self) -> str:
        """Get current day formatted as YYYYMMDD in UTC."""
        return datetime.now(timezone.utc).strftime("%Y%m%d")

    def _get_file_path(self, day: str, exchange: str, symbol: str, market_type: str, category: str) -> Path:
        """Construct the file path for a specific stream."""
        return self.base_dir / day / exchange / symbol / market_type / f"{category}.jsonl"

    async def write(self, exchange: str, symbol: str, market_type: str, category: str, record: Dict[str, Any]):
        """Write a dictionary as a JSON line to the correct file."""
        async with self.lock:
            # Check for UTC midnight transition
            day = self._get_current_day_utc()
            if day != self.current_day_utc:
                logger.info(f"UTC day transition detected: {self.current_day_utc} -> {day}. Flushing files.")
                await self._close_all_handles()
                self.current_day_utc = day

            # Key for managing active file handles
            handle_key = f"{day}_{exchange}_{symbol}_{market_type}_{category}"

            if handle_key in self.file_handles:
                # Move to end to mark as recently accessed
                self.file_handles.move_to_end(handle_key)
            else:
                # Evict the oldest opened file handle if limit reached
                if len(self.file_handles) >= self.max_handles:
                    oldest_key, oldest_handle = self.file_handles.popitem(last=False)
                    try:
                        oldest_handle.close()
                    except Exception as e:
                        logger.error(f"Error closing evicted handle {oldest_key}: {e}")

                file_path = self._get_file_path(day, exchange, symbol, market_type, category)
                file_path.parent.mkdir(parents=True, exist_ok=True)
                # buffering=1 means line-buffered (flushes on every newline)
                self.file_handles[handle_key] = open(file_path, "a", buffering=1, encoding="utf-8")

            # Add normalized timestamp and datetime if not already present
            now = datetime.now(timezone.utc)
            if "timestamp" not in record:
                record["timestamp"] = int(now.timestamp() * 1000)
            if "datetime" not in record:
                record["datetime"] = now.isoformat()

            # Include metadata
            payload = {
                "timestamp": record["timestamp"],
                "datetime": record["datetime"],
                "exchange": exchange,
                "symbol": symbol,
                "market_type": market_type,
                "category": category,
                **record
            }

            try:
                line = json.dumps(payload, separators=(',', ':')) + "\n"
                self.file_handles[handle_key].write(line)
            except Exception as e:
                logger.error(f"Failed to write record to {handle_key}: {e}")

    async def _close_all_handles(self):
        """Close all open file handles."""
        for key, handle in list(self.file_handles.items()):
            try:
                handle.close()
            except Exception as e:
                logger.error(f"Error closing handle {key}: {e}")
        self.file_handles.clear()

    async def close(self):
        """Public method to close writer gracefully."""
        async with self.lock:
            await self._close_all_handles()
            logger.info("All file handles closed.")
