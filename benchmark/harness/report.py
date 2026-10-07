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


def collect(runs_dir):
    rows = []
    for name in sorted(os.listdir(runs_dir)):
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
        rows.append({
            "run": name,
            "condition": run.get("condition"),
            "exit": (run.get("opencode") or {}).get("exit"),
            "duration_s": (run.get("opencode") or {}).get("duration_s"),
            "authority_calls": (run.get("authority") or {}).get("total"),
            "lint_authored": lint.get("authored_total"),
            "lint_counts": lint.get("counts"),
            "lint_by_rule": lint.get("by_rule"),
            "unique_hex": len(drift.get("unique_hex_colors") or []),
            "px_spacing_values": len(drift.get("px_spacing_values") or {}),
            "classes": drift.get("class_count"),
            "important": drift.get("important_count"),
            "inline_styles": drift.get("inline_style_attrs"),
            "backend_files": len(scope.get("backend_files") or []),
            "ui_files": len(scope.get("ui_files") or []),
            "interact": "%s/%s" % ((run.get("interact") or {}).get("passed"),
                                   (run.get("interact") or {}).get("total")),
            "console_errors": console_errors,
        })
    return rows


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
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default=DEFAULT_RUNS)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    rows = collect(args.runs)
    text = render(rows)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text)
        print("report written to %s (%d runs)" % (args.out, len(rows)))
    else:
        print(text)


if __name__ == "__main__":
    main()
