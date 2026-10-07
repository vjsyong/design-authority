# dominion · gap adjudication — cadence-dominion

**Role:** adjudicator seat for the `dominion` Design Authority pack (`packs/dominion`, v0.1.0).
**Input:** the 15 gap requests in `examples/cadence-dominion/.design-authority/gaps.jsonl` (refs G1–G15), the
builder record (`examples/cadence-dominion/NOTES.md`), and the source evidence base
(`docs/synthesis/dominion/`: gestalt, decisions D-01…D-22, evidence inventory, tile, decision sheet).
**Date:** 7 October 2026. **Rule:** judge against source evidence; smallest change wins.
No pack, compiler, app or gap record was modified; proposals are noncanonical candidates.

## Method (re-verification, not trust)

Every gap was re-run independently through the kernel CLI
(`python3 tools/da.py --pack packs/dominion resolve "<phrase>"` and `search "<phrase>"`, all phrasings from the
gap context, plus synonym probes). Every proposed fix and every proposed catalogue entry was then validated by
**in-memory simulation** of the exact change (pack loaded, entries mutated in memory only, resolver re-run;
golden set re-checked after fixes: **10/10**). Outcome vocabulary: RESOLVED (≥6.5 direct, ≥2.0 margin),
COMPOSE (recipe ≥5.0), FALLBACK (scope-token match), UNDEFINED, CONFLICT (prohibition signal).

## Counts

| Class | Count | Gaps |
|---|---|---|
| LEXICON-FIX | 2 | G8, G15 |
| SCOPE-FIX | 3 | G4, G5, G9 |
| PROPOSAL | 5 | G1, G10, G12, G13, G14 |
| NO-ACTION | 5 | G2, G3, G6, G7, G11 |
| INVALID | 0 | — |
| **Total** | **15** | |

## The 15 gaps

Gap ids are `gap/20261007-150030-*` (G1–G5) and `gap/20261007-150031-*` (G6–G15); short suffixes below.

| Ref | Suffix | Request (abridged) | Re-verified today | Class | Disposition |
|---|---|---|---|---|---|
| G1 | 0a71f9 | bar chart · month heatmap · sparkline | UNDEFINED ×3; search: no hits (closest meter 4.0) | **PROPOSAL** | `prop/20261007-151923-bd08f2` — add `pattern/plain-chart` |
| G2 | 05534a | progress ring · streak counter · badge tiles | UNDEFINED ×3 (ring closest meter 4.0) | **NO-ACTION** | ring off-grammar (D-02 rectilinear); streak/badge compose from catalogued primitives; meter is the progress element (D-15) |
| G3 | b20a90 | saving indicator · check-off celebration | UNDEFINED ×3 | **NO-ACTION** | motion gated by doctrine (D-15/D-22; gestalt motion; golden set keeps motion deliberately UNDEFINED); saving state = meter composition |
| G4 | 06610b | toggle · checkbox · radio · check control | FALLBACK ×3 (switch/checkbox/radio); check control UNDEFINED | **SCOPE-FIX** | `fallback/platform-controls` scope += `"check"` |
| G5 | 2eb8c6 | date picker · slider · search box | FALLBACK ×3; "a search input" alone UNDEFINED | **SCOPE-FIX** | `fallback/large-selection` scope += `"search"` |
| G6 | e4273f | view tabs · paging control | UNDEFINED ×2 | **NO-ACTION** | nav idiom already decided (D-08; carried in `component/masthead` active state); paging = outline actions + plain readout composition |
| G7 | 19b53c | per-ritual marker · category tag | UNDEFINED; icon request conflicts (pictograms) | **NO-ACTION** | pictograms prohibited (D-22): adaptation correct; marker/tag are ruled-register compositions (D-10 label idiom) |
| G8 | 842aa2 | drag reorder · undo after delete | UNDEFINED; undo closest action 4.0 | **LEXICON-FIX** | `component/action` aliases += `"undo"` (reorder = native interaction; noted) |
| G9 | f3d993 | number stepper | UNDEFINED (no candidates) | **SCOPE-FIX** | `fallback/platform-controls` scope += `"stepper"` |
| G10 | 0d3443 | onboarding wizard · CSV export · dark theme | UNDEFINED ×4 | **PROPOSAL** | `prop/20261007-151923-0cf7b9` — declare reversed colourway on `token-set/colour`; wizard/export declined (below) |
| G11 | b18038 | avatar photo · empty-state illustration · photo upload | CONFLICT ×3 (prohibit/imagery-pictograms) | **NO-ACTION** | imagery unlicensed (D-22; D-16: imagery absence is a system property); adaptations (initials, ruled statement, written note) correct |
| G12 | 6d60dd | dialog vessel · empty state (decisions-only) | UNDEFINED ×2 | **PROPOSAL** | `prop/20261007-151923-e09f12` — compile D-18 + D-16 into the catalogue |
| G13 | f5a96f | status device · ledger (decisions-only) | UNDEFINED ×2 | **PROPOSAL** | `prop/20261007-151923-522030` — compile D-10 + D-17 into the catalogue |
| G14 | 13d338 | toast · weekly banner | UNDEFINED ×2 | **PROPOSAL** | `prop/20261007-151923-72cc3e` — compile D-13 notice vessel; "toast" deliberately gains no vocabulary |
| G15 | 1eb3c0 | delete-a-ritual flow · confirm dialog | UNDEFINED on resolve; search finds `recipe/retire-confirm` @ 3.0 / 4.5 | **LEXICON-FIX** | `recipe/retire-confirm` needs += `"delete a ritual"`, `"confirmation dialog"` |

