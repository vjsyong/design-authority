# dominion (Canada FIP) · Evidence inventory (Phase 3)

Date: 2026-10-07 (UTC). Workstream: evidence capture for the Government of Canada Federal Identity Program (FIP) as codified in the *Design Standard for the Federal Identity Program* (effective November 19, 2021; replaces FIP Manual volumes 1.1 October 1990, 5.1 March 1989, 5.2 July 1990). Source-positive capture only — no design advice, no comparison to other sources. Tags: [OBSERVED] verbatim from source; [INFERRED] reading across sources; [UNDEFINED] source is silent.

## Fetch log

| URL | ok/failed | used for |
|---|---|---|
| https://www.canada.ca/en/treasury-board-secretariat/services/government-communications/design-standard.html | ok | overview, effective date, product application list |
| https://www.canada.ca/en/treasury-board-secretariat/services/government-communications/design-standard/colour-design-standard-fip.html | ok | official colours, colour codes, pairing rules, signage palette |
| https://www.canada.ca/en/treasury-board-secretariat/services/government-communications/design-standard/typography-design-standard-fip.html | ok | typeface, weights and uses |
| https://www.canada.ca/en/treasury-board-secretariat/services/government-communications/design-standard/official-symbols-design-standard-fip.html | ok | wordmark, signatures, structure, legal protection |
| https://www.canada.ca/en/treasury-board-secretariat/services/government-communications/design-standard/size-position-design-standard-fip.html | ok | sizing ratios, positioning, clear space, dos/don'ts |
| https://www.canada.ca/en/treasury-board-secretariat/services/government-communications/design-standard/treatment-official-languages-design-standard-fip.html | ok | bilingual order/format rules |
| https://www.canada.ca/en/treasury-board-secretariat/services/government-communications/design-standard/government-canada-websites-design-standard-fip.html | ok | website placement rules |
| https://www.canada.ca/en/treasury-board-secretariat/services/government-communications/design-standard/titles-signatures-design-standard-fip.html | ok | titles criteria, signature structure, musical signature |
| https://www.marasigan.ca/behind-the-design/2013/12/21/royal-bank-of-canada | ok | discovery only (RBC article; supplied the FIP article link) |
| https://www.marasigan.ca/behind-the-design/2013/9/30/canadian-federal-identity-program | ok | program history (reproduces TBS history text) |
| https://design.canada.ca/style-guide/ | ok | plain-language / content style rules (focus extract) |
| hound smart_search ×2 (history discovery) | n/a | located marasigan.ca FIP article |

## 1 Colour usage

