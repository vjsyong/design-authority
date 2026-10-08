#!/usr/bin/env python3
"""build_phantom_pack_v2 — emit packs/phantom/*.json (redo, version 0.2.0).

Canon = the DEPLOYED design language of zhenyoyo.github.io, extracted pass-2
(screenshot-first, four domain teams). Pass 1 canonised the template's grey ink
and demoted the deployment's pink type to "deviations" — reversed here.
Every entry is sourced from docs/synthesis/phantom/domains/{a,b,c,d}-*.md with
evidence refs (screens in docs/synthesis/phantom/evidence/screens/).
"""
import json
import os

REPO = "/home/xrim/design-authority"
OUT = os.path.join(REPO, "packs", "phantom")
os.makedirs(OUT, exist_ok=True)

DEP = "zhenyoyo.github.io (HTML5 UP Phantom deployment), rendered mirror docs/synthesis/phantom/_raw/site"
EVID = "docs/synthesis/phantom/evidence/screens"


def S(path, note=None):
    d = {"repo": DEP, "path": path}
    if note:
        d["note"] = note
    return d


def A(aid, kind, title, summary, aliases, body, source, compiled_from, status="stable"):
    if isinstance(source, str):
        source = S(source)
    return {"id": aid, "kind": kind, "title": title, "summary": summary, "status": status,
            "aliases": aliases, "body": body, "source": source, "compiled_from": compiled_from}


# ------------------------------------------------------------- authority ----
auth = json.load(open(os.path.join(REPO, "packs", "wink", "authority.json")))
auth.update({
    "id": "phantom", "name": "Phantom Interface System (deployed language)", "version": "0.2.0",
    "snapshot": {"repo": DEP, "commit": "n/a - public sources", "branch": "n/a",
                 "version": "pass-2 redo 2026-10-08 (screenshot-first, 4 domain teams)",
                 "path_hint": "docs/synthesis/phantom/_raw/site/ (renderable mirror)"},
    "description": ("The interface system of zhenyoyo.github.io as deployed: Source Sans Pro 300/700/900, "
                    "pink reading ink #ff6bbc with neon-green links #6bff2c on a dotted blue underline, "
                    "blue-ground code, a lime slide-in menu, red checked marks with purple labels, "
                    "radius flattened to 0 on marks/boxes/images/chips, ink-ring buttons, underline fields, "
                    "a tiles-only load-in and one interaction pink #f2849e. Contrast failures are recorded "
                    "as measured observations (pass 2 extracted what the site IS; pass 1's grey-ink canon "
                    "was reversed). Per-page black-body overrides are part of the system."),
})
json.dump(auth, open(os.path.join(OUT, "authority.json"), "w"), indent=1, ensure_ascii=False)

scoring = json.load(open(os.path.join(REPO, "packs", "wink", "scoring.json")))
scoring["source"] = "docs/synthesis/phantom/domains/ (a-d) + redo-brief.md"
json.dump(scoring, open(os.path.join(OUT, "scoring.json"), "w"), indent=1)

