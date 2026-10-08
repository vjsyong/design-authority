# 01 · Rule verifiability audit — wink · leader · dominion

**Question:** for every normative item that could affect implementation, can an
independent system establish conformance from observable evidence?

**Audited universe (per authority):** all `rules[]` (2/2/2) and
`prohibitions[]` (2/5/4); every artifact carrying enforceable statements
(components with `verify` selectors + states; patterns with geometry/a11y
statements; guidelines with determinable claims; token-sets); and the
cross-cutting precedents/doctrine statements with observable surfaces
(imagery absence, motion absence, marking). Prose-only editorial items
(voice, register, harmony) are audited as REVIEW rather than dropped.

Each item was classified into exactly one class and, where deterministic
verification is possible, materialised as a check in the pack's
`verification.json` (format: `02-verification-contract.md`).

## Counts

| authority | checks | MECHANICALLY | PARTIALLY | REVIEW | NOT_CURRENTLY |
|---|---|---|---|---|---|
| wink | 29 | 21 | 4 | 3 | 1 |
| leader | 23 | 16 | 3 | 3 | 1 |
| dominion | 22 | 17 | 2 | 2 | 1 |
| **total** | **74** | **54 (73%)** | **9 (12%)** | **8 (11%)** | **3 (4%)** |

By verification mode: COMPUTED_STYLE 32 · STATIC 13 · INTERACTION 10 ·
DOM 8 · REVIEW 11.

## Class criteria (as applied)

- **MECHANICALLY_VERIFIABLE** — a deterministic observation decides it:
  computed-style relations (radius, colour, shadow, stroke, type), DOM
  structure (absence of imagery/svg, status text presence, bilingual pairs),
  file-level patterns (forbidden literals, motion rules, url() assets),
  scripted interaction (focus visibility, destructive non-focus, dialog
  state, floating-surface scan, colour-role scans).
- **PARTIALLY_VERIFIABLE** — a deterministic check covers the core claim but
  leaves a judgement edge. Examples carried: palette *shade* allowlists
  (hues are mechanical; the six-token strictness is curatorial), "red never a
  reading surface" (area heuristic ≤10%), "status words first" (presence
  mechanical; wording adequacy review), error colour (rule-level presence;
  behavioural flow deferred), "marked improvisation" (marking presence;
  quality review).
- **REVIEW_REQUIRED** — no honest deterministic reduction: tone ("warm,
  playful"), register ("editorial restraint"), harmony, ceremony character,
  chart character, red-as-punctuation *character*.
- **NOT_CURRENTLY_VERIFIABLE** — no reliable inspection method yet: hover
  spring character (W-03), cross-view hierarchy calibration (leader),
  bilingual tone parity (dominion).

## Easiest and hardest (evidence from the build/contract work)

Easiest: computed-style geometry and colour on single elements (13/13 wink
computed checks passed first run after two contract corrections). Hardest:
(a) semantics — "words first", "punctuation not alarm"; (b) absence claims
(no imagery, no motion, no toasts) — the verifier must scan whole documents
and *scope correctly*; (c) anything involving state (focus, dialogs) —
interaction scripting is where the verifier needed care to avoid side
effects (an early run failed itself by leaving a dialog open).

## Notable audit findings (recorded, not auto-fixed)

1. **Toast/floating surface had no check** — the only exposure was a
   contrast note (W-15). Added a mechanical `no-floating-surfaces` scan
   (fixed-position elements beyond instrument/nav/scrim). This is a
   *coverage addition*, not an authority change.
2. **Instrument scoping is unavoidable** — all three builds' marks layers
   use colours outside the palette (#B26A00 leader; amber dominion). The
   verifier excludes instrument rules (`.marks-*`, `[data-*]`, `.mark-*`,
   `#provPanel`) from all colour/shape scans; this scoping rule is itself a
   recorded verification design decision (tooling is not app UI).
3. **Dominion amber family** (`#B7791F`/`#7A4E00`) is declared in the build
   but sits outside the pack's stated families — allowlisted here with a
   note; flagged as an `AMBIGUOUS-RULE` candidate for the authority owners
   (see `07`).
4. **`verify` selectors already exist in artifacts** — the packs' components
   carry `body.verify` hints (`['.cta', '.cta.dark', '.cta.outline']`); the
   contracts build on them where possible, keeping the verification contract
   close to the authority's own idiom without kernel changes.
5. **Precedent claims are outside-conformance marks** — e.g. wink's tick is
   a *sanctioned* improvisation (`outside` verdict). The verifier checks the
   implementation's observable claims (marking present, geometry from the
   element itself) but the authority does not supply a constraint for
   "un-codified" behaviour; those stay PARTIAL/REVIEW by design.
