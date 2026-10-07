# Cadence × wink — gap adjudication (16 requests)

Adjudicator seat for the **wink** Design Authority (pack `wink` v0.1.0). This document judges the
16 gap records in `examples/cadence-wink/.design-authority/gaps.jsonl` against the pack
(`packs/wink/`) and the source-evidence base (`docs/synthesis/wink/` — gestalt, decisions, semantic
review, raw extracts, tile, review sheets). No pack, compiler, app, or gap record was modified;
verdicts below are noncanonical until reviewed upstream.

**Method.** Every gap need was re-resolved through the kernel (`python3 tools/da.py --pack
packs/wink resolve|search ...`), key phrasings were searched for near-misses, and every candidate
lexicon/scope fix was simulated in memory (mutating a loaded Pack instance, never on disk) to prove
the fix resolves the need. Policy lines cited are from `packs/wink/authority.json`
(`policy.on_undefined`, `policy.on_conflict`), the two fallbacks' statements/constraints, and the
golden set's deliberate-UNDEFINED case ("animate the dialog with a spring bounce" — *"gap over
guess"*).

## Summary

| class | count | gaps (suffix) |
|---|---|---|
| PROPOSAL | **6** | `ad4b85`, `a0e2b0`, `f646b2`, `a9d93a`, `d19d36`, `d6853d` |
| LEXICON-FIX | **1** | `399e5e` |
| SCOPE-FIX | **2** | `29cca4`, `d651a0` |
| NO-ACTION | **7** | `b6450a`, `cfe3c5`, `a6f9c7`, `088b69`, `f88682`, `a69c21`, `f4c315` |
| INVALID | **0** | — |

All six proposals were filed through the kernel CLI (`propose`, status `candidate`):

| gap | proposal id | proposed entry |
|---|---|---|
| `gap/20261007-145139-ad4b85` | `prop/20261007-151914-9ff839` | `pattern/destructive-confirm` |
| `gap/20261007-145938-a0e2b0` | `prop/20261007-151914-0510d7` | `pattern/dialog-overlay` |
| `gap/20261007-145938-f646b2` | `prop/20261007-151914-d08fa9` | `pattern/inline-notice` |
| `gap/20261007-145938-a9d93a` | `prop/20261007-151914-74dedc` | `pattern/empty-state` |
| `gap/20261007-145939-d19d36` | `prop/20261007-151915-58de37` | `pattern/progress` |
| `gap/20261007-145939-d6853d` | `prop/20261007-151915-44d062` | `component/status-pill` |

## Full table

| # | gap id | need (short) | class | one-line rationale | verdict ref |
|---|--------|--------------|-------|--------------------|-------------|
| 1 | `gap/20261007-145139-ad4b85` | destructive affordance + confirmation + undo | **PROPOSAL** | Source decision W-16 owns the confirm flow (accepted, never shipped in the pack); undo itself has no evidence, so it is not proposed | `prop/…9ff839` |
| 2 | `gap/20261007-145938-a0e2b0` | modal/dialog vessel + wizard | **PROPOSAL** | W-17 dialog vessel accepted-but-unshipped; multi-step editor flow is named source evidence (raw/04) | `prop/…0510d7` |
| 3 | `gap/20261007-145938-f646b2` | toast / banner / celebration feedback | **PROPOSAL** | W-15 owns the feedback surface — *inline notices, toasts rejected*; the notice pattern is proposed, the toast explicitly is not | `prop/…d08fa9` |
| 4 | `gap/20261007-145938-a9d93a` | empty state + illustration | **PROPOSAL** | W-19 empty pattern accepted-but-unshipped; illustration is deferred by asset policy (W-19/W-23) | `prop/…74dedc` |
| 5 | `gap/20261007-145939-d19d36` | loading spinner + progress ring | **PROPOSAL** | W-18 progress semantics accepted-but-unshipped; the indeterminate spinner is unevidenced | `prop/…58de37` |
| 6 | `gap/20261007-145939-b6450a` | bar chart / heatmap / sparkline | **NO-ACTION** | No chart treatment exists anywhere in the evidence; canon must not invent chart grammar | — |
| 7 | `gap/20261007-145939-d6853d` | streak counter / badge states / status label | **PROPOSAL** | W-14 status pill accepted-but-unshipped; locked badge + streak counter have no evidence (excluded) | `prop/…44d062` |
| 8 | `gap/20261007-145939-cfe3c5` | avatar photo + icon glyph set | **NO-ACTION** | Asset policy: illustration/photography not reproduced (no asset library); no glyph-style evidence | — |
| 9 | `gap/20261007-145939-a6f9c7` | neutral small tag variant | **NO-ACTION** | No tag/chip evidence; badge claims "tag" for the *emphasis* case only; neutral variant is a marked consumer composition (borderline — see notes) | — |
| 10 | `gap/20261007-145939-088b69` | toggle / checkbox / radio styling | **NO-ACTION** | `fallback/platform-controls` already scopes all three (resolve → FALLBACK); platform defaults are the sanctioned answer | — |
| 11 | `gap/20261007-145939-29cca4` | slider / date picker / number stepper | **SCOPE-FIX** | Same fallback already covers `date`/`picker`; `slider` and `stepper` are the same class of native control and are missing from scope | `fixes.json` |
| 12 | `gap/20261007-145939-399e5e` | textarea (multiline field) | **LEXICON-FIX** | The field family already answers it; resolve misses only on phrasing (`notes field`, `multiline input` @4.0; `textarea` ∅) | `fixes.json` |
| 13 | `gap/20261007-145939-f88682` | pagination + drag-to-reorder | **NO-ACTION** | No evidence; the pager composes (outline pill + readout), drag is interaction behaviour that is unevidenced | — |
| 14 | `gap/20261007-145939-a69c21` | CSV export affordance | **NO-ACTION** | No evidence; the affordance composes from `component/action-pill`; the download flow is utility behaviour | — |
| 15 | `gap/20261007-145939-f4c315` | dark-mode theme | **NO-ACTION** | `fallback/light-only` is the sanctioned answer; dark mode is a deliberately carried UNDEFINED in the source gestalt | — |
| 16 | `gap/20261007-145939-d651a0` | photo upload | **SCOPE-FIX** | The fallback's `file` token is exactly right, but the need phrases as "upload" (∅ hit); scope should cover it | `fixes.json` |

