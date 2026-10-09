#!/usr/bin/env python3
"""CI check: run each authority's verification contract against its recorded
target (docs/ci/contract-targets.json) and fail only on NEW findings.

Failing statuses: VIOLATION and UNVERIFIABLE. REVIEW_REQUIRED and
NOT_APPLICABLE never fail. Findings listed under the target's
`expected_findings` are tolerated (recorded known state; extending the list
is a deliberate edit with a reason - see docs/ci/README.md).

Usage:  python3 tools/ci_verify.py [--auth NAME]
Exit:   0 when no new findings; 1 otherwise.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF = os.path.join(ROOT, "docs", "ci", "contract-targets.json")
FAILING = ("VIOLATION", "UNVERIFIABLE")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth", default=None, help="one authority; default: all")
    args = ap.parse_args()

    conf = json.load(open(CONF))
    picks = [args.auth] if args.auth else sorted(conf)
    failures = 0
    for auth in picks:
        spec = conf[auth]
        target = os.path.join(ROOT, spec["target"])
        out = tempfile.mkdtemp(prefix="ci-verify-%s-" % auth)
        cmd = [sys.executable, os.path.join(ROOT, "tools", "da_verify.py"),
               "--pack", os.path.join(ROOT, "authorities", auth),
               "--target", target, "--out", out, "--no-shots"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        raw_path = os.path.join(out, "raw.json")
        if not os.path.isfile(raw_path):
            print("[%s] FAIL: da_verify produced no raw.json" % auth)
            print((proc.stdout or "")[-2000:])
            print((proc.stderr or "")[-2000:])
            failures += 1
            continue
        raw = json.load(open(raw_path))
        bad = {c["id"]: c.get("status") for c in raw["checks"]
               if c.get("status") in FAILING}
        expected = set(spec.get("expected_findings", []))
        new = {k: v for k, v in bad.items() if k not in expected}
        print("[%s] %s: %d checks, %d failing, %d new"
              % (auth, spec["target"], len(raw["checks"]), len(bad), len(new)))
        for k, v in sorted(new.items()):
            print("   NEW %s: %s" % (v, k))
        for k in sorted(set(bad) & expected):
            print("   expected: %s" % k)
        for k in sorted(expected - set(bad)):
            print("   note: baseline entry no longer failing: %s" % k)
        if new:
            failures += 1
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
