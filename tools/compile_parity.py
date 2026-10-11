#!/usr/bin/env python3
"""compile_parity — frozen regression fixtures for the unified compiler.

The baselines under docs/synthesis/data/parity/ were captured from the
pre-unification tools (compile_pack.py's hardcoded builders, and
apply_proposals.py's merge over the cadence workspaces). This runner
re-compiles everything through tools/da_compile.py and byte-compares, so any
behavioural drift the unification introduces fails loudly. Wired into
tools/check.sh.

    python3 tools/compile_parity.py [--verbose]

Exit 0 = parity holds; 1 = drift (details on stderr).
"""
import argparse
import difflib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import da_compile  # noqa: E402

REPO = da_compile.ROOT
BASE = os.path.join(REPO, "docs", "synthesis", "data", "parity")
SRCS = ("wink", "leader", "dominion")
WS = {"wink": "examples/cadence-wink",
      "leader": "examples/cadence-leader",
      "dominion": "examples/cadence-dominion"}


def _diff(path_a, path_b):
    """None if byte-identical, else a short human-readable explanation."""
    with open(path_a, "rb") as fh:
        a = fh.read()
    with open(path_b, "rb") as fh:
        b = fh.read()
    if a == b:
        return None
    detail = "bytes differ (%d vs %d)" % (len(a), len(b))
    try:
        d = list(difflib.unified_diff(a.decode().splitlines(),
                                      b.decode().splitlines(),
                                      "baseline", "compiled", lineterm="", n=1))
        detail += "\n" + "\n".join(d[:24])
    except UnicodeDecodeError:
        pass
    return detail


def _compare_dir(exp_dir, got_dir, label, fails, verbose):
    for f in sorted(os.listdir(exp_dir)):
        d = _diff(os.path.join(exp_dir, f), os.path.join(got_dir, f))
        if d:
            fails.append(("%s/%s" % (label, f), d))
        elif verbose:
            print("  ok %s/%s" % (label, f))


def check_compile(tmp, fails, verbose):
    for src in SRCS:
        out = os.path.join(tmp, "compile", src)
        da_compile.compile_synthesis(da_compile.dossier_path(src), out)
        _compare_dir(os.path.join(BASE, "compile-%s" % src), out,
                     "compile/%s" % src, fails, verbose)


def check_codify(tmp, fails, verbose):
    for src in SRCS:
        case = os.path.join(BASE, "codify-%s" % src)
        meta = json.load(open(os.path.join(case, "meta.json")))
        pack = os.path.join(tmp, "codify", src, "pack")
        da_compile.compile_synthesis(da_compile.dossier_path(src), pack)
        report = da_compile.codify(os.path.join(REPO, WS[src]), pack, now=meta["now"])
        if report != meta["report"]:
            fails.append(("codify/%s/report" % src,
                          "report differs:\n  expected %s\n  got      %s"
                          % (meta["report"], report)))
        _compare_dir(os.path.join(case, "expected"), pack,
                     "codify/%s" % src, fails, verbose)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="compile_parity")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    tmp = tempfile.mkdtemp(prefix="da-parity-")
    fails = []
    try:
        check_compile(tmp, fails, args.verbose)
        check_codify(tmp, fails, args.verbose)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if fails:
        for label, detail in fails:
            print("FAIL %s\n%s\n" % (label, detail), file=sys.stderr)
        print("compile parity: FAIL (%d case(s) diverged)" % len(fails))
        return 1
    print("compile parity: OK (compile %d/%d sources · codify %d/%d workspaces)"
          % (len(SRCS), len(SRCS), len(SRCS), len(SRCS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
