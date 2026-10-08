#!/usr/bin/env python3
"""Recompute and compare the sha256 hashes in a built site's archive manifest.

    python3 tools/verify_build_manifest.py <site-dir>   # exit 1 on any mismatch

Used by CI (per-authority and meta) and locally after any manual edit.
Files listed in archive-manifest.json are re-hashed in place; missing or
mismatched files fail. The manifest itself and download bundles are excluded
by construction (the archive tool never lists them).
"""
import hashlib
import json
import os
import sys


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    d = sys.argv[1]
    mp = os.path.join(d, "archive-manifest.json")
    if not os.path.isfile(mp):
        print("no archive-manifest.json in %s" % d)
        sys.exit(2)
    manifest = json.load(open(mp))
    bad, missing = [], []
    for f in manifest["files"]:
        p = os.path.join(d, f["path"])
        if not os.path.isfile(p):
            missing.append(f["path"])
        elif sha256(p) != f["sha256"]:
            bad.append(f["path"])
    if missing or bad:
        for f in missing:
            print("MISSING:", f)
        for f in bad:
            print("MISMATCH:", f)
        print("verify_build_manifest: %d file(s) checked, %d mismatch, %d missing"
              % (len(manifest["files"]), len(bad), len(missing)))
        sys.exit(1)
    print("verify_build_manifest: OK (%d files, %s)"
          % (len(manifest["files"]), os.path.basename(os.path.abspath(d))))


if __name__ == "__main__":
    main()
