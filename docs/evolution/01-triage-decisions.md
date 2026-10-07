# 01 · Upstream design triage — decisions on each consolidated gap

**Phase 2 output.** Stance per protocol: *assume the authority should NOT be
extended; first solve with the existing Triage authority.* Method: 27-phrasing
resolve battery on triage 0.12.1 (saved:
`docs/evolution/data/baseline-resolves-0.12.1.json`), search/inspect probes,
and direct verification against the raw Triage sources (CSS, spec, examples,
docs pages) — not just the pack's summaries.

## Verified ground truth (what Triage actually contains)

1. **Native `<select>` already exists in substance, not in addressability.**
   `core/base.css:101–103` styles `select` (shared with inputs/textareas),
   including focus ring, `aria-invalid`, and 16px/44px phone behaviour. Triage's
   own examples and docs use selects throughout (`examples/form.html`,
   `examples/components.html`, the Forms section of the components page).
   It is **not** in `spec/states.json`, has **no aliases**, and search for
   `assign` / `owner` / `reviewer` returns **zero hits**.
2. **`.progress` CSS ships in `core/base.css:179–180`** (bar + fill +
   `--dur-progress` transition; `.progress-inline` in patterns.css) and is
   demonstrated on the components page — but is **not catalogued**: no spec
   entry, no a11y contract, no aliases, no states.
