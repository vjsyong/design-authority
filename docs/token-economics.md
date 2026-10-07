# Token economics — baseline measurement and tracking policy

**Status:** baseline measured 2026-10-07 (post-hoc, first analysis); tracking
enabled for all future runs. Reproduce with:

```bash
python3 benchmark/harness/token_report.py            # all runs
python3 benchmark/harness/token_report.py b2 c2 e1   # specific runs
```

## Question

Do agents consume fewer tokens working against the **active authority** than
against the **static kit**?

## Method

Every opencode transcript records per-step usage (`step_finish` events:
`{input, output, reasoning, cache{read,write}, total}` + provider `cost`).
`token_report.py` (and `run.json → opencode.tokens` for runs after
2026-10-07) aggregates per session:

- **sum_total** — cumulative tokens across all steps, including cache reads
  (the agent loop rereads its growing context each step; this is the volume
  figure).
- **cost** — provider-billed USD (cache discounts applied).
- **peak** — largest single-step total (≈ peak context window reached).
- **output+reasoning** — generated tokens only.

## Result (medians per condition)

| | A naive | B static kit | C authority | E evolution pack |
|---|---|---|---|---|
| runs (clean) | a2–a4 | b1–b4† | c1–c4 (c2b partial excluded) | e1–e3† |
| sum_total | 2.9M | 8.8M | 8.9M | 11.7M |
| cost | $0.050 | $0.089 | $0.082 | $0.097 |
| peak context | 98K | 203K | 197K | 210K |
| output+reasoning | 58K | 67K | 58K | 63K |
| tokens / step | 59K | 171K | 139K | 153K |

† b3/b4/e2 flagged (see production/evolution reports); c2b is a partial
(killed) run excluded from medians but shown by the tool.

## Verdict

**No meaningful difference between authority and static kit.** C lands within
noise of B on every dimension (cost −8%, peak −3%, sum_total ≈ equal; C's
apparent advantage shrinks to ~nothing when the partial run is excluded).
The only large contrast: **B and C both burn ≈3× the tokens of A** — doing
design-system-conformant work costs more steps and context than a naive build,
regardless of how the knowledge arrives.

Mechanism: token volume is dominated by session length, not retrieval. The
kit is small (~39 KB / ~10K tokens total) and read selectively; MCP queries
replace file reads roughly 1:1. The authority's value proposition is
governance at **cost parity**, not token savings.

## Caveats

- Post-hoc analysis, not pre-registered at run time; n = 3–5 clean runs per
  condition, one model (deepseek-flash), one app; flagged runs vary in
  completeness. Descriptive only — no significance claim is made.
- `sum_total` double-counts context by design (cache reads); prefer `cost`
  and `peak` for spend/context claims.
- For any future token claim: pre-register the metric (recommend: median
  `cost` and median `peak` over ≥5 clean runs per condition, flagged/partial
  runs excluded and disclosed).

## Tracking

- `benchmark/harness/run_condition.py` now records `opencode.tokens` in every
  `run.json` (steps, totals, cache split, peak, cost).
- `benchmark/harness/token_report.py` gives the cross-run view; group medians
  by run-id prefix.
