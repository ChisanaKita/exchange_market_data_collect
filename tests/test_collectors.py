import asyncio
import json
import logging

import pytest

from collectors.base import BaseExchangeCollector
from collectors.bitget import BitgetCollector, PERP, SPOT, route_for
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


# ---------------------------------------------------------------- Bitget


@pytest.mark.parametrize("market, symbol, expected", [
    (SPOT, "BTCUSDT", ("v2", "SPOT", "SPOT")),
    (PERP, "BTCUSDT", ("v2", "USDT-FUTURES", "USDT-FUTURES")),
    (PERP, "HYPEPERP", ("v2", "USDC-FUTURES", "USDC-FUTURES")),
    (PERP, "BTCUSD_CM", ("v3", "coin-futures", "COIN-FUTURES")),
])
def test_bitget_route_for(market, symbol, expected):
    route = route_for(market, symbol)
    assert (route.ws_version, route.ws_inst_type, route.rest_category) == expected


def test_bitget_rejects_unknown_market():
    with pytest.raises(ValueError):
        BitgetCollector(RecordingWriter(), ["BTCUSDT"], market="futures")


def test_bitget_spot_and_perp_streams_are_distinct():
    spot = BitgetCollector(RecordingWriter(), ["BTCUSDT"], market=SPOT)
    perp = BitgetCollector(RecordingWriter(), ["BTCUSDT"], market=PERP)
    assert spot.monitored_streams() == [("bitget", "spot", "BTCUSDT")]
    assert perp.monitored_streams() == [("bitget", "futures", "BTCUSDT")]


def test_bitget_v2_candle_close_time_is_not_the_usdt_volume():
    # v2 candle: [start, open, high, low, close, base vol, quote vol, USDT vol]; index 7 is not a close time
    writer = RecordingWriter()
    collector = BitgetCollector(writer, ["BTCUSDT"], market=SPOT)
    msg = {"action": "update", "arg": {"instType": "SPOT", "channel": "candle1m", "instId": "BTCUSDT"},
           "data": [["1795597680000", "59249.97", "59270", "59248.37", "59264.82", "0.799991",
                     "47402.96363795", "47402.96363795"]], "ts": 1795597705000}

    asyncio.run(collector._handle_ws_message(json.dumps(msg)))

    write = writer.records[0]
    assert write["market_type"] == "spot"
    assert write["category"] == "kline_1m"
    assert write["record"]["close_time"] == 1795597680000 + 59999
    assert write["record"]["close"] == 59264.82
    assert write["record"]["volume"] == 0.799991


def test_bitget_v2_depth_version_comes_from_seq():
    writer = RecordingWriter()
    collector = BitgetCollector(writer, ["BTCUSDT"], market=PERP)
    msg = {"action": "update", "arg": {"instType": "USDT-FUTURES", "channel": "books", "instId": "BTCUSDT"},
           "data": [{"asks": [["59230.4", "3.4898"]], "bids": [], "ts": "1795597705601",
                     "seq": 1306201093551, "pseq": 1306201088805}], "ts": 1795597705602}

    asyncio.run(collector._handle_ws_message(json.dumps(msg)))

    write = writer.records[0]
    assert write["market_type"] == "futures"
    assert write["record"]["version"] == "1306201093551"
    assert write["record"]["asks"] == [[59230.4, 3.4898]]
    assert write["record"]["bids"] == []


def _v3(topic, data, **arg):
    return json.dumps({"action": "update", "arg": {"instType": "coin-futures", "topic": topic,
                                                   "symbol": "BTCUSD_CM", **arg},
                       "data": data, "ts": 1795597643041})


