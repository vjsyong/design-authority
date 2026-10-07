# Cadence v2 — rebuild notes (authority: `packs/wink` @ wink 0.1.0)

**Experiment:** verify the updated wink Design Authority by rebuilding the *Cadence* demo app (ritual tracker) from scratch.
**Workspace:** `examples/cadence2-wink/` · **Date:** 2026-10-07 · **Built:** vanilla HTML/CSS/JS, self-hosted fonts, zero network calls.

**Sources used (quarantine respected):** `packs/wink/` (the only design authority) · `docs/synthesis/wink/` for *style values only* (tile, decision sheet, `decisions.json`, fonts) · kernel CLI (`tools/da.py`) · this output dir. No prior cadence builds, other packs, other examples, or skill files were consulted.

**Policy applied:** `undefined → improvise in character, mark it, report a gap` · `conflict → do not implement as requested` · never present improvisation as canonical.
- `resolve` outcomes cite **pack artifact ids** (kernel CLI).
- Where the pack is silent, in-character improvisation borrows **style values** from `docs/synthesis/wink/` and is marked `data-improvised` (+ gap).
- Deviations from a cited artifact are marked `data-adapted` (+ gap).
- No `CONFLICT` outcome occurred; no requested element collided with a prohibition.

---

## 1. Decision log — the 42 elements

