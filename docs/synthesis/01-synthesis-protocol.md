# Synthesis · 01 · Common synthesis protocol (Phase 2)

One procedure for all three sources. Source-specific deviations are permitted
only if recorded here with reasons. The protocol extends the portability
phase's discipline (`docs/portability/03-kernel-change-ledger.md`,
`08-contamination-audit.md`).

## Roles

- **Machine (synthesis):** evidence capture, gestalt modelling, semantic
  derivation, compilation, CI, probes, metrics. Each source's derivation runs
  in an **isolated context** (separate subagent workstream where useful); the
  orchestrator assembles and never mixes one source's evidence into another's
  derivation.
- **Human (reviewer):** the three gates only — Gestalt (G1), Semantics (G2),
  Reference build (G3). Judgment, not schema work: no JSON/YAML written by
  the reviewer, ever.

## Stage table

| # | stage | input | output (path) |
|---|---|---|---|
| 1 | Source ingestion | public pages/docs (fresh fetches) | raw notes (session; cited in inventory) |
| 2 | Evidence inventory | raw notes | `docs/synthesis/<src>/00-evidence-inventory.md` |
| 3 | Gestalt model | inventory | principles + character + tile (`01-gestalt.md`, `tile/`) |
| G1 | **Gestalt review** | tile + gestalt + 4 questions | verdict + corrections recorded in `01-gestalt.md` |
| 4 | Foundation inference | approved gestalt | decisions (status/evidence/confidence/alternatives) |
| 5 | Interface semantics | decisions + reference-app needs | decision set for review |
| G2 | **Semantic review** | grouped decisions | `02-semantic-review.md` (ACCEPT/REJECT/MODIFY/UNDEFINED) |
| 6 | Compile authority | accepted decisions | `packs/<name>/` (via compile script) |
| 7 | Authority CI | pack | validator (3–6 distinctive checks) + golden |
| 8 | Reference build | common brief + pack | `examples/<name>-reference-app/` + agent run |
| G3 | **Reference review** | running app + captures | `03-reference-review.md` |
| 9 | Polarity probes | all packs | `docs/synthesis/02-cross-authority-probes.md` |
| 10 | Metrics + leakage | all of the above | `04-final-report.md` (+ `03-kernel-change-ledger.md`) |

## Evidence rules

- Every observation carries `OBSERVED` / `INFERRED` / `AUTHORED` / `UNDEFINED`.
  Stage 2 prefers `OBSERVED` + `UNDEFINED`; no operationalizing early.
- Every semantic decision ships as: **Decision · Status · Evidence ·
  Confidence · Reasoning · Alternatives · Human-confirmation-required**.
  Weak evidence → `UNDEFINED`, not filler.
- Provenance: cite the URL (and page/section where applicable) for each
  observed fact cluster.

## Gate formats (what the reviewer sees)

- **G1:** the tile (rendered PNG + HTML/CSS) + a 1-page gestalt summary (5–10
  principles, color/type/shape/density/surface/imagery/motion character, and
  "what this system avoids"). Reviewer answers the protocol's 4 questions and
  gives APPROVE / REVISE / REJECT; corrections are logged verbatim.
- **G2:** decisions grouped as high-confidence observed · high-confidence
  inferred · low-confidence inferred · authored · undefined. Per uncertain
  decision: ACCEPT / REJECT / MODIFY / LEAVE UNDEFINED. Presented as a single
  review page per source (rendered HTML for convenience), not raw schema.
- **G3:** the running reference app (screens + flows) + captures; reviewer
  answers the protocol's 5 questions; verdict APPROVE / REVISE AUTHORITY /
  REJECT SYNTHESIS.

## Quarantine (extends `docs/portability/08`)

- Fresh source fetches only; never read Triage/Indaba CSS in derivation
  contexts; the source's own visuals are the only style evidence.
- No Triage-content skills, no memory house-style directives in derivation
  contexts (explicitly scoped out); curator-distilled notes are project
  memory, never source input.
- Subagent prompts are source-positive (“derive X's grammar”), never
  “avoid the incumbent” — negative priming is a leak channel too.
- Reference systems (Triage/Indaba) appear only in *kernel compatibility and
  probe* contexts, stated as such.

## Machine-heavy commitment

- The compile step (stage 6) is a **script** over accepted decisions
  (`tools/build_pack_synthesis.py`): decisions file → pack JSON. No manual
  schema authoring. If a decision cannot be compiled without judgment, it
  stays out of the pack or goes back to G2 — never silently authored.
- Evidence and gestalt documents use a fixed section template so the
  inventory → gestalt → decisions chain is largely mechanical for the
  machine side.
- Cost/time captured per stage per source (same tracker as `fe341e3`).

## Reference application (stage 8)

**Reuse the Depot brief** (equipment-lending register) for all three: same
product semantics, only the authority changes. Depot already exercises
navigation, repeated content, a form, status, one destructive action,
feedback/progress, responsive layout, and one deliberately underspecified
requirement (borrower selection at scale). Starter, harness and interact
suite are authority-tolerant (see skill lessons). One starter per authority
under `examples/<name>-reference-app/`.

## Deviations log

| source | deviation | reason |
|---|---|---|
| — | none yet | — |