# ------------------------------------------------------------- artifacts ----
artifacts = [
    # --- foundations ---------------------------------------------------------
    A("token-set/colour", "token-set", "Colour — deployed ink (pink type, neon link, blue code)",
      "Deployed reading ink is pink #ff6bbc (body/h1–h4/footer/table/form text), overriding the template's #585858; content links are neon green #6bff2c with a dotted blue #20a3f5 underline and pink #f2849e hover; code sits on a solid blue rgba(46,90,249,.986) ground in pink; project pages flip body ink to black; the menu panel is lime #3ef900 with black text. Measured: pink-on-white 2.6:1, green-on-white 1.32:1 (recorded, not corrected).",
      ["colour", "color", "palette", "ink", "pink ink", "pink text", "neon", "neon text", "green links", "link colour", "reading colour"],
      {"group": "Foundations",
       "tokens": [
           "reading ink (deployed): #ff6bbc rgb(255,107,188) — body, h1-h4, p, header, footer, th/td, field text, blockquote",
           "link ink: #6bff2c; link underline: dotted 1px #20a3f5; hover ink/focus ring: #f2849e (template accent, still live)",
           "code ground: rgba(46,90,249,.986) ≈ #315df9 with pink code text; 1px #c9c9c9 border",
           "menu panel: ground #3ef900, ink #000",
           "control colours: labels #8833e3; checked fill #f51616 / border #f82121; buttons #585858 + white",
           "grounds: #ffffff (white pages) / #fbfbfb (project pages) / #f6f6f6 (footer)"],
       "contrast": {"pink_on_white": 2.60, "green_on_white": 1.32, "pink_on_code_blue": 1.99,
                    "black_on_menu_green": 14.76, "note": "measured; see prohibition/unreadable-accent-ink"},
       "evidence": [f"{EVID}/colour-index-1280.png", f"{EVID}/colour-elements-1280.png", f"{EVID}/colour-light-1280.png"],
       "verify": ["body", "a", "code", "#menu", "h1"]},
      S("_raw/site/assets/css/main.css L122 (ink), L151-152 (links), code/menu blocks; probes evidence/colour-probe-*.json"),
      ["redo/a"]),

    A("token-set/surfaces", "token-set", "Surfaces — grounds, tints, scrims, panels",
      "Grounds: white #ffffff (default), #fbfbfb (project pages via the shared per-page style block), footer #f6f6f6. Panels: menu #3ef900 (lime), code #315df9 composite. Tile resting veils are collapsed near-transparent (#efc5e900/#ffe2e500 → alpha 0, faint #746ffa28/#ffe2e524); the dark scrim is disabled and hover paints an opaque pink veil #eb84da. Zebra rgba(144,144,144,.075); lines #c9c9c9; menu separators rgba(255,255,255,.15).",
      ["surfaces", "backgrounds", "grounds", "tints", "panel", "overlay", "scrim", "veil", "zebra"],
      {"group": "Foundations",
       "tokens": [
           "grounds: #ffffff / #fbfbfb / #f6f6f6", "menu panel: #3ef900; separators rgba(255,255,255,.15)",
           "code ground: rgba(46,90,249,.986)", "tile rest veils: #efc5e900, #ffe2e500 (α0), #746ffa28, #ffe2e524; hover veil #eb84da opaque",
           "zebra: rgba(144,144,144,.075); borders #c9c9c9"],
       "evidence": [f"{EVID}/colour-elements-1280.png", f"{EVID}/colour-index-1280-menu-open.png", f"{EVID}/comp-index-tile-hover-1280.png"],
       "verify": [".tiles article", "#menu", "code", "table tbody tr"]},
      S("_raw/site/assets/css/main.css (tiles/table/menu blocks); probes evidence/colour-probe-*.json"),
      ["redo/a", "redo/c"]),

    A("token-set/type-scale", "token-set", "Type scale — deployed (Source Sans Pro 300/700/900)",
      "Rendered scale: body 12pt=16px at ≤1280 (18.67px ≤1680, 21.33px above), line-height 1.75. h1 2.75em (44px @1280; 32px ≤736) weight 700, lh 1.3, −0.035em. h2 1.1em (17.6px) 900, uppercase, +0.35em. h3 1em (16px) 900 caps; h4 0.8em (12.8px) 900 caps. Buttons 0.8em/900; table heads 0.9em/900 mixed case; code 0.9em.",
      ["type scale", "font size", "heading size", "body size", "type", "typography"],
      {"group": "Type",
       "bands": {"<=1280": "12pt=16px", "<=1680": "14pt=18.67px", ">1680": "16pt=21.33px"},
       "levels": ["h1 44px/700/-0.035em sentence case", "h2 17.6px/900/0.35em caps", "h3 16px/900 caps", "h4 12.8px/900 caps",
                  "body 16px/300", "buttons 12.8px/900 caps", "th 14.4px/900 mixed", "code 14.4px Courier New"],
       "evidence": [f"{EVID}/type-index-1280.png", f"{EVID}/type-elements-1280.png"],
       "verify": ["body", "h1", "h2", "th", ".button"]},
      S("_raw/site/assets/css/main.css L121-143, L172-231, L2404-2484; probes"),
      ["redo/b"]),

    A("token-set/tracking-and-case", "token-set", "Case & tracking voice",
      "h1 is the only tight voice: sentence case, −0.035em. The caps voice (uppercase + 0.35em + weight 900) runs h2–h6, the wordmark, nav and buttons. Exceptions measured: table heads (900, mixed case), form labels and menu links (300), body (300). Case is CSS-authored — source text stays mixed case.",
      ["letter spacing", "tracking", "uppercase headings", "text transform", "caps"],
      {"group": "Type",
       "values": {"h1": "sentence case, -0.035em", "h2-h6/wordmark/nav/buttons": "UPPERCASE, +0.35em, 900",
                  "table heads": "mixed case, 900", "labels/menu links": "300, no tracking"},
       "evidence": [f"{EVID}/type-index-heading-1280.png"],
       "verify": ["#main h1", "#main h2", "#header .logo .title", ".button"]},
      S("_raw/site/assets/css/main.css L177, L201-207, L2476; probes"), ["redo/b"]),

    A("token-set/text-measure-and-leading", "token-set", "Measure & leading",
      "Body leading 1.75 everywhere. Text column 68em (1008px @1280, ≈150 characters per line at 16px Light — an unusually long measure; 350px ≈53ch at 390). A documented observation, kept as-is.",
      ["measure", "line length", "line height", "leading", "column width", "content width"],
      {"group": "Type", "leading": "1.75", "measure": {"@1280": "1008px ≈150ch", "@390": "350px ≈53ch"},
       "evidence": [f"{EVID}/type-index-1280.png"],
       "verify": ["#main > .inner"]},
      S("_raw/site/assets/css/main.css L126, L3332-3345; probes"), ["redo/b", "redo/d"]),

    A("token-set/breakpoints", "token-set", "Breakpoints — xlarge through xxsmall",
      "Template breakpoint set: xlarge 1281–1680, large 981–1280, medium 737–980, small 481–736, xsmall 361–480, xxsmall ≤360. CSS queries at 1280/980/736/480/360 govern gutters (2.5em → 1.25em ≤736), header padding (8em → 4em), menu width (22em → 16.5em), nav offset (2em → .5em) and tile columns (3-up ≤1280, 1-up at 390).",
      ["breakpoints", "responsive", "media queries", "screen sizes"],
      {"group": "Foundations",
       "tokens": ["xlarge 1281-1680 / large 981-1280 / medium 737-980 / small 481-736 / xsmall 361-480 / xxsmall <=360",
                  "queries used: 1280 (tiles 33.33%), 980, 736 (header/menu switch), 480 (hamburger), 360"],
       "verify": ["html", "body"]},
      S("_raw/site/assets/js/main.js breakpoints(); main.css media queries"), ["redo/d"]),

    A("guideline/typography-voices", "guideline", "Typography — three voices of one family",
      "One family renders in three voices: 300 light sentence-case body (the working voice), 700 tight-tracked h1, and 900 uppercase tracked caps for h2–h6, wordmark, nav and buttons. Loaded via Google Fonts @import (300,700,900 only — no 400, no italics; em/blockquote are synthetic oblique). Table heads stay mixed-case 900; labels/menu links stay 300.",
      ["typography", "font", "font weight", "heading voice", "Source Sans Pro", "type system", "fonts"],
      {"group": "Type",
       "faces": ["SourceSansPro-Light (300) body", "SourceSansPro-Bold (700) h1", "SourceSansPro-Black (900) caps voice"],
       "loading": "@import fonts.googleapis.com css?family=Source+Sans+Pro:300,700,900 (main.css:2); no 400, no italics",
       "evidence": [f"{EVID}/type-index-1280.png", f"{EVID}/type-elements-1280.png"],
       "verify": ["body", "#main h1", "#main h2", ".button"]},
      S("_raw/site/assets/css/main.css L1-2, L119-231; CDP platform-font probes"), ["redo/b"]),

    # --- components ----------------------------------------------------------
    A("component/action-button", "component", "Button (ink ring, tracked caps, pink hover)",
      "Uppercase 900 label at 0.8em with 0.35em tracking, 44.8px tall, radius 4px (NOT flattened); default = transparent ground with a 2px ink ring (inset 0 0 0 2px #585858); hover flips label + ring to pink #f2849e; primary = solid #585858 white label, hover ground #f2849e, active #ee5f81; active ground rgba(242,132,158,.1). Small 0.6em (33.6px), large 1em (56px), .fit full width; disabled opacity .25.",
      ["button", "primary button", "cta", "action", "submit button", "small button", "large button", "fit button", "send button"],
      {"class": ".button / input[type=submit|reset|button]", "group": "Actions",
       "states": ["default: transparent + inset 0 0 0 2px #585858 ring, ink label", "hover: label + ring #f2849e",
                  "active: ground rgba(242,132,158,.1)", "primary: ground #585858 white; hover #f2849e; active #ee5f81",
                  "disabled: opacity .25"],
       "spec": ["height 3.5em (44.8px)", "padding 0 1.25em 0 1.6em", "font 0.8em/900, 0.35em, uppercase", "transition 0.2s ease-in-out"],
       "evidence": [f"{EVID}/comp-elements-btn-hover-1280.png", f"{EVID}/comp-elements-1280.png"],
       "verify": [".button", ".button.primary", ".button.small"]},
      S("_raw/site/assets/css/main.css Button block; measured on elements.html"), ["redo/c"]),

    A("component/field", "component", "Field (underline input, pink focus)",
      "Text inputs/textareas: transparent ground (plain white, no tint), no box, radius 0, a single 1px #c9c9c9 bottom line, exact height 3em (48px). Focus trades the line for a 2px pink #f2849e underline (border + inset 0 -1px 0 0). Value text renders in the page ink-pink; placeholders keep browser grey. Width variants .fields > .field half/third/quarter.",
      ["text field", "input", "form field", "email field", "textarea", "contact form", "underline input"],
      {"class": "input[type=text|password|email|tel], textarea", "group": "Form",
       "states": ["default: 1px #c9c9c9 bottom line on white, radius 0", "focus: 2px pink #f2849e underline",
                  "value colour: rgb(255,107,188)"],
       "layout": [".fields flex wrap; .field.half 50% / .third 33% / .quarter 25%"],
       "evidence": [f"{EVID}/comp-elements-field-focus-1280.png"],
       "verify": ["input[type=text]", "textarea"]},
      S("_raw/site/assets/css/main.css Form block; measured on elements.html"), ["redo/c"]),

    A("component/select", "component", "Select (underline, custom chevron)",
      "Native select restyled to the field language: appearance none, transparent, radius 0, 1px #c9c9c9 bottom line, height 3em; chevron = inline SVG arrow (fill #c9c9c9) at 1.25rem offset right calc(100% - 1rem); padding-right 3em; option ground white. Focus = the same pink underline as fields.",
      ["select", "dropdown", "dropdown select", "category picker", "choose option"],
      {"class": "select", "group": "Form",
       "states": ["default like field (radius 0)", "focus: pink #f2849e underline"],
       "verify": ["select"]},
      S("_raw/site/assets/css/main.css select block; measured on elements.html"), ["redo/c"]),

    A("component/checkbox-radio", "component", "Checkbox & radio (red checked fill, purple labels)",
      "Custom marks via input + label:before at 2.25em (28.8px): checkbox radius flattened to 0 (template had 4px), radio stays a 100% circle. Unchecked = 1px #c9c9c9 outline. Checked = solid #f51616 fill, #f82121 border, white checkmark (\\f00c) — the shared rule puts a checkmark inside the radio circle too (no dot state). Labels are purple #8833e3, 1em/300; focus adds a 1px #f2849e ring.",
      ["checkbox", "radio", "radio button", "check box", "consent checkbox", "option mark", "agree to terms"],
      {"class": "input[type=checkbox|radio] + label", "group": "Form",
       "states": ["unchecked: 1px #c9c9c9 box/ring, transparent", "checked: ground #f51616, border #f82121, white checkmark (checkbox AND radio)",
                  "focus: border + 0 0 0 1px #f2849e ring", "label: #8833e3"],
       "evidence": [f"{EVID}/comp-elements-form-1280.png"],
       "verify": ["input[type=checkbox]", "input[type=radio]"]},
      S("_raw/site/assets/css/main.css checkbox/radio block; measured on elements.html"), ["redo/c"]),

    A("component/table", "component", "Table (900 head, 2px rules, tinted odd rows)",
      "Full-width tables: heads 0.9em/900, left-aligned, mixed case (no caps); thead + tfoot 2px #c9c9c9 rules; tbody rows 1px top+bottom rules; odd rows tinted rgba(144,144,144,.075); td padding 0.75em. `.alternate` adds a full 1px cell grid and keeps the same zebra. `.table-wrapper` was meant to give overflow-x — on the deployment its rule is dead (comment edit), so tables have no scroll path.",
      ["table", "data table", "ruled table", "alternate table", "spec table", "rows"],
      {"class": "table / table.alt / .table-wrapper", "group": "Content",
       "states": ["default: horizontal rules only", "alternate: 1px cell grid + same zebra"],
       "evidence": [f"{EVID}/comp-elements-table-1280.png"],
       "verify": ["table", "table.alt", ".table-wrapper"]},
      S("_raw/site/assets/css/main.css Table block; measured on elements.html"), ["redo/c"]),

    A("component/tiles", "component", "Tiles (project grid; deployed hover = flat pink veil, no zoom)",
      "Responsive image grid (3-up at 1280, 322×322px tiles; 1-up at 390). Image radius flattened to 0. Rest veils mostly alpha-0 (#efc5e900, #ffe2e500; faint #746ffa28 / #ffe2e524). Non-touch hover: the veil becomes an OPAQUE flat pink #eb84da (photo fully covered, 97.6% of the tile in the capture), transform stays scale(1) (no zoom), the cross/arrow overlay is disabled, and the white caption fades in (opacity 0→1, max-height 0→15em over 0.5s; white-on-#eb84da 2.37:1).",
      ["tiles", "project grid", "portfolio grid", "project cards", "image cards", "photo grid"],
      {"class": "section.tiles > article (.style1-6) > .image + a", "group": "Content",
       "states": ["rest: plain photo (veils ~invisible), no caption/arrow", "hover: opaque #eb84da wash + white caption, no zoom"],
       "flaws": ["hover photo fully hidden by the veil", "four of six style veils have zero alpha", "caption contrast 2.37:1"],
       "evidence": [f"{EVID}/comp-index-tile-hover-1280.png", f"{EVID}/comp-index-1280.png"],
       "verify": [".tiles article", ".tiles article.style3"]},
      S("_raw/site/assets/css/main.css Tiles block (deployed); measured on index.html"), ["redo/c"]),

    A("component/icon-row", "component", "Icon chips (square) & inline icons",
      "ul.icons rows: style2 = square chip 2.65em (42.4px), 1px #c9c9c9 border, radius flattened to 0 (template 4px), glyph inherits the page ink (pink rgb(255,107,188)); hover = glyph + border #f2849e; active ground rgba(242,132,158,.1). style1 = bare glyph links (rendered green via the link colour). Icons from the bundled Font Awesome set; the index footer mixes an inline book glyph.",
      ["icons", "social icons", "social media icons", "icon chips", "follow row", "social row"],
      {"class": "ul.icons li a.icon (style1|style2, solid|brands)", "group": "Content",
       "states": ["default: 1px #c9c9c9 square outline + pink glyph", "hover: #f2849e glyph + border", "active: rgba(242,132,158,.1) ground"],
       "evidence": [f"{EVID}/comp-elements-icons-hover-1280.png"],
       "verify": ["ul.icons li a.icon.style2"]},
      S("_raw/site/assets/css/main.css Icon block; measured on elements.html"), ["redo/c"]),

    A("component/emblem-logo", "component", "Emblem & wordmark lock-up",
      "Header lock-up: round emblem images/logo.svg at 2em (32×32px) + a 900 uppercase wordmark with 0.35em tracking in the page ink (pink on most pages; black on project pages). Deployed wordmarks differ per page group ('Zhen Wu YoYo 圳' / 'Phantom' / 'About Zhen' / 'Back to main'). The 圳 glyph has no declared CJK font — it falls to the OS (see fallback/cjk-system-fallback).",
      ["logo", "emblem", "symbol", "wordmark", "site title", "logo lockup"],
      {"class": "#header .logo .symbol img + .title", "group": "Header",
       "spec": ["symbol 2em×2em, margin-right 0.65em", "wordmark 900, uppercase, 0.35em", "lock-up margin-bottom 2.5em"],
       "evidence": [f"{EVID}/type-index-heading-1280.png"],
       "verify": ["#header .logo"]},
      S("_raw/site/assets/css/main.css Header/logo; measured on index.html"), ["redo/c", "redo/b"]),

    A("component/nav-hamburger", "component", "Nav trigger (hamburger plate)",
      "Fixed top-right 4em×3em (64×48px) plate, background rgba(255,255,255,.5) (near-invisible on white), radius 4px kept; no visible label (text-indent trick, no aria-label). Icon = inline 3-line SVG: grey #585858 default, pink #f2849e on hover (opacity swap). Triggers the #menu panel.",
      ["hamburger", "menu button", "nav toggle", "menu trigger", "navigation button"],
      {"class": "#header nav ul li a[href='#menu']", "group": "Header",
       "states": ["default: grey lines on white-50% plate", "hover: pink lines"],
       "evidence": [f"{EVID}/comp-menu-open-1280.png"],
       "verify": ["#header nav a[href='#menu']"]},
      S("_raw/site/assets/css/main.css Header nav; measured on index.html"), ["redo/c"]),

    A("component/menu-panel", "component", "Menu panel (neon-green slide-in)",
      "Slide-in nav: 22em (352px) fixed right, full height, ground #3ef900 lime (override of the template's #585858) with black text; inner padding 2.75em; heading in tracked caps; links black, 1em 0 padding, no hover colour, separators remain the template's rgba(255,255,255,.15) rules (faint on green). Opening (body.is-menu-visible) slides it in and dims #wrapper to opacity .25. Close = X (SVG) 6em left of the panel, grey #585858 → pink hover; it sits over the dimmed page.",
      ["menu", "main menu", "navigation", "nav panel", "menu overlay", "the main menu", "slide menu"],
      {"class": "#menu > .inner", "group": "Navigation",
       "states": ["closed: translateX(22em)", "open: translateX(0); #wrapper dimmed to .25 (0.45s ease)",
                  "close control: grey X → pink on hover"],
       "evidence": [f"{EVID}/comp-menu-open-1280.png", f"{EVID}/colour-index-1280-menu-open.png"],
       "verify": ["#menu", "body.is-menu-visible #wrapper"]},
      S("_raw/site/assets/css/main.css Menu block (deployed); measured on index.html"), ["redo/c"]),

    A("component/carousel-gallery", "component", "Random gallery carousel (index)",
      "Auto-advancing single-image carousel: #carouselGallery (max-width 1200, centred), one .carousel-item at a time = img fixed 640×360 object-fit cover + tracked-caps pink h3 title + empty desc p; the DOM item is replaced every 4000ms by an inline script; no controls (showPrev exists, unwired). The six deployed sources (randomgallery/*.jpg) all 404 — the live carousel is broken. Fixed 640px image + 700px collage cause 390px overflow (scrollWidth 700).",
      ["carousel", "random gallery", "gallery slider", "autoplay gallery", "image slider"],
      {"class": "#carouselGallery .carousel-item", "group": "Content",
       "states": ["state A: ILIGHTUUP caption", "state B: SEA, SENSE, AND MELODY caption", "auto-advance 4s, no controls"],
       "flaws": ["all six image sources 404", "no controls/position readout", "390px overflow"],
       "evidence": [f"{EVID}/comp-index-carousel-a-1280.png", f"{EVID}/comp-index-carousel-b-1280.png"],
       "verify": ["#carouselGallery"]},
      S("index.html inline script/styles L82-86, L260-305; measured on index.html"), ["redo/c", "redo/d"]),

    A("component/blockquote", "component", "Blockquote",
      "Italic pull-quote (synthetic oblique — no italic face) with a 4px #c9c9c9 left rule, padding 0.5em 0 0.5em 2em, no quotation marks; text colour inherits the page ink.",
      ["blockquote", "pull quote", "quotation block", "quote"],
      {"class": "blockquote", "group": "Content",
       "evidence": [f"{EVID}/comp-elements-1280.png"],
       "verify": ["blockquote"]},
      S("_raw/site/assets/css/main.css type block; measured on elements.html"), ["redo/c"]),

    A("component/code-pre", "component", "Code & preformatted (blue chip)",
      "Inline code: Courier New 0.9em (14.4px), padding 0.25em 0.65em, 1px #c9c9c9 border, radius 4px, ground rgba(46,90,249,.986) — a solid royal-blue chip with pink text (measured 1.99:1). Pre blocks stay transparent, no border, 1.75 line-height, horizontal scroll (lines clip at 390).",
      ["code", "code block", "code sample", "preformatted", "monospace", "snippet"],
      {"class": "code / pre", "group": "Content",
       "evidence": [f"{EVID}/comp-elements-1280.png"],
       "verify": ["code", "pre"]},
      S("_raw/site/assets/css/main.css type block (deployed ground); measured on elements.html"), ["redo/c"]),

    A("component/hr", "component", "Horizontal rule",
      "1px #c9c9c9 rule with 2em vertical margin; the content divider used across the site.",
      ["rule", "divider", "separator", "hr"],
      {"class": "hr", "group": "Content", "verify": ["hr"]},
      S("_raw/site/assets/css/main.css type block; measured on elements.html"), ["redo/c"], status="stable"),

    A("component/lists", "component", "Lists (default, alt, ordered)",
      "Unordered lists with disc marks and 2em spacing; ul.alt drops marks; ol uses decimal counters; li item spacing 2em. Content primitives — they inherit the page ink (pink on default pages).",
      ["bulleted list", "list", "ordered list", "numbered list", "bullet points"],
      {"class": "ul / ul.alt / ol", "group": "Content", "verify": ["ul", "ol"]},
      S("_raw/site/assets/css/main.css List block; rendered on elements.html", note="carried from pass 1, re-verified rendered"),
      ["redo/c", "pass1"]),

    A("component/image", "component", "Image treatments",
      "Images are structural: .image.main full-column block (2em margins, radius flattened to 0), .image.fit content-width, .left/.right floats ~40%. On index and project pages whole sections sit inside span.image.main wrappers (some 0px-high, empty); project galleries use .image1 float alternation instead (see layout/project-page). Many images carry hard-coded inline px widths (200–1000) that overflow mobile.",
      ["image", "full width image", "left image", "right image", "photo", "figure", "hero image"],
      {"class": ".image (.main .fit .left .right)", "group": "Content",
       "flaws": ["radius flattened to 0", "hard-coded inline widths overflow ≤736"],
       "verify": [".image.main"]},
      S("_raw/site/assets/css/main.css Box/Image blocks; rendered on index/light", note="carried from pass 1 + redo additions"),
      ["redo/d", "pass1"]),

    A("component/actions", "component", "Actions row (ul.actions)",
      "Horizontal cluster of buttons/links (ul.actions) with 1em gaps, right-aligned by default; .fixed stacks full-width. Renders in elements' demo and carries the footer form submits.",
      ["button row", "action row", "submit row", "form actions", "button group"],
      {"class": "ul.actions (.fixed)", "group": "Actions", "verify": ["ul.actions"]},
      S("_raw/site/assets/css/main.css Actions block; rendered on elements.html", note="carried from pass 1, re-verified rendered"),
      ["redo/c", "pass1"]),

    # --- layout --------------------------------------------------------------
    A("layout/page-shell", "layout", "Page shell — header / menu / main / footer slots",
      "Every page: #wrapper > header#header (static, 8em top pad; logo left; fixed 64×48 Menu pill top-right) + nav#menu (fixed slide-in; 22em, 16.5em ≤736) + div#main inside a 68em/2.5em container + optional footer#footer (rendered on only 4 of 9 pages). Project pages add a shared per-page style block. index duplicates id=main and nests a second document head mid-body (renders as whitespace).",
      ["page shell", "page layout", "site shell", "wrapper", "container", "page structure", "content width"],
      {"group": "Layout",
       "structure": ["#wrapper > header#header (logo + Menu pill)", "nav#menu (slide-in panel)",
                     "div#main > .inner (68em; 2.5em gutters, 1.25em ≤736)", "footer#footer (optional; #f6f6f6)"],
       "metrics": ["container 68em (1008px @1280 / 350px @390)", "#header 8em pad (4em ≤736)", "#main pad-bottom 6em", "#menu 22em/16.5em"],
       "variance": "footer on index (custom email variant), elements/generic/publication (template); commented out on light/tame/fafa/Unlogical; absent on email",
       "evidence": [f"{EVID}/layout-index-1280.png", f"{EVID}/layout-elements-1280.png"],
       "verify": ["#wrapper", "#main > .inner", "#footer"]},
      S("_raw/site/assets/css/main.css L3330-3341, L2843-3163; per-page HTML"), ["redo/d"]),

    A("layout/header", "layout", "Header — logo left, fixed Menu pill (no load animation)",
      "Static top block (8em pad; 4em ≤736); logo left = 2em symbol + tracked-caps wordmark; a single Menu control fixed top-right (right 2em/top 2em) as a 64×48 translucent-white plate with hidden label and 3-line SVG icon. Radius 4px kept here while the rest of the deployment flattened radii. The header does NOT fade with load-in (opacity 1 throughout) — pass-1's fade claim was wrong.",
      ["header", "site header", "brand", "top bar", "menu button", "logo", "wordmark", "site header with logo"],
      {"class": "#header", "group": "Layout",
       "structure": ["a.logo > .symbol img (2em) + .title wordmark", "fixed nav: a[href='#menu'] Menu pill (64×48)"],
       "measured": ["pill rect 64×48 @1280 x=1184,y=32; @390 x=318,y=8", "header opacity 1 during is-preload"],
       "evidence": [f"{EVID}/layout-index-1280.png", f"{EVID}/layout-index-nesteddoctype-1280.png"],
       "verify": ["#header", "#header .logo"]},
      S("_raw/site/assets/css/main.css Header block; measured"), ["redo/d"]),

    A("layout/footer", "layout", "Footer — 2 sections + copyright (present on 4 of 9 pages)",
      "Grey #f6f6f6 ground, padding 5em 0 6em; flex .inner: contact block (~66%; underline form + Send on elements/generic/publication; index swaps the form for a plain pink email line) + Follow icon row (~33%) + copyright bar (0.8em, rgba(88,88,88,.5) ≈ 2.23:1). Commented out on the four project pages; absent on email.",
      ["footer", "contact block", "follow block", "copyright", "get in touch"],
      {"class": "#footer", "group": "Layout",
       "states": ["rendered (index/elements/generic/publication)", "commented out (light/tame/fafa/Unlogical)", "absent (email)"],
       "evidence": [f"{EVID}/layout-generic-1280.png", f"{EVID}/layout-light-1280.png"],
       "verify": ["#footer"]},
      S("_raw/site/assets/css/main.css Footer block; per-page HTML"), ["redo/d", "redo/c"]),

    A("layout/page-intro", "layout", "Load-in motion (is-preload) — tiles only",
      "The only authored motion: body.is-preload disables all animation/transition (!important) and holds .tiles article at scale(0.9)/opacity 0; main.js removes the class 100ms after window.load; tiles ramp transform+opacity 0.5s ease (measured 0.22→0.99 over ~350ms, settled ~830ms). The header does NOT animate and no #wrapper fade rule exists anywhere (corrects pass-1). noscript.css neutralises the preload transform.",
      ["page load animation", "intro animation", "fade in", "load transition", "entrance motion", "is-preload"],
      {"class": "body.is-preload", "group": "Layout",
       "spec": ["is-preload disables ALL animation/transition", ".tiles article scale(.9)/opacity 0 under preload",
                "class dropped 100ms after load; ramp measured 0.22→0.99 ≈350ms", "nothing else animates"],
       "evidence": [f"{EVID}/layout-index-1280.png"],
       "verify": ["body", ".tiles article"]},
      S("_raw/site/assets/css/main.css L108-117, L2589, L2771; main.js; probe series"), ["redo/d"]),

    A("layout/project-page", "layout", "Project-detail composition (light / tame / fafa / Unlogical)",
      "Project pages are hand-built inside the shell: h1 with a per-page inline colour (#ff6bbc / #ff8b80 / #fd77af / #71c3de) + span.image.main hero + freeform blocks; one identical style block on all four (body #fbfbfb/black, .image1 70% odd/even floats, img 100%) plus inline px widths 200–1000; bilibili embeds fixed 800×450 (one 600×450; title attr says 'YouTube video player'); footer commented out; document overflows 390 (820–1020px).",
      ["project page", "project detail", "portfolio detail", "case study layout", "project layout", "gallery layout"],
      {"group": "Layout",
       "structure": ["h1 (inline colour) > span.image.main hero > p blurb", "h2 'Trailer video' + iframe 800×450",
                     "h2 'Publication and Exhibition' / 'Concept' / 'Gallery'", ".image1 floats 70% odd/even + inline-width images"],
       "issues": ["fixed px widths overflow ≤736", "footer commented out", "identical leftover style block on 4 pages"],
       "evidence": [f"{EVID}/layout-light-1280.png", f"{EVID}/layout-tame-390.png"],
       "verify": ["#main > .inner > h1", ".image1", "iframe"]},
      S("light.html/tame.html/fafa.html/Unlogical.html per-page styles; measured"), ["redo/d"]),
]

