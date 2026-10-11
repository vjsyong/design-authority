#!/usr/bin/env python3
"""reconcile_regression — pins the tested reconciliation lifecycle.

Formalization gate (docs/14, P1.4): the behaviours proven by the Cadence
lifecycle test (docs/experiments/07-reconciliation-cadence.md) must survive
future refactoring. Deterministic and browser-free: the DOM verifier's
committed outputs are re-checked for FRESHNESS (record hash + build-file
hashes) instead of re-run; if the record or the build changed, this gate
fails and the verifier must be re-run.

Checks: pinned class counts; idempotent re-sweep; chain-derived links equal
explicit links; the legacy default; the closure cycle end to end (stage 1
trigger + due obligation; stage 2 closed obligation + conforming revision);
and evidence freshness. Wired into tools/check.sh.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import da_sweep  # noqa: E402

REPO = da_sweep.REPO
FIX = os.path.join(REPO, "docs", "experiments", "reconcile-cadence")
R2 = os.path.join(REPO, "examples", "cadence-wink-r2")
MAIN_COUNTS = {"conforms": 10, "grandfathered": 18, "rectify": 4, "review": 4}


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


def run_sweep(store, report, portfolio, authority, decision=None):
    cmd = [sys.executable, os.path.join(HERE, "da_sweep.py"),
           "--authority", authority, "--portfolio", portfolio,
           "--store", store, "--target-version", "0.2.0", "--report", report]
    if decision:
        cmd += ["--decision", decision]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    if r.returncode != 0:
        return None
    with open(report) as fh:
        return json.load(fh)


def strip_resolves(authority_dir, out_dir):
    for auth in sorted(os.listdir(authority_dir)):
        src = os.path.join(authority_dir, auth, "artifacts.json")
        if not os.path.exists(src):
            continue
        data = json.load(open(src))
        for rec in data["artifacts"]:
            rec.pop("resolves_cases", None)
        dest = os.path.join(out_dir, auth)
        os.makedirs(dest, exist_ok=True)
        with open(os.path.join(dest, "artifacts.json"), "w") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)


def check_main(tmp, C):
    store = os.path.join(tmp, "main.jsonl")
    report = os.path.join(tmp, "main-report.json")
    r1 = run_sweep(store, report, os.path.join(FIX, "portfolio.json"),
                   os.path.join(FIX, "authority"))
    C.check(r1 is not None, "main sweep failed to run")
    if not r1:
        return
    C.check(r1["counts"] == MAIN_COUNTS, "main counts drifted: %s" % r1["counts"])
    C.check(r1["obligations"] == {"scheduled": 4},
            "main obligations drifted: %s" % r1["obligations"])
    C.check(r1["store"]["new"] == 36, "main run added %s new findings" % r1["store"]["new"])

    r2 = run_sweep(store, report, os.path.join(FIX, "portfolio.json"),
                   os.path.join(FIX, "authority"))
    C.check(r2 and r2["store"]["new"] == 0 and r2["store"]["reused"] == 36,
            "re-sweep not idempotent: %s" % (r2 or {}).get("store"))

    # chain-derived links must equal explicit links
    stripped = os.path.join(tmp, "authority-stripped")
    strip_resolves(os.path.join(FIX, "authority"), stripped)
    report3 = os.path.join(tmp, "chain-report.json")
    r3 = run_sweep(os.path.join(tmp, "chain.jsonl"), report3,
                   os.path.join(FIX, "portfolio.json"), stripped)
    if r3:
        a = {f["id"]: (f["class"], f["reason"]) for f in r1["findings"]}
        b = {f["id"]: (f["class"], f["reason"]) for f in r3["findings"]}
        C.check(a == b, "chain-derived links diverge from explicit links")
        C.check(all(f["link"]["via"] == "proposal-chain" for f in r3["findings"]),
                "chain run did not derive links from the recorded chain")
    else:
        C.check(False, "chain variant sweep failed to run")

    # the legacy default (no transition blocks -> review, no obligations)
    r4 = run_sweep(os.path.join(tmp, "defaults.jsonl"), os.path.join(tmp, "defaults-report.json"),
                   os.path.join(FIX, "portfolio.json"), os.path.join(FIX, "authority-default"))
    C.check(r4 and r4["counts"] == {"conforms": 10, "grandfathered": 0, "rectify": 0, "review": 26}
            and not r4["obligations"],
            "defaults run drifted: %s" % (r4 or {}).get("counts"))


def check_closure(tmp, C):
    store = os.path.join(tmp, "closure.jsonl")
    r1 = run_sweep(store, os.path.join(tmp, "closure-1.json"),
                   os.path.join(FIX, "closure/portfolio-stage1.json"),
                   os.path.join(FIX, "authority"), decision="pattern/inline-notice")
    C.check(r1 is not None, "closure stage 1 failed to run")
    if r1:
        C.check(r1["counts"] == {"conforms": 0, "grandfathered": 1, "rectify": 1, "review": 0},
                "closure stage-1 counts drifted: %s" % r1["counts"])
        C.check(r1["obligations"] == {"due": 1},
                "closure stage-1 obligations drifted: %s" % r1["obligations"])
        v1 = next(f for f in r1["findings"] if f["revision"] == "v1")
        C.check(v1["trigger_state"]["state"] == "occurred"
                and v1["trigger_state"].get("evidence"),
                "v1 trigger not recorded as occurred with evidence")

    r2 = run_sweep(store, os.path.join(tmp, "closure-2.json"),
                   os.path.join(FIX, "closure/portfolio.json"),
                   os.path.join(FIX, "authority"), decision="pattern/inline-notice")
    C.check(r2 is not None, "closure stage 2 failed to run")
    if not r2:
        return
    C.check(r2["counts"] == {"conforms": 1, "grandfathered": 1, "rectify": 1, "review": 0},
            "closure stage-2 counts drifted: %s" % r2["counts"])
    C.check(r2["obligations"] == {"closed": 1},
            "closure stage-2 obligations drifted: %s" % r2["obligations"])
    r2a = next(f for f in r2["findings"] if f["revision"] == "r2a")
    ob = r2a.get("obligation") or {}
    C.check(ob.get("state") == "closed"
            and ob.get("closed_by") and "r2b-migration" in ob["closed_by"][0]
            and (ob.get("verification") or {}).get("result") == "pass",
            "r2a obligation not closed by the verified r2b receipt: %s" % ob)
    C.check((r2a.get("previous") or {}).get("obligation", {}).get("state") == "due",
            "r2a supersession history lost (previous due state)")
    r2b = next(f for f in r2["findings"] if f["revision"] == "r2b")
    C.check(r2b["class"] == "conforms" and r2b.get("receipt_status") == "confirmed",
            "r2b not confirming with a confirmed receipt: %s" % r2b)
    C.check(all(f.get("receipt_status") == "confirmed" for f in r2["findings"]
                if f.get("receipt_status")),
            "a receipt-evidence finding is unconfirmed")


def check_evidence_freshness(C):
    """Committed verifier/confirmer outputs must still describe the live
    record and build; staleness fails loudly instead of silently decaying."""
    pack = json.load(open(os.path.join(REPO, "authorities", "wink", "artifacts.json")))
    record = next((a for a in pack["artifacts"] if a["id"] == "pattern/inline-notice"), None)
    rhash = (hashlib.sha256(json.dumps(record, sort_keys=True, ensure_ascii=False).encode())
             .hexdigest()[:16] if record else None)
    ver = json.load(open(os.path.join(R2, "_evidence/verification/notice-migration.json")))
    C.check(ver.get("verdict") == "pass", "notice-migration verdict is not pass")
    C.check(ver.get("record", {}).get("record_hash") == rhash,
            "verification is STALE: record hash %s != committed %s - re-run the verifier"
            % (rhash, ver.get("record", {}).get("record_hash")))
    C.check(all(c.get("pass") for c in ver.get("checks", [])),
            "a committed verification check is failing")
    conf = json.load(open(os.path.join(R2, "_evidence/verification/receipt-confirmation.json")))
    C.check(conf.get("verdict") == "pass", "receipt confirmation verdict is not pass")
    for f, h in conf.get("hashes", {}).get("r2b_live", {}).items():
        live = hashlib.sha256(open(os.path.join(R2, f), "rb").read()).hexdigest()[:16]
        C.check(live == h, "build file %s changed since confirmation (%s != %s) - "
                           "re-run confirm-receipts.py" % (f, live, h))


def main():
    C = Checker()
    tmp = tempfile.mkdtemp(prefix="da-reconcile-")
    try:
        check_main(tmp, C)
        check_closure(tmp, C)
        check_evidence_freshness(C)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if C.failed:
        for label in C.failed:
            print("FAIL %s" % label, file=sys.stderr)
        print("reconcile regression: %d passed, %d failed" % (C.passed, len(C.failed)))
        return 1
    print("reconcile regression: %d passed, 0 failed "
          "(main 36 pinned · idempotent · chain links · defaults · closure cycle · evidence fresh)"
          % C.passed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
