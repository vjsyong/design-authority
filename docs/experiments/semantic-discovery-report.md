# Semantic discovery for the Design Authority: implementation and evaluation report

Date: 2026-10-08 · Repository: vjsyong/design-authority · Release: **0.4.0** (tag `v0.4.0`, commits `54ae246`, `a238556`, `c7318ff`)

---

## 1 · What this report covers

The brief had three parts: implement a semantic search layer on top of the
frozen lexical resolver, run experiments on it against pre-registered
criteria, and trace how agents work with the authority once the feature is
available. A fourth piece followed: a new demo site built by an agent under
the updated system, with a machine-audited trace.

Everything below is backed by committed evidence: pre-registered plans,
result JSONs, machine-recorded call audits, and agent logs, all in
`docs/experiments/`.

---

## 2 · What shipped (0.4.0)

The retrieval assist, on the stack the review proposed and with its
boundaries intact:

- **Lexical leg**: SQLite FTS5 (BM25) over rendered search documents.
- **Semantic leg**: FastEmbed `BAAI/bge-small-en-v1.5` (ONNX, CPU, 384-d),
  brute-force NumPy cosine. No vector database, no reranker, no LLM.
- **Fusion**: Reciprocal Rank Fusion (k=60) of the two ranked lists.
- **Determination**: unchanged. The existing resolver decides CONFLICT /
  RESOLVED / COMPOSE / FALLBACK / UNDEFINED. Retrieval proposes; it never
  establishes authority.

Surfaces:

- CLI: `da discover "..."` and `resolve --assist semantic` (the assist
  attaches a `retrieval_assist` block only on UNDEFINED).
- MCP: `discover_candidates` (the 11th tool) and an `assist` parameter on
  `resolve_design_problem`.
- Off by default everywhere. Canonical records only by default; precedents
  and candidates are searchable separately and never bind.
- The kernel stays stdlib-only. The assist requires optional extras
  (`fastembed`, `numpy`) and every lexical surface is unchanged without them.

Governance: a semantic change under the change-control rule, released as
0.4.0 with a fresh freeze manifest (19 files), spec sections updated in
`docs/spec/`, and decision **D-025** on record.

---

## 3 · How the stack is assessed

Four layers, each with its own question and failure mode.

1. **Retrieval quality. Does it find the right record?** Paired per-query
   diffs between engines (lexical E0, FTS5-only E1, hybrid E2) on the same
   asks. Paired, not averaged, because the question is where engines
   disagree.
2. **Authority safety. Does it ever mislead?** The hard invariant first:
   outcome classes identical with the assist on and off. Then false
   RESOLVED counts and a hard-negative battery of forbidden retrievals.
3. **Agent behaviour. Does it change what agents do?** Traces, not claims:
   did the agent inspect before adopting, did it catch misfires, were its
   gaps real. The target state is a counterfactual A/B over the same task
   battery.
4. **System properties. Does it stay out of the way?** Latency, footprint,
   and the degradation matrix (no extras, no index, stale index, offline):
   every one must degrade to a structured unavailable, never a blocked
   workflow. Plus rebuildability: same pack hash, same index.

---

## 4 · Experiment 01: the measurements

Pre-registered before any result existed (`docs/experiments/01-semantic-retrieval.md`,
datasets frozen in `datasets/`).

**Datasets.** D1 goldens (56 cases), D2 coverage sweep (134), D3 held-out
paraphrase set (24, two flagged as implementation probes and excluded from
formal stats), D4 hard negatives (8).

**Top-3 recall (paired, same queries).**

| set | n | E0 lexical | E1 FTS5 | E2 hybrid |
|---|---|---|---|---|
| D1 goldens | 53 | 53 | 53 | 53 |
| D2 sweep | 134 | 134 | 133 | 134 |
| D3 paraphrase (formal) | 22 | 13 | 10 | 11 |

**H1 (recall) fails, honestly.** On paraphrase language the hybrid does not
lift top-3 recall over lexical; it trails (11 vs 13 of 22). A bge-base spot
check (768-d) scored 95.7% vs 96.8% for the small model on D1+D2 and did not
repair the probes, so the pinned small model was kept.

**H2 (safety) holds.** 24 end-to-end runs through the real CLI: zero outcome
class changes, zero assist-induced false resolutions. The metric did surface
three pre-existing resolver over-resolutions on new wording (panel to
`pattern/viewer` instead of `component/sheet-end`; status label to
`guideline/voice` instead of `component/badge`; row chevron to
`component/menu-item` instead of `component/menu-pop`). The assist arm
inherited exactly those three and added none.

