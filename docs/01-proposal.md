# 01 · Proposal — minimal Design Authority prototype + three-condition experiment

**Status:** draft v1 (2026-10-07). Companion: `00-audit.md`.
**Question this plan exists to answer:**
*Does an active, queryable and enforceable Design Authority materially improve
an agent's frontend output compared with ordinary design documentation?*

**One-paragraph plan.** Triage is already ~70% machine-readable (tokens, rules,
component states, lint, gates — see audit §4). So the prototype is *thin*:
(1) an **Authority Pack** format — kit-agnostic JSON: artifacts, rules,
recipes (sanctioned compositions), fallbacks, validators, policy — 
(2) a **builder** that generates the Triage pack from the pinned snapshot
(`e374f38`) *and* simultaneously renders the Condition-B static kit from the
same pack (parity by construction), (3) a small **kernel** (Python, stdlib-first)
implementing search / resolution (RESOLVED · COMPOSE · FALLBACK · UNDEFINED ·
CONFLICT) / validation orchestration / gap + proposal records, exposed as both
a CLI and an **MCP server**, and (4) a **benchmark** — one Flask app brief, the
same backend for all runs, three materials conditions, three repetitions,
mostly-deterministic metrics, blind human review. Everything else the original
brief lists (Studio, hosting, Figma, RBAC, ontology…) is deferred.

---

## 1 · What can already function as authority (item 2)

| Triage artifact | Authority role today | Machine-readable? | Enforced? |
|---|---|---|---|
| `tokens/tokens.json` (+ `tokens.css`) | Values + tiers + theme/density variants | Yes (DTCG-ish, 240 nodes) | CI drift + `token_map --check` |
| `spec/rules.json` | Normative rules TDS001–015, severities, why/fix | Yes | triage-lint + CI |
| `lint/engine.py` + CLI | Deterministic checking incl. `--json` report | Yes | CI `--strict` |
| `spec/states.json` | Component states + verify selectors + a11y notes + lifecycle | Yes | `tools/verify.py` |
| `spec/token-consumers.json` / `token-metadata.json` | Consumption contract | Yes (generated) | `token_map.py` |
| `rename-map.json` | Vocabulary authority (old → new) | Yes | TDS001 |
| `INTERACTION.md` | Binding interaction standard + exceptions register | Prose | Partially (lint) |
| `tests/browser/` + `metrics/ui-baseline.json` | Behavioural + visual determinism | Harness + data | CI |
| `examples/*.html` (7) | Reference implementations | Markup | linted |
| `site/` docs | Human docs (foundations/components/patterns) | Python source | dogfooded |
| `AGENTS.md` | Repo-level agent contract | Prose | review |

**Assessment:** the value/rule/component layers are already an authority in
substance. What is missing is entirely on the *consumption* side: a queryable
interface, resolution semantics, composition/fallback tiers, and the
gap/proposal protocol. The kernel therefore models almost nothing that Triage
already models — it models **access and uncertainty**.

## 2 · Important ambiguities / gaps (item 3, condensed from audit §3C)

1. No machine-readable **composition** layer (sanctioned recipes live in prose).
2. No **fallback** tier between "system" and "fork".
3. **Patterns** (7) are second-class: no registry, no states/verification, and
   the component↔pattern boundary is undefined.
4. **Async/long-running work UI** (background jobs, progress, stuck states) has
   no canonical treatment — only spinner/page-state/busy-button fragments.
5. No **protocol for underspecified requests** on the consumer side: no
   improvisation marking, no gap record, no proposal route.
6. Copy rules are prose and unenforceable; a11y requirements have no single
   matrix; dataviz is explicitly token-only; multi-brand and conformance-level
   semantics are undefined.
7. **Severity override semantics** ("what may a product switch off?") implied
   by `.triagerc.json`, never formalised.

These are *opportunities*: the prototype converts some into packed artifacts
(recipes, fallbacks, gap records) and the rest into measured outcomes.

## 3 · Minimal authority representation — the Authority Pack (item 4)

