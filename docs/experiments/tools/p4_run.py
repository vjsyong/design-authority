#!/usr/bin/env python3
"""P4 session runner — one sandboxed session end to end.

    python3 docs/experiments/tools/p4_run.py --id da-h1 [--root ~/p4-maint]
    python3 docs/experiments/tools/p4_run.py --id base-h1 --skip-agent

Pipeline: preparation (copy + byte-verify from the predecessor seal, reference
layer per condition, wrapper, config) -> bubblewrap sandbox run (opencode,
pinned model) -> budget enforcement (wall 2700 s; 20M token cap) -> post:
process reap, changed-file measurement, leakage scan, seal, run.json.

Evidence discipline: every measured artifact comes from this runner or its
tools, never from agent self-reports.
"""
import argparse
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p4_common import (DEFAULT_MODEL, MATS, P4_ROOT, PYVENV, REPO,  # noqa: E402
                       TOKEN_BUDGET, VENV_PY, WALL_BUDGET_S, read_json,
                       seal_dir, sha256_file, now_iso, run_dir,
                       write_json_atomic)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "seed-evolution", "tools"))
from x05_seal import SEAL_EXCLUDES, create as seal_create, verify as seal_verify  # noqa: E402
from x05_leakscan import scan as leak_scan  # noqa: E402
from x05_run import kill_forensics, reap_ws_processes  # noqa: E402


class P4BudgetMonitor(threading.Thread):
    """Token cap monitor. Binary reads with a manual byte offset: fh.tell()
    inside text-file iteration raises OSError (which an outer guard would
    silently swallow, zeroing the count)."""

    def __init__(self, transcript_path, cap):
        super().__init__(daemon=True)
        self.path = transcript_path
        self.cap = cap
        self.total = 0
        self.steps = 0
        self.capped = False
        self.stop_flag = False
        self._pos = 0

    def run(self):
        while not self.stop_flag:
            try:
                with open(self.path, "rb") as fh:
                    fh.seek(self._pos)
                    for raw in fh:
                        self._pos += len(raw)
                        try:
                            ev = json.loads(raw.decode("utf-8", "replace"))
                        except ValueError:
                            continue
                        if ev.get("type") != "step_finish":
                            continue
                        part = ev.get("part") or {}
                        t = (part.get("tokens") or {}).get("total", 0)
                        self.total += t
                        self.steps += 1
                        if self.total >= self.cap:
                            self.capped = True
            except OSError:
                pass
            time.sleep(4)

OPENCODE = os.path.expanduser("~/.opencode/bin/opencode")
HOME = os.path.expanduser("~")
NODE_DIR = os.path.join(HOME, ".hermes", "tools", "node-26.7.0-linux-x64")
PLAYWRIGHT_CACHE = os.path.join(HOME, ".cache", "ms-playwright")
SANDBOX_PATH = "/opt/py/venv/bin:/opt/node/bin:/usr/local/bin:/usr/bin:/bin"

