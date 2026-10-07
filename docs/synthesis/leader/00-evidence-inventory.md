# leader (The Economist) · Evidence inventory (Phase 3)

Date: 2026-10-07 · Authority Synthesis workstream, source 'leader' = The Economist (London) and its Group brand architecture. Pure evidence capture from fresh web fetches; no design advice, source-positive only. Tag legend: **[OBSERVED]** = stated/visible in a cited source; **[INFERRED]** = derived, used sparingly; **[UNDEFINED]** = not found in fetched sources. Live economist.com was hard-blocked (403 / Cloudflare); a 2025-06-01 Wayback snapshot substitutes where noted.

## Fetch log

| url | ok/failed | used for |
|---|---|---|
| https://www.printmag.com/branding-identity-design/the-economist-group-rebrand/ | ok | Wolff Olins Group rebrand; red thread; rectangle motif + semantics; palette |
| https://designcompass.org/en/2025/07/02/the-economist/ | ok | 2025 digital refresh w/ Nomad; glyphs; red + serif retained; motion |
| https://www.economist.com/ (live) | failed — 403 on HTTP + stealthy tiers; real-browser attempts hit Cloudflare "Just a moment" challenge (3 tries) | live 2026 site observation |
| https://marber.economist.com/8e1dcf0b8/p/96e5d5 (typography) | ok | Economist Serif/Sans/Headline; CSS var tokens; fallbacks; 1843 + Group fonts |
| https://marber.economist.com/ (home) | ok (thin, 366 chars) | design-system scope statement |
| https://tdc.org/winner/the-economist/ | ok | typeface design lineage (Plantin/Granjon; Bauer's Venus; Marber) |
| https://a2-type.co.uk/custom | ok | typeface suite scope; project credits; Tokyo TDC 2025 |
| https://www.creativereview.co.uk/the-economist-group-rebrand-wolff-olins/ | ok | rebrand framing; red thread; 50→4 brands |
| https://brandingstyleguides.com/guide/the-economist-group/ | partial — title/date only ("The Economist Group standards manual", posted 2022-03-22); guide body not machine-readable | style-guide existence |
| https://www.economistgroup.com/ | ok | current Group architecture (3 brands); mission/voice |
| https://web.archive.org/web/20250601021008/https://www.economist.com/ | ok (snapshot 2025-06-01) | homepage modules, headline/standfirst pattern, nav, voice |
| http://archive.org/wayback/available?url=www.economist.com | failed (429) | snapshot lookup attempt |
| search ×3: 'Economist Serif Economist Sans typeface'; 'Wolff Olins Economist'; 'marber.economist.com' | ok | source discovery (used to find Marber, TDC, A2-Type, Creative Review) |

## 1 Colour usage

- [OBSERVED] Core palette of the Group brand system = "this red along with black and white" — a "simple and clean" trio. (printmag.com, ¶4)
- [OBSERVED] A "'red thread' design theme" is the brand identifier tying the four Group brands together. (printmag.com, ¶4; creativereview.co.uk, opening)
- [OBSERVED] "The publication's simple but effective red and white graphic has become a regular feature of its branding and advertising" (red+white named as the recurring brand graphic). (creativereview.co.uk, ¶2)
- [OBSERVED] The 2025 digital refresh (Nomad) retained "the iconic red"; red remains the anchor colour. (designcompass.org)
- [UNDEFINED] Exact red value — no hex code or Pantone number stated in any fetched source ("this red" / "iconic red" only). Key gap.

## 2 Typography

