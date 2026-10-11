# reconcile-cadence — reconciliation lifecycle test fixtures

Fixtures for the end-to-end test in `docs/experiments/07-reconciliation-cadence.md`
(run by `tools/da_sweep.py`, the docs/14 prototype).

Reproduce:

    python3 tools/da_sweep.py \
        --authority docs/experiments/reconcile-cadence/authority \
        --portfolio docs/experiments/reconcile-cadence/portfolio.json \
        --store docs/experiments/reconcile-cadence/findings.jsonl \
        --target-version 0.2.0 \
        --report docs/experiments/reconcile-cadence/report.json

## Contents

- `portfolio.json` — the nine applications (three generations x three
  authorities), each with built-under version, evidence path where one
  exists, and a `lineage` declaration that lets the recorded cases of the
  flagship build reach its generations. Decision receipts (P1.1) will make
  this self-describing.
- `authority/<auth>/artifacts.json` — the live 0.2.0 packs' artifact files
  with the reconciliation FIXTURE additions: the **owner's real** transition
  policies (decision page, 2026-10-11) and `resolves_cases` links derived
  from the recorded proposal chain.
- `authority-default/<auth>/artifacts.json` — the same records with the
  transition blocks stripped, to demonstrate the owner-set default
  (legacy records -> `review`).
- `findings.jsonl` / `report.json` — the policy run (36 findings =
  10 conforms + 18 grandfathered + 4 rectify + 4 review, 4 scheduled
  obligations; re-running reuses all 36).
- `findings-defaults.jsonl` / `report-defaults.json` — the defaults run
  (36 = 10 conforms + 26 review).

The `authority/` files are PARTIAL on purpose: only `artifacts.json`, the
sweep prototype's input. The packaged sweep (P1.4) will read real packs
through the kernel loader and receipts through the project contract.

## The closure test (`closure/`)

- `closure/portfolio-stage1.json` / `closure/portfolio.json` — the focused
  two-app scope (the cadence-wink v1 line) at the trigger point and after
  migration.
- `closure/findings.jsonl` + `report-1.json` / `report-2.json` — stage 1
  (trigger detected, obligation due) and stage 2 (r2b conforms; the r2a
  obligation closed by the r2b receipt with its verification result).
- The revisions themselves live in `examples/cadence-wink-r2/`: r2a (the
  modification without migration, deviation receipt) and r2b (the migrated
  state with the independent verifier `_evidence/verify-notice-migration.py`
  and the closing receipt).
- `examples/cadence-wink-r2/_evidence/snapshots/r2a/` — the committed r2a
  code state, so the receipt claims stay confirmable from the repository;
  `_evidence/confirm-receipts.py` + `_evidence/verification/receipt-confirmation.json`
  bind them with source diffs and hashes.
- `tools/reconcile_regression.py` re-runs all of the above from committed
  fixtures inside `check.sh` (plus evidence-freshness checks).
