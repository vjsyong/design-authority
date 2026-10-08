#!/usr/bin/env python3
"""publish_results — copy verifier raw results into each build's _evidence.

The Authority Lens fetches this file relatively; it is evidence output, not
an app modification (additive, like the screenshots folder).
"""
import json
import os
import time

REPO = "/home/xrim/design-authority"
for build in ("wink", "leader", "dominion"):
    raw = json.load(open(os.path.join(REPO, "docs", "verification", "raw", f"{build}-clean", "raw.json")))
    out = {
        "generated": raw["generated"],
        "tool": "tools/da_verify.py",
        "target": raw["target"],
        "summary": raw["summary"],
        "note": "Independent verification results (verification experiment, 2026-10-08). "
                "Claims are not evidence; these results come from files, DOM, computed style and behaviour.",
        "checks": [
            {"id": c["id"], "item": c["item"], "title": c["title"], "mode": c["mode"],
             "severity": c["severity"], "status": c["status"], "selector": c.get("selector"),
             "observed": c.get("observed", [])[:2], "note": c.get("note")}
            for c in raw["checks"]
        ],
    }
    d = os.path.join(REPO, "examples", f"cadence3-{build}", "_evidence", "verification")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"{build}-verification.json")
    with open(p, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print("published", os.path.relpath(p, REPO), f"({len(out['checks'])} checks, "
          f"{out['summary']['PASS']} pass / {out['summary']['VIOLATION']} violations)")
