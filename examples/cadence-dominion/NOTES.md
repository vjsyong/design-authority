# Cadence — dominion variant · notes

App: **Cadence**, a personal ritual tracker (Today / History / Achievements / Settings), single-page
vanilla HTML/CSS/JS, self-hosted Arimo, no network calls. Built in `examples/cadence-dominion/`.

Authority: `packs/dominion` (Dominion Interface System, v0.1.0) + its own synthesis layer
(`docs/synthesis/dominion/`: gestalt, decisions D-01…D-22, refs/sheet.html, tile). Nothing else
was consulted. Design run date: 7 October 2026.

How the authority was applied: every element below was run through
`da.py --pack packs/dominion resolve "<phrase>"`; every UNDEFINED outcome also got a two-to-three
synonym `search` pass before deciding. Outcomes drive the build:

- **RESOLVED / COMPOSE** → implemented per the cited artifact.
- **FALLBACK** → fallback constraints applied (native element, field styling, blue-glow focus), marked, gap filed.
- **UNDEFINED** → improvised in the pack's character (plain, structured, quiet, static), marked, gap filed.
  Where `decisions.json` defines the pattern even though the resolver can't reach it (D-10, D-13, D-16,
  D-17, D-18), the decision was applied and the miss recorded (see *Resolver mismatches*).
- **CONFLICT** → **not implemented as requested**; adapted structurally in character, marked
  `data-adapted`, documented below.

Improv/adaption marks: every improvised element carries `data-improvised="<short note>"`, every
adaptation `data-adapted="…"`; the fixed corner button **◌** toggles `body.show-marks`, which draws
dashed amber outlines and the note label over them. (33 of the 42 elements are marked; resolver-found
and recipe-canonical elements are unmarked. Repeating row-level controls are marked once, on the first
instance.) 15 gaps were filed to `examples/cadence-dominion/.design-authority/gaps.jsonl`
(listed at the end of this file).

---

## The 42 elements

Legend — R = resolved (artifact id cited) · F = fallback · U = undefined · C = conflict ·
**Marked**: ✓I = `data-improvised`, ✓A = `data-adapted`, – = canonical/unmarked · Gap refs G1…G15.

