# 00 · Gap evidence reconstruction

**Authority Evolution Experiment — Phase 1.** Sources of record: the per-run
workspace archives (`benchmark/runs/<id>/ws/.design-authority/gaps.jsonl` and
`proposals/`), run records (`run.json` authority blocks), and the completed
production report (`docs/08`, `docs/09`). Nothing here is inferred from
memory; every ID is traceable to a file in `benchmark/runs/`.

## Scope

- Evidence runs: **c1** (pilot), **c2, c2b, c3, c4** (production; pilot ran
  under the accepted protocol revision). c2b is supplementary: it was killed
  mid-build with 40 authority calls and one unformalised UNDEFINED, and filed
  **no** gap or proposal records — excluded from consolidation.
- Raw records recovered: **8 gap records** (c1×2, c2×1, c3×3, c4×2; of which
  6 are from the three production representatives c2/c3/c4) and **5 proposal
  records** (c1×2, c3×3). c4 filed gaps without proposals; c2 filed neither
  proposal nor more than one gap.
- All records are against **triage 0.12.1 @ e374f38**.

| run | exit | authority calls | resolve outcomes | gaps | proposals |
|---|---|---|---|---|---|
| c1 | 0 | 43 | 7R · 6C · 1F · 2U | 2 | 2 |
| c2 | −15† | 50 | 2R · 1C · 1U | 1 | 0 |
| c3 | 0 | 67 | 5R · 4C · 1F · 2U | 3 | 3 |
| c4 | 0 | 60 | 2R · 4C · 1F · 3U | 2 | 0 |

† flagged run; build complete, measurements from the completed workspace.

## Consolidation

Phrasing differs; the design needs do not. Three distinct needs emerge:

| Consolidated | Reports | Runs | Proposals |
|---|---|---|---|
| **G-01** reviewer/entity assignment picker | 4 | c1, c2, c3, c4 | 2 (c1, c3) |
| **G-02** determinate background-job progress | 3 | c1, c3, c4 | 2 (c1, c3) |
| **G-03** irreversible decision with typed reason | 1 | c3 | 1 (c3) |

---

## G-01 · Assign one reviewer from a fixed list, inline on a record page

**Raw records:** `gap/…ee7a49` (c1) · `gap/…0f2dcf` (c2) · `gap/…6c928b` (c3) ·
`gap/…0888c0` (c4)

- **Need:** a compact single-select picker to assign one person (reviewer)
  from a small fixed set, inline in a request-detail page, minimal footprint.
- **Context:** Procura `/requests/<id>`; frozen backend expects
  `POST reviewer=<name>`; 4 fixed reviewers; dependency-free HTML/CSS/JS, must
  work without JS; used by reviewers and ops staff.
- **Authority version:** triage 0.12.1 @ `e374f38…`
- **Runs reporting:** **4** (c1, c2, c3, c4) — the most independently
  rediscovered need in the whole experiment.
- **Closest existing artifacts cited:** `component/cb` (compatibility 4.0),
  `component/dp` (4.0, date picker — near-miss on name), `component/badge`.
- **Fallback/local solution used:** `fallback/native-control` in all four
  runs — a token-conformant native `<select>` + submit button, marked with
  in-code `TODO(authority-undefined)` provenance (c1/c2 in
  `templates/request_detail.html`; c4 additionally a bespoke
  `.reviewer-picker` class in `static/app.css`).
- **Why existing authority was insufficient (from proposals):**
  `component/cb` is a type-to-filter listbox aimed at larger/unknown option
  sets and drags in listbox JS; its multi mode renders chips rather than one
  value; there is **no documented single-select assign/owner recipe**.
  `component/dp` is a date picker. The native select is styled by base.css
  but is **not represented as a catalogued artifact**, so consumers cannot
  cite canon for the most common real case. `resolve_design_problem`
  returned **UNDEFINED** (c1, c3).
- **Proposals already generated:**
  - c1 `prop/…fedd3f` → `recipe/entity-picker` (single-select combobox on
    `component/cb`, optional avatar, native no-JS fallback; depends on cb +
    fallback/native-control + badge; no new primitives).
  - c3 `prop/…a6668e` → `component/select` (new catalogued primitive) **+
    `recipe/assign-picker`**.
- **Conflicting evidence:** abstraction level. c1 solves with a recipe over
  existing artifacts; c3 argues the native select itself deserves a
  catalogued artifact plus a recipe. Scope hints disagree within the raw
  records (`component` in c2/c3/c4; `page/request-detail` in c1). This must
  be adjudicated in Phase 2, not averaged.
- **Local implementations for Phase 8 migration:** `request_detail.html` +
  `app.css` in c1/c2/c3/c4 workspaces.

## G-02 · Determinate long-running background-job progress

**Raw records:** `gap/…19217d` (c1) · `gap/…e336ee` (c3) · `gap/…0e1da7` (c4)

- **Need:** show status and determinate progress of a long-running background
  operation (running %, stalled/stuck, failed with reason, done) with live
  updates and a re-run affordance.
- **Context:** Procura `/jobs` (+ dashboard strip `/`); background AI triage
  scan; backend exposes `state/scanned/total/percent` via JSON `/api/jobs`;
  deterministic forced states `running|done|failed`; polling is plain DOM.
