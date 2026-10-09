"""da — Design Authority CLI. Same library the MCP server exposes.

    da overview | search Q | discover Q | inspect ID | resolve PROBLEM | validate TARGET
    da golden | gaps | gap-add | propose | dispute-add | disputes | dispute-replay

`discover` and `resolve --assist semantic` are optional retrieval extensions
(install extras: pip install fastembed numpy; build the index once with
tools/da_sem.py build). Retrieval only proposes; it never establishes
authority. Without the extras every lexical surface is unchanged.
"""
import argparse
import json
import os
import sys

from . import records
from .pack import Pack, PackError
from .resolve import resolve, resolve_golden, replay_disputes
from .validate import validate

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_PACK = os.path.join(ROOT, "authorities", "triage")
SEM_TOOLS = os.path.join(ROOT, "tools")


def _load_pack(args):
    path = args.pack or os.environ.get("DA_PACK") or DEFAULT_PACK
    return Pack(path)


def _dump(obj):
    print(json.dumps(obj, indent=1))


def _sem_state():
    """Optional semantic layer: (module, reason). Absent extras are fine."""
    try:
        if SEM_TOOLS not in sys.path:
            sys.path.insert(0, SEM_TOOLS)
        import da_sem  # noqa: WPS433 (optional dependency by design)
    except Exception as exc:  # pragma: no cover
        return None, "da_sem not importable: %s" % exc
    if not da_sem._deps():
        return None, ("semantic extras not installed; "
                      "python3 -m pip install fastembed numpy")
    return da_sem, None


def _sem_index(sem, pack, explicit=None):
    return (explicit or os.environ.get("DA_SEARCH_INDEX")
            or sem.default_index_path(pack.path))


def _sem_query(pack, query, k=8, cls="canonical", explicit_index=None, legs=False):
    """Hybrid retrieval, retrieval-signal only. Never raises; always a dict."""
    sem, reason = _sem_state()
    if sem is None:
        return {"status": "unavailable", "detail": reason,
                "fallback": "the lexical tools (search / resolve) are unchanged"}
    idx = _sem_index(sem, pack, explicit_index)
    if not os.path.exists(idx):
        return {"status": "unavailable", "detail": "index not found: %s" % idx,
                "hint": "build it: python3 tools/da_sem.py build --pack %s" % pack.path}
    try:
        out = sem.query_index(idx, query, k=k, cls=cls, legs=legs)
    except ImportError as exc:
        return {"status": "unavailable", "detail": str(exc)}
    out["status"] = "ok"
    return out


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


def cmd_discover(pack, args):
    result = _sem_query(pack, args.query, k=args.k, cls=args.cls,
                        explicit_index=args.index, legs=args.legs)
    if result.get("status") != "ok":
        if args.json:
            return _dump(result)
        print("semantic discovery unavailable: %s" % result.get("detail"), file=sys.stderr)
        if result.get("hint"):
            print(result["hint"], file=sys.stderr)
        return 4
    if args.json:
        return _dump(result)
    print("candidates (retrieval signal only; NOT authority):")
    for c in result["candidates"]:
        cos = "%.3f" % c["cos"] if c.get("cos") is not None else "  -  "
        print("  rrf %.5f  %-22s %-12s %-34s lex#%-3s sem#%-3s cos %s"
              % (c["rrf"], c["id"], c["kind"], (c["title"] or "")[:34],
                 c["lex_rank"] or "-", c["sem_rank"] or "-", cos))
    print("next: inspect each candidate; authority outcomes still come from `da resolve`.")


def cmd_inspect(pack, args):
    entry = pack.by_id.get(args.id)
    if not entry:
        print("unknown id: %s" % args.id, file=sys.stderr)
        return 1
    _dump(entry)


def cmd_resolve(pack, args):
    context = json.loads(args.context) if args.context else {}
    result = resolve(pack, " ".join(args.problem), context)
    # Optional retrieval assist: attaches only on UNDEFINED, and only as a
    # clearly-labelled retrieval signal. It can never change the outcome.
    if getattr(args, "assist", "off") == "semantic" and result.get("outcome") == "UNDEFINED":
        blk = _sem_query(pack, " ".join(args.problem), k=args.assist_k,
                         explicit_index=args.assist_index)
        blk["note"] = ("retrieval signal only; it cannot establish authority; "
                       "inspect candidates before adopting")
        result["retrieval_assist"] = blk
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
    if result.get("retrieval_assist"):
        blk = result["retrieval_assist"]
        print("retrieval assist (semantic; NOT authority):")
        if blk.get("status") != "ok":
            print("  unavailable: %s" % blk.get("detail"))
        else:
            for c in blk["candidates"]:
                cos = "%.3f" % c["cos"] if c.get("cos") is not None else "  -  "
                print("  rrf %.5f  %-22s cos %s  %s" % (c["rrf"], c["id"], cos,
                                                        c["title"] or ""))
            print("  the outcome above stands; inspect candidates before use")


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


