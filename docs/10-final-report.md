# Design Authority — final report

**Project:** Triage Design Authority prototype + controlled experiment
**Date:** 2026-10-07 · **Status:** complete (D1–D5 measured, blind review done)
**Repo:** `github.com/vjsyong/design-authority` (private) · **Pinned reference:**
Triage 0.12.1 @ `e374f38`

---

## 0 · TL;DR

We built a kit-agnostic **Design Authority** (versioned machine-readable
contract + resolution engine + MCP interface + gap/proposal loop) for the
Triage design system, then ran a controlled experiment: 3 conditions × 3 runs,
one coding agent, identical briefs.

**The answer to the research question:** compared with no design material,
design documentation improves an agent's frontend output *massively and
consistently*. Compared with a **well-made static kit**, an active authority
does **not** materially improve the one-shot *appearance* of the output — the
kit captures that. The authority's measured improvement is one layer up:
**governability** (every decision traceable, no silent canon, sanctioned
fallbacks) and **closed-loop discovery** (6 gaps + 3 proposals filed by the
agents, two confirmed documentation holes found independently by multiple
runs). No quality ceiling: the best build in the whole set was
authority-guided (25/25, blind).

---

## 1 · What was built

- **Authority pack (Triage v0.12.1):** 73 artifacts · 15 rules · 15 recipes ·
  3 sanctioned fallbacks · 9 prohibitions, machine-readable, built by a
  deterministic compiler from the pinned Triage repo with a drift gate.
- **Kernel (kit-agnostic):** resolution order CONFLICT → RESOLVED → COMPOSE →
  FALLBACK → UNDEFINED; every answer cites pack IDs; UNDEFINED is a
  structured success; constraints/scoring externalised per pack. stdlib-first
  Python, no database. 10/10 unit tests, 19/19 golden queries.
- **MCP interface (the "active" layer):** 7 tools — overview, search,
  inspect, resolve, validate, report_gap, propose_extension. 17/17 smoke
  tests; live in both Hermes and opencode.
- **Extension loop:** proposal → review → planned/published, exercised
  end-to-end before the experiment.

## 2 · The experiment

**Question (pre-registered, docs/06):** does an active, queryable, enforceable
authority improve an agent's frontend output vs ordinary design documentation?

- **Conditions:** **A** naive (no design material) · **B** passive static kit
  (DESIGN.md + rendered kit, no interface) · **C** active authority (MCP).
- **App:** "Procura" procurement UI, frozen starter (baseline lint: 10
  findings; all compliance measured as delta vs pristine starter).
- **Agent:** opencode + `deepseek/deepseek-flash`, pinned. Briefs identical
  across conditions (13 deliverable checks; no hints about rules or tools).
- **Containment (hard requirement, D-020):** every run executed in a
  bubblewrap sandbox (no host access, no cross-run access, no benchmark
  access), isolated `XDG_CONFIG_HOME`, strict tool permissions, plus a
  transcript audit (`refs_outside` counter). All production runs clean.
- **Instruments frozen** before execution: lint (D1), drift scan (D2),
  authority interaction logs (D3), functional/engineering probes (D4), blind
  human review (D5). Per-dimension results only — no composite score.
- **Execution note:** pilot (a1/b1/c1) validated the harness and led to
  containment/deviation fixes. In production, c4 was killed by a host-level
  VM restart and re-run on the fresh boot; three further runs (b3, b4, c2)
  carry flags (SIGTERM mid-wrap-up / 30-min wall) with complete builds and
  measurements — every deviation D-1…D-9 is disclosed in `docs/06` and every
  flagged run in `docs/08` §1. All measurements come from completed
  workspaces.

## 3 · Results

### D1 — Design compliance (agent-introduced lint findings, delta vs starter)

| run | A | run | B | run | C |
|---|---|---|---|---|---|
| a2 | 164 (48 err/110 warn/6 info) | b2 | **0** | c2 | **0** |
| a3 | 127 (31/88/8) | b3 | **0** | c3 | **0** |
| a4 | 162 (37/116/9) | b4 | **0** | c4 | **0** |

A-run violations concentrate in: raw colours (TDS002: 99/62/80), border
radii (TDS003: 37/27/33), physical direction terms (TDS013: 16/23/32).
**B and C: nine clean sweeps, zero findings — including eliminating the
starter's own baseline.**

### D2 — Design drift

| metric | A (runs) | B | C |
|---|---|---|---|
| unique hex colours | 57/40/43 | 1/1/0 | 1/0/1 |
| px spacing values | 28/24/27 | 1/0/0 | 0/0/1 |
| border-radius decls | 14/13/10 | 0/0/0 | 0/0/0 |
| `!important` | 3/1/4 | 0/0/0 | 0/0/0 |
| inline styles | 15/33/31 | 25/10/7 | 15/10/4 |
| distinct classes | 181/125/172 | 183/142/159 | 132/140/141 |

Residual B/C hexes are one `<meta theme-color>` literal; c4's two 10px values
are the only stray spacing. A drifts freely; B ≈ C.

