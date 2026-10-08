# Cadence — dominion build v3 · decision log

- **App:** Cadence, a personal ritual tracker (Today · History · Achievements · Settings;
  log/detail/confirm/onboarding flows; fixed copy + frozen fixtures; demo clock 2026-10-07).
- **Authority:** dominion `0.2.0` (format 0.1) — **including the new canon** `component/status`,
  `component/ledger`, `component/notice`, `pattern/plain-chart`, and the seven negative
  precedents (`packs/dominion/precedents.json`).
- **Method:** every element the app needs (the 42 asks of `docs/synthesis/12-stress-plan.md`)
  resolved with `python3 tools/da.py --pack packs/dominion resolve "<ask>" --json`.
  Raw outputs: `_evidence/resolves.jsonl` (1 line per ask, in spec order; line n = ask n).
  Extra near-miss probes (searches, alt resolves, precedent queries): `_evidence/probes.jsonl`.
  Handling per the pack's own policy: **RESOLVED/COMPOSE** build per the cited
  artifact/recipe · **FALLBACK** apply the fallback constraints + mark + report gap where the
  fallback says so · **CONFLICT** do not build as asked; adapt per the cited prohibition ·
  **UNDEFINED** search synonyms, inspect near-misses, then improvise in character + mark + file a gap.
  **Precedent attachments are recorded verbatim** (even alongside COMPOSE/CONFLICT); each
  try-list was followed where it applies. All 7 precedents fired at least once.
- **Zero network:** one HTML file, one CSS file, one JS file, one local font
  (`fonts/Arimo-VF.ttf`, copied from `docs/synthesis/dominion/tile/fonts/`); every path
  relative; CSV export and persistence are on-page (Blob / localStorage).

## Outcome mix (42)

| outcome | n | asks |
|---|---|---|
| RESOLVED | 11 | 1, 2, 9, 12, 13, 14, 17, 24, 30, 31, 36 |
| COMPOSE | 2 | 3, 4 |
| FALLBACK | 7 | 20, 21, 22, 23, 26, 27, 33 |
| CONFLICT | 3 | 18, 41, 42 |
| UNDEFINED | 19 | 5–8, 10, 11, 15, 16, 19, 25, 28, 29, 32, 34, 35, 37, 38, 39, 40 |

The just-codified canon moved **nine asks out of UNDEFINED** vs the phase-3b sweep baseline
(R5 · F6 · X3 · U28 → R11 · C2 · F7 · X3 · U19): delete + confirm → COMPOSE
(`recipe/retire-confirm`); bar chart, heatmap, sparkline → RESOLVED (`pattern/plain-chart`);
status label → `component/status`; entries table → `component/ledger`; undo →
`component/action`; number stepper → platform fallback. The apparent hole that remains is
the gamification core (ring, streak, badge, celebration) — still UNDEFINED *by design*,
answered by precedents rather than canon.

**Precedents attached:** 17 attachments across 16 rows.
`dialog-empty-state-rejected` ×4 (4, 5, 8, 41) · `declined-saving-and-celebration` ×3
(6, 10, 40) · `declined-progress-ring-badges` ×3 (11, 15, 16) · `declined-photographic-imagery`
×3 (18, 41, 42) · `declined-pictograms-and-tags` ×2 (19, 34) · `declined-view-tabs-paging` ×1
(32) · `reversed-colourway-rejected` ×1 (39). No FALLBACK row received a precedent attachment
(observed kernel behaviour: attachments land on COMPOSE/CONFLICT/UNDEFINED).

## The 42-row decision log

