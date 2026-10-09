# Round 3 concept — collaborative aliasing and tagging

Status: **concept, logged 2026-10-09** (owner-directed). Desk study only — no
experiments run, no implementation started. Every claim below cites the files
read at the time of writing (section 7).

## 1 · The idea

When an agent files a proposal (and the gap beneath it), it should tag two
things alongside the record:

1. **the scope of its own functions** — which parts of its product this
   proposal serves (the functional context that made the need real); and
2. **the aliases or concepts it wishes to attach** — the vocabulary the
   agent tried, would try, or wants the eventual record to be resolvable
   under.

*Collaborative* because the authority's vocabulary is then co-authored by its
consumers: every filing nominates terms; upstream curation adjudicates
structured nominations instead of reconstructing vocabulary from prose.

## 2 · Why now — the 0.12.2 worked example

The most recent curation came out of exactly this shape, done by hand. A
consumer (the driftexp blind-review app) filed
`gap/20261009-024914-945233`; its free-text need carried the phrasings
"404 page" and "not found page". The curator extracted them into alias
nominations, the record gained the two aliases plus a provenance block, the
golden set pinned both phrasings, and the change landed as triage **0.12.2**
(commit `2307e53`, tag `v0.12.2`). Structured at filing time, those phrasings
would have arrived as `proposed_aliases` — machine-consumable and clusterable
across consumers.

## 3 · What already exists (facts)

- **Gap records** carry `scope_hint` (coarse: component / pattern / …),
  `context{}`, `evidence[]`, `searched/closest/why_insufficient`, plus
  `precedent_warnings` / `candidate_hints`. There is no function-scope field
  and no alias field (`docs/spec/04-interfaces.md` §3).
- **Proposal records** require `problem, insufficiency, reuse_case,
  composition_check, proposed, tests`; `proposed{}` is freeform. No tags
  (`records.py`; spec 04 §3).
- **Proposal review** already includes the reuse question — "is this
  genuinely reusable beyond this project?" — which function-scope tags
  would evidence directly.
- **Aliases are first-class**: scoring weight 4 with a +5 whole-phrase bonus
  (`references/pack-kernel.md`); curated in the pack generator
  (`EXTRA_ALIASES`, `docs/synthesis/triage/tools/build_triage_pack.py`);
  alias adoption is the lowest rung on the abstraction ladder
  (`DOCUMENTATION-FIX`, `docs/spec/05-governance-and-freeze.md` §1).
- **The evolution loop is built for this**: phase 1 consolidates raw records
  with "phrasing ≠ separate need" (`docs/evolution/00-gap-evidence.md`);
  phase 2 explicitly asks "docs/aliases?" as one of its seven questions;
  phases 4–6 are adversarial review, Authority CI, release
  (`docs/evolution/README.md`).
- **Constructive record-building**: `add_gap` / `add_proposal` build record
  dicts key-by-key (`kernel/design_authority/records.py`), so new top-level
  fields are dropped unless the kernel is taught to store them. (A
  zero-change hack — stuffing tags into `context{}` — works today but is
  invisible to every tool; not recommended.)
- **Precedent for consumer-side structured records**: disputes (0.5) added a
  record kind plus replay fixtures without touching resolution semantics —
  the same pattern applies here.

## 4 · The change surface (feasibility)

### 4.1 Records (`kernel/design_authority/records.py`)

Optional fields on gap + proposal records (format-compatible: "0.2 adds only
optional additions"; consumers ignore unknown keys):

```
"function_scope": ["review flow", "comparison viewer"],        # freeform, ≤6
"proposed_aliases": [                                          # ≤6
  {"phrase": "404 page", "for": "component/page-state"},
  {"phrase": "checkout bar", "for": null, "note": "no record exists"}
]
```

Semantics: `for: <id>` = an alias nomination against an existing artifact
(validated against the pack, never auto-applied); `for: null` = a concept
nomination attached to the proposal itself. Both are **evidence, never
instructions** (the disputes precedent).

### 4.2 Interfaces (`docs/spec/04-interfaces.md`)

- CLI: `gap-add --tags JSON|FILE`; `propose --file` already takes a freeform
  dict, so the keys ride along once the kernel stores them.
- MCP: `report_gap(..., annotations{})`; `propose_extension` unchanged
  (proposal dict).
- The consumption protocol (`AGENT-PROMPT.md` step 3) gains one instruction:
  "when you file, tag your function scope and nominate aliases."

### 4.3 Loop consumption (`docs/evolution/`)

- Phase 1: cluster by shared `function_scope` + `proposed_aliases` — turns
  "phrasing ≠ separate need" from a curator judgement into structured
  cross-consumer agreement.
- Phase 2: the "docs/aliases?" question gets direct nominations; the
  classification stays on the abstraction ladder.
- Phase 3: a new candidate kind, *alias-adoption* — a record edit, no new
  artifacts.
- Phases 5–6: alias additions land through the ritual demonstrated in 0.12.2
  (record edit + golden pins + provenance block + version bump + tag).
- Phase 7 re-runs: adopted phrasings become replayable via their goldens.

### 4.4 Guardrails

- Caps and dedupe; nominations never auto-apply; review gate before anything
  lands; goldens mandatory for adoption.
- `function_scope` stays freeform first — controlled vocabulary, if any,
  should be *derived* by clustering from real filings, not declared up front.

## 5 · Open questions (owner decisions)

1. **Governance layer**: optional addition under change control (the 0.2
   precedent) or a minor version entry? Record formats are listed as a
   semantic surface (`docs/spec/05`, change control), but this is a pure
   optional-field addition with no behaviour change. My read: optional
   addition + spec note; minor bump only if validation changes.
2. **Nomination scope**: which record kinds may carry nominations — gaps,
   proposals, both, disputes too?
3. **Review breadth**: when do `for: <id>` nominations warrant adversarial
   review (any nomination? only broad/conflicting ones?).
4. **Replay**: should `for: <id>` nominations also emit dispute-style replay
   fixtures (phrase → expected record) so adoption has a standing
   expectation, not only golden pins?
5. **Function vocabulary**: freeform vs controlled (recommended: freeform,
   reconcile by clustering).

## 6 · Effort and recommended staging

- **Landing the surface** (kernel fields + CLI/MCP params + spec note +
  brief update + unit tests): roughly one focused session; no new
  infrastructure; no experiments required to ship the surface.
- **Wire loop usage** when the next round fires (phase-1/2 template
  updates only).
- **Revisit vocabulary control** only if freeform clustering demonstrably
  fails in practice.

## 7 · Sources read

`docs/spec/04-interfaces.md` · `kernel/design_authority/records.py` ·
`docs/spec/05-governance-and-freeze.md` · `docs/evolution/00-gap-evidence.md` ·
`docs/evolution/README.md` · `authorities/triage/AGENT-PROMPT.md` ·
`docs/synthesis/triage/tools/build_triage_pack.py` ·
`references/pack-kernel.md` (design-authority skill) ·
`workspaces/x05-blind-review/.design-authority/gaps.jsonl`
