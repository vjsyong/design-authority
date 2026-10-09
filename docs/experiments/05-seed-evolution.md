# Experiment 05 · Seed evolution: does a design language emerge from filings alone?

Status: **draft for owner review**. The design below is complete; the open
decisions in section 8 need the owner's answers before the plan is frozen as
pre-registered. Nothing runs until then.

## 1 · Question

Starting from a completely blank design authority and no judge, does a
coherent design language emerge from agent filings alone, survive handoffs
between fresh agent instances, and carry over to a second, different app?

This simulates the vibes-builder scenario: the owner does not take design
decisions, agents build freely, and every uncovered decision becomes a
recorded improvisation. The risk being tested is drift. One page should not
end up looking different from another.

## 2 · Design

**The blank authority.** A new pack `base` (name and version placeholder,
proposed `0.0.0-rc0`), identity only: empty artifacts, rules, prohibitions,
fallbacks, recipes, golden. It loads in the kernel, resolves UNDEFINED for
every ask, and warns nothing. Both apps share this one authority.

**Two apps, one shared project.** Both apps live in a single project
workspace so records accumulate naturally in one `.design-authority/` store:

- **App A**: a bookmarks manager. Small but real: a list view, an edit or
  detail view, and a tags or settings view. No backend; localStorage; opens
  in a browser.
- **App B**: a meal planner. Same scale: a week view, a meal edit view, and
  a list view.

Both briefs carry the same visual direction, verbatim: "modern, minimalist,
sleek fonts, high contrast, solid colours."

**Six fresh sessions, sequential, one pinned model.** A1 builds app A and
stops. A2 continues app A from its current state. A3 continues after A2.
Then B4 starts app B fresh, with everything the A chain produced, and B5 and
B6 continue the same way. Fresh context each session; the only things that
travel are artifacts on disk.

**What every agent receives**

- The app repo at its current state (empty for A1 and B4).
- The shared records: every prior session's gaps, proposals, decision log.
- The visual brief above and the app spec for its session.
- The protocol, as the pack's AGENT-PROMPT plus a session brief:
  1. Resolve before deciding. Every visual decision goes through the
     authority first.
  2. When resolve returns UNDEFINED, decide, then file a gap with the
     fallback used and the evidence. File continuously as the build
     progresses.
  3. At session end, convert recurring or structural choices into
     proposals, so the archive reads as promotion-ready candidates.
  4. Before any visual decision, read the earlier builds and the records.
     Match what exists. If a better fit demands divergence, say so
     explicitly and file it.
  5. Stop cleanly: the app must run at session end, with a HANDOFF.md
     (done, next, open decisions) and the records appended.

**Data flow.** Session n sees session n-1's repo and the cumulative records.
Nothing else. No transcripts, no chat, no notes from the experimenter.

## 3 · Measures

**Objective census, per checkpoint.** Extract computed styles from the
running build at every handoff: distinct colours, radii, font families, type
scale, spacing. Quantize and compute overlap (Jaccard) for adjacent
checkpoints within a chain and for A-final versus B-final. Calibrate the
thresholds before any run on artifacts we already own: cadence-wink v1
versus v3 is the same-language anchor, wink versus leader is the
different-language anchor. Thresholds are set between the two anchor
distances at freeze time.

**Blind review.** Screenshot pairs, shuffled and unlabeled: A1 vs A2, A2 vs
A3, A3 vs B4, B4 vs B5, B5 vs B6, A-final vs B-final, plus the calibration
pairs. The reviewer rates "same design system?" 1 to 5. The mapping is
sealed until scoring ends.

**Record metrics**, from the audited wrapper and the decision logs:
consultation rate per session (decisions that cite a prior record), duplicate
gap rate (asks already filed), divergence incidents flagged versus unflagged,
proposals filed.

All screenshots and censuses are captured by the experimenter from the built
artifact, never from an agent's self-report.

## 4 · Blinding

The reviewer does not know which pair is which, or which screenshots come
from where. The calibration pairs are hidden inside the shuffled set, so a
reviewer who cannot distinguish them is failing a calibration check. Owner
versus independent reviewer is an open decision (section 8).

## 5 · Hypotheses and decision rules

- **H1, handoff continuity.** Census overlap for adjacent checkpoints clears
  the calibrated threshold in at least 5 of 6 handoffs, and the blind median
  for within-chain pairs is 4 or higher.
- **H2, cross-app transfer.** A-final versus B-final clears both bars.
- **H3, records get used.** Consultation rate rises across sessions and
  duplicate gap filing falls as the archive grows.

Interpretation, fixed in advance:

- H1 and H2 hold: precedent-driven evolution works without a judge; the
  language carried. Priority shifts to shipping the consult tooling as
  designed.
- H1 holds, H2 fails: within-app continuity works, cross-app transfer does
  not. The records fail to transport the language; measured conventions
  (harvest with numbers, not adjectives) become the priority.
- H1 fails: filings alone do not hold a language even inside one app. The
  consult and warning tooling moves from nice-to-have to required.
- H3 fails while H1 or H2 hold: the language carried through the code and
  screenshots, not the records. The record layer needs a redesign before any
  governance claims.

## 6 · Mechanics, controls, threats

- Audited wrapper per workspace: every authority call is logged
  (`audit.jsonl`). Sessions run one at a time, chained as `systemd-run
  --user` units, transcripts archived per session.
- Budget per session: proposed 45 minutes wall, token cap set from the
  benchmark baseline at setup. Both recorded at freeze.
- No human fixes, no mid-run codification, no re-runs except infrastructure
  failures, which are logged as deviations.
- The precedent-consult tooling we designed earlier is deliberately on ice.
  This experiment uses the instruction layer as its stand-in. We are testing
  the emergent process, not the tool support. This is stated in the report.
- Threats: one transition per pair (paired design, small n); one model; the
  census measures style surface, not composition quality; B agents may read
  app A's code directly, which is realistic and part of the transport being
  tested. A records-only control (B built with no records) is parked as the
  follow-up if H2 comes out ambiguous.
- Pre-registration discipline as usual: after the owner's answers in
  section 8, this document is frozen, committed, and deviations are appended
  as D-n entries, never edited in place.

## 7 · Results

To be appended after the runs, the blind review, and the census. Materials
will live under `docs/experiments/seed-evolution/` in the house layout
(workspaces, audits, screenshots, census outputs, sealed mapping).

## 8 · Open decisions (owner confirmation required)

1. App genres: bookmarks manager and meal planner, or something else.
   Proposed: as written.
2. Blank authority name: placeholder `base`. Pick anything.
3. Model: pin the same one as the C-condition benchmark runs, or another.
4. Per-session budget: 45 minutes wall plus a baseline token cap. Confirm.
5. Interface: audited CLI wrapper as the measured path, MCP optional
   alongside. Confirm.
6. Blind reviewer: the owner, or an independent reviewer with the owner
   unblinding after scoring. Proposed: independent if one is available,
   otherwise the owner.
7. Deferred control (app B with no records): parked, run only if H2 is
   ambiguous. Confirm.

## 9 · Deliverables

- Two runnable apps (A and B) with full git history per session handoff.
- The accumulated records archive: gaps, proposals, decision logs, audits.
- The census and blind-review report appended to this document.
- Optional phase after the report: harvest the emerged conventions into the
  first `-rc` candidate pack, the "outsource the initial design to AI"
  moment made concrete.
