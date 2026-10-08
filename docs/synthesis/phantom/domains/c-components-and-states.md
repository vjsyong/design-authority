# Domain C — components & states (phantom redo, pass 2)

**Scope:** every visible component of the deployed site *as rendered*: buttons, underline
fields/selects/textareas, checkboxes/radios, tables, project tiles (+hover), icon chips &
emblem, nav hamburger, slide-in menu, index carousel, footer blocks, hr/blockquote/code.
Pages probed: index, elements, light, publication, generic, tame (1280×900); index+elements
(390×844). Mirror served from `_raw/site/` on :8412; Chromium via Playwright
(`.venv` + `PLAYWRIGHT_BROWSERS_PATH=~/.cache/ms-playwright`).

**Method / evidence key:** `OBSERVED-CSS` = computed style / geometry probe on the rendered
page; `OBSERVED-VISUAL` = plain-language read of the named screenshot file (vision_analyze);
`INFERRED` = conclusion from CSS cascade or layout math. `BASE` = value inherited from the
HTML5 UP Phantom template (verified against `_raw/upstream/main.css` / `css-diff.txt`);
`OVERRIDE` = deployment change. Screenshots live in
`docs/synthesis/phantom/evidence/screens/comp-*.png` (17 files, listed inline below).

## Summary

1. The rendered component language is a hybrid: the template's grey **ink** skeleton
   (buttons/fields/table rules all `#585858` / `#c9c9c9`, 4px radii on buttons) now sits on a
   **pink-typed page** (body `rgb(255,107,188)`), with deployment overrides that re-colour
   islets of the component set (red checked fills, purple control labels, blue code chip,
   neon-green menu) and flatten most radii to 0px.
2. Buttons remain template-ink: `inset 0 0 0 2px #585858` ring, label `#585858`; hover = the
   template's `#f2849e` pink for label + ring (measured); primary = solid `#585858`, hover
   fills `#f2849e`. Height 44.8px, 900 weight, 0.35em tracking, 4px radius (all BASE).
3. Fields are underline-only (1px `#c9c9c9`), 48px tall, no radius; focus swaps to a 2px
   `#f2849e` pink underline (1px border + `inset 0 -1px 0 0`). OBSERVED-VISUAL confirmed.
4. Checked boxes/radios fill **`#f51616` red** with a white `\f00c` checkmark (radio shares
   the checkbox glyph — a check inside a circle); labels are **purple `#8833e3`**. All
   OVERRIDE.
