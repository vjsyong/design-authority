# Cadence — v3 stress build against the “leader” authority

**Verification (2026-10-08, adversarial round):** `tools/da_verify.py` (contract leader 0.1) — 23 checks: **19 PASS · 0 VIOLATION · 4 REVIEW closed**. Machine checks clean; the four register items (register, red character, hierarchy calibration, chart character) adjudicated by the build owner — no findings. Published results: `_evidence/verification/leader-verification.json`.

**Build**: `examples/cadence3-leader/` — a self-contained static app (`index.html` + `app.css` + `app.js` + `fonts/`; three vendored TTFs, zero network). Fixtures are fixed and deterministic (today pinned to **Wednesday 7 October 2026**; log data from a seeded generator, `_evidence/fixture-generator.py`).

**Authority**: `packs/leader` **v0.2.0**, including the 2026-10-07 codification (`pattern/data-charts`, `pattern/data-readouts`, `component/tag`) and `precedents.json` (10 negative precedents). Every spec element was resolved through the kernel CLI:
`python3 tools/da.py --pack packs/leader resolve "<element>" --json` → raw outputs in `_evidence/resolves.jsonl` (42 lines, spec order). Near-miss hunting: `da.py search` → `_evidence/searches.jsonl` (128 queries); declined areas: `da.py precedents --query` → `_evidence/precedent-queries.jsonl`.

**Outcome mix (42 elements)**: **RESOLVED 14 · FALLBACK 10 · UNDEFINED 18 · CONFLICT 0.**
(None of the prohibited treatments were requested by the spec — no square interactives, no red grounds, no emoji, no glows — so no CONFLICT fired; the tokens were still held to the colour families throughout.)

**Marks**: every non-canonical node carries `data-improvised` / `data-adapted` / `data-fallback` (+ a short `data-note`). The fixed **◌** control (bottom-right corner) toggles dashed **amber** outlines and labels on every marked node. At load the DOM contains **44 marked nodes** (7 improvised · 30 adapted · 7 fallback); opening the details panel adds 3 more (fallback). Initial-DOM breakdown: 21 static + 23 rendered (ritual glyphs, logged “celebration” readouts, badges, settings lists).

**Gaps filed** (5 — all genuinely uncodified needs, none overlapping the declined set): see §Gaps.

## Where things are mapped

- Marks key: `☆` = improvised, `†` = adapted, `‡` = fallback, `–` = canonical (no mark).

## Decision log — the 42 elements

Precedent ids are shown without the `precedent/declined-` prefix. “Attached” = attached by `resolve` itself; search-surfaced overlaps are noted in §Precedent compliance.