### 3.1 Principles
- **Kernel knows nothing about design.** Concepts: authority metadata,
  artifacts (opaque kinds), rules, recipes, fallbacks, validators, resolution
  results, gaps, proposals. "Button", "color token", "React component", 
  "Triage" are all declared *by the pack*, not by the kernel.
- **Extensible over rigid.** Kind payloads are validated by pack-declared
  schemas; a lightweight pack can omit recipes/validators entirely.
- **Fabrication impossible by construction.** Every resolution cites artifact/
  recipe/fallback IDs that exist in the pack; the server rejects (as an error)
  any answer that cites something unknown. The LLM never writes authority.
- **JSON files, no database, no service.** A pack is a directory.

### 3.2 Pack layout (Triage pack shown; any pack follows the same shape)

```
packs/triage/
  authority.json        # manifest: id, version, format_version, snapshot, capabilities, policy
  artifacts.json        # all artifacts (id, kind, title, summary, aliases, body, relations, source, status)
  rules.json            # rules (id, severity, applies_to, statement, why, fix, enforcement)
  recipes.json          # sanctioned compositions (ingredients, constraints, when-to-use, evidence)
  fallbacks.json        # sanctioned generic fallbacks (scope, statement, constraints)
  prohibitions.json     # CONFLICT triggers (statement, signals, rule refs)
  validators.json       # validator declarations (how to run, how to parse, findings mapping)
  scoring.json          # optional: score formula (reuse Triage's from spec/rules.json)
```

### 3.3 Manifest (example)

```json
{
  "id": "triage",
  "name": "Triage Design System",
  "format_version": "0.1",
  "version": "0.12.1",
  "snapshot": { "repo": "vjsyong/triage-design-system", "commit": "e374f38" },
  "description": "The central, app-agnostic UI design authority for these products.",
  "kinds": ["component", "pattern", "token-set", "guideline", "recipe", "example", "reference"],
  "capabilities": {
    "search": true, "resolve": true,
    "validators": ["triage-lint", "drift-scan", "a11y-subset"],
    "gap_reporting": true, "extension_proposals": true,
    "resolution_assist": "optional"
  },
  "policy": {
    "on_undefined": "Implement per the consuming project's fallback policy, mark the improvisation, and report a gap. Never present improvisation as canonical.",
    "on_conflict": "Do not implement as requested; the request violates an explicit constraint.",
    "proposals": "Noncanonical. The authority is never modified by a consumer."
  }
}
```

### 3.4 Artifact (example — one component, abbreviated)

```json
{
  "id": "component/badge",
  "kind": "component",
  "title": "Badge",
  "summary": "Compact non-interactive label; never the only carrier of meaning.",
  "status": "stable",
  "aliases": ["status chip", "lozenge", "label", "tag", "pill", "state marker"],
  "body": {
    "class": "badge",
    "states": ["default", "status variants"],
    "a11y": "Colour is never the only signal — pair with text or an icon.",
    "variants_source": "core/base.css"
  },
  "relations": [
    { "rel": "governed-by", "target": "rule/TDS011" },
    { "rel": "composed-of", "target": "token-set/status-colors" }
  ],
  "source": { "path": "spec/states.json#badge", "repo": "…triage-design-system", "commit": "e374f38" },
  "examples": ["example/list", "example/dashboard"]
}
```

Patterns, guidelines, token-sets, references and examples use the same envelope
with different `kind` + `body` schemas (Triage declares them; e.g. a pattern
carries anatomy/screens, a guideline carries do/don't text with citations, an
example carries a file path + the classes it demonstrates).

### 3.5 Recipes (sanctioned compositions) — the new tier

```json
{
  "id": "recipe/status-with-text",
  "kind": "recipe",
  "title": "Status indicator that is never colour-only",
  "needs": ["status of X", "show state", "waiting/pending indicator", "flag as approved"],
  "ingredients": ["component/badge", "token-set/status-colors", "guideline/colour-not-alone"],
  "constraints": ["pair with text or icon", "one badge per row cell"],
  "evidence": { "source": "INTERACTION.md", "quote": "Colour is never the only signal …" }
}
```

