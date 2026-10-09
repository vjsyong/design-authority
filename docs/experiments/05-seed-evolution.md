# Experiment 05 · Seed evolution: can an unadjudicated precedent archive transmit a design language?

Status: **revision 5, targeted measurement and execution pass**. Addresses the
adversarial review of revision 4 in full: departures no longer enjoy scoring
exemptions, the scoring rubric is frozen to pass rules and reference
exemplars, calibration uses controlled ground truth, the blind aggregation
hierarchy is specified, correction scoring is normalized to fixed
opportunities, UI behavior is separated from documentation compliance, and
the execution rules (budget arithmetic, replacement policy, timestamps) are
frozen. Section 8 lists the last owner confirmations.

## 0 · Revision history

**In revisions 2 to 4:** archival transfer as the primary claim with
mandatory baseline and records-only conditions; independent controlled
Phase B builds; frozen six-role opportunity matrix with failures counted,
not excluded; four-class precedent census with Established operationalized;
dimension-level role scoring; H3 made temporal and mechanistic; one-archive
inferential boundary disclosed; randomized interleaved run order; budgets
and tolerances frozen.

**In revision 5 (this version), per the adversarial review of revision 4:**

- Deliberate departures are scored exactly like other departures in the
  primary fidelity measure. Every established role stays in the denominator.
  Acknowledgment is a process outcome reported under H3, never a scoring
  exemption, which also removes the asymmetry between conditions.
- The pass or fail rule for every scoring dimension is frozen, with
  prespecified numeric tolerances for visual properties and discrete
  categories for behavioral properties. Reference exemplars for each
  established role are frozen at the census checkpoint, so the evaluator
  never chooses what to compare against after seeing results.
- Calibration now uses controlled ground truth: a base interface, a faithful
  variant, and a deliberately altered variant with a frozen change list.
  The authority-relationship pairs are demoted to ecological checks, and
  the two no-authority builds are redesignated as model-prior reference
  builds, excluded from the H2 estimator.
- A predetermined rule defines what happens when calibration discrimination
  is unknown for a role.
- The blind-review aggregation hierarchy is fixed: reviewer ratings, then
  comparison means, then a run-level score, then condition medians, with the
  run as the unit of replication.
- Correction requirements are normalized by the fixed evaluation
  opportunities, not by however many views an agent implemented.
- The acknowledgment dimension is replaced by post-action feedback, a UI
  behavior; documentation compliance lives in H3.
- Budget arithmetic corrected to the actual multipliers (wall 4.3x, tokens
  2.25x of the benchmark medians), with the cap-hit caveat for H4 made
  explicit.
- Infrastructure failure versus unsuccessful run is defined on observable
  technical criteria. Implementation-start timestamps are operationalized.
- The minimum meaningful difference is described precisely as a
  two-role-point improvement, and the success claim is bounded to this
  archive, this model, this task.

## 1 · Question

**Primary:** can a coherent design language emerge from agent-generated
decisions and be transmitted to fresh agents through an unadjudicated
precedent archive, without access to the original implementation?

**Inferential boundary, stated now:** this experiment estimates the
descriptive transfer effect of one frozen, agent-generated precedent archive
across repeated fresh-agent implementations of one target task. It is not a
general estimate of how reliably archival transfer works across different
archives, applications, or models. The archive is a single experimental
unit. A successful result does not show that an unadjudicated archive
automatically produces a coherent design system. It shows that this
particular agent-generated archive transmitted measurable conventions better
than no archival access, in this controlled task.

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

Every Phase B run must expose all six roles with the deterministic states in
section 3. If a run fails to implement a required role, that is an
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
exist yet. As part of the census, the reference exemplar sheet is frozen:
for each established role, one reference instance (the A3 instance where the
role appears in A3, otherwise the latest instance) with its measured values
and behavioral categories recorded. Phase B is compared only against this
sheet.

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

**Replacement policy, frozen.** An infrastructure failure is defined on
observable technical criteria: model endpoint unavailability or persistent
transport errors, host-level interruption (unit failure, OOM kill, host
restart), harness or tooling crash unrelated to agent decisions, or
containment misconfiguration visible in logs. An infrastructure failure may
be replaced by a fresh run of the same condition in the same order position;
the failed attempt and the replacement are both logged. An unsuccessful
agent run (broken or incomplete UI, budget or context exhaustion, poor
quality, protocol violations) is never replaced and stays in the analysis.
Eligibility is decided on the technical criteria alone, never on whether
outputs look usable.

