# 0002. Config is the single source of truth for symbols

- Status: Accepted
- Date: 2026-10-15
- Supersedes: decisions 1 and 2 of [0001](0001-per-exchange-symbols-and-hashkey-site-naming.md)

## Context

After ADR 0001 each collector still carried `UNIFIED_TO_EXCHANGE` / `EXCHANGE_TO_UNIFIED` tables
that translated configured "unified" names (`BTCUSDT-PERPETUAL`) into exchange-native ones
(`BTCUSDT`, `BTC_USDT`, `BTCUSDC`). Which names a config value actually meant depended on a table
hidden in each collector, several unified names could collapse to one exchange symbol (OSL), and
unmapped symbols were silently dropped (Bitget/Gate) or passed through (HashKey/OSL).

## Decision

- `config.py` / the `*_TARGET_SYMBOLS` env vars hold **exchange-native** symbols and are the only
  place symbols are defined.
- Collectors use them verbatim for WS subscriptions, REST polling and the output folder/`symbol`
  field. There are no mapping tables, no `to_unified_symbol`, and no filtering or strict mode.
- `config._parse_symbol_list` still upper-cases and de-duplicates values.

## Consequences

- **Breaking output change for Bitget, Gate and OSL.** Folders and the `symbol` field change from the
  unified names to native ones: Bitget `BTCUSDT-PERPETUAL` -> `BTCUSDT`, Gate `BTCUSDT-PERPETUAL` ->
  `BTC_USDT`, OSL `BTC-PERP` -> `BTCUSDC`. HashKey names were already native.
- Cross-exchange comparison by `symbol` is now the consumer's job.
- A wrong symbol is no longer dropped by the collector; the exchange rejects it and the error shows
  in the logs. An old env override such as `BITGET_TARGET_SYMBOLS=BTCUSDT-PERPETUAL` must be updated.
- Bitget (`BTCUSD` -> COIN-FUTURES) and Gate (`BTC_USD` -> btc settle) still derive routing from the
  native symbol inside the collector.
