# 10 · The Triage verification contract (F-2)

Status: **authored, calibrated, shipped** (2026-10-11). Response to the
adoption test finding F-2 (`docs/experiments/08-adoption-test.md`): the
workflow's `da verify` step aborted because the Trips pack shipped no
`verification.json`. What now ships:

- **`verification.json` in the pack** (source: `docs/synthesis/triage/
  verification.json`; shipped by the generator, covered by the drift gate at
  17 files): contract 0.2, 14 checks.
  - 10 mechanical: square cards, square buttons, primary fill pairing
    (ink on paper; paper on the ink bulkbar — both token pairings legal, any
    other fill is a violation), Geist body register, badge label tier
    (13px + uppercase, TDS016), mono register for identifiers, status chips
    nowrap, keyboard focus rings (tab-walk), empty-state action anatomy,
    provenance-record fields.
  - 4 explicit REVIEW entries (armed-delete-inline on surfaces the walk
    cannot reach, voice object-naming, motion token discipline, claim
    traceability). REVIEW is surfaced as REVIEW_REQUIRED and never faked
    into PASS.
  - Selector-absent targets report UNVERIFIABLE (with the selector named),
    never PASS, so partial surfaces cannot fake coverage.
- **Calibration matrix** (clean builds, all zero violations):

| Target | PASS | UNVERIFIABLE | REVIEW_REQUIRED | VIOLATIONS |
|---|---|---|---|---|
| recipe-box consumer build (x06 adoption run, pack refreshed to 0.13.0) | 7 | 3 | 4 | 0 |
| list example | 7 | 3 | 4 | 0 |
| dashboard example | 8 | 2 | 4 | 0 |
| viewer example | 8 | 2 | 4 | 0 |

- **Mutation test** (recipe-box copy): injected `!important` radius bypass,
  off-system font, 11px badges and suppressed focus rings — the contract
  reported exactly 4 violations (square-cards, geist-body, label-tier,
  tab-ring) and no false positives. The radius bypass is realistic: the
  system enforces square corners with `*{border-radius:0 !important}`, so
  the mutation had to use `!important` too.
- **Consumer path verified**: from a bare copy of the pack (no snapshot
  available), `da verify <target> --out …` runs the contract, writes
  receipts (raw.json, summary.txt, screens/) and returns 0 violations on
  the calibrated targets.

## Calibration-discovered tool fixes (da_verify)

1. **Tab-ring sampling now accepts ink rings.** `scenario_tab_walk` only
   recognised outlines; Triage's styled checkboxes focus with a
   `box-shadow 0 0 0 3px` ring and were false-flagged. The walk now accepts
   a visible box-shadow ring (same definition as `border-ring-scan`) while
   keeping the outline path; alpha and width floors unchanged. Only turns
   false negatives into passes; existing receipts are unaffected.
2. No other tool changes were needed: the primary-fill and label-tier
   checks are pure contract refinements against real canon (the bulkbar's
   paper fill is a shipped rule, `core/base.css:151`).

## Artifacts

- Contract source: `docs/synthesis/triage/verification.json`
- Shipped: authority-triage repo `verification.json` (v0.13.0-rc1)
- Receipts: `/tmp/vcal/receipt-*` during calibration; re-runnable with
  `python3 tools/da.py --pack authorities/triage verify <target> --out <dir>`
