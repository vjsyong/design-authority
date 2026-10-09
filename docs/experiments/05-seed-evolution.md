# Experiment 05 · Seed evolution: design drift under successive agent handoffs

Status: **revision 7, adding the orchestration and isolation layer**. The
design, conditions, and measures stand as in revision 6; this revision
specifies how the program actually runs: the run area, the sandboxed session
runner, the per-condition isolation matrix, sealing and handoff flow, the
conductor, capture and extraction, the failure model, and the Phase 0 setup
with rehearsal. Section 9 lists owner confirmations.

## 0 · Revision history

**Revisions 2 to 5** (superseded design): a text-only archival transfer test
between a no-records baseline and a records-only condition, with frozen
roles, a four-class precedent census, dimension-level scoring, controlled
calibration, and hardened execution rules. All of that machinery is carried
forward where it still applies; the transfer test itself becomes a deferred
sub-study.

**In revision 6:** the problem statement was corrected (source and
rendered-UI access are natural development context, not a confound to
remove); the central question became drift reduction beyond natural
continuity and informal precedent; three conditions replaced two; drift over
time became the primary measurement; the program took its formation,
codification, and drift-test structure; the feature sequence was designed
for hard continuity.

**In revision 7 (this version):**

- The mechanics layer is specified in full as section 6: a run area outside
  the meta repository, a session runner with bubblewrap containment modeled
  on the proven benchmark harness, an explicit per-condition isolation
  matrix, immutable sealing with verified handoffs, a resumable conductor
  with taildash monitoring and pause rails, the capture and extraction
  pipeline that freezes applicable conventions before each next step, the
  failure model, and the Phase 0 setup including a three-condition
  rehearsal excluded from analysis.
- Budgets, replacement policy, and blinding carry from revision 5
  unchanged. MCP stays off in this experiment; the audited CLI wrapper is
  the measured path.

## 1 · Question

**Overarching hypothesis:** explicit codification of emergent design
conventions into a machine-consumable authority reduces the rate of design
drift across successive autonomous development sessions, beyond the
consistency maintained through inherited implementation and informal
precedent alone.

**Primary:** to what extent does an explicit design authority reduce design
drift beyond the continuity already provided by inherited code, existing
interfaces, and informal design precedent?

**Comparisons, fixed in advance:**

- B versus A: what does recorded precedent add beyond implementation
  inheritance and natural project context?
- C versus B: what does formal codification add beyond unadjudicated
  precedent?
- C versus A: the total practical benefit of the authority workflow.

**Qualification, stated now.** C versus B measures the combined effect of
canonical information and the tooling that enforces it. Isolating the tooling
alone (the same canon supplied as ordinary documentation) requires an
additional condition and is deferred until the larger effect is established.

**Boundary.** One seed lineage, one application family, one model, one chain
per condition. Trajectories are descriptive and exploratory; nothing here is
a general estimate of authority value across projects.

Three record states keep their distinction throughout: a **gap** is evidence
that an agent improvised; a **proposal** is a candidate normative claim; a
**published authority record** is a binding norm.

## 2 · Program overview

1. **Phase 1, formation.** Three fresh sessions build a seed application
   (bookmarks manager) against an empty authority, filing gaps and
   proposals as they go. Output: the sealed seed app, the archive, the
   precedent census, and the reference exemplar sheet.
2. **Phase 2, codification.** An adjudication session converts the archive
   into a canonical pack (`base 0.1.0-experiment`) using the governance
   machinery: each item resolved, declined, or deferred with grounds.
   Output: the canon plus its quality measures.
3. **Phase 3, drift test (the priority experiment).** Three copies of the
   sealed seed run through the same four-handoff feature sequence under
   conditions A, B, and C. Output: fidelity trajectories, consistency and
   correction measures, and the blind review.

Phase 1 gates the program: without a sufficiently stable seed there is
nothing to codify or drift. Phase 2 does not gate Phase 3; canon quality is
reported as a covariate for interpreting C.

Seventeen sessions in total: f1 to f3, cen (census), cod (adjudication), and
h1a to h4c (the three drift chains).

## 3 · Phase 1 · Formation

**The blank authority.** Pack `base`, version `0.0.0-rc0`: identity only;
empty artifacts, rules, prohibitions, fallbacks, recipes, golden. Resolves
UNDEFINED for every ask; warns nothing.

