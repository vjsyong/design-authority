# Design Authority
## System report and reproduction brief

**What it is. What it has. How to rebuild it.**

Compiled 2026-10-11 from repository state `3b4a239` (master) and specification freeze 0.5.0 (tag `v0.5.0`). Written to be self-contained: no access to the codebase is required to understand the system or to rebuild an equivalent one.

---

### 0 · About this document

This document describes the Design Authority project completely enough to rebuild an equivalent system from scratch. It is organized as:

1. **Orientation** (sections 1-2): the concept, and an inventory of everything that exists today.
2. **The system** (sections 3-9): model, semantics, formats, runtime, compiler, verification, governance, reconciliation. This is the part a rebuild executes.
3. **The processes** (section 10): how authorities are produced from source material.
4. **The evidence** (section 11): what has been measured, including failed hypotheses and limits.
5. **The rebuild order** (section 12): build steps with acceptance gates.
6. **Status** (section 13): where the project stands and what is open.

What this document cannot contain: the several hundred individual records inside the published packs, the full experiment datasets, and the commit-level history. Rebuilding an authority therefore means re-deriving its records from the source design system using section 10's processes, then calibrating until the section 12 gates pass. Everything that governs the *shape* of those records is specified here.

Conventions: RFC 2119 keywords (MUST, SHOULD, MAY) when normative. Identifiers take the form `<kind>/<slug>` (for example `component/btn`). "Kernel" means the kit-agnostic implementation of the format and semantics; "pack" means a conforming JSON directory; "consumer" means the agent or project building under the authority.

---

### 1 · What Design Authority is

**Definition.** A Design Authority is a versioned, machine-readable design contract plus the tooling that serves it to coding agents and the governance process that evolves it. It lets an agent (1) discover what a design system defines, (2) resolve a design problem, (3) inspect citable artifacts, (4) validate an implementation, (5) report gaps upstream instead of silently inventing canon, and (6) propose noncanonical extensions. The kernel is kit-agnostic: it knows artifacts, rules, recipes, fallbacks, precedents, candidates, resolutions, gaps and proposals, and nothing about buttons or colours. A design system enters only as a pack.

**The problem it addresses.** Coding agents guess at design. Design systems exist as prose documentation, screenshots and component libraries that agents cannot reliably consume, so every agent session either copies whatever pattern it has seen before or improvises silently. The founding observation: inference is fine, but **inference is not authority**. An agent may improvise when the system has no answer, but it must never present improvisation as canon, and it must be able to tell the two apart.

**The response.** One deterministic resolver over a governed record set, with a five-way outcome taxonomy (CONFLICT, RESOLVED, COMPOSE, FALLBACK, UNDEFINED); every answer cites ids validated against the pack; UNDEFINED is a first-class outcome carrying a search trace and a gap protocol; downstream evidence (gaps, disputes, proposals) flows back through a governance loop that compiles accepted decisions into new authority versions.

**The organizing abstraction** (adopted 2026-10-11): Design Authority is a **compiler for governed design decisions** with a small runtime that agents use to apply and verify them. Evidence produces decisions; approved decisions compile into authority; agents consume authority; deviations produce new evidence. Extraction, compilation, resolution and verification are stages of one model, not separate products.

**The claim the project defends.** The defensible claim is *persistent, inspectable design judgment across independent agents and successive product generations*. It is not a claim that first-pass visual quality improves because a governance layer exists. Site and README copy are audited against that distinction.

**Non-negotiable invariants** (the rules a rebuild MUST preserve):

1. **Thin kernel.** The kernel adds access and uncertainty layers only (search, resolution, recipes, fallbacks, records). It never re-models tokens, rules or component states; those stay in the source system and enter via the pack.
2. **Deterministic-first resolution.** No network, no time or locale dependence, stable ordering, byte-stable output. An optional retrieval assist, off by default, may only surface candidates; it never establishes authority and never changes an outcome class.
3. **Cited ids only.** Every id in any answer is validated against the pack before the answer is returned. The authority never fabricates.
4. **UNDEFINED is a structured success**, distinguishable from a retrieval failure (which is a tool error, never downgraded into a structured UNDEFINED).
5. **Spec-faithful precedence.** CONFLICT, then RESOLVED, then COMPOSE, then FALLBACK, then UNDEFINED. A dedicated artifact always wins over a recipe; COMPOSE applies only when no artifact directly defines the solution.
6. **Consumers never mutate the authority.** Gaps, proposals, disputes and decision logs are written to the consuming workspace only. Proposals are reviewed upstream.
7. **Agents may improvise, but must mark it**, and may never present improvisation (or a candidate) as canonical.
8. **Golden sets are the contract.** The reference pack's golden agreement is enforced at 100% by unit tests. To fix a miss, adjust curation (aliases, recipe needs) or the tokenizer; never move thresholds to fit a case.
9. **Snapshot discipline.** A pack version pins one immutable source commit; regeneration against a newer source is a new pack version, never a silent rebuild.
10. **Per-dimension measurement only.** No composite score across measurement dimensions. Instruments are frozen and criteria pre-registered before runs; failed hypotheses stay in the record.
11. **Evidence, not commands.** Downstream findings (gaps, disputes, impact) never automatically modify authority; a human-reviewed loop converts them into releases.
12. **Provenance answers "why does this artifact exist?"** from the pack alone: every normative record carries `compiled_from` approved decisions or an explicit exception block.

---

### 2 · What it has (inventory as of 2026-10-11)

**The specification.** Frozen at 0.5.0 (tag `v0.5.0`), six documents (`00-index` scope and conformance, `01-definitions` glossary, `02-pack-format`, `03-resolution-semantics`, `04-interfaces`, `05-governance-and-freeze`), plus SHA-256 freeze manifests for 0.1.0 through 0.5.0. Change control: semantic changes need a minor bump with a fresh freeze and manifest; editorial fixes are patches. Freeze history: 0.1.0 (2026-10-07); 0.2.0 adds negative precedents, candidates, lenient adjudication, tool additions; 0.3.0 adds the lexical normalisation layer; 0.4.0 adds the optional semantic retrieval assist; 0.5.0 adds disputed resolutions (2026-10-08, all).

**The kernel and runtime.** `kernel/design_authority/`: `pack.py` (load + search index + tokenizer), `lex.py` (lexical normalisation), `resolve.py` (outcome pipeline), `validate.py` (validator runner), `records.py` (gaps, proposals, disputes), `cli.py`, `mcp_server.py`. Python 3.12, standard library only; no database; packs are plain JSON directories. Entrypoints: `tools/da.py` (CLI, 17 subcommands) and `tools/da-mcp.py` (stdio MCP launcher; 14 tools, 3 resources; requires `mcp<2` in a venv).

**The compiler.** `tools/da_compile.py` (single decision-to-authority compiler; `synthesis` mode: dossier to full pack; `codify` mode: accepted proposals merged into a pack), with `compile_pack.py` and `apply_proposals.py` as thin compatibility shims. Governance gates: `tools/compile_parity.py` (byte-parity against pre-unification baselines) and `tools/compile_invariants.py` (provenance coverage, trace validity, reference integrity, synthetic-authority test, refusal behavior, re-codification rules; 146 checks at last run).

