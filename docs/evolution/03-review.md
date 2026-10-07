# 03 · Adversarial review — candidate authority changes (Phase 4)

**Reviewer:** clean-context adversarial pass. No proposal internals were seen; verdicts are from the artifacts in `docs/evolution/00–02`, the five `proposals/evolution/cand-*.json`, the frozen kernel, and execution against the pinned snapshot. Read-only: no repo file was modified except this one.
**Authority under review:** triage 0.12.1 @ e374f38, snapshot `~/triage-design-system-demo`. (Note: `/home/xrim/triage-design-system` is at e04e10c — *not* the build source; all CSS/verify claims below were re-checked against the pinned demo tree.)

## 1 · Method and executed verification

**Baseline re-run.** Drove the real kernel (`kernel/design_authority`) over `packs/triage` on all **27** phrasings in `data/baseline-resolves-0.12.1.json`: **27/27 reproduce** outcome+artifact (picker 4× `pattern/detail`, 2× unrelated COMPOSE (`status-with-text`, `entity-delete-armed`), 2× UNDEFINED; progress 3× FALLBACK(`plain-content`), 3× UNDEFINED, 1× COMPOSE; decision 2× COMPOSE, 2× UNDEFINED; regression 8 stable). Note: `01-triage-decisions.md` says "30-phrasing battery" — the saved file contains 27; reconcile the doc.

**Search claims.** `da.py search`: `assign` / `owner` / `reviewer` → **zero hits**; `progress` → `index-eval 1.5`, `spinner 1.0` (matches the doc).

**CSS claims (pinned tree).** `select` styled at `core/base.css:101–103` (shared control rule + focus ring), `:510–511` / `:598` (16px + 44px phone), `:631–633` (aria-invalid), `:732` (focus-visible); `.progress` at `:179–180` (bar + `i` fill + `--dur-progress`), demoed at `examples/components.html:165`; selects used at `examples/components.html:91,261–262` and `examples/form.html:126,157`. **`.select` class does not exist** (only `.select-inline`, `patterns.css:294`, and JS `ta.select()`). All cand/01–02 CSS claims hold.

**Lifecycle / verify mechanics.** `spec/states.json`: 35 components, all `stable` → +2 = "37 components" claim correct. `verify.py` requires status ∈ {stable,beta,experimental,deprecated} + a lifecycle definition, `'.'+class` present in core CSS, and each verify fragment to be a substring of some core selector. **beta** is defined as shipped+dogfooded+example-usage without dedicated browser regression — and **neither select nor progress appears anywhere in `tests/browser/fixtures/` or `metrics/ui-baseline.json`** → **beta is the honest level; stable would over-claim**. Caveat: the `'.'+class` check is substring-based, so `.select` already "exists" via `.select-inline`; Phase 5 must show the real CSS diff, not just a green gate.

**Build mechanics.** `tools/build_pack_triage.py` derives `component/<class>` from snapshot states.json, merges curation (aliases/notes/docs-map), and **hard-fails on unknown recipe ingredients** — so ingredient edits are load-bearing. All non-new ingredients resolve (inspected: `component/btn`, `badge`, `spinner`, `tl`, `recipe/feedback-redirect`, `feedback-inplace`, `status-with-text`, `fallback/native-control`, `recipe/high-stakes-confirm`, `guideline/high-stakes-confirm`).

**Candidate simulation (the core verification).** Scratch copies of the pack with the candidate deltas applied exactly as the builder would emit them (never touching `packs/triage`), then resolver runs over the 27 baseline phrasings + adversarial probes. 5 package variants + 10 micro-tuning variants. Results:

