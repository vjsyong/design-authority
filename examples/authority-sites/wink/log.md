# Authority call log — Wink Interface System site build

All calls made through `./run-authority` (the audited runner; `audit.jsonl` holds the
machine trace of every call, argv + rc + raw output). This file is the narrative
companion: every call in order — exact syntax, trimmed output, one Why + conclusion line.
Deliverable: `index.html` + `fonts/` (3 files) + this log.

Total: 48 calls (cap ~35 — the overrun is the boundary-probe hunt for the two
prohibitions, which no listing surface enumerates; see calls 24–35).

---

**[1] `./run-authority overview`**
```
wink — 0.2.0 (format 0.1)
snapshot: mailchimp.com live product + Mailchimp brand resources @ n/a - deri…
artifacts: component=6, guideline=4, pattern=5, token-set=2
rules=2 recipes=0 fallbacks=2 prohibitions=2
resolution: CONFLICT -> RESOLVED -> COMPOSE -> FALLBACK -> UNDEFINED
```
Why + conclusion: orient before any build. The pack holds 17 artifacts in 4 kinds, 2 rules, 2 prohibitions, 2 fallbacks, 0 recipes; the catalogue must cover all 17, and no COMPOSE outcomes are possible.

**[2] `./run-authority search "mailchimp" --limit 100 --json`**
```
[]
```
Why + conclusion: probe whether brand/source tokens enumerate the catalogue; they do not — a wider vocabulary sweep is required.

**[3] `./run-authority search "component pattern guideline token set colour color typography type font heading title text body label button link card chip badge tag banner alert modal dialog form input select checkbox radio field table list row cell grid layout section header footer navigation sidebar menu hero logo icon imagery spacing radius corner border shadow motion animation accessibility contrast focus state hover active empty error success warning info avatar tooltip accordion tabs breadcrumb pagination progress divider accent surface ink canvas brand product" --limit 100 --json`**
```
 33.5 component/field-select · 29.0 component/ledger · 28.5 precedent/status-pill-rejected
 25.0 token-set/colour · 22.5 guideline/typography · 21.5 pattern/dialog-overlay
 18.5 guideline/hierarchy · 18.0 token-set/type-scale · 16.0 component/navbar
 15.5 component/card · 14.5 pattern/empty-state · 12.5 component/action-pill
 12.5 precedent/declined-photographic-imagery · 12.0 component/badge
 11.0 fallback/platform-controls · 11.0 guideline/shape-language
  8.5 pattern/destructive-confirm · 8.5 pattern/progress · 4.0 candidate/pager-composition
  3.5 fallback/light-only · 1.5 pattern/inline-notice
```
Why + conclusion: wiki-style vocabulary sweep to enumerate the whole catalogue in one audited call. 16 of 17 artifacts found (one guideline and the rules/prohibitions still missing) plus both fallbacks, both precedents and one candidate.

**[4] `./run-authority search "voice tone writing editorial content copy words language naming messaging logo freddie chart graph data density theme dark responsive breakpoint grid column container width rhythm keyboard screenreader motion reduced illustration photography asset a11y" --limit 100 --json`**
```
 16.0 guideline/voice — Voice
 (+ weaker secondary hits: precedent/declined-photographic-imagery 10.5, pattern/empty-state 7.0, …)
```
Why + conclusion: second sweep for the missing guideline. `guideline/voice` found — 17/17 artifacts now enumerated and cross-checked against the overview counts (6+4+5+2).

**[5] `./run-authority golden --json`**
```
total 56, passed 2, rate 0.036
 sample rows: "a primary button" → RESOLVED component/action-pill (expected component/btn)
              "a switch" → FALLBACK fallback/platform-controls · "dark mode" → FALLBACK fallback/light-only
              "the colour tokens" → UNDEFINED (the record exists — retrieval is brittle)
```
Why + conclusion: inspect the pack's golden set for a boundary/id surface. It is not usable as an adoption source (it targets ids this pack does not carry, 2/56) — but it teaches two things: the resolver needs record vocabulary (rephrase rather than trust single misses), and dark-mode asks are fallback territory.