3. **Confirm path exists**: `recipe/high-stakes-confirm` + its guideline fire
   (COMPOSE) for wording close to their `needs`; the **reason-bearing combined
   flow appears nowhere** (checked INTERACTION.md's one-way actions section).
4. **Resolver defect, not just missing content:** picker phrasings mis-route —
   4/8 resolve to `pattern/detail` (token overlap on "record page"), 2/8
   compose unrelated recipes (`status-with-text`, `entity-delete-armed`), 2/8
   UNDEFINED. Progress: 3× FALLBACK(plain-content), 3× UNDEFINED, 1× stray
   COMPOSE. Decision: 2× partial COMPOSE, 2× UNDEFINED.

## G-01 · Reviewer/entity assignment picker — **DOCUMENTATION-FIX + RECIPE**

Evaluated against the seven questions:

1. *Adequate existing solution?* In substance yes: the styled native `<select>`
   is already the system-consistent answer (and the one every downstream run
   independently chose). In contract no: it is unciteable, unfindable, and the
   resolver actively mis-routes to `pattern/detail`.
2. *Would better documentation/aliases solve it?* Partially — it fixes
   addressability (citable artefact + vocabulary), not the flow contract.
3. *Existing artifacts into a reusable recipe?* Yes: labelled `select` +
   submit (`component/btn`) + outcome feedback (`recipe/feedback-redirect` /
   `feedback-inplace`), placed on the existing detail-pattern.
4. *New pattern?* No — `pattern/detail` already owns placement; nothing new at
   page level.
5. *New primitive?* No — no new visual language; `component/cb` remains the
   sanctioned option for large/filtered sets (its filter listbox is the wrong
   tool for 4 fixed names, which is why 4/4 runs refused it).
6. *Project-specific?* No — generic owner/assignee/reviewer semantics.
7. *Conflicts with philosophy?* No — native-first is the philosophy
   (`fallback/native-control`; precedent: `component/dlg` is a catalogued
   **native** dialog).

**Classification: DOCUMENTATION-FIX + RECIPE** (compound — the visual layer
already exists; the change is to make it citable and compose it):
- catalogue `select` as a spec-level component (no new CSS; states
  default/focus/invalid/disabled already styled),
- authority-side: `recipe/assign-picker` + aliases/needs vocabulary.

*Rejected bigger shapes:* `component/select` **as a new visual component**
(c3 proposal) — nothing new to build, so a PRIMITIVE-class change is
unjustified; `recipe/entity-picker` on `component/cb` (c1 proposal) — cb is
the wrong primitive for small fixed enumerations (it brings listbox JS to a
no-JS-required case).

## G-02 · Determinate background-job progress — **DOCUMENTATION-FIX + RECIPE**

1. *Adequate existing solution?* The `.progress` primitive exists (shipped,
   documented as a demo) but is unciteable and lacks states/a11y contract;
   `component/spinner` covers only indeterminate waits; every run rebuilt the
   same composition from scratch under FALLBACK(plain-content).
2. *Doc/aliases alone?* Partially — catalogue `.progress` (+a11y: `role`,
   `aria-valuenow`, text readout) and vocabulary; the multi-state jobs
   surface still needs a sanctioned composition.
3. *Recipe?* Yes: progress bar + state badge (`component/badge`, per
   `recipe/status-with-text`) + scanned/total text + stalled/failed copy +
   retry action; polling stays plain JS.
4. *New pattern?* Arguable but unnecessary — `pattern/index-eval` and
   `pattern/dashboard` already cover placements; the missing unit is the
   job-status composition itself (recipe-sized).
5. *New primitive?* No — the CSS exists; cataloguing is documentation.
6. *Project-specific?* No — background work recurs in every app (3/3 runs).
7. *Conflicts?* No — text-not-colour is already doctrine.

**Classification: DOCUMENTATION-FIX (catalogue `progress` + a11y/states
contract) + RECIPE (`recipe/job-progress`)**. *Rejected:* `component/progress`
as a new build (c3) — nothing new to build; `component/job-progress` (c1) — a
composite is a recipe, not a primitive.

## G-03 · Irreversible decision with typed reason — **DOCUMENTATION-FIX**
*(recipe-level alternative held for review)*

1. *Existing?* Partial — the confirm sentence is covered and fires; the
   reason-typing flow is not covered; adjudicated UNDEFINED for exact wording.
2. *Doc fix?* Likely sufficient: extend `recipe/high-stakes-confirm` coverage
   (needs + constraint: when rationale must be recorded, pair the confirm with
   a required, labelled textarea — native control — and surface the reason in
   the history) + aliases (`typed reason`, `reject with reason`,
   `one-way decision`).
3. *Recipe alternative:* if review judges the extension dilutes the recipe's
   identity, upgrade to a small `recipe/reasoned-decision` composing
   high-stakes-confirm + `fallback/native-control` + `component/tl`.
4. *New pattern/primitive?* No — everything used already exists.
5. *Project-specific?* Generic reject/decline flow; keep. Evidence is a
   single run — treat at lower priority and follow the smallest change.

**Classification: DOCUMENTATION-FIX** (primary). No PRIMITIVE-class change
anywhere in this gap.

## Comparison with the downstream proposals (the review line)

| downstream proposal | upstream decision | movement |
|---|---|---|
| c1 `recipe/entity-picker` (on cb) | recipe, but on native `select` | **REVISE** (ingredient swap) |
| c1 `component/job-progress` | recipe `job-progress` | **DOWNGRADE** (component → recipe) |
| c3 `component/select` (new) | documentation (catalogue existing) | **DOWNGRADE** (component → doc) |
| c3 `component/progress` (new) | documentation (catalogue existing) | **DOWNGRADE** (component → doc) |
| c3 `recipe/assign-picker` | adopted (native-select variant) | **REVISE** |
| c3 `recipe/job-status` | adopted as `recipe/job-progress` | **ACCEPT** (renamed) |
| c3 `recipe/reasoned-decision` + guideline | doc-fix of existing recipe (alt held) | **DOWNGRADE** |

Every agent proposal overshot the abstraction ladder by one to two rungs; the
upstream pass found **zero justifications for new primitives or new CSS**.
This is the first concrete instance of the review discipline the experiment
exists to test.

## Notes for the candidate phase

- Catalogue additions must come from **Triage-side** sources (spec/states.json
  is the builder's component source); recipes/aliases/guidelines are
  **curation-side** (design-authority repo). Candidates must not mutate the
  pinned 0.12.1 snapshot — a candidate branch/worktree + versioned rebuild.
- The resolver mis-route to `pattern/detail` must be re-tested after the
  change; if it persists, vocabulary/needs tuning is in scope (not resolver
  scoring changes — the kernel is frozen).
- Regression invariants to preserve (baseline captured): combobox → cb,
  date picker → dp, loading spinner → spinner, toast message → toast2,
  empty state → empty, banner/delete/pagination composes.
