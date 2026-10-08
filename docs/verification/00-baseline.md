# 00 · Baseline — frozen before measurement

**Captured 2026-10-08 ~03:40 UTC, before anything was touched.** Raw data:
`raw/baseline-hashes.json` (per-file hashes for every frozen artifact, plus a
resolution snapshot). Principle honoured: *do not repair current apps before
measuring them* — nothing under measurement was modified before this capture.

## Immutable references

| item | reference |
|---|---|
| Repository revision | `2a913daaf6576df4c9e0074f09f49a614d79ead8` — **tag `v0.2.0`** |
| VERSION | `0.2.0` |
| pack wink | rollup `87a9c902…0eb59` (10 files) |
| pack leader | rollup `aa518528…f063e9` (10 files) |
| pack dominion | rollup `6b723eb5…08454` (10 files) |
| build examples/cadence3-wink | rollup `8ce130a1…6462` (40 files) |
| build examples/cadence3-leader | rollup `19789e8d…9835` (15 files) |
| build examples/cadence3-dominion | rollup `5b54bf0d…2911` (10 files) |
| build examples/cadence-wink (v1) | rollup `b97aa752…d80` (22 files) |
| build examples/cadence-leader (v1) | rollup `0d86b60a…3b9` (22 files) |
| build examples/cadence-dominion (v1) | rollup `8b00f8fe…fc7` (18 files) |
| review data stress-verdicts.json | sha256 `1e52fd0c…32fd` (owner verdicts, 14) |
| review data feedback.json | sha256 `c9ed477c…64d7` (Gate 2 verdicts) |

Rollups = sha256 over the sorted `relpath sha256(file)` list; full per-file
hashes in `raw/baseline-hashes.json`. Verify anytime:

```bash
python3 docs/verification/tools/baseline.py   # recompute; diff against the raw file
git rev-parse HEAD                            # expect 2a913da (tag v0.2.0)
```

## Resolution behaviour snapshot (10 golden asks per pack)

Recorded in `raw/baseline-hashes.json → resolution_snapshot` (outcome +
resolution id per ask). Example — wink: `RESOLVED component/action-pill`,
`CONFLICT` (×2), `FALLBACK fallback/platform-controls`, `UNDEFINED`, …;
leader: 5 × RESOLVED, 3 × CONFLICT, `FALLBACK fallback/ruled-panel`,
`UNDEFINED`; dominion: 4 × RESOLVED, `COMPOSE recipe/retire-confirm`,
3 × CONFLICT, `FALLBACK fallback/large-selection`, `UNDEFINED`.

## What the experiment added after this baseline (and why it is safe)

- `packs/{wink,leader,dominion}/verification.json` — **additive optional
  artifacts** of the verification experiment. They do not modify authority
  semantics, do not bump any pack version, and every 0.2.0 kernel path still
  loads the packs unchanged (drift gate exercises only generated files; the
  kernel reads specific entrypoints and ignores the new file). No authority
  was redesigned — per the brief, this is a verification experiment.
- `tools/da_verify.py`, `docs/verification/tools/*` — new, additive tooling.
- `packs/*/…/verification.json` results published into each build's
  `_evidence/verification/` (evidence output; e.g.
  `examples/cadence3-wink/_evidence/verification/wink-verification.json`).
- `examples/cadence3-wink` gained the **v3.1d lens section** (app.js/app.css
  extended after measurement to display verifier results; the *measured*
  state remains the rollup above — the addition is presentational and the
  clean conformance checks were re-run against it).
- The lens/provenance annotations in `examples/cadence3-wink` are the v3.1c
  inspector (captured in the build rollup above); the verifier uses marks only
  as locator hints, never as proof (see `01`).

## Scope note (which Cadence builds)

The brief names *cadence-wink / cadence-leader / cadence-dominion*. Those
names exist twice in the repo: the **v1 stress builds** (`examples/cadence-*`)
and the **v3 builds on the codified 0.2.0 authorities** (`examples/cadence3-*`).
The experiment verifies the **v3 trio**: they are the completed builds the
current authorities actually claim to govern (a pack-version alignment), and
the v1 builds predate codification — verifying them against post-hoc contracts
would mix eras and manufacture false violations from structural drift.
The v1 trio remains available as a follow-up datapoint (noted in `07`).
