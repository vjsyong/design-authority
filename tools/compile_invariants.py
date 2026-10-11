#!/usr/bin/env python3
"""compile_invariants — governance invariants of the unified compiler.

compile_parity.py proves the unification did not change output by accident.
This gate proves the properties the output must hold on purpose:

  1. PROVENANCE COVERAGE   every normative record in every compiled pack is
     governed: compiled_from decisions, or an explicit exception block.
  2. TRACE VALIDITY        every compiled_from id is in the dossier's
     approved ledger and has a recorded decision.
  3. RECORD SHAPE          required fields per record type, via the engine's
     own validator (gate and compiler cannot drift apart).
  4. REFERENCE INTEGRITY   prohibition -> rule targets resolve; recipe
     ingredients resolve; ids are unique.
  5. AUTHORITY-AGNOSTIC    a brand-new synthetic authority compiles with zero
     engine changes.
  6. REFUSAL               an unapproved reference refuses AND publishes
     nothing (no partial release).
  7. RE-CODIFICATION       an identical resubmission is a no-op; a differing
     definition for an existing id is refused with the pack untouched.

Wired into tools/check.sh. Exit 0 = all invariants hold; 1 = failures on stderr.
"""
import copy
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import da_compile  # noqa: E402

REPO = da_compile.ROOT
SRCS = ("wink", "leader", "dominion")
EXPECTED_EXCEPTIONS = {
    "wink": ["fallback/light-only", "fallback/platform-controls"],
    "leader": ["fallback/platform-controls", "fallback/ruled-panel"],
    "dominion": ["fallback/platform-controls"],
}
FIXED_NOW = "2026-10-07T15:19:22+00:00"


def load(path):
    with open(path) as fh:
        return json.load(fh)


class Checker(object):
    def __init__(self):
        self.passed = 0
        self.failed = []

    def check(self, cond, label):
        if cond:
            self.passed += 1
        else:
            self.failed.append(label)
        return bool(cond)


def check_source(src, tmp, C):
    dossier = load(da_compile.dossier_path(src))
    approved = set(dossier["approved"])
    decisions = {d["id"] for d in load(os.path.join(REPO, dossier["source"]["decisions"]))["decisions"]}
    out = os.path.join(tmp, "compile", src)
    report = da_compile.compile_synthesis(da_compile.dossier_path(src), out)

    exc_ids = sorted(e["record"] for e in report["exceptions"])
    C.check(exc_ids == sorted(EXPECTED_EXCEPTIONS[src]),
            "%s: exception set drifted: %s" % (src, exc_ids))
    C.check(all(e.get("approval") for e in report["exceptions"]),
            "%s: an exception is missing its approval status" % src)
    C.check(report["counts"]["policy_explicit"] + report["counts"]["policy_missing"]
            == sum(report["counts"][t] for t in da_compile.RECORD_TYPES),
            "%s: policy counts do not account for every record" % src)

    records = 0
    traced = 0
    for rtype in da_compile.RECORD_TYPES:
        recs = load(os.path.join(out, rtype + ".json"))[rtype]
        for rec in recs:
            records += 1
            rid = rec.get("id")
            try:
                route = da_compile.validate_provenance(rec)
                da_compile.validate_record(rtype, rec)
            except da_compile.CompileError as exc:
                C.check(False, "%s %s %s: %s" % (src, rtype, rid, exc))
                continue
            C.check(True, "")
            if route == "decisions":
                traced += 1
                good = set(rec["compiled_from"]) <= approved and set(rec["compiled_from"]) <= decisions
                C.check(good, "%s %s: compiled_from not in the approved ledger: %s"
                        % (src, rid, rec["compiled_from"]))
            else:
                C.check(bool(rec["exception"].get("reason") and rec["exception"].get("basis")),
                        "%s %s: exception lacks reason/basis" % (src, rid))

    # reference integrity
    rule_ids = {r["id"] for r in load(os.path.join(out, "rules.json"))["rules"]}
    art_ids = {a["id"] for a in load(os.path.join(out, "artifacts.json"))["artifacts"]}
    for p in load(os.path.join(out, "prohibitions.json"))["prohibitions"]:
        C.check(p.get("rule") in rule_ids, "%s %s: prohibition targets unknown rule %r"
                % (src, p.get("id"), p.get("rule")))
    for r in load(os.path.join(out, "recipes.json"))["recipes"]:
        for ing in r.get("ingredients", []):
            C.check(ing in art_ids, "%s %s: recipe ingredient %s does not resolve"
                    % (src, r.get("id"), ing))
    return records, traced


