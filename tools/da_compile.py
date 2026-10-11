#!/usr/bin/env python3
"""da_compile — the Design Authority's single decision-to-authority compiler.

One mechanism: approved design decisions (reviewed data) become authoritative
records in a pack. There is no second route. The two historical entry points
delegate here:

    synthesis   an authority dossier (docs/synthesis/<src>/compile.json:
                the approved decision ledger + the records those decisions
                emit) -> a full pack
    codify      reviewer-ACCEPTED workspace proposals
                (<workspace>/.design-authority/proposals/*.json) merged into
                an existing pack

Both modes call the same emit core and obey the same rules:

  - ONLY approved decisions compile. A record referencing an unapproved or
    unknown decision id is a hard error; the compiler refuses.
  - The compiler never invents editorial copy. A record summary comes from
    the decision text; a codified proposal's summary comes from the review's
    recorded `codified_summary` (or the proposal's own note / problem text).
  - Every emitted record carries provenance: `compiled_from` decision ids
    and a `source` naming where the decision was recorded.
  - codify is idempotent: ids already present in the pack are skipped, never
    rewritten.

Usage:
    python3 tools/da_compile.py synthesis --src wink|leader|dominion|all [--out DIR]
    python3 tools/da_compile.py codify --workspace DIR --pack DIR [--now ISO]

`--now` is a testing hook (parity fixtures); production runs leave it unset.
"""
import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RESOLVE_CITES = re.compile(r"resolve\('([^']+)'\)\s+(?:still\s+)?cites\s+([\w/-]+)")


class CompileError(Exception):
    pass


def _load_json(path):
    with open(path) as fh:
        return json.load(fh)


def _write_json(path, obj, indent=2, newline=False):
    """Synthesis-style write: ensure_ascii=False, no trailing newline by default."""
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=indent, ensure_ascii=False)
        if newline:
            fh.write("\n")


def dossier_path(src):
    return os.path.join(ROOT, "docs", "synthesis", src, "compile.json")


# ------------------------------------------------------------------ synthesis

def compile_synthesis(dossier_file, out_dir):
    """Compile one authority dossier into a full pack at `out_dir`.

    Returns {"authority", "out", "counts"}; raises CompileError on any
    unapproved or unknown decision reference.
    """
    dossier = _load_json(dossier_file)
    if dossier.get("format") != "da-compile-dossier/0.1":
        raise CompileError("not a da-compile-dossier/0.1 file: %s" % dossier_file)
    src = dossier["authority"]["id"]
    decisions = {d["id"]: d for d in _load_json(
        os.path.join(ROOT, dossier["source"]["decisions"]))["decisions"]}
    approved = set(dossier["approved"])

    def check(ids):
        for i in ids:
            if i not in approved:
                raise CompileError(
                    "%s: decision %s is not approved at Gate 2 — refusing to compile"
                    % (src, i))
            if i not in decisions:
                raise CompileError("%s: decision %s has no record in %s"
                                   % (src, i, dossier["source"]["decisions"]))

    artifacts = []
    for entry in dossier["records"]["artifacts"]:
        ids = entry["decisions"]
        if not ids:
            raise CompileError("%s: artifact %r has no decision refs"
                               % (src, entry["record"].get("id")))
        check(ids)
        rec = entry["record"]
        note = rec.get("note")
        summary = decisions[ids[0]]["decision"] + ((" (%s)" % note) if note else "")
        artifacts.append({
            "id": rec["id"], "kind": rec["kind"], "title": rec["title"],
            "summary": summary,
            "status": "beta", "aliases": rec["aliases"],
            "body": rec["body"],
            "source": {"repo": dossier["authority"]["repo"],
                       "path": "Gate 2 accepted decisions: " + ", ".join(ids)},
            "compiled_from": ids,
        })

    def rows(key):
        for entry in dossier["records"][key]:
            check(entry["decisions"])
            yield entry["record"]

    out = {
        "artifacts.json": ("artifacts", artifacts, 2),
        "rules.json": ("rules", list(rows("rules")), 2),
        "prohibitions.json": ("prohibitions", list(rows("prohibitions")), 2),
        "fallbacks.json": ("fallbacks", list(rows("fallbacks")), 2),
        "recipes.json": ("recipes", list(rows("recipes")), 2),
        "golden.json": (None, {"version": "0.1",
                               "pack_version": "%s %s" % (src, dossier["manifest"]["version"]),
                               "cases": dossier["golden"]}, 1),
    }
    os.makedirs(out_dir, exist_ok=True)
    for name, (key, data, indent) in out.items():
        _write_json(os.path.join(out_dir, name),
                    {key: data} if key else data, indent=indent)
    _write_json(os.path.join(out_dir, "scoring.json"), dossier["scoring"])
    _write_json(os.path.join(out_dir, "authority.json"), dossier["manifest"])

    counts = {"artifacts": len(artifacts), "rules": len(out["rules.json"][1]),
              "prohibitions": len(out["prohibitions.json"][1]),
              "fallbacks": len(out["fallbacks.json"][1]),
              "recipes": len(out["recipes.json"][1]),
              "golden": len(dossier["golden"])}
    return {"authority": src, "out": out_dir, "counts": counts}


