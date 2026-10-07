#!/usr/bin/env python3
"""Run one benchmark condition end-to-end (sandboxed).

    python3 run_condition.py --condition B --run-id b1 [--model M] [--timeout S]
    python3 run_condition.py --condition A --run-id atest --skip-agent   # pipeline test

Pipeline: materials -> sandboxed opencode agent run -> serve -> capture ->
interact -> scan -> run.json.

Containment (learned the hard way — see docs/06 §Deviations):
  * the workspace lives OUTSIDE the repo, under RUNS_ROOT (default /tmp/da-ws)
  * the agent runs inside bubblewrap with a minimal filesystem: /usr, /etc,
    /bin, /sbin, /lib*, /proc, /dev, a tmpfs /tmp with the run dir bound back,
    ~/.opencode, ~/.local/share/opencode, ~/.hermes/tools and the project
    .venv (+ tools/kernel/packs for condition C). The benchmark repo, other
    home data and sibling runs are invisible; external access fails at the
    filesystem level, not by permission policy alone.
  * opencode gets a per-run XDG_CONFIG_HOME (no global skills/plugins/agents)
    plus strict permissions (skill/webfetch/websearch/external_directory deny)
  * the transcript is audited for references outside the sandbox
"""
import argparse
import json
import os
import shutil
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
RUNS_ROOT = os.environ.get("DA_BENCH_RUNS_ROOT", "/tmp/da-ws")
HOME = os.path.expanduser("~")
NODE_BIN = os.path.join(HOME, ".hermes/tools/node-26.7.0-linux-x64/bin")
SANDBOX_PATH = "%s:%s:/usr/local/bin:/usr/bin:/bin" % (
    os.path.join(ROOT, ".venv", "bin"), NODE_BIN)

STRICT_PERMISSION = {
    "external_directory": {"*": "deny"},
    "skill": {"*": "deny"},
    "webfetch": "deny",
    "websearch": "deny",
    "question": "deny",
    "edit": {"*": "allow"},
    "bash": {"*": "allow"},
    "read": {"*": "allow"},
    "glob": {"*": "allow"},
    "grep": {"*": "allow"},
}

# condition C needs the authority server + pack reachable inside the sandbox
SANDBOX_RO_C = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "kernel"),
                os.path.join(ROOT, "packs")]


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


def bwrap_cmd(run_root, ws, condition):
    """Minimal-filesystem sandbox around the agent run."""
    args = [
        "bwrap",
        "--ro-bind", "/usr", "/usr",
        "--ro-bind", "/etc", "/etc",
        "--ro-bind", "/bin", "/bin",
        "--ro-bind", "/sbin", "/sbin",
    ]
    for lib in ("/lib", "/lib64", "/lib32", "/libx32"):
        if os.path.exists(lib):
            args += ["--ro-bind", lib, lib]
    args += [
        "--proc", "/proc",
        "--dev", "/dev",
        "--tmpfs", "/tmp",
        "--bind", run_root, run_root,
        "--ro-bind", os.path.join(HOME, ".opencode"), os.path.join(HOME, ".opencode"),
        "--bind", os.path.join(HOME, ".local/share/opencode"),
        os.path.join(HOME, ".local/share/opencode"),
        "--ro-bind", os.path.join(HOME, ".hermes/tools"),
        os.path.join(HOME, ".hermes/tools"),
        "--ro-bind", os.path.join(ROOT, ".venv"), os.path.join(ROOT, ".venv"),
        "--die-with-parent",
    ]
    if condition == "C":
        for path in SANDBOX_RO_C:
            args += ["--ro-bind", path, path]
    args += [
        "--setenv", "HOME", HOME,
        "--setenv", "XDG_CONFIG_HOME", os.path.join(run_root, "oc-config"),
        "--setenv", "PATH", SANDBOX_PATH,
        "--chdir", ws,
        "--",
        OPENCODE, "run", "--pure",
    ]
    return args


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
            t = ev.get("type") or "?"
            types[t] += 1
            if t == "tool_use":
                part = ev.get("part") or {}
                tools[str(part.get("tool") or "?")] += 1
    return {"events": n, "tool_calls": sum(tools.values()), "tools": dict(tools),
            "event_types": dict(types)}


SANDBOX_TRIPWIRES = ("/home/xrim/design-authority/benchmark",
                     "/home/xrim/design-authority/packs",
                     "/home/xrim/design-authority/kernel",
                     "/home/xrim/design-authority/tools",
                     "/home/xrim/triage-design-system",
                     "/home/xrim/.claude/skills",
                     "/home/xrim/.agents/skills")


def containment_audit(transcript_path):
    """Tripwire audit. `attempts` = protected-path references inside tool
    INPUTS (the signal that matters); `mentions` = any other occurrence in the
    transcript (results, permission text — informational)."""
    if not os.path.exists(transcript_path):
        return {"attempts": 0, "mentions": 0, "denied_events": 0}
    attempts, mentions, denied = 0, 0, 0
    with open(transcript_path) as fh:
        for line in fh:
            for pat in SANDBOX_TRIPWIRES:
                mentions += line.count(pat)
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") != "tool_use":
                continue
            st = ev.get("part", {}).get("state", {}) or {}
            inp = json.dumps(st.get("input") or {})
            for pat in SANDBOX_TRIPWIRES:
                attempts += inp.count(pat)
            err = str(st.get("error") or "").lower()
            if st.get("status") == "error" and (
                    "denied" in err or "permission" in err or "prevents" in err):
                denied += 1
    return {"attempts": attempts, "mentions": mentions, "denied_events": denied}


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


