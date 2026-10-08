# Round 2 · 06 — Final report

**Date:** 2026-10-08 · **Release:** Triage Authority `0.13.1-experiment`
(snapshot commit `2c701d2`, branch `evolution/0.13-experiment`) · **Pinned
authority:** untouched (`packs/triage` 0.12.1).

## 1 · The question

Round 1 converted benchmark gaps into a governed release. Round 2 takes the
**disputed-resolution evidence** — the failure class the reviewer called
"more dangerous than UNDEFINED" — and asks whether it closes through the
same governed loop: dispute → evidence → triage → candidates → adversarial
review → implementation → CI → release.

## 2 · What closed

On the evolution line, the four seeded disputes replay as **0 standing / 4
cleared** (they remain 4/4 standing on the frozen pinned pack, by design):

1. **Skip link (false RESOLVED eliminated).** The uncatalogued `.skip` is
   now `component/skip` (status `beta`, honest per the lifecycle: no
   behavioural coverage yet), added at the triage-snapshot level with
   selector-verified focus contract. The dispute query resolves to the
   correct record (26.0) instead of falsely claiming `nav-item`.
2. **Sliding panel (mis-route eliminated).** Two aliases on
   `component/sheet-end` route slide-over phrasings to the slide-over
   component; eight collateral phrasings improved, zero false positives.
3. **Row-actions chevron (mis-compose eliminated).** Three need-phrasings
   on `recipe/row-actions` stop `recipe/bulk-actions` hijacking single-row
   chevron queries.
4. **State label (already closed).** No change: round 1's
   `recipe/status-with-text` already answers the query, consistent with the
   pack's own golden semantic.
5. **Status chips (codification).** The shipped `.status-chips` row is now
   named in `pattern/dashboard`'s summary and is searchable. The conditional
   alias was dropped after it failed its own battery (badge tie → margin
   failure → an unrelated recipe degrade) — the review caught this; the
   candidate's own rule said note-only otherwise.

Inflation: **+1 catalogue entry (beta), 0 new CSS rules, +2 aliases, +3
recipe needs, 1 summary naming, 0 kernel changes, 0 new primitives.**

## 3 · Verification

All of §2 is executed, not asserted: triage gates (69-test repo check,
38-component selector matrix, 248/248 browser assertions, zero UI-baseline
drift), pack drift check, the 18-probe battery (3 changed, 15 identical),
convergence 34/34, goldens 27/27 (four new pins), pinned goldens 56/56,
dispute replays for both packs, and the design-authority full gate. The
adversarial review ran 112 probes over 10 variants before implementation.
Details: `04-authority-ci.md`; raw data: `../data/round2/` and
`../data/review-scratch/`.

## 4 · The new finding: margin-clog

Adding the skip record removed the false RESOLVED but introduced a new
collision shape worth recording: skip's alias union now acts as a strong
runner-up on *other* nav phrasings ("a link that jumps past the
navigation": nav-item 13.0 vs skip 12.0), so the 2.0 margin rule fails and
the outcome becomes UNDEFINED. That is the **safer** class (the previous
answers were false RESOLVEDs), and it was accepted deliberately rather than
chased with more aliases. Related kernel observation (report-only, kernel
frozen): UNDEFINED's `why` cites the threshold but does not surface margin
failures; if a future spec round touches diagnostics, this is a candidate.

## 5 · Threats to validity

One reference system (Triage) and one evidence line (this project's
experiments); n = 4 disputes; one adversarial reviewer (clean context,
executed verification); one watch item carried ("open the action menu for
selected rows"); the fixes live on the experimental evolution line — the
pinned authority consumers use today is unchanged, so downstream benefit is
deferred until the evolution line is promoted.

## 6 · Deliverables

- Release: `packs/triage-evolution` @ 0.13.1-experiment (receipt
  `BUILD.json`, overlay `curation/evolution.json`, 27-case golden set) and
  triage commit `2c701d2`.
- Evidence and process: `docs/evolution/round2/00…06` (this package),
  candidates `proposals/evolution/cand-06…09.json`.
- Data: `docs/evolution/data/round2/` (batteries, dispute replays),
  `docs/evolution/data/review-scratch/` (reviewer batteries + hash
  manifests).
- Fixture loop closed: `docs/experiments/disputes/` still pins the pinned
  pack's 4 standing disputes (`tools/check.sh` gate unchanged); the same
  fixture replays 0-standing against the evolution line.
