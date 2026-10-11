#!/usr/bin/env python3
"""check_case_model — pins the Case read model (docs/16) inside check.sh.

The owner's completion criteria for P1 (da_nextsteps.md section 2): historical
gaps, proposals, disputes, and reconciliation findings are all retrievable
through one Case interface, with no loss of provenance and no change to
existing resolution behavior. This gate re-derives the corpus independently
and checks the view against it; it never trusts the tool's own counters.

Checks:
  1. corpus coverage: every store file's gap ids appear in `da_case list`,
     one case row per id, occurrence counts equal
  2. proposals: every proposal file appears in its gap's thread as
     proposal_submitted; every proposal resolves to a stored gap
  3. disputes: every store row is retrievable via `show` with a source
  4. findings: every finding attaches to a listed case; the flagship thread
     carries its impact events; the closure thread carries the closed
     obligation with its verification
  5. golden thread: `show gap/20261007-145139-ad4b85` equals the pinned
     event-kind sequence with the pinned publication detail
  6. `why pattern/destructive-confirm` traces to its proposal and gap;
     `why pattern/inline-notice` carries the r2b receipt and the closed r2a
     obligation
  7. provenance: every event in the golden threads names an existing source
     file and a source record; every kind is in the documented vocabulary
  8. determinism: two independent builds produce identical output
"""
import copy
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import da_case  # noqa: E402

KINDS = {"gap_reported", "evidence_attached", "proposal_submitted", "proposal_reviewed",
         "authority_published", "precedent_recorded", "receipt_recorded",
         "impact_assessed", "migration_required", "migration_verified",
         "obligation_closed", "dispute_raised"}

GOLDEN_SEQ = ["gap_reported", "proposal_submitted", "proposal_reviewed",
              "authority_published", "impact_assessed", "impact_assessed",
              "impact_assessed", "migration_required", "migration_required"]


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


def independent_gap_ids():
    """Walk the corpus directly (no da_case helpers) and collect gap ids."""
    ids = []
    skip = "docs/experiments/seed-evolution/annexes"
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        if skip in dirpath:
            continue
        if os.path.basename(dirpath) == ".design-authority" and "gaps.jsonl" in filenames:
            with open(os.path.join(dirpath, "gaps.jsonl")) as fh:
                for line in fh:
                    if line.strip():
                        ids.append(json.loads(line)["id"])
    return ids