def check_synthetic(tmp, C):
    """A completely new authority compiles with no engine edits."""
    spec = os.path.join(tmp, "specimen")
    os.makedirs(spec, exist_ok=True)
    dec_path = os.path.join(spec, "decisions.json")
    with open(dec_path, "w") as fh:
        json.dump({"source": "specimen", "system": "synthetic fixture", "generated": "2026-10-11",
                   "phase": "fixture", "legend": {},
                   "decisions": [{"id": "SP-01", "area": "actions",
                                  "decision": "The specimen action is a boxed control.",
                                  "status": "OBSERVED", "evidence": "fixture",
                                  "confidence": "high", "reasoning": "fixture",
                                  "alternatives": "none", "review": "none"}]}, fh)

    manifest = load(da_compile.dossier_path("wink"))["manifest"]
    manifest = copy.deepcopy(manifest)
    manifest.update({"id": "specimen", "name": "Specimen Authority", "version": "0.1.0",
                     "description": "Synthetic fixture for the compiler's authority-agnostic invariant.",
                     "snapshot": {"repo": "synthetic fixture", "commit": "n/a",
                                  "branch": "n/a", "version": "n/a", "path_hint": ""}})
    dossier = {
        "format": da_compile.DOSSIER_FORMAT,
        "authority": {"id": "specimen", "name": "Specimen Authority",
                      "description": "synthetic fixture", "repo": "synthetic fixture",
                      "snapshot_version": "n/a"},
        "source": {"decisions": dec_path, "extracted_from": "compile_invariants"},
        "approved": ["SP-01"],
        "records": {
            "artifacts": [{"decisions": ["SP-01"],
                           "record": {"id": "component/gizmo", "kind": "component",
                                      "title": "Gizmo control", "aliases": ["gizmo"],
                                      "body": {"class": "gizmo"}}}],
            "rules": [{"decisions": ["SP-01"],
                       "record": {"id": "SP-R1", "name": "gizmo-discipline",
                                  "severity": "warning", "applies_to": ["css"],
                                  "summary": "Gizmos stay boxed.", "why": "fixture",
                                  "fix": "wrap it"}}],
            "prohibitions": [],
            "fallbacks": [{"decisions": [],
                           "exception": {"reason": "fixture policy not present in the ledger",
                                         "basis": "synthetic fixture", "approval": "pending"},
                           "record": {"id": "fallback/gizmo", "title": "Gizmo fallback",
                                      "statement": "Box the gizmo, mark it.",
                                      "scope": ["gizmo"], "constraints": ["mark it"],
                                      "kind": "fallback"}}],
            "recipes": [],
        },
        "golden": [{"problem": "a gizmo", "expect": "RESOLVED",
                    "expect_id": "component/gizmo", "note": "fixture"}],
        "manifest": manifest,
        "scoring": {"formula": "fixture", "gate": "fixture", "source": "fixture"},
    }
    dossier_file = os.path.join(spec, "compile.json")
    with open(dossier_file, "w") as fh:
        json.dump(dossier, fh, indent=1)
    out = os.path.join(tmp, "specimen-out")
    report = da_compile.compile_synthesis(dossier_file, out)
    C.check(report["counts"] == {"artifacts": 1, "rules": 1, "prohibitions": 0,
                                 "fallbacks": 1, "recipes": 0, "golden": 1,
                                 "exceptions": 1, "policy_explicit": 0,
                                 "policy_missing": 3},
            "synthetic authority counts unexpected: %s" % report["counts"])
    rec = load(os.path.join(out, "artifacts.json"))["artifacts"][0]
    C.check(rec["id"] == "component/gizmo" and rec["compiled_from"] == ["SP-01"],
            "synthetic artifact provenance wrong")


def check_refusal(tmp, C):
    """An unapproved reference refuses and publishes nothing."""
    dossier = load(da_compile.dossier_path("wink"))
    dossier = copy.deepcopy(dossier)
    dossier["records"]["artifacts"].append(
        {"decisions": ["W-999"],
         "record": {"id": "component/invented", "kind": "component", "title": "Invented",
                    "aliases": [], "body": {}}})
    bad = os.path.join(tmp, "refused-compile.json")
    with open(bad, "w") as fh:
        json.dump(dossier, fh)
    out = os.path.join(tmp, "refused-out")
    refused = False
    try:
        da_compile.compile_synthesis(bad, out)
    except da_compile.CompileError:
        refused = True
    C.check(refused, "unapproved reference did not refuse")
    C.check(not os.path.exists(out) or not os.listdir(out),
            "refusal left output behind")