**The reference authority: Triage pack 0.12.2.** 80 artifacts (56 components, 10 guidelines, 7 patterns, 7 token-sets), 19 rules, 3 fallbacks, 6 prohibitions, recipes intentionally empty today, 1 declared validator (the source system's lint engine), golden set 58/58 at last gate, element coverage sweep 134/134. Served from its own repository (`vjsyong/authority-triage`) with `dist/` consumer foundations, `AGENT-PROMPT.md`, and a reference site.

**The authority estate: eight repos.** One repo per authority (records at the root, reference site under `site/`, README, CHANGELOG, LICENSE, CI): `triage` (0.12.2), `triage-evolution` (0.13.1-experiment; the evolution line that carries the flow recipes: 17), `wink` (0.2.0, 17 artefacts, verification contract 0.2, 34 checks), `leader` (contract 0.1+fix), `dominion` (0.2.0, contract 0.2, 26 checks), `phantom` (0.2.0, 29 artefacts, contract 0.2, 15 checks; derived screenshot-first from a deployed HTML5 UP template site), `indaba` (0.1.0, 21 artefacts; portability spike), `orbit` (0.1.0, 21 artefacts). All public as `vjsyong/authority-<name>`.

**The verification engine.** `tools/da_verify.py`: independent conformance checking against per-authority contracts (`verification.json`), five modes (STATIC, DOM, COMPUTED_STYLE, INTERACTION, REVIEW), worst-of aggregation, consumer mapping (`verify.map.json`), mutation-calibrated. Contracts exist for wink, leader, dominion, phantom; indaba and orbit ship none and say so.

**Governance artifacts.** Rolling decision log `docs/02-decisions.md` (D-001 through D-032); pre-registration and deviations D-1..D-9 (`docs/06-preregistration.md`); release policy (agents bump only `X.Y.Z-rcN`; full-version promotion is a human action); freeze manifests; the simplification program (`docs/13`), reconciliation doctrine (`docs/14`), consolidation record (`docs/11`); token-economics baseline (`docs/token-economics.md`).

**Serving surfaces.** Concept explainer at `designauthority.seanyong.xyz` (public and indexable), Triage docs site at `triage.seanyong.xyz` (containerized, indexable), review/audit consoles at `audit.seanyong.xyz` (noindex; Jenkins-style host-driven routing for `/authorities/<name>/audit`, `/demo`, `/stress3/<name>`), the x05 blind-review instrument at `driftexp.seanyong.xyz` (currently stopped; review complete). A refresh timer regenerates authority-site layers against their packs every 5 minutes and commits.

**Evidence programs** (all with written records under `docs/`): the A/B/C authority benchmark; the evolution loop; the second-authority portability spike (Ubuntu "Indaba"); the synthesis experiment (one brief, three authorities); the independent-verification experiment; the seed-evolution program (x05, 17 sessions, blind review); the reconciliation lifecycle experiment; plus semantic-retrieval, consumer-flow, and dispute fixtures. Section 11 summarizes each with numbers.

**Public release mechanics.** A "Use now" one-block install flow for agents (clone, venv, install a pack, prove it resolves, adopt the consumption protocol, wire lint into CI); byte-identical consumer foundations (`dist/`); per-authority download bundles (zip with page, styles, fonts, pack, logs, manifests, agent brief) built by `tools/bundle_authority_site.py`; public skill playbooks `skills/synthesize-authority` and `skills/extract-design-evidence`.

---

### 3 · The model

#### 3.1 Vocabulary (normative glossary, condensed)

**Authority and packs**

| Term | Meaning |
|---|---|
| Authority | A design system expressed as a governed, machine-readable contract (a pack) served by tooling, rather than prose alone. |
| Authority Pack | A directory of JSON files conforming to the data model; the unit of publication, versioning and citation. |
| Manifest (`authority.json`) | The pack's self-description: identity, `format_version`, content `version`, the pinned `snapshot`, kinds, capabilities, policy, entrypoints. |
| Snapshot | The real design system a pack compiles from, pinned by repo, branch, commit. Immutable within a pack version. |
| Curation layer | Hand-authored inputs (aliases, recipes, fallbacks, guideline notes, docs maps, provenance overlays) composed with the snapshot by the builder. MUST NOT contradict the snapshot. |
| Kernel | The kit-agnostic implementation of format and semantics (load, search, resolve, validate, records, CLI, MCP). |
| Format version | Schema version of the pack data model; `0.1` for this specification including its additive extensions. |

**Record kinds**

| Term | Meaning |
|---|---|
| Artifact | Any citable entry. Kinds: `component`, `pattern`, `token-set`, `guideline`, `example`, `reference`, plus governance kinds `rule`, `recipe`, `fallback`, `prohibition`, and the outside-`artifacts.json` kinds `precedent` and `candidate`. |
| Component | Concrete UI element with class contract, states, accessibility notes. |
| Pattern | A recurring page- or flow-level arrangement. |
| Token-set | A named group of design tokens. |
| Guideline | A rule of practice with do/don't lists and a source quote. |
| Rule | A deterministic, enforceable constraint with severity, scope, rationale, fix (e.g. `TDS003`). Enforced by validators. |
| Recipe | A sanctioned composition of existing artifacts answering a recurring need: `needs` phrases, `ingredients` (cited ids), `constraints`, `evidence` (source + quote). |
| Fallback | A scoped, sanctioned degrade path for a stated scope. The wildcard `*` is policy-only and never returned as an automatic FALLBACK. |
| Prohibition | An explicit "never" with detection signals; triggers CONFLICT. |
| Negative precedent | A policy decline recorded as guidance, not a dead end: mandatory `grounds`, `scope.domains`, `scope.boundary`, and a `try[]` list of routes to take instead. Carries a per-ask scope verdict. |
| Candidate | A provisional direction with partial evidence and a mandatory `promote_when` evidence bar. Explicitly NOT authority. |
| Validator / Finding | A declared command producing findings; a finding is `{rule, severity (error|warning|info), message, location{path,line}, fix, excerpt}` (SARIF-aligned). |

**Resolution and governance**

| Term | Meaning |
|---|---|
| Need | A design problem stated in natural language. |
| Resolution | The deterministic, cited answer: exactly one of CONFLICT, RESOLVED, COMPOSE, FALLBACK, UNDEFINED (in that order), plus optional precedent/candidate attachments. |
| Citation | An id that exists in the pack; validated before return. |
| Alias / Need phrase | Authored search terms; multi-word entries also match as phrases. |
| Search score | Sum of per-token weights (max weight per token over all fields) plus phrase bonuses; rounded to 2 decimals. |
| Scope verdict | Per-ask relationship to a precedent: `governs` (inside the decline; follow the try list), `outside` (boundary-only; explicitly not governed; proceed as marked improvisation), `ambiguous` (both; improvised unless a human rules). |
| Attachment | Matching precedents (at most 2) annotate any resolution; candidates (at most 2) attach on UNDEFINED only. Attachments never change the outcome. |
| Gap record | Noncanonical statement that the authority does not cover a need (need, context, authority identity, searched, closest, why insufficient, fallback used, evidence). |
| Proposal record | Noncanonical extension candidate attached to a gap; required: problem, insufficiency, reuse_case, composition_check, proposed, tests. |
| Dispute record | A RESOLVED claim that did not govern the need (a *wrong answer*, distinct from a gap, which is *no answer*). Replayable as a regression fixture. |
| Classification | Upstream triage of a gap: EXISTING-SOLUTION, DOCUMENTATION-FIX, RECIPE, PATTERN, PRIMITIVE, PROJECT-LOCAL, REJECT, following the abstraction ladder documentation < recipe < pattern < primitive. |
| Verdicts | Consumer proposal verdicts: `accept` / `reject` / `needs-info`. Upstream review verdicts: `ACCEPT` / `REVISE` / `REJECT` / `DOWNGRADE`. |
| Lenient adjudication | Declines are reserved for grounded policy with a sanctioned alternative; evidence-poor asks defer to UNDEFINED; partial evidence becomes a candidate. |
| Provenance block | Audit attachment on a changed record: `introduced_in`/`extended_in`, `triggering_gaps`, `review_decision`, `source_commit`, `tests`. |
| Golden set | `{problem, expect, expect_id?, note?}` cases; agreement rate is conformance evidence. |
| Convergence battery | Full-phrasing assertion set over a candidate release, including non-regression and delete-probe batteries. |
| Case (target model) | One lifecycle for gaps, proposals, disputes, verdicts and impact findings, as events on a case: `{id, kind, question, subject_refs, events[], status}`. Reserved event kinds: `impact_finding`, `migration_decision`. |
| Receipt | One immutable file per published build recording intent and outcome; confirmed against source evidence before use. |
| Transition policy | Per-decision property governing obligations to earlier implementations: `prospective` | `when_touched` | `required` (with trigger `by`) | `review`. |
| Obligation | The state of a required migration: `scheduled` | `due` | `overdue` | `closed`. |
| Reconciliation finding | Sweep result: `conforms` | `grandfathered` (always with reason and trigger) | `rectify` | `review`. |
| Inflation | Growth of normative surface required to close gaps, reported as raw dimensions, no composite score. |
| Freeze | A tagged, checksummed state of the specification and kernel. |

#### 3.2 Resolution semantics (the core algorithm, normative)

Applied to a `problem` string; produce exactly one outcome. Deterministic: no network, no time/locale dependence, stable ordering, all cited ids validated.

**Step 0 · Tokenisation and stemming** (identical for queries and index):

1. Lowercase; extract tokens matching `[a-z0-9][a-z0-9-]*`.
2. Drop stopwords (articles, pronouns, modals, common request verbs such as add/show/need; the frozen list ships with the kernel) and any single-character token.
3. Canonicalise spelling variants (chiefly US/UK pairs, canonical direction US) through a curated table; only the token itself or a guarded reduction (plural s, `-ing`/`-ed`/`-able` with an e-restore retry) may fire, so the table bounds every rewrite; canonical forms are idempotent and the table is conflict-validated at import. Every rewrite is reported in the output's `normalized` field (raw to canonical token map).
4. Stem: if length > 3: strip trailing `able` when length > 7 (`searchable` to `search`); else strip a trailing `s` unless the token ends `ss|us|is`; then strip a trailing `e` when length > 3.

**Step 0b · Scoring.** Per token, the maximum weight across fields:

| Entry type | Field | Weight |
|---|---|---|
| artifact | alias | 4.0 |
| artifact | title | 3.0 |
| artifact | body.class | 2.5 |
| artifact | summary | 1.5 |
| artifact | other body fields (`states`, `a11y`, `do`, `dont`, `quote`, `statement`, `group`, `source.path`) | 1.0 |
| recipe | title | 3.0 |
| recipe | need | 3.0 |
| recipe | summary | 1.5 |
| recipe | constraint | 1.0 |
| fallback | scope token | 2.5 |
| fallback | title | 2.0 |
| fallback | statement | 1.5 |
| precedent | matches (vocabulary) | 4.5 |
| precedent | title / request | 3.0 |
| precedent | reason / try | 1.5 / 1.0 |
| candidate | matches (vocabulary) | 4.0 |
| candidate | title | 3.0 |
| candidate | summary / request | 2.0 |

`score = Σ token weights + 5.0 × (number of phrases whose every token occurs in the query)`. Single-token phrases match only by exact query equality. Sort by `(−score, id)`; the id is the tie breaker, giving byte-stable output.

**Step 1 · CONFLICT.** If any prohibition matches (a `detect: color_literal` regex over hex/rgb/hsl literals, a `signals` substring, or a complete `signals_all` token group), the outcome is CONFLICT: cite the prohibition plus its rule (severity, summary, fix) and the policy string. Stop.

**Step 2 · RESOLVED.** Search all entries (artifacts exclude recipes, fallbacks, prohibitions, precedents, candidates). Let `a_best` be the top artifact hit, `runner` the second:

```
RESOLVED iff a_best.score >= 6.5  AND
            (no runner OR a_best.score - runner.score >= 2.0)
```

A dedicated artifact wins over a recipe by spec order: a recipe answers only when no artifact directly defines the need.

**Step 3 · COMPOSE.** Otherwise, search recipes only; COMPOSE iff `r_best.score >= 5.0`. The answer carries the recipe (id, title, summary, constraints, evidence) and resolved ingredient briefs.

**Step 4 · FALLBACK.** Otherwise, intersect each fallback's `scope` (excluding `*`) with the normalised query tokens; a non-empty intersection selects the fallback. Consumers implement per the fallback, mark the improvisation, and SHOULD report a gap if the need is likely to recur.

**Step 5 · UNDEFINED.** Otherwise the outcome is UNDEFINED, a structured success carrying: `closest` (top-3 artifacts), `search_trace` (queries, hits considered, top score, threshold applied), `why`, `fallback_policy` (allowed fallbacks plus the manifest's `policy.on_undefined`), and `next` (implement per policy, mark, report a gap).

**Attachments (after the outcome).** Precedents: scope-aware matching over `matches` vocabulary (single tokens count at 4+ authored characters, before stemming; multi-word entries match only as complete phrases) OR any `scope.boundary` hit; the per-ask verdict is `outside` (boundary hits only), `ambiguous` (boundary and domain both hit), else `governs`; up to 2 attach, ordered governs, ambiguous, outside, then score, then id. Candidates: on UNDEFINED only, up to 2, by score then id. Attachments annotate; they NEVER change the outcome.

**Output shape.** All outcomes return `outcome`, `problem`, `context` (echoed), `resolution` (exactly one primary key: `artifact` | `recipe`+`ingredients` | `fallback` | `prohibition`+`rule`+`detected`, or `closest` on UNDEFINED), `alternatives` (top-3 non-cited hits), `evidence`, `authority` (`{authority, version, commit}`), `next`; optionally `normalized`, `precedents`, `candidates`.

**Reference behaviours** (must keep resolving; used as gates): `"waiting for approval"` to COMPOSE `recipe/status-with-text`; `"compact history of approval steps"` to RESOLVED `component/tl`; `"progress bar for a background job"` to UNDEFINED; `"make the corners rounded"` to CONFLICT (TDS003); `"a primary button"` to RESOLVED `component/btn`.

**Frozen constants:** `DIRECT_MIN = 6.5`, `DIRECT_MARGIN = 2.0`, `COMPOSE_MIN = 5.0`, `PHRASE_BONUS = 5.0`.

#### 3.3 Disputed resolutions and the retrieval assist

**Disputes.** When a RESOLVED outcome does not actually govern the request, the consumer records a dispute (query, the claimed id, reason, optional suggested fix, context). Disputes never change resolution behaviour; replaying the resolver over open disputes (`still_stands` / `cleared`, gateable with `--expect-standing N`) is the regression fixture. A rejected RESOLVED must be distinguishable from an ordinary gap.

**Retrieval assist (optional, off by default).** A fused retrieval index (SQLite FTS5 BM25 + a local embedding model, RRF fusion) returns candidate ids with retrieval evidence only (ranks, similarity, fusion score). `discover` surfaces it; `resolve --assist semantic` attaches a `retrieval_assist` block on UNDEFINED only. Outcome classes, evidence and citations are computed exactly as without the assist (verified end to end). The index is derived data, rebuilt from the pack, stored outside it; the kernel stays stdlib-only and every lexical surface is unchanged without the extras.

---

### 4 · Pack format (the data model)

#### 4.1 Directory

A pack is a directory of JSON files. Required files, with the manifest's `entrypoints` block allowed to rename them:

| File | Top-level key | Required | Contents |
|---|---|---|---|
| `authority.json` | (none) | yes | Manifest (4.2) |
| `artifacts.json` | `artifacts` | yes | Citable artifacts (4.3) |
| `rules.json` | `rules` | yes | Enforceable rules (4.4) |
| `scoring.json` | (none) | yes | Scoring formula + gate description (4.10) |
| `recipes.json` | `recipes` | opt | Sanctioned compositions (4.5) |
| `fallbacks.json` | `fallbacks` | opt | Scoped fallbacks (4.6) |
| `prohibitions.json` | `prohibitions` | opt | Prohibitions (4.6) |
| `precedents.json` | `precedents` | opt | Negative precedents (4.7) |
| `candidates.json` | `candidates` | opt | Provisional directions (4.7) |
| `validators.json` | `validators` | opt | Declared validator commands (4.8) |
| `golden.json` | (none) | opt | Golden set (4.9) |
| `BUILD.json` | (none) | opt | Build receipt (volatile; excluded from drift) |
| `curation/` | (none) | opt | Hand-authored builder inputs; never resolved at runtime |

`format_version` stays `0.1` across all additive extensions: every extension is an optional file or annotation, older packs load unchanged, and consumers MUST ignore unknown keys and MUST NOT require precedents, candidates or provenance blocks for resolution.

#### 4.2 Manifest (`authority.json`)

| Field | Type | Required | Meaning |
|---|---|---|---|
| `id` | string | yes | Authority id (e.g. `triage`) |
| `name` | string | yes | Human name |
| `format_version` | string | yes | Data-model version (`0.1`) |
| `version` | string | yes | Content version of this pack |
| `snapshot` | object | yes | `{repo, commit, branch, version, path_hint}` of the source system |
| `description` | string | opt | One-line purpose |
| `kinds` | string[] | opt | Declared artifact kinds |
| `capabilities` | object | opt | `{search, resolve, validators[], gap_reporting, extension_proposals, resolution_assist}`; `resolution_assist` is `"off"` or (since 0.4) `"optional"` |
| `policy` | object | opt | `{on_undefined, on_conflict, proposals}` human-readable strings surfaced with outcomes |
| `entrypoints` | object | opt | File overrides for standard entrypoint names |

Real example (Triage, showing the shape and the policy strings):

```json
{
  "id": "triage",
  "name": "Triage",
  "format_version": "0.1",
  "version": "0.12.2",
  "snapshot": {
    "repo": "triage-design-system (local; published at triage.seanyong.xyz)",
    "commit": "97cabe5cd03f6ec3a2ebe6f6fdefcbc5e3cf55f2",
    "branch": "main",
    "version": "0.12.1",
    "path_hint": "~/triage-design-system"
  },
  "kinds": ["component", "pattern", "token-set", "guideline", "recipe", "reference"],
  "capabilities": {
    "search": true, "resolve": true, "validators": [],
    "gap_reporting": true, "extension_proposals": true,
    "resolution_assist": "off"
  },
  "policy": {
    "on_undefined": "Implement per the consuming project's fallback policy, mark the improvisation, and report a gap. Never present improvisation as canonical.",
    "on_conflict": "Do not implement as requested; the request violates an explicit constraint (see the cited rule/prohibition).",
    "proposals": "Noncanonical. The authority is never modified by a consumer; proposals are reviewed upstream."
  },
  "entrypoints": {
    "artifacts": "artifacts.json", "rules": "rules.json", "recipes": "recipes.json",
    "fallbacks": "fallbacks.json", "prohibitions": "prohibitions.json",
    "validators": "validators.json", "scoring": "scoring.json",
    "precedents": "precedents.json", "candidates": "candidates.json"
  }
}
```

#### 4.3 Artifacts (`artifacts.json`)

Entry fields: `id` (`<kind>/<slug>`, globally unique), `kind`, `title` (required); optional `summary`, `status` (`stable` | `beta` | `experimental` | `deprecated`), `aliases[]` (multi-word entries are phrases), `body{}` (kind-specific: `class`, `states`, `verify`, `a11y`, `do`, `dont`, `quote`, `statement`, `group`, ...), `relations` (`{rel, target}` pack id or `{rel: "documented-at", url}`), `source` (a dict `{repo, commit, path}`; the kernel calls `.get()` on it, a plain string crashes search), `compiled_from[]` (decision/proposal ids this record compiled from, e.g. `W-01` or `prop/...`), `provenance` (4.11).

Real example:

```json
{
  "id": "component/btn",
  "kind": "component",
  "title": "Button",
  "summary": "Button, from base.css. Documented states: default, hover, active, focus-visible, disabled, busy (guardApply). A11y: Use a real <button> or <a>; never a clickable div.",
  "status": "stable",
  "aliases": ["button", "btn", "primary button", "secondary button", "cta",
               "submit button", "danger button", "icon button", "small button",
               "action", "action button"],
  "body": {
    "class": "btn",
    "group": "Components",
    "source_file": "base.css",
    "states": ["default", "hover", "active", "focus-visible", "disabled", "busy (guardApply)"],
    "verify": [".btn", ".btn:hover", ".btn:active", ".btn:disabled", ".btn:focus-visible"],
    "a11y": ["Use a real <button> or <a>; never a clickable div.",
             "Icon-only buttons need aria-label.",
             "guardApply freezes and relabels the submit button until navigation."]
  },
  "source": {"repo": "triage-design-system", "path": "spec/states.json (btn, base.css)"},
  "compiled_from": ["triage/states"]
}
```

#### 4.4 Rules (`rules.json`)

`{id, name, severity (error|warning|info), applies_to[], summary, why, fix, enforcement?}`. Rule ids are short symbols (`TDS001`).

Real example:

```json
{
  "id": "TDS001",
  "name": "deprecated-name",
  "severity": "error",
  "applies_to": ["css", "html", "js"],
  "summary": "Uses a pre-Triage (mail-triage era) class, id or global instead of the renamed vocabulary.",
  "why": "The 0.1.0 rename sweep defined the public vocabulary; old names are no longer styled by core.css and silently fall back to browser defaults.",
  "fix": "Rename via /RENAME-MAP.md (or run the bulk assemble map tool)."
}
```

#### 4.5 Recipes (`recipes.json`)

`{id, kind: "recipe", title, summary, needs[], ingredients[], constraints[], evidence{source, quote}, provenance?}`. Every ingredient id MUST exist in the pack (the builder refuses unknown ingredients). `needs` is the recall surface for COMPOSE; each need matches by tokens (weight 3.0) and as a phrase (bonus 5.0).

Real example:

```json
{
  "id": "recipe/high-stakes-confirm",
  "kind": "recipe",
  "title": "High-stakes actions keep a native confirm()",
  "summary": "Irreversible, security-relevant, or multi-item actions confirm with a sentence naming the object and consequence.",
  "needs": ["confirm an irreversible action", "confirm account removal",
             "confirm enabling auto-apply", "confirm rebuild", "reject with a reason",
             "require a typed reason at the point of action", "one-way decision with rationale",
             "decline with a reason", "high-stakes confirmation with a required reason"],
  "ingredients": ["guideline/high-stakes-confirm", "fallback/native-control", "component/tl"],
  "constraints": [
    "native confirm() on the form; sentence names object + consequence",
    "the listed set plus reason-bearing reject/decline decisions",
    "when the rationale must be recorded, pair the confirm with a required, labelled textarea (native control); the reason surfaces in the history (component/tl)"
  ],
  "evidence": {
    "source": "INTERACTION.md#one-way-actions",
    "quote": "Actions that are irreversible, security-relevant, or affect more than the clicked item keep a native `confirm()`."
  }
}
```

#### 4.6 Fallbacks and prohibitions

Fallbacks (`fallbacks.json`): `{id, title, statement, scope[], constraints[]}`. `scope` tokens are matched against normalised query tokens; the wildcard `*` is allowed but never participates in matching (fallbacks are non-catch-all by construction). Real ids: `fallback/native-control`, `fallback/platform-controls`, `fallback/light-only`, `fallback/selection`, `fallback/ruled-panel`.

Prohibitions (`prohibitions.json`): `{id, statement, signals[], signals_all[]?, detect?, rule?}`. `signals` are case-insensitive substrings of the lowercased problem; `signals_all` are token groups that must all be present; `detect: "color_literal"` runs a hex/rgb/hsl regex. Real ids: `prohibit/rounded-corners` (rule TDS003), `prohibit/imagery-pictograms` (cites decision D-22). Keep signals phrased for natural word order (an overly literal single phrase misses variants such as "corners rounded").

#### 4.7 Negative precedents and candidates

Precedents (`precedents.json`): `{id, kind: "precedent", title, request, matches[], decision, grounds, reason, scope{domains[], boundary[]}, try[], citation?, provenance?}`. `grounds`, `scope.domains` and `scope.boundary` are required and MUST be non-empty: a decline without a boundary is invalid (enforced by the probe tool). `matches` follows alias matching (single tokens at 4+ authored characters before stemming; multi-word only as phrases).

Real example:

```json
{
  "id": "precedent/renamed-vocabulary",
  "kind": "precedent",
  "title": "Vocabulary rename (0.1.0 sweep)",
  "request": "keep the pre-0.1.0 (mail-triage era) class/id vocabulary alongside new names",
  "matches": ["old class names", "legacy vocabulary", "mail-triage names", "deprecated classes"],
  "decision": "accepted, old names retired",
  "grounds": "TDS001: pre-Triage names are no longer styled by core.css and silently fall back to browser defaults.",
  "reason": "One public vocabulary keeps the contract checkable; a rename map exists for migration.",
  "scope": {"domains": ["css", "html", "js"], "boundary": ["class names", "ids", "globals"]},
  "try": ["rename via RENAME-MAP.md", "run the assemble map tool for bulk migrations"],
  "citation": "rename-map.json + RENAME-MAP.md; spec/rules.json TDS001"
}
```

Candidates (`candidates.json`): `{id, kind: "candidate", title, request, matches[], status: "candidate", summary, promote_when[], evidence_present?, emerges_from?, provenance?}`. `promote_when` is required and MUST be non-empty; promotion requires the named evidence, then proposal, owner verdict, codification. A candidate is never presented as canonical.

#### 4.8 Validators (`validators.json`)

`{name, title, kind, workdir, command[], parser, applies_to[], rules_source, notes}`. Substitutions at run time: `{snapshot}` (the source system's checkout, resolved via `--snapshot` > `DA_SNAPSHOT` env > manifest `snapshot.path_hint`), `{pack}` (the pack's own directory, for pack-local validator scripts), `{target}` (the absolute path being validated). Parser names: `lint-json` (also accepts the legacy alias `triage-lint-json`).

Real example:

```json
{
  "name": "triage-lint", "title": "Triage lint engine", "kind": "command",
  "workdir": "{snapshot}",
  "command": ["python3", "lint/triage_lint.py", "{target}", "--json"],
  "parser": "triage-lint-json", "applies_to": ["css", "html", "js"],
  "rules_source": "rules.json",
  "notes": "Runs the pinned snapshot's linter over the target path."
}
```

#### 4.9 Golden set (`golden.json`)

A JSON array (or `{cases: [...]}`) of `{problem, expect, expect_id?, note?}`. Agreement is conformance evidence, enforced at 100% by the reference implementation's unit tests. Real cases:

```json
[
  {"problem": "a primary button", "expect": "RESOLVED", "expect_id": "component/btn"},
  {"problem": "an icon-only button", "expect": "RESOLVED", "expect_id": "component/iconbtn"},
  {"problem": "a switch", "expect": "RESOLVED", "expect_id": "component/px-sw"}
]
```

#### 4.10 Scoring file (`scoring.json`)

Carries the authoritative per-run score formula and gate description:

```json
{
  "formula": "score = max(0, 100 - (errors*8 + warnings*2 + infos*0.5))",
  "gate": "Authority CI fails on any error; --max-warnings can tighten warnings.",
  "source": "triage-design-system spec/ + INTERACTION.md"
}
```

#### 4.11 Extensions: provenance, release metadata, build receipt

**Provenance block** (any pack entry introduced or modified by the governance loop): `{introduced_in | extended_in, triggering_gaps[], review_decision, source_commit, tests[]}`. Since the compiler formalisation, every normative record also carries either `compiled_from` (approved decision ids) or an explicit `exception` block (`{reason, basis, approval}`); empty provenance is a hard compile error, and the system must be able to answer "why does this record exist?" from the pack alone.

**Release metadata** (`BUILD.json.release`): `{label, kind, experiment, based_on, source_branch, evidence, review}`.

**Build receipt** (`BUILD.json`): snapshot identity, counts, curation hashes, warnings. Volatile (timestamps), excluded from drift comparison.

**Build and drift.** The builder composes snapshot plus curation deterministically; a drift gate re-runs the build and compares generated files against the committed pack (zero drift required for a pinned pack). Generated files are never hand-edited. One builder owns a given pack directory (two builders fighting over one directory desyncs the drift gate).

#### 4.12 The record envelope and the Case (target architecture, staged)

The simplification program (adopted 2026-10-11) stages a unified model: **one envelope for every authoritative record** with a typed payload:

```
id: component/action-button
type: component          # component | guideline | recipe | prohibition | rule | fallback
title: Primary action button
scope: {domain: actions}
contract: {...}          # the type-specific payload
evidence: [evidence refs]
verification: [check refs]
provenance: {case: case/0042, introduced_in: 0.3.0}
```

and **the Case** as one lifecycle for what are today separate record types: `{id, kind, question, subject_refs, events[], status}`, where a gap, a disputed resolution, a proposal and a review verdict are events on a case. First implementation is a canonical view over the existing workspace files (zero migration), with the reconciliation event kinds (`impact_finding`, `migration_decision`) reserved. Published norms and unapproved cases stay physically distinct (pack vs workspace). Until the envelope lands, the current per-file shapes above remain normative and a compatibility layer reads both.

---

### 5 · Architecture and interfaces

#### 5.1 The reference implementation layout

```
kernel/design_authority/    the kernel: pack.py (load + index + tokenizer), lex.py
                            (normalisation), resolve.py (pipeline), validate.py
                            (validator runner), records.py (gaps/proposals/disputes),
                            cli.py, mcp_server.py
tools/                      da.py + da-mcp.py (entrypoints); da_compile.py (compiler);
                            da_verify.py (verification engine); da_sweep.py
                            (reconciliation); pack builders; the gate suite (check.sh);
                            site tooling (bundle/refresh/check scripts)
docs/spec/                  the frozen specification (0.5.0)
authorities/<name>/         one git repo per authority (records at root, site/, dist/)
examples/                   reference builds, review consoles, the concept site
benchmark/                  the A/B/C benchmark harness and reports
workspaces/                 consumer workspaces (each carries .design-authority/)
```

Data flow:

```
reference design system (snapshot, pinned commit)
        |  build (builder + curation layer)
        v
Authority Pack (JSON directory)  -----> served by tools
        ^                                - da CLI (humans, scripts)
        | governance                     - da-mcp (stdio MCP server, agents)
        | (section 8)                    - validators (declared commands)
curation layer
consumer workspace
  `- .design-authority/   (gaps, proposals, disputes, decision log; never touches the pack)
```

Hard layout rules: the kernel contains no system-specific knowledge; consumers interact only through the tool surface; records are written to the consuming workspace, never the pack. The reference is Python 3.12 stdlib-only with plain JSON files and no database. A one-line launcher pattern (`tools/da.py`) inserts `kernel/` on `sys.path` and calls the library, so CLI and MCP share exactly one implementation.

#### 5.2 CLI (`da`)

Global option `--pack PATH`. Subcommands:

| Command | Purpose |
|---|---|
| `overview` | Manifest + counts |
| `search QUERY [--kinds] [--limit] [--json]` | Ranked search (includes precedent/candidate kinds) |
| `discover QUERY [--k] [--class canonical\|history\|all]` | Optional semantic discovery (retrieval signal only) |
| `inspect ID` | Full artifact |
| `resolve PROBLEM [--context] [--assist off\|semantic] [--json]` | Resolution (+ attachments) |
| `validate TARGET [--snapshot PATH] [--json]` | Run declared validators |
| `golden [--file PATH]` | Run the pack's golden set |
| `gaps [--workspace]` / `gap-add --need ...` | List / record gaps |
| `propose --gap ID --file JSON` | File a proposal |
| `review --proposal ID --verdict accept\|reject\|needs-info [--note]` | Record a consumer verdict |
| `precedents [--query]` / `precedent-check --ask TEXT` | Precedent inspection and the pre-deviation check |
| `candidates [--query]` | List provisional candidates |
| `dispute-add --query --resolved-to ID --reason ...` / `disputes` / `dispute-replay [--expect-standing N]` | Disputed resolutions and their replay gate |

#### 5.3 MCP server (stdio)

Entrypoint `tools/da-mcp.py`; environment `DA_PACK` (pack directory; required) and `DA_WORKSPACE` (consumer workspace for records; defaults to the pack-adjacent workspace). Transport: stdio JSON-RPC (MCP SDK, pinned `mcp<2`). **14 tools**:

| Tool | Parameters | Returns |
|---|---|---|
| `authority_overview` | none | Identity, counts, capabilities, policy, entrypoints, usage guide |
| `search_authority` | `query`, `kinds`, `limit` | Ranked `{id, kind, title, score, matched}` |
| `discover_candidates` | `query`, `k`, `include_history` | Fused-retrieval candidates with retrieval evidence only (degrades to `status: unavailable` without the extras) |
| `inspect_artifact` | `id` | Full artifact entry or structured not-found |
| `resolve_design_problem` | `problem`, `context?`, `assist` | The resolution output incl. attachments; `assist="semantic"` adds retrieval hints on UNDEFINED |
| `list_precedents` | `query` | Policy declines with grounds, boundary, try list |
| `check_precedent` | `ask`, `precedent_id?` | Per-ask verdicts (governs/outside/ambiguous) + boundary hits + candidates |
| `list_candidates` | `query` | Provisional directions with `promote_when` |
| `report_dispute` | `query`, `resolved_to`, `reason`, `context?`, `suggested_fix?` | Stored dispute record |
| `list_disputes` | `status` | Disputes by status |
| `replay_disputes` | none | `still_stands` / `cleared` per open dispute |
| `validate_implementation` | `target`, `validators` | Findings, counts, score, per-validator meta |
| `report_gap` | `need`, `context?`, `attempted_resolution?`, `fallback_used?`, `evidence?`, `scope_hint` | Stored gap (+ precedent warnings / candidate hints) |
| `propose_extension` | `gap_id`, `proposal` | Stored proposal (+ review checklist + warnings/hints) |

Resources: `authority://overview`, `authority://rules`, `authority://artifact/{id}`.

Guarantees: responses cite only pack-validated ids; gap/proposal writes stay under the workspace's `.design-authority/`; a **decision log** (`.design-authority/decision-log.jsonl`) is appended on every call (timestamp, tool, params digest, outcome, latency). The log is best-effort audit data, never load-bearing, and is the evidence that a client's call actually reached the server. Error results are structured with recovery hints rather than exceptions.

Client registration (any MCP host; the exact block differs per host):

```json
{"mcpServers": {"design-authority": {
  "command": "/path/to/design-authority/.venv/bin/python",
  "args": ["/path/to/design-authority/tools/da-mcp.py"],
  "env": {"DA_PACK": "/path/to/authority-triage", "DA_WORKSPACE": "/path/to/your/project"}}}}
```

The reference has been verified with three host styles: Claude-Code-style `.mcp.json`, Hermes (`hermes mcp add`), and opencode (project `opencode.json` `mcp` block). A client integration is only considered verified when a call is proven to have reached the server via the workspace decision log; a green handshake or a plausible model answer is not proof.

#### 5.4 Consumer records (workspace)

**Gap** (`gaps.jsonl`, one JSON object per line):

```
{ id: "gap/<utcstamp>-<hex6>", need, context{}, authority{authority,version,commit},
  searched?, closest?, why_insufficient?, fallback_used?, evidence[], scope_hint,
  precedent_warnings?, candidate_hints?, status: "open", created }
```

**Proposal** (`proposals/<id-safe>.json`): required fields `problem`, `insufficiency`, `reuse_case`, `composition_check`, `proposed`, `tests`; plus `gap_id` (must reference a stored gap), `depends_on[]` (each id must exist in the pack), `new_primitives[]`, `status` (`candidate` then `accepted` / `rejected` / `needs-info`), `review {verdict, notes, evidence?, reviewed_at}`, and creation-time `precedent_warnings` / `candidate_hints`. Each stored proposal receives a 7-item review checklist (necessity, reuse, composition, dependencies, new primitives, compliance tests, deterministic checks).

**Dispute** (`disputes.jsonl`): `{id, kind: "disputed-resolution", query, resolved_to (pack-validated id), reason, suggested_fix?, context{}, evidence[], authority{}, status: open|accepted|rejected, status_note?, status_at?, created}`.

#### 5.5 Validator runner

Executes the pack's declared validators against a target path with the substitutions of 4.8. Findings normalise to `{rule, severity, message, location{path,line}, fix, excerpt}`; the summary carries severity counts, per-rule counts, and the score `max(0, round(100 - (errors*8 + warnings*2 + infos*0.5)))`. Unknown parsers and missing workdirs are structured errors with fix hints. A lint score is a gate, never proof of conformance: it covers the configured checks only.

#### 5.6 Error semantics

Structured, non-throwing errors are preferred on all consumer surfaces (missing pack files, unknown ids, missing workdir, unparseable validator output). Tool and CLI failures MUST NOT corrupt records or packs.

---

### 6 · The compiler and its governance invariants

The single compiler (`tools/da_compile.py`) turns approved decisions into authoritative records in two modes over one emit core:

- **`synthesis`**: an authority *dossier* (reviewed data checked into the repository: the approved decision ledger plus the records those decisions emit) compiles into a full pack.
- **`codify`**: reviewer-accepted proposals merge into an existing pack; idempotent, with a recorded `codified_at`.

Hard rules the compiler enforces (each is a gate):

1. **Only approved decisions compile.** An unapproved or unknown reference is refused.
2. **Summaries are never invented.** A record's text is the decision text, the review's recorded `codified_summary`, or the proposal's own fields.
3. **Universal provenance.** Every normative record passes one `_finalize_record` in both modes and carries either `compiled_from` approved decisions or an explicit `exception` block (reason + basis + approval). Empty provenance is a hard error. `validate_record` / `validate_provenance` are public so the compiler and the invariants gate cannot drift apart.
4. **Publication is staged and validated.** Builds happen in memory, land in a staging directory, load through the runtime's own pack loader, and only then are the files atomically replaced (one `os.replace` per file). A validation failure publishes nothing.
5. **Conflicting codification is refused.** An identical resubmission is a silent no-op; a resubmission whose definition differs from the published record for the same id raises an explicit conflict naming the id, proposal and differing fields. Amend through a case, never a second submission.
6. **No per-authority code.** Authority-specific definitions live in reviewed data (dossier files and curation), never in compiler code. A synthetic brand-new authority compiles with zero engine edits (an acceptance test of the invariants gate).

Two gates pin the compiler: **compile parity** (re-compiles through the new engine and byte-compares against baselines captured from the pre-unification tools; baselines are frozen evidence with no update flag) and **compile invariants** (provenance coverage, trace validity against the approved ledger, record shape via the engine's own validator, reference integrity, the synthetic-authority test, refusal-publishes-nothing, identical/conflicting re-codification; 146 checks at last run over 59 records: 53 decision-traced, 6 exception-backed). The six exception-backed records (three protocol-authored platform-controls fallbacks; wink light-only; leader selection; leader ruled-panel) are carried with `approval: pending` owner ratification and are the standing example of the exception path. A real finding surfaced when the enforcement landed: leader `fallback/selection` restated a decision (`L-12`) that review had left undefined; it is now exception-backed with that history recorded.

---

### 7 · The verification engine (independent conformance checking)

`tools/da_verify.py` inspects the *artifact*, never the agent's claims. A contract (`verification.json` in the authority repo, an optional additive artifact that does not touch the pack version) declares checks; each check names the authority item it verifies, a verifiability classification, a mode, and minimal deterministic assertions.

Real contract check (wink, contract 0.2):

```json
{
  "id": "wink/action-pill-radius", "item": "rule/W-R1",
  "title": "Buttons are pills (radius = half height)",
  "classification": "MECHANICALLY_VERIFIABLE", "severity": "error",
  "mode": "COMPUTED_STYLE", "selector": ".cta",
  "assertions": [{"property": "border-radius", "relation": "pill"}],
  "missing": "fail"
}
```

- **Modes**: STATIC (source scanning), DOM, COMPUTED_STYLE, INTERACTION, REVIEW (human-judged items surface as `REVIEW_REQUIRED` and are never faked into PASS).
- **Aggregation is worst-of**: ambiguity is never upgraded to PASS (`missing: fail` becomes VIOLATION, otherwise UNVERIFIABLE).
- **Runner**: `da_verify.py --pack <pack> --target <app-dir> --out <outdir>`; Playwright is optional (browser checks degrade to UNVERIFIABLE with a note; STATIC still runs).
- **Consumer mapping**: a consumer app maps itself onto the contract through `verify.map.json` (files, selectors, `ignore` to NOT_APPLICABLE); interaction parameters resolve through the map. A consumer build re-run under v2 produced 34 checks as 23 PASS / 0 VIOLATION / 7 N/A / 4 REVIEW.
- **Calibration protocol**: calibrate every contract against a known-clean app first (over-assertions surface as violations; fix the check against source truth, never loosen it); then calibrate the verifier itself with mutants (planted violations it must catch); a demo that drifts from the spec gets flagged, and the demo is fixed, never the check.
- **Three always-on rules**: (1) INSTRUMENT SCOPING, exclude marks/review-instrument rules (`.marks-*`, `[data-mark]`, `#provPanel`) from colour and shape scans, pinned to real selectors, never a generic prefix; (2) ARTIFACT-LOCAL RESULTS ARE NEVER PROOF, ship coverage hashes and a "re-run to confirm" label, trust only a fresh verifier run; (3) HARDENING DOCTRINE, strip comments before static scans, parse colours rather than string-compare, all-matches plus size proxy, interaction passes before scanning, DOM-wide censuses for absence claims.
- **Estate status**: contracts ship for wink (0.2, 34 checks), leader (0.1+fix), dominion (0.2, 26 checks; includes the `nav-link-ink` UA-default-link leak class) and phantom (0.2, 15 checks); indaba and orbit ship none and their briefs say so. A meta CI matrix runs `da_verify` per contract-holder against recorded targets, with tolerated findings recorded.

---

### 8 · Governance: the evolution loop, versioning, freezes

#### 8.1 The evolution loop (normative process, ten phases)

Downstream gaps are **evidence, not commands**. Each phase names its required output; a rebuild should reproduce this loop verbatim.

| # | Phase | Required output |
|---|---|---|
| 1 | **Evidence**: reconstruct gap/proposal records from consumer workspaces | Per-need records (need, context, runs reporting, closest artifacts, fallback used, proposals, conflicts) + semantic consolidation rules (different phrasing of one need is one need) |
| 2 | **Triage**: assume no extension; attempt existing-authority solutions first | Per-gap evaluation against seven questions (existing solution? docs/aliases? recipe? pattern? primitive? project-local? conflict?) + classification |
| 3 | **Candidates**: smallest change per gap | Candidate JSON files + a candidates write-up; stored separately from any published pack |
| 4 | **Adversarial review**: independent, clean-context reviewer instructed to *assume rejection* | Per-candidate verdict + rationale + required actions; the reviewer re-verifies claims by execution |
| 5 | **Authority CI**: candidate applied to a candidate branch/version only | Source-system gates green; pack builds deterministically; drift gate passes; pinned pack byte-identical; convergence battery incl. delete probes; golden sets |
| 6 | **Release**: publish beside the pinned pack, never over it | New pack directory + provenance overlay + release metadata; pinned and candidate packs remain comparable |
| 7 | **Re-runs**: fresh consumers against the new release, needs phrased semantically (never by new artifact names) | Run records: outcomes, call counts, whether previously unresolved needs now resolve, whether duplicate gaps are filed |
| 8 | **Migration**: point the new authority at old implementations | Per-usage mapping (superseded local to applying record, direct vs manual) |
| 9 | **Inflation**: measure growth | Raw dimensions: counts before/after, modified entries, vocabulary width; no composite score |
| 10 | **Evaluation**: close or falsify the loop | Gap closure, convergence, recurrence, regression, inflation, review value, provenance, migration, usefulness; threats to validity disclosed |

Classification uses the abstraction ladder strictly: **documentation < recipe < pattern < primitive**; a gap MUST NOT be classified above the smallest rung that can close it. Upstream verdicts are `ACCEPT` / `REVISE` / `REJECT` / `DOWNGRADE` (downgrade = valid in spirit, move one rung down).

#### 8.2 Lenient adjudication

Declines are a last resort, reserved for grounded policy (asset law, motion doctrine, prohibitions, off-grammar geometry) **and** a sanctioned alternative. Three rungs replace the blunt decline:

| Rung | When | What happens |
|---|---|---|
| Candidate | Partial evidence; a direction exists but is not canon | Recorded provisional with mandatory `promote_when`; promotion requires the named evidence, then proposal, owner verdict, codification |
| Undefined deferral | Insufficient evidence | The ask stays UNDEFINED; no precedent; improvise in character, mark it; a gap remains open |
| Decline | Grounded policy only, with a sanctioned alternative | A precedent with mandatory grounds, scope domains, boundary, and try list |

Hard requirements (gate-enforced): every precedent carries non-empty `grounds`, `scope.domains`, `scope.boundary`; every candidate carries `promote_when`. Reviewer rejections are owner decisions and are never re-classified by leniency. Precedent matching is scope-verdict'd so a decline cannot silently cover asks outside its declared scope.

#### 8.3 Provenance and release requirements

Every entry introduced or modified by the loop MUST carry a provenance block; the release as a whole carries release metadata in `BUILD.json.release`. Release gate list: (1) source-system gates green on the candidate branch; (2) pack builds deterministically, drift passes, pinned pack byte-identical; (3) convergence battery passes including non-regression and delete probes; (4) golden sets pass (pinned set against pinned pack; candidate pack carries its own extended set); (5) the release is additive by preference, and any semantic change to existing entries is enumerated and justified in review notes.

#### 8.4 Versioning, change control, and the freeze ritual

| Layer | Example | Changes when |
|---|---|---|
| System (the spec) | `0.5.0` | The frozen semantics/interfaces change |
| Format (pack schema) | `0.1` | The data model changes (additive extensions stay under 0.1) |
| Authority (pack content) | `0.12.1` to `0.13.0-experiment` | Content/governance releases |
| Snapshot (source pin) | commit hash | Never within one pack version |

Change control: editorial clarifications are patches; semantic changes (pipeline order, thresholds, record formats, tool contracts, governance taxonomies) are minor bumps, justified in the decision log, with a fresh freeze and manifest. A pack version is immutable once tagged or released; corrections ship as a new version.

**Freeze ritual** (executed five times, 0.1.0 through 0.5.0): gate first (the full check suite must be green at the freeze commit: freeze a verified state, never a hopeful one); write the SHA-256 manifest of the frozen surface (spec set, kernel files, entrypoints, pack builder; the manifest itself excluded, referencing the tagged commit rather than embedding it); bump VERSION; rewrite the README status line; commit; annotated tag; push code and tag; verify every manifest file. Frozen surface as of 0.5.0: spec `00`-`05`, `kernel/design_authority/*.py`, `tools/da.py`, `tools/da-mcp.py`, `tools/build_pack_triage.py`, plus `lex.py`, `tools/da_sem.py`, `tools/sem_selftest.py` carried since 0.3.0/0.4.0.

**Release policy (owner directive):** agents auto-bump versions only as `X.Y.Z-rcN`; promotion to a full version is a human-reviewer action, recorded in the CHANGELOG with reviewer and date.

**Non-goals** (explicitly out of scope, not to be silently folded in): public catalogue/marketplace; authoring studios or GUIs; Figma-style tool integrations; multi-user collaboration; generic Git governance UI; site reverse engineering as a product; authority inheritance; theme swapping; RBAC; multi-authority arbitration; a universal design ontology.

---

### 9 · Reconciliation and the Case model (the third question)

When the authority evolves, what obligations does that create for applications built under earlier versions? Doctrine: authority evolves **prospectively**; its consequences may be assessed **retroactively**; historical decisions remain intact; current implementations may require reconciliation; assessment **never automatically modifies** any application.

- **Transition policy** is a property of the approved decision (a `transition` block): `prospective` (new implementations only) | `when_touched` | `required` (must name its trigger `by`; creates an obligation) | `review`. The block also supports `supersedes` chains (record lifecycle) and `resolves_cases` (links a new decision to previously unanswerable cases, so the sweep reaches affected apps through recorded cases rather than semantic matching). The compiler validates the rules (policy enum; `by` if and only if `required`; list-typed links; exceptions enum).
- **The sweep** (`da sweep --from --to`) matches deterministically first (recorded cases, and decision receipts; 36 of 53 existing consumer stores already pin the build version they ran under) and treats inferred matches as review candidates only (retrieval never establishes authority, extended to impact matching). Sweeps are idempotent: finding identity is (application, decision, target version, assessed build revision); re-assessments supersede, never duplicate.
- **Findings** classify as `conforms` / `grandfathered` / `rectify` / `review`. Grandfathering always preserves reason and trigger (never "forever"), and carries **trigger state** (`occurred` | `not_occurred` | `unknown`, each with evidence; missing evidence is never "not occurred"; `unknown` is the honest default unless receipts cover the whole post-decision modification history).
- **Obligations** carry state (`scheduled` | `due` | `overdue` | `closed`): a `required` deadline after the target version is scheduled, never presented as already due; a later receipt with `migration_for` closes the obligation and the verification result rides along; the store keeps superseded states as history.
- **Receipts** are one immutable file per published build (intent + outcome), **confirmed against source evidence** before use (a confirmer checks claims against source diffs and hashes; findings using receipt evidence carry `receipt_status: confirmed | unconfirmed`). DOM verification is record-bound: the verifier loads the record at runtime and records its hash (staleness detectable) and discloses coverage against the record's own normative items.
- **The closure cycle** was demonstrated end to end on a real revision (2026-10-11): a next revision of a built app (r2a) modified an area without migrating; the sweep detected the trigger, ended the old permission, and set the obligation `due`; a follow-up revision (r2b) migrated to the recorded pattern and was independently verified from the served DOM (9/9 checks); its receipt closed the obligation. No operation wrote to any application tree. The tested lifecycle is pinned by a regression gate (26 checks, no browser required) that re-runs the sweeps from committed fixtures, including evidence-freshness binding.
- **The Case model** (staged): one lifecycle `{id, kind, question, subject_refs, events[], status}` where gaps, disputes, proposals, verdicts and the reserved reconciliation events (`impact_finding`, `migration_decision`) are events; first as a canonical view over existing workspace files.

---

### 10 · Producing authorities (the processes)

#### 10.1 Spec-first conversion (a documented, machine-readable system)

1. Read the system's machine-readable surfaces first (rule catalogue with ids/severity/why/fix; state/contract matrices; token source file; page/pattern sources). Never re-derive from prose what the system already ships as data.
2. Map 1:1: rule catalogue to `rules.json`; states/contract matrix to component artifacts (class, states, verify selectors, a11y notes verbatim); token file to token-set artifacts; page sources to pattern records with their own descriptions. Keep a per-record `compiled_from` trail naming the source file. Compose summaries from the source's own data; never invent copy.
3. Doctrine/interaction docs become guideline artifacts plus a few behavioural rules; absolute bans become prohibitions; degradation paths become fallbacks; ship an empty candidate list honestly when the source records no open items.
4. Ship `AGENT-PROMPT.md` with the pack: the consumption protocol (resolve first, load the sanctioned way, mark silences, verify; house rules; quick reference).
5. Golden calibration: most misses are alias gaps. Multiword asks need natural multiword aliases ("dashboard page", "diff view"); when a common word matches a fallback's statement instead of the intended pattern, boost the artifact's aliases; never weaken a fallback or a threshold. Iterate to 100% agreement.
6. **Coverage sweep (standing gate)**: keep an element-by-element coverage file listing every element the *system* documents (its navigation: foundations, component furniture, patterns, token sets, doctrine), asked in natural consumer language including carrier phrases. Author the list from the system's own information architecture, not from the pack, or whole artifact-less classes stay invisible. Fix misses via aliases or new records; never loosen coverage. Miss taxonomy: alias gap vs artifact gap vs alias steal (diagnose via the resolver's `matched` fields).

#### 10.2 Domain extraction (systems without machine-readable sources, screenshot-first)

Build a renderable mirror of the source; capture screenshot-first including interaction states; tag every element BASE or OVERRIDE with evidence; partition work across domain teams; merge with explicit reversal rules; re-verify downstream against the live source. One completed derivation (the "phantom" authority, an HTML5 UP template site) exists as the reference record. Audit-console genre: when the derived product is itself a review page, it wears the reviewed language and ships its own verification contract.

#### 10.3 Synthesis (one brief, a new design language)

Source selection, then quarantine (keep the source material out of the agent's working context where required), a gestalt gate (the direction must read as one coherent language before records are written), a `decisions.json` ledger of the design decisions with rationale, a browser review instrument for the human gate, then compilation through the one compiler (dossier to pack), calibration to 100% goldens, stress testing (build real apps under it), and the full governance path (gaps, adjudication, proposals, codification). The three completed derivations (expressive, editorial, institutional) are the worked examples; the per-authority definitions live as reviewed dossier data, never in compiler code. Public playbooks exist as agent skills (`skills/synthesize-authority`, `skills/extract-design-evidence`); when the synthesis method changes, the public copies must be synced in the same session or external agents run an old pipeline.

#### 10.4 Building under an authority (the consumer workflow)

- **Resolve before building.** For each element: resolve the need in natural language; inspect before adopting; adopt only that authority's records, never another authority's or raw source-system classes.
- **Recorded states win.** Use the recorded state where one exists (a version timeline, a table's recorded phone reflow, recorded buttons/chips/dots). Never improvise a state the pack already records.
- **Mark every improvisation**: a data attribute (e.g. `data-improv="<reason>"`) plus a matching title, revealed by a toggle inside the page's own ledger, each filed as a gap with source context. The page's ledger discloses resolved / checked / improvisation count / gap ids, and its counts must match the marks.
- **Validate to zero**: run the declared validator over the build; target 0 errors, 0 warnings, score 100. Fix findings at their source; never suppress.
- **Hand over the receipts.** Built sites ship an artefacts section (every record with title/id/status/summary plus a use block), a generated agent brief, a one-click download bundle (page + styles + fonts + the pack + build log + audit trail + gaps + manifests), and a refresh log. Generated chrome is not exempt from the authority: it must use the authority's own recorded action treatments, colour roles and type registers, and a deterministic traceability gate checks every colour/radius/font in the generated block against the page's own CSS or the pack JSON. A vision review reads "plausible", not "traceable"; role violations are caught by rules, not eyes.
- **Audit agents instead of trusting them**: wrap authority calls in a logged wrapper (argv, exit code, trimmed stdout appended to an audit file), then cross-check the agent's narrative against the audit by count and order; re-run its key claims; confirm it touched nothing outside its workspace. A green handshake or a plausible answer is not proof; the workspace decision log is.

#### 10.5 Review surfaces (conventions worth reusing)

Pages the owner reads or shares follow one-job-per-block structure (title, lede, stat row, controls, contents grid, CTA, caveat); the concept explainer lives on its own page reached by a primary button; prose is plain technical English; explainer graphics are live DOM elements, never poster images; indexability is scoped per host and per path (public explainers indexable, review/commentary hosts noindex); every legacy URL 308s to its canonical successor after any move; static-asset URLs are content-hashed so no cache layer can serve stale CSS; a page that loads but looks stale is the viewer's cache, not the server.

---

### 11 · Evidence: what was measured

All programs keep written records under `docs/`; failed hypotheses and invalid runs stay in the record. Summary of each:

#### 11.1 The A/B/C authority benchmark (the founding experiment)

**Design.** Three conditions, three runs each, same brief, fresh agent context, sandboxed workspace (bubblewrap; config-level isolation alone was proven insufficient because shell tools bypass config permissions). The task app ("Procura", a procurement approvals console) had backend and routes prebuilt; agents implemented UI only, with deterministic state forcing. Condition A: starter only. Condition B: starter plus the design system vendored as a well-made static kit (rendered from the same pack C serves, parity checked by construction). Condition C: same assets plus the active authority over MCP, its validation loop and gap protocol (the treatment; the only B-to-C delta is access mode plus those loops). Metrics, per-dimension, never composited: D1 design compliance (lint), D2 design drift (captures), D3 authority behaviour (C only, from decision logs), D4 engineering quality, D5 blind human review (single reviewer, sealed mapping, scored before unsealing). Deviations D-1 through D-9 are logged in the pre-registration; read them before citing any run.

**Results.** Blind review totals of 25: A 10/18/17, B 22/19/23, C 25/21/19; condition means **A 15.0, B 21.3, C 21.7**. Flags: three runs ended at exit -15 (agent sessions killed) and one timed out, all with complete builds; they were flagged, audited for workspace completeness, and kept. Conclusions the record supports: access mode (active authority vs static docs) both beats the naive baseline decisively and edges the static kit; transcripts show why (agents with the authority check before building, and when the authority is silent they surface the decision rather than burying it). Limits: one reviewer, three runs per condition, small C-minus-B gap; no claim about users' hands.

#### 11.2 Semantic retrieval assist (experiments 01-03)

Pre-registered paraphrase and hard-negative sets. H1 **failed honestly**: no raw top-3 recall lift over lexical matching (11 vs 13 of 22). H3 held: 56% of resolve-level UNDEFINED cases have the wanted record among the candidates. H2 held end to end: zero outcome-class changes with the assist on or off across 24 live runs (the check itself surfaced three pre-existing resolver over-resolutions on new wording, none assist-induced). Performance: warm p50 12.6 ms, p95 17.7 ms; build 3.6 s; index 0.56 MB. Two hard negatives gain plausible-but-wrong neighbours and are the documented failure mode. Verdict: keep the assist frozen as shipped (optional, off by default); invest next in record descriptions, aliases and resolver applicability, not retrieval machinery.

#### 11.3 Agent-level A/B (experiment 04)

Eight builds, blind review: **no demonstrable task-level benefit** from semantic discovery (A 14/14 vs B 13/14 needs correct; zero false authority and zero unnecessary gaps in both arms; B had directionally fewer corrections). The battery's hard needs were codification failures (no records existed for what was asked), which discovery cannot fix. Findings folded back into aliases and record work.

#### 11.4 Independent verification (experiment + estate)

A blind verifier was calibrated with mutants and hardened against its own failure modes; the standing result is that self-report is evidence, never proof, and only a fresh verifier run is trusted. The consumer-flow test (a fresh agent walked the public entry end to end) surfaced two durable gaps in the brief (stale paths; the pack's contract and verifier wiring never mentioned); fixes landed the same day (brief v2, quickstart scripts, verifier v2 with optional Playwright and consumer mapping, member contracts bumped). Post-fix, a consumer build ran 34 checks as 23 PASS / 0 VIOLATION / 7 N/A / 4 REVIEW. Coverage limits are declared, not implied.

#### 11.5 Synthesis and stress (one brief, three design languages)

The same app brief was built under three synthesized authorities from very different precedent (expressive, editorial, institutional). Eleven accepted proposals became canon; twenty-five recorded declines steer later asks toward sanctioned alternatives. The builds share functionality and diverge on every visual and structural decision. Stress rounds v1-v3 generated owner verdicts (14 recorded); a boundary doctrine emerged ("what happens when the authority has no answer": the UNDEFINED case, played out through a paging story); one verdict batch (the v3.2 revision pass) remains open. The review/demo estate grew from this program (live builds served from disk, verdict capture APIs, lens tools).

#### 11.6 Portability (second authority, unmodified kernel)

An authority ("Indaba") was derived from a different source system (an Ubuntu-flavoured, orange-accented language) using the unmodified kernel. Verdict: PORTABLE-WITH-GENERIC-CHANGES; exactly one additive kernel change was required (recorded as KCL-001). The spike's rule: the kernel stays kit-agnostic, and a new authority exercises rather than forks it.

#### 11.7 Seed evolution (x05 program)

A 17-session program testing whether a formed design language can be handed between agents and evaluated without leaking. Structure: formation f1-f3 (a bookmarks app against a blank pack) then a census; adjudication codifying a canon; handoff chains (h1a to h4c) interleaved by index from a recorded seed; sealed captures; a public-but-gated blind review instrument; objective scoring frozen before any scores were computed (Layer 1 role fidelity, Layer 2 cross-component consistency; a "condition qualifier" layer). Results: blind review (single reviewer, a logged deviation from the three-reviewer spec) showed C >= B at all handoffs and C > B > A on means; objective scoring: L1 flat across conditions (no gate met), L2 near-ceiling (A = C, B marginally below). A process audit found the DA heavily consulted in C (14 RESOLVED / 29 UNDEFINED rulings; 32-54 calls per session) and an enforcement gap: the program's validation layer was hollow (no checkable rules ever staged, protocol never instructed validate). The gap was closed under owner direction (a base-lint validator, pack base-0.1.1-experiment, protocol revision mandating validate-or-file, a runner compliance gate; a retrospective sweep of all 17 seals; a live pilot validating 2x at score 100). Remaining deliverable: the program report.

#### 11.8 Reconciliation (the third question, capstone)

Sweeps over the accumulated Cadence corpus produced 36 findings (10 conforms / 22 grandfathered / 3 rectify / 1 review); a re-sweep yielded 0 new and 36 reused (idempotent); chain-derived links matched explicit ones. The closure cycle (section 9) then demonstrated the full lifecycle on a real revision pair, and the whole thing was pinned as a regression gate.

#### 11.9 What the evidence does and does not support

Supported: the authority changes agent behaviour in the loop (checks before building, surfaces silences); access mode matters at least as much as material; the governance machinery (precedents, disputes, reconciliation) closes loops deterministically; portability across source systems holds. Not supported (state plainly): first-pass visual quality improvements attributable to governance; user-level outcome improvements from compliant builds (the queued experiment); semantic retrieval lifting recall beyond lexical at this scale. Every claim in the project's public copy is written to the supported column.

---

### 12 · Rebuilding from scratch: build order and acceptance

A rebuild in ten steps; each step lists its acceptance evidence.

1. **Adopt the model** (sections 1, 3, 4): write the six spec documents for your system; declare format 0.1; fix the invariants of section 1 as non-negotiable. Acceptance: the documents exist and the thresholds, record shapes and vocabulary are pinned.
2. **Implement the kernel**: tokenizer + normalisation + scoring + the five-stage pipeline + records + validators runner, stdlib only, deterministic (no network, no time, id tie-break). Acceptance: unit tests green; byte-stable output; the four frozen constants in code as named constants.
3. **Build a reference pack spec-first** from a real system (10.1), with a curation layer for recall. Acceptance: drift gate green from a clean rebuild; every ingredient/reference id resolves; coverage sweep authored from the source's own IA.
4. **Establish the gates**: golden set at 100% agreement (unit-test enforced); convergence battery; precedent probe; dispute replay fixtures. Acceptance: all green, and deliberately breaking a record makes the relevant gate fail (a gate that cannot fail is decoration).
5. **Expose the interfaces**: CLI and stdio MCP server over the one library; workspace records; decision log. Acceptance: a smoke suite exercises every tool and asserts the decision log; a real client call is verified by the log, not by the handshake.
6. **Build the compiler**: one emit core, both modes; provenance invariants (approved-decisions XOR exception); staged validated publication; conflict refusal. Acceptance: parity against pre-unification baselines; the invariants gate including the synthetic-authority test.
7. **Add verification**: contracts plus the engine; modes and worst-of aggregation; mapping for consumers. Acceptance: contract calibrated on a clean build; mutants caught; no check loosened to pass.
8. **Institute governance**: the decision log discipline; the ten-phase evolution loop; the freeze ritual; the release policy (rc bumps by agents, human promotion). Acceptance: one full loop executed on a real need, with the record written.
9. **Serve it**: consumer foundations (`dist/`), agent brief, bundles, site surfaces, refresh automation. Acceptance: the fresh-machine test (clone, install, resolve, build a tiny sample, validate to zero) passes from committed state only.
10. **Measure it** (recommended, not optional in spirit): pre-register criteria and budgets; freeze instruments; run controlled comparisons; report per-dimension; keep failed hypotheses and invalid runs in the record. Acceptance: a report a skeptic can audit.

**Conformance evidence checklist** (the reference implementation's standing gates): kernel unit tests; triage pack drift; coverage sweep 134/134; triage goldens 58/58; synthesis goldens 18/18, 14/14, 17/17; convergence battery 34/34; compile parity 3/3 + 3/3; compile invariants 146; reconcile regression 26; precedent probe 31/31; dispute replay 4 standing (pinned expectation); MCP smoke 25/25; semantic self-test; concept-site gate.

---

### 13 · Status and open threads (2026-10-11)

**Era.** Post-freeze integration. The specification is frozen at 0.5.0; the concept boundaries are frozen by owner directive (no new capabilities); the remaining work is consolidation around the compiler/runtime/Case model.

**Latest landed.** D-031/D-032 (reconciliation formalized: tri-state triggers, obligation states, closure cycle demonstrated, receipts confirmed against evidence, record-bound verification, compiler-validated transition policies, 26-check survival gate). Repository clean and pushed.

**Staged (from the simplification program).** P0.2 Case model with compatibility adapters; P0.3 documentation-drift fixes folded into a 0.6.0 freeze; P1.1 `plan` operation with a version-pinned project contract and decision receipts; P1.2 verification consolidated under the runtime API; P1.3 source separation (dossiers into authority repos; Phase-2 moves); P2.1 `da init`; P2.2 generated documentation from canonical records.

**Owner actions pending.** Real transition policies for the twelve records and the disposition of the one `review` row (the machinery that receives them is ready); ratification of the six exception-backed records; decisions on the Triage review proposals (four drafted; the theme-profiles one explicitly awaits an owner decision); optionally a quick 0.5.1 re-freeze versus folding doc fixes into 0.6.0.

**Queued engineering.** Consolidating the kit builder's curated flow recipes into the live Triage pack (the live pack ships zero recipes today; the evolution line carries 17); the v3.2 revision pass from the fourteen stress verdicts; the x05 program report; one open pull request in the source system's stacked train.

**Live surfaces.** Concept explainer and Triage docs site public and healthy; review/audit consoles served with noindex; the seed-evolution blind instrument is stopped (its review completed); a site-refresh timer regenerates authority-site layers every five minutes.

---

### Appendix A · Reference constants and headline numbers

**Semantics:** DIRECT_MIN 6.5 · DIRECT_MARGIN 2.0 · COMPOSE_MIN 5.0 · PHRASE_BONUS 5.0 · alias weight 4.0 · score formula `max(0, round(100 - (errors*8 + warnings*2 + infos*0.5)))` · findings severities error/warning/info.

**Reference pack (Triage 0.12.2):** 80 artifacts (56 components, 10 guidelines, 7 patterns, 7 token-sets) · 19 rules · 3 fallbacks · 6 prohibitions · 0 recipes · goldens 58/58 · coverage 134/134 · snapshot commit `97cabe5` (source version 0.12.1) · validator: the source system's own lint engine.

**Estate:** 8 authority repos (triage, triage-evolution 0.13.1-experiment, wink 0.2.0, leader, dominion 0.2.0, phantom 0.2.0, indaba 0.1.0, orbit 0.1.0); 4 verification contracts (wink 34 checks, dominion 26, phantom 15, leader 0.1+fix).

**Benchmark:** condition means of 25: A 15.0 · B 21.3 · C 21.7 (runs A 10/18/17, B 22/19/23, C 25/21/19). **Semantic assist:** H1 failed (11 vs 13 of 22); 56% rescue; zero class changes; p95 17.7 ms warm. **Reconciliation:** 36 findings (10/22/3/1), 0 new on re-sweep. **Freezes:** 0.1.0 (Oct 7), 0.2.0, 0.3.0, 0.4.0, 0.5.0 (Oct 8), each tagged and checksummed.

### Appendix B · Decision-log index (D-001 through D-032, one line each)

- **D-001** Project home `~/design-authority`, separate from Triage; kernel kit-agnostic; Triage is the first pack.
- **D-002** Snapshot pin `e374f38` (Triage 0.12.1); regeneration creates a new pack version.
- **D-003** Thin kernel: access + uncertainty layers only; never re-model tokens or re-implement lint.
- **D-004** Kernel tech: Python 3.12 stdlib-first, JSON packs, no database, one library behind CLI and stdio MCP.
- **D-005** Resolution is deterministic-first; optional LLM assist may only select among retrieved candidates and must cite pack ids; golden set gates.
- **D-006** Benchmark app "Procura" (procurement approvals console); backend frozen; deterministic state forcing.
- **D-007** One pinned model for all benchmark runs; no mid-experiment changes.
- **D-008** Parity by construction: condition B's kit rendered from the same pack C serves; generated parity checklist.
- **D-009** Three runs per condition with a pre-registered extend-to-five trigger.
- **D-010** Per-dimension metrics only, no composite; instruments frozen, pre-registration after the pilot.
- **D-011** Per-condition materials defined (the B-to-C delta is access mode plus validation/gap loops).
- **D-012** Findings contract: SARIF-aligned subset; severities error/warning/info.
- **D-013** Every response echoes `{authority, version, snapshot}`.
- **D-014** The decision log: every tool call appended to the workspace; primary metrics source; never load-bearing.
- **D-015** DTCG tokens format consumed, not forked; conformance deltas recorded.
- **D-016** Proposals use the governance shape; verdicts cite evidence; nothing auto-applied.
- **D-017** Resolution priority and thresholds pinned; the "recipe beats artifact" variant rejected.
- **D-018** Search tuning is curation plus one minimal suffix normaliser; golden edits noted; 100% enforced.
- **D-019** Review verdicts are recorded records (status + notes + timestamp), judged by an agent, booked by the kernel.
- **D-020** Benchmark containment is a hard requirement (sandbox; workspace outside repo; audit; reruns for breaches).
- **D-021** D5 blind review complete: run totals A 10/18/17, B 22/19/23, C 25/21/19; mapping sealed, then unsealed.
- **D-022** Post-0.1.0 consolidation compiled; kernel drift flagged for a 0.2 freeze.
- **D-023** Freeze 0.2.0: negative precedents + candidates, scope verdicts, lenient adjudication, tool additions.
- **D-024** Lexical normalisation layer; freeze 0.3.0 ("retrieval can become fuzzy; authority determination stays grounded").
- **D-025** Optional semantic discovery; freeze 0.4.0; H1 failure recorded; shipped off by default.
- **D-026** Disputed resolutions as a first-class record; freeze 0.5.0 (a false RESOLVED is more dangerous than an UNDEFINED).
- **D-027** Simplification program adopted; P0.1: one decision-to-authority compiler; parity gate.
- **D-028** Compiler governance invariants (P0.1b): one emission path, universal provenance, staged publication, conflict refusal.
- **D-029** Reconciliation adopted: retroactive assessment; transition policy; sweep; findings; case event kinds reserved.
- **D-030** Reconciliation tightened: `resolves_cases`, policy-driven applicability, trigger state, idempotent sweeps; defaults set.
- **D-031** Tri-state triggers, obligation states, and the demonstrated closure cycle on a real revision pair.
- **D-032** Reconciliation formalized: receipt confirmation, record-bound verification, compiler-validated policies, survival gate; concept boundaries frozen (integration only from here).

*End of report. Sources: the repository (`docs/spec/00-05`, `docs/02-decisions.md`, `docs/13-simplification.md`, `docs/14-reconciliation.md`, `docs/06`-`doc 12`, experiment records under `docs/experiments/`, `docs/evolution/`, `docs/portability/`, `docs/synthesis/`, `docs/verification/`), the kernel and tool sources at `3b4a239`, and the pack manifests of the eight authority repositories.*
