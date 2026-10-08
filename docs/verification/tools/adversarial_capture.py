#!/usr/bin/env python3
"""adversarial_capture — ground-truth capture for the adversarial round.

Runs AFTER the blind verification pass: diffs each clean build against its
hacked copy (to diff-<p>.txt) + records post-attack hashes. The orchestrator
reads the diffs only now, then adjudicates with the attack logs.
"""
import hashlib
import os
import subprocess

REPO = "/home/xrim/design-authority"
A = os.path.join(REPO, "docs", "verification", "adversarial")


def sha(p):
    h = hashlib.sha256()
    h.update(open(p, "rb").read())
    return h.hexdigest()


for p in ("wink", "leader", "dominion"):
    clean = os.path.join(REPO, "examples", f"cadence3-{p}")
    hacked = os.path.join(A, f"hacked-{p}")
    out = os.path.join(A, f"diff-{p}.txt")
    r = subprocess.run(["diff", "-ruN", clean, hacked], capture_output=True, text=True)
    open(out, "w").write(r.stdout)
    print(f"{p}: diff -> {os.path.relpath(out, REPO)} ({len(r.stdout.splitlines())} lines)")

# post-attack hash snapshot
lines = []
for root, dirs, files in os.walk(A):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for f in sorted(files):
        fp = os.path.join(root, f)
        lines.append(f"{sha(fp)}  {os.path.relpath(fp, REPO)}")
open(os.path.join(A, "copies.postattack.sha256"), "w").write("\n".join(lines) + "\n")
print(f"post-attack hashes: {len(lines)} files")
