# Round 2 · 02 — Candidate changes

Four candidates, continuing the `proposals/evolution/` series (cand-01…05
were round 1). Every candidate was pre-tested by execution on a scratch
copy of the evolution pack; the pre-test battery lives in
`docs/evolution/data/r2-scratch/`. Final acceptance is conditional on the
independent adversarial review (`03-review.md`) and the post-build battery
(`04-authority-ci.md`).

| # | candidate | layer | need |
|---|---|---|---|
| cand-06 | `cand/06-skip-catalogue` — catalogue `component/skip` | triage-snapshot + curation | N-1 |
| cand-07 | `cand/07-sheet-end-panel-vocabulary` — panel phrasings on sheet-end | curation | N-2 |
| cand-08 | `cand/08-row-actions-chevron` — chevron phrasings in recipe needs | curation | N-4 |
| cand-09 | `cand/09-status-chip-codification` — name the classes, alias pending battery | curation | N-5 |

Design notes:

- cand-06 is the round's only triage-snapshot change: one additive
  `spec/states.json` entry (class `.skip`, minimal states/verify/a11y
  contract, mirroring the sheet-end level of detail), a VERSION bump to
  `0.13.1-experiment`, a CHANGELOG entry, and the curation side
  (component-notes, aliases, docs-map). No CSS is added; the class already
  ships.
- cand-07 and cand-08 are pure curation vocabulary edits, both verified on
  the scratch pack to fix their target queries while the 14-probe
  regression battery stayed identical.
- cand-09 is note-only by default; its alias addition is explicitly
  conditional on the battery (see candidate file).
- N-3 (state label) produces no candidate: the evolution line already
  answers with the pack's own golden-consistent recipe.

Forbidden by construction (checked in review): kernel files untouched;
pinned pack untouched; no threshold, margin or precedence change; no new
CSS or visual language; no alias that a delete/regression probe flips.
