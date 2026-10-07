# wink · Semantic review (Gate 2)

Generated 2026-10-07 from `decisions.json` — **26 decisions**: 14 settled · 12 needing judgment · 0 open.

Legend — status: OBSERVED / INFERRED / AUTHORED / UNDEFINED. Review outcome (fill at Gate 2): ACCEPT / MODIFY / REJECT / LEAVE UNDEFINED.


## Settled (high-confidence — shown for context, no action needed)

### W-01 · actions · OBSERVED · confidence: high
**Decision:** Primary action = pill, filled Cavendish Yellow #FFE01B, label in Peppercorn ink. On yellow or warm fields, primary switches to the dark variant (ink fill, white label). Secondary = outline pill (2px ink inset).

**Evidence:** live DOM: CTA fill rgb(255,224,27) + dark inverse variant observed; pill radius 26px on ~44px height

**Reasoning:** The two variants were both observed live; contrast switching follows from the yellow-on-yellow failure mode.

**Alternatives:** single flat hierarchy (rejected: two variants observed)

### W-02 · actions · OBSERVED · confidence: high
**Decision:** All buttons are pills (radius = half height, ~26px); labels 13px/500 sans; no square buttons anywhere.

**Evidence:** live computed styles: border-radius 26px; label 13px/500

**Reasoning:** Directly measured.

**Alternatives:** 8px default radius (documented but not the CTA reality)

### W-04 · typography · OBSERVED · confidence: high
**Decision:** Two registers: soft-serif display for hero/section headlines (with an italic emphasis fragment allowed inside a headline); grotesque sans for all body, UI, labels and metadata. Serif is the exception, never the working voice.

**Evidence:** font histogram ~5% serif vs ~95% sans; italic emphasis pattern in live headlines

**Reasoning:** Measured distribution + recurring headline pattern.

**Alternatives:** serif body text (rejected: not observed)

### W-05 · typography · OBSERVED · confidence: high
**Decision:** Screen scale: display 48–64px w400 tight tracking (−1.2px at 64); section 35px/1.0; body 16/1.35; small 14; labels/buttons 13/500.

**Evidence:** live computed styles; indicative scale 14→48

**Reasoning:** Directly measured; marketing vs product ramps reconciled.

**Alternatives:** flat scale (rejected)

### W-06 · colour · OBSERVED · confidence: high (yellow/ink/ochre) · medium (kale/error roles)
**Decision:** Roles: yellow = brand field + primary action only; peppercorn = text, ink, shadow tint; white + Parsnip = surfaces; Ochre = section band terminator; Kale = links inside content; #BF4055 = error text/fills.

**Evidence:** brand-assets names; live surfaces; indicative tokens for kale/error

**Reasoning:** Core roles observed live; link/error roles from indicative source, flagged for confirmation.

**Alternatives:** peppercorn links (also live in some spots — conflict noted in evidence)

