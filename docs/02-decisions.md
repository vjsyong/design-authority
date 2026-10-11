# 02 · Decision log (running)

Rules for this log: one entry per durable decision; record the *why* and what
evidence would overturn it. Append-only; supersede with new entries.

---

**D-001 · Project home.** `~/design-authority` as a new repository, separate
from Triage. The kernel is kit-agnostic; Triage is the first *pack*, generated
from a pinned snapshot and never edited in place by consumers.

**D-002 · Snapshot pin = `e374f38`** (Triage 0.12.1, branch `tds-fix-wrap` ==
local `demo`; newest complete state; stacked PRs #1–#6 + fix not yet merged to
`origin/main`). The pack manifest records repo+commit everywhere; if upstream
advances, regeneration creates a new pack version (that's the loop).

**D-003 · Thin kernel.** Audit evidence: Triage is already ~70% machine-
readable (tokens/rules/states/enforcement). The kernel only adds access +
uncertainty layers (search, resolution, recipes, fallbacks, gaps, proposals).
Anything that re-models tokens or re-implements lint is rejected by default.

**D-004 · Kernel tech.** Python 3.12 stdlib-first; packs are JSON directories;
no database; one library exposing both a CLI (`da`) and a stdio MCP server
(`fastmcp`, consistent with existing local MCP servers); server state limited
to the consuming workspace (`.design-authority/`).

**D-005 · Resolution = deterministic-first.** Alias + lexical matching over
pack artifacts; optional LLM assist may only select among retrieved candidates
and must cite pack IDs (server-validated). Outcome classes must not depend on
the assist. A committed golden set (~25 problems, incl. ≥5 UNDEFINED, ≥3
COMPOSE) gates P1.

**D-006 · Benchmark app = "Procura"**, a procurement approvals console.
Backend + routes prebuilt and frozen; agents implement UI only. Deterministic
state forcing via `?empty=1`, `?error=1`, `?job=running|done`.

**D-007 · Benchmark model = single pinned model for all runs.** Candidates
(from opencode providers): `opencode-go/deepseek-v4-flash` (draft default),
`opencode-go/glm-5.3-flash`, `opencode-go/gpt-5.6-luna`. Final pick after a
short capability probe in P3; recorded here. No model changes mid-experiment.

**D-008 · Parity by construction.** Condition B's static kit is *rendered from
the same pack* that Condition C serves via MCP; a generated parity checklist
fails the build if the two representations diverge in content.

**D-009 · Repetitions.** 3 runs per condition (9 total) for v1. Pre-registered
trigger: if within-condition spread dominates the C−B gap on a primary
dimension, extend to 5 per condition before interpreting.

**D-010 · Metrics discipline.** Per-dimension reporting only; no composite
score. Instruments frozen and pre-registration committed after the pilot,
before any comparative interpretation.

**D-011 · Materials per condition.** A: starter only. B: starter + vendored
system assets (`tokens/ core/ fonts/ icons/ examples/` from the snapshot) +
`design/` rendered docs. C: starter + same vendored assets + `DESIGN.md` +
MCP authority. The only B↔C delta is access mode (static docs vs active
authority) — plus C's validation loop and gap protocol, which are the
treatment. Package README/AGENTS/INTERACTION are NOT vendored as files for B/C;
their content enters via the pack render (B) / authority (C).

**D-012 · Findings contract = SARIF-aligned subset.** Validate outputs use
{rule, severity, message, location{path,line}, fix} — ESLint/axe/SARIF
conventions; a `--sarif` export is a later option, never a new format.
Severities stay error/warning/info.

**D-013 · Version identity per read, echoed.** Every tool response includes
`{authority, version, snapshot}`; `DESIGN.md` instructs agents to cite them in
records. (Helios/AntD lesson.)

**D-014 · Authority decision log.** The server appends every tool call (name,
params digest, outcome class, matched IDs, latency) to
`<workspace>/.design-authority/decision-log.jsonl` — primary source for metrics
D3 and for replay. Disabling it must not change behaviour.

**D-015 · DTCG 2025.10 consumed, not forked.** The pack builder validates
Triage's `tokens.json` against the official format where possible and records
conformance deltas in the gap log.

**D-016 · Proposals use the existing governance shape.** Adversarial reviewer
+ deterministic checks + explicit accept/reject/needs-info, every verdict
citing its determining evidence; nothing is ever auto-applied upstream.
(Tokens Studio / OPA / Cedar lessons.)

**D-017 · Resolution priority follows the brief.** CONFLICT first; RESOLVED
when an artifact directly defines the solution (score ≥ 6.5, margin ≥ 2 over
the runner-up); COMPOSE when no artifact qualifies but a recipe does (≥ 5.0);
FALLBACK when a non-catch-all fallback scope matches; else UNDEFINED. A
"recipe beats artifact" variant was prototyped and rejected — it contradicts
the stated meaning of COMPOSE ("no dedicated artifact exists") and was masking
tokenizer precision bugs. Pinned by the golden set (100% gate in unit tests).

**D-018 · Search tuning is curation + minimal mechanics.** One tiny consistent
suffix normaliser (plural, e-drop, guarded -able); artifact aliases and recipe
`needs` are the recall surface, edited deliberately and recorded in the gap
log; thresholds (6.5 / 5.0 / margin 2.0) live in `resolve.py` as named
constants. Golden-set edits require a note here; the unit test enforces 100%
agreement so precision regressions cannot land silently.

**D-019 · Review verdicts are recorded records, not vibes.** `da review
--proposal … --verdict accept|reject|needs-info` (backed by
`records.set_proposal_review`) transitions the proposal status and stores the
review notes + timestamp. The agent does the judging; the kernel does the
bookkeeping. First use: the P2 e2e demo (docs/05) → `needs-info`.

**D-020 · Benchmark containment is a hard requirement.** Agent runs execute
sandboxed: bubblewrap minimal filesystem + per-run `XDG_CONFIG_HOME` + strict
opencode permissions + transcript containment audit. Any run with
`containment.refs_outside > 0` is flagged and rerun; breaches are recorded in
the deviations log (docs/06). Workspaces live outside the repo
(`/tmp/da-ws/<run-id>`), archived back to `benchmark/runs/<run-id>/ws` after
the run. (Triggered by the a1/b1 breach — see docs/06 D-1.)

---

## Assumptions to verify

- **A-1** opencode runs can be isolated per run (dedicated config dir,
  plugins/mem disabled, fresh session id, fresh workdir). Verify in P3.
- **A-2** `fastmcp`/`mcp` installable in the kernel venv. Verify in P2.
- **A-3** Headless Chrome (Playwright cache, cf. `chromium-1234`, v151) is the
  capture engine for apps and docs. Verified present on this host.
- **A-4** Benchmark agents need no network beyond model calls; web-fetch
  availability, if any, is identical across conditions (config-controlled).
- **A-5** One human reviewer (Sean) suffices for v1 blind review; a second
  reviewer is a bonus, not a gate.

## Open questions (resolve in P1–P3)

- Q-1 Model choice (D-007) — probe + decide.
- Q-2 B kit format: markdown corpus + vendored assets (proposed) vs also a
  static snapshot of the docs site. Current lean: markdown only; note the site
  exists in C's citations.
- Q-3 C validation is agent-triggered only (the treatment), never pushed.
- Q-4 Lint scans for D1/D2 exclude vendored assets and the backend; only
  run-authored files count. Confirm wording in pre-registration.
- Q-5 Questionnaire wording + gallery design (P3).
- Q-6 Push to GitHub (`vjsyong/design-authority`, private) at end of P1.

## Deferred (do not build now)

Public catalogue · multi-tenant hosting · Studio · Figma integration · site
reverse-engineering · RBAC · Git governance product · framework breadth ·
universal ontology · HTTP MCP transport · authn · multi-pack arbitration ·
automatic pack regeneration · LLM-authored authority content.

## D-021 · D5 blind review complete (2026-10-07)

Single blind reviewer (project owner) scored all nine production builds
before the condition mapping was unsealed; scores archived at
`benchmark/review/procura-review-2026-10-07.csv`, mapping at
`benchmark/runs/_gallery-mapping-SEALED.json`. Condition totals (of 25):
A 10/18/17 · B 22/19/23 · C 25/21/19. Full analysis in
`docs/09-final-synthesis.md`.

## D-022 · Post-0.1.0 consolidation compiled (2026-10-08)

Everything after the freeze is gathered in
`docs/11-consolidation-since-0.1.0.md` (53 commits + the uncommitted
review-window tail — portability · synthesis Gates 1–2 · Cadence stress
v1–v3 · adjudication + codification · lenient doctrine · decision-review
window). Flagged for owner ruling: the frozen surface has drifted — 6/16
manifest files (all kernel, +731/−13) carry post-freeze semantic deltas
including tool contracts (`precedent-check` · `precedents` · `candidates` ·
`check_precedent` · `list_candidates`) and record-format extensions; per
`docs/spec/05` these want a 0.2 bump + fresh freeze (the conformance battery
is green either way). Recommendation: schedule the 0.2 freeze; alternative:
a logged editorial waiver.

## D-023 · Freeze Design Authority 0.2.0 (2026-10-08)

Owner ruling: *"formalise everything now as 0.2."* Executed the §3 freeze
procedure of `docs/spec/05`: the spec set was updated to document the
post-freeze semantics — negative precedents + candidates as optional
format-0.1 records · precedent scope verdicts `governs`/`outside`/`ambiguous`
· the lenient adjudication doctrine · tool-contract additions (CLI
`precedents` / `precedent-check` / `candidates`; MCP `list_precedents` /
`check_precedent` / `list_candidates` — 10 tools; validator `{pack}`
substitution + `lint-json` parser name; `authority://` resources; record
`precedent_warnings` / `candidate_hints`). VERSION → `0.2.0`; fresh manifest
`docs/spec/freeze-0.2.0.sha256`; tag `v0.2.0`. Conformance at freeze: kernel
17/17 · triage goldens 19/19 · evolution 23/23 · synthesis 18/18 · 14/14 ·
17/17 · convergence battery 34/34 · precedent probe 31/31 · MCP smoke 20/20.
Thresholds, pipeline order and the outcome taxonomy are unchanged between
0.1.0 and 0.2.0; the 0.1.0 frozen bytes remain in `freeze-0.1.0.sha256`.

## D-024 · Lexical normalisation layer; freeze Design Authority 0.3.0 (2026-10-08)

Owner directive: a lexical normalization layer comes first, under the premise
*"Retrieval can become fuzzy. Authority determination must remain grounded,
explicit, and auditable."* Implemented as a retrieval-side kernel layer
(`kernel/design_authority/lex.py`, layer version 1): a curated US/UK
spelling-variant table applied identically to queries and index text before
stemming, with guarded, table-bounded reductions, idempotent canonical forms,
and import-time conflict validation. Every query rewrite is reported in the
`normalized` output field; the outcome taxonomy, thresholds, precedence and
citation rules are unchanged. Evidence: dialogue/dialog, behaviour/behavior
and licence/license asks now meet their curated vocabulary (each was
previously split: e.g. `dialogue` missed `component/dlg` entirely); the
golden set gained US-spelling twins (`the color tokens`, `a dialogue`);
kernel 23/23 · triage goldens 56/56 · sweep 134/134 · precedent probe 31/31 ·
MCP smoke 20/20 at the freeze. Per `docs/spec/05` this is a semantic change →
0.3.0 with a fresh freeze and manifest (`docs/spec/freeze-0.3.0.sha256`),
tag `v0.3.0`.

## D-025 · Optional semantic discovery (retrieval assist); freeze Design Authority 0.4.0 (2026-10-08)

Reviewer proposal adopted as doctrine: *"Retrieval can be probabilistic. The
authority's normative claims must remain grounded in the published record."*
Implemented as an optional, off-by-default retrieval extension: `tools/da_sem.py`
(build / query / info / stale / serve; SQLite FTS5 BM25 + FastEmbed
`bge-small-en-v1.5` + NumPy cosine, RRF fusion, brute force at pack scale),
kernel surfaces `da discover`, `resolve --assist semantic`, MCP
`discover_candidates` (11th tool) and the `assist` parameter on
`resolve_design_problem`. Hard invariants: retrieval never establishes
authority (candidates carry retrieval evidence only, never an outcome class);
ids are validated before return; canonical records are the default scope and
history (precedents, candidates) is searched separately; the assist attaches
only on UNDEFINED; enabling it never changes outcome classes; the kernel
stays stdlib-only and every lexical surface is unchanged without the extras.
Pre-registered experiment (plan, held-out paraphrase set, hard negatives,
decision rules, then results): `docs/experiments/01-semantic-retrieval.md`.
H1 failed honestly (no raw top-3 recall lift on paraphrase, 11 vs 13 of 22);
H3 held (56% of resolve-level UNDEFINED cases have the wanted record among the
candidates); H2 held end-to-end (zero class changes on 24 live runs; the metric
surfaced three pre-existing frozen-resolver over-resolutions on new wording,
none assist-induced); H4 met (warm p50 12.6 ms, p95 17.7 ms; cold 1.02 s;
build 3.6 s; 0.56 MB). Two hard negatives gain plausible-but-wrong neighbours
under the semantic leg and are documented as the shipped failure mode. Agent
interaction traced in `docs/experiments/02-agent-trace.md` (session through
the real MCP server; every call recorded, decision log and gap shipped as
evidence). Conformance at freeze: kernel 30/30 · triage goldens 56/56 · sweep
134/134 · synthesis goldens 18/18 · 14/14 · 17/17 · precedent probe 31/31 ·
MCP smoke 22/22 · semantic self-test OK · concept-site gate green. Per
`docs/spec/05` this is a semantic change → 0.4.0 with a fresh freeze and
manifest (`docs/spec/freeze-0.4.0.sha256`), tag `v0.4.0`.

## D-026 · Disputed resolutions; freeze Design Authority 0.5.0 (2026-10-08)

Reviewer direction adopted: a false RESOLVED is more dangerous than an
UNDEFINED, because a blindly trusting agent builds from it, and agent
scepticism must not be the safeguard. Implemented as a first-class consumer
record (`disputes.jsonl`, kind `disputed-resolution`): query, the id the
resolver claimed, reason, optional suggested fix, context, status — distinct
from a gap (no answer) because a dispute is a wrong answer. Surfaces: CLI
`dispute-add` / `disputes` / `dispute-replay`; MCP `report_dispute` /
`list_disputes` / `replay_disputes` (tools 11 to 14). Replay re-runs the
resolver over open disputes (`still_stands` / `cleared`; `--expect-standing`
gating), making the fixture set the regression harness for resolver
applicability. Resolution semantics are untouched; disputes are evidence,
never instructions. Seeded fixture set: `docs/experiments/disputes/` (four
observed misresolutions: skip link, slide-in panel, state label, row
chevron; all four stand at this freeze and the gate pins that count).
Conformance at freeze: kernel 34/34 · triage goldens 56/56 · sweep 134/134 ·
synthesis goldens 18/18 · 14/14 · 17/17 · precedent probe 31/31 · MCP smoke
25/25 · semantic self-test OK · concept-site gate green · dispute replay
4 standing (expected). Per `docs/spec/05` this is a semantic change → 0.5.0
with a fresh freeze and manifest (`docs/spec/freeze-0.5.0.sha256`), tag
`v0.5.0`.

## D-027 · Simplification program adopted; P0.1 — one decision-to-authority compiler (2026-10-11)

Owner review adopted as the program plan (`docs/13-simplification.md`): the
system is reorganized around one organizing abstraction — a compiler for
governed design decisions, with a small runtime that agents use to apply and
verify them. Doctrine restated and unchanged: evidence produces decisions,
approved decisions compile into authority, agents consume authority,
deviations return as reviewable cases; agents may improvise, never present
improvisation as authority.

P0.1 executed — one generic compile path replaces the two mechanisms that
turned approved decisions into authoritative records. `tools/da_compile.py`
holds the single emit core: `synthesis` mode compiles an authority dossier
(reviewed data at `docs/synthesis/<src>/compile.json`: the approved decision
ledger plus the records those decisions emit), `codify` mode merges
reviewer-accepted proposals into a pack. The hardcoded per-source builders
in `compile_pack.py` (552 → 36 lines) and the `SUMMARY` dict in
`apply_proposals.py` (179 → 38 lines) are gone; both files are
CLI-compatible adapters. The eleven editorial summaries were migrated into
the proposal records they describe (`review.codified_summary`), so summaries
travel with their decisions. Parity fixtures captured from the
pre-unification tools pin behaviour byte-for-byte
(`docs/synthesis/data/parity/`, `tools/compile_parity.py`, wired into
`check.sh`): compile 3/3 sources and codify 3/3 workspaces reproduce their
baselines exactly (codify with its recorded `codified_at`). Conformance at
this change: triage pack drift in sync · coverage sweep 134/134 · kernel
34/34 · triage goldens 58/58 · synthesis goldens 18/18 · 14/14 · 17/17 ·
compile parity OK · precedent probe 31/31 · dispute replay 4 standing
(expected) · MCP smoke 25/25 · concept-site gate PASS · semantic self-test
OK. The kernel and the frozen 0.5 surface are untouched; the next stages
(Case model P0.2, drift fixes P0.3, plan/verify P1, source separation P1.3,
`da init` P2) are staged in `docs/13-simplification.md`.

## D-028 · Compiler governance invariants; P0.1b — shared emission and provenance enforcement (2026-10-11)

Owner code review of P0.1: the unification stopped at the entry points
(synthesis builds whole packs while codify builds records) and non-artifact
records could compile with empty provenance (`"decisions": []`). Parity had
proved "no accidental drift", not "the output satisfies the governance
invariants". Directive adopted: governance is enforced by the compiler
itself, not by convention; declare the invariant, then let the gate test it.

Landed. ONE emission function (`_finalize_record`) now serves both modes,
attaching provenance uniformly and validating record type, required fields
and provenance; `validate_record` / `validate_provenance` are public so the
invariants gate and the compiler cannot drift apart. Every normative record
carries `compiled_from` approved decisions or an explicit `exception` block
(reason + basis + approval); empty provenance is a hard error. The pass
traced 19 non-artifact records to ledger decisions (resolving the citation
text already present in rules and prohibitions) and moved 6 to visible
exceptions, all `approval: pending` owner ratification: the three
protocol-authored platform-controls fallbacks, wink's light-only, leader's
ruled-panel, and leader's selection. The enforcement caught a real finding:
leader `fallback/selection` restates decision L-12, which the Gate-2 review
LEFT UNDEFINED, yet the historical pack shipped it anyway - now
exception-backed with that history recorded (endorse L-12 into the ledger,
or convert the fallback into a case); dominion `prohibit/imagery-pictograms`
leaned on the likewise-undefined D-16 and now cites D-22 alone. Publication
is staged and validated (memory -> staging dir -> runtime pack-loader
validation -> per-file atomic `os.replace`; a failed validation publishes
nothing). Codify refuses a resubmission whose definition differs from the
published record for the same id (explicit conflict naming id, proposal and
differing fields - amend through a case) while identical resubmissions stay
silent no-ops. New gate `tools/compile_invariants.py` (wired into
`check.sh`): provenance coverage, trace validity, record shape via the
engine's own validator, reference integrity, a synthetic brand-new
authority compiled with zero engine edits, refusal-publishes-nothing, and
identical/conflicting re-codification. Compile parity baselines were
intentionally refreshed with exactly the provenance delta (verified
field-by-field before the refresh; artifacts, goldens, scoring and
manifests byte-identical; the P0.1-era baselines remain in history at
`3589d62`). Conformance at this change: compile parity OK (3/3 + 3/3) ·
compile invariants 146/146 (59 records: 53 decision-traced, 6
exception-backed) · kernel 34/34 · coverage sweep 134/134 · triage goldens
58/58 · synthesis goldens 18/18 · 14/14 · 17/17 · precedent probe 31/31 ·
dispute replay 4 standing (expected) · MCP smoke 25/25 · concept-site gate
PASS · semantic self-test OK. Kernel and the frozen surface untouched.

## D-029 · Reconciliation adopted — retroactive assessment of authority evolution (2026-10-11)

Owner capability memo adopted as `docs/14-reconciliation.md`. The system
gains its third question: when the authority evolves, what obligations does
that create for applications built under earlier versions? The principle is
fixed in the spec: authority evolves prospectively, its consequences may be
assessed retrospectively, historical decisions remain intact, current
implementations may require reconciliation.

The doctrine separates three concepts that are never conflated (precedent,
impact, migration policy). Transition policy becomes a property of the
approved decision (`transition` block: prospective | when_touched | required
| review; enforceable `required` must name its trigger `by`; `supersedes`
chains imply a record lifecycle). The sweep (`da sweep --from --to`) matches
deterministically first (recorded cases, and later decision receipts - 36 of
53 existing consumer stores already pin the build version they ran under) and
treats inferred matches as review candidates only (retrieval never
establishes authority, extended to impact matching). Findings classify as
conforms / grandfathered / rectify / review; grandfathering always preserves
reason and trigger, never "forever". Impact findings and migration decisions
attach to the Case lifecycle as reserved event kinds (`impact_finding`,
`migration_decision`) - no fifth lifecycle. Rigid boundary: publishing a
precedent triggers assessment, never automatic modification; changes ship as
new plans and builds under the target version with their own verification.
The four transition policies, report shape, receipt contents and
pre-registered acceptance criteria are in docs/14 sections 3-11.

Sequencing as the owner specified: implemented after P0.2 (Case model) and
P1.1 (project contract + decision receipts); placed as P1.4 in
docs/13-simplification.md. Open governance defaults left to the owner
(docs/14 section 10): the default transition policy for unannotated records,
receipt granularity, supersession lifecycle details, and the seat for
`review`-class migration decisions.

## D-030 · Reconciliation tightened; defaults set; first milestone = the Cadence lifecycle test (2026-10-11)

Owner review of docs/14 tightened four details before implementation:

- **`resolves_cases`** joins the transition block: a new decision links the
  previously unanswerable cases it resolves, so the sweep reaches affected
  applications through recorded cases rather than semantic matching (a
  superseded-records list cannot express a link to a need that had no
  record).
- **`applies_to` removed**: the policy determines applicability (prospective
  = new implementations only; when_touched / required / review = existing
  and new); narrower reach is an optional `scope` restriction. No
  contradictory combinations remain for the compiler to reject.
- **Findings carry trigger state**: a grandfathered when_touched finding
  records whether its trigger has occurred, so grandfathering cannot become
  permanent after its conditions expire.
- **Sweeps are idempotent**: finding identity = (application, decision,
  target version, assessed build revision); unchanged assessments reuse
  findings, re-assessments supersede them - reconciliation after every
  release adds signal, never duplicate noise.

Defaults set (docs/14 section 10): missing transition policy -> `review` for
legacy records while newly approved norms MUST carry an explicit policy
(compiler-enforced); receipts are one immutable file per published build with
a pointer to the latest.

Milestone directed: an end-to-end reconciliation lifecycle test on the
existing Cadence builds across wink/leader/dominion - undefined need ->
provisional implementation -> precedent established -> determination - to
test Design Authority as a system of persistent design governance rather
than its individual interfaces. Executed at prototype level on recorded
data, ahead of the full engine; write-up in
docs/experiments/07-reconciliation-cadence.md.

## D-031 · Reconciliation semantics tightened (tri-state trigger, obligation states); the closure cycle demonstrated (2026-10-11)

Owner review of the Cadence lifecycle test accepted the mechanism and asked
for three corrections, all landed in the spec and the prototype:

- **Trigger state is tri-state** (`occurred | not_occurred | unknown`, each
  with evidence): missing evidence is never treated as "not occurred";
  `unknown` is the honest default unless receipts cover the application's
  whole post-decision modification history. The two editorial slips in the
  experiment record were fixed in the same pass (twelve records, not eleven;
  one `review` row, not two).
- **Obligations carry state** (`scheduled | due | overdue | closed`): a
  `required` deadline after the target version is scheduled, never presented
  as already due; a later receipt with `migration_for` closes the obligation
  and the verification result rides along; the store keeps the superseded
  class/obligation as history.
- **The closure cycle was demanded and demonstrated.** A genuine next
  revision of the cadence-wink build (`examples/cadence-wink-r2/`, with the
  first prototype decision receipts, `prototype-0.1`): r2a modified the
  affected area (settings-save confirmation reworked; the canonical inline
  notice resolved but NOT adopted; deviation recorded in the receipt), and
  the sweep detected the trigger, ended the v1 permission, and put the
  obligation on r2a as due; r2b migrated the confirmation to
  `pattern/inline-notice` and was independently verified from the served DOM
  (8/8 checks: notice in flow, parsnip fill, rounded 12, bold lead + plain
  line, improvised save toast gone), and its receipt closed the obligation
  (verified: pass). Sweep stage 2: r2b conforms, r2a's obligation closed
  (`previous: due` retained), v1 unchanged. No operation wrote to any
  application tree. Full record: docs/experiments/07-reconciliation-cadence.md
  section 5; fixtures: docs/experiments/reconcile-cadence/closure/.

## D-032 · Reconciliation formalized: receipt confirmation, record-bound verification, policy validation, and the survival gate (2026-10-11)

Owner review round three accepted the closure lifecycle and directed
formalization instead of new capabilities; the concept boundaries are frozen
and the remaining work is integration (canonical Case records, formal
receipts, real transition policies, a consolidated API).

- **Receipts are confirmed, not trusted.** A separate confirmer
  (`examples/cadence-wink-r2/_evidence/confirm-receipts.py`) checks the
  r2a/r2b claims against source evidence: diffs show the modification
  confined to the claimed area (10 changed lines) and the migration (15
  changed lines), with hashes of the v1, r2a and r2b states; the r2a code
  state is committed as a snapshot so the claims stay confirmable from the
  repository. Findings that used receipt evidence carry
  `receipt_status: confirmed | unconfirmed`.
- **Verification is bound to the record.** The DOM verifier loads the record
  at runtime and records its hash (staleness is detectable), and discloses
  coverage against the record's own normative items: 9/9 checks, 3 of 4
  requirements mechanically covered, the copy register listed as a
  human-review item instead of being implied.
- **Transition policies are validated by the compiler.**
  `da_compile.validate_transition` enforces the docs/14 section-3 rules
  (policy enum; `by` if and only if `required`; list-typed links; exceptions
  enum); compile reports carry explicit/missing policy counts; the
  invariants gate exercises the validator against invalid combinations.
  Setting the REAL policies for the twelve records remains the owner's
  action - the machinery that receives them is ready.
- **The tested lifecycle is pinned.** `tools/reconcile_regression.py` (in
  `check.sh`) re-runs the sweeps from committed fixtures: pinned class
  counts, idempotency, chain-derived links, the legacy default, the full
  closure cycle, and evidence freshness (record-hash and build-hash binding;
  drift fails the gate and demands a fresh verifier run). 26 checks, no
  browser required.

Remaining owner actions: the real transition policies for the twelve records
and the disposition of the one `review` row. Remaining integration: Case
records (P0.2), formal receipts (P1.1), the consolidated interface (P1.2+).

## D-033 · Owner rulings on the decision page: exceptions ratified, L-12 endorsed, dominion platform-controls revised (2026-10-11)

The owner ruled all six exception-backed normative records on the
consolidated decision page (`workspaces/owner-decisions-0.6`, tailnet
:9120), all marked for the next release:

- Five authored exceptions ratified: wink `fallback/platform-controls` and
  `fallback/light-only`; leader `fallback/platform-controls`; leader
  `fallback/ruled-panel` (L-19 stays undefined by the owner's explicit
  call). Each dossier exception now carries the owner ruling in its
  `approval` field.
- Leader `fallback/selection`: the owner endorsed **L-12 into the approved
  ledger** (chosen over conversion to a case). L-12 joins the approved list
  and the record moves to the decision route (`compiled_from: [L-12]`);
  exception count across the three authorities drops 6 -> 5.
- Dominion `fallback/platform-controls`: **rejected as worded**; the owner
  directed that uncovered controls be themed in the system's own design
  language rather than plain platform defaults. The revision is applied
  (soft border, radius 4, blue glow focus; native semantics kept; mark and
  report), approved as owner-directed, for the next release.

Landed through the unified compiler: dossiers updated, all three
authorities recompiled (synthesis + codify) and deployed; parity baselines
refreshed with the verified delta (`fallbacks.json` per source,
field-by-field before the refresh); manifest entrypoints kept aligned with
the deployed contract (`precedents`/`candidates`, surfaced by the triage
template gate); the codify sources regained the deployed resolution aliases
and the derived golden cases so the re-emission reproduces the deployed
packs (verified field-by-field); the invariants gate pins 5 exception-backed
records of 59; the independent verifier was re-run for the record-hash
rebind (verdict pass, 9/9 checks).

## D-034 · Real transition policies set; the review row disposed; the sweep regenerated (2026-10-11)

Owner-set policies for the twelve cadence records (replacing the simulated
fixture mix): `required` by 0.3.0 for wink `pattern/destructive-confirm`
and `pattern/progress`; `review` for dominion `component/status`;
`prospective` for wink `pattern/empty-state`, leader
`pattern/data-readouts`, dominion `component/ledger` and
`component/notice`; `when_touched` for the remaining five. The `required`
deadline defaults to the next minor (0.3.0) - say the word to change it.

The single review row (cadence3-wink · `pattern/inline-notice`) is disposed
as pending work: adopt at the next revision of cadence3-wink; the review
seat is the owner; the finding stays as the feed for the reserved Case
events (P0.2).

The reconcile fixtures were rebuilt as the live packs + recorded links +
the real policies, and the sweep regenerated: **36 findings = 10 conforms ·
18 grandfathered · 4 rectify · 4 review** with 4 `scheduled` obligations
(pre-ruling simulated mix: 10 · 22 · 3 · 1, 3 obligations). The defaults
run is unchanged (10 + 26 review). Pins updated; reconcile regression 26/26;
full check suite green.

## D-035 · Triage proposal rulings: three advance to merge; theme profiles rejected (2026-10-11)

- **Theme profiles: rejected.** Forks remain the answer; brand stays
  Geist-first. No theme-file mechanism; the proposal closes with the
  owner's direction recorded.
- **Verification levels, density and borders, provenance contract: advance
  to merge** through the Triage repository's normal review route; the
  Level-4 experiment is scheduled after the 0.6 line.
- The 0.6 scope card was confirmed unchanged.

## D-036 · Publication is a journaled transaction (2026-10-11)

The owner's memo flagged one publication detail: the compiler validated a
staging directory but then replaced individual files through os.replace, so
the multi-file publication was not atomic as a whole. Addressed:

- Publication now runs under a journal (`.da-publish-journal.json` plus a
  `.da-publish-backup/` set inside the target): pre-publish bytes are backed
  up, every replacement stays atomic, and the published pack is re-validated
  from disk before the journal clears. A failed write rolls back in-run; a
  hard kill mid-publish leaves the journal, and the very next run rolls the
  interrupted release back before publishing (recovery) - a torn pack
  cannot silently serve.
- The invariants gate grew the publication checks (hard-kill recovery,
  rollback-to-previous on failure, no debris): 164 checks, 0 failed. A
  real-data re-publish through the new path is a byte no-op (authority repo
  status clean, no debris). The triage pack was regenerated for its source
  snapshot rebind (owner-annotation commit); content unchanged.
- The remaining window is bounded to the replace loop itself (milliseconds);
  a fully versioned release layout with a single-reference switch remains
  the recorded follow-up, stated in the compiler's contract.

## D-037 · The Case read model lands: one interface over the record stores (2026-10-11)

P1 of the owner's next-steps memo, implemented exactly as directed: the
canonical Case model is a normalized, append-only EVENT VIEW over the
existing stores, no new storage system, no migration until the read model
is proven against the corpus.

- `tools/da_case.py` (spec: `docs/16-case-read-model.md`): `list` / `show
  <gap|dispute|prop id>` / `why <record id>`. Every event names its source
  file and record; only recorded fields appear; output is deterministic and
  the tool is read-only, so existing resolution behavior cannot change.
- Corpus coverage at landing, through the one interface: **173 unique gaps**
  (217 store occurrences across 61 stores, one case row per id), **4
  disputes**, **24 proposals**, **38 reconciliation findings**, **2
  receipts**; every finding attaches to a case and every proposal resolves
  through its gap thread. The lifecycle reads end to end: report ->
  evidence -> proposal -> review -> publication -> impact ->
  migration_required -> migration_verified -> obligation_closed, with
  reasons, rejected alternatives and receipts.
- Gate: `tools/check_case_model.py` pins the model inside `check.sh` (20
  checks): the corpus is re-derived independently of the tool, every
  proposal/dispute is retrievable, the golden threads are pinned (the
  destructive-confirm chain; the closure cycle with its verified close),
  every event references a live source, the vocabulary is closed, output is
  deterministic.
- Reserved, as documented: case numbering (`case/NNNN`), first-class
  recorded events (`impact_finding`, `migration_decision`) and the
  compatibility adapters land with the 0.6 integration freeze. Sealed
  experiment materials and evidence copies are excluded from the corpus
  (stated in the spec, not silently skipped).
- This marks the 0.6 specification boundary (memo section 2). Next per the
  roadmap: the P1.1/P1.2 vertical slice (plan / verify / receipts through
  the runtime API), then the fresh-agent public adoption test.

## D-038 · The consumer workflow lands end to end; transition policies enter the record layer (2026-10-11)

The memo's vertical slice (P1.1 + P1.2 implemented together) is shipped on
the one runtime library. Spec: `docs/17-consumer-workflow.md`.

- **New public commands** (kernel + CLI, stdlib-only): `da init` pins the
  authority into `.design-authority/authority.lock.json` (id, version,
  commit, pack fingerprint); `da plan BRIEF.md` resolves every brief need
  against the pinned pack, REFUSES on any citation that does not exist, and
  writes the plan plus case stubs for unresolved needs; `da receipt-new` /
  `da receipt-check` formalize the outcome receipts (format 0.2:
  decisions_applied, unresolved_needs, provisional_solutions, deviations,
  areas_modified, migration_for, verification ref); `da verify` is the
  runtime-API alias over the independent verifier; `da reconcile` assesses a
  built workspace and writes a deterministic, portable migration plan.
- **The engine consumes the receipt** (the memo's requirement): receipt-
  claimed decisions scope the sweep for consumer workspaces (chain links
  keep precedence for the recorded corpus), and deviations remove claims
  from adoption, so a recorded deviation on a decision surfaces as a
  rectify row with a due obligation. Version comparisons tolerate rc labels.
- **Transition policies entered the record layer**: the owner-set policies
  (D-034) now ship WITH the packs. Codify carries `transition` from the
  proposals into published records, validates it, and compares it for
  conflicts; wink/leader/dominion were recompiled and redeployed at
  **0.3.0-rc1** (agent-produced bumps carry rc labels per the release
  policy; promotion is a human action). Parity baselines refreshed with the
  verified deltas (transitions + versions only); the closure verifier was
  re-run for its record-hash rebind (9/9 pass).
- **End-to-end acceptance** (`examples/wink-notes/`, the acceptance
  vehicle): brief with 5 needs -> plan (4 resolved, 1 undefined with case
  stub) -> build (recorded values; the toast improvisation marked and a gap
  filed) -> receipt v1 -> independent verification 19 PASS / 1 VIOLATION
  (the declared toast, W-15) / 14 honest exemptions -> reconcile 3 conforms
  + 1 rectify (the deviation produces the due migration obligation).
  `tools/check_project_flow.py` (35 checks) pins the whole flow inside
  `check.sh`, including receipt discipline and the deployed record layer.
- Full check suite green. Next per the roadmap: the fresh-agent public
  adoption test (P3), the longitudinal experiment design (P4), and the
  queued consolidations (recipes promotion, Triage merges).

## D-039 · Adoption test passed; the validator goes portable; program follow-through (2026-10-11)

The independent adoption test (memo section 4) ran and passed its axes;
the same-day fixes and the remaining program items:

- **The test** (`docs/experiments/08-adoption-test.md`; runner
  `x06_run.py`, sandboxed, brief-only, public repo only; run archived at
  `~/x06-adoption/run1/`): a fresh agent found and ran the WHOLE workflow
  unprompted — init, plan (9 resolved / 3 undefined), build on the shipped
  foundations, receipt, reconcile (9 conforms) — filed five gaps, handled
  every undefined need by the prescribed protocol (marked improvisations,
  including an in-character confetti burst with reduced-motion), and
  verified with real browser checks. Claims independently re-verified; zero
  human intervention; zero containment hits.
- **Fix landed (F-1):** the pack's declared lint validator was bound to the
  non-public design-system checkout. The Triage pack now ships a
  self-contained lint bundle and runs it with `workdir {pack}`; the
  generator emits it and the drift gate covers it. Verified from a copied
  pack with no snapshot: the adoption build re-checks at 0 violations /
  score 100 against the real lint.
- **Queued from the test (F-2):** the Triage pack needs a verification
  contract (the `da verify` step). Author + calibrate under
  references/verification.md discipline; the run's gap records it.
- **x05 program report** written (05-seed-evolution.md section 11):
  blind review, objective gates (D1/D2 fail, flat Layer 1), the hollow
  enforcement finding and its rebuild, the exploratory drift sweep, limits.
- **Recipes promotion review** (memo section 6): all 17 evolution recipes
  evaluated against the live pack — 10 promote directly, 6 with a named
  prerequisite record, 1 needs naming reconciliation; queued to the Triage
  review route as bundles, never bulk-copied.
- **P4 designed:** `docs/experiments/09-maintenance-economics.md`, the
  draft pre-registration for the next experiment (maintenance economics of
  governed precedent); frozen only on the owner's go.
- Everything committed and pushed; full check suite green.

## D-040 · The three approved Triage proposals merged; pack 0.13.0-rc1 (2026-10-11)

The owner said "keep going, all approved"; the three proposals the owner
advanced to merge landed in the Triage repo, and the pack followed:

- **density-borders (repo 0.12.2):** label-role sizes raised
  (`size-badge` / `size-nav-label` 12px -> 13px; compact 0.8125rem,
  proportional at the 15px root); new lint rule **TDS016 label-tier**
  (info) with unit tests; border discipline documented in INTERACTION.md
  (three rules + checklist item 9); UI baseline + exports regenerated
  deliberately.
- **verification-levels:** **VERIFICATION.md** — the four-level conformance
  ladder and the four-part traceability contract (rule id · component ·
  location · evidence; a score is a gate, never evidence); `evidence`
  declarations added to `spec/states.json` (L1 for all; L2 browser test ids
  where fixtures exist; undeclared = labelled unverified).
- **provenance-contract (repo 0.13.0):** new component **`.prov`** (beta) —
  the machine-action record with eight required fields, addressable by id,
  explanation folded and labelled supplementary; live usage in
  `examples/viewer.html`; caught and fixed a 320px/200% responsive blowout
  via the layout fixture before landing.
- **Pack cut `0.13.0-rc1`** (rc per release policy): 81 artifacts (+prov),
  20 rules (+TDS016), goldens 58/58, coverage 134/134; consumer lint bundle
  and dist foundations refreshed to the 0.13.0 snapshot; drift gate covers
  the bundle.
- **Resolver ripple, verified not suppressed:** two of four standing
  disputes (panel slide-over; state-label query) now resolve UNDEFINED —
  the new `.prov` artifact reshuffled candidate competition and no wrong
  claim reproduces; the regression pin moved 4 -> 2 with the reason
  recorded in `tools/check.sh`; the product gaps remain with the disputes.
- Kernel count fixtures, MCP smoke pins, README numbers and the concept
  site's byte-identical foundations all refreshed; full `tools/check.sh`
  green.

