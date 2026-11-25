# 0009. Bitget spot and perp lists, and v3 for coin-margined perpetuals

- Status: Accepted
- Date: 2026-11-25
- Amends: the Bitget routing bullet of [0002](0002-config-is-the-single-symbol-source.md); the
  `(exchange, symbol)` freshness key of [0007](0007-telegram-alerts.md)

## Context

The business asked for 19 Bitget spot pairs and 24 perpetuals (`bitget.txt`). Checked against the live
Bitget API on 2026-11-25:

- Nine symbols, such as `BTCUSDT`, are in both lists. They are different instruments with the same native
  name, but `BITGET_TARGET_SYMBOLS` was one flat list and the collector wrote everything as `futures`.
- `HYPEUSDC` does not exist. The USDC-margined perpetual is `HYPEPERP` (USDC-FUTURES).
- `BTCUSD` returns "The symbol has been removed". The coin-margined perpetual is now `BTCUSD_CM`. The v2
  COIN-FUTURES contract list is empty, and the v2 WebSocket rejects `BTCUSD_CM` (30001 "doesn't exist").
  It is only served by the v3 (UTA) WebSocket, `wss://ws.bitget.com/v3/ws/public`, with lowercase
  `instType: coin-futures` and `topic`/`symbol` arguments, and by the v3 REST orderbook.
- The freshness monitor keyed on `(exchange, symbol)`. Fresh futures `BTCUSDT` data would have hidden a
  silent spot `BTCUSDT` feed.

## Decision

- **Two lists, two collectors.** `BITGET_SPOT_TARGET_SYMBOLS` and `BITGET_PERP_TARGET_SYMBOLS` replace
  `BITGET_TARGET_SYMBOLS`. main.py runs one `BitgetCollector(market="spot"|"perp")` per list. Both write
  under exchange `bitget`, with `market_type` `spot` or `futures`, so the folders are
  `bitget/BTCUSDT/spot/` and `bitget/BTCUSDT/futures/`. We rejected a single list with a market prefix
  (`SPOT:BTCUSDT`): the prefix would leak into the output folder or need translation, which ADR 0002 removed.
  We also rejected one collector that holds both lists, because `BaseExchangeCollector` keys its REST
  pollers by symbol, and the same symbol in both markets would collide.
- **Perpetuals are routed by native suffix**, as ADR 0002 already did for `BTCUSD`: `_CM` goes to
  coin-futures on the v3 WebSocket, `PERP` to USDC-FUTURES, and anything else to USDT-FUTURES. The other
  routes stay on v2. REST depth for every market uses `GET /api/v3/market/orderbook`.
- **Only `_CM` uses the v3 WebSocket.** We did not move the other symbols to v3. Their `raw` payloads would
  change shape (short field names `a`/`b`/`p`/`v`/`S`/`T`, `topic` instead of `channel`) for data that is
  already being collected. The v3 handler maps kline, publicTrade, books and books1 onto the same
  normalized records as v2.
- **WebSocket connections carry at most 12 symbols** (48 channels). Bitget advises fewer than 50 channels
  per connection.
- **Freshness is keyed on `(exchange, market_type, symbol)`.** Each collector reports its streams through
  `monitored_streams()`, using `get_market_type()` (the base default is `futures`). Alerts read
  `BTCUSDT (spot)`.
- **`BITGET_REST_RATE_LIMIT_RPS` defaults to 5 per collector** (10 in total, against Bitget's 20 req/s/IP).
  With 2 rps spread over 24 perpetuals, each symbol would get a REST snapshot only every 12 seconds.

## Consequences

- **Breaking config change.** `BITGET_TARGET_SYMBOLS` is ignored. If it is still set, startup logs a warning
  that is sent as an alert.
- **Output changes.** Spot data appears under `bitget/<symbol>/spot/`. Coin-margined data moves from
  `BTCUSD` (which no longer works) to `BTCUSD_CM`. The v2 kline `close_time` was `candle[7]`, which is the
  USDT volume, not a time. It is now `open_time + 59999`. Depth and BBO `version` were always empty
  because the field is `seq`, not `seqNum`. Both bugs are fixed for all Bitget data from this release on.
- v3 coin-futures kline `volume` is the base-currency volume (BTC), as on v2.
- A new suffix-routed product (for example a delivery contract such as `BTCCMZ26`) needs a new route in
  `collectors/bitget.py:route_for`. An unknown symbol falls through to USDT-FUTURES, and Bitget's rejection
  shows in the logs.
