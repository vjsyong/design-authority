#!/usr/bin/env python3
"""Render the Triage Authority Pack into the static documentation kit that
Condition B receives — same information, passive form, parity by construction.

    python3 tools/render_kit_triage.py [--pack DIR] [--out DIR]

Every artifact, rule, recipe, fallback and prohibition in the pack must appear
in the rendered kit or the renderer fails (PARITY.md records the check).
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "kernel"))

from design_authority.pack import Pack  # noqa: E402

DEFAULT_PACK = os.path.join(ROOT, "authorities", "triage")
DEFAULT_OUT = os.path.join(ROOT, "benchmark", "materials", "kit-triage")


def title(entry):
    return entry.get("title") or entry.get("id")


def render(pack, out):
    os.makedirs(out, exist_ok=True)
    seen = set()

    def write(name, text):
        with open(os.path.join(out, name), "w") as fh:
            fh.write(text)

    def bullets(items, indent=""):
        return "\n".join("%s- %s" % (indent, i) for i in items)

    ident = pack.identity()
    comps = [a for a in pack.artifacts if a["kind"] == "component"]
    patterns = [a for a in pack.artifacts if a["kind"] == "pattern"]
    guides = [a for a in pack.artifacts if a["kind"] == "guideline"]
    tsets = [a for a in pack.artifacts if a["kind"] == "token-set"]
    examples = [a for a in pack.artifacts if a["kind"] == "example"]
    refs = [a for a in pack.artifacts if a["kind"] == "reference"]

    # ---- README -------------------------------------------------------------
    readme = """# Triage design kit

The design system this product follows: **Triage %s** (snapshot `%s`).
Everything here comes from the same authority the system is built from.

## Layout

```
design/tokens/      token source (tokens.css is what you load)
design/core/        the stylesheets + behaviour scripts
design/fonts/       Geist / Geist Mono (self-hosted)
design/icons/       icon registry + sprite
design/examples/    seven real example screens (open them in a browser)
design-docs/        this documentation
```

## Quickstart (load order)

```html
<link rel="stylesheet" href="/design/tokens/tokens.css">
<link rel="stylesheet" href="/design/core/base.css">
<link rel="stylesheet" href="/design/core/patterns.css">   <!-- page patterns -->
<script src="/design/core/components.js" defer></script>
```

Theme: `data-theme="light|dark"` on `<html>` (light default). Density:
`data-density="compact"` (comfortable default).

## How to decide (read this first)

1. **A component exists for it** → use it. See `components.md`; a component's
   class is the only canonical implementation of that idea.
2. **No dedicated component, but a sanctioned composition** → follow a recipe
   in `recipes.md` (they compose existing components and carry constraints).
3. **Nothing specific** → follow the fallback policy in `fallbacks.md`:
   plain content on system surfaces, tokens only, clearly not canonical.
4. **Never invent new canonical UI.** Improvisation is allowed when necessary,
   but it must stay marked as an improvisation, never presented as canon.
5. **Some things are prohibited outright** — see `prohibitions.md`.

