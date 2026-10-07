# Final synthesis — Design Authority vs static kit vs naive

**Status: experiment complete.** Automated dimensions (D1–D4) + blind human
review (D5) are in. This document answers the pre-registered question.

> "Does an active, queryable and enforceable Design Authority materially
> improve an agent's frontend output compared with ordinary design
> documentation?"

Conditions: **A** naive (no design material) · **B** passive static kit
(DESIGN.md + rendered kit) · **C** active authority (MCP interface, resolve /
inspect / validate / gap / propose). n=3 per condition, one model
(deepseek-flash), one app (Procura), instruments frozen before execution
(docs/06; all deviations D-1…D-9 disclosed there and in docs/08).

## 1 · Results by condition

| dimension | A (naive) | B (static kit) | C (authority) |
|---|---|---|---|
| D1 lint findings (3 runs) | 164 / 127 / 162 | 0 / 0 / 0 | 0 / 0 / 0 |
| D2 hex colours | 57 / 40 / 43 | 1 / 1 / 0 | 1 / 0 / 1 |
| D2 px values · radii · !important | 28/14/3 · 24/13/1 · 27/10/4 | ≈0 | ≈0 |
| D4 functional checks | 13/13 ×3 | 13/13 ×3 | 13/13 ×3 |
| D5 human total (of 25) | 10 / 18 / 17 | 22 / 19 / 23 | **25** / 21 / 19 |
| D5 condition mean | **15.0** | **21.3** | **21.7** |

## 2 · D5 blind review, unsealed

Single reviewer (project owner), blind to condition; codes unsealed only
after submission. Scores archived at
`benchmark/review/procura-review-2026-10-07.csv`.

| axis | A | B | C |
|---|---|---|---|
| Consistency | 3.67 | 4.67 | **5.00** |
| Coherence | 3.33 | 4.33 | **4.67** |
| Obvious mistakes (5 = none) | 3.00 | 3.67 | 3.67 |
| Confidence to extend | 2.67 | **4.67** | 4.33 |
| Low cleanup needed | 2.33 | 4.00 | 4.00 |

Alignment with the automated instruments: the worst automated build (a2, 164
findings) was also the worst human-scored build (10/25); the only perfect
human score (25/25) belongs to a C run (c2). Ends corroborate; the middle is
murkier (a3/a4 at 18/17 human vs 127/162 lint — plausible-looking drift
reads "fine" to a human eye; the linter is stricter than the reviewer).

## 3 · Findings

**F1 — Active material beats no material, decisively.** Both B and C beat A
on every dimension of both instruments. Naive agents produce functional,
lavish, off-system UI (40–57 colours, 24–28 spacing values, ~10–14 radii
per run); the pre-registered expectation holds.

**F2 — For one-shot output quality, a well-made static kit captures nearly
everything.** B ≈ C on D1 (all-zero ties), D2 (ties), and D5 aggregate
(21.3 vs 21.7). C leads consistency/coherence by small margins; B leads
"confidence to extend" — all inside single-reviewer, n=3 noise. The honest
reading: *the kit, not the protocol, is what makes the artifact look right.*

**F3 — The authority's measured increment is governance, not appearance.**
What C adds is the layer B cannot provide:
- *Zero silent improvisation:* C's divergences are cited decisions,
  sanctioned fallbacks, or filed gaps (c1…c4 in-code `authority-undefined`
  markers + decision logs). B solved the same underspecified problems by
  quietly inventing `.cb` picker and job-progress patterns in all three runs
  — nothing distinguishes that canon from sanctioned design at merge time.
- *Gap discovery:* 3/3 C runs filed gaps; 6 gaps + 3 proposals total; the
  reviewer-picker hole was independently reported by 4 runs (c1–c4) and the
  job-progress hole by 3 — the two most valuable upstream findings of the
  exercise, found by the agents themselves.
- *Enforcement data:* C runs carry validation calls and complete provenance;
  B runs carry none (nothing to merge-governance with).

**F4 — The authority imposes no quality ceiling.** C's best build scored
perfect (25/25) while remaining fully provenance-tracked.

## 4 · Answer

*Compared with no material:* yes, materially — same as any competent design
documentation.

*Compared with well-made ordinary documentation (the literal question):* **on
artifact quality alone, no material improvement — the static kit captures
it.** The authority's material improvement is at the lifecycle layer: it
makes the same-quality output *governable* — traceable, legally fallback-ed,
self-reported, and connected to an upstream improvement loop that this
experiment empirically exercised (6 gaps, 3 proposals, 2 confirmed
underspecified areas, zero silent canon). If "output quality" includes
"output a design team can safely merge, audit, and evolve without reverse-
engineering the diff", the answer is yes — and that is precisely the
difference the prototype set out to test.

## 5 · Limitations

n=3 per condition; one model; one app; one blind reviewer (the project
owner); top-of-scale compression (5-point ceiling for B/C); flagged runs
(b3, b4, c2 — see docs/08 §1) measured from completed workspaces only;
single-host execution with disclosed infra instability (D-9).

## 6 · Next steps

1. **Turn the two discovered holes into formal Triage authority extensions**
   (reviewer-picker recipe; determinate job progress) via the extension loop
   — the first real, evidence-backed Triage changes produced by this
   pipeline.
2. Optional generality test: second app or second model on the same frozen
   protocol.
3. Write-up + decision on whether the authority track continues toward a
   maintained internal tool.
