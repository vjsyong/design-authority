#!/usr/bin/env python3
"""da_sweep — reconciliation prototype (docs/14, phasing P1.4).

Assesses a portfolio against an authority's newly resolved decisions, at the
DETERMINISTIC level only: it follows recorded cases (gaps) through explicit
`resolves_cases` links or the recorded proposal chain, and reads prototype
decision receipts for adoption evidence, modification scope, deviations and
migration closures. It never infers; an inferred level (code analysis /
semantic discovery) is specified in docs/14 but not built here.

    python3 tools/da_sweep.py \
        --authority docs/experiments/reconcile-cadence/authority \
        --portfolio docs/experiments/reconcile-cadence/portfolio.json \
        --store docs/experiments/reconcile-cadence/findings.jsonl \
        --target-version 0.2.0 [--decision ID] [--report report.json] [--quiet]

Finding classes (docs/14 section 4): conforms | grandfathered | rectify |
review. Findings are idempotent by identity (application, decision, target
version, assessed revision): an unchanged assessment reuses the stored
finding, a changed one supersedes it. Nothing here writes to any application
tree.

Two properties, per docs/14 sections 3-5:
  trigger_state   {state: occurred | not_occurred | unknown, evidence, basis}
                  Missing evidence is never treated as "not occurred":
                  not_occurred requires receipts covering the app's whole
                  post-decision modification history with no touch on the
                  affected area.
  obligation      {state: scheduled | due | overdue | closed, by?, closed_by?,
                  verification?} on rectify findings. A `required` deadline
                  after the target version is SCHEDULED, not already due.
                  A later receipt with `migration_for` closes the obligation.

Prototype input formats (the packaged version will read real packs via the
kernel loader and receipts via the project contract):
  --authority dir    <dir>/<authority-id>/artifacts.json, records optionally
                     carrying `transition` (docs/14 section 3) and
                     `resolves_cases`.
  --portfolio file   {"target_version", "apps": [{"name", "authority",
                     "lineage", "builds": [{"dir", "revision", "built_under",
                     "evidence"?, "receipt"?}]}]}
  receipts           <build dir>/.design-authority/receipts/*.json
                     (prototype-0.1 shape; P1.1 formalizes)
"""
import argparse
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLASSES = ("conforms", "grandfathered", "rectify", "review")
_WORD = re.compile(r"[a-z0-9]+")
_STOP = {"the", "and", "or", "of", "a", "an", "to", "for", "on", "in", "with", "no"}


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


def _tokens(text):
    return {w for w in _WORD.findall(str(text).lower()) if w not in _STOP and len(w) > 2}


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


def read_receipt(build):
    """Load the build's prototype receipt, if the manifest names one."""
    rel = build.get("receipt")
    if not rel:
        return None, None
    path = os.path.join(REPO, build["dir"], rel)
    if not os.path.exists(path):
        return None, None
    return load(path), "%s/%s" % (build["dir"], rel)


def read_confirmations(build):
    """Receipt refs this build's confirmation records vouch for (docs/14
    section 5: a receipt is a declaration until confirmed against evidence)."""
    out = set()
    vdir = os.path.join(REPO, build["dir"], "_evidence", "verification")
    if os.path.isdir(vdir):
        for name in sorted(os.listdir(vdir)):
            if not name.endswith(".json"):
                continue
            try:
                rec = load(os.path.join(vdir, name))
            except ValueError:
                continue
            if rec.get("verdict") != "pass":
                continue
            for ref in rec.get("confirms") or []:
                out.add("%s/%s" % (build["dir"], ref))
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

