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

(Appended after the builds and the blind review; see the experiment record
files under `ab/`.)
