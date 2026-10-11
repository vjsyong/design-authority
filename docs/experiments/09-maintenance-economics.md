# 09 · Maintenance economics of governed precedent — pre-registration (FROZEN 2026-10-11)

Owner memo (da_nextsteps.md section 5): finish the x05 report (done:
`docs/experiments/05-seed-evolution.md` section 11), then design the next
experiment around the question:

**Does persistent governed precedent reduce the cost of maintaining
consistency across successive independent agents?**

This document is the pre-registration. Frozen 2026-10-11 (owner go via the
"keep going, all approved" instruction); nothing has been executed. Any
change after this date is an amendment with its own dated note.

## Why this question

x05 showed that the governance layer changes agent behaviour (consultation,
filing, zero unauthorized vocabulary drift in C) without moving first-pass
fidelity scores. The benefit hypothesis that remains testable is economic:
across handoffs, does governed precedent reduce repeated mistakes, drift,
and human coordination versus an equally good static contract?

## Conditions

Two conditions, deliberately matched on information quality (the memo's
table). The baseline must be strong: structured documentation, versioned,
with the same visual assets and the same verification access.

| Static-contract baseline | Design Authority |
|---|---|
| Same design knowledge | Same design knowledge |
| Versioned documentation | Versioned authority (pack + record layer) |
| Same initial implementation | Same initial implementation |
| Conventional handoff notes | Case history and precedent (gaps, proposals, rulings, receipts) |
| Manual design-change guidance | Policy-driven reconciliation (transition policies, da reconcile) |
| Equivalent verification access | Equivalent verification access |

## Protocol

- One application, several handoffs (target: 4+; one chain per condition in
  the first run, more if budget allows). Fresh agent context per session,
  same model and budgets as x05 (2700 s / 20 M tokens), sandboxed per the
  established containment recipe.
- Each handoff introduces, in a recorded order: (a) an ordinary feature,
  (b) a NEW requirement that touches an already-decided area (exercises
  precedent lookup), (c) a previously unresolved situation (exercises
  filing + future rulings), (d) a canonical-rule change introduced between
  sessions through the authority's own process (exercises reconciliation).
- The change in (d) ships with a transition policy; the reconciliation pass
  (`da reconcile`) runs after each handoff in the DA condition and its
  migration plans are available to the next session. The baseline receives
  the equivalent change as conventional release notes.

## Measures (per dimension, no composite score)

- **Unauthorized drift**: token/vocabulary divergence (the bookmarks-lint
  class of checks; enforced validation as built in the x05 rebuild).
- **Recurrence of resolved gaps**: needs re-filed or re-decided that a
  ruling already covers (grep-able from records/traces).
- **Correctness of migration decisions**: whether the reconcile obligation
  was applied, deferred-with-reason, or missed (receipt-checked).
- **Human review interventions**: owner touches required.
- **Engineering effort**: wall time, tool calls, changed lines per handoff.
- **Token consumption and tool-call overhead**: as recorded.

## Gates (to freeze before running)

- Primary: recurrence of resolved gaps (DA < baseline) and unauthorized
  drift (DA <= baseline) across the later handoffs.
- Secondary: migration-decision correctness >= baseline with fewer human
  interventions.
- Kill criterion: if the baseline shows no recurring-cost problem at all
  (everything already cheap), the experiment cannot distinguish the
  conditions and gets reported as such.

## Decisions (resolved at freeze)

1. **Seed application:** the sealed x05 bookmarks line's final state, forked
   as the common starting point in both conditions (comparability with the
   program that motivated this experiment). The feature sequence is
   recorded in this document's run log before chain 1 starts.
2. **Conditions run enforced:** yes. Condition DA runs with the enforced
   pack and protocol rev2 from the x05 rebuild (validators declared,
   validate-as-last-step, repair-or-file); the sealed x05 arm is not
   modified.
3. **Reviewers:** two independent reviewers plus a calibration set of five
   pre-scored screens, closing the x05 single-reviewer deviation; the
   blind-review harness from the estate is reused with its logged
   deviations mechanism.
4. **Budget:** per-session 2700 s / 20 M tokens (x05 parity); run 1 is one
   chain per condition (4 handoffs each); a second chain per condition may
   be added with its own dated amendment if run 1's spread is wide.
5. **Analysis:** paired per handoff, diffs over means (the estate's
   established preference); primary gates and the kill criterion as stated
   above; all receipts and transcripts sealed before analysis.

Frozen: 2026-10-11. Next action on approval of scope: record the feature
sequence and launch chain 1's first session.

## Run log

### 2026-10-11 · seed + sequence recorded (amendment 1)