Recipes are the engine's COMPOSE tier: agent-visible, citation-required, and
honestly attributed ("the authority permits/expects this composition") rather
than pretending a dedicated artifact exists.

### 3.6 Fallbacks

```json
{ "id": "fallback/plain-content", "scope": ["layout", "typography", "status"],
  "statement": "Plain content on system surfaces: system type scale + spacing tokens, no custom chrome.",
  "constraints": ["tokens only", "no new classes presented as canonical"] }
```

v0 ships 2–3 generic fallbacks. `resolve` returns FALLBACK only when a
fallback's scope matches the need; otherwise UNDEFINED.

### 3.7 Resolution semantics (the crux)

```
resolve(problem, context) →
  1. CONFLICT   if problem matches a declared prohibition (e.g. "rounded",
                "custom confirm dialog for entity delete") → cite rule/prohibition.
  2. RESOLVED   if search finds a direct artifact (alias/exact/strong match).
  3. COMPOSE    else if a recipe matches (needs-signals + ingredient availability).
  4. FALLBACK   else if a fallback's scope covers the need.
  5. UNDEFINED  otherwise — with search trace, closest candidates, why
                insufficient, fallback policy, gap guidance.
```

**Guarantees.** Every returned outcome carries `evidence` (matched ids, match
terms/scores, cited rule IDs). UNDEFINED is a *successful* outcome with a
structured body — and is distinguished from retrieval failure (which is a tool
*error*: bad input, missing pack). An optional `resolution_assist` capability
(a small LLM) may *rank/select among retrieved candidates only*; it can never
introduce an ID, and turning it off must not change correctness of the
outcome classes (only match quality within them). The kernel validates every
ID against the pack before returning. Every response echoes the authority identity (`{authority, version, snapshot}`); a miss still carries nearest candidates, the reason each was rejected, and a recovery hint (what to try next).

### 3.8 Gaps and proposals

```json
Gap: { "id": "gap/2026-10-07-001", "need": "show progress of a background job",
  "context": {"project": "procura", "page": "jobs"},
  "authority": {"id": "triage", "version": "0.12.1", "commit": "e374f38"},
  "searched": {"queries": [...], "kinds": [...]},
  "closest": ["component/spinner", "component/page-state"],
  "why_insufficient": "spinner expresses activity, not progress; page-state is full-page only",
  "fallback_used": {"id": "fallback/plain-content", "description": "custom progress row, tokens only"},
  "evidence": ["runs/c2/static/js/jobs.js#L41"],
  "scope_hint": "system-wide", "status": "open", "created": "…" }

Proposal: { "id": "prop/…", "gap_id": "gap/…",
  "problem": "...", "insufficiency": "...", "reuse_case": "...",
  "composition_check": "why existing artifacts cannot compose",
  "proposed": [{ "kind": "component", "name": "progress", "sketch": "..." }],
  "depends_on": ["component/spinner"], "new_primitives": ["determinate progress"],
  "tests": [{ "description": "...", "deterministic": true }],
  "status": "candidate", "review": { "verdict": null } }
```

### 3.9 Assumptions (explicit)
1. A pack is generated from an immutable source snapshot; regeneration = new
   version. Manual curation during v0 generation is allowed but must be
   reproducible and recorded (the "codification sprint" log).
2. Resolution quality is bounded by curation. We bound it with a **golden set**
   of ~25 design problems with expected outcome classes, written before the
   benchmark and versioned with the pack.
3. The kernel's LLM use is optional and sandboxed to candidate selection; the
   authority is deterministic by default (also required for benchmark
   reproducibility).
4. Validators are *declared* (command + parser), not built in; Triage's lint is
   wrapped, not reimplemented.
5. Gap/proposal records live in the *consuming workspace*
   (`<project>/.design-authority/`), not in the published pack.

## 4 · Agent-facing tool surface (item 5) — MCP server `design-authority`

