#!/usr/bin/env python3
"""build_phantom_pack — emit packs/phantom/*.json from the synthesis ledger.

Canon = the Phantom design system (upstream template, CCA 3.0), corroborated by
deployed computed styles. Deployment deviations are NOT canon (see
docs/synthesis/phantom/synthesis-notes.md, D1). Run: python3 this; then
`da.py --pack packs/phantom validate|overview|golden`.
"""
import json
import os

REPO = "/home/xrim/design-authority"
OUT = os.path.join(REPO, "packs", "phantom")
os.makedirs(OUT, exist_ok=True)

UP = "upstream Phantom (html5up.net, CCA 3.0) as deployed at zhenyoyo.github.io; archived docs/synthesis/phantom/_raw/"
DEP = "deployment observation 2026-10-08 (computed + archived sources)"

S = lambda path: {"repo": "HTML5 UP Phantom + zhenyoyo.github.io deployment", "path": path}


def A(aid, kind, title, summary, aliases, body, source, compiled_from, status="stable"):
    if isinstance(source, str):
        source = S(source)
    return {"id": aid, "kind": kind, "title": title, "summary": summary, "status": status,
            "aliases": aliases, "body": body, "source": source, "compiled_from": compiled_from}


# ------------------------------------------------------------- authority ----
auth = json.load(open(os.path.join(REPO, "packs", "wink", "authority.json")))
auth.update({
    "id": "phantom", "name": "Phantom Interface System", "version": "0.1.0",
    "snapshot": {"repo": "HTML5 UP Phantom (template, CCA 3.0) as deployed at zhenyoyo.github.io",
                 "commit": "n/a - public sources", "branch": "n/a",
                 "version": "template as published; deployment fetched 2026-10-08",
                 "path_hint": "docs/synthesis/phantom/_raw/"},
    "description": ("A minimal, flat, monochrome-leaning interface system for portfolio and editorial "
                    "pages: Source Sans Pro with tracked uppercase display caps, ink #585858 on white, "
                    "4px radii, inset-ring buttons, underline fields, pastel accent surfaces led by pink, "
                    "a fixed slide-in menu, and a brief load-in motion. Derived from the Phantom template "
                    "as deployed at zhenyoyo.github.io; the deployment's value edits are recorded as "
                    "improvisations (see synthesis-notes), never canon."),
})
json.dump(auth, open(os.path.join(OUT, "authority.json"), "w"), indent=1)

scoring = json.load(open(os.path.join(REPO, "packs", "wink", "scoring.json")))
scoring["source"] = "docs/synthesis/phantom/synthesis-notes.md"
json.dump(scoring, open(os.path.join(OUT, "scoring.json"), "w"), indent=1)