Every condition files its own records during its run, per protocol, and the
UI workload is identical. Code-only and full-context arms are deferred to a
follow-up and are **not run here**. There is no B handoff chain.

**Frozen task specification.** The agent-facing brief texts (Phase A
sessions, Phase B runs, protocol text) are frozen verbatim as annexes at
freeze time and are not edited afterward.

## 3 · Measures

**Decision units.** A fileable decision is one of: a component treatment, a
semantic colour role, an interaction convention, a layout pattern, or a
deliberate exception. Filing granularity is per decision unit, never per CSS
declaration.

**Deterministic fixtures.** Every scored artifact is captured in five
scripted states: empty dataset, populated list, filtered view (tag or
category applied), invalid form submission, and confirmation open. Capture
at both viewports uses fixed localStorage seeds so states are identical
across runs. Screenshots and measurements are captured by the experimenter,
never from an agent's self-report.

**Frozen scoring rubric.** Each role scores its own dimensions, and every
dimension has a prespecified pass rule. A palette mismatch does not veto
other dimensions; each dimension passes or fails independently.

Visual roles (primary action, surfaces and borders, tags or status):

| Dimension | Pass rule |
|---|---|
| Palette | The element uses the same colour role as the exemplar, and its value is within perceptual tolerance of the exemplar's recorded value (CIELAB delta-E 2000 at most 5, computed from sRGB) |
| Radius | Absolute difference at most 2 px, or both values are pill class (at least 999 px) |
| Typography role | Same recorded role (display, heading, body) and the same generic family class (sans, serif, mono) |
| Spacing rhythm | Matched spacing pairs (padding, gaps) within plus or minus 20 percent of the exemplar's recorded values, preserving the ordering of scale steps |
| Border and treatment | Same category as the exemplar (none, hairline, strong, shadow) |

Interaction roles add behavioral dimensions with discrete categories. Pass
requires the same category as the exemplar's recorded category, regardless
of whether the alternative is reasonable; reasonableness is not fidelity.

| Dimension | Categories |
|---|---|
| Trigger placement (destructive) | row action, toolbar, menu |
| Confirmation pattern (destructive) | dialog, inline, undo |
| Destructive emphasis | colour emphasis, outline, neutral with copy |
| Cancel-first default | cancel focused, confirm focused |
| Post-action feedback | message, undo affordance, none |
| Validation timing | on submit, on blur, live |
| Error placement | inline field, summary, toast |
| Message treatment | colour plus icon, text only, plain |
| Invalid-field signaling | border, colour, icon |
| Recovery affordance | auto-clear, manual, none |

A dimension is legitimately inapplicable only when the exemplar's own
pattern makes it unobservable; inapplicable dimensions are frozen in the
exemplar sheet at the census and removed from both the numerator and the
mandatory set, which is also frozen at the census.

**Role score.** 2 when all mandatory dimensions pass, 1 when at least half
pass, 0 otherwise. Dimension-level results are reported alongside every
composite. Viewports are separate observations: the primary analysis uses
desktop 1280; mobile 390 is reported separately, never averaged in.

**Departures.** Departures from an established convention score as
non-reproduction in the fidelity measure, whether or not the run documented
them. Every established role remains in the denominator, so the treatment
can never appear better through exemptions. Whether a departure was explicit
and recorded at implementation time is a process outcome reported under H3.
This also removes an asymmetry: baseline runs never had the conventions and
therefore cannot acknowledge departing from them.

**Convention reproduction rate.** For each run: R_i = (sum of role scores) /
(2K), over the K established roles. Reported as every individual run value,
per-role tables for both conditions, and condition medians. Raw Jaccard
overlap over computed-style values remains a secondary diagnostic.

**Distinctiveness note (model-prior reference).** Two reduced-scope
no-authority builds are commissioned at setup from the frozen brief with no
records and no prior code. They are secondary model-prior reference builds:
they feed the distinctiveness note (which of A's established conventions
also appear without any archive, that is, plausibly generic model priors)
and are explicitly **excluded from the H2 estimator**. They are not
calibration anchors.

**Instrument discrimination, reliability, and the minimum meaningful
difference (three separate things).**

- *Discrimination* is established with controlled ground truth, frozen
  before calibration: a base interface, a faithful independent variant
  retaining its role treatments (expected high agreement), and a
  deliberately altered variant whose selected role treatments are changed
  per a frozen change list (the altered roles must drop). The change list
  and labels are committed before any calibration scoring. Findings are
  reported per anchor individually, never pooled into bands. Two real-world
  pairs are kept as ecological checks only, not ground truth: the Triage
  concept site versus the Duty console, and Cadence v1 versus v3
  (same-lineage, diagnostic).
