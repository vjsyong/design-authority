"""Gap, proposal and dispute records. Noncanonical by construction: they live
in the consuming workspace under .design-authority/ and never touch the
published pack.
"""
import json
import os
import uuid
from datetime import datetime, timezone

PROPOSAL_REQUIRED = ("problem", "insufficiency", "reuse_case", "composition_check",
                     "proposed", "tests")


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _rid(prefix):
    return "%s/%s-%s" % (prefix, datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
                         uuid.uuid4().hex[:6])


def _ws(workspace):
    d = os.path.join(os.path.abspath(workspace), ".design-authority")
    os.makedirs(os.path.join(d, "proposals"), exist_ok=True)
    return d


def add_gap(pack, workspace, need, context=None, attempted_resolution=None,
            why_insufficient=None, fallback_used=None, evidence=None,
            scope_hint="unknown"):
    gap = {
        "id": _rid("gap"), "need": need, "context": dict(context or {}),
        "authority": pack.identity(),
        "searched": (attempted_resolution or {}).get("searched"),
        "closest": (attempted_resolution or {}).get("closest"),
        "why_insufficient": why_insufficient or (attempted_resolution or {}).get("why"),
        "fallback_used": fallback_used,
        "evidence": list(evidence or []),
        "scope_hint": scope_hint,
        "status": "open",
        "created": _now(),
    }
    matches = pack.precedent_matches(need, limit=2)
    if matches:
        gap["precedent_warnings"] = [
            {"id": m["record"].get("id"), "verdict": m["verdict"],
             "title": m["record"].get("title"), "grounds": m["record"].get("grounds"),
             "reason": m["record"].get("reason"), "try": m["record"].get("try"),
             "citation": m["record"].get("citation")}
            for m in matches]
    cands = pack.candidate_matches(need, limit=2)
    if cands:
        gap["candidate_hints"] = [
            {"id": c.get("id"), "title": c.get("title"), "summary": c.get("summary"),
             "promote_when": c.get("promote_when")} for c in cands]
    path = os.path.join(_ws(workspace), "gaps.jsonl")
    with open(path, "a") as fh:
        fh.write(json.dumps(gap) + "\n")
    gap["stored_at"] = path
    return gap


def list_gaps(workspace):
    path = os.path.join(_ws(workspace), "gaps.jsonl")
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def get_gap(workspace, gap_id):
    for g in list_gaps(workspace):
        if g["id"] == gap_id:
            return g
    return None


def add_proposal(pack, workspace, gap_id, proposal):
    missing = [k for k in PROPOSAL_REQUIRED if not proposal.get(k)]
    if missing:
        raise ValueError("proposal missing required fields: %s" % ", ".join(missing))
    gap = get_gap(workspace, gap_id)
    if gap is None:
        raise ValueError("unknown gap %s (list gaps first)" % gap_id)
    unknown = [t for t in proposal.get("depends_on", []) if t not in pack.by_id]
    if unknown:
        raise ValueError("depends_on cites unknown ids: %s" % ", ".join(unknown))

    pid = _rid("prop")
    record = {
        "id": pid, "gap_id": gap_id,
        "problem": proposal["problem"],
        "insufficiency": proposal["insufficiency"],
        "reuse_case": proposal["reuse_case"],
        "composition_check": proposal["composition_check"],
        "proposed": proposal["proposed"],
        "depends_on": proposal.get("depends_on", []),
        "new_primitives": proposal.get("new_primitives", []),
        "tests": proposal["tests"],
        "status": "candidate",
        "review": {"verdict": None, "notes": None},
        "authority": pack.identity(),
        "created": _now(),
    }
    proposed = proposal.get("proposed")
    if isinstance(proposed, dict) and "add" in proposed:
        titles = [e.get("title", "") for e in proposed["add"] if isinstance(e, dict)]
    elif isinstance(proposed, dict):
        titles = [proposed.get("title", "")]
    else:
        titles = []
    matches = pack.precedent_matches(" ".join([proposal["problem"]] + titles), limit=2)
    if matches:
        record["precedent_warnings"] = [
            {"id": m["record"].get("id"), "verdict": m["verdict"],
             "title": m["record"].get("title"), "grounds": m["record"].get("grounds"),
             "reason": m["record"].get("reason"), "try": m["record"].get("try"),
             "citation": m["record"].get("citation")}
            for m in matches]
    cands = pack.candidate_matches(" ".join([proposal["problem"]] + titles), limit=2)
    if cands:
        record["candidate_hints"] = [
            {"id": c.get("id"), "title": c.get("title"), "summary": c.get("summary"),
             "promote_when": c.get("promote_when")} for c in cands]
    safe = pid.replace("/", "_")
    path = os.path.join(_ws(workspace), "proposals", safe + ".json")
    with open(path, "w") as fh:
        json.dump(record, fh, indent=1)
    record["stored_at"] = path
    record["review_checklist"] = [
        "Necessity: can the existing authority express this? (adversarial review assumes it can)",
        "Reuse: is this genuinely reusable beyond this project?",
        "Composition: why can existing artifacts not compose to satisfy it?",
        "Dependencies: do cited authority ids/decisions hold?",
        "New primitives: are they unavoidable?",
        "Compliance tests: at least one deterministic check proposed?",
        "Deterministic checks pass (shape, citations, tests present)",
    ]
    if record.get("precedent_warnings"):
        record["review_checklist"].append(
            "Prior declines exist for this area — justify against the recorded "
            "precedent(s): " + ", ".join("%s [%s]" % (w["id"], w["verdict"])
                                         for w in record["precedent_warnings"]))
    if record.get("candidate_hints"):
        record["review_checklist"].append(
            "A provisional candidate exists — consider aligning or noting it: "
            + ", ".join(c["id"] for c in record["candidate_hints"]))
    return record