## Fixes (exact, machine-readable — also in `adjudication/fixes.json`)

1. **LEXICON-FIX — `gap/…399e5e`** → target `component/field-select`, field `aliases`,
   add `["textarea", "text area", "multiline field", "notes field"]`.
   Evidence: `component/field-select @ 13.0` (search "multiline text field"); `@ 4.0` (searches
   "notes field" and "multiline input" — both hit the family below the 6.5 direct threshold).
   Simulation: `resolve('text area for notes')` → RESOLVED @17.0; `resolve('textarea')` → RESOLVED @9.0.
   (The artifact's own vocabulary is "Field & small-set select" with alias "text field"; a multiline
   field is the same field language extended — the consumer did exactly that, and it was marked
   only because the phrasings missed.)

2. **SCOPE-FIX — `gap/…29cca4`** → target `fallback/platform-controls`, field `scope`,
   add `["slider", "stepper"]`.
   Evidence: `fallback/platform-controls @ 5.0` (search "date picker", matched `date`+`picker` —
   sibling native control already scoped); `slider` / `range slider` / `stepper` produce no entry.
   Simulation: `resolve('slider for daily goal minutes')` → FALLBACK scope `['slider']`;
   `resolve('number stepper for minutes')` → FALLBACK scope `['stepper']`. The fallback's statement
   ("If the system defines no control for a need, use the platform's native element…") is precisely
   this situation; the scope list just under-enumerates.

3. **SCOPE-FIX — `gap/…d651a0`** → target `fallback/platform-controls`, field `scope`,
   add `["upload"]`.
   Evidence: `fallback/platform-controls @ 2.5` (search "file"); resolve of the need phrase returns
   UNDEFINED purely on vocabulary ("upload a photo" shares no scope token). Simulation:
   `resolve('upload a photo for the ritual')` → FALLBACK scope `['upload']`.
   (Add only `upload`: adding `photo`/`image` would mis-route avatar and illustration needs.)

## Proposals (legitimate new-canon needs — all cite accepted Gate-2 decisions the pack never carried)

The six PROPOSAL gaps map exactly onto the accepted-but-unshipped decisions **W-14…W-19** plus the
behavioural multi-step flow named in `raw/04`. In each case the proposed entry is the smallest
carrier of the decided semantics; each proposal explicitly *excludes* the parts of the request that
have no source evidence (no over-reach).

1. `prop/…9ff839` — **`pattern/destructive-confirm`** (G1). Decisions W-16: rounded 16px confirm
   dialog, consequence sentence in the warm voice, confirm = ink-filled pill with the concrete verb
   (never "OK"), cancel = outline pill, destructive never default focus. Composition check: card,
   action-pill and voice exist individually, but the flow's rules are stated nowhere and
   `recipes.json` is empty. **Undo excluded** (no evidence).
