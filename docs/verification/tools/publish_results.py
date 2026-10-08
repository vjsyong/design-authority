#!/usr/bin/env python3
"""publish_results — copy verifier raw results into each build's _evidence.

The Authority Lens fetches this file relatively; it is evidence output, not
an app modification (additive, like the screenshots folder).
"""
import hashlib
import json
import os

REPO = "/home/xrim/design-authority"


def sha(path):
    h = hashlib.sha256()
    h.update(open(path, "rb").read())
    return h.hexdigest()


TARGETS = [("wink", "harden-clean-wink"), ("leader", "harden-clean-leader"),
           ("dominion", "harden-clean-dominion"), ("phantom", "phantom-app")]
for build, raw_dir in TARGETS:
    raw = json.load(open(os.path.join(REPO, "docs", "verification", "raw", raw_dir, "raw.json")))
    appdir = os.path.join(REPO, "examples", "phantom-audit" if build == "phantom" else f"cadence3-{build}")
    covers = {}
    cover_files = ("assets/css/main.css", "app.js", "index.html") if build == "phantom" else ("app.css", "app.js", "index.html")
    for fn in cover_files:
        pth = os.path.join(appdir, fn)
        if os.path.exists(pth):
            covers[fn] = sha(pth)[:16]
    out = {
        "generated": raw["generated"],
        "tool": "tools/da_verify.py",
        "target": raw["target"],
        "summary": raw["summary"],
        "covers": covers,
        "covers_note": ("sha256[:16] of the app files this run read — if the served files differ, "
                        "these results are stale; re-run the verifier. Results shipped inside the "
                        "artifact are artifact-local: they can be replaced by whoever writes the artifact, "
                        "so re-running tools/da_verify.py is the only trusted confirmation."),
        "note": "Independent verification results (verification experiment, 2026-10-08; post-adversarial hardening). "
                "Claims are not evidence; these results come from files, DOM, computed style and behaviour.",
        "checks": [
            {"id": c["id"], "item": c["item"], "title": c["title"], "mode": c["mode"],
             "severity": c["severity"], "status": c["status"], "selector": c.get("selector"),
             "observed": c.get("observed", [])[:2], "note": c.get("note")}
            for c in raw["checks"]
        ],
    }
    d = os.path.join(appdir, "_evidence", "verification")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"{build}-verification.json")
    with open(p, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print("published", os.path.relpath(p, REPO), f"({len(out['checks'])} checks, "
          f"{out['summary']['PASS']} pass / {out['summary']['VIOLATION']} violations, covers {covers})")
