#!/usr/bin/env python3
"""x05 session runner — one sandboxed session end to end.

    x05_run.py --id f1 [--root /home/xrim/x05]
    x05_run.py --id pilot-a --pilot --condition A --budget 300

Pipeline (plan §6.2):
  preparation (copy + byte-verify against the predecessor seal, brief, wrapper)
  -> bubblewrap sandbox run (opencode, pinned model, one session at a time)
  -> budget enforcement (wall 2700 s; token cap 20M sum_total, monitored)
  -> post-session: containment audit, serve + capture, extraction, census,
     seal, run.json, state.json append.

Evidence discipline: every measured artifact comes from this runner or its
tools, never from agent self-reports.
"""
import argparse
import fcntl
import glob
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from collections import Counter
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from x05_common import (ANNEXES, DEFAULT_MODEL, REPO, TOKEN_BUDGET,  # noqa: E402
                        VENV_PY, WALL_BUDGET_S, X05_ROOT, append_jsonl,
                        hash_tree, load_state, now_iso, read_json, save_state,
                        sha256_file, StateLock, write_json_atomic)
from x05_seal import SEAL_EXCLUDES, create as seal_create, verify as seal_verify  # noqa: E402
from x05_leakscan import scan as leak_scan  # noqa: E402

OPENCODE = os.path.expanduser("~/.opencode/bin/opencode")
HOME = os.path.expanduser("~")
NODE_DIR = os.path.join(HOME, ".hermes", "tools", "node-26.7.0-linux-x64")
PYTOOLCHAIN = sorted(glob.glob(os.path.join(
    HOME, ".hermes", "tools", "python-*-linux-x64")))[-1]
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

GIT_ENV = {"GIT_AUTHOR_NAME": "x05", "GIT_AUTHOR_EMAIL": "x05@local",
           "GIT_COMMITTER_NAME": "x05", "GIT_COMMITTER_EMAIL": "x05@local"}


def log(msg):
    print("[%s] %s" % (now_iso(), msg), flush=True)


def free_port(start=8560):
    for port in range(start, start + 300):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("no free port")


# ---------------------------------------------------------------------- prep
def git_prep(ws):
    env = dict(os.environ, **GIT_ENV)
    def g(*a):
        return subprocess.run(["git"] + list(a), cwd=ws, env=env,
                              capture_output=True, text=True)
    if not os.path.isdir(os.path.join(ws, ".git")):
        g("init", "-q")
        g("add", "-A")
        g("commit", "-qm", "starter")
    g("config", "user.name", "x05")
    g("config", "user.email", "x05@local")


def chmod_writable(root):
    for dirpath, dirnames, filenames in os.walk(root):
        os.chmod(dirpath, 0o755)
        for f in filenames:
            p = os.path.join(dirpath, f)
            if not os.path.islink(p):
                os.chmod(p, 0o644)