**[6] `./run-authority overview --json`**
```
authority: wink 0.2.0 · "n/a - derived from public sources, not a repository"
description: "A friendly, clearly-designed interface system derived from the Mailchimp brand and live
  product for the Design Authority synthesis experiment. Warm, pill-shaped, playful; no Mailchimp
  marks reproduced."
capabilities: validators [] · resolution_assist "off"
policy: on_undefined "Implement per the consuming project's fallback policy, mark the improvisation,
  and report a gap. Never present improvisation as canonical."
```
Why + conclusion: the masthead needs name/version/one-line description and the build needs the policy text. Description + version adopted for the masthead; on_undefined governs the gap behaviour; no validators exist, so no post-build validate call is available.

**[7] `./run-authority inspect token-set/colour`**
```
id: token-set/colour · "Colour roles"
summary: Roles: yellow = brand field + primary action only; peppercorn = text, ink, shadow tint; white +
  Parsnip = surfaces; Ochre = section band terminator; Kale = links inside content; #BF4055 = error text/fills.
aliases: palette, colour, color, yellow, peppercorn, ink colour · source: Gate 2 accepted decisions: W-06
```
Why + conclusion: the token set carries the values; read before any styling. Roles are recorded by name — hexes for Parsnip, Ochre and Kale are absent (recorded later as a gap, call [47]).

**[8] `./run-authority inspect token-set/type-scale`**
```
summary: Screen scale: display 48–64px w400 tight tracking (−1.2px at 64); section 35px/1.0; body 16/1.35;
  small 14; labels/buttons 13/500. · source: W-05
```
Why + conclusion: sizes adopted exactly — display clamp 48→64, section 35/1.0, body 16/1.35, small 14, labels 13/500.

**[9] `./run-authority inspect guideline/typography`**
```
summary: Two registers: soft-serif display for hero/section headlines (italic emphasis fragment allowed);
  grotesque sans for all body, UI, labels and metadata. Serif is the exception, never the working voice. · W-04
```
Why + conclusion: register mapping adopted — Fraunces (display) / Inter (everything else), italic fragment in the h1.

**[10] `./run-authority inspect guideline/hierarchy`**
```
summary: One page title; sections = small uppercase label → display headline → 1–2 sentence paragraph.
  Numbers may take display treatment for proof moments. · W-10
```
Why + conclusion: section anatomy adopted for both sections (01/02 labels → display headline → short paragraph).

**[11] `./run-authority inspect guideline/shape-language`**
```
summary: Shape encodes class: interactive = pill (always with the 1px ink ring); content vessel = 16/24
  soft-radius; structural chrome (bands, dividers, page blocks) = square. · W-08
```
Why + conclusion: the pill/vessel/square discipline drives every radius on the page; the CTA keeps its 1px ink ring.

**[12] `./run-authority inspect component/card`**
```
summary: Content cards: white, borderless, radius 16 (24 for large), elevation via warm ink-tinted shadow
  rgba(35,30,21,.2) 0 8px 32px; interior padding 48. Tinted variant: Parsnip, no shadow. 1px borders
  (#DEDDDC) only on inputs/dividers, never as card devices. · W-07
```
Why + conclusion: the catalogue vessel — adopted verbatim (shadow, radius 16, padding 48, no borders on cards).

**[13] `./run-authority inspect component/navbar`**
```
summary: Top bar: white background; dark links; dropdown items carry chevrons; hover = light-grey
  rounded-rect fill; primary CTA at right end; must stay single-row (no wrapping). · W-11
```
Why + conclusion: the page top rail — adopted (single row enforced at every width; CTA at right end).

**[14] `./run-authority inspect component/badge`**
```
summary: Emphasis badges: pill, yellow fill, 12/600 label (e.g. 'Most popular' on the selected
  plan/category). · W-21
```
Why + conclusion: inspected for the catalogue. Not instantiated on this page — the page's yellow is the recorded brand field + the CTA, and the kind markers are the recorded small-label treatment, so no emphasis badge was warranted.

