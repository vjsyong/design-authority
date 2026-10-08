"""da — Design Authority CLI. Same library the MCP server exposes.

    da overview | search Q | inspect ID | resolve PROBLEM | validate TARGET
    da golden | gaps | gap-add | propose
"""
import argparse
import json
import os
import sys

from . import records
from .pack import Pack, PackError
from .resolve import resolve, resolve_golden
from .validate import validate

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_PACK = os.path.join(ROOT, "packs", "triage")


def _load_pack(args):
    path = args.pack or os.environ.get("DA_PACK") or DEFAULT_PACK
    return Pack(path)


def _dump(obj):
    print(json.dumps(obj, indent=1))


def cmd_overview(pack, args):
    counts = {}
    for a in pack.artifacts:
        counts[a["kind"]] = counts.get(a["kind"], 0) + 1
    data = {
        "authority": pack.identity(),
        "description": pack.manifest.get("description"),
        "counts": {"artifacts": counts, "rules": len(pack.rules),
                   "recipes": len(pack.recipes), "fallbacks": len(pack.fallbacks),
                   "prohibitions": len(pack.prohibitions)},
        "capabilities": pack.manifest.get("capabilities"),
        "policy": pack.manifest.get("policy"),
        "resolution_semantics": [
            "CONFLICT: request contradicts an explicit constraint (prohibition/rule).",
            "RESOLVED: a direct artifact defines the solution.",
            "COMPOSE: a sanctioned recipe composes existing artifacts.",
            "FALLBACK: a sanctioned generic fallback applies.",
            "UNDEFINED: no adequate authority answer exists (structured, not an error).",
        ],
    }
    if args.json:
        return _dump(data)
    i = data["authority"]
    print("%s — %s (format %s)" % (i["authority"], i["version"],
                                   pack.manifest.get("format_version")))
    print("snapshot: %s @ %s" % (pack.manifest.get("snapshot", {}).get("repo"),
                                 (i["commit"] or "")[:10]))
    print("artifacts: " + ", ".join("%s=%d" % kv for kv in sorted(counts.items())))
    print("rules=%d recipes=%d fallbacks=%d prohibitions=%d"
          % (len(pack.rules), len(pack.recipes), len(pack.fallbacks),
             len(pack.prohibitions)))
    print("resolution: CONFLICT -> RESOLVED -> COMPOSE -> FALLBACK -> UNDEFINED")


def cmd_search(pack, args):
    kinds = args.kinds.split(",") if args.kinds else None
    hits = pack.search(args.query, kinds=kinds, limit=args.limit)
    if args.json:
        return _dump(hits)
    for h in hits:
        print("%6.1f  %-12s %-28s %s" % (h["score"], h["kind"], h["id"], h["title"]))


def cmd_inspect(pack, args):
    entry = pack.by_id.get(args.id)
    if not entry:
        print("unknown id: %s" % args.id, file=sys.stderr)
        return 1
    _dump(entry)


def cmd_resolve(pack, args):
    context = json.loads(args.context) if args.context else {}
    result = resolve(pack, " ".join(args.problem), context)
    if args.json:
        return _dump(result)
    print("OUTCOME: %s" % result["outcome"])
    res = result.get("resolution")
    if res:
        print(json.dumps(res, indent=1))
    if result.get("precedents"):
        print("precedents (negative — scope-verdicts: governs | outside | ambiguous):")
        for p in result["precedents"]:
            print("  [%s] %s — %s" % (p.get("verdict"), p.get("title"),
                                      (p.get("reason") or "")[:120]))
            if p.get("verdict") == "governs":
                for t in p.get("try", []):
                    print("    try: %s" % t)
            elif p.get("verdict") == "outside":
                print("    outside the decline's scope — proceed as a marked improvisation")
    if result.get("candidates"):
        print("candidates (provisional — NOT authority):")
        for c in result["candidates"]:
            print("  %s — %s" % (c.get("title"), (c.get("summary") or "")[:120]))
            pw = c.get("promote_when") or []
            if pw:
                print("    promote when: %s" % pw[0])
    if result.get("closest"):
        print("closest:")
        for c in result["closest"]:
            print("  %6.1f  %s" % (c["score"], c["id"]))
    if result.get("why"):
        print("why: %s" % result["why"])
    if result.get("next"):
        print("next: %s" % result["next"])


