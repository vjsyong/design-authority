#!/usr/bin/env python3
"""p4c_build.py — build the counter-default apparatus (docs/experiments/13).

    python3 docs/experiments/tools/p4c_build.py

Outputs (idempotent — rebuilds from the frozen sources each run):
  ~/p4c/seed                        the P4 bookmarks seed restyled onto the
                                    counter-default language (ink/paper/
                                    squared/Geist; Triage token values)
  ~/p4c/materials/packs/p4c-cd-0    the counter-default pack: lint v2
                                    (B001-B004 + B006 default-vocabulary ban,
                                    B007 squared corners, B008 type contract)
                                    with the baseline regenerated from the
                                    restyled seed.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
VENV_PY = os.path.join(REPO, ".venv", "bin", "python3")
P4C = os.path.expanduser("~/p4c")
SRC_SEED = os.path.expanduser("~/p4-maint/seed")
SRC_PACK = os.path.expanduser("~/p4-maint/materials/packs/p4-da-0")
DA_TOOLS = os.path.expanduser("~/p4-maint/materials/da/tools/da.py")
TRIAGE = os.path.expanduser("~/triage-design-system")
PACK = os.path.join(P4C, "materials", "packs", "p4c-cd-0")

ROOT_BLOCK = """\
:root {
  --color-bg: #fafafa;
  --color-surface: #ffffff;
  --color-border: #e5e5e5;
  --color-text: #000000;
  --color-muted: #666666;
  --color-accent: #0057d9;
  --color-accent-hover: #004ab9;
  --color-accent-soft: #dbeafe;
  --color-danger: #c81e2c;
  --radius: 0px;
  --shadow: 0 1px 2px rgba(0, 0, 0, 0.06), 0 1px 3px rgba(0, 0, 0, 0.04);
  --font-sans: Geist, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --font-mono: "Geist Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}\
"""

FONT_FACE = """\
/*! Counter-default type: Geist / Geist Mono (vendored; no external resources). */
@font-face { font-family: "Geist"; src: url("fonts/geist.woff2") format("woff2"); font-weight: 100 900; font-style: normal; font-display: swap; }
@font-face { font-family: "Geist Mono"; src: url("fonts/geist-mono.woff2") format("woff2"); font-weight: 100 900; font-style: normal; font-display: swap; }

"""

LINT_PATCHES = [
    ('VERSION = "bookmarks-lint-1"', 'VERSION = "bookmarks-lint-2-cd"'),
    (
        "ALLOW_KEYWORDS = {\"transparent\", \"currentcolor\", \"inherit\", \"initial\",\n                  \"unset\", \"revert\", \"none\"}",
        "ALLOW_KEYWORDS = {\"transparent\", \"currentcolor\", \"inherit\", \"initial\",\n"
        "                  \"unset\", \"revert\", \"none\"}\n"
        "# counter-default (docs/experiments/13): model-default values are banned\n"
        "# outright, inherited or new; corners are square; type is the contract stack.\n"
        "BANNED_PREFIXES = (\"#2563eb\", \"#1d4ed8\", \"#6b7280\", \"#b91c1c\",\n"
        "                   \"#f4f5f7\", \"#e2e5ea\", \"#1c2024\", \"#eff4ff\",\n"
        "                   \"#991b1b\", \"#fef2f2\", \"#f0f1f4\",\n"
        "                   \"rgba(37,99,235\", \"rgba(20,24,33\")\n"
        "RADIUS_RE = re.compile(r\"border-radius\\s*:\\s*([^;}]+)\")\n"
        "FONT_RE = re.compile(r\"font-family\\s*:\\s*([^;}]+)\")\n"
        "RADIUS_OK = (\"0\", \"0px\", \"0%\", \"var(--radius)\", \"inherit\",\n"
        "             \"initial\", \"unset\")",
    ),
    (
        "    allowed_props = set(baseline.get(\"allowed_custom_props\", []))",
        """    # B006: model-default vocabulary anywhere (inherited or new)
    for fname, text in sorted(scan["all_text"].items()):
        for m in LIT_RE.finditer(text):
            n = norm_literal(m.group(0))
            if n.startswith(BANNED_PREFIXES):
                findings.append({
                    "rule": "B006", "severity": "error", "file": fname,
                    "line": text.count("\\n", 0, m.start()) + 1,
                    "message": ("model-default value %s outside the counter-default "
                                "vocabulary; use the contract tokens" % m.group(0)),
                    "excerpt": "", "fix": "replace with a counter-default token"})
    # B007: squared corners
    for fname, text in sorted(scan["all_text"].items()):
        for m in RADIUS_RE.finditer(text):
            v = m.group(1).strip().lower().replace(" ", "")
            v = v.replace("!important", "").strip()
            if v in RADIUS_OK:
                continue
            findings.append({
                "rule": "B007", "severity": "error", "file": fname,
                "line": text.count("\\n", 0, m.start()) + 1,
                "message": ("rounded corner (border-radius: %s) outside the "
                            "counter-default contract (square by design)" % m.group(1).strip()),
                "excerpt": "", "fix": "remove the radius or use var(--radius)"})
    # B008: type contract
    for fname, text in sorted(scan["all_text"].items()):
        for m in FONT_RE.finditer(text):
            v = m.group(1).strip().lower()
            if "geist" in v or "var(--font" in v or v in ("inherit", "initial", "unset"):
                continue
            findings.append({
                "rule": "B008", "severity": "warning", "file": fname,
                "line": text.count("\\n", 0, m.start()) + 1,
                "message": ("font stack outside the contract type (%s)" % m.group(1).strip()),
                "excerpt": "", "fix": "use var(--font-sans) / var(--font-mono)"})
    allowed_props = set(baseline.get("allowed_custom_props", []))""",
    ),
]

REPLACEMENTS = [
    (r"rgba\(\s*20\s*,\s*24\s*,\s*33", "rgba(0, 0, 0"),
    (r"#f0f1f4", "#f5f5f5"),
    (r"#991b1b", "#aa1925"),
    (r"#fef2f2", "#fee2e2"),
    (r'font-family: system-ui, -apple-system, "Segoe UI", sans-serif;',
     "font-family: var(--font-sans);"),
    (r"font-family: ui-monospace, SFMono-Regular, Menlo, monospace;",
     "font-family: var(--font-mono);"),
]


def log(m):
    print("[p4c] " + m, flush=True)


def restyle_seed():
    dst = os.path.join(P4C, "seed")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(SRC_SEED, dst, symlinks=True, ignore=shutil.ignore_patterns(".git"))
    css = os.path.join(dst, "styles.css")
    text = open(css, encoding="utf-8").read()
    text = re.sub(r":root\s*\{.*?\}", ROOT_BLOCK, text, count=1, flags=re.S)
    text = FONT_FACE + text
    for pat, rep in REPLACEMENTS:
        text = re.sub(pat, rep, text)
    text = re.sub(r"^[ \t]*border-radius:[ \t]*\d+(?:\.\d+)?(?:px|rem|em|%)[ \t]*;[ \t]*\n?",
                  "", text, flags=re.M)
    open(css, "w", encoding="utf-8").write(text)
    fdir = os.path.join(dst, "fonts")
    os.makedirs(fdir, exist_ok=True)
    for f in ("geist.woff2", "geist-mono.woff2"):
        shutil.copy2(os.path.join(TRIAGE, "fonts", f), os.path.join(fdir, f))
    log("seed restyled -> ~/p4c/seed")


def load_lint_module(path):
    spec = importlib.util.spec_from_file_location("cd_lint", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_pack():
    if os.path.exists(PACK):
        shutil.rmtree(PACK)
    shutil.copytree(SRC_PACK, PACK)
    lint = os.path.join(PACK, "lint", "bookmarks_lint.py")
    text = open(lint, encoding="utf-8").read()
    for old, new in LINT_PATCHES:
        if old not in text:
            raise SystemExit("lint patch anchor missing: %r" % old[:60])
        text = text.replace(old, new, 1)
    open(lint, "w", encoding="utf-8").write(text)
    # baseline regenerated from the restyled seed
    mod = load_lint_module(lint)
    scan = mod.scan_tree(os.path.join(P4C, "seed"))
    allowed_lits = sorted({mod.norm_literal(x) for _, _, x in scan["literals"]}
                          | {"#ffffff"})
    baseline = {
        "allowed_literals": allowed_lits,
        "testids": scan["testids"],
        "allowed_custom_props": sorted({p for _, _, p in scan["custom_props"]}),
        "allowed_dup_hashes": sorted(mod.dup_groups(scan["blocks"]).keys()),
        "generated_from": "p4c-cd-0 seed (counter-default restyle)",
        "generator": "bookmarks-lint-2-cd baseline builder",
    }
    with open(os.path.join(PACK, "lint", "baseline.json"), "w") as fh:
        json.dump(baseline, fh, indent=1)
    # token record + authority metadata
    ap = os.path.join(PACK, "artifacts.json")
    d = json.load(open(ap))
    for a in d["artifacts"]:
        if a["id"] == "token/surfaces":
            body = a.setdefault("body", {})
            body["values"] = [
                "surface-page #fafafa", "surface-card #ffffff", "border #e5e5e5",
                "text #000000", "muted #666666", "accent #0057d9",
                "accent-hover #004ab9", "accent-soft #dbeafe", "danger #c81e2c",
                "radius 0px (squared by contract)", "type Geist / Geist Mono",
                "shadows rgba(0,0,0,.04-.06)",
            ]
            body["statement"] = ("Counter-default vocabulary (Triage language): "
                                 "ink text, paper surfaces, squared corners, "
                                 "Geist type. Model-default values are banned "
                                 "(lint B006); rounded corners are violations "
                                 "(B007); foreign type stacks warn (B008).")
            break
    json.dump(d, open(ap, "w"), indent=1, ensure_ascii=False)
    au = os.path.join(PACK, "authority.json")
    j = json.load(open(au))
    j["version"] = "0.2.0-counterdefault"
    j["name"] = "Counter-default (Triage language)"
    j["description"] = ("The bookmarks conventions moved onto the estate's "
                        "Triage language: ink/paper surfaces, squared corners, "
                        "Geist type, counter-default colour tokens. Lint v2 "
                        "bans model-default values outright.")
    json.dump(j, open(au, "w"), indent=1, ensure_ascii=False)
    bp = os.path.join(PACK, "BUILD.json")
    b = json.load(open(bp))
    b.setdefault("notes", []).append(
        "p4c: counter-default restyle + lint v2 (B006/B007/B008); baseline "
        "regenerated from the restyled seed (docs/experiments/13)")
    json.dump(b, open(bp, "w"), indent=1, ensure_ascii=False)
    log("pack built -> %s (lint v2, baseline from restyled seed)" % PACK)
    log("baseline literals: %s" % ", ".join(allowed_lits))


def validate():
    r = subprocess.run([VENV_PY, DA_TOOLS, "--pack", PACK, "validate",
                        os.path.join(P4C, "seed")],
                       capture_output=True, text=True)
    print(r.stdout)
    if r.stderr:
        print(r.stderr[-500:])
    return r.returncode


def main():
    os.makedirs(os.path.join(P4C, "materials"), exist_ok=True)
    restyle_seed()
    build_pack()
    rc = validate()
    log("validate rc=%s %s" % (rc, "(clean)" if rc == 0 else "(SEE FINDINGS)"))


if __name__ == "__main__":
    main()
