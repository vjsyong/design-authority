#!/usr/bin/env python3
"""bookmarks-lint v1 — the base authority's declared validator.

Runs over a bookmarks-app workspace and emits a lint-json report (the
`lint-json` parser shape): findings[{rule,severity,file,line,message,
excerpt,fix}], counts, by_rule, score, files_scanned, version.

Checks (v1), all delta-based against the pack's frozen baseline
(`baseline.json`, generated from the sealed seed f3):

- B001 new raw colour literals outside the :root token block (styles,
  inline style attributes, targeted JS style assignments). Literals already
  present in the seed are part of the established vocabulary and allowed;
  NEW literals are errors. Normalization: lowercase, whitespace stripped,
  hex shorthand expanded (#fff == #ffffff).
- B002 QA hooks: every baseline data-testid must still be present in
  index.html or app.js. New hooks are permitted and ignored.
- B003 canonical storage: `bookmarks.v1` must appear in the JS.
- B004 reuse (warnings, delta): custom properties defined outside :root;
  new identical declaration blocks (>= 3 declarations) shared by distinct
  selectors.

Stdlib only; deterministic ordering; no network. Exit 0 when no errors,
1 when errors were found (the kernel reads the JSON regardless).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE_FILE = os.path.join(HERE, "baseline.json")
VERSION = "bookmarks-lint-1"
APP_FILES = ("index.html", "styles.css", "app.js")
ALLOW_KEYWORDS = {"transparent", "currentcolor", "inherit", "initial",
                  "unset", "revert", "none"}

LIT_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)")
STYLE_ATTR_RE = re.compile(r"""style\s*=\s*["']([^"']*)["']""")
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
JS_STYLE_RE = re.compile(
    r"""\.style\.[A-Za-z]+\s*=\s*["']([^"']*[#;][^"']*)["']|"""
    r"""setProperty\(\s*["'][^"']+["']\s*,\s*["']([^"']*)["']""")
TESTID_RE = re.compile(r"data-testid\s*[=:]\s*[\"']([^\"']+)[\"']")
CUSTOM_PROP_RE = re.compile(r"^\s*(--[A-Za-z0-9-]+)\s*:")
RULE_HEAD_RE = re.compile(r"^\s*([^{}@/][^{}]*?)\s*\{")


# ---------------------------------------------------------------- scanning
def norm_literal(s):
    s = s.strip().lower().replace(" ", "")
    m = re.fullmatch(r"#([0-9a-f]{3,8})", s)
    if m:
        h = m.group(1)
        if len(h) == 3:
            return "#" + "".join(c * 2 for c in h)
        if len(h) == 4:
            return "#" + "".join(c * 2 for c in h)
        return "#" + h
    return s


def _strip_comments_state(line, in_comment):
    """Remove CSS comment spans (stateful) so brace counting is clean."""
    out = []
    i = 0
    while i < len(line):
        if in_comment:
            j = line.find("*/", i)
            if j == -1:
                return "".join(out), True
            i = j + 2
            in_comment = False
        else:
            j = line.find("/*", i)
            if j == -1:
                out.append(line[i:])
                break
            out.append(line[i:j])
            i = j + 2
            in_comment = True
    return "".join(out), in_comment


