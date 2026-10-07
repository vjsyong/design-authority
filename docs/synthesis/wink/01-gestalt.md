# wink · Gestalt model (Phase 4)

Derived from `00-evidence-inventory.md` (9 raw extracts + live-DOM probe).
Draft for **Gate 1** review. Epistemic tags in the inventory; this page
interprets. Nothing here reproduces brand assets or marks — character only.

## The read

Mailchimp's post-2018 identity is **engineered cheer**: a saturated
marigold-yellow field, warm near-black ink, and a soft-serve serif that
*winks in italics* while a plain-speaking grotesque does most of the talking.
It is warm without being soft, playful without being childish: big friendly
colour bands, chunky pill calls-to-action with springy motion, credibility
delivered as numbers, and copy that treats you like a smart friend.

## Visual principles

1. **Yellow leads.** Cavendish yellow `#FFE01B` is the brand field and the
   primary-action colour; it is not decorative confetti.
2. **Ink, not black.** Peppercorn `#241C15` (live `#231E15`, one-step conflict
   carried) is the text colour and the tint basis for shadows; pure black is
   absent from the system.
3. **Serif speaks, sans works.** Means (display, ~5% of elements, italics as
   the wink) + Graphik (UI/body, ~95%).
4. **Pill with a spring.** 26px-radius pill CTA, labels 13px/500, transform +
   shadow transition on a spring curve (`cubic-bezier(0.5, 2.5, 0.7, 0.7)`,
   0.3s) — the interactive signature.
5. **Warm neutrals, never clinical.** Parsnip `#F6F6F4`, white, border
   `#DEDDDC`, ochre band `#E7B75F` as page terminator.
6. **Big soft geometry.** Cards 16/24px radius with *warm-tinted* shadows
   (`rgba(35,30,21,.2) 0 8px 32px`), no card borders; structural chrome may
   be square (0px dominates the histogram) — shape encodes element class.
7. **Airy by default.** 8px base scale (8/16/24/32/48), 48px card interiors,
   full-bleed section stack, generous space around the mark.
8. **The wink is mandatory.** Character is systemic: an illustration system
   (named "Wink") that is themable and *deliberately restrained* so it never
   overpowers functional interface moments.
9. **Proof by number.** Credibility as display copy: 11M businesses, 27× ROI,
   33,000+ reviews, 300+ apps.
10. **Second person, question-first, plain English.** Warm, direct, calm
    authority over hype; dry wit that never excludes the reader.

## Colour character

| token | value | role | status |
|---|---|---|---|
| Cavendish Yellow | `#FFE01B` | hero field, primary action | OBSERVED |
| Peppercorn | `#241C15` (live `#231E15`) | all text/ink, shadow tint | OBSERVED (conflict noted) |
| Parsnip | `#F6F6F4` | warm subtle background | OBSERVED (non-canonical source) |
| White | `#FFFFFF` | primary surface | OBSERVED |
| Border | `#DEDDDC` | dividers/inputs | OBSERVED (non-canonical source) |
| Ochre band | `#E7B75F` | live footer terminator | OBSERVED (live) |
| Kale | `#007C89` | links (supporting, indicative) | OBSERVED (non-canonical; not seen live) |
| Error | `#BF4055` | error copy | OBSERVED (non-canonical) |

Character: one saturated hero, a warm ink, warm neutrals — the palette reads
*sunlight on paper*, not neon on glass.

## Typographic character

- Display: serif, regular weight, tight tracking (live 64px/76.8px, −1.2px),
  with an italic emphasis fragment inside otherwise regular headlines.
- Section heads run tight (live 35.2px, line-height 1.0).
- Body/UI: grotesque 16px/1.35; buttons 13px/500; written for scanability.
- Commercial faces (Means/Graphik) cannot be vendored; the tile will set
  stand-ins (Fraunces ≈ Means' warm soft-serif heritage; Inter ≈ Graphik's
  neutral grotesque) and say so on its face.

## Shape language

Pills for action; 16/24px soft cards; 8px documented default radius; square
structural chrome allowed; rounded ≠ everywhere — the system mixes soft
vessels with plain sheet structure. Shadows are soft, warm and large; borders
are rare.

## Density

Two registers: low-density marketing (stacked full-bleed sections, big type,
generous padding) and a defined product ramp (8px base, 14→48px type scale
from indicative sources). Tile shows the marketing register.

## Surface treatment

White/warm-neutral surfaces; warm-tinted elevation on borderless cards;
colour-band sections (yellow hero, ochre footer); sticky transparent header
that sits over the hero.

## Imagery treatment

Illustration is a first-class, themable system component with documented
restraint (product moments, loading, errors) and a "sophisticated ↔ surreal"
balance; photography carries warmth. (Not reproduced — no marks/assets.)

## Layout rhythm

Section-stacked, full-bleed: small audience label → serif headline with
italic fragment → a one-to-two-sentence paragraph; alternating proof bands;
CTA proximity notes.

## Motion character

Fast hover feedback (0.15s) under a slower movement layer (0.3s) on special
elements; the spring bezier is the signature. Hover *end states*, scroll
motion and hero media behaviour are carried **UNDEFINED**.

## Visual hierarchy

One h1 vs many h2s; display serif used sparingly for contrast; the sans runs
interfaces; numbers get display treatment.

## What wink would avoid (from the evidence)

Clinical grey palettes; pure black type or black-tinted shadows; sharp-corner
systems; density-first utilitarianism; formal/institutional tone; decoration
that overpowers function; hype-yelling copy.

## Carried UNDEFINEDs (deliberate)

Hover end-states · scroll/entrance motion · breakpoints & mobile behaviour ·
dark mode · focus rings & disabled states · product-UI spacing tokens ·
hexes for the described supporting palette (muted greens/peach/blue/red).
