"""Validator runner: declared validators -> normalized, SARIF-aligned findings."""
import json
import os
import subprocess

from .pack import PackError


def snapshot_dir(pack, override=None):
    if override:
        return os.path.expanduser(override)
    env = os.environ.get("DA_SNAPSHOT")
    if env:
        return os.path.expanduser(env)
    hint = (pack.manifest.get("snapshot", {}) or {}).get("path_hint", "")
    return os.path.expanduser(hint) if hint else ""


def _normalize_lint_report(report):
    findings = []
    for f in report.get("findings", []):
        findings.append({
            "rule": f.get("rule"), "severity": f.get("severity"),
            "message": f.get("message"),
            "location": {"path": f.get("file"), "line": f.get("line")},
            "fix": f.get("fix"), "excerpt": f.get("excerpt", ""),
        })
    return findings, {"counts": report.get("counts", {}),
                      "spec_score": report.get("score"),
                      "files_scanned": report.get("files_scanned"),
                      "spec_version": report.get("version"),
                      "by_rule": report.get("by_rule", {})}


def _run_one(pack, v, target, snap, timeout):
    name = v["name"]
    workdir = os.path.expanduser(str(v.get("workdir", "{snapshot}")).replace("{snapshot}", snap))
    if not workdir or not os.path.isdir(workdir):
        return {"validator": name, "status": "error",
                "message": "validator workdir not found: %r" % workdir,
                "hint": ("Set DA_SNAPSHOT to a checkout of the pinned snapshot, or fix "
                         "snapshot.path_hint in the pack manifest."),
                "findings": []}
    cmd = [str(a).replace("{target}", os.path.abspath(target)) for a in v["command"]]
    try:
        proc = subprocess.run(cmd, cwd=workdir, capture_output=True,
                              text=True, timeout=timeout)
    except Exception as exc:
        return {"validator": name, "status": "error",
                "message": "failed to run: %s" % exc, "findings": []}

    if v.get("parser") == "triage-lint-json":
        try:
            report = json.loads(proc.stdout)
        except ValueError:
            return {"validator": name, "status": "error",
                    "message": "unparseable lint output (exit %s)" % proc.returncode,
                    "stderr_tail": proc.stderr[-400:], "findings": []}
        findings, meta = _normalize_lint_report(report)
        return {"validator": name, "status": "ok", "exit": proc.returncode,
                "findings": findings, "meta": meta}

    return {"validator": name, "status": "error",
            "message": "unknown parser %r" % v.get("parser"), "findings": []}


def _score(counts, pack):
    e = counts.get("error", 0)
    w = counts.get("warning", 0)
    i = counts.get("info", 0)
    value = max(0, round(100 - (e * 8 + w * 2 + i * 0.5)))
    return {"value": value, "formula": (pack.scoring or {}).get("formula", ""),
            "gate": (pack.scoring or {}).get("gate", "")}


def validate(pack, target, names=None, snapshot=None, timeout=240):
    results = []
    findings = []
    for v in pack.validators:
        if names and v["name"] not in names:
            continue
        r = _run_one(pack, v, target, snapshot_dir(pack, snapshot), timeout)
        results.append(r)
        findings.extend(r.get("findings", []))
    counts = {"error": 0, "warning": 0, "info": 0}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    return {"target": os.path.abspath(target), "validators": results,
            "findings": findings,
            "summary": {"counts": counts, "total": len(findings),
                        "score": _score(counts, pack)},
            "authority": pack.identity()}
