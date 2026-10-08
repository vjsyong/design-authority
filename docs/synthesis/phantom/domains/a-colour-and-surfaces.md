# Domain A · colour and surfaces — Phantom mirror (zhenyoyo.github.io)

Pass-2 redo. **Frame: what the deployed site IS.** Every value tagged `BASE` (template
value still live) vs `OVERRIDE` (deployment's own value). Pass-1's "grey ink is canon,
pink is a deviation" frame is NOT used; this report supersedes it for colour.

Evidence: rendered mirror served at `localhost:8734` (Chromium 129x via playwright);
screenshots `evidence/screens/colour-*.png`; probe dumps
`evidence/colour-probe-{index,elements,generic,publication,light,tame,fafa,Unlogical,email}.json`,
`evidence/colour-probe2-elements-index.json`, `evidence/colour-probe3-mobile.json`.
Tags: `OBSERVED-CSS` (computed style / in-page WCAG calc) · `OBSERVED-VISUAL`
(seen in a named screenshot) · `OBSERVED-PIXEL` (pixel histogram from a screenshot) ·
`INFERRED`/`DERIVED` (conclusion or ratio computed from measured values).

## 1. Summary (≤15 lines)

1. The deployed system's text ink is **pink `#ff6bbc` (rgb 255,107,188)** on almost every text role — body, h1–h4, p, header/logo, footer, table head+cells, input/select/textarea text, blockquote, carousel headings (OBSERVED-CSS; `colour-index-1280`, `colour-elements-1280`).
2. Content **links are neon green `#6bff2c`** with a **dotted blue `#20a3f5` underline**; hover turns the template's pink accent `#f2849e` (OBSERVED-CSS; visible on all project pages, e.g. `colour-light-1280`).
3. **Inline `code` / `pre > code` sit on a solid blue ground** `rgba(46,90,249,.986)` (≈ `#315df9`) with 1px `#c9c9c9` border; the code text is pink (OBSERVED-CSS + OBSERVED-PIXEL: pink antialiased pixels on blue, zero white text pixels).
4. The **slide-in menu is a 352px full-height neon-green rail `#3ef900` with black text** (14.76:1); its Close × is green `#6bff2c` drawn on the white page (1.32:1, effectively invisible) (OBSERVED-CSS + OBSERVED-PIXEL; `colour-*-1280-menu-open`).
5. Project pages (**light/tame/fafa/Unlogical**) share one identical per-page `<style>` block — body ground `#fbfbfb` + black text — and each carries its own **h1 accent** inline: `#ff6bbc` / `#ff8b80` / `#fd77af` / `#71c3de` (OVERRIDE; OBSERVED-CSS).
6. **publication** is the only page whose main text is black via CSS (`.publication{color:black}`); its header/footer stay pink (OBSERVED-CSS + `colour-publication-1280`).
7. Surfaces: white body / `#fbfbfb` project ground / `#f6f6f6` footer; table zebra + icon chrome `rgba(144,144,144,.075)` (BASE); near-transparent tile tints + an opaque pink **hover veil `#eb84da`**; the dark tile scrim is disabled (OVERRIDE).
8. Template BASE colours still live: buttons `#585858`/white (7.11:1), hover+focus pink `#f2849e`, borders `#c9c9c9`, copyright `rgba(88,88,88,.5)` (2.23:1).
9. Measured contrast of the signature ink: **pink 2.6:1 on white**, **green links 1.32:1** — the deployment runs its text below AA throughout (flaws §8; no fixes proposed in this pass).

## 2. Screenshots read (all 15, OBSERVED-VISUAL)

| file (evidence/screens/) | what it shows (colour-relevant) |
|---|---|
| `colour-index-1280.png` | White ground; ALL text pink (#ff6bbc) — welcome line, sections, captions, footer email; logo + hamburger dark; tiles are natural image colours; "Random Gallery" placeholder tile with thin grey border; light-grey footer band. No dark text anywhere. |
| `colour-elements-1280.png` | All pink type (body/headings/table/blockquote); small + large blue code boxes with pink-on-blue text; grey buttons (filled dark-grey = white text; outline = dark-grey text); checked radio/checkbox filled red with white tick; table zebra faint grey; labels purple; footer band light grey, footer headings pink. |
| `colour-generic-1280.png` | "About Zhen": pink heading + pink paragraph; footer "GET IN TOUCH"/"FOLLOW" pink on grey band; SEND button dark grey w/ white text; copyright light grey; header pink. |
| `colour-publication-1280.png` | Mixed: big h1 "Research publications…" black, body citations black; header "ABOUT ZHEN" + footer headings pink; links lime-green with dotted underlines; icons pink; SEND grey. |
| `colour-light-1280.png` | Off-white ground; title "I Light U Up" PINK; all sections/body black; links "Bilibili"/"SIGGRAPH ASIA 2024" lime green; Bilibili player card (white) embedded mid-page. |
| `colour-tame-1280.png` | Off-white ground; title "Tame" soft salmon-pink (#ff8b80); body charcoal; lime-green links; no solids/panels except imagery. |
| `colour-fafa-1280.png` | Off-white ground; title "FAFA" hot pink (#fd77af); body black; green links; large black diagram image (content, not surface); "BACK TO MAIN" black. |
| `colour-Unlogical-1280.png` | Off-white ground; title + [01]/[02] section headers LIGHT BLUE (#71c3de); body black; green links with dotted underline; a broken-image placeholder icon mid-page. |
| `colour-email-1280.png` | All pink: "ABOUT ZHEN" header, "Email contact~" h1, the email address itself (plain text, not a link); white ground; one large blurry image; no footer visible. |
| `colour-index-1280-menu-open.png` | Neon green rail (right side, 352px) with BLACK menu items (Home / About / Gallery / Publication / Game, Design & Development Log); the × close sits on the white page left of the rail and reads as a pale ghost; page behind shows pink text (reads washed-out). Pixel histogram: 312,939 px of `rgb(62,249,0)` (OBSERVED-PIXEL). |
| `colour-elements-1280-menu-open.png` | Same green panel + black text (stock lorem items: Ipsum veroeros / Tempus etiam / Consequat dolor / Elements); underlying page pink; the panel abuts the page cleanly. |
| `colour-light-1280-menu-open.png` | Green panel with stock lorem menu items; underlying page: black body, pink title; the green × close sits on the white page (measured `#6bff2c`, ~1.3:1 — reads as a ghost). |
| `colour-index-390.png` | Pink type at mobile; tiles stack in a single left column but the capture is **700 px wide** (document scrollWidth 700, OBSERVED-CSS) → wide white dead zone right of content; footer band grey w/ pink. |
| `colour-elements-390.png` | Pink type; blue code boxes; grey buttons; red checked fills; grey zebra; footer grey band. document scrollWidth 390 (fits) with one 398px `.fields` row. |
| `colour-light-390.png` | Title pink; body black; green links; capture is **820 px wide** (scrollWidth 820) due to 800px-wide iframe + `width:800px` inline images → large white overflow. |

## 3. Findings — ink / text colours

All rows OBSERVED-CSS (probe JSONs) unless noted; screenshot refs abbreviate `colour-<page>-1280.png`.

| value | role (what is painted with it) | pages | BASE/OVERRIDE | evidence · screenshot |
|---|---|---|---|---|
| `#ff6bbc` rgb(255,107,188) | body, h1–h4, p, header/logo, footer, table th+td, input/select/textarea text, blockquote, pre text, index h3 (carousel), captions, footer copyright aside | index, elements, generic, publication(header/footer/partial), email, + project pages (header only) | **OVERRIDE** (base `#585858`) | OBSERVED-CSS; `colour-index-1280`, `colour-elements-1280`, `colour-email-1280`, `colour-generic-1280` |
| `#6bff2c` rgb(107,255,44) | links in content (`a`), menu Close ×, footer icon links | all 9 | **OVERRIDE** (base `#585858`) | OBSERVED-CSS; `colour-light-1280` (Bilibili/SIGGRAPH), `colour-publication-1280` |
| `#20a3f5` rgb(32,163,245) | link underline — `border-bottom: dotted 1px` under every content link | all 9 | **OVERRIDE** (base `rgba(88,88,88,.5)`) | OBSERVED-CSS (`main-a` border-bottom-color on every page); dotted underline visible `colour-Unlogical-1280` |
| `#f2849e` rgb(242,132,158) | link **hover** text (`a:hover` rule), button hover ring, input focus underline + inset ring, checkbox/radio focus ring, `.icon.style2:hover` | all 9 (interaction only) | **BASE** (template accent, untouched) | OBSERVED-CSS: `a:hover{color:#f2849e!important}` stylesheet rule + focus probe `box-shadow rgb(242,132,158) 0 -1px 0 inset` |
| `#000000` | menu panel text (h2 + items, incl. email page's menu h2); project-page body text + headings; `#main` text on light/tame/fafa/Unlogical; publication `.publication` h1/p/strong | menu (all), light/tame/fafa/Unlogical, publication main | menu: **OVERRIDE** (base white on grey); project pages: **OVERRIDE** (per-page style block); publication: **OVERRIDE** (`.publication` rule) | OBSERVED-CSS; `colour-light-1280`, `colour-publication-1280`, `colour-index-1280-menu-open` |
| `#ffffff` | tile h2 + `.content p` (over imagery); button-primary + submit labels; checked-mark glyph; menu Close is NOT white (green) | index tiles; elements/generic/publication buttons | **BASE** | OBSERVED-CSS; `colour-index-1280` (white tile titles over images) |
| `#8833e3` rgb(136,51,227) | checkbox + radio **labels** (checked and unchecked) | elements (also any future consumer form) | **OVERRIDE** (base `#585858`) | OBSERVED-CSS; contrast 5.79:1 (measured) |
| `#f51616` fill / `#f82121` border | checked checkbox/radio fill; white check glyph | elements | **OVERRIDE** (base `#585858`) | OBSERVED-CSS (`#demo-copy`, `#demo-priority-low`); `colour-elements-1280` (red ticks) |
| `#585858` rgb(88,88,88) | button base: outline-button text + 2px inset ring; filled-button ground (white label); `hr` chrome | elements, generic, publication, email, index footer forms | **BASE** | OBSERVED-CSS; contrast 7.11:1 white-on-grey (measured) |
| `rgba(88,88,88,0.5)` | footer copyright "© Untitled…" / "la la la" | all 9 | **BASE** | OBSERVED-CSS (12.8px li); composite ≈ `rgb(167,167,167)` on `#f6f6f6` → 2.23:1 (derived) |
| `#c9c9c9` rgb(201,201,201) | borders: field underline, icon squares, code border, table.alt rules | all 9 | **BASE** | OBSERVED-CSS |
| `#808080` rgb(128,128,128) | `hr` element colour (computed `color`; visible rule is its bottom border `#c9c9c9`) | elements | BASE (UA/inherited) | OBSERVED-CSS |

## 4. Findings — surfaces, tints, panels

| value | role | pages | BASE/OVERRIDE | evidence · screenshot |
|---|---|---|---|---|
| `#ffffff` | page ground (body) | index, elements, generic, publication, email | **BASE** | OBSERVED-CSS; `colour-index-1280` |
| `#fbfbfb` rgb(251,251,251) | project-page ground (per-page `<style>` block, identical on all four) | light, tame, fafa, Unlogical | **OVERRIDE** (added) | OBSERVED-CSS; `colour-light-1280` off-white vs white |
| `#f6f6f6` rgb(246,246,246) | footer band ground | all 9 | **BASE** | OBSERVED-CSS; visible `colour-generic-1280`, `colour-index-1280` |
| `#3ef900` rgb(62,249,0) | menu rail ground (352×900 right-side panel shown when `body.is-menu-visible`) | all 9 | **OVERRIDE** (base `#585858` panel) | OBSERVED-CSS + menu-open probes + OBSERVED-PIXEL; `colour-index-1280-menu-open`, `colour-elements-1280-menu-open` |
| `rgba(46,90,249,.986)` → composite `#315df9` | `code` ground (inline + `pre`); 1px `#c9c9c9` border; radius 4px | elements (code demos); any `code` moment | **OVERRIDE** (base `rgba(144,144,144,.075)`) | OBSERVED-CSS + OBSERVED-PIXEL (blue histogram 2926px inline box; 224,498px pre block; pink text pixels only) |
| `#eb84da` rgb(235,132,218), opacity 1 | tile **hover veil** (`article:hover > .image::before`) — flat pink wash over the photo | index | **OVERRIDE** (hover-after was `#333333`/0.35) | OBSERVED-CSS hover probe; seen on `comp-index-tile-hover` (domain C) & live hover |
| `rgba(116,111,250,0.157)`, `rgba(255,226,229,0.14)`, `rgba(255,226,229,0)` | resting tile tints style3 / style6 / style2 (style1 `#efc5e900` = invisible) — near-transparent ghosts of the base pastels | index tiles | **OVERRIDE** (base pastels were `#f2849e/#7ecaf6/#7bd0c1/…`) | OBSERVED-CSS pseudo probes (`style2`, `style3`, `style6` matched on index) |
| `rgba(0,0,0,0)` + opacity 0 | `.tiles article > .image::after` dark scrim — **disabled on hover** (opacity 0); dark scrim never visible in deployment (base `#333333`/0.35) | index | **OVERRIDE** | OBSERVED-CSS pseudo probe |
| `rgba(144,144,144,0.075)` | table zebra rows (`tbody tr` odd) | elements (both tables) | **BASE** | OBSERVED-CSS; faint grey striping `colour-elements-1280` |
| `rgba(255,255,255,0.5)` | header menu-button (`a[href="#menu"]`) background — invisible-on-white pill | subpages (elements at least; selector global) | **BASE** | OBSERVED-CSS path `div.inner > nav > ul > li > a` TEXT=Menu |
| `rgba(255,255,255,0.15)` | `#menu` list-item separators (`border-top`) — 1px light lines on the green panel (composite ≈ `rgb(91,250,38)`) | all 9 | **BASE** | OBSERVED-CSS; visible as faint rules in menu-open shots |
| Bilibili player card (white, third-party chrome) | video embeds on project pages, fixed 800×450; on index: **none** | light, tame, fafa, Unlogical (index: 0) | external | OBSERVED-CSS (no iframe/video on index; iframe 800px on light); `colour-light-1280` |

## 5. Findings — accents per page (the override story)

| page | body ink | ground | h1 | other accents | tag |
|---|---|---|---|---|---|
| index | pink `#ff6bbc` | white | pink `#ff6bbc` | footer pink; tiles white-on-image; copyright grey 50% | OVERRIDE (global) |
| elements | pink | white | pink | code blue; links green; labels purple; checks red; buttons grey | OVERRIDE + BASE remainder |
| generic | pink | white | pink | footer form grey buttons | OVERRIDE |
| publication | pink (header/footer) + **black** `.publication` main | white | **black** `#000` | links green + blue dotted | OVERRIDE (`.publication{color:black}`) |
| light | **black** | `#fbfbfb` | **pink `#ff6bbc`** (inline) | links green; iframe 800px | OVERRIDE (per-page style + inline) |
| tame | black | `#fbfbfb` | **coral `#ff8b80`** (inline) | links green | OVERRIDE |
| fafa | black | `#fbfbfb` | **pink-crimson `#fd77af`** (inline) | links green | OVERRIDE |
| Unlogical | black | `#fbfbfb` | **light blue `#71c3de`** (inline; + 2× h2) | links green + dotted blue | OVERRIDE |
| email | pink | white | pink | email address plain pink text (no link) | OVERRIDE |

The per-page `<style>` block is byte-identical on light/tame/fafa/Unlogical (verified by
source diff of the four blocks) and its Chinese comments say "设置背景颜色为黑色" (set
background black) / "将文本颜色设置为白色" (set text white) while the values are
`background rgb(251,251,251)` / `color rgb(0,0,0)` — comment/value mismatch, recorded as-is.

## 6. Contrast measurements (WCAG 2.x, from OBSERVED-CSS values; ratio in-page or derived)

| foreground | background | ratio | note |
|---|---|---|---|
| black `#000` | menu green `#3ef900` | **14.76** | menu items — passes AA/AAA |
| black `#000` | `#fbfbfb` | **20.29** | project-page body — passes |
| white | button grey `#585858` | **7.11** | buttons — passes |
| purple `#8833e3` | white | **5.79** | form labels — passes AA |
| white glyph | checked red `#f51616` | **4.19** | check mark (large glyph); derived |
| pink `#ff6bbc` | white | **2.60** | all body/heading text on index/elements/generic/email — fails AA |
| pink `#ff6bbc` | `#f6f6f6` | **2.40** | footer text |
| pink `#ff6bbc` | `#fbfbfb` | **2.51** | light.html h1 |
| coral `#ff8b80` | `#fbfbfb` | **2.19** | tame h1 |
| pink-crimson `#fd77af` | `#fbfbfb` | **2.41** | fafa h1 |
| light blue `#71c3de` | `#fbfbfb` | **1.92** | Unlogical h1/h2 |
| green `#6bff2c` | white | **1.32** | links |
| green `#6bff2c` | `#fbfbfb` | **1.27** | links on project pages |
| pink `#ff6bbc` | code blue composite `rgb(49,93,249)` | **1.99** | code text on its blue ground; derived |
| green `#6bff2c` (close ×) | white page ground | **1.32** | close × beside menu rail; derived (1.08 if it sat on the panel) |
| white | tile hover veil `#eb84da` | **2.37** | white tile text against hover veil; derived |
| copyright composite `rgb(167,167,167)` | `#f6f6f6` | **2.23** | "la la la" line; derived |

Method: ratios recomputed with the WCAG 2.x relative-luminance formula from computed
values; `rgb(49,93,249)` = `rgba(46,90,249,.986)` composited over white (alpha .984);
copyright = `rgba(88,88,88,.5)` over `#f6f6f6`. Tile text sits over photography — no
solid background exists for those; the white-1.0 row in probe JSONs is an artifact of the
ancestor walk and is NOT a real ratio (flagged).

## 7. Proposed pack entries

One fenced JSON object per proposal. `source.path` cites the mirror + probe evidence.
Entries 1–2 revise pass-1 `token-set/colour`; the rest are new for this redo.

```json
{
  "id": "token-set/colour",
  "kind": "token-set",
  "title": "Colour — deployed ink system (pink type, neon link, blue code)",
  "summary": "What the deployment actually paints: body/heading/footer/table/form-text ink pink #ff6bbc (OVERRIDE of template #585858); content links neon green #6bff2c with dotted blue #20a3f5 underline (OVERRIDE); code ink pink on solid blue rgba(46,90,249,.986) ground (OVERRIDE); project pages switch body ink to black; menu panel lime #3ef900 with black text (OVERRIDE). Template accent pink #f2849e survives as the hover/focus ink (BASE).",
  "aliases": ["colour", "color", "palette", "ink", "pink ink", "neon"],
  "body": {
    "group": "Foundations",
    "tokens": [
      "text ink (deployed): #ff6bbc rgb(255,107,188) — body,h1-h4,p,header,footer,th/td,field text,blockquote,pre",
      "link ink: #6bff2c; link underline: #20a3f5 dotted 1px; hover ink/focus ring: #f2849e (BASE)",
      "code ground: rgba(46,90,249,.986) ≈ #315df9 on white; border 1px #c9c9c9",
      "menu panel: ground #3ef900, ink #000",
      "grounds: #ffffff (white pages) / #fbfbfb (project pages, per-page style) / #f6f6f6 footer",
      "controls: labels #8833e3; checked fill #f51616 / border #f82121; buttons #585858 + white",
      "per-page h1 accents: #ff6bbc, #ff8b80, #fd77af, #71c3de (inline styles)"
    ],
    "contrast": "pink-on-white 2.6:1; green-on-white 1.32:1; pink-on-code-blue 1.99:1 — measured; black-on-menu-green 14.76:1",
    "verify": ["body", "a", "code", "#menu", "h1"]
  },
  "source": {
    "repo": "zhenyoyo.github.io (deployed HTML5 UP Phantom deploy)",
    "path": "docs/synthesis/phantom/evidence/colour-probe-*.json; _raw/site/assets/css/main.css L122/151-2/273/3005"
  }
}
```

```json
{
  "id": "token-set/surfaces",
  "kind": "token-set",
  "title": "Surfaces — grounds, tints, scrims, panels",
  "summary": "Grounds: white #ffffff (default), #fbfbfb (project pages via per-page style block), footer band #f6f6f6. Panels: menu overlay #3ef900. Tints: table zebra rgba(144,144,144,.075) (BASE); tile resting tints collapsed to near-transparent (#746ffa28, #ffe2e524, #ffe2e500, #efc5e900). Scrims: the dark tile scrim #333333/.35 is disabled — hover instead paints an opaque pink veil #eb84da over the image (::before opacity 1; ::after opacity 0). Chrome lines: #c9c9c9 borders, menu separators rgba(255,255,255,.15) on green.",
  "aliases": ["surfaces", "backgrounds", "grounds", "tints", "panel", "overlay"],
  "body": {
    "group": "Foundations",
    "tokens": [
      "grounds: #ffffff / #fbfbfb / #f6f6f6",
      "menu panel: #3ef900; separators rgba(255,255,255,.15); header menu-button pill rgba(255,255,255,.5) (invisible on white)",
      "code ground: rgba(46,90,249,.986)",
      "tiles: hover veil #eb84da rgba(235,132,218,1); resting tints rgba(116,111,250,.157) / rgba(255,226,229,.14) / transparent",
      "zebra: rgba(144,144,144,.075); borders: #c9c9c9"
    ],
    "verify": [".tiles article", "#menu", "code", "table tbody tr", "#footer"]
  },
  "source": {
    "repo": "zhenyoyo.github.io (deployed HTML5 UP Phantom deploy)",
    "path": "docs/synthesis/phantom/evidence/colour-probe-*.json; _raw/site/assets/css/main.css L2692-2760 (tiles), L3005 (#menu)"
  }
}
```

```json
{
  "id": "rule/link-treatment",
  "kind": "rule",
  "title": "Links carry three colours at once (green text, blue dotted underline, pink hover)",
  "summary": "A content link is painted #6bff2c, underlined with a dotted 1px #20a3f5 border, and turns #f2849e on hover (border-bottom:transparent). The underline is what makes green-on-white findable; the hover colour is the template's pink accent, unchanged. Recorded from measured stylesheet rules and computed styles on all pages.",
  "aliases": ["link colour", "link style", "underline", "hover colour"],
  "body": {
    "group": "Rules",
    "statement": "a { color:#6bff2c; border-bottom: dotted 1px rgba(32,163,245,.999) } a:hover { color:#f2849e !important; border-bottom-color: transparent }",
    "verify": ["#main p a", "a:hover rule"]
  },
  "source": {
    "repo": "zhenyoyo.github.io (deployed HTML5 UP Phantom deploy)",
    "path": "docs/synthesis/phantom/evidence/colour-probe-*.json (main-a rows); _raw/site/assets/css/main.css L151-2 + hover rule"
  }
}
```

```json
{
  "id": "rule/per-page-override-pattern",
  "kind": "rule",
  "title": "Per-page colour overrides (black-body project pages + title accent + .publication)",
  "summary": "Four project pages (light, tame, fafa, Unlogical) inject one identical <style> block — body{background:#fbfbfb; color:#000} — and then colour only their h1 via inline style (light #ff6bbc, tame #ff8b80, fafa #fd77af, Unlogical #71c3de, also applied to its h2 section markers). publication.html instead adds class .publication (main.css) painting its main text black while header/footer stay pink. This is the deployment's override mechanism: global pink ink, locally overridden per page.",
  "aliases": ["override", "per-page style", "black body", "title colour"],
  "body": {
    "group": "Rules",
    "statement": "Global ink #ff6bbc; project pages flip to black body on #fbfbfb (shared style block) + one inline h1 accent; publication keeps pink shell but black .publication main text.",
    "verify": ["body", "h1", ".publication"]
  },
  "source": {
    "repo": "zhenyoyo.github.io (deployed HTML5 UP Phantom deploy)",
    "path": "docs/synthesis/phantom/evidence/colour-probe-light|tame|fafa|Unlogical|publication.json; inline <style> blocks in _raw/site/*.html"
  }
}
```

```json
{
  "id": "rule/template-remainder",
  "kind": "rule",
  "title": "Template remainder — which base colours stay live",
  "summary": "Colours the deployment left untouched and that remain the system's interaction/chrome layer: hover & focus pink #f2849e (link hover, input focus underline+ring, button hover ring, icon hover), buttons #585858 (filled + outline), field underline & borders #c9c9c9, table zebra rgba(144,144,144,.075), footer ground #f6f6f6, copyright rgba(88,88,88,.5). Consumers restoring 'hover affordance' or 'form chrome' from this site are actually reading BASE values.",
  "aliases": ["template", "base layer", "hover pink", "form chrome"],
  "body": {
    "group": "Rules",
    "statement": "Base values still live: #f2849e (hover/focus), #585858 (buttons), #c9c9c9 (lines), rgba(144,144,144,.075) (zebra), #f6f6f6 (footer), rgba(88,88,88,.5) (copyright).",
    "verify": ["a:hover", "input:focus", "input[type=submit]", "#footer"]
  },
  "source": {
    "repo": "HTML5 UP Phantom (base) as left live by zhenyoyo.github.io",
    "path": "docs/synthesis/phantom/evidence/colour-probe2-elements-index.json; _raw/site/assets/css/main.css Button/Form blocks"
  }
}
```

```json
{
  "id": "prohibition/unreadable-accent-ink",
  "kind": "prohibition",
  "title": "Accent ink on light grounds — measured guard",
  "summary": "Measured in the deployment (and left in place — extraction, not correction): pink #ff6bbc text on white = 2.6:1; green #6bff2c links on white = 1.32:1; pink code ink on blue #315df9 = 1.99:1; the Close × (#6bff2c on the white page) = 1.32:1; project-page h1 accents 1.92–2.51:1; copyright 2.23:1. As a reusable-system statement: accent inks must not be the only readable signal on grounds where measured contrast < 3:1 — pair with another affordance (the dotted underline does this for links; nothing does it for body text or the Close ×).",
  "aliases": ["contrast", "neon text", "readability", "accessibility"],
  "body": {
    "group": "Prohibitions",
    "statement": "Do not rely on accent ink alone below 3:1; measurements above record where the deployment currently does.",
    "measurements": ["pink/white 2.60", "green/white 1.32", "pink/code-blue 1.99", "close-×/white 1.32 (1.08 if over the lime panel)"]
  },
  "source": {
    "repo": "zhenyoyo.github.io (deployed HTML5 UP Phantom deploy)",
    "path": "docs/synthesis/phantom/domains/a-colour-and-surfaces.md §6 (contrast table)"
  }
}
```

```json
{
  "id": "candidate/text-as-accent",
  "kind": "candidate",
  "title": "Text-as-accent (pink ink identity)",
  "summary": "The deployment's real design decision: text itself carries the accent colour (pink family) across every text role, with per-page h1 hues and a neon link. Pass-1 filed the pink affinity as candidate/pink-accent-system; this redo sharpens it to 'text as the accent surface'. Promote when: a role map exists (which roles may be pink vs black — the deployment already flips body text to black on project pages), an AA strategy is chosen (size/weight minimums or a dark-ground variant), and the owner signs off.",
  "aliases": ["pink accent", "neon text", "text colour identity"],
  "body": {
    "group": "Candidates",
    "promote_when": ["single role map (pink vs black per role)", "AA strategy documented", "owner sign-off"],
    "evidence": "pink #ff6bbc on body/headings/footer/forms; black fallback already used on 4 project pages; per-page h1 hues #ff6bbc/#ff8b80/#fd77af/#71c3de"
  },
  "source": {
    "repo": "zhenyoyo.github.io (deployed HTML5 UP Phantom deploy)",
    "path": "docs/synthesis/phantom/domains/a-colour-and-surfaces.md §1-§5; evidence/colour-probe-*.json"
  }
}
```

```json
{
  "id": "fallback/no-dark-ground",
  "kind": "fallback",
  "title": "No dark surfaces exist",
  "summary": "The deployment ships no dark ground anywhere (menu panel went lime, not black; the tile dark scrim is disabled, opacity 0). If a dark surface is unavoidable (video overlay, modal), no canon role mapping exists — keep the white-text/base roles, mark the improvisation, and report a gap if it recurs.",
  "aliases": ["dark mode", "dark surface", "overlay"],
  "body": {
    "group": "Fallbacks",
    "statement": "No dark-surface canon; if unavoidable, keep base roles and mark the improvisation.",
    "verify": ["#menu", ".tiles article > .image"]
  },
  "source": {
    "repo": "zhenyoyo.github.io (deployed HTML5 UP Phantom deploy)",
    "path": "docs/synthesis/phantom/evidence/colour-probe-index.json (.tiles ::after opacity 0; #menu #3ef900)"
  }
}
```

## 8. Flaw observations (measured — gap ledger material, not fixes)

1. **AA failure everywhere pink runs**: pink ink `#ff6bbc` on white = **2.6:1**
   (index/elements/generic/email body). The single most-loaded colour on the site fails
   AA for all text sizes (measured).
2. **Neon green links fail catastrophically**: `#6bff2c` on white **1.32:1**, on `#fbfbfb`
   **1.27:1** (measured; only the dotted blue underline distinguishes them).
3. **Code text vs its ground**: pink `#ff6bbc` on composited blue `rgb(49,93,249)` =
   **1.99:1** (derived from measured values; pixel histogram confirms pink text on blue).
4. **Menu Close × nearly invisible**: measured geometry: panel = 352×900 rail at x=928;
   close × = 96×48 at x=832 — i.e. drawn on the **white page ground**, ink `#6bff2c` →
   **1.32:1** (derived; menu-open screenshots show it reading as a ghost × beside the
   panel). If it ever sat on the panel `#3ef900` the pair would be 1.08:1 (derived).
5. **Per-page h1 accents all under 3:1**: light 2.51, tame 2.19, fafa 2.41, Unlogical 1.92
   on `#fbfbfb` (measured). Unlogical additionally paints `[01]/[02]` h2s in the same blue.
6. **Copyright line**: `rgba(88,88,88,.5)` (12.8px) → composite `rgb(167,167,167)` on
   `#f6f6f6` = **2.23:1** (derived). Vision reads "la la la" as near-invisible
   (`colour-index-390.png`).
7. **Tile hover veil vs white tile text**: white on `#eb84da` = **2.37:1** (derived);
   the tile title `.content` only becomes visible on this veil (opacity 0 → 1 measured).
8. **Dark-scrim removal**: tile `.image::after` opacity 0 (scrim `#333333/.35` disabled);
   the hover state replaces a photo-darkening scrim with an opaque pink veil — text
   legibility now depends on the veil's hue (measured).
9. **Mobile horizontal overflow**: at 390px `document.scrollWidth` = **700** (index; inline
   `width:700px` img) and **820** (light; 800px iframe + `width:800px` inline images) —
   colour-relevant because the overflow exposes large empty white canvas in full-page
   captures (`colour-index-390.png` 700px wide, `colour-light-390.png` 820px wide;
   OBSERVED-CSS probe). elements fits (390).
10. **Comment/value mismatch (craft, colour-adjacent)**: the four project pages' identical
    `<style>` block comments say black background / white text but set `#fbfbfb` bg +
    `#000` text (source + measured).
11. **Small pink text at 13px** on index ("Zhen is currently a PhD candidate…" — measured
    13px pink) is the hardest-reading instance of the ink system on mobile
    (`colour-index-390.png`).

## 9. Open questions

1. Is the pink family intentional? Three different pinks coexist: global ink `#ff6bbc`,
   template accent `#f2849e` (hover/focus), per-page `#fd77af` — deliberate gradient of
   "pinks" or drift? (Same for green link `#6bff2c` vs underline blue `#20a3f5` vs code
   blue `#2e5af9`.)
2. Is the menu Close × near-invisibility intended? Measured: the close anchor renders `#6bff2c`
   (it inherits the recoloured global link green) and sits left of the rail on the white
   page — 1.32:1 there, 1.08:1 against the panel it belongs to. Did the panel recolour
   (`#585858`→`#3ef900`) intend to keep the close white (base: white × on grey)?
3. Was `.publication{color:black}` the model for the project pages' black-body treatment,
   or the other way around? The four project-page style blocks are identical — copy-paste
   chain?
4. Who owns "neon set" naming: `#ff6bbc` (pink), `#6bff2c` (green), `#3ef900` (panel
   lime), `#2e5af9` (code blue), `#f51616` (check red), `#8833e3` (label purple) — six
   saturated hues with no shared construction. Is there a rule for which hue earns which
   role, or is each an independent improvisation?
5. Should `prohibition/unreadable-accent-ink` supersede pass-1 `prohibit/neon-text`
   (which banned the whole approach rather than the measured pairings)?
6. The `rgba(255,255,255,0.5)` header menu-button pill and `rgba(255,255,255,0.15)` menu
   separators are BASE values designed for the grey panel; on the new grounds they render
   invisible/near-invisible — keep, or flag as missed in the recolour?