- [OBSERVED] Standard palette for the Canada wordmark, corporate signatures and ministerial signatures: **FIP red, black, white, pewter grey** (colour page, "Colour palette and colour values", Table 1).
- [OBSERVED] **FIP red** — Pantone 032; CMYK 0, 100, 100, 0; RGB 235, 45, 55; vinyl 3M 7725-13.
- [OBSERVED] **Black** — Process black; CMYK 0, 0, 0, 100; RGB 0, 0, 0; vinyl 3M 7725-12.
- [OBSERVED] **White** — Process white; CMYK 0, 0, 0, 0; RGB 255, 255, 255; vinyl 3M 7725-10.
- [OBSERVED] **Pewter grey** — Pantone 429; CMYK 0, 0, 0, 40; RGB 150, 150, 150; vinyl "Not applicable".
- [OBSERVED] Standard-colour application: Canada wordmark = FIP red flag symbol + black type; flag signatures = FIP red flag symbol + black type; arms signatures = black arms of Canada + black type; ministerial signatures = **pewter grey** arms of Canada + black type (colour page, "Standard colours").
- [OBSERVED] Non-standard colours allowed "when a higher level of contrast with the background is needed or when a single colour is used in a product": reversed version (white letters, FIP red flag symbol, shown on black background); all-black or all-white versions "in cases where mandatory colours are not specified"; one-colour reproduction if that colour is the only colour used in the product.
- [OBSERVED] Colour pairing rule: when wordmark and signature appear together, "the type colour must be the same" and "the colour of the flag symbol in the flag signature must be the same as the flag symbol in the wordmark" (figures show correct/incorrect applications).
- [OBSERVED] Signage palette (separate): light grey, dark grey, yellow, blue, green, safety red.
- [OBSERVED] Signage values — light grey Pantone 428 / CMYK 0,0,0,25 / RGB 200,200,200 / 3M VE 3800; dark grey Pantone 432 / 0,0,0,85 / RGB 75,75,75 / 3M VE-3801; yellow Pantone 109 / 0,10,100,0 / RGB 250,215,20 / 3M 7725-15; blue Pantone 301 / 100,30,0,20 / RGB 0,90,155 / 3M 7725-47; green Pantone 348 / 100,0,85,25 / RGB 0,135,80 / 3M 7725-186; safety red Pantone 185 / 0,90,75,0 / RGB 230,15,45 / 3M 7725-13.
- [OBSERVED] "Safety red" shares vinyl spec 3M 7725-13 with FIP red — two distinct red codes (Pantone 032 vs 185) map to the same vinyl series per the tables.
- [INFERRED] Colour functions as a **flag-only accent**: red appears as the flag symbol; all text, arms and structure are black, white or grey; no other accent colours are defined for marks.
- [UNDEFINED] No hex codes published anywhere in the fetched pages (RGB/CMYK/Pantone/vinyl only); no UI/state colours (link, hover, error) in the FIP standard — websites page defers to the Canada.ca Specifications.

## 2 Typography

- [OBSERVED] "Helvetica is the official typeface for the Federal Identity Program. This includes typeface designs with minor variations under the names **Helvetica, Helvetica Neue and Helvetica Now**" (typography page).
- [OBSERVED] Weight → use mapping: **Light: stationery products; Regular: most communications and advertising products; Medium: signage and vehicle markings**.
- [OBSERVED] "Helvetica bold may be applied to messages that appear on signage and vehicles."
- [OBSERVED] Signature typography: flag, arms and ministerial signatures "set in Helvetica light, regular or medium weight" (titles page).
- [OBSERVED] Signatures with service titles: applied title and service title "appear in the same typeface and size", "are separated by a 0.5 to 1-line space", and "may use contrasting weights of Helvetica, for example, Helvetica light with Helvetica medium".
- [OBSERVED] The wordmark lettering is NOT Helvetica: "Canada" is "a graphically modified version of the **Baskerville** typeface" (official symbols page).
- [OBSERVED] Website application: signature and wordmark must appear in "**Helvetica medium weight**" (websites page).
- [OBSERVED] Figure caption: "Helvetica Now typeface in optical size text in light, regular, medium and bold weights" — four weights referenced across the standard (light/regular/medium for marks; bold for signage/vehicle messages).
- [UNDEFINED] No point sizes, px values, line-heights, tracking or optical-size metrics stated.
- [UNDEFINED] No fallback/web-font stack given in the FIP standard (published as PDF-spec and design-canada guidance elsewhere).

## 3 Scale & hierarchy

- [OBSERVED] All sizing is **relative to the Canada wordmark**, not absolute: "The height of the flag symbol in the signature is equal to the distance between the bottom of the wordmark and the bottom of the flag symbol in wordmark" (size & position page, flag signatures; applies regardless of positioning).
- [OBSERVED] Arms signatures: "the height of a 2-line title in the signature is equal to the distance between the bottom of the wordmark and the bottom of the flag symbol in the wordmark. The same applies to arms signatures of 3 or more lines."
- [OBSERVED] Ministerial signatures: "the width of the arms of Canada in the signature is half the width of the Canada wordmark."
- [OBSERVED] Signature line counts: flag signatures mostly 2 lines, 3-line "generally used for long titles"; arms signatures mostly 2 or 3 lines, 4-line "generally used for long titles".
- [OBSERVED] Applied-title structure limits: 2 to 4 words excluding articles; abbreviation max 6 letters (no acronyms/abbreviations/special characters in the title itself).
- [OBSERVED] Ministerial signature composition: arms of Canada centred between the English and French title of the minister.
- [INFERRED] The wordmark is the measurement master of the system: every signature and clear space is derived from either the wordmark's total height or its "C" height, so the identity scales as one lockup ratio.
- [UNDEFINED] No minimum or maximum reproduction size (mm/in/px) anywhere in the fetched pages.

