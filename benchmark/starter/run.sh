#!/usr/bin/env bash
# Run Procura. Uses the benchmark python (Flask + Playwright installed there).
set -e
cd "$(dirname "$0")"
PY="${BENCH_PY:-/home/xrim/design-authority/.venv/bin/python}"
exec "$PY" app.py "$@"
