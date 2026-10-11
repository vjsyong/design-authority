#!/usr/bin/env python3
"""da_compile — the Design Authority's single decision-to-authority compiler.

One mechanism: approved design decisions (reviewed data) become authoritative
records in a pack. There is no second route. The two historical entry points
delegate here:

    synthesis   an authority dossier (docs/synthesis/<src>/compile.json,
                format da-compile-dossier/0.2: the approved decision ledger
                plus the records those decisions emit) -> a full pack
    codify      reviewer-ACCEPTED workspace proposals
                (<workspace>/.design-authority/proposals/*.json) merged into
                an existing pack

Every emitted record, in both modes, passes through ONE emission function
(`_finalize_record`) that validates record type, required fields and
provenance. A record is governed when it either

  - references at least one approved decision (emitted as `compiled_from`), or
  - carries an explicit, visible exception block (reason + basis + approval
    status). Empty provenance is a hard error; nothing is silent.

Other hard rules:

  - only approved decisions compile; unknown or unapproved references refuse
  - summaries are never invented (decision text; the review's recorded
    `codified_summary`; the proposal's own fields)
  - codify is idempotent for identical resubmissions; a PROPOSED DEFINITION
    THAT DIFFERS from the published record for the same id is refused
    (amend through a case, not through a second submission)
  - publication is staged, validated, and journaled before anything is
    replaced: builds happen in memory, land in a staging directory, load
    cleanly through the runtime's own pack loader, and are then moved into
    place under a journal (pre-publish bytes backed up, one atomic
    os.replace per file, the published pack re-validated from disk
    afterwards). A failed write rolls back in-run; a hard kill mid-publish
    leaves the journal, and the next run rolls the interrupted release
    back before publishing. The mixed-read window for a concurrent reader
    is bounded to the replace loop; a fully versioned release layout with
    a single-reference switch is the recorded follow-up

Usage:
    python3 tools/da_compile.py synthesis --src wink|leader|dominion|all [--out DIR]
    python3 tools/da_compile.py codify --workspace DIR --pack DIR [--now ISO]

`--now` is a testing hook (parity fixtures); production runs leave it unset.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RESOLVE_CITES = re.compile(r"resolve\('([^']+)'\)\s+(?:still\s+)?cites\s+([\w/-]+)")
DOSSIER_FORMAT = "da-compile-dossier/0.2"

ARTIFACT_KINDS = ("component", "pattern", "guideline", "token-set", "example", "reference")
RECORD_TYPES = ("artifacts", "rules", "prohibitions", "fallbacks", "recipes")
RECORD_REQUIRED = {
    "artifacts": ("id", "kind", "title"),
    "rules": ("id", "name", "severity", "summary"),
    "prohibitions": ("id", "statement", "signals"),
    "fallbacks": ("id", "title", "statement", "scope"),
    "recipes": ("id", "title", "needs", "summary"),
}


class CompileError(Exception):
    pass


TRANSITION_POLICIES = ("prospective", "when_touched", "required", "review")
TRANSITION_EXCEPTIONS = ("allowed_with_review", "none")


def validate_transition(t):
    """docs/14 section 3: the policy determines applicability; `by` is
    required if and only if the policy is `required`; no invalid combination
    survives validation. Returns the policy."""
    if not isinstance(t, dict):
        raise CompileError("transition must be an object")
    policy = t.get("policy")
    if policy not in TRANSITION_POLICIES:
        raise CompileError("transition policy must be one of %s, got %r"
                           % (" | ".join(TRANSITION_POLICIES), policy))
    by = t.get("by")
    if policy == "required":
        if not (isinstance(by, str) and by.strip()):
            raise CompileError("a 'required' transition must name its trigger ('by')")
    elif by is not None:
        raise CompileError("transition 'by' only applies to policy 'required'")
    if "scope" in t and not (isinstance(t["scope"], str) and t["scope"].strip()):
        raise CompileError("transition 'scope' must be a non-empty string")
    for key in ("supersedes", "resolves_cases"):
        if key in t and not (isinstance(t[key], list)
                             and all(isinstance(x, str) and x for x in t[key])):
            raise CompileError("transition %r must be a list of ids" % key)
    exc = t.get("exceptions")
    if exc is not None and exc not in TRANSITION_EXCEPTIONS:
        raise CompileError("transition 'exceptions' must be one of %s"
                           % " | ".join(TRANSITION_EXCEPTIONS))
    return policy


def _load_json(path):
    with open(path) as fh:
        return json.load(fh)


# ------------------------------------------------------------- record layer

def _validate_exception(exc):
    if not isinstance(exc, dict):
        raise CompileError("exception must be an object with reason/basis/approval")
    for key in ("reason", "basis", "approval"):
        val = exc.get(key)
        if not (isinstance(val, str) and val.strip()):
            raise CompileError("exception is missing a non-empty %r" % key)


def validate_record(rtype, rec):
    """Type + required-field validation for one emitted record."""
    if rtype not in RECORD_REQUIRED:
        raise CompileError("unknown record type %r" % rtype)
    for key in RECORD_REQUIRED[rtype]:
        val = rec.get(key)
        if val is None or (isinstance(val, (str, list, dict)) and len(val) == 0):
            raise CompileError("%s %r is missing required field %r"
                               % (rtype, rec.get("id", "?"), key))
    if rtype == "artifacts" and rec["kind"] not in ARTIFACT_KINDS:
        raise CompileError("artifact %r has unknown kind %r"
                           % (rec["id"], rec["kind"]))


def validate_provenance(rec):
    """Every record carries exactly one provenance route. Returns the route."""
    cf = rec.get("compiled_from")
    exc = rec.get("exception")
    if cf and isinstance(cf, list) and not exc:
        return "decisions"
    if exc and not cf:
        _validate_exception(exc)
        return "exception"
    raise CompileError("record %r must carry either compiled_from decisions or "
                       "an exception block (and not both)" % rec.get("id", "?"))


def _finalize_record(rtype, fields, *, source, decisions=None, exception=None,
                     tail=None):
    """THE emission function. Both modes normalize through here: provenance
    is attached uniformly, then type/required-field validation runs."""
    rec = dict(fields)
    if decisions and exception:
        raise CompileError("record %r: decisions and exception are mutually "
                           "exclusive" % rec.get("id", "?"))
    if decisions:
        rec["source"] = dict(source)
        rec["compiled_from"] = list(decisions)
    elif exception:
        _validate_exception(exception)
        rec["source"] = dict(source)
        rec["exception"] = dict(exception)
    else:
        raise CompileError("record %r carries no provenance route (neither "
                           "decisions nor exception)" % rec.get("id", "?"))
    if tail:
        rec.update(tail)
    if rec.get("transition"):
        validate_transition(rec["transition"])
    validate_record(rtype, rec)
    validate_provenance(rec)
    return rec


# ------------------------------------------------------------ publication

def _validate_pack_dir(path):
    """Load a directory through the runtime's own pack loader."""
    kernel = os.path.join(ROOT, "kernel")
    if kernel not in sys.path:
        sys.path.insert(0, kernel)
    from design_authority.pack import Pack, PackError  # noqa: WPS433
    try:
        return Pack(path)
    except PackError as exc:
        raise CompileError("staged pack failed validation: %s" % exc)