| Tool | Input → Output | Notes |
|---|---|---|
| `authority_overview()` | → manifest, capability list, counts, resolution semantics primer, policy | One call teaches an agent how to use the authority. |
| `search_authority(query, kinds?, limit?)` | → ranked artifacts (id, kind, title, summary, why-matched) + matching rule IDs | Lexical + alias scoring over the pack index. |
| `inspect_artifact(id)` | → full artifact: definition, states, a11y, relations, rules, source refs, examples | Citations point into the Triage snapshot. |
| `resolve_design_problem(problem, context?)` | → `{outcome, resolution, alternatives, constraints, evidence, policy}` | The five outcomes; UNDEFINED structured; CONFLICT cites prohibitions. |
| `validate_implementation(target)` | → normalized findings (validator, rule, severity, file, line, message, fix) + summary | Runs declared validators (triage-lint wrapper first; drift/a11y later). |
| `report_gap(need, context, attempted_resolution)` | → gap record (id, stored path) + template for proposals | Writes to workspace `gaps.jsonl`; marks improvisation. |
| `propose_extension(gap_id, proposal)` | → validated candidate proposal + review checklist | Shape-validated; citations checked; stored noncanonically. |

Prior-art conventions adopted (see §12): every response echoes
`{authority, version, snapshot}` (per-read version identity);
`validate_implementation` findings use a SARIF-aligned subset (rule id,
severity, location, message, fix); error results carry a recovery hint (the
next tool to call); the server keeps a decision log (JSONL) of calls in the
run workspace for metrics and replay.

Also exposed: MCP **resources** `authority://overview`, `authority://rules`,
`authority://artifact/{id}` for agents that prefer passive reads.
Operator-side (CLI, not agent-facing): `da overview/search/inspect/resolve/
validate/gaps/proposals/review` — same library, used by tests, the harness and
the humans.

**Deliberately not included in v0:** update/write tools against the pack,
multi-authority arbitration, authn, HTTP transport, catalog browsing UI.

## 5 · Benchmark application (item 6)

**"Procura" — a procurement approvals console** (fictional; internal ops tool).
Chosen because approvals naturally exercise every required surface and the
brief can carry genuinely underspecified asks that fail in *interesting* ways.

**Deliberate control: the backend is prebuilt and frozen.** The starter repo
ships the full Flask backend (routes, SQLite seed, endpoints) with placeholder
UI pages; agents implement the UI (templates + static assets) only. This keeps
**functionality identical across conditions** by construction and focuses the
measurement on frontend decisions — which is the stated question.

Feature surface (required by the brief, phrased in user terms):
1. Application shell + navigation (Dashboard · Requests · Jobs · Settings).
2. Dashboard/overview: pending count, spend stat, recent activity, jobs strip.
3. Requests data table: filtering (status, category, requester), search,
   pagination, row actions.
4. Request detail: fields + approval actions (approve / reject) + comments.
5. Settings: forms + toggles (notification prefs, auto-approve threshold).
6. Dialogs: reject confirmation (destructive, irreversible note).
7. Feedback: transient success after actions; a persistent connector error
   state; loading state while data loads.
8. Empty states (no requests / no results / no activity).
9. Responsive/mobile rendering.
10. Bulk selection + bulk approve/reject.

The 4 **underspecified asks** (never phrased with Triage names):
- **UQ1** "Users need to see the status of a long-running background operation
  (the AI triage job that scans new requests)."
- **UQ2** "Users should be able to approve or reject many selected requests at
  once."
- **UQ3** "Show a compact history of recent approval steps on each request."
- **UQ4** "We probably need something like a compact picker for assigning a
  reviewer."

The starter backend supports deterministic state forcing (`?empty=1`,
`?error=1`, `?job=running|done`) so empty/error/loading states are capturable
identically in every run. Seed data is fixed and synthetic.

## 6 · Three-condition experimental design (item 7)

### 6.1 Materials (one source → two representations)

```
Triage snapshot e374f38
   ├─ Authority Pack  → served via MCP                      → Condition C
   └─ same Pack ──────→ rendered static kit (markdown)      → Condition B
```

