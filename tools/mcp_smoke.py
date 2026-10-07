#!/usr/bin/env python3
"""Stdio smoke test for the Design Authority MCP server (stdlib client).

Spawns tools/da-mcp.py with the project venv python, performs the MCP
handshake, calls every tool once, reads a resource, and verifies key
behaviors (outcome classes, citations, decision log, gap/proposal flow).

    python3 tools/mcp_smoke.py
"""
import json
import os
import select
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VENV_PY = os.path.join(ROOT, ".venv", "bin", "python")
SNAPSHOT = os.path.expanduser("~/triage-design-system-demo")

PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("%s  %s%s" % ("ok " if cond else "FAIL", name,
                        "  (%s)" % detail if detail else ""))


def send(proc, obj):
    proc.stdin.write(json.dumps(obj) + "\n")
    proc.stdin.flush()


def recv(proc, want_id, timeout=60):
    while True:
        ready, _, _ = select.select([proc.stdout], [], [], timeout)
        if not ready:
            raise TimeoutError("no response for id %s" % want_id)
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError("server closed stdout before id %s" % want_id)
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        if msg.get("id") == want_id:
            return msg


def call(proc, name, args, rid) -> dict:
    send(proc, {"jsonrpc": "2.0", "id": rid, "method": "tools/call",
                "params": {"name": name, "arguments": args}})
    msg = recv(proc, rid)
    if "error" in msg:
        raise RuntimeError("tools/call %s error: %s" % (name, msg["error"]))
    result = msg.get("result", {})
    content = result.get("content") or []
    text = content[0].get("text", "{}") if content else "{}"
    try:
        return json.loads(text)
    except ValueError:
        return {"raw": text}


def main():
    ws = tempfile.mkdtemp(prefix="da-smoke-")
    env = dict(os.environ)
    env["DA_WORKSPACE"] = ws
    env["DA_SNAPSHOT"] = SNAPSHOT
    proc = subprocess.Popen([VENV_PY, os.path.join(HERE, "da-mcp.py")],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, cwd=ws, env=env)
    ok = False
    try:
        # handshake
        send(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": "2024-11-05",
                               "capabilities": {},
                               "clientInfo": {"name": "da-smoke", "version": "0"}}})
        init = recv(proc, 1)
        server_name = init["result"]["serverInfo"]["name"]
        check("initialize", server_name == "design-authority", server_name)
        send(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})

        # discovery
        send(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        tools = [t["name"] for t in recv(proc, 2)["result"]["tools"]]
        expected = {"authority_overview", "search_authority", "inspect_artifact",
                    "resolve_design_problem", "validate_implementation",
                    "report_gap", "propose_extension"}
        check("tools/list has all 7 tools", expected.issubset(set(tools)),
              ",".join(sorted(tools)))

        # overview
        ov = call(proc, "authority_overview", {}, 10)
        check("overview identity", ov.get("status") == "ok"
              and ov["authority"]["authority"] == "triage",
              ov.get("authority", {}).get("version"))
        check("overview counts", ov["counts"]["artifacts"].get("component") == 35)

        # search + inspect
        s = call(proc, "search_authority", {"query": "approval history"}, 11)
        check("search finds timeline", any(h["id"] == "component/tl" for h in s["hits"]))
        ins = call(proc, "inspect_artifact", {"id": "component/badge"}, 12)
        check("inspect returns artifact", ins["artifact"]["body"]["class"] == "badge")
        miss = call(proc, "inspect_artifact", {"id": "component/nope"}, 13)
        check("inspect miss carries hint", miss.get("status") == "error"
              and "hint" in miss)

        # resolution outcomes
        r1 = call(proc, "resolve_design_problem",
                  {"problem": "show whether a request is waiting for approval"}, 14)
        check("resolve COMPOSE", r1["outcome"] == "COMPOSE",
              (r1.get("resolution") or {}).get("recipe", {}).get("id"))
        r2 = call(proc, "resolve_design_problem",
                  {"problem": "add a progress bar for a long-running background job"}, 15)
        check("resolve UNDEFINED (structured)", r2["outcome"] == "UNDEFINED"
              and "fallback_policy" in r2)
        r3 = call(proc, "resolve_design_problem",
                  {"problem": "make the corners rounded"}, 16)
        check("resolve CONFLICT cites rule", r3["outcome"] == "CONFLICT"
              and r3["resolution"]["rule"]["id"] == "TDS003")
        check("resolve echoes authority", r1["authority"]["commit"].startswith("e374f380"))

        # validation
        v = call(proc, "validate_implementation",
                 {"target": os.path.join(SNAPSHOT, "examples")}, 17)
        check("validate runs triage-lint",
              v["validators"][0]["status"] == "ok"
              and v["summary"]["counts"]["error"] == 0,
              "score=%s" % v["summary"]["score"].get("value"))

        # gap -> proposal
        g = call(proc, "report_gap",
                 {"need": "progress indicator for a background job",
                  "context": {"page": "jobs"},
                  "attempted_resolution": {"searched": ["progress", "job"],
                                           "closest": ["component/spinner"]},
                  "scope_hint": "system-wide"}, 18)
        gid = g["gap"]["id"]
        check("report_gap stores record", gid.startswith("gap/"))
        p = call(proc, "propose_extension", {"gap_id": gid, "proposal": {
            "problem": "no progress treatment",
            "insufficiency": "spinner only shows activity",
            "reuse_case": "any consumer with background jobs",
            "composition_check": "spinner+text cannot express progress",
            "proposed": [{"kind": "component", "name": "progress"}],
            "depends_on": ["component/spinner"],
            "new_primitives": ["determinate progress"],
            "tests": [{"description": "renders with aria-valuenow", "deterministic": True}]}}, 19)
        check("propose_extension accepts candidate",
              p["proposal"]["status"] == "candidate")
        bad = call(proc, "propose_extension", {"gap_id": gid, "proposal": {
            "problem": "x", "insufficiency": "y", "reuse_case": "z",
            "composition_check": "c", "proposed": [{}],
            "depends_on": ["component/ghost"], "tests": [{}]}}, 20)
        check("propose_extension rejects unknown dep", bad.get("status") == "error")

        # resource
        send(proc, {"jsonrpc": "2.0", "id": 21, "method": "resources/read",
                    "params": {"uri": "authority://overview"}})
        res = recv(proc, 21)["result"]
        check("resource authority://overview", len(res["contents"][0]["text"]) > 100)

        # decision log
        log_path = os.path.join(ws, ".design-authority", "decision-log.jsonl")
        lines = [l for l in open(log_path)] if os.path.exists(log_path) else []
        check("decision log written", len(lines) >= 8, "%d lines" % len(lines))

        ok = not FAIL
    except Exception as exc:
        print("EXCEPTION: %s" % exc)
        ok = False
    finally:
        proc.terminate()
        try:
            stderr_tail = proc.stderr.read()[-800:]
        except Exception:
            stderr_tail = ""
        if not ok and stderr_tail:
            print("--- server stderr tail ---")
            print(stderr_tail)

    print("\nsmoke: %d passed, %d failed" % (len(PASS), len(FAIL)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