- **Seed:** the sealed chain-C line's final state (`~/x05/seal/h4c`, the
  bookmarks app after its 7th session, import wizard complete). Forked to
  `~/p4-maint/seed` and **byte-verified 130/130 files against the h4c seal
  manifest**. Both conditions start from this identical fork.
- **Area:** `~/p4-maint/` (outside the repo, x05 convention). The sealed
  x05 arm is untouched.
- **Feature sequence (recorded order; a=ordinary, b=touches a decided area,
  c=previously unresolved, d=canonical-rule change with transition policy):**

| Handoff | (a) ordinary | (b) decided area | (c) unresolved | (d) canon change (DA: policy + reconcile / baseline: release notes) |
|---|---|---|---|---|
| H1 | collections: named groups + filter row | import "merge with existing" mode in the wizard's validation step | undo after bulk delete | `pattern/empty-state` prospective → required for list surfaces |
| H2 | full-text search (title/URL/tags) | multi-select tag picker (revisits H1 collections) | share/export a single collection | dialog vessel when_touched → required for new overlays |
| H3 | shortcuts: pin/unpin commands | search operators (tag:…) revisit H2 | bulk tag rename | focus-ring rule tightened for dense rows |
| H4 | pinned favourites section | orphaned collections on delete (revisit H1) | import-conflict resolution (edits vs imported) | final policy sweep + full reconcile |

- **Conditions:** DA = enforced pack + protocol rev2 (validators declared,
  validate-as-last-step, repair-or-file); baseline = the static-contract
  line (versioned docs, conventional handoff notes, equivalent verification
  access — the x05 B-line shape). Budgets: 2700 s / 20 M tokens per session.
- **Runner:** to be built at `docs/experiments/tools/p4_*` adapting the x05
  stack (session runner with `--from-seal` handoff chaining, schedule, seal,
  leakscan); rehearsal required before any chain launches. Next action:
  build + rehearse the runner, then launch chain 1's first session.

### 2026-10-11 · runner built, rehearsed, launched (amendment 2)

- **Tools:** `p4_prepare.py` (materials, pack chain p4-da-0..4, seed seal),
  `p4_schedule.py` (8 sessions, k-wise interleave da/base), `p4_run.py`
  (sandbox, budgets, transcript, seal, leakscan), `p4_conductor.py`
  (sequential driver + DA advisories between handoffs). Frozen sandbox
  tooling: the current `tools/` + `kernel/` copied into materials (the x05
  wrapper and protocol rev2 reused untouched).
- **Pack evolutions:** change 1 empty-state required (0.1.2), change 2
  form-validation required (0.1.3), change 3 row-level focus rule B005
  (0.1.4), change 4 chips settled (0.1.5). Baseline receives the same
  changes as release notes; DA receives them as pack + advisories.
- **Rehearsal found and fixed:** opencode's permission schema (string
  `deny` for webfetch/websearch/question); a token-monitor bug (`tell()`
  during iteration silently zeroing counts — replaced with byte offsets);
  a transient `.tmp-pack` staging dir breaking seal consistency (stripped
  pre-seal); the frozen tool copy missing sibling tools (da_sweep);
  read-only seal trees needing chmod before reconcile. Pilots for both
  conditions ran end to end (300 s budget, timeouts as designed, tokens and
  seals recorded).
- **Reconcile note:** the seed predates the project-contract artifacts
  (no lock/receipt), so the reconcile engine records no receipt-backed
  obligations; the advisories the next session receives are the change
  note + reconcile plan + pack validate output, and migration correctness
  is measured at analysis time from the session diff + HANDOFF.md. Recorded
  here as the honest behaviour of the machinery on this seed.
- **Launched:** conductor started 2026-10-11 (bg process; 8 sessions ×
  <= 2700 s; results land in `~/p4-maint/run/<id>/run.json` + seals).

### 2026-10-11 · program complete; run-1 readout (amendment 3)

- All 8 sessions completed (`ok`), all seals verified, zero flagged leakage
  attempts, 12:21–13:53. Results: `docs/experiments/10-maintenance-economics-results.md`.
- Headline (owner-reviewed framing): *Across one controlled four-handoff
  sequence, Design Authority maintained zero validator findings while the
  static-contract baseline accumulated three, at the cost of approximately
  21% more tokens and 16% more wall time.* Validator conformance = strong
  within this run; recurrence = suggestive (not directly comparable);
  migration = auditability demonstrated, no correctness difference; kill
  criterion not hit.
- Cost of governance at this scale: +21% tokens, +37% tool calls, ≈+16%
  wall. Follow-up recorded: run 1 bundles memory and verification; the
  isolating experiment is drafted at
  `docs/experiments/11-static-enforced-governed.md`.
