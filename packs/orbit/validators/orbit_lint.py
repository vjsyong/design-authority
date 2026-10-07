#!/usr/bin/env python3
"""orbit-lint 0.1 — authority-specific validator for the Orbit pack.

Usage:  python3 orbit_lint.py <target-dir>
Scans .css / .html / .jinja / .j2 files for compliance with the Orbit rules
(ORB-1 square form, ORB-2 accent discipline, ORB-3 no elevation, ORB-4
status needs text) plus palette discipline.

Emits 'lint-json' report shape:
  {version, findings:[{rule,severity,file,line,message,excerpt,fix}],
   counts:{error,warning,info}, by_rule:{...}, score, files_scanned}

Standard library only — runs from the pack directory via the Design
Authority kernel ({pack} substitution); this authority has no snapshot repo.
"""
import json
import os
import re
import sys

VERSION = "orbit-lint 0.1"
PALETTE = {"#ffffff", "#101010", "#6f6f6f", "#e03c31"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".design-authority",
             ".venv", "venv", ".hermes"}

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RADIUS_RE = re.compile(r"border-radius(?:-\w+)*\s*:\s*([^;}]+)", re.I)
SHADOW_RE = re.compile(r"box-shadow\s*:\s*([^;}]+)", re.I)
BG_RE = re.compile(r"background(?:-color)?\s*:\s*([^;}]+)", re.I)
RULE_BLOCK_RE = re.compile(r"([^{}]+)\{([^}]*)\}", re.S)
INDICATOR_RE = re.compile(
    r"<span[^>]*class=\"[^\"]*indicator[^\"]*\"[^>]*>(.*?)</span>", re.S | re.I)
INLINE_STYLE_RE = re.compile(r"style=\"([^\"]*)\"", re.I)
READING_SEL_RE = re.compile(
    r"(^|[,\s>+~.])(p|span|li|td|th|main|body|article|section|h[1-6])([,\s{:.]|$)",
    re.I)


def finding(rule, severity, path, line, message, excerpt="", fix=""):
    return {"rule": rule, "severity": severity, "file": path, "line": line,
            "message": message, "excerpt": excerpt.strip()[:160], "fix": fix}


def norm_hex(h):
    h = h.lower().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h[:6] if len(h) >= 6 else "#" + h


