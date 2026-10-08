# 07 · Final report — can a Design Authority verify itself?

**Experiment:** independent conformance verification of the Design Authority
system against its own implementations, 2026-10-08. Baseline: repo `2a913da`
(tag `v0.2.0`). Nothing was repaired before measuring; no authority was
redesigned (the only pack additions are the experiment's additive
`verification.json` contracts — pack versions untouched).

## Executive summary

An independent verifier — generic machinery driven by pack-local contracts,
reading only files, DOM, computed styles and behaviour — was built and run
against the three Cadence builds and against deliberately poisoned copies of
them, blind to what was poisoned.

- **Clean cooperative builds:** 63/63 independently checkable claims verified,
  zero violations, zero false alarms. Claims were never read by any check.
- **Poisoned builds (20 seeded violations, 12 legitimate-control edits,
  verifier blind):** **19/19 detectable violations caught (100% recall), zero
  false positives, one corroborating cascade.** The single miss was the
  *declared* unverifiable class (editorial hierarchy character) — designed in
  as a coverage-boundary probe and reported, not hidden.
- **The loudest finding for the project:** ~48% of the problem space is
  defined by these authorities; **~73% of the audited definition is
  independently checkable today**; and every *detectable* seeded drift was
  caught without trusting a single word of agent self-report.

## Methods (phases 0–9, one line each)

0. Baseline frozen: hashes of packs, builds, tools, golden/resolution
   snapshots (`00`, `raw/baseline-hashes.json`).
1. Verifiability audit: 74 normative items classified (54 mechanical · 9
   partial · 8 review · 3 not-currently) — `01`.
2. Verification contract: minimal per-pack `verification.json` (modes
   STATIC/DOM/COMPUTED_STYLE/INTERACTION/REVIEW; ~20 relations; no DSL) — `02`.
3–4. Verifier built: `tools/da_verify.py` (serve → normalise → inspect →
   evidence), plus the four layers from the brief.
5. Existing builds verified + claim comparison — `03` (all clean).
6. Mutations: separate injector process, 31 sealed entries, verifier blind —
   `04`.
7. Detection metrics: recall 100% on detectable seeds, FP 0 — `05`.
8. Agent-quality confound: condition A (cooperative) vs B (careless-drift
   proxy) — this report.
9. Coverage measured: semantic vs verification, kept separate — `06`.

## Phase 8 · Was past success just agent obedience?

| condition | authority consultation | independently verified conformance |
|---|---|---|
| **A — cooperative strong agent** (the three real builds) | consumed canon correctly (marked nodes, resolved/gap discipline) | 63/63 checkable pass; **0 violations** |
| **B — careless drift** (20 plausible sloppy changes, proxy for a weaker/faster agent) | would *claim* the same canon (marks left intact, notes unchanged) | **19/19 detectable drift caught**; marks and claims were worthless as evidence — and never used as proof |

Read: the cooperative builds' conformance was **real** (it verified clean),
but it was **cooperation-dependent in the sense that nothing would have
caught a careless agent** — the authority text alone does not mechanically
prevent the seeded drifts. The verifier converts "the agent said so" into
"the implementation shows so", and in condition B that distinction is the
difference between a plausible build and 19 recorded violations.

## Phase 11 · Findings ledger (classified, not auto-applied)

| class | findings |
|---|---|
| **IMPLEMENTATION-VIOLATION** | 20 seeded; 19 detected + 1 designed miss — proves this class detectable with the current contracts |
| **VERIFICATION-GAP** | editorial hierarchy character (L-V5 live proof); felt motion; bilingual tone parity; type-scale values uncontracted — all routed to `REVIEW_REQUIRED` today |
| **AUTHORITY-GAP** | *no floating-surface rule text existed* (only a contrast note); a check was added — recommend codifying the rule explicitly in the packs (owner decision, not auto) |
| **AMBIGUOUS-RULE** | wink non-token ink shades; dominion amber family — allowlisted for now, recorded for adjudication |
| **LOCATOR-GAP** | a pictorial svg under the sanctioned `.spark` class would evade imagery scanning; needs authority vocabulary (e.g. chart-role markings) to close |
| **FALSE-POSITIVE** | **none found** (0/74 on clean + 0 unexpected on mutants beyond one correct cascade) |
| **FALSE-NEGATIVE** | 1 designed (L-V5); documented evasion classes untested (recorded in `06`) |

## The six final questions

