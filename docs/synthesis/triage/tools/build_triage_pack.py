#!/usr/bin/env python3
"""build_triage_pack — convert the Triage Design System (v0.12.1, ~/triage-design-system)
into a Design Authority pack at packs/triage/, plus an agent implementation prompt.

Sources (all read from the triage repo — nothing invented):
  spec/rules.json     the enforceable rule catalogue (TDS001-015)      -> rules.json
  spec/states.json    35-component contract matrix (states/verify/a11y) -> component artifacts
  tokens/tokens.json  DTCG token source                                  -> token-set artifacts
  site/pages_patterns.py  pattern descriptions                           -> pattern artifacts
  INTERACTION.md      binding interaction standard                       -> interaction rules
  README.md, AGENTS.md, CHANGELOG.md  doctrine, integration paths        -> guidelines/fallbacks
"""
import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone

REPO = "/home/xrim/design-authority"
TR = "/home/xrim/triage-design-system"
_ap = argparse.ArgumentParser(description="build packs/triage from the triage repo")
_ap.add_argument("--out", default=None, help="output directory (default: packs/triage)")
_args = _ap.parse_args()
OUT = os.path.abspath(_args.out) if _args.out else os.path.join(REPO, "packs", "triage")
os.makedirs(OUT, exist_ok=True)

V = "0.12.1"

