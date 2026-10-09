#!/usr/bin/env python3
"""x05 materials staging — freeze agent-facing inputs into the run area.

Copies, from the repo annexes + tooling, the immutable inputs every session
consumes: the starter template, briefs, protocol, wrapper template, the blank
`base` pack, the pack-format spec (for the cod session), rubrics, and the
fixture datasets. Also stages the da tooling the sandbox mounts read-only at
/opt/da (tools + kernel).

    x05_materials.py stage [--root X05_ROOT] [--force]
    x05_materials.py verify [--root X05_ROOT]
"""
import argparse
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x05_common import ANNEXES, REPO, X05_ROOT, hash_tree, read_json, sha256_file, write_json_atomic  # noqa: E402

PLAN_COPY = [
    # (src repo-relative under annexes, dst under materials)
    ("starter", "starter"),
    ("briefs", "briefs"),
    ("protocol.md", "protocol.md"),
    ("wrapper", "wrapper"),
    ("packs/base", "packs/base"),
    ("pack-spec", "spec"),
    ("rubrics", "rubrics"),
    ("fixtures", "fixtures"),
]


def copy_tree(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def build_pyvenv(mats):
    """Sanitized toolchain venv mounted at /opt/py/venv: fresh venv from the
    python toolchain + playwright pinned to the repo venv's version, with all
    host paths rewritten. No repo path may appear in the mounted bytes."""
    import glob
    dst = os.path.join(mats, "pyvenv")
    marker = os.path.join(dst, ".x05-sanitized.json")
    if os.path.exists(marker):
        return dst
    toolchain = sorted(glob.glob(os.path.join(
        os.path.expanduser("~"), ".hermes", "tools", "python-*-linux-x64")))[-1]
    shutil.rmtree(dst, ignore_errors=True)
    subprocess.run([os.path.join(toolchain, "bin", "python3"), "-m", "venv",
                    "--copies", dst], check=True)
    repo_py = os.path.join(REPO, ".venv", "bin", "python3")
    show = subprocess.run([repo_py, "-m", "pip", "show", "playwright"],
                          capture_output=True, text=True)
    ver = None
    for line in show.stdout.splitlines():
        if line.startswith("Version:"):
            ver = line.split(":", 1)[1].strip()
    if not ver:
        raise SystemExit("cannot determine repo playwright version")
    subprocess.run([os.path.join(dst, "bin", "pip"), "install", "-q",
                    "playwright==%s" % ver], check=True)
    # sanitize (targeted): drop bytecode caches; rewrite dst path in every
    # text file (shebangs, activate scripts, cfg, RECORD); never touch
    # binaries (marshal/ELF offsets would corrupt).
    bdst = dst.encode()
    for root_, dirs, files in os.walk(dst):
        for d in [d for d in dirs if d == "__pycache__"]:
            shutil.rmtree(os.path.join(root_, d), ignore_errors=True)
        for f in [f for f in files if f.endswith(".pyc")]:
            try:
                os.remove(os.path.join(root_, f))
            except OSError:
                pass
    for root_, dirs, files in os.walk(dst):
        for f in files:
            p = os.path.join(root_, f)
            try:
                data = open(p, "rb").read()
            except OSError:
                continue
            if bdst not in data:
                continue
            try:
                data.decode("utf-8")
            except UnicodeDecodeError:
                continue
            open(p, "wb").write(data.replace(bdst, b"/opt/py/venv"))
    from x05_common import now_iso
    write_json_atomic(marker, {"playwright": ver, "built": now_iso(),
                               "sanitized": True})
    return dst


def stage(root=X05_ROOT, force=False):
    mats = os.path.join(root, "materials")
    os.makedirs(mats, exist_ok=True)
    for src_rel, dst_rel in PLAN_COPY:
        src = os.path.join(ANNEXES, src_rel)
        dst = os.path.join(mats, dst_rel)
        if not os.path.exists(src):
            raise SystemExit("annex missing: %s" % src)
        if os.path.isdir(src):
            copy_tree(src, dst)
        else:
            shutil.copy2(src, dst)
    build_pyvenv(mats)
    # da tooling (tools/da.py + the kernel package)
    da_tools = os.path.join(mats, "da", "tools")
    da_kernel = os.path.join(mats, "da", "kernel", "design_authority")
    for d in (da_tools, da_kernel):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
    shutil.copy2(os.path.join(REPO, "tools", "da.py"),
                 os.path.join(da_tools, "da.py"))
    for name in sorted(os.listdir(os.path.join(REPO, "kernel", "design_authority"))):
        if name.endswith(".py"):
            shutil.copy2(os.path.join(REPO, "kernel", "design_authority", name),
                         os.path.join(da_kernel, name))

    manifest = {"staged": None, "root": root, "trees": {}}
    from x05_common import now_iso
    manifest["staged"] = now_iso()
    for rel in ["starter", "briefs", "wrapper", "packs/base", "spec", "rubrics",
                "fixtures", "da", "protocol.md", "pyvenv"]:
        p = os.path.join(mats, rel)
        if os.path.isdir(p):
            h = hash_tree(p)
            manifest["trees"][rel] = {"files": len(h), "sha256_of_tree": sha256_file_tree(p)}
        else:
            manifest["trees"][rel] = {"sha256": sha256_file(p)}
    write_json_atomic(os.path.join(mats, "manifest.json"), manifest)
    print("staged materials at %s (%d trees)" % (mats, len(manifest["trees"])))
    return manifest


def sha256_file_tree(path):
    import hashlib
    h = hashlib.sha256()
    for rel, ap in sorted(hash_tree(path).items(), key=lambda kv: kv[0]):
        h.update(("%s\0%s\n" % (rel, ap)).encode())
    return h.hexdigest()


def verify(root=X05_ROOT):
    mats = os.path.join(root, "materials")
    manifest = read_json(os.path.join(mats, "manifest.json"))
    if not manifest:
        print("materials manifest missing", file=sys.stderr)
        return 1
    bad = []
    for rel, info in manifest["trees"].items():
        p = os.path.join(mats, rel)
        if "sha256_of_tree" in info:
            if not os.path.exists(p) or sha256_file_tree(p) != info["sha256_of_tree"]:
                bad.append(rel)
        else:
            if not os.path.exists(p) or sha256_file(p) != info["sha256"]:
                bad.append(rel)
    if bad:
        print("MATERIALS VERIFY FAILED: %s" % ", ".join(bad), file=sys.stderr)
        return 1
    print("materials OK (%d trees)" % len(manifest["trees"]))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["stage", "verify"])
    ap.add_argument("--root", default=X05_ROOT)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    if args.cmd == "stage":
        stage(args.root, args.force)
        return 0
    return verify(args.root)


if __name__ == "__main__":
    sys.exit(main())