# ---------------------------------------------------------------- rules -----
rules = [
    {"id": "P-R1", "name": "reading-ink-pink", "severity": "warning", "applies_to": ["css"],
     "summary": "Deployed reading ink is pink #ff6bbc (body/heads/footer/forms) with neon-green links #6bff2c on a dotted blue underline; per-page black-body flips (project pages, .publication) and per-page h1 hues are sanctioned parts of the system. Contrast below AA is measured and recorded (prohibition/unreadable-accent-ink).",
     "why": "Pass 2 extracted what the site IS: the pink/neon ink layer is the deployment's signature, not an accident. Recorded contrast: pink-on-white 2.6:1, green-on-white 1.32:1.",
     "fix": "Follow the deployed ink map; where a consumer needs AA compliance, use the sanctioned black-body override (already in the system) and file the divergence as a gap."},
    {"id": "P-R2", "name": "radius-map", "severity": "warning", "applies_to": ["css"],
     "summary": "Radius map as deployed: 0px on checkbox marks (checkbox only), boxes, .image spans, icon chips (style2) and tiles; 100% on radios and logo/icon discs; 4px kept on buttons, inline code, nav plates and tile captions.",
     "why": "Half the template's 4px family was intentionally flattened; the remainder holds. Both values are canonical in their mapped places.",
     "fix": "Apply the map above by component; do not blanket-flatten or blanket-restore."},
    {"id": "P-R3", "name": "tracked-caps-display", "severity": "warning", "applies_to": ["css", "html"],
     "summary": "Caps voice (uppercase 900, +0.35em) runs h2–h4, wordmark, nav and buttons; h1 stays sentence-case 700 with −0.035em; table heads are 900 mixed case; labels and menu links stay 300.",
     "why": "Measured across type, buttons, menu and tables; the mixed-case exceptions are as deliberate as the caps.",
     "fix": "Apply the caps voice to the list above; never caps-track running text; keep table heads mixed case."},
    {"id": "P-R4", "name": "flat-inset-rings", "severity": "warning", "applies_to": ["css"],
     "summary": "Depth is drawn with inset rings (inset 0 0 0 Npx), hairlines and rules — no blurred/elevation shadows exist anywhere in the system.",
     "why": "Shadow census on the deployed render finds inset rings only; the flat surface is the system's honesty.",
     "fix": "Replace drop shadows with inset rings or 1px rules."},
    {"id": "P-R5", "name": "underline-fields", "severity": "warning", "applies_to": ["css"],
     "summary": "Fields are underline-only on white: no box, radius 0, 1px #c9c9c9 bottom line; focus = 2px pink #f2849e underline (border + inset). Select and textarea follow.",
     "why": "Measured on every input; the box-less language keeps the page rhythm.",
     "fix": "Strip field boxes; keep the bottom line and the pink focus underline."},
    {"id": "P-R6", "name": "link-trio", "severity": "info", "applies_to": ["css"],
     "summary": "A content link carries three colours at once: text #6bff2c, dotted 1px #20a3f5 underline, #f2849e hover (underline goes transparent). The underline is the link's findability anchor under failing contrast; the hover pink is the template accent.",
     "why": "Measured as one wrapped rule on all 9 pages; removing any leg changes the system.",
     "fix": "Keep the trio intact; do not 'fix' the link colour without re-opening the ink decision."},
    {"id": "P-R7", "name": "per-page-override-pattern", "severity": "info", "applies_to": ["css", "html"],
     "summary": "Global pink ink is overridden per page: light/tame/fafa/Unlogical inject one identical style block (body #fbfbfb + black text) and recolour only their h1 via inline style; publication adds a .publication class painting its main text black while header/footer stay pink.",
     "why": "This override mechanism is the system's actual extension model for 'quieter' pages; new pages should follow it rather than introduce new mechanisms.",
     "fix": "To quiet a page, reuse the shared style block + one h1 accent; do not fork the global stylesheet."},
    {"id": "P-R8", "name": "state-colour-pink", "severity": "info", "applies_to": ["css"],
     "summary": "One interaction-state colour: #f2849e. It is the hover label+ring on buttons, field/select focus underline, icon-chip hover glyph+border, :active ground at 10% alpha, and link hover. Measured on every interactive control.",
     "why": "Single accent keeps the state language coherent (2.45:1 on white — state emphasis only, never reading ink).",
     "fix": "Use #f2849e for state emphasis; do not add a second state colour."},
]

