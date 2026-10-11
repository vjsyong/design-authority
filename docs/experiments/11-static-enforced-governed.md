# 11 · Static vs enforced vs governed — the three-arm experiment (draft pre-registration)

Owner review of run 1 (2026-10-11): the observed difference "might come from
several causes… the authority imposes a more disciplined workflow" — and
the directive: *"Pre-register the primary comparison as C versus B, not C
versus A."* This document is that design. It becomes a pre-registration
when frozen and committed before any session runs; nothing below has been
executed.

## Question

Is the drift/maintenance advantage of the full Design Authority workflow
attributable to **automated enforcement and feedback alone**, or to the
**incremental value of governed institutional memory on top of
enforcement**?

## Arms (all run fresh — uniform observability beats reusing run-1 chains)

| Arm | Materials | Enforcement | Governed memory |
|---|---|---|---|
| **A · Static contract** | components, rules, docs, conventional handoff notes | none in the loop | none |
| **B · Static + enforcement** | identical static materials + the equivalent validator shipped + **mandatory checks at every handoff** (validate-as-last-step, repair-or-file) | yes | none — no pack resolution, no cases, no receipts, no reconcile |
| **C · Full Design Authority** | everything in B **plus** governed resolutions, persistent cases, receipts, reconciliation | yes | yes |

Run 1's chains are context, not references: with the new uniform
observability below, all three arms re-run from the same seed on the same
handoff sequence under the same harness.

## Uniform observability (the run-1 review's methodological fixes)

1. **`DECISIONS.md` in every arm** — a plain decision log ("what was
   decided, where, why"), no machinery. Re-logging a decision already
   logged is countable in *every* arm; in C, re-filing a need the record
   already covers is additionally counted from the gap store.
2. **A held-out measure.** Session-end screens are blind-reviewed by two
   independent reviewers (calibration set + logged deviations) who never
   see validator output — so an arm that merely repairs to pass its own
   loop cannot hide visible divergence.
3. **A constant external yardstick.** The frozen pack-chain validator runs
   at analysis time on every session state of every arm, regardless of what
   the sessions were given.
4. **Continuous cost tracking** — per-session tokens / tool calls / wall /
   edits across all five handoffs, never only the final total.
5. **Governance-overhead instrumentation** — every arm's tool invocations
   logged and bucketed (lookups / record writes / retrieval / validation /
   orientation / errors, `new` vs `repeat-context`), extending the run-1
   call profile (`docs/10` §6.1). Optimization ideas (batched resolution,
   cached briefs, incremental verification) are deliberately **out of
   scope**: first measure the baseline overhead, then measure each
   optimization — never assume fewer calls is better.

## H5 · The remediation phase (preventive vs deferred economics)

After H4, each arm's state goes to a **fresh session** whose task is fixed:
reach zero findings under the validator (shipped to every arm for H5 — it
is a repair task by definition) **while preserving functionality** (the
project's regression suite must pass). Measure the additional tokens, tool
calls, wall time and lines touched to reach zero.

This answers the review's economic question directly: *would repairing the
accumulated drift cost more or less than the overhead of preventing it?*
(C's H5 should be near-zero if prevention worked; A's H5 is the deferred
bill; B's H5 tests whether enforcement alone prevented enough.)

## Replications

Three recorded seeds (the interleave/ordering seed; same handoff sequence
and frozen evaluation protocol each time): **3 seeds × 3 arms × 5 sessions
= 45 sessions**, run-1 budgets (2700 s / 20 M tokens), sequential ≈ 9–12 h
(overnight, conductor + taildash as in P4). Staged option: run R1 alone
first (15 sessions, ≈ 3–4 h) and extend by dated amendment; any
"general effect" claim requires ≥ 2 seeds — R1 alone is pilot grade.

The memory-only corner (precedent without enforcement) is deferred: B−A and
C−B bound the enforcement and memory contributions against a no-enforcement
floor; a future memory-only arm would complete the 2×2 if either contrast
is ambiguous.

## Measures and the primary comparison

**Primary: C versus B** on (a) validator findings trajectory, (b) decision-
log recurrence, (c) H5 remediation cost. **Secondary:** blind-review
divergence; the cost deltas themselves (B−A = the price of enforcement;
C−B = the price of memory); the governance-overhead profile. Dimensions
reported separately, no composite score.

## Gates

- **C < B on recurrence/drift/remediation →** the governance layer does
  something enforcement cannot: the differentiation stands.
- **C ≈ B →** enforcement carries the conformance gain; the authority's
  distinctive value narrows toward reconciliation and preserving decision
  rationale. Reported as such — not redundancy, a reframe (the review's
  own reading).
- **B ≈ A →** enforcement alone is insufficient at this scale.
- **Kill criterion:** all three arms flat (no accumulated cost anywhere) →
  no discriminable effect at this scale; reported as such.

## Open decisions (resolve at freeze)

1. Reviewers for the blind round (owner + one independent; the estate's
   calibration set and logged-deviations mechanism).
2. Seeds: 3 recommended; 2 acceptable; R1-only = pilot grade.
3. Freeze date and go.

Status: design draft; freeze + pre-registration committed only on the
owner's go.