- [OBSERVED] The Economist's design system ("Marber") states: "The Economist has two typefaces that form the visual core of everything published across digital, print, social, video and marketing: Economist Serif and Economist Sans. Both typefaces have been custom designed." (marber.economist.com typography page)
- [OBSERVED] **Economist Serif** — "Primarily for body text, descriptions and headlines." 14 styles: Light → Black, each with italic. Token: CSS var `--mb-typeface-serif`. Fallback stack: `'EconomistSerif', ui-serif, Georgia, Times, 'Times New Roman', serif`. (marber.economist.com)
- [OBSERVED] **Economist Sans** — "Primarily for navigation elements, such as: section openers, fly titles, datelines, metadata, captions." Same full weight range Light → Black + italics. Token: `--mb-typeface-sans`. Fallback stack: `'EconomistSans', system-ui, 'Segoe UI', Helvetica, Arial, sans-serif`. (marber.economist.com)
- [OBSERVED] **Economist Sans Headline** — "For use in display headlines"; 5 styles (Regular, Medium, Bold, ExtraBold, Black). Token: `--mb-typeface-sans-display`. Fallback stack: `'EconomistSansHeadline', Impact, Haettenschweiler, 'Franklin Gothic Bold', 'Helvetica Inserat', 'Arial Black', sans-serif`. (marber.economist.com)
- [OBSERVED] TDC: the headline sans is "for use on covers only" and originates "in a variety of industrial condensed sans sources all found in our print archive". (tdc.org)
- [OBSERVED] **1843 magazine** (section/vertical) uses its own display face: **Sunday Clarendon** — token `--mb-typeface-slab-serif-display`; fallback `'SundayClarendon', 'ITC Lubalin Graph', Rockwell, serif`. (marber.economist.com)
- [OBSERVED] **The Economist Group** brands use **GT Zirkon**: "For use in titles and headlines throughout The Economist Group, Economist Education, Economist Intelligence, and Economist Impact." Fallback `'GTZirkon', system-ui, 'Segoe UI', Helvetica, Arial, sans-serif`. (marber.economist.com)
- [OBSERVED] Design lineage: serif "references our use of Plantin, but goes back to Robert Granjon's original 16th-century drawings for inspiration over a Plantin revival"; sans "looks to Bauer's Venus, a typeface popular in early 20th-century advertising and a favorite of Romek Marber, The Economist's cover designer in the 1960s". (tdc.org; repeated at a2-type.co.uk)
- [OBSERVED] Purpose statement: typefaces exist "not only being the voice of the journalism, but supporting the presentation of a lot of different data. Be that facts and figures, charts and graphs, or scientific and mathematical equations." (tdc.org)
- [OBSERVED] Suite described as "a suite of interconnected and complementary typefaces (sans, serif, headline)". (a2-type.co.uk)
- [OBSERVED] Project credits: directed by Stephen Petch (Art Director), Adam Morris (Head of Product Design and UX), Mark Mitchell (Principal Product Designer). Selected 'Prize Nominee Work', Tokyo Type Directors Club Awards 2025. (a2-type.co.uk)
- [OBSERVED] 2025 refresh: "The iconic red and Economist serif typeface were retained." (designcompass.org)
- [OBSERVED — search snippet, page not fetched] Pre-2018 faces were "Officina, Johnston, and Eco Type". (587.claudiastrong.com snippet via hound search)
- [UNDEFINED] Numeric size scale (px/rem) — Marber states "a selection of font sizes" but values were not in the extracted text.

## 3 Scale & hierarchy

- [OBSERVED] Marber: "Our typographic system provides a selection of font sizes and reusable type styles" — a tokenized scale exists (values undisclosed in extract). (marber.economist.com)
- [OBSERVED] Role-based hierarchy: Serif = body text / descriptions / headlines; Sans = section openers, fly titles, datelines, metadata, captions; Sans Headline = display (covers). (marber.economist.com; tdc.org)
- [OBSERVED] Homepage headline→standfirst pairing as a fixed unit: headline ("There is an 'imminent' threat to Taiwan, America warns") + one-line dek ("Pete Hegseth says a war would be devastating for the world"). (wayback snapshot 2025-06-01, economist.com homepage)
- [OBSERVED] Section labels precede headline groups: "Asia", "The world in brief", "Discover more", "Latest videos", "Special reports". (wayback snapshot)
- [OBSERVED] Edition module: "Edition: May 31st 2025" + cover-story headline ("New, untested and dangerous") with 4 sub-headlines, each carrying a one-line dek. (wayback snapshot)
- [INFERRED] Hierarchy leans on family/weight/role contrast between Serif and Sans rather than on colour.

## 4 Spacing & density

- [OBSERVED] Homepage text structure is headline-led and dense: stacked groups of headlines + one-line deks with minimal intervening copy; no imagery or promo cards discernible in the text extraction. (wayback snapshot)
- [OBSERVED] The design system explicitly includes "Web Grid, components and patterns" — a defined grid exists. (marber.economist.com home, via search snippet "colour, typography and brand Web Grid, components and patterns")
- [UNDEFINED] Spacing scale values, margins, masonry/grid parameters — none surfaced (Marber grid page not fetched).

