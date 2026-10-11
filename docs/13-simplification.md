# Design Authority — simplification plan (P0–P2)

**Status:** working plan. P0.1 is executed (section 5). Everything else is
staged below for review. Baseline for the findings: commit `3eb576a`, before
any of this landed.

## 0 · Context

Owner review (2026-10-11, against the public repo and the concept site): the
individual pieces have recognizable purposes, but together they read as
research projects that gradually became a platform, because there is no
single organizing abstraction. The adopted direction is to reorganize around
one:

> Design Authority is a **compiler for governed design decisions**, with a
> small runtime that agents use to apply and verify them.

Evidence produces decisions. Approved decisions compile into authority.
Agents consume authority. Deviations produce new evidence. Extraction,
compilation, resolution and verification are not separate products; they are
stages operating on the same model. The central principle is unchanged and
load-bearing: **agents may improvise; they may not confuse improvisation with
authority.**

This document verifies the review's claims against the code (section 1),
fixes the target shape (sections 2 and 3), and stages the work (section 4).
It is written to be reviewed before further large implementation starts;
section 5 records what already landed.

## 1 · Verified findings

Each review claim, checked against the code at `3eb576a`:

**Data model — separate storage and handling per record type.**
The pack loader reads artifacts, rules, recipes, fallbacks, prohibitions,
validators, precedents and candidates through separate paths with separate
shapes (`kernel/design_authority/pack.py:72-99`); the workspace side has
three more shapes: gaps, proposals, disputes with three lifecycles
(`kernel/design_authority/records.py:29, 79, 190`). Confirmed; the change is
one record envelope with typed payloads (section 3).

**Decision lifecycle — four workflows for one concept.**
Synthesis gate verdicts live in a review app's `feedback.json`
(`docs/synthesis/tools/compile_pack.py@3eb576a:27-40`); proposal verdicts in
workspace records (`records.py:166`); adjudication declines in
`precedents.json`; disputes in `disputes.jsonl` with their own
open/accepted/rejected states (`records.py:236`). Confirmed; the change is
one Case lifecycle (section 4, P0.2).

**Compilation — two mechanisms for one operation.**
"Approved decision -> authoritative record" is implemented twice:
`compile_pack.py` (552 lines, hardcoded `build_wink()`/`build_leader()`/
`build_dominion()` at lines 92/206/330, reading one review app's feedback
file) and `apply_proposals.py` (179 lines, a merge loop plus a hardcoded
`SUMMARY` dict keyed by eleven historical proposal ids, lines 56-71). Two
further builders exist for other inputs: `build_triage_pack.py` (spec-first
conversion, 741 lines) and `build_pack_triage.py` (curation-based, in the
frozen surface). Confirmed. P0.1 (section 5) unified the first two; the
other two are convergence targets (section 4, P1.3).

**Tooling — broad surface, and verification outside the runtime.**
14 MCP tools (`mcp_server.py`, counted) and 17 CLI subcommands (`cli.py`,
counted) front the same library, which is good in principle; but independent
verification is a separate engine (`tools/da_verify.py`, 1,166 lines) reached
mainly through its own CLI, and compilation is not reachable through the
library at all. The change is a small public API with CLI/MCP as adapters
(section 3).

**Repository organization.** Product code (`kernel/`, `tools/`), synthesis
tooling, the benchmark, governance experiments, authority repos and sites all
share one tree; `authorities/README.md:56-63` itself records the remaining
consolidation as open ("Phase 2"). Confirmed; staged in P1.3.

**Documentation drift (minor, characteristic).** The frozen 0.5 spec's
conformance section still says 0.3 (`docs/spec/00-index.md:65`); the
interfaces doc still points at `packs/triage` (`docs/spec/04-interfaces.md:55`);
the `VERSION` file stalled at `0.3.0` while the spec and README declare
0.5.0. Fold into the next freeze (P0.3), except `VERSION`, which is not in
the frozen manifest and is aligned now.

## 2 · The organizing idea (adopted)

- **One compiler.** Approved source decisions are the only input that
  produces authority; the same generic mechanism compiles all authorities.
  Authority-specific definitions are reviewed data, not code in a compiler.
- **One runtime.** Resolution, search, verification and case recording are
  one library; CLI, MCP and future interfaces are adapters over it.
- **One lifecycle.** Gaps, proposals, disputes, verdicts and published
  precedents are one Case concept with events, not five workflows.
- **Runtime observations return as reviewable cases** and never change
  authority directly. Published authority is immutable to consumers.
- **Keep:** deterministic-first resolution; retrieval never establishes
  authority; golden sets as the contract; the thin kernel; the spec
  change-control (semantic change = minor bump + fresh freeze, editorial =
  patch). The frozen 0.5 surface is not touched by P0.1.

