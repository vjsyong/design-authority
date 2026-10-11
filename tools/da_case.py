#!/usr/bin/env python3
"""da_case — the canonical Case read model (spec: docs/16-case-read-model.md).

One interface over the governance record stores: gaps, proposals, the
codification ledger, reconciliation findings, decision receipts, and disputes.
A Case is a normalized, append-only EVENT VIEW over existing records: nothing
is copied, nothing is rewritten, every event names its source (file + record
id), and output is deterministic. Per the owner's direction (da_nextsteps.md
section 2), existing stores are NOT migrated; this read model must prove
itself against the current corpus first.

    python3 tools/da_case.py list [--json]
    python3 tools/da_case.py show <gap/… | dispute/… | prop/…> [--json]
    python3 tools/da_case.py why <record id> [--json]

Event kinds (v0, all derived):
    gap_reported             the need and its context, from gaps.jsonl
    evidence_attached        the gap's recorded evidence, when non-empty
    proposal_submitted       a proposal against the gap, with its entries
    proposal_reviewed        the recorded verdict (accepted | rejected | needs-info)
    authority_published      the codification ledger row (pack + version + entries)
    receipt_recorded         a decision receipt (revisions, deviations, migration)
    impact_assessed          a reconciliation finding on an entry of this case
    migration_required       an obligation (scheduled | due | overdue)
    migration_verified       an obligation closed with a verification result
    obligation_closed        an obligation closed (alias of the above, kept explicit)
    dispute_raised           a disputed resolution, from its recorded store

Reserved for the recorded-case era (docs/14 section 10; not produced here):
case numbering (case/NNNN) and first-class recorded events (`impact_finding`,
`migration_decision`). Until then cases are addressed by their root record id.

Read-only by design: this tool never writes to any store.
"""
import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LEDGER = "docs/synthesis/data/codified.json"
ADJUDICATION = "docs/synthesis/data/adjudication.json"
# Real governance history only: the `findings-defaults` store is the DEFAULTS
# SCENARIO check (no transition blocks), not an assessment of any build, and is
# deliberately excluded.
FINDING_GLOBS = ("docs/experiments/reconcile-cadence/findings.jsonl",
                 "docs/experiments/reconcile-cadence/closure/findings.jsonl")
DISPUTE_REPLAY_GLOBS = ("docs/experiments/disputes/replay-*.json",)
DECISION_SOURCES = {"wink": "docs/synthesis/wink/decisions.json",
                    "leader": "docs/synthesis/leader/decisions.json",
                    "dominion": "docs/synthesis/dominion/decisions.json"}
PACK_RECORD_FILES = ("artifacts", "rules", "prohibitions", "fallbacks", "recipes")


def _rel(path):
    return os.path.relpath(path, ROOT)


def _load(path):
    with open(path) as fh:
        return json.load(fh)


def _load_jsonl(path):
    out = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


# --------------------------------------------------------------------- stores

# Repo-wide discovery: every workspace's `.design-authority` store is part of
# the governance corpus. Sealed experiment materials are excluded (they are
# frozen fixtures, not history), and `.git` is never entered.
SKIP_FRAGMENTS = ("docs/experiments/seed-evolution/annexes/",)


def workspace_stores():
    """[(workspace rel path, store dir rel path)] repo-wide, sorted."""
    out = []
    for dirpath, dirnames, _ in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        rel = _rel(dirpath)
        relslash = rel + "/" if rel != "." else ""
        if any(frag in relslash for frag in SKIP_FRAGMENTS):
            continue
        if os.path.basename(dirpath) == ".design-authority":
            out.append((os.path.dirname(rel), rel))
    return sorted(set(out))


def scan_gaps():
    """[(workspace, gap record, file)] from every store in the corpus."""
    out = []
    for ws, adir in workspace_stores():
        path = os.path.join(ROOT, adir, "gaps.jsonl")
        if not os.path.exists(path):
            continue
        for rec in _load_jsonl(path):
            out.append((ws, rec, _rel(path)))
    return out


