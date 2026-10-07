# Cadence — dominion (REBUILD v2) — decision log

Demo app: **Cadence**, a personal ritual tracker (fixed spec), built as a fresh rebuild against
`packs/dominion/` (v0.1.0, Gate 2 closed) — the **only** design source. Prior cadence builds were
not consulted (quarantine respected). No git commits; no services restarted. All decisions below
come from `tools/da.py --pack packs/dominion` (42 resolve runs in `_evidence/resolve-out/`, synonym
searches in `_evidence/searches/search-log.txt`) plus `docs/synthesis/dominion/` style values.

Pack policy applied throughout: RESOLVED/COMPOSE → implement per cited artifact · FALLBACK →
apply constraints · UNDEFINED → improvise in character, mark, file gap · CONFLICT → do not
implement as requested; adapt + document.

## CLI outcome mix (42 elements)

| Outcome | n | Elements |
|---|---|---|
| RESOLVED | 6 | primary button (component/action), secondary+link (component/action), error message (component/field), text field (component/field), bottom nav → masthead (mismatch, see notes), undo (component/action) |
| COMPOSE | 2 | delete permanently, confirmation dialog (recipe/retire-confirm) |
| CONFLICT | 3 (+1 synonym) | avatar photo, illustration, photo upload (prohibit/imagery-pictograms) · + ritual icon (resolve UNDEFINED, synonym "pictogram" is a prohibition signal → treated as CONFLICT) |
| FALLBACK | 7 | toggle, slider, date picker, stepper, checkbox, radios (fallback/platform-controls) · search box (fallback/large-selection) |
| UNDEFINED | 24 | modal, toast, banner, empty state, spinner, ring, bar chart, heatmap, sparkline, streak counter, badge, status label, icon, select, textarea, tabs, table, pagination, tag, drag reorder, wizard, export CSV, dark mode, celebration |

Of the 24 UNDEFINED: select was **recovered by synonym search** (→ component/select, score 9.0);
ring was answered by search with the closest primitive (meter, score 4.0) and adapted; the other
22 were improvised in character (plain, structured, quiet) and marked; 14 gaps filed.

## 42-element decision table

Marks: I = `data-improvised`, A = `data-adapted`, F = `data-fallback` (◌ corner toggles the dashed-amber layer).

