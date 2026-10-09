# Experiment 05 · Seed evolution: can an unadjudicated precedent archive transmit a design language?

Status: **revision 3, incorporating the second owner review**. All four
methodological corrections and both smaller improvements are applied. The
remaining owner knobs are listed in section 8; on confirmation this document
is frozen as pre-registered, and deviations are appended as D-n entries
afterward, never edited in place.

## 0 · Revision history

**In revision 2:** research question narrowed to archival transfer; mandatory
records-only and baseline controls, never conditioned on outcomes; B
continuation chain replaced by independent controlled builds; forced new
work per session with new-versus-inherited element evaluation; role-aware
matched-region consistency as the primary measure with Jaccard demoted to a
diagnostic; anchors rematched to same-brief independent pairs and
known-common-authority pairs; hypotheses restructured and framed
exploratory; handoff arithmetic corrected; seeded opportunities and a silent
drift measure introduced; multiple anonymized reviewers.

**In revision 3 (this version):**

- H3 is split so baseline runs are never scored on information they never
  received: convention reproduction is compared across conditions, while
  consultation and acknowledgment are measured only in records-access runs.
- The six target design roles are frozen before Phase A as transfer targets,
  and a blinded precedent census at the A3 checkpoint classifies each as
  Established, Inconsistent, or Absent. Formation quality and transfer
  quality are reported separately, so a weak archive cannot be scored only
  on its strongest records.
- Scoring, aggregation, missing-role handling, reviewer combination, and the
  minimum meaningful difference are all specified before data exists, with
  the difference threshold derived from a calibration exercise rather than
  chosen after seeing results. No significance testing at this n; individual
  run values, paired role comparisons, and descriptive effect sizes only.
- The blind-review calibration rule no longer disqualifies reviewers for
  disagreeing with an anchor's intended classification. Calibration
  describes instrument discriminability and collects qualitative notes;
  inter-rater agreement is reported.
- The tested intervention is stated precisely: text-only, unadjudicated
  precedent. A negative result bounds that specific configuration, not
  design precedent in general; a follow-up may add rendered references.
- Interpretation of a positive result is softened, and "human corrections"
  is renamed identified correction requirements.
- Per the review, no experimental arms are added and the chain is not
  extended: code-only and full-context are deferred to a follow-up, and the
  Tier 3 B handoff chain is removed. This experiment runs Tier 1 only.

## 1 · Question

**Primary:** can a coherent design language emerge from agent-generated
decisions and be transmitted to fresh agents through an unadjudicated
precedent archive, without access to the original implementation?

**Secondary (Phase A):** across fresh-agent handoffs on one application, do
newly introduced elements preserve the conventions established by earlier
sessions, with no human adjudication?

**Progression.** This experiment tests whether informal precedent transmits.
A follow-up experiment asks whether human adjudication of the archive into
canonical authority improves coherence and transferability. The long-term
question is whether the process reduces ongoing design correction. Each
stage yields an interpretable negative result on its own.

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

**Frozen target roles.** Before Phase A begins, six target design roles are
frozen as the transfer targets: primary action, destructive confirmation,
empty state, form validation, tags or status treatment, surfaces and
borders. These are fixed now, not selected later.

**Phase A · Generate precedent (exploratory emergence).**

Three fresh sessions on one app, sequential, one pinned model:

| Session | Required new work |
|---|---|
| A1 | Bookmarks manager: list, navigation, primary actions, shell |
| A2 | Tag filtering, empty state, bulk actions |
| A3 | Edit flow, destructive confirmation, responsive details |

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
SHA-256 manifests. At seal time, and strictly before any Phase B run, an
independent classifier scores each frozen target role as Established,
Inconsistent, or Absent against a fixed rubric, producing the **precedent
census**. The classifier cannot know transfer outcomes because none exist
yet.

**Phase B · Controlled transfer.**

The same meal-planner specification, identical tools, identical broad visual
brief, identical per-run budget in both conditions. One fresh agent per run,
three independent runs per condition. Each run starts a brand new app repo
and a fresh workspace for its own filings.

