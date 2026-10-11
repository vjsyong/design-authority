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
  with the reconciliation FIXTURE additions: **simulated** transition blocks
  (the policy mix a reviewer would set at publication; not owner decisions)
  and `resolves_cases` links derived from the recorded proposal chain.
- `authority-default/<auth>/artifacts.json` — the same records with the
  transition blocks stripped, to demonstrate the owner-set default
  (legacy records -> `review`).
- `findings.jsonl` / `report.json` — the policy run (36 findings; re-running
  reuses all 36).
- `findings-defaults.jsonl` / `report-defaults.json` — the defaults run
  (36 = 10 conforms + 26 review).

The `authority/` files are PARTIAL on purpose: only `artifacts.json`, the
sweep prototype's input. The packaged sweep (P1.4) will read real packs
through the kernel loader and receipts through the project contract.
