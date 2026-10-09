#!/usr/bin/env python3
"""x05 seal tool — immutable checkpoints.

A seal is a SHA-256 manifest over code, records and HANDOFF.md, plus a
read-only copy. The sealed (excluded) boundary keeps runner-managed,
agent-facing reference layers out of the integrity claim:

  excluded: reference/            (brief, protocol, screens — runner-provided)
            opencode.json         (per-run tool config)
            run-authority         (per-run tooling, re-installed every session)

Everything else — source, git history, .design-authority records, QA.md,
HANDOFF.md — is sealed.

Usage:
  x05_seal.py create --ws WS --id SID [--root X05_ROOT]
  x05_seal.py verify --seal SEALDIR        # exit 1 on mismatch
  x05_seal.py manifest --ws WS [--json]
"""
import argparse
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x05_common import (X05_ROOT, hash_tree, iter_tree, now_iso,  # noqa: E402
                        read_json, sha256_file, write_json_atomic)

SEAL_EXCLUDES = ["reference", "opencode.json", "run-authority"]


def make_manifest(ws):
    files = hash_tree(ws, excludes=SEAL_EXCLUDES)
    records = {k: v for k, v in files.items() if k.startswith(".design-authority/")}
    return {
        "created": now_iso(),
        "exclude": SEAL_EXCLUDES,
        "file_count": len(files),
        "files": files,
        "summary": {
            "records": len(records),
            "code": len(files) - len(records),
            "has_git": any(k.startswith(".git/") for k in files),
            "has_handoff": "HANDOFF.md" in files,
        },
    }


def create(ws, sid, root=X05_ROOT):
    ws = os.path.abspath(ws)
    seal_dir = os.path.join(root, "seal", sid)
    tree_dir = os.path.join(seal_dir, "tree")
    if os.path.exists(seal_dir):
        raise SystemExit("seal already exists: %s (seals are immutable; "
                         "delete only with a recorded reason)" % seal_dir)
    manifest = make_manifest(ws)
    manifest["id"] = sid
    os.makedirs(tree_dir)
    for rel, src in iter_tree(ws, excludes=SEAL_EXCLUDES):
        dst = os.path.join(tree_dir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.islink(src):
            os.symlink(os.readlink(src), dst)
        else:
            shutil.copy2(src, dst)
    write_json_atomic(os.path.join(seal_dir, "manifest.json"), manifest)
    # make the copy read-only (dirs 0555, files 0444); parent stays writable
    for dirpath, dirnames, filenames in os.walk(tree_dir, topdown=False):
        for f in filenames:
            p = os.path.join(dirpath, f)
            if not os.path.islink(p):
                os.chmod(p, 0o444)
        os.chmod(dirpath, 0o555)
    return seal_dir, manifest


def verify(seal_dir):
    manifest = read_json(os.path.join(seal_dir, "manifest.json"))
    if manifest is None:
        return ["missing manifest"], {}
    tree = os.path.join(seal_dir, "tree")
    bad = []
    for rel, want in manifest["files"].items():
        p = os.path.join(tree, rel)
        if os.path.islink(p):
            got = "symlink:" + os.readlink(p)
        elif os.path.isfile(p):
            got = sha256_file(p)
        else:
            bad.append("missing: " + rel)
            continue
        if got != want:
            bad.append("mismatch: " + rel)
    return bad, manifest


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create")
    c.add_argument("--ws", required=True)
    c.add_argument("--id", required=True)
    c.add_argument("--root", default=X05_ROOT)
    v = sub.add_parser("verify")
    v.add_argument("--seal", required=True)
    m = sub.add_parser("manifest")
    m.add_argument("--ws", required=True)
    m.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd == "create":
        seal_dir, manifest = create(args.ws, args.id, args.root)
        print("sealed %s -> %s (%d files, records=%d)"
              % (args.id, seal_dir, manifest["file_count"],
                 manifest["summary"]["records"]))
        return 0
    if args.cmd == "verify":
        bad, manifest = verify(args.seal)
        if bad:
            print("SEAL VERIFY FAILED: %s" % os.path.basename(args.seal),
                  file=sys.stderr)
            for b in bad[:20]:
                print("  " + b, file=sys.stderr)
            return 1
        print("seal OK: %s (%d files)" % (os.path.basename(args.seal),
                                          len(manifest["files"])))
        return 0
    if args.cmd == "manifest":
        mf = make_manifest(args.ws)
        if args.json:
            print(json.dumps(mf, indent=1))
        else:
            print("files=%d records=%d git=%s handoff=%s"
                  % (mf["file_count"], mf["summary"]["records"],
                     mf["summary"]["has_git"], mf["summary"]["has_handoff"]))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
