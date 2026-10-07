#!/usr/bin/env python3
"""Run the Orbit agent build test (portability spike, Phase 6).

    python3 orbit_run.py --run-id orbit-a1 [--timeout 2400]

A fresh opencode agent receives ONLY: the Depot brief, the Orbit authority
(via MCP at /opt/da/packs/orbit), and the shared Design Authority interface.
Triage is not present anywhere in the sandbox (only packs/orbit is mounted).

Pipeline: stage starter + filtered tools -> sandboxed agent run -> serve ->
capture -> interact -> stats -> run.json (all under benchmark/runs/<id>/).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

from run_condition import (  # noqa: E402
    OPENCODE, VENV_PY, HOME, SANDBOX_PATH, STRICT_PERMISSION, SANDBOX_MOUNTS,
    now_iso, free_port, wait_http, tool_stats, token_stats, containment_audit,
    authority_stats, kill_ws_processes,
)

STARTER = os.path.join(ROOT, "examples", "orbit-reference-app")
RUNS_STAGE = "/tmp/da-orbit"


def bwrap_cmd(run_root, ws):
    """Sandbox: only the Orbit pack, a filtered da-tools dir and the kernel
    are visible under /opt/da — Triage exists nowhere in this sandbox."""
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
        "--die-with-parent",
    ]
    for src, dest in SANDBOX_MOUNTS:
        args += ["--ro-bind", src, dest]
    args += [
        "--ro-bind", os.path.join(ROOT, "kernel"), "/opt/da/kernel",
        "--ro-bind", os.path.join(run_root, "da-tools"), "/opt/da/tools",
        "--ro-bind", os.path.join(ROOT, "packs", "orbit"), "/opt/da/packs/orbit",
        "--clearenv",
        "--setenv", "HOME", HOME,
        "--setenv", "PATH", SANDBOX_PATH,
        "--setenv", "TMPDIR", "/tmp",
        "--setenv", "XDG_CONFIG_HOME", os.path.join(run_root, "oc-config"),
        "--setenv", "PLAYWRIGHT_BROWSERS_PATH", "/opt/playwright",
        "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
        "--setenv", "LANG", "C.UTF-8",
        "--chdir", ws,
        "--",
        OPENCODE, "run", "--pure",
    ]
    return args


def triage_mentions(transcript_path):
    """How often the word 'triage' appears anywhere in the transcript."""
    if not os.path.exists(transcript_path):
        return 0
    n = 0
    with open(transcript_path, errors="ignore") as fh:
        for line in fh:
            n += line.lower().count("triage")
    return n


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", default="orbit-a1")
    ap.add_argument("--model", default="deepseek/deepseek-flash")
    ap.add_argument("--timeout", type=int, default=2400)
    ap.add_argument("--no-sandbox", action="store_true")
    args = ap.parse_args(argv)

    run_dir = os.path.join(ROOT, "benchmark", "runs", args.run_id)
    run_root = os.path.join(RUNS_STAGE, args.run_id)
    ws = os.path.join(run_root, "ws")
    os.makedirs(run_dir, exist_ok=True)
    if os.path.exists(run_root):
        shutil.rmtree(run_root)
    os.makedirs(os.path.join(run_root, "oc-config"), exist_ok=True)

    run = {"run_id": args.run_id, "kind": "orbit-build", "model": args.model,
           "started": now_iso(), "status": "running"}
    run_path = os.path.join(run_dir, "run.json")

    def save():
        with open(run_path, "w") as fh:
            json.dump(run, fh, indent=1)

    # ---- stage workspace + filtered tools ----
    shutil.copytree(STARTER, ws)
    os.rename(os.path.join(ws, "brief.md"), os.path.join(ws, "BRIEF.md"))
    da_tools = os.path.join(run_root, "da-tools")
    os.makedirs(da_tools)
    shutil.copy2(os.path.join(ROOT, "tools", "da-mcp.py"), da_tools)
    run["staged"] = {"starter": STARTER, "ws": ws}

    prompt = open(os.path.join(STARTER, "brief.md")).read()
    with open(os.path.join(run_dir, "prompt.md"), "w") as fh:
        fh.write(prompt)

    cfg = {"$schema": "https://opencode.ai/config.json", "model": args.model,
           "permission": STRICT_PERMISSION,
           "mcp": {"design_authority": {
               "type": "local",
               "command": ["/opt/py/venv/bin/python3", "/opt/da/tools/da-mcp.py"],
               "environment": {"DA_WORKSPACE": ws, "DA_PACK": "/opt/da/packs/orbit"},
               "enabled": True}}}
    with open(os.path.join(ws, "opencode.json"), "w") as fh:
        json.dump(cfg, fh, indent=1)

    sandboxed = not args.no_sandbox and shutil.which("bwrap") is not None
    run["isolation"] = {"sandbox": "bwrap" if sandboxed else "none",
                        "mounts": "orbit pack only (no triage)", "permissions": "strict"}

    # ---- agent run ----
    t0, timed_out, rc = time.time(), False, None
    cmd = (bwrap_cmd(run_root, ws) if sandboxed
           else [OPENCODE, "run", "--pure"])
    cmd += ["-m", args.model, "--title", "orbit-" + args.run_id,
            "--format", "json", prompt]
    transcript = os.path.join(run_dir, "transcript.jsonl")
    with open(transcript, "w") as fh_out, \
            open(os.path.join(run_dir, "opencode-stderr.log"), "w") as stderr:
        try:
            proc = subprocess.run(cmd, cwd=ws, stdout=fh_out, stderr=stderr,
                                  timeout=args.timeout)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            rc, timed_out = "timeout", True
    run["opencode"] = {"exit": rc, "timed_out": timed_out,
                       "duration_s": round(time.time() - t0, 1), "sandboxed": sandboxed}
    run["opencode"].update(tool_stats(transcript))
    run["opencode"]["tokens"] = token_stats(transcript)
    run["containment"] = containment_audit(transcript)
    run["containment"]["triage_word_mentions"] = triage_mentions(transcript)
    run["authority"] = authority_stats(ws)
    run["cleanup_agent_procs"] = kill_ws_processes(ws)
    save()

    # ---- serve + capture + interact ----
    port = free_port(8300)
    server = subprocess.Popen(
        [VENV_PY, "app.py", "--port", str(port)], cwd=ws,
        stdout=open(os.path.join(run_dir, "server.log"), "w"),
        stderr=subprocess.STDOUT)
    url = "http://127.0.0.1:%d" % port
    try:
        if not wait_http(url + "/healthz"):
            run["serve"] = {"error": "healthz never came up"}
        else:
            run["serve"] = {"port": port, "ok": True}
            subprocess.run([VENV_PY, os.path.join(HERE, "orbit_capture.py"),
                            "--url", url, "--out", os.path.join(run_dir, "capture")],
                           check=False)
            run["capture"] = "capture/"
            subprocess.run([VENV_PY, os.path.join(HERE, "orbit_interact.py"),
                            "--url", url, "--out", os.path.join(run_dir, "interact.json")],
                           check=False)
            interact_out = os.path.join(run_dir, "interact.json")
            if os.path.exists(interact_out):
                with open(interact_out) as fh:
                    res = (json.load(fh) or {}).get("result", {})
                run["interact"] = {"passed": res.get("passed"), "total": res.get("total")}
    except Exception as exc:
        run["serve"] = {"error": str(exc)[:300]}
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except Exception:
            server.kill()
        run["cleanup_serve_procs"] = kill_ws_processes(ws)

    # ---- archive the workspace ----
    archive = os.path.join(run_dir, "ws")
    if os.path.exists(archive):
        shutil.rmtree(archive)
    shutil.copytree(ws, archive, symlinks=True)
    run["finished"] = now_iso()
    run["status"] = "ok"
    save()
    oc = run.get("opencode") or {}
    print("run %s: exit=%s duration=%ss interact=%s tok=%s"
          % (args.run_id, oc.get("exit"), oc.get("duration_s"),
             run.get("interact"), (oc.get("tokens") or {}).get("total")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