## Fixes (exact, machine-readable — see `adjudication/fixes.json`)

All five were simulated against the loaded pack; each produces the intended outcome with the golden set intact (10/10).

1. **G15 · `recipe/retire-confirm` · needs += `["delete a ritual", "confirmation dialog"]`**
   - Today: `resolve("delete a ritual permanently")` → UNDEFINED (recipe scores 3.0, below COMPOSE_MIN 5.0);
     `search("delete a ritual")` already finds the recipe @ 3.0 — reachable by search, not by resolve.
   - After fix: COMPOSE @ **11.0** for both `"delete a ritual permanently"` and `"a confirmation dialog before deleting"`
     (token weights 3+3 plus the multi-word alias-phrase bonus 5.0). `"remove an item"` remains COMPOSE.
2. **G8 · `component/action` · aliases += `["undo"]`**
   - Today: `resolve("an undo button after deleting")` → UNDEFINED (only "button" matches, 4.0); `search("undo")` → no hits.
   - After fix: RESOLVED @ **8.0** ("undo" 4.0 + "button" 4.0). The builder already treats Undo as a tertiary action
     ("Close, Skip, Dismiss, Undo" ride `component/action`), so this is vocabulary only.
3. **G4 · `fallback/platform-controls` · scope += `["check"]`**
   - Today: check control → UNDEFINED (the scope word "checkbox" does not match the phrasing "check");
     toggle/checkbox/radio already ride the fallback correctly (matched via switch/checkbox/radio).
   - After fix: FALLBACK, matched_scope `["check"]` — a completion control is an uncovered control and belongs
     on the platform default with field styling.
4. **G5 · `fallback/large-selection` · scope += `["search"]`**
   - Today: `"a search input"` → UNDEFINED (closest `component/field` 4.0); the reported phrasing only worked
     because it contained the word "filter". After fix: FALLBACK, matched_scope `["search"]`.
5. **G9 · `fallback/platform-controls` · scope += `["stepper"]`**
   - Today: `"a number stepper for minutes"` → UNDEFINED (zero candidates). After fix: FALLBACK, matched_scope `["stepper"]`.

## Proposals (filed via CLI; candidates, noncanonical)

