# Authority Evolution Experiment — report package

**Date:** 2026-10-07 · **Status:** complete · **Repo:** `github.com/vjsyong/design-authority` (master `d43f80a`) · **Release:** Triage Authority `0.13.0-experiment` (snapshot branch `evolution/0.13-experiment` @ `32e680b`)

> **Round 2 (2026-10-08):** the disputed-resolution follow-through is in
> [`round2/`](round2/06-final-report.md) — release `0.13.1-experiment`
> (snapshot `2c701d2`): skips catalogued, slide-over and row-actions
> vocabulary fixed, status chips named; all four seeded disputes replay
> 0-standing on the evolution line (frozen pinned pack keeps its 4/4 gate).
>
> **Round 3 (concept, not started):** collaborative aliasing/tagging —
> consumer filings nominate function-scope tags and aliases; see
> [`round3/00-concept-collaborative-aliasing.md`](round3/00-concept-collaborative-aliasing.md)
> (logged 2026-10-09; feasibility only, no experiments).

This package consolidates every report and raw measurement from the Authority
Evolution Experiment: taking the gap evidence filed by downstream agents
against Triage 0.12.1, converting it through a governed upstream process into
an experimental authority release, and re-testing it against fresh agents.

**Headline:** the loop closed — all three consolidated needs now resolve to
sanctioned answers, zero gaps were re-filed in three fresh runs, and the
release added **0 new primitives and 0 new CSS** (+2 beta catalogue entries,
+2 recipes, +1 extension).

## Reading order

| file | what it is |
|---|---|
| `00-gap-evidence.md` | P1 — 8 raw gap records → 3 consolidated needs (4/3/1 runs) |
| `01-triage-decisions.md` | P2 — upstream triage: what was tried first, why extensions were held to doc/recipe level |
| `02-candidates.md` | P3 — the five candidate changes (+ per-candidate JSON in `proposals/`) |
| `03-review.md` | P4 — independent adversarial review (all REVISE; executed verification) |
| `04-authority-ci.md` | P5 — full CI record: gates, convergence 34/34, goldens, second-pass tuning |
| `05-migration.md` | P8 — pointing the new authority at old implementations (7 usages: 5 direct, 2 manual) |
| `06-final-report.md` | P10 — final synthesis, inflation, threats to validity, the research question answered |
| `proposals/` | the five machine-readable candidate files (`cand-01…05`) |
| `data/` | raw measurements: baseline resolves (0.12.1), evolution resolves (0.13), inflation, migration checks, downstream re-run records |
| `release/` | the published pack's receipt (`BUILD.json`), provenance overlay (`evolution.json`), 23-case golden set |
| `phase-1-context/` | the first experiment's reports (A/B/C benchmark: production report, synthesis, standalone report) — background for the evolution round |

## Where things live upstream

- Full repository: `~/design-authority` — evolution work under `docs/evolution/`, `proposals/evolution/`, `packs/triage-evolution/`.
- Fresh re-run artifacts: `benchmark/runs/e1…e3` (locally archived, gitignored).
- Pinned authority (0.12.1): `packs/triage/` — byte-untouched by this experiment.
