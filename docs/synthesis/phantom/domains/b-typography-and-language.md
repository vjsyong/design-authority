# B · Typography & Language — deployed typography of the Phantom site

Pass-2 domain report (screenshot-first). Source of truth: the renderable mirror at
`docs/synthesis/phantom/_raw/site/` (served on 127.0.0.1:8943 with network on, so the
deployed Google-Fonts import loads exactly as for a real visitor; live site
`zhenyoyo.github.io` cross-checked for the font import + wordmark only). Substrate
`_raw/upstream/` + `_raw/css-diff.txt` used for BASE/OVERRIDE tagging.

## Summary (what the site IS, typographically)

- One family, three deployed weights: **Source Sans Pro 300 / 700 / 900** loaded via
  `@import` from Google Fonts (`main.css:2`). No 400, no italic faces.
- Three voices: **300 light sentence-case body**; **700 bold, tight (−0.035em) sentence-case
  h1**; **900 black, uppercase, +0.35em-tracked heads/wordmark/nav/buttons**. Table heads,
  form labels and menu links drop the caps voice and sit at mixed case.
- Body leading 1.75; body text column 68em (1008px at 1280 / 350px at 390) → extremely long
  measure at desktop (≈150 chars/line estimate).
- **Pink body type is the deployed default** (`#ff6bbc` replacing the template's `#585858` grey,
  an OVERRIDE); links are neon green `#6bff2c` with a blue dotted underline. Per-page overrides
  flip whole pages to black (light/fafa/tame/Unlogical via inline `<style>`; publication via a
  `.publication{color:black}` rule appended to main.css) or tint only the h1 (project pages).
- **CJK: no CJK font is declared anywhere.** The 圳 in index's wordmark falls through the stack to
  the OS — in this render: WenQuanYi Zen Hei (system font), unstyled and untracked, next to
  SourceSansPro-Black Latin. All other pages' Chinese text is in comments/CSS comments (not
  rendered) or inside embeds/images.
- Italic (`em`, `blockquote`) is **synthesised** — the roman Light file is used, no italic face
  exists in any import.
- Language: pages are English; only `index.html` carries a `lang` attribute (on a second, nested
  `<html lang="en">` tag). Wordmark copy differs on every page group (template leftovers:
  `Phantom`, `© Untitled. All rights reserved`).

## Method & evidence

- Probes: Playwright (Chromium) computed-style collection for ~35 selectors × 9 pages at
  1280×900 and 390×844; CDP `CSS.getPlatformFontsForNode` for actual per-glyph font attribution;
  `document.fonts` for webfont load state; canvas char-width measurement; pixel sampling of the
  screenshots (PIL) to arbitrate rendered colours.
- Screenshots (14, `docs/synthesis/phantom/evidence/screens/`), each read with vision:

| file | viewport | vision read (gist) |
|---|---|---|
| type-index-1280.png | 1280 full | pale pink body, bright pink h1 + tracked caps h2, 圳 in wordmark, very low contrast body |
| type-elements-1280.png | 1280 full | pink page; blue-ground code; tables with pink 900 heads; buttons grey/white |
| type-light-1280.png | 1280 full | black body + pink h1; black tracked-caps h2; green links (vision first said "pink" — pixel sampling shows green) |
| type-publication-1280.png | 1280 full | black h1/body; pink footer heads; green links; comfortable contrast |
| type-generic-1280.png | 1280 full | pink body+h1; tracked caps heads; grey footer w/ pink heads, charcoal Send button |
| type-email-1280.png | 1280 full | two pink sentence-case h1s; page ends abruptly, no footer |
| type-fafa-1280.png | 1280 full | pink-coral h1; black h2/body; green links; empty video slot |
| type-tame-1280.png | 1280 full | coral h1; black tracked-caps h2; near-black body; green links |
| type-unlogical-1280.png | 1280 full | pastel-blue h1 + `[01]/[02]` blue h2s; dark body; bilibili player shows CN chrome |
| type-index-390.png | 390 full | pink hierarchy scales cleanly; 圳 present; no overflow |
| type-elements-390.png | 390 full | table stacks cleanly; blue code block lines clipped at right edge |
| type-light-390.png | 390 full | black body, pink h1; CN text visible in embed chrome + artwork images |
| type-index-heading-1280.png | 1280 crop | wordmark `ZHEN WU YOYO 圳` pink; RANDOM GALLERY tracked caps; light pink intro |
| type-index-menuopen-1280.png | 1280 | neon-green overlay panel; black caps MENU heading; black title-case links |