- *Reliability* is reported as inter-rater agreement: exact agreement and
  the within-one-point share across reviewers, per comparison.
- *The minimum meaningful treatment effect (MMD)* is a two-role-point
  improvement: equivalent in magnitude to fully reproducing one additional
  established role, and equally satisfiable by two roles each moving one
  level. MMD = 1/K on the normalized scale (approximately 0.167 at K = 6),
  committed now and not derived from calibration.

**The rule when discrimination is unknown.** Each established role carries a
discrimination verdict from calibration: demonstrated, not demonstrated, or
unknown. If at most one established role lacks demonstrated discrimination,
the objective analysis runs over the subset S of roles with demonstrated
discrimination, with R over 2|S| and MMD = 1/|S|, and the remaining role is
reported descriptively. If two or more roles lack demonstrated
discrimination, the objective gate is declared not evaluable and H2 rests on
the blind measure alone, labeled reduced precision. The rule is fixed now;
it cannot be chosen after seeing results.

**H2 gate.** H2 holds only when all of: K is at least 4; delta_R (median of
run-level R for records-only minus median for baseline) is at or above MMD;
the blind median improvement is at least 1.0 point in the same direction;
and the discrimination rule above yields an evaluable objective side.
Sensitivity analyses (means instead of medians, leave-one-role-out) are
secondary and can never override the primary decision. Individual runs are
always reported; a threshold crossing is not statistical confirmation.

**H3, temporal and mechanistic.** For each established, accessible
precedent, per records-only run: was the relevant record inspected before
implementation of the corresponding surface began, and was the implementation
faithful or an explicit, recorded departure, or was it not consulted.
Implementation start means the first recorded source-file creation or
modification implementing the relevant role, per transcript file-write
events or version history. Where first inspection or implementation start
cannot be confidently identified, the case is reported as unknown, never
inferred as successful consultation. Acknowledged departures are counted
here, per role. This replaces any use of "correct reproduction"; fidelity is
measured against established precedent, because no adjudicated authority
exists in this experiment.

**Unsupported deviation rate (records-access runs only).** The proportion of
applicable, accessible conventions a run violates without acknowledging the
departure, per role. Not scored for baseline runs.

**Blind review, aggregation hierarchy fixed.** Each scored comparison is one
established role in its designated scripted state, at the desktop viewport:
primary action in populated list; destructive confirmation in confirmation
open; empty state in empty dataset; form validation in invalid submission;
tags in filtered view; surfaces in populated list. Mobile is reported
separately and does not enter the primary blind score. Hierarchy: (1)
individual reviewer ratings, 1 to 5 per comparison; (2) mean across three
reviewers, one value per comparison; (3) mean across the K role comparisons,
one blind score per run; (4) condition medians of the three run-level
scores. The run is the unit of replication; no screenshot-level
pseudoreplication. Reviewers rate cropped, matched regions for scored
comparisons; full screens are provided only for the itemized qualitative
question.

**Cost and correction requirements.** Budget per run, frozen: 2700 seconds
wall and a 20M sum_total token cap. Actual multipliers against the
benchmark medians: wall 4.3x (633 s median; cap chosen because multi-view
app builds are roughly twice the scope, expected around 21 minutes, leaving
about 2.1x headroom over the expected duration), tokens 2.25x (8.9M median;
expected around 18M at twice the scope). Per run, report completion status
per required opportunity, token use, wall time, and budget-exhaustion
effects per role. Identified correction requirements use a severity rubric:
S1 conformance-critical, S2 in-view inconsistency, S3 polish, weighted 3, 2,
1, and normalized by the fixed evaluation opportunities (the six roles in
their designated states), never by however many views the agent chose to
implement; absent required opportunities count as failures in this metric
too. Tolerance for H4: records-only median tokens and wall time within 1.25x
baseline medians, and severity-weighted requirement scores per required
opportunity within 0.5 severity points of baseline. If both conditions hit
their caps in two or more of three runs each, the resource comparison is
labeled non-informative for efficiency (it measures the constraint, not the
cost), and H4 rests on the correction-requirement and completion measures.

## 4 · Blinding

Reviewers do not know the condition, run number, or which screenshots come
from where. Pair orientation, presentation order, and identifiers are
randomized; reviewers are independent of agent execution; the mapping is
sealed until scoring ends. Three independent reviewers are predetermined;
fewer is logged as a deviation. Per pair, reviewers answer "how likely are
these interfaces to belong to the same design system" (1 to 5) for scored
comparisons, and itemize consistency and inconsistency observations for the
qualitative record. Calibration anchors (controlled variants and ecological
checks) are embedded in the shuffled set; anchor disagreement is reported
and never disqualifies a reviewer.

