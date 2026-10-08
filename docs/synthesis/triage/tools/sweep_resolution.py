#!/usr/bin/env python3
"""sweep_resolution — the element-by-element coverage sweep for packs/triage.

Every element the triage design system documents (the 35-component contract
matrix, the furniture documented in core and the component pages, the seven
page patterns, the token sets, the foundations and doctrine guidelines) gets
asked for in natural consumer language. Each ask must resolve to its element;
anything else is a coverage miss and fails the run.

    python3 docs/synthesis/triage/tools/sweep_resolution.py            # run + report
    python3 docs/synthesis/triage/tools/sweep_resolution.py --json     # machine-readable report
"""
import argparse
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "kernel"))

from design_authority.pack import Pack  # noqa: E402
from design_authority.resolve import resolve  # noqa: E402

PACK = os.path.join(ROOT, "authorities", "triage")
CASES = os.path.join(ROOT, "docs", "synthesis", "triage", "coverage.json")
REPORT = os.path.join(ROOT, "docs", "synthesis", "triage", "coverage-report.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    ap.add_argument("--quiet", action="store_true", help="only print the summary line")
    args = ap.parse_args()

    pack = Pack(PACK)
    cases = json.load(open(CASES))["cases"]

    rows, misses = [], []
    for c in cases:
        r = resolve(pack, c["ask"])
        outcome = r.get("outcome")
        rid = None
        res = r.get("resolution") or {}
        if outcome == "RESOLVED":
            rid = (res.get("artifact") or {}).get("id")
        ok = outcome == c.get("expect_outcome", "RESOLVED") and rid == (c.get("expect_id") or rid)
        row = {"element": c["element"], "ask": c["ask"], "expect_id": c.get("expect_id"),
               "outcome": outcome, "got_id": rid, "ok": ok}
        rows.append(row)
        if not ok:
            misses.append(row)

    report = {"pack": pack.manifest.get("id"), "pack_version": pack.manifest.get("version"),
              "total": len(rows), "passed": len(rows) - len(misses), "misses": misses, "rows": rows}
    json.dump(report, open(REPORT, "w"), indent=1, ensure_ascii=False)

    if args.json:
        print(json.dumps(report, indent=1, ensure_ascii=False))
        return 1 if misses else 0

    if misses and not args.quiet:
        print("MISSES (%d):" % len(misses))
        for m in misses:
            print("  [%s]  ask: %r\n      want: %s\n      got:  %s (%s)"
                  % (m["element"], m["ask"], m["expect_id"], m["got_id"], m["outcome"]))
    print("sweep: %d/%d asks resolve to the right element" % (report["passed"], report["total"]))
    if misses:
        print("report written to %s" % REPORT)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