def compile_authorities(srcs, out_base=None):
    reports = []
    for src in srcs:
        out = (os.path.join(out_base, src) if out_base
               else os.path.join(ROOT, "authorities", src))
        reports.append(compile_synthesis(dossier_path(src), out))
    return reports


# --------------------------------------------------------------------- codify

def _norm_proposed(prop):
    """Proposal payloads are one entry, or {'add': [entries], 'extend': ...}."""
    if isinstance(prop, dict) and "add" in prop:
        items = prop["add"]
        return items if isinstance(items, list) else [items]
    return [prop] if isinstance(prop, dict) else []


def _norm_tests(tests):
    """tests is {golden: [...], checks: [...]} or a plain list of checks."""
    if isinstance(tests, dict):
        return (tests.get("golden") or [], tests.get("checks") or [])
    if isinstance(tests, list):
        return ([], tests)
    return ([], [])


def _derive_golden(checks, entry_ids):
    """Derive golden cases from the proposal's own `resolve('X') cites ID` checks."""
    out = []
    for c in checks:
        m = RESOLVE_CITES.search(str(c))
        if m and m.group(2) in entry_ids:
            out.append({"problem": m.group(1), "expect": "RESOLVED",
                        "expect_id": m.group(2),
                        "note": "Derived from the proposal's own compliance checks."})
    return out


def _codified_summary(prop, rec):
    """Never invent copy: the review's recorded summary, else the proposal's
    own fields. (Per-entry override -> proposal-level review summary ->
    note -> problem text.)"""
    review = rec.get("review") or {}
    return (prop.get("codified_summary") or review.get("codified_summary")
            or prop.get("note") or (rec.get("problem", "") or "")[:160])


def _bump(version):
    try:
        a, b, c = (int(x) for x in version.split("."))
        return "%d.%d.%d" % (a, b + 1, c)
    except Exception:
        return version


