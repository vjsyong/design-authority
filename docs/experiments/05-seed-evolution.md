# Experiment 05 · Seed evolution: can an unadjudicated precedent archive transmit a design language?

Status: **revision 4, incorporating the adversarial review**. All eight items
of the review's minimum revision checklist are addressed. Section 8 lists the
last owner confirmations; on confirmation this document is frozen as
pre-registered, and deviations are appended as D-n entries afterward, never
edited in place.

## 0 · Revision history

**In revision 2:** research question narrowed to archival transfer; mandatory
records-only and baseline controls, never conditioned on outcomes; B
continuation chain replaced by independent controlled builds; forced new
work per session; role-aware matched-region consistency as the primary
measure; hypotheses restructured; handoff arithmetic corrected; multiple
anonymized reviewers.

**In revision 3:** H3 split so baseline is never scored on information it
never received; six target roles frozen; blinded precedent census at seal
time; scoring and reviewer combination specified; calibration rule fixed
(anchor disagreement not disqualifying); text-only intervention scope stated;
deferred arms per review (Tier 1 only, no B chain).

**In revision 4 (this version), per the adversarial review:**

- The calibration midpoint is no longer the effect threshold. Three concepts
  are separated: instrument discrimination, measurement reliability, and the
  minimum meaningful treatment effect, which is now one full role
  (1/K on the normalized scale), justified from the scoring granularity.
- The six roles have a frozen opportunity matrix with guaranteed
  opportunities in Phase A and required surfaces in Phase B. Missing
  required implementations count as failures, never exclusions. Below four
  established roles, the primary transfer evaluation is not performed.
- Established is operationalized (repeated compatible use across at least
  two distinct opportunities, traceable record), with explicit handling for
  conventions observed only once.
- Role scoring is dimension-level and role-specific: visual roles score
  visual dimensions, interaction roles score presentation plus behavioral
  dimensions. Weights, thresholds, viewport handling, and missing data are
  frozen. Acknowledged deliberate departures are excluded from scores and
  reported with rationale; unacknowledged departures count as
  non-reproduction.
- H3 is strictly temporal and mechanistic (inspection before implementation,
  fidelity to established precedent), not a second version of H2.
- Phase B results are explicitly conditional on one frozen archive, and run
  order is randomized and interleaved.
- The task specification, budgets, reviewer count, and cost tolerances are
  frozen concretely (sections 2, 3, 6).
- Baseline reporting is per role; a distinctiveness note documents whether
  A's conventions offer plausible room for transfer against model priors.
- Blinding is strengthened: randomized orientation, order, and identifiers;
  reviewers independent of execution; exact agreement reported alongside
  tolerance agreement; three reviewers predetermined.
- The negative-result wording is corrected: "transfer was not demonstrated
  under the tested configuration," followed only by evidence-supported
  explanations.

## 1 · Question

**Primary:** can a coherent design language emerge from agent-generated
decisions and be transmitted to fresh agents through an unadjudicated
precedent archive, without access to the original implementation?

**Inferential boundary, stated now:** this experiment estimates the
descriptive transfer effect of one frozen, agent-generated precedent archive
across repeated fresh-agent implementations of one target task. It is not a
general estimate of how reliably archival transfer works across different
archives, applications, or models. The archive is a single experimental
unit.

**Claims, kept separate:**

- **Claim A (Phase A, exploratory):** continuity of conventions across
  fresh-agent handoffs under combined code inheritance, visible precedent,
  and written records. Success is descriptive and is not evidence that the
  textual archive caused continuity.
- **Claim B (Phase B):** transfer through text-only records, without code or
  rendered references, against a no-records baseline.

**Progression.** This experiment tests whether informal precedent transmits.
A follow-up experiment asks whether human adjudication improves the archive.
The long-term question is whether the process reduces ongoing design
correction.

Three record states must not collapse into one another, and the report keeps
them distinct throughout:

- a **gap** is evidence that an agent improvised;
- a **proposal** is a candidate normative claim;
- a **published authority record** is a binding norm.

Nothing is promoted to records during this experiment. The archive under test
is the workspace store: gaps, proposals, decision logs.

## 2 · Design

**The blank authority.** A new pack (proposed name `base`, version
`0.0.0-rc0`): identity only; empty artifacts, rules, prohibitions, fallbacks,
recipes, golden. It loads in the kernel, resolves UNDEFINED for every ask,
and warns nothing.

**Frozen target roles and opportunity matrix.** Six roles are frozen before
execution. Each role has at least two distinct opportunities within Phase A
and a required surface in Phase B:

| Frozen role | Phase A opportunities | Phase B requirement |
|---|---|---|
| Primary action | A1: add bookmark; A2: bulk apply action; A3: save in edit flow | Add meal or recipe |
| Destructive confirmation | A2: bulk delete confirmation; A3: single delete confirmation | Delete meal or recipe, with confirmation |
| Empty state | A1: first-run empty list; A2: no filter matches; A3: collection empty after cleanup | No saved meals, and no filter matches |
| Form validation | A2: add-bookmark form (required fields, invalid URL); A3: edit form | Create and edit meal form |
| Tags or status | A2: tag filter chips; A3: tag editing | Meal categories or status |
| Surfaces and borders | A1: bookmark cards; A2: bulk-selection surfaces; A3: edit panel | Meal cards and panels |

Every Phase B run must expose all six roles with the deterministic states
listed in section 3. If a run fails to implement a required role, that is an
implementation failure scored as zero, not an exclusion.

**Phase A · Generate precedent (exploratory emergence).**

Three fresh sessions on one app, sequential, one pinned model:

| Session | Required new work |
|---|---|
| A1 | Bookmarks manager: shell, list, navigation, primary action (add), cards |
| A2 | Tag filtering with empty-filtered state, bulk actions (bulk delete confirmation), add form with validation, selection surfaces |
| A3 | Edit flow (save, validation), single delete confirmation, tag editing, responsive details |

Protocol per session (pack AGENT-PROMPT plus session brief): resolve before
deciding; file a gap for every uncovered decision unit with the fallback used
and its evidence; at session end convert recurring or structural choices into
proposals; before any visual decision read the earlier builds and the
records, match what exists or explicitly flag and file divergence; stop
cleanly with the app runnable and a HANDOFF.md. Proposals are nonbinding
precedent, not authority: the published pack remains empty throughout, and
an agent treating a proposal as binding is a protocol violation recorded in
the analysis.

At the end of A3 the checkpoint is **sealed**: code and records frozen with
SHA-256 manifests. At seal time, strictly before any Phase B run, an
independent classifier scores each frozen role against a fixed rubric,
producing the **precedent census**:

| Classification | Operational meaning |
|---|---|
| Established | Repeated compatible use across at least two distinct opportunities, supported by a traceable record |
| Observed once | One clear implementation, insufficient evidence of stability |
| Inconsistent | Multiple incompatible treatments without a documented exception |
| Absent | No usable evidence of a convention |

K is the number of roles classified Established. If K is below 4, the primary
transfer evaluation is not performed and the result is reported as formation
insufficient. The classifier cannot know transfer outcomes because none
exist yet.

**Phase B · Controlled transfer.**

The same meal-planner specification, identical tools, identical broad visual
brief, identical frozen budgets in both conditions. One fresh agent per run,
three independent runs per condition. Each run starts a brand new app repo
and a fresh workspace for its own filings. Conditions:

| Condition | Prior code | Prior records | What it isolates |
|---|---|---|---|
| Baseline | no | no | Same brief and model priors alone |
| Records-only | no | yes | Archival transfer (primary claim) |

Isolation for records-only runs: the archive is **text only** (gaps,
proposals, decision logs; any binary or image evidence stripped), with no
access to A's source, rendered output, or screenshots. Containment follows
the benchmark discipline, and tool inputs are audited for attempts to locate
A (count must be 0).

**Execution order.** The six Phase B runs are interleaved and randomized:
the run order is fixed by a recorded seed at freeze, alternating conditions
so no condition runs as a temporal block. Each run records start and end
times.

Every condition files its own records during its run, per protocol, and the
UI workload is identical. Code-only and full-context arms are deferred to a
follow-up and are **not run here**. There is no B handoff chain.

**Frozen task specification.** The agent-facing brief texts (Phase A
sessions, Phase B runs, protocol text) are frozen verbatim as annexes at
freeze time and are not edited afterward. The tables above define their
required content.

## 3 · Measures

**Decision units.** A fileable decision is one of: a component treatment, a
semantic colour role, an interaction convention, a layout pattern, or a
deliberate exception. Filing granularity is per decision unit, never per CSS
declaration.

**Deterministic fixtures.** Every scored artifact is captured in five
scripted states: empty dataset, populated list, filtered view (tag or
category applied), invalid form submission, and confirmation open. Screenshot
capture at both viewports uses scripted data seeds (fixed localStorage
fixtures) so states are identical across runs. Screenshots and measurements
are captured by the experimenter, never from an agent's self-report.

**Role scoring, dimension-level and frozen.**

- Visual roles (primary action, surfaces and borders, tags or status) score
  visual dimensions: palette, radius, typography role, spacing rhythm, and
  border or treatment.
