# x05 · Process audit — how the sessions were run, DA consultation, prompt compliance

- **Date:** 2026-10-09 (read-only audit; nothing in the run area was modified).
- **Question driving it (owner):** did the sessions actually consult the design
  authority (C), did they follow the briefs at all, and what does that say
  about the uniform-looking outputs.
- **Evidence:** `ws/audit.jsonl` wrapper traces (every CLI call, timestamped,
  with output), `run.json` telemetry, session transcripts, the frozen briefs,
  the wrapper + CLI sources, `schedule.json` flags. No interpretation is
  sourced from anything the sessions were asked to self-report.

## 1 · Isolation as executed (verified)

| | A | B | C |
|---|---|---|---|
| Briefs (same file per handoff) | ✓ | ✓ | ✓ |
| Frozen current-state screenshots | ✓ | ✓ | ✓ |
| `PROTOCOL.md` in `reference/` | absent | present | present |
| Audited wrapper (`run-authority`) | absent | present | present |
| Pack mounted | — | `base 0.0.0-rc0` (blank) | `base 0.1.0-experiment` (canon) |
| Records in ws (`.design-authority/`) | stripped (code diff shows removals at h1a) | present, growing | present, growing |

Corroboration: C sessions' `overview` prints `base — 0.1.0-experiment`;
A handoffs themselves note ("the da CLI and the `.design-authority/` records
directory were not present in this session's environment").

## 2 · Did C consult the authority? YES — heavily and substantively

Wrapper calls per session window (A: zero, by design):

| sid | calls | mix |
|---|---|---|
| h1b | 18 | resolve×5, gap-add×6, propose×5, overview |
| h1c | 32 | resolve×6, inspect×6, search×5, golden, validate×2, gap-add×5, propose×5 |
| h2b | 19 | resolve×6, gap-add×6, propose×6, overview |
| h2c | 43 | search×15, inspect×6, resolve×10, validate×1, gap-add×4, propose×4, candidates, precedents |
| h3b | 27 | resolve×8, gap-add×8, propose×8, inspect, search |
| h3c | 49 | resolve×13, search×9, inspect×6, discover×2, gap-add×7, propose×7 |
| h4b | 29 | resolve×8, gap-add×10, propose×10 |
| h4c | 54 | resolve×14, inspect×7, search×5, discover×2, gap-add×10, propose×10, candidates×2, review, golden |

Resolve outcomes: **C** — 14 RESOLVED / 29 UNDEFINED across the chain
(canonical asks get rulings; new territory correctly returns UNDEFINED and is
filed). **B** — 27 UNDEFINED / 0 RESOLVED (blank pack, by design; filing
protocol executed, gaps+proposals each session).

h4c as the exemplar sequence: `overview` → `search surface/token/pattern` →
inspect `token/surfaces, pattern/destructive, pattern/empty-state,
component/primary-action, component/tags-status` (everything the wizard would
touch) → resolve the 9 new wizard components (all UNDEFINED) → **file 10 gaps
+ 10 proposals** → resolve guard-rail asks ("two solid primary buttons on one
surface", "a new radius or shadow for a card", "delete without confirmation",
"solid danger for a per-row trigger") → **RESOLVED** rulings. That is the
authority being consulted for decisions, not decoration.

B archive use: e.g. h4b read `.design-authority/gaps.jsonl` directly;
proposal files referenced in transcripts.

## 3 · The enforcement layer was hollow (material audit finding)

- The canon pack (`base-0.1.0-experiment`) declares **no `validators.json`**
  (contents: artifacts 6, rules 4, prohibitions 1, candidates, golden,
  scoring). The kernel runs `pack.validators` — an empty list.
  ⇒ every `validate` call returns "findings: 0 … spec score=100" **by
  construction**, on any target.
- Usage matched: 3 `validate` calls total across the whole C drift chain
  (h1c×2, h2c×1; h3c/h4c none), all against non-existent paths
  (`bookmark-list`, `token/surfaces`) — vacuous both ways.
- `discover` (semantic search) was **broken in runtime** (`da_sem not
  importable`); `golden` points at a stale `packs/triage/golden.json` and
  errors. C agents tried these and got nothing.
- ⇒ **As executed, condition C = canon + heavy consultation + filing; the
  enforcement mechanism never fired.** ("validate against canon" existed as a
  command, not as a check.) Register for the program report: the C-vs-B
  contrast in practice tested *consultation + canon*, not *tooling
  enforcement*.

**Root cause (traced same day, from the cod brief + protocol + materials):**
this is not a codification failure. The canon **was** codified — 36 records
adjudicated → 6 artifacts, 4 rules, 1 prohibition, 9 golden cases, 2
candidates; 14 RESOLVED rulings were actually served during the drift phase.
What was never *produced* is **checkable rules** (validators), at three
layers:

1. The pack-format spec marks `validators.json` **optional** ("declared
   validator commands"); the cod brief's deliverables did not include it and
   its acceptance test was only "the pack loads and answers" (overview + 3
   resolves). The session wrote `"validators": []` explicitly.
2. A validator is a declared *command* — real lint tooling. **No bookmarks
   linter was ever built or staged by anyone** (materials contain none; the
   only validator tooling on the box belongs to the real Triage authority).
   There was literally nothing to declare.
3. The B/C protocol — the thing sessions actually followed — never mentions
   `validate`. Its enforcement is consultative: resolve → adopt; CONFLICT →
   reconcile; UNDEFINED → decide + file. Sessions followed it faithfully.

⇒ The C-design's "validate against canon" (§6.3) was never operationalized
end-to-end: **consultation-enforcement worked; inspection-enforcement had
nothing to run.** Log as a program-design gap, not an execution failure.
(Reinforcing detail: the canon's rules DO shape resolve outcomes — B001
semantic-tokens etc. — so violations were surfaced only when an agent chose
to ask, never by inspection.)

**Update (same day, owner-directed):** the gap is closed and
pilot-validated — see `enforcement-rebuild.md` (base-lint v1 +
`base-0.1.1-experiment` + protocol rev2 + runner compliance gate; live
pilot pv1: validate ×2, score 100, compliance YES). The sealed run remains
as analyzed.

## 4 · Did sessions follow the briefs? (checked axes — all pass)

- **Brief read in-session:** every session (BRIEF mentions 4-10×).
- **Screenshots actually seen:** every session loaded reference screenshots as
  images ("Image read successfully": 8-26 per session — A 8-20, B 14-26,
  C 8-24). Continuity path was exercised in all conditions.
- **Features built per brief:** QA hooks present (extraction), all sessions
  diffs show the required new work; each handoff's HANDOFF.md documents what
  was built and what changed.
- **Self-testing:** 36-76 serve/curl/localhost commands per session; all
  captures report 0 console errors.
- **Commits:** 2-4 `git commit`s per session; checkpoint = committed state.
- **Budget:** sessions used 378-576 s of 2700 s and ≤31 k output tokens of the
  20 M cap — all self-terminated early, `status: ok`, `exit: 0`, no cap hits.
- **Test-server cleanup:** recorded `pkill`s are agents stopping their own
  `serve.py` test servers (one even uses the `[s]erve.py` bracket form);
  benign; no session harmed by them.

## 5 · Effort profile (context for "they all looked the same / bland")

Per session: 53-90 tool calls, ~9 min wall, 15-31 k output tokens, 8-26
screenshot views. Pattern across all 12: study brief + screenshots → re-use
existing classes/tokens for new components → wire features → quick self-test
→ file records (B/C) → handoff. Design was mostly *recombinative* (same token
set, same chrome vocabulary), and nothing in the process pushed refinement:
no visual bar beyond "read as part of the same design language", no working
validation, no iteration pressure, single pass per handoff.

## 6 · Audit limits

- Transcript greps are heuristic (regex over JSONL); counts are lower bounds.
- No per-bullet compliance scoring of the briefs was attempted; the axes above
  are the checkable ones.
- The validate finding rests on the pack contents + kernel source + audit
  outputs (all read-only).

**Recorded to accompany `objective-scoring-record.md` and
`blind-review.md`; feeds the program report.**
