#!/usr/bin/env python3
"""apply_hardening — adversarial-round-1 contract & verifier deltas.

Applies the adjudicated hardening for the evasion classes found by the
adversarial round (docs/verification/09). Generic mechanisms only; no
authority-specific verifier branching. Re-run the full regression after this.
"""
import json
import os

REPO = "/home/xrim/design-authority"
PACKS = os.path.join(REPO, "packs")

INSTRUMENT = "marks-on|mark-lbl|mark-toggle|\\[data-mark\\]|prov-"


def load(p):
    return json.load(open(os.path.join(PACKS, p, "verification.json")))


def save(p, d):
    with open(os.path.join(PACKS, p, "verification.json"), "w") as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False)
    print(f"saved packs/{p}/verification.json ({len(d['checks'])} checks)")


def by_id(d):
    return {c["id"]: c for c in d["checks"]}


# ---------------------------------------------------------------- wink -----
d = load("wink")
c = by_id(d)
c["wink/no-pure-black-static"]["assertions"][0]["pattern"] = (
    "#000000?(?![0-9a-fA-F])|rgba?\\(\\s*0\\s*,\\s*0\\s*,\\s*0(?:\\s*,\\s*(?:1|1\\.0*))?\\s*\\)")
c["wink/no-pure-black-static"]["note"] = "hex form + opaque rgb()/rgba() forms; transparent rgba(0,0,0,0) stays allowed"
c["wink/dialog-scrim"]["assertions"][0]["pattern"] = (
    "::backdrop[^}]*rgba\\(35,\\s*30,\\s*21,\\s*(?:\\.35|0\\.35)\\)")
c["wink/dialog-scrim"]["note"] = "accepts .35 and 0.35 alpha spellings (same colour — formatting is not the claim)"
c["wink/focus-visible"]["scenario"] = "tab-walk"
c["wink/focus-visible"]["params"] = {"stops": 26}
c["wink/focus-visible"]["assertions"] = [
    {"evidence": "tab_bad", "relation": "count_eq", "value": 0},
    {"evidence": "tab_samples", "relation": "min", "value": 6}]
c["wink/focus-visible"]["note"] = "walks up to 26 tab stops; every distinct focused control needs a visible ring"
c["wink/destructive-not-focused"]["assertions"] = [
    {"evidence": "dialog_open", "relation": "equals", "value": True},
    {"evidence": "destructive_found", "relation": "equals", "value": True},
    {"evidence": "focus_destructive_like", "relation": "equals", "value": False}]
c["wink/destructive-not-focused"]["note"] = "fails if the destructive target vanishes; judges focus by what it IS (a damage-verb button), not only by a pinned id"
c["wink/no-floating-surfaces"]["params"] = {
    "allow_regex": "mark-toggle|provPanel|bottomnav",
    "pre_steps": [["click", ".log-tick"], ["wait", 500]],
    "steps_required": True}
for a in c["wink/no-imagery"]["assertions"]:
    if a.get("relation") == "no_css_url_images":
        a["allow_regex"] = "fonts/"
d["checks"].append({
    "id": "wink/svg-census", "item": "precedent/declined-photographic-imagery",
    "title": "SVG census matches the sanctioned set (no added graphics)",
    "classification": "MECHANICALLY_VERIFIABLE", "severity": "warning",
    "mode": "INTERACTION", "scenario": "svg-census", "params": {"max_count": 4},
    "assertions": [{"evidence": "svg_excess", "relation": "count_eq", "value": 0}],
    "note": "census bound = the clean build's 4; added svg (however classed) trips the census — renaming is not enough"})
d["checks"].append({
    "id": "wink/background-scan", "item": "precedent/declined-photographic-imagery",
    "title": "No url() backgrounds on rendered elements",
    "classification": "MECHANICALLY_VERIFIABLE", "severity": "warning",
    "mode": "INTERACTION", "scenario": "background-scan", "params": {},
    "assertions": [{"evidence": "bg_url_unexpected", "relation": "count_eq", "value": 0}]})
d["checks"].append({
    "id": "wink/animation-census", "item": "guideline/shape-language",
    "title": "No element runs a CSS animation (invented motion)",
    "classification": "MECHANICALLY_VERIFIABLE", "severity": "warning",
    "mode": "INTERACTION", "scenario": "animation-census", "params": {},
    "assertions": [{"evidence": "animations_found", "relation": "count_eq", "value": 0}]})
save("wink", d)

# -------------------------------------------------------------- leader -----
d = load("leader")
c = by_id(d)
c["leader/no-square-interactive"]["assertions"][0]["pattern"] = "border-radius:\\s*0(?:\\.0+)?(?:px)?\\s*[;}]"
c["leader/no-square-interactive"]["assertions"][0]["except_line_regex"] = INSTRUMENT
c["leader/no-glow"]["files"] = ["app.css", "index.html"]
c["leader/no-glow"]["assertions"][0]["except_line_regex"] = INSTRUMENT
c["leader/no-keyframes"]["files"] = ["app.css", "index.html"]
c["leader/palette-literals"]["assertions"][0]["exclude_line_regex"] = INSTRUMENT
c["leader/error-line"]["missing"] = "fail"
c["leader/error-line"]["note"] = "selector must resolve; a renamed/removed error line is a finding, not silence"
c["leader/focus-visible"]["scenario"] = "tab-walk"
c["leader/focus-visible"]["params"] = {"stops": 22}
c["leader/focus-visible"]["assertions"] = [
    {"evidence": "tab_bad", "relation": "count_eq", "value": 0},
    {"evidence": "tab_samples", "relation": "min", "value": 6}]