## 5 Shape language & corner treatment

- [OBSERVED] "Rectangles of varying sizes at play throughout both in static and animated assets" are the core shape device of the Group identity. (printmag.com, ¶4)
- [OBSERVED] Rectangle motif semantics per entity: "The Lens" (Intelligence), "The Steps" (Education), "The Frame" (Group), "The Stage" (Impact). (printmag.com, ¶4)
- [OBSERVED] 2025 refresh (Nomad): 'glyphs' — symbols "previously used as periods at the end of articles" — "reborn as a visual language that composes marketing texts, emphasizes key messages, and adds rhythm and precision". (designcompass.org)
- [UNDEFINED] Corner radius / stroke weights — no values stated.

## 6 Borders, surfaces & elevation

- [OBSERVED] "Crisp lines, typing cursors, and search bars... dominate the new visual identity." (printmag.com, ¶5)
- [OBSERVED] Palette base is black/white with red as the single accent; described as "simple and clean". (printmag.com, ¶4; creativereview.co.uk)
- [UNDEFINED] Shadow/elevation treatment, card surface treatment — nothing captured.

## 7 Iconography & imagery

- [OBSERVED] Imagery device: "blurred-out photographs that come into focus in particular sections". (printmag.com, ¶5)
- [OBSERVED] Homepage carries a "Latest videos" module and 1843 magazine story slots. (wayback snapshot)
- [OBSERVED] Glyphs (small period-like marks) function as a symbolic micro-language. (designcompass.org)
- [UNDEFINED] Icon-set specifics — not captured.

## 8 Layout rhythm & navigation

- [OBSERVED] Homepage module inventory: regional section blocks ("Asia"), "The world in brief" (news digest: bold entity names + terse updates), "Discover more" (product links: The Intelligence podcast, poll trackers), "Latest videos", weekly "Edition" block, "Special reports". (wayback snapshot)
- [OBSERVED] Group site (current) presents three brands — *The Economist*, Economist Enterprise, Economist Education — with the Group "existing to champion progress". (economistgroup.com)
- [OBSERVED] 2022 rebrand had consolidated "over fifty brands down to four": The Economist, Economist Impact, Economist Intelligence, Economist Education. (printmag.com, ¶3; creativereview.co.uk)
- [INFERRED] Group architecture evolved between 2022 (four entities incl. Impact/Intelligence) and the current site (three: Enterprise/Education + The Economist).
- [OBSERVED] Marber design system is scoped as "a visual language, set of components, and guidelines that form the foundation of our products and digital experiences", covering "colour, typography and brand Web Grid, components and patterns". (marber.economist.com home + search snippet)
- [UNDEFINED] Masthead/nav component specifics — live site unobservable.

## 9 Interaction cues & motion

- [OBSERVED] Rectangle assets exist "in static and animated" form — motion is native to the identity. (printmag.com, ¶4)
- [OBSERVED] Nomad's scope included "motion design, and toolkit development" with consistency "across all touchpoints" (podcasts, videos, live events). (designcompass.org)
- [OBSERVED] "Typing cursors, and search bars" recur as interface cues in the identity. (printmag.com, ¶5)
- [OBSERVED] Blur→focus photographic reveals act as a sectional transition device. (printmag.com, ¶5)
- [UNDEFINED] Durations / easing / specific animated behaviours.

## 10 Feedback & status representation

- [UNDEFINED] No feedback/status/error/notification components observed in any fetched source; Marber's component pages beyond typography were not reached.

## 11 Content style, tone & voice

- [OBSERVED] Founding mission quote (still quoted by the Group): "in a severe contest between intelligence, which presses forward, and an unworthy, timid ignorance obstructing our progress". (economistgroup.com; founding September 1843)
- [OBSERVED] Group self-description: "exists to champion progress"; provides "expertise, insights and perspective to press forward"; "commitment to excellence and independent thought"; editorial independence protected by trustees. (economistgroup.com)
- [OBSERVED] "The Economist's unique sharp writing style" is named as part of the brand identity; Nomad's scope included "language identity design". (designcompass.org)
- [OBSERVED] Standfirst voice examples — terse, witty, declarative: "From chips to satellites Euro-champions are back. Expect turbulence."; "Studies suggest moderate consumption is harmless. It may even be beneficial". (wayback snapshot)
- [OBSERVED] Homepage meta description: "Independent journalism"; site tagline framing "Get in-depth global news and analysis." (wayback snapshot metadata) — [OBSERVED] red+white graphic "used to champion both the quality of its reporting and the intellect of its readership". (creativereview.co.uk, ¶2)
- [OBSERVED] Group narrative built by "taking the success of The Economist editorial approach and applying it to how the other facets of The Economist Group function". (printmag.com, ¶3)
- [OBSERVED] Brand language positioned as fact-based, rigorous, "nearly two centuries" of reporting. (printmag.com, ¶1)

