#!/usr/bin/env bash
# Repo gates: pack drift, kernel unit tests, golden set, MCP smoke (venv).
set -e
cd "$(dirname "$0")/.."
echo "== triage pack drift check (synthesis pipeline)"
# The live triage pack is built by docs/synthesis/triage/tools/build_triage_pack.py.
# The kit builder (tools/build_pack_triage.py) remains for the evolution packs (--out).
python3 tools/check_triage_pack.py
echo "== triage coverage sweep (element by element)"
python3 docs/synthesis/triage/tools/sweep_resolution.py --quiet
echo "== kernel unit tests"
python3 -m unittest discover -s kernel/tests -t . -q
echo "== golden set"
python3 tools/da.py golden | tail -1
echo "== synthesis pack goldens"
for p in wink leader dominion; do python3 tools/da.py --pack packs/$p golden --file packs/$p/golden.json | tail -1; done
echo "== synthesis precedents"
python3 tools/precedent_probe.py | tail -1
if [ -x .venv/bin/python ]; then
  echo "== MCP smoke"
  python3 tools/mcp_smoke.py | tail -1
else
  echo "== MCP smoke skipped (no .venv; python3 -m venv .venv && .venv/bin/pip install 'mcp<2')"
fi
echo "== concept-site gate (designauthority.seanyong.xyz)"
python3 tools/check_concept_site.py
echo "gates: OK"
