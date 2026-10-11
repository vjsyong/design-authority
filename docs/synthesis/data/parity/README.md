# Compile parity fixtures

Baselines captured **2026-10-11** at commit `3eb576a`, from the
pre-unification tools, before they were replaced by shims:

- `compile-<src>/` — the output of the old hardcoded compiler
  (`docs/synthesis/tools/compile_pack.py` with its `build_wink` / `build_leader`
  / `build_dominion` functions) for each of wink / leader / dominion: the full
  eight-file pack (records, golden, scoring, manifest).
- `codify-<src>/expected/` + `meta.json` — the output of the old codifier
  (`tools/apply_proposals.py` including its hardcoded `SUMMARY` dict) applied
  to the compile baseline plus the workspace `examples/cadence-<src>`.
  `meta.json` records the `codified_at` timestamp the old tool wrote
  (injected into the new engine run, so runs are deterministic) and the
  expected report.

`tools/compile_parity.py` re-compiles everything through
`tools/da_compile.py` and byte-compares the results; it runs inside
`tools/check.sh`. The fixtures are frozen evidence — there is deliberately
no `--update` flag. A divergence means the unified compiler changed
behaviour these baselines pin.