| # | Element | Outcome | Source cited | Built as | Mark | Gap |
|---|---|---|---|---|---|---|
| 01 | Primary button | RESOLVED | component/action (D-01) | Solid slate #26374A, radius 4, white label; one primary per view | — | — |
| 02 | Secondary button + text link | RESOLVED | component/action | 2px slate outline; tertiary = underlined black link | — | — |
| 03 | Delete a ritual permanently | COMPOSE | recipe/retire-confirm (D-14) | Detail → confirm dialog → removed from list + storage; Undo notice | — | — |
| 04 | Confirmation dialog | COMPOSE | recipe/retire-confirm | Square sheet, consequence sentence, verb button, never pre-focused, bilingual title | — | — |
| 05 | Modal with ritual details | UNDEFINED | none (D-18 doctrine used) | Square white sheet, 2px frame, black scrim 55%, instant | I | 3f77db |
| 06 | Toast saying logged | UNDEFINED | none (D-13: "no toasts") | Ruled notice box: 2px top rule, band ground, plain sentence "Logged ✓" | I | f085a0 |
| 07 | Banner summarizing week | UNDEFINED | none | Ruled banner (same vessel), one/two plain sentences, bilingual | I | f085a0 |
| 08 | Empty state (no rituals) | UNDEFINED | none (D-16 doctrine used) | Ruled statement + one action ("Restore rituals"); no imagery | I | 1d1c88 |
| 09 | Error under the field | RESOLVED | component/field | Left rule on input + plain sentence under (never red) | — | — |
| 10 | Loading spinner while saving | UNDEFINED | none (motion gated) | Words "Saving…" + disabled button de-emphasised to pewter outline, ~750 ms | I | 55f0a7 |
| 11 | Circular progress ring | UNDEFINED → search: meter 4.0 | component/meter (D-15) | Square meter (band track, black fill) + readout "3 of 5 · 60%"; ring geometry undefined, rectilinear doctrine wins | A | 55f0a7 |
| 12 | Bar chart of weekly minutes | UNDEFINED | none | Rectilinear bars: black fill on band track, value labels, Mon–Sun, 2px baseline | I | 8fb9eb |
| 13 | Calendar heatmap | UNDEFINED | none | Mon-start month grid, hairline cells, ink-density levels (grey, not colour) + word legend | I | 8fb9eb |
| 14 | Sparkline trend | UNDEFINED | none | Mini-bar trender (7 bars) above a 2px rule, in the detail overlay | I | 8fb9eb |
| 15 | Big streak counter | UNDEFINED | none | Ruled stat block: large numeral + "day streak · série" label | I | 196ed1 |
| 16 | Achievement badge (7 days) | UNDEFINED | none | Square ruled plate; earned = 2px black frame; locked = pewter hairline; status in words | I | 196ed1 |
| 17 | Status label (on track / slipping) | UNDEFINED | none (D-10 doctrine used) | Words in a ruled box ("On track · Dans les temps"); emphasis by structure, never colour | I | 196ed1 |
| 18 | Profile avatar photo | CONFLICT | prohibit/imagery-pictograms | **Adapted**: initials plate "S" + name in masthead | A | 3797fe |
| 19 | Icon for each ritual | CONFLICT (by synonym) | prohibit/imagery-pictograms | **Adapted**: ordinal markers 01–05 in ruled squares | A | 3797fe |
| 20 | Toggle switch (settings) | FALLBACK | fallback/platform-controls | Native checkbox squared, field styling, blue glow focus | F | e8407e |
| 21 | Slider for daily goal | FALLBACK | fallback/platform-controls | Native range, band track + hairline, square black thumb | F | e8407e |
| 22 | Date picker for log entry | FALLBACK | fallback/platform-controls | Native date input, field styling | F | ac9998 |
| 23 | Number stepper (minutes) | FALLBACK | fallback/platform-controls | Native number input + outline square − / + buttons | F | e8407e |
| 24 | Text field (ritual name) | RESOLVED | component/field (D-11) | Soft border 1px #E0E0E0, radius 4, label above in medium caps | — | — |
| 25 | Select for ritual category | UNDEFINED → search: select 9.0 | component/select (D-12) | Native select squared like a field; small fixed set | — | — (lexicon note) |
| 26 | Checkbox for reminders | FALLBACK | fallback/platform-controls | Native checkbox squared, field styling | F | ac9998 |
| 27 | Radio buttons | FALLBACK | fallback/platform-controls | Native radios, squared; used for week-start choice (spec's radio instance) | F | ac9998 |
| 28 | Text area for notes | UNDEFINED | none (field family extended) | Multi-line variant of the field (soft border, radius 4, glow focus) | I | 15c56c |
| 29 | Tabs (today/history/achievements) | UNDEFINED | none (masthead nav doctrine) | Plain row nav; active = medium + 2px black underline | I | 23f357 |
| 30 | Bottom navigation on mobile | RESOLVED → masthead (mismatch) | component/masthead + D-20 | **Not built as a bottom bar**: nav stays a plain top row, quiet collapse; mismatch documented | A | 23f357 |
| 31 | Table of logged entries | UNDEFINED | none (D-17 doctrine used) | Ruled register: 2px header rule, #C9C9C9 row hairlines, no zebra, row hover band | I | d03223 |
| 32 | Pagination (older entries) | UNDEFINED | none | Outline buttons ("Older/Newer entries") + plain readout "Showing 1–8 of 28" | I | d03223 |
| 33 | Search box to filter | FALLBACK | fallback/large-selection | Field-styled search input filtering the register | F | — (mark only) |
| 34 | Small category tag | UNDEFINED | none | Square hairline-bordered caps label (no fill) | I | ce60f0 |
| 35 | Drag to reorder rituals | UNDEFINED | none (motion gated) | **Motion-free**: "Move up / Move down" underlined controls in the detail overlay | A | ce60f0 |
| 36 | Undo button after deleting | RESOLVED | component/action (alias "undo") | Tertiary link "Undo · Rétablir" in the post-delete notice; restores item + its check state | — | — |
| 37 | Three-step onboarding wizard | UNDEFINED | none (D-18 doctrine used) | Square sheet, 3 steps, square dots + "Step n of 3", Next/Back/Skip | I | 3f77db |
| 38 | Export the data as CSV | UNDEFINED | none (action family) | Outline action button + client-side CSV download; ruled notice after | I | 15c56c |
| 39 | Dark mode theme | UNDEFINED | none (reversed colourway attested) | **Reversed**: black ground, white ink, rules invert, bands → rules-only, slate actions → white solid/outline; red stays ceremony | A | de23a9 |
| 40 | Celebration on check-off | UNDEFINED | none (motion gated) | Static ceremony beat: state changes + notice with the red identity accent for 1.8 s, then clears. No animation | A | de23a9 |
| 41 | Illustration in empty state | CONFLICT | prohibit/imagery-pictograms | **Adapted**: no imagery; plain ruled statement + one action (D-16 shape) | A | 1d1c88 |
| 42 | Upload a photo for a ritual | CONFLICT | prohibit/imagery-pictograms | **Adapted**: marker statement in the detail overlay — rituals are marked by number/initials | A | 1d1c88 |

## Conflict adaptations (documented, not implemented as requested)

1. **Avatar photo → initials plate** ("S" in a ruled square). Imagery prohibited; initials are the in-character identity device.
2. **Ritual icons → ordinals 01–05**. Pictograms prohibited; ordinals are structural, not illustrative.
3. **Illustration → ruled statement.** The empty state is a plain statement + one action, no decoration.
4. **Photo upload → marker statement.** No upload affordance; rituals carry number/initials markers.
5. **Progress ring → square meter** (searched: closest primitive is component/meter; D-02 "everything rectilinear").
6. **Celebration animation → static ceremony beat.** Motion is gated ("nothing animates decoratively"); the red identity accent appears for 1.8 s on the completion notice and clears. Red remains ceremony (never status/errors — errors are words + left rule).
7. **Drag-to-reorder → Move up/down controls.** Drag implies motion choreography; the answer is text controls.
8. **Bottom nav → plain top row nav** (D-20: nav collapses to a plain row; resolve mapped "navigation" to the masthead).
9. **Toast → ruled notice** (D-13: notices are ruled boxes, "no toasts").
10. **Dark mode → reversed colourway** applied wholesale (white-on-black is attested; "dark mode" as a feature is undefined).

## Gaps filed (14 entries; `.design-authority/gaps.jsonl`, via `da.py gap-add`, workspace `examples/cadence2-dominion`)

| Gap id (suffix) | Covers (elements) |
|---|---|
| 3f77db | overlay/sheet primitive — modal (05), wizard (37) |
| f085a0 | transient feedback + banner — toast (06), weekly banner (07) |
| 1d1c88 | empty-state pattern + image-free alternatives — empty (08), illustration (41), photo upload (42) |
| 55f0a7 | loading/saving indicator + non-linear completion — spinner (10), ring (11) |
| 8fb9eb | chart primitives — bars (12), heatmap (13), sparkline (14) |
| 196ed1 | stat/counter, badge plate, status label — (15, 16, 17) |
| 23f357 | tab navigation + mobile nav positioning — (29, 30) |
| d03223 | ruled register + pagination — (31, 32) |
| ce60f0 | tag/chip primitive + motion-free reorder — (34, 35) |
| de23a9 | theme modes + completion ceremony/motion — (39, 40) |
| 3797fe | image-free identity markers — avatar (18), icons (19) |
| 15c56c | multi-line field variant + export pattern — textarea (28), CSV export (38) |
| e8407e | platform fallbacks: toggle/slider/stepper — (20, 21, 23) |
| ac9998 | platform fallbacks: date/checkbox/radio — (22, 26, 27) |

All 14 open. 33 of 42 elements are covered by a gap; the 9 that are not (01–04, 09, 24, 25, 33, 36)
are resolved/compose/fallback elements whose needs the pack answers directly.

## Mismatches & lexicon notes (never forced)

- **Bottom navigation on mobile → resolved to component/masthead.** "navigation" is a masthead alias, and the masthead is a *top* bar. The spec element was not implemented as a bottom bar; the nav is a plain row (D-20). Gap filed; lexicon could distinguish positional variants.
- **"a select for ritual category" missed the resolve** but "select"/"dropdown" search finds component/select at 9.0 — implemented per artifact. Lexicon could add the phrase "select for…".
- **"an icon for each ritual" missed the prohibitions** although "pictogram" is a signal; treated as CONFLICT by synonym reasoning. Lexicon could add "icon" to the signals list.
- **"progress ring" search-suggests meter** (4.0); ring geometry is undefined — adapted, not forced.
- **"export csv", "dark mode", "banner", "toast", "pagination", "drag"** return no hits — improvised and gapped.

## Self-test recap (port 8483, local server; killed after)

- `curl`: index/css/js/font all 200 (font 496 KB, self-hosted Arimo VF; zero external requests recorded).
- **Playwright DOM pass: 93/93 checks passed** (`_evidence/selftest.py`, log in `_evidence/selftest.log`). Coverage includes: wizard on first visit + skip/replay; hero "3 of 5 … 60%" + meter width; check-off → ring update, `Logged ✓` notice in a 2px-ruled box, ceremony accent present; localStorage persistence across reload; detail overlay (sparkline 7 bars, mini history 5 rows, move reorder); delete → confirm (bilingual title, consequence sentence, confirm never pre-focused) → cancel → delete → Undo restores; log form (5 options, date input, stepper, minutes error under field) → ~750 ms saving state → "Logged ✓" + entry joins the register; History (banner 245 min, bars 45/30/60/25/50/0/35, 31-cell heatmap with 6 ink-density cells, 8-row ledger, pagination "1–8 of 28", search filter, CSV download `cadence-entries.csv`); Achievements (tiles 12/21/240, 6 badges 4 earned/2 locked, empty-state demo = statement + one action); Settings (name/week/slider/reminders, name error path, Saved ✓, dark ground rgb(0,0,0), Replay intro, delete-all confirm + reset to 3 of 5).
- Style-token checks: ground white, primary rgb(38,55,74) radius 4, 2px black rules, no box-shadow on cards, keyboard focus glow rgb(102,175,233), 500-weight headings, 1px bilingual divider.
- **No console errors, no external network requests.** Narrow viewport (480 px): bilingual pairs collapse over-under (divider hidden).
- Screenshots: `_evidence/screens/` (today, history, achievements, settings, detail, log form, wizard, marks layer, dark, narrow).

## Coverage analysis

- Every one of the 42 elements is implemented (none unplaceable); completeness preserved — nothing was dropped because the pack was silent: silent needs were improvised in character, marked, and gapped.
- Where the pack spoke (RESOLVED/COMPOSE/FALLBACK, 15 elements), it was followed literally: slate actions on radius 4, blue glow focus, soft field borders, the retire-confirm recipe, platform fallbacks under field styling.
- 22 improvised + 10 adapted + 7 fallback-marked surfaces render in the ◌ marks layer (dashed amber outlines + labels; DOM counts at test time: 17 `data-improvised`, 10 `data-adapted`, 12 `data-fallback` nodes — some elements repeat per row).
- Known deliberate deviations from a naive reading of the spec: no red anywhere except masthead accent + the 1.8 s ceremony beat (red is never status/error); no shadows/animations/radii beyond the web-layer 4 px; no imagery of any kind.

## Files

- App (5 files): `examples/cadence2-dominion/{index.html, app.css, app.js, fonts/Arimo-VF.ttf, NOTES.md}`
- Evidence: `examples/cadence2-dominion/_evidence/` (42 resolve outputs, search log, gap script, selftest + log, screenshots, workflow scripts)
- Gaps: `examples/cadence2-dominion/.design-authority/gaps.jsonl` (14 open)
