# Portability Spike · 05 · Portability report (Phase 9)

**Question:** can a public brand kit that was not designed around Triage be
derived into a small design system, encoded as a second Design Authority,
and served by the existing kernel without Triage-specific special cases?

**Answer: yes — `PORTABLE-WITH-GENERIC-CHANGES`.** Details below; evidence in
`docs/portability/00–04` + `benchmark/runs/orbit-a1/` + `packs/orbit/` +
`examples/orbit-reference-app/`.

---

## 1 · Representation

**Could the second system be represented without changing the core schema?
Yes.** Orbit 0.1 was authored directly in the existing pack format
(`authority.json`, `artifacts.json`, `rules.json`, `recipes.json`,
`fallbacks.json`, `prohibitions.json`, `validators.json`, `scoring.json`,
`golden.json`): 21 artifacts across all five kinds (component ×12, pattern
×4, token-set ×2, guideline ×2, reference ×1), 4 rules, 3 recipes, 2
fallbacks, 3 prohibitions. Nothing required a new concept, a new file type,
or an inheritance mechanism — a completely separate identity (`orbit`),
no Triage imports, no shared naming. The only representational lesson:
hand-authoring a pack (no builder) must supply fields the Triage curation
pipeline injects (`kind` on recipes/fallbacks/prohibitions — KCL-002); that
is a tooling gap, not a schema gap.

## 2 · Resolution

**Did the same resolution model remain useful? Yes — and all five outcomes
occurred organically in one build run** (agent asks + our probes):

- `CONFLICT` — “rounded corners and drop shadows”, “drop shadow to separate a
  panel” (prohibition signals; the agent shipped neither).
- `RESOLVED` — status display → `component/indicator`; job progress →
  `pattern/job-view`; “primary button” → `component/command` (never `btn`).
- `COMPOSE` — “confirm retiring an item permanently” →
  `recipe/destructive-confirm`; form creation → `recipe/form-section`.
- `FALLBACK` — checkbox/toggle/number/date needs → `fallback/platform-controls`.
- `UNDEFINED` — the seeded ambiguous requirement (borrower picker at scale)
  plus motion, letter-spacing and other gaps: **12 UNDEFINEDs**, respected
  by the agent as “do not do this / use the fallback”, never canonised.

Nuances recorded honestly: `CONFLICT` fires via prohibition signals, so
constraints expressed as rules/guidelines can surface as `RESOLVED` to the
constraining artifact (e.g. zebra striping → `component/register`, whose
text forbids it) rather than as a conflict; and lexical overlap can compose
loosely (a “gradient + animation” probe composed to
`recipe/status-console`). In practice the agent treated resolutions as
authoritative pointers, and the deterministic validator + its own reading
carried the fine print — which is exactly the design's judgment/vs-
deterministic split. Candidate pack-side sharpening (more prohibitions) is
noted, not required for portability.

## 3 · Triage leakage

Kernel assumptions that turned out to be Triage-derived: **exactly one.**

- **KCL-001** — validators were assumed to live inside a pinned *snapshot
  repository* (`{snapshot}` workdir). A document-derived authority has no
  such repo. Fixed generically (`{pack}` substitution — see §4).
- (Related, cosmetic: the lint parser name `triage-lint-json`; now aliased
  to the shape name `lint-json`.)

Everything else held: no authority-specific branches were added; the kernel
answers “this authority says X” — proven by 14 same-query probes across
`triage 0.12.1`, `triage-evolution 0.13`, and `orbit 0.1`
(`docs/portability/data/divergence-probes.json`): delete→`entity-delete-armed`
vs `destructive-confirm`; picker→`component/cb` vs `UNDEFINED`; button→
`btn` vs `command`; empty state→`component/empty` vs `pattern/register-view`
— every authority answered in its own world with zero cross-references.

## 4 · Kernel changes

- **Proposed: 2** (both in `kernel/design_authority/validate.py`, recorded
  as KCL-001 + its rider): `{pack}` substitution for validator workdir +
  command args; `lint-json` accepted as the parser shape name (legacy alias
  kept).
- **Genuinely generic: 2/2** — both add capability for *any* pack; neither
  names an authority; Triage behaviour is byte-identical (tests 10/10, MCP
  smoke 17/17, Triage validate re-verified).
- **Avoided by moving semantics into the pack: everything else** — the
  missing builder (hand-authoring instead), field requirements (KCL-002,
  pack fixed), prohibition breadth, vocabulary, fallbacks, recipes. Zero
  `if authority == ...` branches exist anywhere in the kernel.