# ------------------------------------------------------------- artifacts ----
artifacts = [
    A("token-set/type", "token-set", "Type set — Source Sans Pro",
      "One family, three voices: body 12pt/300 (light; ≈16px observed), display sentence-case h1 44px/700/-0.035em, and tracked caps (uppercase 900, letter-spacing 0.35em) for h2-h4, buttons, and table heads. Headings shrink through breakpoints (2.75em → 2em → 1.75em for h1).",
      ["type", "typography", "fonts", "heading style", "source sans pro", "type scale", "site title typography"],
      {"group": "Foundations",
       "scale": [
           "body 12pt/300 (light), line-height 1.75 (observed 16px/28px at 1265w)",
           "h1 2.75em/700, line-height 1.3, letter-spacing -0.035em (sentence case; 44px observed)",
           "h2 1.1em/900, uppercase, letter-spacing 0.35em (17.6px observed)",
           "h3 1em/900, uppercase, 0.35em (16px observed)",
           "h4 0.8em/900, uppercase, 0.35em (12.8px observed)"],
       "verify": ["h1", "h2", "body"],
       "a11y": ["Uppercase tracked caps are for short labels/heads only, never for running text."]},
      S("upstream main.css L119-317 (Type); observed on deployment"), ["phantom-type-01"], "stable"),

    A("token-set/colour", "token-set", "Colour set — ink, ground, tint, pink-led accents",
      "Ink #585858 on white; faint grey tint rgba(144,144,144,.075) for fields/code; line #c9c9c9 and #f0f0f0 for borders/rules; footer ground #f6f6f6. Accents are SURFACES, led by pink #f2849e (hover text/ring, focus underline), plus the six tile pastels (#f2849e, #7ecaf6, #7bd0c1, #c75b9b, #ae85ca, #8499e7). Text runs in ink, never in accents.",
      ["colour", "color", "palette", "ink", "accents", "pastels"],
      {"group": "Foundations",
       "tokens": [
           "ink #585858; strong ink #494949; white #ffffff; ground #f6f6f6 (footer)",
           "tint rgba(144,144,144,0.075); lines #c9c9c9 / #f0f0f0",
           "accent pink #f2849e (hover text + ring, focus underline); tile pastels style1-6"],
       "deployment_note": "deployment re-inks text #ff6bbc / links #6bff2c and repaints surfaces — recorded as improvisations, not canon (contrast: pink-on-white ≈2.1:1).",
       "verify": ["body", "a"],
       "a11y": ["Accent colours appear as hover/focus/graphic surfaces; body text stays ink for contrast."]},
      S("upstream main.css (Basic/Type/Button/Form/Tiles blocks)"), ["phantom-colour-01"], "stable"),

    A("component/action-button", "component", "Button (ink ring, tracked caps)",
      "The system's action: uppercase 900 tracked-caps label at 0.8em, 3.5em tall, 4px radius, 2px ink ring drawn as `box-shadow: inset 0 0 0 2px #585858` on transparent ground; hover flips label+ring to pink #f2849e. Primary = solid ink ground, white label (hover: pink ground). Small 0.6em / large 1em; `.fit` sizes to content; `.icon` carries a leading glyph.",
      ["button", "primary button", "cta", "action", "submit button", "small button", "large button", "fit button", "icon button"],
      {"class": "button (.primary .small .large .fit .icon)",
       "group": "Actions",
       "states": [
           "default: transparent, ink label + inset 2px ink ring (radius 4)",
           "hover: label + ring #f2849e; active: slightly darker ring",
           "primary: ink ground, white label; hover ground #f2849e",
           "small 0.6em | large 1em | fit auto width | icon leading glyph | disabled opacity .25"],
       "spec": ["height 3.5em, line-height 3.45em, padding 0 1.25em 0 1.6em",
                "font-size 0.8em, weight 900, letter-spacing 0.35em, uppercase",
                "transition background-color/color/box-shadow 0.2s ease-in-out"],
       "verify": [".button", ".button.primary", ".button.small"],
       "a11y": ["Real <button>/<a> semantics; focus must remain visible (template: focus ring on fields; buttons inherit UA focus by default)."]},
      "upstream main.css L2451-2574 (Button)", ["phantom-button-01"], "stable"),

    A("component/field", "component", "Field (underline input)",
      "Text-like inputs and textareas: transparent ground over the faint tint, no box and no radius — a single 1px #c9c9c9 bottom line; focus trades the line for a 2px pink underline (`inset 0 -1px 0 0` + reset). Half/third/quarter width variants live in `.fields > .field`.",
      ["text field", "input", "form field", "email field", "textarea", "contact form", "underline input"],
      {"class": "input[type=text|email|tel|password], textarea",
       "group": "Form",
       "states": ["default: tint ground, 1px #c9c9c9 bottom line, flat (radius 0)", "focus: pink #f2849e underline", "invalid: platform default (undefined by system)"],
       "layout": [".fields flex wrap; .field.half 50%, .third 33%, .quarter 25%"],
       "verify": ["input[type=text]", "textarea"],
       "a11y": ["Placeholders are examples, not labels; provide visible labels where possible."]},
      "upstream main.css L2057-2197 (Form)", ["phantom-field-01"], "stable"),

    A("component/select", "component", "Select (styled, underline)",
      "Native select restyled to the field language (tint ground, bottom line, 4px radius, appearance:none); options carry the system font. Use where a short list of choices is needed.",
      ["select", "dropdown", "dropdown select", "choose option", "category picker"],
      {"class": "select", "group": "Form",
       "states": ["default like fields", "focus: pink underline (same as field)"],
       "verify": ["select"]},
      "upstream main.css L2100-2197 (Form/select)", ["phantom-select-01"], "stable"),

    A("component/checkbox-radio", "component", "Checkbox & radio (custom mark)",
      "Custom checkboxes/radios drawn with `+ label:before` boxes (2.25em); checked fills ink with a white mark; focus adds a 1px pink ring. Labels stay ink and readable at a glance.",
      ["checkbox", "radio", "toggle", "option mark", "check box", "radio button", "consent", "consent checkbox", "agree to terms", "opt in"],
      {"class": "input[type=checkbox|radio] + label", "group": "Form",
       "states": ["unchecked: ink 7.5% box + ink outline", "checked: ink fill, white mark", "focus: 0 0 0 1px #f2849e ring"],
       "verify": ["input[type=checkbox]", "input[type=radio]"]},
      "upstream main.css L2198-2292 (Form/checkbox+radio)", ["phantom-check-01"], "stable"),

    A("component/actions", "component", "Actions row (ul.actions)",
      "A horizontal group of buttons/links (ul.actions), right-aligned by default with 1em gaps; `.fixed` stacks full-width; supports spacer items. The standard footer/hero action cluster.",
      ["button row", "action row", "submit row", "form actions", "button group"],
      {"class": "ul.actions (.fixed)", "group": "Actions",
       "verify": ["ul.actions"]},
      "upstream main.css L1921-2042 (Actions)", ["phantom-actions-01"], "stable"),

    A("component/table", "component", "Table (ruled, tracked-caps head)",
      "Default and `.alternate` tables: full width, 2em bottom margin; heads at 0.9em/900 with a 2px #c9c9c9 header rule; tinted alternate rows. `.table-wrapper` provides horizontal scroll on small screens (broken on the deployment — the comment edit killed the selector).",
      ["table", "data table", "spec table", "rows", "alternate table", "ruled table"],
      {"class": "table / .table-wrapper", "group": "Content",
       "states": ["default: 1px #f0f0f0 row rules", "alternate: tinted rows", "wrapper: overflow-x auto"],
       "verify": ["table", ".table-wrapper"]},
      "upstream main.css L2373-2444 (Table)", ["phantom-table-01"], "stable"),

    A("component/tiles", "component", "Tiles (project grid)",
      "The portfolio's heart: a responsive grid of image tiles (3-up, 2-up small, 1-up xsmall). Each tile = `.image` (4px radius) + hover system: content panel slides up (max-height/opacity 0.45s), pastel veil by `.styleN`, arrow marker fades out; non-touch hover zooms the image (scale 1.1). `.is-preload` staggers tiles in from scale(0.9).",
      ["tiles", "project grid", "portfolio grid", "photo grid", "image cards", "project cards"],
      {"class": "section.tiles", "group": "Content",
       "structure": ["article > .image (picture) + a > h2 + .content (copy revealed on hover)"],
       "styles": ["style1 pink #f2849e", "style2 blue #7ecaf6", "style3 teal #7bd0c1", "style4 magenta #c75b9b", "style5 purple #ae85ca", "style6 periwinkle #8499e7"],
       "states": ["rest: arrow marker", "hover: veil + copy panel + image zoom (desktop only)"],
       "verify": [".tiles", ".tiles article"]},
      "upstream main.css L2575-2842 (Tiles)", ["phantom-tiles-01"], "stable"),

    A("component/blockquote", "component", "Blockquote",
      "Italic pull-quote with a 4px #c9c9c9 left rule, 2em clearance and 2em item spacing; no quotation glyphs.",
      ["blockquote", "quotation block", "pull quote", "quote"],
      {"class": "blockquote", "group": "Content", "verify": ["blockquote"]},
      "upstream main.css L119-317 (Type/blockquote)", ["phantom-quote-01"], "stable"),

    A("component/code-pre", "component", "Code & preformatted",
      "Inline code sits on the faint tint with a 1px #c9c9c9 border and 4px radius (Courier New); pre blocks pad 1em 1.5em, line-height 1.75, horizontal scroll. On the deployment the inline ground became a solid blue block.",
      ["code block", "code sample", "preformatted", "monospace", "snippet"],
      {"class": "code / pre", "group": "Content", "verify": ["code", "pre"]},
      "upstream main.css L119-317 (Type/code,pre)", ["phantom-code-01"], "stable"),

    A("component/lists", "component", "Lists (default, alt, ordered)",
      "Unordered lists with disc marks and 2em spacing; the alternate variant drops the marks; ordered lists use decimal counters. Lists are content primitives, not UI.",
      ["bulleted list", "list", "ordered list", "numbered list", "alternate list"],
      {"class": "ul / ul.alt / ol", "group": "Content", "verify": ["ul", "ol"]},
      "upstream main.css L1870-1920 (List)", ["phantom-list-01"], "stable"),

    A("component/image", "component", "Image treatments",
      "Images are structural: `.image.main` full-column block (2em margins), `.image.fit` content-width block, `.left`/`.right` floats at 40%/40% with 2em gutter. All carry the 4px radius.",
      ["image", "full width image", "left image", "right image", "photo", "figure"],
      {"class": ".image (.main .fit .left .right)", "group": "Content", "verify": [".image.main"]},
      "upstream main.css L2314-2444 (Box/Image)", ["phantom-image-01"], "stable"),

    A("component/icon-row", "component", "Icon (circles) & social row",
      "Circular icon buttons (2.75em circles, ink ring) for social links, plus the icons list (ul.icons) for inline rows; icons come from the bundled Font Awesome set.",
      ["icons", "social icons", "social media icons", "icon circle", "follow row"],
      {"class": ".icon (solid|brands) / ul.icons", "group": "Content",
       "states": ["default: ink ring, ink glyph", "hover: ink ground, white glyph"],
       "verify": ["ul.icons", ".icon"]},
      "upstream main.css L1804-2056 (Icon/Icons)", ["phantom-icon-01"], "stable"),

    A("layout/header", "layout", "Header & logo",
      "A centered header: circular logo symbol (image) + wordmark title, with a single 'Menu' link to the overlay. Sits over the page, fades with the load-in.",
      ["header", "site header", "logo", "brand", "top bar", "site header with logo"],
      {"class": "#header", "group": "Layout",
       "structure": ["a.logo > .symbol (circle, ~3em) + .title (wordmark)"],
       "verify": ["#header", "#header .logo"]},
      "upstream main.css L2843-2978 (Header)", ["phantom-header-01"], "stable"),

    A("layout/menu", "layout", "Menu overlay (slide-in)",
      "The signature navigation: a fixed 22em right-edge panel, ink ground, white links in a bordered list (0.15 white rules), 0.45s ease slide + fade; `body.is-menu-visible` reveals it; click-away/Escape closes. Deployment recoloured the panel neon green.",
      ["menu", "main menu", "navigation", "nav overlay", "slide menu", "the main menu"],
      {"class": "#menu / #wrapper", "group": "Layout",
       "states": ["hidden: translateX(22em), visibility hidden", "visible: translateX(0), inner opacity 1 (0.45s ease)"],
       "structure": ["#menu > .inner > h2 'Menu' + ul of links (1px rgba(255,255,255,.15) rules)"],
       "verify": ["#menu"]},
      "upstream main.css L2979-3164 (Menu) + main.js", ["phantom-menu-01"], "stable"),

    A("layout/footer", "layout", "Footer (2 sections + copyright)",
      "Grey ground #f6f6f6; two columns (66% / 33%): left = contact block (form), right = follow block (icon row); full-width copyright bar in 0.8em ink-50%.",
      ["footer", "contact block", "follow block", "copyright", "footer contact section"],
      {"class": "#footer", "group": "Layout", "verify": ["#footer"]},
      "upstream main.css L3179-3327 (Footer)", ["phantom-footer-01"], "stable"),

    A("layout/page-intro", "layout", "Load-in motion (is-preload)",
      "A brief entrance: `body.is-preload` hides the wrapper (opacity 0) and holds tiles at scale(0.9); on load the class drops and the system fades/slides in over 0.45s ease. All other animation/transition is disabled during preload. This is the system's ONLY sanctioned motion.",
      ["page load animation", "intro animation", "fade in", "load transition", "entrance motion", "page load fade-in"],
      {"class": "body.is-preload", "group": "Layout",
       "spec": ["#wrapper opacity transition 0.45s ease (0 → 1)", "tiles article scale 0.9 → 1 stagger", "is-preload disables all other animation/transition"],
       "verify": ["body"]},
      "upstream main.css (is-preload blocks) + main.js", ["phantom-intro-01"], "stable"),

    A("component/hr", "component", "Horizontal rule",
      "A 1px #c9c9c9 rule with 2em vertical margin; the system's default content divider.",
      ["rule", "divider", "horizontal rule", "separator", "hr"],
      {"class": "hr", "group": "Content", "verify": ["hr"]},
      "upstream main.css L119-317 (Type/hr)", ["phantom-hr-01"], "stable"),
]

