#!/usr/bin/env python3
"""x06_run — the independent adoption test (da_nextsteps.md section 4).

A fresh, sandboxed opencode session gets: an empty working directory, network
access, and ONE instruction file (BRIEF.md). It must independently discover
the public repository, set it up, build the briefed app under it, handle an
undefined requirement, verify its work, and report. No internal materials,
tools, packs, da-configs, or walkthroughs are mounted; the repository only
reaches it the way it reaches any stranger: a public git clone.

    python3 docs/experiments/tools/x06_run.py --root ~/x06-adoption --run-id run1 [--timeout 4500]

The workspace, transcript, and prompt land under <root>/<run-id>/. Nothing is
deleted; invalid runs stay archived.
"""
import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
BRIEF = os.path.join(REPO, "docs", "experiments", "adoption", "BRIEF.md")

OPENCODE = os.path.expanduser("~/.opencode/bin/opencode")
HOME = os.path.expanduser("~")
NODE_DIR = os.path.join(HOME, ".hermes", "tools", "node-26.7.0-linux-x64")
PLAYWRIGHT_CACHE = os.path.join(HOME, ".cache", "ms-playwright")
MODEL = "deepseek/deepseek-flash"  # pinned, same as the x05 program
SANDBOX_PATH = "/opt/node/bin:/usr/local/bin:/usr/bin:/bin"

PERMISSION = {
    "external_directory": {"*": "deny", "/tmp/*": "allow", "/tmp/**": "allow"},
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


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())


def bwrap_cmd(run_dir):
    """Adoption-shaped sandbox: no /opt/da, no pack mounts, no pyvenv."""
    ws = os.path.join(run_dir, "ws")
    oc_config = os.path.join(run_dir, "oc-config")
    os.makedirs(oc_config, exist_ok=True)
    args = ["bwrap",
            "--ro-bind", "/usr", "/usr",
            "--ro-bind", "/etc", "/etc",
            "--ro-bind", "/bin", "/bin",
            "--ro-bind", "/sbin", "/sbin"]
    for lib in ("/lib", "/lib64", "/lib32", "/libx32"):
        if os.path.exists(lib):
            args += ["--ro-bind", lib, lib]
    args += [
        "--proc", "/proc",
        "--dev", "/dev",
        "--tmpfs", "/tmp",
        "--bind", ws, "/opt/ws",
        "--bind", oc_config, "/opt/oc-config",
        "--ro-bind", os.path.join(HOME, ".opencode"), os.path.join(HOME, ".opencode"),
        "--bind", os.path.join(HOME, ".local/share/opencode"),
        os.path.join(HOME, ".local/share/opencode"),
        "--ro-bind", NODE_DIR, "/opt/node",
        "--ro-bind", PLAYWRIGHT_CACHE, "/opt/playwright",
        "--unshare-pid", "--unshare-ipc", "--unshare-uts", "--new-session",
        "--die-with-parent",
        "--clearenv",
        "--setenv", "HOME", HOME,
        "--setenv", "PATH", SANDBOX_PATH,
        "--setenv", "TMPDIR", "/tmp",
        "--setenv", "XDG_CONFIG_HOME", "/opt/oc-config",
        "--setenv", "PLAYWRIGHT_BROWSERS_PATH", "/opt/playwright",
        "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
        "--setenv", "LANG", "C.UTF-8",
        "--chdir", "/opt/ws",
    ]
    return args


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.expanduser("~/x06-adoption"))
    ap.add_argument("--run-id", default="run1")
    ap.add_argument("--timeout", type=int, default=4500)
    ap.add_argument("--dry-run", action="store_true", help="prep only, no agent")
    args = ap.parse_args(argv)

    run_dir = os.path.join(os.path.expanduser(args.root), args.run_id)
    if os.path.exists(os.path.join(run_dir, "run.json")):
        raise SystemExit("run already exists: %s" % run_dir)
    ws = os.path.join(run_dir, "ws")
    os.makedirs(ws, exist_ok=True)

    # the brief is the ONE instruction file the agent gets
    shutil.copy2(BRIEF, os.path.join(ws, "BRIEF.md"))
    with open(os.path.join(ws, "opencode.json"), "w") as fh:
        json.dump({"$schema": "https://opencode.ai/config.json",
                   "model": MODEL, "permission": PERMISSION}, fh, indent=1)

    run = {"id": args.run_id, "kind": "adoption-test", "model": MODEL,
           "started": now_iso(), "status": "running",
           "brief": os.path.relpath(BRIEF, REPO), "timeout_s": args.timeout,
           "sandbox": "bubblewrap (no internal mounts)", "ws": ws}
    with open(os.path.join(run_dir, "run.json"), "w") as fh:
        json.dump(run, fh, indent=1)

    if args.dry_run:
        print("prepped (dry run): %s" % run_dir)
        return 0

    transcript = os.path.join(run_dir, "transcript.jsonl")
    prompt_file = os.path.join(run_dir, "prompt.txt")
    with open(BRIEF) as fh, open(prompt_file, "w") as out:
        # the prompt IS the brief; stdin only, never argv (self-kill guard)
        out.write(fh.read())
    cmd = bwrap_cmd(run_dir) + [OPENCODE, "run", "--pure", "-m", MODEL,
                                "--title", "x06-adoption", "--format", "json"]
    t0 = time.time()
    timed_out = False
    with open(transcript, "w") as tout, \
            open(os.path.join(run_dir, "opencode-stderr.log"), "w") as terr, \
            open(prompt_file) as pin:
        proc = subprocess.Popen(cmd, cwd=ws, stdout=tout, stderr=terr,
                                stdin=pin, start_new_session=True)
        while proc.poll() is None:
            if time.time() - t0 > args.timeout:
                timed_out = True
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                except ProcessLookupError:
                    pass
                time.sleep(5)
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except ProcessLookupError:
                    pass
                break
            time.sleep(5)
    rc = proc.poll()
    run.update({"status": "timed_out" if timed_out else "completed",
                "exit": rc, "wall_s": round(time.time() - t0, 1),
                "finished": now_iso()})
    # quick completeness probe (evaluation proper is a separate pass)
    run["done_md"] = os.path.exists(os.path.join(ws, "DONE.md"))
    run["ws_entries"] = sorted(os.listdir(ws))
    with open(os.path.join(run_dir, "run.json"), "w") as fh:
        json.dump(run, fh, indent=1)
    print(json.dumps(run, indent=1))
    return 0 if rc == 0 and not timed_out else 1


if __name__ == "__main__":
    sys.exit(main())
