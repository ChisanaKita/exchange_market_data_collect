import logging

from monitor import DataFreshnessMonitor


class FakeWriter:
    def __init__(self):
        self.last_write = {}


def test_spot_and_futures_with_the_same_symbol_are_monitored_separately(caplog):
    # Bitget has BTCUSDT in both markets; fresh futures data must not hide a silent spot feed
    writer = FakeWriter()
    expected = [("bitget", "spot", "BTCUSDT"), ("bitget", "futures", "BTCUSDT")]
    monitor = DataFreshnessMonitor(writer, expected, stale_after=60)
    monitor.started_at = 0
    writer.last_write[("bitget", "futures", "BTCUSDT")] = 100

    with caplog.at_level(logging.ERROR):
        monitor.check(now=120)

    assert monitor.stale == {("bitget", "spot", "BTCUSDT")}
    assert "bitget: BTCUSDT (spot)" in caplog.text
    assert "(futures)" not in caplog.text