# ---------------------------------------------------------------- rules ----
rules = [
    {"id": "P-R1", "name": "ink-text-policy", "severity": "warning", "applies_to": ["css"],
     "summary": "Text and UI ink is #585858 on white; saturated colour arrives only through sanctioned surfaces (hover/focus states, tile pastels, menu ground).",
     "why": "The template's monochrome reading surface is its design identity; colour-as-surface keeps contrast safe (pink #ff6bbc on white ≈ 2.1:1).",
     "fix": "Return text colours to ink; move accent ambitions into hover/focus/surface roles or the pink-accent candidate."},
    {"id": "P-R2", "name": "radius-family", "severity": "error", "applies_to": ["css"],
     "summary": "Corners are 4px across buttons, fields, boxes, images and tiles (circles only for logo/icon discs).",
     "why": "One radius family ties the system together; the deployment flattened everything to 0px.",
     "fix": "Restore border-radius: 4px on affected components (or re-open the radius decision as a candidate)."},
    {"id": "P-R3", "name": "tracked-caps-display", "severity": "warning", "applies_to": ["css", "html"],
     "summary": "Display labels (h2-h4, buttons, table heads) are uppercase 900 with 0.35em letter-spacing; h1 stays sentence case 700.",
     "why": "Observed across type, buttons and heads; the tracking is the system's typographic signature.",
     "fix": "Apply uppercase/900/0.35em to display labels; never apply caps-tracking to running text."},
    {"id": "P-R4", "name": "flat-inset-rings", "severity": "warning", "applies_to": ["css"],
     "summary": "Depth is drawn with inset rings (`inset 0 0 0 Npx`) and rules — never blurred or elevated shadows.",
     "why": "No blurred shadow exists in the template; borders-as-shadows keep the flat surface honest.",
     "fix": "Replace drop shadows with inset rings or 1px rules."},
    {"id": "P-R5", "name": "underline-fields", "severity": "warning", "applies_to": ["css"],
     "summary": "Fields are underline-only: tint ground, 1px #c9c9c9 bottom line, pink underline on focus.",
     "why": "The form language is minimal by design; boxes around fields would break the page rhythm.",
     "fix": "Strip field box borders; keep the bottom line + focus underline."},
]

