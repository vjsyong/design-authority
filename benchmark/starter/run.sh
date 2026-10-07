#!/usr/bin/env bash
# Run Procura. Uses the benchmark python (Flask + Playwright installed there),
# resolved from PATH so it works inside the benchmark sandbox too.
set -e
cd "$(dirname "$0")"
PY="${BENCH_PY:-python3}"
exec "$PY" app.py "$@"