def cmd_validate(pack, args):
    result = validate(pack, args.target, snapshot=args.snapshot)
    if args.json:
        return _dump(result)
    s = result["summary"]
    print("target: %s" % result["target"])
    for v in result["validators"]:
        print("validator %s: %s%s" % (v["validator"], v["status"],
              " (%s)" % v.get("message") if v.get("status") == "error" else ""))
    print("findings: %d  errors=%d warnings=%d info=%d  spec score=%s"
          % (s["total"], s["counts"].get("error", 0),
             s["counts"].get("warning", 0), s["counts"].get("info", 0),
             s["score"].get("value")))
    for f in result["findings"][:40]:
        print("  %-8s %-8s %s:%s  %s" % (f["severity"], f["rule"],
              f["location"]["path"], f["location"]["line"], f["message"]))
    if len(result["findings"]) > 40:
        print("  … %d more" % (len(result["findings"]) - 40))


def cmd_golden(pack, args):
    path = args.file or os.path.join(os.path.dirname(pack.path), "triage", "golden.json")
    if not os.path.exists(path):
        print("golden file not found: %s" % path, file=sys.stderr)
        return 2
    with open(path) as fh:
        cases = json.load(fh)["cases"]
    report = resolve_golden(pack, cases)
    if args.json:
        return _dump(report)
    for row in report["rows"]:
        mark = "ok " if row["ok"] else "MISS"
        print("%s  %-10s (want %-10s) %s%s" % (mark, row["got"], row["expected"],
              row["problem"], "  -> %s" % row["resolution_id"] if row["resolution_id"] else ""))
    print("agreement: %d/%d (%.0f%%)" % (report["passed"], report["total"],
                                         100 * report["rate"]))


def cmd_gaps(pack, args):
    ws = args.workspace or os.getcwd()
    gaps = records.list_gaps(ws)
    if args.json:
        return _dump(gaps)
    if not gaps:
        print("no gaps recorded in %s" % ws)
    for g in gaps:
        print("%s  [%s]  %s" % (g["id"], g["status"], g["need"][:90]))


def cmd_gap_add(pack, args):
    ws = args.workspace or os.getcwd()
    context = json.loads(args.context) if args.context else {}
    gap = records.add_gap(pack, ws, args.need, context=context,
                          scope_hint=args.scope or "unknown")
    _dump(gap)


def cmd_propose(pack, args):
    ws = args.workspace or os.getcwd()
    with open(args.file) as fh:
        proposal = json.load(fh)
    try:
        record = records.add_proposal(pack, ws, args.gap, proposal)
    except ValueError as exc:
        print("proposal rejected: %s" % exc, file=sys.stderr)
        return 2
    _dump(record)


def cmd_precedents(pack, args):
    if args.query:
        recs = [dict(m["record"], verdict=m["verdict"])
                for m in pack.precedent_matches(args.query, limit=25)]
    else:
        recs = pack.precedents
    data = {"authority": pack.identity(), "count": len(recs), "precedents": recs}
    if args.json:
        return _dump(data)
    print("%s — %d negative precedent(s) (policy declines only)" % (pack.identity()["authority"], len(recs)))
    for p in recs:
        print("  %-18s %s" % (p.get("decision", "?"), p.get("id")))
        if p.get("verdict"):
            print("      verdict: %s" % p["verdict"])
        print("      request: %s" % (p.get("request", "")[:100]))
        print("      why:     %s" % (p.get("reason", "")[:100]))


def cmd_precedent_check(pack, args):
    ask = args.ask
    results = pack.precedent_matches(ask, limit=10)
    cands = pack.candidate_matches(ask, limit=5)
    data = {"authority": pack.identity(), "ask": ask,
            "results": [{"id": m["record"]["id"], "verdict": m["verdict"],
                         "boundary_hits": m["boundary_hits"],
                         "grounds": m["record"].get("grounds"),
                         "try": m["record"].get("try")} for m in results],
            "candidates": [{"id": c.get("id"), "summary": c.get("summary"),
                            "promote_when": c.get("promote_when")} for c in cands]}
    if args.json:
        return _dump(data)
    print("ask: %s" % ask)
    if not results:
        print("  not governed by any precedent — proceed per the ordinary rules "
              "(improvise in character, mark, report a gap if it recurs)")
    for m in results:
        r = m["record"]
        print("  [%s] %s — %s" % (m["verdict"], r["id"], r.get("title")))
        if m["verdict"] == "governs":
            for t in r.get("try", []):
                print("      try: %s" % t)
        elif m["verdict"] == "outside":
            print("      outside this decline's scope (boundary: %s) — go ahead and mark it"
                  % ", ".join(m["boundary_hits"][:2]))
        else:
            print("      ambiguous (domain + boundary overlap) — treat as an ordinary "
                  "improvisation unless a human rules on it")
    for c in cands:
        print("  [candidate] %s — %s" % (c["id"], (c.get("summary") or "")[:110]))
        pw = c.get("promote_when") or []
        if pw:
            print("      promote when: %s" % pw[0])


