# 05 · Extension-loop demo (P2 e2e)

**Date:** 2026-10-07 · **Pack:** `triage@e374f38` (v0.12.1) · **Records:**
`workspaces/extension-loop-demo/` (gap, proposal, verdict, transcripts, decision log).

This is the first full traversal of the loop the project exists to test:

```
Gap → candidate extension → review → validation → accepted/rejected/needs-info candidate
```

with the review performed by **a second clean agent context** instructed adversarially.

## What ran

1. **Gap recorded** (consumer side, via the kernel):
   need = *"Users need to see the progress of a long-running background operation
   (the AI triage job that scans new requests)"*, scope `system-wide`.
   Real gap: the goldens already pin this class as UNDEFINED (G-004).

2. **Candidate extension proposed** (`propose_extension`-equivalent path):
   a `component/progress` (determinate bar, `role=progressbar`, square, token-only),
   a `guideline/job-status-anatomy`, `depends_on: [component/spinner, component/badge]`,
   `new_primitives: ["determinate progress"]`, three deterministic compliance tests.
   Deterministic pre-checks passed: shape valid, citations resolve, tests present.

3. **Adversarial review in a clean context** — opencode run (`deepseek-flash`,
   plugins off), authority MCP connected to the same pack; reviewer prompt:
   *"Assume this extension should NOT be added. First attempt to solve the need
   using the existing authority ONLY. Only accept the need for an extension if
   the current authority genuinely cannot express it."*

## What the reviewer did (21 authority calls, all in the decision log)

- 8 `search_authority`, 8 `inspect_artifact`, 4 `resolve_design_problem`, 1 `authority_overview`.
- Resolution outcomes observed: **2 × UNDEFINED, 2 × COMPOSE**.
- It tried and **succeeded on part of the need**: the *indeterminate* half
  ("still running, not stuck") is covered by `component/spinner` +
  `recipe/status-with-text` + `pattern/dashboard` — a composition it found
  through the authority itself.
- It confirmed the *determinate, numeric* half is genuinely absent: nothing in
  the pack carries `aria-valuenow`/percent; spinner is indeterminate, badge
  static, bulkbar selection-only, tl historical.
- It **caught a resolver false positive**: `resolve("percent-complete progress …
  on a dashboard")` returned COMPOSE citing `recipe/status-with-text`, which
  cannot encode a percentage.

## Verdict: **NEEDS-INFO** (recorded; status `needs-info`)

Required changes before acceptance (verbatim from the review, condensed):

1. Demonstrate that text/count progress ("1,204 of 3,000 scanned") is
   *insufficient* for the use case.
2. Add `recipe/status-with-text` and `guideline/colour-not-alone` to `depends_on`.
3. Justify `guideline/job-status-anatomy` against `pattern/dashboard` /
   `pattern/index-eval`, or fold it into them.
4. Ground the "square" bar in a radius token.

The reviewer also separated concerns explicitly:
- **Deterministic**: `role=progressbar` + consistent `aria-valuenow/valuemax`;
  non-empty text per state; zero radius; token-only values; id-collision checks.
- **Judgment**: necessity vs text/count composition; vocabulary coherence;
  guideline overlap; `progressbar` vs `meter` semantics.

## Observations (fed back into the project)

1. **The loop works end to end** across two independent agent contexts, with
   every step recorded (gap → proposal → review → verdict → status).
2. **The review *reduced* scope instead of rubber-stamping**: it found the
   spinner+status composition for half the need and demanded proof for the rest.
   This is the intended behaviour ("do not make an LLM judge what can be tested
   deterministically" — it didn't; it mapped each aspect to the right evaluator).
3. **First real resolver-precision data point**: a recipe matched a need it
   cannot satisfy (percentage). Added to the gap log as a tuning item; the
   benchmark will quantify how often this class occurs.
4. **Deterministic checks are still thin at proposal time** (shape + citations
   only). Next iteration: a `compliance_test` runner so "tests present" becomes
   "tests executable", and the review verdict cites run results.

## Reproduce

```bash
# records live in the repo; inspect them directly
cat workspaces/extension-loop-demo/.design-authority/gaps.jsonl
cat workspaces/extension-loop-demo/.design-authority/proposals/*.json
cat workspaces/extension-loop-demo/verdict.md
python3 tools/da.py gaps --workspace workspaces/extension-loop-demo
```