def _write_files(dirpath, files):
    """files: {name: (obj, indent, newline, ensure_ascii)}"""
    for name, (obj, indent, newline, ensure_ascii) in files.items():
        with open(os.path.join(dirpath, name), "w") as fh:
            json.dump(obj, fh, indent=indent, ensure_ascii=ensure_ascii)
            if newline:
                fh.write("\n")


PUBLISH_JOURNAL = ".da-publish-journal.json"
PUBLISH_BACKUP = ".da-publish-backup"


class _PublishCrash(Exception):
    """Test hook: simulates a hard kill mid-publish (journal left behind)."""


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _replace_file(src, dst):
    """The one replacement primitive; a seam for failure-injection tests."""
    os.replace(src, dst)


def _rollback_publish(out_dir, journal):
    """Restore the pre-publish state described by the journal."""
    backup = os.path.join(out_dir, PUBLISH_BACKUP)
    for name in journal.get("new", {}):
        cur = os.path.join(out_dir, name)
        src = os.path.join(backup, name)
        if name in journal.get("backup", {}):
            if os.path.exists(src):
                os.replace(src, cur)
        elif os.path.exists(cur):
            os.remove(cur)
    shutil.rmtree(backup, ignore_errors=True)
    jpath = os.path.join(out_dir, PUBLISH_JOURNAL)
    if os.path.exists(jpath):
        os.remove(jpath)


