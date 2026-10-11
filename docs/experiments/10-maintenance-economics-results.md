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
its recurrence is invisible-by-construction and this comparison is
suggestive only: the baseline's repeated re-derivation surfaces as the
accumulating duplicate treatments in measure 1, not as filed needs. On the
owner review's reading, **this claim is not directly comparable across
conditions**; the DA-side evidence (0 true refilings) stands alone as
suggestive.

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

**No independent correctness difference was observed** — both conditions
implemented the changes, both with zero human interventions. The
demonstrable difference is **auditability** (receipt-backed vs implicit),
valuable in itself and not scored as superior implementation correctness.
The recurrence comparison is fixed for future runs by the uniform
decision-log convention in `docs/experiments/11`.

## 4 · Human review interventions

Zero in both conditions (fully automated run; the conductor handled handoff
chaining and, for DA, the reconcile advisories).

## 5 · Engineering effort

Wall: DA Σ 2,972 s (~50 min) vs base Σ 2,570 s (~43 min) — DA ≈ +16%.
Code churn: near-identical (see table). Handoff documents: DA slightly
larger (they carry the receipt sections; 168–202 lines vs 146–178).

## 6 · Token consumption and tool-call overhead

DA Σ 50.2 M tokens vs base Σ 41.6 M — **DA ≈ +21%**. Tool calls: DA Σ 553
vs base Σ 405 — **DA ≈ +37%**.

### 6.1 · Authority-call profile (review follow-up, corrected)

The first draft of this document reported "1,467 audited authority calls
(317→429 per session)". That was an artifact: the wrapper's `audit.jsonl`
is carried across handoffs, so those figures were the *cumulative log
sizes* at each session end (seed 243 + session work). The real in-run
trace: **186 new wrapper calls across the four sessions** (74 / 25 / 37 /
50), on top of the seed's 243 recorded calls. The profile is what matters
for governance overhead:

| bucket | calls | share | reading |
|---|---|---|---|
| lookups (`resolve` 49, `search` 12) | 61 | 33% | of the 49 resolves, **31 returned UNDEFINED** (new advice sought = new information); 18 hit RESOLVED (repeat-context retrievals) |
| record writes (`gap-add` 31, `propose` 31) | 62 | 33% | the memory-accrual cost — a third of all governance calls create the record |
| retrieval (`inspect` 21) | 21 | 11% | re-fetching known records (cacheable) |
| validation (`validate` 15, all rc 0) | 15 | 8% | used as the protocol asks (last step, repair-or-file) |
| orientation/misc (`gaps`, `overview`, `candidates`, `list`, `--help`, `discover`, `golden`, `review`, `verify`, `precedents`) | 27 | 15% | context re-establishment (batched-brief / cacheable) |
| **errors** (nonzero rc) | 15 | 8% | bad args / not-found: a call-quality target |

Zero resolve queries repeated *across* sessions; the repetition that exists
is within-session re-checking (the 18 RESOLVED lookups + 21 inspects ≈ 21%
of activity re-fetching established context). Directly actionable against
the planned `da plan` architecture: batched resolution, a cached authority
brief per handoff, and incremental verification of changed areas would
target the ~26% retrieval/orientation share without weakening controls —
and the 8% error share argues for CLI ergonomics work. As the review notes,
each optimization should be measured, not assumed.

## Verdict (revised per owner review, 2026-10-11)

**Headline:** *Across one controlled four-handoff sequence, Design Authority
maintained zero validator findings while the static-contract baseline
accumulated three, at the cost of approximately 21% more tokens and 16% more
wall time.*

Three claims, at three levels of confidence:

| Claim | Evidence | Assessment |
|---|---|---|
| DA maintained better validator conformance | 0 findings throughout vs 1, 1, 2, 3 | **Strong within this run** |
| DA reduced repeated design decisions | No repeated decided gaps; baseline developed duplicate treatments | **Suggestive, not directly comparable** (the baseline has no case store, so repeated gap reports cannot be counted in both conditions) |
| DA produced more explicit migration accountability | Recorded receipts vs implicit adherence | **Demonstrated — but migration correctness was not superior** (both conditions implemented the changes; no independent correctness difference). Auditability is the difference, and it is not scored as superior implementation correctness. |

- **Unauthorized drift:** the pre-registered primary gate — met, strongly
  (above). This is the result the run establishes.
- **Recurrence of resolved gaps:** the pre-registered gate as worded cannot be
  satisfied from this run's data — the baseline's recurrence is
  invisible-by-construction. Read the duplicate-treatment accumulation in
  measure 1 as its only cross-comparable trace, and treat the DA-chain
  evidence (0 true refilings) as suggestive.
- **Migration handling:** no independent correctness difference; the
  demonstrable difference is auditability.
- **Human interventions:** 0 in both conditions — no discrimination.
- **Kill criterion:** not hit — the baseline did show accumulating cost, so
  the conditions are distinguishable at this scale.

## What this does and does not establish

Run 1 demonstrates that **the complete Design Authority workflow** reduces
drift against a strong static-contract baseline on a 4-handoff continuation.
It does **not** isolate how much of the improvement comes from institutional
memory (precedent, records, resolve-before-deciding) versus continuous
verification (the validator, validate-as-last-step, advisories) — run 1
bundled both. Separating them is the next experiment:
`docs/experiments/11-static-enforced-governed.md` (draft pre-registration,
freeze on owner go).

## Limits (recorded per the pre-registration)

- One chain per condition (per the frozen decision; a second chain is a
  dated amendment if wanted); single pinned model; the seed carried its
  x05 history for both chains equally.
- The baseline's recurrence measure is proxy-only (no record store).
- Change 4 is exercised only through the post-h4 reconcile.
- The reconcile engine had no receipt evidence on this seed, so the DA
  advisories were change-note + validate-based (recorded in the run log);
  migration correctness was read from receipts + diffs at analysis time.