| Condition | Prior code | Prior records | What it isolates |
|---|---|---|---|
| Baseline | no | no | Same brief and model priors alone |
| Records-only | no | yes | Archival transfer (primary claim) |

Isolation for records-only runs: the archive is **text only** (gaps,
proposals, decision logs; any binary or image evidence stripped), with no
access to A's source, rendered output, or screenshots. Containment follows
the benchmark discipline, and tool inputs are audited for attempts to locate
A (count must be 0).

Every condition files its own records during its run, per protocol, and the
UI workload is identical. Code-only and full-context arms are specified for
the deferred follow-up experiment and are **not run here**. There is no B
handoff chain.

## 3 · Measures

**Decision units.** A fileable decision is one of: a component treatment, a
semantic colour role, an interaction convention, a layout pattern, or a
deliberate exception. Filing granularity is per decision unit, never per CSS
declaration.

**Role-aware consistency (primary objective measure).** From the frozen
checkpoints and the finished runs, capture matched interface regions at
standard viewports (desktop 1280, mobile 390) for each frozen target role.
Compare like with like: A's primary action against B's primary action, A's
surfaces against B's surfaces. Each role pair scores 2 (reproduced: palette,
radius, type role and spacing rhythm agree within tolerance), 1 (partial),
or 0 (not reproduced). Tolerances are fixed at setup via the calibration
exercise below. Roles are weighted equally. A role is **applicable** when
B's specification requires that surface; roles B lacks entirely are excluded
from both sides of a comparison, never scored as zero. Raw Jaccard overlap
over all computed-style values is reported as a secondary diagnostic only.

**Convention reproduction rate (compared across conditions).** Per
applicable frozen role, per run: score sum divided by twice the number of
applicable roles. Reported as every individual run value plus condition
medians, and as per-role tables showing baseline and records-only runs side
by side.

**Precedent consultation rate (records-access runs only).** For each
applicable role: did the run locate and inspect the relevant archived
records. Not scored for baseline runs, which never received the archive.

**Unsupported deviation rate (records-access runs only).** The proportion of
applicable, accessible conventions the run violates without acknowledging
the departure. The silent-drift measure. Not scored for baseline runs.

**Blind review.** Matched-region screenshot pairs, shuffled and anonymized:
within-A handoffs (A1 vs A2, A2 vs A3), each Phase B run against A, baseline
pairs against each other, and calibration anchors measured with the same
instrument: (a) same-brief independent builds and (b) distinct apps under
one known common authority (candidates: the Triage concept site versus the
Duty console). Each reviewer answers two questions per pair: "how likely are
these interfaces to belong to the same design system" (1 to 5), and "which
elements are consistent or inconsistent" (short, itemized). Three
independent reviewers where available; the mapping is sealed until scoring
ends.

**Calibration and the meaning of an improvement.** Before Phase B, run the
instrument over a fixed calibration set: the known-same band is distinct
apps under one known authority (the Triage concept site versus the Duty
console) and same-lineage revisions (Cadence v1 versus v3); the
known-different band is one app form under different authorities (the Wink
site versus the Leader site). The minimum meaningful difference for role
scores is the midpoint between the two bands' medians, fixed before any
Phase B run; if the bands overlap, the instrument is declared
non-discriminating at this scale and that limitation leads the report.
Reviewer handling: per pair, the mean across reviewers; per-reviewer
values and inter-rater agreement (share of ratings within one point) are
reported alongside. H2 requires both: a condition-median role-score
difference at or above the set minimum, and a blind median difference of at
least 1.0 point in the same direction. Direction across individual runs is
reported as a robustness display. No significance testing at this sample
size; a marginal win is described as marginal, not as proof.

**Record transfer, traceable.** For each frozen target role that Phase A
established (per the census), per run: was the relevant decision available
in the provided material, was it found and inspected, was it reproduced, and
if divergent, was that deliberate and recorded.

**Cost.** Identified correction requirements (reviewer-listed changes needed
for consistency; not human editing time), wall time, and token use,
comparing records-only against baseline.

All screenshots and measurements are captured by the experimenter from the
built artifact, never from an agent's self-report.

## 4 · Blinding

