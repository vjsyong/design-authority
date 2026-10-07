# Cadence (wink variant) — authority decision log

App: a personal ritual tracker ("Cadence") built as a stress-test consumer of the **wink**
Design Authority (pack `wink` v0.1.0, `packs/wink/`). Every decision below was produced by
`tools/da.py --pack packs/wink resolve "<phrase>"`, followed by the documented synonym-search
step for UNDEFINED outcomes. **wink is the only design source**: nothing outside
`packs/wink/` + `docs/synthesis/wink/` informed any visual value.

- Build: `index.html` + `app.css` + `app.js` + `fonts/` (3 self-hosted TTFs, copied from the source tile).
  All paths relative (app served under a subpath). No network calls; fixtures only.
- Marks: `data-improvised` (amber dashed outline + note label when `body.show-marks` is on,
  toggled by the fixed **◌** button). `data-adapted` supported for conflicts — **zero conflicts
  occurred**, so no `data-adapted` nodes exist.
- Gaps: filed to `examples/cadence-wink/.design-authority/gaps.jsonl` (16 total, verified via `da gaps`).

## The 42 elements

Legend — **R** resolved · **R\*** resolved via documented search step · **F** sanctioned fallback ·
**U** undefined → improvised in character, marked, gap filed. "Marked?" = carries `data-improvised`.

