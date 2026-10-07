# Cadence (v2 rebuild) — build notes against the LEADER Design Authority

- Authority: pack `leader` v0.1.0 (`packs/leader/`, snapshot marber.economist.com + economist.com live product)
- Workspace: `examples/cadence2-leader/` · Kernel CLI: `tools/da.py --pack packs/leader`
- Fonts: self-hosted from `docs/synthesis/leader/tile/fonts/` (Gelasio VF, Inter VF, Archivo Black). No network calls; data-URI SVG only.
- Files: `index.html`, `app.css`, `app.js`, `fonts/` (3×ttf) — 6 app files. `NOTES.md` (this report) and `.design-authority/gaps.jsonl` (gap store written by the kernel CLI) are outside the app bundle.
- Serve: `python3 -m http.server 8482` from this directory; self-tested at `http://127.0.0.1:8482/`.

## Outcome mix (42 elements)

| Outcome | Rows | Count |
|---|---|---|
| RESOLVED (CLI, direct artifact) | 1, 7, 9, 24, 28, 30, 33 | 7 |
| RESOLVED (via synonym search + inspect) | 2, 29 | 2 |
| COMPOSE (canonical parts, platform mechanism) | 38 | 1 |
| FALLBACK (routed; applied with constraints; marked) | 4, 5, 20, 21, 22, 23, 25, 26, 27, 37 | 10 |
| IMPROVISED (undefined → in-character invention; marked; gap filed) | 3, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19, 31, 32, 34, 35, 36, 39 | 17 |
| ADAPTED (spec ask overridden by pack constraint; marked; gap filed) | 6, 18, 40, 41, 42 | 5 |

Marks in DOM (boot state, all views): **30 nodes with `data-improvised`**, **4 with `data-adapted`**; with the log form open: 33 / 5. Mark labels are applied to one representative instance per repeated element (list rows) to keep the overlay legible.

## The 42 elements — decisions and provenance

