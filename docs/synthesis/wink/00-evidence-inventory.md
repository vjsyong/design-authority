# wink (Mailchimp) · Evidence inventory (Phase 3)

Date: 2026-10-07 (UTC) · Workstream: Authority Synthesis — source-positive evidence capture for source "wink" (Mailchimp, the email-marketing brand by Intuit; identity since the 2018 Collins redesign). Scope: evidence capture only, no design advice, no comparison with other sources. Every line carries [OBSERVED] / [INFERRED] / [UNDEFINED] and cites its source; short source keys map to the fetch log below. Values are verbatim from sources where quoted.

## Fetch log

| # | url | ok/failed | used for |
|---|---|---|---|
| 1 | https://mailchimp.com/about/brand-assets/ | ok (200, x2) | official usage rules, name rule, Freddie, colour names |
| 2 | https://fontsinuse.com/uses/39539/mailchimp-identity-2018-redesign | ok (200; content 2014 days old) | Collins redesign, Cooper BT Light → Means history, quotes |
| 3 | https://www.canny-creative.com/atlas/brand/mailchimp/ | ok (200) | hex values, Means/Graphik pairing, history/voice summary |
| 4 | https://www.designsystems.one/design-systems/mailchimp-design | ok (200; truncated 9000/10209) | token tables (self-declared non-canonical) |
| 5 | https://mailchimp.com/ | ok (200; truncated 9000/11599) | live homepage copy, structure, CTAs |
| 6 | https://wearecollins.com/case-studies/mailchimp/ | partial (200; SPA — content_ok=false, boilerplate/shell text captured) | Collins system rationale |
| 7 | https://gdusa.com/collins-goes-bananas-over-mailchimp-identity/ | ok (200; 2018 launch press) | 2018 launch description |
| 8 | https://mailchimp.com/design/ | ok (200 — serves brand-assets content) | official "design" docs URL resolution |
| 9 | https://mailchimp.com/pricing/ → /pricing/marketing/ | ok (200; truncated 6500/23885) | plan UI, badges, validation strings, microcopy |
| 10 | https://mailchimp.com/ (live DOM, real browser, 1280×577) | ok | computed styles: type, colour, radius, shadow, motion |
| 11 | live hover-state probe on same page (CDP Input.dispatchMouseEvent) | failed (daemon timeout after 5s) | intended: :hover end values — not captured |

Raw extracts: raw/01…raw/09 (see bottom).

## 1 Colour usage

- [OBSERVED] "Cavendish Yellow is Mailchimp's hero color. We use Peppercorn for accents." (mailchimp.com/about/brand-assets/ §guidelines). The page states colour names, not hex values.
- [OBSERVED] Cavendish Yellow = #FFE01B (canny-creative brand atlas, §Colour; corroborated by designsystems.one token table `--mc-cavendish #ffe01b`, and by live button fill below).
- [OBSERVED] Peppercorn = #241C15, described as "near-black … (warm black)" and "Primary text" (canny-creative §Colour; designsystems.one `--mc-peppercorn`).
- [OBSERVED] designsystems.one supporting set: `--mc-text-secondary #5d5245`, `--mc-white #ffffff`, `--mc-parsnip #f6f6f4` ("warm subtle background"), `--mc-border #dedddc`, `--mc-kale #007c89` ("Links and interactive (teal)"), `--mc-error #bf4055` ("Errors"). Source self-declares "0/66 fields have an explicit source" — indicative, not canonical.
- [OBSERVED] Live CTA fill = rgb(255, 224, 27) = #FFE01B with text rgb(35, 30, 21) = #231E15 (mailchimp.com, computed style of "Start Free Trial"). Note: the live ink value #231E15 differs by one step from the documented Peppercorn #241C15 — flagged in Gaps.
- [OBSERVED] Live inverse CTA: background rgb(35, 30, 21) with white text (mailchimp.com, "Start Free Trial" sample) — a dark variant of the same button pattern.
- [OBSERVED] Live footer surface = rgb(231, 183, 95) = #E7B75F (warm ochre/wheat) with black text and links rgb(35, 30, 21) (mailchimp.com, computed style of `footer`).
- [OBSERVED] Live surfaces are predominantly white: body background #ffffff; a section-level neutral #F5F5F5 also present (mailchimp.com, bg histogram).
- [OBSERVED] canny-creative: "a broader supporting palette of muted greens, peach tones, blues and reds used across campaigns so the system doesn't lean on yellow alone" (§Colour) — described in words, no values given.
- [OBSERVED] Live inline link on white uses rgb(35, 30, 21) with underline (mailchimp.com, sampled "Essentials" link); the documented teal link token #007c89 was not observed in the sampled elements.
- [OBSERVED] Collins: "yellow-heavy color palette" (wearecollins.com case study §approach).

