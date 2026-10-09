# Experiment 05 · Seed evolution: design drift under successive agent handoffs

Status: **revision 6, restructured per the third review direction**. The
central question, the conditions, and the primary measurement are replaced.
The earlier text-only transfer framing is retired to a deferred sub-study
(full specification preserved in git history). Code and rendered-UI access
are no longer treated as a confound: they are part of the natural development
context in every condition, and the tested contrast is the same context
with and without normative structure. Section 8 lists owner confirmations.

## 0 · Revision history

**Revisions 2 to 5** (superseded design): a text-only archival transfer test
between a no-records baseline and a records-only condition, with frozen
roles, a four-class precedent census, dimension-level scoring, controlled
calibration, and hardened execution rules. All of that machinery is carried
forward where it still applies; the transfer test itself becomes a deferred
sub-study.

**In revision 6 (this version):**

- The problem statement is corrected. Removing source and rendered-UI access
  was testing the wrong thing: in a realistic workflow, agents already have
  components, stylesheets, screenshots, and project history, and a useful
  authority must improve consistency on top of those mechanisms, not
  substitute for their absence.
- The central question becomes: how much does an explicit design authority
  reduce design drift beyond the continuity already provided by inherited
  code, existing interfaces, and informal design precedent?
- Three conditions replace the two: A, natural continuity (source, rendered
  UI, project history); B, informal precedent (A plus the gaps, proposals,
  and decision-log archive); C, canonical authority (B plus the adjudicated,
  binding pack and the enforcement tooling).
- Drift is measured over time: convention fidelity of newly introduced or
  meaningfully modified decisions across successive handoffs is the primary
  outcome, with cross-component consistency and correction burden as
  secondary outcomes. Inherited components are always separated from new
  ones.
- The program becomes formation, then codification, then the drift test:
  a formation chain produces the common seed and the archive; an
  adjudication session converts the archive into the canon; the drift test
  runs the same seed under the three conditions through an identical,
  escalating feature sequence that forces genuinely new components.
- The feature sequence is designed for hard continuity: later handoffs
  demand components the application has never had (data visualisation, a
  command palette, a multi-step import flow), so consistency cannot come
  from reusing what exists.
- The phase structure corresponds to the review's proposed 05, 06, and 07;
  it is kept in one document for coherence and can be split later.

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
handoff. Containment: conditions never see each other's materials, and the
audit wrapper logs every authority call.

**Budgets and execution rules** (carried from revision 5): 2700 seconds
wall and 20M sum_total tokens per run; sessions one at a time as
`systemd-run --user` units; infrastructure-failure versus unsuccessful-run
replacement policy unchanged; briefs frozen as annexes; no human fixes
mid-run; agents never told the conditions or metrics.

### 5.2 Measures

**Primary: convention fidelity of new and modified decisions.** At each
handoff, the new or meaningfully modified interface elements are enumerated
from the frozen per-handoff opportunity list and the implementation diff.
For each decision point where an applicable convention exists (established
by the seed or by earlier handoffs of that chain, extracted and frozen at
each checkpoint under the same census protocol), reproduction is scored
with the frozen dimension rubric (section 6). Departures score as
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

## 6 · Shared machinery (carried from revision 5)

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

## 7 · Deferred

- **Text-only transfer sub-study** (revisions 1 to 5): retained as a
  narrower investigation, not central. Its full specification is preserved
  in git history and can be revived unchanged.
- **Tooling isolation condition:** the same canon supplied as ordinary
  documentation instead of enforced tooling, to separate information from
  enforcement. Deferred until the larger C versus B effect is established.
- **Net effort economics** and **additional seed lineages or chains per
  condition** for replication. Deferred as cost follows value.

## 8 · Owner confirmations

1. Model: pin the same one as the C-condition benchmark runs, or another.
2. Pack name: `base`; canon label `base 0.1.0-experiment` with optional
   owner ratification recorded.
3. Seed app and feature sequence: bookmarks manager progressing through
   search and sort, analytics, command palette, import wizard.
4. Handoffs: four per condition, interleaved by index; second chains
   deferred.
5. Budgets, reviewers (three predetermined), calibration set, and
   replacement policy carried from revision 5.
6. Text-only transfer stays deferred.

On confirmation this document becomes the pre-registered plan, committed
and dated, before any session runs.

## 9 · Deliverables

- The sealed seed application with per-session history, the census, and the
  exemplar sheet.
- The archive and the canon pack with Phase 2 quality measures.
- Three condition chains, each with per-handoff checkpoints, audits, and
  records; the fidelity trajectories and the blind review.
- The program report appended to this document, including the caveats in
  sections 1 and 5.3.