def codify(workspace, pack_dir, now=None):
    """Merge ACCEPTED proposals from `workspace` into the pack at `pack_dir`.

    Returns {"pack", "applied", "skipped", "version"}. Rejected and
    needs-info proposals are never touched; already-codified ids are skipped.
    """
    prop_dir = os.path.join(os.path.abspath(workspace), ".design-authority", "proposals")
    files = sorted(glob.glob(os.path.join(prop_dir, "*.json")))
    arts_path = os.path.join(pack_dir, "artifacts.json")
    gold_path = os.path.join(pack_dir, "golden.json")
    auth_path = os.path.join(pack_dir, "authority.json")
    arts = _load_json(arts_path)
    gold = _load_json(gold_path)
    auth = _load_json(auth_path)

    existing = {a.get("id") for a in arts["artifacts"]}
    applied, skipped = [], []
    now = now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    repo = (auth.get("snapshot") or {}).get("repo", "")

    for f in files:
        rec = _load_json(f)
        if rec.get("status") != "accepted":
            continue
        pid = rec["id"]
        entries = _norm_proposed(rec.get("proposed"))
        if not entries:
            skipped.append(pid)
            continue
        golden_cases, checks = _norm_tests(rec.get("tests"))
        new_ids = [e.get("id") for e in entries if e.get("id")]
        derived = _derive_golden(checks, set(new_ids))
        applied_here = False
        for prop in entries:
            if not prop.get("id") or prop["id"] in existing:
                continue
            applied_here = True
            body = dict(prop.get("body") or {})
            if prop.get("group") and "group" not in body:
                body["group"] = prop["group"]
            reviewed_at = (rec.get("review") or {}).get("reviewed_at")
            adjudicated = (" (adjudicated %s)" % reviewed_at[:10]) if reviewed_at else ""
            entry = {
                "id": prop["id"],
                "kind": prop.get("kind", "component"),
                "title": prop.get("title") or prop["id"],
                "summary": _codified_summary(prop, rec),
                "status": "beta",
                "aliases": prop.get("aliases", []),
                "body": body,
                "source": {"repo": repo,
                           "path": "Reviewer-accepted proposal %s%s" % (pid, adjudicated)},
                "compiled_from": [pid],
                "provenance": {
                    "proposal": pid, "gap": rec.get("gap_id"), "verdict": "accept",
                    "reviewed_at": reviewed_at,
                    "codified_at": now,
                },
                "checks": checks,
            }
            if prop.get("note"):
                entry["notes"] = prop["note"]
            arts["artifacts"].append(entry)
            existing.add(prop["id"])
        if applied_here:
            applied.append(pid)
            gold["cases"].extend(golden_cases)
            gold["cases"].extend(derived)
        else:
            skipped.append(pid)

    if applied:
        old = auth.get("version", "0.0.0")
        new = _bump(old)
        auth["version"] = new
        gold["pack_version"] = "%s %s" % (auth.get("id"), new)
        for path, obj in ((auth_path, auth), (arts_path, arts), (gold_path, gold)):
            with open(path, "w") as fh:
                json.dump(obj, fh, indent=2)
                fh.write("\n")
    return {"pack": auth.get("id"), "applied": applied, "skipped": skipped,
            "version": auth.get("version")}


# ------------------------------------------------------------------------ cli

SRCS = ("wink", "leader", "dominion")


def run_synthesis(srcs, out_base=None):
    """CLI helper shared by da_compile and the compile_pack shim."""
    try:
        reports = compile_authorities(srcs, out_base)
    except CompileError as exc:
        print("compile refused: %s" % exc, file=sys.stderr)
        return 2
    for r in reports:
        out_rel = os.path.relpath(r["out"], ROOT) if r["out"].startswith(ROOT) else r["out"]
        print("%s -> %s  %s" % (r["authority"], out_rel, json.dumps(r["counts"])))
    return 0


def run_codify(workspace, pack, now=None):
    """CLI helper shared by da_compile and the apply_proposals shim."""
    pack = pack if os.path.isabs(pack) else os.path.join(ROOT, pack)
    report = codify(workspace, pack, now=now)
    print(json.dumps(report, indent=1))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="da_compile",
                                 description="the Design Authority's single decision-to-authority compiler")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("synthesis", help="compile an authority dossier into a pack")
    p.add_argument("--src", default="all", choices=list(SRCS) + ["all"])
    p.add_argument("--out", default=None,
                   help="output base dir (single source only; default: authorities/<src>)")

    p = sub.add_parser("codify", help="merge accepted workspace proposals into a pack")
    p.add_argument("--workspace", required=True)
    p.add_argument("--pack", required=True)
    p.add_argument("--now", default=None, help="testing hook: pin the codified_at timestamp")

    args = ap.parse_args(argv)
    if args.cmd == "synthesis":
        srcs = list(SRCS) if args.src == "all" else [args.src]
        if args.out and len(srcs) > 1:
            ap.error("--out requires a single --src")
        return run_synthesis(srcs, args.out)

    if args.cmd == "codify":
        return run_codify(args.workspace, args.pack, now=args.now)


if __name__ == "__main__":
    sys.exit(main())