**H3 (rescue) holds.** For 10 of the 18 baseline-UNDEFINED cases (56%) the
wanted record appears in the assist's candidate list, including pure semantic
captures lexical search never reached (switch, armed delete, combobox,
avatar, stepper, topbar, diff, keycap, dropzone, segmented control). Five
cases neither engine finds: the honest remaining tail.

**D4 hard negatives.** Forbidden-id hits in top-3: E0 2, E1 1, E2 3. The two
the hybrid introduced are exactly the reviewed risk (benign selection
surfaced `component/bulkbar`; scheduled delivery surfaced `component/msg`).
They are documented as the shipped failure mode, and they are why the assist
is retrieval-only, canonical-only by default, and always carries an
inspect-first note.

**H4 (budget) fully met.** E0 search 0.37 ms avg; E2 warm p50 12.6 ms, p95
17.7 ms; cold CLI query 1.02 s (model load included); index build 3.6 s;
index size 0.56 MB.

**Decision.** H2, H3 and H4 hold, H1 fails. Shipped as an optional,
off-by-default retrieval extension, with H1's failure stated prominently: it
does not fix paraphrase recall at the top-3 level; it gives an
inspector-facing candidate list that rescues a majority of resolve-level
misses.

---

## 5 · Experiments 02 and 03: how agents actually work with it

### 02 · Two traces of the settings-section task class

Part A, a scripted session through the real MCP server
(`docs/experiments/02-agent-trace.md`): 11 calls, 0.7 s client-side. The
paraphrase ask returns UNDEFINED, discovery surfaces `component/px-sw`, the
agent inspects, adopts under canonical wording, and the second resolve is
RESOLVED. The assist block attached on another ask proposed near-misses; the
agent did not accept them, reworded its discovery, and the right record
(badge) surfaced. Similarity ranked; wording and inspection decided.

Part B, an independent agent (fresh context, CLI): 24 logged commands. It
walked the pattern unaided, validated its artifact at score 100, and
produced two findings worth keeping:

- the assist carried the px-sw phrasing gap (resolve UNDEFINED at 4.0,
  discovery rank 3, canonical adoption clean);
- the distribution ships a `.status-chip` class in `patterns.css` with zero
  catalogue presence. The agent refused to treat an unrecorded class as
  canon, built from recorded pieces, and filed the gap with that evidence.

### 03 · The Duty demo site, machine-audited

Sean's brief: build a new demo site under Triage with the updated system and
trace what the agent does. New instrument: every authority call went through
a wrapper (`run-authority`) that records the call, output and timing to
`audit.jsonl`, so the trace is machine-recorded rather than self-reported.

- **37 authority calls, 0 failures**, 5.7 s total. Breakdown: 1 overview,
  1 flag check (`--help`), 15 resolve, 3 discover, 12 inspect, 3 gap-add,
  2 validate (sums to 37). The agent's narrative log matches the audit 37
  for 37, in order. Completeness note: the wrapper records what passes
  through it, so the agent's full live transcript was scanned afterwards;
  it contains no authority invocation outside the wrapper (every `da.py`
  mention in it is a read of the tool file). Guaranteeing exclusivity for
  future runs is a containment problem, not an instruction problem, and is
  listed under next steps.
- **12 records adopted**, all inspected first. Both pages validate at
  **0 errors / 0 warnings / score 100 on the first run**. Scope note: the
  validator checks the configured lint rules (tokens, prohibitions,
  structure). It does not establish that every semantic or perceptual
  requirement was met; that stays a human review question.
- Discovery carried exactly the three blind spots, including a new failure
  flavor: **composite ties** (chip vs index-row at 13.0 each; the margin
  rule correctly refuses to pick, so UNDEFINED).
- The best catch of the entire arc: "a skip link to jump past the
  navigation" returned `RESOLVED component/nav-item`, which is wrong. The
  agent inspected it, refused the resolution, used the shipped `.skip`
  class, and filed a gap whose recorded outcome reads `RESOLVED (misfire)`.
  This is the second observed agent-side catch of a resolver edge (the
  first was the unrecorded `.status-chip` class).

---

## 6 · Live artifacts

- **Duty demo**: <https://designauthority.seanyong.xyz/authorities/triage/demo/duty/>
  (list page, and `case.html` for the detail view), published under the
  standard taxonomy, linked from the Triage catalogue card.