**Frozen roles and opportunity matrix** (carried from revision 5): primary
action, destructive confirmation, empty state, form validation, tags or
status, surfaces and borders. Each role has at least two distinct
opportunities across the three sessions:

| Frozen role | Phase A opportunities |
|---|---|
| Primary action | F1: add bookmark; F2: bulk apply action; F3: save in edit flow |
| Destructive confirmation | F2: bulk delete confirmation; F3: single delete confirmation |
| Empty state | F1: first-run empty list; F2: no filter matches; F3: collection empty after cleanup |
| Form validation | F2: add-bookmark form; F3: edit form |
| Tags or status | F2: tag filter chips; F3: tag editing |
| Surfaces and borders | F1: bookmark cards; F2: bulk-selection surfaces; F3: edit panel |

**Sessions** (fresh agent each, sequential, one pinned model):

| Session | Required new work |
|---|---|
| F1 | Shell, list, navigation, primary action (add), cards |
| F2 | Tag filtering with empty-filtered state, bulk actions, add form with validation, selection surfaces |
| F3 | Edit flow, single delete confirmation, tag editing, responsive details |

Protocol per session: resolve before deciding; file a gap for every
uncovered decision unit with the fallback used and its evidence; convert
recurring or structural choices into proposals at session end; read earlier
builds and records before visual decisions, matching or explicitly flagging
divergence; stop cleanly with the app runnable and a HANDOFF.md. Proposals
are nonbinding precedent; the published pack stays empty; treating a
proposal as binding is a protocol violation recorded in the analysis.

**Seal and census.** At F3's end the checkpoint is sealed (SHA-256
manifests). At seal time, before anything downstream runs, an independent
classifier scores each role: Established (repeated compatible use across at
least two distinct opportunities with a traceable record), Observed once,
Inconsistent, or Absent. K counts Established roles. The reference exemplar
sheet freezes one exemplar per established role with measured values and
behavioral categories. If K is below 4, the program stops and reports
formation insufficient.

**Formation measures** (new, per the review): formation quality (K and
role-level classifications), contradiction rate (incompatible treatments
for the same role across sessions), record coverage (share of decision
units with a filed record containing need, fallback, and evidence), and
stability (conventions unchanged from first to last use).

## 4 · Phase 2 · Codification

**Input:** the sealed checkpoint, the archive (gaps, proposals, decision
logs), the census, and the exemplar sheet.

**Process.** A dedicated adjudication session (fresh agent, same model,
same budget) operates the authority's own governance machinery: every gap
and proposal is resolved (codified into a canonical record), declined, or
deferred, each with grounds and citations to the sealed artifacts. The
release policy normally requires a human for full-version promotion; for
this experiment the output is labeled `base 0.1.0-experiment` and owner
ratification is optional and recorded either way, so no result is
overstated as human-endorsed.

**Output:** the canon pack used by condition C.

**Measures:** resolution quality (per item, is the resolved, declined, or
deferred outcome defensible against a fixed rubric, reviewer-classified),
coverage (share of established conventions present as records), ambiguity
(overlapping or contradictory rules detected by a fixed check plus a
reviewer pass), and adjudication effort (items handled, authority calls,
tokens, wall time).

## 5 · Phase 3 · Drift test

### 5.1 Design

**Common seed.** Three identical copies of the sealed F3 application: full
source, git history, and the ability to run and preview it; plus a frozen
set of current-state screenshots. Identical in every condition.

**Conditions.**

| Condition | Available guidance | What it tests |
|---|---|---|
| A: Natural continuity | Source, rendered UI, project history | How much consistency emerges naturally |
| B: Informal precedent | A plus the gaps, proposals, and decision logs (the archive, growing as the chain files new records) | Does accumulating precedent improve continuity |
| C: Canonical authority | B plus the adjudicated `base` pack and the authority tooling (resolve, inspect, validate against canon) | Does formal codification reduce drift further |

Everything else is identical: the same briefs, the same feature sequence,
the same build tools, the same budgets, the same fixtures. Existing code
access is unrestricted in every condition. B and C both run the filing
protocol; only C resolves against canonical records. The canon is frozen
after Phase 2 and is not extended mid-chain.

**Feature sequence** (same across conditions; escalating novelty so later
handoffs force genuinely new components):

