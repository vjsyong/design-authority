# Cadence — leader-variant demo · notes

**Authority:** pack `leader` 0.1.0 (Leader Interface System) — the only design source used.
**Policy applied:** undefined → improvise per project policy, mark the improvisation
(`data-improvised`), report a gap; conflict → do not implement as requested
(none occurred).
**Files:** `index.html` · `app.css` · `app.js` · `fonts/` (Gelasio, Inter, Archivo Black,
copied from the synthesis tile) — 6 build files, all paths relative, no network calls.
**Records:** gaps in `.design-authority/gaps.jsonl` (via `tools/da.py gap-add`).
Working logs (resolve/search JSON) captured during the build in
`~/.hermes/cache/scratch/cadence-leader/`.

Build decisions were driven by 42 `resolve` calls (one per element). Distribution:
**6 RESOLVED · 8 FALLBACK · 28 UNDEFINED · 0 CONFLICT**. Every UNDEFINED element had
2–3 synonym `search` queries run per the workflow. Resolved elements use the cited
artifact's exact values (inspected in `artifacts.json` / the Gate-2 sheet):
ink `#1A1A1A`, London `#666666 / #D9D9D9 / #F2F2F2`, Economist Red `#E3120B`
(punctuation only), Chicago blue `#2E45B8` actions / `#141F52` deep, radius ~8 on all
interactive + container surfaces, 2px ink rules + hairlines for separation, serif
(Gelasio) for story, sans (Inter) for apparatus, Archivo Black reserved for one
display moment (the streak numeral).

## The 42 elements