### W-07 · surfaces · OBSERVED · confidence: high
**Decision:** Content cards: white, borderless, radius 16 (24 for large), elevation via warm ink-tinted shadow rgba(35,30,21,.2) 0 8px 32px; interior padding 48. Tinted variant: Parsnip, no shadow. 1px borders (#DEDDDC) only on inputs/dividers, never as card devices.

**Evidence:** live computed styles (shadow string, radii, 48px padding, border token)

**Reasoning:** Directly measured across elements.

**Alternatives:** bordered cards (contradicts observed borderless + shadow pattern)

### W-08 · shape · INFERRED · confidence: high
**Decision:** Shape encodes class: interactive = pill; content vessel = 16/24 soft-radius; structural chrome (bands, dividers, page blocks) = square.

**Evidence:** radius histogram (0px dominant + pills + 16/24 cards)

**Reasoning:** The mixed histogram reads as a deliberate class system, not noise.

**Alternatives:** global soft rounding (rejected: 0px dominant)

### W-09 · spacing · OBSERVED · confidence: high
**Decision:** 8px base scale (8/16/24/32/48); section padding 56–72; card interior 48; button padding 12/24.

**Evidence:** live paddings (40/68/60/48/12×24) + indicative 8px base

**Reasoning:** All observed values are multiples of 8 or half-steps.

**Alternatives:** 4px base (rejected: no evidence)

### W-10 · hierarchy · OBSERVED · confidence: high
**Decision:** One page title; sections = small uppercase label → display headline → 1–2 sentence paragraph. Numbers may take display treatment for proof moments.

**Evidence:** live section pattern; 1×h1 vs 25×h2 counts; number-led proof

**Reasoning:** Recurring observed pattern.

**Alternatives:** multi-h1 (rejected)

### W-11 · navigation · OBSERVED · confidence: high
**Decision:** Top bar: sticky, transparent over the opening band, ≤68px tall; text links in sans; primary CTA at the right end; no bottom border.

**Evidence:** live computed header (position sticky, 68px, transparent, no border)

**Reasoning:** Directly measured.

**Alternatives:** solid bar (rejected for hero pages; may be needed on content pages — flagged)

### W-21 · badges · OBSERVED · confidence: high
**Decision:** Emphasis badges: pill, yellow fill, 12/600 label (e.g. 'Most popular' on the selected plan/category).

**Evidence:** live 'Most Popular' badge

**Reasoning:** Direct observation.

**Alternatives:** none

### W-22 · voice · OBSERVED · confidence: high
**Decision:** Second person, question-first, plain English, non-blaming; dry wit allowed in microcopy; italic serif emphasis fragment allowed in headlines.

**Evidence:** multiple live samples + brand voice descriptions

**Reasoning:** Quoted register across sources.

**Alternatives:** neutral corporate (rejected)

### W-23 · imagery · OBSERVED · confidence: high
**Decision:** Illustration is a real system capability but treated as optional garnish: allowed in empty/loading moments, restrained, never over functional content. Not reproduced in the reference build (no asset library).

**Evidence:** illustration system named and described as restrained; no assets reproduced by policy

**Reasoning:** Matches the observed restraint rule; keeps the build free of cloned art.

**Alternatives:** placeholder illustrations (rejected: would fabricate the asset library)

### W-26 · prohibitions · INFERRED · confidence: high
**Decision:** Never: pure black text/shadows; clinical neutral greys as the palette; square primary buttons; 1px borders as card devices; decorative use of yellow; invented hues beyond the palette.

**Evidence:** absence of these across all observed material + stated warm-ink discipline

**Reasoning:** The prohibitions codify what the evidence never does.

**Alternatives:** none


## Needing judgment (authored or low-confidence)

### W-03 · events · AUTHORED · confidence: medium
**Decision:** Hover end-state for pills: lift (-3px translate, slight scale) + warm ink-tinted shadow, on the spring curve cubic-bezier(0.5,2.5,0.7,0.7) at 0.3s. Other interactive elements get fast feedback (~0.15s).

**Evidence:** transition declarations observed; end-state values not captured (probe failed)

**Reasoning:** Transition targets (transform, box-shadow) imply a lift+shadow response; magnitude authored to stay gentle.

**Alternatives:** scale-only; glow highlight (rejected: not in evidence)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### W-12 · forms · AUTHORED · confidence: medium
**Decision:** Inputs: white fill, 1px #DEDDDC border, radius 8, 16px text, label above in 14/500; focus = 3px yellow ring (outer, offset 2). Error = border+message in #BF4055.

**Evidence:** border token + 8px radius documented; focus treatment not evidenced

**Reasoning:** Extends the documented field language; yellow ring is the only on-brand focus signal.

**Alternatives:** 2px ink focus border; double-ring

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### W-13 · selection · AUTHORED · confidence: low
**Decision:** Native select styled as a field for small fixed sets (≤ ~12). Larger or filtered selection is out of scope by design; use the platform-controls fallback and mark it.

**Evidence:** no picker evidence captured; product shows list-based interactions at scale

**Reasoning:** Keeping the pledge honest: no invented searchable picker canon.

**Alternatives:** invent a combobox pattern (rejected: no evidence)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### W-14 · status · AUTHORED · confidence: medium
**Decision:** Status = word-first pill: neutral (Parsnip bg, ink text), attention (Ochre bg, ink text), positive (ink text, no colour — word carries it), problem (#BF4055 tint bg, dark red text). Colour supports the word; never replaces it.

**Evidence:** no status component observed; error colour indicative; ochre/parsnip surfaces observed

**Reasoning:** Derived from the warm neutral + single-accent discipline; avoids inventing new hues.

**Alternatives:** green/red dots (rejected: no green exists in the system)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### W-15 · feedback · AUTHORED · confidence: medium
**Decision:** Inline notices (rounded 12, tinted fill) rather than floating toasts; copy is plain, non-blaming, question-first.

**Evidence:** validation copy observed (non-blaming, plain); no toast pattern observed anywhere

**Reasoning:** Follows observed copy+tone; toasts use a component that does not exist in evidence.

**Alternatives:** toast stack (rejected: unevidenced)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### W-16 · destructive · AUTHORED · confidence: medium
**Decision:** High-consequence actions route through a rounded confirm dialog (16px) with a consequence sentence in the warm voice; confirm = ink-filled pill labelled with the concrete verb (never 'OK'); cancel = outline pill. Destructive is never the default focus.

**Evidence:** no destructive pattern captured; dialog styling inferred from card language

**Reasoning:** Uses only observed primitives (card, pill, voice).

**Alternatives:** inline two-step reveal; typed confirmation (both rejected as heavier than the brand's register)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### W-17 · overlays · AUTHORED · confidence: medium
**Decision:** Dialog: white 16px card, 48px padding, warm ink scrim (rgba(35,30,21,.35)); instant appearance (no motion defined; none invented).

**Evidence:** shadow/card language observed; motion undefined

**Reasoning:** Same vessel as content cards; motion gap carried, not filled.

**Alternatives:** fade/slide entrance (rejected: motion undefined in source)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### W-18 · progress · AUTHORED · confidence: medium
**Decision:** Progress = pill track (Parsnip) with yellow fill in flight, ink fill when complete, plus a text readout ('7 of 10 steps'). Job actions: start / restart as pills; pause-and-resume allowed (named flow in the product).

**Evidence:** multi-step editor with pause-and-resume named in product notes; no visual captured

**Reasoning:** Tracks observed primitives; readout keeps it honest without animation.

**Alternatives:** spinner-only (rejected: steps are the point)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### W-19 · empty · AUTHORED · confidence: medium
**Decision:** Empty state = tinted Parsnip panel with one warm sentence + one action pill ('Add your first item').

**Evidence:** no empty state captured; voice + tinted surface observed

**Reasoning:** Composes observed primitives; copy follows the observed warm-plain register.

**Alternatives:** illustration-led empty state (deferred: illustration system exists but is not reproduced)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### W-20 · repeated-content · INFERRED · confidence: medium
**Decision:** Ledger: white surface, 16px padded rows, hairline #DEDDDC dividers (no zebra striping), header row in Parsnip with 13/500 labels; row hover = Parsnip tint; status pill inline; text links in ink with underline.

**Evidence:** pricing comparison table observed; hairline border token; link treatment observed

**Reasoning:** Extends the observed table language to the register list.

**Alternatives:** zebra rows (rejected: borderless/warm pattern)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### W-24 · responsive · AUTHORED · confidence: low
**Decision:** Single-column collapse; hero display scales 64→40; sticky bar keeps height; no evidence of mobile-specific patterns — carried UNSPECIFIED beyond collapse.

**Evidence:** no responsive evidence captured (single viewport probe)

**Reasoning:** Minimal, honest collapse rather than invented responsive canon.

**Alternatives:** full responsive system (rejected: unevidenced)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### W-25 · focus · AUTHORED · confidence: low
**Decision:** Focus = 3px yellow ring (outer). On yellow surfaces, focus switches to the ink ring.

**Evidence:** focus treatment not evidenced anywhere

**Reasoning:** Yellow is the natural focus signal; the on-yellow switch follows the CTA contrast rule (W-01).

**Alternatives:** ink-only ring; blue default

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED


## Open (genuinely undefined — may remain so)

_None._