def cmd_dispute_add(pack, args):
    ws = args.workspace or os.getcwd()
    context = json.loads(args.context) if args.context else {}
    try:
        record = records.add_dispute(pack, ws, args.query, args.resolved_to,
                                     args.reason, context=context,
                                     suggested_fix=args.suggested_fix)
    except ValueError as exc:
        print("dispute rejected: %s" % exc, file=sys.stderr)
        return 2
    _dump(record)
    return 0


def cmd_disputes(pack, args):
    ws = args.workspace or os.getcwd()
    recs = records.list_disputes(ws)
    data = {"authority": pack.identity(), "count": len(recs), "disputes": recs}
    if args.json:
        return _dump(data)
    print("%s — %d disputed resolution(s)" % (pack.identity()["authority"], len(recs)))
    for d in recs:
        print("  [%s] %s -> %s" % (d.get("status"), d.get("query", "")[:64],
                                   d.get("resolved_to")))
    return 0


def cmd_dispute_replay(pack, args):
    """Re-run the resolver over recorded disputes: standing = still claimed."""
    ws = args.workspace or os.getcwd()
    recs = records.list_disputes(ws, status="open")
    rep = replay_disputes(pack, recs)
    rep["authority"] = pack.identity()
    rep["workspace"] = ws
    if args.json:
        _dump(rep)
    else:
        for r in rep["rows"]:
            print("%-7s %-26s %s" % ("STANDS" if r["still_stands"] else "cleared",
                                     r.get("disputed"), r.get("query", "")[:56]))
        print("standing %d / %d (cleared %d)" % (rep["standing"], rep["total"],
                                                 rep["cleared"]))
    if args.expect_standing is not None and rep["standing"] != args.expect_standing:
        print("dispute-replay: expected %d standing, got %d"
              % (args.expect_standing, rep["standing"]), file=sys.stderr)
        return 5
    return 0


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

    p = sub.add_parser("discover")
    p.add_argument("query"); p.add_argument("--index", default=None)
    p.add_argument("--k", type=int, default=8)
    p.add_argument("--class", dest="cls", default="canonical",
                   choices=["canonical", "history", "all"])
    p.add_argument("--legs", action="store_true", help="include both retrieval legs (debug)")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("inspect"); p.add_argument("id")

    p = sub.add_parser("resolve")
    p.add_argument("problem", nargs="+")
    p.add_argument("--context", default=""); p.add_argument("--json", action="store_true")
    p.add_argument("--assist", default="off", choices=["off", "semantic"],
                   help="optional retrieval assist (attaches candidates on UNDEFINED; never changes outcomes)")
    p.add_argument("--assist-k", type=int, default=5)
    p.add_argument("--assist-index", default=None)

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

    p = sub.add_parser("dispute-add")
    p.add_argument("--query", required=True)
    p.add_argument("--resolved-to", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--context", default="")
    p.add_argument("--suggested-fix", default=None)
    p.add_argument("--workspace", default=None)

    p = sub.add_parser("disputes")
    p.add_argument("--workspace", default=None); p.add_argument("--json", action="store_true")

    p = sub.add_parser("dispute-replay")
    p.add_argument("--workspace", default=None); p.add_argument("--json", action="store_true")
    p.add_argument("--expect-standing", type=int, default=None)

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

    handler = {"overview": cmd_overview, "search": cmd_search, "discover": cmd_discover,
               "inspect": cmd_inspect,
               "resolve": cmd_resolve, "validate": cmd_validate, "golden": cmd_golden,
               "gaps": cmd_gaps, "gap-add": cmd_gap_add, "propose": cmd_propose,
               "review": cmd_review,
               "dispute-add": cmd_dispute_add, "disputes": cmd_disputes,
               "dispute-replay": cmd_dispute_replay,
               "precedents": cmd_precedents,
               "precedent-check": cmd_precedent_check,
               "candidates": cmd_candidates}[args.cmd]
    return handler(pack, args) or 0


if __name__ == "__main__":
    sys.exit(main())
