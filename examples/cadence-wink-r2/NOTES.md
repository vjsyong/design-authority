# cadence-wink r2 — revision notes (reconciliation closure test)

This directory is a genuine next revision of the cadence-wink build (stress
experiment v1, archived at `examples/cadence-wink`), created for the
reconciliation closure test in `docs/experiments/07-reconciliation-cadence.md`
section 6. It modifies ONE area of the v1 app to exercise the
grandfathered -> trigger -> rectify -> migrate -> verified -> conforms cycle
against the same wink authority. It is not a new experiment arm.

## Revision r2a - 2026-10-11 (modification; migration NOT applied)

- Changed: the settings-save confirmation. v1 showed a transient toast
  (`showToast("Saved")`, improvised while feedback was undefined). r2a
  reworks it into a persistent ad-hoc text echo (`.save-echo`) near the save
  control.
- Resolution session (recorded in `_evidence/resolves.jsonl`): "a saved
  confirmation after saving settings" resolved to `pattern/inline-notice`
  under wink 0.2.0, and the ad-hoc treatment shipped anyway. The deviation is
  recorded in the r2a receipt
  (`.design-authority/receipts/2026-10-11-r2a-modification.json`).
- This is the trigger event: the affected area (feedback / save confirmation)
  was modified without migrating.

## Revision r2b - 2026-10-11 (migration applied)

- The settings-save confirmation now renders the canonical inline notice
  (pattern/inline-notice): parsnip fill, rounded 12, bold lead sentence plus
  a plain supporting line, in flow near the save control; the improvised save
  toast is gone from this flow.
- Independently verified: `_evidence/verify-notice-migration.py` re-derives
  the record's claims from the served DOM (8/8 checks pass; fresh run in
  `_evidence/verification/notice-migration.json`).
- Receipt: `.design-authority/receipts/2026-10-11-r2b-migration.json`
  (migration_for: pattern/inline-notice; closes the r2a deviation).

## Reconciliation trail (docs/experiments/07-reconciliation-cadence.md section 6)

- Stage 1 (r2a, `closure/report-1.json`): trigger detected on cadence-wink
  (v1) - permission ended; r2a carries the due obligation.
- Stage 2 (r2b, `closure/report-2.json`): r2b conforms; the r2a obligation
  is closed by the r2b receipt (verification: pass).
