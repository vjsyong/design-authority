#!/usr/bin/env python3
"""Aggregate benchmark runs into a per-dimension report (no composite score).

    python3 report.py [--runs DIR] [--out FILE]
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DEFAULT_RUNS = os.path.join(ROOT, "benchmark", "runs")


def load(path):
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    return None


def collect(runs_dir, include=None):
    rows = []
    for name in sorted(os.listdir(runs_dir)):
        if include and name not in include:
            continue
        rdir = os.path.join(runs_dir, name)
        run = load(os.path.join(rdir, "run.json"))
        if not run:
            continue
        scan = load(os.path.join(rdir, "scan.json")) or {}
        capture = load(os.path.join(rdir, "capture", "capture.json")) or {}
        interact = load(os.path.join(rdir, "interact.json")) or {}
        console_errors = 0
        for entry in (capture.get("routes") or {}).values():
            console_errors += len(entry.get("console_errors") or [])
        lint = (scan.get("lint") or {})
        drift = (scan.get("drift") or {})
        scope = (scan.get("scope") or {})
        # gaps / proposals recorded by a C run inside its workspace archive
        gaps_n, proposals_n = 0, 0
        attr_dir = os.path.join(rdir, "ws", ".design-authority")
        gaps_path = os.path.join(attr_dir, "gaps.jsonl")
        if os.path.exists(gaps_path):
            with open(gaps_path) as fh:
                gaps_n = sum(1 for line in fh if line.strip())
        prop_dir = os.path.join(attr_dir, "proposals")
        if os.path.isdir(prop_dir):
            proposals_n = len([f for f in os.listdir(prop_dir) if f.endswith(".json")])
        inter = interact.get("result") or {}
        rows.append({
            "run": name,
            "condition": run.get("condition"),
            "exit": (run.get("opencode") or {}).get("exit"),
            "duration_s": (run.get("opencode") or {}).get("duration_s"),
            "authority_calls": (run.get("authority") or {}).get("total"),
            "authority": run.get("authority") or {},
            "containment": run.get("containment") or {},
            "sandbox": (run.get("isolation") or {}).get("sandbox"),
            "lint_authored": lint.get("authored_total"),
            "lint_counts": lint.get("counts"),
            "lint_by_rule": lint.get("by_rule"),
            "unique_hex": len(drift.get("unique_hex_colors") or []),
            "px_spacing_values": len(drift.get("px_spacing_values") or {}),
            "classes": drift.get("class_count"),
            "important": drift.get("important_count"),
            "inline_styles": drift.get("inline_style_attrs"),
            "drift_detail": {
                "hex": drift.get("unique_hex_colors"),
                "px": drift.get("px_spacing_values"),
                "radii": len(drift.get("border_radii") or []),
                "fonts": drift.get("font_families"),
            },
            "backend_files": len(scope.get("backend_files") or []),
            "ui_files": len(scope.get("ui_files") or []),
            "interact": "%s/%s" % (inter.get("passed"), inter.get("total")),
            "interact_failures": [c.get("name") for c in (inter.get("checks") or [])
                                  if not c.get("ok")],
            "console_errors": console_errors,
            "gaps_n": gaps_n,
            "proposals_n": proposals_n,
        })
    return rows


def _top(d, n=12):
    """Render a dict/list of extractor findings compactly."""
    if not d:
        return "-"
    if isinstance(d, dict):
        items = sorted(d.items(), key=lambda kv: -kv[1] if isinstance(kv[1], int) else 0)
        return ", ".join("%s×%s" % (k, v) for k, v in items[:n])
    items = list(d)
    return ", ".join(str(x) for x in items[:n]) + ("" if len(items) <= n else " …(+%d)" % (len(items) - n))


def render(rows):
    lines = ["# Benchmark runs — per-dimension summary", "",
             "No composite score. Read dimensions independently; paired",
             "comparisons (C vs B, B vs A) are the interesting ones.", ""]
    header = ("| run | cond | exit | dur(s) | auth calls | lint (e/w/i) | hex | "
              "px vals | classes | !imp | inline | backend | ui files | interact | console err |")
    sep = "|" + "---|" * 15
    lines += [header, sep]
    for r in rows:
        c = r["lint_counts"] or {}
        lines.append("| %s | %s | %s | %s | %s | %s/%s/%s | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
                     % (r["run"], r["condition"], r["exit"], r["duration_s"],
                        r["authority_calls"] if r["authority_calls"] is not None else "-",
                        c.get("error", 0), c.get("warning", 0), c.get("info", 0),
                        r["unique_hex"], r["px_spacing_values"], r["classes"],
                        r["important"], r["inline_styles"], r["backend_files"],
                        r["ui_files"], r["interact"], r["console_errors"]))
    lines.append("")
    by_rule = {}
    for r in rows:
        for rule, d in (r["lint_by_rule"] or {}).items():
            by_rule.setdefault(rule, {})[r["run"]] = d["count"]
    if by_rule:
        lines.append("## triage-lint findings by rule")
        lines.append("")
        rules = sorted(by_rule)
        lines.append("| rule | " + " | ".join(r["run"] for r in rows) + " |")
        lines.append("|" + "---|" * (len(rows) + 1))
        for rule in rules:
            cells = [str(by_rule[rule].get(r["run"], 0)) for r in rows]
            lines.append("| %s | %s |" % (rule, " | ".join(cells)))
        lines.append("")

    lines.append("## drift detail (one-off treatments)")
    lines.append("")
    for r in rows:
        d = r["drift_detail"]
        lines.append("- **%s**: hex [%s] · px [%s] · radii decls %s · fonts [%s]"
                     % (r["run"], _top(d["hex"]), _top(d["px"]), d["radii"],
                        _top(d["fonts"], 4)))
    lines.append("")

    c_rows = [r for r in rows if r["condition"] == "C"]
    if c_rows:
        lines.append("## authority behavior (condition C)")
        lines.append("")
        lines.append("| run | calls | RESOLVED | COMPOSE | FALLBACK | UNDEFINED | CONFLICT | gaps | proposals |")
        lines.append("|" + "---|" * 9)
        for r in c_rows:
            a = r["authority"]
            o = a.get("resolve_outcomes") or {}
            lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |"
                         % (r["run"], a.get("total", 0),
                            o.get("RESOLVED", 0), o.get("COMPOSE", 0),
                            o.get("FALLBACK", 0), o.get("UNDEFINED", 0),
                            o.get("CONFLICT", 0), r["gaps_n"], r["proposals_n"]))
        lines.append("")
        for r in c_rows:
            calls = (r["authority"].get("calls") or {})
            lines.append("- **%s tool mix**: %s"
                         % (r["run"], ", ".join("%s×%s" % (k, v) for k, v in
                                                sorted(calls.items()))))
        lines.append("")

    if any(r["containment"] for r in rows):
        lines.append("## containment")
        lines.append("")
        lines.append("| run | sandbox | attempts | mentions | denied | da_zone |")
        lines.append("|" + "---|" * 6)
        for r in rows:
            c = r["containment"]
            lines.append("| %s | %s | %s | %s | %s | %s |"
                         % (r["run"], r["sandbox"], c.get("attempts"),
                            c.get("mentions"), c.get("denied_events"),
                            c.get("da_zone", "-")))
        lines.append("")

    fails = [r for r in rows if r["interact_failures"]]
    if fails:
        lines.append("## interact failures")
        lines.append("")
        for r in fails:
            lines.append("- %s: %s" % (r["run"], ", ".join(r["interact_failures"])))
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default=DEFAULT_RUNS)
    ap.add_argument("--include", default=None,
                    help="comma-separated run ids to include (default: all)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    include = set(args.include.split(",")) if args.include else None
    rows = collect(args.runs, include)
    text = render(rows)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text)
        print("report written to %s (%d runs)" % (args.out, len(rows)))
    else:
        print(text)


if __name__ == "__main__":
    main()