## 3 · Target architecture (staged)

Layout, from the review adapted to the current repo (the authority repos
stay separate repos; they version independently):

    design-authority/                     # the engine, installable
    ├── src/design_authority/
    │   ├── model/        Norm records (envelope + typed payloads), Case, Evidence
    │   ├── compile/      Decisions -> release (the unified compiler)
    │   ├── runtime/      Resolve, search, plan
    │   ├── verify/       Verification engine (da_verify core)
    │   ├── governance/   Cases, review, publish
    │   └── adapters/     CLI, MCP
    ├── schemas/  tests/  skills/  examples/
    └── docs/ {guide, spec, research}

    authorities/<name>/                   # separate repos, unchanged in kind
    ├── source/           reviewed inputs (decisions, dossiers, cases)
    ├── <records>.json    the published pack (kept at root for now)
    ├── site/             generated catalogue + receipts
    └── CHANGELOG.md

Two notes on this shape. First, `src/` vs `kernel/`: the current
`kernel/design_authority/` package becomes the `model/`+`runtime/` core of
the new package when P1.3 lands, which is a spec-touching move and gets its
own freeze. Second, the review's sketch shows the generated pack under
`dist/`; today records sit at the repo root and roughly a dozen surfaces read
them (bootstrap, gallery discovery, CI, review app, da.py defaults), so a
`dist/` move is a coordinated migration rather than a rename; decided in
P1.3, flagged in section 6.

**The record envelope** (P0.2, when it lands): one envelope for every
authoritative record, with a typed payload for behavior:

    id: component/action-button
    type: component          # component | guideline | recipe | prohibition | rule | fallback
    title: Primary action button
    scope: {domain: actions}
    contract: {...}          # the type-specific payload
    evidence: [evidence refs]
    verification: [check refs]
    provenance: {case: case/0042, introduced_in: 0.3.0}

The current files keep their shapes until the envelope work lands; a
compatibility layer reads both. Published norms and unapproved cases stay
physically distinct (they already are: pack vs workspace; that distinction is
kept).

**The Case** (P0.2): `{id, kind, question, subject_refs, events[], status}`,
where a gap, a disputed resolution, a proposal and a review verdict are all
*events* on a case rather than sibling record types. First implemented as a
canonical view over the existing workspace files (zero migration), with
adapters; storage changes only if authority-side case pages need more. The
event vocabulary reserves the reconciliation events (`impact_finding`,
`migration_decision`; docs/14) so retroactive assessment attaches to the same
lifecycle instead of founding another.

**Interfaces** (P1.1/P1.2): `plan` / `resolve` / `verify` / `case` as the
public operations; `review` / `publish` stay human-side. MCP, CLI, and any
web surface call the same functions. Existing tools keep working as aliases
while the transition runs.

## 4 · Phased plan

Owner priorities, kept as given, with the gate for each phase.

| Phase | Change | Gate |
|---|---|---|
| **P0.1** | One generic compile path replacing source-specific compilation and proposal application | **DONE** (section 5, two passes): parity fixtures byte-compare both mechanisms; shared emission invariants + governance gate; check.sh green |
| **P0.2** | Canonical Case model with compatibility adapters | Existing surfaces unchanged; dispute replay + goldens + kernel tests green; freeze 0.6.0 only after a stability window |
| **P0.3** | Documentation drift folded into the next freeze (`00-index` conformance text, `04-interfaces` paths); VERSION aligned now | Freeze ritual when 0.6.0 lands |
| **P1.1** | Batch planning: `da plan` producing a version-pinned project contract (`.design-authority/authority.lock.json`, `design-plan.json`, `cases/`, `verification/`) and the decision receipts (intent + outcome; docs/14 §5) | Plan validation = every cited norm exists; resolve-only workflow unaffected |
| **P1.2** | Independent verification consolidated under the runtime API (`da_verify` core behind the library; contracts unchanged) | Contract matrix in meta CI stays green; consumer `verify.map.json` flow unchanged |
| **P1.3** | Finish separation: dossiers -> `authorities/<auth>/source/`; Phase-2 moves (synthesis tiles, cadence builds, audit console, font route); converge `build_pack_triage.py` (curation -> dossier adapter) | Per-authority CI + meta integration gates; route rewiring verified live |
| **P1.4** | Reconciliation (docs/14): `transition` policy on records, `da sweep` (deterministic + inferred impact), `da reconcile` (migration plan + case events); assessment never auto-modifies | Depends on P0.2 + P1.1 receipts; docs/14 §11 pre-registered criteria; sweep writes nothing to application trees |
| **P2.1** | `da init --authority <name>`; single install; CLI-only parity (no MCP required) | Fresh-machine acceptance test, agent-completable, like the current Use-now flow |
| **P2.2** | Generated documentation and case timelines from canonical records | Docs regenerate from records; drift classes gone; concept-site copy re-checked |