## 2 Typography

- [OBSERVED] Display face (live): `"Means Web", Georgia, Times, "Times New Roman", serif` — h1 at 64px, weight 400, line-height 76.8px, letter-spacing -1.2px, colour rgb(255,255,255) (mailchimp.com, computed style of `h1`).
- [OBSERVED] Secondary display sample: h2 "Most Popular" — Means Web, 35.2px / line-height 35.2px (ratio 1.0), weight 400, letter-spacing -0.5px (mailchimp.com, computed style).
- [OBSERVED] UI/body face (live): `"Graphik Web", "Helvetica Neue", Helvetica, Arial, Verdana, sans-serif` — body 16px / line-height 21.6px (1.35) (mailchimp.com, computed style of `body`).
- [OBSERVED] Button label type: Graphik Web, 13px, weight 500 (mailchimp.com, computed style of "Start Free Trial").
- [OBSERVED] Live weight-of-use: Graphik Web on ~967 sampled elements vs Means Web on ~50 — the display serif is used sparingly; the sans carries the interface (mailchimp.com, font histogram).
- [OBSERVED] Stack fallbacks documented as `Means, Georgia, serif` and `Graphik, 'Helvetica Neue', Arial, sans-serif`; Means weights: 400; Graphik weights: 400, 500, 700 (designsystems.one §Typography).
- [OBSERVED] Documented type scale: display 48/56, h1 32/40, h2 24/32, body 16/24, small 14/20 (designsystems.one §Type scale). Live marketing h1 (64px) and h2 (35.2px) exceed those steps.
- [OBSERVED] History: 2018 identity shipped with "Cooper BT Light, Bitstream's cleaned-up digital version of the much better-known Cooper Black" (fontsinuse.com).
- [OBSERVED] 2020: Cooper replaced by Means — "Greg Gazdowicz at Commercial Type redrew Cooper Old Style and expanded it into an entirely new family called Means" (fontsinuse.com). Rationale quoted: Cooper "came up short in its limited weight range, poor suitability for interface design" (fontsinuse.com).
- [OBSERVED] Means positions between extremes, in Mailchimp's words: "Smart but not stuffy. Goofy but definitely aced its SATs." (fontsinuse.com).
- [OBSERVED] canny-creative: "Means now carries large marketing headlines, while the clean, highly legible sans-serif Graphik handles body copy and product UI" (§Typography).
- [OBSERVED] Wordmark: "a new hand-lettered logo" (fontsinuse.com); "The wordmark was redrawn based on Cooper Light, customised for distinctiveness and digital use" (canny-creative); "an updated logo simplified to work at any size" (gdusa.com).
- [OBSERVED] Discrepancy: gdusa.com (2018) says the wordmark "replaces the previous script with a bold sans-serif font" — conflicting with the Cooper/Means serif accounts; unresolved (see Gaps).
- [OBSERVED] Name rule: "'Mailchimp' is one word, spelled with a big M and a little c. It used to have a big M and a big C, but the times have changed." (mailchimp.com/about/brand-assets/ §Our name).
- [OBSERVED] No font licence/vendor line for Graphik was seen on any fetched source; Means is attributed to Commercial Type / Greg Gazdowicz (fontsinuse.com).

## 3 Scale & hierarchy

- [OBSERVED] Homepage runs 1 × h1 against 25 × h2 (mailchimp.com, DOM counts) — one page-level title, then section-level sub-headings.
- [OBSERVED] Live hero h1 (64px) sits ~4× the body size (16px); hero supporting paragraph 20px/32px (mailchimp.com, computed styles).
- [OBSERVED] Live h2 renders at a non-integer size (35.2px) with 1.0 line-height — tight, headline-as-block treatment (mailchimp.com, computed style).
- [OBSERVED] Documented 5-step scale (14→48px, designsystems.one §Type scale) functions as the product-UI ramp; marketing pages run a larger, separate range (64px h1 observed live).
- [OBSERVED] Pricing page plan tier order: Premium / Standard / Essentials / Free, with Standard badged "Most Popular"; plan headers are h2-level (mailchimp.com/pricing/marketing/).
- [OBSERVED] Credibility numbers are given display treatment in copy: "11 million businesses", "27x ROI", "33,000+ reviews", "300+ apps" (mailchimp.com homepage).