- Interaction roles score presentation plus behavioral dimensions.
  Destructive confirmation: trigger placement, confirmation pattern
  (dialog, inline, undo), destructive emphasis, cancel-first default,
  acknowledgment recorded. Form validation: timing (submit, blur, live),
  error placement, message treatment, invalid-field signaling, recovery
  affordance.
- Each dimension is pass or fail, independently; a palette mismatch does not
  veto other dimensions. Role score: 2 when all mandatory dimensions pass,
  1 when at least half pass, 0 otherwise.
- Acknowledged deliberate departure: a departure documented at
  implementation time in the run's own records is excluded from the role
  score and reported separately with its rationale. An unacknowledged
  departure counts as non-reproduction.
- Viewports are separate observations: the primary analysis uses desktop
  1280; mobile 390 is reported separately, never averaged in.
- All six roles are applicable in every Phase B run by construction.
  Missing data is failure, per section 2.
- Dimension-level scores are reported alongside every composite.

**Convention reproduction rate.** For each run: R_i = (sum of role scores) /
(2K), over the K roles classified Established in the census. Reported as
every individual run value, per-role tables for both conditions, and
condition medians. Raw Jaccard overlap over computed-style values remains a
secondary diagnostic. A distinctiveness note reports which of A's
established conventions also appear in the no-authority calibration builds
(that is, are plausibly generic model priors), reported by role, never
excluded from analysis.

**Instrument discrimination, reliability, and the minimum meaningful
difference (three separate things).**

- *Discrimination* is established during calibration and reported per role:
  does the instrument separate anchor pairs that are known-same from pairs
  that are known-different? Calibration anchors share the relationship of
  the main comparison, independently implemented different applications with
  and without a shared authority: (a) Triage concept site versus Duty
  console (shared authority, existing builds), and (b) two reduced-scope
  calibration builds commissioned at setup from the frozen Phase B brief
  with no records and no prior code (no shared authority; they also serve as
  the model-prior reference). Each anchor is reported individually; bands
  are never pooled into a threshold. Same-lineage pairs (Cadence v1 versus
  v3) are diagnostic only and are excluded from threshold derivation. For
  any role the anchors do not expose, discrimination is reported as unknown
  and quantitative results for that role are flagged, with the blind measure
  carrying the weight for it.
- *Reliability* is reported as inter-rater agreement: exact agreement and
  the within-one-point share across the three reviewers, per pair.
- *The minimum meaningful treatment effect (MMD)* is one fully reproduced
  established role: MMD = 1/K on the normalized scale (approximately 0.167
  when K = 6). It is committed now, grounded in the scoring granularity, and
  is not derived from calibration.

**H2 gate.** H2 holds only when all of: K is at least 4; the difference
between condition medians, delta_R = median(R_records) minus
median(R_baseline), is at or above MMD; the blind median improvement is at
least 1.0 point in the same direction; and the instrument is discriminating
for the affected roles. Sensitivity analyses (means instead of medians,
leave-one-role-out) are reported as secondary and can never override the
primary decision. Individual runs are always reported; a threshold crossing
is not described as statistical confirmation.

**H3, temporal and mechanistic.** For each established, accessible
precedent, per records-only run: was the relevant record inspected *before*
implementation of the corresponding surface began (timestamps from the
audited wrapper and the transcript step timeline), was the implementation
faithful to the established precedent or an acknowledged departure, or was
it not consulted at all. Reported per role. This replaces any use of
"correct reproduction"; fidelity is measured against established precedent,
because no adjudicated authority exists in this experiment.

**Unsupported deviation rate (records-access runs only).** The proportion of
applicable, accessible conventions a run violates without acknowledging the
departure. Not scored for baseline runs, which never received the archive.

**Cost and correction requirements.** Budget per run, frozen: 2700 seconds
wall and a 20M sum_total token cap. Derivation: the benchmark's
authority-condition single-page runs had a median of about 633 seconds and
8.9M sum_total tokens; app builds are roughly twice the scope, so caps are
set near 2.2x the benchmark median. Per run, report completion status per
view, token use, wall time, and whether budget exhaustion affected any
role's implementation (censored outcomes are named, not hidden). Identified
correction requirements use a severity rubric: S1 conformance-critical
(wrong role treatment or violation of an established convention), S2
in-view inconsistency, S3 polish; weighted 3, 2, 1 and normalized per
implemented view. Tolerance for H4: records-only median tokens and wall
time within 1.25x baseline medians, and severity-weighted requirement
scores per view within 0.5 severity points of baseline.

## 4 · Blinding

