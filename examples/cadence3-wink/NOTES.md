# Cadence · wink build — decision log (42 elements)

**Build**: `examples/cadence3-wink/` — self-contained static app (`index.html` · `app.css` · `app.js` ·
`fonts/`), zero network (fonts vendored locally). A personal ritual tracker: Today · History ·
Achievements · Settings, overlays for detail/confirm/onboarding, inline feedback, fixed fixtures.

**Authority**: `packs/wink` v0.2.0 — **rebuild against the codified canon** (5 new patterns landed
2026-10-07: `dialog-overlay`, `empty-state`, `destructive-confirm`, `inline-notice`, `progress`)
plus **8 negative precedents** (`precedents.json`).

**Method** (same for all 42 elements):
1. `python3 tools/da.py --pack packs/wink resolve "<element>" --json` — raw JSON per element stored
   one-line-each in `_evidence/resolves.jsonl` (outcome · resolution id · any attached precedents).
2. Near-misses: `search` synonyms (66 queries, `_evidence/searches.jsonl`).
3. Declined areas: `precedents --query` (20 queries, `_evidence/precedents-queries.jsonl`).
4. Handling: RESOLVED → build per cited artifact; FALLBACK → apply constraints + mark;
   UNDEFINED → improvise in character, mark, file a gap; precedents attach *alongside* any outcome —
   try-lists followed and marked.
5. Gaps filed via `da.py gap-add` (6 filed — v1 filed 16).

**In-app traceability**: the fixed **◌ toggle** (bottom-right corner) reveals dashed amber outlines +
labels on every non-canonical node. Nodes carry `data-improvised` / `data-adapted` / `data-fallback`
(title tooltip = the short note).

---

## Outcome mix (v0.2.0 vs the v1 stress sweep)

| | v1 (0.1) | **v3 (0.2.0)** |
|---|---|---|
| RESOLVED | 4 (+6 search-assisted) | **12 (+2 search-assisted)** |
| FALLBACK | 5 | **8** |
| UNDEFINED | 33 | **22** |
| CONFLICT | 0 | **0** |

Raw outcomes across the 42 rows: **R12 · F8 · U22**. Two UNDEFINED-by-threshold rows were rescued by
the mandated search step (both scored 9.0 with the right wording):

- **#25 select for ritual category** → `component/field-select` (search `"select"` 9.0; W-13 small-set select).
- **#31 table of logged entries** → `component/ledger` (search `"table"`/`"ledger"` 9.0).

**Precedent attachments: 15 across 14 rows · 7 distinct ids fired.**

| precedent | fired on | how it steered the build |
|---|---|---|
| `precedent/declined-chart-treatments` | #12 #13 #14 | compose minimal data blocks (numerals · rules · spacing), mark as improvisation |
| `precedent/declined-photographic-avatars-glyphs` | #18 #19 #41 #42 | monograms in canon type; words over glyphs; no photo/illustration display |
| `precedent/declined-native-form-controls` | #20 #26 #27 | platform defaults with field-level styling only; do not style beyond |
| `precedent/declined-pager-and-drag` | #32 #35 | pager = outline pill + readout; reorder via explicit move actions |
| `precedent/declined-csv-export-affordance` | #38 | action pill with the concrete verb; file flow = app utility |
| `precedent/declined-dark-mode` | #39 | light-only fallback applied; roles kept |
| `precedent/status-pill-rejected` | #17 | status as words (+ badge only for emphasis) |