def scan_proposals():
    """[(workspace, proposal record, file)] from every store in the corpus."""
    out = []
    for ws, adir in workspace_stores():
        pdir = os.path.join(ROOT, adir, "proposals")
        if not os.path.isdir(pdir):
            continue
        for f in sorted(glob.glob(os.path.join(pdir, "*.json"))):
            out.append((ws, _load(f), _rel(f)))
    return out


def scan_disputes():
    """[(root, dispute row, file)]: live stores plus recorded replay fixtures
    (replay rows decorate matching live records with their standing state)."""
    out = []
    for _, adir in workspace_stores():
        path = os.path.join(ROOT, adir, "disputes.jsonl")
        if not os.path.exists(path):
            continue
        for rec in _load_jsonl(path):
            out.append((rec.get("id"), rec, _rel(path)))
    seen = {rid for rid, _, _ in out}
    for pat in DISPUTE_REPLAY_GLOBS:
        for path in sorted(glob.glob(os.path.join(ROOT, pat))):
            replay = _load(path)
            for row in replay.get("rows", []):
                if row.get("id") not in seen:
                    out.append((row.get("id"), row, _rel(path)))
                else:
                    for i, (rid, rec, f) in enumerate(out):
                        if rid == row.get("id"):
                            rec.setdefault("still_stands", row.get("still_stands"))
    return out


def scan_findings():
    """[(finding, file)] across the reconciliation stores, deduplicated by
    finding id: superseding runs (the closure store) carry the final state, so
    a closed obligation wins; otherwise the later assessment wins."""
    by_id = {}
    order = []
    for rel in FINDING_GLOBS:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        for rec in _load_jsonl(path):
            fid = rec.get("id")
            if fid not in by_id:
                by_id[fid] = (rec, rel)
                order.append(fid)
            else:
                cur, cur_file = by_id[fid]
                def rank(item):
                    f, _ = item
                    ob = (f.get("obligation") or {}).get("state")
                    return (ob == "closed", f.get("assessed_at") or "")
                if rank((rec, rel)) >= rank((cur, cur_file)):
                    by_id[fid] = (rec, rel)
    return [by_id[fid] for fid in order]


def scan_receipts():
    """[(receipt, file)] decision receipts from every store in the corpus."""
    out = []
    for _, adir in workspace_stores():
        rdir = os.path.join(ROOT, adir, "receipts")
        if not os.path.isdir(rdir):
            continue
        for path in sorted(glob.glob(os.path.join(rdir, "*.json"))):
            out.append((_load(path), _rel(path)))
    return out


def scan_ledger():
    """codified.json: {prop id: {status, verdict, reviewed_at, outcome, pack, version, entries}}."""
    path = os.path.join(ROOT, LEDGER)
    return _load(path) if os.path.exists(path) else {}


def scan_adjudication():
    """{prop id: adjudication row} — rationale for the review outcome."""
    path = os.path.join(ROOT, ADJUDICATION)
    if not os.path.exists(path):
        return {}
    out = {}
    for row in _load(path):
        if row.get("prop_id"):
            out.setdefault(row["prop_id"], row)
    return out


def scan_records():
    """{(record id): (record, pack, pack version)} across every authority pack."""
    out = {}
    for pack_dir in sorted(glob.glob(os.path.join(ROOT, "authorities", "*"))):
        auth_file = os.path.join(pack_dir, "authority.json")
        if not os.path.exists(auth_file):
            continue
        manifest = _load(auth_file)
        pack = manifest.get("id") or os.path.basename(pack_dir)
        version = manifest.get("version")
        for kind in PACK_RECORD_FILES:
            f = os.path.join(pack_dir, kind + ".json")
            if not os.path.exists(f):
                continue
            for rec in _load(f).get(kind, []):
                if rec.get("id"):
                    out[rec["id"]] = (rec, pack, version, _rel(f))
    return out


def scan_decisions():
    """{decision id: decision record} from the local decision ledgers."""
    out = {}
    for src, rel in DECISION_SOURCES.items():
        path = os.path.join(ROOT, rel)
        if os.path.exists(path):
            for d in _load(path).get("decisions", []):
                out[d["id"]] = d
    return out