def classify(build, rec_id, adopted, policy, transition, target_version,
             trigger, is_source, closer):
    """Return (class, reason, trigger_state, obligation). Policy-driven."""
    built = build["built_under"]
    if adopted:
        why = ("the build applied this decision (recorded receipt evidence)"
               if build.get("_receipt") else
               "the build resolved this decision (recorded evidence)")
        return "conforms", why, None, None
    scope = transition.get("scope") or "the affected interface"
    if policy == "required":
        by = transition.get("by")
        if _ver(by) > _ver(target_version):
            state, word = "scheduled", "not yet due (scheduled for %s)" % by
        elif _ver(by) == _ver(target_version):
            state, word = "due", "due at this target (%s)" % by
        else:
            state, word = "overdue", "overdue since %s" % by
        obligation: dict = {"state": state, "by": by}
        reason = ("policy 'required': migration obligation is %s; the "
                  "implementation has not adopted the decision" % word)
        if closer:
            obligation["state"] = "closed"
            obligation["closed_by"] = [closer["ref"]]
            obligation["verification"] = closer.get("verification")
            reason += "; closed by %s" % closer["revision"] + (
                " (verification: %s)" % closer["verification"]["result"]
                if closer.get("verification") else "")
        return "rectify", reason, None, obligation
    if policy == "when_touched" and is_source and trigger["state"] == "occurred":
        obligation: dict = {"state": "due", "trigger": "occurred"}
        reason = ("the affected area (%s) was modified without migrating; "
                  "policy 'when_touched': the obligation is due for this "
                  "revision" % scope)
        if closer:
            obligation["state"] = "closed"
            obligation["closed_by"] = [closer["ref"]]
            obligation["verification"] = closer.get("verification")
            reason += "; closed by %s" % closer["revision"] + (
                " (verification: %s)" % closer["verification"]["result"]
                if closer.get("verification") else "")
        return "rectify", reason, trigger, obligation
    if _ver(built) >= _ver(target_version) and not transition.get("legacy_default"):
        return ("review",
                "built at or after the decision without recorded adoption; "
                "assess (sanctioned deviation, pending work, or a conformance finding)",
                None, None)
    if policy == "when_touched":
        reason = "built while the need was UNDEFINED; policy 'when_touched' " \
                 "permits until %s is next modified" % scope
        if trigger["state"] == "occurred":
            reason += " (permission ended: trigger recorded; the obligation " \
                      "rides the modified revision)"
        return "grandfathered", reason, trigger, None
    if policy == "prospective":
        return ("grandfathered",
                "policy 'prospective': no obligation on existing implementations",
                None, None)
    return ("review",
            "no explicit transition policy (legacy default): assess before any obligation",
            None, None)


def sweep(authority_dir, portfolio_file, target_version, decision_filter=None):
    portfolio = load(portfolio_file)
    apps = portfolio["apps"]

    # per-build prep: cases, evidence, receipts
    for app in apps:
        app["_gaps"] = {}
        for build in app["builds"]:
            app["_gaps"].update(read_gap_ids(os.path.join(REPO, build["dir"])))
            build["_receipt"], build["_receipt_ref"] = read_receipt(build)
            build["_confirmed"] = read_confirmations(build)
            ev_dir = build.get("evidence") or None
            build["_resolves"] = read_adopted(os.path.join(REPO, ev_dir)) if ev_dir else set()
            build["_adopted"] = set(build["_resolves"])
            if build["_receipt"] is not None:
                receipt = build["_receipt"]
                dev_ids = {d.get("decision") for d in receipt.get("deviations") or []}
                build["_adopted"] = (set(receipt.get("decisions_applied") or []) | set(build["_resolves"])) - dev_ids
                build["_deviation_ids"] = dev_ids
            else:
                build["_deviation_ids"] = set()

    # lineage pools: recorded cases + trigger events (deviations) + receipt coverage
    lineages = {}
    for app in apps:
        L = lineages.setdefault(app["lineage"], {"cases": set(), "events": {},
                                                 "receipts": [], "confirmed": set()})
        L["cases"].update(app["_gaps"].keys())
        for build in app["builds"]:
            L["confirmed"] |= build["_confirmed"]
            receipt = build["_receipt"]
            if receipt is None:
                continue
            ref = build["_receipt_ref"]
            L["receipts"].append({"ref": ref, "revision": build["revision"],
                                  "areas": _tokens(" ".join(receipt.get("areas_modified") or []))})
            for d in receipt.get("deviations") or []:
                if d.get("decision"):
                    L["events"].setdefault(d["decision"], []).append(
                        {"ref": ref, "revision": build["revision"], "reason": d.get("reason")})

    findings = []
    for auth in sorted(os.listdir(authority_dir)):
        auth_path = os.path.join(authority_dir, auth, "artifacts.json")
        if not os.path.exists(auth_path):
            continue
        for rec in load(auth_path)["artifacts"]:
            if decision_filter and rec["id"] != decision_filter:
                continue
            links = case_links(rec, apps)
            if not links:
                continue
            transition = rec.get("transition") or {}
            policy = transition.get("policy") or "review"
            explicit = bool(transition)
            for app in apps:
                if app["authority"] != auth:
                    continue
                L = lineages.get(app["lineage"])
                if not L:
                    continue
                hits = [l for l in links if l["case"] in L["cases"]]
                if not hits:
                    continue
                hit = hits[0]
                # receipts covering every post-decision build of this app?
                post = [b for b in app["builds"]
                        if _ver(b["built_under"]) >= _ver(target_version)]
                cover = None
                if post and all(b["_receipt"] is not None for b in post):
                    areas = set()
                    for b in post:
                        areas |= _tokens(" ".join(b["_receipt"].get("areas_modified") or []))
                    cover = {"refs": [b["_receipt_ref"] for b in post], "areas": areas}
                for build in app["builds"]:
                    trigger = _trigger_for2(rec, build, L, cover)
                    is_source = any(e["revision"] == build["revision"]
                                    for e in L["events"].get(rec["id"], []))
                    closer = None
                    for other in app["builds"]:
                        other_rec = other["_receipt"]
                        if (other_rec and other["revision"] != build["revision"]
                                and rec["id"] in (other_rec.get("migration_for") or [])):
                            closer = {"ref": other["_receipt_ref"], "revision": other["revision"],
                                      "verification": other_rec.get("verification")}
                    tr = dict(transition)
                    if not explicit:
                        tr["legacy_default"] = True
                    cls, reason, trigger_state, obligation = classify(
                        build, rec["id"], rec["id"] in build["_adopted"], policy, tr,
                        target_version, trigger, is_source, closer)
                    involved = set()
                    if build["_receipt"] is not None:
                        involved.add(build["_receipt_ref"])
                    involved.update(e["ref"] for e in L["events"].get(rec["id"], []))
                    if closer:
                        involved.add(closer["ref"])
                    receipt_status = None
                    if involved:
                        receipt_status = ("confirmed" if involved <= L["confirmed"]
                                          else "unconfirmed")
                    findings.append({
                        "id": "finding/%s/%s/%s/%s" % (
                            app["name"], _slug(rec["id"]), target_version, build["revision"]),
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
                        "link": hit,
                        "trigger_state": trigger_state,
                        "obligation": obligation,
                        "receipt_status": receipt_status,
                        "reason": reason,
                    })
    return findings