## 4 Spacing & density

- [OBSERVED] Clear space around the Canada wordmark (x) = "the height of its letter 'C'", surrounding the wordmark on all 4 sides.
- [OBSERVED] Clear space around a flag signature = height of the flag symbol in the signature, on all 4 sides.
- [OBSERVED] Clear space around an arms signature or ministerial signature = half the width of the arms of Canada, on all 4 sides.
- [OBSERVED] Pairing space: between the wordmark and signature, the minimum space is equal, on all sides, to either the height of the flag symbol in the signature or half the width of the arms of Canada.
- [OBSERVED] "More clear space is encouraged if the design of the product permits"; dos include "display them in generous, open space".
- [OBSERVED] Service title: separated from the applied title by a 0.5 to 1-line space.
- [OBSERVED] Don'ts: no skew/stretch/compress; no alteration; not on a visually conflicting background; not as part of a headline, phrase or sentence; never angled.
- [INFERRED] The spacing unit is mark-relative and self-scaling (letter-C height / flag height / half arms width) — spacing breathes with the mark, no absolute margins specified.
- [UNDEFINED] No page margins, gutters, grid or density values.

## 5 Shape language & corner treatment

- [OBSERVED] Two official symbol shapes only: the Canada wordmark (word + flag symbol) and a corporate signature (flag symbol or arms of Canada + bilingual applied title).
- [OBSERVED] Arms signatures come in two layouts: asymmetrical (arms left, bilingual title right; "used in all products unless otherwise specified") and symmetrical (arms centre, one language on each side; e.g., federal tribunal decision letters).
- [OBSERVED] Marks must sit "on a horizontal baseline, never on an angle or their side"; no skew/stretch/compress; nothing may be altered.
- [OBSERVED] Ministerial signature geometry: arms centred, pewter grey.
- [UNDEFINED] No corner radii, stroke weights, or container shapes specified anywhere; all figures show rectangular/rectilinear marks and fields. No shape language beyond heraldic symbols.

## 6 Borders, surfaces & elevation

- [OBSERVED] Surfaces are defined by mandatory background pairings: standard = black type + FIP red flag on white; animated wordmark = black type on white **or** white type with FIP red flag on black (the latter "recommended for large scale formats").
- [OBSERVED] Reversed versions: white letters + FIP red flag (shown on black background).
- [OBSERVED] Constraint: don't place marks "on a visually conflicting background" — the only surface rule besides mandatory colourways.
- [OBSERVED] All-black / all-white versions permitted "in cases where mandatory colours are not specified"; one-colour reproductions permitted when that colour is the only colour in the product.
- [UNDEFINED] No borders, card surfaces, elevation, shadow or divider styles — not addressed by the FIP standard (web treatment deferred to Canada.ca Specifications).

## 7 Iconography & imagery

- [OBSERVED] Only 2 official symbols exist; anything else is controlled: specialized symbols require policy criteria met + approval by heads of communications.
- [OBSERVED] Additional corporate identifiers require Treasury Board approval (sought through a Treasury Board submission).
- [OBSERVED] Non-GoC logos may be displayed only in formal partnering or sponsorship arrangements, per the agreement's terms and conditions.
- [OBSERVED] Social media provider icons "can be used when linking to an official social media account or when promoting it"; social-media product list includes avatars, text identifiers, account icons.
- [OBSERVED] Animated wordmark must always "appear in its static form as the final image" and only in one of the 2 approved colourways.
- [OBSERVED] Legal protection: Trademarks Act s.9(1) prohibited marks; Copyright Act; Article 6ter of the Paris Convention.
- [INFERRED] The system's imagery posture is protectionist: one flag symbol, one wordmark, everything else gated behind approval chains.
- [UNDEFINED] No photography, illustration or pictogram style rules in the fetched FIP pages (signage technical specs not fetched).

