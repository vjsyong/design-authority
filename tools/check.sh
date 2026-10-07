#!/usr/bin/env bash
# Repo gates: pack drift, kernel unit tests, golden-set agreement.
set -e
cd "$(dirname "$0")/.."
echo "== pack drift check"
python3 tools/build_pack_triage.py --check
echo "== kernel unit tests"
python3 -m unittest discover -s kernel/tests -t . -q
echo "== golden set"
python3 tools/da.py golden | tail -1
echo "gates: OK"
