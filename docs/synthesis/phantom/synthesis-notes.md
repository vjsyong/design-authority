# Phantom synthesis — evidence ledger & decisions (pass 1 — SUPERSEDED)

> **SUPERSEDED by the pass-2 redo (2026-10-08).** Pass 1 canonicalised the
> template's grey ink and misfiled the deployment's pink type as "deviations".
> The owner rejected that frame; pass 2 re-extracted from rendered evidence
> (see `redo-brief.md`, `domains/a–d`, and `packs/phantom` 0.2.0). This file is
> kept for provenance — read it for the substrate inventory, not for canon.

Source: **https://zhenyoyo.github.io** (Zhen Wu / Yoyo, HKUST ISD PhD candidate).
Locally archived evidence in `_raw/` (fetched 2026-10-08):
`index.html`, `elements.html`, `generic.html`, `publication.html`, `light.html`,
`tame.html`, `fafa.html`, `Unlogical.html`, `email.html`, `main.css`,
`noscript.css`, `main.js` + upstream template zip (`upstream/`, "Phantom by
HTML5 UP", CCA 3.0) + `css-diff.txt` (deployment vs upstream, 152 lines).

## 1 · What this site is

An HTML5 UP **Phantom** template deploy: a minimal personal portfolio with a
full element library page (`elements.html`). The base system is coherent and
well-formed (upstream SASS + CSS, ~3.3k lines); the deployment adds content,
per-page inline styles, and a handful of CSS value edits.

## 2 · Deployment deviation ledger (deployed vs upstream)

CSS (`main.css`, line refs from `css-diff.txt`):
1. L122 `body, input, select, textarea` colour `#585858` → **`#ff6bbc`** (neon pink — note: the template's own hover accent is pink `#f2849e`).
2. L151-2 links `#585858` + dotted `rgba(88,88,88,.5)` → **`#6bff2c`** + dotted `rgba(32,163,245,.999)` (green over blue).
3. L273 inline `code` background → **`rgba(46,90,249,.986)`** (blue block).
4. `border-radius: 4px` → **`0px`** at L1845/2254/2283/2293/2314/2321/2597 (buttons, form controls, boxes, images, tiles) — the radius family flattened.
5. L2231 checkbox/radio labels → **`#8833e3`** (purple).
6. L2273 checked-mark fills → **`#f51616`** (red).
7. L3005 `#menu` panel `#585858`/white → **`#3ef900`**/black.
8. Tiles: hover zoom `scale(1.1)` → `scale(1)`; pastel overlays → near-transparent (`#efc5e900` etc.) or `#eb84da` (open pink, opacity 1); overlay `#333333/.35` → `#eb84da/1`.
9. `/* Table */` comment markers deleted → stray `Table` text makes the next selector `Table .table-wrapper` (matches nothing): **the table scroll wrapper rule is dead**.
10. Added: `.imagemain { width:5%; height:1%; }` (unused anywhere); `.publication { color: black; }` (a per-page fix fighting the global pink); `/* // */`, commented-out background `#fbf6fa`.

HTML:
- `index.html`: rewritten for content (Zhen Wu YoYo 圳; projects grid: ILightUUp, Tame, Unlogical Instrument, FAFA, observer/observed, Sea, sense, Orchid, SoundMorphTPU; random gallery carousel w/ autoplay; footer contacts). Contains a **nested `<!DOCTYPE html><html><head>…` block inside `<body>`** (lines 58-67), an unclosed stray `</h1>`, commented-out headings, inline styles (`font-size: small`, `width:700px`), an empty `<span class="image main">` wrapper around whole sections.
- `elements.html`: **byte-identical to upstream** (title still "Elements - Phantom by HTML5 UP", logo still "Phantom") — i.e. the "Game, Design & Development Log" menu entry leads to the untouched template demo.
- Project pages (`light/tame/fafa/Unlogical/email/publication`): cloned template pages with **stock lorem menu links** ("Ipsum veroeros… Elements"), per-page `<style>` blocks and inline styles, e.g. `light.html`: floats-based `.image1` layout, inline pink h1; `publication.html` has a broken title tag `</S></title>`; `generic.html` doubles as About **and** placeholder for 3 project tiles; lorem text remains in the "Sea, sense" card.
- CDN Font Awesome 6.0.0-beta3 loaded on `index.html` only, on top of the bundled FontAwesome (fonts duplicated conceptually).

## 3 · Decisions

- **D1 — Canon = the Phantom system** (upstream template, corroborated by deployed computed styles). The deployment's value edits are **consumer improvisations**: documented as deviations, *not* canonised. Rationale: the template is the designed system; its monochrome ink + 4px radii + pastel accent surfaces are coherent; the edits (neon text on white) fail contrast (pink `#ff6bbc` on white ≈ 2.1:1; green ≈ 1.3:1) and fracture the radius family.
- **D2 — The pink affinity is real, treat it as a pathway.** The template's own accent is pink (`#f2849e` hover, focus underline, tile style1); the deployment pushes pink/turquoise/near-neons into text roles. The system's answer is a **candidate** (`candidate/pink-accent-system`) with a promote_when bar (single role map + AA + owner sign-off), not a scolding.
- **D3 — The carousel is a genuine gap.** The template defines no carousel; the deployment hand-rolls one (inline styles, autoplay, dead prev/next code). Filed as `candidate/carousel` with a motion-policy promote bar.
- **D4 — Provenance-first:** every artifact carries its upstream source ref; every deviation above is cited in the audit app's gap ledger with line refs.
- **D5 — License:** Phantom is CCA 3.0 (attribution kept in the pack's authority snapshot + app footer). No template imagery is redistributed; the audit app is our own build.

## 4 · Gap survey (feeds the audit app)

Design-system: palette crash (9 CSS deviations), radius flattening, dead table-wrapper rule, menu recolour, tile-hover system disabled, double Font Awesome, orphan `.imagemain`, per-page inline styles vs system classes.
Content: elements.html untouched; lorem in "Sea, sense"; generic.html serving 4 roles; empty carousel descriptions; "la la la" copyright; commented-out forms; stock menus on subpages.
Craft: nested doctype in body; stray `</h1>`; broken title tag; inline + per-page styles; dead JS (showPrev/showNext partially unused); FA duplication; inconsistent logo titles ("Zhen Wu YoYo 圳" vs "About Zhen" vs "Back to main" vs "Phantom").
Missing patterns (portfolio-relevant, undefined by the template): project-detail layout (handled by reusing generic.html), carousel controls spec, CN/EN mixed-language policy, active-nav state, alt text discipline (all `alt=""`), meta/OG/description, favicon, motion policy (autoplay carousel vs intro-motion canon).
