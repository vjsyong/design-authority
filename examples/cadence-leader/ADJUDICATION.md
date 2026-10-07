# ADJUDICATION — leader pack · Cadence gap docket (17 requests)

**Role:** adjudicator (the missing judge seat) · **Pack:** `packs/leader` 0.1.0 (Leader Interface System) · **Workspace:** `examples/cadence-leader` · **Date:** 2026-10-07
**Method:** every gap was re-verified independently against the kernel (`python3 tools/da.py --pack packs/leader …`, plus the `resolve`/`search` library directly), then judged against the source evidence base (`docs/synthesis/leader/` — revised `decisions.json` post-Gate-2, `01-gestalt.md`, `00-evidence-inventory.md`, `refs/sheet.html`; plus the pack's own artifacts/fallbacks). Candidate fixes were simulated on a scratch **copy** of the pack — before/after scores below are real kernel output; the shipped pack was not modified.

## Counts (gap-level verdicts)

| class | count | gaps |
|---|---|---|
| PROPOSAL | **6** | deea1f · d20922 · 1ae98e · 878f7a · d4706a · 4bf6e3 |
| SCOPE-FIX | **2** | 84338e · 0b2e49 (primary) |
| LEXICON-FIX | **1** | 0643c3 (0b2e49 carries a second, LEXICON-FIX defect — see fixes.json row 4) |
| NO-ACTION | **8** | 7e2442 · 6a07a0 · 125884 · d24275 · f9b5a1 · 9146b6 · 5bb40b · ca8e6c |
| INVALID | **0** | — (boundary cases explained below) |
| **total** | **17** | |

Machine-readable fixes: `examples/cadence-leader/adjudication/fixes.json` (4 rows, verified). Proposals filed via CLI: `prop/20261007-151947-45862b`, `prop/20261007-151947-81e020`, `prop/20261007-151947-916eda`, `prop/20261007-151948-91ef4b`, `prop/20261007-151948-992c62`, `prop/20261007-151948-25306d`.

## The 17 (full table)

| # | gap | key need(s) | independent re-verification (baseline pack) | class | disposition |
|---|---|---|---|---|---|
| 1 | `…-deea1f` | delete a ritual permanently; post-delete undo | `delete a ritual permanently` → **UNDEFINED** (no hits; `destructive action` → action@4.0) | **PROPOSAL** | `pattern/destructive-confirm` (L-15). Undo composes as notice + tertiary link — no new canon. |
| 2 | `…-84338e` | modal detail; delete-confirm dialog; 3-step wizard | modal → FALLBACK ruled-panel@['modal']; confirm → FALLBACK@['dialog']; `wizard` → **UNDEFINED** (no hits) | **SCOPE-FIX** | ruled-panel scope += `wizard`, `onboarding`. First two already correct FALLBACKs. |
| 3 | `…-0643c3` | toast "logged"; week-summary banner; check-off celebration | `a banner summarizing the week` → UNDEFINED (notice@4.0; bare `banner` hits notice@9.0); toast → UNDEFINED (notice@4.0); celebration → UNDEFINED (motion@4.0) | **LEXICON-FIX** | notice aliases += `weekly summary`, `week summary`, `week-summary` (verified → RESOLVED@8.0/13.0). Toast + celebration sub-elements: NO-ACTION (below). |
| 4 | `…-7e2442` | saving/loading state (~700 ms) | `a loading spinner while saving` → UNDEFINED (no hits; `progress indicator` → meter@4.0) | **NO-ACTION** | Transient persist is terminal feedback; register-derivable (static readout, L-16; notices, L-14). No spinner canon (L-03; golden keeps motion patterns UNDEFINED). |
| 5 | `…-d20922` | empty states (zero rituals/badges); illustration | `empty state` → UNDEFINED (no hits) | **PROPOSAL** | `pattern/empty-state` (L-17). Illustration explicitly denied (L-17/L-21). |
| 6 | `…-1ae98e` | circular ring; bar chart; calendar heatmap | bar/ring → UNDEFINED (meter@4.0); heatmap/chart → UNDEFINED (no hits) | **PROPOSAL** | `pattern/data-charts` (rectilinear; tdc.org charts evidence + city palettes). Ring: not in register — readouts use meter family. |
| 7 | `…-878f7a` | sparkline; big streak counter | `sparkline` → UNDEFINED (no hits); `big number readout` → UNDEFINED (meter@4.0) | **PROPOSAL** | `pattern/data-readouts` (L-04 "big statics"; L-05 display 44/−1). |
| 8 | `…-d4706a` | achievement badge; status label; category tag | `status label` → UNDEFINED (hierarchy@4.0); badge/tag → UNDEFINED (no hits) | **PROPOSAL** | `component/tag` (L-13 — in the Gate-2 sheet, not in the pack). Badge: compose from tag + glyph; no medal family. |
| 9 | `…-6a07a0` | avatar photo; ritual icons; photo upload | all → UNDEFINED (no hits) | **NO-ACTION** | L-21: no imagery; iconography = rhythm glyphs. Absence is honest, not a gap. |
| 10 | `…-0b2e49` | number stepper; textarea for notes | stepper → UNDEFINED (no hits); `text area` → UNDEFINED (field@4.0) | **SCOPE-FIX** (+ secondary LEXICON-FIX) | platform-controls scope += `stepper`; component/field aliases += `textarea`, `text area`, `multiline field` (verified → FALLBACK / RESOLVED@13.0). |
| 11 | `…-4bf6e3` | tabs; entries table; pagination | `tab navigation` → UNDEFINED (navbar@4.0); table/ledger/pagination → UNDEFINED (no hits) | **PROPOSAL** | `pattern/ledger` (L-18). Tabs: nav-register composition — no entry needed. Pagination: unevidenced, stays marked. |
| 12 | `…-125884` | drag-to-reorder | `reorder` → UNDEFINED (no hits) | **NO-ACTION** | No interaction evidence; restrained register. Correctly out (marked improvisation). |
| 13 | `…-d24275` | CSV export | `export` → UNDEFINED (no hits) | **NO-ACTION** | App plumbing, not interface canon; no evidence. Correctly out. |
| 14 | `…-f9b5a1` | dark-mode theme | `dark mode` → UNDEFINED (no hits) | **NO-ACTION** | No dark surfaces/themings anywhere in evidence; re-stating red/blue roles on ink ground would be invention. Correctly out. |
| 15 | `…-9146b6` | toggle switch; daily-goal slider | `toggle switch` → FALLBACK@['switch']; `slider` → FALLBACK@['slider'] | **NO-ACTION** | The platform-controls fallback is the designed answer; used, marked, reported. No expansion (see quirk note re: bare `toggle`). |
| 16 | `…-5bb40b` | checkbox; radio buttons | checkbox → FALLBACK@['checkbox']; radio → FALLBACK@['radio'] | **NO-ACTION** | Same: sanctioned fallback, correct outcome. |
| 17 | `…-ca8e6c` | date picker; category select | date picker → FALLBACK selection@['picker']; select → FALLBACK@['select'] | **NO-ACTION** | Fallback-covered; routing nuance has identical constraints/outcome (quirk note below). |

## Fixes shipped (in `fixes.json`, each simulated before shipping)

1. **notice · aliases += `["weekly summary","week summary","week-summary"]`** — the reported phrase-level miss: bare `banner` hit notice@9.0 (alias + whole-query phrase bonus), but multi-word phrasings collapsed to the 4.0 alias weight. Verified: `a banner summarizing the week` UNDEFINED→RESOLVED@8.0; `weekly summary` →RESOLVED@13.0; `a week-summary banner on Today` →RESOLVED@8.0.
2. **ruled-panel · scope += `["wizard","onboarding"]`** — scope miss; the fallback statement ("interstitials render as plain ruled panels in the page flow") clearly should cover it. `a three-step onboarding wizard` UNDEFINED→FALLBACK@['onboarding','wizard'].
3. **platform-controls · scope += `["stepper"]`** — scope miss; the fallback statement ("uncovered control → native element + leader field styling") governs. `a number stepper for minutes` UNDEFINED→FALLBACK@['stepper'].
4. **field · aliases += `["textarea","text area","multiline field"]`** (secondary defect of gap `0b2e49`) — `multiline field` search near-miss @4.0; `a text area for notes` UNDEFINED→RESOLVED@13.0.
   All four together leave the pack's **golden set 10/10** (checked pre/post on a scratch copy).

## Proposals filed (candidate records, noncanonical)

| gap | proposal id | shape | source evidence |
|---|---|---|---|
| deea1f | `prop/20261007-151947-45862b` | `pattern/destructive-confirm` (red verb confirm + consequence + never pre-focused; rides the ruled-panel surface) | L-15; sheet L-15; L-02 v4; L-20 |
| d20922 | `prop/20261007-151947-81e020` | `pattern/empty-state` (ruled statement + exactly one action; no illustration) | L-17; sheet L-17; L-21 |
| 1ae98e | `prop/20261007-151947-916eda` | `pattern/data-charts` (rectilinear marks; city palettes for series; red = single attention mark; no rings) | inventory §2 (TDC "charts and graphs") + §1 addendum; gestalt "rectangles"; L-16 |
| 878f7a | `prop/20261007-151948-91ef4b` | `pattern/data-readouts` (sparkline columns; one display-face numeral + caps label per screen) | L-04 "big statics"; L-05; L-03 |
| d4706a | `prop/20261007-151948-992c62` | `component/tag` (ink-outline caps tag; attention = solid red; no pills/dots) | L-13; sheet L-13; L-02 v4 |
| 4bf6e3 | `prop/20261007-151948-25306d` | `pattern/ledger` (editorial table; rules do the separating; no zebra; red-95 hover) | L-18; sheet + components refs |

Each draft carries the six required fields (problem / insufficiency / reuse_case / composition_check / proposed / tests), only real `depends_on` ids, and deterministic tests (resolve-checks + DOM/token spec checks).

## NO-ACTION rationale (policy lines)

- **7e2442 (saving state)** — `authority.policy.on_undefined` (improvise, mark, report) + register: L-16 readout / L-14 notices cover terminal feedback; L-03 excludes chrome motion; golden precedent keeps motion patterns UNDEFINED. The marked static readout was the right move; canon should not grow a loading/spinner pattern.
- **6a07a0 (imagery)** — L-21: "No imagery in the reference build… absence here is honest, not a gap"; imagery is story-bound. Iconography is the rhythm-glyph language (L-08 motif).
- **125884 / d24275 / f9b5a1 (reorder / export / dark theme)** — no evidence anywhere; gestalt's carried-UNDEFINEDs anticipate none of them; correctly out (marked improvisations). "Genuinely out", confirmed against evidence.
- **9146b6 / 5bb40b / ca8e6c (platform controls ×3)** — the fallbacks exist precisely for this class; statement + constraints ("use the platform's native element with the leader field styling; mark the improvisation; report a gap if the need recurs") were followed exactly. No evidence supports promoting custom controls now (L-12 already endorses the native select for small sets; toggle evidence is a Gate-2 screenshot mention only). Canon should not expand to absorb them.
- **3's toast & celebration sub-elements** — toast: L-14's stance ("no toasts, none evidenced") is honored by silence + the notice vessel; the marked notice-family readout was correct. Celebration: L-03 register + the glyph motif compose it; no expansion. (Both flagged as the closest calls under uncertainties.)

**INVALID: none.** Gaps 2, 3, 15–17 bundle elements already covered by fallbacks — that is prescribed behavior (the fallbacks themselves say to report), not mis-filing, and each gap still carries a real defect or a real judgment call.

## Uncertainties & upstream observations

1. **Kernel scope-matching quirk (observed, not a pack fix).** Fallback matching compares **raw** scope strings against **stemmed** query tokens, so the scope entries `date` and `toggle` are inert: `resolve("date")` → UNDEFINED and `resolve("toggle")` → UNDEFINED even though both words are listed (search stems both sides, which is why `platform-controls@2.5` surfaces in search yet the fallback misses). The recorded phrasings still land correctly only via other tokens (`picker`, `switch`). Recommendation: normalize scope entries with the same stemmer in the fallback overlap check — upstream kernel change, deliberately **not** patched and **not** worked around with garbage scope values. Classified NO-ACTION because outcomes are already right.
2. **Stale "square" wording.** L-15/L-19 say "square dialog/sheet" but accepted L-02 v4 makes rounded ~8 the live system (refs/components.html and the tile predate that revision). Treated `decisions.json` (revised) + `refs/sheet.html` + the pack as current; the destructive proposal follows L-02 v4 and rides the pack's deliberate no-dialog-canon fallback.
3. **Closest calls** (documented alternatives): gap 4 could alternatively be a soft LEXICON-FIX to meter ("saving"/"loading" readout aliases) if upstream wants the readout register formalised; gap 3's toast could alternatively be carried as a `no toasts` prohibition (L-14) — judged unnecessary now. Neither changes the shipped output.
4. **Badges.** No source support as a distinct object; judged composable from `component/tag` + rhythm glyph. If an achievement-badge family is wanted upstream, it should return as a new request with evidence.
5. **Uncarried source decision adjacent to the docket:** L-08 motifs (red thread + rhythm glyphs) are not in the pack, yet the demo's icons (gap 9), badge tiles (gap 8) and celebration (gap 3) all lean on rhythm glyphs. Flagged for upstream attention; not filed as a proposal because no gap requested motifs directly.
6. **Residual lexicon phrasings after the fixes** (not covered, accepted): `digest block`, `notes input`, `setup flow`, `increment control`. The recorded need phrasings are all covered and verified.

## Non-modifications (per mandate)

Packs, compiler, app and gap records untouched (17 gaps still `open`; verdicts live here + in `fixes.json` + proposal records). Files written: `examples/cadence-leader/adjudication/{fixes.json,proposal-deea1f.json,proposal-d20922.json,proposal-1ae98e.json,proposal-878f7a.json,proposal-d4706a.json,proposal-4bf6e3.json}`, this file, and the six CLI proposal records under `.design-authority/proposals/`. No git commits. Verification harnesses live in scratch (`~/.hermes/cache/scratch/adjudicator/`).