1. **G12 → `prop/20261007-151923-e09f12`** — *compile fix, decisions as source evidence.*
   D-18 (dialog = square white sheet, 2px black frame, scrim 55%, instant) and D-16 (empty state = plain ruled
   statement + one action, no imagery) exist in `docs/synthesis/dominion/decisions.json` but have no catalogue
   entries, so resolve cannot cite them. Proposal adds `component/dialog` + `component/empty-state` exactly as
   the decisions define them (no new design). Simulated: `"a modal with ritual details"` → RESOLVED 8.0;
   `"an empty state when no rituals exist"` → RESOLVED 17.0.
2. **G13 → `prop/20261007-151923-522030`** — *compile fix.*
   Same defect for the status device (D-10: words, never colour; structure carries emphasis) and the ledger
   (D-17: 2px black header rule, 1px pewter hairlines, no zebra). Proposal adds `component/status` +
   `component/ledger`. Simulated: status → RESOLVED 21.0; ledger → RESOLVED 13.0.
3. **G14 → `prop/20261007-151923-72cc3e`** — *compile fix.*
   D-13 defines the notice vessel (2px black top rule, grey ground, plain sentence, **no toasts**) but it is
   uncatalogued, so the save-confirmation and the weekly banner cannot cite a vessel. Proposal adds
   `component/notice`. The toast remains a deviation: the proposal deliberately adds no "toast" vocabulary, so
   toast requests stay visible as UNDEFINED. Simulated: `"a save confirmation message"` → RESOLVED 17.0;
   `"a banner"` → RESOLVED 9.0; `"a toast notification saying logged"` stays UNDEFINED.
4. **G1 → `prop/20261007-151923-bd08f2`** — *new pattern, smallest shape.*
   No figure grammar exists anywhere in the pack (search: chart/graph/data-visualization → no hits; meter is
   single-value only, D-15). Proposal adds one entry, `pattern/plain-chart`, covering bars / month grid /
   sparkline, shaped only from attested primitives — 2px rules, fills, the grey ramp, plain labels — citing
   the gestalt's shape language ("rectangles, bars, rules, measured space" / "Rule over ornament",
   `01-gestalt.md`) and the D-02/D-05/D-06/D-15 doctrine. No new primitives; no hue; static.
   Simulated: the three gap phrasings → RESOLVED 13.0 / 8.0 / 13.0.
5. **G10 → `prop/20261007-151923-0cf7b9`** — *small colourway declaration.*
   Of the three sub-needs, two are declined (onboarding wizard = dialog vessel + steps, once G12 compiles;
   CSV export = app behaviour, not an interface pattern). The dark theme is a real catalogue gap: the
   reversed colourway (white on black) is an observed source property
   (`00-evidence-inventory.md` §1/§6; gestalt "Reversed colourway (white on black) exists";
   `tile/tile.html` "Reversed colourway — white on black, formal and large-format") and was composed by hand.
   Proposal extends `token-set/colour` with the declared mapping + vocabulary (ground #000; white text/rules;
   band/pewter inverted; red ceremonial-only, D-05; blue focus glow kept, D-21). Simulated:
   `"a dark mode theme"` → RESOLVED 22.0. The source recommends the reversal for large formats; the full-UI
   ground is flagged as a reviewable interpretation.

## No-action ledger (and why canon should not expand)

- **G2 (progress ring / streak / badge)** — a circular ring conflicts with the system's rectilinear property
  (D-02 "Everything rectilinear"; gestalt "Rectilinear by nature… every figure is rectangular"): it must not be
  canonized. The progress element is the meter (D-15, catalogued); a streak figure and a badge tile are
  compositions of catalogued primitives (type rhythm D-04/`token-set/type-scale`, D-06 band, D-10 label idiom,
  D-09 bilingual labels). Improvising them (marked) is the sanctioned path — the same answer the system gives
  any request it expresses by composition.
- **G3 (saving indicator / celebration)** — motion is gated by doctrine: D-15 "Static only; nothing decoratively
  animates"; gestalt motion section "Nothing animates decoratively"; the golden set fixes motion as a deliberate
  UNDEFINED ("animate the dialog opening" → expected UNDEFINED). The saving state is a meter composition
  (catalogued). Canon must not expand into animation; the static composition stands.