## Findings 1 — families actually rendering (all rows OBSERVED-CSS unless noted)

| element | spec (as rendering) | pages | BASE/OVERRIDE | evidence |
|---|---|---|---|---|
| body/input/select/textarea | stack `"Source Sans Pro", Helvetica, sans-serif`; webfont loaded per `@import url(fonts.googleapis.com/css?family=Source+Sans+Pro:300,700,900)` (main.css:2) | all 9 | BASE (same upstream; live site identical) | computed + `document.fonts` (21 face entries = 7 subsets × 3 weights; latin subsets `loaded`) |
| body / p / a / inputs / blockquote / table cells | face **SourceSansPro-Light** (300) | all | BASE | CDP platform fonts: `Source Sans Pro Light`/`SourceSansPro-Light`, isCustomFont:true |
| h1 | face **SourceSansPro-Bold** (700) | all | BASE | CDP platform fonts |
| h2–h4, strong/b, wordmark, nav, buttons | face **SourceSansPro-Black** (900) | all | BASE | CDP platform fonts (`Source Sans Pro Black`/`SourceSansPro-Black`) |
| 圳 (index wordmark) | **WenQuanYi Zen Hei** (system; not a webfont) — no CJK family declared anywhere (the CSS's text families are only Source Sans Pro and Courier New; the rest are Font Awesome icon fonts) | index | OVERRIDE (deployed content) | CDP platform fonts: 1 glyph, `isCustomFont:false`; observed type-index-1280.png, type-index-heading-1280.png |
| em / i / blockquote italic | roman Light file used (postScript `SourceSansPro-Light`); zero italic faces in the captured Google CSS; import requests normal style only ⇒ **synthetic oblique** | elements (em, blockquote) | BASE | INFERRED from OBSERVED-CSS (postScriptName + zero `font-style: italic` faces) |
| code / pre | `"Courier New", monospace` → resolves to system **Liberation Mono** in this env | elements | BASE | computed + CDP platform fonts (`Liberation Mono`, non-custom) |

## Findings 2 — the scale (rendered px; BASE unless noted)

Body root sizes per band (rendered, OBSERVED-CSS): **12pt = 16px** at ≤1280 (measured 1280, 390),
**14pt = 18.67px** at ≤1680 (measured 1440), **16pt = 21.33px** above (measured 1920). Leading 1.75
everywhere (28px / 32.67px / 37.33px).

| level | size | weight | lh | tracking | case | pages | evidence |
|---|---|---|---|---|---|---|---|
| h1 | 2.75em = 44px @1280 (32px @≤736, 28px @≤360) | 700 | 1.3 | −0.035em (−1.54px) | as authored (sentence case) | all | OBSERVED-CSS; type-light-1280 (`I Light U Up`), type-publication-1280 |
| h2 | 1.1em = 17.6px (16px @≤736) | 900 | 1.5 | +0.35em (6.16px) | UPPERCASE (CSS) | all | OBSERVED-CSS + OBSERVED-VISUAL (all 1280/390 shots) |
| h3 | 1em = 16px (12.8px @≤736) | 900 | 1.5 | +0.35em (5.6px) | UPPERCASE | index, elements | OBSERVED-CSS |
| h4 | 0.8em = 12.8px | 900 | 1.5 | +0.35em (4.48px) | UPPERCASE | elements | OBSERVED-CSS; OBSERVED-VISUAL type-elements-1280 |
| h5/h6 | 0.8em | 900 | 1.5 | +0.35em | UPPERCASE | none rendered | CSS declaration only (main.css:225-231) |
| body p | 16px @1280 | 300 | 1.75 | normal | sentence case | all | OBSERVED-CSS + screens |
| links | inherit 16px | 300 | 1.75 | normal | sentence case | all | OBSERVED-CSS + pixel-sample (`#6bff2c`, dotted underline rgb(32,163,245)) |
| wordmark (.logo .title) | 16px (inherits) | 900 | 28px (1.75) | +0.35em (5.6px) | UPPERCASE (CSS on `YoYo` → `YOYO`) | all | OBSERVED-CSS + OBSERVED-VISUAL type-index-heading-1280 |
| header nav "Menu" | 16px, w900, +0.35em, uppercase in CSS but **visually suppressed** (text-indent 4em/overflow hidden; hamburger icon drawn by pseudo-elements) | all | BASE | OBSERVED-CSS + OBSERVED-VISUAL (icon-only in type-index-heading-1280.png) |
| buttons (input[submit]/.button) | 0.8em = 12.8px; .small 0.6em; .large 1em | 900 | 3.45em (44.16px) | +0.35em (4.48px) | UPPERCASE | elements | OBSERVED-CSS; type-elements-1280 |
| table th | 0.9em = 14.4px | 900 | 1.75 | none | **mixed case** (`Name`, `Description`, `Price`) | elements | OBSERVED-CSS + full-res crop read (`Name` mixed-case, heavy, pink) |
| table td | 16px | 300 | 1.75 | normal | mixed | elements | OBSERVED-CSS |
| code (inline) | 0.9em = 14.4px | 300 | 1.75 | normal | mixed | elements | OBSERVED-CSS |
| pre (block) | 0.9em = 14.4px; nested `pre code` 0.9em of that = 12.96px | 300 | 1.75 | normal | mixed | elements | OBSERVED-CSS |
| blockquote | 16px | 300 italic (synthetic) | 1.75 | normal | mixed | elements | OBSERVED-CSS |
| form labels/check labels | 1em = 16px | 300 | 1.75 | normal | sentence case | elements | OBSERVED-CSS |
| placeholder text | 16px | 300 | 1.75 | normal | mixed | elements+footers | UA default `rgb(117,117,117)`, unstyled (OBSERVED-CSS) |
| copyright / small print | 0.8em = 12.8px | 300 | 1 (12.8px) | normal | mixed | index, elements, publication, generic | OBSERVED-CSS |
| menu overlay links | 16px | 300 | 1.5 (24px) | normal | Title case (`Home`, `About` … ) | all (overlay) | OBSERVED-CSS + OBSERVED-VISUAL type-index-menuopen-1280 |
| menu overlay h2 "MENU" | 17.6px | 900 | 1.5 | +0.35em | UPPERCASE | all (overlay) | OBSERVED-CSS + OBSERVED-VISUAL |

Typography-only specs (radius/colour details of these controls belong to dom. C): button label colour
white; primary fill #585858; check/radio checked fill #f51616; field label colour #8833e3.

## Findings 3 — heading voice (case & tracking), BASE unless noted

- h1 voice: sentence case + w700 + negative tracking (−0.035em) — the only tight, mixed-case display voice.
- h2–h4 + wordmark + nav + buttons: UPPERCASE + w900 + +0.35em tracking (the template's "small-caps shout").
- Exceptions to the caps voice (measured): table heads (900, mixed case), form labels (300, sentence
  case), menu links (300, title case), body (300).
- The uppercase transform is CSS, not authored: source text uses mixed case (`Zhen Wu YoYo 圳`,
  `Random Gallery`); screenshots show `ZHEN WU YOYO 圳`, `RANDOM GALLERY` (type-index-1280.png).

## Findings 4 — pink-vs-black type story (computed colour per page)

| page | h1 | h2/h3 | body/p + strong | links | wordmark | grounds | tag |
|---|---|---|---|---|---|---|---|
| index | pink `#ff6bbc` | pink (section h2); tile h2 `#fff` over images | pink | green `#6bff2c` | pink + 圳 | white body, grey #f6f6f6 footer | OVERRIDE (pink) / BASE (tile white) |
| elements | pink | pink | pink (strong 900 pink) | green | `Phantom` pink | white / grey footer | OVERRIDE |
| light | pink (inline `style="color:#ff6bbc"`) | black | black | green | `Back to main` black | rgb(251,251,251) via inline `<style>` | page OVERRIDE |
| publication | **black** | black; footer h2 pink | black | green | `About Zhen` pink | white / grey footer | OVERRIDE (`.publication{color:black}` rule appended to main.css:3347) |
| generic | pink | pink | pink | green | `About Zhen` pink | white / grey footer | OVERRIDE |
| email | pink (“Email contact~”, and the address as a second h1) | — | — | — | `About Zhen` pink | white, no footer | OVERRIDE |
| fafa | `#fd77af` | black | black | green | `Back to main` black | rgb(251,251,251) | page OVERRIDE |
| tame | `#ff8b80` | black | black | green | black | rgb(251,251,251) | page OVERRIDE |
| Unlogical | `#71c3de` | `[01]`/`[02]` `#71c3de`; others black | black | green | black | rgb(251,251,251) | page OVERRIDE |

Deployment-wide pink/green swap (main.css overrides of the template): body/input/select/textarea
`#585858 → #ff6bbc`; `a` `#585858 → #6bff2c`; link underline `rgba(88,88,88,.5) → rgba(32,163,245,.999)`;
checkbox/radio label `#585858 → #8833e3`; checked-control fill `#585858 → #f51616`; code ground
`rgba(144,144,144,.075) → rgba(46,90,249,.986)`; menu overlay ground `#585858/#fff → #3ef900/#000`.

## Findings 5 — per-page variance (typography-relevant)

- **Footer presence/typography**: index & elements & publication & generic have the grey footer
  (h2 `GET IN TOUCH`/`FOLLOW` 900 tracked caps). light/fafa/tame/Unlogical ship with the whole
  `<footer>` **commented out** in source (no footer type at all); email has no footer block.
- **Wordmark copy per page**: index `Zhen Wu YoYo 圳`; elements `Phantom` (template leftover);
  publication/generic/email `About Zhen`; light/fafa/tame/Unlogical `Back to main`.
- **Small print copy**: index `la la la` (single li); elements/publication/generic
  `© Untitled. All rights reserved` + `Design: HTML5 UP`.
- **Titles**: index `Zhen Wu Yoyo` · elements `Elements - Phantom by HTML5 UP` · light `ILightUUP` ·
  publication `Zhen's publication</S>` (malformed closing tag in source) · generic `About Zhen` ·
  email `Zhen's email` · fafa `FAFA` · tame `Tame` · Unlogical `Unlogical Instrument`.
- **Mobile (390)**: hierarchy scales via media queries (h1 32px, h2 16px, h3 12.8px) and wraps
  cleanly; the only text-level breakage observed is the `pre` block, whose lines are clipped
  horizontally (overflow-x scroll) — OBSERVED-VISUAL type-elements-390.png.
- light.html's inline `<style>` comments are Chinese and one comment contradicts its value
  (comment 设置背景颜色为黑色 "set background to black" while the value is near-white
  rgb(251,251,251) — as deployed).

## Language notes (mixed CN/EN)

- `lang` attribute: only index reports `en` — and it comes from a *second, nested*
  `<html lang="en">` tag (source has `<html>` then `<html lang="en">`); all other 8 pages have no
  lang attribute. OBSERVED-CSS.
- Rendered Chinese text on the site = **only the 圳 glyph** in index's wordmark. Chinese elsewhere is
  non-rendered source (index inline-JS comments, the shared `<style>` comments in
  light/fafa/tame/Unlogical, commented-out Chinese paragraphs in index).
- Chinese does appear *rendered* inside third-party embeds: bilibili iframes show CN player chrome
  and CN video titles when loaded (type-unlogical-1280.png: `[1. Raincoat instrument]`; type-light-390.png:
  player labels 已静音开启 / 点击恢复音量 etc.), and artwork images contain CN text (type-light-390.png read).
- Embed load is flaky in the mirror: on index/fafa two of the embeds rendered as empty white space
  (type-fafa-1280.png) — footprint belongs to dom. D.

## Proposed pack entries

```json
[
  {
    "id": "guideline/typography-voices",
    "kind": "guideline",
    "title": "Typography — three voices of one family",
    "summary": "One family (Source Sans Pro 300/700/900 via Google Fonts @import). 300 light sentence-case body is the working voice; 700 tight-tracked sentence-case h1 (2.75em, -0.035em); 900 black tracked-caps for h2-h6, wordmark, nav, buttons (+0.35em). Table heads stay mixed-case 900; labels/menu links stay 300. Italic is synthetic (no italic faces loaded).",
    "aliases": ["typography", "font", "font weight", "heading voice", "Source Sans Pro", "type system"],
    "body": {
      "group": "Type",
      "faces": ["SourceSansPro-Light (300) body", "SourceSansPro-Bold (700) h1", "SourceSansPro-Black (900) heads/wordmark/nav/buttons"],
      "loading": "@import url(\"https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,700,900\") — main.css:2; no 400, no italics",
      "verify": ["body", "#main h1", "#main h2", "#header .logo .title", ".button"]
    },
    "source": {"repo": "zhenyoyo.github.io mirror docs/synthesis/phantom/_raw/site", "path": "assets/css/main.css:1-2,119-231"}
  },
  {
    "id": "token-set/type-scale",
    "kind": "token-set",
    "title": "Deployed type scale",
    "summary": "Rendered: body 16/18.67/21.33px (12/14/16pt bands ≤1280/≤1680/>1680), lh 1.75. h1 2.75em (44px @1280; 32px ≤736; 28px ≤360) w700 lh1.3. h2 1.1em (17.6px; 16px ≤736) 900 lh1.5. h3 1em (16px; 12.8px ≤736). h4 0.8em (12.8px). Buttons 0.8em w900 lh3.45em (0.6em small / 1em large). th 0.9em w900. code 0.9em (nested pre code 12.96px). copyright 0.8em lh1.",
    "aliases": ["type scale", "font size", "heading size", "body size", "px scale"],
    "body": {"group": "Type", "bands": {"<=1280": "12pt=16px", "<=1680": "14pt=18.67px", ">1680": "16pt=21.33px"}},
    "source": {"repo": "zhenyoyo.github.io mirror", "path": "assets/css/main.css:121-143,172-231,2404-2484,3215-3231"}
  },
  {
    "id": "token-set/tracking-and-case",
    "kind": "token-set",
    "title": "Case & tracking voice",
    "summary": "h1 sentence case, letter-spacing -0.035em (only tight voice). h2-h6, .logo wordmark, nav and buttons: text-transform uppercase + letter-spacing 0.35em + weight 900. Body, form labels, menu-overlay links and table heads carry no tracking and mixed case. Case is CSS-authored (source is mixed case).",
    "aliases": ["letter spacing", "tracking", "uppercase headings", "text transform"],
    "body": {"group": "Type", "values": {"h1": "sentence case, -0.035em", "h2-h6/logo/nav/buttons": "UPPERCASE, +0.35em, 900"}},
    "source": {"repo": "zhenyoyo.github.io mirror", "path": "assets/css/main.css:177,201-207,2476,2854,2913"}
  },
  {
    "id": "guideline/type-colour-per-page",
    "kind": "guideline",
    "title": "Type colour story — pink default, black by page override",
    "summary": "Deployed default: ALL type pink #ff6bbc (template grey replaced), links neon green #6bff2c with blue dotted underline. Page overrides: light/fafa/tame/Unlogical flip body to black via inline <style> leaving a project-shade h1 (#ff6bbc/#fd77af/#ff8b80/#71c3de); publication flips to black via .publication class; index/elements/generic/email stay fully pink. Tile titles on index are white over images.",
    "aliases": ["pink text", "black text page", "text colour", "link colour"],
    "body": {"group": "Type", "default": "pink #ff6bbc body+heads; green #6bff2c links", "overrides": ["light.html <style> body{color:rgb(0,0,0)}", "fafa/tame/Unlogical same pattern", ".publication{color:black} (main.css:3347)"]},
    "source": {"repo": "zhenyoyo.github.io mirror", "path": "assets/css/main.css (css-diff vs upstream), light.html/light <style>, fafa/tame/Unlogical <style>"}
  },
  {
    "id": "token-set/text-measure-and-leading",
    "kind": "token-set",
    "title": "Measure & leading",
    "summary": "Body leading 1.75 everywhere. Text column #wrapper .inner max-width 68em (1008px @1280 viewport, 1344px @1920, 350px @390; padding 2.5em/1.25em). At 16px Light the desktop line runs ≈150 characters (canvas estimate, avg char 6.65px) — an unusually long measure; mobile ≈53.",
    "aliases": ["measure", "line length", "line height", "column width"],
    "body": {"group": "Type", "leading": "1.75", "measure": {"@1280": "1008px ≈150ch", "@390": "350px ≈53ch"}},
    "source": {"repo": "zhenyoyo.github.io mirror", "path": "assets/css/main.css:126,3332-3345 (#wrapper > * > .inner)"}
  },
  {
    "id": "fallback/cjk-system-fallback",
    "kind": "fallback",
    "title": "CJK falls back to the OS (no CJK stack declared)",
    "summary": "The site declares no CJK font family; the wordmark's 圳 and any future CJK text fall through Source Sans Pro → Helvetica → OS sans-serif. In the extraction render the glyph resolved to WenQuanYi Zen Hei (system), weight/tracking mismatched to the SSP-Black Latin next to it. Rendering of 圳 therefore differs per visitor OS.",
    "aliases": ["Chinese", "CJK", "深圳", "fallback font", "missing glyph"],
    "body": {"group": "Type", "observed_fallback": "WenQuanYi Zen Hei (headless Linux render)", "declared": "none"},
    "source": {"repo": "zhenyoyo.github.io mirror", "path": "index.html wordmark span.title; CDP platform-font attribution"}
  },
  {
    "id": "fallback/synthetic-italic",
    "kind": "fallback",
    "title": "Italic is synthetic (no italic faces loaded)",
    "summary": "The Google-Fonts import requests normal style only (300,700,900); the captured Google CSS contains zero italic faces and the platform-font attribution for em/blockquote is the roman SourceSansPro-Light file. Italic emphasis (em, italic blockquote) therefore renders as browser-synthesised oblique.",
    "aliases": ["italic", "oblique", "em", "blockquote"],
    "body": {"group": "Type", "evidence": "postScriptName SourceSansPro-Light on em/blockquote; 0 italic @font-face in captured google.css"},
    "source": {"repo": "zhenyoyo.github.io mirror", "path": "assets/css/main.css:2,164-166,265-270"}
  }
]
```

## Flaw observations (measured; no fixes proposed)

1. **Pink body type on white ≈ 2.60:1** (#ff6bbc vs #ffffff, WCAG 2.x relative-luminance
   computation) — below AA for large text (3:1) and far below 4.5:1. It is the default body colour on
   index/elements/generic/email and the h2 colour on every page. Screens: type-index-1280.png,
   type-elements-1280.png, type-generic-1280.png.
2. **Link text #6bff2c on white ≈ 1.32:1** — the least readable text on the site; its dotted
   underline rgb(32,163,245) ≈ 2.76:1 is the only stronger cue. Pixel-sampled green
   (218,255,116)/(215,253,115) antialiasing in type-elements-1280.png / type-light-1280.png.
3. **Per-page h1 shades ≈ 1.99–2.60:1** (#71c3de 1.99, #ff8b80 2.27, #fd77af 2.49, #ff6bbc 2.60) —
   each fails 3:1. Screens: type-unlogical-1280.png, type-tame-1280.png, type-fafa-1280.png.
4. **Inline code: pink #ff6bbc on blue ground ≈ 2.01:1** (ground measures rgb(49,93,249) blended) —
   pink code text on blue fill (type-elements-1280.png; full-res pixel sample #315cf9 ground,
   border #c9c9c9).
5. **Small print rgba(88,88,88,0.5) ⇒ ≈ #acacac, 2.27:1 on white** (copyright line on 4 pages;
   invisible-on-grey at #f6f6f6 footer). type-generic-1280.png (footer read).
6. **Measure ≈150 characters/line @1280** for 16px Light text (1008px column; canvas estimate) —
   well past comfortable reading measure; ≈53 chars at 390.
7. **`pre` clips horizontally at mobile width** (element width 350px = viewport; content wider;
   overflow-x scroll) — lines truncated in view (type-elements-390.png).
8. **CJK/Latin mismatch in wordmark**: 圳 comes from a different family (OS fallback) than the
   SSP-Black Latin; visual reads of the crop disagree on how strongly the weight differs but agree
   the two families do not match (type-index-heading-1280.png, wordmark crop).
9. **Two competing heavy registers**: 900-mixed-case table heads next to 900-uppercase-tracked
   section heads; and the nav's authored "Menu" text is invisible (suppressed by text-indent trick,
   icon-only affordance).
10. **Unstyled placeholders**: form placeholder text keeps the UA default #757575 while real labels
    are purple #8833e3 — field text styling is inconsistent (OBSERVED-CSS).
11. light.html's `<style>` comment says "set background colour to black" while the deployed value is
    near-white rgb(251,251,251); the comment set is Chinese (OBSERVED in source; rendered result
    type-light-1280.png).

## Open questions

- `_raw/fonts/google.css` contains 300/400/700/900 faces (28 blocks) while the deployed import
  requests only 300,700,900 — the capture's exact request/UA is unclear; no 400 face was fetched by
  the pages as rendered.
- 圳 fallback on macOS/Windows visitors is INFERRED-as-OS-dependent (not measured here; this render
  used WenQuanYi Zen Hei).
- Is the pink/black split a per-project palette system or drift? (Extraction only — recorded, not
  judged. dom. A owns the colour values.)
- Italic synthesis is measured, but whether the original design intended italics at all (only
  em/blockquote/template copy use it) is unknown.
- h5/h6 tokens exist in CSS but render nowhere in the mirror; sub/sup defined but not sampled —
  treat scale as h1–h4 + body in practice.
