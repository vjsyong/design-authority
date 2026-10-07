"""Design Authority — MCP server (stdio).

Exposes the kernel as tools + read-only resources. Conventions (proposal §4,
D-013/D-014): every response echoes {authority, version, snapshot}; errors carry
a recovery hint; each call is appended to the workspace decision log
(<workspace>/.design-authority/decision-log.jsonl).

Run via tools/da-mcp.py with the project venv (mcp<2, FastMCP).
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Optional

from mcp.server.fastmcp import FastMCP

from . import records
from .pack import Pack, PackError
from .resolve import resolve
from .validate import validate

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DEFAULT_PACK = os.path.join(ROOT, "packs", "triage")

mcp = FastMCP("design-authority")

_pack: Optional[Pack] = None


def get_pack() -> Pack:
    global _pack
    if _pack is None:
        _pack = Pack(os.environ.get("DA_PACK") or DEFAULT_PACK)
    return _pack


def workspace() -> str:
    return os.environ.get("DA_WORKSPACE") or os.getcwd()


def _log(tool: str, params: dict, summary: dict, t0: float) -> None:
    """Decision log (D-014). Never load-bearing; failures are swallowed."""
    try:
        d = os.path.join(workspace(), ".design-authority")
        os.makedirs(d, exist_ok=True)
        rec = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "tool": tool, "params": {k: (v if isinstance(v, (str, int, float, type(None))) else "...") for k, v in params.items()},
               "latency_ms": round((time.time() - t0) * 1000),
               "summary": summary}
        with open(os.path.join(d, "decision-log.jsonl"), "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    except Exception:
        pass


def _err(msg: str, hint: str) -> dict:
    return {"status": "error", "message": msg, "hint": hint,
            "authority": get_pack().identity()}


@mcp.tool()
def authority_overview() -> dict:
    """Overview of this design authority: identity, counts, capabilities,
    policy, and the resolution semantics. Call this first."""
    t0 = time.time()
    pack = get_pack()
    counts = {}
    for a in pack.artifacts:
        counts[a["kind"]] = counts.get(a["kind"], 0) + 1
    data = {
        "status": "ok",
        "authority": pack.identity(),
        "description": pack.manifest.get("description"),
        "counts": {"artifacts": counts, "rules": len(pack.rules),
                   "recipes": len(pack.recipes), "fallbacks": len(pack.fallbacks),
                   "prohibitions": len(pack.prohibitions)},
        "capabilities": pack.manifest.get("capabilities"),
        "policy": pack.manifest.get("policy"),
        "how_to_use": [
            "search_authority(query) to find artifacts; inspect_artifact(id) for detail.",
            "resolve_design_problem(problem) returns one of CONFLICT / RESOLVED / COMPOSE / FALLBACK / UNDEFINED with citations; matching negative precedents are attached when present.",
            "list_precedents() surfaces declined requests with reasons and alternatives — consult it before coining something new.",
            "validate_implementation(target) runs the authority's validators over a path.",
            "UNDEFINED is a useful answer: implement per the fallback policy, mark the improvisation, then report_gap(...).",
            "Never present improvisation as canonical; never modify the authority.",
        ],
    }
    _log("authority_overview", {}, {"counts": data["counts"]}, t0)
    return data


@mcp.tool()
def search_authority(query: str, kinds: str = "", limit: int = 12) -> dict:
    """Search the authority catalogue (artifacts: components, patterns,
    guidelines, token-sets, examples, references) and recipes.
    kinds: optional comma-separated filter (component,pattern,guideline,
    token-set,example,reference,recipe)."""
    t0 = time.time()
    pack = get_pack()
    kind_list = [k.strip() for k in kinds.split(",") if k.strip()] or None
    hits = pack.search(query, kinds=kind_list, limit=max(1, min(limit, 50)))
    out = {"status": "ok", "authority": pack.identity(), "query": query,
           "hits": hits}
    if not hits:
        out["hint"] = ("No matches. Try broader wording, or resolve_design_problem "
                       "for an outcome-typed answer; a no-match may legitimately be UNDEFINED.")
    _log("search_authority", {"query": query, "kinds": kinds},
         {"hits": len(hits), "top": hits[0]["id"] if hits else None}, t0)
    return out


@mcp.tool()
def inspect_artifact(id: str) -> dict:
    """Full detail for one artifact by id (e.g. 'component/badge',
    'recipe/status-with-text', 'guideline/armed-delete')."""
    t0 = time.time()
    pack = get_pack()
    entry = pack.by_id.get(id)
    if entry is None:
        return _err("unknown id %r" % id,
                    "Use search_authority(query) or authority_overview() to find ids.")
    _log("inspect_artifact", {"id": id}, {"kind": entry.get("kind")}, t0)
    return {"status": "ok", "authority": pack.identity(), "artifact": entry}


@mcp.tool()
def resolve_design_problem(problem: str, context: Optional[dict] = None) -> dict:
    """Resolve a design problem against the authority. Returns an outcome:
    CONFLICT (contradicts an explicit constraint), RESOLVED (an artifact
    defines it), COMPOSE (a sanctioned recipe composes it), FALLBACK (a
    sanctioned generic fallback applies) or UNDEFINED (no adequate answer —
    legitimate; follow the fallback policy and report a gap). Every citation
    is validated against the pack."""
    t0 = time.time()
    pack = get_pack()
    result = resolve(pack, problem, context or {})
    result["status"] = "ok"
    _log("resolve_design_problem", {"problem": problem},
         {"outcome": result["outcome"],
          "resolution": (result.get("resolution") or {}).get("artifact", {}).get("id")
          or (result.get("resolution") or {}).get("recipe", {}).get("id")
          or (result.get("resolution") or {}).get("fallback", {}).get("id")
          or (result.get("resolution") or {}).get("prohibition", {}).get("id")},
         t0)
    return result


@mcp.tool()
def list_precedents(query: str = "") -> dict:
    """List the authority's negative precedents: requests previously declined,
    each with the reason and the routes to try instead. Optional `query`
    filters by keyword overlap. Consult before coining something new — a
    decline is guidance, not a dead end."""
    t0 = time.time()
    pack = get_pack()
    if query:
        recs = pack.precedent_matches(query, limit=25)
    else:
        recs = pack.precedents
    _log("list_precedents", {"query": query}, {"count": len(recs)}, t0)
    return {"status": "ok", "authority": pack.identity(),
            "count": len(recs), "precedents": recs}


@mcp.tool()
def validate_implementation(target: str, validators: str = "") -> dict:
    """Run the authority's declared validators over a path (directory or file).
    Returns normalized findings (rule, severity, message, location{path,line},
    fix) plus a summary with counts and the spec score."""
    t0 = time.time()
    pack = get_pack()
    names = [v.strip() for v in validators.split(",") if v.strip()] or None
    result = validate(pack, target, names=names)
    result["status"] = "ok"
    _log("validate_implementation", {"target": target},
         {"findings": result["summary"]["total"],
          "counts": result["summary"]["counts"]}, t0)
    return result


@mcp.tool()
def report_gap(need: str, context: Optional[dict] = None,
               attempted_resolution: Optional[dict] = None,
               fallback_used: str = "", evidence: Optional[list] = None,
               scope_hint: str = "unknown") -> dict:
    """Record a design-system gap in the consuming workspace (noncanonical).
    Call after resolve_design_problem returns UNDEFINED (or a fallback was
    used). Returns the gap record id and the next-step guidance."""
    t0 = time.time()
    pack = get_pack()
    gap = records.add_gap(pack, workspace(), need, context=context,
                          attempted_resolution=attempted_resolution,
                          fallback_used=fallback_used or None,
                          evidence=evidence, scope_hint=scope_hint)
    _log("report_gap", {"need": need}, {"gap": gap["id"]}, t0)
    return {"status": "ok", "authority": pack.identity(), "gap": gap,
            "next": ("Optionally call propose_extension(gap_id, proposal) with a "
                     "structured candidate: problem, insufficiency, reuse_case, "
                     "composition_check, proposed[], depends_on[], tests[]. "
                     "Proposals are noncanonical and reviewed upstream.")}


@mcp.tool()
def propose_extension(gap_id: str, proposal: dict) -> dict:
    """Submit a noncanonical extension candidate for a recorded gap. The
    proposal must answer: problem, insufficiency, reuse_case,
    composition_check, proposed[], tests[]; optional depends_on[] (must cite
    existing authority ids). Returns the candidate record + review checklist."""
    t0 = time.time()
    pack = get_pack()
    try:
        record = records.add_proposal(pack, workspace(), gap_id, proposal)
    except ValueError as exc:
        return _err(str(exc),
                    "Fix the proposal fields or cite only existing ids "
                    "(depends_on targets must exist in the pack).")
    _log("propose_extension", {"gap_id": gap_id}, {"proposal": record["id"]}, t0)
    return {"status": "ok", "authority": pack.identity(), "proposal": record}


# -- read-only resources ------------------------------------------------------

@mcp.resource("authority://overview")
def res_overview() -> str:
    """The authority manifest and how to use it."""
    return json.dumps(authority_overview(), indent=1)


@mcp.resource("authority://rules")
def res_rules() -> str:
    """The full rule catalogue."""
    return json.dumps({"authority": get_pack().identity(),
                       "rules": get_pack().rules}, indent=1)


@mcp.resource("authority://artifact/{artifact_id}")
def res_artifact(artifact_id: str) -> str:
    """One artifact by id."""
    entry = get_pack().by_id.get(artifact_id)
    if entry is None:
        return json.dumps(_err("unknown id %r" % artifact_id,
                               "Use search_authority(query) to find ids."))
    return json.dumps(entry, indent=1)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
