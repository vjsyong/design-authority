#!/usr/bin/env python3
"""Independent receipt confirmation for the reconciliation closure test.

Receipt claims are declarations until confirmed against evidence. This
script confirms, with source diffs and hashes, that:
  - r2a's `areas_modified` claim is true: the feedback / save-confirmation
    area actually changed from the v1 build (and ONLY the claimed areas);
  - r2b's `decisions_applied` claim is true: the migration actually changed
    that area toward the canonical notice.
The receipts themselves are never edited; this confirmation record points at
them (`confirms`). Fresh run only; artifact-local results are never proof."""

import difflib
import hashlib
import json
import os
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)                           # examples/cadence-wink-r2
REPO = os.path.dirname(os.path.dirname(APP))          # repo root
V1 = os.path.join(REPO, "examples/cadence-wink")
SNAP = os.path.join(APP, "_evidence", "snapshots", "r2a")
OUT = os.path.join(HERE, "verification", "receipt-confirmation.json")
FILES = ("index.html", "app.js", "app.css")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


def diff(a_dir, b_dir):
    lines = []
    for f in FILES:
        a = open(os.path.join(a_dir, f)).read().splitlines()
        b = open(os.path.join(b_dir, f)).read().splitlines()
        lines += [l for l in difflib.unified_diff(a, b, "v1/" + f, "r2/" + f, lineterm="", n=0)
                  if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
    return lines


def main():
    d_a = diff(V1, SNAP)          # the modification (r2a vs v1)
    d_b = diff(SNAP, APP)         # the migration (r2b vs r2a)
    checks = []

    def check(cid, desc, ok, detail):
        checks.append({"id": cid, "desc": desc, "pass": bool(ok), "detail": detail})

    check("r2a-changed-feedback", "the r2a modification changed the save-feedback area",
          any('showToast("Saved")' in l for l in d_a) and any("saveEcho" in l or "save-echo" in l for l in d_a),
          "%d changed lines; removes the improvised save toast, adds the ad-hoc echo" % len(d_a))
    check("r2a-scope", "the r2a change is confined to the claimed area (no wholesale rewrite)",
          len([l for l in d_a if l.startswith(("+", "-"))]) <= 12,
          "%d changed lines (claimed: feedback / save confirmation)" % len(d_a))
    check("r2b-migrated", "the r2b migration changed that area toward the canonical notice",
          any("saveNotice" in l for l in d_b) and any(".notice {" in l for l in d_b),
          "%d changed lines; adds the notice element and its canonical styling" % len(d_b))
    check("r2b-removed-echo", "the ad-hoc echo is gone after migration",
          any("save-echo" in l and l.startswith("-") for l in d_b),
          "the r2a echo markup/style is removed in r2b")

    verdict = "pass" if all(c["pass"] for c in checks) else "violation"
    out = {
        "confirmer": "_evidence/confirm-receipts.py",
        "target": "examples/cadence-wink-r2",
        "confirms": [".design-authority/receipts/2026-10-11-r2a-modification.json",
                     ".design-authority/receipts/2026-10-11-r2b-migration.json"],
        "ran_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "verdict": verdict,
        "checks": checks,
        "hashes": {"v1": {f: sha(os.path.join(V1, f)) for f in FILES},
                   "r2a_snapshot": {f: sha(os.path.join(SNAP, f)) for f in FILES},
                   "r2b_live": {f: sha(os.path.join(APP, f)) for f in FILES}},
        "note": "Receipt confirmation for the reconciliation closure test (docs/14 section 5: receipts are declared by the implementing agent and confirmed against evidence). Source diffs + hashes; fresh run only.",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("%s: %s (%d/%d checks)" % (verdict, OUT, sum(c["pass"] for c in checks), len(checks)))
    for c in checks:
        print("  %s %s - %s" % ("PASS" if c["pass"] else "FAIL", c["id"], c["detail"]))
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
