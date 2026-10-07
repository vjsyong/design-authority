# Synthesis · 00 · Source selection (Phase 1)

Prototype: **Authority Synthesis** — can a machine-guided process compile messy
design evidence into distinct, useful candidate Design Authorities?

Fixed premises from the protocol: Triage, Indaba and the kernel are **frozen**
(Phase 0); no reference-implementation knowledge enters synthesis contexts
(quarantine per `docs/portability/08-contamination-audit.md` extends to this
phase); sources should be brand/design kits, not component libraries — we are
testing *synthesis*, not API translation.

Selection goals: maximum stylistic divergence across three archetypes, strong
public evidence, defensible usage posture, and useful stress tests. Working
codenames below; final authority names land at gestalt stage.

## Candidates considered

| archetype | primary | alternates | why not (alternates) |
|---|---|---|---|
| A expressive / playful | **Mailchimp** | Duolingo · Headspace | Duolingo: guidelines not officially public (blog-only) — weak citable evidence. Headspace: guidelines site won't render for us; orange warmth risks Indaba adjacency. |
| B editorial / premium | **The Economist** | FT · Aesop | FT: strong product, but brand guides not public (Financier story only). Aesop: no formal kit; observation-only, thin formalizable evidence. |
| C civic / institutional | **Canada FIP (Federal Identity Program)** | TfL · Wikimedia | TfL: site is bot-walled (403) — poor evidence access; very restrictive IP posture. Wikimedia: style guide is component-library-adjacent (translation risk). |

## Recommended sources

### A · Mailchimp — working name `wink`

- **Source material:** `mailchimp.com/about/brand-assets/` (official asset
  usage page); 2018 Collins identity documented across Fonts In Use
  (`fontsinuse.com/uses/39539`), Canny Creative brand atlas, and the live
  product site. Yellow-led identity (2018 Freddie-era), winking chimp mark,
  soft-serif display + grotesque pairing (exact values to be confirmed in the
  Phase 3 inventory), illustration system, warm non-corporate voice.
- **License / usage:** Trademarked brand; the asset page is a usage policy,
  not a republication license. Synthesis reproduces **no assets or marks** —
  it derives a grammar. Citations retained.
- **Why it diverges:** saturated yellow is absent from both incumbents (Indaba
  = aubergine/orange; Triage = monochrome + alert red); illustration-led,
  wink-culture, "warm non-corporate" posture has no incumbent analogue.
- **Expected difficulty:** medium. Identity is well documented; *motion and
  illustration* are the soft spots — likely carrying genuine `UNDEFINED`s.
- **Likely ambiguities:** how a playful brand constrains dense data
  screens; illustration usage rules vs imagery the authority can actually
  specify (placement/treatment rules, not drawing chimps).
- **Stress-test value:** can synthesis carry *personality* without collapsing
  into generic "friendly SaaS"?

### B · The Economist — working name `leader`

- **Source material:** The Economist Group 2017 brand style guide (publicly
  documented; red = Pantone 485C family); Wolff Olins "red thread" group
  architecture (2022, rectangles motif: Lens/Steps/Frame/Stage — PRINT
  Magazine); 2025 digital refresh with Nomad (red + Economist serif retained —
  Design Compass); typography articles by their own design director; the live
  publication as ongoing evidence.
- **License / usage:** Brand-protected; third-party guide copies carry rights
  disclaimers (noted). Grammar derivation only; no assets.
- **Why it diverges:** typography-led, restrained palette (red/black/white),
  print heritage, masonry/rectangle rhythm — an *editorial* logic neither
  incumbent has (Indaba is humanist-warm, Triage is utility-UI).
- **Expected difficulty:** medium-high. Rich evidence, but the governing
  documents are style guides → UI semantics must be *inferred*, which is
  exactly the synthesis test.
- **Likely ambiguities:** media-brand (Group) vs newsroom expression; 2017
  guide vs 2022+ refresh tension; motion (animated rectangles as brand
  device).
- **Stress-test value:** can synthesis translate *editorial authority* into
  interface grammar without becoming "another serif SaaS"?

### C · Canada FIP — working name `dominion`

- **Source material:** Canada.ca official Design Standard for the Federal
  Identity Program (effective 2021, replacing the 1990 manual volumes):
  official symbols, colour codes and pairing, typography ("Helvetica is the
  official typeface"), size/position, official languages (bilingual
  treatment), plus application pages incl. **Websites, mobile apps, signage,
  motion graphics**. The 1970s FIP program history is documented by design
  historians.
- **License / usage:** Crown copyright; official symbols are controlled
  (reproduction restricted to authorized government use). Synthesis derives a
  *new* system; no symbols or marks reproduced; citations retained.
- **Why it diverges:** austere, paper-form federal logic — white/black with a
  ceremonial red, Helvetica discipline, bilingual structure, bureaucratic
  utility. Note a watch-item: red appears in Triage too (alarm states) — the
  polarity probes will test whether the derived system keeps its different
  *role* for red (ceremonial/identity) vs Triage's (state).
- **Expected difficulty:** high, deliberately: the standard formalizes
  identity but only lightly touches screens → deep inference required. This is
  the strongest test of "evidence → semantics" (most `INFERRED`, clear view
  of where machines must stop).
- **Likely ambiguities:** how much screen behavior can be legitimately
  inferred from an identity standard; bilingual zones as a layout rule vs a
  content rule.
- **Stress-test value:** can synthesis stay austere without re-deriving
  Triage-style utility chrome?

## Divergence axes vs incumbents (summary)

| | wink (Mailchimp) | leader (Economist) | dominion (FIP) |
|---|---|---|---|
| palette | saturated yellow + ink | red / black / white | white / black / ceremonial red |
| type | soft-serif display + grotesque | editorial serif-led | Helvetica discipline |
| shape/motif | round mark, wink, illustration | rectangles / rules / masonry | flag geometry, official grids |
| density | warm, breathable, playful | dense but typographic | austere, structured |
| posture | irreverent warmth | editorial authority | bureaucratic calm |

## Process notes for this phase

- Source dirs: `docs/synthesis/{wink,leader,dominion}/` for evidence,
  gestalt, semantic review, reference review.
- The existing per-source gate order is preserved and extended: **evidence
  inventory → gestalt (Gate 1) → semantics (Gate 2) → compile → CI → build
  (Gate 3) → probes**.
- Same quarantine discipline as the portability phase (fresh fetches, no
  incumbent CSS in derivation contexts, no Triage/Indaba-content skills).
- Deliverables and stage outputs follow the protocol paths exactly
  (`docs/synthesis/*`).

**Awaiting reviewer confirmation of the trio** (or a swap) before Phase 3
begins.
