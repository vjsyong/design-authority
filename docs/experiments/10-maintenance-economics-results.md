# 10 · Maintenance economics — run 1 results (2026-10-11)

Pre-registration: `docs/experiments/09-maintenance-economics.md` (frozen
2026-10-11; seed, sequence and runner in its run log). This is the run-1
readout. Raw evidence: `~/p4-maint/run/<id>/{run.json,ws,transcript.jsonl}` +
verified seals in `~/p4-maint/seal/`.

## Run summary

8 sessions (2 conditions × 4 handoffs), k-wise interleave, one at a time.
All sessions completed (`status ok`), all 8 seals verified, zero flagged
leakage attempts in either condition. Wall clock 12:21–13:53 (92 min).

| | da-h1 | da-h2 | da-h3 | da-h4 | base-h1 | base-h2 | base-h3 | base-h4 |
|---|---|---|---|---|---|---|---|---|
| wall s | 952 | 944 | 494 | 582 | 678 | 654 | 588 | 650 |
| tokens (M) | 16.2 | 13.3 | 7.2 | 13.6 | 9.9 | 10.0 | 9.1 | 12.5 |
| steps | 130 | 131 | 87 | 105 | 95 | 92 | 96 | 95 |
| tool calls | 170 | 144 | 116 | 123 | 103 | 95 | 100 | 107 |
| code +/− | +561/−39 | +448/−8 | +308/−8 | +394/−53 | +565/−50 | +380/−8 | +364/−12 | +467/−56 |

Both chains built all four handoffs' features (commit messages confirm the
same feature set); code output is near-identical (DA +1711/−108 vs base
+1776/−126).

## 1 · Unauthorized drift (primary) — DA flat, baseline decays

Constant yardstick: the pack's own validator (`p4-da-0` baseline, unchanged
across the run) run against every session-end workspace:

| | da-h1 | da-h2 | da-h3 | da-h4 | base-h1 | base-h2 | base-h3 | base-h4 |
|---|---|---|---|---|---|---|---|---|
| findings | 0 | 0 | 0 | 0 | 1 | 1 | 2 | 3 |
| spec score | 100 | 100 | 100 | 100 | 98 | 98 | 96 | 94 |

The baseline's decay is style-level divergence of the exact kind the metric
names: parallel treatments accumulate (`.add-form-error`/`.wizard-error`
never converge, then `.bookmark-title-row`/`.bulk-actions`, then
`.conflict-choices`/`.control`), one duplicated treatment per handoff.
The DA chain converges at every handoff — zero findings, 100/100, four
sessions in a row. **Gate: DA <= baseline — met, strictly.**

## 2 · Recurrence of resolved gaps (primary)

DA filed 28 new needs in-run (11/3/8/6 per session, `gaps.jsonl` 44→72),
all feature-specific for new work; no true re-filing of a ruled need. The
three touches on decided areas (the sequence's (b) dimension: tag editing,
palette commands, chip rows) were handled by consulting the record —
including one self-caught false lexical match (da-h4 audited its own
`pattern/empty-state` hit before trusting it).

The baseline has no record store (by design — conventional notes only), so
its recurrence is invisible-by-construction and this comparison is proxy:
the baseline's repeated re-derivation surfaces as the accumulating
duplicate treatments in measure 1, not as filed needs. **Gate: recurrence
DA < baseline — met under the proxy reading, with this caveat recorded.**

## 3 · Migration correctness (secondary)

Changes 1–3 arrived between handoffs; change 4 (chips) lands after h4 and
its reconcile is recorded (`run/da-h4/reconcile*.md`).

- **DA** sessions carry explicit receipts: each of h2/h3/h4 opens with a
  "Migration obligation (change k)" section stating coverage ("Every list
  surface ships its empty state… No surface is left without one"), then the
  code shows it (row-level focus rules present, validation on new submit
  surfaces, chip treatment converged).
- **BASE** sessions received the same changes as release notes; the code
  reflects them, but no obligation framing or coverage claim exists
  (implicit adherence).

**Gate: DA >= baseline — met (receipt-backed vs implicit), with zero human
interventions in either condition.**

## 4 · Human review interventions

Zero in both conditions (fully automated run; the conductor handled handoff
chaining and, for DA, the reconcile advisories).

## 5 · Engineering effort

Wall: DA Σ 2,972 s (~50 min) vs base Σ 2,570 s (~43 min) — DA ≈ +16%.
Code churn: near-identical (see table). Handoff documents: DA slightly
larger (they carry the receipt sections; 168–202 lines vs 146–178).

## 6 · Token consumption and tool-call overhead

DA Σ 50.2 M tokens vs base Σ 41.6 M — **DA ≈ +21%**. Tool calls: DA Σ 553
vs base Σ 405 — **DA ≈ +37%**. The overhead is the governance itself: the
DA chain made 1,467 audited authority calls across the run (317→429 per
session, rising as the record grew).

## Verdict against the pre-registered gates

- **Unauthorized drift: met strictly** (flat 100 vs monotone decay to 94).
- **Recurrence of resolved gaps: met under the proxy reading** (0 true
  refilings vs an unrecordable baseline — caveat above).
- **Migration correctness: met** (explicit receipts + equal code outcomes).
- **Kill criterion: not hit** — the baseline did show accumulating cost, so
  the conditions are distinguishable at this scale.

Run 1 therefore answers the memo's question positively at this scale: on a
4-handoff continuation of an existing app, governed precedent bought flat
consistency and a receipt-backed audit trail for ≈ +21% tokens, +37% tool
calls and ≈ +16% wall (~9 M tokens and ~7 minutes of extra compute against
a visible, monotone consistency decay in the strong static-contract
baseline).

## Limits (recorded per the pre-registration)

- One chain per condition (per the frozen decision; a second chain is a
  dated amendment if wanted); single pinned model; the seed carried its
  x05 history for both chains equally.
- The baseline's recurrence measure is proxy-only (no record store).
- Change 4 is exercised only through the post-h4 reconcile.
- The reconcile engine had no receipt evidence on this seed, so the DA
  advisories were change-note + validate-based (recorded in the run log);
  migration correctness was read from receipts + diffs at analysis time.