## 5 · Hypotheses and decision rules

Framed as exploratory. Phase A is a single lineage; its transitions are not
independent observations, and H1 concerns continuity under combined
mechanisms, reported descriptively. Phase B is the primary comparison
surface.

- **H1 (Phase A, continuity):** newly introduced elements in A2 and A3
  preserve the conventions established earlier, judged on the new-element
  regions; descriptive only.
- **H2 (Phase B, archival transfer):** delta_R at or above MMD; blind median
  improvement at least 1.0 in the same direction; K at least 4;
  discrimination rule satisfied.
- **H3 (mechanism, records-only):** among established and accessible
  precedents: the proportion inspected before implementation with faithful
  reproduction, the proportion inspected with explicit recorded departure,
  and the proportion not consulted; reported per role, with acknowledgments
  counted here rather than in the fidelity score.
- **H4 (cost):** within the frozen tolerances (1.25x tokens and wall, 0.5
  severity points per required opportunity), subject to the cap-hit caveat.

Decision table, fixed in advance:

| Result | Decision |
|---|---|
| Fewer than 4 established roles | Formation insufficient for the planned primary transfer evaluation |
| delta_R at or above MMD, blind improvement at least 1 point, discrimination satisfied | Descriptive evidence supporting archival transfer |
| 0 < delta_R < MMD | Positive but below the defined meaningful difference |
| delta_R at or below 0 | No observed advantage in the primary role score |
| Objective gate not evaluable (two or more roles without demonstrated discrimination) | H2 reported on the blind measure alone, labeled reduced precision |
| Objective and blind measures disagree | Mixed evidence; both outcomes reported separately |

Interpretation notes. If no meaningful difference is observed, the
conclusion is "transfer was not demonstrated under the tested
configuration," followed only by evidence-supported explanations, which may
include weak precedent formation, insufficient consultation, ineffective
prompting, application mismatch, constrained budgets, inadequate measurement
sensitivity, or genuinely insufficient textual specification. The last is
not assumed. A positive result is bounded the same way: this archive, this
model, this task.

## 6 · Mechanics, controls, threats

- Audited wrapper per workspace; every authority call logged. Sessions run
  one at a time, chained as `systemd-run --user` units, transcripts archived
  with step timelines.
- Frozen budget per run: 2700 seconds wall, 20M sum_total tokens.
- No human fixes, no mid-run codification; replacements only under the
  frozen infrastructure-failure definition, and every failed attempt and
  replacement is logged.
- The precedent-consult tooling designed earlier remains on ice. The
  instruction layer stands in for it. Stated in the report.
- Threats: one archive is one experimental unit; one model; possible ceiling
  effect if A converges on generic model priors, quantified by the
  distinctiveness note rather than assumed away; recorded budgets may censor
  slow runs, reported with the cap-hit caveat; reviewer learning mitigated
  by randomized orientation and order.
- Agents are never told this plan, the conditions, or the metrics; briefs
  are frozen annexes.

## 7 · Results

To be appended after the runs, the census, the calibration, and the blind
review. Materials live under `docs/experiments/seed-evolution/`: per-run
workspaces and audits, sealed checkpoint manifests, the precedent census and
reference exemplar sheet, fixture screenshots, census outputs, reviewer
sheets, the controlled calibration set (change list and labels), the
model-prior reference builds, the run-order seed, and the sealed mapping.

## 8 · Final confirmations (owner)

1. Model: pin the same one as the C-condition benchmark runs, or another.
2. Blank authority name: placeholder `base`.
3. Confirm the frozen budgets (2700s wall, 20M tokens), cost tolerances
   (1.25x; 0.5 severity points per required opportunity), and three
   predetermined reviewers.
4. Confirm commissioning the controlled calibration set (base interface plus
   two variants with a frozen change list) and the two model-prior
   reference builds at setup.
5. Confirm that agent-facing brief texts are frozen as annexes at freeze
   time.

On confirmation: this document becomes the pre-registered plan, committed
and dated, before any session runs.

## 9 · Deliverables

- Phase A app (bookmarks) with per-session git history, the sealed
  checkpoint, the precedent census, and the reference exemplar sheet.
- Phase B apps (meal planner), one per run, each with an audit and records.
- The archive under test, archived verbatim.
- The controlled calibration record, the census, and the blind-review and
  traceability report appended to this document.
- Deferred: the code-only and full-context arms and the adjudication
  experiment, as specified.