Rules (`rules.md`) are the enforceable contract; `guidelines.md` covers the
normative-but-human parts (interaction, copy, accessibility); `tokens.md`
explains the value tiers; `patterns.md` the page-level compositions.
"""
    write("README.md", readme % (ident["version"], ident["commit"][:10]))

    # ---- components ----------------------------------------------------------
    lines = ["# Components (%d)" % len(comps),
             "",
             "Each entry: class, what it is, states it ships, accessibility notes,",
             "docs page. Source: `design/core/`.", ""]
    for c in comps:
        seen.add(c["id"])
        b = c.get("body", {})
        via = next((r.get("url") for r in c.get("relations", [])
                    if r.get("rel") == "documented-at"), None)
        lines.append("## %s — `.%s`" % (title(c), b.get("class", "?")))
        lines.append("")
        lines.append(c.get("summary", ""))
        lines.append("")
        if b.get("states"):
            lines.append("States: " + ", ".join(b["states"]))
        if b.get("a11y"):
            lines.append("")
            lines.append("Accessibility:")
            lines.append(bullets(b["a11y"]))
        if via:
            lines.append("")
            lines.append("Docs page (in the system site): `%s`" % via)
        lines.append("")
    write("components.md", "\n".join(lines))

    # ---- patterns -------------------------------------------------------------
    lines = ["# Patterns (%d)" % len(patterns), "",
             "Page-level compositions (CSS in `design/core/patterns.css`, real",
             "screens in `design/examples/`). Patterns are documented; unlike",
             "components they carry no states contract.", ""]
    for p in patterns:
        seen.add(p["id"])
        src = p.get("body", {}).get("sources", {})
        lines.append("## %s" % title(p))
        lines.append("")
        lines.append(p.get("summary", ""))
        if src:
            lines.append("")
            lines.append("Sources: docs page `%s`, example `%s`"
                         % (src.get("docs", "-"), src.get("example", "-")))
        lines.append("")
    write("patterns.md", "\n".join(lines))

    # ---- guidelines -------------------------------------------------------------
    lines = ["# Guidelines (%d)" % len(guides), "",
             "Normative guidance that humans apply (interaction, feedback, copy,",
             "accessibility, hierarchy). These are part of the system, not advice.", ""]
    for g in guides:
        seen.add(g["id"])
        b = g.get("body", {})
        lines.append("## %s" % title(g))
        lines.append("")
        lines.append(g.get("summary", ""))
        lines.append("")
        if b.get("do"):
            lines.append("Do:")
            lines.append(bullets(b["do"]))
        if b.get("dont"):
            lines.append("")
            lines.append("Don't:")
            lines.append(bullets(b["dont"]))
        if b.get("quote"):
            lines.append("")
            lines.append("> %s" % b["quote"])
        lines.append("")
    write("guidelines.md", "\n".join(lines))

    # ---- recipes -----------------------------------------------------------------
    lines = ["# Sanctioned compositions (recipes, %d)" % len(pack.recipes), "",
             "When there is no single component for a need, compose using these.",
             "Ingredients are components/guidelines you must use; constraints are",
             "binding.", ""]
    for r in pack.recipes:
        seen.add(r["id"])
        ings = []
        for i in r.get("ingredients", []):
            entry = pack.by_id.get(i, {})
            ings.append("`%s` (%s)" % (i, entry.get("title", "")))
        lines.append("## %s" % r["title"])
        lines.append("")
        lines.append(r.get("summary", ""))
        lines.append("")
        lines.append("Use when: " + "; ".join(r.get("needs", [])))
        lines.append("")
        lines.append("Build from: " + ", ".join(ings))
        if r.get("constraints"):
            lines.append("")
            lines.append("Constraints:")
            lines.append(bullets(r["constraints"]))
        ev = r.get("evidence") or {}
        if ev.get("quote"):
            lines.append("")
            lines.append("> %s  \n> — %s" % (ev["quote"], ev.get("source", "")))
        lines.append("")
    write("recipes.md", "\n".join(lines))

    # ---- rules --------------------------------------------------------------------
    lines = ["# Rules (%d)" % len(pack.rules), "",
             "The enforceable contract (checked by the Triage linter). Severities:",
             "error / warning / info. A rule's `fix` is the remedy.", ""]
    for r in pack.rules:
        seen.add(r["id"])
        lines.append("## %s · %s — %s" % (r["id"], r["severity"], r["name"]))
        lines.append("")
        lines.append("**What:** %s" % r["summary"])
        lines.append("")
        lines.append("**Why:** %s" % r["why"])
        lines.append("")
        lines.append("**Fix:** %s" % r["fix"])
        lines.append("")
    write("rules.md", "\n".join(lines))

    # ---- prohibitions ----------------------------------------------------------------
    lines = ["# Prohibited / conflict triggers (%d)" % len(pack.prohibitions), "",
             "Requests that contradict these must not be implemented as stated;",
             "follow the referenced rule instead.", ""]
    for p in pack.prohibitions:
        seen.add(p["id"])
        ref = (" (rule %s)" % p["rule"]) if p.get("rule") else ""
        lines.append("- **%s**%s — %s" % (title(p), ref, p["statement"]))
    lines.append("")
    write("prohibitions.md", "\n".join(lines))

    # ---- fallbacks -----------------------------------------------------------------------
    pol = pack.manifest.get("policy", {})
    lines = ["# Fallbacks — when the system has no answer", "",
             "Sanctioned generic fallbacks (not canonical components; keep them",
             "plain and token-conformant):", ""]
    for f in pack.fallbacks:
        seen.add(f["id"])
        lines.append("## %s" % title(f))
        lines.append("")
        lines.append(f.get("statement", ""))
        lines.append("")
        lines.append("Scope: " + ", ".join(f.get("scope", [])))
        if f.get("constraints"):
            lines.append("")
            lines.append("Constraints:")
            lines.append(bullets(f["constraints"]))
        lines.append("")
    lines.append("## Policy")
    lines.append("")
    lines.append(pol.get("on_undefined", ""))
    lines.append("")
    lines.append(pol.get("on_conflict", ""))
    lines.append("")
    lines.append(pol.get("proposals", ""))
    lines.append("")
    write("fallbacks.md", "\n".join(lines))

    # ---- tokens -----------------------------------------------------------------------
    lines = ["# Tokens", "",
             "All values live in `design/tokens/tokens.css` (generated from",
             "`design/tokens/tokens.json`, the source of truth). Never hardcode a",
             "colour/spacing/duration that has a token.", ""]
    for t in tsets:
        seen.add(t["id"])
        lines.append("## %s" % title(t))
        lines.append("")
        lines.append(t.get("summary", ""))
        lines.append("")
    lines.append("Theme via `data-theme` (light/dark); density via `data-density`")
    lines.append("(comfortable/compact). Fixed chrome widths live as `--layout-*`.")
    lines.append("")
    write("tokens.md", "\n".join(lines))

    # ---- examples + references ----------------------------------------------------------
    lines = ["# Example screens (%d)" % len(examples), "",
             "Real screens from the system, in `design/examples/` — open them in a",
             "browser for how the pieces actually fit together.", ""]
    for e in examples:
        seen.add(e["id"])
        lines.append("- `%s` — %s" % (e["body"].get("path", "?"), title(e)))
    lines.append("")
    write("examples.md", "\n".join(lines))

    lines = ["# Reference documents (in the system repository)", ""]
    for r in refs:
        seen.add(r["id"])
        src = r.get("source", {}).get("path", "")
        lines.append("- **%s** (`%s`) — %s" % (title(r), src, r.get("summary", "")))
    lines.append("")
    write("references.md", "\n".join(lines))

    # ---- parity check -------------------------------------------------------------------
    expected = set()
    expected.update(a["id"] for a in pack.artifacts)
    expected.update(r["id"] for r in pack.recipes)
    expected.update(f["id"] for f in pack.fallbacks)
    expected.update(p["id"] for p in pack.prohibitions)
    expected.update(r["id"] for r in pack.rules)
    missing = sorted(expected - seen)
    parity = ["# Parity check",
              "",
              "- pack entries: %d" % len(expected),
              "- rendered entries: %d" % len(seen),
              "- missing: %s" % (", ".join(missing) if missing else "none"),
              "",
              "Result: %s" % ("FAIL" if missing else "PASS"),
              ""]
    write("PARITY.md", "\n".join(parity))
    if missing:
        raise SystemExit("parity check FAILED: %s" % ", ".join(missing))
    return {"rendered": len(seen), "missing": missing}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", default=DEFAULT_PACK)
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args(argv)
    pack = Pack(args.pack)
    result = render(pack, args.out)
    print("kit rendered to %s (%d entries, parity %s)"
          % (args.out, result["rendered"], "PASS" if not result["missing"] else "FAIL"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
