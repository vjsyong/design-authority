#!/usr/bin/env bash
# Launch the Phase-7 evolution re-runs as a detached systemd user unit.
set -u
mkdir -p /tmp/da-launch
systemd-run --user --unit=da-evo --collect \
  -p WorkingDirectory=/home/xrim/design-authority \
  -p "Environment=HOME=/home/xrim" \
  -p "Environment=PATH=/home/xrim/design-authority/.venv/bin:/usr/local/bin:/usr/bin:/bin" \
  -p MemoryMax=8G \
  -p StandardOutput=append:/tmp/da-launch/evo.log \
  -p StandardError=append:/tmp/da-launch/evo.err \
  /bin/bash /home/xrim/design-authority/benchmark/harness/evo_runs.sh
echo "da-evo unit launched"