# --------------------------------------------------------- prohibitions -----
prohibitions = [
    {"id": "prohibit/unreadable-accent-ink", "kind": "prohibition",
     "statement": "Accent ink relied on as the only readable signal where measured contrast < 3:1 — as a reusable-system guard. Measured in the deployment: pink/white 2.60, green/white 1.32, pink/code-blue 1.99, close-X/white 1.32. Pair the colour with another affordance (the dotted underline does this for links; nothing does it for body text) or use a sanctioned override.",
     "signals": ["contrast", "low contrast", "readability", "accessibility", "unreadable", "aa", "wcag"],
     "rule": "P-R1"},
    {"id": "prohibit/blurred-shadows", "kind": "prohibition",
     "statement": "Blurred/drop elevation shadows — depth is inset rings and rules only (P-R4).",
     "signals": ["drop shadow", "box shadow blur", "elevation", "soft shadow", "card shadow", "glow"],
     "rule": "P-R4"},
]

# ------------------------------------------------------------ fallbacks -----
fallbacks = [
    {"id": "fallback/light-only", "kind": "fallback",
     "title": "Light grounds only (no dark surfaces)",
     "statement": "The deployment ships no dark ground anywhere — the menu went lime, the tile scrim is disabled. If a dark surface is unavoidable (video overlay, modal), keep the base text roles, mark the improvisation and file a gap.",
     "scope": ["dark", "dark mode", "dark surface", "overlay", "theme"],
     "constraints": ["no dark canon exists", "keep base roles if forced", "mark + file gap if it recurs"]},
    {"id": "fallback/no-script", "kind": "fallback",
     "title": "No-JS fallback (noscript stylesheet)",
     "statement": "Without JS the load-in is skipped and content renders immediately (noscript.css lifts is-preload). The menu remains JS-dependent (slide-in + dimming); without JS its control degrades to an in-page anchor at best — undefined beyond that.",
     "scope": ["motion", "intro", "menu", "javascript"],
     "constraints": ["content readable without JS", "menu behaviour undefined without JS — mark it"]},
    {"id": "fallback/cjk-system-fallback", "kind": "fallback",
     "title": "CJK text falls to the OS (no CJK family declared)",
     "statement": "No CJK font is declared anywhere; Chinese glyphs fall through Source Sans Pro → Helvetica → the OS (observed: WenQuanYi Zen Hei in a headless Linux render), mismatched to the 900-weight Latin beside them. Rendering of 圳 therefore differs per visitor OS.",
     "scope": ["chinese", "cjk", "圳", "fallback font", "mixed script"],
     "constraints": ["if CJK becomes a real role, it needs a declared stack + weight match — file as gap", "never assert a specific CJK face from this system"]},
    {"id": "fallback/synthetic-italic", "kind": "fallback",
     "title": "Italic is synthetic (no italic faces loaded)",
     "statement": "The Google-Fonts import requests 300/700/900 normal styles only; em/blockquote render as browser-synthesised oblique. Treat any italic as an approximation, not a system face.",
     "scope": ["italic", "oblique", "em", "blockquote"],
     "constraints": ["do not design italic-dependent hierarchy", "a real italic face is a new decision (gap if needed)"]},
]

