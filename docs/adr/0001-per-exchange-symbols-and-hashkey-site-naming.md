# 0001. Per-exchange target symbols and HashKey site naming

- Status: Accepted
- Date: 2026-10-15

## Context

A single global `TARGET_SYMBOLS` list no longer fits: HashKey HK, Global and MENA list different
instruments, and Bitget, Gate and OSL each support a different subset. HashKey is also now three
collectors (Global, HK, MENA) that share one WS/REST implementation but differ by host and `site`
parameter.

## Decisions

1. **Per-exchange symbol lists.** Each collector has its own `<EXCHANGE>_TARGET_SYMBOLS` setting
   (`HASHKEY_GLOBAL_`, `HASHKEY_HK_`, `HASHKEY_MENA_`, `BITGET_`, `GATE_`, `OSL_`). Values are
   upper-cased and de-duplicated on load, and again after unified-to-exchange mapping
   (`BaseExchangeCollector.map_target_symbols`), because several unified names can map to one
   exchange symbol (OSL: all of `BTCUSDT-PERPETUAL`, `BTCUSD-PERPETUAL`, `BTC-PERP` map to `BTCUSDC`).
2. **Strict vs pass-through mapping.**
   - Bitget and Gate are *strict* (`STRICT_SYMBOL_MAPPING = True`): unmapped symbols are dropped with
     a warning, because their WS channel/instrument type is derived from the mapped symbol and an
     unmapped one would only produce subscription errors and wasted REST budget.
   - HashKey (all sites) and OSL *pass through* unmapped symbols as exchange-native names: HK and
     MENA list many spot pairs that are intentionally not in the perpetual mapping table.
3. **HashKey exchange names.** The HK collector keeps the historical name `hashkey`; Global is
   `hashkey_global`; MENA is `hashkey_mena`. This sets the output directory and the `exchange` field.
4. **One shared HashKey base.** `HashkeyCollector` holds all WS/REST logic and is not instantiated
   directly; sites are thin subclasses that set `exchange_name`, `WS_SUBSCRIBE_EXTRA` and
   `REST_EXTRA_PARAMS`.

## Consequences

- **Historical data caveat:** before 2026-10-15 the `hashkey` name was produced by the collector that
  pointed at HashKey **Global** (`api-glb`). From the cutover, `hashkey/` holds **HK** data and Global
  moves to `hashkey_global/`. Downstream consumers must treat `hashkey/` before and after the cutover
  as different venues.
- Legacy `HASHKEY_*` env vars (no site prefix) are still read as fallbacks, but only for Global.
- HK and MENA share `api-pro.hashkey.com` from one IP with independent rate limiters. Their combined
  REST rate must stay under the documented 5 rps query limit (default 1.5 + 1.5 = 3 rps).
- With 12 HK symbols at 1.5 rps each symbol's REST snapshot is refreshed roughly every 8 s; WS carries
  the real-time data.

## Rejected alternatives

- **Rename HK to `hashkey_hk`:** cleaner, but silently changes output paths for the venue the data
  was already stored under.
- **Pass-through everywhere:** simplest, but turns a typo in a Bitget/Gate list into a permanent
  error loop.
- **Strict everywhere:** would require enumerating every HK/MENA spot pair in the mapping tables.