def _trigger_for2(rec, build, L, cover):
    """trigger_state for a finding: events win; receipts can prove not_occurred;
    otherwise unknown."""
    ev = L["events"].get(rec["id"], [])
    if ev:
        return {"state": "occurred",
                "evidence": [e["ref"] for e in ev],
                "basis": "recorded modification of the affected area without migration"}
    if cover:
        scope = _tokens((rec.get("transition") or {}).get("scope") or "")
        if scope and not (cover["areas"] & scope):
            return {"state": "not_occurred",
                    "evidence": list(cover["refs"]),
                    "basis": "receipts cover the post-decision modification history; "
                             "none recorded a change to this area"}
    return {"state": "unknown",
            "basis": "complete modification history not established "
                     "(no receipts covering the window)"}


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
                        "built_under", "target_version", "obligation", "receipt_status"))
            if same:
                reused += 1
            else:
                f["assessed_at"] = now
                f["previous"] = {k: old.get(k) for k in ("class", "obligation",
                                                         "trigger_state", "assessed_at", "reason")}
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
    ap.add_argument("--decision", default=None, help="assess a single decision id only")
    ap.add_argument("--report", default=None, help="write the report JSON here")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    findings = sweep(os.path.join(REPO, args.authority) if not os.path.isabs(args.authority) else args.authority,
                     os.path.join(REPO, args.portfolio) if not os.path.isabs(args.portfolio) else args.portfolio,
                     args.target_version, decision_filter=args.decision)
    store = os.path.join(REPO, args.store) if not os.path.isabs(args.store) else args.store
    stats = upsert(store, findings, now)

    counts = {c: sum(1 for f in findings if f["class"] == c) for c in CLASSES}
    obligations = {}
    for f in findings:
        o = f.get("obligation")
        if o:
            obligations[o["state"]] = obligations.get(o["state"], 0) + 1
    report = {"target_version": args.target_version, "decision": args.decision,
              "counts": counts, "obligations": obligations, "store": stats,
              "findings": sorted(findings, key=lambda f: f["id"])}
    if args.report:
        with open(args.report, "w") as fh:
            json.dump(report, fh, indent=1, ensure_ascii=False)
            fh.write("\n")

    if not args.quiet:
        print("findings: %d — %s" % (len(findings),
              " · ".join("%s %d" % (c, counts[c]) for c in CLASSES if counts[c])))
        if obligations:
            print("obligations: " + " · ".join("%s %d" % kv for kv in sorted(obligations.items())))
        print("store: %s (%d new, %d reused, %d superseded; total %d)"
              % (args.store, stats["new"], stats["reused"], stats["superseded"], stats["total"]))
        for f in findings:
            if f["class"] in ("rectify", "review") or (f.get("trigger_state") or {}).get("state") == "occurred":
                ob = (" obligation=%s" % f["obligation"]["state"]) if f.get("obligation") else ""
                tr = (" trigger=%s" % f["trigger_state"]["state"]) if f.get("trigger_state") else ""
                print("  [%s%s%s] %s · %s (%s) — %s" % (
                    f["class"], ob, tr, f["application"], f["decision"], f["revision"],
                    f["reason"][:130]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