43 `resolve` calls were run (element #2 is "secondary button **and** a text link" → two phrases). Outcomes: **RESOLVED 5 · FALLBACK 8 · UNDEFINED 30 · CONFLICT 0 · COMPOSE 0**.

`∅` = no hits. Scores are the kernel's reported evidence scores. Marked = `data-improvised` (improvised) / `data-adapted` (adapted) as shipped.

| # | Element | Outcome + id | Searches (UNDEFINED only) | Action | Marked | Gap |
|---|---------|--------------|---------------------------|--------|--------|-----|
| 1 | Primary button (main action) | RESOLVED `component/action-pill` (17.0) | — | `.cta` yellow pill + 1px ink ring; dark variant on the yellow hero; hover −4.875px + hard ink shadow (W-03); focus = 3px yellow ring (W-25) | — | — |
| 2a | Secondary button | RESOLVED `component/action-pill` (13.0) | — | Outline pill: 2px ink inset ("New ritual", "Export CSV") | — | — |
| 2b | Text link | UNDEFINED (alternatives: field-select, ledger, colour) | `link` → ledger 1.5 / navbar 1.5 / colour 1.5; `hyperlink` ∅; `inline link` → ledger 3.0 | Implemented per cited artifacts: content links = **Kale** (colour role) with underline; ledger-context links ink+underline. Kale-vs-ink tension flagged below (never forced) | — | — |
| 3 | Delete a ritual permanently | UNDEFINED (∅) | `delete` ∅; `remove` ∅; `destructive action` → action-pill 4.0 | Improvised: outline pill in error ink (`#BF4055` role), routed through the confirm dialog; undo grace via toast after deletion | improvised | G1 |
| 4 | Confirmation dialog before deleting | UNDEFINED (∅) | `dialog` ∅; `confirm` ∅; `alert box` ∅ | Improvised per W-16/W-17 primitives: white 16px card, 48px padding, scrim `rgba(35,30,21,.35)`, consequence sentence, confirm = ink pill with concrete verb ("Delete ritual"), cancel = outline ("Keep it"), destructive never pre-focused | improvised | G1 |
| 5 | Modal with ritual details | UNDEFINED (∅) | `modal` ∅; `overlay` ∅; `dialog` ∅ | Improvised: W-17 vessel at radius 24, instant appearance (no motion invented), contains sparkline + streak + mini history + delete | improvised | G1 |
| 6 | Toast notification "logged" | UNDEFINED (∅) | `notification` ∅; `snackbar` ∅; `toast message` ∅ | Improvised as a transient notice (W-15 form: rounded 12, tinted Parsnip fill, plain copy) → "Logged ✓ — Morning run, 30 min." **Tension flagged:** W-15 prefers *inline* notices and records no toast pattern; implemented because the demo requires it — marked, not canon | improvised | G2 |
| 7 | Banner summarizing the week | UNDEFINED (∅) | `banner` ∅; `notice band` → shape-language 1.5 / colour 1.5; `callout` ∅ | Improvised per colour role: ochre band (section-band terminator), square chrome, Fraunces number — "245 minutes this week" | improvised | G3 |
| 8 | Empty state (no rituals) | UNDEFINED (alternatives: card, ledger, navbar) | `empty state` ∅; `zero state` → action-pill 1.0; `nothing here` ∅ | Improvised per W-19: Parsnip panel, one warm sentence, one action pill; reused in Achievements (demo toggle) and Today (when the list empties) | improvised | G6 |
| 9 | Error message under the field | UNDEFINED (alternatives: field-select 5.0, colour, action-pill) | `validation error` → colour 1.5; `form error` → field-select 4.0; `invalid field` → field-select 5.0 | Implemented per cited artifacts: field `.invalid` state + `#BF4055` border/message (W-12 message styling), non-blaming copy | — | — |
| 10 | Loading spinner while saving | UNDEFINED (∅) | `spinner` ∅; `loading indicator` ∅; `busy` ∅ | Improvised: 16px ink ring spinner inside the button; ~700 ms simulated save on log/save/add; W-18's "spinner-only rejected" applies to multi-step progress, noted | improvised | G10 |
| 11 | Circular progress ring (today) | UNDEFINED (alternatives: action-pill 1.5, shape-language 1.5) | `progress ring` → action-pill 1.5; `progress indicator` ∅; `circular gauge` ∅ | Improvised: W-18 roles in circular geometry — Parsnip track, yellow in flight, ink when complete, text readout "3 of 5" | improvised | G4 |
| 12 | Bar chart (weekly minutes) | UNDEFINED (navbar 4.0 via "bar") | `bar chart` → navbar 4.0; `chart` ∅; `graph` ∅ | Improvised: yellow bars, ink value labels, today ringed; zero-day shown as a grey stub | improvised | G3 |
| 13 | Calendar heatmap (month) | UNDEFINED (∅) | `heatmap` ∅; `calendar grid` ∅; `activity grid` ∅ | Improvised: yellow alpha levels only (no new hues), today ringed, tooltips per day | improvised | G3 |
| 14 | Tiny sparkline (last week) | UNDEFINED (∅) | `sparkline` ∅; `line chart` ∅; `mini chart` ∅ | Improvised: ink polyline + yellow end dot, in the detail overlay | improvised | G5 |
| 15 | Big streak counter | UNDEFINED (hierarchy 1.5 via "number") | `streak` ∅; `counter` ∅; `stat number` → hierarchy 1.5 | Improvised: display-number treatment, which is sanctioned ("numbers may take display treatment") → Fraunces "12" + "day streak" | improvised | G4 |
| 16 | Achievement badge (7 days) | UNDEFINED phrase; synonym hit | `achievement badge` → badge 4.0; **`badge` → component/badge 9.0**; `reward` ∅ | Badge form cited (pill/emphasis language) → medallions for earned badges; locked variant + grid improvised | improvised | G5 |
| 17 | Status label (on track / slipping) | UNDEFINED (near: ledger 3.0 via "status pill") | `status pill` → action-pill 4.0 / shape 4.0 / ledger 3.0; `status` → ledger 1.5; `state label` → badge 4.0 | Improvised per W-14 word-first roles: positive = word carries it (outline pill); attention = ochre pill; flips live at 3-of-5 | improvised | G4 |
| 18 | Profile avatar photo | UNDEFINED (∅) | `avatar` ∅; `profile photo` ∅; `picture` ∅ | Improvised: abstract bust mark (ink on yellow disc) — no photo asset library exists | improvised | G8 |
| 19 | Icon for each ritual | UNDEFINED (∅) | `icon` ∅; `glyph` ∅; `symbol` ∅ | Improvised: inline 24px SVG set drawn to palette and stroke language | improvised | G8 |
| 20 | Toggle switch in settings | FALLBACK `fallback/platform-controls` | — | Fallback applied: native checkbox core with switch skin; field styling (radius 8, 1px `#DEDDDC`, warm ink); marked | improvised | G11 |
| 21 | Slider for daily goal | FALLBACK `fallback/platform-controls` | — | Native range, field styling, ink accent, live readout "30 min"; marked | improvised | G11 |
| 22 | Date picker for log entry | FALLBACK `fallback/platform-controls` | — | Native `input[type=date]`, field styling, warm ink; marked | improvised | G11 |
| 23 | Number stepper for minutes | FALLBACK `fallback/platform-controls` | — | Native number input + round −/+ buttons; marked | improvised | G12 |
| 24 | Text field (ritual name) | RESOLVED `component/field-select` (13.0) | — | Field per artifact: label above 14/500, white fill, 1px `#DEDDDC`, radius 8, 16px text; focus 3px yellow ring | — | — |
| 25 | Select for ritual category | UNDEFINED phrase; synonym hit | **`select` → component/field-select 9.0**; `dropdown` → 9.0; `form select` → 8.0 | Implemented per W-13: native select, radius 12, Fraunces field text | — | — |
| 26 | Checkbox for reminders | FALLBACK `fallback/platform-controls` | — | Applied in the onboarding "Pick your rituals" step (reminder rows themselves are toggles per spec); marked | improvised | G12 |
| 27 | Radio buttons for frequency | FALLBACK `fallback/platform-controls` | — | Applied for "Week starts on" (Monday/Sunday), field styling; marked | improvised | G12 |
| 28 | Text area for notes | RESOLVED `component/field-select` (17.0) | — | Field per artifact (textarea alias), log form | — | — |
| 29 | Tabs | UNDEFINED (navbar 4.0 via "bar") | `tabs` ∅; `tab bar` → navbar 4.0; `navigation tabs` → navbar 4.0 | Improvised: navbar chrome (white bar, dark links, hover fill); active state = parsnip fill + `aria-current`; single row kept | improvised | G7 |
| 30 | Bottom navigation bar (mobile) | RESOLVED `component/navbar` (8.0) | — | Adapted: navbar chrome pinned to the bottom ≤760px, single-row kept. **Resolve looks wrong vs the pack** (navbar is defined as a *top* bar; W-24 carries mobile unspecified) — noted, not forced | adapted | G7 |
| 31 | Table of logged entries | UNDEFINED phrase; synonym hit | **`table` → component/ledger 9.0**; `ledger` → 9.0; `data table` → 4.0 | Ledger per artifact: white, 16px rows, hairline dividers, Parsnip header 13/500, row hover tint, status pills inline | — | — |
| 32 | Pagination (older entries) | UNDEFINED (∅) | `pagination` ∅; `pager` ∅; `more results` → field-select 1.5 | Improvised: Kale "Older entries →" link + "1–8 of 24" label + "← Newer" (8/page over 24 fixtures) | improvised | G9 |
| 33 | Search box to filter | UNDEFINED (field-select 4.0 near) | `search` ∅; `filter` ∅; `search field` → field-select 4.0 | Implemented per field family: field input + inline search icon; filters all 24 entries live | — | — |
| 34 | Small category tag | UNDEFINED phrase; synonym hit | **`tag` → component/badge 9.0**; `chip` ∅; `category label` → badge 5.5 | Adapted: badge pill form (12/600) but neutral Parsnip fill — yellow is reserved (W-06) and badges "never decorate a section" (W-21) | adapted | G5 |
| 35 | Drag to reorder rituals | UNDEFINED (∅) | `drag` ∅; `reorder` ∅; `drag and drop` ∅ | Improvised: drag handle + HTML5 DnD + drop tint; order persists; keyboard reorder pending canon | improvised | G9 |
| 36 | Undo button after deleting | UNDEFINED (alternatives: action-pill, type-scale) | `undo` ∅; `revert` ∅; `rollback` ∅ | Improvised: outline pill action inside the delete toast (6 s grace), restores ritual at its old index | improvised | G2 |
| 37 | Three-step onboarding wizard | UNDEFINED (stepper 2.5 near-miss) | `wizard` ∅; `onboarding` ∅; `stepper` → platform-controls 2.5 | Improvised: dialog vessel + step dots; Welcome → Pick your rituals (checkbox fallback) → Set your goal (slider fallback); opens on first visit and via "Replay intro" | improvised | G10 |
| 38 | Export the data as CSV | UNDEFINED (∅) | `csv` ∅; `export` ∅; `download data` ∅ | Improvised: outline pill action; client-side Blob download (`cadence-entries.csv`), no network | improvised | G10 |
| 39 | Dark mode theme | FALLBACK `fallback/light-only` | — | Fallback applied: no dark canon → ink/parsnip/yellow roles kept, surfaces derived via alpha of ink/parsnip; marked; destructive-ink contrast (~3.4:1) flagged for canon | improvised | G13 |
| 40 | Celebration when checking off | UNDEFINED (∅) | `celebration` ∅; `confetti` ∅; `animation` ∅ | Improvised: ~700 ms palette dot-burst + ring pulse + check pop; honours `prefers-reduced-motion`. **Motion is deliberately undefined in the pack** (golden case: "gap over guess") — flagged, restrained, not canon | improvised | G2 |
| 41 | Illustration in the empty state | UNDEFINED (∅) | `illustration` ∅; `drawing` ∅; `image` ∅ | Policy-carry: illustration-capable zone held **empty** (W-23: no asset library reproduced; placeholder art rejected as fabricating it) with the dashed zone device; marked | improvised | G6 |
| 42 | Upload a photo for the ritual | FALLBACK `fallback/platform-controls` | — | Native file input + field styling; local FileReader preview only, nothing leaves the browser; marked | improvised | G13 |

---

## 2. Marking system

- Every improvised element ships `data-improvised="…"`; the two adaptations ship `data-adapted="…"`.
- The fixed corner button **◌** (`#marksToggle`) toggles `body.show-marks`: amber (=ochre) dashed outlines + small note labels on every marked element.
- 34 of 42 elements carry a mark: **32 × `data-improvised` · 2 × `data-adapted`** (E30 bottom nav, E34 category tag).
- 8 elements carry no mark because they are covered by citations: E01, E02a, E02b*, E09, E24, E25*, E28, E31*, E33 (*covered via synonym/near-hit search + artifact cross-reference; flagged in §4).

## 3. Self-test (port 8481, killed after)

`python3 -m http.server 8481` from the workspace; `curl` + Playwright DOM pass (`.venv`, `PLAYWRIGHT_BROWSERS_PATH=~/.cache/ms-playwright`).

- **60/60 Playwright assertions passed** on desktop (1280×900) + a 420×820 mobile context.
- **Zero console errors, zero page errors, zero failed requests**; `curl` 200s for index/css/js/3 fonts.
- Verified: wizard opens → Next/Next/Get started; ring "3 of 5" → check-off → "4 of 5" + "Logged" toast + burst; uncheck reverts; detail overlay opens with sparkline/streak/mini-history; confirm dialog opens, destructive never pre-focused, cancel works; tabs switch all four views; 7 bars, 31 heatmap cells, 8-row table; "Older entries" → "9–16 of 24"; search filters; CSV download `cadence-entries.csv`; badge grid 4 earned/2 locked; empty-state toggle; dark toggle; Save spinner + "Saved" toast; Replay intro; log form stepper 30→35 + save; empty-name error state; new ritual added (6 rows); ◌ marks on/off (marks count > 10); reload persistence (no wizard, 4 of 6, 6 rows); mobile bottom-nav switches views.

## 4. Resolve outcomes that looked wrong vs the pack (noted, never forced)

1. **E30 "bottom navigation bar on mobile" → RESOLVED `component/navbar` (8.0).** `component/navbar` is defined as a **top** bar (W-11: "Top bar… must stay single-row"). A bottom bar is a distinct (mobile) pattern; W-24 carries mobile unspecified. Implemented as an *adaptation* of the navbar chrome (same single-row, same hover language), marked `data-adapted`, gap filed.
2. **E25 "a select for ritual category" → UNDEFINED** although `component/field-select` lists `select`/`dropdown` as aliases (standalone `select` resolves 9.0). Looks like query-dilution by "ritual/category" tokens rather than a true gap. Implemented per the artifact via synonym search.
3. **E31 "a table of logged entries" → UNDEFINED** although `component/ledger` covers tables (`table` → 9.0). Same dilution pattern.
4. **E34 "a small category tag" → UNDEFINED** although `component/badge` lists alias `tag` (`tag` → 9.0). Same pattern.
5. **E02b "a text link" → UNDEFINED** with link treatment split across two artifacts — `token-set/colour` ("Kale = links inside content") vs `component/ledger` ("text links in ink with underline"). decisions.json itself records the conflict ("peppercorn links … also live"). Implemented both in their own contexts; flagged.
6. Feedback/overlays/destructive/charts/empty/motion are UNDEFINED in the pack although Gate-2 docs (W-15…W-19, W-23) describe stances — the pack is a subset. Gaps filed rather than treating docs as canon.
7. Type-scale wrinkle: W-02's parenthetical says button label sizing was "withdrawn (13/500)", while `token-set/type-scale` (W-05) still states "labels/buttons 13/500". Implemented 13/500 per the type-scale artifact.
8. `da validate` returns **0 findings / score 100** — wink declares no validators, so validate verifies nothing (recorded for honesty; the Playwright pass is the real check).

## 5. Coverage analysis

- Resolve outcomes (43 phrases): **RESOLVED 5 · FALLBACK 8 · UNDEFINED 30 · CONFLICT 0 · COMPOSE 0.**
- Implementation provenance: 5 per resolve citation · 5 via synonym/near-hit citation (E02b, E09, E25, E31, E33) · 32 improvised-in-character (24 from the UNDEFINED families + 8 governed by the two fallbacks) · 2 adaptations of cited artifacts (E30, E34).
- Marks: **34/42 elements marked** (32 improvised + 2 adapted). No element was implemented against a prohibition (no CONFLICT encountered).
- Style values sourced only from pack artifacts + docs/synthesis (tile, sheet, decisions): fonts with `font-variation-settings "SOFT" 80, "WONK" 1, "opsz" 40`; palette exactly `#FFE01B / #241C15 (+#231E15 ring) / #F6F6F4 / #DEDDDC / #E7B75F / #007C89 / #BF4055`; muted text via ink-alpha (no green/cold-grey/new hues); pills with 1px ink ring; hover −4.875px + hard zero-blur shadow; cards radius 16/24 + warm shadow; ochre band terminator; ledger/hairlines; 8px spacing; buttons 13/500.
- Deliberate refusals to invent: illustration assets (zone empty, W-23), continuous motion beyond the celebration (pack: "gap over guess"), dark-mode canon (fallback: roles kept only), mobile patterns beyond collapse + the demo-required bottom bar.

## 6. Gap register (13 open gaps, `examples/cadence2-wink/.design-authority/gaps.jsonl`)

| Gap | Covers (elements) |
|-----|--------------------|
| `gap/20261007-153917-c14b9e` | delete control, confirm dialog, detail modal |
| `gap/20261007-153917-0e8205` | logged toast, undo-after-delete, celebration motion |
| `gap/20261007-153917-5953b8` | week banner, bar chart, calendar heatmap |
| `gap/20261007-153917-647b6b` | completion ring, streak counter, status label |
| `gap/20261007-153917-adf09e` | sparkline, achievement badge family, category tag variant |
| `gap/20261007-153917-7f97cf` | empty state, illustration device |
| `gap/20261007-153917-e83ba2` | tab set active state, mobile bottom bar |
| `gap/20261007-153917-aeeb1b` | ritual icons, avatar mark |
| `gap/20261007-153917-78c2dc` | pagination, drag-to-reorder |
| `gap/20261007-153918-ba2b12` | onboarding wizard, CSV export, save spinner |
| `gap/20261007-153918-121f93` | toggle switch, slider, date picker |
| `gap/20261007-153918-5b5493` | number stepper, checkbox, radio group |
| `gap/20261007-153918-cd511d` | dark theme, photo upload |

Context (element lists + screens) for each gap is stored in the JSONL above.

## 7. Files & how to run

```
examples/cadence2-wink/
  index.html    — all views, overlays, wizard, marks button
  app.css       — tokens + components (pack citations inline)
  app.js        — state, fixtures, interactions, CSV export, localStorage
  NOTES.md      — this file
  fonts/        — Fraunces-VF, Fraunces-Italic-VF, Inter-VF (copied from docs/synthesis/wink/tile/fonts)
  .design-authority/gaps.jsonl — the 13 gap records
```

Serve with any static server from the folder (e.g. `python3 -m http.server 8481`) — relative paths only, no network calls, no build step.

**Repo note (for the audit):** this build performed **no git operations**. A concurrent workstream active in this repo (`Proposal gate…` commits, 15:33–15:37 UTC) committed repo-wide snapshots that swept the in-flight `cadence2-wink` files into commits `96bd066`, `2307fa7`, `b2fb11a`. The worktree here is the source of truth; the only delta vs `HEAD` is the final off-palette fix in `app.css` (dark-mode destructive ink → exact `--err` token).
