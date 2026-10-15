# 0003. OSL collector on the v5 public API

- Status: Accepted
- Date: 2026-10-15

## Context

OSL moved market data to API v5 (`wss://stream-hk.osl.com/ws/v5/public`,
`https://trade-hk.osl.com/api/v5`). The old collector spoke the v1 Binance-style protocol
(`SUBSCRIBE` / `btcusdc@depth`, `/openapi/v1/depth`) which does not exist on v5. The v5 WS channels
are `ticker`, `books5`/`books15` and `trade`; the documented REST market-data endpoint is `/kline`
(there is no documented REST order book).

## Decision

| v5 source | Category written | Notes |
|---|---|---|
| WS `ticker` | `bbo` | bid/ask price + size, plus `last_price`; 24h stats stay in `raw` |
| WS `books15` | `depth` | full snapshots of up to 15 levels, no deltas |
| WS `trade` | `trades` | one row per trade; the first push is a snapshot of recent trades |
| REST `/kline` (limit 1) | `kline_1m_rest` | latest 1m candle per poll, mirrors the `*_rest` snapshot convention |

- All OSL instruments are written as `market_type: spot` (v5 `instType` is `SPOT`). The old v1
  collector labelled `BTCUSDC` as `futures` only because it was mapped from `BTC-PERP`.
- Symbols come from `OSL_TARGET_SYMBOLS` verbatim ([0002](0002-config-is-the-single-symbol-source.md)).
  The default is `BTCUSD,USDTUSD`; `BTCUSDC` does not exist on v5.
- The base REST hook is renamed `_fetch_and_write_rest` because OSL's REST source is not an order book.
- REST errors arrive as HTTP 200 with `{"code": ..., "msg": ...}` and are raised so they are logged
  instead of being stored as data.

## Rate limits

OSL v5 allows 1800 weight per minute per source IP (public endpoints included), 1 weight per call, so
about 30 requests/s. `OSL_REST_RATE_LIMIT_RPS` defaults to 2.0 (about 7% of the quota). 429 means
slow down (honour `Retry-After`); 50 cumulative 429s in a minute cause a 60 s ban where every request
returns 418. The shared REST poller therefore backs off on both 429 and 418 and uses `Retry-After`
when present (previously 429 only, fixed 60 s). The doc gives no WebSocket message-rate limit; the
public WS allows 100 connections per IP and drops connections idle for 60 s.

## Consequences

- **Breaking for OSL consumers:** folders become `osl/<SYMBOL>/spot/`, the REST category changes from
  `orderbook_rest` to `kline_1m_rest`, and there is no WS `kline_1m` (the v5 docs list no kline channel).
- WS reconnects re-deliver the recent-trades snapshot, so `trades.jsonl` can contain duplicate
  `trade_id`s; consumers should de-duplicate on `trade_id`.
- Unknown symbols get no WS error from OSL (the subscribe is acked) and only show up as REST kline
  errors in the log.