The **pack builder emits both**; a generated **parity checklist** asserts that
every artifact/rule/recipe/fallback appears in B's kit and nothing appears in
B's kit that is not in the pack. Condition B must not be artificially weak:
its kit is a genuinely excellent static document set (same words, same rules
with why/fix, same catalogue data, same examples).

**Workspaces per run:**

| | Condition A — naive | Condition B — passive kit | Condition C — authority |
|---|---|---|---|
| Starter app (frozen backend) | ✓ | ✓ | ✓ |
| System assets vendored (`tokens/ core/ fonts/ icons/ examples/`) | – | ✓ | ✓ |
| Static design kit `design/` (rendered docs) | – | ✓ | – |
| `DESIGN.md` (rules of engagement) | – | – | ✓ |
| MCP `design-authority` connected | – | – | ✓ |
| Instruction block | none (brief only) | "Follow the design system in `design/`." | "Consult the authority; validate; never present improvisation as canon; report gaps." |

Prompts: identical base brief; condition blocks are the only delta (full texts
committed under `benchmark/briefs/`). The same model (pinned; single choice
recorded in the decision log) runs all conditions with the same agent config,
same turn budget, fresh session and fresh workdir per run.

### 6.2 Repetitions & execution
- v1: **3 runs per condition (9 total)**; pre-registered rule: if spread within
  a condition on any primary dimension is large enough to dominate the C−B
  gap, extend to 5 per condition *before* interpreting.
- Serial execution on one machine, same day-part where feasible; every run
  fully recorded: prompt, transcript, tool calls (C), git diff, validation
  outputs, screenshots, runtime, token/time metrics.
- Runs are automated by the harness (`opencode run` headless, dedicated config
  dir with plugins/mem disabled); a run that crashes is retried once and the
  incident recorded.

### 6.3 What must stay equal (and what is deliberately different)
Equal: model, agent, budget, brief, starter commit, seed data, capture
procedure, validators, reviewers. Deliberately different (the treatment):
knowledge *access mode* — files vs tools; C additionally gets a validation
loop and the gap protocol; B's docs are static. Known asymmetries are
documented in the pre-registration (e.g. C pays tool round-trips; B can grep
freely).

## 7 · Metrics & validation strategy (item 8)

**Pre-registered before looking at outputs** (instruments frozen after the
pilot, `docs/03-preregistration.md`); per-dimension reporting only — **no
composite score** (unless later justified in writing).

### D1 · Design compliance (deterministic)
- triage-lint (same snapshot, default config) over each output: findings by
  rule/severity, score; unsupported colours / spacing / type / radius /
  border / elevation; invented component styles (parsed); canonical class use;
  known misuse; TDS014/015 a11y findings.
### D2 · Design drift (deterministic, condition-blind where possible)
- code scans: unique raw colour values; unique px spacing values; distinct
  radii; font stacks; `!important` count; inline style attributes; one-off
  class count; duplicate declaration blocks; backend-diff (scope discipline).
- DOM probes (headless Chrome, computed styles over all elements): unique
  background/fg colours, radii, font families; spacing-value histogram; inline
  styles; landmark/semantic checks; per-screen consistency probes (same
  semantic element → same treatment across pages; e.g. destructive styling,
  row actions, empty-state anatomy).
### D3 · Authority behaviour (C only; partially manual)
- authority calls by tool (from the server decision log); **incorrect resolutions**
  (manual audit vs golden-set expectations); UNDEFINED cases handled as
  UNDEFINED (not silently invented); gaps reported; unauthorised inventions;
  fallback use conformance; validation calls and reaction to findings.
### D4 · Engineering quality
- functional probes (scripted, tolerant, identical across conditions: pages
  200, filters/pagination work, approve/bulk/reject actions execute, error/
  empty states render); component reuse counts; duplication; tests present;
  crash/console error counts.
### D5 · Human review (blind)
- anonymised screenshot galleries (random build codes, shuffled), fixed routes
  × 2 viewports; reviewer rates: consistency; coherence; obvious design
  mistakes; confidence that another page could be added consistently; amount
  of manual cleanup required. Reviewer sees no condition labels; mapping is
  sealed.