# -------------------------------------------------------------------- events

def _ev(kind, at, source_file, record_id, **detail):
    ev = {"kind": kind, "at": at, "source": {"file": source_file, "record": record_id}}
    ev.update(detail)
    return ev


def gap_events(gap, gap_file, proposals, findings, receipts, ledger, adjudication):
    """The normalized event timeline for one gap root."""
    gid = gap["id"]
    ev = [_ev("gap_reported", gap.get("created"), gap_file, gid,
              need=gap.get("need"), context=gap.get("context"),
              authority=gap.get("authority"), scope_hint=gap.get("scope_hint"),
              status=gap.get("status"))]
    for i, e in enumerate(gap.get("evidence") or []):
        ev.append(_ev("evidence_attached", None, gap_file, gid, evidence=e))
    entry_ids = []
    for ws, prop, pfile in proposals:
        if prop.get("gap_id") != gid:
            continue
        entries = []
        proposed = prop.get("proposed")
        if isinstance(proposed, dict) and "add" in proposed:
            items = proposed["add"]
            proposed = items if isinstance(items, list) else [items]
        elif isinstance(proposed, dict):
            proposed = [proposed]
        else:
            proposed = []
        for item in proposed:
            if isinstance(item, dict) and item.get("id"):
                entries.append(item["id"])
        entry_ids.extend(entries)
        review = prop.get("review") or {}
        ev.append(_ev("proposal_submitted", review.get("reviewed_at"), pfile, prop["id"],
                      gap=gid, workspace=ws, problem=prop.get("problem"),
                      entries=entries, note=prop.get("note")))
        row = ledger.get(prop["id"]) or {}
        adj = adjudication.get(prop["id"]) or {}
        ev.append(_ev("proposal_reviewed", review.get("reviewed_at"), pfile, prop["id"],
                      outcome=prop.get("status"), verdict=review.get("verdict") or prop.get("verdict"),
                      rationale=adj.get("rationale")))
        if row.get("outcome") == "codified":
            ev.append(_ev("authority_published", row.get("reviewed_at"), LEDGER, prop["id"],
                          pack=row.get("pack"), version=row.get("version"),
                          entries=row.get("entries")))
        if row.get("outcome") == "precedent" and row.get("precedent_id"):
            ev.append(_ev("precedent_recorded", row.get("reviewed_at"), LEDGER, prop["id"],
                          precedent=row["precedent_id"]))
    for rec, rfile in receipts:
        applied = set(rec.get("decisions_applied") or []) | set(rec.get("migration_for") or [])
        if applied & set(entry_ids):
            ev.append(_ev("receipt_recorded", rec.get("built_at"), rfile,
                          "%s/%s" % (rec.get("application"), rec.get("revision")),
                          decisions_applied=rec.get("decisions_applied"),
                          migration_for=rec.get("migration_for"),
                          deviations=rec.get("deviations"),
                          verification=(rec.get("verification") or {}).get("result")
                          if isinstance(rec.get("verification"), dict) else rec.get("verification")))
    for f, ffile in findings:
        link = f.get("link") or {}
        if link.get("case") != gid:
            continue
        ev.append(_ev("impact_assessed", f.get("assessed_at"), ffile, f["id"],
                      application=f.get("application"), revision=f.get("revision"),
                      decision=f.get("decision"), outcome_class=f.get("class"),
                      policy=f.get("policy"), reason=f.get("reason")))
        ob = f.get("obligation") or {}
        if ob.get("state") in ("scheduled", "due", "overdue"):
            ev.append(_ev("migration_required", f.get("assessed_at"), ffile, f["id"],
                          application=f.get("application"), revision=f.get("revision"),
                          decision=f.get("decision"), state=ob.get("state"), by=ob.get("by")))
        elif ob.get("state") == "closed":
            ver = ob.get("verification") or {}
            ev.append(_ev("migration_verified", f.get("assessed_at"), ffile, f["id"],
                          application=f.get("application"), revision=f.get("revision"),
                          decision=f.get("decision"), closed_by=ob.get("closed_by"),
                          verification=ver.get("result") if isinstance(ver, dict) else ver))
            ev.append(_ev("obligation_closed", f.get("assessed_at"), ffile, f["id"],
                          application=f.get("application"), revision=f.get("revision"),
                          decision=f.get("decision"), closed_by=ob.get("closed_by")))
    return ev, entry_ids