**[15] `./run-authority inspect component/action-pill`**
```
summary: Primary action = pill, filled Cavendish Yellow #FFE01B with a 1px ink ring (box-shadow
  0 0 0 1px #231E15 — live-measured), label in Peppercorn ink. On yellow/warm fields, primary switches
  to the dark variant. Secondary = outline pill (2px ink inset).
states: … hover: translateY(-4.875px) + hard ink shadow 0 4.875px 0 0 (live-measured, zero blur) · W-01..03
```
Why + conclusion: the CTA language — adopted (yellow fill, ink ring, ink label, recorded hover lift with zero-blur hard shadow).

**[16] `./run-authority inspect component/ledger`**
```
summary: Ledger: white surface, 16px padded rows, hairline #DEDDDC dividers (no zebra striping), header
  row in Parsnip with 13/500 labels; row hover = Parsnip tint; status pill inline; text links in ink
  with underline. · W-20
```
Why + conclusion: the specification table's vessel — adopted (hairline rows, no zebra, 13/500 header, hover tint).

**[17] `./run-authority inspect component/field-select`**
```
summary: Native select styled as a field for small fixed sets (≤ ~12): more rounded (12px) with serif
  field text per Gate 2 review. Larger or filtered selection out of scope; use the platform-controls
  fallback and mark it. · W-13
```
Why + conclusion: catalogue entry; no field is built on a documentation page. Its recorded 12px radius informed the nav-hover rect.

**[18] `./run-authority inspect guideline/voice`**
```
summary: Second person, question-first, plain English, non-blaming; dry wit allowed in microcopy;
  italic serif emphasis fragment allowed in headlines. · W-22
```
Why + conclusion: page prose written to this register (question-first section ledes, plain sentences).

**[19] `./run-authority inspect pattern/dialog-overlay`**
```
summary: Dialog/overlay vessel: white 16px-rounded card on a warm ink scrim, instant appearance
  (no motion invented), content composed from existing primitives.
```
Why + conclusion: pattern read for the catalogue; not instantiated (a documentation page has no overlays) — listed with its recorded summary.

**[20] `./run-authority inspect pattern/empty-state`**
```
summary: Empty states are a centered notice card: serif headline, one plain warm sentence,
  one primary pill action.
```
Why + conclusion: pattern read for the catalogue; not instantiated (the page has no zero-content moment) — listed with its recorded summary.

**[21] `./run-authority inspect pattern/destructive-confirm`**
```
summary: High-consequence actions route through a rounded 16px confirm dialog with a consequence
  sentence in the warm voice; confirm = ink-filled pill labelled with the concrete verb (never 'OK');
  cancel = outline pill; the destructive action never receives default focus.
```
Why + conclusion: pattern read for the catalogue; not instantiated (no destructive actions exist on the page) — listed with its recorded summary.

**[22] `./run-authority inspect pattern/progress`**
```
summary: Progress: yellow fill (#FFE01B) on a parsnip track, fully rounded; pair with a short step
  caption; no indeterminate motion.
```
Why + conclusion: pattern read for the catalogue; not instantiated (no progress moment on the page) — listed with its recorded summary.

**[23] `./run-authority inspect pattern/inline-notice`**
```
summary: Inline notices: parsnip-filled rounded block with a bold lead sentence and a plain
  supporting line; no toast pattern observed.
```
Why + conclusion: pattern read for the catalogue; not instantiated (no feedback moment on the page) — listed with its recorded summary.

**[24] `./run-authority resolve "add a gradient, a drop shadow, photographic imagery and an illustration to the hero" --json`**
```
OUTCOME: UNDEFINED · closest: component/card 1.5, guideline/typography 1.5, token-set/colour 1.5
precedents: [governs] precedent/declined-photographic-imagery — "photography and illustration are not
  reproduced; use monograms and words instead."
```
Why + conclusion: boundary probe 1 — imagery is precedent-governed (not prohibited); gradients and shadows carry no constraint trigger. No prohibition surfaced.

**[25] `./run-authority resolve "animate the dialog with a bounce, add a toast notification, an indeterminate spinner and a yellow status pill; use the hex #ff00ff for the accent" --json`**
```
OUTCOME: UNDEFINED · closest: component/action-pill 5.5, pattern/destructive-confirm 5.5, pattern/inline-notice 5.5
precedents: [governs] precedent/status-pill-rejected — "Express status with words plus component/badge…"
```
Why + conclusion: boundary probe 2 — motion/toasts/spinners are undefined land (not prohibited), status pills are precedent-governed, and there is no colour-literal trigger. No prohibition surfaced.