### D6 · Process/metrics of the experiment itself
- runtime, tool calls, tokens where available; incidents; deviations.

Instrument notes: axe-core vendored for a11y scanning (fallback: hand-rolled
subset); screenshots at 1440×900 and 390×844 with animations settled; all
instruments run identically over all three conditions.

## 8 · Smallest prototype architecture (item 9)

```
~/design-authority/               (new repo; local, push later)
├─ kernel/design_authority/       # Python package, stdlib-first
│   ├─ pack.py                    # load/validate packs, index build (aliases, search)
│   ├─ search.py                  # lexical + alias scoring (difflib/token overlap)
│   ├─ resolve.py                 # 5-outcome pipeline; prohibitions; recipes; fallbacks
│   ├─ validate.py                # validator runner + normalized findings
│   ├─ records.py                 # gaps + proposals (workspace JSONL/files)
│   ├─ mcp_server.py              # stdio MCP (fastmcp), 7 tools + resources
│   └─ cli.py                     # `da` — same library for humans/tests/harness
├─ tools/build_pack_triage.py     # snapshot → pack (+ golden-set checks)
├─ tools/render_kit.py            # pack → Condition-B static kit (parity by construction)
├─ packs/triage/                  # generated + curated (committed; manifest pins e374f38)
├─ benchmark/
│   ├─ starter/                   # Procura Flask starter (backend frozen; UI = task)
│   ├─ briefs/                    # base brief + condition blocks
│   ├─ harness/                   # run / capture / scan / a11y / interact / report
│   └─ runs/                      # per-run artifacts (gitignored; summaries committed)
└─ docs/                          # audit, proposal, decisions, gap log, preregistration, report
```

Dependencies: Python 3.12 stdlib for the kernel core; `fastmcp`/`mcp` for the
server (already proven in this environment); headless Chrome for capture
(Playwright cache on this host); opencode for benchmark runs. No server
hosting, no database, no web UI beyond generated galleries.

## 9 · Phased implementation plan (item 10)

| Phase | Deliverable | Gate (must pass to proceed) |
|---|---|---|
| **P0** Audit + plan (this doc) | `docs/00`–`03` | Your review of this proposal. |
| **P1** Kernel + pack | pack v0 from `e374f38`; `da` CLI (overview/search/inspect/resolve/validate); golden set (~25 problems, ≥5 UNDEFINED, ≥3 COMPOSE); unit tests; B-kit renderer + parity check | `da resolve` agrees with golden set ≥85%; parity checklist clean; `da validate` reproduces triage-lint findings on a sample target. |
| **P2** Agent interface | MCP server; opencode + Hermes smoke tests; e2e gap → proposal → adversarial review (synthetic gap, reviewer prompt from the brief) | Recorded e2e; two clients connect; proposal review produces a verdict + deterministic checks. |
| **P3** Benchmark scaffold | Procura starter; briefs; materials generator; harness (run/capture/scan/a11y/interact/report); pilot 1×3 | Pilot report; instruments frozen + pre-registration committed; no blockers. |
| **P4** Runs | 3×(A,B,C) full runs with complete recordings (extend to 5 if pre-registered trigger fires) | Every run has complete artifacts; spot-check verification passed. |
| **P5** Evaluation | Analysis + blind human review + `docs/05-benchmark-report.md` + Triage gap log + ≥1 real extension proposal through the adversarial loop (+ optional authority-v2 rerun) | Report with per-dimension results, threats, and next-step recommendation. |

Observations discovered during P1–P3 (e.g. which recipes/fallbacks had to be
formalised) are first-class results — logged in `docs/04-gap-log.md` as the
codification sprint proceeds.

## 10 · Threats to validity (initial; expanded in pre-registration)

1. **Snapshot drift** — upstream Triage is moving fast; the pack pins
   `e374f38` and records it everywhere. Reruns against newer snapshots are a
   *feature* (loop), not a bug, but must be labelled.
2. **Single model** — findings may not generalise across models; recorded.
3. **N small** — 3 reps detect large effects only; treated as iteration
   signal, not significance; paired per-dimension diffs.
