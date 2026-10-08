# 03 · Independent verification of the existing Cadence builds

Verified: **examples/cadence3-wink · cadence3-leader · cadence3-dominion**
(built on the codified 0.2.0 authorities; see `00` for the scope decision).
Raw results: `raw/{wink,leader,dominion}-clean/raw.json` + `summary.txt`.
The verifier never consulted the build agents' notes; agent claims below are
listed only to *compare* claim against observation.

## Headline

| build | checks | PASS | VIOLATION | UNVERIFIABLE | REVIEW_REQUIRED |
|---|---|---|---|---|---|
| cadence3-wink | 29 | 25 | **0** | 0 | 4 |
| cadence3-leader | 23 | 19 | **0** | 0 | 4 |
| cadence3-dominion | 22 | 19 | **0** | 0 | 3 |

**For the cooperative builds, every independently verifiable claim held.**
That is the honest result for strong-agent builds — and precisely why it
cannot distinguish enforceability from cooperation: the discriminating test
is the mutation experiment (`04`–`05`). Claims below turned out *consistent*
with verification; they were neither necessary (the verifier does not read
them) nor sufficient (a future careless agent can carry the same marks).

## cadence3-wink — claim vs verifier

| authority item | target | agent claim (marks/notes) | verifier | observed |
|---|---|---|---|---|
| component/action-pill | `.cta` | CANONICAL (unmarked) | PASS | radius 26px (pill), yellow fill, ink ring, 13/500 |
| component/action-pill | `.cta.dark` | CANONICAL | PASS | ink fill rgb(36,28,21) + white label |
| component/card | `.card` | CANONICAL | PASS | radius 16, borderless, warm shadow |
| rule/W-R2 palette | app.css | CANONICAL (implicit) | PASS | 32 literals, all allowlisted (ink-shade allowlist noted) |
| pattern/dialog-overlay | `.dlg` | CANONICAL | PASS | radius 16, white, padding 48; scrim rgba(35,30,21,.35); no motion |
| pattern/destructive-confirm | confirm flow | CANONICAL | PASS | dialog opens; focus NOT on `#confirmDelete` |
| component/badge | `.badge` | **improvised** ("composed: card + badge + numerals") | PASS | pill 999, yellow, 12/600 — conforms to the badge canon it composes with |
| rule W-14 status | `.status` | **adapted** ("words + tint composition") | PASS | text present; wording adequacy → review |
| pattern/empty-state | `#emptyState` | **adapted** ("illustration omitted — W-19") | PASS | no img/svg in panel |
| v3.1 tick | `.log-tick` | **improvised** ("outside verdict — boundary-exempt") | PASS (marked) | 5 × `[data-improvised]` ticks; geometry per its record |

## cadence3-leader — claim vs verifier

| authority item | target | agent claim | verifier | observed |
|---|---|---|---|---|
| rule/L-R1 | `.btn` | fallback *(nearest marked ancestor: wizard inner controls)* | PASS | radius 8 |
| component/action | `.b-navy` | fallback *(same ancestor)* | PASS | #2E45B8 + white |
| component/action | `.b-out` | improvised *(nearest marked ancestor)* | PASS | 2px ink outline, white |
| component/tag | `.tag` | CANONICAL | PASS | radius 8, 2px ink, uppercase; `.tag.attn` solid red |
| component/field | `.err` | CANONICAL | PASS | red family line |
| prohibition ambient-glow | app.css | CANONICAL | PASS | zero box-shadow declarations |
| prohibition red-surface | page scan | CANONICAL | PASS | max red-block area below 10% viewport |
| prohibition decorative-noise | page text | CANONICAL | PASS | no emoji, no "!" |
| rule/L-R2 palette | app.css | CANONICAL | PASS | 37 literals allowlisted (families) |
| guideline motion | `.btn` | CANONICAL | PASS | no keyframes; transitions ≤0.12s |

## cadence3-dominion — claim vs verifier

| authority item | target | agent claim | verifier | observed |
|---|---|---|---|---|
| component/action | `.b-slate` | CANONICAL | PASS | #26374A, radius 4 |
| component/field | `.field input` | fallback *(native control + field language)* | PASS | radius 4, border #E0E0E0 |
| rule/D-R1 focus | input focus | CANONICAL | PASS | blue glow `rgb(102,175,233)` signal |
| rule/D-R2 ceremony | `.identity .acc`, `.ceremony .acc-red` | CANONICAL / **adapted** | PASS | red-family accents as ceremony |
| prohibition red-status | `.st/.err/.notice` scan | CANONICAL | PASS | 0 red hits in status/error/reading roles |
| guideline/bilingual | `.bil` pairs | **adapted** (pairing composition) | PASS | 5/5 pairs EN+FR non-empty |
| prohibition elevation-shadows | app.css | CANONICAL | PASS | only the focus glow survives |
| prohibition imagery | page | CANONICAL | PASS | no img; no svg beyond sanctioned `.spark` |
| component/ledger, notice, meter | DOM | adapted/CANONICAL | PASS | 2px black rules; grey band; black fill |

## Notes that matter for the experiment

1. **Claim agreement ≠ verification.** The verifier produced identical results
   with claims entirely hidden; every above claim row was decided from computed
   style / DOM / files alone.
2. **Claims locate attention, not truth.** On leader, the element-level claim
   walk surfaced nearest *marked ancestors* (wizard/quarantine containers), not
   the element's own status — a reminder that annotations are hints; the
   contracts never assert them.
3. **REVIEW_REQUIRED is real work, not a rounding error:** 11 items (tone,
   register, harmony, chart/ceremony character, hover spring, hierarchy
   calibration, bilingual quality) are emitted to humans — see `07` for how
   they surface in the lens.
4. **Three verifier-side corrections were required during calibration** (all
   recorded in session logs): box-shadow serialization order, hidden-first
   element selection (revealed views), and scenario side effects (dialog left
   open). Each was a verifier bug, not an implementation finding — the clean
   builds flagged zero genuine violations.
5. **Two authority-side ambiguities surfaced** and were recorded rather than
   silently absorbed: wink's palette admits non-token ink shades; dominion's
   build declares an amber family outside the pack's stated families. Both are
   `AMBIGUOUS-RULE` candidates in `06`/`07`.
