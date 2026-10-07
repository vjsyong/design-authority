#!/usr/bin/env python3
"""Static scans for a benchmark run workspace.

Dimensions:
  D1  triage-lint over the authored surface (templates/ + static/, minus the
      vendored design assets) -> findings by rule/severity + spec score.
  D2  drift scan: raw colours, off-scale spacing, radii, fonts, surprises.
  D3  scope discipline: git diff vs the starter commit (UI vs backend vs other).

    python3 scan.py --ws DIR --out DIR/scan.json [--snapshot DIR]
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "kernel"))

from design_authority.pack import Pack  # noqa: E402
from design_authority.validate import validate  # noqa: E402

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
FUNC_RE = re.compile(r"\b(?:rgba?|hsla?|oklch|lab|lch|color-mix)\([^)]*\)")
PX_RE = re.compile(r"(-?\d+(?:\.\d+)?)px")
RADIUS_RE = re.compile(r"border(?:-[a-z]+)?-radius\s*:\s*([^;\"'}]+)", re.I)
FONT_RE = re.compile(r"font-family\s*:\s*([^;\"'}]+)", re.I)
SPACE_PROP_RE = re.compile(r"(margin|padding|gap|row-gap|column-gap)(?:-[a-z]+)?\s*:\s*([^;\"'}]+)", re.I)
DUR_RE = re.compile(r"(\d+(?:\.\d+)?)(ms|s)\b")
IMPORTANT_RE = re.compile(r"!important")
INLINE_STYLE_RE = re.compile(r'style\s*=\s*"([^"]*)"|style\s*=\s*\'([^\']*)\'')
CLASS_RE = re.compile(r'class\s*=\s*"([^"]*)"|class\s*=\s*\'([^\']*)\'')
TEXT_EXTS = {".html", ".css", ".js", ".py", ".jinja", ".jinja2", ".svg", ".json", ".md"}


def walk_text(root, subdirs):
    files = []
    for sub in subdirs:
        base = os.path.join(root, sub)
        for dirpath, dirnames, names in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", "node_modules", "design")]
            for n in names:
                if os.path.splitext(n)[1].lower() in TEXT_EXTS:
                    files.append(os.path.join(dirpath, n))
    return files


def drift_scan(root):
    colors, funcs, radii, fonts, spacings, durations, important = {}, {}, {}, {}, {}, {}, 0
    inline_styles, classes, files = 0, {}, []
    for path in walk_text(root, ["templates", "static"]):
        rel = os.path.relpath(path, root)
        if rel.startswith("static/design/"):
            continue
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        files.append(rel)
        for m in HEX_RE.findall(text):
            colors[m.lower()] = colors.get(m.lower(), 0) + 1
        for m in FUNC_RE.findall(text):
            key = re.sub(r"\s+", "", m.lower())[:60]
            funcs[key] = funcs.get(key, 0) + 1
        for m in RADIUS_RE.findall(text):
            radii[m.strip()] = radii.get(m.strip(), 0) + 1
        for m in FONT_RE.findall(text):
            fonts[m.strip()[:80]] = fonts.get(m.strip()[:80], 0) + 1
        for _prop, val in SPACE_PROP_RE.findall(text):
            if "var(" in val or "calc(" in val or "%" in val or "auto" in val:
                continue
            for px in PX_RE.findall(val):
                key = px + "px"
                spacings[key] = spacings.get(key, 0) + 1
        for num, unit in DUR_RE.findall(text):
            key = num + unit
            durations[key] = durations.get(key, 0) + 1
        important += len(IMPORTANT_RE.findall(text))
        inline_styles += len(INLINE_STYLE_RE.findall(text))
        for m in CLASS_RE.findall(text):
            chunk = m[0] or m[1]
            for c in chunk.split():
                classes[c] = classes.get(c, 0) + 1
    return {"files": sorted(files),
            "unique_hex_colors": sorted(colors), "hex_colors": colors,
            "unique_color_functions": sorted(funcs), "color_functions": funcs,
            "border_radii": radii, "font_families": fonts,
            "px_spacing_values": spacings, "durations": durations,
            "important_count": important, "inline_style_attrs": inline_styles,
            "class_usage": classes, "class_count": len(classes)}


def scope_scan(root):
    def git(*args):
        return subprocess.run(["git", "-C", root] + list(args), text=True,
                              capture_output=True)
    head = git("rev-parse", "HEAD").stdout.strip()
    first = git("rev-list", "--max-parents=0", "HEAD").stdout.strip()
    diff = git("diff", "--stat", first).stdout
    names = git("diff", "--name-only", first).stdout.splitlines()
    untracked = git("status", "--porcelain").stdout.splitlines()
    ui, backend, other = [], [], []
    for n in names:
        if n.startswith(("templates/", "static/")) and not n.startswith("static/design/"):
            ui.append(n)
        elif n in ("app.py", "run.sh", "README.md") or n.startswith("data/"):
            backend.append(n)
        else:
            other.append(n)
    return {"head": head, "starter_commit": first,
            "changed_files": names, "ui_files": ui, "backend_files": backend,
            "other_files": other, "untracked": untracked, "diffstat": diff}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--snapshot", default=os.path.expanduser("~/triage-design-system-demo"))
    args = ap.parse_args(argv)
    ws = os.path.abspath(args.ws)

    pack = Pack(os.path.join(ROOT, "packs", "triage"))
    lint = validate(pack, ws, snapshot=args.snapshot)
    # keep only findings from the authored surface
    authored = [f for f in lint["findings"]
                if f["location"]["path"]
                and not f["location"]["path"].replace(ws + os.sep, "").startswith("static/design/")
                and not f["location"]["path"].replace(ws + os.sep, "").startswith(".bench/")]
    counts = {"error": 0, "warning": 0, "info": 0}
    for f in authored:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1

    # baseline = the pristine starter, linted identically; delta = agent-introduced
    baseline = validate(pack, os.path.join(ROOT, "benchmark", "starter"),
                        snapshot=args.snapshot)["findings"]
    base_counts = {"error": 0, "warning": 0, "info": 0}
    for f in baseline:
        base_counts[f["severity"]] = base_counts.get(f["severity"], 0) + 1
    base_multiset = Counter((f["rule"], f["message"]) for f in baseline)
    cur_multiset = Counter((f["rule"], f["message"]) for f in authored)
    sev_of = {f["rule"]: f["severity"] for f in authored + baseline}
    delta_by_rule, delta_counts = {}, {"error": 0, "warning": 0, "info": 0}
    for (rule, _msg), n in cur_multiset.items():
        extra = n - base_multiset.get((rule, _msg), 0)
        if extra > 0:
            delta_by_rule[rule] = delta_by_rule.get(rule, 0) + extra
            delta_counts[sev_of.get(rule, "warning")] += extra

    out = {
        "ws": ws,
        "lint": {"findings_total": len(lint["findings"]), "authored_total": len(authored),
                 "counts": counts, "by_rule": {},
                 "baseline_total": len(baseline), "baseline_counts": base_counts,
                 "delta_total": sum(delta_by_rule.values()), "delta_counts": delta_counts,
                 "delta_by_rule": delta_by_rule,
                 "top_findings": authored[:80]},
        "drift": drift_scan(ws),
        "scope": scope_scan(ws),
    }
    for f in authored:
        r = out["lint"]["by_rule"].setdefault(f["rule"], {"severity": f["severity"], "count": 0})
        r["count"] += 1
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=1)
    print("scan: lint authored=%d baseline=%d delta=%d (%s) | unique hex=%d px-values=%d classes=%d | backend files=%d"
          % (len(authored), len(baseline), out["lint"]["delta_total"], delta_counts,
             len(out["drift"]["unique_hex_colors"]),
             len(out["drift"]["px_spacing_values"]), out["drift"]["class_count"],
             len(out["scope"]["backend_files"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
