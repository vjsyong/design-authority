#!/usr/bin/env bash
# Serve the pilot-condition builds for review.
#   A (a1) -> 9100 · B (b1) -> 9101 · C (c1) -> 9102
# usage: ./pilot_serve.sh start|stop|status
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PY="$ROOT/.venv/bin/python"
declare -A PORTS=( [a1]=9100 [b1]=9101 [c1]=9102 )

start() {
  for r in a1 b1 c1; do
    ws="$ROOT/benchmark/runs/$r/ws"; port="${PORTS[$r]}"
    if [ -f "$ws/serve.pid" ] && kill -0 "$(cat "$ws/serve.pid")" 2>/dev/null; then
      echo "$r: already running (pid $(cat "$ws/serve.pid"), port $port)"; continue
    fi
    cd "$ws" || continue
    nohup setsid "$PY" app.py --port "$port" > serve.log 2>&1 &
    echo $! > "$ws/serve.pid"
    cd "$ROOT" || exit 1
    sleep 1
    if curl -fsS -o /dev/null "http://127.0.0.1:$port/healthz"; then
      echo "$r: up on http://127.0.0.1:$port (pid $(cat "$ws/serve.pid"))"
    else
      echo "$r: FAILED to start — see $ws/serve.log"; tail -3 "$ws/serve.log" 2>/dev/null
    fi
  done
}

stop() {
  for r in a1 b1 c1; do
    ws="$ROOT/benchmark/runs/$r/ws"
    if [ -f "$ws/serve.pid" ]; then
      pid="$(cat "$ws/serve.pid")"
      kill "$pid" 2>/dev/null && echo "$r: stopped pid $pid" || echo "$r: pid $pid not running"
      rm -f "$ws/serve.pid"
    else
      echo "$r: no pidfile"
    fi
  done
}

status() {
  for r in a1 b1 c1; do
    port="${PORTS[$r]}"
    if curl -fsS -o /dev/null "http://127.0.0.1:$port/healthz" 2>/dev/null; then
      echo "$r: UP on :$port"
    else
      echo "$r: down"
    fi
  done
}

case "${1:-status}" in
  start) start ;;
  stop) stop ;;
  status) status ;;
  *) echo "usage: $0 start|stop|status"; exit 2 ;;
esac