4. **Our own curation** — resolution/recipe quality is authored by us and can
   bias C; the golden set + honest UNDEFINED policy bound it; the goldens are
   committed before runs.
5. **B-kit authorship** — mitigated by generation-from-pack + parity check +
   review.
6. **Access-mode asymmetry** — C's tool round-trips vs B's file reads; budget
   controlled by turns/time, documented.
7. **Reviewer bias** — blind galleries, sealed mapping; reviewer familiarity
   with Triage is noted.
8. **Screenshot determinism** — fonts/animations/data; mitigated by fixed
   viewports, settled waits, seeded data; residual noise recorded.
9. **Task narrowness** — one app, one brief; scope statement in the report.

## 11 · Non-goals (item 11 — deferred, explicitly)

Public catalogue · multi-tenant hosting · visual Studio · Figma integration ·
site reverse-engineering · enterprise RBAC · full Git governance product ·
every framework · universal design ontology. Also deferred within scope:
multi-authority packs, HTTP transport, authn, LLM-authored authority content,
automatic pack regeneration on upstream changes.

## 12 · Prior art (folded 2026-10-07)

Two research passes surveyed ~40 agent-facing design-system servers and the
design-linting / policy-as-code canon. Condensed findings and what they change:

**Agent-facing design systems (selected).** Figma Dev Mode MCP (~30 tools,
typed fallbacks); Storybook addon-mcp (component manifest; docs→generate→
test-run→fix loop; `isError` + "use docs-list" recovery hints); zeroheight
(search; token linting with nearest-name suggestions; "tell the agent what's
missing so it doesn't guess"); Supernova (**the only shipped agent
feedback/gap primitive found**); Atlassian ADS MCP (**explicit canonical tier
vs fallback tier**: "do not treat as equal-priority replacements"); Tokens
Studio (review→apply/discard/undo governance, branch provenance); shadcn /
Ant Design / MUI (staged discovery list→search→view→examples; per-version
pinning + changelog diffs; validation lives in their CLIs); Helios (tools +
resources + prompts; explicit installed-vs-bundled version seam; top-5
suggestions on miss); figma-console-mcp (DTCG verify + parity scoring —
community).

**Key lessons (mapped to this plan).**
1. The five-way outcome vocabulary is **unclaimed**. Nearest precedents:
   Atlassian's canonical/fallback tiers, zeroheight's exact/close suggestions.
   The kernel's differentiator stands.
2. Structured gap reporting is nearly greenfield; keep `report_gap` +
   proposals as core, not garnish.
3. Never confabulate a match: misses carry nearest candidates, rejection
   reasons, recovery hints (Helios / zeroheight / Storybook lessons).
4. Version identity per read, echoed back; model version seams explicitly
   (done: manifest + snapshot echo; D-013).
5. Reuse lint/report conventions: stable rule IDs, error/warn/info severities,
   why/fix, and a SARIF-aligned findings shape (D-012).
6. Copy the policy-engine operating model (OPA/Conftest/Cedar): decisions cite
   the determining rule(s); policies have their own tests (our golden set);
   keep an optional decision log for replay/metrics (D-014).
7. DTCG 2025.10 is now a stable spec with a JSON Schema + conformance suite:
   consume it, don't fork it (D-015).
8. Validation archetypes to copy: snippet→validated result; artifact→parity
   verifier; model→dry-run validator. Uber/Atlassian/Primer component-usage
   linting confirms Triage's rule-content direction; API Extractor's
   golden-file pattern is noted for a later component-API contract.
9. Human governance channels already exist (RFC/stages/contribution models;
   Brad Frost's flow covers exactly our UNDEFINED/COMPOSE cases) — proposals
   hook into that shape rather than a parallel process (D-016).

**Consequential adjustments:** findings shape SARIF-aligned (§4, D-012);
per-response version echo (§3.7/§4, D-013); decision log for D3 (§7, D-014);
DTCG conformance check added to pack-builder gates (P1, D-015); recipe and
prohibition content seeded from INTERACTION.md rather than invented (P1).
