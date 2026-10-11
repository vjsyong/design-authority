# 17 · The consumer workflow: init → plan → build → receipt → verify → reconcile

One path for a new application under an authority (docs/13 P1.1/P1.2). The
target interface from the owner's memo, now shipped:

    da init --pack <authority>        # pin the authority into the workspace
    da plan BRIEF.md                  # brief needs -> version-pinned plan
    # the agent builds the application
    da receipt-new --revision v1      # scaffold the outcome receipt
    da verify <app-dir> --out <dir>   # independent verification
    da reconcile --workspace <dir>    # assess against the current authority

All commands are ordinary public interfaces of the same runtime library; the
specialized tools (`da_verify.py`, `da_sweep.py`) remain available and are
the engines behind the aliases.

## The project contract (docs/14 section 5)

`.design-authority/` inside the consumer workspace:

- `authority.lock.json` — the pinned authority: id, version, commit, and a
  deterministic fingerprint of the pack's record files;
- `design-plan.json` — the intent: one entry per brief need with its outcome
  (RESOLVED · COMPOSE · FALLBACK · UNDEFINED · CONFLICT), the resolved
  record id, the intent (adopt / compose / fallback_marked /
  improvise_and_report / avoid) and the resolver evidence;
- `cases/` — plan-side stubs for unresolved needs (the future case files);
- `receipts/` + `receipt.json` — the outcome: immutable receipts (format
  0.2), one per published build, with a pointer to the latest;
- `verification/` — verifier outputs.

**Plan discipline.** The brief convention: one bullet per need under a
`## Needs` heading. `da plan` resolves every need against the pinned pack
and refuses to write anything if a cited resolution does not exist in the
pack. Unresolved needs become case stubs: the build is expected to improvise
them, mark them, and report them (a gap in the workspace).

**Receipt discipline.** A receipt captures consequential decisions only:
`decisions_applied`, `unresolved_needs`, `provisional_solutions`,
`deviations` (with the decision and the reason), `areas_modified` (the
`when_touched` trigger surface), `migration_for` (closes earlier
obligations), and a `verification` reference. Receipts are declarations
until a confirmer vouches for them: the sweep marks every finding that used
receipt evidence `receipt_status: confirmed | unconfirmed` and never
upgrades a declaration to proof. `da receipt-check` validates the shape and
every referenced id against the pack.

## Verification

`da verify <target> --out <dir>` runs the pack's verification contract
(`verification.json`) against the actual product. A consumer app maps itself
onto the contract with `verify.map.json` at its root (files / selectors /
ignore-with-reason). Statuses: PASS, VIOLATION, UNVERIFIABLE,
NOT_APPLICABLE, REVIEW_REQUIRED. The verifier is independent: it reads the
served DOM and computed styles, never the builder's self-report.

## Reconciliation

`da reconcile --workspace <dir>` assesses the built workspace against the
current authority and writes `.design-authority/reconciliation.json`: the
findings (conforms / grandfathered / rectify / review), the obligations,
and a migration plan of actions. The engine consumes the same receipt the
build produced - `decisions_applied` and `deviations` scope and classify the
assessment; `areas_modified` is the `when_touched` trigger surface. A
deviation on a decision that is otherwise adopted surfaces as a `rectify`
row with a due obligation. The plan is deterministic and portable (receipt
references are workspace-relative).

## The acceptance reference

`examples/wink-notes/` is the end-to-end acceptance vehicle, frozen by
`tools/check_project_flow.py` (in `check.sh`, 35 checks):

- brief (5 needs) → plan: 4 RESOLVED (action-pill, inline-notice,
  empty-state, progress), 1 UNDEFINED (a floating toast) with its case stub;
- the build (fresh markup, recorded values, a marked toast improvisation
  with a filed gap);
- receipt v1 declaring 4 applied decisions, the toast as a provisional
  solution and an explicit deviation;
- independent verification: 19 PASS / 1 VIOLATION (the declared toast, W-15
  no-floating-surfaces) / 14 honest exemptions;
- reconcile: 3 conforms + 1 rectify; the toast deviation produces a due
  migration obligation on `pattern/inline-notice`.

## Release and versioning notes

- The owner-set transition policies (D-034) enter the record layer at first
  publication: the packs now ship them (0.3.0-rc1 across wink, leader and
  dominion). Agent-produced version bumps carry `-rcM` labels per the
  release policy; promotion to a full version is a human action.
- Limits kept honest: rc versions compare by their numeric prefix; case
  numbering and the confirmation flow for receipts remain minimal until the
  0.6 freeze (docs/16); `da verify` needs Playwright for browser-backed
  modes (STATIC still runs without it).