def prep_ws(entry, root, run_dir):
    """Build run/<id>/ws from the entry's input. Returns prep metadata."""
    ws = os.path.join(run_dir, "ws")
    mats = entry.get("_materials") or os.path.join(root, "materials")
    os.makedirs(run_dir, exist_ok=True)
    if os.path.exists(ws):
        shutil.rmtree(ws)
    meta = {"input": entry.get("input"), "condition": entry.get("condition")}
    mode = entry.get("input_mode")
    if mode == "starter":
        shutil.copytree(os.path.join(mats, "starter"), ws)
    elif mode == "seal":
        prev = entry["prev"]
        seal_dir = os.path.join(root, "seal", prev)
        bad, _ = seal_verify(seal_dir)
        if bad:
            raise SystemExit("predecessor seal %s failed verification: %s"
                             % (prev, bad[:3]))
        shutil.copytree(os.path.join(seal_dir, "tree"), ws)
        chmod_writable(ws)
        # byte-verify the copy against the seal manifest (before transforms)
        manifest = read_json(os.path.join(seal_dir, "manifest.json")) or {}
        if not manifest.get("files"):
            raise SystemExit("seal %s has no manifest" % prev)
        got = hash_tree(ws, excludes=SEAL_EXCLUDES)
        diff = [k for k in manifest["files"] if got.get(k) != manifest["files"][k]]
        if diff:
            raise SystemExit("workspace copy differs from seal %s: %s"
                             % (prev, diff[:5]))
        meta["seal_verified"] = prev
        # condition transform: A never sees records (code + history only)
        if entry.get("kind") == "handoff" and entry.get("condition") == "A":
            rec = os.path.join(ws, ".design-authority")
            if os.path.isdir(rec):
                shutil.rmtree(rec)
    else:
        raise SystemExit("bad input_mode %r" % mode)

    # reference layer (never sealed)
    ref = os.path.join(ws, "reference")
    os.makedirs(ref, exist_ok=True)
    brief_src = os.path.join(mats, "briefs", entry["brief"])
    shutil.copy2(brief_src, os.path.join(ref, "BRIEF.md"))
    meta["brief"] = entry["brief"]
    meta["brief_sha"] = sha256_file(brief_src)
    if entry.get("protocol"):
        shutil.copy2(os.path.join(mats, "protocol.md"),
                     os.path.join(ref, "PROTOCOL.md"))
    for extra in entry.get("reference_extra", []) or []:
        src = os.path.join(mats, extra)
        dst = os.path.join(ref, os.path.basename(extra))
        shutil.copy2(src, dst)
    for extra in entry.get("extra_files", []) or []:
        src = os.path.join(root, extra["src"])
        dst = os.path.join(ref, extra["dst"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    # frozen current-state screenshots from the predecessor's capture
    if entry.get("prev"):
        prev_screens = os.path.join(root, "run", entry["prev"], "capture", "screens")
        if os.path.isdir(prev_screens):
            dst = os.path.join(ref, "screens")
            os.makedirs(dst, exist_ok=True)
            for f in sorted(os.listdir(prev_screens)):
                shutil.copy2(os.path.join(prev_screens, f),
                             os.path.join(dst, f))
            meta["screens"] = len(os.listdir(dst))
    # authority wrapper (audited CLI) for formation + B/C sessions
    if entry.get("wrapper"):
        wsrc = os.path.join(mats, "wrapper", "run-authority")
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


# -------------------------------------------------------------------- sandbox
def bwrap_cmd(entry, root, run_dir):
    ws = os.path.join(run_dir, "ws")
    oc_config = os.path.join(run_dir, "oc-config")
    mats = entry.get("_materials") or os.path.join(root, "materials")
    os.makedirs(oc_config, exist_ok=True)
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
        "--bind", ws, "/opt/ws",
        "--bind", oc_config, "/opt/oc-config",
        "--ro-bind", os.path.join(HOME, ".opencode"), os.path.join(HOME, ".opencode"),
        "--bind", os.path.join(HOME, ".local/share/opencode"),
        os.path.join(HOME, ".local/share/opencode"),
        "--ro-bind", os.path.join(mats, "pyvenv"), "/opt/py/venv",
        "--ro-bind", NODE_DIR, "/opt/node",
        "--ro-bind", PLAYWRIGHT_CACHE, "/opt/playwright",
        "--ro-bind", PYTOOLCHAIN, PYTOOLCHAIN,
    ]
    if entry.get("da_tools"):
        mats = entry.get("_materials") or os.path.join(root, "materials")
        args += ["--ro-bind", os.path.join(mats, "da", "tools"), "/opt/da/tools",
                 "--ro-bind", os.path.join(mats, "da", "kernel"), "/opt/da/kernel"]
    if entry.get("pack"):
        ptpl = "base-0.1.0-experiment" if entry["pack"] == "canon" else "base"
        mats = entry.get("_materials") or os.path.join(root, "materials")
        args += ["--ro-bind", os.path.join(mats, "packs", ptpl),
                 "/opt/da/packs/base"]
    args += [
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
    if entry.get("da_tools"):
        args += ["--setenv", "DA_PACK", "/opt/da/packs/base"]
    return args


# ------------------------------------------------------------------- monitors
class BudgetMonitor(threading.Thread):
    """Tracks transcript step_finish token totals; sets capped flag."""

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
                with open(self.path, encoding="utf-8", errors="replace") as fh:
                    fh.seek(self._pos)
                    for line in fh:
                        self._pos = fh.tell()
                        try:
                            ev = json.loads(line)
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


def reap_ws_processes(ws):
    victims = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit() or int(pid) == os.getpid():
            continue
        try:
            cwd = os.readlink("/proc/%s/cwd" % pid)
        except Exception:
            continue
        if cwd == ws or cwd.startswith(ws + os.sep) or cwd.startswith("/opt/ws"):
            victims.append(int(pid))
    killed = 0
    for pid in victims:
        try:
            os.kill(pid, signal.SIGTERM)
            killed += 1
        except Exception:
            pass
    if victims:
        time.sleep(0.5)
        for pid in victims:
            try:
                os.kill(pid, signal.SIGKILL)
            except Exception:
                pass
    return killed


def kill_forensics(transcript):
    """Record agent-issued process-kill commands (self-kill forensics)."""
    found = []
    if not os.path.exists(transcript):
        return found
    with open(transcript, encoding="utf-8", errors="replace") as fh:
        for i, line in enumerate(fh):
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") != "tool_use":
                continue
            part = ev.get("part") or {}
            inp = json.dumps(part.get("state", {}).get("input") or {})
            if any(k in inp for k in ("pkill", "killall", "kill -", " kill ")):
                found.append({"line": i, "tool": part.get("tool"),
                              "command": inp[:400]})
    return found


def token_stats(transcript):
    out = {"steps": 0, "total": 0, "input": 0, "output": 0, "reasoning": 0,
           "cache_read": 0, "cache_write": 0, "peak": 0, "cost": 0.0}
    if not os.path.exists(transcript):
        return out
    with open(transcript, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") != "step_finish":
                continue
            part = ev.get("part") or {}
            t = part.get("tokens") or {}
            out["steps"] += 1
            out["input"] += t.get("input", 0)
            out["output"] += t.get("output", 0)
            out["reasoning"] += t.get("reasoning", 0)
            out["cache_read"] += (t.get("cache") or {}).get("read", 0)
            out["cache_write"] += (t.get("cache") or {}).get("write", 0)
            tot = t.get("total", 0)
            out["total"] += tot
            out["peak"] = max(out["peak"], tot)
            out["cost"] = round(out["cost"] + (part.get("cost") or 0.0), 6)
    return out


def tool_stats(transcript):
    types, tools = Counter(), Counter()
    if not os.path.exists(transcript):
        return {"events": 0, "tool_calls": 0, "tools": {}}
    n = 0
    with open(transcript, encoding="utf-8", errors="replace") as fh:
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


# --------------------------------------------------------------------- runner
def run_session(sid, root, entry, budget_wall, budget_tokens, skip_agent=False):
    run_dir = os.path.join(root, "run", sid)
    run_path = os.path.join(run_dir, "run.json")
    if os.path.exists(run_path) and not skip_agent:
        raise SystemExit("run already exists: %s" % run_path)
    os.makedirs(run_dir, exist_ok=True)
    run = {"id": sid, "kind": entry.get("kind"), "condition": entry.get("condition"),
           "model": entry.get("model") or DEFAULT_MODEL, "step": entry.get("step"),
           "chain": entry.get("chain"), "k": entry.get("k"),
           "started": now_iso(), "status": "running",
           "budget": {"wall_s": budget_wall, "tokens": budget_tokens}}

    def save():
        write_json_atomic(run_path, run)

    save()
    ws, meta = prep_ws(entry, root, run_dir)
    run["prep"] = meta
    save()
    log("prep %s done (ws files=%d, brief=%s)" % (sid, meta.get("ws_files"),
                                                  meta.get("brief")))

    transcript = os.path.join(run_dir, "transcript.jsonl")
    if not skip_agent:
        cmd = bwrap_cmd(entry, root, run_dir)
        # The prompt goes via stdin, never argv: an agent cleanup pattern
        # (pkill -f "<words from the brief>") must not be able to match its
        # own opencode process (observed exit 143 self-kill in rehearsal).
        prompt = open(os.path.join(ws, "reference", "BRIEF.md")).read()
        prompt_file = os.path.join(run_dir, "prompt.txt")
        with open(prompt_file, "w") as fh:
            fh.write(prompt)
        run["prompt_file"] = os.path.basename(prompt_file)
        cmd += [OPENCODE, "run", "--pure", "-m", run["model"],
                "--title", "x05-" + sid, "--format", "json"]
        monitor = BudgetMonitor(transcript, budget_tokens)
        monitor.start()
        t0 = time.time()
        timed_out, capped = False, False
        with open(transcript, "w") as tout, \
                open(os.path.join(run_dir, "opencode-stderr.log"), "w") as terr, \
                open(prompt_file) as pin:
            proc = subprocess.Popen(cmd, cwd=ws, stdout=tout, stderr=terr,
                                    stdin=pin, start_new_session=True)
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
            rc = proc.returncode if not (timed_out or capped) else (
                "cap" if capped else "timeout")
        monitor.stop_flag = True
        run["opencode"] = {"exit": rc, "timed_out": timed_out,
                           "token_cap_hit": capped,
                           "duration_s": round(time.time() - t0, 1)}
        run["opencode"].update(tool_stats(transcript))
        run["opencode"]["tokens"] = token_stats(transcript)
        run["opencode"]["kill_commands"] = kill_forensics(transcript)
        run["containment"] = leak_scan(transcript, sid,
                                       [s["id"] for s in
                                        (read_json(os.path.join(root, "schedule.json"), {})
                                         or {}).get("sessions", [])])
        os.makedirs(run_dir, exist_ok=True)
        if os.path.exists(os.path.join(ws, "audit.jsonl")):
            shutil.copy2(os.path.join(ws, "audit.jsonl"),
                         os.path.join(run_dir, "audit.jsonl"))
        run["reaped"] = reap_ws_processes(ws)
        save()
        log("session %s: exit=%s duration=%ss tokens=%s containment_attempts=%s"
            % (sid, rc, run["opencode"]["duration_s"],
               run["opencode"]["tokens"].get("total"),
               run["containment"].get("flagged_attempts")))
    else:
        run["opencode"] = {"skipped": True}
        save()

    # ---- serve + capture ----
    env = dict(os.environ, PLAYWRIGHT_BROWSERS_PATH=PLAYWRIGHT_CACHE)
    caps = [VENV_PY, os.path.join(HERE, "x05_capture.py"),
            "--ws", ws, "--out", os.path.join(run_dir, "capture")]
    fix = os.path.join(entry.get("_materials") or root + "/materials",
                       "fixtures", "bookmarks-seed.json")
    if os.path.exists(fix):
        caps += ["--fixtures", fix]
    cap = subprocess.run(caps, capture_output=True, text=True, env=env,
                         timeout=600)
    run["capture"] = {"rc": cap.returncode, "log": (cap.stdout or "").strip()[-300:]}
    save()

    # ---- extraction + census ----
    ex = subprocess.run(
        [VENV_PY, os.path.join(HERE, "x05_extract.py"), "--id", sid,
         "--root", root],
        capture_output=True, text=True, timeout=300)
    run["extraction"] = {"rc": ex.returncode, "log": (ex.stdout or "").strip()[-300:]}
    if entry.get("kind") == "handoff":
        cs = subprocess.run(
            [VENV_PY, os.path.join(HERE, "x05_census.py"), "--id", sid,
             "--root", root],
            capture_output=True, text=True, timeout=300)
        run["census"] = {"rc": cs.returncode, "log": (cs.stdout or "").strip()[-300:]}
    if entry.get("kind") == "census":
        # the census session's judgment outputs become chain-visible evidence
        ext = os.path.join(run_dir, "extraction")
        for name in ("census.json", "exemplars.json"):
            src = os.path.join(ws, name)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(ext, name))
                run.setdefault("census_outputs", []).append(name)
            else:
                run.setdefault("census_missing", []).append(name)
    save()

    # ---- seal ----
    if not os.path.exists(os.path.join(root, "seal", sid)):
        seal_dir, manifest = seal_create(ws, sid, root)
        run["seal"] = {"dir": seal_dir, "files": manifest["file_count"],
                       "records": manifest["summary"]["records"]}
    else:
        run["seal"] = {"existing": True}
    # cod output: stage the canon pack into the run area's materials
    if entry.get("kind") == "cod":
        canon_src = os.path.join(ws, "pack")
        canon_dst = os.path.join(entry.get("_materials")
                                 or os.path.join(root, "materials"),
                                 "packs", "base-0.1.0-experiment")
        if os.path.isdir(canon_src):
            if os.path.exists(canon_dst):
                shutil.rmtree(canon_dst)
            shutil.copytree(canon_src, canon_dst)
            run["canon_staged"] = canon_dst
        else:
            run["canon_staged"] = None
            run["canon_error"] = "ws/pack not found after cod session"
    save()

    run["finished"] = now_iso()
    run["status"] = "ok"
    save()
    # ---- state append ----
    with StateLock(root):
        st = load_state(root)
        st["sessions"][sid] = {"status": "ok", "finished": run["finished"],
                               "exit": run.get("opencode", {}).get("exit"),
                               "seal": run.get("seal", {}).get("dir")}
        save_state(root, st)
    log("session %s COMPLETE" % sid)
    return run


def load_entry(root, sid):
    schedule = read_json(os.path.join(root, "schedule.json"))
    if not schedule:
        raise SystemExit("schedule.json missing under %s" % root)
    for s in schedule.get("sessions", []):
        if s["id"] == sid:
            return s, schedule
    raise SystemExit("session %s not in schedule" % sid)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--root", default=X05_ROOT)
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--condition", choices=["A", "B", "C"])
    ap.add_argument("--budget", type=int, default=None)
    ap.add_argument("--skip-agent", action="store_true")
    args = ap.parse_args(argv)

    root = args.root
    materials = os.path.join(root, "materials")
    if args.pilot:
        root = os.path.join(root, "pilot")
        os.makedirs(root, exist_ok=True)
        cond = args.condition or "A"
        entry = {
            "id": args.id, "kind": "pilot", "condition": cond, "step": None,
            "input_mode": "starter", "brief": "pilot.md",
            "protocol": cond in ("B", "C"),
            "wrapper": cond in ("B", "C"),
            "da_tools": cond in ("B", "C"),
            "pack": {"B": "base", "C": "base"}.get(cond),
            "prev": None, "model": DEFAULT_MODEL,
            "_materials": materials,
        }
        budget_wall = args.budget or 300
        budget_tokens = 8_000_000
    else:
        entry, _ = load_entry(root, args.id)
        entry["_materials"] = materials
        budget_wall = args.budget or entry.get("budget_wall") or WALL_BUDGET_S
        budget_tokens = entry.get("budget_tokens") or TOKEN_BUDGET
    # single-session guard
    lock_path = os.path.join(root, "session.lock")
    lock_fh = open(lock_path, "w")
    try:
        fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        raise SystemExit("another x05 session appears to be running (lock busy)")
    try:
        run_session(args.id, root, entry, budget_wall, budget_tokens,
                    skip_agent=args.skip_agent)
    finally:
        fcntl.flock(lock_fh, fcntl.LOCK_UN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