## 4 Spacing & density

- [OBSERVED] Documented base unit 8px with scale 8 / 16 / 24 / 32 / 48 (designsystems.one §Spacing).
- [OBSERVED] Live CTA padding 12px 24px (mailchimp.com, computed style) — 4/8px-multiple geometry.
- [OBSERVED] Live hero container padding 40px 0; hero section padding 68px 0 0 (matches the 68px sticky header height — content offset under the sticky bar) (mailchimp.com, computed styles).
- [OBSERVED] Live card interior padding 48px (mailchimp.com, 16px-radius card with white bg).
- [OBSERVED] Live footer padding 60px 0 (mailchimp.com, computed style).
- [OBSERVED] Homepage structure spans 55 `<section>` elements (mailchimp.com, DOM counts) — a long, low-density, section-stacked marketing page.
- [OBSERVED] `main` computed max-width: none at 1280px — full-bleed layout rather than a centred fixed container (mailchimp.com).

## 5 Shape language & corner treatment

- [OBSERVED] Live border-radius histogram across a,button,input,div: 0px ×599, 4px ×177, 3px ×55, 16px ×35, 26px ×25, 8px ×21, 2px ×20, 24px ×8, 10px ×5, 50% ×4 (mailchimp.com).
- [OBSERVED] Primary CTA is a pill: border-radius 26px on a ~43.5px-high button (≈ half-height, full pill); one sampled variant at 40px (mailchimp.com, computed styles).
- [OBSERVED] Cards/panels: 16px and 24px radii (mailchimp.com, computed styles).
- [OBSERVED] Documented radius tokens: `default 8px`, `pill 9999px` (designsystems.one §Corner radius).
- [INFERRED] No single global radius: the system mixes square structural elements (0px dominant), small 2–4px details, and fully-rounded pill CTAs — shape encodes element class.

## 6 Borders, surfaces & elevation

