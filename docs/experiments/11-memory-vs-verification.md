# 11 · Memory vs verification — isolating the source of the drift advantage (draft pre-registration)

Owner review of run 1 (2026-10-11): the experiment "demonstrates that the
complete Design Authority workflow reduces drift. It does not yet isolate how
much of that improvement comes from institutional memory versus continuous
verification. That distinction matters for your next experiment."

This document is the design for that experiment. It becomes a
pre-registration when frozen and committed before any session runs; nothing
below has been executed.

## Question

Run 1's advantage bundled two mechanisms: **institutional memory** (the pack
+ records, resolve-before-deciding, advisory handoffs) and **continuous
verification** (the validator, validate-as-last-step, repair-or-file). Which
one carries the drift reduction — memory, verification, or only their
interaction?

## Arms

Two new arms, plus the two run-1 chains as declared references:

| Arm | Institutional memory | Continuous verification |
|---|---|---|
| **MV** (= run 1 DA, reference) | yes | yes |
| **M** (new) | pack + wrapper + protocol resolve/records + advisories | **none in the loop** — no validator provided; sessions never run it; drift measured externally by us |
| **V** (new) | none — static design docs only | validator shipped + **validate-as-last-step (repair-or-file required)**; no pack resolution, no records |
| **NULL** (= run 1 baseline, reference) | none | none (equivalent access only) |

References are declared, not re-run: same seed (`seal/seed`, the sealed
bookmarks line), same four handoffs (the docs/09 feature sequence), same
model, budgets and sandbox harness. The only difference between any two arms
is the reference layer — exactly as in run 1. (Symmetric N=1 per arm;
recorded explicitly.)

## Methodological fixes carried in from the run-1 review

1. **A uniform recurrence trace.** Every M and V session appends to a plain
   `DECISIONS.md` decision log (conventional notes: what was decided, where,
   why) — no machinery required. Re-logging a decision already logged (or,
   in M, already ruled in the record) is countable in both arms, fixing run
   1's "the baseline cannot produce the datum" weakness.
2. **A held-out measure.** The validator is the V arm's own loop, so
   conformance alone cannot separate "consistently designed" from "repaired
   to pass". Session-end screens capture the four handoff states, and the
   blind-review harness (two independent reviewers + the five-screen
   calibration set, per the P4 prereg's reviewer decision) scores visible
   divergence. Reviewers never see the validator output; the validator yard
   is never shown to reviewers.
3. **Constant external yardstick.** The validator runs at analysis time for
   every arm from the frozen pack chain (p4-da-0..4) — unchanged by whatever
   the sessions were given.

## Measures (same dimensions as run 1)

- **Validator conformance** (external, constant) per handoff per arm —
  primary.
- **Blind-review divergence** per handoff per arm — held-out secondary
  (recognition of inconsistency a reviewer sees but the validator does not).
- **Recurrence** from `DECISIONS.md` (all arms) + the record (M, MV) —
  now directly comparable.
- **Cost**: tokens, tool calls, wall per session (governance overhead of
  each mechanism alone, vs the bundled +21%).

## Gates (to freeze before running)

- **Discrimination:** if memory drives run 1's advantage, M's conformance
  trajectory should track MV (flat) while V decays toward the run-1
  baseline's 98→96→94; if verification drives it, the reverse. The gate is
  stated as an ordered expectation, not a point prediction: report the full
  four-arm trajectories + blind-review divergence; declare discrimination
  only if the single-mechanism arms land on opposite sides with non-
  overlapping trajectories.
- **Kill criterion:** if M ≈ V ≈ MV (all flat), the advantage is
  interaction-only at this scale; report as such. If M ≈ V ≈ NULL (both
  decay), neither mechanism alone explains it; report as such.
- Blind-review divergence is reported per arm, never composited with the
  validator score.

## Budget

2 arms x 4 handoffs = 8 sessions at run-1 budgets (2700 s / 20 M tokens),
sequential, ~1.5–2 h. Rehearsal not required beyond the existing p4 harness
(two config deltas: the M/V reference layers and the DECISIONS.md
convention); a `--skip-agent` prep pass per arm is the rehearsal.

## Open decisions (resolve at freeze)

1. Reviewers for the blind round (owner + one independent; the calibration
   set and the logged-deviations mechanism from the estate).
2. Whether the NULL reference stays run-1's baseline or is re-run for
   same-batch comparability (recommended: keep as reference; the harness and
   seed are identical).
3. Freeze date and go — per the standing pattern, on the owner's word.

Status: design draft; freeze + pre-registration committed only on the
owner's go.
