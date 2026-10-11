#!/usr/bin/env python3
"""P4 conductor — drives the 8-session program, one session at a time.

    python3 docs/experiments/tools/p4_conductor.py [--root ~/p4-maint] [--status]

Completion is derived from artifacts (run.json + verified seal), so a restart
continues at the first incomplete step. After each DA handoff the conductor
runs the reconciliation pass (frozen tooling, pack p4-da-<k>) over a copy of
the seal and writes the migration summary the next DA session receives as
reference/MIGRATION.md. Completed-but-unsuccessful runs advance (the
checkpoint is the state, broken states included); only infrastructure
failures (no run.json) are retried once, with the failed attempt moved aside.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p4_common import (MATS, P4_ROOT, VENV_PY, read_json, run_dir,  # noqa: E402
                       seal_dir)
from p4_run import seal_verify  # noqa: E402

TAILDASH = os.environ.get("TAILDASH_URL", "http://localhost:8080")
POLL_S = 15


def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S", time.gmtime()), msg), flush=True)


def dash(method, path, payload=None):
    try:
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(TAILDASH + path, data=data, method=method,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            return json.loads(resp.read().decode() or "{}")
    except Exception:
        return None


def heartbeat(title, status, pct, note):
    task = None
    out = dash("GET", "/api/tasks")
    tasks = out if isinstance(out, list) else (out or {}).get("tasks", [])
    if isinstance(tasks, dict):
        tasks = list(tasks.values())
    for t in tasks:
        if t.get("title") == title:
            task = t
            break
    if task is None:
        task = dash("POST", "/api/tasks", {"title": title, "status": status,
                                           "progress": pct, "note": note})
    tid = (task or {}).get("id")
    if tid:
        dash("PATCH", "/api/tasks/%s" % tid,
             {"status": status, "progress": pct, "note": note})


def session_complete(sid, root):
    rj = os.path.join(run_dir(sid, root), "run.json")
    if not os.path.isfile(rj):
        return False
    d = read_json(rj) or {}
    if d.get("status") == "running":
        return False
    bad, _ = seal_verify(seal_dir(sid, root))
    return not bad


def session_failed_waiting(sid, root):
    rj = os.path.join(run_dir(sid, root), "run.json")
    return os.path.isfile(rj) and not session_complete(sid, root)


def run_session(sid, root):
    rd = run_dir(sid, root)
    os.makedirs(rd, exist_ok=True)
    logf = open(os.path.join(rd, "runner.log"), "a")
    proc = subprocess.Popen([VENV_PY, os.path.join(HERE, "p4_run.py"),
                             "--id", sid, "--root", root],
                            stdout=logf, stderr=subprocess.STDOUT, cwd=root)
    return proc


def reconcile_after(sid, root, entry):
    """DA-only: reconcile + validate the sealed workspace against change-k pack.

    The seed predates the project-contract artifacts (no lock/receipt), so the
    reconcile engine has no receipt evidence to evaluate (findings ~empty by
    design); the material the next session receives is the union of the
    reconcile plan, the pack's validate output, and the change note itself.
    Migration correctness is measured at analysis time from the session diff +
    HANDOFF.md against these advisories."""
    k = int(entry.get("k") or 1)
    pack = os.path.join(MATS, "packs", "p4-da-%d" % k)
    if not os.path.isdir(pack):
        log("no pack %s; skipping reconcile" % pack)
        return
    tmp = tempfile.mkdtemp(prefix="p4-rec-")
    try:
        ws = os.path.join(tmp, "ws")
        shutil.copytree(os.path.join(seal_dir(sid, root), "tree"), ws, symlinks=True)
        from p4_run import chmod_writable
        chmod_writable(ws)
        da = os.path.join(MATS, "da", "tools", "da.py")
        r = subprocess.run([VENV_PY, da, "--pack", pack, "reconcile",
                            "--workspace", ws], capture_output=True, text=True)
        v = subprocess.run([VENV_PY, da, "--pack", pack, "validate", ws],
                           capture_output=True, text=True)
        recp = os.path.join(ws, ".design-authority", "reconciliation.json")
        out = {"session": sid, "pack": "p4-da-%d" % k, "rc": r.returncode,
               "stderr": r.stderr[-300:],
               "validate_rc": v.returncode,
               "validate_stdout_tail": (v.stdout or "")[-2500:],
               "validate_stderr_tail": (v.stderr or "")[-500:],
               "ran": True}
        rec = {}
        if os.path.isfile(recp):
            rec = read_json(recp) or {}
            out["reconciliation"] = rec
        change_note = os.path.join(MATS, "relnotes", "c%d.md" % k)
        lines = ["# Advisories after the previous handoff",
                 "",
                 "The project's design guidance changed (change %d). The machinery below "
                 "records what the change implies for this workspace; work it into your "
                 "changes and say in HANDOFF.md how each obligation was handled." % k,
                 ""]
        if os.path.isfile(change_note):
            lines += ["## The change", "", open(change_note).read().strip(), ""]
        lines += ["## Reconcile plan (transition policies, pack p4-da-%d)" % k, ""]
        if rec.get("findings") or rec.get("actions"):
            for f in rec.get("findings", []):
                lines.append("- **%s** — %s (class: %s)" %
                             (f.get("decision"), f.get("note", ""), f.get("class", "")))
            for a in rec.get("actions", []):
                lines.append("- Action: %s -> %s" % (a.get("decision"), a.get("action")))
        else:
            lines.append("- No receipt-backed obligations were recorded for this workspace "
                         "(the app predates project contracts); treat the change itself as "
                         "the obligation.")
        lines += ["", "## Validate (pack linters against the workspace)", ""]
        vtail = (v.stdout or "").strip().splitlines()
        lines += ["- " + ln for ln in (vtail[-12:] or ["validate produced no output"])]
        lines.append("")
        with open(os.path.join(run_dir(sid, root), "reconcile_migration.md"), "w") as fh:
            fh.write("\n".join(lines) + "\n")
        write_json(os.path.join(run_dir(sid, root), "reconcile.json"), out)
        log("advisories after %s: reconcile rc=%s (findings=%d) validate rc=%s" %
            (sid, r.returncode, len(rec.get("findings", [])), v.returncode))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def write_json(path, data):
    with open(path, "w") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=P4_ROOT)
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(os.path.expanduser(args.root))
    schedule = read_json(os.path.join(root, "schedule.json"))
    if not schedule:
        raise SystemExit("no schedule.json under %s; run p4_schedule.py first" % root)
    order = schedule["order"]

    if args.status:
        for sid in order:
            rj = os.path.join(run_dir(sid, root), "run.json")
            st = (read_json(rj) or {}).get("status") if os.path.isfile(rj) else "pending"
            print("%-9s %s" % (sid, st))
        return 0

    title = "P4 maintenance economics"
    heartbeat(title, "working", 0, "starting")
    done = 0
    for i, sid in enumerate(order):
        entry = next(s for s in schedule["sessions"] if s["id"] == sid)
        if session_complete(sid, root):
            log("%s already complete" % sid)
            done += 1
            continue
        if session_failed_waiting(sid, root):
            log("%s has an incomplete run.json; advancing is the recorded policy, "
                "but this means a manual look" % sid)
        log("starting %s" % sid)
        heartbeat(title, "working", int(100 * i / len(order)),
                  "running %s" % sid)
        proc = run_session(sid, root)
        proc.wait()
        if not os.path.isfile(os.path.join(run_dir(sid, root), "run.json")):
            # infrastructure failure: one retry, attempt moved aside
            log("infra failure on %s; retrying once" % sid)
            aside = os.path.join(run_dir(sid, root), "_attempt1")
            if not os.path.exists(aside):
                os.rename(run_dir(sid, root), aside)
            os.makedirs(run_dir(sid, root), exist_ok=True)
            proc = run_session(sid, root)
            proc.wait()
            if not os.path.isfile(os.path.join(run_dir(sid, root), "run.json")):
                heartbeat(title, "error", 50, "infra failure on %s" % sid)
                raise SystemExit("infrastructure failure on %s; paused" % sid)
        rj = read_json(os.path.join(run_dir(sid, root), "run.json")) or {}
        log("%s finished: status=%s" % (sid, rj.get("status")))
        if entry["chain"] == "da":
            reconcile_after(sid, root, entry)
        done += 1
        heartbeat(title, "working", int(100 * done / len(order)),
                  "%s %s" % (sid, rj.get("status")))

    heartbeat(title, "done", 100, "all sessions complete")
    log("PROGRAM COMPLETE: %d sessions" % done)
    return 0


if __name__ == "__main__":
    sys.exit(main())