| # | Element | Outcome | Searches (U only) | Action taken | Marked | Gap |
|---|---------|---------|-------------------|--------------|--------|-----|
| 1 | a primary button for the main action | R `component/action` | | solid slate `#26374A`, radius 4, white label; one primary per view ("Log a ritual", "Save settings", dialog verbs) | – | |
| 2 | a secondary button and a text link | R `component/action` | | 2px slate outline button; tertiary = underlined text button (Close, Skip, Dismiss, Undo) | – | |
| 3 | delete a ritual permanently | U | "delete remove an item permanently" → `recipe/retire-confirm` 14.0 | implemented per the recipe: confirmation dialog first, consequence sentence, verb on the slate confirm, never pre-focused; one-shot Undo afterwards | – | G15 |
| 4 | a confirmation dialog before deleting | U | "confirmation dialog destructive delete" → `recipe/retire-confirm` 9.0 | same recipe flow; used for both "Delete ritual" and "Delete all data" (bilingual titles per recipe) | – | G15 |
| 5 | a modal with ritual details | U | "modal dialog overlay details" → none | square white sheet, 2px black frame, scrim 55%, instant (per D-18); detail overlay with sparkline, streak, mini history, delete | ✓I | G12 |
| 6 | a toast notification saying logged | U | "toast notification message saved" → none useful | **adapted**: D-13 says *no toasts* — shipped as an in-flow ruled notice (2px black top rule, `#F4F4F4` ground, plain sentence: what happened + ring change), dismissible | ✓A | G14 |
| 7 | a banner summarizing the week | U | "banner summary week notice" → none | grey-band notice with bilingual key label "This week \| Cette semaine" + one plain sentence (245 minutes, 6 days, longest day) | ✓I | G14 |
| 8 | an empty state when no rituals exist | U | "empty state nothing yet blank" → none | plain ruled statement + one action, no imagery (per D-16); reused for filter-no-match and the achievements demo toggle | ✓I | G12 |
| 9 | an error message under the field | R `component/field` | | error = 2px black left rule + plain sentence under the field (D-11); wired to the Settings name field | – | |
| 10 | a loading spinner while saving | U | "loading busy saving progress waiting" → `component/meter` 4.0 | meter compose: "Saving \| Enregistrement…" readout + indeterminate black sweep inside the `#F4F4F4`/hairline track; ~700 ms; `prefers-reduced-motion` turns it static; used in log + settings flows | ✓I | G3 |
| 11 | a circular progress ring of today's completion | U | "progress ring circle completion" → `component/meter` 4.0 | ring composed from meter primitives (band disc + hairline, black arc, plain readout "60% / 3 of 5"); static — updates instantly, no tween | ✓I | G2 |
| 12 | a bar chart of weekly minutes | U | "bar chart minutes graph data" → none | black bars on a 2px black baseline, plain value labels, Mon–Sun labels | ✓I | G1 |
| 13 | a calendar heatmap of the month | U | "heatmap calendar month data" → none | month grid; heat = black/white/pewter grey ramp (no hue); today marked with a 2px black border; plain legend | ✓I | G1 |
| 14 | a tiny sparkline trend of the last week | U | "sparkline trend line chart" → none | 2px black polyline + 4px square markers above a 1px hairline baseline | ✓I | G1 |
| 15 | a big streak counter | U | "streak counter number days" → none | large numeral (Arimo 300/54) + bilingual label "day streak \| jours d'affilée" | ✓I | G2 |
| 16 | an achievement badge for seven days | U | "badge achievement seven days award" → none | ruled tile: name + state word ("Earned — date" / "Reach a 21-day streak"); locked = grey band + hairline + pewter text; no pictograms | ✓I | G2 |
| 17 | a status label on track or slipping | U | "status label on track slipping" → none useful | words, never colour (D-10): "On track" = 1px black box; "Slipping" = 4px black left rule + grey band + bold | ✓I | G13 |
| 18 | a profile avatar photo | **C** `prohibit/imagery-pictograms` | | **adapted**: squared initials block ("S") + name, 2px black frame — no photo | ✓A | G11 |
| 19 | an icon for each ritual | U | "icon pictogram symbol" → none | **adapted** (pictograms prohibited, D-22): ordinal marker "01"–"05" in a 2px black square; doubles as the drag handle | ✓A | G7 |
| 20 | a toggle switch in settings | F `fallback/platform-controls` | | native checkbox under a squared switch visual (2px black frame, square knob), field register, blue-glow focus; used for reminders + dark mode | ✓I | G4 |
| 21 | a slider for daily goal minutes | F `fallback/platform-controls` | | native range: hairline track on band, 16px square black thumb, plain "30 min" readout, blue-glow focus | ✓I | G5 |
| 22 | a date picker for the log entry | F `fallback/large-selection` | | native date input with field styling (1px `#E0E0E0`, radius 4) | ✓I | G5 |
| 23 | a number stepper for minutes | U | "number stepper increment minutes" → none | field-styled number input + two outline square buttons (− / +) | ✓I | G9 |
| 24 | a text field for the ritual name | R `component/field` | | field per D-11 (soft border, radius 4, label above in medium caps) — the Settings name field | – | |
| 25 | a select for ritual category | U → search | "select dropdown category choice" → `component/select` 12.0 | native select styled like a field (D-12 small fixed set) | – | |
| 26 | a checkbox for reminders | F `fallback/platform-controls` | | reminders use the native checkbox under switch styling; literal native checkboxes also used in the intro's "Pick your rituals" step | ✓I | G4 |
| 27 | radio buttons for frequency | F `fallback/platform-controls` | | native radios, squared 18px (black ring; dot = inner band ring), week starts Monday/Sunday | ✓I | G4 |
| 28 | a text area for notes | U → search | "text area notes multiline input" → `component/field` 8.0 | textarea with the field styling (D-11) | – | |
| 29 | tabs for today history achievements | U | "tabs views switch sections" → none useful | ruled tab row per the D-08 nav idiom; active = medium weight + 2px underline | ✓I | G6 |
| 30 | a bottom navigation bar on mobile | R `component/masthead` | | the same nav in a plain row; under 760px it docks to the bottom (2px black top rule) with EN over FR (D-20 collapse) | – | |
| 31 | a table of logged entries | U | "table rows register entries ledger" → none | ledger per D-17: 2px black header rule over medium caps labels, 1px pewter row hairlines, no zebra, row hover = band | ✓I | G13 |
| 32 | pagination for older entries | U | "pagination older entries next page" → none | outline square buttons (Older/Newer entries) + plain readout "Page 1 of 2" | ✓I | G6 |
| 33 | a search box to filter rituals | F `fallback/large-selection` | | native search input with field styling; filters the entries ledger; empty state when nothing matches | ✓I | G5 |
| 34 | a small category tag | U | "tag chip label small" → none useful | caps micro-label, 1px black rule, square (D-10 label idiom); streak chip = same in hairline grey | ✓I | G7 |
| 35 | drag to reorder rituals | U | "drag reorder move list sort" → none | native row drag with a plain drop target + Alt+Arrow keys on the marker; order persists | ✓I | G8 |
| 36 | an undo button after deleting | U | "undo revert restore" → none | underlined "Undo" inside the ruled notice (one-shot): restores a deleted ritual, or the full state after "Delete all data" | ✓I | G8 |
| 37 | a three-step onboarding wizard | U | "onboarding steps wizard setup intro" → none | 3-step sheet: Welcome → Pick your rituals → Set your goal; step dots as small squares; Next/Back/Skip; replayable | ✓I | G10 |
| 38 | export the data as csv | U | "export download csv data" → none | client-side Blob download `cadence-entries.csv` (no network); in History and Settings | ✓I | G10 |
| 39 | a dark mode theme | U | "dark mode reversed colourway theme" → none | the reversed colourway: black ground, white rules/text, inverted grey ramp, white-on-black primary button; FIP red stays ceremony-only; blue focus glow kept | ✓I | G10 |
| 40 | a celebration animation when checking off | U | "celebration animation check off done" → none | 900 ms **reversed row** (white-on-black, the system's colourway inversion) then an instant settle to the static checked state — no keyframes, no easing; plus the Logged notice | ✓I | G3 |
| 41 | an illustration in the empty state | **C** `prohibit/imagery-pictograms` | | **adapted**: plain ruled statement + one action (D-16) — imagery absence is a system property | ✓A | G11 |
| 42 | upload a photo for the ritual | **C** `prohibit/imagery-pictograms` | | **adapted**: no upload; the written note carries the record (imagery is not licensed anywhere in the system) | ✓A | G11 |

Two elements outside the 42 were also marked while building: the **ritual check control**
(composed from action + field primitives; no check control is defined) and the **stat tiles** on
Achievements (ruled headline figures). Both appear in gaps G4 / G2 respectively.

## Resolver mismatches (noted, never forced)

- `delete a ritual permanently` and `a confirmation dialog before deleting` returned **UNDEFINED**
  although `recipe/retire-confirm` exists and covers them; **search** found it (14.0 / 9.0). Implemented
  per the recipe; the resolve miss is recorded in gap G15. The phrase "remove an item" matches; the
  phrase "delete a ritual" apparently doesn't cross the direct-match threshold.
- `a modal with ritual details`, `an empty state…`, `a status label…`, `a table of logged entries`
  returned **UNDEFINED** although decisions D-18 / D-16 / D-10 / D-17 define these patterns exactly.
  They live in `decisions.json` but are not in the artifact catalogue, so the resolver cannot cite them.
  Implemented per the decisions; recorded in gaps G12 / G13.
- `a toast notification saying logged` returned UNDEFINED; the pack's reading (D-13: "Notices = ruled
  boxes … no toasts") makes the request a deviation, so it is treated as an adaptation (notice vessel)
  and recorded in G14.
- `a select for ritual category` and `a text area for notes` missed on resolve (4.0 — just under
  threshold) but were found by search (`component/select` 12.0, `component/field` 8.0) and implemented
  as canonical.
- `a bottom navigation bar on mobile` resolved to `component/masthead` — the nav idiom; the bottom
  placement on narrow screens follows D-20's plain-row collapse.

## Conflict adaptations (all five)

| Requested | Request conflicts with | Shipped instead |
|---|---|---|
| profile avatar photo | `prohibit/imagery-pictograms` (D-22) | squared initials block + name |
| icon for each ritual | D-22 pictograms prohibited | ordinal marker 01–05 in a 2px black square (also the drag handle) |
| illustration in the empty state | `prohibit/imagery-pictograms` | plain ruled statement + one action (D-16) |
| upload a photo for the ritual | `prohibit/imagery-pictograms` | written note is the record; no upload control |
| toast notification | D-13 "no toasts" | in-flow ruled notice (2px black top rule, band ground), dismissible |

## What the authority could not cover

- **Data visualisation** — no chart/heatmap/sparkline primitives; composed monochrome structure
  (black fills, hairlines, grey ramp) and flagged (G1).
- **Progress & achievement display** — the meter is the only progress element; the ring, streak
  counter and badge tiles are composed interpretations (G2).
- **Transient feedback & motion** — D-15 gates motion ("static only") but the app needs a saving
  state and a check-off moment; one functional sweep + one colourway-inversion celebration, both
  marked (G3).
- **Platform controls** — the fallback exists (native + field styling) but the fallback itself
  requires marking + gap reporting; six control types ride on it (G4, G5).
- **Navigation & repeated-content affordances** — tabs, paging, row markers, drag/reorder, undo,
  stepper: all outside the catalogue, improvised in the ruled register idiom (G6–G9).
- **App-level patterns** — no onboarding, export, or theme patterns; dark mode was composed from the
  system's own reversed colourway (G10).
- **Imagery** — the system licenses none, so three requested surfaces were structurally adapted
  (G11).
- **Catalogue vs decisions** — several accepted decisions (D-10, D-13, D-16, D-17, D-18) are not
  catalogued artifacts, so common needs resolve UNDEFINED; and one recipe is unreachable from its own
  natural phrasing (G12–G15).

## Self-test (7 October 2026)

Served at `python3 -m http.server 8483` from `examples/cadence-dominion/`; `curl` returned 200 for
index.html, app.css, app.js, fonts/Arimo-VF.ttf (19 KB / 24 KB / 33 KB / 496 KB). Playwright
(Chromium, DOM pass; server killed afterwards):

- **Pass 1 — 60 checks, 0 failed.** Tab switching (4 views); check-off updates the ring 60% → 80% +
  celebration class applied + "Logged ✓" notice; check click does not open the detail overlay; ◌
  toggle works (34 marked nodes on Today); detail modal opens with sparkline + mini history; log
  modal opens, shows the saving state, closes, persists an entry (9 rows on History, 60 → 80%);
  charts (7 bars), heatmap (34 cells), ledger (8 fixture rows + filter/no-match/clear), pagination
  page 1↔2, banner, export present; achievements (6 badges, 2 locked, empty-state toggle round-trip);
  settings (dark toggle on/off, error under empty name, saving state, "Saved" notice); wizard 3 steps
  and close; destructive confirm opens with focus NOT on the confirm button (sheet focused, D-14),
  delete → 4 rows, Undo → 5; bottom nav is `position:fixed` under 760px; **zero console errors, zero
  page errors, zero failed requests**.
- **Pass 2 — computed styles, 11 checks, 0 failed.** Arimo loaded (400 + 500); **no external
  requests** (all local/data:); primary button `rgb(38,55,74)`; masthead rule `2px rgb(0,0,0)`;
  dark mode ground `#000` / text `#fff` / primary inverted to white; ◌ marks = `dashed rgb(217,119,6)`
  outline with note labels, adaptations in deep amber `rgb(124,45,18)`; keyboard focus shows the blue
  glow (`rgba(102,175,233,.6) 0 0 8px` + `1px rgb(102,175,233)` outline).

**Total: 71 checks, 0 failed.** One UI bug was found and fixed during testing (`display:grid`
overriding `[hidden]` on the badge grid; a global `[hidden]{display:none!important}` rule now
guards all view/overlay toggles).

## Files

```
examples/cadence-dominion/
├── index.html            all views, dialogs, marks button (relative paths only)
├── app.css               tokens + components; dark = reversed colourway; marks overlay
├── app.js                fixtures, state (localStorage), renderers, interactions — no network
├── fonts/Arimo-VF.ttf    self-hosted, copied from docs/synthesis/dominion/tile/fonts/
├── NOTES.md              this file
└── .design-authority/    CLI-managed gap records (15 gaps, gaps.jsonl)
```

Fixture notes: the date renders "Tuesday, 7 October" exactly as specified in the brief (the civil
calendar puts 7 October 2026 on a Wednesday — the brief's fixture was followed verbatim; the heatmap
grid is drawn consistently with it: October starts Wednesday in a Monday-first grid). Weekly chart
Mon–Sun = 45/30/60/25/50/0/35; heatmap days 1–7 = 55/40/70/0/45/30/30; stats 12/21/240; 16 logged
entries across two pages; check-off, logged entries, order, settings and dark mode persist in
`localStorage` under `cadence-dominion-v1`; "Delete all data" clears it with a one-shot undo.

## Gap records (15) — examples/cadence-dominion/.design-authority/gaps.jsonl

| Ref | Scope | Gap id |
|-----|-------|--------|
| G1 | data-viz | gap/20261007-150030-0a71f9 |
| G2 | progress-display | gap/20261007-150030-05534a |
| G3 | feedback-motion | gap/20261007-150030-b20a90 |
| G4 | platform-controls (binary/choice) | gap/20261007-150030-06610b |
| G5 | platform-controls (inputs) | gap/20261007-150030-2eb8c6 |
| G6 | navigation | gap/20261007-150030-e4273f |
| G7 | row-markers | gap/20261007-150031-19b53c |
| G8 | list-management | gap/20261007-150031-842aa2 |
| G9 | forms (stepper) | gap/20261007-150031-f3d993 |
| G10 | app-level-patterns | gap/20261007-150031-0d3443 |
| G11 | imagery | gap/20261007-150031-b18038 |
| G12 | catalogue-coverage (dialog, empty) | gap/20261007-150031-6d60dd |
| G13 | catalogue-coverage (status, ledger) | gap/20261007-150031-f5a96f |
| G14 | feedback (toast, banner) | gap/20261007-150031-13d338 |
| G15 | resolution (destructive flow) | gap/20261007-150031-1eb3c0 |
