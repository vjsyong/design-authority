#!/usr/bin/env python3
"""x05 schedule generator — freeze the run plan (17 sessions).

Produces schedule.json in the run area: ids, order, budgets, brief hashes,
the recorded seed, model pin, and the instrument manifest. The interleave
order within each handoff index is fixed by the recorded seed; the next index
starts only after all three chains of the previous index are complete.

    x05_schedule.py generate [--root X05_ROOT] [--seed HEX]
"""
import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x05_common import (DEFAULT_MODEL, TOKEN_BUDGET, WALL_BUDGET_S,  # noqa: E402
                        X05_ROOT, hash_tree, now_iso, sha256_file,
                        write_json_atomic)

CHAIN_CONDS = ["a", "b", "c"]


def seeded_order(seed, idx):
    return sorted(CHAIN_CONDS,
                  key=lambda c: hashlib.sha256(
                      ("%s|%d|%s" % (seed, idx, c)).encode()).hexdigest())


def build(root, seed=None):
    mats = os.path.join(root, "materials")
    if not os.path.exists(os.path.join(mats, "manifest.json")):
        raise SystemExit("materials not staged; run x05_materials.py stage first")
    seed = seed or hashlib.sha256(os.urandom(32)).hexdigest()[:16]

    def sess(sid, step, kind, **kw):
        s = {"id": sid, "step": step, "kind": kind, "model": DEFAULT_MODEL,
             "budget_wall": WALL_BUDGET_S, "budget_tokens": TOKEN_BUDGET}
        s.update(kw)
        return s

    sessions = [
        sess("f1", 0, "formation", input_mode="starter", brief="f1.md",
             protocol=True, wrapper=True, da_tools=True, pack="base", prev=None),
        sess("f2", 1, "formation", input_mode="seal", brief="f2.md",
             protocol=True, wrapper=True, da_tools=True, pack="base", prev="f1"),
        sess("f3", 2, "formation", input_mode="seal", brief="f3.md",
             protocol=True, wrapper=True, da_tools=True, pack="base", prev="f2"),
        sess("cen", 3, "census", input_mode="seal", brief="cen.md", prev="f3",
             protocol=False, wrapper=False, da_tools=False, pack=None,
             reference_extra=["rubrics/census-rubric.md"],
             extra_files=[
                 {"src": "run/f3/extraction/inventory.json",
                  "dst": "extraction/inventory.json"},
                 {"src": "run/f3/extraction/roles.json",
                  "dst": "extraction/roles.json"},
                 {"src": "run/f3/extraction/evidence.md",
                  "dst": "extraction/evidence.md"}]),
        sess("cod", 4, "cod", input_mode="seal", brief="cod.md", prev="f3",
             protocol=False, wrapper=False, da_tools=True, pack=None,
             reference_extra=["spec/02-pack-format.md",
                              "spec/03-resolution-semantics.md",
                              "spec/05-governance-and-freeze.md",
                              "rubrics/census-rubric.md"],
             extra_files=[
                 {"src": "run/cen/extraction/census.json",
                  "dst": "census/census.json"},
                 {"src": "run/cen/extraction/exemplars.json",
                  "dst": "census/exemplars.json"}]),
    ]
    step = 5
    chain_prev = {c: "f3" for c in CHAIN_CONDS}
    for idx in range(1, 5):
        for cond in seeded_order(seed, idx):
            sid = "h%d%s" % (idx, cond)
            entry = sess(sid, step, "handoff", input_mode="seal",
                         condition=cond.upper(), chain=[idx, cond], k=idx,
                         brief="h%d.md" % idx, prev=chain_prev[cond],
                         protocol=cond in ("b", "c"),
                         wrapper=cond in ("b", "c"),
                         da_tools=cond in ("b", "c"),
                         pack={"c": "canon", "b": "base"}.get(cond))
            sessions.append(entry)
            chain_prev[cond] = sid
            step += 1

    brief_hashes = {}
    for s in sessions:
        p = os.path.join(mats, "briefs", s["brief"])
        brief_hashes[s["id"]] = {"file": s["brief"],
                                 "sha256": sha256_file(p)}
    instrument = {}
    for rel in ["starter", "wrapper", "packs/base", "rubrics", "fixtures"]:
        instrument[rel] = hash_tree(os.path.join(mats, rel))

    schedule = {
        "program": "x05", "created": now_iso(), "model": DEFAULT_MODEL,
        "seed": seed,
        "budgets": {"wall_s": WALL_BUDGET_S, "tokens": TOKEN_BUDGET},
        "brief_hashes": brief_hashes,
        "instrument_hashes": {k: {"files": len(v)} for k, v in instrument.items()},
        "materials_manifest": os.path.join(mats, "manifest.json"),
        "sessions": sessions,
        "order": [s["id"] for s in sessions],
        "index_order": {str(i): seeded_order(seed, i) for i in range(1, 5)},
    }
    return schedule


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["generate"])
    ap.add_argument("--root", default=X05_ROOT)
    ap.add_argument("--seed", default=None)
    args = ap.parse_args(argv)
    sched = build(args.root, args.seed)
    out = os.path.join(args.root, "schedule.json")
    if os.path.exists(out):
        raise SystemExit("schedule.json already exists (frozen): %s" % out)
    write_json_atomic(out, sched)
    print("schedule frozen: %d sessions, seed=%s" % (len(sched["sessions"]),
                                                     sched["seed"]))
    print("order: " + " ".join(sched["order"]))
    print("index order: %s" % json.dumps(sched["index_order"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
