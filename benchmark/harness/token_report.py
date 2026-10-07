#!/usr/bin/env python3
"""Token economics across benchmark runs.

Reads `benchmark/runs/<id>/transcript.jsonl` (opencode `step_finish` usage
events) or the recorded `run.json` → `opencode.tokens` block when present
(runs after 2026-10-07), and prints per-run aggregates plus per-group medians.
Writes nothing.

Usage:
  python3 benchmark/harness/token_report.py              # every run with a transcript
  python3 benchmark/harness/token_report.py a3 b2 c3 e1  # specific runs

Groups are formed by run-id prefix (a = naive, b = static kit, c = authority,
e = evolution pack, others as-is); medians print per group, with run counts.

Baseline record and interpretation: docs/token-economics.md.
"""
import json
import os
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS_DIR = os.path.normpath(os.path.join(HERE, "..", "runs"))


def token_stats(transcript_path):
    """Same aggregation as run_condition.token_stats (kept local: analysis tool
    must run standalone)."""
    out = {"steps": 0, "total": 0, "input": 0, "output": 0, "reasoning": 0,
           "cache_read": 0, "cache_write": 0, "peak": 0, "cost": 0.0}
    if not os.path.exists(transcript_path):
        return out
    with open(transcript_path) as fh:
        for line in fh:
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") != "step_finish":
                continue
            part = ev.get("part") or {}
            t = part.get("tokens") or {}
            out["steps"] += 1
            out["input"] += t.get("input", 0)
            out["output"] += t.get("output", 0)
            out["reasoning"] += t.get("reasoning", 0)
            out["cache_read"] += (t.get("cache") or {}).get("read", 0)
            out["cache_write"] += (t.get("cache") or {}).get("write", 0)
            tot = t.get("total", 0)
            out["total"] += tot
            out["peak"] = max(out["peak"], tot)
            out["cost"] = round(out["cost"] + (part.get("cost") or 0.0), 6)
    return out


def for_run(run_id):
    run_path = os.path.join(RUNS_DIR, run_id, "run.json")
    if os.path.exists(run_path):
        try:
            rec = (json.load(open(run_path)).get("opencode") or {}).get("tokens")
            if rec and rec.get("steps"):
                return rec
        except ValueError:
            pass
    return token_stats(os.path.join(RUNS_DIR, run_id, "transcript.jsonl"))


def group_of(run_id):
    return run_id[0] if run_id and run_id[0].isalpha() else "?"


def main():
    args = sys.argv[1:]
    if args:
        runs = args
    else:
        runs = sorted(d for d in os.listdir(RUNS_DIR)
                      if os.path.exists(os.path.join(RUNS_DIR, d, "transcript.jsonl"))
                      and not d.endswith("-broken-pilot"))
    groups = {}
    print(f"{'run':16s} {'steps':>5s} {'sum_total':>12s} {'sum_input':>10s} {'cache_read':>12s} "
          f"{'output':>8s} {'reason':>8s} {'peak':>9s} {'cost_usd':>9s}")
    for r in runs:
        t = for_run(r)
        if not t["steps"]:
            print(f"{r:16s}   (no usage data)")
            continue
        groups.setdefault(group_of(r), []).append(t)
        print(f"{r:16s} {t['steps']:5d} {t['total']:12,d} {t['input']:10,d} {t['cache_read']:12,d} "
              f"{t['output']:8,d} {t['reasoning']:8,d} {t['peak']:9,d} {t['cost']:9.4f}")
    if groups:
        print()
        print("group medians:")
        for g, ts in sorted(groups.items()):
            med = lambda k: st.median([t[k] for t in ts])  # noqa: E731
            print(f"  {g} (n={len(ts)}): sum_total={med('total'):,.0f}  cost=${med('cost'):.4f}  "
                  f"peak={med('peak'):,.0f}  output+reasoning={med('output') + med('reasoning'):,.0f}  "
                  f"tok/step={med('total') / med('steps'):,.0f}")
    print()
    print("note: sum_total counts cumulative context (incl. cache reads) across steps; "
          "cost is the provider-billed figure. See docs/token-economics.md.")


if __name__ == "__main__":
    main()