# --------------------------------------------------------- prohibitions ----
prohibitions = [
    {"id": "prohibit/blurred-shadows", "statement": "Blurred/drop elevation shadows — depth is inset rings and rules only (P-R4).",
     "signals": ["drop shadow", "box shadow blur", "elevation", "soft shadow", "card shadow", "glow"],
     "rule": "P-R4", "kind": "prohibition"},
    {"id": "prohibit/neon-text", "statement": "Neon or saturated colour as body/UI text ink (text runs in #585858; colour is a surface behaviour).",
     "signals": ["neon text", "pink text", "green links", "bright text", "colored text", "coloured text", "rainbow"],
     "rule": "P-R1", "kind": "prohibition"},
    {"id": "prohibit/square-strays", "statement": "Corners outside the 4px family (squared components break the radius system — P-R2).",
     "signals": ["square corners", "sharp corners", "zero radius", "border-radius: 0", "squared"],
     "rule": "P-R2", "kind": "prohibition"},
]

# ------------------------------------------------------------ fallbacks ----
fallbacks = [
    {"id": "fallback/platform-controls", "kind": "fallback",
     "title": "Platform defaults for uncovered controls",
     "statement": "If the system defines no control for a need, use the platform's native element restyled to the field language (tint ground, #c9c9c9 lines, 4px radius, ink text); keep native semantics.",
     "scope": ["date", "time", "file", "slider", "range", "color", "picker", "upload", "stepper", "switch", "combobox"],
     "constraints": ["field language (underline, 4px radius, ink)", "mark the improvisation and file a gap if it recurs"]},
    {"id": "fallback/no-script", "kind": "fallback",
     "title": "No-JS fallback (noscript stylesheet)",
     "statement": "Without JavaScript, the load-in is skipped and content renders immediately (noscript.css lifts the is-preload state).",
     "scope": ["motion", "intro", "menu", "javascript"],
     "constraints": ["content readable without JS", "menu degrades to in-page anchor (undefined beyond that)"]},
    {"id": "fallback/light-only", "kind": "fallback",
     "title": "Light ground only",
     "statement": "No dark mode is defined; dark contexts are outside this authority (undecided, not declined).",
     "scope": ["dark", "dark mode", "theme", "contrast mode"],
     "constraints": ["file a gap if a dark requirement appears"]},
]