def dispute_events(row, dfile):
    rid = row.get("id")
    return [_ev("dispute_raised", row.get("created"), dfile, rid,
                query=row.get("query"),
                resolved_to=row.get("resolved_to") or row.get("disputed"),
                outcome=row.get("outcome"), reason=row.get("reason"),
                status=row.get("status"), still_stands=row.get("still_stands"))]


KIND_RANK = {"gap_reported": 0, "evidence_attached": 1, "proposal_submitted": 2,
             "proposal_reviewed": 3, "authority_published": 4, "precedent_recorded": 5,
             "receipt_recorded": 6, "impact_assessed": 7, "migration_required": 8,
             "migration_verified": 9, "obligation_closed": 10, "dispute_raised": 11}


def sort_events(ev):
    return sorted(ev, key=lambda e: (e.get("at") or "",
                                     KIND_RANK.get(e["kind"], 99),
                                     str(e["source"]["record"])))


# --------------------------------------------------------------------- views

def build():
    return {"gaps": scan_gaps(), "proposals": scan_proposals(),
            "disputes": scan_disputes(), "findings": scan_findings(),
            "receipts": scan_receipts(), "ledger": scan_ledger(),
            "adjudication": scan_adjudication(), "records": scan_records(),
            "decisions": scan_decisions()}


def _primary_index(occurrences):
    """Occurrences are (workspace, record, file). Derived verification probe
    workspaces re-file a gap copied from a build workspace; the primary
    recording is the first non-verification store (then sorted order)."""
    order = sorted(occurrences, key=lambda o: ("docs/verification/" in o[0], o[0]))
    return order


def resolve_root(db, ident):
    """(title, events) for a gap / dispute / proposal id."""
    gap_occ = [(ws, gap, gfile) for ws, gap, gfile in db["gaps"] if gap["id"] == ident]
    if gap_occ:
        occ = _primary_index(gap_occ)
        ws, gap, gfile = occ[0]
        ev, _ = gap_events(gap, gfile, db["proposals"], db["findings"],
                           db["receipts"], db["ledger"], db["adjudication"])
        title = "%s  [%s%s]" % (gap.get("need"), ws,
                                "; recorded in %d stores" % len(occ) if len(occ) > 1 else "")
        return (title, sort_events(ev))
    for rid, row, dfile in db["disputes"]:
        if rid == ident:
            return ("disputed resolution: %s" % row.get("query"), dispute_events(row, dfile))
    for ws, prop, pfile in db["proposals"]:
        if prop["id"] == ident:
            gap = next((g for w, g, f in db["gaps"] if g["id"] == prop.get("gap_id")), None)
            if gap:
                ev, _ = gap_events(gap, pfile, [p for p in db["proposals"] if p[1]["id"] == ident],
                                   db["findings"], db["receipts"], db["ledger"], db["adjudication"])
                return ("%s  (proposal %s)" % (gap.get("need"), ident), sort_events(ev))
    return (None, None)


