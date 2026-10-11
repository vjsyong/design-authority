#!/usr/bin/env python3
"""da_sweep — reconciliation prototype (docs/14, phasing P1.4).

Assesses a portfolio against an authority's newly resolved decisions, at the
DETERMINISTIC level only: it follows recorded cases (gaps) through explicit
`resolves_cases` links or the recorded proposal chain. It never infers; an
inferred level (code analysis / semantic discovery) is specified in docs/14
but not built here.

    python3 tools/da_sweep.py \
        --authority docs/experiments/reconcile-cadence/authority \
        --portfolio docs/experiments/reconcile-cadence/portfolio.json \
        --store docs/experiments/reconcile-cadence/findings.jsonl \
        --target-version 0.2.0 [--report report.json] [--quiet]

Finding classes (docs/14 section 4): conforms | grandfathered | rectify |
review. Findings are idempotent by identity (application, decision, target
version, assessed revision): an unchanged assessment reuses the stored
finding, a changed one supersedes it. Nothing here writes to any application
tree.

Prototype input formats (the packaged version will read real packs via the
kernel loader and receipts via the project contract):
  --authority dir    <dir>/<authority-id>/artifacts.json, records optionally
                     carrying `transition` (docs/14 section 3) and
                     `resolves_cases`.
  --portfolio file   {"target_version", "apps": [{"name", "authority",
                     "lineage", "builds": [{"dir", "revision",
                     "built_under", "evidence"}]}]}
"""
import argparse
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLASSES = ("conforms", "grandfathered", "rectify", "review")


def load(path):
    with open(path) as fh:
        return json.load(fh)


def _slug(s):
    return s.replace("/", "~").replace(" ", "-")


def _ver(s):
    try:
        return tuple(int(x) for x in str(s).split("."))
    except ValueError:
        return (0,)


def read_gap_ids(store_dir):
    path = os.path.join(store_dir, ".design-authority", "gaps.jsonl")
    out = {}
    if os.path.exists(path):
        with open(path) as fh:
            for line in fh:
                if line.strip():
                    g = json.loads(line)
                    out[g["id"]] = g.get("need", "")
    return out


def read_adopted(evidence_dir):
    path = os.path.join(evidence_dir, "resolves.jsonl")
    out = set()
    if evidence_dir and os.path.exists(path):
        with open(path) as fh:
            for line in fh:
                if not line.strip():
                    continue
                r = json.loads(line)
                if r.get("outcome") == "RESOLVED":
                    res = r.get("resolution") or {}
                    for key in ("artifact", "recipe", "fallback"):
                        if res.get(key):
                            out.add(res[key]["id"])
    return out


# ---------------------------------------------------------------- linking

def case_links(record, portfolio_apps):
    """The recorded cases a decision resolves: explicit `resolves_cases` if
    present, else the proposal chain (record.provenance.proposal -> workspace
    proposal record -> gap_id). Returns [{case, via}]."""
    links = []
    for case in record.get("resolves_cases") or []:
        links.append({"case": case, "via": "resolves_cases"})
    if links:
        return links
    prop_id = (record.get("provenance") or {}).get("proposal")
    if prop_id:
        for app in portfolio_apps:
            for build in app["builds"]:
                pdir = os.path.join(REPO, build["dir"], ".design-authority", "proposals")
                if not os.path.isdir(pdir):
                    continue
                for name in sorted(os.listdir(pdir)):
                    if not name.endswith(".json"):
                        continue
                    rec = load(os.path.join(pdir, name))
                    if rec.get("id") == prop_id and rec.get("gap_id"):
                        links.append({"case": rec["gap_id"], "via": "proposal-chain",
                                      "proposal": prop_id})
    return links


# ------------------------------------------------------------ assessment

def classify(build, adopted, policy, transition, target_version):
    """Return (class, reason, trigger_state). Deterministic, policy-driven."""
    built = build["built_under"]
    if adopted:
        return ("conforms",
                "the build resolved this decision (recorded evidence)",
                None)
    scope = transition.get("scope") or "the affected interface"
    if policy == "required":
        return ("rectify",
                "policy 'required': migration obligation is live (by %s); the "
                "implementation has not adopted the decision" % transition.get("by"),
                {"occurred": False, "basis": "obligation live until %s" % transition.get("by")})
    if _ver(built) >= _ver(target_version) and not transition.get("legacy_default"):
        return ("review",
                "built at or after the decision without recorded adoption; "
                "assess (sanctioned deviation, pending work, or a conformance finding)",
                None)
    if policy == "when_touched":
        return ("grandfathered",
                "built while the need was UNDEFINED; policy 'when_touched' "
                "permits until %s is next modified" % scope,
                {"occurred": False,
                 "basis": "no modification recorded after the decision shipped"})
    if policy == "prospective":
        return ("grandfathered",
                "policy 'prospective': no obligation on existing implementations",
                None)
    return ("review",
            "no explicit transition policy (legacy default): assess before any obligation",
            None)