| Handoff | Required new work | Continuity stress |
|---|---|---|
| H1 | Search, sort, and list density controls | New control patterns on the existing list |
| H2 | A tag analytics view | First data visualisation components in the app |
| H3 | A command palette with fuzzy actions and recent history | A new interaction surface and keyboard layer |
| H4 | A multi-step import wizard with mapping table, validation, and progress | A new multi-step flow and table pattern |

**Handoff mechanics.** Per condition, one fresh agent per handoff receives
its own chain's previous state. Interleave execution across conditions by
handoff index (H1 across A, B, C, then H2, and so on), with within-index
order fixed by a recorded seed. Checkpoint seal and HANDOFF.md after every
handoff. Containment and the full mechanics layer are section 6.

**Budgets and execution rules.** 2700 seconds wall and 20M sum_total tokens
per run; briefs frozen as annexes; no human fixes mid-run; agents never
told the conditions or metrics. Enforcement, replacement policy, and
monitoring are section 6.

### 5.2 Measures

**Primary: convention fidelity of new and modified decisions.** At each
handoff, the new or meaningfully modified interface elements are enumerated
from the frozen per-handoff opportunity list and the implementation diff.
For each decision point where an applicable convention exists (established
by the seed or by earlier handoffs of that chain, extracted and frozen at
each checkpoint under the same census protocol), reproduction is scored
with the frozen dimension rubric (section 7). Departures score as
non-reproduction whether or not they were documented; whether a departure
was explicit and recorded is reported separately. Fidelity per handoff:
score sum divided by twice the applicable decision count. Reported as every
value, per-decision-point tables, and per-condition trajectories across
handoffs. Inherited elements are never counted in this measure.

**Secondary outcomes.**

- *Cross-component consistency.* For new components with no applicable
  precedent (the hard-continuity cases), score internal coherence with the
  established vocabulary under the same rubric applied against the frozen
  vocabulary exemplars, plus a pattern-reuse observation log.
- *Correction burden.* Independent reviewer corrections, severity-weighted
  (S1 conformance-critical, S2 in-view inconsistency, S3 polish; weights 3,
  2, 1), normalized by the fixed per-handoff opportunity sets. This
  approximates the practical value of each condition.
- *C-specific mechanism record.* Enforcement interactions: conflicts the
  tooling surfaced, deviations recognized before correction, and whether
  new gaps were filed rather than silently absorbed.

**Blind layer.** Reviewers rate adjacent-checkpoint pairs within each chain
(does handoff k+1 still belong to the same product) plus matched role and
component regions, at the desktop viewport, on cropped matched crops, with
full screens for the qualitative itemized question. Hierarchy: individual
ratings, then per-comparison means across three reviewers, then per-handoff
scores, then condition trajectories. Calibration uses the controlled
variant set (base, faithful variant, altered variant with a frozen change
list) to report instrument discrimination; ecological pairs remain
diagnostic only. Pair orientation, order, and identifiers randomized;
mapping sealed until scoring ends.

**Fixtures.** The five standard states (empty dataset, populated list,
filtered view, invalid submission, confirmation open) plus per-handoff
feature states (analytics view, palette open, wizard step), all captured
with fixed localStorage seeds, by the experimenter, never from agent
self-reports.

### 5.3 Hypotheses and decision rules

Framed as exploratory; one chain per condition; all values reported
individually; no significance testing.

- **D1 (primary):** fidelity trajectory ordering C greater or equal to B
  greater or equal to A. Primary gate: C exceeds B in at least three of
  four handoffs, with the median per-handoff delta at or above the value of
  one fully reproduced decision point at the median handoff (one over its
  applicable decision count, fixed before scoring), corroborated by a
  blind median difference of at least 1.0 point in the same direction.
- **D2 (secondary):** B exceeds A on the same measures.
- **D3 (secondary):** cross-component consistency favors C on the
  hard-continuity handoffs (H2 to H4).
- **D4 (secondary):** correction burden lowest in C, highest in A.
- **D5 (mechanism, descriptive):** in C, deviations from canon are surfaced
  by tooling and repaired or filed, rather than absorbed silently.

Decision table, fixed in advance:

