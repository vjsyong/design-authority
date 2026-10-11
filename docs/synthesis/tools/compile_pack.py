#!/usr/bin/env python3
"""compile_pack — synthesis compiler entry point (thin adapter).

As of the P0.1 unification this file is a shim over the single
decision-to-authority compiler, `tools/da_compile.py`. The Wink/Leader/
Dominion definitions that used to live here as hardcoded builders are
reviewed data now: `docs/synthesis/<src>/compile.json` (the approved
decision ledger + the records those decisions emit). See
`docs/13-simplification.md`.

Usage:  python3 docs/synthesis/tools/compile_pack.py [--src wink|leader|dominion|all] [--out DIR]
Output: authorities/<src>/ (or DIR/<src> with --out)
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import da_compile  # noqa: E402


def main():
    ap = argparse.ArgumentParser(prog="compile_pack")
    ap.add_argument("--src", default="all", choices=list(da_compile.SRCS) + ["all"])
    ap.add_argument("--out", default=None, help="output base dir (single source only)")
    args = ap.parse_args()
    srcs = list(da_compile.SRCS) if args.src == "all" else [args.src]
    if args.out and len(srcs) > 1:
        ap.error("--out requires a single --src")
    return da_compile.run_synthesis(srcs, args.out)


if __name__ == "__main__":
    sys.exit(main())