# ----------------------------------------------------------- precedents -----
precedents = [
    {"id": "precedent/pink-ink-canonised", "kind": "precedent",
     "title": "Pink/neon reading ink — canonised on redo",
     "request": "body/UI text in the deployment's pink/neon ink family (#ff6bbc text, #6bff2c links) as the system's reading surface",
     "matches": ["neon text", "pink text", "green links", "bright colour text", "pink reading ink"],
     "decision": "accepted (pass-2 redo; supersedes precedent/declined-neon-reading-ink)",
     "grounds": "Rendered evidence: the deployed site paints reading text pink on 6 pages and links green on all 9; pass 1 had canonicalised the template's grey and misfiled the deployment's actual language. Extraction principle: extract what the site IS.",
     "reason": "The pink reading ink is the portfolio's identity. Its measured contrast failures (2.6:1 / 1.32:1) are recorded as observations and bounded by prohibition/unreadable-accent-ink (do not extend the pattern past its measured roles; pair colour with other affordances).",
     "scope": {"domains": ["css", "html"], "boundary": ["roles as deployed", "documented contrast limits"]},
     "try": ["follow the deployed ink map (P-R1)", "for AA-sensitive consumers use the sanctioned black-body override and file a gap"],
     "citation": "docs/synthesis/phantom/domains/a-colour-and-surfaces.md + b-typography-and-language.md; evidence/screens/colour-*, type-*",
     "provenance": {"source": "pass-2 redo adjudication 2026-10-08", "note": "reversal of pass-1 declination; owner-directed"}},
]