### D3 — Authority behaviour (C only)

| run | calls | RESOLVED | COMPOSE | FALLBACK | UNDEFINED | gaps | proposals |
|---|---|---|---|---|---|---|---|
| c2 | 50 | 2 | 1 | 0 | 1 | 1 | 0 |
| c3 | 67 | 5 | 4 | 1 | 2 | 3 | 3 |
| c4 | 60 | 2 | 4 | 1 | 3 | 2 | 0 |

- Three distinct usage styles (inspect-heavy / balanced / resolve-forward) —
  the interface supports different strategies.
- **Every C run filed ≥1 gap (3/3):** 6 gaps, 3 proposals total.
- Two themes confirmed independently: **reviewer picker** (4 runs incl.
  pilot) and **determinate job progress** (3 runs). Both are genuine
  documentation holes in Triage 0.12.1, discovered by agents through the
  sanctioned channel — the concrete output of the loop.

### D4 — Engineering quality

- Functional: **13/13 checks passed in all nine runs**; 0 console errors in
  all nine captures; backend untouched (UI-only discipline held).
- Durations: A 468/591/633s · B 866/471/1800s · C 510/771/647s.
- Containment: clean; C runs probed the authority zone then used the MCP
  interface; no run escaped its sandbox.

### D5 — Blind human review (single reviewer, project owner)

Codes unsealed only after submission; scores archived
(`benchmark/review/procura-review-2026-10-07.csv`).

| code | condition | score /25 |
|---|---|---|
| CWGM | A | 10 |
| NGQC | A | 18 |
| DWFP | A | 17 |
| XCVJ | B | 22 |
| XQCK | B | 19 |
| CDRR | B | 23 |
| KXCX | C | **25** |
| DKDW | C | 21 |
| RCXF | C | 19 |

**Condition means: A 15.0 · B 21.3 · C 21.7** (axes: consistency A 3.67 /
B 4.67 / C 5.00; coherence 3.33/4.33/4.67; mistakes 3.00/3.67/3.67;
confidence 2.67/4.67/4.33; cleanup 2.33/4.00/4.00).

Human and automated instruments corroborate: worst automated build (a2) = worst
human score; only perfect 25 = a C run.

## 4 · Findings

1. **Active beats no material decisively** — every dimension, both instruments.
   Naive output is functional but lavishly off-system (40–57 colours, 24–28
   spacing values, ~10–14 radii per run).
2. **A good static kit captures nearly all one-shot output quality** —
   B ≈ C on D1, D2, and D5 aggregate. The kit, not the protocol, makes the
   artifact *look* right.
3. **The authority's increment is governance:**
   - *Zero silent improvisation* — C's divergences are cited, sanctioned-
     fallback, or filed gaps. B solved the same underspecified problems by
     quietly inventing patterns (all 3 runs) with no record; at merge time
     nothing distinguishes its improvisation from canon.
   - *Discovery loop* — 6 gaps + 3 proposals, 100% run participation, two
     confirmed holes surfaced from the field.
   - *Enforcement data* — validation calls + complete provenance vs B's none.
4. **No quality ceiling imposed** — C's best build scored perfect while
   staying fully provenance-tracked.

## 5 · Threats to validity

n=3/condition; single model; single app; single blind reviewer; 5-point scale
compression at the top for B/C; three flagged runs (b3, b4, c2 — infra
instability, disclosed) measured from completed workspaces; class-count and
inline-style metrics are static approximations.

## 6 · Artifacts & reproduction

- Report data: `benchmark/runs/<id>/` (run.json, scan.json, interact.json,
  24 screenshots, workspace archive). Summary tables: `benchmark/runs/_summary.md`.
- Review: gallery `https://gpu-vm1.bigscale-snapper.ts.net:9110/` · mapping
  `benchmark/runs/_gallery-mapping-SEALED.json` (now unsealed) · scores
  `benchmark/review/procura-review-2026-10-07.csv` · questionnaire
  `benchmark/harness/questionnaire.html`.
- Docs: `docs/00-audit` (Triage audit) · `01-proposal` · `02-decisions`
  (D-001…D-021) · `06-preregistration` (frozen protocol + deviations
  D-1…D-9) · `08-production-report` · `09-final-synthesis` · **10 = this
  report**.
- Re-run a condition:
  `systemd-run --user … run_condition.py --condition C --run-id cN --timeout 1800`
- Regenerate tables: `report.py --runs benchmark/runs --include a2,…,c4`.
- Rebuild gallery: `gallery.py --include … --out …` (seed fixed → same codes).

## 7 · Next steps

1. **First real authority extensions** from the discovered gaps (reviewer
   picker recipe; determinate job progress) through the proposal → review →
   published loop — the pipeline's first evidence-backed Triage changes.
2. Optional generality test: second app and/or second model on the frozen
   protocol.
3. Decision: continue the authority track toward a maintained internal tool,
   or park it with this evidence base.