| # | element | outcome + cited id | searches tried (if U) | action taken | marked? | gap id |
|---|---------|--------------------|----------------------|--------------|---------|--------|
| 1 | primary button | R — `component/action-pill` (17.0) | — | Yellow pill, 1px ink ring; hover −4.875px + hard ink shadow (0 4.875px 0 0, zero blur) on spring curve `.cta` | no | — |
| 2 | secondary button + text link | R — `component/action-pill` (13.0, "~secondary button") | — | Secondary = outline pill (2px ink inset) per artifact; text link from Kale link role (W-R2 palette) → `.link` on the wizard Skip | no | — |
| 3 | delete a ritual permanently | U | "delete destructive" ∅ · "destructive action" (n/a) · "remove item" (n/a) | Destructive affordance: outline pill, `#BF4055` ring/label; requires confirmation | **yes** | `gap/20261007-145139-ad4b85` |
| 4 | confirmation dialog | U | "confirm dialog" ∅ · "dialog" ∅ · "are you sure" ∅ | Rounded white dialog on 35% ink scrim; consequence sentence; ink pill with concrete verb; never pre-focused | **yes** | `gap/20261007-145139-ad4b85` |
| 5 | modal with ritual details | U | "modal" ∅ · "overlay dialog" ∅ · "popup" ∅ | White 16px dialog vessel, warm shadow, 35% scrim; shared by detail/log/wizard | **yes** | `gap/20261007-145938-a0e2b0` |
| 6 | toast saying logged | U | "notice" ∅ · "toast message" ∅ · "inline notice" ∅ | Ink toast pill, bottom-centre, transient. Note: source layer prefers inline notices↔spec demanded a toast — tension recorded below | **yes** | `gap/20261007-145938-f646b2` |
| 7 | banner summarizing the week | U | "banner" ∅ · "band" ∅ · "summary strip" ∅ | Ochre band (band role), serif metrics ("proof by number" treatment) | **yes** | `gap/20261007-145938-f646b2` |
| 8 | empty state | U | "empty" ∅ · "empty state" ∅ · "nothing yet" ∅ | Parsnip panel + one warm sentence + one action pill | **yes** | `gap/20261007-145938-a9d93a` |
| 9 | error message under field | R\* — search "invalid field" → `component/field-select` (5.0) | — | Implemented the artifact's **invalid** state + `#BF4055` message copy (palette error role) | no | — |
| 10 | loading spinner | U | "loading" ∅ · "spinner" ∅ · "saving indicator" ∅ | In-flight arc in the submit button (yellow-on-dark / ink-on-light); used during the ~700 ms simulated saves | **yes** | `gap/20261007-145939-d19d36` |
| 11 | circular progress ring | U | "progress" ∅ · "meter" ∅ · "progress ring" (n/a) | SVG ring: parsnip track, yellow fill, ink "when complete" logic reused from progress conventions; % + count readout | **yes** | `gap/20261007-145939-d19d36` |
| 12 | bar chart (weekly minutes) | U | "chart" ∅ · "bar chart" (n/a) · "graph" ∅ | Yellow bars on parsnip tracks, ink labels; Saturday 0 = empty track | **yes** | `gap/20261007-145939-b6450a` |
| 13 | calendar heatmap | U | "heatmap" ∅ · "calendar" ∅ · "calendar grid" ∅ | Yellow opacity ramp over parsnip cells; legend Less→More | **yes** | `gap/20261007-145939-b6450a` |
| 14 | sparkline trend | U | "sparkline" ∅ · "trend line" ∅ · "tiny chart" ∅ | Ink polyline + yellow end-dot on a parsnip block (detail overlay) | **yes** | `gap/20261007-145939-b6450a` |
| 15 | big streak counter | U | "streak" ∅ · "counter" ∅ · "stat number" ∅ | Fraunces display number + sans label (display treatment for numbers); streak chips on rows use the same treatment | **yes** | `gap/20261007-145939-d6853d` |
| 16 | achievement badge (seven days) | R\* — search "badge" → `component/badge` (9.0) | "achievement badge" (4.0) · "seven day badge" (4.0) | Earned = yellow pill per artifact; **locked variant** (parsnip muted) improvised + marked | **yes** (locked only) | `gap/20261007-145939-d6853d` |
| 17 | status label (on track / slipping) | U | "status" ∅ · "status label" (badge 4.0, hierarchy 4.0) · "chip" ∅ | Word-first pill on badge geometry; states: parsnip neutral / yellow attention; state colours improvised + marked | **yes** | `gap/20261007-145939-d6853d` |
| 18 | profile avatar photo | U | "avatar" ∅ · "profile photo" ∅ · "user image" ∅ | Initials avatar (yellow circle, ink ring) — no photo assets exist to reproduce | **yes** | `gap/20261007-145939-cfe3c5` |
| 19 | icon per ritual | U | "icon" ∅ · "ritual icon" ∅ · "glyph" ∅ | Inline SVG line glyphs (ink stroke, round caps): runner/book/lotus/drop/guitar | **yes** | `gap/20261007-145939-cfe3c5` |
| 20 | toggle switch | F — `fallback/platform-controls` (scope: toggle, switch) | — | Native checkbox presented as a switch; field styling cues; marked per fallback constraint | **yes** | `gap/20261007-145939-088b69` |
| 21 | slider (daily goal) | U | "slider" ∅ · "range slider" ∅ · "goal slider" ∅ (not in fallback scope) | Native range styled: parsnip pill track, yellow thumb w/ ink ring; ink value readout | **yes** | `gap/20261007-145939-29cca4` |
| 22 | date picker | F — `fallback/platform-controls` (scope: date, picker) | — | Native date input with field styling (radius 8, 1px `#DEDDDC`, warm ink) | **yes** | `gap/20261007-145939-29cca4` |
| 23 | number stepper | U | "stepper" ∅ · "number input" → field-select (4.0) · "minutes stepper" ∅ | Composed: field input + −/+ outline pills (action-pill) | **yes** | `gap/20261007-145939-29cca4` |
| 24 | text field (ritual name) | R — `component/field-select` (13.0, "~text field") | — | Label + input per artifact; field serves the profile name ("Sam"). App spec has no ritual-name editor — noted below | no | — |
| 25 | select (category) | R\* — search "select" → `component/field-select` (9.0) | "dropdown" (9.0) · "category select" (4.0) | Native select, field styling radius 8 (pack-literal — see mismatch note on the source-layer "more rounded + serif" variant) | no | — |
| 26 | checkbox | F — `fallback/platform-controls` (scope: checkbox) | — | Native checkbox, ink/yellow check; used for the wizard ritual picker | **yes** | `gap/20261007-145939-088b69` |
| 27 | radio buttons | F — `fallback/platform-controls` (scope: radio) | — | Native radios (week starts Monday/Sunday) | **yes** | `gap/20261007-145939-088b69` |
| 28 | text area (notes) | U | "textarea" ∅ · "notes field" (field-select 4.0) · "multiline input" (4.0) | Field styling extended to a multiline box; no textarea canon → marked | **yes** | `gap/20261007-145939-399e5e` |
| 29 | tabs | R\* — search "tab bar" → `component/navbar` (4.0) | "tabs" ∅ · "segmented control" (fallback 2.0) | Navbar row as tab switcher; active item reuses the documented hover fill (#F3F3F3 rounded-rect); single row, never wraps | no | — |
| 30 | bottom nav on mobile | R — `component/navbar` (8.0) | — | White bar, dark links; collapses to a bottom bar <760px (placement adaptation — noted) | no | — |
| 31 | table of entries | R\* — search "table" → `component/ledger` (9.0) | "ledger" (9.0) · "entries table" (4.0) | `.ledger`: parsnip header, hairline rows, row hover tint | no | — |
| 32 | pagination | U | "pagination" ∅ · "pager" ∅ · "older entries" ∅ | Outline pill + "Showing 8 of 14" readout; append-older semantics | **yes** | `gap/20261007-145939-f88682` |
| 33 | search box | R\* — search "search input" → `component/field-select` (4.0) | "search box" ∅ · "filter" ∅ | Field input + magnifier glyph (glyph folds into the icon gap) | no | — |
| 34 | small category tag | U | "tag" → badge (9.0) · "category tag" (4.0) · "chip" ∅ | Badge geometry in a **neutral parsnip variant** (yellow stays reserved for emphasis) → variant marked | **yes** | `gap/20261007-145939-a6f9c7` |
| 35 | drag to reorder | U | "drag" ∅ · "reorder" ∅ · "drag handle" ∅ | Six-dot grip handle + ink drop indicator; HTML5 drag & drop | **yes** | `gap/20261007-145939-f88682` |
| 36 | undo after delete | U | "undo" ∅ · "undo button" (action-pill 4.0) · "restore" ∅ | Post-delete notice line + outline pill Undo (8 s window) | **yes** | `gap/20261007-145139-ad4b85` |
| 37 | three-step wizard | U | "wizard" ∅ · "onboarding" ∅ · "step by step" ∅ | Overlay: kicker → serif headline → sentence per hierarchy pattern; step dots; Back / Skip / Next | **yes** | `gap/20261007-145938-a0e2b0` |
| 38 | export CSV | U | "export" ∅ · "csv" ∅ · "download data" ∅ | Outline pill + client-side Blob download + toast | **yes** | `gap/20261007-145939-a69c21` |
| 39 | dark mode | F — `fallback/light-only` | — | No dark canon; implemented an ink-dominant theme **keeping ink/yellow roles**; marked per fallback constraint | **yes** | `gap/20261007-145939-f4c315` |
| 40 | celebration on check-off | U | "animation" ∅ · "celebration" ∅ · "confetti" ∅ | Restrained: check-button pop on the spring curve + toast + ring transition; reduced-motion respected; the (also improvised) check control carries this moment | **yes** | `gap/20261007-145938-f646b2` |
| 41 | illustration in empty state | U | "illustration" ∅ · "empty illustration" ∅ · "drawing" ∅ | Simple warm line art (sun/plant), no assets reproduced | **yes** | `gap/20261007-145938-a9d93a` |
| 42 | upload a photo | U → fallback by scope | "upload" ∅ · "photo upload" ∅ · "file" → `fallback/platform-controls` (2.5) | Native file input (the fallback's `file` scope), field-adjacent; marked | **yes** | `gap/20261007-145939-d651a0` |

**Tally: 4 R · 6 R\* · 5 F · 27 U = 42** (one of the 27 U's — #42 — lands on a scoped fallback found
via search). Marked: 33 element-types (70+ DOM nodes in default view). Gaps: 16.

## Self-test recap

Served from the repo root at `127.0.0.1:8481`, page loaded **under the subpath**
`/examples/cadence-wink/` (relative-path requirement exercised end-to-end).

- `curl`: html/css/js/ttf all `200`.
- Playwright (chromium, venv) — **pass 1: 46/46**, **pass 2: 19/19**:
  - tabs switch views (Today→History→Achievements→Settings), bottom bar mirrors them
  - onboarding wizard auto-opens on first run, closes via Skip; reopenable via "Replay intro"
  - check-off: ring 60% → 80%, toast "Logged ✓", check pop, status/hero readout update; uncheck reverts
  - one modal opens/closes (detail overlay: sparkline + mini history); Esc and scrim-click close
  - log form: stepper works; 700 ms spinner visible during save; toast after; validation error state
  - settings save: spinner + "Saved" toast; dark toggle applies; name validation error
  - destructive flows: confirm dialog (verb, never pre-focused) → delete → Undo restores; delete-all flow
  - pager 8→14 rows; search filters; CSV export path exercised (Blob, no network)
  - ◌ toggle: `body.show-marks` set, computed outline of marked elements = `dashed`, 70+ marked nodes
  - mobile 390px: top tabs hidden, bottom nav visible and functional
  - **zero console errors, zero page errors, zero external network requests**, both fonts load
- Screenshots recorded (scratch): `shot-today.png`, `shot-today-vp.png`, `shot-history.png`,
  `shot-marks.png`, `shot-mobile.png`. Server killed after the run.

## What the authority could not cover

The pack is a compact 12-artifact system (actions, type, colour, card, navbar, field,
ledger, badge + guidelines). A product-shaped app barely fits inside it: **only 4 of 42
elements resolve directly**, 6 more via the search step (badge family, ledger, field family,
navbar), 5 fall back, and **27 have no canon at all** (one of which finds a scoped fallback by
searching "file"). The uncovered zone is systematic, not
random — everything product-flavoured is missing: **overlays & confirmations, feedback/toasts,
empty states & illustration, all data-viz, counters & state badges, iconography & avatars,
all non-text form controls, list controls (pagination, drag), export, onboarding, dark mode,
motion beyond hover**. 16 gaps were filed to capture that surface.

Also noted: the pack declares `capabilities.validators: []` and ships no `validators.json`,
so `validate_implementation` has nothing to run against the build; `recipes.json` is empty,
so COMPOSE never fires.

## Mismatches & judgment calls (never forced)

- **Element 30 (navbar → "bottom navigation")**: resolve matched navbar at 8.0 on
  "navigation bar" tokens. Accepted as the nav component; the artifact governs appearance and
  single-row structure, not vertical placement — the mobile bottom collapse is an adaptation,
  left unmarked but recorded here.
- **Element 2 (text link)**: resolve covered the "secondary button" alias; the link part is drawn
  from the Kale link role (W-R2; source gestalt), not from a dedicated link artifact.
- **Element 6 (toast)**: the source layer explicitly prefers *inline* notices over floating
  toasts; the app spec *requires* a toast. Requested pattern implemented, but only as a **marked
  improvisation** — never presented as canonical; gap filed.
- **Element 25 (select)**: the source layer's review-directed "more rounded + serif field text"
  select treatment is not carried by the pack; the pack-literal field styling (radius 8) was used
  because the pack is authoritative. Flagged for the pack maintainers.
- **Element 24 (text field)**: phrase says "ritual name"; the app spec provides no ritual-name
  editor, so the field component serves the profile-name field ("Sam"). Recorded rather than
  invented extra UI.
- **Element 42 (photo upload)**: resolve returned UNDEFINED (no scope-token overlap); the scoped
  fallback was found through the search step ("file" → platform-controls). The fallback's own
  constraint to mark + report was honoured.
- **Element 9 (error message)**: no error artifact; search hit the field's "invalid" state,
  so the message treatment is a thin extension of that state with the palette error colour.
- **Marks mode cosmetics**: note labels on right-edge elements can clip at the viewport edge in
  annotation mode — cosmetic in a debug overlay, left as-is.

Policy applied throughout: undefined → fall back per project policy, **mark the improvisation,
report a gap**; conflict → don't implement as requested. No resolve outcome looked wrong against
this reading of the pack; nothing was forced. No consumer writes touched the pack.