- [OBSERVED] Card elevation: shadow `rgba(35, 30, 21, 0.2) 0px 8px 32px 0px`, no border, white bg, 16px radius, 48px padding (mailchimp.com) — shadow tinted with the warm ink colour, not pure black.
- [OBSERVED] Second elevation sample: `rgba(0, 0, 0, 0.06) 0px 4px 16px 0px` on a 24px-radius element (mailchimp.com).
- [OBSERVED] Header: sticky, 68px tall, background rgba(0,0,0,0) (transparent over the hero), no bottom border (mailchimp.com, computed style).
- [OBSERVED] Footer is a solid warm fill (#E7B75F) with 60px vertical padding — a full-width colour block as page terminator (mailchimp.com).
- [OBSERVED] Documented border colour token #dedddc (designsystems.one §Color tokens).
- [OBSERVED] Live homepage bg histogram: transparent ×38, #ffffff ×17, #F5F5F5 ×3, #E7B75F ×1 (mailchimp.com) — mostly white with coloured banding.

## 7 Iconography & imagery

- [OBSERVED] "We always pair our company name with the Freddie icon. And Freddie's always winking because he has a great attitude." (mailchimp.com/about/brand-assets/) — the wink is a fixed, non-optional attribute of the mark.
- [OBSERVED] "When placing our logo on a dark background, use the reverse version" (mailchimp.com/about/brand-assets/) — a dedicated reversed lockup.
- [OBSERVED] Clear-space rule: "Provide plenty of space around the Mailchimp logo and Freddie. Make them big, make them small, just give them the chance to breathe and not feel cluttered." (mailchimp.com/about/brand-assets/).
- [OBSERVED] "Freddie was simplified into cleaner lines and a stronger silhouette" in 2018; Freddie "promoted from mascot to genuine brand asset, now appearing in product UI moments, loading states, error messages, campaign creative, social avatars and merchandise, deliberately restrained so as not to feel childish or overpower functional interfaces." (canny-creative §identity history).
- [OBSERVED] Collins: the system includes "hallmark illustration and photographic styles" maintaining "a precise balance between the sophisticated and the surreal" (wearecollins.com); "Imagery and illustrations are also quirky and new, and the guidelines provide greater flexibility in their use." (gdusa.com).
- [OBSERVED] Illustration is a named system component: "Wink (illustration system) — Branded illustration set with documented usage and themable color"; "Illustration as a system component — house-style, themable, and used consistently across surfaces" (designsystems.one §Components / Known for).
- [OBSERVED] Live homepage carries 104 `<img>` and 73 `<svg>` (mailchimp.com, DOM counts); image alts include functional UI icons — "chat icon", "star icon", "calendar icon" — and third-party logos (Shopify, WooCommerce, Canva, Zapier, Square, Wix, Squarespace, Stripe, Salesforce, LinkedIn, Wordpress, Facebook) (mailchimp.com, alt sample).
- [OBSERVED] Browser title carries an emoji: "🐴 Email & SMS Marketing Platform | Mailchimp" (mailchimp.com, live `document.title`).

## 8 Layout rhythm & navigation

- [OBSERVED] Nav information architecture: "Industries and Solutions" mega-menu with audience column (Restaurants, Entertainment + Leisure, Non-profit, Ecommerce, Small Business, Professional Services, Mid Market) and a solutions column (Email marketing, AI marketing tools, Marketing automations, Content creation tools, Social media marketing, Reporting and analytics, Lead generation platform, Templates, "See all features and solutions") (mailchimp.com, header links).
- [OBSERVED] A resources/secondary group follows: Help Center, Case Studies, Events, Hire an Expert, Personalized onboarding, Customer success (mailchimp.com).
- [OBSERVED] An integrations directory is exposed in nav: "See 300+ Integrations" plus per-app entries (Shopify, WooCommerce, Canva, Zapier, Square, Wix, Squarespace, Stripe, Salesforce, LinkedIn, Wordpress, Facebook) and categories (E-commerce, Analytics, Booking & Scheduling) (mailchimp.com).
- [OBSERVED] Homepage section rhythm, in order: rotating audience hero headlines (Ecommerce, Small Business, Non-profit, Professionals, Content creators) → "Take an interactive product tour" → "Recommended for your business" → "Businesses like yours are thriving with Mailchimp" → Standard plan trial promo → Premium offer → "One marketing platform to unite 300+ apps" → "Millions of users trust us…" → footnoted disclaimers (mailchimp.com).
- [OBSERVED] Section header pattern: small audience label ("EMAIL & SMS FOR ECOMMERCE") above a display headline, followed by a one-to-two-sentence supporting paragraph (mailchimp.com).
- [OBSERVED] Social-proof block format: "4.5 out of five" with "Based on 33,000+ reviews across G2 · Capterra · TrustRadius" attribution (mailchimp.com homepage and /pricing/marketing/).
- [OBSERVED] Pricing layout: tier cards (Premium / Standard / Essentials / Free) followed by a "Key Plan Features" comparison table with per-tier columns (mailchimp.com/pricing/marketing/).
- [OBSERVED] Sticky header persists over the hero (position: sticky; height 68px) (mailchimp.com, computed style).

## 9 Interaction cues & motion

- [OBSERVED] Primary CTA transition: `transform 0.3s cubic-bezier(0.5, 2.5, 0.7, 0.7), box-shadow 0.3s cubic-bezier(0.5, 2.5, 0.7, 0.7)` — a spring/overshoot easing (control-point values above 1) (mailchimp.com, computed style of "Start Free Trial").
- [OBSERVED] Common transition set on links/buttons: `background-color 0.15s` (182 elements), `all` (157), `box-shadow 0.2s` (34), `color 0.15s ease-in-out, transform 0.3s` (7), `font-size 0.3s ease-in-out` (4) (mailchimp.com, transition histogram) — hover feedback is fast (0.15s) with a slower 0.3s movement layer on special elements.
- [OBSERVED] Animated font-size transition (0.3s ease-in-out) appears on 4 elements — size itself animates in at least one pattern (mailchimp.com).
- [INFERRED] The spring bezier on the CTA implies a scale/lift-and-shadow response on hover; the exact end transform/shadow values were not captured.
- [UNDEFINED] Hover end-states, focus rings, scroll-triggered animation, and hero media behaviour (video/Lottie) — not captured; the hover probe (CDP `Input.dispatchMouseEvent`) failed with a 5s daemon timeout (fetch log #11).
- [OBSERVED] Hero composition implies an overlay treatment: the h1 renders white on transparent ancestors (no background colour on the hero chain), i.e. type sits on a non-CSS-colour backdrop (image/video) (mailchimp.com, hero chain computed styles).
- [OBSERVED] "a multi-step editor with previews and pause-and-resume" and "async send" are named as flow patterns in the product (designsystems.one §Components worth studying) — behavioural, not visual, evidence.

## 10 Feedback & status representation

- [OBSERVED] Validation string in the live pricing UI: "Contact limit exceeded — You've selected more contacts than this plan allows" (mailchimp.com/pricing/marketing/).
- [OBSERVED] Status copy: "Sending will be paused if contact or email send limit is exceeded." (mailchimp.com/pricing/marketing/).
- [OBSERVED] Badge/banner copy: "Most Popular" plan badge; "Save 15%"; "Free for 14 days"; "Under 250 contacts? It's free." (mailchimp.com/pricing/marketing/).
- [OBSERVED] Rating representation: "4.5 out of five" with star imagery implied by alt "star icon" (mailchimp.com alt sample; /pricing/marketing/ copy).
- [OBSERVED] Documented semantic colours: `--mc-error #bf4055` ("Errors"); a success token is named in the illustrative token list ("color-success — Confirmed actions, sent campaigns"), value not given (designsystems.one §Color tokens).
- [OBSERVED] Error/limit states are phrased plainly and non-blaming ("You've selected more contacts than this plan allows"; "We've got your back") (mailchimp.com/pricing/marketing/).
- [OBSERVED] Footnote discipline: homepage ends with numbered disclaimers and a CTA-proximity note ("'Terms apply' / '14-day trial terms apply' next to Start Free Trial") (mailchimp.com homepage).

## 11 Content style, tone & voice

- [OBSERVED] Tone described as "straightforward, encouraging, confident and creative-led … plain English over jargon, calm authority over hype, and dry wit that never excludes the audience from the joke" (canny-creative §voice).
- [OBSERVED] Collins framing: "a potent combination of wry humor, modest celebration, and a dash of absurdity"; "growing up and staying weird" (wearecollins.com; same quote in fontsinuse.com).
- [OBSERVED] Headline grammar: an italicised emphasis fragment sits inside an otherwise regular headline — "Email & SMS marketing *minus the learning curve*"; "*Effortless growth* powered by your data"; "*AI-powered marketing* that brings your customers to you" (mailchimp.com, markdown emphasis preserved from italics).
- [OBSERVED] Microcopy samples: "Not sure how to choose? We've got your back. Answer a few quick questions and we can make a personalized recommendation for you."; "Discover why 11 million businesses choose Mailchimp."; "Larger contact list? Call +1 (800) 330-4838…" (mailchimp.com, /pricing/marketing/).
- [OBSERVED] Copy addresses the reader directly in second person, question-first ("Under 250 contacts? It's free."), and offers an easy exit from commitment ("Cancel or downgrade … at any time").
- [OBSERVED] Even legal copy is warmed: "This is a friendly legal reminder that these graphics are proprietary…"; "just give them the chance to breathe and not feel cluttered" (mailchimp.com/about/brand-assets/).
- [OBSERVED] CTA labels in use: "Start Free Trial", "Take an interactive product tour", "View all integrations", "Contact sales", "Learn more" — all plain, low-pressure verbs (mailchimp.com).
- [OBSERVED] Self-description for the post-2018 brand era: "35 cutting-edge AI-driven marketing technology stack … sorted into five categories" and the strategy line "Fuel small and midsize businesses growth by democratizing cutting-edge marketing technology" (wearecollins.com).

## 12 Responsive behaviour notes

- [OBSERVED] All live observations were made at a single viewport, 1280×577 (mailchimp.com, browser probe) — no responsive comparison was performed.
- [OBSERVED] `main` computed `max-width: none` at 1280px (mailchimp.com) — the marketing layout is full-bleed, not a centred fixed-width container.
- [OBSERVED] Header is 68px tall and sticky; hero section padding-top equals 68px, consistent with a header-height offset (mailchimp.com) — the mechanism to accommodate it at other heights is not evidenced.
- [UNDEFINED] Breakpoints, mobile nav pattern, type down-scaling, and touch-target sizing — no evidence captured on any fetched source.
- [INFERRED] The 64px / 1.2-line-height / -1.2px-tracking hero headline is a large-screen treatment; its small-viewport rendering was not observed.

## 13 Repeated motifs & devices

- [OBSERVED] Yellow-as-CTA: every sampled "Start Free Trial" button fills with #FFE01B except one dark inverse variant (mailchimp.com, button sample) — yellow is reserved for primary action + brand surface.
- [OBSERVED] Fred the winking chimp (Freddie) is a mandatory companion to the wordmark, never drawn non-winking (mailchimp.com/about/brand-assets/).
- [OBSERVED] Serif-display / sans-UI pairing (Means + Graphik), with the sans doing ~95% of on-page work (mailchimp.com font histogram; canny-creative §Typography).
- [OBSERVED] Emphasis-by-italic inside regular-weight serif headlines (mailchimp.com live headline set).
- [OBSERVED] Pill CTA + springy micro-motion as a repeated interactive signature (radius 26px + cubic-bezier(0.5, 2.5, 0.7, 0.7)) (mailchimp.com computed styles).
- [OBSERVED] Warm neutral surfaces instead of clinical grey: #F6F6F4 "Parsnip" documented; #F5F5F5 and #E7B75F observed live (designsystems.one; mailchimp.com).
- [OBSERVED] Audience-segmented headline rotation (Ecommerce / Small Business / Non-profit / Professionals / Content creators) as a page-opening device (mailchimp.com).
- [OBSERVED] Number-led credibility devices: 11 million businesses, 27x ROI, 33,000+ reviews, 300+ apps, 35 tools (mailchimp.com; wearecollins.com).
- [OBSERVED] Playful micro-signals: winking mascot, horse emoji in the browser title, "a dash of absurdity" in illustration (mailchimp.com; brand-assets; Collins).

## Gaps & UNDEFINED candidates

- [UNDEFINED] Hover/focus end-states for the CTA (transform + shadow values at `:hover`) — probe failed (daemon timeout); only the transition declarations were captured.
- [UNDEFINED] Motion beyond hover: scroll animations, hero media (image vs video vs Lottie), page transitions — no evidence.
- [UNDEFINED] Exact values for the "broader supporting palette of muted greens, peach tones, blues and reds" (canny-creative) — described in words only; no hexes found.
- [UNDEFINED] Pantone / CMYK equivalents — not stated on the brand-assets page or any fetched source.
- [UNDEFINED] Breakpoints and mobile-specific layout/type behaviour.
- [UNDEFINED] Dark-mode treatment; focus-ring styling; disabled states; loading-state visuals (mentioned in canny-creative as a Freddie placement but not observed).
- [UNDEFINED] Spacing tokens for the product UI itself (only marketing-page geometry was measurable live).
- [CONFLICT] Peppercorn value: documented #241C15 vs live ink rgb(35,30,21) = #231E15 — one-step difference, unresolved.
- [CONFLICT] Wordmark type class: gdusa.com (2018) "bold sans-serif font" vs fontsinuse.com / canny-creative "redrawn based on Cooper Light" (serif) — unresolved from public sources.
- [CAVEAT] designsystems.one self-declares "0/66 fields have an explicit source and 0 have a recorded check date" and an "Editable editorial reference"; all its token values are indicative, not canonical. The official docs URL it cites, mailchimp.com/design/, currently serves the brand-assets page.
- [CAVEAT] The brand-assets page itself is partially generic SEO/FAQ copy ("Some of the most common questions people ask about branding assets…") — only the quoted guideline sentences are treated as Mailchimp-specific here.

## Raw extracts

- raw/01-mailchimp-brand-assets.md — official guidelines, name rule, Freddie, colour names
- raw/02-fontsinuse-39539.md — Collins/Collins-era type history and quotes
- raw/03-canny-creative-atlas-mailchimp.md — hex values, Means/Graphik, history, voice
- raw/04-designsystems-one-mailchimp.md — token tables, type scale, spacing, radius, components (non-canonical)
- raw/05-mailchimp-homepage.md — live homepage copy and structure
- raw/06-collins-case-study.md — Collins rationale (partial; SPA)
- raw/07-gdusa.md — 2018 launch press text
- raw/08-live-dom-probe.md — computed-style JSON from live mailchimp.com
- raw/09-pricing-and-design-redirect.md — /design/ resolution + pricing UI copy