# ----------------------------------------------------------- candidates -----
candidates = [
    {"id": "candidate/text-as-accent", "kind": "candidate",
     "title": "Text-as-accent (pink ink identity) — promotion dossier",
     "request": "the pink reading-ink identity as a promoted, reusable system feature",
     "matches": ["pink accent", "pink theme", "accent colour", "text as accent", "neon pink"],
     "status": "candidate",
     "summary": "The deployment's real design decision: text itself carries the accent (pink family) across every role, with per-page h1 hues and a neon link. Canonised as observed (token-set/colour); promotion asks for a role map, an AA strategy and owner sign-off — the dossier, not the fact.",
     "emerges_from": ["token-set/colour (canonised pass 2)", "per-page h1 hues #ff6bbc/#ff8b80/#fd77af/#71c3de"],
     "evidence_present": "12 text roles measured pink; per-page black flips already provide an AA path; hover/focus pink #f2849e is the state accent.",
     "promote_when": ["single role map (pink vs black per role) drafted",
                      "AA strategy chosen (size/weight minimums or darkened ground variants)",
                      "owner sign-off"],
     "provenance": {"source": "redo domains a+b; supersedes candidate/pink-accent-system"}},
    {"id": "candidate/carousel", "kind": "candidate",
     "title": "Gallery carousel — repair & controls dossier",
     "request": "a working, controlled image carousel for the random gallery",
     "matches": ["carousel", "slideshow", "gallery slider", "image slider", "rotating gallery", "image carousel"],
     "status": "candidate",
     "summary": "A carousel exists as deployed (component/carousel-gallery) but ships broken: all six sources 404, no controls, autoplay only, 390px overflow. Promotion = re-source the images, decide the motion policy (autoplay vs static/controls) and add position affordances.",
     "emerges_from": ["component/carousel-gallery", "layout open question D-4"],
     "evidence_present": "Two captured states; showPrev unwired; comment 'Buttons removed for automatic switching'.",
     "promote_when": ["images re-sourced (or fallback state designed)", "motion policy agreed (no autoplay, or pause/bounded)",
                      "control spec captured (prev/next + position)", "static fallback defined"],
     "provenance": {"source": "redo domains c+d"}},
    {"id": "candidate/project-gallery", "kind": "candidate",
     "title": "Project gallery pattern — promotion dossier",
     "request": "the project-page gallery composition (float alternation) as a reusable pattern",
     "matches": ["project gallery", "gallery layout", "float gallery", "alternating gallery"],
     "status": "candidate",
     "summary": "The four project pages apply one consistent composition (identical style block: .image1 70% floats odd/even, img 100%) — arguably a de-facto pattern. Promotion requires a width policy that survives ≤736 (currently 820–1020px overflow) and a decision on the shared-style-block mechanism.",
     "emerges_from": ["layout/project-page", "open question D-6"],
     "evidence_present": "Byte-identical style blocks on 4 pages; float alternation consistently applied.",
     "promote_when": ["responsive width policy (max-width + height:auto) drafted",
                      "shared-block vs class migration decided", "one page rebuilt as the reference"],
     "provenance": {"source": "redo domain d"}},
]