- **Concept site**: <https://designauthority.seanyong.xyz>
- **Repo**: <https://github.com/vjsyong/design-authority> (PUBLIC, MIT);
  release pinned at tag `v0.4.0`.
- **Evidence**: `docs/experiments/01-semantic-retrieval.md` (plan and
  results), `01-semantic-retrieval-results.json`,
  `01-semantic-retrieval-d3-detail.json`, `02-agent-trace.md`,
  `03-agent-site-build.md`, and the raw workspaces under
  `docs/experiments/` (`agent-session-workspace/`, `duty-build/` with
  `audit.jsonl`, `log.md`, gap records).

---

## 7 · Conformance at the 0.4.0 freeze

kernel 30/30 (including 7 new semantic unit tests) · triage goldens 56/56 ·
coverage sweep 134/134 · synthesis goldens 18/18, 14/14, 17/17 · precedent
probe 31/31 · MCP smoke 22/22 (including two new semantic checks) · semantic
self-test OK (wired into `tools/check.sh`) · concept-site gate green.

---

## 8 · Limits and next steps

Stated plainly, because they matter more than the headline numbers:

- **n is small.** D3 has 22 formal cases, and the agent-level A/B
  (section 10) ran 8 builds. The paraphrase set still wants widening (more
  authors, blind labeling) before any public claims about recall.
- **The paraphrase ceiling is real.** Small embedding models do not close
  purpose-language to canonical-vocabulary gaps at this scale. Discovery
  mitigates; it does not solve.
- **Hard negatives need red-teaming.** The battery grows with adversarial
  near-neighbours across jurisdictions (destructive controls, outbound
  messaging, scheduling).
- **Resolver edges are now first-class work items.** The metric found
  composite ties, the skip-link misfire, and three over-resolutions on new
  wording. The skip-link case is the sharpest: a false RESOLVED is more
  dangerous than an UNDEFINED, because a blindly trusting agent would build
  a canonically wrong implementation. Next, in priority order: (1) a
  disputed-resolution case type with regression fixtures (query plus the
  record it must not resolve to), distinguishable from an ordinary gap;
  (2) a ranking experiment that preserves strong lexical hits and treats
  semantic matches as supplementary discovery, without changing the stack;
  (3) the agent-level A/B over the same task battery, scoring correct
  canonical adoption, false authority adoption, unnecessary gaps, and
  human corrections.
- **The skip link is not in the catalogue.** Checked: `.skip` ships in
  `core/base.css` and appears in the Triage site's own layout, but no pack
  record exists. The Duty agent's gap stands, and recording it upstream is
  a candidate.
- **Exclusivity is containment.** For future audited runs the wrapper
  should be the only reachable route to the authority (sandbox or path
  control), not merely the instructed one.
- **One operational habit.** The index is derived data, keyed by pack
  version and content hash. Rebuild it after any pack change; `da_sem.py
  stale` exits 3 when it is out of date.

---

## 9 · Provenance

Design, implementation, experiments, and this report: Hermes agent session
with Sean, 2026-10-08. The 0.4.0 release followed the project's own
governance: pre-registered experiments, a fresh freeze manifest, a recorded
decision (D-025), and every claim in this report traceable to committed
evidence.

---

## 10 · Update: the agent-level A/B (experiment 04)

Run after the review's directive to freeze retrieval development and answer
the question this report could not: does semantic discovery make agents
actually better under authority?

**Design** (pre-registered in `04-agent-ab.md`): 2 briefs x 2 conditions
(lexical only; lexical plus semantic) x 2 runs, fresh agents, isolated
workspaces, condition-enforcing audited wrappers, and one independent blind
reviewer with a fixed rubric over anonymized artifacts.

**Result**: A 14/14 needs correct, B 13/14; false authority 0 in both arms;
unnecessary gaps 0 in both arms; corrections 0.75 per artifact (B) vs 1.25
(A), directional only at n=4. B used discovery in every run (8 calls); A
never attempted it. Against the frozen rules: H1 failed, H3 tied, only H4
favored B, which is below the two-of-three bar.

**Decision**: the feature stays frozen exactly as shipped, optional and off
by default, with no further retrieval investment. The experiment also
sharpened the finding: the battery's binding failures were codification
failures (needs with no records at all), which no retrieval layer can fix,
and the workflow absorbed the retrieval misses in both arms. The next
investments are record descriptions, aliases, resolver applicability, and
disputed-resolution handling.

Full record: `docs/experiments/04-agent-ab.md` and the raw workspaces under
`docs/experiments/ab/`.
