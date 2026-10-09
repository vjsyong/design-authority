# x05 · Blind review — results

- **Date (ratings window):** 2026-10-09 06:02–06:04 UTC · scored 2026-10-09T08:26:37+00:00
- **Reviewer:** "Sean Yong" — single reviewer (owner). Blind: the code → (condition, chain, handoff) mapping stayed sealed in `blindset/key.json` (server-side only) until this scoring pass; item order + left/right orientation were randomized with a recorded seed.
- **Instrument:** driftexp (capability-gated, `driftexp.seanyong.xyz`) — 15 items = 12 matched-region comparisons (4 handoffs x 3 chains) + 3 whole-screen seed→H1 pairs; one narrow 1–5 question per screen. Scale: 1 = clearly different · 3 = unsure · 5 = clearly the same (higher = less drift).
- **Evidence hashes:** ratings.jsonl `fdbb5b9e8cf90214…` · key.json `0b091fec08aba269…` (full in `blind-review.json`)

## Deviations from pre-registration (logged)

1. **Single reviewer** — the plan specifies three predetermined reviewers with per-comparison means across them (plan §5.2). Executed with one reviewer. All values are single-rater; **reduced precision** label applies.
2. **Calibration not run** — the controlled variant set (instrument discrimination) was never assembled (reviewer confirmation skipped, I-15). No discrimination estimate accompanies these numbers.
3. Duplicate submissions R07, R08 (identical values, idempotent re-submit) — deduplicated, no effect. One abandoned start ("Sean", no answers) precedes the completed run.

## Ratings (single reviewer)

Matched-region comparisons (the drift-sensitive measure):

| Handoff | A | B | C | C−B | C−A |
|---|---|---|---|---|---|
| H1 · list-controls vs seed tag-filter | 3 | 3 | 3 | +0 | +0 |
| H2 · analytics view vs card | 2 | 4 | 4 | +0 | +2 |
| H3 · palette vs card | 1 | 4 | 4 | +0 | +3 |
| H4 · wizard vs card | 4 | 3 | 4 | +1 | +0 |

Whole-screen pairs (seed → H1): **A 4 · B 3 · C 4**

Per-item detail: `blind-review.json`.

## Aggregates

| Statistic | A | B | C |
|---|---|---|---|
| Matches mean (n=4) | 2.5 | 3.5 | 3.75 |
| Matches median | 2.5 | 3.5 | 4.0 |
| All-items mean (n=5) | 2.8 | 3.4 | 3.8 |
| All-items median | 3 | 3 | 4 |

- **Trajectories (matches):** A 3→2→1→4 (collapses at H2–H3, recovers at H4) · B 3→4→4→3 · C 3→4→4→4.
- **D1 blind corroboration input** (plan: "blind median difference of at least 1.0 point in the same direction"):
  - all-items read: median C − median B = **+1.0** → at the threshold.
  - matched-regions-only read: **+0.5** → below the threshold.
  - Both reads favor C; single-rater → reduced precision regardless.
- **Ordering:** C > B > A on means; C ≥ B at all four handoffs (strictly above at H4); B ≥ A at three of four.

## Status

Blind layer recorded (with the deviations above). Pending in the analysis half: objective fidelity scoring (primary gate) + correction-burden / cross-component / mechanism sections, calibration, then the program report.