| # | Element | Outcome | Resolution id | Precedents attached | Built as | Marked |
|---|---------|---------|---------------|---------------------|----------|--------|
| 1 | a primary button for the main action | RESOLVED | `component/action` | — | Navy solid actions: per-ritual **Log**, **Save log** | – |
| 2 | a secondary button and a text link | RESOLVED | `component/action` | — | Outline secondary (**Back**, **Keep**, **Clear search**) + underlined blue tertiary links (**Cancel / Details / Close / Skip**) | – |
| 3 | delete a ritual permanently | UNDEFINED | — | `destructive-confirm-rejected` | In-flow ruled confirm inside the details panel; explicit verbs (“Remove ritual” solid red in attention duty / “Keep” outline); destructive never pre-focused | † data-adapted |
| 4 | a confirmation dialog before deleting | FALLBACK | `fallback/ruled-panel` | — (search surfaced `destructive-confirm-rejected` @7.5) | Same in-flow confirm panel — no scrim, no motion | ‡ data-fallback |
| 5 | a modal with ritual details | FALLBACK | `fallback/ruled-panel` | — | Details as an in-flow ruled panel under the ritual action | ‡ data-fallback |
| 6 | a toast notification saying logged | UNDEFINED | — | `saving-state-spinner` | Ruled **Logged** notice that changes at the end of the save | † data-adapted |
| 7 | a banner summarizing the week | RESOLVED | `component/notice` | — | Ruled **Week to date** notice (now resolves — notice gained week-summary aliases) | – |
| 8 | an empty state when no rituals exist | UNDEFINED | — | — | Ruled statement block + one outline action — “Clear search” when a filter matches nothing; the same block serves the no-rituals case (“Run setup”); typographic only | ☆ data-improvised · gap 1 |
| 9 | an error message under the field | RESOLVED | `component/field` | — | Small red line + red text under the minutes field | – |
| 10 | a loading spinner while saving | UNDEFINED | — | `saving-state-spinner` | Static readout “Saving… → Saved · N min”; no spinner, no motion beyond instant text swap | † data-adapted |
| 11 | a circular progress ring of today’s completion | UNDEFINED | — | — (data-charts geometry note directs substitution) | Rectilinear meter (London-85 track, red fill) + “N of M rituals · N minutes” readout | † data-adapted |
| 12 | a bar chart of weekly minutes | RESOLVED | `pattern/data-charts` | — | 7 bars, Chicago blue series, **today red** (single attention mark); 2px ink origin rule; hairline gridlines; sans numerals; exact values | – |
| 13 | a calendar heatmap of the month | RESOLVED | `pattern/data-charts` | — | Month grid of square cells; intensity in Chicago blues; today red; hairline borders | – |
| 14 | a tiny sparkline trend of the last week | RESOLVED | `pattern/data-readouts` | — | Mini columns in Chicago blue over a London-95 strip; no axes; History + per-ritual in details | – |
| 15 | a big streak counter | RESOLVED | `pattern/data-readouts` | — | Archivo Black 44 numeral + sans-caps label; the one display moment on Achievements | – |
| 16 | an achievement badge for seven days | UNDEFINED | — | — | Ink-stamp badges: earned = solid ink block; in-progress = outline + readout (“12 of 30”, “101 of 150”) | ☆ data-improvised · gap 2 |
| 17 | a status label on track or slipping | RESOLVED | `component/tag` | — | Ink-outline caps tags; **SLIPPING** flips solid red (attention) | – |
| 18 | a profile avatar photo | UNDEFINED | — | `imagery-and-icons` | Monogram tile “AM” in the top bar | † data-adapted |
| 19 | an icon for each ritual | UNDEFINED | — | `imagery-and-icons` | Rhythm glyph marks — graded ink squares (L-08) | † data-adapted |
| 20 | a toggle switch in settings | FALLBACK | `fallback/platform-controls` | `toggle-and-slider` | Native checkbox as switch, field-styled | ‡ data-fallback |
| 21 | a slider for daily goal minutes | FALLBACK | `fallback/platform-controls` | `toggle-and-slider` | Native range input | ‡ data-fallback |
| 22 | a date picker for the log entry | FALLBACK | `fallback/platform-controls` | `date-picker-select` | Native date input, field-styled | ‡ data-fallback |
| 23 | a number stepper for minutes | FALLBACK | `fallback/platform-controls` | — | Native number input, field-styled | ‡ data-fallback |
| 24 | a text field for the ritual name | RESOLVED | `component/field` | — | Canonical field (rounded ~8, 1px soft border, sans text, caps label above) | – |
| 25 | a select for ritual category | FALLBACK | `fallback/selection` | `date-picker-select` | Native select, field-styled | ‡ data-fallback |
| 26 | a checkbox for reminders | FALLBACK | `fallback/platform-controls` | `checkbox-radio` | Native checkbox | ‡ data-fallback |
| 27 | radio buttons for frequency | FALLBACK | `fallback/platform-controls` | `checkbox-radio` | Native radios | ‡ data-fallback |
| 28 | a text area for notes | RESOLVED | `component/field` | — | Canonical multiline field | – |
| 29 | tabs for today history achievements | UNDEFINED | — | — | View row in navbar link language (sans links, active blue underline); on mobile it stays a top text row (L-22) — no bottom bar, no tab canon | ☆ data-improvised · gap 3 |
| 30 | a bottom navigation bar on mobile | RESOLVED | `component/navbar` | — | Canonical top bar (serif name, view row, search); the literal bottom bar was not built — the ask resolves to the navbar, single-column collapse per L-22 | – (deviation noted on the #29 row’s label) |
| 31 | a table of logged entries | UNDEFINED | — | `ledger-rejected` | Editorial table composed per the try-list: 2px ink header rule, sans-caps heads, London-85 hairlines, serif names, tabular sans numerals, Red-95 hover | † data-adapted |
| 32 | pagination for older entries | UNDEFINED | — | — | “Newer / Older” text actions + “Page N of M” readout | ☆ data-improvised · gap 4 |
| 33 | a search box to filter rituals | RESOLVED | `component/navbar` | — | Navbar search rectangle with typing-cursor motif; filters the Today list | – |
| 34 | a small category tag | RESOLVED | `component/tag` | — | Ink-outline caps tag | – |
| 35 | drag to reorder rituals | UNDEFINED | — | `drag-reorder` | Explicit **Move up / Move down** controls (Settings → Order); order applies everywhere | † data-adapted |
| 36 | an undo button after deleting | UNDEFINED | — | — | **Removed** ruled notice + Undo tertiary link; restores the ritual (and its log) exactly | ☆ data-improvised · gap 5 |
| 37 | a three-step onboarding wizard | FALLBACK | `fallback/ruled-panel` | — | Three in-flow step panels (“Step N of 3”), navy Next / outline Back / Skip link; no scrim, no motion | ‡ data-fallback |
| 38 | export the data as csv | UNDEFINED | — | `csv-export` | **Download CSV** outline action with the concrete verb; file mechanics as app utility | † data-adapted |
| 39 | a dark mode theme | UNDEFINED | — | `dark-mode` | Stays light; colour roles kept as tokens; static readout “Light only. No dark mode in this system.” | † data-adapted |
| 40 | a celebration animation when checking off | UNDEFINED | — | — (closest `guideline/motion`) | Static state flip on log: row readout, meter, charts and day cell update instantly; no decorative motion (L-03) | † data-adapted |
| 41 | an illustration in the empty state | UNDEFINED | — | `imagery-and-icons` | None built — the declined route (absence is the adaptation); the empty block is typographic | – (absence; noted on the #8 block) |
| 42 | upload a photo for the ritual | UNDEFINED | — | `imagery-and-icons` | “Next mark” glyph picker per the try-list (“mark picker rather than photo uploads”) | † data-adapted |

## Handling rules applied

- **RESOLVED** → built per the cited artifact; no mark.
- **FALLBACK** → built per the fallback’s constraints (ruled panel = plain panel in page flow, no scrim/motion; platform controls = native elements at field level); mark `data-fallback`.
- **UNDEFINED with precedent** → followed the precedent’s **try-list**; mark `data-adapted`; no new gap (already adjudicated).
- **UNDEFINED with a canon directive but no artifact** → adapted per the directive (ring → meter/readout family; celebration → static per L-03); mark `data-adapted`; no gap.
- **UNDEFINED, genuinely uncodified** → searched synonyms, checked near-misses and precedent queries, then improvised **in character** (each improvisation composes from canonical vocabulary — notices, rules, tags, actions); mark `data-improvised`; **gap filed**.

## Precedent compliance — all 10 declines honoured

1. `saving-state-spinner` (toast + spinner) — fired on #6/#10. Static readouts/notices that change at the end of the operation; transient motion deliberately none (the ≤0.15 s colour/text swap is the existing interaction timing, not new motion).
2. `imagery-and-icons` — fired on #18/#19/#41/#42. Monogram avatar; rhythm glyph marks; no illustration; photo upload → mark picker.
3. `drag-reorder` — fired on #35. Explicit move controls built (the preferred try). Recurrence note: this is the second consumer asking; the alternative route was adjudicated, so no recurrence re-file.
4. `csv-export` — fired on #38. Concrete-verb action; file mechanics treated as app utility.
5. `dark-mode` — fired on #39. Stayed light; roles mapped as tokens.
6. `toggle-and-slider` — fired on #20/#21. Platform controls, field-styled, marked fallback.
7. `checkbox-radio` — fired on #26/#27. Same.
8. `date-picker-select` — fired on #22/#25. Same; select keeps field styling.
9. `destructive-confirm-rejected` — fired on #3 (and surfaced by search on #4). In-flow ruled confirm, explicit verbs, destructive never pre-focused, red only as attention on the destructive verb.
10. `ledger-rejected` — fired on #31. Table composed from typography + hairlines as a marked composition; not re-proposed.

Across the 42 resolves, `resolve` attached precedents 17 times covering all 10 precedents; the remaining declines were reached via `precedents --query` / `search` (all 10 appear in `_evidence/precedent-queries.jsonl`).

## Gaps filed (5, via `da.py gap-add --workspace examples/cadence3-leader`)

| # | Gap id | Need | Scope |
|---|--------|------|-------|
| 1 | `gap/20261007-161121-64118f` | Empty-state block for a filtered/empty list | core-screen |
| 2 | `gap/20261007-161121-360b2b` | Achievement badge / earned-milestone stamp | achievements |
| 3 | `gap/20261007-161121-576d7c` | View tabs / in-page segmented switcher | navigation |
| 4 | `gap/20261007-161121-9d486e` | Pagination for long lists | history |
| 5 | `gap/20261007-161121-129285` | Undo affordance after a destructive action | feedback |

Gap 5 carries a `precedent_warnings` entry (`destructive-confirm-rejected`) — expected: the destructive *confirm* flow follows that precedent; the *undo* affordance itself is uncodified. All five are new areas, not repeats of the ten declines. **Fewer gaps than v1**: nothing already adjudicated was re-filed.

## Notable findings

- **Charts, readouts and tags now RESOLVE.** Six formerly-open asks (bar chart, calendar heatmap, sparkline, streak counter, status label, category tag) hit canon directly — the pre-codification sweep had leader at R6 · F8 · U28; v3 measured **R14 · F10 · U18** on the same 42 asks.
- **The weekly banner resolved as-is** — `component/notice` now carries week-summary aliases, so “a banner summarizing the week” is a canonical ruled notice rather than an improvisation.
- **The completion ring is declined-by-canon**: `pattern/data-charts` explicitly rules out ring geometry and routes completion to the meter/readout family — built as a meter + readout, marked adapted, no new gap (canon already speaks).
- **Red restraint**: red appears only where canon assigns attention duty — section labels (L-09), focus rings (L-23), the completion meter fill (L-16), the SLIPPING tag flip, today’s bar/cell, the destructive verb, and the red-thread rules. Nothing else: no red grounds, no red decoration, no red as a data series.
- **No-imagery adaptations all marked**: avatar → monogram, icon → glyph marks, illustration → none, photo upload → mark picker. The map stays typographic.
- **Motion held near zero**: the “celebration” is a static state flip; the “spinner” is a text readout; the only timing anywhere is the system’s ≤0.15 s colour swap.
- **Platform controls settle in one place** (log panel + details + settings), all rendered natively with field styling and marked `data-fallback` — the 8 FALLBACK outcomes cluster exactly where the fallbacks’ scopes predict.
- **The two rejected proposals stayed rejected**: destructive-confirm and ledger were both built the alternative way, marked adapted, with no re-proposal.

## Evidence files

- `_evidence/resolves.jsonl` — 42 raw `resolve --json` outputs, spec order.
- `_evidence/searches.jsonl` — 128 near-miss searches (element + synonym passes).
- `_evidence/precedent-queries.jsonl` — the `precedents --query` hits for every decline query.
- `_evidence/fixture-generator.py` — deterministic fixture generator (seed 20261007; produces the embedded `FIXTURE_LOGS`).
- `_evidence/selftest.py` / `_evidence/selftest.txt` — the Playwright pass and its recorded output.
- `.design-authority/gaps.jsonl` — the 5 gaps above.

## Self-test results

Served with `python3 -m http.server 8482`, exercised in Chromium (Playwright, `.venv` python, `PLAYWRIGHT_BROWSERS_PATH=~/.cache/ms-playwright`), then the server was killed.

- **106/106 checks passed** (zero console errors, zero failed requests).
- **Assets**: `200` for index.html, app.css, app.js and all three fonts (curl).
- **Fixtures verified in-browser**: week sums `[66, 84, 37, 0, 0, 0, 0]`, streak `12`, `101` log entries, `2,091` minutes; month grid 35 cells with today red; heatmap intensity spread i1–i3.
- **Charts exact**: every bar’s `data-value` equals the state-derived sum (pre-log `[66,84,37,…]`, post-log `[66,84,71,…]`); sparkline columns equal the last-7-day totals.
- **Flows**: onboarding wizard (3 steps → adds ritual, sets goal; “Run setup again” reopens it), log save (error under field on empty minutes → “Saving…” → “Saved · 34 min”, meter/bars/notice/day-cell update), details edits (select/radios/checkbox persist), destructive remove (inline confirm, not pre-focused, Keep/Undo paths), reorder, mark cycler, CSV download (`cadence-log.csv`), search filter + empty state (both the no-match and no-rituals variants).
- **Marks toggle**: 44 nodes labelled, dashed amber outline confirmed on a sampled node, `aria-pressed` flips.
- **Persistence**: reload retains log, note, goal, order, category edits; wizard stays dismissed.
- **Mobile (≤760 px)**: ledger collapses to stacked rows (L-22), top nav row remains.