def why_view(db, rid):
    """The record view: provenance, decisions, chain, impacts, disputes."""
    hit = db["records"].get(rid)
    if not hit:
        return None
    rec, pack, version, rfile = hit
    out = {"record": {"id": rid, "pack": pack, "version": version, "title": rec.get("title"),
                      "status": rec.get("status"), "source_file": rfile},
           "provenance": {}, "decisions": [], "chain": [], "findings": [], "disputes": [],
           "receipts": []}
    prov = rec.get("provenance") or {}
    if rec.get("compiled_from"):
        out["provenance"]["compiled_from"] = rec["compiled_from"]
    if rec.get("exception"):
        out["provenance"]["exception"] = rec["exception"]
    if prov:
        out["provenance"]["proposal"] = prov.get("proposal")
        out["provenance"]["gap"] = prov.get("gap")
        out["provenance"]["codified_at"] = prov.get("codified_at")
    # decisions: dossier lineage (compiled_from = decision ids) + decisions behind this record's proposals
    dids = [d for d in (rec.get("compiled_from") or []) if not str(d).startswith("prop/")]
    for ws, prop, pfile in db["proposals"]:
        for item in _proposed_items(prop):
            if item.get("id") == rid:
                for d in prop.get("decisions") or []:
                    dids.append(d)
    for d in sorted(set(dids)):
        dec = db["decisions"].get(d)
        row = {"id": d, "file": DECISION_SOURCES.get(pack)}
        if dec:
            row.update({"decision": dec.get("decision"), "status": dec.get("status"),
                        "alternatives": dec.get("alternatives"), "review": dec.get("review")})
        out["decisions"].append(row)
    # chain: proposals -> gaps
    seen_gaps = set()
    for ws, prop, pfile in db["proposals"]:
        for item in _proposed_items(prop):
            if item.get("id") != rid:
                continue
            out["chain"].append({"proposal": prop["id"], "gap": prop.get("gap_id"),
                                 "workspace": ws, "status": prop.get("status")})
            if prop.get("gap_id"):
                seen_gaps.add(prop["gap_id"])
    for f, ffile in db["findings"]:
        if f.get("decision") == rid:
            out["findings"].append({"id": f["id"], "class": f.get("class"),
                                    "application": f.get("application"),
                                    "revision": f.get("revision"),
                                    "obligation": f.get("obligation"),
                                    "assessed_at": f.get("assessed_at"), "file": ffile})
    for did, row, dfile in db["disputes"]:
        if rid in (row.get("resolved_to"), row.get("disputed")):
            out["disputes"].append({"id": did, "query": row.get("query"),
                                    "still_stands": row.get("still_stands"), "file": dfile})
    for r, rfile in db["receipts"]:
        if rid in set(r.get("decisions_applied") or []) | set(r.get("migration_for") or []):
            out["receipts"].append({"application": r.get("application"),
                                    "revision": r.get("revision"), "file": rfile,
                                    "deviations": r.get("deviations")})
    return out


def _proposed_items(prop):
    proposed = prop.get("proposed")
    if isinstance(proposed, dict) and "add" in proposed:
        items = proposed["add"]
        return [i for i in (items if isinstance(items, list) else [items]) if isinstance(i, dict)]
    elif isinstance(proposed, dict):
        return [proposed]
    return []


def list_view(db):
    findings_by_case = {}
    for f, _ in db["findings"]:
        case = (f.get("link") or {}).get("case")
        if case:
            findings_by_case[case] = findings_by_case.get(case, 0) + 1
    props_by_gap = {}
    for ws, prop, pfile in db["proposals"]:
        props_by_gap.setdefault(prop.get("gap_id"), []).append(prop["id"])
    occ_by_gap = {}
    for ws, gap, gfile in db["gaps"]:
        occ_by_gap.setdefault(gap["id"], []).append((ws, gap, gfile))
    rows = []
    for gid in sorted(occ_by_gap):
        occ = _primary_index(occ_by_gap[gid])
        ws, gap, gfile = occ[0]
        rows.append({"id": gid, "kind": "gap", "workspace": ws, "status": gap.get("status"),
                     "need": gap.get("need"), "proposals": sorted(props_by_gap.get(gid, [])),
                     "findings": findings_by_case.get(gid, 0), "store": gfile,
                     "occurs": len(occ),
                     "recorded_in": sorted(w for w, _, _ in occ)})
    disputes = []
    for rid, row, dfile in db["disputes"]:
        disputes.append({"id": rid, "kind": "dispute", "query": row.get("query"),
                         "status": row.get("status"), "still_stands": row.get("still_stands"),
                         "store": dfile})
    return {"gaps": rows, "disputes": disputes,
            "counts": {"gaps": len(rows), "gap_occurrences": len(db["gaps"]),
                       "disputes": len(disputes), "proposals": len(db["proposals"]),
                       "findings": len(db["findings"]), "receipts": len(db["receipts"])}}


