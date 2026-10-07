#!/usr/bin/env bash
# Sequential production chain — runs the remaining benchmark reps one at a
# time (parallel batches proved unstable on this host; see docs/06 D-7/D-8).
# Own systemd unit, own cgroup, survives session lifecycles.
set -u
cd /home/xrim/design-authority
PY=/home/xrim/design-authority/.venv/bin/python
for spec in "A a4" "B b3" "B b4" "C c3" "C c4"; do
  set -- $spec
  echo "=== chain: $2 ($1) start $(date -u +%H:%M:%S)"
  "$PY" benchmark/harness/run_condition.py --condition "$1" --run-id "$2" --timeout 1800 || true
  echo "=== chain: $2 done $(date -u +%H:%M:%S)"
done
echo "=== CHAIN COMPLETE $(date -u +%H:%M:%S) ==="
