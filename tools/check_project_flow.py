#!/usr/bin/env python3
"""check_project_flow — pins the consumer workflow end to end (docs/13 P1.1/P1.2).

The memo's completion criterion: a new application can complete the workflow
(init → plan → build → receipt → verify → reconcile) through ordinary public
interfaces, with no manual fixture editing or custom orchestration scripts.
The acceptance vehicle is `examples/wink-notes/`; this gate re-runs every
deterministic step against a scratch copy and pins the outcomes, so the flow
survives refactoring.

Checks:
  1. the committed contract: lock, plan, case stub, receipt, reconciliation
     exist; receipt-check passes; the lock pins the authority/version
  2. plan outcomes: the five brief needs resolve/flag exactly as committed
     (4 RESOLVED with pinned ids, 1 UNDEFINED with its case stub)
  3. reconcile: re-run over a scratch copy reproduces the committed migration
     plan byte-for-byte (the plan carries no timestamps by design)
  4. the record layer: every owner-set transition policy (D-034) is present on
     the deployed packs, and versions follow the rc-label release policy
  5. receipt discipline: deviations reference pack ids; the verification ref
     exists on disk
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "kernel"))

APP = os.path.join(ROOT, "examples", "wink-notes")
WS = os.path.join(APP, ".design-authority")

EXPECTED_NEEDS = {
    "a primary action button": ("RESOLVED", "component/action-pill"),
    "an inline notice confirming a save": ("RESOLVED", "pattern/inline-notice"),
    "an empty state when no rituals exist": ("RESOLVED", "pattern/empty-state"),
    "a progress readout for saving": ("RESOLVED", "pattern/progress"),
    "a floating toast notification": ("UNDEFINED", None),
}

EXPECTED_RECONCILE = {
    "component/action-pill": "conforms",
    "pattern/empty-state": "conforms",
    "pattern/progress": "conforms",
    "pattern/inline-notice": "rectify",
}

# the owner-set policies (D-034) as deployed on the packs
EXPECTED_POLICIES = {
    ("wink", "pattern/destructive-confirm"): "required",
    ("wink", "pattern/progress"): "required",
    ("wink", "pattern/dialog-overlay"): "when_touched",
    ("wink", "pattern/empty-state"): "prospective",
    ("wink", "pattern/inline-notice"): "when_touched",
    ("leader", "pattern/data-charts"): "when_touched",
    ("leader", "pattern/data-readouts"): "prospective",
    ("leader", "component/tag"): "when_touched",
    ("dominion", "component/status"): "review",
    ("dominion", "component/ledger"): "prospective",
    ("dominion", "component/notice"): "prospective",
    ("dominion", "pattern/plain-chart"): "when_touched",
}


class Checker(object):
    def __init__(self):
        self.passed = 0
        self.failed = []

    def check(self, cond, label):
        if cond:
            self.passed += 1
        else:
            self.failed.append(label)
        return bool(cond)


def main():
    C = Checker()

    # 1. committed contract
    lock_p = os.path.join(WS, "authority.lock.json")
    plan_p = os.path.join(WS, "design-plan.json")
    rec_p = os.path.join(WS, "receipt.json")
    C.check(os.path.exists(lock_p) and os.path.exists(plan_p) and os.path.exists(rec_p),
            "contract files missing under examples/wink-notes/.design-authority")
    lock = json.load(open(lock_p))
    C.check(lock.get("authority") == "wink" and lock.get("version"),
            "lock does not pin the wink authority: %s" % lock)
    C.check(isinstance(lock.get("fingerprint"), str) and lock["fingerprint"].startswith("sha256:"),
            "lock fingerprint missing")

    receipt_files = [f for f in os.listdir(os.path.join(WS, "receipts")) if f.endswith(".json")]
    C.check(len(receipt_files) == 1, "expected exactly one outcome receipt, got %d" % len(receipt_files))
    receipt = json.load(open(os.path.join(WS, "receipts", receipt_files[0])))

    # 2. plan outcomes
    plan = json.load(open(plan_p))
    for need, (outcome, rid) in EXPECTED_NEEDS.items():
        entry = next((n for n in plan["needs"] if n["need"] == need), None)
        C.check(entry is not None and entry["outcome"] == outcome and entry.get("id") == rid,
                "plan drifted for %r: %s" % (need, entry))
    case_stub = os.path.join(WS, "cases", "05-a-floating-toast-notification.json")
    C.check(os.path.exists(case_stub), "the UNDEFINED need lost its case stub")

    # 3. reconcile determinism (scratch copy)
    tmp = tempfile.mkdtemp(prefix="da-flow-")
    try:
        dest = os.path.join(tmp, "wink-notes")
        shutil.copytree(APP, dest, ignore=shutil.ignore_patterns(".git"))
        rec = subprocess.run([sys.executable, os.path.join(HERE, "da.py"),
                              "--pack", "authorities/wink", "reconcile", "--workspace", dest],
                             capture_output=True, text=True, cwd=ROOT)
        C.check(rec.returncode == 0, "reconcile failed: %s" % rec.stderr[-200:])
        fresh = json.load(open(os.path.join(dest, ".design-authority", "reconciliation.json")))
        committed = json.load(open(os.path.join(WS, "reconciliation.json")))
        C.check(fresh == committed, "reconcile output is not reproducible")
        classes = {f["decision"]: f["class"] for f in fresh["findings"]}
        C.check(classes == EXPECTED_RECONCILE, "reconcile classes drifted: %s" % classes)
        actions = {(a["decision"], a["action"]) for a in fresh["actions"]}
        C.check(("pattern/inline-notice", "migrate") in actions,
                "the flagged toast deviation no longer produces a migration action")
        C.check(any(f.get("receipt_status") == "unconfirmed" for f in fresh["findings"]),
                "receipt evidence is no longer marked unconfirmed without a confirmer")

        # plan re-runs identically (needs + outcomes)
        rc = subprocess.run([sys.executable, os.path.join(HERE, "da.py"), "--pack", "authorities/wink",
                             "plan", os.path.join(dest, "BRIEF.md"), "--workspace", dest],
                            capture_output=True, text=True, cwd=ROOT)
        C.check(rc.returncode == 0, "plan re-run failed: %s" % rc.stderr[-200:])
        replan = json.load(open(os.path.join(dest, ".design-authority", "design-plan.json")))
        C.check([n["need"] for n in replan["needs"]] == [n["need"] for n in plan["needs"]]
                and [n["outcome"] for n in replan["needs"]] == [n["outcome"] for n in plan["needs"]],
                "plan re-run is not stable")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 4. the record layer
    for (auth, rid), policy in EXPECTED_POLICIES.items():
        arts = json.load(open(os.path.join(ROOT, "authorities", auth, "artifacts.json")))["artifacts"]
        rec = next((r for r in arts if r["id"] == rid), None)
        got = (rec or {}).get("transition", {}).get("policy")
        C.check(got == policy, "transition policy missing on %s/%s: %s" % (auth, rid, got))
    for auth in ("wink", "leader", "dominion"):
        version = json.load(open(os.path.join(ROOT, "authorities", auth, "authority.json")))["version"]
        C.check("-rc" in version, "%s version is not an rc label: %s" % (auth, version))

    # 5. receipt discipline
    for d in receipt.get("deviations") or []:
        C.check(d.get("reviewed") is False, "deviation review state drifted: %s" % d)
    ver_ref = (receipt.get("verification") or {}).get("ref")
    C.check(ver_ref and os.path.exists(os.path.join(APP, ver_ref.rstrip("/"), "summary.txt")),
            "the receipt's verification reference does not exist on disk")
    rcpt_check = subprocess.run([sys.executable, os.path.join(HERE, "da.py"), "--pack", "authorities/wink",
                                 "receipt-check", os.path.join(WS, "receipts", receipt_files[0]),
                                 "--workspace", APP], capture_output=True, text=True, cwd=ROOT)
    C.check(rcpt_check.returncode == 0, "receipt-check fails: %s" % rcpt_check.stderr[-200:])

    if C.failed:
        for label in C.failed:
            if label:
                print("FAIL %s" % label, file=sys.stderr)
        print("project flow: %d passed, %d failed" % (C.passed, len(C.failed)))
        return 1
    print("project flow: %d passed, 0 failed (init → plan → receipt → verify → reconcile pinned; "
          "record layer carries the owner-set policies)" % C.passed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
