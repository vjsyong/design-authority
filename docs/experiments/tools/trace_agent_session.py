#!/usr/bin/env python3
"""Experiment 02, part A: trace a real agent session against the MCP server.

Spawns tools/da-mcp.py (project venv) and walks a realistic build-time
workflow: overview, an approximate ask, discovery, inspection, adoption,
verification, and a gap report. Every call is recorded with its own latency;
the server also writes its decision log into the session workspace, both of
which are the committed evidence for docs/experiments/02-agent-trace.md.

    .venv/bin/python3 docs/experiments/tools/trace_agent_session.py
"""
import json
import os
import select
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
VENV_PY = os.path.join(ROOT, ".venv", "bin", "python")
WS = os.path.join(ROOT, "docs", "experiments", "agent-session-workspace")
OUT = os.path.join(ROOT, "docs", "experiments", "02-agent-session-transcript.json")


def send(proc, obj):
    proc.stdin.write(json.dumps(obj) + "\n")
    proc.stdin.flush()


def recv(proc, want_id, timeout=120):
    while True:
        ready, _, _ = select.select([proc.stdout], [], [], timeout)
        if not ready:
            raise TimeoutError("no response for id %s" % want_id)
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError("server closed stdout")
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        if msg.get("id") == want_id:
            return msg


def main():
    os.makedirs(os.path.join(WS, ".design-authority"), exist_ok=True)
    env = dict(os.environ, DA_WORKSPACE=WS)
    proc = subprocess.Popen([VENV_PY, os.path.join(ROOT, "tools", "da-mcp.py")],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, cwd=WS, env=env)
    transcript = []
    rid = 100

    def call(tool, args, note=""):
        nonlocal rid
        rid += 1
        t0 = time.time()
        send(proc, {"jsonrpc": "2.0", "id": rid, "method": "tools/call",
                    "params": {"name": tool, "arguments": args}})
        msg = recv(proc, rid)
        ms = round((time.time() - t0) * 1000, 1)
        result = msg.get("result", {})
        content = result.get("content") or []
        try:
            data = json.loads(content[0].get("text", "{}")) if content else {}
        except ValueError:
            data = {"raw": content[0].get("text") if content else ""}
        step = {"step": len(transcript) + 1, "tool": tool, "args": args,
                "note": note, "latency_ms": ms}
        if tool == "authority_overview":
            step["got"] = {"authority": data.get("authority"),
                           "counts": data.get("counts")}
        elif tool == "resolve_design_problem":
            step["got"] = {"outcome": data.get("outcome"),
                           "resolution_id": ((data.get("resolution") or {}).get("artifact") or
                                             (data.get("resolution") or {}).get("fallback") or
                                             (data.get("resolution") or {}).get("recipe") or
                                             (data.get("resolution") or {}).get("prohibition") or {}
                                             ).get("id"),
                           "assist": ((data.get("retrieval_assist") or {}).get("status")),
                           "assist_top": [c.get("id") for c in
                                          ((data.get("retrieval_assist") or {}).get("candidates") or [])][:3]}
        elif tool == "discover_candidates":
            step["got"] = {"status": data.get("status"),
                           "top": [(c.get("id"), c.get("lex_rank"), c.get("cos"))
                                   for c in (data.get("candidates") or [])][:4]}
        elif tool == "inspect_artifact":
            art = data.get("artifact") or {}
            step["got"] = {"status": data.get("status"), "id": art.get("id"),
                           "title": art.get("title"),
                           "class": (art.get("body") or {}).get("class")}
        elif tool == "search_authority":
            step["got"] = {"hits": [(h.get("id"), h.get("score"))
                                    for h in (data.get("hits") or [])][:3]}
        elif tool == "report_gap":
            step["got"] = {"status": data.get("status"),
                           "gap": (data.get("gap") or {}).get("id")}
        else:
            step["got"] = data if isinstance(data, dict) else str(data)
        transcript.append(step)
        print("[%2d] %-22s %6sms  %s" % (step["step"], tool, ms,
                                         json.dumps(step["got"])[:110]))
        return step

    try:
        send(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                               "clientInfo": {"name": "da-trace", "version": "0"}}})
        recv(proc, 1)
        send(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})

        # The task: "add a way to flip one setting on or off, with a status
        # chip on the settings page" under the Triage authority.
        call("authority_overview", {}, "orient")
        call("resolve_design_problem",
             {"problem": "let people flip one preference on or off right away"},
             "approximate wording, expect UNDEFINED")
        d = call("discover_candidates",
                 {"query": "let people flip one preference on or off right away"},
                 "semantic discovery")
        top = ((d["got"].get("top") or [["component/px-sw"]])[0][0])
        call("inspect_artifact", {"id": top}, "inspect the top candidate")
        call("resolve_design_problem", {"problem": "a switch"},
             "adopt with canonical vocabulary")
        call("resolve_design_problem",
             {"problem": "a filterable status field", "assist": "semantic"},
             "second ask with assist block")
        call("discover_candidates", {"query": "labels that show a record's state"},
             "discovery for the chip part")
        call("search_authority", {"query": "filter chip"}, "lexical search")
        call("inspect_artifact", {"id": "component/chip"}, "confirm the chip record")
        call("resolve_design_problem", {"problem": "a status chip with text padding"},
             "composition question")
        call("report_gap",
             {"need": "a settings-page convention for preference rows",
              "context": {"page": "settings", "observed": "no pattern record for preference rows"},
              "scope_hint": "settings-pages"},
             "what stays undefined")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()

    with open(OUT, "w") as fh:
        json.dump({"session": "trace A: scripted agent session via MCP stdio",
                   "workspace": WS, "calls": transcript}, fh, indent=1)
    total = sum(c["latency_ms"] for c in transcript)
    print("\n%d calls, total %.1fs client-side; transcript: %s"
          % (len(transcript), total / 1000.0, OUT))


if __name__ == "__main__":
    main()