# ----------------------------------------------------------- precedents ----
precedents = [
    {"id": "precedent/declined-neon-reading-ink",
     "kind": "precedent",
     "title": "Neon accent colours as reading ink",
     "request": "body/UI text in the deployment's neon palette (#ff6bbc text, #6bff2c links) as a design direction",
     "matches": ["neon text", "pink text", "green links", "bright colour text"],
     "decision": "declined",
     "grounds": "readability + monochrome reading surface (P-R1); neon-on-white fails contrast (pink ≈2.1:1, green ≈1.3:1)",
     "reason": "Text ink is a reading surface; the system carries colour through hover/focus states and tile pastels. A promoted pink accent remains available via the candidate pathway.",
     "scope": {"domains": ["css", "html"], "boundary": ["body copy", "long-form text", "reading surface"]},
     "try": ["use ink text and move the pink to hover/focus/surface roles",
             "or promote the pink-accent candidate with an AA-checked role map"],
     "citation": "upstream main.css (ink #585858 text; pink #f2849e hover/focus accent)",
     "provenance": {"source": "adjudication-observation", "note": "documented from the deployment deviation ledger, 2026-10-08"}},
]

# ----------------------------------------------------------- candidates ----
candidates = [
    {"id": "candidate/pink-accent-system", "kind": "candidate",
     "title": "Pink accent system (provisional)",
     "request": "a pink-led accent identity for the portfolio",
     "matches": ["pink accent", "pink theme", "accent colour", "accent color", "brand pink", "neon pink"],
     "status": "candidate",
     "summary": "Promote the template's own pink family (#f2849e hover/focus accent; darker AA-safe derivate for text roles) into a small sanctioned accent system: one accent, roles = hover / focus underline / marker / link underline colour.",
     "emerges_from": ["deployment deviation ledger (body #ff6bbc, links #6bff2c)"],
     "evidence_present": "Upstream already uses pink as its hover/focus accent (#f2849e) — the ambition exists in the system; only the role mapping and contrast are unresolved.",
     "promote_when": ["a single accent role map is drafted (hover/focus/marker only; never reading ink)",
                      "AA contrast verified (≥4.5:1 for text roles, ≥3:1 for graphics) or a darkened pink chosen",
                      "owner sign-off"],
     "provenance": {"source": "synthesis decision D2 (docs/synthesis/phantom/synthesis-notes.md)"}},
    {"id": "candidate/carousel", "kind": "candidate",
     "title": "Gallery carousel (provisional)",
     "request": "an image carousel for the random gallery",
     "matches": ["carousel", "slideshow", "gallery slider", "image slider", "rotating gallery", "image carousel"],
     "status": "candidate",
     "summary": "Compose a controlled carousel from existing parts: image + caption + small ink buttons for prev/next, no autoplay by default; keep the 4px radius and ink-ring button language.",
     "emerges_from": ["deployment hand-rolled autoplay carousel (subpage inline styles)"],
     "evidence_present": "The template defines no carousel; the deployment built one ad hoc (inline styles, autoplay every 4s, dead prev/next code).",
     "promote_when": ["a motion policy is agreed (no autoplay, or pauses/bounded duration)",
                      "control spec captured (prev/next + position readout)",
                      "static fallback defined"],
     "provenance": {"source": "synthesis decision D3 (docs/synthesis/phantom/synthesis-notes.md)"}},
]

