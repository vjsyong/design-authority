#!/usr/bin/env python3
"""Build a benchmark run workspace (materials per condition).

    python3 benchmark/harness/materials.py --condition B --dest DIR
    python3 benchmark/harness/materials.py --condition C --dest DIR

Layout produced (condition-dependent parts marked):

    DIR/
      app.py, templates/, static/, data/, run.sh, README.md   (starter copy)
      design/{tokens,core,fonts,icons,examples}               (B + C)
      design-docs/                                            (B only, rendered kit)
      DESIGN.md                                               (C only)
      .bench/materials.json                                   (manifest + hashes)
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
STARTER = os.path.join(ROOT, "benchmark", "starter")
SNAPSHOT = os.path.expanduser("~/triage-design-system-demo")
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "kernel"))

VENDOR = ["tokens", "core", "fonts", "icons", "examples"]


def run(cmd, cwd=None, check=True):
    return subprocess.run(cmd, cwd=cwd, check=check, text=True,
                          capture_output=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_starter(dest):
    shutil.copytree(STARTER, dest,
                    ignore=shutil.ignore_patterns("data", "__pycache__", "*.pyc"))


def vendor_design(dest):
    design = os.path.join(dest, "design")
    os.makedirs(design, exist_ok=True)
    for sub in VENDOR:
        src = os.path.join(SNAPSHOT, sub)
        if not os.path.isdir(src):
            raise SystemExit("snapshot subdir missing: %s" % src)
        shutil.copytree(src, os.path.join(design, sub))


def build(condition, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    copy_starter(dest)
    manifest = {"condition": condition, "starter": STARTER, "snapshot": SNAPSHOT,
                "files": {}}
    if condition in ("B", "C"):
        vendor_design(dest)
    if condition == "B":
        from render_kit_triage import render
        from design_authority.pack import Pack
        out = os.path.join(dest, "design-docs")
        result = render(Pack(os.path.join(ROOT, "packs", "triage")), out)
        manifest["kit"] = result
    if condition == "C":
        shutil.copy(os.path.join(ROOT, "benchmark", "materials", "DESIGN.md"),
                    os.path.join(dest, "DESIGN.md"))
    # git init so runs are diffable
    run(["git", "init", "-q"], cwd=dest)
    run(["git", "add", "-A"], cwd=dest)
    run(["git", "-c", "user.name=bench", "-c", "user.email=bench@local",
         "commit", "-qm", "starter + materials (%s)" % condition], cwd=dest)
    starter_sha = run(["git", "rev-parse", "HEAD"], cwd=dest).stdout.strip()
    manifest["starter_commit"] = starter_sha
    for rel in ("app.py", "templates/base.html", "static/app.css"):
        manifest["files"][rel] = sha256(os.path.join(dest, rel))
    return manifest


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", required=True, choices=["A", "B", "C"])
    ap.add_argument("--dest", required=True)
    args = ap.parse_args(argv)
    m = build(args.condition, os.path.abspath(args.dest))
    print("built %s workspace at %s (starter commit %s)"
          % (m["condition"], args.dest, m["starter_commit"][:10]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