- **G6 (tabs / paging)** — the nav treatment is already decided: D-08 (nav links; active = medium + underline)
  is carried in `component/masthead`'s active state, and D-20 gives the plain-row collapse; paging composes from
  `component/action` (outline square buttons) + a plain readout. No new element; no lexicon path is honest here
  (aliasing "tabs" onto the masthead would mislead).
- **G7 (row marker / category tag)** — the icon request is prohibited (D-22; `prohibit/imagery-pictograms`); the
  ordinal-marker adaptation is correct. A non-pictographic marker and a caps micro-label tag are ruled-register
  compositions (1px rules, square geometry, D-10 label idiom). Once G13's `component/status` compiles, the
  label family has a citable home; no new canon is needed for the marker itself.
- **G11 (avatar / illustration / photo upload)** — imagery is unlicensed anywhere in the system (D-22;
  `prohibit/imagery-pictograms`; D-16 "imagery absence is a system property"). These requests are
  conflict-resolved, not undefined — the authority already answers them ("do not implement as requested",
  adapted structurally). Canon must not expand; the adaptations (initials block, ruled statement, written note)
  are correct. Strictly, these are the records closest to mis-filed (a handled CONFLICT is not a canon gap);
  they are dispositioned no-action rather than invalid because they usefully document the adaptations.

## Uncertainties & judgment calls

1. **Scope reachability bug (hygiene finding, not fixed here).** Fallback `scope` entries are compared *raw*
   against *stemmed* query tokens, so scope words whose stem differs can never match: `"date"` (stem `dat`) and
   `"toggle"` (stem `toggl`) are currently dead — `"a date field"` and `"a toggle for dark mode"` return
   UNDEFINED despite the words being in scope. The reported gap phrasings passed via other tokens
   ("picker", "switch"), so I kept fixes.json strictly to the gap needs; if upstream wants the dead entries
   live, the minimal values are `"dat"` and `"toggl"` (or normalize scope tokens in the matcher — a compiler
   change, outside this seat's remit).
2. **G6/G2 could later flip to small compile fixes** if recurrence evidence accumulates (tab rows; a
   "readout figure" tile for streak/badge). Judged no-action now under smallest-change.
3. **G10 interpretation caveat.** The source recommends the reversed colourway for large formats; the
   proposal declares the colourway and flags the full-UI-ground application as reviewable.
4. **G14 toast.** Declined by D-13; no toast vocabulary was added. If toast requests recur, upstream could
   consider an explicit signal; not proposed, to keep the change minimal.
5. **G1 granularity.** Proposed as one `pattern/plain-chart` covering three forms; reviewers may split it into
   atomic entries if preferred — the smallest-change shape stands either way.
6. **No INVALID findings.** All 15 records address distinct needs; G11 comes closest to mis-filed (see above)
   but was kept as a documented no-action.
7. **All five proposals are `candidate` status** per the pack's proposal policy (`authority.json`: proposals are
   noncanonical, reviewed upstream; the authority is never modified by a consumer).

## Provenance

- Re-verified with: `da.py resolve` / `da.py search` (CLI, all phrases per gap + synonym probes).
- Fixes/entries verified by in-memory pack simulation (no writes): resolver outcomes quoted above; golden set
  10/10 with fixes applied.
- Filed with: `da.py propose --workspace examples/cadence-dominion` (five proposals; ids above).
- Files written: `examples/cadence-dominion/adjudication/fixes.json`,
  `examples/cadence-dominion/adjudication/proposal-{0a71f9,0d3443,6d60dd,f5a96f,13d338}.json`, this file,
  and the CLI-managed proposal records under `examples/cadence-dominion/.design-authority/proposals/`.
- Not modified: `packs/dominion/`, kernel/compiler, `examples/cadence-dominion/app.*`, `gaps.jsonl` and NOTES.md.
  No git commit; no services touched.