## 8 Layout rhythm & navigation

- [OBSERVED] 4 approved positioning options for wordmark + corporate signature in most products: (1) same baseline, signature left; (2) wordmark bottom-right, signature top-left; (3) wordmark directly below signature aligned with the signature's left-most text; (4) wordmark directly below signature, left-aligned to the identifying symbol's left edge.
- [OBSERVED] Websites (external-facing): "the Government of Canada signature appears in the top left corner of the header" and "the Canada wordmark appears in the bottom right corner of the footer" — a fixed bookend layout.
- [OBSERVED] Certain products (stationery, videos) have their own positioning requirements, per their product pages.
- [OBSERVED] Ministerial signatures "typically appear above the Canada wordmark", arms centre-aligned with the wordmark.
- [OBSERVED] Side-by-side bilingual format required for: business cards (or double-sided), primary identification signs, directory boards, common-use and operational signs, project signs, commemorative plaques, vehicle/aircraft/watercraft markings, personnel identification.
- [OBSERVED] Bilingual ordering logic (English left by default; French left when content is French-only, the office/asset is in Quebec, etc.; National Capital Region may alternate order on opposing vehicle doors and uniform shoulder flashes).
- [INFERRED] Layout rhythm is a fixed-corner discipline: top-left identifies, bottom-right anchors; interiors are out of the FIP standard's scope.

## 9 Interaction cues & motion

- [OBSERVED] Animated Canada wordmark "may be used in certain government communications products, for example, videos"; it must end as the static mark in one of the 2 approved colourways.
- [OBSERVED] Musical signature = "the first 4 notes of 'O Canada' and lasts 1.5 seconds"; in video it "plays while the wordmark is on the screen"; standard version available, but departments "may create alternative instrumental variations".
- [UNDEFINED] No easing, duration, hover/focus/pressed states, or transition guidance in the FIP standard (web interactivity deferred to Canada.ca Specifications, not fetched).
- [INFERRED] Motion is treated as a gated, end-state-fixed device: animation is permitted only if the identity resolves to the static approved mark.

## 10 Feedback & status representation

- [OBSERVED] "Safety red" (Pantone 185) is the only semantically named colour; used in the signage palette only.
- [OBSERVED] Status-bearing products listed: text messages "sent by or on behalf of the Government of Canada, emergency alerts"; signage categories include "operational signs, project signs, tactile signs"; awards/certificates.
- [UNDEFINED] No success/warning/error colour semantics, banners, toasts or validation feedback patterns anywhere in the FIP standard.

## 11 Content style, tone & voice

- [OBSERVED] FIP's founding guidelines "are based on the use of plain, non-bureaucratic language, functional graphic design and a systems approach in identifying government services" (TBS history text via marasigan.ca).
- [OBSERVED] Canada.ca Content Style Guide is mandatory: "All departments ... subject to the Directive on the Management of Communications must use the Canada.ca Style Guide ... for all public-facing websites and digital services, regardless of the technology, domain name or publishing platform used" (referenced in Appendix D of the Directive).
- [OBSERVED] Writing principles: "Help people complete tasks"; people scan rather than read word-by-word; content must be intuitive, comprehensive, targeted ("most important information first"), consistent ("standardized approach ... confidence and trust").
- [OBSERVED] "Make gender-inclusive writing your standard practice"; write for accessibility (incl. WCAG 2.0 reference) and readability/reading level.
- [OBSERVED] Mandated phrasing: where unilingual versions are produced, content "must state that the same material is available in the other official language" — e.g., *version française disponible*.
- [OBSERVED] Applied-title naming rules read as tone rules: include "Canada" (jurisdiction) not "Canadian" (nationality); as short as possible; keywords only; no acronyms, abbreviations or special characters; EN/FR versions equivalent in style and grammar.
- [OBSERVED] Ministerial-title formula: "Office of" / "Cabinet du" prefix added for staff-produced items; parliamentary secretaries add their designation.
- [OBSERVED] The wordmark and signature titles "must not be translated into another language. They must appear in English and French only"; third languages go to the right of or below EN/FR, visually equal.
- [OBSERVED] Legal titles are "used only where required by law, such as in legislation, orders-in-council and contracts".