def check_recodification(tmp, C):
    """Identical resubmission = no-op; conflicting definition = refused."""
    pack = os.path.join(tmp, "recodify-pack")
    da_compile.compile_synthesis(da_compile.dossier_path("wink"), pack)
    ws = os.path.join(REPO, "examples", "cadence-wink")

    r1 = da_compile.codify(ws, pack, now=FIXED_NOW)
    C.check(r1["applied"] and not r1["conflicts"], "first codification failed: %s" % r1)
    snap = {f: open(os.path.join(pack, f), "rb").read()
            for f in ("artifacts.json", "golden.json", "authority.json")}

    r2 = da_compile.codify(ws, pack, now=FIXED_NOW)
    C.check(r2["applied"] == [] and r2["conflicts"] == [],
            "identical resubmission was not a no-op: %s" % r2)
    same = all(open(os.path.join(pack, f), "rb").read() == b for f, b in snap.items())
    C.check(same, "identical resubmission changed the pack")

    scratch_ws = os.path.join(tmp, "ws-conflict")
    shutil.copytree(os.path.join(ws, ".design-authority"),
                    os.path.join(scratch_ws, ".design-authority"))
    prop_path = os.path.join(scratch_ws, ".design-authority", "proposals",
                             "prop_20261007-151914-0510d7.json")
    prop = load(prop_path)
    prop["proposed"]["title"] = "Changed definition (should conflict)"
    with open(prop_path, "w") as fh:
        json.dump(prop, fh, indent=1)
    refused = False
    detail = ""
    try:
        da_compile.codify(scratch_ws, pack, now=FIXED_NOW)
    except da_compile.CompileError as exc:
        refused = True
        detail = str(exc)
    C.check(refused and "pattern/dialog-overlay" in detail,
            "conflicting definition was not refused: %s" % detail)
    same = all(open(os.path.join(pack, f), "rb").read() == b for f, b in snap.items())
    C.check(same, "conflicting codification changed the pack")


def check_transition_validation(C):
    """docs/14 section 3: no invalid transition combination survives the
    compiler-side validator."""
    good = {"policy": "when_touched", "scope": "feedback", "supersedes": [],
            "resolves_cases": ["case/0001"], "exceptions": "allowed_with_review"}
    bads = [
        {"policy": "sometimes"},
        {"policy": "required"},
        {"policy": "when_touched", "by": "0.3.0"},
        {"policy": "required", "by": "0.3.0", "exceptions": "maybe"},
        {"policy": "review", "scope": ""},
        {"policy": "review", "supersedes": "component/old"},
    ]
    try:
        da_compile.validate_transition(good)
        C.check(True, "")
    except da_compile.CompileError as exc:
        C.check(False, "valid transition rejected: %s" % exc)
    for i, bad in enumerate(bads):
        refused = False
        try:
            da_compile.validate_transition(bad)
        except da_compile.CompileError:
            refused = True
        C.check(refused, "invalid transition accepted (case %d): %r" % (i, bad))


def main():
    C = Checker()
    tmp = tempfile.mkdtemp(prefix="da-invariants-")
    counts = {}
    try:
        for src in SRCS:
            counts[src] = check_source(src, tmp, C)
        check_synthetic(tmp, C)
        check_refusal(tmp, C)
        check_recodification(tmp, C)
        check_transition_validation(C)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if C.failed:
        for label in C.failed:
            if label:
                print("FAIL %s" % label, file=sys.stderr)
        print("compile invariants: %d passed, %d failed" % (C.passed, len(C.failed)))
        return 1
    total = sum(n for n, _ in counts.values())
    traced = sum(t for _, t in counts.values())
    exc = sum(len(v) for v in EXPECTED_EXCEPTIONS.values())
    print("compile invariants: provenance %d records (%d decision-traced, %d exception-backed)"
          % (total, traced, exc))
    print("compile invariants: synthetic authority, refusal, re-codification OK")
    print("compile invariants: %d passed, 0 failed" % C.passed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