def kill_ws_processes(ws):
    """Kill stray processes whose cwd is inside the workspace (agent servers)."""
    victims = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit() or int(pid) == os.getpid():
            continue
        try:
            cwd = os.readlink("/proc/%s/cwd" % pid)
        except Exception:
            continue
        if cwd == ws or cwd.startswith(ws + os.sep):
            victims.append(int(pid))
    for sig in (15, 9):
        for pid in list(victims):
            try:
                os.kill(pid, sig)
            except Exception:
                victims.remove(pid)
                continue
        if not victims:
            break
        time.sleep(0.5)
    return len(victims)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", required=True, choices=["A", "B", "C"])
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--model", default="deepseek/deepseek-flash")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--skip-agent", action="store_true")
    ap.add_argument("--no-sandbox", action="store_true",
                    help="debugging only — run opencode without bwrap")
    ap.add_argument("--prompt-file", default=None,
                    help="override the brief prompt (smoke tests)")
    args = ap.parse_args(argv)

    run_dir = os.path.join(ROOT, "benchmark", "runs", args.run_id)
    run_root = os.path.join(RUNS_ROOT, args.run_id)
    ws = os.path.join(run_root, "ws")
    os.makedirs(run_dir, exist_ok=True)
    if os.path.exists(run_root):
        shutil.rmtree(run_root)
    os.makedirs(os.path.join(run_root, "oc-config"), exist_ok=True)

    run = {"run_id": args.run_id, "condition": args.condition, "model": args.model,
           "started": now_iso(), "status": "running"}
    run_path = os.path.join(run_dir, "run.json")

    def save():
        with open(run_path, "w") as fh:
            json.dump(run, fh, indent=1)

    manifest = build(args.condition, ws)
    run["materials"] = {"starter_commit": manifest["starter_commit"]}
    with open(os.path.join(run_dir, "materials.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)

    if args.prompt_file:
        with open(args.prompt_file) as fh:
            prompt = fh.read()
    else:
        prompt = open(os.path.join(ROOT, "benchmark", "briefs", "base.md")).read()
        prompt += "\n\n" + open(os.path.join(
            ROOT, "benchmark", "briefs", "condition-%s.md" % args.condition.lower())).read()
    with open(os.path.join(run_dir, "prompt.md"), "w") as fh:
        fh.write(prompt)

    cfg = {"$schema": "https://opencode.ai/config.json", "model": args.model,
           "permission": STRICT_PERMISSION}
    if args.condition == "C":
        cfg["mcp"] = {"design_authority": {
            "type": "local",
            "command": [VENV_PY, os.path.join(ROOT, "tools", "da-mcp.py")],
            "environment": {"DA_WORKSPACE": ws},
            "enabled": True}}
    with open(os.path.join(ws, "opencode.json"), "w") as fh:
        json.dump(cfg, fh, indent=1)

    sandboxed = not args.no_sandbox and shutil.which("bwrap") is not None
    run["isolation"] = {"sandbox": "bwrap" if sandboxed else "none",
                        "runs_root": run_root,
                        "xdg_config_home": os.path.join(run_root, "oc-config"),
                        "permissions": "strict"}

    # ---- agent run ----
    if args.skip_agent:
        run["opencode"] = {"skipped": True}
    else:
        t0, timed_out, rc = time.time(), False, None
        cmd = (bwrap_cmd(run_root, ws, args.condition) if sandboxed
               else [OPENCODE, "run", "--pure"])
        cmd += ["-m", args.model, "--title", "bench-" + args.run_id,
                "--format", "json", prompt]
        with open(os.path.join(run_dir, "transcript.jsonl"), "w") as transcript, \
                open(os.path.join(run_dir, "opencode-stderr.log"), "w") as stderr:
            try:
                proc = subprocess.run(cmd, cwd=ws, stdout=transcript, stderr=stderr,
                                      timeout=args.timeout)
                rc = proc.returncode
            except subprocess.TimeoutExpired:
                rc, timed_out = "timeout", True
        run["opencode"] = {"exit": rc, "timed_out": timed_out,
                           "duration_s": round(time.time() - t0, 1),
                           "sandboxed": sandboxed}
        run["opencode"].update(tool_stats(os.path.join(run_dir, "transcript.jsonl")))
        run["containment"] = containment_audit(os.path.join(run_dir, "transcript.jsonl"))
        run["authority"] = authority_stats(ws)
        run["cleanup_agent_procs"] = kill_ws_processes(ws)
    save()

    # ---- serve + capture + interact (outside the sandbox) ----
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
        run["cleanup_serve_procs"] = kill_ws_processes(ws)

    # ---- static scan + archive copy of the workspace ----
    subprocess.run([VENV_PY, os.path.join(HERE, "scan.py"),
                    "--ws", ws, "--out", os.path.join(run_dir, "scan.json")],
                   check=False)
    run["scan"] = "scan.json"
    archive = os.path.join(run_dir, "ws")
    if os.path.exists(archive):
        shutil.rmtree(archive)
    shutil.copytree(ws, archive, symlinks=True)
    run["finished"] = now_iso()
    run["status"] = "ok"
    save()
    oc = run.get("opencode") or {}
    print("run %s (%s): exit=%s duration=%ss interact=%s containment=%s"
          % (args.run_id, args.condition, oc.get("exit"), oc.get("duration_s"),
             run.get("interact"), run.get("containment")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