def list_proposals(workspace):
    d = os.path.join(_ws(workspace), "proposals")
    out = []
    for name in sorted(os.listdir(d)):
        if name.endswith(".json"):
            with open(os.path.join(d, name)) as fh:
                out.append(json.load(fh))
    return out


VERDICT_STATUS = {"accept": "accepted", "reject": "rejected",
                  "needs-info": "needs-info", "needs_info": "needs-info"}


def set_proposal_review(workspace, proposal_id, verdict, notes=None,
                        evidence=None):
    """Record a review verdict on a candidate proposal (D-016: explicit
    accept/reject/needs-info, nothing auto-applied)."""
    v = verdict.strip().lower()
    if v not in VERDICT_STATUS:
        raise ValueError("verdict must be accept|reject|needs-info, got %r" % verdict)
    safe = proposal_id.replace("/", "_")
    path = os.path.join(_ws(workspace), "proposals", safe + ".json")
    if not os.path.exists(path):
        raise ValueError("unknown proposal %s" % proposal_id)
    with open(path) as fh:
        record = json.load(fh)
    record["review"] = {"verdict": v, "notes": notes, "evidence": evidence,
                        "reviewed_at": _now()}
    record["status"] = VERDICT_STATUS[v]
    with open(path, "w") as fh:
        json.dump(record, fh, indent=1)
    record["stored_at"] = path
    return record


# -- disputed resolutions (0.5) ------------------------------------------------

def add_dispute(pack, workspace, query, resolved_to, reason, context=None,
                suggested_fix=None, evidence=None):
    """Record that a RESOLVED outcome did not govern the requesting need.

    Distinct from a gap: a gap means the authority had no answer; a dispute
    means it gave a wrong one. Disputes are consumer-side and noncanonical,
    they never change resolution behavior, and they are replayable as
    regression fixtures.
    """
    if not query or not reason:
        raise ValueError("dispute requires query and reason")
    if not resolved_to:
        raise ValueError("dispute requires resolved_to (the id the resolver claimed)")
    if resolved_to not in pack.by_id:
        raise ValueError("resolved_to cites unknown id: %s" % resolved_to)
    record = {
        "id": _rid("dispute"),
        "kind": "disputed-resolution",
        "query": query,
        "resolved_to": resolved_to,
        "reason": reason,
        "suggested_fix": suggested_fix,
        "context": dict(context or {}),
        "evidence": list(evidence or []),
        "authority": pack.identity(),
        "status": "open",
        "created": _now(),
    }
    path = os.path.join(_ws(workspace), "disputes.jsonl")
    with open(path, "a") as fh:
        fh.write(json.dumps(record) + "\n")
    record["stored_at"] = path
    return record


def list_disputes(workspace, status=None):
    path = os.path.join(_ws(workspace), "disputes.jsonl")
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        records = [json.loads(line) for line in fh if line.strip()]
    if status:
        records = [r for r in records if r.get("status") == status]
    return records


DISPUTE_STATUS = ("open", "accepted", "rejected")


def set_dispute_status(workspace, dispute_id, status, note=None):
    """Reviewer-side ruling on a dispute: accepted (the record does not
    govern), rejected (the resolution holds), or back to open."""
    if status not in DISPUTE_STATUS:
        raise ValueError("status must be open|accepted|rejected, got %r" % status)
    records = list_disputes(workspace)
    found = None
    for r in records:
        if r["id"] == dispute_id:
            r["status"] = status
            r["status_note"] = note
            r["status_at"] = _now()
            found = r
    if found is None:
        raise ValueError("unknown dispute %s" % dispute_id)
    path = os.path.join(_ws(workspace), "disputes.jsonl")
    with open(path, "w") as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")
    return found
