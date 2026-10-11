#!/usr/bin/env python3
"""P4b schedule — freeze the three-arm run plan (docs/experiments/11).

    python3 docs/experiments/tools/p4_schedule.py [--root ~/p4-maint]

3 seeds x 3 arms x 5 sessions = 45 sessions:
  arms   a = static contract            (no enforcement, no record)
         b = static + enforcement       (check-design mandatory at handoff end)
         c = full Design Authority      (protocol + wrapper + pack + reconcile)
  seeds  r1..r3 (one replication each; r1 is the blind-reviewed one)
  k      1..4 handoffs; h5 = the remediation session (validator repair task,
         identical interface for every arm)

Change k is introduced AFTER handoff k, so session h<k> runs with pack
p4-da-<k-1>; c sessions additionally receive reference/MIGRATION.md produced
by the conductor's reconcile pass over the previous c session.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p4_common import (DEFAULT_MODEL, MATS, P4_ROOT, TOKEN_BUDGET,  # noqa: E402
                       WALL_BUDGET_S, now_iso, sha256_file, write_json_atomic)

REPS = [("r1", 1101), ("r2", 2202), ("r3", 3303)]
ARMS = ("a", "b", "c")


def arm_fields(arm, k, kind):
    e = {}
    if arm == "c":
        e.update({"protocol": True, "wrapper": True, "da_tools": True,
                  "pack_k": k - 1})
    elif arm == "b":
        e.update({"protocol": False, "wrapper": False, "da_tools": True,
                  "pack_k": k - 1})
    else:
        e.update({"protocol": False, "wrapper": False, "da_tools": False,
                  "pack_k": None})
    if kind == "remediation":
        # the repair task is identical across arms: the validator + latest pack
        e.update({"da_tools": True, "pack_k": 4})
    return e


def build(root):
    sessions = []
    for rep, seed in REPS:
        for k in range(1, 5):
            for arm in ARMS:
                sid = "%s-%s-h%d" % (rep, arm, k)
                entry = {
                    "id": sid, "rep": rep, "rep_seed": seed, "arm": arm,
                    "condition": arm, "k": k, "kind": "handoff",
                    "input_mode": "seal",
                    "prev": ("seed" if k == 1 else "%s-%s-h%d" % (rep, arm, k - 1)),
                    "brief": "h%d.md" % k,
                    "model": DEFAULT_MODEL,
                    "budget_wall": WALL_BUDGET_S,
                    "budget_tokens": TOKEN_BUDGET,
                }
                entry.update(arm_fields(arm, k, "handoff"))
                sessions.append(entry)
        for arm in ARMS:
            sid = "%s-%s-h5" % (rep, arm)
            entry = {
                "id": sid, "rep": rep, "rep_seed": seed, "arm": arm,
                "condition": arm, "k": 5, "kind": "remediation",
                "input_mode": "seal", "prev": "%s-%s-h4" % (rep, arm),
                "brief": "h5.md",
                "model": DEFAULT_MODEL,
                "budget_wall": WALL_BUDGET_S,
                "budget_tokens": TOKEN_BUDGET,
            }
            entry.update(arm_fields(arm, 5, "remediation"))
            sessions.append(entry)

    order = [s["id"] for s in sessions]
    brief_hashes = {}
    for k in range(1, 6):
        p = os.path.join(MATS, "briefs", "h%d.md" % k)
        brief_hashes["h%d.md" % k] = sha256_file(p)
    schedule = {
        "program": "p4b three-arm: static vs enforced vs governed (docs/experiments/11)",
        "created": now_iso(),
        "model": DEFAULT_MODEL,
        "seed": "seal/seed",
        "reps": [{"id": r, "seed": s} for r, s in REPS],
        "budgets": {"wall_s": WALL_BUDGET_S, "tokens": TOKEN_BUDGET},
        "brief_hashes": brief_hashes,
        "sessions": sessions,
        "order": order,
    }
    write_json_atomic(os.path.join(root, "schedule.json"), schedule)
    print("schedule.json written: %d sessions (%d reps x %d arms x 5)"
          % (len(sessions), len(REPS), len(ARMS)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=P4_ROOT)
    args = ap.parse_args()
    build(os.path.abspath(os.path.expanduser(args.root)))


if __name__ == "__main__":
    main()
