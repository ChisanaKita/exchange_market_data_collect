import asyncio
import logging

from collectors.base import BaseExchangeCollector
from collectors.panther import PantherCollector


class RecordingWriter:
    def __init__(self):
        self.records = []

    async def write(self, **kwargs):
        self.records.append(kwargs)


def test_panther_orderbook_with_one_empty_side_is_written():
    # A thin book returns no `bids` key at all (seen live for USDT-USD on 2026-11-18)
    writer = RecordingWriter()
    collector = PantherCollector(writer, ["USDT-USD"], api_key="k", api_secret="s", passphrase="p")

    async def fake_get_json(path, params):
        return {"product_symbol": "USDT-USD", "asks": [{"price": "0.999", "size": "100000"}],
                "sequence": 2132843, "time": 1794974024022}
    collector._get_json = fake_get_json

    asyncio.run(collector._fetch_orderbook("USDT-USD"))

    assert len(writer.records) == 1
    record = writer.records[0]["record"]
    assert record["bids"] == []
    assert record["asks"] == [[0.999, 100000.0]]


def test_rest_poll_error_log_names_the_exception_type(caplog):
    # str(asyncio.TimeoutError()) is "", which left log lines like "Error polling REST data for BTCUSD: "
    class TimingOutCollector(BaseExchangeCollector):
        async def _fetch_and_write_rest(self, symbol):
            self.running = False
            raise asyncio.TimeoutError()

    collector = TimingOutCollector(RecordingWriter(), ["BTCUSD"], rest_rate_limit_rps=0, rest_poll_interval_ms=1)
    collector.running = True

    with caplog.at_level(logging.ERROR):
        asyncio.run(collector._run_rest_polling("BTCUSD"))

    assert "Error polling REST data for BTCUSD: TimeoutError" in caplog.text