| config | G-01 (8 phrasings) | G-02 (7) | G-03 (4) | delete probes |
|---|---|---|---|---|
| 0.12.1 | 4× pattern/detail, 2× unrelated, 2× UNDEFINED | 3× FALLBACK, 3× UNDEF, 1× compose | 2× compose, 2× UNDEFINED | all → entity-delete-armed |
| **as drafted** | 7× component/select, 1× still pattern/detail, **0× recipe** | 4× component/progress, 3× recipe | 3× recipe, 1× still UNDEFINED | **flip**: "remove a reviewer…" → select; "remove/delete a person…" → assign-picker |
| **recommended edits** | 7× select + 1× recipe, 0 detail | 5× recipe + 2× component | 4× recipe | all → entity-delete-armed ✓ |

Verified specifics used below: `combobox` → cb, `date picker` → dp under both drafted and tuned configs (no cross-hijack); "Entity picker for assigning a record to a person" keeps mis-routing to pattern/detail unless a `record picker` alias is added; adding an `entity picker` alias *instead* hijacks "delete an entity from a list" (armed → component/select); assign-picker's drafted title/needs leak the token **`from`** (not a kernel stopword), producing 9.0=9.0 ties with `entity-delete-armed`; cand/05 as drafted leaves "High stakes confirmation with a required reason" UNDEFINED (4.0 < 5.0 compose threshold).

## 2 · Verdict table

| # | candidate | verdict | summary |
|---|---|---|---|
| 01 | select catalogue + aliases | **REVISE** | approach right; alias list and convergence criterion are not |
| 02 | progress catalogue + a11y | **REVISE** (minor) | one alias trim; a11y contract needs aria-valuetext |
| 03 | recipe/assign-picker | **REVISE** | delete-probe flips; dual-feedback ambiguity; criterion |
| 04 | recipe/job-progress | **REVISE** (minor) | missing retry ingredient; queued/done coverage; criterion |
| 05 | confirm-reason extension | **REVISE** | Option A chosen, but needs 3 edits; Option B not built |

## 3 · Per-candidate

### cand/01 — `.select` catalogue  →  REVISE

- **Necessity**: strong. 4/4 runs, zero search hits, mis-routes reproduced by execution.
- **Semantic coherence**: naming/level right. The `.select` class alias is the *only* mechanically compliant shape: verify.py's class + verify-fragment checks need literal class-scoped selectors, and the styling genuinely exists as element rules (`101–103`, `510–511`, `631–633`). "Additive selector aliases only, no new declarations" is accurate.
- **Reusability / Visual coherence**: global, zero new visual language. Verified: nothing to restyle; the class makes existing canon citable.
- **Interaction coherence**: native-first, consistent with `fallback/native-control` and the catalogued native `component/dlg`. No-JS safe.
- **Compositional fit**: incomplete on its own — a RESOLVED `component/select` answer must route onward to the flow recipe (see required edit 2).
- **Accessibility**: inherits focus ring, aria-invalid, 44px, 16px phone behavior. Recommend also including `.select` in the `:focus-visible` group (base.css:732) for parity; not required by verify.
- **Complexity cost**: low, but every alias token is a global scoring influence — the collateral below is real, not theoretical.
- **Risk of authority inflation**: low — a spec entry over shipped CSS. Accepted.

**REQUIRED ACTIONS**
1. `curation/aliases.json#component/select` := `["select","native select","single select","select control","assign picker","reviewer picker","owner picker","record picker"]` — i.e. **drop `"fixed list picker"`** (its `list`/`fixed` tokens make "remove a reviewer from a list" RESOLVE `component/select` where 0.12.1 answered `entity-delete-armed`; verified) and **add `"record picker"`** (without it, one of the four benchmarked picker mis-routes — "Entity picker for assigning a record to a person" → `pattern/detail` — survives the whole package; verified). Do **not** add `"entity picker"` (verified hijack: "delete an entity from a list" flips to `component/select`).
2. `curation/component-notes.json#component/select`: append cross-reference — "for the labelled assign flow (action + outcome) compose `recipe/assign-picker`."
3. Rewrite the convergence criterion in `cand-01`'s `validation`: under the frozen kernel artifacts take precedence over recipes, so "8 picker phrasings → `recipe/assign-picker`" is **not achievable** by any vocabulary that also removes the `pattern/detail` mis-routes (verified: once the picker vocabulary exists, 7/8 phrasings clear DIRECT_MIN with margin; every variant that keeps the recipe in front leaves ≥4 pattern/detail mis-routes). Replace with the verified contract + per-phrasing mapping: 7 → `component/select`, #5 ("Choose one owner from a list of people") → `recipe/assign-picker`, zero `pattern/detail`, zero unrelated recipes.
4. Add the delete probes to the non-regression battery (see cross-cutting §4.2).