| # | Element | Outcome + cited id | Searches tried (if U) | Action taken | Marked | Gap |
|---|---------|--------------------|-----------------------|--------------|--------|-----|
| 01 | primary button (main action) | RESOLVED — `component/action` (17.0) | — | Solid `#2E45B8`, radius 8, white label (L-01) | — | — |
| 02 | secondary button + text link | RESOLVED — `component/action` (14.0) | — | 2px ink outline; underlined `#2E45B8` text link | — | — |
| 03 | delete a ritual permanently | UNDEFINED | delete permanently→–; destructive action→action@4.0; remove ritual→– | Solid red button with the verb; consequence sentence in confirm (sheet L-15 character) | yes | `gap/20261007-145916-deea1f` |
| 04 | confirmation dialog before deleting | FALLBACK — `fallback/ruled-panel` | — | In-flow ruled panel: 2px ink frame, hairline detail, no scrim, no motion; confirm never pre-focused | yes | `gap/20261007-145916-84338e` |
| 05 | modal with ritual details | FALLBACK — `fallback/ruled-panel` | — | Detail as ruled panel in page flow (sparkline, streak, mini history, delete) | yes | `gap/20261007-145916-84338e` |
| 06 | toast saying logged | UNDEFINED | toast→–; transient notification→notice@4.0; snackbar→notice@1.0 | Transient ruled notice-family readout (sheet L-14 says no toasts; not a pack prohibition) | yes | `gap/20261007-145916-0643c3` |
| 07 | banner summarizing the week | UNDEFINED (phrase scored notice@4.0 < 6.5) | banner→**notice@9.0** (alias hit); weekly summary→–; digest block→– | Implemented as `component/notice` via scoped search; phrase-level resolve missed the alias | yes | `gap/20261007-145916-0643c3` |
| 08 | empty state (no rituals) | UNDEFINED | empty state→–; nothing yet→–; first run state→– | Ruled statement block + one action, no illustration | yes | `gap/20261007-145916-d20922` |
| 09 | error message under the field | RESOLVED — `component/field` (18.0) | — | Small red line under the field on invalid submit / empty rename | — | — |
| 10 | loading spinner while saving | UNDEFINED | loading spinner→–; saving indicator→–; progress indicator→meter@4.0 | Stepped meter readout “Saving…” (~700 ms) — no spinner chrome, static-update character | yes | `gap/20261007-145916-7e2442` |
| 11 | circular progress ring (today) | UNDEFINED | circular progress→meter@4.0; ring gauge→–; completion readout→meter@4.0 | SVG ring in meter colours (grey track, red arc); kept circular per app spec — flagged against rectilinear character | yes | `gap/20261007-145916-1ae98e` |
| 12 | bar chart of weekly minutes | UNDEFINED | bar chart→meter@4.0/navbar@4.0; chart→–; data visualization→– | Rectilinear bars in Chicago 45 `#2E45B8` (city palettes = data accents); today marked with red cap + red label | yes | `gap/20261007-145916-1ae98e` |
| 13 | calendar heatmap of October | UNDEFINED | calendar heatmap→–; activity heatmap→–; month grid→– | Square cells on the London grey ramp; red outline on today | yes | `gap/20261007-145916-1ae98e` |
| 14 | sparkline (last week) | UNDEFINED | sparkline→–; trend line→noise@1.0; mini chart→– | Mini rectilinear columns, Chicago blue | yes | `gap/20261007-145916-878f7a` |
| 15 | big streak counter | UNDEFINED | streak counter→–; big number readout→meter@4.0; counter→– | Archivo Black numeral (the single rare display moment) + sans caps label | yes | `gap/20261007-145916-878f7a` |
| 16 | achievement badge (seven days) | UNDEFINED | achievement badge→–; badge→–; medal→– | Rounded badge tile, ink frame, rhythm glyph, Earned/Locked tag; locked = hairline + grey | yes | `gap/20261007-145916-d4706a` |
| 17 | status label (on track / slipping) | UNDEFINED | status label→hierarchy@4.0; state tag→–; progress status→meter@4.0 | Tag per sheet L-13: ink outline when on track, solid red when slipping | yes | `gap/20261007-145916-d4706a` |
| 18 | profile avatar photo | UNDEFINED | profile avatar→–; avatar photo→–; user image→– | Initials block — photo imagery absent from the system’s posture (no illustration either) | yes | `gap/20261007-145916-6a07a0` |
| 19 | icon for each ritual | UNDEFINED | ritual icon→–; icon→–; glyph marks→noise@1.5 | Rhythm-glyph squares per category (echoes the four rectangle registers) | yes | `gap/20261007-145916-6a07a0` |
| 20 | toggle switch in settings | FALLBACK — `fallback/platform-controls` | — | Native checkbox, leader field styling; blue when on (dark mode) | yes | `gap/20261007-145917-9146b6` |
| 21 | slider for daily goal | FALLBACK — `fallback/platform-controls` | — | Native range, leader-styled track/thumb | yes | `gap/20261007-145917-9146b6` |
| 22 | date picker for the log | FALLBACK — `fallback/selection` (via ‘picker’) | — | Native date input in field styling; dark `color-scheme` — routed by token, semantically a platform control | yes | `gap/20261007-145917-ca8e6c` |
| 23 | number stepper for minutes | UNDEFINED — scope miss (‘stepper’ not in any fallback scope) | number stepper→–; increment control→platform-controls@2.0; quantity input→field@4.0 | − / + outline buttons around a field-styled number input | yes | `gap/20261007-145916-0b2e49` |
| 24 | text field for the ritual name | RESOLVED — `component/field` (13.0) | — | Rename field in the detail panel (caps label, error line, no focus border highlight) | — | — |
| 25 | select for ritual category | FALLBACK — `fallback/selection` | — | Native select in field styling | yes | `gap/20261007-145917-ca8e6c` |
| 26 | checkbox for reminders | FALLBACK — `fallback/platform-controls` | — | Native checkboxes, leader box styling (radius 8, blue when checked) | yes | `gap/20261007-145917-5bb40b` |
| 27 | radio buttons (mapped: week start) | FALLBACK — `fallback/platform-controls` | — | Monday/Sunday radios; circular affordance kept | yes | `gap/20261007-145917-5bb40b` |
| 28 | text area for notes | UNDEFINED | textarea→–; multiline field→field@4.0; notes input→field@4.0 | Field styling extended to a textarea | yes | `gap/20261007-145916-0b2e49` |
| 29 | tabs (today history achievements) | UNDEFINED | tabs→–; tab bar→meter@4.0/navbar@4.0; segmented nav→navbar@4.0 | Tab row in navbar language (sans links, active blue underline); tab set includes Settings per app spec | yes | `gap/20261007-145917-4bf6e3` |
| 30 | bottom navigation bar (mobile) | RESOLVED — `component/navbar` (8.0) | — | Navbar styling kept; re-anchored as a fixed bottom dock ≤760px (extrapolation — see below) | — | — |
| 31 | table of logged entries | UNDEFINED | data table→–; ledger→–; entries table→– | Ledger per sheet L-18: 2px ink header rule, hairlines, serif names, sans numbers, red95 row hover, no zebra | yes | `gap/20261007-145917-4bf6e3` |
| 32 | pagination for older entries | UNDEFINED | pagination→–; pager→–; older entries→– | Ruled strip: sans meta + Newer/Older outline controls; disabled while filtering | yes | `gap/20261007-145917-4bf6e3` |
| 33 | search box to filter | RESOLVED — `component/navbar` (13.0) | — | Crisp search rectangle + red typing-cursor motif; filters the entries table | — | — |
| 34 | small category tag | UNDEFINED | category tag→–; label tag→hierarchy@4.0; chip→– | Small tag per sheet L-13 (caps sans, 2px ink outline, radius 8) | yes | `gap/20261007-145916-d4706a` |
| 35 | drag to reorder rituals | UNDEFINED | drag reorder→–; sortable list→–; reorder rows→– | HTML5 drag on rows, square-dot handle, order persisted; no added motion | yes | `gap/20261007-145917-125884` |
| 36 | undo button after deleting | UNDEFINED | undo→–; revert action→action@4.0; restore deleted→– | Ruled notice with Undo / Dismiss links; restores at the original position | yes | `gap/20261007-145916-deea1f` |
| 37 | three-step onboarding wizard | UNDEFINED — scope miss (‘wizard’/‘onboarding’ not in ruled-panel scope) | onboarding wizard→–; wizard steps→–; setup flow→ruled-panel@1.5 | Ruled panel in flow (no scrim, no motion), 3 steps, square step markers, Next/Back/Skip | yes | `gap/20261007-145916-84338e` |
| 38 | export the data as CSV | UNDEFINED | export csv→–; download data→–; data export→– | Client-side CSV blob download from History and Settings | yes | `gap/20261007-145917-d24275` |
| 39 | dark mode theme | UNDEFINED | dark mode→–; dark theme→–; night theme→– | Ink-ground theme repainted from the same tokens; red/blue roles held | yes | `gap/20261007-145917-f9b5a1` |
| 40 | celebration on check-off | UNDEFINED | celebration animation→motion@4.0; success moment→–; confetti→– | Stepped glyph reveal + red thread, ≤150 ms, no bounce/glow (motion character) | yes | `gap/20261007-145916-0643c3` |
| 41 | illustration in the empty state | UNDEFINED | illustration→–; drawing→–; empty state artwork→– | Deliberately omitted — no imagery/illustration in the system’s character; ruled text block only | yes | `gap/20261007-145916-d20922` |
| 42 | upload a photo for the ritual | UNDEFINED | upload photo→–; image upload→–; file input→field@4.0 | Field-styled file input; chosen file shows in a plain ruled frame, local only | yes | `gap/20261007-145916-6a07a0` |

