#!/usr/bin/env python3
"""Semi-automated migration check (Phase 8, authority-evolution experiment).

Points the 0.13.0-experiment authority at a workspace built under 0.12.1 and
reports, per improvised usage: which local implementation is now superseded,
which new authority artifact applies, and what needs to change.
Report-grade tooling only (no migration framework) per the experiment protocol.

Usage:
  python3 tools/migration_check.py benchmark/runs/c3/ws [--pack packs/triage-evolution] [--json out.json]
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "kernel"))

from design_authority.pack import Pack            # noqa: E402
from design_authority.resolve import resolve      # noqa: E402

MARKER = re.compile(r"TODO\(authority[- ]undefined\)", re.I)

# group heuristics: which canonical need to re-resolve for each detected usage
GROUPS = [
    ("G-01 reviewer/entity assignment", re.compile(r"reviewer|assign|picker", re.I),
     "A compact picker for assigning a reviewer to a request from a small fixed list"),
    ("G-02 background-job progress", re.compile(r"progress|job|scan|stall", re.I),
     "Show the status and determinate progress of a long-running background triage scan, including running / done / failed and a stalled indication, with live updates"),
    ("G-03 reason-bearing decision", re.compile(r"reason|reject|irreversible|decision", re.I),
     "Rejecting a request requires typing a reason"),
]

TEXT_EXT = (".html", ".js", ".css", ".py", ".md")


def classify(snippet):
    for name, rx, need in GROUPS:
        if rx.search(snippet):
            return name, need
    return "G-?? unrecognised", None


def rid(result):
    res = result.get("resolution") or {}
    for key in ("artifact", "recipe", "fallback", "prohibition"):
        if isinstance(res.get(key), dict) and res[key].get("id"):
            return res[key]["id"]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--pack", default="packs/triage-evolution")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    pack = Pack(os.path.join(ROOT, args.pack))
    ws = os.path.join(ROOT, args.workspace) if not os.path.isabs(args.workspace) else args.workspace

    usages = []
    for dirpath, dirnames, filenames in os.walk(ws):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", "design")]
        for fn in filenames:
            if not fn.endswith(TEXT_EXT):
                continue
            path = os.path.join(dirpath, fn)
            try:
                lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                if MARKER.search(line):
                    rel = os.path.relpath(path, ws)
                    group, need = classify(" ".join(lines[max(0, i - 3):i + 3]))
                    entry = {"file": rel, "line": i, "snippet": line.strip()[:150], "group": group}
                    if need:
                        r = resolve(pack, need)
                        entry["authority_answer"] = {"outcome": r.get("outcome"), "id": rid(r)}
                    usages.append(entry)

    print(f"workspace: {ws}")
    print(f"markers found: {len(usages)}")
    for u in usages:
        a = u.get("authority_answer") or {}
        print(f"  {u['group']:34s} {u['file']}:{u['line']}")
        print(f"      {u['snippet']}")
        if a:
            print(f"      -> {a['outcome']} {a['id']}")

    # summary by group with supersede candidates
    summary = {}
    for u in usages:
        g = summary.setdefault(u["group"], {"count": 0, "files": [], "answer": None})
        g["count"] += 1
        if u["file"] not in g["files"]:
            g["files"].append(u["file"])
        if u.get("authority_answer"):
            g["answer"] = u["authority_answer"]
    print()
    print("summary:")
    for g, d in summary.items():
        print(f"  {g}: {d['count']} usage(s) in {len(d['files'])} file(s) -> {d['answer']}")

    if args.json:
        json.dump({"workspace": args.workspace, "pack": args.pack,
                   "usages": usages, "summary": summary},
                  open(os.path.join(ROOT, args.json), "w"), indent=1)
        print("saved ->", args.json)


if __name__ == "__main__":
    main()
