#!/usr/bin/env python3
"""x05 conductor — drives the 17-session program, one session at a time.

Boot-persistent (systemd user unit, restart-safe). Consumes schedule.json,
verifies dependencies (predecessor seal), runs each session as a transient
systemd user unit, heartbeats taildash, and pauses on the frozen rails:

  * any seal verification failure
  * the third infrastructure failure (program-wide, since last resume)
  * formation insufficient (K < 4 at the census) or a missing canon after cod

Policy (rev 5, carried): only infrastructure failures are replaced (same
position, both attempts logged, failed attempt moved aside, never deleted).
Completed-but-unsuccessful runs (broken state, timeout, cap, zero change)
advance: the checkpoint is the state, broken states included.

Resumability: completion is derived from artifacts (run.json + verified seal
+ extraction), so a conductor restart continues at the first incomplete step.

    x05_conductor.py [--root X05_ROOT] [--once] [--resume] [--status]
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from x05_common import (VENV_PY, X05_ROOT, load_state, log_line, now_iso,  # noqa: E402
                        read_json, save_state, StateLock)
from x05_seal import verify as seal_verify  # noqa: E402

TAILDASH = os.environ.get("TAILDASH_URL", "http://localhost:8080")
POLL_S = 20
HEARTBEAT_S = 60
UNIT_MEM_MAX = "6G"
UNIT_RUNTIME_MAX = 5400  # backstop; the runner enforces the 2700 s budget


# ------------------------------------------------------------------ taildash
def dash(method, path, payload=None):
    try:
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(TAILDASH + path, data=data, method=method,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            return json.loads(resp.read().decode() or "{}")
    except Exception:
        return None


def dash_find(title):
    out = dash("GET", "/api/tasks")
    tasks = out if isinstance(out, list) else (out or {}).get("tasks", [])
    if isinstance(tasks, dict):
        tasks = list(tasks.values())
    for t in tasks:
        if t.get("title") == title and t.get("status") not in ("completed", "failed"):
            return t.get("task_id") or t.get("id")
    return None


def dash_register(title, total=0):
    out = dash("POST", "/api/tasks", {"title": title, "total_steps": total,
                                      "agent_name": "x05-conductor"})
    return (out or {}).get("task_id")


def dash_quiet(method, path, payload=None):
    if path and "None" not in path:
        try:
            dash(method, path, payload)
        except Exception:
            pass


# ------------------------------------------------------------------ program
def session_missing(root, sid):
    """List what is missing for a session to count as complete."""
    missing = []
    run = read_json(os.path.join(root, "run", sid, "run.json"))
    if not run or run.get("status") != "ok":
        missing.append("run.json:ok")
    seal_dir = os.path.join(root, "seal", sid)
    if not os.path.isdir(seal_dir):
        missing.append("seal/")
    else:
        bad, _ = seal_verify(seal_dir)
        if bad:
            missing.append("seal-verify(%s)" % ",".join(bad[:2]))
    ex = os.path.join(root, "run", sid, "extraction")
    if not os.path.exists(os.path.join(ex, "inventory.json")):
        missing.append("extraction/inventory.json")
    if run and run.get("kind") == "handoff" and not os.path.exists(
            os.path.join(ex, "census.json")):
        missing.append("extraction/census.json")
    return missing


def session_done(root, sid):
    return not session_missing(root, sid)


def classify_failure(root, sid):
    run = read_json(os.path.join(root, "run", sid, "run.json"))
    if run and run.get("status") == "ok":
        return "complete", ""
    if not run:
        return "infrastructure", "no run.json (runner never completed)"
    if run.get("status") == "running":
        p = os.path.join(root, "run", sid, "opencode-stderr.log")
        stderr = ""
        if os.path.exists(p):
            stderr = open(p, encoding="utf-8", errors="replace").read()[-4000:]
        transport = any(s in stderr for s in
                        ("ECONNREFUSED", "ETIMEDOUT", "fetch failed",
                         "socket hang up"))
        if transport:
            return "infrastructure", "model transport errors during run"
        return "infrastructure", "died mid-flight (environment as working hypothesis)"
    return "unsuccessful", "recorded a terminal outcome"


def unit_state(unit):
    out = subprocess.run(["systemctl", "--user", "show", unit,
                          "-p", "ActiveState,SubState,Result"],
                         capture_output=True, text=True)
    vals = dict(l.split("=", 1) for l in out.stdout.strip().splitlines() if "=" in l)
    return vals.get("ActiveState", "gone"), vals.get("SubState", ""), vals.get("Result", "")


def launch_unit(unit, root, sid):
    cmd = ["systemd-run", "--user", "--unit", unit,
           "--property", "MemoryMax=" + UNIT_MEM_MAX,
           "--property", "MemorySwapMax=2G",
           "--property", "RuntimeMaxSec=%d" % UNIT_RUNTIME_MAX,
           "--description", "x05 session %s" % sid,
           VENV_PY, os.path.join(HERE, "x05_run.py"), "--id", sid,
           "--root", root]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        return False, (out.stderr or out.stdout).strip()[-400:]
    return True, ""


def archive_attempt(root, sid, attempt):
    for kind in ("run", "seal"):
        src = os.path.join(root, kind, sid)
        dst = os.path.join(root, kind, "%s-a%d" % (sid, attempt))
        if os.path.exists(dst):
            raise SystemExit("attempt archive already exists: %s" % dst)
        if os.path.exists(src):
            os.rename(src, dst)


def run_one(root, entry, state):
    sid = entry["id"]
    unit = "x05-" + sid.replace("/", "-")
    st = state["sessions"].setdefault(sid, {"attempts": [], "attempt": 0})
    st["attempt"] = st.get("attempt", 0) + 1
    label = {"formation": "formation", "handoff": "drift", "census": "census",
             "cod": "codification", "pilot": "pilot"}.get(entry.get("kind"), "session")
    title = "X05 %s %s" % (sid, label)
    task = dash_find(title) or dash_register(title, total=1)
    st.update({"status": "running", "started": now_iso(), "unit": unit,
               "taildash": task, "label": title})
    save_state(root, state)
    log_line(root, "START %s attempt %d (unit %s)" % (sid, st["attempt"], unit))
    dash_quiet("POST", "/api/tasks/%s/progress" % task,
               {"current_step": 0, "total_steps": 1, "message": "session started"})
    ok, err = launch_unit(unit, root, sid)
    if not ok:
        log_line(root, "unit launch failed for %s: %s" % (sid, err))
        st["status"] = "launch_failed"
        save_state(root, state)
        dash_quiet("POST", "/api/tasks/%s/fail" % task, {"error": "launch failed: " + err})
        return "launch_failed"
    t0 = time.time()
    last_hb = 0
    while True:
        a, sub, result = unit_state(unit)
        if a in ("inactive", "failed", "gone"):
            break
        if time.time() - last_hb > HEARTBEAT_S:
            dash_quiet("POST", "/api/tasks/%s/heartbeat" % task, {})
            last_hb = time.time()
        time.sleep(POLL_S)
    elapsed = round(time.time() - t0, 1)
    subprocess.run(["systemctl", "--user", "reset-failed", unit],
                   capture_output=True, text=True)
    if session_done(root, sid):
        run = read_json(os.path.join(root, "run", sid, "run.json")) or {}
        oc = run.get("opencode") or {}
        note = "exit=%s" % oc.get("exit")
        if oc.get("timed_out"):
            note += " (wall cap)"
        if oc.get("token_cap_hit"):
            note += " (token cap)"
        st.update({"status": "ok", "finished": now_iso(), "elapsed_s": elapsed,
                   "note": note})
        save_state(root, state)
        log_line(root, "DONE %s (%.0fs, %s)" % (sid, elapsed, note))
        dash_quiet("POST", "/api/tasks/%s/complete" % task, {"message": note})
        return "ok"
    run = read_json(os.path.join(root, "run", sid, "run.json"))
    if run and run.get("status") == "ok":
        # runner completed but the pipeline artifacts are incomplete:
        # instrument trouble, not an agent outcome; needs a human look
        missing = session_missing(root, sid)
        st["attempts"].append({"attempt": st["attempt"], "finished": now_iso(),
                               "classification": "inconsistent",
                               "reason": "missing: " + ", ".join(missing),
                               "elapsed_s": elapsed, "unit_result": result})
        st["status"] = "inconsistent"
        save_state(root, state)
        log_line(root, "INCONSISTENT %s attempt %d: missing %s"
                 % (sid, st["attempt"], ", ".join(missing)))
        return "inconsistent"
    cls, why = classify_failure(root, sid)
    st["attempts"].append({"attempt": st["attempt"], "finished": now_iso(),
                           "classification": cls, "reason": why,
                           "elapsed_s": elapsed, "unit_result": result})
    st["status"] = cls
    save_state(root, state)
    log_line(root, "FAILED %s attempt %d: %s (%s)" % (sid, st["attempt"], cls, why))
    dash_quiet("POST", "/api/tasks/%s/fail" % task,
               {"error": "%s: %s" % (cls, why)})
    return cls


def notify_pause(root, reason):
    with StateLock(root):
        st = load_state(root)
        st["paused"] = True
        st["pause_reason"] = reason
        st["paused_at"] = now_iso()
        save_state(root, st)
    log_line(root, "PAUSED: %s" % reason)
    parent = dash_find("X05 program")
    if parent:
        dash_quiet("POST", "/api/tasks/%s/fail" % parent, {"error": "PAUSED: " + reason})


def post_session_rails(root, entry):
    """Extra rails: formation gate at cen; canon must exist after cod."""
    sid = entry["id"]
    if entry.get("kind") == "census":
        census = read_json(os.path.join(root, "run", sid, "extraction", "census.json"))
        if not census:
            return "census session produced no census.json"
        k = len(census.get("established") or census.get("K_established") or [])
        if k < 4:
            return "formation insufficient (K=%d)" % k
    if entry.get("kind") == "cod":
        run = read_json(os.path.join(root, "run", sid, "run.json")) or {}
        if not run.get("canon_staged"):
            return "cod session produced no canon pack (ws/pack missing)"
    return None


def first_incomplete(root, schedule):
    for s in schedule["sessions"]:
        if not session_done(root, s["id"]):
            return s
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=X05_ROOT)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args(argv)

    root = args.root
    schedule = read_json(os.path.join(root, "schedule.json"))
    if not schedule:
        raise SystemExit("no schedule.json under %s" % root)

    if args.status:
        for s in schedule["sessions"]:
            mark = "OK " if session_done(root, s["id"]) else "   "
            print(mark, s["id"], s.get("kind") or "", s.get("condition") or "")
        st = load_state(root)
        print("paused:", st.get("paused"), st.get("pause_reason") or "")
        return 0

    if args.resume:
        with StateLock(root):
            st = load_state(root)
            st["paused"] = False
            st["pause_reason"] = None
            st["infra_failures_since_resume"] = 0
            save_state(root, st)
        print("resumed")

    st = load_state(root)
    st.setdefault("infra_failures_since_resume", 0)
    parent = st.get("parent_task")
    if not (parent and dash("GET", "/api/tasks/%s" % parent)):
        parent = dash_find("X05 program") or dash_register("X05 program",
                                                           total=len(schedule["sessions"]))
        st["parent_task"] = parent
        save_state(root, st)
    total = len(schedule["sessions"])
    done0 = sum(1 for s in schedule["sessions"] if session_done(root, s["id"]))
    dash_quiet("POST", "/api/tasks/%s/progress" % parent,
               {"current_step": done0, "total_steps": total,
                "message": "conductor up"})
    log_line(root, "conductor start: %d/%d complete" % (done0, total))

    while True:
        st = load_state(root)
        if st.get("paused"):
            log_line(root, "paused (%s); waiting for resume"
                     % (st.get("pause_reason") or "?"))
            if args.once:
                return 0
            time.sleep(60)
            continue

        entry = first_incomplete(root, schedule)
        if entry is None:
            log_line(root, "PROGRAM COMPLETE")
            dash_quiet("POST", "/api/tasks/%s/complete" % parent,
                       {"message": "all %d sessions complete" % total})
            return 0

        # attempt cap: never loop forever on one session
        stc = st.get("sessions", {}).get(entry["id"], {})
        if stc.get("attempt", 0) >= 4:
            notify_pause(root, "attempt cap reached for %s (last: %s)"
                         % (entry["id"], stc.get("status")))
            if args.once:
                return 0
            continue

        prev = entry.get("prev")
        if prev:
            bad, _ = seal_verify(os.path.join(root, "seal", prev))
            if bad:
                notify_pause(root, "seal verification failed for %s" % prev)
                if args.once:
                    return 0
                continue

        result = run_one(root, entry, st)

        if result == "inconsistent":
            missing = session_missing(root, entry["id"])
            notify_pause(root, "pipeline incomplete for %s (missing: %s)"
                         % (entry["id"], ", ".join(missing)))
            if args.once:
                return 0
            continue

        if result == "ok":
            rail = post_session_rails(root, entry)
            if rail:
                notify_pause(root, rail)
                if args.once:
                    return 0
                continue
            st = load_state(root)
            st["infra_failures_since_resume"] = 0
            save_state(root, st)
            done = sum(1 for s in schedule["sessions"] if session_done(root, s["id"]))
            dash_quiet("POST", "/api/tasks/%s/progress" % parent,
                       {"current_step": done, "total_steps": total,
                        "message": "%s complete" % entry["id"]})
            if args.once:
                return 0
            continue

        if result in ("infrastructure", "launch_failed"):
            st = load_state(root)
            st["infra_failures_since_resume"] = st.get("infra_failures_since_resume", 0) + 1
            n = st["infra_failures_since_resume"]
            save_state(root, st)
            if n >= 3:
                notify_pause(root, "third infrastructure failure (%s)" % entry["id"])
                if args.once:
                    return 0
                continue
            attempt = st["sessions"].get(entry["id"], {}).get("attempt", 1)
            archive_attempt(root, entry["id"], attempt)
            log_line(root, "replacement scheduled for %s (after attempt %d)"
                     % (entry["id"], attempt))
            if args.once:
                return 0
            continue

        # 'unsuccessful' never happens for a completed runner; guard anyway
        log_line(root, "unexpected result %r for %s" % (result, entry["id"]))
        if args.once:
            return 0
        time.sleep(30)


if __name__ == "__main__":
    sys.exit(main())