1. **How much of the current authority is independently verifiable?**
   73% of the audited surface mechanically, +12% partially; 15% human-review
   or not-currently (by *audited items*; entry-level mapping in `06`).
2. **Which classes are easiest/hardest?** Easiest: computed geometry/colour,
   file-level prohibitions (100% first-pass). Hardest: semantics and absence
   claims across whole documents, stateful interaction, and "character"
   (tone/harmony/motion feel).
3. **Does the verifier catch seeded violations?** Yes — 19/19 detectable
   (100%), blind, zero false positives, including one seeded violation only
   detectable by a coverage addition made during this experiment.
4. **How often does it falsely reject freedom?** Never in this experiment:
   0 flags across 9 control edits + 3 undefined-region changes + both
   sanctioned-red controls retained.
5. **How strongly did apparent conformance depend on the agent being good?**
   Fully for the clean sheet — and that's now measurable: the same contracts
   that pass the cooperative builds catch a careless agent's drift at 100%
   on the detectable surface. Obedience is no longer load-bearing.
6. **Smallest verification model worth incorporating into the core?**
   An optional pack-level `verification.json` (additive, format 0.1
   unchanged) + a generic runner with the five modes, the relation set of
   `02`, three conventions (instrument exclusion, missing-policy, worst-of
   aggregation that never upgrades ambiguity to PASS) — and nothing else
   from this harness (mutation machinery and metrics stay experiment
   tooling, not core).

## Success / failure criteria disposition

Success criteria 1–8: **all met** (details: 1→ no check reads claims, mutants
kept claims; 2→ 19/19; 3→ 0 FP on 12 freedom edits; 4→ three authorities,
zero verifier branching (`02`); 5→ 11 honest REVIEW items + UNVERIFIABLE
machinery; 6→ contracts are data, verified by construction + grep; 7→ `03`
tables; 8→ every finding carries observed evidence + screenshots, no
authority auto-mutation).

Failure conditions: **none triggered** — no hand-authored markers required
(1); most meaningful rules checkable (2); no authority-specific verifier
hardcoding (3); zero FP (4); verification is not a self-report echo — the
blind run is the proof (5); visual/normative rules kept as REVIEW instead of
forced numerics (6); a careless or hostile agent cannot evade by editing
annotations because no check trusts annotations (7).

## Phase 10 · Lens integration (completed)

`examples/cadence3-wink` v3.1d: the click-through inspector now fetches
`_evidence/verification/wink-verification.json` (published by
`tools/publish_results.py`; absent on file:// → degrades silently) and shows
an **independent verification** section *separately from the agent claim*:
build totals (25 verified · no violations · 4 open to review), the checks
that directly target the clicked element (self or descendants), each with
status + observed evidence, and a link to the raw verification JSON. Verified
live (`tools/lens_check.py`: all assertions OK, zero console errors);
screenshot: `examples/cadence3-wink/_evidence/screens/v31d-verification-lens.png`.
Leader/dominion results are published into their own `_evidence/verification/`
folders for a lens port when those builds get one.

## Adversarial round (08 · 09) — completed

A full-knowledge hostile adversary (three agents, one per authority) was let
loose on the pipeline with the verifier itself as its oracle. **Round 1:
0/28 evasions detected, 5 induced false flags, 6/6 corruption acts landed.**
One generic hardening pass (all-matches, comment stripping, parsed colours,
precise instrument exclusions, interaction passes, tab-walk, censuses,
must-exist targets, html scoped) flipped it to **28/28 detected, 0 false
flags, mutants still 19/19** — and surfaced one *genuine* new finding in the
clean leader build (search input lacks any focus indication; v3.2 queue).
Signal corruption remains structurally bounded by labelling + covers hashes,
with fresh runs as the only trusted confirmation. Full adjudication:
`docs/verification/09-adversarial-results.md`.

## Recommendation

Adopt the model in question 6 as an **optional, additive capability** — a
pack may ship a verification contract; any generic runner can enforce it;
results surface separately from agent claims (lens integration, below).
Nothing else should graduate: the scoring-free, dimension-separate posture of
the experiment is the point.

## Limitations (stated)

Single-author (contracts + mutations + verifier); one kernel era; the three
authorities share synthesis provenance; partial checks have declared
heuristics; no truly hostile agent was tested (out of scope); "claims"
comparison is qualitative where marks were container-level. Next candidates:
independent mutation agent, navbar/token-value checks, and the v3.2 revision
pass that consumes the owner's existing review verdicts.