def hex_pastel(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return False
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    sat = 0 if mx == 0 else (mx - mn) / mx
    light = (mx + mn) / 2
    # Pastels: a little hue, very light. (Pure white/gray neutrals are not
    # "pastels" in the source rule's sense — and palette neutrals are exempt.)
    return 0.08 < sat < 0.45 and light > 0.82


def nonzero_radius(val):
    """True when a border-radius value is not all zeros."""
    for tok in re.split(r"[\s/]+", val.strip()):
        if not tok:
            continue
        if not re.match(r"^0(\.0+)?(px|%|em|rem|pt)?$", tok):
            return True
    return False


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def scan_css(path, rel, findings, seen_hex):
    text = open(path, errors="ignore").read()

    for m in RADIUS_RE.finditer(text):
        val = m.group(1)
        if nonzero_radius(val):
            findings.append(finding(
                "ORB-1", "error", rel, line_of(text, m.start()),
                "border-radius must always be 0 (square form is a system rule).",
                m.group(0).strip(), "Remove border-radius or set it to 0."))

    for m in SHADOW_RE.finditer(text):
        val = m.group(1).strip().lower()
        if val not in ("none", "initial", "unset", "0"):
            findings.append(finding(
                "ORB-3", "warning", rel, line_of(text, m.start()),
                "No drop shadows or elevation; hierarchy uses rules, bands, inversion.",
                m.group(0).strip(), "Replace box-shadow with a 1px border or rule."))

    for m in RULE_BLOCK_RE.finditer(text):
        selector, body = m.group(1).strip(), m.group(2)
        bm = BG_RE.search(body)
        if not bm:
            continue
        bg = bm.group(1).lower()
        if ("#e03c31" in bg or "var(--accent" in bg.replace(" ", "")) \
                and READING_SEL_RE.search(selector):
            findings.append(finding(
                "ORB-2", "error", rel, line_of(text, m.start(0)),
                "Accent used as a reading surface (red never sits behind reading text).",
                (selector + " { " + bm.group(0).strip() + " }")[:160],
                "Move content off the accent surface; ink on paper."))

    for m in HEX_RE.finditer(text):
        raw = norm_hex(m.group(0))
        if raw not in PALETTE:
            key = ("hex", raw, rel, line_of(text, m.start()))
            if key in seen_hex:
                continue
            seen_hex.add(key)
            findings.append(finding(
                "ORB-2", "warning", rel, line_of(text, m.start()),
                "Raw color outside the Orbit palette; use palette tokens "
                "(--paper/--ink/--gray-mid/--accent).",
                m.group(0), "Map to the nearest palette token."))
            if hex_pastel(raw):
                key = ("pastel", raw, rel, line_of(text, m.start()))
                if key in seen_hex:
                    continue
                seen_hex.add(key)
                findings.append(finding(
                    "ORB-2", "warning", rel, line_of(text, m.start()),
                    "Pale/pastel color discouraged system-wide (source-derived rule).",
                    m.group(0), "Use palette tones."))


def scan_html(path, rel, findings, seen_hex):
    text = open(path, errors="ignore").read()

    for sm in INLINE_STYLE_RE.finditer(text):
        style = sm.group(1)
        rm = RADIUS_RE.search(style)
        if rm and nonzero_radius(rm.group(1)):
            findings.append(finding(
                "ORB-1", "error", rel, line_of(text, sm.start()),
                "Inline border-radius must be 0.", rm.group(0),
                "Remove inline radius; keep square form."))
        shm = SHADOW_RE.search(style)
        if shm and shm.group(1).strip().lower() not in ("none", "0"):
            findings.append(finding(
                "ORB-3", "warning", rel, line_of(text, sm.start()),
                "Inline box-shadow not allowed (no elevation).", shm.group(0),
                "Use a border or rule."))

    for m in INDICATOR_RE.finditer(text):
        inner = re.sub(r"<[^>]+>", "", m.group(1))
        if not re.search(r"[A-Za-z0-9]", inner):
            findings.append(finding(
                "ORB-4", "warning", rel, line_of(text, m.start()),
                "Status marker without a text label (text must carry the status).",
                m.group(0)[:120], "Add the status word next to the marker."))

    for m in HEX_RE.finditer(text):
        raw = norm_hex(m.group(0))
        if raw in PALETTE:
            continue


def artifact_usage(project_text, findings):
    """Info-level nudges: confirm the build actually uses authority artifacts."""
    for cls in ("command", "band", "register", "notice", "indicator"):
        token = re.compile(r"(class=\"[^\"]*\b%s\b|\\.%s\b)" % (cls, cls))
        if not token.search(project_text):
            findings.append(finding(
                "ORB-USE", "info", "(project)",
                0, "No use of authority artifact '.%s' found." % cls,
                "", "Confirm the build uses the authority's own artifacts."))


def main():
    if len(sys.argv) != 2:
        print("usage: orbit_lint.py <target-dir>", file=sys.stderr)
        return 2
    target = os.path.abspath(sys.argv[1])
    findings, seen_hex = [], set()
    files_scanned = 0
    project_text = []

    for root, dirs, names in os.walk(target):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in names:
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, target)
            if fn.endswith(".css"):
                files_scanned += 1
                scan_css(path, rel, findings, seen_hex)
                project_text.append(open(path, errors="ignore").read())
            elif fn.endswith((".html", ".htm", ".jinja", ".j2")):
                files_scanned += 1
                scan_html(path, rel, findings, seen_hex)
                project_text.append(open(path, errors="ignore").read())

    artifact_usage("\n".join(project_text), findings)

    counts = {"error": 0, "warning": 0, "info": 0}
    by_rule = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
        by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1
    score = max(0, round(100 - (counts["error"] * 8 + counts["warning"] * 2
                                + counts["info"] * 0.5)))
    report = {"version": VERSION, "findings": findings, "counts": counts,
              "by_rule": by_rule, "score": score, "files_scanned": files_scanned}
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