2. `prop/…0510d7` — **`pattern/dialog-overlay`** (G2). W-17: white 16px card vessel, 48px padding,
   warm ink scrim `rgba(35,30,21,.35)`, instant appearance (motion deliberately undefined).
   Wizard = named multi-step flow (`raw/04` lines 59/67) that composes this vessel + progress
   readout + action pills; no separate wizard entry claimed.
3. `prop/…d08fa9` — **`pattern/inline-notice`** (G3). W-15: inline notices (rounded 12, tinted
   fill), plain non-blaming question-first copy — *"rather than floating toasts"*. This adjudication
   canonizes the notice; it does **not** canonize the toast (the Cadence toast stays a marked
   improvisation) and does not canonize celebration motion.
4. `prop/…74dedc` — **`pattern/empty-state`** (G4). W-19: tinted Parsnip panel + one warm sentence
   + one action pill. Illustration stays deferred (W-19 alternative; W-23 no asset library).
5. `prop/…58de37` — **`pattern/progress`** (G5). W-18: Parsnip track, yellow fill in flight, ink
   fill when complete, text readout; start/restart pills; pause-and-resume allowed. The ring/track
   shape is an application choice; the indeterminate spinner stays outside canon.
6. `prop/…44d062` — **`component/status-pill`** (G7). W-14: word-first pill — neutral (Parsnip),
   attention (Ochre), positive (ink, no colour), problem (#BF4055 tint); colour supports the word.
   Note: the consumer's improvised yellow "attention" state conflicts with W-14 (Ochre) — the
   proposal fixes that drift. Locked-badge state and streak counter excluded (no evidence; the
   streak number composes from display typography + hierarchy).

## No-action calls (policy line + why canon should not expand)

All cite `authority.json → policy.on_undefined`: *"Implement per the consuming project's fallback
policy, mark the improvisation, and report a gap. Never present improvisation as canonical."*
Reporting was the right move; expanding is not — in each case the expansion would fabricate
evidence the source does not contain, which this authority's golden set explicitly refuses
("gap over guess").

- **G6 data-viz (`b6450a`)** — zero chart treatment in any source (no decision; no raw mention
  beyond "reporting dashboards" as a product area). Consumer charts are constrained to the palette
  (W-R2) but their grammar (axes, scales, legend, series colour) must not be invented. Revisit if
  upstream ever captures chart material.
- **G8 avatar/icons (`cfe3c5`)** — imagery policy: the illustration system is real but *not
  reproduced* (W-23 "no asset library"; W-19 illustration-led states deferred). No avatar or glyph
  style was captured (live alts show icons exist, nothing about their drawing). Initials avatar +
  line glyphs remain marked improvisations.
- **G9 neutral tag (`a6f9c7`)** — no tag/chip evidence anywhere (checked raw extracts, decisions,
  tile, review sheets; the tile's only badge is the yellow "Most popular"). The pack's
  `component/badge` claims "tag" (search @9.0) for the *emphasis* case; a *neutral* variant is a
  composition of owned materials (Parsnip surface + pill geometry + ink text) kept as marked
  improvisation. **Borderline** — see notes below.
- **G10 toggle/checkbox/radio (`088b69`)** — resolve returns FALLBACK for all three
  (`matched_scope`: switch / checkbox / radio); the fallback's constraint ("mark the
  improvisation and report a gap if the need recurs") was honoured by the report, and the
  sanctioned answer — platform-native control + field styling — stands. There is no control-styling
  evidence to canonize.
- **G13 pagination/drag (`f88682`)** — no evidence. The pager composes from `action-pill` (outline)
  + a text readout; drag is an interaction behaviour with no visual evidence. Keep marked.
- **G14 CSV export (`a69c21`)** — no evidence; the affordance composes from `component/action-pill`;
  the Blob/download flow is utility behaviour outside visual canon. Keep marked.
- **G15 dark mode (`f4c315`)** — the fallback/light-only statement is the authority's answer:
  *"No dark-mode canon exists; if a dark surface is unavoidable, keep ink/yellow roles and mark the
  improvisation."* Dark mode is a **deliberately carried UNDEFINED** in the source gestalt
  (01-gestalt.md, "Carried UNDEFINEDs"). The pack golden expects FALLBACK here and passes (9/9).
  Canon should not expand without dark-mode evidence.

## Uncertainties, mismatches, and deliberately excluded parts

- **G9 is the one judgment call.** A `LEXICON-FIX` adding `category tag`/`chip` aliases to
  `component/badge` resolves mechanically (`resolve('small category tag')` → RESOLVED @22.0 in
  simulation) — but it would route non-emphasis labels to a yellow *Emphasis* badge, which
  contradicts the pack's own role discipline (W-21/W-06). A `PROPOSAL` for a neutral variant has
  only adjacent support (W-14's neutral Parsnip tone), not a tag decision. Chosen: **NO-ACTION**
  under the conservative rule ("would the source genuinely own this?" → not evidenced), flagged as
  the least-certain verdict. If upstream wants a minimal middle path: a one-line note on
  `component/badge` clarifying that non-emphasis labels are not covered would prevent silent
  yellow-for-all-tags routing.
- **Select treatment mismatch (not one of the 16 gaps).** NOTES.md element 25 flags that
  decisions.json W-13 (Gate-2 revision) directs "more rounded (12px) with serif field text" for the
  small-set select, while the pack's `component/field-select` carries the radius-8 field states;
  the builder correctly stayed pack-literal. Recommend upstream reconcile W-13's revision with the
  artifact (pack-data issue, no gap filed, no fix invented here).
- **Deliberately excluded from proposals (no source evidence):** undo/recovery (G1), dialog
  motion (G2), floating toasts + celebration animation (G3), illustration style (G4), indeterminate
  spinner (G5), locked badge state + streak-counter element (G7). Each stays a marked
  improvisation; a future evidence capture could reopen them.
- **Zero INVALID.** All 16 records were checked for mis-filing/duplication: each names a distinct,
  real, recurring need not covered elsewhere in the set (the three form-control gaps — G10/G11/G12 —
  target different controls; G1's confirm dialog and G2's vessel overlap in usage but not in scope);
  the fallback-origin reports (G10/G15/G16) are explicitly invited by the fallback constraints.
  Nothing was rejected as invalid on the evidence available.
- **Verification limits.** Judged only against `packs/wink/` + `docs/synthesis/wink/` (no network,
  no other packs/dirs). Fix simulations were in-memory only. Scores cited are the kernel's own
  (`da search` / resolve evidence); re-verification was run after the pack's mtime (2026-10-07
  14:47) and matches NOTES.md's recorded scores where they overlap (`tag`@9.0, `file`@2.5).

## Appendix — key verification runs (kernel CLI)

```
resolve('delete a ritual permanently')        -> UNDEFINED ; searches delete/destructive/undo/confirm/dialog/scrim: no hits
resolve('modal with ritual details')          -> UNDEFINED ; modal/dialog/overlay/wizard/onboarding/popup: no hits
resolve('toast notification saying logged')   -> UNDEFINED ; toast/notice/banner/feedback: no hits
resolve('empty state when no rituals exist')  -> UNDEFINED (closest component/card@1.0)
resolve('loading spinner while saving')       -> UNDEFINED ; spinner/progress/meter: no hits
search('bar chart')                           -> component/navbar@4.0 ('bar' noise) ; chart/heatmap/sparkline: no hits
resolve('big streak counter')                 -> UNDEFINED ; search('badge') -> component/badge@9.0
resolve('profile avatar photo')               -> UNDEFINED ; avatar/photo/icon/glyph: no hits
resolve('small category tag')                 -> UNDEFINED (closest badge@4.0); search('tag') -> badge@9.0
resolve('toggle switch in settings')          -> FALLBACK fallback/platform-controls (scope: switch)
resolve('slider for daily goal minutes')      -> UNDEFINED  [SCOPE-FIX applies]
resolve('date picker for the log entry')      -> FALLBACK fallback/platform-controls (scope: date,picker)
resolve('text area for notes')                -> UNDEFINED (field-select@4.0)  [LEXICON-FIX applies]
resolve('pagination for older entries')       -> UNDEFINED ; export/download/drag/pager: no hits
resolve('a dark mode theme')                  -> FALLBACK fallback/light-only (scope: dark)
resolve('upload a photo for the ritual')      -> UNDEFINED  [SCOPE-FIX applies]
golden (packs/wink/golden.json)               -> agreement 9/9 (100%) — incl. checkbox->FALLBACK, dark->FALLBACK, spring-bounce->UNDEFINED
```

Proposals filed via `da propose` (all `status: candidate`, six required fields present,
`depends_on` restricted to real pack ids):

```
ad4b85 -> prop/20261007-151914-9ff839   (pattern/destructive-confirm)
a0e2b0 -> prop/20261007-151914-0510d7   (pattern/dialog-overlay)
f646b2 -> prop/20261007-151914-d08fa9   (pattern/inline-notice)
a9d93a -> prop/20261007-151914-74dedc   (pattern/empty-state)
d19d36 -> prop/20261007-151915-58de37   (pattern/progress)
d6853d -> prop/20261007-151915-44d062   (component/status-pill)
```