STRICT_PERMISSION = {
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

GIT_ENV = {"GIT_AUTHOR_NAME": "p4", "GIT_AUTHOR_EMAIL": "p4@local",
           "GIT_COMMITTER_NAME": "p4", "GIT_COMMITTER_EMAIL": "p4@local"}

CONDITION_LINE = {
    "da": ("\nHouse process: this project keeps a design authority and a record. "
           "Follow `reference/PROTOCOL.md`; resolve interface decisions with "
           "`./run-authority` before building, inspect what it gives you, and "
           "file the gaps (see the protocol). If `reference/MIGRATION.md` exists, "
           "work its obligations into this session's changes.\n"),
    "base": ("\nHouse process: follow the design contract in "
             "`reference/DESIGN-DOC.md` and any release notes in `reference/`; "
             "the app's QA conventions are in `QA.md`. Where the contract does "
             "not cover a case, extend the nearest convention and note the "
             "decision in your handoff.\n"),
}


def log(msg):
    print("[%s] %s" % (now_iso(), msg), flush=True)


def git_prep(ws):
    env = dict(os.environ, **GIT_ENV)
    def g(*a):
        return subprocess.run(["git"] + list(a), cwd=ws, env=env,
                              capture_output=True, text=True)
    if not os.path.isdir(os.path.join(ws, ".git")):
        g("init", "-q")
        g("add", "-A")
        g("commit", "-qm", "session start")
    g("config", "user.name", "p4")
    g("config", "user.email", "p4@local")


def chmod_writable(root):
    for dirpath, dirnames, filenames in os.walk(root):
        os.chmod(dirpath, 0o755)
        for f in filenames:
            p = os.path.join(dirpath, f)
            if not os.path.islink(p):
                os.chmod(p, 0o644)


def _relnotes_for(entry):
    k = int(entry.get("k") or 1)
    parts = []
    for i in range(1, k):
        p = os.path.join(MATS, "relnotes", "c%d.md" % i)
        if os.path.isfile(p):
            parts.append(open(p).read().strip())
    if not parts:
        return ("# Release notes\n\nNo design-guidance changes since the last "
                "session. Keep following the design contract.\n")
    return "# Release notes — accumulated guidance changes\n\n" + "\n\n".join(parts) + "\n"


def prep_ws(entry, root, run_dir):
    ws = os.path.join(run_dir, "ws")
    os.makedirs(run_dir, exist_ok=True)
    if os.path.exists(ws):
        shutil.rmtree(ws)
    prev = entry["prev"]
    sdir = seal_dir(prev, root)
    bad, info = seal_verify(sdir)
    if bad:
        raise SystemExit("predecessor seal %s failed verification: %s" % (prev, bad[:3]))
    shutil.copytree(os.path.join(sdir, "tree"), ws, symlinks=True)
    chmod_writable(ws)
    manifest = read_json(os.path.join(sdir, "manifest.json")) or {}
    if not manifest.get("files"):
        raise SystemExit("seal %s has no manifest" % prev)
    got = {}
    from p4_common import hash_tree
    got = hash_tree(ws, excludes=SEAL_EXCLUDES)
    diff = [k for k in manifest["files"] if got.get(k) != manifest["files"][k]]
    if diff:
        raise SystemExit("workspace copy differs from seal %s: %s" % (prev, diff[:5]))

    # condition transforms
    if entry["condition"] == "base":
        for rel in ("run-authority", "audit.jsonl"):
            p = os.path.join(ws, rel)
            if os.path.isdir(p):
                shutil.rmtree(p)
            elif os.path.exists(p):
                os.remove(p)
        rec = os.path.join(ws, ".design-authority")
        if os.path.isdir(rec):
            shutil.rmtree(rec)

    # reference layer
    ref = os.path.join(ws, "reference")
    if os.path.exists(ref):
        shutil.rmtree(ref)
    os.makedirs(ref, exist_ok=True)
    brief_src = os.path.join(MATS, "briefs", entry["brief"])
    shutil.copy2(brief_src, os.path.join(ref, "BRIEF.md"))
    meta = {"brief": entry["brief"], "brief_sha": sha256_file(brief_src),
            "seal_verified": prev}
    if entry["condition"] == "da":
        psrc = os.path.join(MATS, "protocol-rev2.md")
        shutil.copy2(psrc, os.path.join(ref, "PROTOCOL.md"))
        meta["protocol"] = "protocol-rev2.md"
        migrate = os.path.join(run_dir_of(prev, root), "reconcile_migration.md")
        if os.path.isfile(migrate):
            shutil.copy2(migrate, os.path.join(ref, "MIGRATION.md"))
            meta["migration"] = True
    else:
        with open(os.path.join(ref, "RELNOTES.md"), "w") as fh:
            fh.write(_relnotes_for(entry))
        shutil.copy2(os.path.join(MATS, "design-doc.md"),
                     os.path.join(ref, "DESIGN-DOC.md"))

    # wrapper
    if entry.get("wrapper"):
        wsrc = os.path.join(MATS, "wrapper", "run-authority")
        wdst = os.path.join(ws, "run-authority")
        shutil.copy2(wsrc, wdst)
        os.chmod(wdst, 0o755)

    # opencode project config
    cfg = {"$schema": "https://opencode.ai/config.json",
           "model": entry.get("model") or DEFAULT_MODEL,
           "permission": STRICT_PERMISSION}
    with open(os.path.join(ws, "opencode.json"), "w") as fh:
        json.dump(cfg, fh, indent=1)
    git_prep(ws)
    meta["ws_files"] = len(hash_tree(ws, excludes=SEAL_EXCLUDES))
    return ws, meta


def run_dir_of(sid, root):
    return os.path.join(root, "run", sid)


def bwrap_cmd(entry, root, run_dir):
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
    args += ["--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--bind", ws, "/opt/ws",
             "--bind", oc_config, "/opt/oc-config",
             "--ro-bind", os.path.join(HOME, ".opencode"), os.path.join(HOME, ".opencode"),
             "--bind", os.path.join(HOME, ".local/share/opencode"),
             os.path.join(HOME, ".local/share/opencode"),
             "--ro-bind", PYVENV, "/opt/py/venv",
             "--ro-bind", NODE_DIR, "/opt/node",
             "--ro-bind", PLAYWRIGHT_CACHE, "/opt/playwright"]
    if entry.get("da_tools"):
        args += ["--ro-bind", os.path.join(MATS, "da", "tools"), "/opt/da/tools",
                 "--ro-bind", os.path.join(MATS, "da", "kernel"), "/opt/da/kernel"]
    if entry.get("pack_k") is not None:
        pack = os.path.join(MATS, "packs", "p4-da-%d" % entry["pack_k"])
        args += ["--ro-bind", pack, "/opt/da/packs/base"]
    args += ["--unshare-pid", "--unshare-ipc", "--unshare-uts", "--new-session",
             "--die-with-parent", "--clearenv",
             "--setenv", "HOME", HOME,
             "--setenv", "PATH", SANDBOX_PATH,
             "--setenv", "TMPDIR", "/tmp",
             "--setenv", "XDG_CONFIG_HOME", "/opt/oc-config",
             "--setenv", "PLAYWRIGHT_BROWSERS_PATH", "/opt/playwright",
             "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
             "--setenv", "LANG", "C.UTF-8",
             "--chdir", "/opt/ws"]
    if entry.get("da_tools"):
        args += ["--setenv", "DA_PACK", "/opt/da/packs/base"]
    return args


def measure_changes(ws):
    env = dict(os.environ, **GIT_ENV)
    subprocess.run(["git", "add", "-A"], cwd=ws, env=env, capture_output=True)
    numstat = subprocess.run(["git", "diff", "--cached", "--numstat"], cwd=ws,
                             env=env, capture_output=True, text=True).stdout
    files, added, deleted = 0, 0, 0
    for line in numstat.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            files += 1
            try:
                added += int(parts[0]); deleted += int(parts[1])
            except ValueError:
                pass
    commits = subprocess.run(["git", "log", "--oneline"], cwd=ws, env=env,
                             capture_output=True, text=True).stdout.strip().splitlines()
    return {"changed_files": files, "added": added, "deleted": deleted,
            "commit_count": len(commits)}


def transcript_stats(path):
    kinds = Counter()
    total = 0
    tokens = 0
    steps = 0
    if not os.path.exists(path):
        return {"events": 0, "kinds": {}, "tokens_total": 0, "steps": 0}
    with open(path, "rb") as fh:
        for raw in fh:
            try:
                ev = json.loads(raw.decode("utf-8", "replace"))
            except ValueError:
                continue
            total += 1
            if ev.get("type") == "tool_use":
                part = ev.get("part") or {}
                kinds[part.get("tool") or "?"] += 1
            elif ev.get("type") == "step_finish":
                part = ev.get("part") or {}
                tokens += (part.get("tokens") or {}).get("total", 0)
                steps += 1
    return {"events": total, "kinds": dict(kinds), "tokens_total": tokens, "steps": steps}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--root", default=P4_ROOT)
    ap.add_argument("--skip-agent", action="store_true")
    ap.add_argument("--budget", type=int, default=None)
    args = ap.parse_args(argv)

    root = os.path.abspath(os.path.expanduser(args.root))
    schedule = read_json(os.path.join(root, "schedule.json")) or {}
    entry = next((s for s in schedule.get("sessions", []) if s["id"] == args.id), None)
    if entry is None:
        raise SystemExit("session %s not in schedule" % args.id)
    budget_wall = args.budget or entry.get("budget_wall") or WALL_BUDGET_S
    budget_tokens = entry.get("budget_tokens") or TOKEN_BUDGET

    rd = run_dir_of(args.id, root)
    run_path = os.path.join(rd, "run.json")
    if os.path.exists(run_path) and not args.skip_agent:
        raise SystemExit("run already exists: %s" % run_path)
    os.makedirs(rd, exist_ok=True)
    run = {"id": args.id, "kind": entry.get("kind"), "condition": entry.get("condition"),
           "chain": entry.get("chain"), "k": entry.get("k"),
           "model": entry.get("model") or DEFAULT_MODEL,
           "started": now_iso(), "status": "running",
           "budget": {"wall_s": budget_wall, "tokens": budget_tokens}}

    def save():
        write_json_atomic(run_path, run)

    save()
    ws, meta = prep_ws(entry, root, rd)
    run["prep"] = meta
    save()
    log("prep %s done (ws files=%d, brief=%s)" % (args.id, meta.get("ws_files"), meta.get("brief")))

    if args.skip_agent:
        run["status"] = "skipped (rehearsal)"
        save()
        log("skip-agent rehearsal complete for %s" % args.id)
        return 0

    transcript = os.path.join(rd, "transcript.jsonl")
    cmd = bwrap_cmd(entry, root, rd)
    prompt = open(os.path.join(ws, "reference", "BRIEF.md")).read() + CONDITION_LINE[entry["condition"]]
    prompt_file = os.path.join(rd, "prompt.txt")
    with open(prompt_file, "w") as fh:
        fh.write(prompt)
    run["prompt_file"] = os.path.basename(prompt_file)
    cmd += [OPENCODE, "run", "--pure", "-m", run["model"], "--title", "p4-" + args.id,
            "--format", "json"]
    monitor = P4BudgetMonitor(transcript, budget_tokens)
    monitor.start()
    t0 = time.time()
    timed_out, capped = False, False
    with open(transcript, "w") as tout, \
            open(os.path.join(rd, "opencode-stderr.log"), "w") as terr, \
            open(prompt_file) as pin:
        proc = subprocess.Popen(cmd, cwd=ws, stdout=tout, stderr=terr, stdin=pin,
                                start_new_session=True)
        while True:
            rc = proc.poll()
            if rc is not None:
                break
            if monitor.capped:
                capped = True
                break
            if time.time() - t0 > budget_wall:
                timed_out = True
                break
            time.sleep(2)
        if proc.poll() is None:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except Exception:
                pass
            try:
                proc.wait(timeout=15)
            except Exception:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except Exception:
                    pass
                proc.wait()
        rc = proc.returncode if not (timed_out or capped) else ("cap" if capped else "timeout")
    wall = round(time.time() - t0, 1)
    monitor.stop_flag = True
    killed = reap_ws_processes(ws)
    kills = kill_forensics(transcript)
    if kills:
        run["self_kill_commands"] = kills[:5]

    run["wall_s"] = wall
    run["rc"] = rc
    run["capped"] = capped
    run["reaped_processes"] = killed
    ts = transcript_stats(transcript)
    run["transcript"] = ts
    run["tokens_total"] = ts["tokens_total"]
    run["steps"] = ts["steps"]
    run["changes"] = measure_changes(ws)

    # transient staging (validator tmp packs) must not enter the seal
    shutil.rmtree(os.path.join(ws, ".tmp-pack"), ignore_errors=True)

    # leakage containment scan
    all_ids = [s["id"] for s in schedule.get("sessions", [])]
    try:
        scan = leak_scan(transcript, args.id, all_ids)
        run["leakscan"] = scan
    except Exception as exc:
        run["leakscan"] = {"error": str(exc)[:200]}

    # seal
    seal_create(ws, args.id, root=root)
    bad, info = seal_verify(seal_dir(args.id, root))
    run["seal"] = {"files": (info or {}).get("file_count"), "verified": not bad}
    if bad:
        run["seal"]["bad"] = bad[:5]
    run["status"] = "ok" if (rc == 0 and not bad) else ("timeout" if timed_out else
                                                        "capped" if capped else "failed")
    run["finished"] = now_iso()
    save()
    log("session %s done: status=%s rc=%s wall=%ss tokens=%s files=%s" %
        (args.id, run["status"], rc, wall, run["tokens_total"], run["changes"]["changed_files"]))
    return 0 if run["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
