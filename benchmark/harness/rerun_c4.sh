#!/usr/bin/env bash
# Rerun c4 — the partial run was lost to the host-level VM restart (~05:58).
# Cleans the dead partial artifacts and launches the run as its own systemd
# user unit (own cgroup, survives session lifecycles).
set -u
cd /home/xrim/design-authority
mkdir -p /tmp/da-launch benchmark/runs/_launch
rm -rf benchmark/runs/c4 /tmp/da-ws/c4
systemd-run --user --unit=da-c4 --collect \
  -p WorkingDirectory=/home/xrim/design-authority \
  -p "Environment=HOME=/home/xrim" \
  -p "Environment=PATH=/home/xrim/design-authority/.venv/bin:/usr/local/bin:/usr/bin:/bin" \
  -p MemoryMax=8G \
  -p StandardOutput=append:/tmp/da-launch/c4.log \
  -p StandardError=append:/tmp/da-launch/c4.err \
  /home/xrim/design-authority/.venv/bin/python benchmark/harness/run_condition.py --condition C --run-id c4 --timeout 1800
echo "da-c4 unit launched"