**[26] `./run-authority resolve "add the Mailchimp wordmark and the Freddie mascot to the top bar; use a thick border as the card device; let the top bar wrap onto two rows; add zebra striping to the ledger rows; use yellow for the body text; remove the ink ring from the interactive pills" --json`**
```
OUTCOME: RESOLVED → component/ledger (score 15.5; matched: striping, ledger, ink, row, text, zebra, pill)
```
Why + conclusion: boundary probe 3 — none of these themes is prohibited; "zebra striping" is refused by the ledger record's own constraint. No prohibition surfaced.

**[27] `./run-authority resolve "square corners on the buttons; square pills; give the cards a 1px border; a bordered card surface; set the body text in the serif font; serif body copy for paragraphs; add a glow around the card" --json`**
```
OUTCOME: CONFLICT
 prohibition: prohibit/square-buttons — "Square or sharp button shapes — buttons are pills (W-02, W-08)."
 rule (linked): W-R1, severity error — "Buttons are pills; no square primary buttons anywhere."
 detected: signal 'square corners'
```
Why + conclusion: boundary probe 4 — **prohibition #1 surfaced**: square button shapes. Its linked rule W-R1 is the first of the two rules.

**[28] `./run-authority resolve "let the top bar wrap onto a second line; a second page title; two primary actions in the empty state; label the confirm button OK; add exclamation marks; add an emoji; add an undo button; underline the headings" --json`**
```
OUTCOME: RESOLVED → component/action-pill
```
Why + conclusion: boundary probe 5 — none of these themes is prohibited (no wrapping ban trigger, no OK-label trigger, no emoji trigger). No prohibition surfaced.

**[29] `./run-authority resolve "give the cards a border; a bordered card surface; set the body in the serif; serif paragraphs; add a glow; use a red background for the section; a green accent; a purple heading; set the headline in all caps; add a third font; a decorative font for the body" --json`**
```
OUTCOME: RESOLVED → guideline/typography
```
Why + conclusion: boundary probe 6 — no prohibition for card borders, serif body, glow, red/green/purple, caps or extra fonts on this pack.

**[30] `./run-authority resolve "set the headlines in the sans font; the hero in the sans; yellow cards; purple buttons; blue primary buttons; an icon-only button; buttons without the ink ring; centre all the text; italicise the body copy; two columns of body text; corporate jargon in the copy; another row for the nav links" --json`**
```
OUTCOME: RESOLVED → guideline/typography
```
Why + conclusion: boundary probe 7 — no prohibition for sans headlines, coloured buttons/cards, icon-only buttons, ring removal or copy register. No prohibition surfaced.

**[31] `./run-authority resolve "round the corners of the section bands; rounded page blocks; round the footer band; a frosted glass card; a blur behind the dialog; translucent panels; a 3D beveled button; a textured background; rotate the cards slightly; a dark mode version of the page; lowercase section labels" --json`**
```
OUTCOME: FALLBACK → fallback/light-only —
 "No dark-mode canon exists; if a dark surface is unavoidable, keep ink/yellow roles and mark the
  improvisation." (constraints: keep the palette roles; mark the improvisation)
```
Why + conclusion: boundary probe 8 — dark surfaces route to the recorded fallback (not a prohibition); glass/blur/3D/texture/rotation carry no constraint. Bonus: the fallback statement captured for the spec section.

**[32] `./run-authority inspect W-R1`**
```
id W-R1 · name "pill-language" · severity error · applies_to [css, html]
summary: Buttons are pills; no square primary buttons anywhere.
why: Observed live (radius = half height) and reaffirmed at Gate 2.
fix: Replace square corners on buttons with the pill radius.
```
Why + conclusion: the conflict at [27] cited W-R1; read in full for the specification section — quoted verbatim there.

