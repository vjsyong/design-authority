#!/usr/bin/env python3
"""P4 (maintenance economics, docs/experiments/09) common helpers.

Run area: ~/p4-maint (P4_ROOT, x05 convention: outside the repo). The
session-level machinery (seal, leakscan, atomic io) is reused from the x05
toolchain, frozen at docs/experiments/seed-evolution/tools/.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
X05_TOOLS = os.path.join(os.path.dirname(HERE), "seed-evolution", "tools")
if X05_TOOLS not in sys.path:
    sys.path.insert(0, X05_TOOLS)

from x05_common import (append_jsonl, hash_tree, log_line, now_iso,  # noqa: E402,F401
                        read_json, sha256_file, StateLock, write_json_atomic)

REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))  # ~/design-authority
P4_ROOT = os.environ.get("P4_ROOT", "/home/xrim/p4-maint")
MATS = os.path.join(P4_ROOT, "materials")
VENV_PY = os.path.join(REPO, ".venv", "bin", "python3")

# the frozen sandbox interpreter (x05 materials; carries the QA deps)
PYVENV = os.path.expanduser("~/x05/materials/pyvenv")

DEFAULT_MODEL = "deepseek/deepseek-flash"
WALL_BUDGET_S = 2700
TOKEN_BUDGET = 20_000_000

CHAINS = ("da", "base")


def run_dir(sid, root=None):
    return os.path.join(root or P4_ROOT, "run", sid)


def seal_dir(sid, root=None):
    return os.path.join(root or P4_ROOT, "seal", sid)


def materials(*parts):
    return os.path.join(MATS, *parts)
