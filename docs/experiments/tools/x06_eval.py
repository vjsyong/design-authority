#!/usr/bin/env python3
"""x06_eval — structured evaluation for an adoption-test run (x06_run.py).

Reads a run directory and produces the evaluation surface the owner memo
asks for: did the agent consult the authority, are its claims plausible,
how much setup friction existed, did it stay contained. Read-only.

    python3 docs/experiments/tools/x06_eval.py --root ~/x06-adoption --run-id run1
"""
import argparse
import json
import os
import re
import sys

HOST_ONLY_PATHS = ("/home/xrim/.hermes", "/home/xrim/x05", "/home/xrim/mail-triage",
                   "/home/xrim/design-authority/docs/experiments", "/home/xrim/.hermes/skills")


def classify_command(cmd):
    c = cmd.strip()
    if "git clone" in c:
        return "setup/network"
    if "da.py" in c:
        return "authority-cli"
    if "da_verify" in c or "verify" in c:
        return "verify"
    if any(x in c for x in ("pip ", "venv", "npm ", "apt ")):
        return "install"
    if any(x in c for x in ("curl ", "wget ", "playwright")):
        return "network/browser"
    return "other"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.expanduser("~/x06-adoption"))
    ap.add_argument("--run-id", default="run1")
    args = ap.parse_args(argv)

    run_dir = os.path.join(os.path.expanduser(args.root), args.run_id)
    run = json.load(open(os.path.join(run_dir, "run.json")))

    events = []
    with open(os.path.join(run_dir, "transcript.jsonl")) as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except ValueError:
                    pass

    tool_calls, commands, da_calls, host_hits = [], [], [], []
    for e in events:
        part = e.get("part") or {}
        if e.get("type") != "tool_use":
            continue
        tool = part.get("tool")
        st = part.get("state") or {}
        inp = st.get("input") or {}
        tool_calls.append(tool)
        blob = json.dumps(inp)
        for p in HOST_ONLY_PATHS:
            if p in blob:
                host_hits.append(p)
        if tool == "bash" and inp.get("command"):
            cmd = inp["command"]
            commands.append(cmd)
            if "da.py" in cmd:
                m = re.search(r"da\.py[^\n;&|]*", cmd)
                da_calls.append(m.group(0).strip() if m else cmd[:120])

    ws = os.path.join(run_dir, "ws")
    ws_files = []
    for dirpath, dirnames, filenames in os.walk(ws):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__")]
        for f in filenames:
            ws_files.append(os.path.relpath(os.path.join(dirpath, f), ws))

    kinds = {}
    for c in commands:
        k = classify_command(c)
        kinds[k] = kinds.get(k, 0) + 1

    out = {
        "run": {k: run.get(k) for k in ("id", "model", "status", "exit", "wall_s", "timeout_s")},
        "events": len(events),
        "tools": {t: tool_calls.count(t) for t in sorted(set(tool_calls))},
        "command_kinds": kinds,
        "bash_commands": len(commands),
        "authority_cli_calls": len(da_calls),
        "authority_cli_sample": da_calls[:40],
        "host_only_path_hits": sorted(set(host_hits)),
        "ws_file_count": len(ws_files),
        "ws_files_sample": ws_files[:60],
        "done_md": os.path.exists(os.path.join(ws, "DONE.md")),
        "done_md_path": os.path.join(ws, "DONE.md") if os.path.exists(os.path.join(ws, "DONE.md")) else None,
    }
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