def test_bitget_v3_messages_are_written_like_v2():
    # Payloads captured from wss://ws.bitget.com/v3/ws/public on 2026-11-25
    writer = RecordingWriter()
    collector = BitgetCollector(writer, ["BTCUSD_CM"], market=PERP)
    for raw in (
        _v3("kline", [{"start": "1795597620000", "open": "59141.5", "close": "59160.9", "high": "59164.3",
                       "low": "59141.5", "volume": "0.1184", "turnover": "6997"}], interval="1m"),
        _v3("publicTrade", [{"i": "1509411404596895744", "p": "59160.9", "v": "1998", "S": "buy",
                             "T": "1795597643040", "L": "1509411404596895745", "isRPI": "no"}]),
        _v3("books", [{"a": [["59171.6", "32976"]], "b": [["57688.5", "0"]], "seq": 706187742002,
                       "pseq": 706187738805, "ts": "1795597639006", "maxdepth": "1000"}]),
        _v3("books1", [{"a": [["59182.4", "30119"]], "b": [["59172.4", "30999"]], "seq": 706179628814,
                        "pseq": 0, "ts": "1795597468244"}]),
        "pong",
        json.dumps({"event": "subscribe", "arg": {"instType": "coin-futures", "topic": "books1",
                                                  "symbol": "BTCUSD_CM"}}),
    ):
        asyncio.run(collector._handle_v3_ws_message(raw))

    by_category = {w["category"]: w for w in writer.records}
    assert list(by_category) == ["kline_1m", "trades", "depth", "bbo"]
    assert all(w["symbol"] == "BTCUSD_CM" and w["market_type"] == "futures" for w in writer.records)

    kline = by_category["kline_1m"]["record"]
    assert (kline["open_time"], kline["close_time"]) == (1795597620000, 1795597679999)
    assert (kline["open"], kline["high"], kline["low"], kline["close"]) == (59141.5, 59164.3, 59141.5, 59160.9)

    trade = by_category["trades"]["record"]
    assert (trade["timestamp"], trade["price"], trade["quantity"], trade["side"], trade["trade_id"]) == (
        1795597643040, 59160.9, 1998.0, "buy", "1509411404596895744")

    depth = by_category["depth"]["record"]
    assert (depth["asks"], depth["bids"], depth["version"]) == ([[59171.6, 32976.0]], [[57688.5, 0.0]],
                                                                "706187742002")

    bbo = by_category["bbo"]["record"]
    assert (bbo["bid_price"], bbo["bid_quantity"], bbo["ask_price"], bbo["ask_quantity"]) == (
        59172.4, 30999.0, 59182.4, 30119.0)


def test_bitget_subscribe_splits_by_protocol_and_chunk():
    sent = {}

    class FakeWs:
        def __init__(self, name):
            self.name = name

        async def send(self, payload):
            sent[self.name] = json.loads(payload)["args"]

    perps = [f"S{i}USDT" for i in range(13)] + ["HYPEPERP", "BTCUSD_CM"]
    collector = BitgetCollector(RecordingWriter(), perps, market=PERP)

    async def run():
        await collector._subscribe_v2(perps[:12], FakeWs("v2a"))
        await collector._subscribe_v3(["BTCUSD_CM"], FakeWs("v3"))
    asyncio.run(run())

    assert len(sent["v2a"]) == 48
    assert {a["instType"] for a in sent["v2a"]} == {"USDT-FUTURES"}
    assert sent["v3"] == [
        {"instType": "coin-futures", "topic": "kline", "symbol": "BTCUSD_CM", "interval": "1m"},
        {"instType": "coin-futures", "topic": "publicTrade", "symbol": "BTCUSD_CM"},
        {"instType": "coin-futures", "topic": "books", "symbol": "BTCUSD_CM"},
        {"instType": "coin-futures", "topic": "books1", "symbol": "BTCUSD_CM"},
    ]


def test_bitget_starts_one_ws_loop_per_protocol_chunk():
    perps = [f"S{i}USDT" for i in range(13)] + ["HYPEPERP", "BTCUSD_CM"]
    collector = BitgetCollector(RecordingWriter(), perps, market=PERP)
    urls = []

    async def fake_loop(ws_url, subscribe_func, heartbeat_func, message_handler_func):
        urls.append(ws_url)

    collector._run_ws_loop = fake_loop

    async def run():
        await asyncio.gather(*collector._start_ws_tasks())
    asyncio.run(run())

    # 14 v2 symbols -> 2 connections (12 + 2), 1 v3 symbol -> 1 connection
    assert sorted(urls) == sorted([collector.ws_url, collector.ws_url, collector.v3_ws_url])
