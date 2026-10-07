#!/usr/bin/env bash
# Single Phase-7 re-run (e3): e2 came back flagged (functional defect in the
# detail route on a rushed 210s run). One clean third rep restores n=2 clean.
set -u
mkdir -p /tmp/da-launch
systemd-run --user --unit=da-evo3 --collect \
  -p WorkingDirectory=/home/xrim/design-authority \
  -p "Environment=HOME=/home/xrim" \
  -p "Environment=PATH=/home/xrim/design-authority/.venv/bin:/usr/local/bin:/usr/bin:/bin" \
  -p MemoryMax=8G \
  -p StandardOutput=append:/tmp/da-launch/evo3.log \
  -p StandardError=append:/tmp/da-launch/evo3.err \
  /home/xrim/design-authority/.venv/bin/python \
      benchmark/harness/run_condition.py --condition C --run-id e3 \
      --pack triage-evolution --timeout 1800
echo "da-evo3 unit launched"
