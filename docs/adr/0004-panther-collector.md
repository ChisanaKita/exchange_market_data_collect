# 0004. PantherTrade collector

- Status: Accepted (live behaviour unverified, see "Unverified")
- Date: 2026-11-03

## Context

Business wants PantherTrade (`usdtusd`, `usdthkd`, `btcusd`, `ethusd`) collected. The API doc
(`docs/PantherTrade.md`, copied by hand from an invite-only page) describes a spot-only venue with a
WebSocket (`wss://ws-api.panthertrade.com/v1`) and REST (`https://web-api.panthertrade.com`). Unlike the
other exchanges there is no public market data: the WebSocket must log in within 10 s and every REST
request carries `PT-ACCESS-KEY`, `PT-SIGNATURE`, `PT-TIMESTAMP` and `PT-Passphrase`.

## Decision

| Panther source | Category written | Notes |
|---|---|---|
| WS `ticker` | `bbo` | `timestamp` is receipt time: the ticker carries no event time (`last_trade_time` is the last trade) |
| WS `trade` | `trades` | one row per push |
| WS `book`, depth 20 | `depth` | snapshot + deltas applied to a local book; each row is the full top 20, the delta stays in `raw` |
| REST `/orderbook?depth=20` | `orderbook_rest` | polled every cycle |
| REST `/ohlc` 1m | `kline_1m_rest` | the WS has no kline; closed candles only, requested once per minute over the last 3 minutes and de-duplicated on `open_time` |

- Exchange name, folder and config prefix are `panther`; all data is `spot`.
- Symbols are native `BASE-QUOTE` (`USDT-USD`, `USDT-HKD`, `BTC-USD`, `ETH-USD`) from `PANTHER_TARGET_SYMBOLS`
  ([0002](0002-config-is-the-single-symbol-source.md)).
- Credentials come from `PANTHER_API_KEY`, `PANTHER_API_SECRET`, `PANTHER_PASSPHRASE`. If any is empty,
  `main.py` skips the collector with a warning so the other exchanges still run.
- Book deltas are rebuilt locally so `depth` matches the other exchanges (full books). A delta whose
  `prev_seq_id` differs from the last `seq_id` means the book is wrong; the collector closes the socket
  and reconnects for a fresh snapshot.
- Rate limits: REST is 2 rps/IP across all endpoints, so `PANTHER_REST_RATE_LIMIT_RPS` defaults to 1.5 and
  the once-a-minute kline call takes a slot from the same limiter. WS: 3 handshakes/s/IP, 50 connections per
  entity, 60 s idle timeout (heartbeat every 30 s). After a failed login the collector pauses 30 s before
  reconnecting.
- The key must whitelist the collector's IP (error -803008) and the host clock must be within 30 s of
  Panther's.

## Unverified

Written without credentials, tested only against a fake server built from the doc. The doc contradicts itself in
places, so the parser accepts both variants: channel `trade`/`trades`; `last_trade_price`/`last_price`;
book `qty`/`quantity` (and `size` on REST); `prev_seq_id`/`pre_seq_id`. Open questions to confirm on the
first live run:

1. Whether the REST signature covers the query string. The code signs `ts + GET + path?query` (as in the
   Coinbase and OKX APIs this one resembles). If REST returns signature errors, sign the bare path instead.
2. Whether `prev_seq_id` chains cleanly on a depth-20 subscription; a false gap would cause a reconnect loop.
3. Whether the `/ohlc` range is inclusive of a candle whose `close_time` equals the range end.

## Consequences

- New folders `panther/<SYMBOL>/spot/` with `bbo`, `trades`, `depth`, `orderbook_rest`, `kline_1m_rest`.
- Candles for quiet pairs (for example `USDT-HKD`) will have gaps: the doc says periods without trades are missing.
- Each symbol's REST order book refreshes every few seconds, not every 200 ms, because of the 2 rps budget.