5. Tiles: radius flattened to 0; rest veils are mostly *fully transparent* (`#ffe2e500`,
   `#efc5e900`, two faint tints); hover = **opaque flat pink `#eb84da`** covering the whole
   photo (measured pixel-histogram 97.6% of the tile), no zoom (`scale(1)`, OVERRIDE of the
   template's 1.1), white caption overlay appears (opacity 0→1, max-height 0→15em).
6. Icon chips (`style2`) are 42.4px **squares** (radius 0, OVERRIDE from 4px) with 1px
   `#c9c9c9` borders and pink glyphs; hover = pink border + glyph `#f2849e`. `style1` icons
   are bare glyph links (green, like links). The round emblem = 32×32px `logo.svg` in the
   header lock-up.
7. Menu overlay: **neon green `#3ef900` panel** (OVERRIDE from `#585858`) with black links;
   separators stay template-white at 15% alpha (BASE value, now on green); page behind dims
   to 25% opacity (measured `#585858`→(214,214,214)); close X sits left of the panel.
8. Tables are template-pure: 900 heads at 14.4px, 2px `#c9c9c9` header/footer rules, 1px row
   rules, odd rows tinted `rgba(144,144,144,0.075)` (pixel-verified bands), pink cell text.
9. Index carousel: fixed 640×360 images, 4s auto-advance, no controls, pink tracked title
   (captured 2 states). Mirror caveat: carousel images 404 locally (live returns 200).
10. Measured contrast of state colours: state pink `#f2849e` on white 2.45:1; white caption
    on the pink tile-hover veil 2.37:1; link green `#6bff2c` on white 1.32:1 (component
    relevance: tile captions + hover affordances).

---

## Findings

### C-1 · Buttons — ink ring, tracked caps, pink-on-hover

Rendered on `elements.html` (Buttons/Actions/Form sections) and as the only real submit
controls (footer "Send", form "Send Message"). Screenshots: `comp-elements-1280.png`,
`comp-elements-btn-hover-1280.png` (region, default button hovered).

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| ring (default) | `box-shadow: inset 0 0 0 2px rgb(88,88,88)` (`#585858`), transparent fill | BASE | OBSERVED-CSS |
| label (default) | `#585858` `!important`, 12.8px (0.8em), weight 900, letter-spacing 3.36–4.48px (0.35em), uppercase | BASE | OBSERVED-CSS |
| height / radius | 44.8px (3.5em); `border-radius: 4px` (NOT flattened) | BASE | OBSERVED-CSS |
| padding | `0 16px 0 20.48px` (0 1.25em 0 1.6em) | BASE | OBSERVED-CSS |
| hover (default) | label → `rgb(242,132,158)` `#f2849e`, ring → `inset 0 0 0 2px #f2849e` (measured with real pointer move) | BASE | OBSERVED-CSS + VISUAL (`comp-elements-btn-hover-1280.png`: pink ring + pink label) |
| active | `background-color: rgba(242,132,158,0.1)` | BASE | CSS text |
| primary | fill `#585858`, label white; hover fill `#f2849e` (measured); active `#ee5f81` | BASE | OBSERVED-CSS |
| sizes | small 0.6em → 33.6px tall; large 1em → 56px tall; `.fit` full width | BASE | OBSERVED-CSS |
| disabled | `opacity: 0.25`, `pointer-events: none` (renders as faint grey plate — near-illegible) | BASE | OBSERVED-CSS |
| transition | background-color/color/box-shadow 0.2s ease-in-out | BASE | OBSERVED-CSS |

Deltas vs pass-1 pack (`component/action-button`): summary said "hover: label + ring
#f2849e; active: slightly darker ring" — active is a *fill*, `rgba(242,132,158,0.1)`; also
pass-1 said "focus must remain visible… UA focus by default" — no button focus style exists
(tab focus = UA default). What pass-1 got wrong is elsewhere (tiles/checkbox/icon).

### C-2 · Fields (underline inputs, textarea, select) + focus state

Rendered on `elements.html` Form + footer contact forms. Screenshots:
`comp-elements-field-focus-1280.png` (focused Name vs idle Email),
`comp-elements-form-1280.png` (whole form).

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| geometry | exact height 48px (3em), width 100%, padding 0, radius 0 | BASE | OBSERVED-CSS |
| line | `border-bottom: 1px solid rgb(201,201,201)` (`#c9c9c9`), no other border, transparent bg | BASE | OBSERVED-CSS |
| text/placeholder | value colour `rgb(255,107,188)` ink-pink (OVERRIDE via body/input colour); placeholders un-styled browser grey | OVERRIDE (colour) | OBSERVED-CSS + VISUAL |
| focus | `border-bottom-color: #f2849e` + `box-shadow: inset 0 -1px 0 0 #f2849e` → 2px pink underline | BASE | OBSERVED-CSS + VISUAL (screenshot shows thick pink vs thin grey line) |
| textarea | min-height 3.75em (60px measured), same line/focus | BASE | OBSERVED-CSS |
| select | height 3em; chevron = inline SVG arrow `fill %23c9c9c9`, `background-size 1.25rem`, positioned `calc(100% - 1rem) center`; padding-right 3em; radius 0; `option { background: #fff }` | BASE | OBSERVED-CSS |
| widths | `.fields > .field.half` 50%, `.third` 33%, `.quarter` 25% | BASE | CSS text |

Deltas vs pass-1: pass-1 pack described fields as sitting on a "faint tint" — the *deployed*
field ground is plain white `rgb(255,255,255)` (measured); the tint was not applied. Pass-1
focus description ("2px pink underline") is correct.

### C-3 · Checkbox & radio — red checked fill, purple labels

Rendered on `elements.html` Form. Screenshot: `comp-elements-form-1280.png`.

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| box size | 28.8×28.8px (2.25em at 0.8em font-size) | BASE | OBSERVED-CSS |
| checkbox shape | `border-radius: 0px` (template 4px) | OVERRIDE | OBSERVED-CSS + css-diff |
| radio shape | `border-radius: 100%` (circle kept) | BASE | OBSERVED-CSS |
| unchecked | 1px solid `#c9c9c9` border, transparent fill | BASE | OBSERVED-CSS |
| checked fill | `background: rgb(245,22,22)` `#f51616`, `border-color: rgb(248,33,33)` `#f82121`, glyph `content:"\f00c"` white (900) | OVERRIDE (template: `#585858`) | OBSERVED-CSS |
| radio checked glyph | same `\f00c` **checkmark inside the circle** (shared rule; not a dot) | BASE rule + OVERRIDE colours | OBSERVED-CSS |
| label | colour `rgb(136,51,227)` `#8833e3`, 1em/300, `padding-left: 2.55em` | OVERRIDE (template: ink) | OBSERVED-CSS |
| focus | border `#f2849e` + `box-shadow: 0 0 0 1px #f2849e` (1px pink ring) | BASE | OBSERVED-CSS |

Vision read (`comp-elements-form-1280.png`): checked radio & checked checkbox both "filled
bright red with a white checkmark glyph, not a dot"; labels "light purple/lavender";
unchecked rings grey — OBSERVED-VISUAL.

### C-4 · Tables — 900 heads, 2px rules, tinted alternates

Rendered on `elements.html` (Default + Alternate). Screenshots:
`comp-elements-table-1280.png`, `comp-elements-1280.png`.

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| th | 14.4px (0.9em) weight **900**, `text-align: left`, `padding: 0 10.8px 10.8px`; inherits pink text | BASE (pink via body OVERRIDE) | OBSERVED-CSS |
| header/footer rules | thead `border-bottom: 2px solid #c9c9c9`; tfoot `border-top: 2px solid #c9c9c9` | BASE | OBSERVED-CSS + VISUAL |
| row rules | `tbody tr` 1px solid `#c9c9c9` top+bottom, no side borders | BASE | OBSERVED-CSS |
| zebra | `tbody tr:nth-child(2n+1)` → `rgba(144,144,144,0.075)` (~#f7f7f7) — odd rows (1,3,5) tinted; pixel band scan of the screenshot confirms tint–white–tint–white–tint in both tables | BASE | OBSERVED-CSS + pixel scan |
| td | `padding: 12px` (0.75em), pink text | BASE | OBSERVED-CSS |
| alt table | `border-collapse: separate` + 1px `#c9c9c9` cell grid; same zebra as default (vision's claim of *inverted* striping was not supported by the pixel scan — both tables tint odd rows) | BASE | OBSERVED-CSS |
| small screens | `.table-wrapper { overflow-x: auto }` | BASE | CSS text |

### C-5 · Project tiles — the deployed hover system (no zoom, flat pink veil)

Rendered on `index.html` (Artwork / Computational tools / Technology probe grids).
Screenshots: `comp-index-1280.png` (rest), `comp-index-tile-hover-1280.png` (hovered first
tile), `comp-index-390.png` (1-up mobile).

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| tile geometry | 322.66×322.66px at 1280 (3-up, `calc(33.33% - 2.5em)`), 2.5em gutters/margins | BASE | OBSERVED-CSS |
| image radius | `border-radius: 0px` (template 4px) | OVERRIDE | OBSERVED-CSS |
| rest veil (`:before`) | per style: unclassed/`style1`/`style2` → `#efc5e900`/`#ffe2e500` (**alpha 0, invisible**); `style3` → `rgba(116,111,250,0.157)`; `style4–6` → `#ffe2e524` (α0.141); base opacity 0.8 | OVERRIDE (template pastels) | OBSERVED-CSS |
| hover veil | `:before { background-color: rgb(235,132,218) #eb84da; opacity: 1 }` — **fully opaque**: pixel histogram of `comp-index-tile-hover-1280.png` = 102,098/104,652 px exactly (235,132,218), i.e. 97.6% flat pink; photo not visible through it | OVERRIDE (template `#333` α0.35) | OBSERVED-CSS + pixel histogram + VISUAL ("photo heavily veiled, distinct pink tint") |
| hover zoom | `transform: scale(1)` — **no zoom** (template hovered to `scale(1.1)`) | OVERRIDE | OBSERVED-CSS (CSS text) |
| `:after` cross overlay | `background-image` commented out; `opacity: 0` at rest, `0` on hover (template 0.25 → 0) | OVERRIDE | OBSERVED-CSS |
| caption overlay (`a`) | `a { opacity: 0; padding: 1em; color #fff !important; border-radius: 4px }`; hover `opacity: 1` (deployment added the opacity dance) | OVERRIDE | OBSERVED-CSS |
| caption text | h2 + `.content` white; `.content` `max-height: 0 → 15em` (240px measured), `opacity: 0 → 1`, transition 0.5s; white-on-`#eb84da` contrast **2.37:1** | OVERRIDE (opacities) | OBSERVED-CSS + contrast calc |
| rest state look | tile photos shown plain; **no resting caption or arrow chrome visible** | — | OBSERVED-VISUAL (`comp-index-1280.png`: clean photos, no overlays) |

Deltas vs pass-1 pack (`component/tiles`): pass-1 promised "pastel veil by .styleN", "image
zoom (scale 1.1)", "arrow marker fades out", "4px radius". Rendered truth: zoom removed,
cross/arrow gone, radius 0, four of six style veils are α0, and the hover veil is opaque
flat `#eb84da` — the module the pass-1 summary describes no longer exists in that form.

### C-6 · Icon chips (`style2`) & inline icons (`style1`)

Rendered in Lists section and every footer. Screenshots:
`comp-elements-icons-hover-1280.png` (hovered first chip), `comp-elements-1280.png`,
`comp-index-1280.png` (footer, 4 chips).

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| chip box | 42.4×42.4px (2.65em), `border: 1px solid #c9c9c9`, **`border-radius: 0px`** (template 4px), transparent ground | OVERRIDE (radius) | OBSERVED-CSS |
| base glyph | colour `inherit` (class beats `a` selector) → pink `rgb(255,107,188)` on pink-body pages; footer chips same | OVERRIDE (via body colour) | OBSERVED-CSS |
| hover | glyph + border → `#f2849e` (`comp-elements-icons-hover-1280.png`: first chip pink border + pink icon vs three grey-bordered pink icons) | BASE | OBSERVED-CSS + VISUAL |
| active | `background-color: rgba(242,132,158,0.1)` | BASE | CSS text |
| `style1` (bare icons) | no chip; glyph takes link colour — renders **green `#6bff2c`** in the Lists row | OVERRIDE (via link colour) | OBSERVED-VISUAL (green icons row) + INFERRED (specificity: `a` green applies where `.icon.style2` doesn't override) |
| row layout | `ul.icons li` inline, 0.5em gaps (flex) | BASE | CSS text |

Deltas vs pass-1 (`component/icon-row`): pass-1 title says "Icon (**circles**)" — the
rendered chips are 0px-radius squares (the template itself was 4px rounded, not circles);
the colour story (pink glyph + pink hover) is deployment/body-colour driven.

### C-7 · Round emblem + wordmark lock-up

Header, every page (`.logo` → `.symbol img` = `images/logo.svg`). Screenshots:
`comp-index-1280.png`, `comp-elements-1280.png` (top-left).

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| symbol | 32×32px (2em) `logo.svg` round mark, `margin-right: 0.65em` | BASE | OBSERVED-CSS + VISUAL (dark grey round emblem) |
| wordmark | 900 weight, uppercase, letter-spacing 5.6px (0.35em), colour = body pink `#ff6bbc`; per-page titles differ ("Zhen Wu YoYo 圳", "Phantom" on elements) | OVERRIDE (content) | OBSERVED-CSS + VISUAL |
| lock-up | inline-block, symbol+title inline, `margin-bottom: 2.5em` | BASE | OBSERVED-CSS |
| index title | "ZHEN WU YOYO 圳" (wordmark), rendered pink; vision saw "妍" mis-read of 圳 — treat character as 圳 per HTML | — | OBSERVED-VISUAL (typo by vision, corrected against HTML) |

### C-8 · Nav hamburger trigger

Fixed top-right on every page. Screenshots: `comp-menu-open-1280.png` and full-page shots.

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| plate | 64×48px (4em×3em) link, `background: rgba(255,255,255,0.5)`, `border-radius: 4px`, fixed `right: 2em; top: 2em` | BASE | OBSERVED-CSS |
| icon | 3-line SVG (stroke 8px): grey `%23585858` default layer (`:after`), pink `%23f2849e` layer (`:before`, opacity 0) | BASE | CSS text |
| hover | pink layer `opacity 1`, grey layer `0` | BASE | CSS text |
| label | text "Menu" hidden via `text-indent`/`overflow:hidden` (no visible label, no aria-label in HTML) | BASE | CSS text + HTML |

### C-9 · Menu panel (slide-in, neon green) + open state

Screenshot: `comp-menu-open-1280.png` (viewport, open). Probes on `index.html`.

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| panel | fixed right, 352px wide (22em; 16.5em ≤736px), full height; `background: rgb(62,249,0)` `#3ef900`; text `#000` | OVERRIDE (template `#585858`/white) | OBSERVED-CSS + VISUAL (neon green panel) |
| inner | padding 44px (2.75em) | BASE | OBSERVED-CSS |
| heading | "Menu", 17.6px/900, uppercase, 6.16px tracking, black | BASE (colour via panel) | OBSERVED-CSS |
| list | links black, `padding: 1em 0`, line-height 24px, no underline; separators `border-top: 1px solid rgba(255,255,255,0.15)` on li 2…n (first li `border-top: 0; margin-top: -1em` — measured -16px) | separators BASE (white-15% tuned for dark ground, now on green) | OBSERVED-CSS |
| open mechanics | `body.is-menu-visible` slides panel in (translateX 0) and dims `#wrapper` to `opacity: 0.25` — measured: `#585858` text renders (214,214,214) over white (≈0.25 blend) | BASE | OBSERVED-CSS |
| close control | 96×48px X (SVG lines) at `top:2em; left:-6em` — i.e. sits on the dimmed page, left of the panel; grey `#585858` stroke, pink `#f2849e` on hover (opacity swap) | BASE | OBSERVED-CSS + VISUAL (grey X over dimmed page) |
| link states | menu links: `color: inherit` (black); hover keeps black, no pink here (no hover rule) | OVERRIDE by panel colour | CSS text |

Vision (`comp-menu-open-1280.png`): green panel, black caps heading, black link list with
"faint thin horizontal separators", X placed outside the panel on the light page — OBSERVED-VISUAL.

### C-10 · Index carousel (Random Gallery)

Screenshot pair: `comp-index-carousel-a-1280.png`, `comp-index-carousel-b-1280.png`
(+ `comp-index-1280.png`, `comp-index-390.png`).

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| frame | `#carouselGallery`, `max-width: 1200px; margin: auto; position: relative` (inline styles), no border/controls | OVERRIDE (inline, not in template) | OBSERVED-CSS + HTML |
| item | `<img>` fixed **640×360** (`object-fit: cover`, inline), centred; `h3` title 16px/900 uppercase 5.6px tracking pink; empty `<p>` desc | OVERRIDE | OBSERVED-CSS |
| motion | `setInterval(showNext, 4000)`; DOM item replaced each tick (no CSS transition, no controls — "Buttons removed for automatic switching" comment) | OVERRIDE | JS |
| captured states | state A title `ILIGHTUUP`; state B title `SEA, SENSE, AND MELODY` (both pink tracked caps) | — | OBSERVED-CSS + VISUAL |
| asset caveat | in the mirror the six `randomgallery/*.jpg` files are **missing** (dir empty) → capture shows a broken-image box + border; live URLs return HTTP 200 (curl) → mirror gap, not a live-site defect | — | VISUAL + curl |
| 390 overflow | fixed 640px carousel img + inline 700px webcollage img → document scrollWidth **700** vs clientWidth **390** | OVERRIDE | OBSERVED-CSS (probe) |

### C-11 · Footer blocks

All pages. Screenshots: `comp-elements-1280.png` (footer with form), `comp-publication-1280.png`,
`comp-index-1280.png` (email-only variant), `comp-generic-1280.png`.

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| footer ground | `background-color: rgb(246,246,246)`; `padding: 80px 0 48px` (5em/3em ≤1280) | BASE | OBSERVED-CSS |
| sections | 2-col 66%/33% flex (with 2.5em gutter) then full-width `.copyright` | BASE | OBSERVED-CSS |
| "Get in touch" | form (underline fields + primary submit "Send") on elements/generic/publication; **index instead shows plain text email** `zwuch@connect.ust.hk` (form commented out in HTML) | OVERRIDE (index) | VISUAL + HTML |
| "Follow" | icon chips row (style2, see C-6); index mixes a Font-Awesome book glyph for Google Scholar + chips | OVERRIDE (content) | VISUAL |
| copyright | 12.8px, `rgba(88,88,88,0.5)`, `li` separators `border-left: 1px solid rgba(88,88,88,0.15)` | BASE | OBSERVED-CSS |

### C-12 · hr / blockquote / code / pre

Rendered on `elements.html`. Screenshot: `comp-elements-1280.png`.

| value | measured | BASE/OVERRIDE | evidence |
|---|---|---|---|
| hr | `border-bottom: 1px solid #c9c9c9`, margin 2em top/bottom | BASE | OBSERVED-CSS |
| blockquote | `border-left: 4px solid rgb(201,201,201)`, italic, `padding: 8px 0 8px 32px`; text colour = body pink (inherits) | spec BASE / colour OVERRIDE | OBSERVED-CSS + VISUAL |
| code (inline) | Courier New 14.4px (0.9em), `padding: 3.6px 9.36px`, 1px `#c9c9c9` border, radius **4px** (not flattened), `background: rgba(46,90,249,0.986)` — solid royal blue (template: grey 7.5% tint) | OVERRIDE (ground) | OBSERVED-CSS + VISUAL ("bright royal blue block") |
| pre | transparent, no border, line-height 25.2px, horizontal scroll; monospace 14.4px | BASE | OBSERVED-CSS |

---

## Per-page variance (components)

| page | component-relevant variance | evidence |
|---|---|---|
| index | tiles + carousel + email-only footer; no buttons/tables; body pink `#ff6bbc`; footer chips carry an inline `<i class="fa-solid fa-book">` child (mixed icon source) | OBSERVED-CSS / VISUAL |
| elements | full component set renders (all widgets above); body pink; wordmark says "Phantom" | OBSERVED-CSS |
| light | inline `<style>`: body `background rgb(251,251,251)`, `color rgb(0,0,0)`; h1 inline `color:#ff6bbc`; no buttons/tables/controls; images carry inline widths (800/500/600px etc.) | OBSERVED-CSS + HTML |
| publication | `.publication` class (added to CSS at deploy end): `color: black` on h1 + all `<p>`; links green; footer form + chips | OBSERVED-CSS (h1 black) / VISUAL |
| generic | body pink "About Zhen"; footer form + 8 chips; image span radius 0 | OBSERVED-CSS / VISUAL |
| tame | inline `<style>` body black on `rgb(251,251,251)`; h1 inline `color:#ff8b80` (salmon); no controls; video block renders as black rectangle (iframe/poster) | OBSERVED-CSS + HTML |

## Proposed pack entries

Fenced JSON, pack conventions (`packs/wink` schema; ids aligned with the pass-1 `packs/phantom`
id space so each can supersede its counterpart). `source.path` cites the deployed substrate
that was measured; all numeric values are from the rendered page unless marked otherwise.

```json
[
  {
    "id": "component/action-button",
    "kind": "component",
    "title": "Button (ink ring, tracked caps, pink hover)",
    "summary": "Rendered action: uppercase 900 label at 0.8em with 0.35em tracking, 44.8px tall, radius 4px; default = transparent ground with a 2px ink ring drawn as inset box-shadow #585858; hover flips label + ring to pink #f2849e (measured); primary = solid #585858 with white label, hover ground #f2849e, active #ee5f81. Small 0.6em (33.6px), large 1em (56px), .fit = 100% width. Disabled = opacity .25.",
    "aliases": ["button", "primary button", "cta", "action", "submit button", "small button", "large button", "fit button", "disabled button"],
    "body": {
      "class": ".button / input[type=submit|reset|button]",
      "group": "Actions",
      "states": [
        "default: transparent, ink #585858 label + inset 0 0 0 2px #585858 ring (radius 4px)",
        "hover: label + ring #f2849e (OBSERVED-CSS; screenshot comp-elements-btn-hover-1280.png)",
        "active: ground rgba(242,132,158,0.1)",
        "primary: ground #585858 white label; hover ground #f2849e; active #ee5f81",
        "disabled: opacity .25, pointer-events none (renders near-illegible)"
      ],
      "spec": ["height 3.5em (44.8px measured)", "padding 0 1.25em 0 1.6em", "font 0.8em/900, letter-spacing 0.35em, uppercase", "transition background-color/color/box-shadow 0.2s ease-in-out"],
      "verify": [".button", ".button.primary", ".button.small", ".button.disabled"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css Button block; measured on elements.html"}
  },
  {
    "id": "component/field",
    "kind": "component",
    "title": "Field (underline input, pink focus)",
    "summary": "Text-like inputs and textareas: transparent ground, no box, no radius — a single 1px #c9c9c9 bottom line, exact height 3em (48px). Focus replaces it with a 2px pink #f2849e underline (border color + inset 0 -1px 0 0). Value text renders in the page ink-pink rgb(255,107,188); placeholders stay browser-default grey.",
    "aliases": ["text field", "input", "form field", "email field", "textarea", "contact form", "underline input"],
    "body": {
      "class": "input[type=text|password|email|tel], textarea",
      "group": "Form",
      "states": [
        "default: 1px solid #c9c9c9 bottom line, transparent ground, radius 0",
        "focus: bottom line + 1px inset shadow #f2849e (2px pink; OBSERVED-CSS + screenshot comp-elements-field-focus-1280.png)",
        "value colour: rgb(255,107,188) (body/input colour override)"
      ],
      "layout": [".fields flex wrap; .field.half 50% / .third 33% / .quarter 25%"],
      "verify": ["input[type=text]", "textarea"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css Form block; measured on elements.html"}
  },
  {
    "id": "component/select",
    "kind": "component",
    "title": "Select (underline, custom chevron)",
    "summary": "Native select restyled to the field language: appearance none, transparent, radius 0, 1px #c9c9c9 bottom line, height 3em; chevron is an inline SVG arrow (fill #c9c9c9) at 1.25rem, right offset calc(100% - 1rem); padding-right 3em; option ground white. Focus = same pink underline as fields.",
    "aliases": ["select", "dropdown", "dropdown select", "category picker"],
    "body": {
      "class": "select",
      "group": "Form",
      "states": ["default like field", "focus: pink #f2849e underline"],
      "verify": ["select"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css select block; measured on elements.html"}
  },
  {
    "id": "component/checkbox-radio",
    "kind": "component",
    "title": "Checkbox & radio (red checked fill, purple labels)",
    "summary": "Custom marks drawn with + label:before boxes at 2.25em (28.8px): checkbox radius flattened to 0 (template 4px), radio stays 100%. Unchecked = 1px #c9c9c9 outline; checked = solid #f51616 fill / #f82121 border with a white \u201cf00c checkmark — the shared rule puts the checkmark inside the radio circle too (no dot state). Labels are purple #8833e3 (override), 1em/300, padding-left 2.55em; focus adds a 1px #f2849e ring.",
    "aliases": ["checkbox", "radio", "radio button", "check box", "option mark", "consent checkbox"],
    "body": {
      "class": "input[type=checkbox|radio] + label",
      "group": "Form",
      "states": [
        "unchecked: 1px #c9c9c9 box/ring, transparent",
        "checked: ground #f51616, border #f82121, white \\f00c checkmark (checkbox AND radio; OBSERVED-CSS + screenshot comp-elements-form-1280.png)",
        "focus: border + 0 0 0 1px #f2849e ring",
        "label: #8833e3"
      ],
      "verify": ["input[type=checkbox]", "input[type=radio]"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css checkbox/radio block; measured on elements.html"}
  },
  {
    "id": "component/table",
    "kind": "component",
    "title": "Table (900 head, 2px rules, tinted odd rows)",
    "summary": "Full-width tables: heads 0.9em/900 left-aligned; thead 2px #c9c9c9 rule, tfoot 2px rule, tbody rows 1px top+bottom rules; odd rows tinted rgba(144,144,144,0.075) (~#f7f7f7, pixel-verified); td padding 0.75em. `.alternate` adds a full 1px cell grid and keeps the same zebra. `.table-wrapper` gives overflow-x auto on small screens. Cell text inherits the page ink.",
    "aliases": ["table", "data table", "ruled table", "alternate table", "rows"],
    "body": {
      "class": "table / table.alt / .table-wrapper",
      "group": "Content",
      "states": ["default: horizontal rules only", "alternate: 1px cell grid + same odd-row tint", "wrapper: horizontal scroll"],
      "verify": ["table", "table.alt", ".table-wrapper"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css Table block; measured on elements.html (comp-elements-table-1280.png)"}
  },
  {
    "id": "component/tiles",
    "kind": "component",
    "title": "Tiles (project grid; deployed hover = flat pink veil, no zoom)",
    "summary": "Responsive image grid (3-up at 1280, 322×322px tiles). Image radius flattened to 0. Rest veil per .styleN: unclassed/style1/style2 are alpha-0 (#efc5e900, #ffe2e500), style3 rgba(116,111,250,0.157), style4-6 #ffe2e524. Non-touch hover: veil becomes OPAQUE rgb(235,132,218) #eb84da (opacity 1 — photo fully covered; 97.6% flat-pink in the capture), transform stays scale(1) (template's 1.1 zoom removed), the :after cross overlay is commented out, and the anchor overlay (white h2 + .content) fades in: opacity 0→1, max-height 0→15em over 0.5s.",
    "aliases": ["tiles", "project grid", "portfolio grid", "project cards", "image cards"],
    "body": {
      "class": "section.tiles > article (.style1-6) > .image + a",
      "group": "Content",
      "states": [
        "rest: plain photo (alpha-0 veils on most styles), no caption/arrow visible",
        "hover: opaque #eb84da wash + white caption overlay, no zoom (OBSERVED-CSS + screenshot comp-index-tile-hover-1280.png)"
      ],
      "flaws": ["white caption on #eb84da = 2.37:1 contrast while the photo is invisible", "four of six style veils have zero alpha"],
      "verify": [".tiles article", ".tiles article.style3"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css Tiles block (deployed); measured on index.html"}
  },
  {
    "id": "component/icon-row",
    "kind": "component",
    "title": "Icon chips (square) & inline icons",
    "summary": "ul.icons rows: style2 = square chip 2.65em (42.4px) with 1px #c9c9c9 border, radius flattened to 0 (template 4px), transparent ground, glyph colour inherits the page ink (pink rgb(255,107,188)); hover = glyph + border #f2849e; active ground rgba(242,132,158,0.1). style1 = bare glyph links, no chip (rendered green via the link colour #6bff2c). Icons come from the bundled Font Awesome set; index footer also inlines a fa-solid book glyph.",
    "aliases": ["icons", "social icons", "icon chips", "follow row", "social row"],
    "body": {
      "class": "ul.icons li a.icon (style1|style2, solid|brands)",
      "group": "Content",
      "states": ["default: 1px #c9c9c9 square outline + inherited (pink) glyph", "hover: #f2849e glyph + border (screenshot comp-elements-icons-hover-1280.png)", "active: rgba(242,132,158,0.1) ground"],
      "verify": ["ul.icons li a.icon.style2"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css Icon block (deployed); measured on elements.html"}
  },
  {
    "id": "component/emblem-logo",
    "kind": "component",
    "title": "Emblem & wordmark lock-up",
    "summary": "Header lock-up: round emblem images/logo.svg rendered at 2em (32×32px) + wordmark in 900 uppercase with 0.35em tracking, colour = page ink (pink on most pages). Per-page wordmarks differ (site title vs template 'Phantom').",
    "aliases": ["logo", "emblem", "symbol", "wordmark", "site title"],
    "body": {
      "class": "#header .logo .symbol img + .title",
      "group": "Header",
      "spec": ["symbol 2em×2em, margin-right 0.65em", "wordmark 900, uppercase, letter-spacing 0.35em", "lock-up margin-bottom 2.5em"],
      "verify": ["#header .logo"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css Header/logo; measured on index.html & elements.html"}
  },
  {
    "id": "component/nav-hamburger",
    "kind": "component",
    "title": "Nav trigger (hamburger plate)",
    "summary": "Fixed top-right 4em×3em (64×48px) plate, background rgba(255,255,255,0.5), radius 4px, no visible label (text-indent hidden). Icon = inline 3-line SVG: grey #585858 layer default, pink #f2849e layer revealed on hover (opacity swap). Trigger for the #menu panel.",
    "aliases": ["hamburger", "menu button", "nav toggle", "menu trigger"],
    "body": {
      "class": "#header nav ul li a[href='#menu']",
      "group": "Header",
      "states": ["default: grey lines on white-50% plate", "hover: pink lines"],
      "verify": ["#header nav a[href='#menu']"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css Header nav; measured on index.html"}
  },
  {
    "id": "component/menu-panel",
    "kind": "component",
    "title": "Menu panel (neon green slide-in)",
    "summary": "Slide-in nav panel: 22em (352px, max 80%) fixed right, full height, ground #3ef900 neon green (override of the template's #585858) with black text; inner padding 2.75em; heading in tracked caps; list links black, 1em 0 padding, no underline, item separators remain the template's rgba(255,255,255,0.15) top rules (low-visibility on green). Opening (body.is-menu-visible) slides it in and dims #wrapper to opacity 0.25 (measured #585858 → rgb(214,214,214) over white). Close control = X icon (SVG) placed 6em left of the panel, grey #585858 → pink on hover.",
    "aliases": ["menu", "slide-in menu", "nav panel", "menu overlay", "close menu"],
    "body": {
      "class": "#menu > .inner",
      "group": "Navigation",
      "states": ["closed: translateX(22em), hidden", "open: translateX(0); page dimmed to 25% opacity (screenshot comp-menu-open-1280.png)", "close control: grey X → pink on hover"],
      "verify": ["#menu", "body.is-menu-visible #wrapper"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css Menu block (deployed); measured on index.html"}
  },
  {
    "id": "component/carousel-gallery",
    "kind": "component",
    "title": "Random gallery carousel (index)",
    "summary": "Auto-advancing single-image carousel added on index: #carouselGallery (max-width 1200, centred), one item at a time = img fixed 640×360 object-fit cover + tracked-caps pink h3 title (+ empty desc p). DOM item replaced every 4000ms by inline script; controls removed; no hover states. Two captured states: 'ILIGHTUUP' and 'SEA, SENSE, AND MELODY'.",
    "aliases": ["carousel", "random gallery", "gallery slider", "autoplay gallery"],
    "body": {
      "class": "#carouselGallery .carousel-item",
      "group": "Content",
      "states": ["state A: ILIGHTUUP (comp-index-carousel-a-1280.png)", "state B: SEA, SENSE, AND MELODY (comp-index-carousel-b-1280.png)", "auto-advance 4s, no controls"],
      "flaws": ["fixed 640px image + fixed 700px collage cause document overflow at 390 (scrollWidth 700 vs 390)", "mirror lacks randomgallery assets; live URLs 200"],
      "verify": ["#carouselGallery"]
    },
    "source": {"repo": "zhenyoyo.github.io index.html inline script/styles", "path": "index.html L82-86, L260-305; measured on index.html"}
  },
  {
    "id": "component/footer-block",
    "kind": "component",
    "title": "Footer blocks (contact, follow, copyright)",
    "summary": "Footer: ground #f6f6f6, padding 5em 0 3em; two flex sections (66% / 33%): 'Get in touch' (underline fields + primary submit on elements/generic/publication; index shows a plain email line instead) and 'Follow' (style2 icon chips). Full-width copyright at 0.8em rgba(88,88,88,0.5) with 1px rgba(88,88,88,0.15) left-rule separators between items.",
    "aliases": ["footer", "contact form", "follow row", "copyright"],
    "body": {
      "class": "#footer > .inner",
      "group": "Footer",
      "states": ["form variant (send button)", "index text-email variant"],
      "verify": ["#footer"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css Footer block; measured on elements.html"}
  },
  {
    "id": "component/blockquote",
    "kind": "component",
    "title": "Blockquote",
    "summary": "Italic pull-quote with a 4px #c9c9c9 left rule, padding 0.5em 0 0.5em 2em, no quotation marks; text colour inherits the page ink (pink on elements).",
    "aliases": ["blockquote", "pull quote", "quote"],
    "body": {
      "class": "blockquote",
      "group": "Content",
      "verify": ["blockquote"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css type block; measured on elements.html"}
  },
  {
    "id": "component/code-pre",
    "kind": "component",
    "title": "Code & preformatted (blue chip)",
    "summary": "Inline code: Courier New 0.9em (14.4px), padding 0.25em 0.65em, 1px #c9c9c9 border, radius 4px, ground rgba(46,90,249,0.986) — a solid royal-blue chip (override of the template's grey tint) with pink text. Pre blocks stay transparent, no border, 1.75 line-height, horizontal scroll.",
    "aliases": ["code", "code block", "preformatted", "monospace", "snippet"],
    "body": {
      "class": "code / pre",
      "group": "Content",
      "verify": ["code", "pre"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css type block (deployed ground); measured on elements.html"}
  },
  {
    "id": "component/hr",
    "kind": "component",
    "title": "Horizontal rule",
    "summary": "1px #c9c9c9 rule with 2em vertical margin; the content divider used across the site.",
    "aliases": ["rule", "divider", "separator", "hr"],
    "body": {
      "class": "hr",
      "group": "Content",
      "verify": ["hr"]
    },
    "source": {"repo": "zhenyoyo.github.io (HTML5 UP Phantom deployment)", "path": "main.css type block; measured on elements.html"}
  },
  {
    "id": "rule/state-pink",
    "kind": "rule",
    "name": "state-colour-pink",
    "severity": "info",
    "applies_to": ["css"],
    "aliases": ["hover pink", "focus pink", "state colour", "interaction colour", "f2849e"],
    "summary": "One interaction-state colour: #f2849e. It is the hover label+ring on buttons, the focus underline on fields/selects/textareas, the hover glyph+border on icon chips, the :active ground (10% alpha), and a:hover for links (with a border-bottom-colour reset). Rendered as-is from the template on the deployment.",
    "why": "Measured across every interactive control; single accent keeps state language coherent. Contrast on white: 2.45:1 (state emphasis only, not text-role).",
    "fix": "n/a (observational)",
    "verify": [".button:hover", "input:focus", ".icon.style2:hover", "a:hover"]
  },
  {
    "id": "rule/radius-flattening",
    "kind": "rule",
    "name": "radius-flattening",
    "severity": "info",
    "applies_to": ["css"],
    "aliases": ["radius", "corner radius", "0px", "flattening", "border-radius"],
    "summary": "Deployment flattens the template's 4px radius family to 0px on: checkbox boxes, .box, .image spans, .icon.style2 chips, and .tiles article > .image. Radios stay 100% circles; buttons, code chips, and the header nav plate keep 4px.",
    "why": "Measured via css-diff + computed styles; describes what is in play rather than a defect judgement (flaw ledger holds the UX observations).",
    "fix": "n/a (observational)",
    "verify": [".icon.style2", ".image", ".tiles article > .image", "input[type=checkbox]+label:before"]
  }
]
```

## Flaw observations (measured; for the gap ledger — observations only, no fixes)

1. **Tile hover hides the work.** Hovering any project tile covers the photo with an opaque
   `#eb84da` wash (pixel histogram: 97.6% of the tile is exactly (235,132,218)); the only
   visible content is the white caption, at **2.37:1** contrast. Combined with the removed
   zoom, the tile reads as a flat pink square on hover. — OBSERVED-CSS + pixel scan of
   `comp-index-tile-hover-1280.png`.
2. **Four of six tile veils are invisible at rest.** `style1`/`style2` (and unclassed tiles
   on index) carry `#efc5e900` / `#ffe2e500` — 8-digit hex with **alpha 0**; `style4–6`
   `#ffe2e524` and `style3` `#746ffa28` are faint. Value pattern suggests "pastel + trailing
   alpha" experiments whose alpha digit landed at 00. — OBSERVED-CSS.
3. **Menu separators are white-15% on neon green.** `border-top: 1px solid
   rgba(255,255,255,0.15)` was tuned for the template's dark panel; on `#3ef900` the rules are
   barely visible (seen as "faint thin lines" in vision). — OBSERVED-CSS + VISUAL.
4. **Menu close control is grey on the dimmed page, outside the panel.** The X (grey
   `#585858` stroke; pink only on hover) sits at `left:-6em` from the panel over the 25%-opacity
   page — it works but is visually detached from the green panel. — OBSERVED-CSS + VISUAL.
5. **Hamburger plate is white-on-white.** `rgba(255,255,255,0.5)` on the white page; only the
   3 grey lines identify it. — OBSERVED-CSS.
6. **Disabled buttons are near-invisible.** `opacity .25` over grey fill renders a faint
   plate; vision flagged it unprompted ("nearly invisible"). — OBSERVED-CSS + VISUAL.
7. **Radio checked state uses a checkmark, not a dot** (shared `\f00c` rule for checkbox and
   radio). — OBSERVED-CSS.
8. **Carousel: no controls, no captions beyond the title, links unwired** (`link:'#'` in data)
   and fixed 640×360 images. At 390px the fixed 640px carousel image plus the inline
   `width:700px` collage produce document overflow (scrollWidth **700** vs clientWidth
   **390**). — OBSERVED-CSS (probe) + OBSERVED-VISUAL (`comp-index-390.png` is 700px wide as a
   result).
9. **Mirror caveat, not a site flaw:** the mirror's `randomgallery/` dir is empty, so the
   carousel captures show a broken-image box; the live URLs return HTTP 200 (curl cross-check).
   Carousel imagery evidence must be re-fetched (or read live) before any pack use. —
   curl + VISUAL.
10. **Dead CSS rule** `.imagemain { width:5%; height:1% }` added by the deployment but used by
    no page's HTML. — search over `*.html` (no matches) + CSS text.
11. **Button focus state undefined** (tab focus falls back to the browser ring); and the
    component set is near-unused in content — the only buttons outside `elements.html` are the
    two form submits. — OBSERVED-CSS + HTML survey.

## Deltas vs the pass-1 pack (context only — pass-1 is not canon)

| pass-1 claim (packs/phantom) | rendered truth (pass 2) |
|---|---|
| tiles: "image zoom (scale 1.1)", "pastel veil by .styleN", "arrow marker", 4px radius | no zoom (`scale(1)`), veil override `#eb84da` opaque, cross/arrow disabled, radius 0 |
| checkbox: "checked: **ink** fill, white mark"; "labels stay ink" | checked fill **red #f51616**; labels **purple #8833e3** |
| icon-row: "icon **circles**" 2.75em, ink ring, hover ink ground | **squares** 2.65em (radius 0), grey hairline, glyph pink, hover pink border |
| field: "transparent ground over the faint tint" | plain white ground (no tint rendered) |
| radius rule P-R2 "Corners are 4px across…" (deployment flattening = error) | flattening is half the rendered system (checkbox/box/image/icon/tile→0; radio/button/code/plate stay 4px) |
| rule P-R1 "Text and UI ink is #585858…" | rendered pages run pink body/headings; ink survives only in buttons/table rules/fields |
| menu (`layout/menu`) on template ground #585858 | panel ground **#3ef900**, black links (override) |

## Open questions

- Are the alpha-00 tile veils (`#efc5e900` etc.) deliberate "no veil" choices or a hex-editing
  slip? The rendered result is identical either way, but the pack should say which value is
  canonical.
- Is the opaque `#eb84da` hover veil intended to fully hide the photo (caption-first hover) or
  meant to be semi-transparent (an alpha suffix dropped)? Evidence cannot decide; the rendered
  fact is opaque.
- Palette roles for menu-green `#3ef900`, check-red `#f51616`, label-purple `#8833e3`,
  code-blue `rgba(46,90,249,0.986)`: one-off experiments or an emerging accent set? (colour
  domain A owns the palette; flagged here because they arrive through component states.)
- `.tiles` hover is `body:not(.is-touch)`-gated: on touch devices the caption shows statically
  (`body.is-touch .content { max-height: 15em }`) — capture on a touch profile was out of
  scope; worth one mobile-device pass before the pack ships hover guidance.
- Should `component/menu-panel` + `component/nav-hamburger` supersede the pass-1 `layout/menu`
  entry, or coexist? (Both describe the same subsystem from different angles.)
- The `#menu` separators and the close-X position are template values kept unchanged on an
  overridden ground — decide whether the pack records them as "in play" (do) or as flaws (log).

## Evidence inventory (screenshots, 17)

Full-page 1280×900 (lazy→full): `comp-index-1280.png`, `comp-elements-1280.png`,
`comp-light-1280.png`, `comp-publication-1280.png`, `comp-generic-1280.png`,
`comp-tame-1280.png`. Full-page 390×844: `comp-index-390.png` (renders 700px wide — overflow,
see flaw 8), `comp-elements-390.png`. State/close-up (all 1280 unless noted):
`comp-elements-btn-hover-1280.png` (pointer-hovered default button: pink ring+label),
`comp-elements-field-focus-1280.png` (focused Name field: pink underline),
`comp-elements-form-1280.png` (select, checked radio/checkbox red fill, purple labels,
textarea, submits), `comp-elements-table-1280.png` (both tables), `comp-elements-icons-hover-1280.png`
(hovered chip pink), `comp-index-tile-hover-1280.png` (opaque pink tile hover),
`comp-menu-open-1280.png` (open green panel + dimmed page), `comp-index-carousel-a-1280.png`
& `comp-index-carousel-b-1280.png` (two carousel states). Raw probe dump:
`~/.hermes/cache/scratch/phantom-probes.json` (transient; values transcribed above).


