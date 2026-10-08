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
      ["colour", "color", "palette", "tokens", "ink", "paper", "dark mode", "theme"],
      {"group": "Foundations",
       "tokens": COLOR_KEYS[:24],
       "extensions": ["com.triage.dark (per-token dark values)", "com.triage.compact (density values)"],
       "verify": ["tokens/tokens.css"]},
      "tokens/tokens.json (color group)", ["triage/tokens"]),

    A("token-set/typography", "token-set", "Typography — system stack, one base, a rem ladder",
      "Typography is tokenised: family tokens, a single base-size (16) that the rem ladder divides by, "
      "and an fs-* design scale. Font stacks derive from family tokens; off-system fonts are lint errors "
      "(TDS008).",
      ["typography", "type", "fonts", "font", "type scale"],
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
      ["spacing", "space", "gaps", "padding", "layout scale"],
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
      ["motion", "animation", "transition", "duration", "easing", "reduced motion"],
      {"group": "Foundations",
       "tokens": MOTION_KEYS[:12],
       "verify": ["tokens/tokens.css", "src/core/additions.css (prefers-reduced-motion)"]},
      "tokens/tokens.json (motion group)", ["triage/tokens"]),

    A("token-set/elevation", "token-set", "Elevation — reserved for floating layers",
      "Elevation is reserved for layers that float (menus, dialogs, sheets, toasts); in-flow surfaces use "
      "hairline lines and paper tints instead of shadows. Tokenised shadow values only.",
      ["elevation", "shadow", "depth", "floating"],
      {"group": "Foundations",
       "tokens": [k for k in TOK.get("shadow", {}).keys() if not k.startswith("$")],
       "verify": ["tokens/tokens.css"]},
      "tokens/tokens.json (shadow group)", ["triage/tokens"]),

    A("token-set/dataviz", "token-set", "Data visualisation — Okabe–Ito derived series",
      "A categorical series palette derived from Okabe–Ito and contrast-adjusted, with pairwise "
      "colour-vision-deficiency separation checked. Charts consume series tokens like everything else.",
      ["dataviz", "data visualisation", "charts", "series", "palette for charts"],
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
    "msg": ["flash message", "banner", "message banner", "status banner", "inline banner", "alert banner"],
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
    "tl": ["timeline", "activity timeline", "approval history", "activity log", "event trail"],
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
    artifacts.append(A(
        "component/%s" % cls, "component", name, summary, aliases,
        {"class": cls, "group": "Components",
         "source_file": c["source"], "states": c["states"],
         "verify": c.get("verify", []), "a11y": a11y, "status": c.get("status", "stable")},
        "spec/states.json (%s, %s)" % (cls, c["source"]), ["triage/states"]))

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
        {"problem": "a bulk action bar", "expect": "RESOLVED", "expect_id": "component/bulkbar"},
        {"problem": "a save bar", "expect": "RESOLVED", "expect_id": "component/savebar"},
        {"problem": "a flash message", "expect": "RESOLVED", "expect_id": "component/msg"},
        {"problem": "a banner", "expect": "RESOLVED", "expect_id": "component/msg"},
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
