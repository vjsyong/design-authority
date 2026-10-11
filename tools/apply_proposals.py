#!/usr/bin/env python3
"""apply_proposals — proposal codification entry point (thin adapter).

As of the P0.1 unification this is a shim over the single decision-to-authority
compiler, `tools/da_compile.py` (codify mode). The hardcoded editorial
summaries that used to live in this file are part of the review record now:
`review.codified_summary` on the accepted proposal. See
`docs/13-simplification.md`.

Reads <workspace>/.design-authority/proposals/*.json where status == "accepted"
and merges each proposal's `proposed` entry into the pack's artifacts.json, its
tests.golden cases into the pack golden set, and bumps the pack version.
Idempotent (skips artifact ids already present); non-accepted proposals are
never touched. Rejected proposals are NOT codified — they become precedents
(see precedents.json).

    python3 tools/apply_proposals.py --workspace examples/cadence-wink --pack authorities/wink
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import da_compile  # noqa: E402


def main():
    ap = argparse.ArgumentParser(prog="apply_proposals.py")
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--pack", required=True)
    args = ap.parse_args()
    return da_compile.run_codify(args.workspace, args.pack)


if __name__ == "__main__":
    sys.exit(main())