| Result | Reading |
|---|---|
| C beats B by the gate, B at or above A | Authority reduces drift beyond both natural continuity and informal precedent |
| C beats B, B level with A | Codification helps; the informal archive alone did not |
| C level with B, both above A | Recorded precedent carries the effect; formal codification added nothing measurable |
| All conditions level | No detectable differentiation at this size; ceiling effects or model priors dominate |
| Objective gate not evaluable (calibration) | Report on the blind measure alone, labeled reduced precision |

Interpretation notes. Every outcome is bounded by one seed lineage, one
application family, one model, four handoffs, and one chain per condition.
Canon quality (Phase 2 measures) is reported as a covariate: if C's canon is
weak, that is part of the finding, not an excuse. A positive result does not
show that authority works in general; it shows it worked here, at this
scale.

## 6 · Orchestration and isolation (mechanics layer)

The run machinery reuses proven house components rather than inventing new
ones: the benchmark session runner (`benchmark/harness/run_condition.py`:
bubblewrap minimal filesystem, containment audit, token capture, serve and
capture pipeline) and the sandboxed-agent-runs recipe (the containment
fence, the audit surface, and the production lessons about one-session-at-a-
time execution, temp-dir leakage, and unexplained kills).

### 6.1 Run area and repository separation

All live run state lives outside the meta repository, at `/home/xrim/x05/`.
The repository contains this plan and is a thing agents must never be able
to read; keeping the run area outside it means even a containment defect
exposes nothing beyond the experiment's own tree. The system temp area is
rejected as the run location because reboots wipe it; the run area must
survive restarts and be resumable.

```
/home/xrim/x05/
  schedule.json     frozen run plan: ids, order, budgets, brief hashes, seed
  state.json        conductor progress, written atomically, resumable
  run/<id>/         per session: ws/ (agent workspace), transcript.jsonl,
                    run.json, audit.jsonl, capture/, extraction/
  seal/<id>/        immutable sealed checkpoints: hash manifests and copies
  materials/        staged inputs: blank pack copy, archive copy, canon copy,
                    wrapper template
  pilot/            rehearsal artifacts, excluded from analysis
  logs/             conductor log
```

Experiment tooling lives in the repository under
`docs/experiments/seed-evolution/tools/` and is executed from there by the
conductor; agents never see it because the sandbox binds only `run/<id>`.
When phases complete, the durable artifacts (seals, captures, run.json
files, the report) are archived into the repository under
`docs/experiments/seed-evolution/`; the x05 area is the working area, the
repository is the record of truth.

### 6.2 Session runner

`x05_run.py`, modeled on the benchmark runner. Per session:

1. **Preparation.** Copy the input state into `run/<id>/ws` (the sealed
   previous checkpoint for handoffs, staged materials for f1), and verify
   the copy byte-wise against the seal manifest. Write the frozen brief as
   the prompt. For B and C, install the per-run authority wrapper.
2. **Sandbox.** Bubblewrap minimal filesystem: read-only system directories,
   proc and dev, tmpfs temp, and a single bind of `run/<id>`; opaque
   toolchain mounts; cleared environment with explicit variables only; a
   per-run config home so no global configuration, plugins, or skills load;
   home limited to the agent's authentication paths. Python, node, and
   browser tooling are present so agent self-tests do not hang. The seat of
   write access is the workspace; seals, the x05 root, other runs, and the
   repository are invisible.
3. **Budget enforcement.** Wall clock via the unit timeout (2700 seconds);
   token cap by monitoring transcript step events and stopping the session
   at 20M sum_total; both recorded, cap hits named.
4. **Post-session.** Containment audit over the transcript (protected-path
   attempts versus mentions, against the X05 protected list: x05 paths,
   other session ids, `schedule`, `seal`, the repository path). Serve and
   capture the fixtures outside the sandbox. Extract the computed-style
   inventory and the element diff versus the previous checkpoint. Seal the
   workspace (SHA-256 manifest over code and records; read-only copy into
   `seal/<id>`). Write `run.json`; append to `state.json`.
5. **Evidence discipline.** Every measured artifact is produced by the
   runner, never from agent self-report.

### 6.3 Per-condition isolation matrix

What the agent can see, per condition:

| Material | A | B | C |
|---|---|---|---|
| Its own chain's application state (fresh copy) | yes | yes | yes |
| Frozen current-state screenshots | yes | yes | yes |
| Its session brief and the prior HANDOFF.md | yes | yes | yes |
| Informal archive copy (read-only, cumulative) | no | yes | yes |
| Authority CLI wrapper (audited) | no | yes, against the blank pack (filing and reading) | yes, against the canon (resolve, inspect, validate) |
| Canon pack | no | no | yes |

