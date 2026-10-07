#!/usr/bin/env bash
# Repo gates: pack drift, kernel unit tests, golden set, MCP smoke (venv).
set -e
cd "$(dirname "$0")/.."
echo "== pack drift check"
python3 tools/build_pack_triage.py --check
echo "== kernel unit tests"
python3 -m unittest discover -s kernel/tests -t . -q
echo "== golden set"
python3 tools/da.py golden | tail -1
if [ -x .venv/bin/python ]; then
  echo "== MCP smoke"
  python3 tools/mcp_smoke.py | tail -1
else
  echo "== MCP smoke skipped (no .venv; python3 -m venv .venv && .venv/bin/pip install 'mcp<2')"
fi
echo "gates: OK"
