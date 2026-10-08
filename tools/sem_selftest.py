#!/usr/bin/env python3
"""Semantic layer self-test (optional extras: fastembed, numpy).

Builds a throwaway index, answers known asks, checks fusion and staleness.
Skips with exit 0 when the extras are not installed. Wired into check.sh.

    .venv/bin/python3 tools/sem_selftest.py
"""
import os
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "kernel"))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import da_sem  # noqa: E402

PACK = os.path.join(ROOT, "packs", "triage")
fails = []


def ck(name, ok, detail=""):
    print(("%s %s%s" % ("ok " if ok else "FAIL", name,
                        ("  (%s)" % detail) if detail else "")))
    if not ok:
        fails.append(name)


def main():
    if not da_sem._deps():
        print("skip: semantic extras not installed (pip install fastembed numpy)")
        return 0
    with tempfile.TemporaryDirectory() as td:
        idx = os.path.join(td, "selftest.sqlite")
        t0 = time.time()
        info = da_sem.build_index(PACK, idx, quiet=True)
        build_s = time.time() - t0
        ck("build completes", True, "%.1fs (%.2f MB)" % (build_s, info["size_mb"]))
        ck("build under 120s", build_s < 120)
        ck("index under 30 MB", info["size_mb"] < 30)
        ck("docs indexed", info["docs"] > 50, str(info["docs"]))

        q = da_sem.query_index(idx, "a skeleton loader", k=3)
        ck("known positive in top-3", any(c["id"] == "component/skeleton"
                                          for c in q["candidates"]),
           ",".join(c["id"] for c in q["candidates"]))
        ck("canonical class filter holds",
           all(c["class"] == "canonical" for c in q["candidates"]))
        q2 = da_sem.query_index(idx, "a primary button", k=3)
        ck("primary button in top-3", any(c["id"] == "component/btn"
                                          for c in q2["candidates"]),
           ",".join(c["id"] for c in q2["candidates"]))
        q3 = da_sem.query_index(idx, "status light", k=5, cls="history")
        ck("history class queries separately", isinstance(q3["candidates"], list))

        fused = da_sem.rrf_fuse(["a", "b"], ["b", "a"])
        ck("rrf tie-breaks by id order", [k for k, _ in fused] == ["a", "b"])

        st = da_sem.stale_index(idx)
        ck("fresh index not stale", st["stale"] is False)

    if fails:
        print("semantic self-test: FAILED: %s" % ", ".join(fails))
        return 1
    print("semantic self-test: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
