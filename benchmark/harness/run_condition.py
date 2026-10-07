#!/usr/bin/env python3
"""Run one benchmark condition end-to-end.

    python3 run_condition.py --condition B --run-id b1 [--model M] [--timeout S]
    python3 run_condition.py --condition A --run-id atest --skip-agent   # pipeline test

Pipeline: materials -> (opencode agent run) -> serve -> capture -> interact ->
scan -> run.json.
"""
import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from collections import Counter
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

from materials import build  # noqa: E402

OPENCODE = os.path.expanduser("~/.opencode/bin/opencode")
VENV_PY = os.path.join(ROOT, ".venv", "bin", "python")


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def free_port(start=8200):
    for port in range(start, start + 200):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("no free port")


def wait_http(url, timeout=30):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            time.sleep(0.4)
    return False


def tool_stats(transcript_path):
    types, tools = Counter(), Counter()
    if not os.path.exists(transcript_path):
        return {"events": 0, "tool_calls": 0, "tools": {}}
    n = 0
    with open(transcript_path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            n += 1
            t = ev.get("type") or (ev.get("event") or {}).get("type") or "?"
            types[t] += 1
            name = ev.get("tool") or ev.get("name")
            props = ev.get("properties") or {}
            if isinstance(props, dict):
                name = name or props.get("tool") or props.get("name")
            if name:
                tools[str(name)] += 1
    return {"events": n, "tool_calls": sum(tools.values()), "tools": dict(tools),
            "event_types": dict(types)}


def authority_stats(ws):
    log = os.path.join(ws, ".design-authority", "decision-log.jsonl")
    if not os.path.exists(log):
        return None
    calls, outcomes = Counter(), Counter()
    with open(log) as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            calls[rec.get("tool")] += 1
            if rec.get("tool") == "resolve_design_problem":
                outcomes[(rec.get("summary") or {}).get("outcome")] += 1
    return {"calls": dict(calls), "resolve_outcomes": dict(outcomes),
            "total": sum(calls.values())}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", required=True, choices=["A", "B", "C"])
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--model", default="deepseek/deepseek-flash")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--skip-agent", action="store_true")
    args = ap.parse_args(argv)

    run_dir = os.path.join(ROOT, "benchmark", "runs", args.run_id)
    ws = os.path.join(run_dir, "ws")
    os.makedirs(run_dir, exist_ok=True)
    run = {"run_id": args.run_id, "condition": args.condition, "model": args.model,
           "started": now_iso(), "status": "running"}
    run_path = os.path.join(run_dir, "run.json")

    def save():
        with open(run_path, "w") as fh:
            json.dump(run, fh, indent=1)

    manifest = build(args.condition, ws)
    run["materials"] = {"starter_commit": manifest["starter_commit"]}

    prompt = open(os.path.join(ROOT, "benchmark", "briefs", "base.md")).read()
    prompt += "\n\n" + open(os.path.join(
        ROOT, "benchmark", "briefs", "condition-%s.md" % args.condition.lower())).read()
    prompt_path = os.path.join(run_dir, "prompt.md")
    with open(prompt_path, "w") as fh:
        fh.write(prompt)
    run["prompt"] = "prompt.md"

    cfg = {"$schema": "https://opencode.ai/config.json", "model": args.model}
    if args.condition == "C":
        cfg["mcp"] = {"design_authority": {
            "type": "local",
            "command": [VENV_PY, os.path.join(ROOT, "tools", "da-mcp.py")],
            "environment": {"DA_WORKSPACE": ws},
            "enabled": True}}
    with open(os.path.join(ws, "opencode.json"), "w") as fh:
        json.dump(cfg, fh, indent=1)

    # ---- agent run ----
    if args.skip_agent:
        run["opencode"] = {"skipped": True}
    else:
        t0, timed_out, rc = time.time(), False, None
        cmd = [OPENCODE, "run", "--pure", "-m", args.model,
               "--title", "bench-" + args.run_id, "--format", "json", prompt]
        with open(os.path.join(run_dir, "transcript.jsonl"), "w") as transcript, \
                open(os.path.join(run_dir, "opencode-stderr.log"), "w") as stderr:
            try:
                proc = subprocess.run(cmd, cwd=ws, stdout=transcript, stderr=stderr,
                                      timeout=args.timeout)
                rc = proc.returncode
            except subprocess.TimeoutExpired:
                rc, timed_out = "timeout", True
        run["opencode"] = {"exit": rc, "timed_out": timed_out,
                           "duration_s": round(time.time() - t0, 1)}
        run["opencode"].update(tool_stats(os.path.join(run_dir, "transcript.jsonl")))
        run["authority"] = authority_stats(ws)
    save()

    # ---- serve + capture + interact ----
    port = free_port()
    server = subprocess.Popen([VENV_PY, "app.py", "--port", str(port)], cwd=ws,
                              stdout=open(os.path.join(run_dir, "server.log"), "w"),
                              stderr=subprocess.STDOUT)
    url = "http://127.0.0.1:%d" % port
    try:
        if not wait_http(url + "/healthz"):
            run["serve"] = {"error": "healthz never came up"}
        else:
            run["serve"] = {"port": port, "ok": True}
            subprocess.run([VENV_PY, os.path.join(HERE, "capture.py"),
                            "--url", url, "--out", os.path.join(run_dir, "capture")],
                           check=False)
            run["capture"] = "capture/capture.json"
            subprocess.run([VENV_PY, os.path.join(HERE, "interact.py"),
                            "--url", url, "--out", os.path.join(run_dir, "interact.json")],
                           check=False)
            interact_out = os.path.join(run_dir, "interact.json")
            if os.path.exists(interact_out):
                with open(interact_out) as fh:
                    res = (json.load(fh) or {}).get("result", {})
                run["interact"] = {"passed": res.get("passed"),
                                   "total": res.get("total")}
    except Exception as exc:
        run["serve"] = {"error": str(exc)[:300]}
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except Exception:
            server.kill()

    # ---- static scan ----
    subprocess.run([VENV_PY, os.path.join(HERE, "scan.py"),
                    "--ws", ws, "--out", os.path.join(run_dir, "scan.json")],
                   check=False)
    run["scan"] = "scan.json"
    run["finished"] = now_iso()
    run["status"] = "ok"
    save()
    oc = run.get("opencode") or {}
    print("run %s (%s): exit=%s duration=%ss interact=%s"
          % (args.run_id, args.condition, oc.get("exit"), oc.get("duration_s"),
             run.get("interact")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