## 5 · Agent behavior

**Could the agent build with the second authority? Yes — fully.** One fresh
agent, no Triage exposure (word count 0; containment clean): 15/15
interactive checks, orbit-lint 100/100, ~4.4 min, 75 authority calls
(1 overview / 18 search / 26 inspect / 28 resolve / 2 validate), 121 tool
calls total, $0.045. It read the authority deeply (including the pack's own
lint script), built a provenance-annotated stylesheet, and wrote its own
smoke test before finishing. Two honest marks: it **did not file any
`report_gap`** despite 12 UNDEFINEDs (it marked improvisations in markup and
claimed gap recording in comments — an instruction/behavior finding; the
channel itself is proven mechanically, `data/gap-demo-gaps.jsonl`), and it
read pack files directly in addition to the MCP interface (permitted;
recorded).

## 6 · Unknowns

**Did the authority expose its incompleteness cleanly? Yes.** The seeded
ambiguous requirement (borrower selection at scale) returned `UNDEFINED`
with `closest: component/chooser (6.5)` — precisely the designed boundary.
Twelve UNDEFINEDs in total; the build contains no invented canon beyond two
explicitly marked platform fallbacks. Nothing silently became “Triage says X”.

## 7 · Validation

**Could authority-specific validation run through the generic kernel? Yes**
(after KCL-001’s generic fix): `orbit-lint` is a pack-local stdlib script
(kernel knows nothing about ORB-1..4); the kernel orchestrates it and
normalises the shared report shape. Evidence: fixture with deliberate
violations → 7 findings incl. all four rule families (score 68); the
agent-built app → **100/100, 0 findings**; Triage’s own validator path
unaffected.

## 8 · Human effort

One focused working session. ≈2.4 k lines authored: derived-system docs 657,
Orbit pack 839, reference app 523, harness 391, plus ~15 kernel lines (both
generic changes). The dominant cost was **design formalisation and pack
content, not adapter code** — the ratio the spike was built to test. Zero
Triage-specific code was added anywhere.

---

## Success criteria (protocol §Primary)

1. Visually different authority represented — **yes** (red/black/white
   aerospace register vs Triage blue; verified in captures).
2. Same kernel loads and serves it — **yes** (untouched load/resolve; only
   the two generic validator substitutions).
3. Same agent-facing interface works — **yes** (75 MCP calls; golden 10/10).
4. Authority-specific rules remain in the pack — **yes** (ORB rules,
   validator script, prohibitions, recipes all live in `packs/orbit/`).
5. Agent builds a coherent small app — **yes** (15/15, lint 100/100).
6. Missing knowledge surfaced as missing — **yes** (12 UNDEFINEDs; no
   silent Triage substitution; improvisations marked).
7. No Triage-specific branches required — **yes**.

Acceptable-incompleteness clauses honoured: the authority is incomplete by
design; several requests return UNDEFINED; it is far smaller than Triage.

## Failure conditions (protocol §Failure) — none triggered

Closest call: “the pack format assumes Triage concepts” — the format held
(the one real assumption, validator workdir, was kernel-side and generic).
“Validators cannot remain authority-specific” — avoided: Orbit’s validator
is pack-local, kernel-orchestrated. “Requires concepts the kernel cannot
represent” — none found beyond the generic substitutions. “Mostly arbitrary
authored decisions” — no: every decision carries an
OBSERVED/INFERRED/AUTHORED/UNDEFINED ledger with page citations
(`docs/portability/02-derived-system.md`).

## Do-not-build list — respected

No catalogue, no studio, no inheritance, no theme switching, no Figma
import, no reverse engineering, no multi-authority arbitration, no
governance, no RBAC, no migration tooling.

## Final decision

**`PORTABLE-WITH-GENERIC-CHANGES`**

The abstraction survived a second, independently derived design system: the
kernel loaded, searched, resolved, gap-tracked and validated a system whose
vocabulary, structure and provenance share nothing with Triage except the
pack schema. The “changes” qualifier is honest rather than damning: the two
deltas are small, additive, genuinely generic substitutions (a pack may
ship its own validators; lint report shapes have a name), adjudicated
through the ledger with no authority-specific branching and no Triage
regression. The result was not optimised for: the run’s own findings (no
gap filings; resolution-lexicality nuances) are kept on the record.
