#!/usr/bin/env python3
"""P4 schedule — freeze the run plan (2 chains x 4 handoffs, k-wise interleave).

    python3 docs/experiments/tools/p4_schedule.py [--root ~/p4-maint]

Writes schedule.json: ids, order, budgets, brief hashes, condition fields
(da = protocol + wrapper + frozen tooling + pack k-1; base = relnotes +
design-doc, no machine records). Change k is introduced AFTER handoff k, so
session h<k> runs with pack p4-da-<k-1> and sees the reconcile migration from
handoff k-1 as reference/MIGRATION.md.
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p4_common import (DEFAULT_MODEL, MATS, P4_ROOT, TOKEN_BUDGET,  # noqa: E402
                       WALL_BUDGET_S, now_iso, sha256_file, write_json_atomic)


def build(root):
    sessions = []
    for k in range(1, 5):
        for chain in ("da", "base"):
            sid = "%s-h%d" % (chain, k)
            entry = {
                "id": sid,
                "chain": chain,
                "k": k,
                "kind": "handoff",
                "condition": chain,
                "input_mode": "seal",
                "prev": ("seed" if k == 1 else "%s-h%d" % (chain, k - 1)),
                "brief": "h%d.md" % k,
                "model": DEFAULT_MODEL,
                "budget_wall": WALL_BUDGET_S,
                "budget_tokens": TOKEN_BUDGET,
            }
            if chain == "da":
                entry.update({"protocol": True, "wrapper": True, "da_tools": True,
                              "pack_k": k - 1})
            else:
                entry.update({"protocol": False, "wrapper": False, "da_tools": False,
                              "pack_k": None})
            sessions.append(entry)
    order = [s["id"] for s in sessions]
    brief_hashes = {}
    for k in range(1, 5):
        p = os.path.join(MATS, "briefs", "h%d.md" % k)
        brief_hashes["h%d.md" % k] = sha256_file(p)
    schedule = {
        "program": "p4 maintenance economics (docs/experiments/09)",
        "created": now_iso(),
        "model": DEFAULT_MODEL,
        "seed": "seal/seed",
        "budgets": {"wall_s": WALL_BUDGET_S, "tokens": TOKEN_BUDGET},
        "brief_hashes": brief_hashes,
        "sessions": sessions,
        "order": order,
    }
    write_json_atomic(os.path.join(root, "schedule.json"), schedule)
    print("schedule.json written: %d sessions (%s)" % (len(sessions), ", ".join(order)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=P4_ROOT)
    args = ap.parse_args()
    build(os.path.abspath(os.path.expanduser(args.root)))


if __name__ == "__main__":
    main()
