#!/usr/bin/env python3
"""x05 declared-validator pass + handoff compliance check.

Three modes (all read-only over the run area):

  validate --id <sid> [--root DIR] [--write] [--json]
      Run the pack's declared validators (base-lint) over the sealed
      checkpoint (seal/<sid>/tree, falling back to run/<sid>/ws) and, with
      --write, record extraction/validation.json in the run dir.

  sweep [--root DIR] [--json]
      Validate every seal under <root>/seal, write <root>/analysis/
      validation-sweep.json, print one line per checkpoint.

  compliance --id <sid> [--root DIR] [--json]
      Handoff compliance for the session (repair-or-file policy):
        1. at least one `validate` call in the session window (audit.jsonl,
           ts >= run start), and
        2. every error finding on the sealed workspace is either absent
           (repaired) or matched by a gap filed after the session started.
      Writes extraction/compliance.json in the run dir.

Evidence discipline: results are computed from sealed artifacts via the
authority kernel — never from agent self-reports.
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

X05 = "/home/xrim/x05"
MATS = os.environ.get("X05_MATERIALS", os.path.join(X05, "materials"))
PY = os.path.join(MATS, "pyvenv", "bin", "python3")
DA = os.path.join(MATS, "da", "tools", "da.py")
PACK = os.path.join(MATS, "packs", "base-0.1.1-experiment")
if not os.path.exists(PY):
    PY = sys.executable


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_validate(target):
    """Shell out to the authority CLI; return the parsed JSON result."""
    proc = subprocess.run([PY, DA, "--pack", PACK, "validate", target,
                           "--json"], capture_output=True, text=True,
                          timeout=300)
    try:
        return json.loads(proc.stdout)
    except ValueError:
        return {"error": "unparseable validate output",
                "rc": proc.returncode, "stdout": proc.stdout[-500:],
                "stderr": proc.stderr[-500:]}


def target_for(root, sid):
    seal = os.path.join(root, "seal", sid, "tree")
    if os.path.isdir(seal):
        return seal, "seal"
    ws = os.path.join(root, "run", sid, "ws")
    if os.path.isdir(ws):
        return ws, "ws"
    raise SystemExit("no seal or ws for %s under %s" % (sid, root))


def cmd_validate(args):
    target, where = target_for(args.root, args.id)
    res = run_validate(target)
    out = {"ts": now(), "id": args.id, "source": where, "target": target,
           "pack": os.path.basename(PACK), "result": res}
    if args.write:
        ext = os.path.join(args.root, "run", args.id, "extraction")
        os.makedirs(ext, exist_ok=True)
        with open(os.path.join(ext, "validation.json"), "w") as fh:
            json.dump(out, fh, indent=1)
    if args.json:
        print(json.dumps(out, indent=1))
    else:
        s = (res.get("summary") or {})
        c = s.get("counts") or {}
        print("validate %s (%s): findings=%s errors=%s warnings=%s info=%s "
              "score=%s" % (args.id, where, s.get("total"),
                            c.get("error"), c.get("warning"), c.get("info"),
                            (s.get("score") or {}).get("value")))
    return 0


def cmd_sweep(args):
    seal_dir = os.path.join(args.root, "seal")
    ids = sorted(d for d in os.listdir(seal_dir)
                 if os.path.isdir(os.path.join(seal_dir, d, "tree")))
    rows = {}
    for sid in ids:
        res = run_validate(os.path.join(seal_dir, sid, "tree"))
        s = res.get("summary") or {}
        rows[sid] = {"counts": s.get("counts") or {},
                     "total": s.get("total"),
                     "score": (s.get("score") or {}).get("value"),
                     "by_rule": (res.get("validators") or [{}])[0].get(
                         "meta", {}).get("by_rule", {}),
                     "findings": res.get("findings") or []}
        c = rows[sid]["counts"]
        print("%-5s findings=%-3s errors=%-2s warnings=%-2s info=%-2s "
              "score=%s" % (sid, rows[sid]["total"], c.get("error", 0),
                            c.get("warning", 0), c.get("info", 0),
                            rows[sid]["score"]))
    out = {"ts": now(), "pack": os.path.basename(PACK), "rows": rows}
    ana = os.path.join(args.root, "analysis")
    os.makedirs(ana, exist_ok=True)
    with open(os.path.join(ana, "validation-sweep.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    if args.json:
        print(json.dumps(out, indent=1))
    return 0


def _iter_jsonl(path):
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except ValueError:
                continue


def cmd_compliance(args):
    run_dir = os.path.join(args.root, "run", args.id)
    run_json = os.path.join(run_dir, "run.json")
    started = None
    if os.path.exists(run_json):
        started = (json.load(open(run_json)) or {}).get("started")
    audit_candidates = [os.path.join(run_dir, "audit.jsonl"),
                        os.path.join(run_dir, "ws", "audit.jsonl")]
    validate_calls = []
    for path in audit_candidates:
        validate_calls = []
        for e in _iter_jsonl(path):
            argv = e.get("argv") or []
            if argv and argv[0] == "validate":
                ts = e.get("ts") or ""
                if not started or ts[:19] >= str(started)[:19]:
                    validate_calls.append({"ts": ts, "argv": argv,
                                           "rc": e.get("rc")})
        if validate_calls or os.path.exists(path):
            break

    # error findings on the sealed workspace (run the pass now; source of
    # truth is the seal, independent of any recorded validation.json)
    target, where = target_for(args.root, args.id)
    res = run_validate(target)
    errors = [f for f in (res.get("findings") or [])
              if f.get("severity") == "error"]

    gaps_path = os.path.join(run_dir, "ws", ".design-authority", "gaps.jsonl")
    gap_lines = []
    for g in _iter_jsonl(gaps_path):
        ts = str(g.get("ts") or g.get("created") or "")
        if started and ts[:19] < str(started)[:19]:
            continue
        gap_lines.append(json.dumps(g))

    unmatched = []
    for f in errors:
        rule = f.get("rule") or ""
        base = os.path.basename((f.get("location") or {}).get("path") or "")
        hit = any(rule and rule in line for line in gap_lines)
        if not hit and base:
            hit = any(base in line for line in gap_lines)
        if not hit:
            unmatched.append({"rule": rule, "file": base,
                              "message": f.get("message")})

    compliant = bool(validate_calls) and not unmatched
    reasons = []
    if not validate_calls:
        reasons.append("no validate call in the session window")
    for u in unmatched:
        reasons.append("unfiled error finding: %s %s" % (u["rule"],
                                                         u["file"]))
    out = {"ts": now(), "id": args.id, "compliant": compliant,
           "validate_calls": validate_calls, "reasons": reasons,
           "post_seal": {"source": where,
                         "counts": (res.get("summary") or {}).get("counts"),
                         "score": ((res.get("summary") or {}).get("score")
                                   or {}).get("value")},
           "unmatched_errors": unmatched}
    ext = os.path.join(run_dir, "extraction")
    os.makedirs(ext, exist_ok=True)
    with open(os.path.join(ext, "compliance.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    if args.json:
        print(json.dumps(out, indent=1))
    else:
        print("compliance %s: %s (validate_calls=%d, unfiled_errors=%d)%s"
              % (args.id, "YES" if compliant else "NO", len(validate_calls),
                 len(unmatched),
                 (" — " + "; ".join(reasons)) if reasons else ""))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    p = sub.add_parser("validate")
    p.add_argument("--id", required=True)
    p.add_argument("--root", default=X05)
    p.add_argument("--write", action="store_true")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("sweep")
    p.add_argument("--root", default=X05)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("compliance")
    p.add_argument("--id", required=True)
    p.add_argument("--root", default=X05)
    p.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    return {"validate": cmd_validate, "sweep": cmd_sweep,
            "compliance": cmd_compliance}[args.mode](args)


if __name__ == "__main__":
    sys.exit(main())