Reviewers do not know the condition, run number, or which screenshots come
from where. Pair orientation (which side is A), presentation order, and
identifiers are randomized. Reviewers are independent of agent execution.
The mapping is sealed until scoring ends. Three independent reviewers are
the predetermined target; if fewer are available that is logged as a
deviation. Each reviewer answers, per pair: "how likely are these interfaces
to belong to the same design system" (1 to 5), and "which elements are
consistent or inconsistent" (itemized). Calibration anchors are embedded in
the shuffled set to describe instrument discrimination and collect
qualitative notes. A reviewer disagreeing with an anchor's intended
classification is not disqualified; disagreement patterns are reported, and
the itemized explanations are treated as diagnostic evidence about why a
quantitative measure reads as it does.

## 5 · Hypotheses and decision rules

Framed as exploratory. Phase A is a single lineage; its transitions are not
independent observations, and H1 concerns continuity under combined
mechanisms (code inheritance, visible precedent, written records), reported
descriptively. Phase B is the primary comparison surface.

- **H1 (Phase A, continuity):** newly introduced elements in A2 and A3
  preserve the conventions established earlier, judged on the new-element
  regions, not whole pages; descriptive only.
- **H2 (Phase B, archival transfer):** delta_R at or above MMD, blind median
  improvement of at least 1.0 in the same direction, K at least 4,
  discriminating instrument.
- **H3 (mechanism, records-only):** among established and accessible
  precedents, the proportion inspected before implementation and reproduced
  with fidelity, or explicitly departed from; reported per role.
- **H4 (cost):** records-only within the frozen cost tolerances, wall time
  and tokens within 1.25x baseline medians, severity-weighted requirements
  within 0.5 points per view.

Decision table, fixed in advance:

| Result | Decision |
|---|---|
| Fewer than 4 established roles | Formation insufficient for the planned primary transfer evaluation |
| delta_R at or above MMD, blind improvement at least 1 point, discriminating instrument | Descriptive evidence supporting archival transfer |
| 0 < delta_R < MMD | Positive but below the defined meaningful difference |
| delta_R at or below 0 | No observed advantage in the primary role score |
| Objective and blind measures disagree | Mixed evidence; both outcomes reported separately |

Interpretation notes, fixed in advance. If no meaningful difference is
observed, the conclusion is "transfer was not demonstrated under the tested
configuration," followed only by evidence-supported explanations, which may
include weak precedent formation, insufficient consultation, ineffective
prompting, application mismatch, constrained budgets, inadequate
measurement sensitivity, or genuinely insufficient textual specification.
The last is not assumed. A negative result bounds the text-only,
unadjudicated configuration under one archive, one model, and one target
task.

## 6 · Mechanics, controls, threats

- Audited wrapper per workspace; every authority call logged. Sessions run
  one at a time, chained as `systemd-run --user` units, transcripts archived
  with step timelines.
- Frozen budget per run: 2700 seconds wall, 20M sum_total tokens.
- No human fixes, no mid-run codification, no re-runs except infrastructure
  failures, logged as deviations.
- The precedent-consult tooling designed earlier remains on ice. The
  instruction layer stands in for it. Stated in the report.
- Threats: one archive is one experimental unit (three records-only runs are
  replications of agent behavior conditional on that archive, not three
  independent formation events); one model; possible ceiling effect if A
  converges on generic model priors, quantified by the distinctiveness note
  and the no-authority calibration builds rather than assumed away;
  reviewer learning mitigated by randomized orientation and order;
  recorded budgets may censor slow runs, which is reported.
- Agents are never told this plan, the conditions, or the metrics; briefs
  are frozen annexes.

## 7 · Results

To be appended after the runs, the census, the calibration, and the blind
review. Materials live under `docs/experiments/seed-evolution/`: per-run
workspaces and audits, sealed checkpoint manifests, the precedent census,
fixture screenshots, census outputs, reviewer sheets, the calibration
record, the run-order seed, and the sealed mapping.

## 8 · Final confirmations (owner)

1. Model: pin the same one as the C-condition benchmark runs, or another.
2. Blank authority name: placeholder `base`.
3. Confirm the frozen budgets (2700s wall, 20M tokens), cost tolerances
   (1.25x, 0.5 severity points per view), and three predetermined reviewers.
4. Confirm commissioning the two reduced-scope no-authority calibration
   builds at setup.
5. Confirm that agent-facing brief texts are frozen as annexes at freeze
   time.

On confirmation: this document becomes the pre-registered plan, committed
and dated, before any session runs.

## 9 · Deliverables

- Phase A app (bookmarks) with per-session git history and the sealed
  checkpoint, including the precedent census.
- Phase B apps (meal planner), one per run, each with an audit and records.
- The archive under test, archived verbatim.
- The calibration record, the census, and the blind-review and traceability
  report appended to this document.
- Deferred: the code-only and full-context arms and the adjudication
  experiment, as specified.
