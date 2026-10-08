# phantom redo — extraction charter (v2, screenshot-first, domain teams)

## Why this redo exists

Pass 1 derived the authority from the TEMPLATE's CSS text and demoted the
deployment's visual language to "deviations" — while the site that actually
exists runs **pink type everywhere** (live-measured: body/h1/h2/links all
`rgb(255,107,188)` on `index.html` and `elements.html`; per-page overrides
make `light.html` black-bodied with a pink h1). Pass 1 also never rendered the
site correctly (its local serve 404'd the assets) and barely used screenshots.
**Rejected.**

**Pass 2 rule #1: extract what the site IS, from what it LOOKS LIKE.** The
rendered site is the primary evidence. Flaws (contrast, inconsistency) are
recorded as *flaw observations with measurements* — never silently "corrected".

## Sources (all local; read-only)

| what | where |
|---|---|
| **Renderable mirror** (serve this) | `docs/synthesis/phantom/_raw/site/` — all 9 pages + assets + images |
| Live site (cross-check only) | https://zhenyoyo.github.io/ |
| Template substrate (base system) | `docs/synthesis/phantom/_raw/upstream/` (+ `css-diff.txt` = deployed vs upstream) |
| Pass-1 material (context, NOT canon) | `docs/synthesis/phantom/synthesis-notes.md` |
| Pack under revision | `packs/phantom/` |

Serve: `cd docs/synthesis/phantom/_raw/site && python3 -m http.server <port>`
Browsers: `/home/xrim/design-authority/.venv/bin/python3` with
`PLAYWRIGHT_BROWSERS_PATH=/home/xrim/.cache/ms-playwright` (playwright synced API).

## Method (every team, every page in scope)

1. **Screenshot**: full-page, at **1280×900** and **390×844** →
   `docs/synthesis/phantom/evidence/screens/<domain>-<page>-<width>.png`
   (use `full_page=True`).
2. **Look at every screenshot** with the vision_analyze tool; write down what
   it shows in plain language (colours of type, weights, densities, oddities).
3. **Measure**: computed-style + geometry probes for exact values.
4. **Tag evidence**: `OBSERVED-CSS` (measured) · `OBSERVED-VISUAL` (seen in a
   screenshot, cite file) · `INFERRED` (conclusion). Compare against the
   substrate to mark each value: `BASE` (template) or `OVERRIDE` (deployment).
   Overrides are the design decisions in play — extract them fully, including
   per-page inline styles.

## Deliverables (per team)

`docs/synthesis/phantom/domains/<a|b|c|d>-<domain>.md` containing:
- summary (≤ 15 lines);
- findings tables (token/notation value · where used · BASE/OVERRIDE · evidence tag · screenshot ref);
- per-page variance notes;
- **proposed pack entries** as fenced JSON: `{id, kind, title, summary, aliases, body, source}` (pack schema: mirror `packs/wink` conventions — one object per artifact/rule/fallback/candidate);
- **flaw observations** (measured) — for the gap ledger, phrased as observations;
- open questions.

Final reply to the orchestrator: compact only — domain · #screenshots ·
#proposed entries · top-3 findings · report path.

## Hard rules

- Writes ONLY under `docs/synthesis/phantom/domains/` and
  `docs/synthesis/phantom/evidence/`. Everything else is read-only
  (`_raw/` incl. the mirror, `packs/`, `examples/`, other teams' files).
- Do not fabricate measurements; every numeric claim needs OBSERVED-CSS or a
  screenshot ref.
- No recommendations to "fix" the design in this pass — extraction first.

## Domain charters

- **A · colour-and-surfaces**: every colour in use (values + sources), the pink
  family + the neon set, roles per page (what is coloured: body/h1/h2/links/
  code/labels/menu/buttons/tiles), surfaces (grounds, tints, scrims), contrast
  measurements for text roles, the per-page override story (light.html etc.),
  the bilibili embed's visual footprint on index if visible.
- **B · typography-and-language**: families actually rendering (incl. any CJK
  fallback behaviour), the scale (sizes/weights/tracking/case per level),
  line-height + measure, pink-vs-black type per page, mixed CN/EN rendering,
  button/table/heading voice, small-print styles.
- **C · components-and-states**: buttons (all variants seen), fields/selects/
  checkboxes (incl. red checked fill + purple labels), tables (ruled heads),
  tiles (hover system as deployed: veil colours, zoom state), icon circles +
  emblem, menu overlay (green panel), overlays/carousel (index), email/contact
  blocks. Geometry (radius/padding/heights) + colours + all reachable states
  (hover/focus where capturable) with screenshots.
- **D · layout-pages-motion**: page-by-page structure (full-page screenshots),
  header/menu/footer composition, the nested-doctype + duplicated `#main`
  region on index, the intro/load motion, the autoplay carousel (capture two
  states), per-page menu/wordmark inconsistency, and the WIP/gap sweep
  (lorem, alt text, meta/OG/favicon, inline styles inventory).
