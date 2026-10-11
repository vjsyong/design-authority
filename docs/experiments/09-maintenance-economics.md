# 09 · Maintenance economics of governed precedent — experiment design (draft pre-registration)

Owner memo (da_nextsteps.md section 5): finish the x05 report (done:
`docs/experiments/05-seed-evolution.md` section 11), then design the next
experiment around the question:

**Does persistent governed precedent reduce the cost of maintaining
consistency across successive independent agents?**

This document is the design. It becomes a pre-registration when frozen and
committed before any session runs; nothing below has been executed.

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

## Open decisions before freezing

1. Seed application and feature sequence (new app, or a fork of the x05
   bookmarks line for comparability).
2. Whether condition C runs with the enforced pack + protocol rev2 from the
   start (recommended: yes; the sealed x05 arm stays untouched).
3. Reviewer count and calibration set (the single-reviewer deviation from
   x05 should not repeat).
4. Budget and session count.

Status: design draft; freeze + pre-registration committed only on the
owner's go.