# ------------------------------------------------------------- golden ------
golden = {
    "version": "0.1", "pack_version": "phantom 0.1.0",
    "cases": [
        {"problem": "a primary button", "expect": "RESOLVED", "expect_id": "component/action-button", "note": "Solid ink ground, white label."},
        {"problem": "the main menu", "expect": "RESOLVED", "expect_id": "layout/menu", "note": "Slide-in overlay."},
        {"problem": "site header with logo", "expect": "RESOLVED", "expect_id": "layout/header", "note": "Centered logo + Menu link."},
        {"problem": "a text input for the contact form", "expect": "RESOLVED", "expect_id": "component/field", "note": "Underline field."},
        {"problem": "dropdown select", "expect": "RESOLVED", "expect_id": "component/select", "note": "Styled native select."},
        {"problem": "a checkbox for consent", "expect": "RESOLVED", "expect_id": "component/checkbox-radio", "note": "Custom mark."},
        {"problem": "a data table of publications", "expect": "RESOLVED", "expect_id": "component/table", "note": "Tracked-caps heads."},
        {"problem": "project grid of image tiles", "expect": "RESOLVED", "expect_id": "component/tiles", "note": "The portfolio grid."},
        {"problem": "pull quote in an article", "expect": "RESOLVED", "expect_id": "component/blockquote", "note": "Left-rule quote."},
        {"problem": "a code sample block", "expect": "RESOLVED", "expect_id": "component/code-pre", "note": "Tint + border."},
        {"problem": "bulleted list of materials", "expect": "RESOLVED", "expect_id": "component/lists", "note": "Disc list."},
        {"problem": "a full width image in the article", "expect": "RESOLVED", "expect_id": "component/image", "note": ".image.main."},
        {"problem": "social media icons in the footer", "expect": "RESOLVED", "expect_id": "component/icon-row", "note": "Circle icons."},
        {"problem": "the page fade in on load", "expect": "RESOLVED", "expect_id": "layout/page-intro", "note": "The only sanctioned motion."},
        {"problem": "footer contact section", "expect": "RESOLVED", "expect_id": "layout/footer", "note": "Grey ground, two columns."},
        {"problem": "an image carousel for the gallery", "expect": "UNDEFINED", "note": "No carousel canon — candidate/carousel surfaces."},
        {"problem": "make the text neon pink", "expect": "UNDEFINED", "note": "Surfaces the declined precedent + pink-accent candidate."},
    ],
}

# ------------------------------------------------------------- emit --------
json.dump({"artifacts": artifacts}, open(os.path.join(OUT, "artifacts.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"rules": rules}, open(os.path.join(OUT, "rules.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"prohibitions": prohibitions}, open(os.path.join(OUT, "prohibitions.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"fallbacks": fallbacks}, open(os.path.join(OUT, "fallbacks.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"precedents": precedents}, open(os.path.join(OUT, "precedents.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"candidates": candidates}, open(os.path.join(OUT, "candidates.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"recipes": []}, open(os.path.join(OUT, "recipes.json"), "w"), indent=1, ensure_ascii=False)
json.dump(golden, open(os.path.join(OUT, "golden.json"), "w"), indent=1, ensure_ascii=False)
print(f"emitted packs/phantom: {len(artifacts)} artifacts, {len(rules)} rules, {len(prohibitions)} prohibitions, "
      f"{len(fallbacks)} fallbacks, {len(precedents)} precedents, {len(candidates)} candidates, {len(golden['cases'])} golden cases")
