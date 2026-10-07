"""Resolution pipeline.

CONFLICT -> RESOLVED -> COMPOSE -> FALLBACK -> UNDEFINED.
Deterministic by default: every citation is a pack ID, validated before return.
"""
import re

from .pack import norm_tokens

DIRECT_MIN = 6.5      # a direct artifact hit must reach this score
DIRECT_MARGIN = 2.0   # and lead the runner-up by this much
COMPOSE_MIN = 5.0

COLOR_LITERAL_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(")


def _brief(entry):
    return {"id": entry.get("id"), "kind": entry.get("kind"),
            "title": entry.get("title"), "summary": entry.get("summary")}


def _artifact_view(art):
    view = dict(_brief(art))
    view["status"] = art.get("status")
    body = art.get("body", {}) or {}
    for key in ("class", "states", "a11y"):
        if key in body:
            view[key] = body[key]
    view["aliases"] = art.get("aliases", [])
    src = art.get("source", {})
    view["source"] = {k: src.get(k) for k in ("repo", "commit", "path") if src.get(k)}
    return view


def _alts(hits, skip=None, n=3):
    return [{"id": h["id"], "kind": h["kind"], "title": h["title"],
             "score": h["score"]} for h in hits if h["id"] != skip][:n]


def _prohibition_hit(pack, problem):
    low = problem.lower()
    for p in pack.prohibitions:
        if p.get("detect") == "color_literal":
            m = COLOR_LITERAL_RE.search(problem)
            if m:
                return p, "colour literal '%s'" % m.group(0)
        for sig in p.get("signals", []):
            if sig in low:
                return p, "signal '%s'" % sig
        for group in p.get("signals_all", []):
            if all(s in low for s in group):
                return p, "signals " + "+".join("'%s'" % s for s in group)
    return None


def _emit_resolved(out, pack, hit, art_hits):
    out["outcome"] = "RESOLVED"
    out["resolution"] = {"artifact": _artifact_view(pack.by_id[hit["id"]])}
    out["evidence"] = {"score": hit["score"], "matched": hit["matched"],
                       "threshold": DIRECT_MIN}
    out["alternatives"] = _alts(art_hits, skip=hit["id"])
    out["next"] = ("Call inspect_artifact('%s') for full detail; "
                   "validate_implementation(target) after building." % hit["id"])
    return out


def _emit_compose(out, pack, hit, art_hits):
    rec = pack.by_id[hit["id"]]
    ingredients = [_brief(pack.by_id[i]) for i in rec.get("ingredients", [])
                   if i in pack.by_id]
    out["outcome"] = "COMPOSE"
    out["resolution"] = {
        "recipe": {"id": rec["id"], "title": rec["title"], "summary": rec["summary"],
                   "constraints": rec.get("constraints", []),
                   "evidence": rec.get("evidence")},
        "ingredients": ingredients,
    }
    out["evidence"] = {"score": hit["score"], "matched": hit["matched"],
                       "threshold": COMPOSE_MIN}
    out["alternatives"] = _alts(art_hits, None)
    out["next"] = ("Compose strictly per the recipe constraints; inspect the "
                   "ingredient artifacts before building.")
    return out


def resolve(pack, problem, context=None):
    context = dict(context or {})
    out = {"outcome": None, "problem": problem, "context": context,
           "resolution": None, "alternatives": [], "evidence": {},
           "authority": pack.identity()}

    # 1. CONFLICT — explicit prohibitions first.
    hit = _prohibition_hit(pack, problem)
    if hit:
        prohib, how = hit
        rule = pack.rule(prohib["rule"]) if prohib.get("rule") else None
        out["outcome"] = "CONFLICT"
        out["resolution"] = {
            "prohibition": {"id": prohib["id"], "statement": prohib["statement"]},
            "rule": ({"id": rule["id"], "severity": rule["severity"],
                      "summary": rule["summary"], "fix": rule["fix"]} if rule else None),
            "detected": how,
        }
        out["policy"] = pack.manifest.get("policy", {}).get("on_conflict")
        return out

    # 2/3. RESOLVED vs COMPOSE — spec order: a dedicated artifact wins; a
    # sanctioned recipe is the answer only when no artifact directly defines it.
    hits = pack.search(problem, limit=8)
    art_hits = [h for h in hits if h["kind"] not in ("recipe", "fallback", "prohibition")]
    rh = pack.search(problem, kinds=["recipe"], limit=3)
    a_best = art_hits[0] if art_hits else None
    r_best = rh[0] if rh and rh[0]["score"] >= COMPOSE_MIN else None
    runner = art_hits[1] if len(art_hits) > 1 else None

    if a_best and a_best["score"] >= DIRECT_MIN and (
            not runner or a_best["score"] - runner["score"] >= DIRECT_MARGIN):
        return _emit_resolved(out, pack, a_best, art_hits)

    if r_best:
        return _emit_compose(out, pack, r_best, art_hits)

    # 4. FALLBACK — a scoped sanctioned fallback (non-catch-all scope).
    qset = set(norm_tokens(problem))
    for fb in pack.fallbacks:
        scope = [s for s in fb.get("scope", []) if s != "*"]
        overlap = qset & set(scope)
        if scope and overlap:
            out["outcome"] = "FALLBACK"
            out["resolution"] = {"fallback": {
                "id": fb["id"], "title": fb["title"], "statement": fb["statement"],
                "constraints": fb.get("constraints", [])}}
            out["evidence"] = {"matched_scope": sorted(overlap)}
            out["next"] = ("Use the fallback; mark the improvisation; "
                           "report_gap if the need is likely to recur.")
            return out

    # 5. UNDEFINED — a legitimate, structured outcome (not an error).
    out["outcome"] = "UNDEFINED"
    out["closest"] = art_hits[:3]
    out["search_trace"] = {"queries": [problem], "hits_considered": len(hits),
                           "top_score": a_best["score"] if a_best else 0.0,
                           "threshold": DIRECT_MIN}
    out["why"] = ("No artifact met the direct-match threshold%s; no recipe matched; "
                  "no scoped fallback applies."
                  % ("" if not a_best else
                     " (top candidate %s scored %.2f vs %.2f needed)"
                     % (a_best["id"], a_best["score"], DIRECT_MIN)))
    out["fallback_policy"] = {
        "allowed": [{"id": f["id"], "title": f["title"]} for f in pack.fallbacks],
        "note": pack.manifest.get("policy", {}).get("on_undefined"),
    }
    out["next"] = ("Implement per the consuming project's fallback policy; mark the "
                   "improvisation; then report_gap(need, context, attempted_resolution).")
    return out


def resolve_golden(pack, cases):
    """Run a golden set: [{problem, expect, expect_id?, note}] -> agreement report."""
    rows = []
    for case in cases:
        r = resolve(pack, case["problem"], case.get("context"))
        res = r.get("resolution") or {}
        rid = None
        for key in ("artifact", "recipe", "fallback", "prohibition"):
            if isinstance(res.get(key), dict) and res[key].get("id"):
                rid = res[key]["id"]
                break
        ok = r["outcome"] == case["expect"]
        if ok and case.get("expect_id"):
            ok = rid == case["expect_id"]
        rows.append({"problem": case["problem"], "expected": case["expect"],
                     "expected_id": case.get("expect_id"),
                     "got": r["outcome"], "ok": ok, "resolution_id": rid,
                     "note": case.get("note")})
    passed = sum(1 for row in rows if row["ok"])
    return {"total": len(rows), "passed": passed,
            "rate": round(passed / len(rows), 3) if rows else 0.0, "rows": rows}
