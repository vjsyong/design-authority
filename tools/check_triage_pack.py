#!/usr/bin/env python3
"""check_triage_pack — fail if packs/triage drifts from its generator output.

The live triage pack is built by docs/synthesis/triage/tools/build_triage_pack.py
(sources: ~/triage-design-system; nothing hand-edited in the generated files).
This gate rebuilds the pack into a temp dir and diffs every generated file
against the committed one. BUILD.json is excluded: it carries a built_at
timestamp by design.

The older kit builder (tools/build_pack_triage.py, snapshot + curation) remains
in the repo for the evolution packs (--out packs/triage-evolution etc.).
"""
import filecmp
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(ROOT, "docs", "synthesis", "triage", "tools", "build_triage_pack.py")
PACK = os.path.join(ROOT, "packs", "triage")

FILES = ["authority.json", "scoring.json", "artifacts.json", "rules.json",
         "prohibitions.json", "fallbacks.json", "precedents.json",
         "candidates.json", "recipes.json", "golden.json"]


def main():
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run([sys.executable, GEN, "--out", td],
                           stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if r.returncode != 0:
            print("ERROR: generator failed: %s" % (r.stderr or "").strip()[:300])
            return 1
        drifted = []
        for f in FILES:
            fresh, committed = os.path.join(td, f), os.path.join(PACK, f)
            if not os.path.exists(fresh):
                drifted.append(f + " (not generated)")
            elif not os.path.exists(committed):
                drifted.append(f + " (missing in pack)")
            elif not filecmp.cmp(fresh, committed, shallow=False):
                drifted.append(f)
    if drifted:
        print("ERROR: triage pack drift: %s" % ", ".join(drifted))
        print("rerun: python3 docs/synthesis/triage/tools/build_triage_pack.py")
        return 1
    print("triage pack in sync with the synthesis generator (%d files)" % len(FILES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
