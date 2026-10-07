# Triage Authority Pack — 0.13.0-experiment (authority-evolution release)

**Experimental.** Generated from the candidate snapshot
`vjsyong/triage-design-system @ 32e680b` (branch `evolution/0.13-experiment`,
version `0.13.0-experiment`), which is `e374f38` (0.12.1) plus the
authority-evolution changes. This pack sits **beside** the pinned
`packs/triage` (0.12.1) and does not alter it — both are available for
comparison.

Why this release exists: downstream coding agents filed gap evidence against
0.12.1 (4 independent runs for a reviewer/entity assignment picker, 3 for
determinate background-job progress, 1 for a reason-bearing rejection flow).
An upstream triage + adversarial review converted that evidence into the
smallest changes that close the gaps — no new visual language, no new
primitives. Full trail: `docs/evolution/00…04` in the design-authority repo.

## What changed vs 0.12.1

| | 0.12.1 | 0.13.0-experiment |
|---|---|---|
| components | 35 | **37** (+`select`, +`progress`, both `beta`) |
| recipes | 15 | **17** (+`assign-picker`, +`job-progress`) |
| extended | — | `high-stakes-confirm` (+reason-bearing coverage) |
| vocabulary | — | select/progress/assign/reason aliases + needs |

Every new/changed entry carries a `provenance` block (triggering gap IDs,
review decision, source branch, tests). The receipt (`BUILD.json`) carries the
`release` metadata. `curation/evolution.json` is the overlay that produces
both — a no-op for the pinned pack.

## Build / gate

```bash
python3 tools/build_pack_triage.py --snapshot ~/triage-design-system-evo \
    --out packs/triage-evolution --allow-drift        # build
python3 tools/build_pack_triage.py --snapshot ~/triage-design-system-evo \
    --out packs/triage-evolution --check --allow-drift # drift gate
python3 tools/evolution_convergence.py                 # 34/34 contract battery
python3 tools/da.py --pack packs/triage-evolution golden --file packs/triage-evolution/golden.json
```

Verified: triage gates (build.py check 37-component matrix, strict lint
100/100, browser suite 248/248, UI baseline zero-drift), convergence 34/34,
goldens 23/23 (evolution) — full record in `docs/evolution/04-authority-ci.md`.
