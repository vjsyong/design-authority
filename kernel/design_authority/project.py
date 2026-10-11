"""Project contracts and decision receipts (docs/13 P1.1, docs/14 section 5).

The consumer half of the runtime: `da init` pins an authority, `da plan`
turns a brief into a version-pinned project contract, `da receipt` formats
the outcome half, and `da reconcile` wraps the sweep over one consumer
workspace. Everything here is stdlib-only and writes only under
`<workspace>/.design-authority/`; the published pack is never touched.

Contract layout (docs/14 section 5):

    .design-authority/
      authority.lock.json   # pinned {authority, version, commit, fingerprint}
      design-plan.json      # intent (written by `da plan`)
      receipt.json          # pointer to the latest outcome receipt
      receipts/             # immutable, append-only outcome receipts
      cases/                # plan-side stubs for unresolved needs
      verification/         # verifier outputs

The plan validates its own citations: every resolved id must exist in the
pinned pack, or the plan refuses. Receipts are declarations until confirmed
(the sweep says so per row); this module validates their references, not
their prose.
"""
import hashlib
import json
import os
import re
import uuid
from datetime import datetime, timezone

PACK_FILES = ("artifacts.json", "rules.json", "prohibitions.json", "fallbacks.json",
              "recipes.json", "golden.json", "scoring.json", "authority.json")
RECEIPT_REQUIRED = ("receipt_version", "application", "revision", "built_at", "authority",
                    "decisions_applied", "unresolved_needs", "provisional_solutions",
                    "deviations", "areas_modified")