def scan_css(text, fname, root_aware=True):
    """Return (literal_hits, custom_props, rule_blocks).

    literal_hits: [(line, literal)] outside :root (when root_aware).
    custom_props: [(line, name)] outside :root.
    rule_blocks: [(selector, decls_tuple)] for duplicate-block detection.
    """
    lits, props, blocks = [], [], []
    depth, in_root, in_comment = 0, False, False
    cur_sel, cur_decls, cur_line = None, [], 0

    def flush():
        if cur_sel is not None and len(cur_decls) >= 3:
            decls = tuple(sorted(d.strip().lower() for d in cur_decls
                                 if d.strip()))
            if decls:
                blocks.append((cur_line, cur_sel.strip(), decls))

    for i, raw in enumerate(text.split("\n"), 1):
        clean, in_comment = _strip_comments_state(raw, in_comment)
        scanning = not (root_aware and in_root)
        if scanning:
            for m in LIT_RE.finditer(clean):
                lits.append((i, m.group(0)))
        if root_aware and not in_root and re.search(r":root\s*\{", clean):
            in_root = True
        else:
            pass
        if not in_root:
            cm = CUSTOM_PROP_RE.match(clean)
            if cm:
                props.append((i, cm.group(1)))
        # collect rule blocks for duplicate detection
        mh = RULE_HEAD_RE.match(clean)
        if mh and not in_root:
            flush()
            cur_sel, cur_decls, cur_line = mh.group(1), [], i
        if cur_sel is not None and not in_root:
            body = clean
            if mh:
                body = clean[mh.end():]
            for d in body.split(";"):
                d = d.strip()
                if d and not d.startswith("}") and "{" not in d:
                    cur_decls.append(d.rstrip("}").strip())
            if "}" in clean:
                flush()
                cur_sel, cur_decls = None, []
        depth += clean.count("{") - clean.count("}")
        if in_root and depth <= 0:
            in_root = False
        if not root_aware:
            in_root = False
    flush()
    return lits, props, blocks


def scan_tree(target):
    """Scan an app workspace. Returns a dict of raw scan data."""
    files = []
    if os.path.isfile(target):
        files = [target]
        base = os.path.dirname(target)
    else:
        base = target
        for f in sorted(os.listdir(target)):
            if f.endswith((".html", ".css", ".js")) and f != "serve.py":
                files.append(os.path.join(target, f))
    out = {"files_scanned": [os.path.basename(f) for f in files],
           "literals": [], "testids": [], "custom_props": [], "blocks": [],
           "js_text": "", "all_text": {}}
    for path in files:
        name = os.path.basename(path)
        text = open(path, encoding="utf-8", errors="replace").read()
        out["all_text"][name] = text
        if name.endswith(".css"):
            l, p, b = scan_css(text, name)
            out["literals"] += [(name, i, x) for i, x in l]
            out["custom_props"] += [(name, i, x) for i, x in p]
            out["blocks"] += [(name,) + blk for blk in b]
        elif name.endswith(".html"):
            for m in STYLE_ATTR_RE.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                for lm in LIT_RE.finditer(m.group(1)):
                    out["literals"].append((name, line, lm.group(0)))
            for blk in STYLE_BLOCK_RE.findall(text):
                l, p, b = scan_css(blk, name)
                out["literals"] += [(name, 0, x) for _, x in l]
                out["custom_props"] += [(name, 0, x) for _, x in p]
                out["blocks"] += [(name,) + bb for bb in b]
        elif name.endswith(".js"):
            out["js_text"] += text
            for m in JS_STYLE_RE.finditer(text):
                lit = m.group(1) or m.group(2) or ""
                line = text.count("\n", 0, m.start()) + 1
                for lm in LIT_RE.finditer(lit):
                    out["literals"].append((name, line, lm.group(0)))
        for m in TESTID_RE.finditer(text):
            out["testids"].append(m.group(1))
    out["testids"] = sorted(set(out["testids"]))
    return out


def dup_groups(blocks):
    """Map normalized block key -> list of selectors (>= 2 selectors only)."""
    keymap = {}
    for fname, line, sel, decls in blocks:
        key = "|".join(decls)
        keymap.setdefault(key, []).append(sel)
    groups = {}
    for key, sels in keymap.items():
        if len(set(sels)) >= 2:
            groups[key] = sorted(set(sels))
    return groups