def cmd_candidates(pack, args):
    recs = pack.candidate_matches(args.query, limit=25) if args.query else pack.candidates
    data = {"authority": pack.identity(), "count": len(recs), "candidates": recs}
    if args.json:
        return _dump(data)
    print("%s — %d candidate(s) (provisional — NOT authority)"
          % (pack.identity()["authority"], len(recs)))
    for c in recs:
        print("  %s — %s" % (c.get("id"), c.get("title")))
        print("      %s" % (c.get("summary", "")[:110]))


def cmd_review(pack, args):
    ws = args.workspace or os.getcwd()
    notes = None
    if args.notes:
        with open(args.notes) as fh:
            notes = fh.read()
    elif args.note:
        notes = args.note
    try:
        record = records.set_proposal_review(ws, args.proposal, args.verdict,
                                             notes=notes)
    except ValueError as exc:
        print("review failed: %s" % exc, file=sys.stderr)
        return 2
    _dump({"id": record["id"], "status": record["status"],
           "review": record["review"]})


def main(argv=None):
    ap = argparse.ArgumentParser(prog="da", description=__doc__)
    ap.add_argument("--pack", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("overview"); p.add_argument("--json", action="store_true")

    p = sub.add_parser("search")
    p.add_argument("query"); p.add_argument("--kinds", default="")
    p.add_argument("--limit", type=int, default=10); p.add_argument("--json", action="store_true")

    p = sub.add_parser("inspect"); p.add_argument("id")

    p = sub.add_parser("resolve")
    p.add_argument("problem", nargs="+")
    p.add_argument("--context", default=""); p.add_argument("--json", action="store_true")

    p = sub.add_parser("validate")
    p.add_argument("target"); p.add_argument("--snapshot", default=None)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("golden")
    p.add_argument("--file", default=None); p.add_argument("--json", action="store_true")

    p = sub.add_parser("gaps")
    p.add_argument("--workspace", default=None); p.add_argument("--json", action="store_true")

    p = sub.add_parser("gap-add")
    p.add_argument("--need", required=True); p.add_argument("--context", default="")
    p.add_argument("--scope", default=None); p.add_argument("--workspace", default=None)

    p = sub.add_parser("propose")
    p.add_argument("--gap", required=True); p.add_argument("--file", required=True)
    p.add_argument("--workspace", default=None)

    p = sub.add_parser("review")
    p.add_argument("--proposal", required=True)
    p.add_argument("--verdict", required=True, choices=["accept", "reject", "needs-info"])
    p.add_argument("--note", default=None)
    p.add_argument("--notes", default=None, help="file with the full review notes")
    p.add_argument("--workspace", default=None)

    p = sub.add_parser("precedents")
    p.add_argument("--query", default="")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("precedent-check")
    p.add_argument("--ask", required=True)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("candidates")
    p.add_argument("--query", default="")
    p.add_argument("--json", action="store_true")

    args = ap.parse_args(argv)
    try:
        pack = _load_pack(args)
    except PackError as exc:
        print("pack error: %s" % exc, file=sys.stderr)
        return 2

    handler = {"overview": cmd_overview, "search": cmd_search, "inspect": cmd_inspect,
               "resolve": cmd_resolve, "validate": cmd_validate, "golden": cmd_golden,
               "gaps": cmd_gaps, "gap-add": cmd_gap_add, "propose": cmd_propose,
               "review": cmd_review, "precedents": cmd_precedents,
               "precedent-check": cmd_precedent_check,
               "candidates": cmd_candidates}[args.cmd]
    return handler(pack, args) or 0


if __name__ == "__main__":
    sys.exit(main())
