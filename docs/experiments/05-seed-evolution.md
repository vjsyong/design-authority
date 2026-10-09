# Experiment 05 · Seed evolution: can an unadjudicated precedent archive transmit a design language?

Status: **revision 2, draft for owner confirmation**. Incorporates the owner
review of 2026-10-08. Nothing runs until the open decisions in section 8 are
answered and the plan is frozen as pre-registered. Deviations after that are
appended as D-n entries, never edited in place.

## 0 · What changed from revision 1

- The research question is narrowed. The primary claim is now about
  **archival transfer**: a fresh agent reproducing the language from archived
  decisions, without access to the original implementation. Emergence itself
  becomes Phase A of the design rather than half of one headline claim.
- The records-only comparison is **mandatory**, pre-specified, and never
  conditioned on outcomes. Baseline is mandatory with it. Code-only and
  full-context are pre-specified extensions, gated on budget only.
- The B continuation chain (B4 to B6) is **replaced by independent controlled
  B builds**: one fresh agent per run, several runs per condition. Handoff
  continuity remains measured in Phase A, where it belongs.
- Every session gets an explicit list of **new work**: previously unseen
  interface decisions, so continuity cannot come from mere extension.
- Evaluation splits **newly created or changed elements from inherited
  elements**. Whole-page similarity alone cannot carry a claim.
- Consistency measurement becomes **role-aware matched regions** as the
  primary objective measure. Raw value overlap (Jaccard) is demoted to a
  secondary diagnostic.
- The calibration anchors are rematched to the experiment: independent
  same-brief builds (our own baseline runs) and distinct apps under one known
  common authority, measured with the same instrument.
- Hypotheses are restructured and framed as exploratory. The handoff count is
  corrected: six sessions give five adjacent handoffs, of which four are
  within-app. A-final versus B-final is a separate comparison, not a handoff.
- Record consultation becomes traceable through a **seeded set of precedent
  opportunities**, plus an **unsupported deviation rate** (silent drift) as a
  named measure. A decision-unit definition fixes filing granularity.
- Blind review uses multiple independent reviewers where available, two
  questions, anonymized files, matched viewports and states.

## 1 · Question

**Primary:** can a coherent design language emerge from agent-generated
decisions and be transmitted to fresh agents through an unadjudicated
precedent archive, without access to the original implementation?

**Secondary (Phase A):** across fresh-agent handoffs on one application, do
newly introduced elements preserve the conventions established by earlier
sessions, with no human adjudication?

**Follow-up (separate experiment, not this one):** does human adjudication of
the archive into binding authority records improve coherence and
transferability?

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
cleanly with the app runnable and a HANDOFF.md.

At the end of A3 the checkpoint is **sealed**: code and records frozen with
SHA-256 manifests, before any transfer condition runs.

**Phase B · Controlled transfer.**

The same meal-planner specification, identical tools, identical broad visual
brief, identical per-session budget in every condition. One fresh agent per
run, several independent runs per condition. Each run starts a brand new app
repo and a fresh workspace for its own filings.

| Condition | Prior code | Prior records | What it isolates |
|---|---|---|---|
| Baseline | no | no | Same brief and model priors alone |
| Records-only | no | yes | Archival transfer (primary claim) |
| Code-only | yes (read-only) | no | Ordinary implementation inheritance |
| Full context | yes (read-only) | yes | Combined effect |

Isolation mechanics:

- Records-only runs receive the archive as **text only**: gaps, proposals,
  decision logs, with any binary or image evidence stripped, and with no
  access to A's source, rendered output, or screenshots. Containment follows
  the benchmark discipline (a workspace where A does not exist), and tool
  inputs are audited for attempts to locate A (count must be 0).
- Code-only runs get a read-only copy of A's frozen code and no records
  beyond their own fresh workspace.
- Every condition files its own records during its run, per protocol, and the
  UI workload is identical.

Tiering, fixed before any run and gated on budget only, never on outcomes:

- **Tier 1 (mandatory):** Phase A, plus baseline and records-only at three
  runs each.
- **Tier 2 (pre-specified extension):** code-only and full-context at two
  runs each, run if wall and token budget allow. Proposal in section 8.

## 3 · Measures

**Decision units.** A fileable decision is one of: a component treatment, a
semantic colour role, an interaction convention, a layout pattern, or a
deliberate exception. Filing granularity is per decision unit, never per CSS
declaration.

**Role-aware consistency (primary objective measure).** From the frozen
checkpoints and the finished runs, capture matched interface regions at
standard viewports (desktop 1280, mobile 390): primary action, card or
surface, form field, list row, status or tag treatment, heading typography,
navigation active state. Compare like with like: A's primary action against
B's primary action, A's surfaces against B's surfaces. Score each role pair
for value agreement (palette, radius, type role, spacing rhythm) on a fixed
scale. Raw Jaccard overlap over all computed-style values is reported as a
secondary diagnostic only.

