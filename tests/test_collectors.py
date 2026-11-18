import asyncio

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

