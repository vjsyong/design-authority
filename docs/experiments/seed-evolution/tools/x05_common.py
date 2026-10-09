#!/usr/bin/env python3
"""x05 common helpers — shared by the seed-evolution (experiment 05) toolchain.

All host-side tooling runs from this directory (the repo) with the repo venv
python. The run area lives at X05_ROOT (default /home/xrim/x05), outside the
repo, and is the only place session state is written.
"""
import fcntl
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone

TOOLS = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT_DIR = os.path.dirname(TOOLS)              # docs/experiments/seed-evolution
REPO = os.path.dirname(os.path.dirname(os.path.dirname(EXPERIMENT_DIR)))
# repo = /home/xrim/design-authority ; sanity: the plan lives under docs/experiments/
ANNEXES = os.path.join(EXPERIMENT_DIR, "annexes")    # frozen agent-facing annexes

X05_ROOT = os.environ.get("X05_ROOT", "/home/xrim/x05")
VENV_PY = os.path.join(REPO, ".venv", "bin", "python3")

DEFAULT_MODEL = "deepseek/deepseek-flash"

# Budgets (plan §5.1/§7): wall 2700 s, 20M sum_total tokens per scored session.
WALL_BUDGET_S = 2700
TOKEN_BUDGET = 20_000_000


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def epoch():
    return time.time()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_tree(root, excludes=()):
    """Yield (relpath, abspath) for every entry under root, skipping entries
    whose relpath equals or is under one of the excludes (prefix match on
    path components). Sorted for determinism."""
    root = os.path.abspath(root)
    excl = [e.rstrip("/") for e in excludes]
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == ".":
            rel_dir = ""
        dirnames.sort()
        filenames.sort()
        keep = []
        for d in dirnames:
            rel = os.path.join(rel_dir, d) if rel_dir else d
            if any(rel == e or rel.startswith(e + "/") for e in excl):
                continue
            keep.append(d)
        dirnames[:] = keep
        for f in filenames:
            rel = os.path.join(rel_dir, f) if rel_dir else f
            if any(rel == e or rel.startswith(e + "/") for e in excl):
                continue
            yield rel, os.path.join(dirpath, f)


def hash_tree(root, excludes=()):
    """Deterministic {relpath: sha256} over regular files. Symlinks are
    recorded as 'symlink:<target>'."""
    out = {}
    for rel, path in iter_tree(root, excludes):
        if os.path.islink(path):
            out[rel] = "symlink:" + os.readlink(path)
        elif os.path.isfile(path):
            out[rel] = sha256_file(path)
    return out


def write_json_atomic(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp.%d" % os.getpid()
    with open(tmp, "w") as fh:
        json.dump(obj, fh, indent=1, sort_keys=False)
        fh.write("\n")
    os.replace(tmp, path)


def read_json(path, default=None):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def append_jsonl(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as fh:
        fh.write(json.dumps(obj) + "\n")


class StateLock(object):
    """flock-based lock around the run-area state file."""

    def __init__(self, root):
        os.makedirs(root, exist_ok=True)
        self.path = os.path.join(root, "state.lock")
        self.fh = None

    def __enter__(self):
        self.fh = open(self.path, "w")
        fcntl.flock(self.fh.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        if self.fh is not None:
            fcntl.flock(self.fh.fileno(), fcntl.LOCK_UN)
            self.fh.close()
            self.fh = None
        return False


def load_state(root=X05_ROOT):
    st = read_json(os.path.join(root, "state.json"))
    if not isinstance(st, dict):
        st = {"program": "x05", "created": now_iso(), "sessions": {},
              "order": [], "step_index": 0, "paused": False, "notes": []}
    st.setdefault("sessions", {})
    return st


def save_state(root, st):
    st["updated"] = now_iso()
    write_json_atomic(os.path.join(root, "state.json"), st)


def session_chain_of(sid):
    """f1..f3/cen/cod -> None; h<idx><cond> -> (idx, cond); <sid>r2 -> base."""
    base = sid
    while base and base[-1].isdigit() and base[-2:-1] == "r":
        base = base[:-2]
    if len(base) == 3 and base[0] == "h" and base[1] in "1234" and base[2] in "abc":
        return int(base[1]), base[2]
    if base.startswith("h") and len(base) == 4 and base[3] in "abc":
        return int(base[1]), base[3]
    return None


def chain_ids(sid):
    """For a chain session id, the full chain list from the schedule order."""
    return sid


def log_line(root, msg):
    os.makedirs(os.path.join(root, "logs"), exist_ok=True)
    line = "%s  %s" % (now_iso(), msg)
    with open(os.path.join(root, "logs", "conductor.log"), "a") as fh:
        fh.write(line + "\n")
    print(line, flush=True)


def run_quiet(cmd, cwd=None, timeout=None):
    import subprocess
    return subprocess.run(cmd, cwd=cwd, timeout=timeout,
                          capture_output=True, text=True)


if __name__ == "__main__":
    print(json.dumps({"tools": TOOLS, "experiment": EXPERIMENT_DIR,
                      "repo": REPO, "annexes": ANNEXES, "root": X05_ROOT,
                      "venv_py": VENV_PY, "model": DEFAULT_MODEL}, indent=1))
    sys.exit(0)