_src_commit = subprocess.run(["git", "-C", TR, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip() or "unknown"
_src_branch = subprocess.run(["git", "-C", TR, "rev-parse", "--abbrev-ref", "HEAD"],
                             capture_output=True, text=True).stdout.strip() or "unknown"

# ---------------------------------------------------------------- helpers ----
def load(p):
    with open(os.path.join(TR, p)) as fh:
        return json.load(fh)

def read(p):
    with open(os.path.join(TR, p)) as fh:
        return fh.read()

RULES_SRC = load("spec/rules.json")
STATES = load("spec/states.json")
TOK = load("tokens/tokens.json")

def A(aid, kind, title, summary, aliases, body, source, compiled_from, status="stable"):
    return {"id": aid, "kind": kind, "title": title, "summary": summary, "status": status,
            "aliases": aliases, "body": body,
            "source": {"repo": "triage-design-system (triage.seanyong.xyz)", "path": source},
            "compiled_from": compiled_from}

# ------------------------------------------------------------- authority ----
auth = json.load(open(os.path.join(REPO, "packs", "wink", "authority.json")))
auth.update({
    "id": "triage", "name": "Triage", "version": V,
    "snapshot": {"repo": "triage-design-system (local; published at triage.seanyong.xyz)",
                 "commit": _src_commit, "branch": _src_branch, "version": V,
                 "path_hint": "~/triage-design-system"},
    "description": ("Triage is the app-agnostic, paper-and-ink UI design authority: one token source of "
                    "truth, one component runtime, one enforceable lint gate. Square corners, hairline "
                    "rules, ink-on-paper surfaces, two themes (light/dark), two densities, a 35-component "
                    "contract matrix, and a binding interaction standard. Dependency-free: plain CSS "
                    "tokens, a small behaviour layer that degrades without JS, and generated artifacts."),
})
json.dump(auth, open(os.path.join(OUT, "authority.json"), "w"), indent=1, ensure_ascii=False)

sl = json.load(open(os.path.join(REPO, "packs", "wink", "scoring.json")))
sl["source"] = "triage-design-system spec/ + INTERACTION.md"
json.dump(sl, open(os.path.join(OUT, "scoring.json"), "w"), indent=1)

# ------------------------------------------------------------- artifacts ----
COLOR_KEYS = [k for k in TOK["color"].keys() if not k.startswith("$") and k != "semantic"]
TYPO_KEYS = [k for k in TOK["typography"].keys() if not k.startswith("$")]
MOTION_KEYS = [k for k in TOK["motion"].keys() if not k.startswith("$")]
BP = (TOK.get("misc") or {}).get("breakpoint") or TOK.get("misc") or {}

artifacts = [
    A("token-set/colour", "token-set", "Colour — paper, ink, one accent, status trio",
      "Ink-on-paper colour through tokens only: surfaces, text tiers, tints and line roles, one accent, "
      "a status trio (ok/warn/err) with tint and solid variants. Every token ships light and dark; "
      "compact density lives in token extensions. Raw colour values are lint errors (TDS002).",
      ["colour", "color", "palette", "colour palette", "color palette", "tokens", "colour tokens", "color tokens", "ink", "paper"],
      {"group": "Foundations",
       "tokens": COLOR_KEYS[:24],
       "extensions": ["com.triage.dark (per-token dark values)", "com.triage.compact (density values)"],
       "verify": ["tokens/tokens.css"]},
      "tokens/tokens.json (color group)", ["triage/tokens"]),

    A("token-set/typography", "token-set", "Typography — system stack, one base, a rem ladder",
      "Typography is tokenised: family tokens, a single base-size (16) that the rem ladder divides by, "
      "and an fs-* design scale. Font stacks derive from family tokens; off-system fonts are lint errors "
      "(TDS008).",
      ["typography", "type", "fonts", "font", "type scale", "typography tokens", "type tokens"],
      {"group": "Foundations",
       "families": [k for k in TYPO_KEYS if "family" in k],
       "scale": [k for k in TYPO_KEYS if "fs-" in k][:14],
       "base": TOK["typography"].get("base-size", {}).get("$value") if isinstance(TOK["typography"].get("base-size"), dict) else 16,
       "verify": ["tokens/tokens.css"]},
      "tokens/tokens.json (typography group)", ["triage/tokens"]),

    A("token-set/spacing", "token-set", "Spacing — preferred scale plus semantic roles",
      "Spacing has a curated preferred scale (2/4/8/12/16/24/32/48) and semantic roles (page/card/field/"
      "control) emitted as --space-*; primitives consume roles by intent. Off-scale spacing is a lint "
      "warning (TDS005); fixed chrome widths live in misc.layout.",
      ["spacing", "space", "gaps", "padding", "layout scale", "spacing tokens"],
      {"group": "Foundations",
       "preferred": ["2", "4", "8", "12", "16", "24", "32", "48"],
       "roles": ["page", "card", "field", "control"],
       "tokens": [k for k in TOK["spacing"].keys() if not k.startswith("$")][:16],
       "verify": ["tokens/tokens.css"]},
      "tokens/tokens.json (spacing group)", ["triage/tokens"]),

    A("token-set/motion", "token-set", "Motion — durations and easing, reduced-motion aware",
      "Motion is tokenised (dur-*/ease-*); off-token durations are flagged (TDS006). The system ships "
      "prefers-reduced-motion handling (spinner slows, reveal transitions collapse) instead of ignoring "
      "the user setting.",
      ["motion", "animation", "transition", "duration", "easing", "reduced motion", "motion tokens"],
      {"group": "Foundations",
       "tokens": MOTION_KEYS[:12],
       "verify": ["tokens/tokens.css", "src/core/additions.css (prefers-reduced-motion)"]},
      "tokens/tokens.json (motion group)", ["triage/tokens"]),

    A("token-set/elevation", "token-set", "Elevation — reserved for floating layers",
      "Elevation is reserved for layers that float (menus, dialogs, sheets, toasts); in-flow surfaces use "
      "hairline lines and paper tints instead of shadows. Tokenised shadow values only.",
      ["elevation", "shadow", "depth", "floating", "elevation tokens", "shadow tokens"],
      {"group": "Foundations",
       "tokens": [k for k in TOK.get("shadow", {}).keys() if not k.startswith("$")],
       "verify": ["tokens/tokens.css"]},
      "tokens/tokens.json (shadow group)", ["triage/tokens"]),

    A("token-set/dataviz", "token-set", "Data visualisation — Okabe–Ito derived series",
      "A categorical series palette derived from Okabe–Ito and contrast-adjusted, with pairwise "
      "colour-vision-deficiency separation checked. Charts consume series tokens like everything else.",
      ["dataviz", "data visualisation", "charts", "series", "palette for charts", "chart colours", "chart colors"],
      {"group": "Foundations",
       "series": [k for k in TOK.get("dataviz", {}).keys() if not k.startswith("$")][:12],
       "verify": ["tokens/tokens.css"]},
      "tokens/tokens.json (dataviz group)", ["triage/tokens"]),

    A("token-set/breakpoints", "token-set", "Breakpoints — phone through wide, incl. phone-mode chrome",
      "Media queries in source use {bp-*} placeholders resolved from the misc.breakpoint tokens "
      "(phone/desk/wide; phone-up variants). Phone mode also swaps chrome (drawer nav, sticky bars).",
      ["breakpoints", "responsive", "media queries", "phone", "wide"],
      {"group": "Foundations",
       "tokens": [str(k) for k in (BP.keys() if isinstance(BP, dict) else [])][:16],
       "verify": ["tokens/tokens.json (misc.breakpoint)"]},
      "tokens/tokens.json (misc.breakpoint)", ["triage/tokens"]),

    A("guideline/interaction-standard", "guideline", "Interaction standard (binding)",
      "The interaction standard is binding for every screen: armed two-step deletes, confirm() only for "
      "one-way actions, show-the-reverse for reversible mutations, the three-channel feedback standard "
      "(banner/toast/empty state), save bars for editors, copy rules, and an exceptions register for "
      "deliberate deviations.",
      ["interaction", "behaviour", "behavior", "ux standard", "interaction standard"],
      {"group": "Doctrine",
       "source_doc": "INTERACTION.md (repo root; enforced by lint/triage_lint.py)",
       "channels": ["banner (persistent)", "toast (transient)", "empty state (structural)"],
       "verify": ["INTERACTION.md"]},
      "INTERACTION.md", ["triage/interaction"]),

    A("guideline/consumption", "guideline", "Consumption paths — global and scoped",
      "Two sanctioned ways to adopt: the global path (four lines: tokens.css, base.css, optional "
      "patterns.css, components.js) styles the whole page; the scoped path wraps a region in .triage and "
      "loads scoped.css so host content is never restyled. Pair the scoped bundle with reset.css for "
      "parity; without it the host owns root sizing.",
      ["consumption", "getting started", "adopt", "integration", "scoped", "global"],
      {"group": "Doctrine",
       "global": ["tokens/tokens.css", "core/base.css", "core/patterns.css (optional)", "core/components.js"],
       "scoped": [".triage wrapper", "core/scoped.css", "core/reset.css (recommended)"],
       "verify": ["README.md"]},
      "README.md + CHANGELOG.md 0.12.0", ["triage/consumption"]),
]

# ---- components (35, from the contract matrix) ----
EXTRA_ALIASES = {
    "btn": ["button", "primary button", "secondary button", "cta", "submit button", "danger button", "icon button", "small button"],
    "iconbtn": ["icon-only button", "icon button"],
    "px-sw": ["switch", "toggle", "on off switch"],
    "menu-item": ["menu item", "overflow menu", "row action"],
    "nav-item": ["nav item", "navigation link", "sidebar link"],
    "chip": ["chip", "filter chip", "tag"],
    "index-row": ["index row", "list row"],
    "tbl": ["table", "data table", "rows"],
    "bulkbar": ["bulk bar", "bulk actions", "selection bar"],
    "savebar": ["save bar", "sticky save", "unsaved changes bar"],
    "msg": ["flash message", "banner", "message banner", "status banner", "inline banner", "alert banner", "banner surface", "banner surfaces", "banner style", "banner styles", "banner variants", "paper banner", "ink banner", "tint banner", "solid banner", "informational banner", "info banner", "success banner", "warning banner", "error banner", "result banner"],
    "toast2": ["toast", "toast notification", "transient message"],
    "badge": ["badge", "status badge", "label"],
    "empty": ["empty state", "no results", "zero state"],
    "dlg": ["dialog", "modal", "native dialog"],
    "tip": ["tooltip", "hint bubble"],
    "spinner": ["spinner", "loading indicator", "busy"],
    "field-err": ["field error", "validation message", "inline error"],
    "tabs": ["tabs", "tab bar"],
    "crumbs": ["breadcrumbs", "breadcrumb"],
    "radio": ["radio", "radio group", "radio button"],
    "slider": ["slider", "range input", "range slider"],
    "cb": ["combobox", "autocomplete", "filterable select", "typeahead"],
    "dp": ["date picker", "datepicker", "calendar input"],
    "acc": ["accordion", "disclosure", "foldable section"],
    "avatar-sq": ["avatar", "user avatar"],
    "img": ["image", "figure", "responsive image"],
    "drop": ["dropzone", "file upload", "upload area"],
    "notif": ["notifications panel", "notification list", "bell panel"],
    "cmd": ["command palette", "command menu", "cmd-k"],
    "page-state": ["full-page state", "error page", "empty page", "maintenance page"],
    "pager-num": ["numbered pagination", "pagination", "pager"],
    "tl": ["timeline", "activity timeline", "approval history", "activity log", "event trail",
          "version timeline", "version history"],
    "diff": ["diff", "diff view", "version comparison", "change comparison", "before after diff"],
    "sheet-end": ["sheet", "bottom sheet", "side sheet", "drawer"],
}

GENERIC_EXTRA = {
    "Button": ["action", "action button"], "Table": ["grid"], "Tabs": ["tabbed"],
}

for c in STATES["components"]:
    cls, name = c["class"], c["name"]
    aliases = [name.lower(), cls] + EXTRA_ALIASES.get(cls, []) + GENERIC_EXTRA.get(name, [])
    a11y = c.get("a11y") or []
    summary = "%s — from %s. Documented states: %s." % (name, c["source"], ", ".join(c["states"]))
    if a11y:
        summary += " A11y: " + a11y[0]
    body = {"class": cls, "group": "Components",
            "source_file": c["source"], "states": c["states"],
            "verify": c.get("verify", []), "a11y": a11y, "status": c.get("status", "stable")}
    source_str = "spec/states.json (%s, %s)" % (cls, c["source"])
    compiled = ["triage/states"]
    if cls == "msg":
        # the banner family as documented on /foundations and implemented in base.css:
        # paper/ink surfaces, tint/solid styles, informational/success/warning/error kinds
        summary += (" Documented variants: paper (default) and ink surfaces; tint and solid styles; "
                    "informational, success, warning and error kinds.")
        body["variants"] = {
            "surfaces": ["paper (default) — --surface-banner",
                         "ink — --surface-banner-ink (solid black, both themes)"],
            "styles": ["tint — soft matching border and text (.msg.tint.ok|warn|err; .note.tint accent)",
                       "solid — full-saturation surface, --text-on-ink white; contrast "
                       "6.06/4.84/5.02/4.96 pass 4.5:1 (TDS011)"],
            "kinds": ["neutral — .msg base (ink-secondary edge)",
                      "success — .ok", "warning — .warn", "error — .err",
                      "informational — .note carries the accent edge; info is retired as a flash kind (see voice & copy)"],
            "edge_chip": ("status colour lives in the var(--bw-edge) left chip; paper/tint keep the "
                          "normal chip; highlights inside ink/solid banners use light-grey text on a dark chip"),
            "sibling": ".note shares the surface and style families for inline notices (documented on /foundations)",
            "source": "core/base.css + site/pages_foundations.py (banner spec)",
        }
        source_str = "spec/states.json (%s, %s) + site/pages_foundations.py (banner spec)" % (cls, c["source"])
        compiled = ["triage/states", "triage/banner-spec"]
    artifacts.append(A(
        "component/%s" % cls, "component", name, summary, aliases,
        body, source_str, compiled))

# ---- patterns (7, from the site's pattern pages) ----
PATTERN_ALIASES = {
    "dashboard": ["dashboard", "dashboard page", "home dashboard", "metrics page"],
    "viewer": ["detail page", "detail view", "record page", "item page"],
    "settings": ["settings", "settings page", "preferences", "settings screen"],
    "flows": ["flow canvas", "flow builder", "rule builder", "automation canvas"],
    "simulator": ["dry run", "dry-run report", "simulation report"],
    "learning": ["learning loop", "stepper", "step rail", "model cards"],
    "misc": ["index page", "overflow index", "blind label", "blind-label review"],
}
PATTERNS = [
    ("dashboard", "Dashboard", "Status first, attention second: system strip, hero metrics, stacked feed, filings and activity."),
    ("viewer", "Detail page", "Two-column detail: plain/HTML body and queue controls left, sticky metadata and audit right."),
    ("settings", "Settings", "Task sections with a sticky side nav, scoped setting-row forms and per-card save bars."),
    ("flows", "Flow canvas", "The rule/flow builder: nodes, connectors with insert points, smart condition rows and live summary."),
    ("simulator", "Dry-run report", "Dry-run report: draft controls, per-stage decision trail, proposed actions and a plain-English verdict."),
    ("learning", "Stepper & folds", "The learning loop: step rail, evidence folds, model cards and promotion prerequisites."),
    ("misc", "Index & eval", "Two small page patterns: the phone overflow index and blind-label review."),
]
for slug, title, desc in PATTERNS:
    artifacts.append(A(
        "pattern/%s" % slug, "pattern", title, desc,
        PATTERN_ALIASES.get(slug, [title.lower(), slug + " pattern", slug]),
        {"group": "Patterns", "source_file": "site/pages_patterns.py (%s)" % slug},
        "site/pages_patterns.py", ["triage/patterns"]))

artifacts.append(A(
    "guideline/verification-levels", "guideline", "Verification levels (traceable conformance)",
    "Four levels of conformance — static (shipped), behavioural (partial), rendered and product (proposed) — "
    "with the traceability contract: every conformance claim cites its rule id, implementation location and "
    "evidence; a lint score is a gate, never evidence. Coverage is declared per component.",
    ["verification", "conformance", "evidence", "verification levels", "traceability"],
    {"group": "Doctrine",
     "levels": ["L1 static — lint + states matrix (shipped)",
                "L2 behavioural — keyboard, state transitions, focus restoration, lifecycle (partial; declared per component)",
                "L3 rendered — screenshots, overflow, zoom, dark, reduced motion, visual regression (proposed)",
                "L4 product — workflow success, error recovery, comprehension (proposed cross-product agent experiment)"],
     "contract": "rule id · component · implementation · evidence — score is a gate, not proof",
     "source_doc": "spec/proposals/verification-levels.md",
     "verify": ["spec/proposals/verification-levels.md"]},
    "spec/proposals/verification-levels.md", ["triage/review-2026-10"]))


# ---- foundations: the system's own /foundations pages, as guidelines ----
FOUNDATIONS = [
    ("guideline/philosophy", "Design philosophy (paper and ink)",
     "Triage is a paper-and-ink interface language for tools that do real work on real data: one light paper (#fafafa), "
     "one ink layer, one accent, square geometry, and every machine action auditable. Depth is not faked with blur or "
     "gradient; only things that genuinely float cast shadows. Black ink is a material, not a theme; colour always means "
     "meaning, never decoration. Enforced by tokens and the spec, not just words.",
     ["philosophy", "design philosophy", "design principles", "principles", "paper and ink", "the why"],
     {"group": "Foundations",
      "paper_and_ink": ["grey paper holds white cards with hairline borders and square corners",
                        "shadows reserved for floating layers (menus, toasts, dialogs, drawers)",
                        "black ink is a material: brand, key number, terminal, primary action",
                        "one saturated blue accent; status colour only where a status exists, always with text"],
      "deliberately_absent": ["dark patterns (countdowns, disguised cancellation, notification nagging)",
                              "confirmation popups for entities — deletes arm in place; native confirm() only for irreversible actions",
                              "colour-only meaning or emoji as status",
                              "grey-on-grey typography — every text token is contrast-checked",
                              "a second stylesheet for dark mode — one token file flips both themes"],
      "source_file": "site/pages_foundations.py (philosophy)"}),
    ("guideline/brand", "Brand & theming",
     "One source of truth: Triage themes from tokens/tokens.json (W3C DTCG) and the core stylesheets carry no :root, so a "
     "re-theme is one JSON edit plus a rebuild. Two token tiers (semantic aliases over the raw palette — products prefer "
     "the alias column). The mark is a 24x24 ink square with an accent chip on the leading edge; lockups, favicon and "
     "templates ship in brand/. Never theme by overriding components.",
     ["brand", "logo", "brand mark", "the mark", "wordmark", "theming", "theming rules", "re-theme", "retheme",
      "white label", "white-label", "brand assets", "favicon", "brand strategy"],
     {"group": "Foundations",
      "tiers": ["semantic alias tier over the raw palette (surface.page -> {color.bg}; prefer aliases)",
                "tokens.css is generated from tokens.json; core carries no :root"],
      "mark": "24x24 ink square with an accent chip on the leading edge; lockups, favicon and templates in brand/",
      "rule": "do not theme by overriding components - edit the token source",
      "source_file": "site/pages_foundations.py (brand)"}),
    ("guideline/platform", "Platform & themes",
     "One token file, four platform modes: dark theme, Windows High Contrast (forced-colors), RTL and print - all handled "
     "from the token layer and logical properties, no second stylesheet, no per-component overrides. In the dark theme "
     "surfaces rise instead of casting shadows.",
     ["platform", "platform modes", "themes", "theme", "dark mode", "dark theme", "light mode", "high contrast",
      "forced colors", "rtl", "rtl support", "print", "print styles", "print stylesheet", "platform support"],
     {"group": "Foundations",
      "modes": ["dark theme - surfaces rise instead of casting shadows; one token file flips both themes",
                "forced-colors / Windows High Contrast - system colours respected; borders via CanvasText",
                "RTL - logical properties (TDS013), one stylesheet, auto-mirroring chips/drawers/tooltips",
                "print - handled from the token layer"],
      "source_file": "site/pages_foundations.py (platform)"}),
    ("guideline/icons", "Iconography",
     "A transferable icon system - 174 glyphs, one spec. The registry is the Lucide set (ISC licence) normalised to the "
     "Triage drawing spec: 24x24 grid, fill:none, stroke:currentColor, stroke-width 1.7, round caps and joins. Ship it "
     "as a sprite (icons/sprite.svg), individual SVGs (icons/svg/*.svg), or a registry (icons/icons.json); original "
     "mail-triage names survive as aliases.",
     ["iconography", "icons", "icon", "icon set", "icon system", "glyph", "glyphs", "icon sprite", "sprite",
      "lucide", "svg icons"],
     {"group": "Foundations",
      "spec": "24x24 grid / fill:none / stroke:currentColor / stroke-width 1.7 / round caps and joins",
      "delivery": ["sprite - icons/sprite.svg + <use>", "individual SVGs - icons/svg/*.svg",
                   "registry - icons/icons.json (path bodies)"],
      "sizes_a11y": "size tokens (--icon-*); decorative icons aria-hidden, meaningful icons labelled",
      "source_file": "site/pages_foundations.py (icons) + icons/icons.json"}),
    ("guideline/accessibility", "Accessibility (WCAG 2.2)",
     "WCAG 2.2 scorecard against the source audit: focus visible, focus not obscured, non-text contrast, target size, "
     "contrast, animation, forced colours, resize and reflow pass; focus appearance partial. The ring is global - "
     ":focus-visible is never removed anywhere; inputs add a border and ring. Reduced motion is honoured.",
     ["accessibility", "a11y", "wcag", "wcag 2.2", "focus", "focus visible", "focus ring", "contrast",
      "contrast rules", "target size", "screen reader", "reduced motion"],
     {"group": "Foundations",
      "focus": ":focus-visible{outline:2px solid var(--interactive);outline-offset:2px} - never removed anywhere",
      "scorecard": ["2.4.7 Focus Visible - pass", "2.4.11 Focus Not Obscured - pass",
                    "1.4.11 Non-Text Contrast - pass", "2.4.13 Focus Appearance - partial",
                    "2.5.8 Target Size - pass", "1.4.3 Contrast - pass", "2.3.3 Animation - pass",
                    "1.4.1 forced colors - pass", "1.4.4 Resize Text - pass", "4.1.3 Status Messages - pass",
                    "1.4.10 Reflow - pass"],
      "source_file": "site/pages_foundations.py (accessibility)"}),
    ("guideline/voice", "Voice & copy",
     "Sentence case for buttons, links and menu items (uppercase micro-labels are CSS). Verbs are Enable/Disable for "
     "entity state. Announce every mutation in past tense, naming the object. Three flash kinds only - ok, warn, err; "
     "info is retired. Name the object in destructive labels. Empty states: title + one-line reason + at most one "
     "action. One-way actions keep a native confirm().",
     ["voice", "voice and copy", "copy", "copy rules", "microcopy", "tone", "writing", "wording", "labels",
      "message copy", "empty state copy"],
     {"group": "Foundations",
      "rules": ["sentence case for buttons, links, menu items",
                "Enable/Disable for entity state - never Pause/Resume or On/Off",
                "announce mutations in past tense, naming the object",
                "three flash kinds only: ok / warn / err - info is retired",
                "name the object in destructive labels and aria-labels",
                "empty states: title + one-line reason + at most one action"],
      "source_file": "site/pages_foundations.py (voice)"}),
    ("guideline/localisation", "Localisation & i18n",
     "RTL is mechanics; i18n is content. The system ships the mechanics - logical properties (TDS013), auto-mirroring "
     "chips/drawers/tooltips and core/i18n.js for locale, messages and formats. Content rules: whole-message "
     "placeholders (never concatenate sentences), counts through plural(), store ISO and display via Intl, room for "
     "extra width (German ~35%), bidi hygiene with <bdi> for embedded identifiers.",
     ["localisation", "localization", "i18n", "internationalisation", "internationalization", "rtl",
      "bilingual", "bilingual copy", "translations", "locale", "plural", "intl"],
     {"group": "Foundations",
      "copy_rules": ["whole-message placeholders - never concatenate sentences",
                     "counts go through plural() (Arabic six forms, Japanese one)",
                     "store ISO, display via Intl: dates YYYY-MM-DD, numbers raw",
                     "give first-class strings room: German adds ~35% width",
                     "bidi hygiene: wrap embedded Latin identifiers in <bdi>"],
      "source_file": "site/pages_foundations.py (localisation) + core/i18n.js"}),
]
for aid, title, summary, aliases, body in FOUNDATIONS:
    body = dict(body)
    body.setdefault("verify", ["site/pages_foundations.py"])
    artifacts.append(A(aid, "guideline", title, summary, aliases, body,
                       "site/pages_foundations.py (%s)" % aid.split("/", 1)[1], ["triage/foundations"]))

# ---- furniture: core components documented on the component group pages ----
FURNITURE = [
    ("component/check", "Checkbox", ".check",
     "A real checkbox wrapped in label.check; forms post a hidden twin (value 0) so a missing key cannot silently "
     "mean off. Grouped checkboxes live in a fieldset with a legend.",
     ["checkbox", "check", "tick box", "checkbox group", "hidden twin"]),
    ("component/dot", "Status dot", ".dot",
     "A 7px square status dot; neutral by default, with ok / warn / err variants paired with text (never colour alone).",
     ["dot", "status dot", "status light", "indicator dot"]),
    ("component/kbd", "Keycap", ".kbd",
     "A monospace keycap with a 2px base edge, for keyboard hints such as shortcuts.",
     ["keycap", "kbd", "keyboard hint", "shortcut hint", "key hint"]),
    ("component/stat", "Stat tile", ".stat",
     "An ink panel carrying one number and its label - the dashboard hero metric.",
     ["stat tile", "stat", "metric tile", "big number", "kpi tile"]),
    ("component/kv", "Key-value rows", ".kv",
     "A two-column metadata grid (label -> value) for detail panes and sidebars.",
     ["key value rows", "kv rows", "metadata rows", "property list", "definition list"]),
    ("component/progress", "Progress", ".progress",
     "A 6px progress bar with an inline variant (.progress-inline) for rows and tasks; pair with text so state never "
     "relies on the bar alone.",
     ["progress bar", "progress", "progress indicator", "inline progress", "loading bar"]),
    ("component/skeleton", "Skeleton", ".skeleton",
     "An animated shimmer placeholder shown while content loads.",
     ["skeleton", "skeleton loader", "shimmer", "loading placeholder"]),
    ("component/logpanel", "Log panel", ".logpanel",
     "An ink terminal panel for logs and streamed output; rows colour by kind (green / amber / red / dim / time).",
     ["log panel", "terminal panel", "console panel", "log viewer", "terminal"]),
    ("component/audit-row", "Audit rows", ".audit-list",
     "Audit trail rows - the flat list of machine and human actions with time, actor and detail columns; the "
     "provenance surface for accountable actions.",
     ["audit row", "audit rows", "audit trail", "audit list", "activity audit"]),
    ("component/bubble", "Chat bubble", ".bubble",
     "A chat message turn (max-width 75%); user and model turns differ by surface, not by colour alone.",
     ["chat bubble", "message bubble", "chat message", "turn bubble"]),
    ("component/composer", "Composer", ".composer",
     "The message input card at the foot of a chat: input, send, and any attachments.",
     ["composer", "message composer", "chat input", "prompt input"]),
    ("component/proposal", "Proposal card", ".proposal",
     "The one visual contract for every AI action that needs review: proposal text, evidence and review actions.",
     ["proposal card", "proposal", "ai action card", "suggestion card"]),
    ("component/menu-pop", "Overflow menu", ".menu-pop",
     "The absolute popover anchored to a trigger; shadows mark it as floating.",
     ["overflow menu", "menu popover", "popover menu", "row menu", "kebab menu"]),
    ("component/scrim", "Scrim", ".scrim",
     "The fixed backdrop behind drawers, sheets and dialogs.",
     ["scrim", "backdrop", "overlay backdrop", "dim layer"]),
    ("component/bottom-nav", "Bottom navigation", ".bottom-nav",
     "The persistent phone tab bar, with view transitions between tabs.",
     ["bottom navigation", "bottom nav", "tab bar", "phone tab bar", "mobile navigation"]),
    ("component/dock", "Dock", ".dock",
     "The slim fixed side panel (46px) for persistent auxiliary tools; opens on demand.",
     ["dock", "side dock", "dock panel"]),
    ("component/topbar", "App topbar", ".topbar",
     "The tablet and phone chrome header (menu, title, theme and density toggles, status); hidden on desktop where "
     "the sidebar carries the brand.",
     ["topbar", "app topbar", "top bar", "mobile header", "app header"]),
    ("component/page-head", "Page header", ".page-head",
     "The title row at the top of a page: title, description and actions.",
     ["page header", "page title block", "page heading", "page frame"]),
    ("component/seg", "Segmented control", ".seg",
     "The inline segmented selector for mutually exclusive views.",
     ["segmented control", "segmented", "seg control", "segmented selector", "toggle group"]),
    ("component/arm-del", "Armed delete", ".arm-del",
     "The two-step, in-place destructive control: the first click arms, the second confirms. No dialog; native "
     "confirm() stays reserved for irreversible actions.",
     ["armed delete", "two-step delete", "in-place confirm", "destructive arm"]),
    ("component/shell", "App shell", ".app",
     "The page skeleton: sidebar, main column and content frame (.app / .side / .main), with the shell contract on "
     "/components/navigation.",
     ["app shell", "shell", "page shell", "layout shell", "sidebar layout"]),
]
for aid, title, cls, summary, aliases in FURNITURE:
    artifacts.append(A(
        aid, "component", title, summary,
        [title.lower()] + aliases,
        {"class": cls.lstrip("."), "group": "Components - furniture",
         "source_file": "core/base.css", "matrix": "documented in core and the component pages; no states-matrix entry",
         "note": summary},
        "core/base.css (%s)" % cls, ["triage/furniture"]))

json.dump({"artifacts": artifacts}, open(os.path.join(OUT, "artifacts.json"), "w"), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- rules -----
rules = []
for r in RULES_SRC["rules"]:
    rules.append({"id": r["id"], "name": r["name"], "severity": r["severity"],
                  "applies_to": r["applies_to"], "summary": r["summary"], "why": r["why"], "fix": r["fix"]})

rules += [
    {"id": "INT001", "name": "armed-two-step-delete", "severity": "error", "applies_to": ["html", "js"],
     "summary": "Item deletes are armed and two-step: the control arms first (label names the object), the second activation deletes; Escape and outside click disarm.",
     "why": "Destructive actions must never fire on one click; the armed pattern makes the object explicit and the step reversible.",
     "fix": "Use .arm-del with data-arm-label; disarm on Escape/outside click/details close."},
    {"id": "INT002", "name": "one-way-confirm", "severity": "warning", "applies_to": ["html", "js"],
     "summary": "One-way / high-stakes actions use confirm() naming the object; reversible mutations instead show their reverse ('Shown as deleted · Undo').",
     "why": "The interaction standard splits destructive undoable from destructive irreversible; each gets the cheapest safe pattern.",
     "fix": "confirm() for irreversible; a visible reverse action for reversible mutations."},
    {"id": "INT003", "name": "three-channel-feedback", "severity": "warning", "applies_to": ["html"],
     "summary": "Feedback uses the three sanctioned channels only: banner (persistent page/section state), toast (transient confirmation), empty state (structural absence) — plus in-flight treatments for long actions.",
     "why": "One feedback taxonomy keeps the product legible; ad-hoc alerts drift.",
     "fix": "Map each message to banner / toast / empty state; use the in-flight pattern for queued work."},
    {"id": "INT004", "name": "editor-save-bars", "severity": "warning", "applies_to": ["html"],
     "summary": "Editors and settings keep a sticky save bar with explicit unsaved-changes state; save bars apply per card in settings patterns.",
     "why": "Explicit save state prevents silent loss in long forms.",
     "fix": "Add .savebar with its unsaved/dirty state; scope per card where sections save independently."},
]
json.dump({"rules": rules}, open(os.path.join(OUT, "rules.json"), "w"), indent=1, ensure_ascii=False)

# ---------------------------------------------------------- prohibitions -----
prohibitions = [
    {"id": "prohibit/raw-colour", "kind": "prohibition",
     "statement": "Raw colour literals (hex/rgb/hsl) outside the token layer — colour arrives only via tokens (lint TDS002).",
     "signals": ["hex colour", "raw hex", "rgb(", "hsl(", "hard-coded colour"], "rule": "TDS002"},
    {"id": "prohibit/focus-removal", "kind": "prohibition",
     "statement": "Removing focus outlines without replacement — :focus-visible affordances are mandatory (lint TDS004).",
     "signals": ["outline none", "remove focus ring", "focus removed"], "rule": "TDS004"},
    {"id": "prohibit/token-override", "kind": "prohibition",
     "statement": "Overriding token values downstream (the token layer is the only place values change; lint TDS009).",
     "signals": ["override token", "redefine variable", "patch css variable"], "rule": "TDS009"},
    {"id": "prohibit/token-fonts", "kind": "prohibition",
     "statement": "Fonts outside the system stack — family tokens own typefaces (lint TDS008).",
     "signals": ["custom font", "webfont", "google font", "font import"], "rule": "TDS008"},
    {"id": "prohibit/off-radius", "kind": "prohibition",
     "statement": "Non-zero corner radius — the system is squarely squared; radius stays 0 (lint TDS003).",
     "signals": ["rounded", "rounded corners", "rounded card", "corner radius", "border radius", "border-radius", "pill shape"], "rule": "TDS003"},
    {"id": "prohibit/label-less-controls", "kind": "prohibition",
     "statement": "Interactive controls without accessible names — icon-only means aria-label, never a bare glyph (lint TDS015).",
     "signals": ["unlabeled", "icon only", "no aria label", "mystery icon"], "rule": "TDS015"},
]
json.dump({"prohibitions": prohibitions}, open(os.path.join(OUT, "prohibitions.json"), "w"), indent=1, ensure_ascii=False)

# ------------------------------------------------------------ fallbacks -----
fallbacks = [
    {"id": "fallback/no-js", "kind": "fallback", "title": "Behaviour without JavaScript",
     "statement": "Every component degrades to its plain markup; the behaviour layer (components.js) is additive. Without JS, interactive widgets show their static forms (tabs stack, menus remain details/summary, file inputs remain native).",
     "scope": ["javascript", "no-js", "degradation"],
     "constraints": ["never require JS for content", "prefer native elements (dialog, details, input) so no-JS still works"]},
    {"id": "fallback/scoped-embedding", "kind": "fallback", "title": "Scoped embedding into a host page",
     "statement": "Drop Triage into an existing product without restyling it: wrap the region in .triage and load core/scoped.css (rules live in @scope(.triage) under @layer triage.components). Font-faces and keyframes stay global. Without core/reset.css the host owns root sizing and typography.",
     "scope": ["integration", "scoped", "adoption", "host page"],
     "constraints": ["host content outside .triage is never restyled", "pair with reset.css for parity, or own the root size"]},
    {"id": "fallback/motion-reduction", "kind": "fallback", "title": "Reduced-motion handling",
     "statement": "The system honours prefers-reduced-motion: spinners slow to the slow duration and reveal transitions collapse. Motion tokens stay the single source for durations either way.",
     "scope": ["motion", "accessibility", "reduced motion"],
     "constraints": ["never opt out of the user preference", "keep durations on tokens even in the reduced path"]},
]
json.dump({"fallbacks": fallbacks}, open(os.path.join(OUT, "fallbacks.json"), "w"), indent=1, ensure_ascii=False)

# ----------------------------------------------------------- precedents -----
precedents = [
    {"id": "precedent/renamed-vocabulary", "kind": "precedent", "title": "Vocabulary rename (0.1.0 sweep)",
     "request": "keep the pre-0.1.0 (mail-triage era) class/id vocabulary alongside new names",
     "matches": ["old class names", "legacy vocabulary", "mail-triage names", "deprecated classes"],
     "decision": "accepted — old names retired", "grounds": "TDS001: pre-Triage names are no longer styled by core.css and silently fall back to browser defaults.",
     "reason": "One public vocabulary keeps the contract checkable; a rename map exists for migration.",
     "scope": {"domains": ["css", "html", "js"], "boundary": ["class names", "ids", "globals"]},
     "try": ["rename via RENAME-MAP.md", "run the assemble map tool for bulk migrations"],
     "citation": "rename-map.json + RENAME-MAP.md; spec/rules.json TDS001",
     "provenance": {"source": "triage-design-system 0.1.0 rename sweep", "note": "enforced by lint"}},
]
json.dump({"precedents": precedents}, open(os.path.join(OUT, "precedents.json"), "w"), indent=1, ensure_ascii=False)

# ----------------------------------------------------------- candidates -----
candidates = [
    {"id": "candidate/behavioural-verification", "kind": "candidate",
     "title": "Declared behavioural (L2) evidence per component",
     "request": "prove interactive components behave, not just that their selectors exist",
     "matches": ["behavioural verification", "behaviour tests", "keyboard tests", "state transitions"],
     "status": "candidate",
     "summary": "Level 2 currently covers several families (badges, interaction, layout, contrast, roles, screens; datepicker arithmetic pinned). Overlays, combobox, command palette, dialog focus-restore and mobile sheets lack declared behavioural evidence.",
     "emerges_from": ["external review 2026-10 (point C)", "spec/proposals/verification-levels.md"],
     "evidence_present": "headless-Chrome fixtures exist; spec/states.json lists verify selectors per component.",
     "promote_when": ["tests/browser coverage extended to overlays, combobox, command palette, dialog and sheets",
                      "each component row in spec/states.json declares its L2 test ids",
                      "CI runs the behavioural set on every change"],
     "provenance": {"source": "triage repo review + proposals"}},
    {"id": "candidate/rendered-verification", "kind": "candidate",
     "title": "Rendered (L3) conformance — condition matrix + baselines",
     "request": "verify how builds render, not only what they declare",
     "matches": ["rendered verification", "visual regression", "screenshots", "overflow", "zoom"],
     "status": "candidate",
     "summary": "No automated rendered conformance: responsive overflow, 200% text zoom, dark mode, reduced motion, print and forced-colors are unchecked by the gate. Proposed: screenshot pass keyed by component id, diffed against metrics/ui-baseline.json.",
     "emerges_from": ["external review 2026-10 (point C)", "spec/proposals/verification-levels.md"],
     "evidence_present": "screens gallery exists; metrics/ui-baseline.json exists; tests/browser has the Chrome harness.",
     "promote_when": ["baseline harness lands in tests/browser",
                      "condition matrix (zoom/dark/reduced-motion/print/forced-colors) recorded per component",
                      "L3 evidence declared in spec/states.json"],
     "provenance": {"source": "triage repo review + proposals"}},
    {"id": "candidate/provenance-contract", "kind": "candidate",
     "title": "Machine-action provenance record (formal component contract)",
     "request": "audit records that are evidence, distinct from transcripts and explanations",
     "matches": ["provenance", "audit record", "provenance contract", "machine action", "reasoning"],
     "status": "candidate",
     "summary": "A required record shape for machine actions: action, initiating authority, input evidence, rule/model version, evaluation outcome, timestamp, state change, available reversal. Explanations are supplementary; confidence numbers need calibration or are omitted.",
     "emerges_from": ["external review 2026-10 (point F)", "spec/proposals/provenance-contract.md"],
     "evidence_present": "chat components already separate reasoning folds, tool disclosures and proposals; rule-versus-model rows exist.",
     "promote_when": ["field schema merged into spec/",
                      "one live surface rebuilt with the record (chat proposal card or audit row)",
                      "lint check for record presence on machine actions"],
     "provenance": {"source": "triage repo review + proposals"}},
    {"id": "candidate/theme-profiles", "kind": "candidate",
     "title": "Invariants vs theme opinions (adoption profiles)",
     "request": "let adopters keep Triage's quality bar without inheriting every aesthetic choice",
     "matches": ["theme profiles", "adoption", "invariants", "themeability", "radius policy"],
     "status": "candidate",
     "summary": "Split core invariants (status semantics, accessibility, state contracts, reversibility, traceability — always enforced) from theme opinions (radius, typeface, button fills, accent, density — overridable via a declared theme file). Strict profile stays the default identity.",
     "emerges_from": ["external review 2026-10 (point D)", "spec/proposals/theme-profiles.md"],
     "evidence_present": "scoped consumption path already exists; radius reset currently !important-locked.",
     "promote_when": ["owner decision on adopt mode",
                      "theme.json mechanism implemented and lint reads profiles",
                      "radius reset moved behind its token"],
     "provenance": {"source": "triage repo review + proposals"}},
    {"id": "candidate/hierarchy-and-density", "kind": "candidate",
     "title": "Hierarchy pass + density/border discipline",
     "request": "make the interface decide what deserves attention first",
     "matches": ["hierarchy", "density", "typography floor", "border discipline", "message list"],
     "status": "candidate",
     "summary": "The message-list and dashboard patterns get a pass against the three-level model (attention/decision → what happened → telemetry); supporting labels move toward 13–14px in comfortable density (12px reserved for secondary metadata); borders become structure/interaction-only with grouping via spacing and type.",
     "emerges_from": ["external review 2026-10 (points A and E)", "spec/proposals/density-borders.md"],
     "evidence_present": "published screens show the proposed-rule card pushing messages below the fold; dashboard flattens priorities.",
     "promote_when": ["both patterns rebuilt against the three-level model",
                      "label tiers applied and documented; border-discipline checklist added to INTERACTION.md",
                      "the hierarchy change survives the L4 experiment"],
     "provenance": {"source": "triage repo review + proposals"}},
]
json.dump({"candidates": candidates}, open(os.path.join(OUT, "candidates.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"recipes": []}, open(os.path.join(OUT, "recipes.json"), "w"), indent=1, ensure_ascii=False)

# ------------------------------------------------------------- golden -------
golden = {
    "version": "0.1", "pack_version": "triage %s" % V,
    "cases": [
        {"problem": "a primary button", "expect": "RESOLVED", "expect_id": "component/btn"},
        {"problem": "an icon-only button", "expect": "RESOLVED", "expect_id": "component/iconbtn"},
        {"problem": "a switch", "expect": "RESOLVED", "expect_id": "component/px-sw"},
        {"problem": "a menu item", "expect": "RESOLVED", "expect_id": "component/menu-item"},
        {"problem": "a nav item", "expect": "RESOLVED", "expect_id": "component/nav-item"},
        {"problem": "a chip", "expect": "RESOLVED", "expect_id": "component/chip"},
        {"problem": "a data table", "expect": "RESOLVED", "expect_id": "component/tbl"},
        {"problem": "a version timeline", "expect": "RESOLVED", "expect_id": "component/tl"},
        {"problem": "a bulk action bar", "expect": "RESOLVED", "expect_id": "component/bulkbar"},
        {"problem": "a save bar", "expect": "RESOLVED", "expect_id": "component/savebar"},
        {"problem": "a flash message", "expect": "RESOLVED", "expect_id": "component/msg"},
        {"problem": "a banner", "expect": "RESOLVED", "expect_id": "component/msg"},
        {"problem": "a tint banner", "expect": "RESOLVED", "expect_id": "component/msg"},
        {"problem": "a solid banner", "expect": "RESOLVED", "expect_id": "component/msg"},
        {"problem": "an informational banner", "expect": "RESOLVED", "expect_id": "component/msg"},
        {"problem": "the design philosophy", "expect": "RESOLVED", "expect_id": "guideline/philosophy"},
        {"problem": "the logo and brand mark", "expect": "RESOLVED", "expect_id": "guideline/brand"},
        {"problem": "dark mode", "expect": "RESOLVED", "expect_id": "guideline/platform"},
        {"problem": "the icon set", "expect": "RESOLVED", "expect_id": "guideline/icons"},
        {"problem": "accessibility", "expect": "RESOLVED", "expect_id": "guideline/accessibility"},
        {"problem": "the voice and copy rules", "expect": "RESOLVED", "expect_id": "guideline/voice"},
        {"problem": "localisation and i18n", "expect": "RESOLVED", "expect_id": "guideline/localisation"},
        {"problem": "a checkbox", "expect": "RESOLVED", "expect_id": "component/check"},
        {"problem": "a progress bar", "expect": "RESOLVED", "expect_id": "component/progress"},
        {"problem": "a chat bubble", "expect": "RESOLVED", "expect_id": "component/bubble"},
        {"problem": "a proposal card", "expect": "RESOLVED", "expect_id": "component/proposal"},
        {"problem": "a keycap", "expect": "RESOLVED", "expect_id": "component/kbd"},
        {"problem": "a toast notification", "expect": "RESOLVED", "expect_id": "component/toast2"},
        {"problem": "a status badge", "expect": "RESOLVED", "expect_id": "component/badge"},
        {"problem": "an empty state", "expect": "RESOLVED", "expect_id": "component/empty"},
        {"problem": "a dialog", "expect": "RESOLVED", "expect_id": "component/dlg"},
        {"problem": "a tooltip", "expect": "RESOLVED", "expect_id": "component/tip"},
        {"problem": "a loading spinner", "expect": "RESOLVED", "expect_id": "component/spinner"},
        {"problem": "tabs", "expect": "RESOLVED", "expect_id": "component/tabs"},
        {"problem": "breadcrumbs", "expect": "RESOLVED", "expect_id": "component/crumbs"},
        {"problem": "a radio group", "expect": "RESOLVED", "expect_id": "component/radio"},
        {"problem": "a range slider", "expect": "RESOLVED", "expect_id": "component/slider"},
        {"problem": "an autocomplete", "expect": "RESOLVED", "expect_id": "component/cb"},
        {"problem": "a date picker", "expect": "RESOLVED", "expect_id": "component/dp"},
        {"problem": "an accordion", "expect": "RESOLVED", "expect_id": "component/acc"},
        {"problem": "a user avatar", "expect": "RESOLVED", "expect_id": "component/avatar-sq"},
        {"problem": "a file dropzone", "expect": "RESOLVED", "expect_id": "component/drop"},
        {"problem": "a notifications panel", "expect": "RESOLVED", "expect_id": "component/notif"},
        {"problem": "a command palette", "expect": "RESOLVED", "expect_id": "component/cmd"},
        {"problem": "numbered pagination", "expect": "RESOLVED", "expect_id": "component/pager-num"},
        {"problem": "a diff view", "expect": "RESOLVED", "expect_id": "component/diff"},
        {"problem": "a bottom sheet", "expect": "RESOLVED", "expect_id": "component/sheet-end"},
        {"problem": "a dashboard page", "expect": "RESOLVED", "expect_id": "pattern/dashboard"},
        {"problem": "a settings page", "expect": "RESOLVED", "expect_id": "pattern/settings"},
        {"problem": "the colour tokens", "expect": "RESOLVED", "expect_id": "token-set/colour"},
        {"problem": "the color tokens", "expect": "RESOLVED", "expect_id": "token-set/colour"},
        {"problem": "a dialogue", "expect": "RESOLVED", "expect_id": "component/dlg"},
        {"problem": "the spacing scale", "expect": "RESOLVED", "expect_id": "token-set/spacing"},
        {"problem": "rounded corners on the cards", "expect": "CONFLICT"},
        {"problem": "make all the buttons rounded", "expect": "CONFLICT"},
        {"problem": "a carousel", "expect": "UNDEFINED"},
    ],
}
json.dump(golden, open(os.path.join(OUT, "golden.json"), "w"), indent=1, ensure_ascii=False)

build = {
    "generator": "docs/synthesis/triage/tools/build_triage_pack.py",
    "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "source": {"repo": TR, "commit": _src_commit, "version": V},
    "counts": {"artifacts": len(artifacts), "rules": len(rules),
               "prohibitions": len(prohibitions), "fallbacks": len(fallbacks),
               "precedents": len(precedents), "candidates": len(candidates),
               "golden_cases": len(golden["cases"])},
}
json.dump(build, open(os.path.join(OUT, "BUILD.json"), "w"), indent=1)

print("emitted packs/triage: %d artifacts, %d rules, %d prohibitions, %d fallbacks, %d precedents, %d candidates, %d golden cases"
      % (len(artifacts), len(rules), len(prohibitions), len(fallbacks), len(precedents), len(candidates), len(golden["cases"])))