Reviewers do not know the condition, run number, or which screenshots come
from where. The mapping is sealed until scoring ends. Calibration anchors
are embedded in the shuffled set and serve two purposes: describing whether
the instrument separates known-same from known-different pairs, and
collecting qualitative notes. A reviewer disagreeing with an anchor's
intended classification is **not** disqualified; disagreement patterns are
reported, and the reviewer's itemized explanations are treated as diagnostic
evidence about why a quantitative measure reads as it does.

## 5 · Hypotheses and decision rules

Framed as exploratory. Phase A is a single lineage; adjacent transitions are
not independent observations. Phase B is the confirmatory surface, with
three independent runs per condition.

- **H1 (Phase A, within-app continuity):** newly introduced elements in A2
  and A3 preserve the visual conventions A1 established, judged on the
  new-element regions, not whole pages.
- **H2 (Phase B, archival transfer):** records-only runs show greater
  convention reproduction and blind-rated consistency with A than baseline
  runs, by at least the pre-set minimum meaningful difference.
- **H3 (record utility):** access to archived precedent increases correct
  reproduction of established design conventions. Within records-access
  runs, successful reproduction is supported by traceable consultation, and
  deviations from applicable precedent are explicitly acknowledged.
- **H4 (cost, optional):** records access does not worsen identified
  correction requirements, wall time, or token use beyond the set budget
  tolerance.

Interpretation, fixed in advance:

| Observed | Reading |
|---|---|
| Records-only meaningfully exceeds baseline | Evidence that the text archive supports cross-application design-language transfer under the tested conditions (text-only, unadjudicated precedent, one model, small n). Proceed to evaluating dedicated consultation tooling |
| No meaningful difference | The archive effect is not detectable at this power. Consult the precedent census: poor formation (roles Absent or Inconsistent) reads as an upstream formation failure; adequate formation reads as transfer not demonstrated in this configuration |
| Records-only below baseline | Reported honestly; investigate with the census and consultation rates before drawing conclusions |
| Records-only wins on H2 but fails consultation traceability | Similarity without traceable use; investigate review artifacts and reproduction |

Scope of the claim, stated now: the tested intervention is text-only,
unadjudicated precedent. A negative result bounds that configuration. It
would not show that design precedent generally cannot transfer, only that
this archive form lacks sufficient visual specification, which motivates
richer, evidence-grounded precedent (role-specific values, component
examples, rendered references) in a follow-up.

## 6 · Mechanics, controls, threats

- Audited wrapper per workspace; every authority call logged. Sessions run
  one at a time, chained as `systemd-run --user` units, transcripts archived.
- Budget per run: proposed 45 minutes wall and a token cap set from the
  benchmark baseline, recorded at freeze.
- No human fixes, no mid-run codification, no re-runs except infrastructure
  failures, logged as deviations.
- The precedent-consult tooling designed earlier remains on ice. The
  instruction layer stands in for it. Stated in the report.
- Threats: Phase A is one lineage (exploratory); three runs per condition is
  small; one model; the role-aware census measures surface agreement, not
  composition quality; formation quality may dominate transfer results,
  which the census separates rather than hides; calibration region mapping
  is approximate where a calibration page's markup does not expose the
  target roles cleanly, and that is reported.
- Agents are never told this plan, the conditions, or the metrics.

## 7 · Results

To be appended after the runs, the census, the calibration, and the blind
review. Materials live under `docs/experiments/seed-evolution/` in the house
layout: per-run workspaces and audits, the sealed checkpoint manifests, the
precedent census, screenshots, census outputs, reviewer sheets, the
calibration record, and the sealed mapping.

## 8 · Remaining owner knobs (everything else is settled by the reviews)

1. App genres: bookmarks manager and meal planner, or something else.
2. Blank authority name: placeholder `base`.
3. Model: pin the same one as the C-condition benchmark runs, or another.
4. Budget numbers: 45 minutes wall plus a baseline token cap, both recorded
   at freeze.
5. Interface: audited CLI wrapper as the measured path, MCP optional.
6. Reviewers: three independent if available; otherwise two.
7. Confirm the frozen target roles as listed in section 2.

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