Marked = carries `data-improvised` (36 of 42 elements; the ◌ button toggles dashed
amber outlines + note labels, per the briefing). No element ended as CONFLICT, so
`data-adapted` is unused (its styles exist). 42 marked DOM nodes appear at runtime —
the count exceeds 36 because repeated instances (each row glyph, each category tag)
carry the marker individually.

## Mismatches noticed (recorded, not forced)

- **07 banner** — the full phrase resolved UNDEFINED at 4.0 while the one-word synonym
  “banner” scored 9.0 (it is an explicit alias on `component/notice`). Not forced:
  implemented as notice after the scoped search, still marked, gap filed.
- **22 date picker** — routed to `fallback/selection` through the token ‘picker’;
  semantically a platform control. Same effective outcome (native element + field styling).
- **23 stepper** — ‘stepper’ appears in no fallback scope, so the pipeline says
  UNDEFINED even though a synonym search surfaces `fallback/platform-controls` at low
  confidence. Treated as a platform control manually and marked.
- **37 wizard** — an interstitial, but ‘wizard’/‘onboarding’ miss the ruled-panel
  scope; improvisation mirrored the fallback’s constraints anyway (in-flow, no scrim,
  no motion) and is marked.
- **30 bottom nav** — resolved to `component/navbar`, whose artifact describes a top
  bar; the app spec requires a mobile bottom dock. Styling kept per the artifact
  (white, 2px ink rule, sans links, blue underline); the placement is an unmarked
  extrapolation, listed in “undercarried” below.