## 12 Responsive behaviour notes

- [OBSERVED] Mark-relative sizing (wordmark-referenced heights and clear spaces) means the lockup carries its own scale ratio wherever it is placed.
- [OBSERVED] Website rules apply to "external-facing and internal-facing sites", "web applications and ... sites that are password protected".
- [OBSERVED] "These requirements are also in the Canada.ca Specifications, which sets out the mandatory design requirements for the government's web presence" (websites page).
- [OBSERVED] Explicit compact-width fallback: "Where horizontal space is limited, an over-and-under format is permitted" for common-use/operational signs and personnel identification; the top language is the one that would appear left in side-by-side.
- [OBSERVED] Third-language stacking rule (right of > below) is the only other reflow rule.
- [INFERRED] Responsiveness is content-driven (language/format alternates when space is constrained), not breakpoint-driven; no breakpoints, fluid type or touch-target sizes are specified.
- [UNDEFINED] No viewport/breakpoint/interaction-size values anywhere in fetched pages.

## 13 Repeated motifs & devices

- [OBSERVED] The FIP red flag symbol is the recurring accent across wordmark, flag signatures and (per websites page) the web header/footer application.
- [OBSERVED] Default lockup: black type + FIP red flag on white; alternate: white type + FIP red flag on black; both defined for wordmark and signatures.
- [OBSERVED] The horizontal baseline pairing of two distinct elements (wordmark + signature) is the canonical device; marks are never combined into one composite graphic.
- [OBSERVED] Bookend framing on websites (signature TL header / wordmark BR footer) repeats the 4-option positioning discipline.
- [OBSERVED] Bilingual side-by-side EN|FR pairing appears in every signature form (corporate, ministerial) as a structural motif.
- [OBSERVED] Digital master files: marks are never redrawn — "can only be reproduced using the digital master file"; masters are created and maintained by the TBS Communications and Federal Identity Policy Centre.
- [OBSERVED] The word "Canada" recurs as verbal motif: mandatory in applied titles; the wordmark is literally the word "Canada" + flag; GoC signature reads "Government of Canada" bilingually.
- [INFERRED] System identity = one wordmark, two symbol types (flag/arms), restricted palette, relative sizing — a closed grammar where every new application is a re-arrangement of fixed parts.

## Gaps & UNDEFINED candidates

- [UNDEFINED] No hex colour codes published (RGB/CMYK/Pantone/vinyl only); consuming systems must convert FIP red 235,45,55 themselves.
- [UNDEFINED] No absolute minimum/print sizes, no px values, no grids/margins/gutters.
- [UNDEFINED] No UI-specific rules in the FIP standard: no states (hover/focus/pressed), no component shapes, borders, elevation or shadows; web page explicitly defers to the Canada.ca Specifications (not fetched).
- [UNDEFINED] No motion timing beyond the 1.5 s musical signature; no transition/easing guidance.
- [UNDEFINED] No feedback/status semantics (error/success colours) anywhere.
- [UNDEFINED] Tone-of-voice detail lives outside FIP: the Content Style Guide (fetched, excerpt only) carries the writing rules; sentence-length standards etc. not captured in the focused extract.
- [UNDEFINED] Figures (clear-space diagrams, correct/incorrect examples) are images; geometry captured only as text rules, not measured values.
- Note: signage/stationery/vehicle technical specifications pages were out of budget and not fetched.

## Raw extracts

- raw/01-design-standard-overview.md
- raw/02-colour.md
- raw/03-typography.md
- raw/04-official-symbols.md
- raw/05-size-position.md
- raw/06-official-languages.md
- raw/07-websites.md
- raw/08-titles-signatures.md
- raw/09-marasigan-fip-history.md
- raw/10-style-guide-plain-language.md