| # | Element | Resolve phrase(s) → outcome | Implemented as (with mark note) |
|---|---|---|---|
| 1 | Primary button | "primary button for the main action" → **RESOLVED** `component/action` (states: primary = solid navy #2E45B8, radius ~8, white label) | `.btn.b-navy` ("Log a ritual", "Log ritual", "Save settings", "Begin"); hover to Chicago deep #141F52 |
| 2 | Secondary button + text link | resolve UNDEFINED → synonyms "outline button" (action@5.5), "underlined link" (action@5.5) → **RESOLVED via synonym**; states documented in the artifact ("secondary: 2px ink outline", "tertiary: underlined blue link") | `.btn.b-out` (2px ink outline), `.btn.b-txt` (underlined blue link, e.g. Close/Skip/Undo) |
| 3 | Delete a ritual permanently | "delete"/"remove action" UNDEFINED (only generic action matched) → **IMPROVISED** | Red solid verb rect "Delete" in the confirmation flow; trigger = ink-outline button with red label. Mark: `red verb rect (L-15)` — deck L-15 guidance (accepted destructive register), red as attention. |
| 4 | Confirmation dialog | → **FALLBACK** `fallback/ruled-panel` ("interstitials render as plain ruled panels in the page flow; no scrim, no motion") | Inline ruled confirmation panel below the detail panel: 2px top rule, consequence sentence ("Delete “Morning run”? Its log history is removed."), solid-red confirm + outline cancel; destructive never pre-focused (focus lands on "Keep"). Mark: `ruled panel; fallback`. Spec asked a dialog/overlay — NOT implemented as requested (policy: conflict → do not implement as requested); recorded here. |
| 5 | Modal with ritual details | → **FALLBACK** `fallback/ruled-panel` | In-flow detail panel below the ritual list: sparkline, streak, last-3 history, delete flow. No scrim/motion. Mark: `ruled panel; fallback`. Spec asked an overlay — adapted to ruled panel per fallback. |
| 6 | Toast "Logged ✓" | "toast notification saying logged" UNDEFINED → synonyms "toast"→notice@1.5, "feedback message"→notice@5.0 → **ADAPTED** | Ruled notice strip (2px ink left rule, terse copy, auto-dismiss ~2.8 s, no motion); `component/notice` explicitly documents *no toasts*. Mark: `toast → ruled notice`. |
| 7 | Banner summarizing the week | "banner summarizing the week" → **RESOLVED** `component/notice` (aliases include week-summary) | Ruled banner (2px ink top rule): "245 minutes across six days. Sunday stayed empty." + status tag |
| 8 | Empty state (no rituals) | UNDEFINED; synonyms ("empty state", "empty list", "no data") none → **IMPROVISED** | Ruled statement block + one outline action, no illustration (deck L-17); shown in Today when rituals = 0 (Delete all data) and in Achievements via the demo toggle. Mark: `deck L-17 ruled block`. |
| 9 | Error message under field | "error message under the field" → **RESOLVED** `component/field` ("error = small red line under the field") | `.field.invalid`: small 18×2px red line + red message under the field; clears on input/change |
| 10 | Loading spinner while saving | UNDEFINED; synonyms ("spinner", "loading", "indicator") none → **IMPROVISED** | Stepped meter (crisp rectangle track, London 85; red fill stepping 25→55→85→100 % over ~700 ms; "Saving" label). No motion, static-register (L-16/L-03). Mark: `stepped meter (L-16)`. |
| 11 | Circular progress ring | UNDEFINED at resolve; synonyms "progress ring"/"radial progress" → meter@4.0 → **IMPROVISED** | SVG ring: London-85 track, red arc (L-16 colours), sans readout "60 %" + "3 of 5 rituals done" |
| 12 | Bar chart of weekly minutes | UNDEFINED; synonyms none → **IMPROVISED** | 7 crisp ink rectangles, 2px ink baseline, sans values/labels; zero day = hairline stub. Mon–Sun = 45/30/60/25/50/0/35. |
| 13 | Calendar heatmap | UNDEFINED; synonyms none → **IMPROVISED** | October 2026 grid: 24px crisp cells shaded by London ramp steps (wash/line/mute/ink); Oct 7 = 2px red outline; legend Less→More |
| 14 | Tiny sparkline (last week) | UNDEFINED; synonyms none → **IMPROVISED** | Mini rectangle bars (7) in the detail panel; max value red |
| 15 | Big streak counter | UNDEFINED; synonyms none → **IMPROVISED** | "12" in Archivo Black 46/tracking −1 (display register for big statics, L-04/L-05) + sans "day streak" |
| 16 | Achievement badge (7 days) | UNDEFINED; synonyms none → **IMPROVISED** | Ruled tiles with glyph marks, serif name, EARNED/LOCKED tag; earned: First week / 10 days / Early bird / Century club; locked: 21 days / Perfect month |
| 17 | Status label (on track/slipping) | UNDEFINED; synonyms none ("state label" only hit hierarchy) → **IMPROVISED** | Rectangular tag, uppercase sans 11/0.06em (deck L-13); ink outline "On track", solid red "Slipping" — live: ≥60 % of today done = On track; drops below = Slipping |
| 18 | Profile avatar photo | UNDEFINED; synonyms none → **ADAPTED** | Monogram "S"/"A" in a 2px ink rounded square. No imagery in system (deck L-21: purposeful/story-bound; absence honest). Mark: `monogram (no imagery)`. Photo not implemented as requested — recorded. |
| 19 | Icon for each ritual | UNDEFINED ("glyph" only weak hit on shape-language) → **IMPROVISED** | Rhythm glyphs (deck L-08): black squares of graded size per ritual; crisp corners (glyph marks stay crisp per shape guideline) |
| 20 | Toggle switch in settings | → **FALLBACK** `fallback/platform-controls` (scope: toggle/switch) | Native `<input type=checkbox>` restyled as a switch on a leader field skin (2px ink / blue when on). Marked; gap filed. |
| 21 | Slider for daily goal | → **FALLBACK** `fallback/platform-controls` (slider) | Native range; 2px track (line), ink thumb, sans readout "30 min". Marked; gap filed. |
| 22 | Date picker | → **FALLBACK** `fallback/platform-controls` (date) | Native `input[type=date]` with field styling. Marked; gap filed. |
| 23 | Number stepper for minutes | → **FALLBACK** `fallback/platform-controls` (stepper) | Native number input + outline −/+ buttons (2px, radius 8). Marked; gap filed. |
| 24 | Text field (ritual name / name) | "text field for the ritual name" → **RESOLVED** `component/field` | 1px soft border, radius 8, sans field text, caps label above; focus adds no border highlight (a11y via L-23 red ring) |
| 25 | Select for ritual category | → **FALLBACK** `fallback/selection` ("small sets use a native select styled like a field") | Native select + field styling + crisp caret. Marked; gap filed. |
| 26 | Checkbox for reminders | → **FALLBACK** `fallback/platform-controls` (checkbox) | Native checkbox, 2px ink, radius 8, blue check; "Morning reminder" |
| 27 | Radio buttons for frequency | → **FALLBACK** `fallback/platform-controls` (radio) | Native radios, rounded-square, blue inner block; week starts Mon/Sun |
| 28 | Text area for notes | "text area for notes" → **RESOLVED** `component/field` | Field-styled textarea (min 84px, resizable) |
| 29 | Tabs (Today/History/Achievements/Settings) | resolve UNDEFINED → synonym "tab bar" → navbar@4.0 → **RESOLVED via synonym** | Top bar link row per `component/navbar`: sans links, active = blue underline, over the 2px ink bar rule |
| 30 | Bottom navigation bar (mobile) | "bottom navigation bar on mobile" → **RESOLVED** `component/navbar`; relocated to the bottom edge at ≤720px | Same link language, 2px ink top rule, active blue underline. Attendance note: positional relocation marked `navbar language at bottom edge (mobile)` (adaptation). |
| 31 | Table of logged entries | UNDEFINED; synonyms none → **IMPROVISED** | Editorial table per deck L-18: 2px ink header rule, sans-caps labels, hairlines, serif ritual names, sans numbers right-aligned, no zebra, red-95 row hover |
| 32 | Pagination for older entries | UNDEFINED; synonyms none → **IMPROVISED** | "Older entries"/"Newer" outline buttons + sans range readout ("1–8 of 24"), disabled at edges |
| 33 | Search box to filter rituals | "search box to filter rituals" → **RESOLVED** `component/navbar` ("crisp search rectangle with typing-cursor motif right") | Crisp rectangle (1px ink, radius 8) + static 2px typing-cursor motif; filters the ledger by date/ritual/category |
| 34 | Small category tag | UNDEFINED; synonyms ("tag", "chip", "category") none → **IMPROVISED** | Rectangular ink-outline tag, uppercase sans 11/0.06em (deck L-13); muted variant in the ledger |
| 35 | Drag to reorder rituals | UNDEFINED; synonyms none → **IMPROVISED** | Native HTML5 drag from a 2-bar glyph handle; drop indicator = 2px red rule (attention punctuation); order persists |
| 36 | Undo button after deleting | UNDEFINED; synonyms none → **IMPROVISED** | Ruled notice "Ritual deleted." + underlined blue "Undo" (tertiary action); restores at original index |
| 37 | Three-step onboarding wizard | → **FALLBACK** `fallback/ruled-panel` (wizard/onboarding in scope) | In-flow ruled wizard (replaces the page region): "Small rituals, kept daily." → "Pick your rituals" → "Set your goal"; Back/Next/Skip + 3 square dots; via "Replay intro". No scrim/motion. Mark: `ruled panel; fallback`. |
| 38 | Export CSV | UNDEFINED; synonyms none → **COMPOSE** | Canonical secondary action (`component/action`) + platform Blob download; exports Date,Ritual,Category,Minutes. Visual fully canonical, no mark. |
| 39 | Dark mode theme | UNDEFINED; synonyms none → **IMPROVISED** | Token inversion on `<html data-theme="dark">`: ink ground #1A1A1A, white text, London ramp darkened for rules/washes; red + Chicago blue families unchanged; blue text links switch to white text + blue underline where contrast fails. Mark: `token inversion`. |
| 40 | Celebration when checking off | UNDEFINED; synonyms none → **ADAPTED** | Instant glyph stamp (graded black squares, last red) beside the streak for ~1.6 s + ring step + notice. No bounce/spring/decorative motion (L-03). Mark: `instant stamp (no motion, L-03)`. |
| 41 | Illustration in empty state | UNDEFINED; synonyms none → **ADAPTED** | Declined as imagery (deck L-17/L-21); replaced by a rhythm-glyph mark. Mark: `glyph mark (no imagery)`. Not implemented as requested — recorded. |
| 42 | Upload a photo for a ritual | UNDEFINED; synonyms none → **ADAPTED** | Replaced by a "Ritual mark" glyph picker in the log form (choice persists to the ritual). No imagery in system. Mark: `mark picker (no imagery)`. Not implemented as requested — recorded. |

## Conflicts & adaptations (spec ask vs pack)

1. **Dialog / modal / wizard ("overlay")** — spec asks overlays; `fallback/ruled-panel` states there is no dialog canon and interstitials render as ruled panels **in the page flow**, no scrim, no motion. Implemented as in-flow ruled panels and marked; gaps filed (G13). This is the pack's explicit ruling — not implemented as requested (per policy: conflict → do not implement as requested; fallback applied).
2. **Toast** — spec asks a toast; the notice artifact documents "no toasts (none evidenced)". Implemented as a brief ruled notice strip; marked as adapted; gap filed (G1).
3. **Celebration "animation"** — interaction transitions are near-instant colour swaps; no decorative movement in UI chrome (L-03). Implemented as an instant glyph stamp + colour/step updates; marked adapted; gap filed (G9).
4. **Avatar photo / illustration / photo upload** — no imagery (deck L-21; empty state without illustration L-17). Monogram, glyph marks, and a mark picker used instead; marked adapted; gap filed (G4/G5).
5. **Dark mode** — undefined; invented as pure token inversion using only defined families (no invented hues). Where blue-on-dark contrast fails, links use white text + blue underline. Marked; gap filed (G9).
6. **Fixture date** — spec fixes "Tuesday, 7 October"; the real 2026-10-07 is a Wednesday. Rendered exactly as the spec string (fixtures), no correction applied.
7. **"No sugar" row** — the fixture defines no minutes; the row shows no duration and the ledger shows "—" in the minutes column (CSV leaves the field blank).

## Gaps filed (13 entries, kernel CLI, workspace `examples/cadence2-leader`)

| # | Gap id | Covers |
|---|---|---|
| G1 | `gap/20261007-154226-66f16d` | transient feedback: toast, loading spinner, undo |
| G2 | `gap/20261007-154217-3d0d81` | data-viz: ring, bar chart, heatmap |
| G3 | `gap/20261007-154217-c770d8` | motivation: sparkline, streak counter, badge |
| G4 | `gap/20261007-154217-e31e20` | empty state + imagery (illustration, photo upload) |
| G5 | `gap/20261007-154217-8f07c1` | identity marks: avatar, icon, category tag |
| G6 | `gap/20261007-154209-fa9121` | status label (on track / slipping) |
| G7 | `gap/20261007-154217-269a0a` | table + pagination |
| G8 | `gap/20261007-154217-1f8c67` | drag reorder + destructive delete |
| G9 | `gap/20261007-154217-a67ee7` | dark mode + celebration |
| G10 | `gap/20261007-154217-36d7fd` | toggle, slider, stepper (platform fallback) |
| G11 | `gap/20261007-154217-f27459` | date picker, checkbox, radio (platform fallback) |
| G12 | `gap/20261007-154217-ffce09` | select (selection fallback) |
| G13 | `gap/20261007-154218-bc2400` | interstitials: confirm, detail, wizard (ruled-panel routing) |

`python3 tools/da.py --pack packs/leader gaps --workspace examples/cadence2-leader` lists all 13 as `open`.

## Self-test recap (port 8482)

- **curl**: `/` 200, `app.css` 200, `app.js` 200, all 3 fonts 200 (local server, killed after testing).
- **Playwright DOM pass — 98 checks, ALL PASS** (fresh Chromium, `PLAYWRIGHT_BROWSERS_PATH=~/.cache/ms-playwright`, repo venv). Covered: fonts loaded (3 registers); 4 tabs + 4 bottom links; greeting/date/ring 60 %/readout/streak; check-off → ring 80 %, "Logged ✓" notice, celebration stamp; log form validation (ritual + minutes errors), autofill, ~700 ms loading state, success flow (ring 100 %); detail panel (7-bar sparkline, streak, history), delete confirm (cancel + confirm + "Ritual deleted." + Undo restore, destructive not pre-focused); drag reorder; History bars (exact fixture values), heatmap (35 cells, today outlined), ledger (8 rows, "1–8 of 25" after a logged entry, filter 5/5, pagination both ways); CSV download (header + 25 rows, spot-checked); Achievements tiles/badges/empty toggle; Settings validation + error clearing, dark toggle, "Saved." after loading; localStorage persistence across reload (name, theme, checks); wizard 3 steps + back/skip; marks toggle (dashed outlines + labels rendered, 30 improvised / 4 adapted nodes); delete-all → empty state → restore. **0 console errors / page errors.**
- **Mobile probe (390×844)**: bottom nav visible, top tabs hidden, 4 links 98px each (no overflow), content clears the fixed bar at scroll bottom (bottom 718 vs bar top 806), no horizontal scroll (scrollWidth 390 = innerWidth).
- **Design pass**: screenshots reviewed (14 files under `.hermes/cache/scratch/screens/`); fixes applied after review — shorter mark labels, collision-free distribution of list marks, crisper search rectangle, error-clearing on input, larger marks button.
- **Copy scan**: no exclamation marks, no emoji anywhere in rendered text (mandated ✓ and ◌ excepted); no network calls (data-URI SVGs only).

## Coverage analysis

- **Canonical coverage used**: actions (3 states), fields (input/textarea/error), notice (banner + feedback), navbar (top bar, tabs-by-synonym, bottom bar, search box), meter (extended radially), plus the guidelines/token sets: type registers (Gelasio/Inter/Archivo Black), type scale, colour roles (red punctuation, Chicago blue interactive, ink/white/London frame), shape radius 8 with crisp rules/hairlines, white ground + 2px rules, section rhythm (red caps label → serif head → muted standfirst), motion ≤0.15 s, focus ring (red, switched on fills).
- **The updated-pack lexicon/scope fixes that mattered**: `component/notice` week-summary aliases (banner resolved directly), `component/field` textarea/error aliases (both resolved), the fallbacks file routing platform controls / selection / ruled panels (everything the app needed beyond the 12 artifacts routed cleanly), and prohibitions (square interactive corners, emoji, exclamation marks, off-family colour, ambient glow, red reading backgrounds — all avoided).
- **Where the boundaries were**: 27 of 42 rows needed a fallback, an improvisation, or an adaptation; the pack's 12 artifacts cover actions, four form primitives, two feedback vessels, navigation/search, shape/motion/colour/type/surfaces/hierarchy guidelines. Everything chart-, list-, badge-, theming- and identity-shaped is absent — all filed as gaps (13 entries) rather than silently invented.
- **Marks**: every improvisation/adaptation is visible in-app via the fixed corner `◌` toggle (`body.show-marks`): dashed amber outlines + short labels; representative instances only where elements repeat.
- Quarantine respected: only `packs/leader/`, `docs/synthesis/leader/`, the kernel CLI, and this output directory were read; no prior `cadence*` build consulted; no git writes; no service restarts.
