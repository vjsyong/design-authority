#!/usr/bin/env python3
"""indaba-lint 0.1 — authority-specific validator for the Indaba pack.

Usage:  python3 indaba_lint.py <target-dir>
Scans .css / .html for compliance with the Indaba rules:
  IND-1 rounded language (no square corners)
  IND-2 palette-only colours (+ IND-3 text never pure black)
  IND-4 status word-first (pills carry text)

Emits 'lint-json': {version, findings:[{rule,severity,file,line,message,
excerpt,fix}], counts, by_rule, score, files_scanned}. Standard library only.
"""
import json
import os
import re
import sys

VERSION = "indaba-lint 0.1"
PALETTE = {
    "#ffffff", "#000000", "#333333", "#111111",
    "#77216f", "#9d5a96", "#5e2750", "#2c001e", "#40022c",
    "#e95420", "#cf4617", "#d3461a", "#fcebe3",
    "#aea79f", "#e6e2df", "#f6f4f2", "#efece9", "#eeedeb",
    "#d9d5d1", "#f5f3f1", "#8a8681", "#5d5a57",
}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".design-authority",
             ".venv", "venv", ".hermes"}

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RADIUS_RE = re.compile(r"border-radius(?:-\w+)*\s*:\s*([^;}]+)", re.I)
RULE_BLOCK_RE = re.compile(r"([^{}]+)\{([^}]*)\}", re.S)
STATUS_RE = re.compile(r"<span[^>]*class=\"[^\"]*\bstatus\b[^\"]*\"[^>]*>(.*?)</span>", re.S | re.I)
INLINE_STYLE_RE = re.compile(r"style=\"([^\"]*)\"", re.I)


def finding(rule, severity, path, line, message, excerpt="", fix=""):
    return {"rule": rule, "severity": severity, "file": path, "line": line,
            "message": message, "excerpt": excerpt.strip()[:160], "fix": fix}


def norm_hex(h):
    h = h.lower().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h[:6] if len(h) >= 6 else "#" + h


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def square_radius(val):
    """True when a border-radius value is square (all zeros)."""
    toks = [t for t in re.split(r"[\s/]+", val.strip()) if t]
    if not toks:
        return False
    return all(re.match(r"^0(\.0+)?(px|%|em|rem|pt)?$", t) for t in toks)


def scan_css(path, rel, findings, seen):
    text = open(path, errors="ignore").read()
    for m in RADIUS_RE.finditer(text):
        if square_radius(m.group(1)):
            findings.append(finding(
                "IND-1", "error", rel, line_of(text, m.start()),
                "Square corners are not part of this language — use the system radius or a pill.",
                m.group(0).strip(), "Set border-radius to 12/16px, or 999px for pills."))
    for m in HEX_RE.finditer(text):
        raw = norm_hex(m.group(0))
        if raw == "#000000":
            findings.append(finding(
                "IND-3", "warning", rel, line_of(text, m.start()),
                "Pure black — text is #111111; black is harsh with aubergine.",
                m.group(0), "Use #111111 (or the banner grey #333333 for surfaces)."))
        elif raw not in PALETTE:
            key = ("hex", raw, rel, line_of(text, m.start()))
            if key in seen:
                continue
            seen.add(key)
            findings.append(finding(
                "IND-2", "warning", rel, line_of(text, m.start()),
                "Colour outside the Ubuntu palette and its tints.",
                m.group(0), "Map to the nearest palette token."))


def scan_html(path, rel, findings, seen):
    text = open(path, errors="ignore").read()
    for sm in INLINE_STYLE_RE.finditer(text):
        rm = RADIUS_RE.search(sm.group(1))
        if rm and square_radius(rm.group(1)):
            findings.append(finding(
                "IND-1", "error", rel, line_of(text, sm.start()),
                "Inline square corners (border-radius: 0).", rm.group(0),
                "Use the system radius or a pill."))
    for m in STATUS_RE.finditer(text):
        inner = re.sub(r"<[^>]+>", "", m.group(1))
        if not re.search(r"[A-Za-z]", inner):
            findings.append(finding(
                "IND-4", "error", rel, line_of(text, m.start()),
                "Status pill without its word — status reads as a word first.",
                m.group(0)[:120], "Put the status word inside the pill."))
    for m in HEX_RE.finditer(text):
        raw = norm_hex(m.group(0))
        if raw == "#000000":
            findings.append(finding(
                "IND-3", "warning", rel, line_of(text, m.start()),
                "Pure black in markup — use #111111.", m.group(0),
                "Use #111111."))
        elif raw not in PALETTE:
            key = ("hex", raw, rel, line_of(text, m.start()))
            if key in seen:
                continue
            seen.add(key)
            findings.append(finding(
                "IND-2", "warning", rel, line_of(text, m.start()),
                "Colour outside the Ubuntu palette and its tints.", m.group(0),
                "Map to the nearest palette token."))


def artifact_usage(project_text, findings):
    for cls in ("action", "masthead", "ledger", "status", "surface"):
        token = re.compile(r"(class=\"[^\"]*\b%s\b|\\.%s\b)" % (cls, cls))
        if not token.search(project_text):
            findings.append(finding(
                "IND-USE", "info", "(project)", 0,
                "No use of authority artifact '.%s' found." % cls, "",
                "Confirm the build uses the authority's own artifacts."))


def main():
    if len(sys.argv) != 2:
        print("usage: indaba_lint.py <target-dir>", file=sys.stderr)
        return 2
    target = os.path.abspath(sys.argv[1])
    findings, seen = [], set()
    files_scanned = 0
    project_text = []
    for root, dirs, names in os.walk(target):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in names:
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, target)
            if fn.endswith(".css"):
                files_scanned += 1
                scan_css(path, rel, findings, seen)
                project_text.append(open(path, errors="ignore").read())
            elif fn.endswith((".html", ".htm", ".jinja", ".j2")):
                files_scanned += 1
                scan_html(path, rel, findings, seen)
                project_text.append(open(path, errors="ignore").read())
    artifact_usage("\n".join(project_text), findings)
    counts = {"error": 0, "warning": 0, "info": 0}
    by_rule = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
        by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1
    score = max(0, round(100 - (counts["error"] * 8 + counts["warning"] * 2
                                + counts["info"] * 0.5)))
    print(json.dumps({"version": VERSION, "findings": findings, "counts": counts,
                      "by_rule": by_rule, "score": score,
                      "files_scanned": files_scanned}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