# ----------------------------------------------------------------------- cli

def main(argv=None):
    ap = argparse.ArgumentParser(prog="da_case",
                                 description="one interface over the governance record stores (docs/16)")
    ap.add_argument("--json", action="store_true", help="machine output")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p_show = sub.add_parser("show")
    p_show.add_argument("id")
    p_why = sub.add_parser("why")
    p_why.add_argument("record")
    args = ap.parse_args(argv)

    db = build()
    if args.cmd == "list":
        view = list_view(db)
        if args.json:
            print(json.dumps(view, indent=1, sort_keys=True))
            return 0
        c = view["counts"]
        print("cases: %d gaps (%d store occurrences), %d disputes | stores: %d proposals, %d findings, %d receipts"
              % (c["gaps"], c["gap_occurrences"], c["disputes"], c["proposals"], c["findings"], c["receipts"]))
        for r in view["gaps"]:
            print("  %-32s [%s]  %-34s props:%d findings:%d%s"
                  % (r["id"], r["status"] or "?", r["workspace"], len(r["proposals"]), r["findings"],
                     "  (%dx)" % r["occurs"] if r["occurs"] > 1 else ""))
        for r in view["disputes"]:
            print("  %-32s [%s]  %s%s" % (r["id"], r["status"] or "standing", r["query"],
                                          " (still stands)" if r["still_stands"] else ""))
        return 0

    if args.cmd == "show":
        title, ev = resolve_root(db, args.id)
        if title is None:
            print("unknown case id: %s" % args.id, file=sys.stderr)
            return 2
        if args.json:
            print(json.dumps({"id": args.id, "title": title, "events": ev or []},
                             indent=1, sort_keys=True))
            return 0
        print("case %s" % args.id)
        print("  %s" % title)
        for e in ev or []:
            at = e.get("at") or "-"
            detail = " ".join("%s=%s" % (k, json.dumps(v, ensure_ascii=False))
                              for k, v in sorted(e.items())
                              if k not in ("kind", "at", "source") and v is not None)
            print("  %s  %-20s %s" % (at, e["kind"], detail[:150]))
        return 0

    if args.cmd == "why":
        view = why_view(db, args.record)
        if view is None:
            print("unknown record id: %s" % args.record, file=sys.stderr)
            return 2
        if args.json:
            print(json.dumps(view, indent=1, sort_keys=True))
            return 0
        r = view["record"]
        print("%s — %s (%s %s)" % (r["id"], r["title"], r["pack"], r["version"]))
        prov = view["provenance"]
        if prov.get("proposal"):
            print("  provenance: codified from %s%s" % (prov["proposal"],
                  " via %s" % prov.get("gap") if prov.get("gap") else ""))
        if prov.get("compiled_from"):
            print("  compiled from: %s" % ", ".join(prov["compiled_from"]))
        if prov.get("exception"):
            print("  exception: %s" % json.dumps(prov["exception"], ensure_ascii=False)[:160])
        for d in view["decisions"]:
            print("  decision %s: %s" % (d["id"], (d.get("decision") or "-")[:160]))
            if d.get("alternatives"):
                print("    rejected: %s" % d["alternatives"][:140])
        for c in view["chain"]:
            print("  chain: %s (%s) -> %s [%s]" % (c["proposal"], c["status"], c["gap"], c["workspace"]))
        for f in view["findings"]:
            ob = f.get("obligation") or {}
            print("  finding: %s %s %s | %s%s" % (f["application"], f["revision"], f["class"],
                  f["assessed_at"], " | obligation %s" % ob.get("state") if ob else ""))
        for d in view["disputes"]:
            print("  dispute %s: %s%s" % (d["id"], d["query"],
                  " (still stands)" if d.get("still_stands") else ""))
        for rc in view["receipts"]:
            print("  receipt: %s %s (%s)" % (rc["application"], rc["revision"], rc["file"]))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