The 8th precedent, `precedent/declined-neutral-tag-variant`, **did not attach** to #34
(`"a small category tag"`) — the matching rule needs single tokens ≥4 chars and `"tag"` is 3, with no
phrase hit. It is reachable via `search "tag"` (14.5) and `precedents --query "neutral tag"` / `"chip"`;
its try-list was followed manually and marked. (Pack-maintenance signal: consider a ≥3-char rule or a
`"category tag"` match, but that is the adjudication loop's call — recorded, not applied.)

## Gaps filed (6 — genuinely uncodified; v1 filed 16)

| gap id | need |
|---|---|
| `gap/20261007-161102-0511da` | in-flight feedback for quick saves (indeterminate progress) — #10 |
| `gap/20261007-161103-e5e7ac` | page-level weekly summary banner — #7 |
| `gap/20261007-161103-ffeb9c` | streak / momentum readout — #15 |
| `gap/20261007-161103-e2d499` | in-view tabs / segmented view switcher — #29 |
| `gap/20261007-161103-db0703` | search box to filter a list — #33 |
| `gap/20261007-161103-daae93` | celebration moment when completing — #40 |

No gap filed where a route already existed (fallback, precedent try-list, or compose from cited
entries — e.g. toast→inline-notice, error-under-field→invalid state + error colour). None of the six
filed gaps triggered `precedent_warnings` — they sit outside every declined area.

## Marks census (fresh state, all views in DOM)

**20 improvised · 35 adapted · 19 fallback = 74 annotated nodes.** The marks layer adds breathing
room and cycles labels through 4 corners so annotations sit in gaps, not over content.

## Self-test (Playwright, real Chromium, ×2 runs)

**90/90 checks, 0 failures** — onboarding wizard (3 steps, skip, replay), Today (ring, banner, log ×2,
celebration notices), search filter, Achievements (counter, badges), History (tabs; bar/heatmap/spark;
ledger pagination ×8→16→26; pager hide; log-form validation + saving state + saved notice), details
modal (Esc / close), **delete-confirm flow** (Esc cancel, scrim dismiss, confirm; *destructive never
pre-focused — focus lands on the heading*), empty state at zero rituals, add-ritual + error + success,
settings (slider, toggle persistence, light-only row, CSV download), ◌ marks toggle (dashed outline
computed, labels set/cleared), mobile bottom nav at 390px (no horizontal overflow), persistence across
reload, **zero console errors, zero page errors, zero external network requests**. All 6 assets curl
200. Screenshots + exported CSV in `_evidence/screens/`.

## Notable deviations (all deliberate, all marked)

1. **Toast (#6) → inline notice.** No toast canon (W-15); the canonical surface for "logged" feedback
   is the inline notice, placed near the list. *Deviation from the ask, marked `data-adapted`.*
2. **No undo (#36).** `pattern/destructive-confirm` states "no undo/recovery UI is canonical" (W-16).
   Built confirm-first deletion + a post-delete notice; the requested undo button was **not built**.
   *Deviation from the ask, recorded here and marked on the notice.*
3. **Dialogs are instant (#5/#37).** Dialog-overlay forbids invented entrance/exit motion; no
   transition on `<dialog>`, scrim rgba(35,21,.), Esc + scrim-click baseline.
4. **Dark mode not built (#39).** `fallback/light-only` + `precedent/declined-dark-mode`: an
   "Appearance — Light only" readout replaces a working theme switch.
5. **Illustration omitted (#41).** `pattern/empty-state` dont + asset policy: text-only empty panel.
6. **Celebration = instant (#40).** Motion is deliberately undefined; check-off produces an instant
   state change + notice, no animation invented. Gap filed.
7. **Saving = text state (#10).** No indeterminate spinner canon (W-18 dont); "Saving…" + disabled
   pill, completion notice. Gap filed.
8. **Photo upload (#42): native input kept; identity stays a monogram.** Fallback answers the upload
   control; the precedent's try-list decides the rendering.
9. **Native controls are intentionally unstyled** (checkbox/radio/range/date/number/file) — the
   precedent forbids styling beyond the field language; they will look platform-default in any browser.

## The 42-row decision log

| # | element | outcome | resolution id | precedents attached | built as | marked |
|---|---|---|---|---|---|---|
| 1 | a primary button for the main action | RESOLVED | `component/action-pill` | — | "Add ritual" CTA: yellow `#FFE01B`, 1px `#231E15` ring, 13/500, hover lift `-4.875px` + hard ink shadow (W-01..03) | — (canonical) |
| 2 | a secondary button and a text link | RESOLVED | `component/action-pill` | — | secondary = outline pill (2px ink inset) for cancels/pager; text links = ink underline (ledger W-20) | — |
| 3 | delete a ritual permanently | RESOLVED | `pattern/destructive-confirm` | — | Delete link → confirm dialog → removal; browser-verified | — |
| 4 | a confirmation dialog before deleting | RESOLVED | `pattern/destructive-confirm` | — | 16px vessel on warm scrim; consequence sentence; confirm = ink pill "Delete ritual"; destructive never focused | — |
| 5 | a modal with ritual details | RESOLVED | `pattern/dialog-overlay` | — | details dialog from the card vessel; instant; Esc/scrim close; focus in/out | — |
| 6 | a toast notification saying logged | UNDEFINED | — (closest `pattern/inline-notice`) | — | **adapted** to inline notice near the list ("Logged. That's 4 of 5 today.") — W-15: toasts unevidenced | `data-adapted` (notice) |
| 7 | a banner summarizing the week | UNDEFINED | — | — | improvised week banner: parsnip block, numeral lead + support line (searches `banner`/`announcement`/`summary` = 0 hits) | `data-improvised` · GAP `…e5e7ac` |
| 8 | an empty state when no rituals exist | RESOLVED | `pattern/empty-state` | — | tinted parsnip panel, one warm sentence, one action pill ("Add your first ritual") | — (container marked per #41) |
| 9 | an error message under the field | UNDEFINED | — | — | composed: `.field.invalid` border+ring in `#BF4055` + 13px error line (W-12) — no new grammar invented | `data-improvised` (2 error lines) |
| 10 | a loading spinner while saving | UNDEFINED | — (closest `pattern/progress`) | — | **adapted**: "Saving…" text state + disabled pill; no indeterminate motion (W-18 dont) | `data-adapted` · GAP `…0511da` |
| 11 | a circular progress ring of today's completion | RESOLVED | `pattern/progress` | — | SVG ring: yellow on parsnip, rounded caps, ink when complete; readout "3 of 5" | — |
| 12 | a bar chart of weekly minutes | UNDEFINED | — | `declined-chart-treatments` | try-list: minimal data block — 3px ink rules + numerals + day letters | `data-improvised` |
| 13 | a calendar heatmap of the month | UNDEFINED | — | `declined-chart-treatments` | try-list: hairline grid rules; yellow field + minutes numeral on logged days; today ring | `data-improvised` |
| 14 | a tiny sparkline trend of the last week | UNDEFINED | — | `declined-chart-treatments` | try-list: 2px ink rules + baseline rule; caption first→last | `data-improvised` |
| 15 | a big streak counter | UNDEFINED | — | — | composed readout: Fraunces display numeral + label (W-10 "numbers may take display treatment") | `data-improvised` · GAP `…ffeb9c` |
| 16 | an achievement badge for seven days | UNDEFINED | — (closest `component/badge` 4.0) | — | composed: achievement cards; earned uses the canonical badge; locked = plain readout | `data-improvised` (cards) |
| 17 | a status label on track or slipping | UNDEFINED | — | `status-pill-rejected` | try-list: words first — "On track" plain ink; "Slipping" + ochre **tint** chip; badge reserved for emphasis | `data-adapted` (`.status`) |
| 18 | a profile avatar photo | UNDEFINED | — | `declined-photographic-avatars-glyphs` | try-list: monogram "A" + name, canon type | `data-adapted` |
| 19 | an icon for each ritual | UNDEFINED | — | `declined-photographic-avatars-glyphs` | try-list: per-ritual monogram tile (first letter, Fraunces) | `data-adapted` (`.monogram`) |
| 20 | a toggle switch in settings | FALLBACK | `fallback/platform-controls` | `declined-native-form-controls` | native checkbox as the platform switch; field row; not styled beyond field language | `data-fallback` |
| 21 | a slider for daily goal minutes | FALLBACK | `fallback/platform-controls` | — | native range + readout (Settings + wizard step 3) | `data-fallback` |
| 22 | a date picker for the log entry | FALLBACK | `fallback/platform-controls` | — | native date input, field language (radius 8, `#DEDDDC`) | `data-fallback` |
| 23 | a number stepper for minutes | FALLBACK | `fallback/platform-controls` | — | native number input, field language | `data-fallback` |
| 24 | a text field for the ritual name | RESOLVED | `component/field-select` | — | Add-ritual dialog; label above 14/500; error under field on empty | — |
| 25 | a select for ritual category | UNDEFINED → **search-assisted RESOLVED** | `component/field-select` | — | search `"select"` 9.0; native select, radius 12 + serif text (W-13) | — |
| 26 | a checkbox for reminders | FALLBACK | `fallback/platform-controls` | `declined-native-form-controls` | native checkbox, field row | `data-fallback` |
| 27 | radio buttons for frequency | FALLBACK | `fallback/platform-controls` | `declined-native-form-controls` | native radios (Add dialog + wizard step 2) | `data-fallback` |
| 28 | a text area for notes | RESOLVED | `component/field-select` | — | textarea in the log form | — |
| 29 | tabs for today history achievements | UNDEFINED | — | — | improvised ink-filled pill tab strip in History (Charts / Entries); global nav stays the navbar | `data-improvised` · GAP `…e2d499` |
| 30 | a bottom navigation bar on mobile | RESOLVED | `component/navbar` | — | navbar language, bottom placement <760px; single row; words only | `data-adapted` (`.bottomnav`) |
| 31 | a table of logged entries | UNDEFINED → **search-assisted RESOLVED** | `component/ledger` | — | search `"table"` 9.0; ledger: parsnip header 13/500, 16px rows, hairlines, hover tint | — |
| 32 | pagination for older entries | UNDEFINED | — | `declined-pager-and-drag` | try-list: outline pill "Load older entries" + readout "Showing 8 of 26" | `data-adapted` |
| 33 | a search box to filter rituals | UNDEFINED | — | — | improvised: field-styled input + Clear link + no-match line | `data-improvised` · GAP `…db0703` |
| 34 | a small category tag | UNDEFINED | — | none attached — see `declined-neutral-tag-variant` (reached via query "neutral tag"/"chip") | try-list: neutral label = text pill, parsnip bg + ink; no emphasis badge for neutral | `data-adapted` (`.tag`) |
| 35 | drag to reorder rituals | UNDEFINED | — | `declined-pager-and-drag` | try-list: explicit **Move up / Move down** actions (cards + details); edges dimmed; no drag | `data-adapted` |
| 36 | an undo button after deleting | UNDEFINED | — (closest `pattern/destructive-confirm` 5.0) | — | **not built** — W-16: no recovery-UI canon; confirm-first + post-delete notice; deviation recorded | `data-adapted` (notice) |
| 37 | a three-step onboarding wizard | RESOLVED | `pattern/dialog-overlay` | — | wizard composes the vessel; step bar = `pattern/progress`; inner controls = platform fallbacks | — (inner fallbacks marked) |
| 38 | export the data as csv | UNDEFINED | — | `declined-csv-export-affordance` | try-list: outline action pill "Download CSV"; Blob flow = app utility | `data-adapted` (button) |
| 39 | a dark mode theme | FALLBACK | `fallback/light-only` | `declined-dark-mode` | **not built** — "Appearance: Light only" readout; palette roles kept; deliberate | `data-fallback` (row) |
| 40 | a celebration animation when checking off | UNDEFINED | — | — | **adapted**: instant state change (Logged → ring → all-done notice); no motion invented | `data-adapted` · GAP `…daae93` |
| 41 | an illustration in the empty state | RESOLVED | `pattern/empty-state` | `declined-photographic-avatars-glyphs` | illustration **omitted** per asset policy (W-19/W-23); text-only panel | `data-adapted` (`#emptyState`) |
| 42 | upload a photo for the ritual | FALLBACK | `fallback/platform-controls` | `declined-photographic-avatars-glyphs` | native file input; monogram identity stays (try-list); filename readout only | `data-fallback` (field) + `data-adapted` (note) |

GAP id shorthand: `…e5e7ac` = `gap/20261007-161103-e5e7ac`, `…0511da` = `gap/20261007-161102-0511da`,
`…ffeb9c` = `gap/20261007-161103-ffeb9c`, `…e2d499` = `gap/20261007-161103-e2d499`,
`…db0703` = `gap/20261007-161103-db0703`, `…daae93` = `gap/20261007-161103-daae93`.

## Findings worth keeping

- **New canon paid off exactly where the v1 sweep said it would.** Modal/dialog, empty state,
  destructive flow, inline feedback, progress: all previously U → now RESOLVED with cited values; the
  delete flow resolves through `pattern/destructive-confirm` end-to-end (dialog, verb-labelled ink
  confirm, cancel outline, **no default focus on the destructive action** — asserted in the browser).
- **Precedents steer, they don't block.** 15 attachments pulled 14 rows toward sanctioned routes
  (compose/mark, fallback+mark, try-list) — the rebuild is *smaller* (6 gaps) than v1 (16) without
  silencing any request; every declined ask is traceable to a built alternative.
- **Resolve alone under-reports canon — still true at 0.2.0.** #25/#31 needed the search step
  (9.0 each with the right noun). The resolve→search pairing is the workflow.
- **One vocabulary miss stays:** `"a small category tag"` can't reach its own precedent
  (≥4-char single-token rule vs `"tag"`). Steered manually; recorded for pack maintenance.
- **Deliberate non-canon is visible non-canon**: dark mode, undo, illustration, spinner, motion — each
  *declined/undefined by the authority* and built as the sanctioned alternative, marked in-app, with
  the deviation recorded (section above).
- **Composition is the main verb at 0.2.0**: 20 of 42 rows are marked improvisations/adaptations —
  but 14 of those follow a cited route (fallback/precedent/pattern), so the un-routed remainder is
  just the 6 filed gaps.
