# Round 2 · 04 — Authority CI record

Run 2026-10-08. Every claim below is an executed command result, reproducible
from the committed tree.

## 1 · Triage side (snapshot commit `2c701d2`, branch `evolution/0.13-experiment`)

Command chain: `python3 build.py core` → `build.py tokens` →
`tools/build_icons.py` (version banner regeneration; per the review, diffs
are version-string-only — restated as "no rule changes; generated banners
regenerate") → `python3 build.py check` → `python3 tools/verify.py` →
`python3 tests/browser/run.py`.

| gate | result |
|---|---|
| repo self-check (`build.py check`) | **69 tests OK** (release version sync, core stylesheet sync, tokens, rename sweep, lint catalogue, brand assets, icon package 174 icons) |
| component matrix | **38 components verified selector-by-selector** (skip included; verify `.skip`, `.skip:focus`) |
| strict lint | 46 files, 0 errors, 0 warnings, **spec score 100/100** |
| browser suite | **248/248 assertions across 10 fixtures** |
| UI baseline | **30 captures match `metrics/ui-baseline.json` (zero drift)** |

The review ran the same gates independently on its own snapshot copy and
reached identical results before this implementation (see `03-review.md` §1).

## 2 · Authority pack build

`tools/build_pack_triage.py --snapshot ~/triage-design-system-evo --out
packs/triage-evolution --allow-drift`

- Counts: artifacts **75 → 76**, components **37 → 38**, recipes 17, rules
  15, fallbacks 3, prohibitions 9, patterns 7, guidelines 13, examples 7,
  token_sets 6, references 5.
- One recorded warning (disclosed): *snapshot commit ≠ expected* (the
  pinned-commit guard; the evolution snapshot is intentionally different —
  same disclosure as round 1).
- Drift: `--check --allow-drift` → *pack is up to date (9 files checked)*.
- Overlay: `curation/evolution.json` extended with round-2 release metadata
  and provenance for `component/skip`, `component/sheet-end`,
  `recipe/row-actions`, `pattern/dashboard` (round-1 blocks untouched).

## 3 · Authority batteries (against the built pack)

| battery | baseline 0.13.0 | candidate 0.13.1 |
|---|---|---|
| 18-probe battery | — | **3 changed (the three targets), 15 identical** (`data/round2/baseline-resolves-r2.json` vs `candidate-resolves-r2.json`) |
| convergence battery (round-1, 34 hard assertions) | 34/34 | **34/34 OK** (watch: *"remove a reviewer"* UNDEFINED — the round-1 adjudication, unchanged) |
| evolution golden set | 23/23 | **27/27** (4 new cases: skip, sheet-end, row-actions, nav lock) |
| pinned golden set (56 cases, run against pinned pack) | 56/56 | **56/56** (untouched) |
| dispute replay vs evolution pack | 4 standing | **0 standing / 4 cleared** (`data/round2/dispute-replay-evolution.json`) |
| dispute replay vs pinned pack | 4 standing | **4 standing** (frozen; `dispute-replay-pinned.json`) |
| design-authority `tools/check.sh` full gate | green | **green** (kernel 34/34, goldens 56/56, sweep 134/134, MCP smoke 25/25, dispute fixture 4/4, semantic self-test, concept-site gate) |

## 4 · Review-executed surface (cross-check)

The adversarial review ran 112 probes over 10 pack variants before
implementation: 22 improvements, 1 downgrade (the accepted margin-clog
transition), convergence 34/34 and goldens 23/23 on every variant. Its raw
probe batteries are kept in `data/review-scratch/results/`.

## 5 · Watch items (carried, not defects)

1. *"open the action menu for selected rows"* flips COMPOSE
   bulk-actions → row-actions (ambiguous phrasing; defensible row-menu
   reading; keep on the watch battery).
2. *"a link that jumps past the navigation"* and *"a link to jump past the
   navigation"* move false-RESOLVED nav-item → UNDEFINED (margin-clog class;
   safer class; accepted, do not chase with more aliases).
3. Kernel note (report-only, kernel frozen): the UNDEFINED `why` text cites
   the score threshold but does not surface margin failures.