# ------------------------------------------------------------- golden -------
golden = {
    "version": "0.2", "pack_version": "phantom 0.2.0",
    "cases": [
        {"problem": "a primary button", "expect": "RESOLVED", "expect_id": "component/action-button", "note": "Ink ring, pink hover, radius 4."},
        {"problem": "the main menu", "expect": "RESOLVED", "expect_id": "component/menu-panel", "note": "Lime slide-in panel, black links."},
        {"problem": "site header with logo", "expect": "RESOLVED", "expect_id": "layout/header", "note": "Logo left, fixed Menu pill."},
        {"problem": "a text input for the contact form", "expect": "RESOLVED", "expect_id": "component/field", "note": "Underline field, pink focus."},
        {"problem": "dropdown select", "expect": "RESOLVED", "expect_id": "component/select", "note": "Underline + chevron."},
        {"problem": "a checkbox for consent", "expect": "RESOLVED", "expect_id": "component/checkbox-radio", "note": "Red checked fill, purple label."},
        {"problem": "a data table of publications", "expect": "RESOLVED", "expect_id": "component/table", "note": "900 heads, tinted rows."},
        {"problem": "project grid of image tiles", "expect": "RESOLVED", "expect_id": "component/tiles", "note": "Opaque pink hover veil, no zoom."},
        {"problem": "pull quote in an article", "expect": "RESOLVED", "expect_id": "component/blockquote", "note": "Left-rule quote."},
        {"problem": "a code sample block", "expect": "RESOLVED", "expect_id": "component/code-pre", "note": "Blue chip, pink text."},
        {"problem": "bulleted list of materials", "expect": "RESOLVED", "expect_id": "component/lists", "note": "Disc list."},
        {"problem": "a full width image in the article", "expect": "RESOLVED", "expect_id": "component/image", "note": ".image.main."},
        {"problem": "social media icons in the footer", "expect": "RESOLVED", "expect_id": "component/icon-row", "note": "Square chips, pink glyph."},
        {"problem": "the page fade in on load", "expect": "RESOLVED", "expect_id": "layout/page-intro", "note": "Tiles-only entrance."},
        {"problem": "footer contact section", "expect": "RESOLVED", "expect_id": "layout/footer", "note": "Grey ground, two columns."},
        {"problem": "an image carousel for the gallery", "expect": "RESOLVED", "expect_id": "component/carousel-gallery", "note": "Exists as deployed; repair dossier open."},
        {"problem": "make the text neon pink", "expect": "RESOLVED", "expect_id": "token-set/colour", "note": "Canonised on redo (pink reading ink)."},
        {"problem": "a carousel with prev next controls", "expect": "UNDEFINED", "note": "Deployed controls were removed — candidate/carousel holds the spec question."},
        {"problem": "a project detail page for a new work", "expect": "RESOLVED", "expect_id": "layout/project-page", "note": "Hero + floats + iframe composition."},
        {"problem": "matching Chinese type in the wordmark", "expect": "FALLBACK", "expect_id": "fallback/cjk-system-fallback", "note": "No CJK stack declared — the resolver surfaces the OS-fallback constraint."},
        {"problem": "link colours for content links", "expect": "RESOLVED", "expect_id": "token-set/colour", "note": "Green + dotted blue + pink hover (P-R6)."},
    ],
}

# ------------------------------------------------------------- emit ---------
json.dump({"artifacts": artifacts}, open(os.path.join(OUT, "artifacts.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"rules": rules}, open(os.path.join(OUT, "rules.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"prohibitions": prohibitions}, open(os.path.join(OUT, "prohibitions.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"fallbacks": fallbacks}, open(os.path.join(OUT, "fallbacks.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"precedents": precedents}, open(os.path.join(OUT, "precedents.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"candidates": candidates}, open(os.path.join(OUT, "candidates.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"recipes": []}, open(os.path.join(OUT, "recipes.json"), "w"), indent=1, ensure_ascii=False)
json.dump(golden, open(os.path.join(OUT, "golden.json"), "w"), indent=1, ensure_ascii=False)
print(f"emitted packs/phantom v0.2.0: {len(artifacts)} artifacts, {len(rules)} rules, {len(prohibitions)} prohibitions, "
      f"{len(fallbacks)} fallbacks, {len(precedents)} precedents, {len(candidates)} candidates, {len(golden['cases'])} golden cases")
