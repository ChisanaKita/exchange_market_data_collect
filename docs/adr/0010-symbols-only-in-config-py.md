# 0010. Target symbols are set only in config.py

- Status: Accepted
- Date: 2026-11-26
- Amends: [0002](0002-config-is-the-single-symbol-source.md) ("`config.py` / the `*_TARGET_SYMBOLS` env
  vars"), and the env var names in [0009](0009-bitget-spot-and-perp-lists-and-v3-coin-margined.md)

## Context

ADR 0002 made config the single source of symbols, but every list could still be overridden by a
`*_TARGET_SYMBOLS` environment variable, usually set in the server's `.env`. Overrides make the symbols
being collected differ from the ones in git without leaving a trace. For example, after ADR 0009 an old
`BITGET_TARGET_SYMBOLS=BTCUSDT,ETHUSDT` line would have narrowed the business's new pair list. The owner
ruled that `config.py` is the only symbol source.

## Decision

- The symbol lists in `config.py` are plain Python lists (`_symbols([...])` only upper-cases and
  de-duplicates them). No `*_TARGET_SYMBOLS` variable is read from the environment or `.env`.
- `.env.example` and the README configuration table no longer list symbol variables.
- At startup, `main.py` sends an alert-level warning naming any `*_TARGET_SYMBOLS` variable that is still
  set, so a leftover `.env` line is removed instead of being silently ignored.
- Connection settings (URLs, poll intervals, rate limits) are still read from the environment.

## Consequences

- Changing symbols needs a commit and a redeploy. That is intended: what is collected is what is in git.
- Any `*_TARGET_SYMBOLS` lines in a server `.env` stop taking effect on the release that includes this ADR.
  The startup warning names them.