- **Authority version:** triage 0.12.1 @ `e374f38…`
- **Runs reporting:** **3** (c1, c3, c4).
- **Closest existing artifacts cited:** `component/spinner` (indefinite
  only), `component/tl` (append-only history), `component/badge`,
  `pattern/index-eval` (queue flow, not a live meter), `pattern/dry-run`,
  `recipe/status-with-text`.
- **Fallback/local solution used:** `fallback/plain-content` in all three —
  composing `.progress` (base.css ships unstyled-as-canon CSS with
  `role=progressbar` semantics), `.spinner`, `.badge`, `.tl` on a system
  card, plus JSON polling and stall detection in plain JS; marked
  `TODO(authority-undefined)` (c1 `templates/jobs.html` + `static/app.js`;
  c4 `#active-job`, `data-job-bar`, `data-job-progress-text`, `#job-stall`).
- **Why existing authority was insufficient (from proposals):** the
  catalogue has spinner (indeterminate) and badge (state label) but **no
  determinate progress artifact and no status recipe**; `tl` is history, not
  a meter; `index-eval` is a queue flow. The `.progress` primitive exists in
  CSS without a catalogued artifact, so the arrangement is an **unciteable
  improvisation**. `resolve_design_problem` returned **FALLBACK**
  (plain-content) in c1/c3/c4.
- **States the runs found missing:** queued, running (percent +
  scanned/total), stalled (must be text, not colour alone), failed (must
  name the reason + offer retry), done.
- **Proposals already generated:**
  - c1 `prop/…2c593d` → `component/job-progress` (.job-progress wrapping
    .progress + meta + state badge; depends on spinner, tl,
    recipe/status-with-text, fallback/plain-content).
  - c3 `prop/…286a7e` → `component/progress` (determinate bar, aria-valuenow)
    **+ `recipe/job-status`** (status card composition with stalled warning,
    failed note, history table).
- **Conflicting evidence:** c1 wants the composite named as one component;
  c3 wants the progress primitive catalogued plus a composition recipe.
  Neither proposes new CSS primitives beyond what base.css already ships.
- **Local implementations for Phase 8 migration:** `jobs.html` +
  `dashboard.html` + `app.js` in c1/c3/c4 workspaces.

## G-03 · Irreversible decision with a typed reason

**Raw record:** `gap/…b66012` (c3)

- **Need:** an irreversible approval decision (reject) that requires a typed
  reason at the point of action, with feedback the requester sees.
- **Context:** Procura `/requests/<id>`; reject form with required textarea +
  native `confirm()` naming object and consequence; reason stored in history.
- **Authority version:** triage 0.12.1 @ `e374f38…`
- **Runs reporting:** 1 (c3).
- **Closest existing artifacts cited:** `recipe/high-stakes-confirm`,
  `guideline/high-stakes-confirm`, `fallback/native-control`.
- **Fallback/local solution used:** `recipe/high-stakes-confirm` for the
  confirmation sentence + `fallback/native-control` for the textarea;
  `resolve_design_problem` returned **UNDEFINED** for the exact wording.
- **Why insufficient (from proposal):** the pieces exist but **no artifact
  describes the combined pattern** (required reason + confirm sentence that
  names the object and states the decision is final + reason surfacing in
  history).
- **Proposal already generated:** c3 `prop/…1ebb04` →
  `recipe/reasoned-decision` + `guideline/one-way-decision-copy`.
- **Conflicting evidence:** none (single-run evidence — treat with
  correspondingly lower confidence; likely outcome: documentation-level or
  recipe-level at most).

---

## Annex A · Raw record index

| record | run | path (under `benchmark/runs/<run>/ws/.design-authority/`) |
|---|---|---|
| `gap/…ee7a49` | c1 | `gaps.jsonl` line 2 |
| `gap/…19217d` | c1 | `gaps.jsonl` line 1 |
| `gap/…0f2dcf` | c2 | `gaps.jsonl` line 1 |
| `gap/…6c928b` | c3 | `gaps.jsonl` line 1 |
| `gap/…b66012` | c3 | `gaps.jsonl` line 2 |
| `gap/…e336ee` | c3 | `gaps.jsonl` line 3 |
| `gap/…0888c0` | c4 | `gaps.jsonl` line 1 |
| `gap/…0e1da7` | c4 | `gaps.jsonl` line 2 |

## Annex B · Proposal index

| proposal | run | targets | status |
|---|---|---|---|
| `prop/…fedd3f` | c1 | `recipe/entity-picker` | candidate, unreviewed |
| `prop/…2c593d` | c1 | `component/job-progress` (+states) | candidate, unreviewed |
| `prop/…a6668e` | c3 | `component/select` + `recipe/assign-picker` | candidate, unreviewed |
| `prop/…286a7e` | c3 | `component/progress` + `recipe/job-status` | candidate, unreviewed |
| `prop/…1ebb04` | c3 | `recipe/reasoned-decision` + `guideline/one-way-decision-copy` | candidate, unreviewed |

## Notes on record quality

- Several raw gap records leave `why_insufficient`/`searched` null — the
  agents encoded rationale in their decision logs and proposals instead; the
  narratives above use the proposal records as the authoritative rationale.
- Decision-log phrasing detail (the exact `resolve` phrasings tried per run)
  will be cross-referenced during Phase 7 when old-vs-new authority
  behaviour is measured; the gap records themselves carry the needs in the
  agents' own words, which is what the downstream comparisons must reuse.
- No conflicting evidence was found between runs on the *needs* themselves;
  conflicts are strictly about the abstraction level of the remedy (Phase 2
  adjudicates).