Hidden in all conditions: the x05 root, the schedule, seals, other runs,
other conditions, this plan, and all measurement tooling. B's wrapper
reproduces the formation-era filing behavior; C's wrapper adds canonical
resolution and enforcement, with every call audited. MCP stays off in this
experiment; the audited CLI wrapper is the measured path. The
cross-condition leakage audit scans every transcript for other session ids,
condition names, and x05 paths; nonzero attempts on protected paths are
flagged and the run is examined before scoring, and is kept unless the
attempt invalidated its own inputs.

### 6.4 Sealing and handoff flow

A seal is a hash manifest over code, records, and HANDOFF.md, copied
read-only. The same sealed bytes feed every downstream consumer: the next
handoff, capture, extraction, scoring, and audit. A session's workspace is a
fresh copy of its chain's latest seal, verified against the manifest at
preparation time, so chains provably continue from identical inputs and the
three Phase 3 seeds are hash-identical at start (checked and recorded).
Agents never write to seals; all measurement reads only seals.

### 6.5 Conductor

`x05_conductor.py`, run as the `x05-conductor` user unit (boot-persistent,
restart-safe).

- Consumes `schedule.json` and executes strictly one session at a time (the
  host-stability lesson). Before each session it verifies the dependency:
  the predecessor's seal exists and its manifest verifies. Extraction steps
  run immediately after each session; census and adjudication run at their
  scheduled positions.
- Ordering: interleaved by handoff index; within-index order fixed by the
  recorded seed; the next index starts only after all three chains of the
  previous index are sealed and extracted.
- Resumability: on start it reads `state.json`, verifies the last completed
  seal, and continues at the next incomplete step. If the host reboots
  mid-session, the dead session is classified as infrastructure interruption
  and scheduled for replacement under the frozen policy.
- Monitoring: a taildash parent task (`X05 program`, progress of 17
  sessions) plus one task per session (`X05 f2 formation`, `X05 h2b drift`),
  with heartbeats while sessions run and real outcomes on completion. The
  dashboard, now containerized on this host, is the at-a-glance surface for
  overnight chains.
- Rails: the conductor pauses and notifies after the third infrastructure
  failure, after a session that dies in an unexplained kill cluster (the
  production lesson: treat the environment as the working hypothesis and
  check host stability), and on any seal verification failure. Stray
  processes are reaped between sessions by scanning for working directories
  inside the run's workspace, never by broad pattern kills.

### 6.6 Capture and extraction pipeline

The capture harness runs outside the sandbox: it serves the sealed app on a
per-session port, applies the fixed localStorage seeds, and screenshots the
five standard states plus the handoff's feature states at both viewports.
The extraction pass (deterministic wherever possible) records the element
inventory, computed styles, and the diff against the previous checkpoint.
Extraction is what freezes the applicable conventions for each handoff
before the next session starts; any judgment classification that remains is
performed against the frozen evidence, blinded to results, and timestamped,
never re-chosen later. The census after f3 and the adjudication session are
sessions like any other: budgeted, sandboxed, sealed. The census classifier
sees only the sealed seed and its rubric, and cannot see Phase 3 because it
has not run.

### 6.7 Failure model

- Infrastructure failure versus unsuccessful run: the revision 5 definition,
  decided on observable technical criteria; replacements are logged
  alongside the failed attempt, never deleted.
- Wall and token caps enforced by the runner; cap hits recorded and reported
  as censored outcomes.
- Zero-change sessions (exit zero, no diff against the input state) are
  detected by the diff step and treated as unsuccessful runs; they stay in
  the analysis.
- No repairs and no human fixes, ever. The checkpoint is the state,
  including broken states; that is the drift being measured.

### 6.8 Setup artifacts and rehearsal

Phase 0 builds, before any scored session: `x05_run.py`, `x05_conductor.py`,
materials staging (blank pack copy, archive copy, canon copy, wrapper
template), the capture harness (fixture seeds and screenshot script), the
extraction script, the seal tool, the leakage scan, the schedule generator
(seed and brief hashes), the systemd units, and taildash wiring.