c["leader/no-floating-surfaces"]["params"] = {
    "allow_regex": "marks-toggle|mark-toggle|bottomnav",
    "pre_steps": [["click", "[data-log]"], ["wait", 300], ["click", "#log-save"], ["wait", 1200]],
    "steps_required": True}
c["leader/red-not-surface"]["note"] = "gradient-painted red counts as a red surface (background-image is parsed)"
d["checks"].append({
    "id": "leader/svg-census", "item": "precedent/declined-imagery-and-icons",
    "title": "SVG census matches the sanctioned set (leader ships none)",
    "classification": "MECHANICALLY_VERIFIABLE", "severity": "error",
    "mode": "INTERACTION", "scenario": "svg-census", "params": {"max_count": 0},
    "assertions": [{"evidence": "svg_excess", "relation": "count_eq", "value": 0}]})
d["checks"].append({
    "id": "leader/shadow-census", "item": "prohibition/ambient-glow",
    "title": "No computed shadows anywhere (static + inline + runtime)",
    "classification": "MECHANICALLY_VERIFIABLE", "severity": "error",
    "mode": "INTERACTION", "scenario": "shadow-census", "params": {"allow_regex": "$^"},
    "assertions": [{"evidence": "shadow_unexpected", "relation": "count_eq", "value": 0}]})
d["checks"].append({
    "id": "leader/animation-census", "item": "guideline/motion",
    "title": "No element runs a CSS animation (invented motion)",
    "classification": "MECHANICALLY_VERIFIABLE", "severity": "error",
    "mode": "INTERACTION", "scenario": "animation-census", "params": {},
    "assertions": [{"evidence": "animations_found", "relation": "count_eq", "value": 0}]})
save("leader", d)

# ------------------------------------------------------------ dominion -----
d = load("dominion")
c = by_id(d)
c["dominion/slate-primary"]["assertions"].append(
    {"property": "background-image", "relation": "equals", "value": "none"})
c["dominion/radius-discipline"]["assertions"][0]["except_line_regex"] = INSTRUMENT
c["dominion/palette-literals"]["assertions"][0]["exclude_line_regex"] = INSTRUMENT
c["dominion/no-imagery"]["assertions"] = [
    {"relation": "absent", "selector": "img"},
    {"relation": "absent", "selector": "svg:not(.spark)"},
    {"relation": "no_css_url_images", "files": ["app.css"], "allow_regex": "fonts/"}]
c["dominion/no-imagery"]["note"] = ("sanctioned chart svg (.spark) excepted; css url() restricted to fonts; "
                                    "svg census bounds the class-smuggling route")
c["dominion/no-red-status"]["params"] = {
    "pre_steps": [["click", ".r-details"], ["wait", 350]], "steps_required": True}
c["dominion/focus-glow"]["params"] = {"selectors": [".field input", "#ledger-search"]}
c["dominion/focus-glow"]["assertions"] = [
    {"evidence": "focus_signals", "relation": "all_contains", "value": "102, 175, 233"}]
c["dominion/focus-glow"]["note"] = "every sampled field must show the sanctioned glow — not just the first"
c["dominion/no-floating-surfaces"]["params"] = {
    "allow_regex": "marks-toggle|dialog-scrim|scrim",
    "pre_steps": [["click", "#export-csv"], ["wait", 500]],
    "steps_required": True}
c["dominion/no-keyframes"]["files"] = ["app.css", "index.html"]
d["checks"].append({
    "id": "dominion/svg-census", "item": "prohibition/imagery-pictograms",
    "title": "SVG census matches the sanctioned set (the one chart spark)",
    "classification": "MECHANICALLY_VERIFIABLE", "severity": "error",
    "mode": "INTERACTION", "scenario": "svg-census", "params": {"max_count": 1},
    "assertions": [{"evidence": "svg_excess", "relation": "count_eq", "value": 0}]})
d["checks"].append({
    "id": "dominion/shadow-census", "item": "prohibition/elevation-shadows",
    "title": "No computed shadows beyond the focus glow",
    "classification": "MECHANICALLY_VERIFIABLE", "severity": "error",
    "mode": "INTERACTION", "scenario": "shadow-census", "params": {"allow_regex": "102, 175, 233"},
    "assertions": [{"evidence": "shadow_unexpected", "relation": "count_eq", "value": 0}]})
d["checks"].append({
    "id": "dominion/animation-census", "item": "prohibition/red-status",
    "title": "No element runs a CSS animation (invented motion)",
    "classification": "MECHANICALLY_VERIFIABLE", "severity": "warning",
    "mode": "INTERACTION", "scenario": "animation-census", "params": {},
    "assertions": [{"evidence": "animations_found", "relation": "count_eq", "value": 0}]})
d["checks"].append({
    "id": "dominion/meter-after-save", "item": "component/meter",
    "title": "Meter fills stay black/slate through the save flow",
    "classification": "MECHANICALLY_VERIFIABLE", "severity": "warning",
    "mode": "INTERACTION", "scenario": "computed-list",
    "params": {"selector": ".meter i", "property": "background-color",
               "pre_steps": [["click", ".r-log"], ["wait", 300], ["click", "#log-save"], ["wait", 1300]],
               "steps_required": True},
    "assertions": [
        {"evidence": "values", "relation": "all_color_in", "value": ["#000000", "#26374A"]},
        {"evidence": "values_count", "relation": "min", "value": 1}]})
save("dominion", d)

print("hardening deltas applied: wink 29->32 · leader 23->26 · dominion 22->26 checks")