### cand/02 — `.progress` catalogue  →  REVISE (minor)

- **Necessity**: strong (3 runs; unciteable CSS; no a11y contract exists).
- **Semantic coherence**: states `["determinate (aria-valuenow)","complete (100%)"]` are honest for the *component*; the queued/stalled/failed states belong to the recipe — correct layering.
- **Reusability / Visual coherence**: zero CSS changes; global.
- **Interaction coherence**: text-not-colour is doctrine; `--dur-progress` respected; polling stays outside.
- **Compositional fit**: good; but the alias list must not pull flow phrasings away from the recipe (edit 1).
- **Accessibility**: cataloguing is *worth it precisely because* the a11y contract is the missing piece. Incomplete without `aria-valuetext` (the scanned/total semantics that motivated the gap).
- **Complexity / inflation**: lowest of the package. beta correct (verified no browser coverage; example usage exists).

**REQUIRED ACTIONS**
1. `curation/aliases.json#component/progress` := `["progress bar","progress meter","progress track"]` — **drop `"determinate progress"`**: with it, baseline phrasings #3, #4, #6 resolve to the bare component instead of `recipe/job-progress`; without it they compose the recipe (verified).
2. `a11y` add: "`aria-valuetext` carries the human readout (e.g. '12 of 40 scanned'); the adjacent visible text is the same words."
3. Rewrite `validation`: verified mapping = 5 × COMPOSE `recipe/job-progress` (#1,#3,#4,#6,#7) + 2 × RESOLVED `component/progress` (#2 "…live progress readout", #5 "Progress bar … stalled state"), zero FALLBACK/UNDEFINED/stray COMPOSE. Document why #2/#5 stay component-level (the bar is named; routing them to the recipe would require contorting component docs — not recommended).

### cand/03 — `recipe/assign-picker`  →  REVISE

- **Necessity**: strong (the recurring arrangement; needed to make flows citable).
- **Semantic coherence**: needs are faithful to the 8 baseline vocabularies *except* the `from` leak (below); title/needs wording otherwise fine. Ingredients: citing **two** feedback recipes is semantically ambiguous — a consumer gets both paths with no rule for choosing.
- **Reusability**: global; composes only existing artifacts.
- **Visual / Interaction coherence**: no new language; "degrades without JS" matches the native-first doctrine.
- **Compositional fit**: depends on cand/01's edit 1; must not tie with `entity-delete-armed` on delete phrasings.
- **Accessibility**: inherited (labelled control stated in constraints). OK.
- **Complexity / inflation**: the component-alias ↔ recipe-needs duplication is this package's main collision surface; keep it minimal.

**REQUIRED ACTIONS**
1. `ingredients` := `["component/select","component/btn","recipe/feedback-redirect"]` (single primary path; both feedback recipes verified to exist — the ambiguity is semantic, not mechanical) and `constraints_add`: "if the assign is handled in place (fetch), the outcome uses `recipe/feedback-inplace` instead of the redirect banner."
2. De-leak `from` (verified mechanism: `from` is not a stopword; title + 3 needs contributed it, making "remove/delete a person from a list" tie 9.0=9.0 and flip to assign-picker by id sort). Verified fix: `title` → "Assign one person to a small fixed set" (any title without `from`; re-run probes if reworded) and `needs` := `["assign a reviewer to a request","assign an owner to a record","choose one reviewer in a fixed list","pick a person in a small fixed list","single select of a fixed set of options","choose an assignee for a record"]`. Verified effect: all six delete probes return to `entity-delete-armed` (9.0 vs 6.0) with zero loss to G-01/flow behaviour.
3. Rewrite `validation` ("8 G-01 phrasings → recipe/assign-picker") to the same verified mapping as cand/01 req 3; add the delete battery to non-regression.
4. Keep the "pick a person…" phrase coverage — it is what makes "choose a person from a list" COMPOSE `recipe/assign-picker` (verified).

### cand/04 — `recipe/job-progress`  →  REVISE (minor)

- **Necessity**: strong (3 runs rebuilt the same composition).
- **Semantic coherence**: needs cover running/stalled/failed/percent/scan, but the evidence's state list (queued · running · stalled · failed · done) and the re-run affordance are not fully covered.
- **Compositional fit**: constraints promise a retry action but the ingredient list has no button (every named behavior should be backed by an ingredient).
- **Reusability / Visual coherence**: composes existing artifacts; no new language.
- **Interaction coherence**: JSON polling, no reloads, text-not-colour — consistent with doctrine.
- **Accessibility**: "state changes announced" is stated but the mechanism is unnamed; name it (aria-live or the toast host).
- **Complexity / inflation**: low; history (`.tl`) deliberately dropped — acceptable, it is not promised by the recipe text.

**REQUIRED ACTIONS**
1. `ingredients_add`: `"component/btn"` (the retry action; verified to exist).
2. `needs_add`: `"re-run a failed background job"` (verbatim from the G-02 evidence; "re-run a failed job" verified → COMPOSE once present in the tuned config).
3. `constraints_add`: "queued and done are labelled states too (same text+colour treatment; a completed bar is not left unlabelled)" and amend "state changes announced" to name the mechanism ("via an aria-live region on the status line / the shared toast host").
4. Rewrite `validation`: verified mapping = 5 × COMPOSE `recipe/job-progress` + 2 × RESOLVED `component/progress` (#2, #5), zero FALLBACK/UNDEFINED/stray COMPOSE (as in cand/02 req 3).

### cand/05 — high-stakes-confirm extension  →  REVISE  (Option A, edited; Option B not built)

- **Necessity**: single-run evidence (c3). Documentation-level is the right weight; no new artifact is justified yet.
- **A vs B (adjudicated)**: **Option A**. Justification: smallest change; keeps one home for the one-way-action doctrine; B duplicates needs and adds surface with no verified benefit — B reaches #1–#3 but "High stakes confirmation with a required reason" stays UNDEFINED (4.5) unless the same need is added anyway, and B fragments confirm guidance across two recipes. B stays held; **not built this phase**.
- **Semantic coherence**: the extension fits `INTERACTION.md#one-way-actions`, but as drafted it contradicts the recipe's own constraint "only the listed set" (the guideline's representative set does not include reject/decline-with-reason).
- **Compositional fit**: the new constraint names a textarea and history, but the ingredient list still only cites the guideline.
- **Reusability / Visual / Interaction coherence**: wording-only extension; no new visual language or interaction, applies the existing one-way-action doctrine to the reason-bearing case.
- **Accessibility**: required, labelled textarea (native) — fine once ingredient-cited.
- **Complexity / inflation**: near-zero for A; B would be inflation on 1-run evidence. Watch this as the "smallest change" precedent.

**REQUIRED ACTIONS**
1. `needs_add`: the drafted four **plus** `"high-stakes confirmation with a required reason"` — as drafted, that phrasing stays UNDEFINED (4.0 < 5.0; "required" does not stem to the added needs' tokens). Verified: with the added need, all 4 decision phrasings COMPOSE `recipe/high-stakes-confirm` (scores 34/12/6/9).
2. `ingredients_add`: `["fallback/native-control","component/tl"]` (both named by the new constraint; both verified to exist).
3. `curation/guidelines.json#guideline/high-stakes-confirm`: extend the representative set (quote) to include the reason-bearing reject/decline case, and update `recipe/high-stakes-confirm` constraint "only the listed set" → "the listed set plus reason-bearing reject/decline decisions" — otherwise the recipe contradicts its own new coverage.
4. Non-regression verified: "confirm rebuild" → high-stakes-confirm; "delete a rule from a list" → entity-delete-armed (unchanged).

## 4 · Cross-cutting findings

1. **The Phase-2 downgrade story holds, with one hidden cost.** Verified: zero justifications for new primitives/CSS; both catalogues and both recipes are genuinely documentation/composition-level. But under the frozen kernel's artifact-priority, a catalogued control that carries assignment vocabulary *outcompetes the recipe adopted to fix G-01*: as drafted, 0 of 8 baseline picker phrasings reach `recipe/assign-picker`, and one mis-route survives. The honest resolution is to re-establish the success criteria (this review's edits), **not** to touch the kernel or inflate vocabulary to game scores.
2. **Collision class (new).** Vocabulary is global. Verified flips caused by the draft: `fixed list picker` + `reviewer picker` aliases and the `from`-leaking title/needs moved "remove a reviewer/person/owner …" queries from `entity-delete-armed` to `select`/`assign-picker`; an `entity picker` alias would move "delete an entity from a list" to `select`. Every future candidate needs a collision battery — delete / toggle / route-adjacent probes, not just the 8-item regression list. The recommended edits restore all probed deletes to `entity-delete-armed`.
3. **`from` is not a kernel stopword.** Function words leak 3.0/4.0 weights and create ties broken by artifact id — the exact mechanism above. Check needs/aliases for stopword-adjacent words before submitting.
4. **Doc accuracy.** "30-phrasing battery" vs 27 saved; also `01` says `search "progress"` yields "only spinner + index-eval" — verified, but index-eval actually outranks spinner (cosmetic).
5. **verify.py gate is weaker than it looks** (substring class check; `.select` already matches via `.select-inline`). Phase 5 evidence for cand/01 must include the actual additive CSS diff + re-run of the 37-component gate.
6. **Snapshot discipline.** Builds must come from `~/triage-design-system-demo` @ e374f38 (or an explicit candidate clone) — not the newer `/home/xrim/triage-design-system` tree (e04e10c). None of the candidates touch the pinned 0.12.1 pack; that discipline is respected.
7. **Evidence chain spot-checked**: `benchmark/runs/c3/ws/.design-authority/gaps.jsonl` (`gap/…6c928b`) matches the G-01 record's need/fallback text; c4 anchors exist. Nothing undermines the Phase-1 consolidation.

## 5 · Authority inflation — explicit statement

**Net new visual language: zero; new CSS declarations: zero; new patterns/primitives/tokens: zero.** Surface growth = 2 spec entries (first `beta`-level entries; justified by the lifecycle's own definitions and verified evidence), 2 curated recipes, 1 recipe extension, plus vocabulary. That is proportionate to the evidence (4/3/3/1 independent runs) and *smaller* than what the downstream agents proposed (two of their component proposals are correctly downgraded, one recipe rename accepted). The one place where inflation **did** materialise is vocabulary breadth — aliases and needs with generic tokens (`list`, `from`, `entity`, `determinate`) that alter routing outside the target need domains; it is quantified above and bounded by the required edits. Option B (a second decision recipe) would be unjustified inflation on single-run evidence and must not be built. Recommendation: **proceed only with the REQUIRED ACTIONS applied and the convergence criteria rewritten to the verified, achievable contract** — a package whose stated criteria cannot be met would be worse than no package, because it would pass review on paper while failing the exact phrasings it exists to fix.
