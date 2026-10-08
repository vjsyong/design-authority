# D · layout · pages · motion — phantom redo extraction

Team D, pass 2 (screenshot-first). Sources: rendered mirror `_raw/site` served at
127.0.0.1:8747, captured with Playwright (Chromium) 2026-10-08. Screenshots:
`docs/synthesis/phantom/evidence/screens/layout-*.png` (18 files; all read with
vision + DOM/CSS probes). Tag key: `OBSERVED-CSS` = computed-style/geometry
measured in the browser; `OBSERVED-DOM` = DOM/source/log fact; `OBSERVED-VISUAL`
= seen in a cited screenshot; `INFERRED` = conclusion. BASE/OVERRIDE compared
against `_raw/upstream` (template substrate).

## Summary

- One shell, nine pages: `#wrapper > header#header` (static, 8em top pad; logo
  left; fixed 64×48 translucent "Menu" pill top-right) → `nav#menu` (fixed
  slide-in; 22em @1280, 16.5em @≤736) → `#main > .inner` (68em container,
  2.5em gutters) → optional `footer#footer` (grey `#f6f6f6`). Shell is BASE.
- Footer is rendered on only **4 of 9 pages** (index, elements, generic,
  publication); commented out wholesale on light/tame/fafa/Unlogical; absent on
  email. index replaces the template footer with custom contact + icons ("la la
  la" copyright).
- Two competing menus: "site" set (Home/About/Gallery/Publication/Game, Design
  & Development Log) on index + publication; stock lorem set (Ipsum veroeros/
  Tempus etiam/Consequat dolor/Elements) on the other 7 pages. Wordmarks come in
  4 variants; titles in 9 different strings.
- index carries structural damage: a nested `<!DOCTYPE html><html><head>…`
  block mid-`<body>` (parses to 2 invisible metas + a `<title>Document</title>`
  absorbed into `<header>`; renders as blank line), a **duplicated `id="main"`**
  (outer + nested), a stray `</h1>`, commented-out headings, and
  `span.image.main` wrappers around whole sections.
- Motion: the only sanctioned motion is load-in — `body.is-preload` gates all
  animation and holds `.tiles article` at scale(.9)/opacity 0; main.js removes
  the class 100 ms after `window.load`; tiles run transform+opacity 0.5 s ease
  (measured ramp 0.22→0.99 over ~350 ms, settled ≈830 ms after nav start).
  **Header/wrapper do NOT animate** (header opacity 1 during preload; no
  `#wrapper` fade rule exists in deployed or upstream CSS).
- Carousel: hand-rolled autoplay (`setInterval(showNext, 4000)`, no controls),
  640×360 inline-fixed image, instant DOM swap; **all 6 `randomgallery/*`
  sources 404** — both captured states show the broken-image placeholder.
- Mobile: pages render at 390 but documents reach 700–1020 px scrollWidth
  (horizontal overflow 310–630 px) on index/light/tame/fafa/Unlogical, from
  hard-coded inline px widths (640/700/800/900/1000 px images, 800 px iframes).
- WIP sweep: 8 referenced assets 404 (6 carousel + `tame/emotion map.jpg` +
  `unlogical/BOOKLET-01 - Copy.jpg`); mp4 source is a 133-byte git-LFS pointer;
  no favicon/OG/description anywhere; `alt=""` almost everywhere; per-page
  inline styles 6–22 per project page + one shared `<style>` block on 4 pages.

---

## 1 · Shell architecture (BASE/OVERRIDE)

| Slot | What it is (measured) | BASE/OVERRIDE | Evidence | Screenshot |
|---|---|---|---|---|
| container | `#wrapper > * > .inner { width:100%; max-width:68em; margin:0 auto; padding:0 2.5em }` (1.25em ≤736) — measured content 1008px @1280, 350px @390 | BASE | OBSERVED-CSS (main.css L3330-3341; probes) | all |
| header | `#header { padding: 8em 0 0.1em }` (4em ≤736), static; measured height 202 @1280 / 138 @390 | BASE | OBSERVED-CSS (L2845-2847, L2964) | layout-index-1280/390 |
| logo | `a.logo` → `.symbol img` (logo.svg, 2em×2em) + `.title` tracked-caps wordmark (letter-spacing .35em, uppercase, 900) | BASE | OBSERVED-CSS (L2857-2874) | layout-index-1280 |
| menu control | single `a[href="#menu"]` label "Menu", `position:fixed; right:2em; top:2em` (.5em ≤736); 64×48 px box, `text-indent:64px; overflow:hidden`, translucent white bg `rgba(255,255,255,.5)`, **radius 4px kept** (not flattened); hamburger lines drawn by `::before/::after` (64×48 pseudo boxes) | BASE | OBSERVED-CSS (L2876-2879, L2909, L2917+; probe rect x=1184,y=32 @1280; x=318,y=8 @390) | layout-index-1280/390 |
| slide menu | `nav#menu`: fixed right panel, `transform:translateX(22em)` hidden → 0 visible; width 22em @1280, **16.5em ≤736** (measured 352 / 264 px); ground `#3ef900` (OVERRIDE) / ink; `#menu > .inner > ul` links with 1px rules; close button `position .5em / left -4.25em` ≤736 (sits LEFT of panel — seen at x≈58 @390); JS moves `#menu` to `<body>` and wraps `.inner`; `body.is-menu-visible #wrapper { opacity:.25 }` dims the page | composition BASE · colours OVERRIDE | OBSERVED-CSS (L2989-3163; probe: w=264, bg rgb(62,249,0), transform identity when open) | layout-index-menu-open-390, layout-elements-1280 |
| main | `div#main` `padding: 0 0 6em` (4em ≤736); index **duplicates this id** (see §5) | BASE | OBSERVED-CSS (L3166-3174); DOM count | layout-index-1280 |
| footer | `footer#footer { padding:5em 0 6em; background:#f6f6f6 }`; `> .inner` flex-wrap row; section 1 (contact, ~66%) + section 2 (Follow icons, ~33%) + full-width `.copyright` bar | BASE | OBSERVED-CSS (L3179-3236) | layout-index-1280, layout-generic-1280 |

Per-page footer presence (rendered): index ✓ custom · elements ✓ template ·
generic ✓ template · publication ✓ template · light ✗ (commented out, source
L164-202) · tame ✗ · fafa ✗ · Unlogical ✗ · email ✗ (no footer markup at all).
`#footer` section h2s and copyright rows are empty on all 5 footerless pages
(DOM probe), so project pages visually end after the last gallery image
(OBSERVED-VISUAL, layout-light-1280 — "content ends after the final dictionary
image", no footer).

## 2 · Per-page structure table

docH = full-page document height px (Playwright). Menu sets: **S** = site menu,
**L** = stock lorem menu. Overflow = document scrollWidth @390 vs 390 viewport.

| page | `<title>` | wordmark | menu | footer | h1 (colour) | sections | docH@390 | docH@1280 | mobile overflow | screenshots |
|---|---|---|---|---|---|---|---|---|---|---|
| index | `Zhen Wu Yoyo` | `Zhen Wu YoYo 圳` | S | custom ("la la la") | ` Projects` (pink #ff6bbc) | intro header + carousel + 3 `.tiles` sets (8 articles) + collage | 5103 | 3587 | **700** (webcollage 700px, carousel img 640px) | layout-index-390/1280 |
| elements | `Elements - Phantom by HTML5 UP` | `Phantom` | L | template (© Untitled) | `Elements` (pink) | 6 sections (Text/Lists/Actions/Table/Form/Image) | 9312 | 7049 | none | layout-elements-390/1280 |
| generic | `About Zhen` | `About Zhen` | L | template | `About Zhen` (pink) | About bio + pic13 hero | 1526 | 1414 | none | layout-generic-390/1280 |
| publication | `Zhen's publication</S>` (broken tag) | `About Zhen` | S | template | `Research publications from Yoyo` (**black** via `.publication`) | 10 citations (5+5) in 12 `.publication` paragraphs | 3189 | 2021 | none | layout-publication-390/1280 |
| light | `ILightUUP` | `Back to main` | L | **commented out** | `I Light U Up` (inline `#ff6bbc`) | hero + FAFA blurb + video + 2×"Publication and Exhibition" + Concept + Gallery (12 imgs) | 7012 | 7931 | **820** (800px img/iframe) | layout-light-390/1280 |
| tame | `Tame` | `Back to main` | L | **commented out** | `Tame` (inline `#ff8b80`) | video + Concept + Gallery (11 imgs) | 6702 | — | **920** (900px img) | layout-tame-390 |
| fafa | `FAFA` | `Back to main` | L | **commented out** | `FAFA` (inline `#fd77af`) | video + Concept + Publication + Gallery (6 content imgs) | 5028 | — | **920** | layout-fafa-390 |
| Unlogical | `Unlogical Instrument` | `Back to main` | L | **commented out** | `Unlogical Instrument` (inline `#71c3de`) | 3 bilibili embeds + [01]/[02] sections (9 content imgs) | 6184 | — | **1020** (1000px img) | layout-unlogical-390 |
| email | `Zhen's email` | `About Zhen` | L | **none in markup** | `Email contact~` + `zwuch@connect.ust.hk` (pink ×2) | pic13 hero only | 844 | — | none | layout-email-390 |

All 390 widths are 390×844 viewport with `full_page=True`; file widths differ
where the document overflows (index 700, light 820, tame/fafa 920, unlogical
1020 — PNG confirmed with PIL). 1280 captures are 1280×900 viewport.

## 3 · Layout-component findings

| # | Component / behaviour | Value / fact | BASE/OVERRIDE | Evidence | Screenshot ref |
|---|---|---|---|---|---|
| 3.1 | index header block content | `<header>` holds the nested-doctype wreckage + 3 `<p>` intro lines; all `<h2>` headings are commented out; the block renders as blank line + 3 pink lines | OVERRIDE | OBSERVED-DOM (innerHTML probe; source L54-74) | layout-index-nesteddoctype-1280 |
| 3.2 | duplicated `id="main"` | 2 elements with `id="main"` on index (outer rect 1280×2572; nested 1008×570 @1280; 390×4131 + 350×527 @390); other 8 pages: 1 | OVERRIDE (artifact) | OBSERVED-CSS (probe) | layout-index-1280 |
| 3.3 | `span.image.main` as section wrapper | index: 2 wrappers (1008×1715 around the Artwork/Tools/Probe block; 1280×422 around the collage). Project pages: 5–9 wrappers incl. 0px/20px-high empty ones | OVERRIDE | OBSERVED-CSS (clientHeight probes) | layout-index-1280, layout-light-1280 |
| 3.4 | index tile grid | 3 sections `.tiles` with 6+1+1 articles (=8); 3-up @1280, 1-up @390 (measured tile width 350 = container) | BASE | OBSERVED-CSS + OBSERVED-VISUAL | layout-index-1280/390 |
| 3.5 | index carousel region | `#carouselGallery` inline `position:relative;max-width:1200px;margin:auto`; one `.carousel-item` per tick: `img` inline 640×360 `object-fit:cover` + `h3` + empty `p`; rect 1008×402 @1280 | OVERRIDE | OBSERVED-DOM + OBSERVED-CSS | layout-carousel-state1/2-1280 |
| 3.6 | project-page freeform layout | h1 → `span.image.main` hero → text; then h2 sections; Gallery images alternate `float:left/right` via `.image1:nth-child(odd/even)` (70% width, 60px margin) from the shared per-page `<style>` | OVERRIDE | OBSERVED-DOM (source L55-100 etc.) + OBSERVED-CSS (img rects) | layout-light-390/1280, layout-fafa-390 |
| 3.7 | fixed pixel widths | project-page inline widths 200/300/400/500/600/800/900/1000 px (index collage 700 px; carousel img 640 px) — these are the overflow source at 390 | OVERRIDE | OBSERVED-CSS (probe: light imgs right=820; collage right=700) | layout-light-390, layout-index-390 |
| 3.8 | project-page shared `<style>` | four pages carry the identical block: `body{background:rgb(251,251,251); color:rgb(0,0,0)}` + `.image1{width:70%;margin:60px}` floats + `img{width:100%;height:100%}` — the style's own comment says "背景颜色为黑色" (black) while the value is near-white | OVERRIDE | OBSERVED-DOM (byte-identical blocks) | layout-light-1280 |
| 3.9 | email page | minimal: h1 "Email contact~" + pic13 + h1 address; no footer, no sections; docH 844 = viewport height | OVERRIDE | OBSERVED-DOM (source) | layout-email-390 |
| 3.10 | bilibili embeds | fixed `width=800 height=450` iframes (`title="YouTube video player"` though src is bilibili; Unlogical has 3 incl. one 600×450); loaded state shows the Bilibili player chrome (Chinese UI) at 390 captures for tame/fafa/unlogical; light capture shows a black iframe block | OVERRIDE | OBSERVED-DOM (source) + OBSERVED-VISUAL | layout-light-390, layout-tame-390, layout-fafa-390, layout-unlogical-390 |
| 3.11 | table scroll wrapper | `.table-wrapper` exists on elements; rule `Table .table-wrapper` is dead (deleted `/* Table */` comment) → computed `overflow-x:visible`; measured table fits 350px @390 so no visual break today, but no scroll path remains | OVERRIDE (bug) | OBSERVED-CSS (probe: wrapperOverflowX visible) | layout-elements-390 |

## 4 · Motion findings

| # | Motion | Value | Evidence | Ref |
|---|---|---|---|---|
| 4.1 | preload gate | `body.is-preload *,:before,:after { animation:none !important; transition:none !important }` | OBSERVED-CSS (main.css L108-117; same in upstream L105) | — |
| 4.2 | preload visual state | with main.js blocked: body class `is-preload`, `.tiles article` opacity **0**, transform `matrix(0.9,0,0,0.9,0,0)`, transition `none`; `#header` opacity **1** | OBSERVED-CSS (probe) | — |
| 4.3 | load-in trigger | main.js removes `is-preload` 100 ms after `window.load` (`setTimeout(...,100)`) | OBSERVED-DOM (main.js) | — |
| 4.4 | tiles entrance | `.tiles article { transition: transform .5s ease, opacity .5s ease }`; measured opacity ramp: t≈398 ms → 0.221, 484 → 0.576, 571 → 0.802, 659 → 0.925, 746 → 0.990, ~830 → 1.0 with transform scale 0.922→1 synchronised (class present at t=312, gone at t=398) | OBSERVED-CSS (probe series) | — |
| 4.5 | what animates | ONLY `.tiles article` (index's 8 articles). No `#wrapper` opacity rule exists in deployed or upstream CSS (grep: 0 hits); header measured opacity 1 under preload → pass-1 pack claims "header fades with load-in" and "#wrapper opacity 0.45s (0→1)" are **not supported by rendered evidence** | OBSERVED-CSS | — |
| 4.6 | no-JS fallback | noscript.css: `body.is-preload .tiles article { transform:none; opacity:1 }` | OBSERVED-DOM | — |
| 4.7 | menu slide | `transform .45s ease, visibility .45s`; inner `opacity .45s`; close button `scale(.25) rotate(180deg)` → `scale(1) rotate(0)`; wrapper dims to opacity .25 (all ≤450ms) | OBSERVED-CSS (L2994-3163) + probe | layout-index-menu-open-390 |
| 4.8 | carousel autoplay | inline script: `setInterval(showNext, 4000)`; each tick removes all `.carousel-item` and inserts a new one (instant swap, no transition). Observed state change at `performance.now()=4132 ms` after navigation (≈4.0 s after DOMContentLoaded), caption "ILightUUp" → "Sea, Sense, and Melody" | OBSERVED-DOM (source + probe) | layout-carousel-state1/2-1280 |
| 4.9 | dead carousel controls | `showPrev` defined but never wired; comment "Buttons removed for automatic switching"; no prev/next/pause in DOM | OBSERVED-DOM (source L291-298, L84) | layout-carousel-state1-1280 |

## 5 · WIP / gap sweep (ledger-ready)

| item | evidence | screenshot / measure ref |
|---|---|---|
| 6 carousel sources unreachable: `randomgallery/{light,seasense,tame,installation1,installation5,lightinstallation}.jpg` | serve log 404s; `img.naturalWidth=0, complete=true` | layout-carousel-state1/2-1280 (broken-image box in both states) |
| `tame/emotion map.jpg` unreachable (broken placeholder mid-page) | serve log 404; DOM broken list | layout-tame-390 |
| `unlogical/BOOKLET-01 - Copy.jpg` unreachable | serve log 404; DOM broken list | layout-unlogical-390 |
| `light/ILightUUp1080p.mp4` is a 133-byte git-LFS pointer, not a video (its `<video>` is commented out anyway) | `file` + head check | source L84-87 |
| nested `<!DOCTYPE html><html><head>…</head><body></body></html>` mid-body on index | source L58-67; DOM: 4 `<meta>`, 2nd `<title>Document</title>` parented to `<header>`; renders as blank line | layout-index-nesteddoctype-1280 |
| duplicated `id="main"` on index | DOM: `querySelectorAll('#main').length = 2` | layout-index-390/1280 |
| stray `</h1>` + commented-out `<h2>` headings + commented `<!-- <p>… -->` in index header | source L56-57, L68-69 | layout-index-nesteddoctype-1280 |
| stock lorem menus on 7 pages ("Ipsum veroeros / Tempus etiam / Consequat dolor / Elements" → all link `generic.html`/`elements.html`) | DOM menu items | layout-elements-1280, layout-light-390 |
| elements.html = untouched template demo (title/logo "Phantom", © Untitled, lorem blocks ×5, demo form) | source + DOM | layout-elements-1280/390 |
| index lorem survivor: "Sea, sense" tile copy "Sed nisl arcu euismod…" | source L163 | layout-index-1280 (tile row 2) |
| light.html carries the FAFA blurb ("FAFA is a plant-like virus program…") under `I Light U Up` — copy-paste | source L79 + rendered | layout-light-1280/390 |
| light.html stray `.*` paragraphs (one live, others commented) | source L91 + DOM text | — |
| 2nd/3rd "Publication and Exhibition" h2 duplication on light (h2 list) | DOM `#main h2` | layout-light-1280 |
| no favicon, no OG tags, no meta description on any of the 9 pages | DOM `head link/meta` inventory | — |
| index metas doubled (charset+viewport from nested block) and `user-scalable=yes` vs `no` elsewhere | DOM metas | — |
| broken `</S>` inside publication title: `Zhen's publication</S>` (browser title bar literal) | DOM `document.title` | layout-publication-1280 |
| wordmarks 4 variants (`Zhen Wu YoYo 圳` / `Phantom` / `About Zhen` / `Back to main`) | DOM `.logo .title` | layout-index-1280 vs layout-elements-1280 vs layout-light-390 |
| footers: commented-out on 4 project pages; absent on email; template `© Untitled` on elements/generic/publication; index "la la la" | source + DOM | layout-light-1280 (no footer), layout-generic-1280 |
| alt text: nearly all `alt=""` (index 11, elements 13, generic 2, publication 1, Unlogical 10, email 2); light/tame use repeated `alt="Visual Design"` | DOM img inventory | — |
| per-page inline styles (source): index 8 · light 13 · tame 14 · fafa 10 · Unlogical 22 (+ JS textarea styles); full lists in §Appendix | source grep + DOM | — |
| identical per-page `<style>` block on light/tame/fafa/Unlogical (bg `rgb(251,251,251)`, body colour black, `.image1` floats, `img 100%`) | byte-identical source | layout-light-1280, layout-fafa-390 |
| mobile horizontal overflow: document scrollWidth 700 (index), 820 (light), 920 (tame, fafa), 1020 (Unlogical) at 390 viewport — from fixed inline px widths | Playwright measure + PNG widths | layout-index-390, layout-light-390, layout-tame-390, layout-fafa-390, layout-unlogical-390 |
| index collage img inline `width:700px` (overflows 390; right edge flush 700) + "This is Yoyo~" caption | DOM probe | layout-index-390 |
| `.table-wrapper` scroll rule dead (selector `Table .table-wrapper` after deleted comment) | css-diff.txt #9 + probe `overflow-x:visible` | layout-elements-390 |
| iframes: fixed 800×450 (one 600×450), `title="YouTube video player"` but bilibili src | source | layout-unlogical-390 |
| carousel: controls removed, `showPrev` unused, empty `desc`, captions repeat (ILightUUp ×4 of 6) | source L263-298 | layout-carousel-state1/2-1280 |
| "Short description" placeholder h1s remain as comments on 4 project pages | source L77/81 (commented) | — |
| generic.html serves About **and** is the target of 4 unrelated project tiles (observer/Sea sense/Orchid/SoundMorphTPU) | source links | layout-index-1280 |
| email page: two h1s stacked ("Email contact~" then the address) | DOM h1 inventory | layout-email-390 |

## 6 · Proposed pack entries

Seven objects (pack revision; `layout/*` ids marked *rev* replace the pass-1
entries, whose "centered header / header fades / #wrapper fade" claims are
contradicted by rendered evidence in §4.5).

```json
[
 {
  "id": "layout/page-shell",
  "kind": "layout",
  "title": "Page shell — header / menu / main / footer slots",
  "summary": "Every page is #wrapper > header#header (static, 8em top pad; logo left; fixed 64x48 translucent 'Menu' pill top-right) + nav#menu (fixed slide-in panel; 22em @1280, 16.5em <=736) + div#main inside a 68em/2.5em container (1.25em gutters <=736) + an optional footer#footer slot that is rendered on only 4 of 9 pages.",
  "aliases": ["page shell", "page layout", "site shell", "wrapper", "container", "page structure", "main container", "content width"],
  "body": {
   "group": "Layout",
   "structure": [
    "#wrapper > header#header > .inner (a.logo: .symbol img logo.svg 2em + .title wordmark; nav = single 'Menu' link)",
    "nav#menu (fixed right panel; JS moves it to <body> and wraps #menu > .inner; h2 'Menu' + ul links)",
    "div#main > .inner (68em container)",
    "footer#footer (grey #f6f6f6; 2 flex sections + copyright bar) — optional per page"
   ],
   "metrics": [
    "container max-width 68em, padding 0 2.5em (1.25em <=736); measured content 1008px @1280 / 350px @390",
    "#header static; padding-top 8em (4em <=736); measured height 202 @1280 / 138 @390",
    "#main padding-bottom 6em (4em <=736); #footer padding 5em 0 6em",
    "#menu width 22em (352px @1280) / 16.5em (264px <=736); close button sits left of panel (left:-4.25em <=736); body.is-menu-visible dims #wrapper to opacity .25"
   ],
   "verify": ["#wrapper", "#main > .inner", "#footer"],
   "variance": "footer rendered on index (custom), elements/generic/publication (template); commented out on light/tame/fafa/Unlogical; absent on email"
  },
  "source": {"repo": "HTML5 UP Phantom + zhenyoyo.github.io deployment", "path": "deployed main.css L3330-3341 (container), L2843-2978 (header), L2979-3163 (menu); per-page HTML footer blocks"}
 },
 {
  "id": "layout/header",
  "kind": "layout",
  "title": "Header — logo left, fixed Menu pill (no load animation)",
  "summary": "Static top block: padded 8em (4em <=736); logo left = 2em symbol image + tracked-caps (0.35em) wordmark; a single 'Menu' control is fixed top-right (right 2em/top 2em; .5em <=736) as a 64x48 translucent-white box with its label hidden (text-indent 64px, overflow hidden) and hamburger lines drawn by ::before/::after. Radius 4px kept here while the rest of the deployment flattened radii to 0. The header does NOT fade with the load-in (opacity 1 during is-preload — measured).",
  "aliases": ["header", "site header", "logo", "brand", "top bar", "menu button", "hamburger", "site header with logo"],
  "body": {
   "class": "#header",
   "group": "Layout",
   "structure": [
    "a.logo > .symbol (img logo.svg 2em x 2em) + .title (uppercase, 900, letter-spacing .35em)",
    "#header nav { position: fixed; right: 2em; top: 2em } (right/top .5em <=736) — the only nav item is a[href='#menu']"
   ],
   "verify": ["#header", "#header .logo", "#header nav a[href='#menu']"],
   "measured": [
    "menu pill rect 64x48; @1280 x=1184,y=32; @390 x=318,y=8",
    "wordmark variants deployed: 'Zhen Wu YoYo 圳' / 'Phantom' / 'About Zhen' / 'Back to main'"
   ]
  },
  "source": {"repo": "HTML5 UP Phantom + zhenyoyo.github.io deployment", "path": "deployed main.css L2843-2978 (Header); measured in browser"}
 },
 {
  "id": "layout/footer",
  "kind": "layout",
  "title": "Footer — 2 sections + copyright (present on 4 of 9 pages)",
  "summary": "Grey #f6f6f6 ground, padding 5em 0 6em; flex .inner with contact block (form, ~66%) + Follow icon row (~33%) + full-width copyright bar (0.8em, ink-50%). Rendered on only 4 pages: index replaces the form with plain email text, a 4-icon custom row (Instagram, Google Scholar book, GitHub, Email) and a 'la la la' copyright; elements/generic/publication keep the untouched template footer (Contact form 'Send', 8 icons, (c) Untitled); light/tame/fafa/Unlogical comment the whole footer out; email has none.",
  "aliases": ["footer", "contact block", "follow block", "copyright", "footer contact section", "get in touch"],
  "body": {
   "class": "#footer",
   "group": "Layout",
   "states": ["rendered (index/elements/generic/publication)", "commented out (light/tame/fafa/Unlogical)", "absent (email)"],
   "verify": ["#footer"],
   "measured": ["section h2s when rendered: 'Get in touch' + 'Follow'", "ground #f6f6f6; copyright variants: 'la la la' vs '(c) Untitled. All rights reserved' + 'Design: HTML5 UP'"]
  },
  "source": {"repo": "HTML5 UP Phantom + zhenyoyo.github.io deployment", "path": "deployed main.css L3179-3327 (Footer); per-page HTML"}
 },
 {
  "id": "layout/page-intro",
  "kind": "layout",
  "title": "Load-in motion (is-preload) — tiles only",
  "summary": "The deployment's only authored motion: body.is-preload disables all animation/transition (!important) and holds .tiles article at scale(0.9)/opacity 0; main.js removes the class 100ms after window.load; tiles run transform+opacity 0.5s ease to scale(1)/opacity 1 (measured ramp 0.22->0.99 across ~350ms, settled ~830ms after navigation). Header stays opacity 1 and no #wrapper fade rule exists in deployed or upstream CSS. noscript.css neutralises the preload transform.",
  "aliases": ["page load animation", "intro animation", "fade in", "load transition", "entrance motion", "page load fade-in", "is-preload"],
  "body": {
   "class": "body.is-preload",
   "group": "Layout",
   "spec": [
    "is-preload disables ALL animation/transition (main.css L108-117)",
    ".tiles article: transform scale(0.9) + opacity 0 under is-preload (L2771-2777); transition transform .5s ease, opacity .5s ease (L2589-2593)",
    "trigger: class removed 100ms after window.load (main.js)",
    "measured: opacity 0 -> 0.221 (t=398ms) -> 0.576 -> 0.802 -> 0.925 -> 0.990 -> 1.0 (~830ms), transform scale 0.922 -> 1 synchronised",
    "nothing else animates: header opacity 1 under preload; no #wrapper rule in CSS (correction of pass-1 claim)"
   ],
   "verify": ["body", ".tiles article"]
  },
  "source": {"repo": "HTML5 UP Phantom + zhenyoyo.github.io deployment", "path": "deployed main.css L108-117, L2589-2593, L2771-2777; main.js; measured series"}
 },
 {
  "id": "layout/project-page",
  "kind": "layout",
  "title": "Project-detail composition (light / tame / fafa / Unlogical)",
  "summary": "Project pages are hand-built inside the shell: h1 with per-page inline colour (#ff6bbc / #ff8b80 / #fd77af / #71c3de) + span.image.main hero + freeform blocks; each page carries an identical <style> block (body rgb(251,251,251)/black text, .image1 70% odd/even floats, img 100%) plus inline px widths 300-1000px; a 'Trailer video' section embeds a fixed 800x450 bilibili iframe (title attr says 'YouTube video player'); Gallery alternates floats left/right; the footer is commented out everywhere. Fixed widths overflow mobile (document 820-1020px at a 390 viewport). No shared classes beyond the template's .image/.image.main.",
  "aliases": ["project page", "project detail", "portfolio detail", "case study layout", "project layout", "gallery layout"],
  "body": {
   "group": "Layout",
   "structure": [
    "#main .inner > h1 (inline colour) > span.image.main hero > <p> blurb",
    "h2 'Trailer video' + centered div > iframe 800x450 (bilibili) + 'Video source:' link",
    "h2 'Publication and Exhibition' / h2 'Concept' / h2 'Gallery'",
    "Gallery: .image1 (float odd/even, width 70%) + inline-width images"
   ],
   "verify": ["#main > .inner > h1", ".image1", "iframe"],
   "issues": [
    "hard-coded px widths (300-1000) overflow <=736 viewports",
    "footer commented out; 'Short description' placeholder h1 left commented",
    "4 pages carry the same leftover style block; light.html carries the FAFA copy"
   ]
  },
  "source": {"repo": "HTML5 UP Phantom + zhenyoyo.github.io deployment", "path": "light.html/tame.html/fafa.html/Unlogical.html (per-page <style> + inline styles); measured"}
 },
 {
  "id": "candidate/carousel",
  "kind": "candidate",
  "title": "Random-gallery carousel (autoplay, hand-rolled)",
  "summary": "Deployed-only autoplay gallery: #carouselGallery (inline position:relative; max-width:1200px; margin:auto) receives one .carousel-item per tick — img 640x360 object-fit:cover (inline), h3 title, empty p — and swaps it instantly every 4000ms (setInterval(showNext, 4000); no controls, buttons removed; showPrev unused). All six deployed sources (randomgallery/*.jpg) 404, so both captured states show the broken-image placeholder; captions repeat (ILightUUp x4) and descriptions are empty. Motion-policy questions: autoplay vs the is-preload intro canon, and no pause/prev/next affordance.",
  "aliases": ["carousel", "gallery carousel", "autoplay", "slideshow", "random gallery", "image slider"],
  "body": {
   "group": "Overlays",
   "contract": [
    "#carouselGallery + .carousel-item { img 640x360 cover, h3 title, p desc }",
    "tick = remove all .carousel-item, insert new one at currentIndex"
   ],
   "motion": ["setInterval 4000ms (declared); observed change ~4.0s after DOMContentLoaded (t=4132ms post-nav)", "no transition on swap (instant DOM replacement)"],
   "states": ["default (broken image, caption only)", "tick N (broken image, next caption)"],
   "open": ["autoplay timing/looping policy", "controls spec (prev/next/pause were removed)", "fallback for unreachable sources"]
  },
  "source": {"repo": "zhenyoyo.github.io deployment (index.html inline script)", "path": "index.html L261-305; observed at runtime"}
 },
 {
  "id": "token-set/breakpoints",
  "kind": "token-set",
  "title": "Breakpoints — xlarge through xxsmall",
  "summary": "Template breakpoints (main.js breakpoints()): xlarge 1281-1680, large 981-1280, medium 737-980, small 481-736, xsmall 361-480, xxsmall <=360. CSS queries at 1280/980/736/480/360 govern container gutters (2.5em -> 1.25em at <=736), header padding (8em -> 4em at <=736), menu width (22em -> 16.5em at <=736), menu button offset (2em -> .5em at <=736) and tiles per row (3-up at <=1280; 1-up measured at 390).",
  "aliases": ["breakpoints", "responsive", "media queries", "screen sizes"],
  "body": {
   "group": "Foundations",
   "tokens": [
    "xlarge 1281-1680 / large 981-1280 / medium 737-980 / small 481-736 / xsmall 361-480 / xxsmall <=360",
    "css queries used: 1280 (tiles 33.33%), 980, 736 (header/menu scale switch), 480 (menu-button hamburger), 360"
   ],
   "verify": ["html", "body"]
  },
  "source": {"repo": "HTML5 UP Phantom + zhenyoyo.github.io deployment", "path": "main.js breakpoints(); deployed main.css media queries"}
 }
]
```

## 7 · Open questions

1. Are the six `randomgallery/*` images recoverable from the live site, or is
   the carousel broken in production too? (mirror + serve log say 404; live
   cross-check out of this team's scope).
2. Project-page footers are commented out identically on all four project
   pages — deliberate simplification or leftover comment-outs?
3. Which menu set is canonical: the index/publication set, or the stock lorem
   set used by the other seven pages ("Elements" links even point at the
   untouched demo)?
4. `light.html` carries the FAFA blurb and repeats "Publication and
   Exhibition" twice — copy-paste accident to record as-is, or intended reuse?
5. Duplicated `id="main"` and the nested `<!DOCTYPE html>` block render
   harmlessly (blank line) but are invalid markup; keep as "content", or treat
   as defects in the revised ledger?
6. Should the four identical project-page `<style>` blocks + inline px widths
   be extracted as a "project gallery" pattern candidate (float alternation is
   consistently applied), or held as one-off improvisation?
7. Mid-breakpoint behaviour (736/480) was not captured — tile counts, header
   stacking and menu states between 390 and 1280 remain unverified.
8. `alt="Visual Design"` repeats on light/tame vs `alt=""` elsewhere — is any
   alt-text discipline intended?

## Appendix · evidence files

Screenshots (`docs/synthesis/phantom/evidence/screens/`, 18 files):
9 × `layout-<page>-390.png` (index file is 700px wide due to overflow; light
820; tame 920; fafa 920; unlogical 1020) · `layout-{index,elements,generic,
publication,light}-1280.png` · `layout-carousel-state1-1280.png` (1008×403,
broken image + "ILightUUp") · `layout-carousel-state2-1280.png` (broken image +
"Sea, Sense, and Melody") · `layout-index-menu-open-390.png` (green #3ef900
panel, 264px, 5 items + Close) · `layout-index-nesteddoctype-1280.png` (header
region: no heading, 3 pink intro lines, no visible trace of the nested block).

Inline-style inventory (source grep, `style\s*=\s*"`): index 8
(`font-size: small` ×2; carousel gallery/item/img/h3/p; collage `width:700px`;
center p) · light 13 · tame 14 · fafa 10 · Unlogical 22 (`color:#…` on h1/h2;
`text-align:center/right/left` divs; `width:200–1000px` imgs; float `width:500px`
with `margin-left:20px;margin-top:10px;margin-bottom:30px`) · elements/generic/
publication/email 0 author inline styles (only main.js textarea styles appear at
runtime). Runtime `[style]` counts add the JS-set inline styles: index 9,
elements 2, generic/publication 1 each.