**[33] `./run-authority inspect W-R2`**
```
id W-R2 · name "palette-discipline" · severity warning · applies_to [css, html]
summary: Colours come from the wink palette only: Cavendish Yellow, Peppercorn ink, Parsnip, Ochre,
  Kale, #BF4055 error. · fix: Map the colour to the nearest palette token.
```
Why + conclusion: rules=2, so W-R2 is the second rule — found and read. It is colour-related, so the second prohibition is likely colour-related too.

**[34] `./run-authority resolve "use my company's brand colours; a custom colour for the header; an off-palette accent; a colour outside the wink palette; a colour that isn't in the palette; add a new colour; a different shade of yellow to match my logo" --json`**
```
OUTCOME: RESOLVED → token-set/colour
```
Why + conclusion: colour probe round 1 — absorbed by the colour record; no prohibition trigger yet. One more probe with sharper vocabulary needed.

**[35] `./run-authority resolve "use pure black #000000 for the body text; a neon accent colour; cyan and magenta accents; make the headlines heavy bold; a light grey body text for a subtle effect; thin pale labels" --json`**
```
OUTCOME: CONFLICT
 prohibition: prohibit/off-palette-colours — "Colours outside the wink palette, including pure black
  text and clinical cold greys (W-06)."
 rule (linked): W-R2, severity warning (palette-discipline)
 detected: signal 'pure black'
```
Why + conclusion: boundary probe 10 — **prohibition #2 surfaced**: off-palette colours. Both rules and both prohibitions now in hand; the specification section is fully sourced.

**[36] `./run-authority resolve "a display font for the headlines and a body font for the text" --json`**
```
OUTCOME: RESOLVED → guideline/typography
```
Why + conclusion: page need — type registers resolved to the recorded guideline; Fraunces/Inter adopted.

**[37] `./run-authority resolve "the colour roles for ink, surfaces, accents and links on the page" --json`**
```
OUTCOME: RESOLVED → token-set/colour
```
Why + conclusion: page need — the colour roles resolved; yellow (brand field + CTA), ink, white, hairline adopted; Kale links realized as ink+underline per the ledger record.

**[38] `./run-authority resolve "a top bar with navigation links for the page" --json`**
```
OUTCOME: RESOLVED → component/navbar
```
Why + conclusion: page need — top bar resolved; built as the recorded navbar (white, dark links, hover fill, CTA at right end, single row).

**[39] `./run-authority resolve "a card for each catalogue entry" --json`**
```
OUTCOME: UNDEFINED · top candidate component/card scored 4.00 vs 6.50 needed
```
Why + conclusion: retrieval miss — the record exists (inspected at [12]); the ask matched only one token. Rephrase with the record's own vocabulary rather than accepting the miss.

**[40] `./run-authority resolve "a card surface for each catalogue entry" --json`**
```
OUTCOME: RESOLVED → component/card
```
Why + conclusion: page need — resolved on rephrase ("card" + "surface"); the catalogue cards adopt the recorded card treatment.

**[41] `./run-authority resolve "ledger rows for the specification summary" --json`**
```
OUTCOME: RESOLVED → component/ledger
```
Why + conclusion: page need — the specification summary renders as the recorded ledger.

**[42] `./run-authority resolve "the section rhythm with a small label and a display headline" --json`**
```
OUTCOME: RESOLVED → guideline/hierarchy
```
Why + conclusion: page need — section anatomy resolved; both sections use label → headline → paragraph.

**[43] `./run-authority resolve "a footer attribution line for the page" --json`**
```
OUTCOME: UNDEFINED · closest: guideline/hierarchy 4.0, guideline/shape-language 1.5, pattern/inline-notice 1.5
```
Why + conclusion: the authority is silent on footer furniture → build from nearest recorded pieces, mark the improvisation, file a gap ([45]).

**[44] `./run-authority resolve "a page that stacks to a single column on small screens" --json`**
```
OUTCOME: UNDEFINED · closest: guideline/hierarchy 5.5, token-set/type-scale 4.5
```
Why + conclusion: no responsive record exists → stacking built from the nearest recorded pieces, marked, gap filed ([46]).