- **06 toast** — the sheet layer says “no toasts”, but the pack carries no toast
  prohibition and resolve says UNDEFINED; implemented as notice-family readout, marked.
- The amber marks chrome (`#B7791F` family) is test-harness tooling, deliberately
  outside the brand palette; it never renders in normal mode.

## Self-test recap (port 8482, then server stopped)

- Serve: `python3 -m http.server 8482` in `examples/cadence-leader`; `curl` returned
  **200** for `/`, `app.css`, `app.js`, `fonts/Gelasio-VF.ttf`; title `Cadence`.
- Playwright (chromium, repo venv): **45/45 checks passed** —
  tab switching across all four views; log panel opens/closes; ritual detail panel
  opens (sparkline + delete present); **check-off updates the ring** (“3 of 5” → “4 of 5”,
  dashoffset 140.74 → 70.37) with toast “Logged ✓” and the celebration moment firing;
  settings save shows the ~700 ms saving state then toast “Saved”; dark toggle on/off;
  CSV export triggers a `cadence-entries.csv` download; **◌ toggles `body.show-marks`**
  (42 marked nodes, dashed outline + note label verified via computed style);
  pagination, badge empty-state toggle verified.
- Mobile pass (390×844): tabs fixed to the bottom edge (y 801–844), tab switching OK,
  body padding 66px, 0 console errors.
- **Zero console errors and zero page errors** in both runs.
- `da validate examples/cadence-leader`: the pack declares **no validators**, so the
  runner reports 0 findings (nothing to execute; not a pass signal to over-read).

## What the authority could not cover

17 gap reports filed (`gap-add`, kept ids above; grouped ≤3 related elements each):
destructive+undo · overlays/interstitials · feedback moments (toast/banner/celebration) ·
loading state · empty states+illustration · data-viz charts · data-viz trends/counters ·
labels/badges/tags · imagery/iconography/upload · stepper+textarea · tabs/table/pagination ·
drag-reorder · CSV export · dark theme · platform controls ×3 (switch+slider,
checkbox+radio, date+select).

Dominant themes: the pack is a component-and-guideline sampler (11 artifacts, 3 fallbacks,
5 prohibitions) with **no chart, no overlay canon, no imagery, no data-entry controls beyond
single-line fields, no empty/feedback/status patterns, and no theming**. The rectilinear
“rectangles are the geometry” character also directly conflicts with the spec’s circular
ring; the ring was kept (app spec wins on presence), styled from the meter artifact, and
flagged. The 6 resolved elements lean entirely on the action / field / navbar trio.
Three example ids: `gap/20261007-145916-1ae98e` (charts), `gap/20261007-145916-84338e`
(interstitials/wizard), `gap/20261007-145916-deea1f` (destructive+undo).

Undercarried, noted honestly: element 30’s bottom dock placement (styling resolved,
placement extrapolated); element 33’s filter box lives in History over entries rather
than over rituals; element 27’s “frequency” radios map to the week-start radios the app
spec defines; drag reorder has no keyboard affordance; dark-theme contrast on links is
the least-verified improvisation.
