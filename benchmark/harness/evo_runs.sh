#!/usr/bin/env bash
# Authority-evolution downstream re-runs (Phase 7): fresh C-condition runs
# against the 0.13.0-experiment authority pack. Sequential (host-stability
# lesson from P4). Each run gets its own cgroup via the wrapping systemd unit.
set -u
cd /home/xrim/design-authority
PY=/home/xrim/design-authority/.venv/bin/python
mkdir -p /tmp/da-launch
for rid in e1 e2; do
  echo "=== evo: $rid start $(date -u +%H:%M:%S)"
  "$PY" benchmark/harness/run_condition.py --condition C --run-id "$rid" \
      --pack triage-evolution --timeout 1800 || true
  echo "=== evo: $rid done $(date -u +%H:%M:%S)"
done
echo "=== EVO CHAIN COMPLETE $(date -u +%H:%M:%S) ==="