def _recover_interrupted_publish(out_dir):
    """A journal means a publish died mid-replace: roll it back first."""
    jpath = os.path.join(out_dir, PUBLISH_JOURNAL)
    if not os.path.exists(jpath):
        return False
    with open(jpath) as fh:
        journal = json.load(fh)
    _rollback_publish(out_dir, journal)
    print("recovered an interrupted publish in %s (rolled back to the "
          "previous release)" % out_dir)
    return True


def _stage_and_publish(files, out_dir, *, whole_copy=None, _fault=None):
    """Stage -> validate -> journaled publish.

    files       {name: (obj, indent, newline, ensure_ascii)} to become authoritative
    out_dir     the pack directory being (re)published
    whole_copy  if set, stage a full copy of this pack first (codify: the staged
                view must contain the untouched files for a real pack load)
    _fault      test hook: crash after N replacements (journal left behind)

    The staged set is validated first, then published under a journal: the
    pre-publish bytes are backed up, every replacement is atomic, and the
    published pack is re-validated from disk before the journal clears. A
    failed replacement rolls back in-run; a hard kill leaves the journal and
    the next run rolls the interrupted release back before publishing.
    """
    out_dir = os.path.abspath(out_dir)
    os.makedirs(os.path.dirname(out_dir) or ".", exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    _recover_interrupted_publish(out_dir)

    staging = tempfile.mkdtemp(prefix=".da-compile-staging-",
                               dir=os.path.dirname(out_dir))
    try:
        target = staging
        if whole_copy:
            target = os.path.join(staging, "pack")
            shutil.copytree(whole_copy, target)
        _write_files(target, files)
        _validate_pack_dir(target)

        backup_dir = os.path.join(out_dir, PUBLISH_BACKUP)
        shutil.rmtree(backup_dir, ignore_errors=True)
        os.makedirs(backup_dir)
        journal = {"new": {}, "backup": {}, "created": []}
        for name in files:
            journal["new"][name] = _sha256(os.path.join(target, name))
            cur = os.path.join(out_dir, name)
            if os.path.exists(cur):
                shutil.copy2(cur, os.path.join(backup_dir, name))
                journal["backup"][name] = _sha256(cur)
            else:
                journal["created"].append(name)
        jpath = os.path.join(out_dir, PUBLISH_JOURNAL)
        with open(jpath + ".tmp", "w") as fh:
            json.dump(journal, fh, indent=1)
        os.replace(jpath + ".tmp", jpath)

        try:
            for i, name in enumerate(files):
                if _fault is not None and i == _fault:
                    raise _PublishCrash(
                        "fault injected after %d replacement(s)" % i)
                _replace_file(os.path.join(target, name),
                              os.path.join(out_dir, name))
            _validate_pack_dir(out_dir)
        except _PublishCrash:
            raise
        except Exception:
            _rollback_publish(out_dir, journal)
            raise
        os.remove(jpath)
        shutil.rmtree(backup_dir, ignore_errors=True)
    finally:
        shutil.rmtree(staging, ignore_errors=True)


# ---------------------------------------------------------------- synthesis

def dossier_path(src):
    return os.path.join(ROOT, "docs", "synthesis", src, "compile.json")


def compile_synthesis(dossier_file, out_dir):
    """Compile one authority dossier into a full pack at `out_dir`.

    Returns {"authority", "out", "counts", "exceptions"}; raises CompileError
    on any unapproved/unknown decision reference or ungoverned record.
    """
    dossier = _load_json(dossier_file)
    if dossier.get("format") != DOSSIER_FORMAT:
        raise CompileError("not a %s file: %s" % (DOSSIER_FORMAT, dossier_file))
    src = dossier["authority"]["id"]
    repo = dossier["authority"]["repo"]
    decisions = {d["id"]: d for d in _load_json(
        os.path.join(ROOT, dossier["source"]["decisions"]))["decisions"]}
    approved = set(dossier["approved"])

    records = {}
    exceptions = []
    policy_counts = {"policy_explicit": 0, "policy_missing": 0}
    seen_ids = set()
    for rtype in RECORD_TYPES:
        out_recs = []
        for entry in dossier["records"].get(rtype, []):
            ids = entry.get("decisions") or []
            exc = entry.get("exception")
            for i in ids:
                if i not in approved:
                    raise CompileError(
                        "%s: decision %s is not approved at Gate 2 - refusing to compile"
                        % (src, i))
                if i not in decisions:
                    raise CompileError("%s: decision %s has no record in %s"
                                       % (src, i, dossier["source"]["decisions"]))
            if rtype == "artifacts":
                if not ids:
                    raise CompileError("%s: artifact %r has no decision refs"
                                       % (src, entry["record"].get("id")))
                rec = entry["record"]
                note = rec.get("note")
                fields = {
                    "id": rec["id"], "kind": rec["kind"], "title": rec["title"],
                    "summary": decisions[ids[0]]["decision"] + ((" (%s)" % note) if note else ""),
                    "status": "beta", "aliases": rec["aliases"],
                    "body": rec["body"],
                }
                rec = _finalize_record(
                    "artifacts", fields,
                    source={"repo": repo,
                            "path": "Gate 2 accepted decisions: " + ", ".join(ids)},
                    decisions=ids)
            elif ids:
                rec = _finalize_record(
                    rtype, entry["record"],
                    source={"repo": repo,
                            "path": "Gate 2 accepted decisions: " + ", ".join(ids)},
                    decisions=ids)
            else:
                rec = _finalize_record(
                    rtype, entry["record"],
                    source={"repo": repo, "path": "Authored policy (see exception)"},
                    exception=exc)
                exceptions.append({"record": rec["id"], "type": rtype,
                                   "approval": exc["approval"]})
            if rec["id"] in seen_ids:
                raise CompileError("%s: duplicate record id %r" % (src, rec["id"]))
            seen_ids.add(rec["id"])
            tblock = rec.get("transition")
            if tblock:
                validate_transition(tblock)
                policy_counts["policy_explicit"] += 1
            else:
                policy_counts["policy_missing"] += 1
            out_recs.append(rec)
        records[rtype] = out_recs

    manifest = dossier["manifest"]
    golden = {"version": "0.1",
              "pack_version": "%s %s" % (src, manifest["version"]),
              "cases": dossier["golden"]}
    files = {}
    for rtype in RECORD_TYPES:
        files[rtype + ".json"] = ({rtype: records[rtype]}, 2, False, False)
    files["golden.json"] = (golden, 1, False, False)
    files["scoring.json"] = (dossier["scoring"], 2, False, False)
    files["authority.json"] = (manifest, 2, False, False)

    _stage_and_publish(files, out_dir)
    counts = {rtype: len(records[rtype]) for rtype in RECORD_TYPES}
    counts["golden"] = len(dossier["golden"])
    counts["exceptions"] = len(exceptions)
    counts.update(policy_counts)
    return {"authority": src, "out": out_dir, "counts": counts,
            "exceptions": exceptions}


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


def _candidate_payload(prop, rec):
    """The artifact fields a codification would write (used for conflicts)."""
    body = dict(prop.get("body") or {})
    if prop.get("group") and "group" not in body:
        body["group"] = prop["group"]
    out = {
        "id": prop["id"],
        "kind": prop.get("kind", "component"),
        "title": prop.get("title") or prop["id"],
        "summary": _codified_summary(prop, rec),
        "status": "beta",
        "aliases": prop.get("aliases", []),
        "body": body,
    }
    if prop.get("transition"):
        # The release policy travels with the decision from first publication
        # (docs/14 section 3; owner-set policies, D-034).
        out["transition"] = prop["transition"]
    return out


def codify(workspace, pack_dir, now=None):
    """Merge ACCEPTED proposals from `workspace` into the pack at `pack_dir`.

    Idempotent: an identical resubmission for an existing id is skipped. A
    resubmission whose definition DIFFERS from the published record is an
    explicit conflict - refused before anything is written. Rejected and
    needs-info proposals are never touched. Returns
    {"pack", "applied", "skipped", "conflicts", "version"}.
    """
    prop_dir = os.path.join(os.path.abspath(workspace), ".design-authority", "proposals")
    files = sorted(glob.glob(os.path.join(prop_dir, "*.json")))
    arts = _load_json(os.path.join(pack_dir, "artifacts.json"))
    gold = _load_json(os.path.join(pack_dir, "golden.json"))
    auth = _load_json(os.path.join(pack_dir, "authority.json"))

    existing = {a.get("id"): a for a in arts["artifacts"]}
    applied, skipped, conflicts = [], [], []
    now = now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    repo = (auth.get("snapshot") or {}).get("repo", "")
    compare_fields = ("kind", "title", "summary", "aliases", "body", "transition")

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
            if not prop.get("id"):
                continue
            cand = _candidate_payload(prop, rec)
            if prop["id"] in existing:
                cur = existing[prop["id"]]
                diffs = [k for k in compare_fields if cur.get(k) != cand.get(k)]
                if diffs:
                    conflicts.append((prop["id"], pid, diffs))
                continue
            applied_here = True
            reviewed_at = (rec.get("review") or {}).get("reviewed_at")
            adjudicated = (" (adjudicated %s)" % reviewed_at[:10]) if reviewed_at else ""
            tail = {
                "provenance": {
                    "proposal": pid, "gap": rec.get("gap_id"), "verdict": "accept",
                    "reviewed_at": reviewed_at,
                    "codified_at": now,
                },
                "checks": checks,
            }
            if prop.get("note"):
                tail["notes"] = prop["note"]
            entry = _finalize_record(
                "artifacts", cand,
                source={"repo": repo,
                        "path": "Reviewer-accepted proposal %s%s" % (pid, adjudicated)},
                decisions=[pid], tail=tail)
            arts["artifacts"].append(entry)
            existing[prop["id"]] = entry
        if applied_here:
            applied.append(pid)
            gold["cases"].extend(golden_cases)
            gold["cases"].extend(derived)
        else:
            skipped.append(pid)

    if conflicts:
        detail = "; ".join("%s (proposal %s differs in: %s)"
                           % (rid, pid, ", ".join(diffs)) for rid, pid, diffs in conflicts)
        raise CompileError(
            "conflicting codification refused: %s. An existing id cannot be "
            "redefined by a second submission - amend through a case (a new "
            "proposal against the published record) instead." % detail)

    if applied:
        old = auth.get("version", "0.0.0")
        new = _bump(old)
        auth["version"] = new
        gold["pack_version"] = "%s %s" % (auth.get("id"), new)
        files_out = {
            "authority.json": (auth, 2, True, True),
            "artifacts.json": (arts, 2, True, True),
            "golden.json": (gold, 2, True, True),
        }
        _stage_and_publish(files_out, pack_dir, whole_copy=pack_dir)
    return {"pack": auth.get("id"), "applied": applied, "skipped": skipped,
            "conflicts": [{"id": rid, "proposal": pid, "fields": diffs}
                          for rid, pid, diffs in conflicts],
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
    try:
        report = codify(workspace, pack, now=now)
    except CompileError as exc:
        print("codify refused: %s" % exc, file=sys.stderr)
        return 2
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
