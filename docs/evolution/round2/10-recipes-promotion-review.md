# Recipes promotion review — the 17 evolution recipes against the live Triage pack

Owner memo (da_nextsteps.md section 6): the live Triage authority ships zero
recipes while the evolution line carries 17; evaluate them for promotion
through the normal review process rather than bulk-copying them, so the main
reference authority demonstrates COMPOSE on realistic needs.

- **Method:** mechanical pass on 2026-10-11. Live pack: `authorities/triage`
  (0.12.2, 108 ids). Evolution source: `authorities/triage-evolution`
  (0.13.x-experiment). For each recipe: do its ingredients resolve in the
  live pack, and how do its recorded `needs` phrasings resolve against the
  live resolver today. Judgment follows the round2 review record
  (`docs/evolution/round2/03-review.md`) and the live canon.
- **Headline:** every recipe's needs phrasings mostly resolve UNDEFINED
  against the live pack today (spot checks below). That is the gap the memo
  names: the live pack's COMPOSE surface is empty for realistic asks.
  Promotion would fill it; nothing in the live canon contradicts the recipes
  (Round 2 already aligned the vocabulary: skip, sheet-end, row-actions,
  status words).

## Mechanical findings (per recipe)

| recipe | ingredients live? | notes |
|---|---|---|
| feedback-redirect | ✓ (all) | needs: 4/5 phrasings UNDEFINED live ("show the result of a form submit"), 1 alias away ("show a success message" → component/msg) |
| feedback-inplace | ✓ (all) | live already ships `component/toast2`; 5/6 phrasings UNDEFINED |
| entity-delete-armed | missing `guideline/armed-delete` | live ships `component/arm-del`; the guideline is the missing half |
| high-stakes-confirm | missing `guideline/high-stakes-confirm`, `fallback/native-control` | "confirm an irreversible action" already resolves `component/arm-del`; the typed-reason asks are the new surface |
| entity-toggle | ✓ (all) | live ships `component/px-sw`; 3/3 phrasings UNDEFINED |
| status-with-text | `token-set/color` is `token-set/colour` live; missing `guideline/colour-not-alone` | 6/6 phrasings UNDEFINED |
| empty-with-cta | ✓ (all) | 3/4 phrasings UNDEFINED |
| bulk-actions | ✓ (all) | 3/3 phrasings UNDEFINED |
| editor-savebar | ✓ (all) | 3/3 phrasings UNDEFINED |
| row-actions | ✓ (all) | 4/6 phrasings already steer to menu-item/menu-pop; promotion plus vocabulary tightens the standing dispute (chevron → menu-pop, not menu-item) |
| page-head | missing `guideline/page-hierarchy` | "page title with actions" already resolves `component/page-head` |
| dialog-task | ✓ (all) | 3/3 phrasings UNDEFINED |
| paginated-list | ✓ (all) | today "long list with pages" steers to `fallback/scoped-embedding`; the recipe is the right determinate answer |
| copy-value | missing `guideline/copy-helper` | 2/2 phrasings UNDEFINED |
| filter-row | ✓ (all) | 4/4 phrasings UNDEFINED |
| assign-picker | missing `component/select` (live naming differs; reconcile against the live field/dropdown components) + `recipe/feedback-redirect` | 6/6 phrasings UNDEFINED |
| job-progress | missing `recipe/status-with-text` (promotes with it) | 7/7 phrasings UNDEFINED; live ships progress + spinner + badge |

## Verdicts

**Promote directly (10)** — all ingredients live, no canon conflict:
`feedback-redirect`, `feedback-inplace`, `entity-toggle`, `empty-with-cta`,
`bulk-actions`, `editor-savebar`, `row-actions`, `dialog-task`,
`paginated-list`, `filter-row`.

**Promote with a named prerequisite record (6)** — the recipe plus the
missing record(s) it depends on, reviewed together:
`entity-delete-armed` (+`guideline/armed-delete`),
`high-stakes-confirm` (+`guideline/high-stakes-confirm`,
+`fallback/native-control`), `status-with-text` (+`guideline/colour-not-alone`;
ingredient corrected `token-set/color` → `token-set/colour`),
`page-head` (+`guideline/page-hierarchy`),
`copy-value` (+`guideline/copy-helper`),
`job-progress` (+`recipe/status-with-text`, which rides the batch above).

**Reconcile naming first (1)** — `assign-picker`: its `component/select`
ingredient has no live counterpart under that name; reconcile against the
live component set (the live pack's field/dropdown surface) in review, then
promote with `recipe/feedback-redirect` as its prerequisite.

## Process

Route for promotion (per the memo: the normal review process, not a bulk
copy):

1. One bundled proposal per verdict group, filed in the Triage repository
   with this document as evidence (the same route the three owner-approved
   proposals travel; reviewer = owner).
2. The prerequisite records ride their recipe's proposal with their round2
   provenance (`docs/evolution/round2/`) declared.
3. On acceptance: merge into the live spec, regenerate the pack
   (`build_triage_pack.py`), re-run goldens and the coverage sweep, log
   alias/needs additions in the gap log. The pack's COMPOSE surface gains
   the 17 realistic needs above.

Status: evaluation complete; promotion queued to the review route.