Rehearsal: one throwaway session per condition at a reduced budget and a
trivial task, against scratch copies, to validate containment, wrappers,
capture, sealing, and auditing end to end. Inside the sandbox the
verification probes from the containment recipe are run: toolchains import,
a browser launches, and the isolation probe shows no experiment-visible
paths. Rehearsal artifacts live under `pilot/` and are excluded from all
analysis; they are recorded as pre-flight evidence. The checklist must pass
on all three conditions before f1 starts.

## 7 · Shared machinery (carried from revision 5)

**Decision units.** A fileable decision is one of: a component treatment, a
semantic colour role, an interaction convention, a layout pattern, or a
deliberate exception.

**Frozen dimension pass rules.** Visual dimensions: palette (same colour
role and value within CIELAB delta-E 2000 of at most 5), radius (within 2
px or both pill class), typography role (same recorded role and generic
family class), spacing rhythm (matched pairs within plus or minus 20
percent, scale ordering preserved), border and treatment (same category:
none, hairline, strong, shadow). Behavioral dimensions are discrete
categories, pass only on the same category as the exemplar: trigger
placement (row action, toolbar, menu), confirmation pattern (dialog,
inline, undo), destructive emphasis (colour emphasis, outline, neutral with
copy), cancel-first default (cancel focused, confirm focused), post-action
feedback (message, undo affordance, none), validation timing (on submit, on
blur, live), error placement (inline field, summary, toast), message
treatment (colour plus icon, text only, plain), invalid-field signaling
(border, colour, icon), recovery affordance (auto-clear, manual, none).
Role score: 2 when all mandatory dimensions pass, 1 when at least half
pass, 0 otherwise. Inapplicable dimensions are frozen per exemplar and
removed from both sides. Desktop 1280 is primary; mobile 390 reported
separately.

**Reference exemplars.** Frozen per checkpoint (seed census, then each
chain checkpoint for that chain), never re-chosen after results are seen.
Fidelity for handoff k compares only against exemplars frozen before k.

**Departures.** Non-reproduction in the fidelity measure whether
acknowledged or not; acknowledgment is a process outcome reported
separately, never a scoring exemption.

**Calibration and reliability.** Controlled variant set for instrument
discrimination, reported per anchor individually; inter-rater agreement
reported as exact and within-one-point shares; discriminating requirements
per the revision 5 rule, applied to the primary gate.

**Costs and budgets.** Per run: 2700 seconds wall, 20M sum_total tokens.
Cap-hit caveat as in revision 5. Adjudication effort measured in Phase 2.
Net effort saved (corrections avoided minus codification and maintenance
effort) needs editing-time observations and is deferred; the priority is
establishing whether authority reduces drift at all.

## 8 · Deferred

- **Text-only transfer sub-study** (revisions 1 to 5): retained as a
  narrower investigation, not central. Its full specification is preserved
  in git history and can be revived unchanged.
- **Tooling isolation condition:** the same canon supplied as ordinary
  documentation instead of enforced tooling, to separate information from
  enforcement. Deferred until the larger C versus B effect is established.
- **Net effort economics** and **additional seed lineages or chains per
  condition** for replication. Deferred as cost follows value.

## 9 · Owner confirmations

1. Model: pin the same one as the C-condition benchmark runs, or another.
2. Pack name: `base`; canon label `base 0.1.0-experiment` with optional
   owner ratification recorded.
3. Seed app and feature sequence: bookmarks manager progressing through
   search and sort, analytics, command palette, import wizard.
4. Handoffs: four per condition, interleaved by index; second chains
   deferred.
5. Budgets, reviewers (three predetermined), calibration set, and
   replacement policy carried from revision 5.
6. Mechanics layer as specified in section 6: run area at
   `/home/xrim/x05/`, bubblewrap containment, conductor with taildash
   monitoring, rehearsal excluded from analysis.
7. Text-only transfer stays deferred.

On confirmation this document becomes the pre-registered plan, committed
and dated, before any session runs.

## 10 · Deliverables

- The sealed seed application with per-session history, the census, and the
  exemplar sheet.
- The archive and the canon pack with Phase 2 quality measures.
- Three condition chains, each with per-handoff checkpoints, audits, and
  records; the fidelity trajectories and the blind review.
- The orchestration stack (runner, conductor, harnesses, seal and audit
  tools) and the pre-flight rehearsal record.
- The program report appended to this document, including the caveats in
  sections 1 and 5.3.