**Blind review.** Matched-region screenshot pairs, shuffled and anonymized:
within-A handoffs (A1 vs A2, A2 vs A3), each transfer condition against A,
baseline pairs against each other, and two calibration anchors measured with
the same instrument: (a) same-brief independent builds (our own baseline
pairs) and (b) distinct apps under one known common authority (candidates:
the Triage concept site versus the Duty console). Each reviewer answers two
questions per pair: "how likely are these interfaces to belong to the same
design system" (1 to 5), and "which elements are consistent or inconsistent"
(short, itemized). Three independent reviewers where available; the mapping
is sealed until scoring ends.

**Record transfer, traceable.** Before Phase B, a small set of precedent
opportunities is pre-registered (for example: the primary action treatment,
destructive confirmation, empty state, form field validation, status or tag
treatment, surface and border language). Only opportunities that A actually
established count; the set is finalized against the sealed checkpoint. For
each opportunity, per run: was the relevant decision available in the
provided material, was it found and inspected, was it reproduced (versus a
divergent treatment), and if divergent, was that deliberate and recorded.

**Unsupported deviation rate.** The proportion of applicable prior
conventions that a run violates without acknowledging the departure. This is
the silent-drift measure.

**Cost of continuity.** Human corrections required (reviewer-listed, per
run), wall time, and token use, comparing records arms against baseline.

All screenshots and measurements are captured by the experimenter from the
built artifact, never from an agent's self-report.

## 4 · Blinding

Reviewers do not know the condition, run number, or which screenshots come
from where. Calibration anchors are embedded in the shuffled set; a reviewer
who cannot separate them from the experimental pairs fails the calibration
check. Owner versus independent reviewers is a decision in section 8.

## 5 · Hypotheses and decision rules

Framed as exploratory. Phase A is a single lineage; adjacent transitions are
not independent observations. Phase B is the confirmatory surface, with
several independent runs per condition.

- **H1 (Phase A, within-app continuity):** newly introduced elements in A2
  and A3 preserve the visual conventions A1 established, judged on the
  new-element regions, not whole pages.
- **H2 (Phase B, archival transfer):** records-only runs are more consistent
  with A than baseline runs are, on role-aware consistency and blind review.
- **H3 (record utility):** record access increases the share of seeded
  opportunities found and reproduced, and lowers the unsupported deviation
  rate, relative to baseline.
- **H4 (cost, optional):** records access does not worsen corrections, wall
  time, or tokens beyond the pre-set budget tolerance.

Interpretation, fixed in advance:

| Observed | Reading |
|---|---|
| Records-only beats baseline | The archive transmits the language; ship the consult tooling |
| Code-only beats baseline, records-only does not | Implementation inheritance carries the language; the archive is insufficient for transmission and needs richer, evidence-grounded precedent (role-specific values, component examples, rendered references) |
| Full context beats both | Code and records are complementary; the archive amplifies implementation inheritance |
| All conditions similar | The generic brief or model priors explain the similarity; the experiment cannot detect an archive effect at this power |
| Records-only wins on H2 but fails H3 | Similarity without traceable use; investigate review artifacts and reproduction |

## 6 · Mechanics, controls, threats

- Audited wrapper per workspace; every authority call logged. Sessions run
  one at a time, chained as `systemd-run --user` units, transcripts archived.
- Budget per run: proposed 45 minutes wall and a token cap set from the
  benchmark baseline, recorded at freeze.
- No human fixes, no mid-run codification, no re-runs except infrastructure
  failures, logged as deviations.
- The precedent-consult tooling we designed earlier remains on ice. The
  instruction layer stands in for it. Stated in the report.
- Threats: Phase A is one lineage (exploratory); Phase B seeds are few; one
  model; the role-aware census measures surface agreement, not composition
  quality; records-only agents may reconstruct more from the brief than
  expected, which the baseline arm quantifies rather than assumes away.
- Agents are never told this plan, the conditions, or the metrics.

## 7 · Results

To be appended after the runs, the blind review, and the census. Materials
live under `docs/experiments/seed-evolution/` in the house layout:
per-run workspaces and audits, the sealed checkpoint manifests, screenshots,
census outputs, reviewer sheets, and the sealed mapping.

## 8 · Open decisions (owner confirmation required)

1. App genres: bookmarks manager and meal planner, or something else.
2. Blank authority name: placeholder `base`.
3. Model: pin the same one as the C-condition benchmark runs, or another.
4. Run plan and budget: Tier 1 with three runs per core condition (proposed),
   or two; Tier 2 code-only and full-context at two each, now or later.
5. Interface: audited CLI wrapper as the measured path, MCP optional.
6. Reviewers: three independent if available; otherwise two; the owner
   included only if independent reviewers are unavailable.
7. Seeded opportunity list: approve the proposed six, adjusted against the
   sealed checkpoint.
8. Confirmation that Phase A keeps the sequential-handoff structure (A1 to
   A3) and that the B handoff chain is dropped in favor of independent
   controlled builds. If you want a B handoff chain as well, it becomes an
   explicitly labeled Tier 3 extra, not part of the primary claim.

## 9 · Deliverables

- Phase A app (bookmarks) with per-session git history and the sealed
  checkpoint.
- Phase B apps (meal planner), one per run, each with an audit and records.
- The archive under test, archived verbatim.
- The census, blind-review, and traceability report appended to this
  document.
- Deferred: harvesting emerged conventions into a first `-rc` candidate pack,
  and the follow-up adjudication experiment.