**[45] `./run-authority gap-add --need "a footer attribution line (page furniture for a documentation page under this authority)" --context '{"source":"examples/authority-sites/wink","page":"index.html","attempted":"resolve UNDEFINED: closest guideline/hierarchy 4.0, shape-language 1.5 (no footer record)","fallback":"built from nearest recorded pieces (typography + colour + dividers); improvisation marked in markup"}' --scope "page-furniture"`**
```
gap/20261008-165711-47e269 — footer attribution line
```
Why + conclusion: gap filed for the unrecorded footer furniture; the built footer is marked `data-improv` in the markup.

**[46] `./run-authority gap-add --need "narrow-screen stacking for the documentation page layout (readable at 390px)" --context '{"source":"examples/authority-sites/wink","page":"index.html","attempted":"resolve UNDEFINED: closest guideline/hierarchy 5.5, token-set/type-scale 4.5 (no responsive record)","fallback":"single-column stacking built from the recorded card/section pieces; marked in markup"}' --scope "responsive-layout"`**
```
gap/20261008-165711-5f8d96 — narrow-screen stacking
```
Why + conclusion: gap filed for unrecorded responsive behaviour; grids and label swaps are marked `data-improv`.

**[47] `./run-authority gap-add --need "exact hex values for the Parsnip, Ochre and Kale colour roles (recorded as names only in token-set/colour)" --context '{"source":"examples/authority-sites/wink","page":"index.html","attempted":"resolve RESOLVED token-set/colour; record names roles without values; components cite Parsnip fills/tints with no hex","fallback":"warm ink tint rgba(35,30,21,.05) used for Parsnip surfaces (nearest recorded construction); marked in markup"}' --scope "colour-tokens"`**
```
gap/20261008-165711-89f9be — Parsnip/Ochre/Kale hex values
```
Why + conclusion: the one documented value gap in the pack (roles recorded without hexes); the ledger's Parsnip fills/tints are built from the recorded warm ink tint mechanism at low alpha, marked `data-improv`.

**[48] `./run-authority inspect fallback/platform-controls`**
```
id fallback/platform-controls · "Platform defaults for uncovered controls"
statement: If the system defines no control for a need, use the platform's native element with the wink
  field styling (radius 8, warm ink text); keep native semantics.
scope: checkbox radio date time file toggle switch picker combobox slider stepper upload
constraints: field styling (radius 8, 1px #DEDDDC border) · warm ink text · mark the improvisation…
```
Why + conclusion: the specification section quotes both fallbacks; this is the second one — captured and quoted verbatim.

---

## Adoptions · improvisations · gaps (summary)

**Adopted (all 17 artifacts inspected first; the ones instantiated on the page):**
token-set/colour · token-set/type-scale · guideline/typography · guideline/hierarchy ·
guideline/shape-language · guideline/voice · component/navbar · component/action-pill ·
component/card · component/ledger. Every CSS value traces to these records; adoption ids sit in
the comments next to each block in `index.html`.

**Reasoned non-use (inspected, not instantiated):** component/badge, component/field-select and the
five patterns (dialog, empty state, destructive confirm, progress, inline notice) — a static
documentation page contains none of those moments.

**Improvisations (each marked in the markup with `data-improv` + an HTML comment):**
1. footer attribution line (gap 47e269)
2. narrow-screen stacking / compact brand / short CTA label / scaled card padding (gap 5f8d96)
3. Parsnip tint as warm ink `rgba(35,30,21,.05)` where a tint is required (gap 89f9be)
4. page shell measure (single-column document width) — covered by the responsive gap note.

**Gaps filed:** gap/20261008-165711-47e269 · gap/20261008-165711-5f8d96 · gap/20261008-165711-89f9be.

**Prohibitions respected in the build:** no square buttons (all interactive = pill), no off-palette
colours (yellow/ink/white + recorded hairline; no pure black, no cold greys).

**Verification:** rendered headless (Chromium) at 1280px and 390px — `scrollWidth == innerWidth`
at both (no horizontal scroll); all three fonts load; 17 cards + ledger + footer present; computed
styles match the recorded values (masthead `rgb(255,224,27)`, card shadow `rgba(35,30,21,0.2) 0 8px
32px`, CTA ring `rgb(35,30,21) 0 0 0 1px`, radius 999px / 16px).