# ---------------------------------------------------------------- checks
def run_checks(scan, baseline):
    findings = []
    allowed_lits = set(baseline.get("allowed_literals", []))
    for f, line, lit in scan["literals"]:
        n = norm_literal(lit)
        if n in allowed_lits or n in ALLOW_KEYWORDS:
            continue
        findings.append({
            "rule": "B001", "severity": "error", "file": f, "line": line,
            "message": ("new raw colour literal %s outside the token "
                        "vocabulary; use a var(--color-*) token" % lit),
            "excerpt": "", "fix": ("replace with the nearest semantic token "
                                   "or file a gap if a new token is needed")})
    have = set(scan["testids"])
    for tid in baseline.get("testids", []):
        if tid not in have:
            findings.append({
                "rule": "B002", "severity": "error", "file": "index.html",
                "line": 0,
                "message": "required QA hook data-testid=%r is missing" % tid,
                "excerpt": "", "fix": "restore the hook on its element"})
    js = scan["js_text"]
    if "bookmarks.v1" not in js:
        findings.append({
            "rule": "B003", "severity": "error", "file": "app.js", "line": 0,
            "message": "canonical storage key 'bookmarks.v1' not found",
            "excerpt": "", "fix": "persist under bookmarks.v1 per QA.md"})
    allowed_props = set(baseline.get("allowed_custom_props", []))
    for f, line, name in scan["custom_props"]:
        if name not in allowed_props:
            findings.append({
                "rule": "B004", "severity": "warning", "file": f,
                "line": line,
                "message": ("custom property %s defined outside :root; "
                            "tokens belong in the token block" % name),
                "excerpt": "", "fix": "move it into :root or reuse a token"})
    allowed_dups = set(baseline.get("allowed_dup_hashes", []))
    refmap = {}
    for fname, line, sel, decls in scan["blocks"]:
        refmap.setdefault("|".join(decls), (fname, line))
    for key, sels in dup_groups(scan["blocks"]).items():
        if key in allowed_dups:
            continue
        rf, rl = refmap.get(key, ("(workspace)", 0))
        findings.append({
            "rule": "B004", "severity": "warning",
            "file": rf, "line": rl,
            "message": ("identical declaration block shared by %d selectors "
                        "(%s); consider a shared class" %
                        (len(sels), ", ".join(sorted(set(sels))[:4]))),
            "excerpt": " ; ".join(key.split("|")[:4]), "fix": "reuse before adding"})
    return findings


def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    target = args.target
    findings, scanned = [], []
    if not os.path.exists(target):
        findings = [{"rule": "lint-setup", "severity": "error",
                     "file": target, "line": 0,
                     "message": "target path does not exist", "excerpt": "",
                     "fix": "pass the workspace directory"}]
    else:
        baseline = {}
        if os.path.exists(BASELINE_FILE):
            baseline = json.load(open(BASELINE_FILE))
        else:
            findings = [{"rule": "lint-setup", "severity": "error",
                         "file": BASELINE_FILE, "line": 0,
                         "message": "baseline.json missing next to the linter",
                         "excerpt": "", "fix": "rebuild the pack"}]
        if not findings:
            scan = scan_tree(target)
            scanned = scan["files_scanned"]
            findings = run_checks(scan, baseline)
            # attach excerpts from the scanned files
            for f in findings:
                text = scan["all_text"].get(f["file"], "")
                if text and f["line"]:
                    lines = text.split("\n")
                    if 0 < f["line"] <= len(lines):
                        f["excerpt"] = lines[f["line"] - 1].strip()[:140]

    findings.sort(key=lambda f: (f["file"], f["line"] or 0, f["rule"]))
    counts = {"error": 0, "warning": 0, "info": 0}
    by_rule = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
        by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1
    score = max(0, round(100 - (counts["error"] * 8
                                + counts["warning"] * 2
                                + counts["info"] * 0.5)))
    report = {"version": VERSION, "target": os.path.abspath(target),
              "files_scanned": len(scanned), "findings": findings,
              "counts": counts, "by_rule": by_rule, "score": score}
    print(json.dumps(report, ensure_ascii=False))
    return 1 if counts["error"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