Deliberately *not* in scope: collapsing authority repos into a monorepo
(independent versioning is useful), changing resolution semantics, and any
kernel change before its freeze.

## 5 · Executed: P0.1 — one decision-to-authority compiler

What landed (all in this repo; authority repos untouched):

- **`tools/da_compile.py` (338 lines)** — the single compiler. Two modes
  over one emit core: `synthesis` (authority dossier -> full pack) and
  `codify` (accepted proposals merged into a pack). Hard rules: only
  approved decisions compile (an unapproved or unknown reference is refused);
  summaries are never invented (decision text, or the review's recorded
  `codified_summary`, or the proposal's own fields); every record carries
  `compiled_from` provenance; codify is idempotent.
- **Dossiers as reviewed data** — `docs/synthesis/{wink,leader,dominion}/compile.json`
  (609/672/613 lines): the approved decision ledger plus the records those
  decisions emit, extracted mechanically from the old builders. The
  Wink/Leader/Dominion definitions no longer exist in any compiler's Python.
- **`compile_pack.py` 552 -> 36 lines** and **`apply_proposals.py` 179 -> 38
  lines**: both are thin adapters now, CLI-compatible, delegating to
  `da_compile`. 715 lines of hardcoded definitions left the tool code.
- **The `SUMMARY` dict is gone.** The eleven editorial summaries were
  migrated into the proposal records they describe
  (`review.codified_summary` on `examples/cadence-{wink,leader,dominion}`
  proposals), so the summary travels with the decision it summarizes, and
  future codifications read it from the record.
- **Parity fixtures + gate** — `docs/synthesis/data/parity/` holds baselines
  captured from the pre-unification tools; `tools/compile_parity.py`
  re-compiles through the new engine and byte-compares; wired into
  `tools/check.sh`. Parity is **not** self-referential: the baselines were
  produced by the old implementations, the gate proves the new one matches.

Evidence (all run 2026-10-11):

- `compile parity: OK (compile 3/3 sources · codify 3/3 workspaces)` — 24
  compile files and 3 codify merges byte-identical to the pre-unification
  outputs (codify compared with its recorded `codified_at` injected; without
  injection the only delta is that timestamp, by design).
- `check.sh` green: triage pack drift in sync (10 files) · coverage sweep
  134/134 · kernel 34/34 · triage goldens 58/58 · synthesis goldens 18/18,
  14/14, 17/17 · precedent probe 31/31 · dispute replay 4 standing (expected)
  · MCP smoke 25/25 · concept-site gate PASS · semantic self-test OK.
- The shims were exercised end-to-end: `compile_pack.py --src wink` output is
  byte-identical to the baseline; `apply_proposals.py` on the cadence-wink
  workspace re-applies the same five proposals with the same report.

What P0.1 deliberately did **not** change: the kernel (frozen), the triage
and evolution builders (frozen / spec-first, converge in P1.3), live authority
repos (regeneration only happens when explicitly run), and any pack content.

### P0.1b — shared emission invariants and publication hardening (review-driven, same day)

The owner's code review of P0.1 found the unification stopped at the entry
points (synthesis built whole packs; codify built records) and that
non-artifact records could compile with empty provenance
(`"decisions": []`). Parity had proved "no accidental drift", not "the
output satisfies the governance invariants". Fixed in a second pass:

- **One emission function through both modes.** `_finalize_record` is now
  the only path a record takes to disk, in either mode; it attaches
  provenance uniformly and validates record type, required fields and
  provenance. `validate_record` and `validate_provenance` are public, so the
  invariants gate and the compiler cannot drift apart.
- **Provenance is universal.** Every normative record carries either
  `compiled_from` (approved decisions) or an explicit `exception` block
  (reason + basis + approval status). Empty provenance is a hard error; the
  old silent `"decisions": []` no longer compiles. The pass traced 19
  non-artifact records to ledger decisions (resolving the existing citation
  text in rules and prohibitions) and moved 6 to visible exceptions:
  - wink `fallback/platform-controls`, `fallback/light-only`
  - leader `fallback/platform-controls`, `fallback/selection`, `fallback/ruled-panel`
  - dominion `fallback/platform-controls`
  (all `approval: pending`; see open question 7.)
- **A real finding, caught by the new enforcement.** Leader
  `fallback/selection` restates decision `L-12`, which the Gate-2 review
  left undefined, yet the historical pack shipped it anyway; it is now
  exception-backed with that history recorded (endorse L-12 into the ledger,
  or convert the fallback into a case). Dominion
  `prohibit/imagery-pictograms` leaned on the similarly-undefined `D-16` and
  now cites `D-22` alone.
- **Publication is staged and validated.** Builds happen in memory, land in
  a staging directory, load through the runtime's own pack loader, and only
  then are the files atomically replaced (one `os.replace` per file). A
  validation failure publishes nothing.
- **Conflicting codification is refused.** An identical resubmission stays
  a silent no-op (idempotent); a resubmission whose definition differs from
  the published record for the same id raises an explicit conflict naming
  the id, the proposal and the differing fields - amend through a case, not
  a second submission. Nothing is written on conflict.
- **New gate** `tools/compile_invariants.py` (wired into `check.sh`):
  provenance coverage and trace validity against the approved ledger,
  record shape via the engine's own validator, reference integrity
  (prohibition -> rule; recipe ingredients), a synthetic brand-new authority
  compiled with zero engine edits (the review's acceptance test 1), refusal
  publishes nothing, and identical/conflicting re-codification behaviour
  (acceptance test 2 is the trace rule itself; test 3, one Case interface,
  is P0.2).

Evidence: compile baselines intentionally refreshed with exactly the
provenance delta (verified field-by-field before the refresh: records change
only by `source` + `compiled_from`, or `source` + `exception`; artifacts,
goldens, scoring and manifests byte-identical; P0.1-era baselines remain in
git history at `3589d62`); `compile parity: OK (3/3 + 3/3)`; `compile
invariants: 146 passed, 0 failed (59 records: 53 decision-traced, 6
exception-backed)`; full `check.sh` green.

## 6 · Open questions for the owner

1. **Dossier home.** The definitions are reviewed data now, but still live
   in the meta repo (`docs/synthesis/<src>/compile.json`). Moving them to
   `authorities/<name>/source/` is the natural finishing step (the review's
   sketch); it needs commits in each authority repo, so it is staged at
   P1.3 with the other Phase-2 moves. Say the word to bump it earlier.
2. **`dist/` for the generated pack.** Moving records from authority-repo
   root to `dist/` touches about a dozen read surfaces; recommended to happen
   once, in P1.3, as a coordinated migration with CI and app routing updated
   in the same change. Alternative: keep records at root and treat the repo
   root as the distribution.
3. **Freeze mechanics.** The editorial spec fixes (0.3 -> 0.5 conformance
   text; `packs/` paths) are staged for the 0.6.0 freeze that P0.2's record
   work requires. If a patch-level 0.5.1 re-freeze is preferred now, it is a
   small ritual on its own.
4. **Engine placement.** `tools/da_compile.py` is outside the frozen
   surface, deliberately. It moves into the package (`compile/`) with the
   P1.3 layout change, at which point it enters the frozen surface through
   the normal freeze.
5. **Case storage.** Recommend implementing Case first as a canonical view
   over the existing workspace records (gaps/proposals/disputes), zero
   migration, then deciding on dedicated storage when authority-side case
   pages become real.
6. **Positioning.** The review's final point stands: the defensible claim is
   *persistent, inspectable design judgment across independent agents and
   successive product generations*, not that first-pass visual quality
   improves because of the governance layer. Concept-site and README copy
   audited against that distinction in P2.2.
7. **Ratify the six exception-backed records** (listed in section 5). Three
   are the same protocol-authored platform-controls fallback; the leader two
   carry findings (`L-12` left undefined; the ruled-panel premise vs the
   never-endorsed dialog decision `L-19`). Ratify them as authored policy,
   or supply ledger decisions to map them.
8. **Reconciliation defaults.** The default transition policy for
   unannotated records and the receipt granularity (docs/14 section 10) are
   the two governance defaults staged for your ruling; everything else in
   docs/14 is specified and resolvable at implementation time.

## 7 · Gates applied to every change

Per the review's closing requirement, each phase runs the existing suites
before replacing anything old: `tools/check.sh` (pack drift, coverage sweep,
kernel tests, goldens, compile parity, compile invariants, precedent probe,
dispute replay, MCP smoke, concept-site gate, semantic self-test), plus
phase-specific fixtures (evolution convergence battery when records or
curation change; the verification contract matrix when the verify engine
moves). No behaviour change ships without a fixture that would catch its
reversal.

## References

- Reviews this plan responds to: owner memo 2026-10-11 (D-027); owner code
  review of P0.1, 2026-10-11 (D-028, section 5 P0.1b); owner capability memo
  on reconciliation, 2026-10-11 (D-029, `docs/14-reconciliation.md`).
- P0.1 code: `tools/da_compile.py`, `tools/compile_parity.py`,
  `tools/compile_invariants.py`, `docs/synthesis/data/parity/`, dossiers
  under `docs/synthesis/<src>/compile.json`.
- Frozen surface and change control: `docs/spec/05-governance-and-freeze.md`.
- Remaining consolidation items: `authorities/README.md` (Phase 2).
