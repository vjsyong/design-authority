# Round 2 · 03 — Adversarial review (cand-06 … cand-09)

**Reviewer:** clean-context adversarial pass. Stance: every candidate assumed wrong until proved by execution; the baseline was re-run from the packs, and the scratch was re-created from `packs/triage-evolution` (the package's `docs/evolution/data/r2-scratch` was audited, not trusted). Everything below was executed against the real kernel (`python3 tools/da.py`, i.e. `kernel/design_authority`) and the real pack builder. Read-only outside `docs/evolution/data/review-scratch/`; `packs/triage` (0.12.1) and `packs/triage-evolution` (0.13.0) are byte-identical before/after (sha256 manifests in the scratch dir).

## 1 · Method and executed verification

**Baseline re-run (evolution pack).** The four disputed queries reproduce exactly as claimed on `packs/triage-evolution`: (1) `component/nav-item` 13.0 — the "~navigation link" phrase bonus firing on {navigation, link}; (2) `pattern/detail` 8.0 with `component/sheet-end` 4.0 as a runner-up (cand-07's claim confirmed); (3) COMPOSE `recipe/status-with-text` 7.5; (4) COMPOSE `recipe/bulk-actions` 6.0.

**Pinned re-check.** On `packs/triage` 0.12.1: nav-item 13.0, pattern/viewer 8.0, guideline/voice 8.0, menu-item 13.0; `da dispute-replay --expect-standing 4` → standing 4/4 (cleared 0). **Discrepancy:** cand-06's evidence says the pinned misfire scores "(8.0)"; the executed score is 13.0 on both pinned and evolution (8.0 is the token part; +5.0 is the `~navigation link` phrase bonus). Fix the number.

**Scratch re-creation (not the package's scratch).** `docs/evolution/data/review-scratch/`:
- `base/` — byte-identical copy of `packs/triage-evolution` (sha256-verified) — behaves identically to the original on all 78 probes.
- `evo-snap/` + `evo-snap-skip/` — copies of the evolution snapshot (32e680b); the `-skip` copy carries cand-06's exact `spec/states.json` entry and the 0.13.1-experiment version bumps.
- `packs/v06, v07, v08, v09note, v09sum, v09alias, vall, vall_alias` — built with the **real builder** (`tools/build_pack_triage.py`; one scratch copy adds optional per-pattern note support — verified byte-identical output when the key is absent, so it is a no-op for everything except the cand-09 note simulation). `vall` = the package default (06+07+08+09 note-only); `vall_alias` = with cand-09's conditional alias.
- Batteries executed over 10 packs: 4 disputes + 14-probe regression battery (reconstructed — the package publishes no exact list; its 10 named phrasings + 4 area probes) + 60 adversarial probes + 21 focused margin probes + 13 mini probes (112 queries total); plus the round-1 convergence battery (34 hard cases, incl. 5 delete probes) and the evolution golden set (23 cases) on **every** pack.
- Triage gates run in the `-skip` snapshot copy: `tools/verify.py` all-green — including **"38 components verified selector-by-selector"** — and `tests/browser/run.py` **248/248 assertions across 10 fixtures** with `metrics/ui-baseline.json` **30 captures, zero drift** (after the required banner regeneration, §3/cand-06).

**Results (all variants).** Convergence 34/34 and goldens 23/23 hold on every variant, including `vall` and `vall_alias`. The four disputes under `vall` are as claimed: skip 26.0 · sheet-end 13.0 · status-with-text (unchanged) · row-actions 20.0. The full change surface of the package (base → vall) is **23 of 112 probes**: 22 improvements (UNDEFINED/FALLBACK or wrong-owner → correct owner / dispute closure) and **1 downgrade** (false RESOLVED → UNDEFINED; §3/cand-06 action 5). The 14-probe battery: all 14 identical.

## 2 · Verdict table

| # | candidate | verdict | summary |
|---|---|---|---|
| 06 | `cand/06-skip-catalogue` | **REVISE** (minor) | fix works by execution; `status` must be `beta`, docs-map URL pinned, version-regen + evidence-number + scratch fixes |
| 07 | `cand/07-sheet-end-panel-vocabulary` | **ACCEPT** | target + 8 collateral probes verified; zero regressions |
| 08 | `cand/08-row-actions-chevron` | **ACCEPT** | target + 5 collateral probes verified; one advisory watch item |
| 09 | `cand/09-status-chip-codification` | **REVISE** | the conditional alias fails its own battery (badge → tie → unrelated recipe); implement note-only, but fix implementation route + criterion |

## 3 · Per-candidate

### cand/06 — `cand/06-skip-catalogue` → **REVISE (minor)**

**What holds (verified by execution).** With the record present: "a skip link to jump past the navigation" → **RESOLVED `component/skip` 26.0** (matched: skip·navigation·link·jump + `~skip link` + `~skip navigation`; runner-up nav-item 13.0, margin 13.0). "skip to content" → skip 13.0 and `da search "skip to content"` / `da search "skip"` hit `component/skip`. Named nav non-regression holds: "a navigation link in the sidebar" 22.0, "a sidebar link with an active state" 16.0, "navigation links" — all unchanged. The states matrix gate: **38 components verified selector-by-selector**; browser suite 248/248; zero UI-baseline drift. No CSS *rule* changes.

**REQUIRED ACTIONS**

1. **`status`: "stable" → "beta".** The matrix's own lifecycle (`spec/states.json#lifecycle`) + `AGENTS.md` require behavioural regression coverage for `stable` ("the interactive states are exercised in `tests/browser/` — not merely selector presence"). `.skip` has **no** coverage in `tests/browser/` or `metrics/ui-baseline.json` (verified). All three `beta` requirements are met (selector coverage `core/base.css:19/30`; a11y notes; example-page usage — 6 example pages + the site shell). Same doctrine as round 1's select/progress. (Status does not affect resolution; this is an honesty fix, not a gate fix.)
2. **docs-map URL.** "The shell/accessibility page" is not a route; the Shell contract card that lists `.skip` lives at `/components/navigation`. Pin `component/skip: "/components/navigation"` (map URL style).
3. **Version mechanics.** The `0.13.1-experiment` bump mechanically regenerates the generated files whose banners/version fields embed `VERSION`: `core/{base,patterns,reset,scoped}.css`, `tokens/tokens.css`, `icons/icons.json` (rerun `build.py core`, `build.py tokens`, `tools/build_icons.py`). Verified: version-string-only diffs; afterwards `verify.py` all-green, browser 248/248, zero baseline drift. Restate "no CSS changes; the class already ships" → "no rule changes; generated banners regenerate".
4. **Evidence hygiene.** "(8.0) on pinned" → 13.0 (both packs). Rebuild the scratch from snapshot+curation (see §4.1) — the r2-scratch skip record diverges from builder output (no `source.pointer`, no docs-map relation, truncated commit `32e680b`, shortened a11y/summary).
5. **Record as accepted (margin-clog, no code change).** Two adjacent nav phrasings move RESOLVED nav-item → **UNDEFINED**: "a link that jumps past the navigation" and "a link to jump past the navigation" (mechanism below). Baseline answers were *false* RESOLVEDs to nav-item; UNDEFINED is the safer class. Decision to record: accept; do not chase with more aliases.

**Margin-clog mechanism (new collision class).** skip's alias union grants it the token set {skip, link, content, navigation, jump}. A query with {link, jump, navigation} but no "skip" gives skip 12.0 as a runner-up while nav-item leads at 13.0 → the 2.0 margin rule fails → no recipe ≥ 5.0 (next hit 3.0), no fallback → UNDEFINED. Executed search on the v06 pack shows the clog directly (nav-item 13.0, skip 12.0, then 3.0). Note: the kernel's UNDEFINED `why` text only cites the threshold ("scored 13.00 vs 6.50 needed") and does not surface margin failures; kernel is frozen — report-only.

### cand/07 — `cand/07-sheet-end-panel-vocabulary` → **ACCEPT**

**Verified.** Target: dispute query → **RESOLVED `component/sheet-end` 13.0** (panel 4 + sliding 4 + `~sliding panel` 5; runner-up pattern/detail 8.0, margin 5.0). Alias normalization confirmed: "slide-in panel" normalizes to tokens {slid, panel} and fires on "slides in"-style phrasings too. Collateral (8 probes — 4 in the main battery, 4 in the focused set; all improvements): "a slide-in panel", "a sliding panel", "sliding panel for filters", "panel sliding from the edge", "a panel sliding in from the edge", "a record panel sliding in", "a sliding panel with a record", "sheet sliding from the edge" — UNDEFINED → sheet-end. Named non-regression holds: "open an end sheet for secondary details" 14.5, "a side panel with filters" 13.0, "a detail view of a record" 17.0, "a record page for one item" 22.0, "a detail panel for a record" 8.0, "a filter panel beside the list" unchanged; "a carousel with sliding cards"/"a slide-out menu"/"a settings panel" unchanged (no false positives). Convergence 34/34, goldens 23/23.

**REQUIRED ACTIONS:** none (accept as drafted). Rebuild the scratch pre-test from the builder for the record (§4.1).

### cand/08 — `cand/08-row-actions-chevron` → **ACCEPT**

**Verified.** Target: dispute query → **COMPOSE `recipe/row-actions` 20.0** (chevron·reveal·action·single·row + `~the chevron that reveals actions for a single row`; previous answer was bulk-actions 6.0). Collateral (5 probes, all to the semantically-correct recipe): "reveal the actions for one row" 17.0, "the chevron that reveals actions for one row" 20.0, "row actions chevron" / "the actions chevron on a row" / "click the chevron to see row actions" 9.0. Non-regression holds: "batch delete selected" 14.0, "act on many selected records" 17.0, "select rows then approve", "delete selected rows", "bulk actions" unchanged; "per-row actions" 11.0, "more menu on a row" 14.0, "actions for a list item" unchanged; delete probes all stable. The recipe's evidence quote was re-checked against `INTERACTION.md` §Lists & row actions (accurate). Convergence 34/34, goldens 23/23.

**REQUIRED ACTIONS:** none blocking. **Advisory watch:** "open the action menu for selected rows" flips COMPOSE bulk-actions 9.0 → row-actions 17.0 — an ambiguous cross-over phrasing (batch context, menu shape); defensible under the recorded canon (bulk = bar buttons, row = menu), keep it on the watch battery. Rebuild the scratch pre-test from the builder for the record (§4.1).

### cand/09 — `cand/09-status-chip-codification` → **REVISE**

**The conditional alias fails its own battery — decide "note-only".** At the `v09alias` config, badge phrasings tie `pattern/dashboard` and the 2.0 margin fails; resolution then degrades to COMPOSE of an unrelated recipe:

| query | base | with the alias |
|---|---|---|
| a row of status chips | RESOLVED badge 13.0 | **COMPOSE recipe/filter-row 9.0** (alts: badge 13.0, dashboard 13.0 — tie) |
| status chips for system state | RESOLVED badge 17.0 | **COMPOSE recipe/filter-row 6.0** (tie 17.0/17.0) |
| a status chip | RESOLVED badge 13.0 | **COMPOSE recipe/filter-row 6.0** (tie 13.0/13.0) |
| the dashboard status chips | RESOLVED badge 13.0 | RESOLVED pattern/dashboard 17.0 |

The dossier predicted "may route to pattern/dashboard, the correct owner"; execution shows dashboard only wins when a *dashboard* token is present — otherwise the badge query loses its RESOLVED to a tie and lands on `recipe/filter-row` ("Filtering a list is a chip row over the table"), which has nothing to do with state labels. By the candidate's own rule ("only if the battery shows no badge disruption; otherwise note-only"), the answer is **note-only**.

**REQUIRED ACTIONS**

1. **Drop the conditional alias** (`pattern/dashboard += ["status chips"]`) with the evidence above.
2. **Implementability.** "patterns.json note/body +=" has no mechanical path: the builder hard-codes `body.note = "no states/verify contract (see gap G-003)"` for every pattern and the patterns curation schema has no note/body field. Choose one: **(a)** extend the builder to honour an optional per-pattern `note` (one line; verified output-identical when absent) and add the note text — zero resolution effect, since `body.note` is neither indexed nor scored; or **(b)** if searchability is a hard requirement, put the class names in the pattern `summary` (verified: `da search "status-chips"` then hits `pattern/dashboard` 1.5; note-only yields 0 hits). The battery is unchanged under both routes (34 focused probes).
3. **Fix the validation criterion.** "the class names appear in the catalogue (searchable)" is false under route (a): `da search` indexes title/summary/aliases only. State the property of the chosen route ("named in the record, inspect-visible" for (a); "searchable" only for (b)).
4. **Post-implementation check.** The four badge phrasings must stay 13.0 / 17.0 / 13.0 / 13.0 (they do under both routes as measured). Rebuild the scratch pre-test from the builder (§4.1).

## 4 · Cross-cutting findings

1. **The package's scratch pre-test is not a build (`r2-scratch` audit).** It is the 0.13.0 pack copy with `artifacts.json` + `recipes.json` hand-edited; its `curation/` is byte-identical to the pack's (its own receipt's `curation_sha256` matches — curation was never edited); the receipt is stale (still 37 components, same `built_at`); the `component/skip` record diverges from what the builder emits (missing `source.pointer`, missing docs-map `relations`, truncated commit, shortened a11y/summary); and **cand-09 is not represented at all** (no dashboard change anywhere). So the claim "built from the exact record edits the candidates propose" (and "regenerated for the review") does not hold, and the pre-test table cannot be replayed from the package contents. The same edit path would also ship a degraded provenance record if phase 5 copied it verbatim. **Required action (shared, phase 5/6):** rebuild the scratch/receipts from snapshot+curation — this review's `docs/evolution/data/review-scratch/` is the reference implementation (base + 8 builder-built variants + probe results), and every number above was re-derived from it.
2. **Margin-clog is a new collision class to watch** (detail in §3/cand-06). Adding an alias-union to one artifact can defeat another artifact's RESOLVED through the 2.0 margin rule (13.0 vs 12.0 → UNDEFINED) without ever outscoring it. Quantified here: 2 probes, outcomes in the safer class. Add margin-clog probes (nearby vocabularies, no trigger token) to future batteries alongside the delete probes.
3. **Numbers to fix in the dossier.** cand-06 "(8.0) on pinned" → 13.0. Everything else spot-checked held: pinned replay 4/4; sheet-end runner-up 4.0; the `INTERACTION.md` quote; the scratch battery's behavioral table; the 14-probe non-regression claim (for the reconstruction). The package does not publish its exact 14 probes — publish the list in phase 5/6.
4. **Provenance/release metadata is missing from every candidate.** None of the four `proposed_change` blocks touches `curation/evolution.json`. Phase 5 must add provenance blocks for `component/skip`, `component/sheet-end`, `recipe/row-actions`, `pattern/dashboard` (introduced_in `0.13.1-experiment`, triggering disputes/gaps, review decision = this file, tests) and bump `release.label`, mirroring round 1 — otherwise the built receipt still claims 0.13.0-experiment / round-1 review.
5. **Discipline checks (all verified).** Pinned + evolution packs byte-identical before/after (sha256 manifests in the scratch). No kernel, threshold, margin or precedence change is proposed or needed. Delete probes (5) stable on every variant; convergence 34/34 and goldens 23/23 on every variant. The candidates' "forbidden by construction" list (02-candidates.md) holds as written, with the one process caveat: "no alias that a delete/regression probe flips" is true of the *named* probes; the unwritten surface (margin-clog, cross-over) is quantified in §3–4.
6. **Not re-run here (phase-6 scope):** the full strict-lint / browser suite on the actual `triage-design-system-evo` worktree (instructed read-only; run on a byte-copy), and the release build itself. Both are covered by the standing gates and reproduce green on the copy.

## 5 · Authority inflation — explicit statement

Net: **+1 component** (`component/skip`, status to be `beta`), **+6 alias entries** (skip ×4, sheet-end ×2), **+3 recipe needs**, **+1 documentation note** on a pattern. No new CSS rules (regenerated bytes are version banners only), no new recipes/patterns/tokens/rules/prohibitions, no kernel change. Change surface: 23 of 112 probes move under the full package — 22 improvements, 1 safer-class downgrade. That is proportionate to the five consolidated needs and smaller than what a "new visual language" response would have been. Recommendation: **proceed with cand-07 and cand-08 as drafted, apply cand-06 with required actions 1–4, and implement cand-09 note-only via an explicit builder note field (or the summary route) with the criterion corrected** — all four then converge on the executable contract verified in this review.

## Evidence inventory (all under `docs/evolution/data/review-scratch/`)

- `hashes-pinned-start.txt`, `hashes-evo-start.txt` — protected-path manifests (re-checked at review end: identical).
- `base/` — verified copy of `packs/triage-evolution`; `evo-snap/`, `evo-snap-skip/` — snapshot copies (the latter with cand-06's states entry + version regen, triage gates green).
- `packs/{v06,v07,v08,v09note,v09sum,v09alias,vall,vall_alias}` — builder-built variants; `packs/v06/BUILD.json` warns only the expected snapshot drift (76 artifacts, 38 components, no curation warnings).
- `results/probes-ALL.json` (+ per-pack files), `results/probes-extra.json` — every probe, outcome, resolution id, score, matched tokens and runner-ups.
- `scratch-build/{make_variants.py,bld_sim.py,run_probes.py,run_extra.py,v06_real/}` — reproducible pipeline; `v06_real/` is the real-builder equivalence proof (all generated files identical to the bld_sim build).
