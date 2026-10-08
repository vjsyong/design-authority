# Experiment 04 · Agent-level A/B: does semantic discovery change what agents build?

Status: **pre-registered**. Plan frozen before any build was dispatched. The
review's directive: freeze retrieval development and test whether the
discovery infrastructure actually reduces the cost of making agents follow
design authority. Results are appended in section 7 after the runs and the
blind review.

## 1 · Question

Does giving agents semantic discovery (v0.4) produce more correct canonical
decisions, fewer unnecessary gaps, and fewer human corrections than lexical
discovery alone, on identical briefs?

The reviewer's framing is adopted verbatim: the experiment must distinguish
retrieval failure, resolution failure, and codification failure, and its
outcome decides whether the feature earns maintenance.

## 2 · Design

Two briefs, two conditions, two runs each: 8 builds in total.

- **Brief S (settings)**: a preference control ("flip one preference on or
  off right away"), a compact current-state display beside it, inside the
  app chrome if covered. One page.
- **Brief R (release notes)**: a list of past releases (version, date,
  one-line summary), each showing stable or beta, with channel narrowing if
  a sanctioned pattern exists. One page.

Both briefs use consumer language and deliberately include needs the lexical
path is known to miss (from experiments 02 and 03): "flip one preference on
or off right away" misses `component/px-sw` below threshold; "a status chip
showing the current state" is UNDEFINED at 4.0. This tests discovery exactly
where its benefit would appear; if it cannot win here, it will not win.

- **Condition A (lexical)**: every authority call goes through the audited
  wrapper; `discover` and `--assist` are rejected by the wrapper with an
  explanatory error, and the blocked attempt is recorded in `audit.jsonl`.
- **Condition B (lexical + semantic)**: identical wrapper, discovery
  enabled.
- Everything else is identical: same briefs, same model and agent class,
  isolated workspaces (`docs/experiments/ab/<cell>/`), the same asset copy,
  the same rules (orient, resolve in natural language, inspect every record
  before adopting, validate until clean, gaps via gap-add, complete log.md,
  cap ~30 authority calls).

## 3 · Measures

Blind-reviewed, per artifact:

- **Correct canonical adoption**: for each brief need, built from a record
  that actually governs it (reviewer cites the id and verifies the record's
  scope).
- **False authority adoption**: built from a record that does not govern the
  need.
- **Unnecessary gap**: a gap filed for a need a covering record exists for.
- **Gap detection**: genuinely undefined needs correctly filed.
- **Corrections required**: the reviewer lists the changes needed to make
  the artifact conformant, to the authority, per need.

Process, from `audit.jsonl` (machine-recorded): authority calls, validates,
gap-adds, discovery uses (B) and blocked discovery attempts (A), plus total
authority time.

## 4 · Blinding

After all builds complete, each workspace's single HTML page is copied to
`ab/blind/ART-01 … ART-08` in shuffled order with no path or label that
reveals condition. An independent reviewer (fresh context, no knowledge of
this experiment) scores each artifact against its brief and the authority
records using the rubric above. The mapping is held by the experimenter and
revealed only after scoring is complete.

## 5 · Hypotheses and decision rules

- **H1 (adoption)**: B beats A on correct canonical adoption for the
  paraphrase needs, in both briefs (mean over runs).
- **H2 (safety)**: false authority adoptions in B are not more than in A.
- **H3 (gaps)**: B files fewer unnecessary gaps than A.
- **H4 (corrections)**: B needs fewer blind-review corrections per artifact
  than A.
- **H5 (process, descriptive)**: how often B uses discovery and how often A
  attempts it (blocked attempts reveal demand).

**Decision**: if B fails H1 and H3 and H4, freeze the feature exactly as it
ships (optional, off by default, no further retrieval investment; redirect
effort to record descriptions, aliases and resolver applicability). If B wins
two or more of H1/H3/H4 without violating H2, the feature is justified as an
optional aid, still with no v0.5 retrieval machinery. No threshold or design
change is made mid-run.

## 6 · Threats, stated up front

n = 4 artifacts per condition (small; paired by brief to use what there is).
Single agent model. One independent reviewer. Briefs intentionally contain
known-hard phrasing, so absolute scores may be low for both conditions; the
comparison is the point. A-condition agents may work around misses by
rewording, which is precisely the counterfactual being measured.

## 7 · Results

Runs of 2026-10-08. All 8 builds completed; all 8 artifacts validate at
0 errors / 0 warnings / score 100. The blind reviewer (independent context,
fixed rubric, 222 authority calls of verification) scored anonymized copies.
The mapping, revealed only after scoring:
ART-01=s-b1 · ART-02=r-b1 · ART-03=r-a2 · ART-04=r-b2 · ART-05=s-a2 ·
ART-06=s-b2 · ART-07=s-a1 · ART-08=r-a1.

Blind scores (post-unblinding):

| cell | condition | brief | needs correct | false authority | unnecessary gaps | corrections |
|---|---|---|---|---|---|---|
| s-a1 | A | S | 3/3 | 0 | 0 | 3 |
| s-a2 | A | S | 3/3 | 0 | 0 | 1 |
| s-b1 | B | S | 3/3 | 0 | 0 | 1 |
| s-b2 | B | S | 3/3 | 0 | 0 | 1 |
| r-a1 | A | R | 4/4 | 0 | 0 | 0 |
| r-a2 | A | R | 4/4 | 0 | 0 | 1 |
| r-b1 | B | R | 3/4 | 0 | 0 | 1 |
| r-b2 | B | R | 4/4 | 0 | 0 | 0 |

Aggregates: **A: 14/14 needs correct (100%), 0 false authority, 0
unnecessary gaps, 5 corrections (1.25 per artifact). B: 13/14 (93%), 0 false
authority, 0 unnecessary gaps, 3 corrections (0.75 per artifact).**

Process (from the audits): B used discovery in every run (1, 3, 1, 3 calls,
8 total); A made zero attempts and the wrapper had nothing to block (the
feature was absent, not advertised). Total authority calls: 316 across the 8
builds, ranging 33 to 52 per build (several agents exceeded the ~30 cap with
exploration and said so in their logs).

### Hypothesis verdicts, against the frozen rules

- **H1 (adoption) fails.** A beats B (14/14 vs 13/14). There is no
  paraphrase need where B outperformed A: the settings readout need was
  handled correctly in all four runs by both conditions (improvised per the
  fallback policy), and on channel narrowing A was perfect (2/2) while B
  missed the marking-and-gap step once (r-b1).
- **H2 (safety) holds.** Zero false authority adoptions in both conditions.
  B's extra candidates introduced nothing wrong.
- **H3 (gaps) ties.** Zero unnecessary gaps in both conditions.
- **H4 (corrections) favors B, weakly.** 0.75 vs 1.25 corrections per
  artifact, driven by one A artifact with a three-item tail (missing
  aria-label verb, a readout that never syncs, copy vocabulary). With n=4,
  this is directional at best.
- **H5 (process).** Discovery did not change any differential outcome. The
  needs it was expected to rescue did not need rescuing (both conditions'
  agents recovered the recorded elements by rewording and search), and the
  needs that did bind were outside retrieval's reach.

### The finding behind the flat result

The battery's hard needs turned out to be **codification failures**, not
retrieval failures: there is no record at all for a preference state readout
or for channel narrowing, so no discovery layer over existing records can
close them. The retrieval-side paraphrases did not bind either, because both
conditions' agents worked around them with search, canonical rewording, and
the golden sets. The workflow absorbed imperfect retrieval in both arms, and
agents improvised visibly, marked the improvisations, and filed gaps in both
arms. That repeats the pattern of experiments 02 and 03 and extends it: the
authority process is the robust part; retrieval assistance is not the
bottleneck.

### Decision (per the frozen rule)

B fails H1, ties H3, wins only H4: below the two-of-three bar. **The feature
is frozen exactly as shipped** (optional, off by default, no further
retrieval investment). The redirect named in the pre-registration stands:
record descriptions, aliases, resolver applicability, and disputed-resolution
handling, not more retrieval machinery.

### Threats to validity

n = 4 artifacts per condition; one model; one reviewer; briefs hard by
design; discovery used only 8 times in total, so the experiment has weak
power to show a benefit even if one exists at larger scale. The A-condition
also cannot reveal demand for discovery because the feature was absent rather
than refused.

Raw evidence: the 8 cell workspaces (`ab/<cell>/`: audit.jsonl, log.md,
index.html, gap records), `ab/review/` (rubric, blind copies, reviewer audit,
score.json), `ab/process-metrics.json`, `ab/score-summary.json`,
`ab/aggregate_scores.py`, `ab/_mapping.json`.