def sweep(authority_dir, portfolio_file, target_version, quiet=False):
    portfolio = load(portfolio_file)
    apps = portfolio["apps"]
    for app in apps:
        app["_gaps"] = {}
        for build in app["builds"]:
            app["_gaps"].update(read_gap_ids(os.path.join(REPO, build["dir"])))
        ev = [b.get("evidence") for b in app["builds"] if b.get("evidence")]
        app["_adopted"] = read_adopted(os.path.join(REPO, ev[0])) if ev else set()

    # lineage case pools: which recorded cases does each lineage hold?
    lineages = {}
    for app in apps:
        lineages.setdefault(app["lineage"], set()).update(app["_gaps"].keys())

    findings = []
    for auth in sorted(os.listdir(authority_dir)):
        auth_path = os.path.join(authority_dir, auth, "artifacts.json")
        if not os.path.exists(auth_path):
            continue
        records = load(auth_path)["artifacts"]
        for rec in records:
            links = case_links(rec, apps)
            if not links:
                continue
            transition = rec.get("transition") or {}
            policy = transition.get("policy") or "review"
            explicit = bool(transition)
            for app in apps:
                if app["authority"] != auth:
                    continue
                lineage_cases = lineages.get(app["lineage"], set())
                hit = [l for l in links if l["case"] in lineage_cases]
                if not hit:
                    continue
                for build in app["builds"]:
                    adopted = rec["id"] in app["_adopted"]
                    tr = dict(transition)
                    if not explicit:
                        tr["legacy_default"] = True
                    cls, reason, trigger_state = classify(build, adopted, policy, tr, target_version)
                    fid = "finding/%s/%s/%s/%s" % (
                        app["name"], _slug(rec["id"]), target_version, build["revision"])
                    findings.append({
                        "id": fid,
                        "application": app["name"],
                        "revision": build["revision"],
                        "built_under": build["built_under"],
                        "lineage": app["lineage"],
                        "decision": rec["id"],
                        "decision_title": rec.get("title"),
                        "target_version": target_version,
                        "policy": policy,
                        "policy_source": "explicit" if explicit else "default (legacy record)",
                        "class": cls,
                        "assessment": "deterministic",
                        "link": hit[0],
                        "trigger_state": trigger_state,
                        "reason": reason,
                    })
    return findings


# ------------------------------------------------------------ store

def upsert(store_path, findings, now):
    existing = {}
    if os.path.exists(store_path):
        with open(store_path) as fh:
            for line in fh:
                if line.strip():
                    rec = json.loads(line)
                    existing[rec["id"]] = rec
    new = reused = superseded = 0
    for f in findings:
        old = existing.get(f["id"])
        if old is None:
            f["assessed_at"] = now
            existing[f["id"]] = f
            new += 1
        else:
            same = all(old.get(k) == f.get(k) for k in
                       ("class", "policy", "policy_source", "trigger_state", "reason",
                        "built_under", "target_version"))
            if same:
                reused += 1
            else:
                f["assessed_at"] = now
                f["previous"] = {"class": old.get("class"), "assessed_at": old.get("assessed_at"),
                                 "reason": old.get("reason")}
                existing[f["id"]] = f
                superseded += 1
    with open(store_path, "w") as fh:
        for fid in sorted(existing):
            fh.write(json.dumps(existing[fid], ensure_ascii=False) + "\n")
    return {"new": new, "reused": reused, "superseded": superseded,
            "total": len(existing)}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="da_sweep",
                                 description="reconciliation prototype: assess a portfolio against newly resolved decisions")
    ap.add_argument("--authority", required=True, help="directory of <auth>/artifacts.json fixtures")
    ap.add_argument("--portfolio", required=True)
    ap.add_argument("--store", required=True, help="findings.jsonl (upserted)")
    ap.add_argument("--target-version", required=True)
    ap.add_argument("--report", default=None, help="write the report JSON here")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    findings = sweep(os.path.join(REPO, args.authority) if not os.path.isabs(args.authority) else args.authority,
                     os.path.join(REPO, args.portfolio) if not os.path.isabs(args.portfolio) else args.portfolio,
                     args.target_version, quiet=args.quiet)
    store = os.path.join(REPO, args.store) if not os.path.isabs(args.store) else args.store
    stats = upsert(store, findings, now)

    counts = {c: sum(1 for f in findings if f["class"] == c) for c in CLASSES}
    report = {"target_version": args.target_version, "counts": counts,
              "store": stats, "findings": sorted(findings, key=lambda f: f["id"])}
    if args.report:
        with open(args.report, "w") as fh:
            json.dump(report, fh, indent=1, ensure_ascii=False)
            fh.write("\n")

    if not args.quiet:
        print("findings: %d — %s" % (len(findings),
              " · ".join("%s %d" % (c, counts[c]) for c in CLASSES if counts[c])))
        print("store: %s (%d new, %d reused, %d superseded; total %d)"
              % (args.store, stats["new"], stats["reused"], stats["superseded"], stats["total"]))
        for c in ("rectify", "review"):
            for f in findings:
                if f["class"] == c:
                    print("  [%s] %s · %s (%s) — %s" % (c, f["application"], f["decision"],
                          f["revision"], f["reason"][:110]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
