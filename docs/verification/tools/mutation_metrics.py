#!/usr/bin/env python3
"""mutation_metrics — TP/FP/FN against the sealed ground truth.

Opened ONLY after all blind verifier runs completed. Prints the detection
table and writes mutations/metrics.json.
"""
import json
import os

REPO = "/home/xrim/design-authority"
V = os.path.join(REPO, "docs", "verification")
manifest = json.load(open(os.path.join(V, "mutations", "manifest.sealed.json")))

report = {}

for build in ("wink", "leader", "dominion"):
    mut = json.load(open(os.path.join(V, "raw", f"mutant-{build}", "raw.json")))
    clean = json.load(open(os.path.join(V, "raw", f"{build}-clean", "raw.json")))
    mut_v = {c["id"] for c in mut["checks"] if c["status"] == "VIOLATION"}
    clean_v = {c["id"] for c in clean["checks"] if c["status"] == "VIOLATION"}

    rows = {"tp": [], "fn": [], "control_ok": [], "control_bad": [], "unexpected": []}
    expected = set()
    for m in manifest["mutations"]:
        if m["build"] != build:
            continue
        exp = m["expected_check"]
        if m["kind"] == "violation" and exp:
            expected.add(exp)
            if exp in mut_v:
                rows["tp"].append((m["id"], exp))
            else:
                rows["fn"].append((m["id"], exp, "expected check not flagged"))
        elif m["kind"] == "control-pass" and exp:
            expected.add(exp)
            ok = exp not in mut_v
            (rows["control_ok"] if ok else rows["control_bad"]).append((m["id"], exp))
    # violations not attributable to any seeded expectation
    rows["unexpected"] = sorted(mut_v - expected)
    # clean-build re-check: anything flagged on clean? (should be empty)
    rows["clean_violations"] = sorted(clean_v)
    report[build] = rows
    print(f"== {build}: TP {len(rows['tp'])} / expected {len(rows['tp']) + len(rows['fn'])}"
          f" | FN {len(rows['fn'])} | controls ok {len(rows['control_ok'])} | unexpected {rows['unexpected']}")
    for mid, cid in rows["tp"]:
        print(f"   TP  {mid:6s} -> {cid}")
    for mid, cid, why in rows["fn"]:
        print(f"   FN  {mid:6s} -> {cid} ({why})")
    for cid in rows["unexpected"]:
        print(f"   EXTRA flag: {cid}")

tu = sum(len(report[b]["tp"]) for b in report)
fu = sum(len(report[b]["fn"]) for b in report)
print(f"\nTOTAL: TP {tu} / (TP+FN) {tu + fu} — recall {tu/(tu+fu)*100:.0f}% "
      f"(designed miss excluded below)")
for b in report:
    for mid, cid, why in report[b]["fn"]:
        if mid == "L-V5":
            use = sum(len(report[x]["tp"]) for x in report)
            tot = use + fu - 1
            print(f"  (excluding designed miss L-V5: recall {use/tot*100:.0f}%)")

with open(os.path.join(V, "mutations", "metrics.json"), "w") as fh:
    json.dump(report, fh, indent=1, ensure_ascii=False)
print("wrote mutations/metrics.json")