def run_tool(*args):
    r = subprocess.run([sys.executable, os.path.join(HERE, "da_case.py")] + list(args),
                       capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def main():
    C = Checker()
    db = da_case.build()
    view = da_case.list_view(db)

    # 1. corpus coverage
    ids = independent_gap_ids()
    seen = sorted(g["id"] for _, g, _ in db["gaps"])
    C.check(sorted(ids) == seen, "gap corpus coverage drifted: %d direct vs %d scanned"
            % (len(ids), len(seen)))
    rows = {r["id"]: r for r in view["gaps"]}
    C.check(len(rows) == len(set(ids)), "case rows are not one per unique gap id")
    occ = {gid: ids.count(gid) for gid in set(ids)}
    bad = [gid for gid, n in occ.items() if rows.get(gid, {}).get("occurs") != n]
    C.check(not bad, "occurrence counts wrong for %s" % bad[:4])

    # 2. proposals
    missing = []
    for ws, prop, pfile in db["proposals"]:
        if prop.get("gap_id") not in rows:
            missing.append(prop["id"])
            continue
        title, ev = da_case.resolve_root(db, prop.get("gap_id"))
        if not any(e["kind"] == "proposal_submitted" and e["source"]["record"] == prop["id"]
                   for e in ev):
            missing.append(prop["id"])
    C.check(not missing, "proposals not retrievable through their gap thread: %s" % missing[:4])

    # 3. disputes
    dmissing = []
    for rid, row, dfile in db["disputes"]:
        rc, out, err = run_tool("--json", "show", rid)
        if rc != 0 or '"dispute_raised"' not in out:
            dmissing.append(rid)
    C.check(not dmissing, "disputes not retrievable: %s" % dmissing)
    C.check(len(db["disputes"]) >= 4, "recorded disputes missing (found %d)" % len(db["disputes"]))

    # 4. findings attachment
    unattached = [f["id"] for f, _ in db["findings"]
                  if (f.get("link") or {}).get("case") not in rows]
    C.check(not unattached, "findings without a listed case: %s" % unattached[:4])
    _, flagship = da_case.resolve_root(db, "gap/20261007-145139-ad4b85")
    flagship = flagship or []
    impacts = [e for e in flagship if e["kind"] == "impact_assessed"
               and e["decision"] == "pattern/destructive-confirm"]
    C.check(len(impacts) == 3, "flagship impacts drifted: %d" % len(impacts))
    _, closure = da_case.resolve_root(db, "gap/20261007-145938-f646b2")
    closure = closure or []
    C.check(any(e["kind"] == "obligation_closed" and (e.get("closed_by") or [])
                for e in closure), "closure thread lost its closed obligation")
    C.check(any(e["kind"] == "migration_verified" and e.get("verification") == "pass"
                for e in closure), "closure thread lost the verification result")

    # 5. golden sequence
    C.check([e["kind"] for e in flagship] == GOLDEN_SEQ,
            "flagship event sequence drifted: %s" % [e["kind"] for e in flagship])
    pub = next((e for e in flagship if e["kind"] == "authority_published"), {})
    C.check(pub.get("pack") == "wink" and pub.get("version") == "0.2.0"
            and pub.get("entries") == ["pattern/destructive-confirm"],
            "flagship publication detail drifted: %s" % pub)

    # 6. why views
    stop = da_case.why_view(db, "pattern/destructive-confirm")
    C.check(stop and stop["provenance"].get("compiled_from") == ["prop/20261007-151914-9ff839"],
            "destructive-confirm provenance drifted")
    C.check(stop and stop["provenance"].get("gap") == "gap/20261007-145139-ad4b85",
            "destructive-confirm gap link drifted")
    revs = sorted((f["revision"], f["class"]) for f in (stop or {}).get("findings", []))
    C.check(revs == [("v1", "rectify"), ("v2", "rectify"), ("v3", "conforms")],
            "destructive-confirm findings drifted: %s" % revs)
    notice = da_case.why_view(db, "pattern/inline-notice")
    C.check(any(r["revision"].startswith("r2b") for r in (notice or {}).get("receipts", [])),
            "inline-notice lost the r2b receipt")
    C.check(any((f.get("obligation") or {}).get("state") == "closed"
                for f in (notice or {}).get("findings", [])),
            "inline-notice lost the closed obligation")

    # 7. provenance + vocabulary in golden threads
    bad_src = []
    threads = flagship + closure
    for e in threads:
        sf = e["source"]["file"]
        if not sf or not os.path.exists(os.path.join(ROOT, sf)) or not e["source"]["record"]:
            bad_src.append(e)
        if e["kind"] not in KINDS:
            bad_src.append(e)
    C.check(not bad_src, "events with missing source or unknown kind: %s" % bad_src[:3])

    # 8. determinism
    rc1, out1, _ = run_tool("--json", "list")
    rc2, out2, _ = run_tool("--json", "list")
    C.check(rc1 == 0 and rc2 == 0 and out1 == out2, "list output is not deterministic")
    rc3, out3, _ = run_tool("--json", "show", "gap/20261007-145139-ad4b85")
    rc4, out4, _ = run_tool("--json", "show", "gap/20261007-145139-ad4b85")
    C.check(rc3 == 0 and rc4 == 0 and out3 == out4, "show output is not deterministic")

    if C.failed:
        for label in C.failed:
            if label:
                print("FAIL %s" % label, file=sys.stderr)
        print("case model: %d passed, %d failed" % (C.passed, len(C.failed)))
        return 1
    print("case model: %d passed, 0 failed (corpus %d gaps / %d disputes / %d proposals / "
          "%d findings retrieved through one interface)" % (C.passed, len(rows),
          len(db["disputes"]), len(db["proposals"]), len(db["findings"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
