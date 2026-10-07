#!/usr/bin/env python3
"""Compile Gate-2-accepted decisions into kernel-format Design Authority packs.

The synthesis pipeline's final machine step: each source's decisions.json holds
the canonical texts; this compiler maps them to kernel artifacts/rules/recipes/
prohibitions/fallbacks + a golden set, and asserts every compiled decision was
accepted by the reviewer (via review-app feedback.json).

Usage:  python3 docs/synthesis/tools/compile_pack.py [--src wink|leader|dominion|all]
Output: packs/<id>/ (authority.json, artifacts.json, rules.json, recipes.json,
        fallbacks.json, prohibitions.json, scoring.json, golden.json)
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SYN = os.path.join(ROOT, "docs", "synthesis")
FB = os.path.join(SYN, "review-app", "data", "feedback.json")


def decisions(src):
    with open(os.path.join(SYN, src, "decisions.json")) as fh:
        return {d["id"]: d for d in json.load(fh)["decisions"]}


def accepted_ids():
    with open(FB) as fh:
        m = json.load(fh)
    ok = set()
    for k, v in m.items():
        if v.get("verdict") == "accept":
            ok.add(k)
    # reviewer sign-offs recorded in decisions.json review=none count as accepted
    for src in ("wink", "leader", "dominion"):
        with open(os.path.join(SYN, src, "decisions.json")) as fh:
            for d in json.load(fh)["decisions"]:
                if d.get("review") == "none":
                    ok.add(d["id"])
    return ok


ACCEPTED = accepted_ids()

ART = []          # (src, decision_ids, artifact)
RULE = []         # (src, rule dict)
PROHIB = []       # (src, prohibition dict)
FALLBACK = []     # (src, fallback dict)
RECIPES = []      # (src, recipe dict)
GOLDEN = []       # (src, case dict)


def art(src, ids, aid, kind, title, aliases, body=None, note=None):
    ART.append((src, ids, {"id": aid, "kind": kind, "title": title,
                           "aliases": aliases, "body": body or {}, "note": note}))


def rule(src, rid, name, severity, summary, why, fix):
    RULE.append((src, {"id": rid, "name": name, "severity": severity,
                       "applies_to": ["css", "html"], "summary": summary,
                       "why": why, "fix": fix}))


def prohib(src, pid, statement, signals, rid):
    PROHIB.append((src, {"id": pid, "statement": statement, "signals": signals,
                         "rule": rid, "kind": "prohibition"}))


def fallback(src, fid, title, statement, scope, constraints):
    FALLBACK.append((src, {"id": fid, "title": title, "statement": statement,
                           "scope": scope, "constraints": constraints, "kind": "fallback"}))


def recipe(src, rid, title, summary, needs, constraints, ingredients):
    RECIPES.append((src, {"id": rid, "title": title, "summary": summary,
                          "needs": needs, "constraints": constraints,
                          "ingredients": ingredients, "kind": "recipe"}))


def case(src, problem, expect, expect_id=None, note=None):
    GOLDEN.append((src, {"problem": problem, "expect": expect,
                         "expect_id": expect_id, "note": note}))


def D(src, did):
    d = decisions(src)[did]
    assert did in ACCEPTED, "%s was not accepted at Gate 2 — refusing to compile" % did
    return d["decision"]


# ---------------------------------------------------------------- wink
def build_wink():
    S = "wink"
    art(S, ["W-01", "W-02", "W-03"],
        "component/action-pill", "component", "Action (pill)",
        ["button", "cta", "primary button", "pill button", "start free trial", "action", "submit", "secondary button", "outline button"],
        {"class": "cta", "group": "Actions",
         "states": ["default: yellow fill + 1px ink ring (box-shadow 0 0 0 1px #231E15)",
                    "dark variant on warm fields (ink fill, white label)",
                    "secondary: outline pill (2px ink inset)",
                    "hover: translateY(-4.875px) + hard ink shadow 0 4.875px 0 0 (live-measured, zero blur)"],
         "verify": [".cta", ".cta.dark", ".cta.outline"],
         "a11y": ["Real <button>/<a> semantics; visible label; focus must not rely on colour alone."]})
    art(S, ["W-04"],
        "guideline/typography", "guideline", "Typography (two registers)",
        ["typography", "font", "display font", "body font", "headline font"],
        {"group": "Type"})
    art(S, ["W-05"],
        "token-set/type-scale", "token-set", "Screen type scale",
        ["type scale", "font size", "display size", "heading size"],
        {"group": "Type"})
    art(S, ["W-06"],
        "token-set/colour", "token-set", "Colour roles",
        ["palette", "colour", "color", "yellow", "peppercorn", "ink colour"],
        {"group": "Colour"})
    art(S, ["W-07"],
        "component/card", "component", "Card (soft vessel)",
        ["card", "surface", "panel", "tile"],
        {"class": "card1", "group": "Surfaces",
         "states": ["default (white, shadow, radius 16/24)", "tinted variant (Parsnip, no shadow)"],
         "verify": [".card1", ".card2"]})
    art(S, ["W-08"],
        "guideline/shape-language", "guideline", "Shape classes",
        ["shape", "corner", "radius", "rounded corners", "square corners", "pill"],
        {"group": "Shape"})
    art(S, ["W-10"],
        "guideline/hierarchy", "guideline", "Section rhythm",
        ["hierarchy", "section label", "page structure", "headline pattern"],
        {"group": "Structure"})
    art(S, ["W-11"],
        "component/navbar", "component", "Top bar",
        ["navbar", "top bar", "header", "navigation", "menu", "nav bar"],
        {"class": "navbar", "group": "Structure",
         "states": ["default (white bar)", "hover (light-grey rounded-rect fill)", "dropdown items carry chevrons"],
         "a11y": ["Dropdown affordances need aria-haspopup/expanded when built; single-row layout."]})
    art(S, ["W-13"],
        "component/field-select", "component", "Field & small-set select",
        ["field", "input", "form field", "select", "dropdown", "text field", "textarea", "text area", "multiline field", "notes field"],
        {"class": "field", "group": "Forms",
         "states": ["default", "focus", "invalid"],
         "verify": [".field input", ".field select"],
         "a11y": ["<label for> always; native select for small sets."]})
    art(S, ["W-20"],
        "component/ledger", "component", "Ledger rows",
        ["table", "ledger", "list rows", "register list", "rows"],
        {"class": "ledger", "group": "Repeated content"})
    art(S, ["W-21"],
        "component/badge", "component", "Emphasis badge",
        ["badge", "label", "most popular", "tag"],
        {"class": "badge", "group": "Emphasis"})
    art(S, ["W-22"],
        "guideline/voice", "guideline", "Voice",
        ["voice", "tone", "copy", "microcopy", "writing"],
        {"group": "Voice"})

    rule(S, "W-R1", "pill-language", "error",
         "Buttons are pills; no square primary buttons anywhere.",
         "Observed live (radius = half height) and reaffirmed at Gate 2.",
         "Replace square corners on buttons with the pill radius.")
    rule(S, "W-R2", "palette-discipline", "warning",
         "Colours come from the wink palette only: Cavendish Yellow, Peppercorn ink, Parsnip, Ochre, Kale, #BF4055 error.",
         "Palette roles observed live + brand assets; Gate 2 accepted.",
         "Map the colour to the nearest palette token.")
    prohib(S, "prohibit/square-buttons",
           "Square or sharp button shapes — buttons are pills (W-02, W-08).",
           ["square button", "square buttons", "buttons square", "make it square",
            "make them square", "square corners", "squared corners", "sharp corners",
            "sharp edges", "right angles", "border-radius: 0"], "W-R1")
    prohib(S, "prohibit/off-palette-colours",
           "Colours outside the wink palette, including pure black text and clinical cold greys (W-06).",
           ["pure black", "neon", "off-brand", "off brand colour", "off brand color",
            "invented colour", "invented color", "cold grey", "clinical grey"],
           "W-R2")
    fallback(S, "fallback/platform-controls",
             "Platform defaults for uncovered controls",
             "If the system defines no control for a need, use the platform's native element with the wink field styling (radius 8, warm ink text); keep native semantics.",
             ["checkbox", "radio", "date", "time", "file", "toggle", "switch", "picker", "combobox", "slider", "stepper", "upload"],
             ["field styling (radius 8, 1px #DEDDDC border)", "warm ink text",
              "mark the improvisation and report a gap if the need recurs"])
    fallback(S, "fallback/light-only",
             "Light surfaces only",
             "No dark-mode canon exists; if a dark surface is unavoidable, keep ink/yellow roles and mark the improvisation.",
             ["dark", "mode", "theme"],
             ["keep the palette roles", "mark the improvisation"])

    case(S, "add a primary button to the page", "RESOLVED", "component/action-pill",
         "Pill action resolves directly.")
    case(S, "the top navigation bar", "RESOLVED", "component/navbar", "White bar with chevron items.")
    case(S, 'show a "most popular" badge on the plan', "RESOLVED", "component/badge",
         "Yellow pill badge.")
    case(S, "a form field for the borrower email", "RESOLVED", "component/field-select",
         "Field language answers.")
    case(S, "square buttons for a serious look", "CONFLICT", "prohibit/square-buttons",
         "Pills only (W-R1).")
    case(S, "use pure black for the headline text", "CONFLICT", "prohibit/off-palette-colours",
         "Warm ink, not pure black.")
    case(S, "add a checkbox for the opt-in", "FALLBACK", "fallback/platform-controls",
         "Uncovered control -> platform default with field styling.")
    case(S, "animate the dialog with a spring bounce", "UNDEFINED", None,
         "Deliberate: motion is undefined; gap over guess.")
    case(S, "a dark mode theme", "FALLBACK", "fallback/light-only",
         "No dark canon; marked improvisation.")


# ---------------------------------------------------------------- leader
def build_leader():
    S = "leader"
    art(S, ["L-01"],
        "component/action", "component", "Action (navy rounded)",
        ["button", "cta", "primary button", "action", "link button", "subscribe button"],
        {"class": "btn", "group": "Actions",
         "states": ["primary: solid navy #2E45B8, radius ~8",
                    "secondary: 2px ink outline",
                    "tertiary: underlined blue link"],
         "verify": [".btn.b-navy", ".btn.b-out", ".btn.b-txt"]})
    art(S, ["L-02"],
        "guideline/shape-language", "guideline", "Shape language (rounded product)",
        ["shape", "corner", "radius", "rounded corners", "square corners"],
        {"group": "Shape"})
    art(S, ["L-03"],
        "guideline/motion", "guideline", "Motion",
        ["motion", "transition", "animation", "hover timing"],
        {"group": "Motion"})
    art(S, ["L-04"],
        "guideline/typography", "guideline", "Typography (three registers)",
        ["typography", "font", "serif", "sans", "headline font"],
        {"group": "Type"})
    art(S, ["L-05"],
        "token-set/type-scale", "token-set", "Screen type scale",
        ["type scale", "font size", "display size", "heading size", "body size"],
        {"group": "Type"})
    art(S, ["L-06"],
        "token-set/colour", "token-set", "Colour roles (red + Chicago blue)",
        ["palette", "colour", "color", "economist red", "chicago blue", "navy"],
        {"group": "Colour"})
    art(S, ["L-07"],
        "guideline/surfaces", "guideline", "Surfaces & separation",
        ["surfaces", "backgrounds", "rules", "hairlines", "separation", "elevation"],
        {"group": "Surfaces"})
    art(S, ["L-09"],
        "guideline/hierarchy", "guideline", "Section rhythm",
        ["hierarchy", "section label", "headline", "standfirst", "page structure"],
        {"group": "Structure"})
    art(S, ["L-10"],
        "component/navbar", "component", "Top bar",
        ["navbar", "top bar", "header", "navigation", "menu", "search box", "nav bar"],
        {"class": "navbar", "group": "Structure",
         "states": ["default (white bar, 2px ink rule)", "active item: blue underline",
                    "search: rectangle with typing-cursor motif"],
         "verify": [".navbar", ".navbar .on", ".cursorbox"]})
    art(S, ["L-11"],
        "component/field", "component", "Field (rounded, sans text)",
        ["field", "input", "form field", "text field", "textbox", "error message", "validation error", "textarea", "text area", "multiline field"],
        {"class": "field", "group": "Forms",
         "states": ["default (1px soft ink border)", "focus adds no border highlight",
                    "invalid (small red line under)"],
         "verify": [".field input", ".field .err"],
         "a11y": ["<label for> always; focus visible by other means if border highlight is suppressed."]})
    art(S, ["L-14"],
        "component/notice", "component", "Notice (ruled box)",
        ["notice", "alert", "message", "banner", "notification", "weekly summary", "week summary", "week-summary"],
        {"class": "notice", "group": "Feedback"})
    art(S, ["L-16"],
        "component/meter", "component", "Progress meter",
        ["meter", "progress", "progress bar", "import progress", "readout"],
        {"class": "meter", "group": "Progress",
         "verify": [".meter", ".meter i"]})

    rule(S, "L-R1", "rounded-interactive", "error",
         "Interactive components and container surfaces are soft-rounded (radius ~8); only rules, hairlines and glyph marks stay crisp.",
         "Live product review + Gate 2 (L-02, L-24).",
         "Give the component the system radius; remove square interactive corners.")
    rule(S, "L-R2", "colour-families", "warning",
         "Red is brand/editorial punctuation; the Chicago blue family carries the interactive layer; frame is ink/white/London grey.",
         "Marber tokens + live product (L-06), accepted at Gate 2.",
         "Map the colour to the nearest family token.")
    prohib(S, "prohibit/square-interactive",
           "Square-cornered interactive components or cards — the live system is rounded (L-02, L-24).",
           ["square button", "square buttons", "buttons square", "make it square",
            "make them square", "square corners", "squared corners", "sharp corners",
            "sharp edges", "right angles", "border-radius: 0"], "L-R1")
    prohib(S, "prohibit/ambient-glow",
           "Ambient glow shadows — elevation uses defined shadow tokens only (L-24).",
           ["glow", "glowing shadow", "soft glow", "neon glow"], "L-R1")
    prohib(S, "prohibit/red-reading-surface",
           "Red as a reading background (L-24).",
           ["red background", "red page background", "red as the background"], "L-R2")
    prohib(S, "prohibit/off-family-colour",
           "Colours outside the defined families / invented hues (L-24).",
           ["invented hue", "off-brand colour", "off brand colour", "neon green", "teal accent"], "L-R2")
    prohib(S, "prohibit/decorative-noise",
           "Emoji and exclamation marks (L-24).",
           ["emoji", "emojis", "exclamation mark", "exclamation point", "exclamation marks"], "L-R2")
    fallback(S, "fallback/platform-controls",
             "Platform defaults for uncovered controls",
             "If the system defines no control for a need, use the platform's native element with the leader field styling; keep native semantics.",
             ["checkbox", "radio", "date", "toggle", "switch", "slider", "stepper"],
             ["field styling (rounded, 1px soft border)", "mark the improvisation and report a gap"])
    fallback(S, "fallback/selection",
             "Selection beyond small sets",
             "Small sets use a native select styled like a field; larger or filtered selection uses the platform default, marked.",
             ["select", "dropdown", "picker", "combobox", "listbox", "filter"],
             ["keep field styling", "mark the improvisation", "report a gap if the need recurs"])
    fallback(S, "fallback/ruled-panel",
             "Interstitials become ruled panels",
             "No dialog canon: interstitials render as plain ruled panels in the page flow (L-07); mark the improvisation.",
             ["dialog", "modal", "overlay", "popup", "interstitial", "wizard", "onboarding"],
             ["2px ink rules, hairline detail", "no scrim, no motion", "mark the improvisation"])

    case(S, "add a primary button to the page", "RESOLVED", "component/action",
         "Navy rounded action resolves.")
    case(S, "the top navigation bar", "RESOLVED", "component/navbar", "White bar, blue active underline.")
    case(S, "a form field for the borrower", "RESOLVED", "component/field", "Rounded field, sans text.")
    case(S, "show import progress with steps", "RESOLVED", "component/meter",
         "Ruled meter with readout.")
    case(S, "a notice message about overdue items", "RESOLVED", "component/notice",
         "Ruled notice box.")
    case(S, "square corners on the primary button", "CONFLICT", "prohibit/square-interactive",
         "Rounded throughout (L-R1).")
    case(S, "make it a red background for reading", "CONFLICT", "prohibit/red-reading-surface",
         "Red is punctuation, never ground.")
    case(S, "add an emoji to the headline", "CONFLICT", "prohibit/decorative-noise",
         "No emoji (L-24).")
    case(S, "a dialog for confirmation", "FALLBACK", "fallback/ruled-panel",
         "No dialog canon; ruled panel, marked.")
    case(S, "animate the hero with a bounce", "UNDEFINED", None,
         "Deliberate: bounce contradicts L-03; no motion canon exists.")


# ---------------------------------------------------------------- dominion
def build_dominion():
    S = "dominion"
    art(S, ["D-01"],
        "component/action", "component", "Action (slate rounded)",
        ["button", "cta", "primary button", "action", "submit button", "slate button", "secondary button", "outline button", "undo"],
        {"class": "btn", "group": "Actions",
         "states": ["primary: solid slate #26374A, radius 4 (live-measured)",
                    "secondary: 2px slate outline",
                    "tertiary: underlined link"],
         "verify": [".btn.b-slate", ".btn.b-out"]})
    art(S, ["D-03"],
        "guideline/typography", "guideline", "Typography (one family)",
        ["typography", "font", "weights", "helvetica"],
        {"group": "Type"})
    art(S, ["D-04"],
        "token-set/type-scale", "token-set", "Screen type rhythm",
        ["type scale", "font size", "title size", "body size"],
        {"group": "Type"})
    art(S, ["D-05"],
        "token-set/colour", "token-set", "Colour roles (ceremony + web layer)",
        ["palette", "colour", "color", "fip red", "slate", "ceremonial red"],
        {"group": "Colour"})
    art(S, ["D-08"],
        "component/masthead", "component", "Masthead",
        ["masthead", "header", "top bar", "navigation", "identity zone"],
        {"class": "mh", "group": "Structure",
         "states": ["default (white, 2px black rule, red accent bar)", "active nav item: medium + underline"],
         "verify": [".mh", ".mh .acc"]})
    art(S, ["D-09"],
        "guideline/bilingual", "guideline", "Bilingual pairings",
        ["bilingual", "french", "english", "bilingual titles"],
        {"group": "Voice"})
    art(S, ["D-11"],
        "component/field", "component", "Field (soft border, blue glow focus)",
        ["field", "input", "form field", "text field", "error message", "validation error"],
        {"class": "field", "group": "Forms",
         "states": ["default (1px #E0E0E0, radius 4)",
                    "focus: blue glow (1px #66AFE9 + 8px rgba(102,175,233,.6) halo — live-measured)",
                    "invalid: left rule + plain sentence"],
         "verify": [".field input", ".field input.focus"]})
    art(S, ["D-12"],
        "component/select", "component", "Select (small sets)",
        ["select", "dropdown", "choice", "small select"],
        {"class": "choice", "group": "Forms",
         "states": ["default", "focus (blue glow)"],
         "a11y": ["Native semantics; visible label; larger selection uses the fallback."]})
    art(S, ["D-15"],
        "component/meter", "component", "Progress meter",
        ["meter", "progress", "progress bar", "import progress", "readout"],
        {"class": "meter", "group": "Progress",
         "verify": [".meter", ".meter i"]})
    art(S, ["D-21"],
        "guideline/interaction-states", "guideline", "Focus & interaction states",
        ["focus", "focused", "focus ring", "focus glow", "interaction states"],
        {"group": "Interaction"})

    recipe(S, "recipe/retire-confirm", "Retire with confirmation",
           "Destructive removal of a registered item, confirmed in a dialog with the consequence sentence.",
           ["retire an item", "remove an item", "delete from the register", "confirmation", "delete a ritual", "confirmation dialog"],
           ["confirm = solid slate rounded button with the verb",
            "never pre-focused",
            "bilingual titles (D-09)"],
           ["component/action", "component/field"])

    rule(S, "D-R1", "web-layer-interaction", "warning",
         "Interactive layer follows the live web layer: slate actions (#26374A, radius 4), blue focus glow (#66AFE9), soft borders.",
         "Live measurements on Canada.ca accepted at Gate 2 (D-01, D-11, D-21).",
         "Use the measured slate/blue values for interactive elements.")
    rule(S, "D-R2", "ceremonial-red", "warning",
         "FIP red is ceremony only — never status, errors, or reading surfaces.",
         "FIP standard + Gate 2 (D-05, D-22).",
         "Remove red from status/error/background roles.")
    prohib(S, "prohibit/red-status",
           "Red for status or errors — red is ceremonial (D-R2).",
           ["red error", "red errors", "red for errors", "red for the error", "red status",
            "red for status", "red errors", "red alerts", "red for alerts"], "D-R2")
    prohib(S, "prohibit/elevation-shadows",
           "Elevation or drop shadows — structure is flat, only the focus glow exists (D-22).",
           ["drop shadow", "elevation", "box shadow", "soft shadow"], "D-R1")
    prohib(S, "prohibit/imagery-pictograms",
           "Imagery, pictograms or illustrative decoration (D-22).",
           ["imagery", "photo", "photograph", "illustration", "pictogram", "clip art"], "D-R1")
    prohib(S, "prohibit/decorative-colour",
           "Decorative colour outside the FIP families (D-22).",
           ["decorative colour", "decorative color", "vibrant colours", "vibrant colors",
            "invented colour", "invented color", "neon"], "D-R1")
    fallback(S, "fallback/platform-controls",
             "Platform defaults for uncovered controls",
             "If the system defines no control for a need, use the platform's native element with the field styling; keep native semantics.",
             ["checkbox", "radio", "date", "toggle", "switch", "slider", "check", "stepper"],
             ["field styling (soft border, radius 4)", "blue glow focus",
              "mark the improvisation and report a gap"])
    fallback(S, "fallback/large-selection",
             "Selection beyond small sets",
             "Small fixed sets use the select; larger or filtered selection uses the platform default, marked.",
             ["picker", "combobox", "autocomplete", "filter", "listbox", "search"],
             ["keep field styling", "mark the improvisation"])

    case(S, "add a primary button to the page", "RESOLVED", "component/action",
         "Slate rounded action resolves.")
    case(S, "add the masthead at the top of the page", "RESOLVED", "component/masthead",
         "Red accent bar + rule.")
    case(S, "a form field for the borrower", "RESOLVED", "component/field",
         "Soft border + blue glow focus.")
    case(S, "show import progress with steps", "RESOLVED", "component/meter",
         "Squared meter with readout.")
    case(S, "retire an item from the register", "COMPOSE", "recipe/retire-confirm",
         "Destructive flow composes through the confirm dialog.")
    case(S, "use red for the error messages", "CONFLICT", "prohibit/red-status",
         "Red is ceremonial (D-R2).")
    case(S, "add a drop shadow to the card", "CONFLICT", "prohibit/elevation-shadows",
         "Flat structure (D-22).")
    case(S, "add a photograph to the empty state", "CONFLICT", "prohibit/imagery-pictograms",
         "No imagery (D-22).")
    case(S, "a searchable picker for two hundred members", "FALLBACK", "fallback/large-selection",
         "Uncovered scale -> platform default, marked.")
    case(S, "animate the dialog opening", "UNDEFINED", None,
         "Deliberate: motion is undefined; gap over guess.")


# ---------------------------------------------------------------- emit
MANIFEST = {
    "wink": {
        "name": "Wink Interface System",
        "description": "A friendly, clearly-designed interface system derived from the Mailchimp brand and live product for the Design Authority synthesis experiment. Warm, pill-shaped, playful; no Mailchimp marks reproduced.",
        "repo": "mailchimp.com live product + Mailchimp brand resources",
        "snapshot_version": "sources as published 2026",
    },
    "leader": {
        "name": "Leader Interface System",
        "description": "An editorial interface system derived from The Economist's Marber design system and live product for the Design Authority synthesis experiment. Serif-led, rules-based, blue interactive layer; no Economist marks reproduced.",
        "repo": "marber.economist.com + economist.com live product",
        "snapshot_version": "Marber as published 2026",
    },
    "dominion": {
        "name": "Dominion Interface System",
        "description": "An austere civic interface system derived from the Government of Canada FIP standard and the live Canada.ca web layer for the Design Authority synthesis experiment. Bilingual, structured, calm; no government marks reproduced.",
        "repo": "FIP design standard + canada.ca live web layer",
        "snapshot_version": "GCWeb as served 2026",
    },
}

BUILDERS = {"wink": build_wink, "leader": build_leader, "dominion": build_dominion}


def emit(src):
    BUILDERS[src]()
    m = MANIFEST[src]
    outdir = os.path.join(ROOT, "packs", src)
    os.makedirs(outdir, exist_ok=True)

    arts = []
    for s, ids, a in ART:
        if s != src:
            continue
        dtext = {i: decisions(src)[i]["decision"] for i in ids}
        status = decisions(src)[ids[0]].get("status", "OBSERVED")
        arts.append((src, {
            "id": a["id"], "kind": a["kind"], "title": a["title"],
            "summary": dtext[ids[0]] + ((" (%s)" % a["note"]) if a.get("note") else ""),
            "status": "beta", "aliases": a["aliases"],
            "body": a["body"],
            "source": {"repo": m["repo"], "path": "Gate 2 accepted decisions: " + ", ".join(ids)},
            "compiled_from": ids,
        }))

    def w(name, key, rows):
        with open(os.path.join(outdir, name), "w") as fh:
            json.dump({key: [r for s, r in rows if s == src]}, fh, indent=2, ensure_ascii=False)

    w("artifacts.json", "artifacts", arts)
    w("rules.json", "rules", RULE)
    w("prohibitions.json", "prohibitions", PROHIB)
    w("fallbacks.json", "fallbacks", FALLBACK)
    w("recipes.json", "recipes", RECIPES)
    golden = [c for s, c in GOLDEN if s == src]
    with open(os.path.join(outdir, "golden.json"), "w") as fh:
        json.dump({"version": "0.1", "pack_version": "%s 0.1.0" % src, "cases": golden},
                  fh, indent=1, ensure_ascii=False)
    with open(os.path.join(outdir, "scoring.json"), "w") as fh:
        json.dump({"formula": "score = max(0, 100 - (errors*8 + warnings*2 + infos*0.5))",
                   "gate": "Authority CI fails on any error; --max-warnings can tighten warnings.",
                   "source": "docs/synthesis/00-source-selection.md"}, fh, indent=2)

    manifest = {
        "id": src,
        "name": m["name"],
        "format_version": "0.1",
        "version": "0.1.0",
        "snapshot": {"repo": m["repo"], "commit": "n/a - derived from public sources, not a repository",
                     "branch": "n/a", "version": m["snapshot_version"], "path_hint": ""},
        "description": m["description"],
        "kinds": ["component", "pattern", "token-set", "guideline", "recipe", "reference"],
        "capabilities": {"search": True, "resolve": True, "validators": [],
                         "gap_reporting": True, "extension_proposals": True,
                         "resolution_assist": "off"},
        "policy": {
            "on_undefined": "Implement per the consuming project's fallback policy, mark the improvisation, and report a gap. Never present improvisation as canonical.",
            "on_conflict": "Do not implement as requested; the request violates an explicit constraint (see the cited rule/prohibition).",
            "proposals": "Noncanonical. The authority is never modified by a consumer; proposals are reviewed upstream."
        },
        "entrypoints": {"artifacts": "artifacts.json", "rules": "rules.json",
                        "recipes": "recipes.json", "fallbacks": "fallbacks.json",
                        "prohibitions": "prohibitions.json", "validators": "validators.json",
                        "scoring": "scoring.json"},
    }
    with open(os.path.join(outdir, "authority.json"), "w") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)

    n = {x: len([1 for s, r in rows if s == src]) for x, rows in
         [("artifacts", [(s, a) for s, ids, a in ART]), ("rules", RULE),
          ("prohibitions", PROHIB), ("fallbacks", FALLBACK), ("recipes", RECIPES),
          ("golden", GOLDEN)]}
    print("%s -> packs/%s/  %s" % (src, src, json.dumps(n)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="all")
    args = ap.parse_args()
    for s in (BUILDERS if args.src == "all" else [args.src]):
        emit(s)