## 12 Responsive behaviour notes

- [OBSERVED] Marber tokens carry "iOS/Android" columns alongside CSS variables — cross-platform tokenization is built into the system. (marber.economist.com typography tables)
- [UNDEFINED] Breakpoints, responsive grids, mobile navigation behaviour — not captured (live site blocked).

## 13 Repeated motifs & devices

- [OBSERVED] "Red thread" connective theme across all Group brands. (printmag.com; creativereview.co.uk)
- [OBSERVED] Rectangles of varying sizes, static + animated, with four semantic registers (Lens / Steps / Frame / Stage). (printmag.com)
- [OBSERVED] Article-end 'glyphs' reused as a marketing/message-formatting visual language. (designcompass.org)
- [OBSERVED] Typing cursors, search bars, crisp lines. (printmag.com)
- [OBSERVED] Blur→focus photographic reveals. (printmag.com)
- [OBSERVED] Headline + one-line standfirst cadence; section-label grouping; "The world in brief" digest module; weekly cover-story "Edition" composition. (wayback snapshot)
- [OBSERVED] A2-Type's "interconnected and complementary" (sans, serif, headline) suite = a three-register typographic motif. (a2-type.co.uk; tdc.org)

## Gaps & UNDEFINED candidates

- **Red value** — no hex/Pantone for The Economist red in any fetched source (the brief asked for Pantone 485C family / hex "if stated"; it was not stated). HIGH priority gap.
- **Colour & grid token values** — Marber's colour page and Web Grid page were not fetched (only the typography page was reachable; direct URL unknown). Token namespace observed: `--mb-*`.
- **Live 2026 site behaviour** — economist.com 403/Cloudflare-blocked; substitutions: 2025-06-01 Wayback snapshot (structure/voice only, no CSS) — hover/motion timing, nav components, responsive behaviour unobserved.
- **Shape specifics** — corner radii, rectangle proportions, glyph geometry: UNDEFINED.
- **Style-guide body** — brandingstyleguides.com page is "The Economist Group standards manual" (posted 2022) but content is not machine-readable (title/date only).
- **Feedback/status patterns** — nothing captured.

## Raw extracts

- raw/printmag-economist-group-rebrand.md
- raw/designcompass-2025-refresh.md
- raw/marber-ds-typography.md
- raw/marber-ds-home.md
- raw/tdc-award-typography.md
- raw/a2type-custom.md
- raw/creativereview-wolff-olins.md
- raw/brandingstyleguides-teg.md
- raw/economistgroup-home.md
- raw/wayback-economist-home-2026.md

## Addendum (post-inventory follow-up fetches, 2026-10-07)

- [OBSERVED] **Marber colour values page** (fetched: `marber.economist.com/8e1dcf0b8/p/543b0f-colour` + subpage b/37fc5e): Economist Red **#E3120B** (RGB 227,18,11; CMYK 0,100,100,0); Red 42 #CC100A · Red 60 #F6423C · Red 95 #FEE7E7; greyscale ramp "London" #0D0D0D → #FFFFFF (9 steps); canvas tints (Chicago/Los Angeles/Paris/Singapore/Economist Red 85/90/95); accent city palettes (Chicago blue · Hong Kong teal · New York yellow · Shanghai green · Singapore orange · Tokyo pink) for data/section use; 1843 Red #B30000 + Zurich #FFBB1A; token namespace `--mb-colour-*`. **This closes the red-value gap.**
- [OBSERVED] **Marber principles page**: six design principles quoted verbatim — "Less is more / Deliberate typography / Visual harmony / Clear wayfinding / Intelligence and wit / Recognisable consistency" (raw/marber-ds-principles.md).
- Raw extracts: raw/marber-ds-colour-values.md · raw/marber-ds-principles.md
