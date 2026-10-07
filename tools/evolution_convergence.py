#!/usr/bin/env python3
"""Authority-evolution convergence battery (Phase 5).

Asserts the review-verified contract of the 0.13.0-experiment pack against the
recorded 0.12.1 baseline (docs/evolution/data/baseline-resolves-0.12.1.json):
  G-01: 7 -> component/select, 1 -> recipe/assign-picker, zero pattern/detail
  G-02: 5 -> recipe/job-progress, 2 -> component/progress
  G-03: 4 -> recipe/high-stakes-confirm
  regression battery: identical to the 0.12.1 outcomes
  delete probes: all -> recipe/entity-delete-armed

Usage: python3 tools/evolution_convergence.py [--pack packs/triage-evolution]
Exit 0 = all hard assertions hold.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "kernel"))

from design_authority.pack import Pack          # noqa: E402
from design_authority.resolve import resolve    # noqa: E402

G01 = [
    ("A compact picker to assign one reviewer (a person) from a fixed list on a record page", "RESOLVED", "component/select"),
    ("A compact picker for assigning a reviewer to a request (choose one of a small fixed set of reviewers and submit)", "RESOLVED", "component/select"),
    ("A compact picker for assigning a reviewer to a request from a small fixed list, inline in a detail page", "RESOLVED", "component/select"),
    ("A compact picker for assigning a reviewer to a request from the request detail page", "COMPOSE", "recipe/assign-picker"),
    ("Choose one owner from a list of people", "COMPOSE", "recipe/assign-picker"),
    ("Single select from a short fixed set of options", "RESOLVED", "component/select"),
    ("Entity picker for assigning a record to a person", "RESOLVED", "component/select"),
    ("Assign a reviewer to a request", "RESOLVED", "component/select"),
]

G02 = [
    ("Show the status and progress of a long-running background operation (running with percent complete, potentially stalled/stuck, or failed) and let the user re-run it", "COMPOSE", "recipe/job-progress"),
    ("A determinate long-running background-operation status: show how far an AI triage scan has come and whether it is stuck or failed, with a live progress readout", "RESOLVED", "component/progress"),
    ("Show the status and determinate progress of a long-running background triage scan, including running / done / failed and a stalled indication, with live updates", "COMPOSE", "recipe/job-progress"),
    ("Determinate progress for a long-running background job", "COMPOSE", "recipe/job-progress"),
    ("Progress bar showing percent complete with a stalled state", "RESOLVED", "component/progress"),
    ("Background job status card with progress", "COMPOSE", "recipe/job-progress"),
    ("Show how far a background scan has come and whether it is stuck", "COMPOSE", "recipe/job-progress"),
]

G03 = [
    ("An irreversible approval decision that requires a typed reason at the point of action (reject a purchase request with a reason the requester sees)", "COMPOSE", "recipe/high-stakes-confirm"),
    ("One-way decision with a reason field and a confirmation", "COMPOSE", "recipe/high-stakes-confirm"),
    ("Rejecting a request requires typing a reason", "COMPOSE", "recipe/high-stakes-confirm"),
    ("High stakes confirmation with a required reason", "COMPOSE", "recipe/high-stakes-confirm"),
]

REGRESSION = [
    ("combobox", "RESOLVED", "component/cb"),
    ("date picker", "RESOLVED", "component/dp"),
    ("loading spinner", "RESOLVED", "component/spinner"),
    ("toast message", "RESOLVED", "component/toast2"),
    ("empty state with a call to action", "RESOLVED", "component/empty"),
    ("banner after redirect", "COMPOSE", "recipe/feedback-redirect"),
    ("delete a rule from a list", "COMPOSE", "recipe/entity-delete-armed"),
    ("pagination for a long list", "COMPOSE", "recipe/paginated-list"),
]

DELETE_PROBES = [
    "remove a reviewer from a list",
    "remove a person from a list",
    "delete a person from a list",
    "remove an owner from a list",
    "delete an entity from a list",
]

# Hard-locked re-tests of cases whose semantics must survive the evolution:
#   - 'searchable picker' phrases stay with component/cb (frozen-golden semantic)
#   - the 0.12.1 golden that expected UNDEFINED for a progress bar now resolves
# watch items are informational (no assertion) — terse phrasing 'remove a
# reviewer' was UNDEFINED on 0.12.1 too (not a regression).
WATCH = [
    ("remove a reviewer", None, None),
]


def rid(result):
    res = result.get("resolution") or {}
    for key in ("artifact", "recipe", "fallback", "prohibition"):
        if isinstance(res.get(key), dict) and res[key].get("id"):
            return res[key]["id"]
    return None


def run(pack, cases, group, report, hard=True):
    ok = bad = 0
    for problem, exp_outcome, exp_id in cases:
        r = resolve(pack, problem)
        got_outcome, got_id = r.get("outcome"), rid(r)
        good = got_outcome == exp_outcome and (exp_id is None or got_id == exp_id)
        if good:
            ok += 1
        else:
            bad += 1
        flag = "ok  " if good else ("FAIL" if hard else "warn")
        print("  %s [%s] %-24s %-28s << %s" % (flag, group, got_outcome, got_id or "", problem[:64]))
        report.append({"group": group, "problem": problem, "outcome": got_outcome,
                       "id": got_id, "expected": [exp_outcome, exp_id], "ok": good, "hard": hard})
    return ok, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", default="packs/triage-evolution")
    args = ap.parse_args()
    pack = Pack(os.path.join(ROOT, args.pack))
    print("pack:", pack.identity().get("version"), os.path.join(ROOT, args.pack))
    report = []
    ok1, bad1 = run(pack, G01, "G-01", report)
    ok2, bad2 = run(pack, G02, "G-02", report)
    ok3, bad3 = run(pack, G03, "G-03", report)
    ok4, bad4 = run(pack, REGRESSION, "regr", report)
    ok5, bad5 = run(pack, [(q, "COMPOSE", "recipe/entity-delete-armed") for q in DELETE_PROBES], "del", report)
    ok6, bad6 = run(pack, [
        ("assign a reviewer with a searchable picker", "RESOLVED", "component/cb"),
        ("add a progress bar for a long-running background job", "RESOLVED", "component/progress"),
    ], "lock", report)
    ok7, bad7 = run(pack, WATCH, "watch", report, hard=False)

    total_ok, total_bad = ok1 + ok2 + ok3 + ok4 + ok5 + ok6, bad1 + bad2 + bad3 + bad4 + bad5 + bad6
    print()
    print("hard assertions: %d ok, %d failed (G-01 %d/%d, G-02 %d/%d, G-03 %d/%d, regression %d/%d, delete %d/%d, lock %d/%d)"
          % (total_ok, total_bad, ok1, len(G01), ok2, len(G02), ok3, len(G03), ok4, len(REGRESSION), ok5, len(DELETE_PROBES), ok6, 2))
    out = os.path.join(ROOT, "docs", "evolution", "data", "evolution-resolves-0.13.json")
    json.dump({"pack": args.pack, "report": report}, open(out, "w"), indent=1)
    print("saved ->", out)
    if total_bad:
        print("CONVERGENCE FAILURES — see FAIL rows above")
        return 1
    print("CONVERGENCE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