INTENTS = {"RESOLVED": "adopt", "COMPOSE": "compose", "FALLBACK": "fallback_marked",
           "UNDEFINED": "improvise_and_report", "CONFLICT": "avoid"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _ws_dir(workspace):
    d = os.path.join(os.path.abspath(workspace), ".design-authority")
    os.makedirs(os.path.join(d, "proposals"), exist_ok=True)
    os.makedirs(os.path.join(d, "cases"), exist_ok=True)
    os.makedirs(os.path.join(d, "verification"), exist_ok=True)
    os.makedirs(os.path.join(d, "receipts"), exist_ok=True)
    return d


def pack_fingerprint(pack_path):
    """Deterministic fingerprint over the pack's record files (sha256, 16c)."""
    h = hashlib.sha256()
    for name in PACK_FILES:
        path = os.path.join(pack_path, name)
        h.update(name.encode())
        if os.path.exists(path):
            with open(path, "rb") as fh:
                h.update(fh.read())
    return "sha256:" + h.hexdigest()[:16]


def write_lock(workspace, pack, pack_path):
    lock = {
        "lock_version": "0.1",
        "authority": pack.manifest.get("id"),
        "version": pack.manifest.get("version"),
        "commit": (pack.manifest.get("snapshot") or {}).get("commit"),
        "fingerprint": pack_fingerprint(pack_path),
        "pack": {"path": os.path.abspath(pack_path)},
        "locked_at": _now(),
    }
    path = os.path.join(_ws_dir(workspace), "authority.lock.json")
    with open(path, "w") as fh:
        json.dump(lock, fh, indent=1)
    return lock


def read_lock(workspace):
    path = os.path.join(os.path.abspath(workspace), ".design-authority", "authority.lock.json")
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        return json.load(fh)


_HEADING = re.compile(r"^#+\s*(.+?)\s*$")
_BULLET = re.compile(r"^\s*[-*]\s+(.+?)\s*$")


def parse_needs(text):
    """The brief convention: bullet items under a `Needs` heading (any level,
    case-insensitive; `Design needs` also accepted). One need per bullet."""
    needs, in_needs = [], False
    for line in text.splitlines():
        m = _HEADING.match(line)
        if m:
            in_needs = m.group(1).strip().lower() in ("needs", "design needs")
            continue
        if in_needs:
            b = _BULLET.match(line)
            if b:
                needs.append(b.group(1))
    return needs


def _resolution_id(resolution):
    if not isinstance(resolution, dict):
        return None
    for key in ("artifact", "recipe", "fallback"):
        if isinstance(resolution.get(key), dict) and resolution[key].get("id"):
            return resolution[key]["id"]
    return None


def build_plan(pack, workspace, brief_path, pack_path=None):
    """Resolve every brief need against the pinned pack; write the contract.

    Refuses on any citation that does not exist in the pack (plan validation,
    docs/13 P1.1). Unresolved needs become plan-side cases (stubs); they are
    expected to be improvised, marked, and reported during the build.
    """
    from .resolve import resolve

    with open(brief_path) as fh:
        brief_text = fh.read()
    needs = parse_needs(brief_text)
    if not needs:
        raise ValueError("no needs found: put one bullet per need under a '## Needs' heading")
    ws_dir = _ws_dir(workspace)
    lock = write_lock(workspace, pack, pack_path or ".")

    entries, cases = [], []
    for i, need in enumerate(needs, 1):
        result = resolve(pack, need)
        rid = _resolution_id(result.get("resolution"))
        if rid and rid not in pack.by_id:
            raise ValueError("plan refused: resolved id %r does not exist in the pack" % rid)
        intent = INTENTS.get(result["outcome"], "review")
        entry = {"need": need, "outcome": result["outcome"], "id": rid, "intent": intent,
                 "evidence": result.get("evidence")}
        if result.get("next"):
            entry["next"] = result["next"]
        if result["outcome"] in ("UNDEFINED", "CONFLICT"):
            slug = re.sub(r"[^a-z0-9]+", "-", need.lower()).strip("-")[:48]
            case_id = "%02d-%s" % (i, slug)
            case = {"case_version": "0.1", "id": case_id, "need": need,
                    "outcome": result["outcome"], "status": "open",
                    "raised_in": os.path.relpath(brief_path, workspace), "created": _now()}
            with open(os.path.join(ws_dir, "cases", case_id + ".json"), "w") as fh:
                json.dump(case, fh, indent=1)
            entry["case"] = case_id
            cases.append(case_id)
        entries.append(entry)

    plan = {"plan_version": "0.1", "brief": os.path.relpath(brief_path, workspace),
            "authority": {k: lock[k] for k in ("authority", "version", "commit", "fingerprint")},
            "created": _now(), "needs": entries, "cases": cases}
    with open(os.path.join(ws_dir, "design-plan.json"), "w") as fh:
        json.dump(plan, fh, indent=1)
    return plan


def receipt_new(pack, workspace, revision, application=None, pack_path=None):
    """Scaffold the outcome receipt (docs/14 section 5, format 0.2). The
    implementing agent fills the claims at completion; the verifier confirms
    them; the sweep trusts only confirmed variants."""
    ws_dir = _ws_dir(workspace)
    lock = read_lock(workspace) or write_lock(workspace, pack, pack_path or ".")
    receipt = {
        "receipt_version": "0.2",
        "note": ("Written by the implementing agent at completion; confirmed against evidence "
                 "by the verifier (docs/14 section 5). Claims: decisions_applied, "
                 "unresolved_needs, provisional_solutions, deviations, areas_modified, "
                 "verification."),
        "application": application or os.path.basename(os.path.abspath(workspace)),
        "revision": revision,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "authority": {k: lock.get(k) for k in ("authority", "version", "commit", "fingerprint")},
        "decisions_applied": [],
        "unresolved_needs": [],
        "provisional_solutions": [],
        "deviations": [],
        "areas_modified": [],
        "verification": {},
    }
    slug = re.sub(r"[^a-z0-9]+", "-", revision.lower()).strip("-")
    name = "%s-%s.json" % (receipt["built_at"], slug)
    with open(os.path.join(ws_dir, "receipts", name), "w") as fh:
        json.dump(receipt, fh, indent=1)
    pointer = os.path.join(ws_dir, "receipt.json")
    existing = []
    if os.path.exists(pointer):
        with open(pointer) as fh:
            existing = json.load(fh).get("receipts", [])
    ref = "receipts/" + name
    if ref not in existing:
        existing.append(ref)
    with open(pointer, "w") as fh:
        json.dump({"latest": ref, "receipts": existing}, fh, indent=1)
    return {"receipt": receipt, "path": os.path.join(ws_dir, "receipts", name), "pointer": ref}


def receipt_check(pack, workspace, receipt_path):
    """Validate a receipt: shape, pack-referenced ids, case references."""
    with open(receipt_path) as fh:
        rec = json.load(fh)
    problems = []
    for key in RECEIPT_REQUIRED:
        if key not in rec:
            problems.append("missing field %r" % key)
    for key in ("decisions_applied", "unresolved_needs", "provisional_solutions",
                "deviations", "areas_modified"):
        if key in rec and not isinstance(rec[key], list):
            problems.append("%r must be a list" % key)
    for rid in rec.get("decisions_applied") or []:
        if rid not in pack.by_id:
            problems.append("decisions_applied id %r does not exist in the pack" % rid)
    for rid in rec.get("migration_for") or []:
        if rid not in pack.by_id:
            problems.append("migration_for id %r does not exist in the pack" % rid)
    for d in rec.get("deviations") or []:
        did = d.get("decision") if isinstance(d, dict) else d
        if isinstance(did, str) and did not in pack.by_id:
            problems.append("deviation decision %r does not exist in the pack" % did)
    known_cases = set()
    ws_dir = os.path.join(os.path.abspath(workspace), ".design-authority")
    cdir = os.path.join(ws_dir, "cases")
    if os.path.isdir(cdir):
        known_cases = {f[:-5] for f in os.listdir(cdir) if f.endswith(".json")}
    for c in rec.get("unresolved_needs") or []:
        if isinstance(c, str) and c and c not in known_cases and not c.startswith("gap/"):
            problems.append("unresolved need %r is neither a plan case nor a recorded gap" % c)
    return problems


def build_portfolio(workspace, pack, target_version):
    """A single-application portfolio for the sweep, from the workspace's own
    contract. Absolute paths throughout (the sweep joins relative dirs onto
    the meta repo; absolute ones pass through)."""
    ws = os.path.abspath(workspace)
    lock = read_lock(ws) or {}
    pointer = os.path.join(ws, ".design-authority", "receipt.json")
    receipt_rel = None
    if os.path.exists(pointer):
        with open(pointer) as fh:
            receipt_rel = json.load(fh).get("latest")
    build = {"dir": ws, "revision": "latest", "built_under": lock.get("version") or "0.0.0"}
    if receipt_rel:
        build["receipt"] = os.path.join(".design-authority", receipt_rel)
    app_name = os.path.basename(ws)
    return {"portfolio": "consumer workspace (%s)" % app_name,
            "target_version": target_version,
            "apps": [{"name": app_name, "authority": pack.manifest.get("id"),
                      "lineage": app_name, "builds": [build]}]}


def migration_plan(report, ws_path=None):
    """Transform a sweep report into the consumer-facing migration plan.
    Receipt refs are normalized to workspace-relative paths so the plan is
    portable (it is committed evidence, not machine state)."""
    def _rel(s):
        if ws_path and isinstance(s, str) and s.startswith(os.path.abspath(ws_path) + os.sep):
            return os.path.relpath(s, os.path.abspath(ws_path))
        return s

    def _rel_state(state):
        if isinstance(state, dict) and isinstance(state.get("evidence"), list):
            state = dict(state)
            state["evidence"] = [_rel(x) for x in state["evidence"]]
        return state

    actions = []
    for f in report.get("findings", []):
        ob = f.get("obligation") or {}
        if f.get("class") == "rectify":
            actions.append({"decision": f.get("decision"), "revision": f.get("revision"),
                            "action": "migrate", "by": ob.get("by"), "state": ob.get("state"),
                            "reason": f.get("reason")})
        elif f.get("class") == "review":
            actions.append({"decision": f.get("decision"), "revision": f.get("revision"),
                            "action": "assess", "reason": f.get("reason")})
    return {"plan_version": "0.1", "target_version": report.get("target_version"),
            "counts": report.get("counts"), "obligations": report.get("obligations"),
            "findings": [{"decision": f.get("decision"), "revision": f.get("revision"),
                          "class": f.get("class"), "reason": f.get("reason"),
                          "obligation": f.get("obligation"), "receipt_status": f.get("receipt_status"),
                          "trigger_state": _rel_state(f.get("trigger_state"))}
                         for f in report.get("findings", [])],
            "actions": actions}