| # | element | outcome | resolution id | precedents attached | built-as | marked |
|---|---------|---------|---------------|---------------------|----------|--------|
| 1 | a primary button for the main action | RESOLVED | `component/action` | — | Slate primary 'Save log' in the log editor; the next unlogged ritual's Log button is the row-level primary; one primary per view. | — |
| 2 | a secondary button and a text link | RESOLVED | `component/action` | — | Outline 'Log' / 'Cancel' buttons (secondary) + underlined 'Details' link (tertiary). | — |
| 3 | delete a ritual permanently | COMPOSE | `recipe/retire-confirm` | — | 'Remove ritual' action; consequence sentence in the confirm step; entries kept after removal. | — |
| 4 | a confirmation dialog before deleting | COMPOSE | `recipe/retire-confirm` | dialog-empty-state-rejected | Square confirm sheet per the recipe: 2px black frame, black scrim 55%, instant; confirm = slate button with the verb; never pre-focused; bilingual title. | data-adapted |
| 5 | a modal with ritual details | UNDEFINED | — | dialog-empty-state-rejected | In-page detail block under the list (no overlay): category, frequency, target, status, recent count. | data-adapted |
| 6 | a toast notification saying logged | UNDEFINED | — | declined-saving-and-celebration | Ruled notice (#F4F4F4 band under a 2px rule) after save; dismissible; no toasts. | data-adapted |
| 7 | a banner summarizing the week | UNDEFINED | — | — | Ruled summary band with a plain sentence + display numerals (slots, minutes, streak). | data-improvised [G1] |
| 8 | an empty state when no rituals exist | UNDEFINED | — | dialog-empty-state-rejected | Ruled statement + one outline action ('Add a ritual'); shown when all rituals are removed. | data-adapted |
| 9 | an error message under the field | RESOLVED | `component/field` | — | Field invalid state: 2px black left rule + plain sentence under the name input. | — |
| 10 | a loading spinner while saving | UNDEFINED | — | declined-saving-and-celebration | Saving state as a meter composition: 'Saving · 0 of 1 steps' → 'Saved · 1 of 1 steps'; no spinner. | data-adapted |
| 11 | a circular progress ring of today's completion | UNDEFINED | — | declined-progress-ring-badges | Declined; square meter with plain readout for today's completion. | data-adapted |
| 12 | a bar chart of weekly minutes | RESOLVED | `pattern/plain-chart` | — | Bars: black fill on a 2px black baseline; value labels + Mon–Sun; frozen fixture values. | — |
| 13 | a calendar heatmap of the month | RESOLVED | `pattern/plain-chart` | — | Month grid, monochrome ramp (white · #F4F4F4 · pewter · black); today = 2px black border; plain legend. | — |
| 14 | a tiny sparkline trend of the last week | RESOLVED | `pattern/plain-chart` | — | 2px black polyline + 4px square markers over a 1px hairline; values written as plain text. | — |
| 15 | a big streak counter | UNDEFINED | — | declined-progress-ring-badges | Display numeral + word line in the ruled register (numeral 7, 'days in a row'). | data-adapted |
| 16 | an achievement badge for seven days | UNDEFINED | — | declined-progress-ring-badges | Ruled tile: numeral 7 + 'Seven-day run' + '7 of 7 days'. | data-adapted |
| 17 | a status label on track or slipping | RESOLVED | `component/status` | — | Word chips: 'On track' plain; 'Slipping' with a 2px black left rule; never colour. | — |
| 18 | a profile avatar photo | CONFLICT | `prohibit/imagery-pictograms` | declined-photographic-imagery | Conflict → initials plate 'AM'; no photo. | data-adapted |
| 19 | an icon for each ritual | UNDEFINED | — | declined-pictograms-and-tags | Ordinals 01–05 in the ruled register. | data-adapted |
| 20 | a toggle switch in settings | FALLBACK | `fallback/platform-controls` | — | Platform control with field styling, marked. | data-fallback [G6] |
| 21 | a slider for daily goal minutes | FALLBACK | `fallback/platform-controls` | — | Platform range input with field styling; plain readout. | data-fallback [G6] |
| 22 | a date picker for the log entry | FALLBACK | `fallback/platform-controls` | — | Native date input with field styling. | data-fallback [G6] |
| 23 | a number stepper for minutes | FALLBACK | `fallback/platform-controls` | — | Native number input + − / + outline square buttons. | data-fallback [G6] |
| 24 | a text field for the ritual name | RESOLVED | `component/field` | — | component/field: soft border, radius 4, label above (medium caps), blue glow focus. | — |
| 25 | a select for ritual category | UNDEFINED | — | — | Near-miss component/select (small fixed set of 4): native select squared like a field. | data-adapted |
| 26 | a checkbox for reminders | FALLBACK | `fallback/platform-controls` | — | Platform checkbox with field styling. | data-fallback [G6] |
| 27 | radio buttons for frequency | FALLBACK | `fallback/platform-controls` | — | Native radios, three options. | data-fallback [G6] |
| 28 | a text area for notes | UNDEFINED | — | — | Native textarea in the field idiom (multi-line). | data-improvised [G2] |
| 29 | tabs for today history achievements | UNDEFINED | — | — † | Declined; view switching = masthead active state (underlined medium). Precedent located by manual search. | data-adapted |
| 30 | a bottom navigation bar on mobile | RESOLVED | `component/masthead` | — | Masthead nav collapses to a plain row on narrow screens; no bottom bar. | data-adapted |
| 31 | a table of logged entries | RESOLVED | `component/ledger` | — | component/ledger: 2px header rule, medium caps labels, hairline rows, hover #F4F4F4; statuses inline. | — |
| 32 | pagination for older entries | UNDEFINED | — | declined-view-tabs-paging | Outline Previous/Next + plain 'Page n of m' readout; disabled at bounds. | data-adapted |
| 33 | a search box to filter rituals | FALLBACK | `fallback/large-selection` | — | Platform search input with field styling; filters ledger rows. | data-fallback |
| 34 | a small category tag | UNDEFINED | — | declined-pictograms-and-tags | Word label in a ruled chip (uppercase); no decorative tag. | data-adapted |
| 35 | drag to reorder rituals | UNDEFINED | — | — | Move up / Move down outline actions in the editor; drag not built. | data-improvised [G3] |
| 36 | an undo button after deleting | RESOLVED | `component/action` | — | Outline 'Undo' action inside the post-delete notice; restores the ritual. | — |
| 37 | a three-step onboarding wizard | UNDEFINED | — | — | In-page 3 steps with a 'Step n of 3' readout; Back/Next/Finish. | data-improvised [G4] |
| 38 | export the data as csv | UNDEFINED | — | — | Outline action; CSV built on the page (Blob), nothing leaves the page. | data-improvised [G5] |
| 39 | a dark mode theme | UNDEFINED | — | reversed-colourway-rejected | Declined; disabled control + ruled statement — the light register stands. | data-adapted |
| 40 | a celebration animation when checking off | UNDEFINED | — | declined-saving-and-celebration | Declined; static red ceremony accent (red bar + 'Logged'); no motion. | data-adapted |
| 41 | an illustration in the empty state | CONFLICT | `prohibit/imagery-pictograms` | dialog-empty-state-rejected, declined-photographic-imagery | Same empty state as #8: ruled statement; no illustration (imagery forbidden). | data-adapted |
| 42 | upload a photo for the ritual | CONFLICT | `prohibit/imagery-pictograms` | declined-photographic-imagery | Declined; a ruled statement replaces the upload control. | data-adapted |

† the kernel attached no precedent to ask 29; `search "tabs"` finds
`precedent/declined-view-tabs-paging` at 9.5 and its try-list was applied (see findings).

## Precedent try-lists — what the build actually did

- **progress ring declined** → *square meter* for progress (11); *numerals + ruled register*
  for the streak (15) and the seven-day achievement tile (16). No ring, no badge shapes.
- **saving / celebration / toasts declined** → saving = meter composition (10); check-off =
  **static red ceremony accent + ruled notice**, no animation (40, 6).
- **view tabs / paging declined** → masthead active state for view switching (29, 30);
  paging = outline buttons + plain readout (32).
- **pictograms & tags declined** → ordinals 01–05 (19); category as a word chip in the
  ruled register (34). No icons anywhere.
- **photographic imagery declined** → initials plate (18); ruled statement + one action for
  the empty state (8, 41); a written note where upload would sit (42). Zero `<img>` elements.
- **reversed colourway declined** → dark mode shown *declined* in Settings; light register
  stands (39).
- **dialog & empty state declined** → every generic flow stays in-page: details (5), empty
  state (8), onboarding (37). The **only** vessel is the recipe-driven destructive confirm
  (see reconciliation).

## Gaps filed (`.design-authority/gaps.jsonl`, via `da.py gap-add`)

6 gaps, only for genuinely uncodified elements (no canon, no fallback, no adjudicated route):

| ref | id | need |
|---|---|---|
| G1 | `gap/20261007-161226-738d5d` | a weekly summary band (aggregate counts for the week) on the Today view |
| G2 | `gap/20261007-161226-704118` | a multi-line text area for notes (multi-line field) |
| G3 | `gap/20261007-161226-c12b70` | a reorder mechanism for rituals (drag or an equivalent) |
| G4 | `gap/20261007-161226-eba05a` | a three-step onboarding flow (in-page steps with a plain readout) |
| G5 | `gap/20261007-161226-93c724` | export the data as CSV (action plus on-page file generation) |
| G6 | `gap/20261007-161226-225410` | canon controls for core settings: toggle, slider, stepper, date, checkbox, radio |

Not filed, deliberately: the ring/streak/badge/toast/motion/tabs/imagery asks (adjudicated
precedents already answer them), the category select (canon `component/select` covers small
fixed sets — the resolve miss is vocabulary, not substance), and the empty state (the
precedent's try-list *is* the composition). G6 is theme-level: six settings controls fall to
`fallback/platform-controls`, whose own constraint says "mark the improvisation and report a
gap"; one consolidated gap avoids six duplicates.

## Reconciliation notes & findings

1. **The confirm dialog (4) is the one vessel.** The recipe (`recipe/retire-confirm`,
   canon) names a dialog for the destructive confirm; the rejected proposal declined
   *canonising* dialog/empty-state *components* and says keep flows in-page. Reconciliation
   kept: the recipe's vessel exists (square sheet, 2px frame, black scrim 55%, instant —
   no elevation), its constraints are kept (slate verb button, never pre-focused, bilingual
   title), and **no generic modal/dialog component was built** — details, empty state,
   onboarding all stay in-page. Marked `data-adapted`; tension recorded here rather than hidden.
2. **Kernel observation — precedent attachment misses 3-letter stems.** Ask 29 (“tabs …”)
   received no precedent: `precedent_matches` requires shared single-word tokens of length
   ≥ 4, and “tabs” stems to “tab”. `search "tabs"` finds the precedent at 9.5. It was
   applied manually and the miss is recorded (no gap — the need is adjudicated).
3. **Phrase dilution above exact canon.** “a select for ritual category” scores 4.0 for
   `component/select` (single token `select` alone scores 9.0) and “a banner summarizing the
   week” scores 4.0 for `component/notice` (`banner` alone: 9.0). The select was built to
   canon in substance (marked); the banner-week ask differs in substance (a numeric summary
   surface) so it was improvised **and** filed as G1.
4. **Fallback rows get no precedent attachments** in this pack (they would be covered by
   the fallback itself). The pack's fallback constraint still asks for a gap report → G6.
5. **Square meter, no imagery, bilingual collapse** are the three system traits that bend
   the app hardest: the ring/heatmap idiom became a meter + grids; three imagery demands
   (avatar, illustration, upload) all collapsed to *words and rules*; bilingual pairs mark
   themselves `data-adapted` and stack over-under below 560px.
6. **Fixed fixtures:** charts freeze “last complete week” (25 · 20 · 0 · 25 · 20 · 35 · 20,
   = 145 min) and the sparkline is the last 7 days (25 · 20 · 35 · 20 · 35 · 55 · 45);
   today = 2026-10-07, meter 2 of 5. All exact values are asserted in the self-test.

## Marks (in-app traceability)

`◌` toggle (fixed corner, `#marks-toggle`) turns on dashed amber outlines + inline labels
for every non-canonical node, driven by the literal attributes:

- `data-improvised` — 6 nodes (week band, notes textarea, move up/down, onboarding, export)
- `data-adapted` — 21 nodes (ring→meter, spinner→meter, toast→notice, modal→in-page block,
  tabs/bottom-nav→masthead, pagination, streak, tile, icons→ordinals, tag, category select,
  initials plate, dark-mode row, ceremony accent, popup vessel, empty state, photo row,
  the four bilingual titles, save meter)
- `data-fallback` — 7 nodes (toggle, slider, date, stepper, checkbox, radios, search)

Every one of the 42 asks also carries at least one `data-el="<ask #>"` node (audit hook;
the self-test asserts coverage of 1–42).

## Self-test (headless Playwright + curl)

- Served with `python3 -m http.server 8483` (killed after the run).
- `curl` — `/`, `/app.css`, `/app.js`, `/fonts/Arimo-VF.ttf`: all **200**, no other requests.
- Playwright: **110/110 checks** (`_evidence/selftest.py`, report
  `_evidence/selftest-report.txt`): all views; exact chart values; status words + structure
  emphasis; ledger rules + paging + search; notice/undo/dialog flow (confirm not
  pre-focused); saving meter; ceremony accent; marks toggle (dashed amber + labels);
  bilingual pairs + <560px collapse; persistence across reload; empty state; CSV export;
  no shadows / no motion / no `<img>`; red only in the two ceremony nodes; **0 console
  errors, 0 page errors, same-origin only**.

## Independent verification (da_verify)

`tools/da_verify.py --pack packs/dominion` — 22 checks: **19 PASS · 3 REVIEW_REQUIRED · 0 VIOLATION**
(results: `_evidence/verification/dominion-verification.json`; mechanical surface: palette, radii,
shadows, imagery, bilingual pairing, red-status scan, floating surfaces).

## Files

- `index.html` · `app.css` · `app.js` · `fonts/Arimo-VF.ttf`
- `_evidence/resolves.jsonl` (42 raw resolve results) · `_evidence/probes.jsonl`
  (near-miss probes) · `_evidence/selftest.py` · `_evidence/selftest-report.txt`
- `.design-authority/gaps.jsonl` (6 gaps)
