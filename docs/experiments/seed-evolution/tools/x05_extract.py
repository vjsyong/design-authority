#!/usr/bin/env python3
"""x05 extraction pass — deterministic evidence from a sealed checkpoint.

Runs after capture, for every session. Records (into run/<id>/extraction/):
  inventory.json — element inventory (testid-indexed, desktop probes) + meta
  diff.json      — element diff versus the previous checkpoint + code diff
  roles.json     — role-tagged instances (six frozen roles) with measured
                   values and raw behavioral observations
  evidence.md    — human-readable digest (census review + blind prep)

The extraction is what freezes applicable conventions for the next session:
judgment classification that remains happens downstream (census) against this
frozen evidence, timestamped, never re-chosen after results exist.

Usage: x05_extract.py --id SID [--root X05_ROOT] [--schedule PATH]
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from x05_common import (X05_ROOT, hash_tree, now_iso, read_json,  # noqa: E402
                        write_json_atomic)

SEAL_EXCLUDES = ["reference", "opencode.json", "run-authority"]

ROLE_HOOKS = {
    "primary-action": ["btn-add-bookmark", "submit-add", "submit-edit",
                       "import-submit", "bulk-apply"],
    "destructive": ["bookmark-delete", "bulk-delete", "confirm", "confirm-accept",
                    "confirm-cancel"],
    "empty-state": ["empty-state", "filter-empty"],
    "form-validation": ["form-add", "input-title", "input-url", "form-error",
                        "submit-add", "form-edit"],
    "tags-status": ["tag-filter", "tag-chip", "tag-edit"],
    "surfaces": ["bookmark-card", "bulk-bar", "edit-panel", "import-wizard",
                 "mapping-table", "command-palette", "analytics-view"],
}

STYLE_KEYS = ["color", "bg", "borderTop", "radius", "font", "padding", "display",
              "shadow", "textTransform"]


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_prev_extraction(root, sid, schedule):
    """Previous checkpoint's extraction dir for this session's chain."""
    prev = None
    for s in schedule.get("sessions", []):
        if s["id"] == sid:
            prev = s.get("prev")
            break
    if not prev:
        return None, None
    d = os.path.join(root, "run", prev, "extraction")
    return prev, d


def build_inventory(sid, run_dir):
    cap = read_json(os.path.join(run_dir, "capture", "capture.json"), {}) or {}
    probes = read_json(os.path.join(run_dir, "capture", "probes.json"), {}) or {}
    inv = {
        "id": sid, "extracted": now(),
        "capture_ok": bool(cap and not cap.get("error")),
        "capture_error": cap.get("error") if cap else "capture.json missing",
        "fixture": cap.get("fixture"),
        "states": {},
    }
    for state, entry in (cap.get("states") or {}).items():
        st = {"available": False, "viewports": {}}
        for vp, v in (entry.get("viewports") or {}).items():
            st["viewports"][vp] = {"ok": v.get("ok"), "shot": v.get("shot"),
                                   "console_errors": v.get("console_errors", [])[:10]}
            if vp == "desktop" and v.get("ok"):
                st["available"] = True
        if state in probes:
            p = probes[state]
            st["counts"] = p.get("counts")
            st["testids"] = {tid: [normalize_el(e) for e in els]
                             for tid, els in (p.get("testids") or {}).items()}
            st["focus"] = p.get("focus")
            if "invalid_timing" in p:
                st["invalid_timing"] = p["invalid_timing"]
        inv["states"][state] = st
    return inv


def normalize_el(e):
    return {
        "tag": e.get("tag"), "classes": " ".join(sorted((e.get("classes") or "").split())),
        "role": e.get("role"), "aria": e.get("aria"), "text": e.get("text"),
        "rect": e.get("rect"),
        "styles": {k: (e.get("styles") or {}).get(k) for k in STYLE_KEYS},
    }


def signature(instances):
    """Stable signature for set-diffing a testid across checkpoints."""
    sig = []
    for e in instances:
        sig.append({
            "tag": e.get("tag"), "classes": e.get("classes"),
            "text": (e.get("text") or "")[:80],
            "styles": e.get("styles"),
        })
    return sig


def element_diff(prev_inv, inv):
    if prev_inv is None:
        return {"prev": None, "note": "no previous checkpoint (first of chain)"}
    if not inv.get("capture_ok"):
        return {"prev": prev_inv.get("id"), "note": "capture unavailable; diff skipped"}
    out = {"prev": prev_inv.get("id"), "added": [], "removed": [],
           "changed": [], "states": {}}
    pstates = prev_inv.get("states") or {}
    nstates = inv.get("states") or {}
    for state in sorted(set(pstates) | set(nstates)):
        p = (pstates.get(state) or {}).get("testids") or {}
        n = (nstates.get(state) or {}).get("testids") or {}
        if not p and not n:
            continue
        sdiff = {"added": sorted(set(n) - set(p)), "removed": sorted(set(p) - set(n)),
                 "changed": []}
        for tid in sorted(set(p) & set(n)):
            ps, ns = signature(p[tid]), signature(n[tid])
            if ps != ns:
                sdiff["changed"].append(tid)
        out["states"][state] = sdiff
        out["added"] += [t for t in sdiff["added"] if t not in out["added"]]
        out["removed"] += [t for t in sdiff["removed"] if t not in out["removed"]]
        out["changed"] += [t for t in sdiff["changed"] if t not in out["changed"]]
    return out


def code_diff(ws, root, prev_sid):
    if not prev_sid:
        return {"prev": None}
    prev_tree = os.path.join(root, "seal", prev_sid, "tree")
    if not os.path.isdir(prev_tree):
        return {"prev": prev_sid, "note": "prev seal tree missing"}
    now_h = hash_tree(ws, excludes=SEAL_EXCLUDES)
    prev_h = hash_tree(prev_tree, excludes=SEAL_EXCLUDES)
    added = sorted(set(now_h) - set(prev_h))
    removed = sorted(set(prev_h) - set(now_h))
    modified = sorted(k for k in set(now_h) & set(prev_h) if now_h[k] != prev_h[k])
    return {"prev": prev_sid, "added": added, "removed": removed,
            "modified": modified,
            "n_added": len(added), "n_removed": len(removed),
            "n_modified": len(modified)}


def _find_instances(inv, testid):
    out = []
    for state, st in (inv.get("states") or {}).items():
        for i, e in enumerate((st.get("testids") or {}).get(testid, []) or []):
            out.append({"state": state, "index": i, "el": e})
    return out


def build_roles(inv):
    roles = {}
    for role, hooks in ROLE_HOOKS.items():
        entries = []
        for tid in hooks:
            for inst in _find_instances(inv, tid):
                entries.append({"testid": tid, "state": inst["state"],
                                "index": inst["index"], "measured": inst["el"]})
        block = {"entries": entries}
        if role == "destructive":
            block["behavior"] = destructive_behavior(inv)
        if role == "form-validation":
            block["behavior"] = validation_behavior(inv)
        if role == "primary-action":
            block["behavior"] = feedback_behavior(inv)
        roles[role] = block
    return roles


def destructive_behavior(inv):
    states = inv.get("states") or {}
    out = {}
    for sname in ("confirm", "confirm-bulk", "post-delete"):
        st = states.get(sname) or {}
        tids = st.get("testids") or {}
        obs = {"confirm_surface": [el_summary(e) for e in tids.get("confirm", [])],
               "accept": [el_summary(e) for e in tids.get("confirm-accept", [])],
               "cancel": [el_summary(e) for e in tids.get("confirm-cancel", [])],
               "focus": st.get("focus"),
               "dialog_count": (st.get("counts") or {}).get("dialogs"),
               "trigger_delete": [el_summary(e) for e in tids.get("bookmark-delete", [])],
               "trigger_bulk": [el_summary(e) for e in tids.get("bulk-delete", [])],
               "undo": [el_summary(e) for e in tids.get("undo", [])]}
        out[sname] = obs
    # trigger placement: containment of the delete control within a card / bar
    cards = [e["el"].get("rect") for e in _find_instances(inv, "bookmark-card")]
    dels = _find_instances(inv, "bookmark-delete")
    placement = []
    for d in dels:
        r = (d["el"].get("rect") or {})
        inside_card = any(_rect_inside(r, c) for c in cards if c)
        placement.append({"state": d["state"], "inside_card": inside_card,
                          "rect": r})
    out["placement_observations"] = placement
    return out


def _rect_inside(inner, outer):
    try:
        return (outer["x"] <= inner["x"] and outer["y"] <= inner["y"]
                and inner["x"] + inner["w"] <= outer["x"] + outer["w"] + 1
                and inner["y"] + inner["h"] <= outer["y"] + outer["h"] + 1)
    except Exception:
        return False


def _rect_distance(a, b):
    try:
        ax, ay = a["x"] + a["w"] / 2, a["y"] + a["h"] / 2
        bx, by = b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
        return round(((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5, 1)
    except Exception:
        return None


def el_summary(e):
    return {"tag": e.get("tag"), "classes": e.get("classes"), "text": e.get("text"),
            "rect": e.get("rect"),
            "styles": {k: (e.get("styles") or {}).get(k)
                       for k in ("bg", "color", "borderTop", "radius", "font")}}


def validation_behavior(inv):
    st = (inv.get("states") or {}).get("invalid") or {}
    timing = st.get("invalid_timing") or {}
    steps = timing.get("steps") or []
    first_error_step = None
    for step in steps:
        errs = step.get("errors") or {}
        n = len(errs.get("form_error_nodes") or []) + len(errs.get("invalid_fields") or [])
        if n:
            first_error_step = step.get("when")
            break
    cleared_after_fix = None
    for step in steps:
        if step.get("when") == "after-fix-typing":
            errs = step.get("errors") or {}
            n = len(errs.get("form_error_nodes") or []) + len(errs.get("invalid_fields") or [])
            cleared_after_fix = (n == 0)
    return {"first_error_at": first_error_step,
            "cleared_after_fix_typing": cleared_after_fix,
            "steps": steps,
            "form_error_nodes": (st.get("testids") or {}).get("form-error", []),
            "url_field": el_summary(((st.get("testids") or {}).get("input-url") or [{}])[0])
            if (st.get("testids") or {}).get("input-url") else None}


def feedback_behavior(inv):
    """Post-action feedback observed after a completed destructive action."""
    st = (inv.get("states") or {}).get("post-delete") or {}
    tids = st.get("testids") or {}
    return {"post_delete_testids": sorted(tids.keys()),
            "undo": [el_summary(e) for e in tids.get("undo", [])],
            "toast_or_message": [el_summary(e) for e in tids.get("toast", [])] +
                                [el_summary(e) for e in tids.get("message", [])]}


def write_evidence(md_path, inv, ediff, cdiff, roles):
    lines = ["# Extraction evidence — %s" % inv["id"],
             "", "Capture ok: %s" % inv.get("capture_ok"),
             "Extracted: %s" % inv.get("extracted"), ""]
    lines.append("## States")
    for state, st in (inv.get("states") or {}).items():
        tids = st.get("testids") or {}
        lines.append("- **%s**: available=%s, testids=%d, console_errors=%d"
                     % (state, st.get("available"), len(tids),
                        len(((st.get("viewports") or {}).get("desktop") or {})
                            .get("console_errors", []))))
    if ediff:
        lines += ["", "## Element diff vs %s" % ediff.get("prev"),
                  "added: %s" % ", ".join(ediff.get("added", [])) or "added: -",
                  "removed: %s" % ", ".join(ediff.get("removed", [])) or "removed: -",
                  "changed: %s" % ", ".join(ediff.get("changed", [])) or "changed: -"]
    if cdiff and cdiff.get("prev"):
        lines += ["", "## Code diff vs %s" % cdiff.get("prev"),
                  "added=%d removed=%d modified=%d"
                  % (cdiff.get("n_added", 0), cdiff.get("n_removed", 0),
                     cdiff.get("n_modified", 0))]
        for key in ("added", "modified", "removed"):
            items = cdiff.get(key) or []
            if items:
                lines.append("- %s: %s" % (key, ", ".join(items[:40])))
    lines += ["", "## Roles"]
    for role, block in roles.items():
        lines.append("- **%s**: %d instance(s)" % (role, len(block.get("entries", []))))
    with open(md_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--root", default=X05_ROOT)
    ap.add_argument("--schedule", default=None)
    args = ap.parse_args(argv)

    root = args.root
    sched_path = args.schedule or os.path.join(root, "schedule.json")
    schedule = read_json(sched_path, {}) or {}
    run_dir = os.path.join(root, "run", args.id)
    ws = os.path.join(run_dir, "ws")
    out_dir = os.path.join(run_dir, "extraction")
    os.makedirs(out_dir, exist_ok=True)

    inv = build_inventory(args.id, run_dir)
    prev_sid, prev_dir = load_prev_extraction(root, args.id, schedule)
    prev_inv = read_json(os.path.join(prev_dir, "inventory.json")) if prev_dir else None
    ediff = element_diff(prev_inv, inv)
    cdiff = code_diff(ws, root, prev_sid)
    roles = build_roles(inv)

    write_json_atomic(os.path.join(out_dir, "inventory.json"), inv)
    write_json_atomic(os.path.join(out_dir, "diff.json"),
                      {"element": ediff, "code": cdiff, "extracted": now()})
    write_json_atomic(os.path.join(out_dir, "roles.json"),
                      {"id": args.id, "roles": roles, "extracted": now()})
    write_evidence(os.path.join(out_dir, "evidence.md"), inv, ediff, cdiff, roles)
    print("extract %s: capture_ok=%s states=%d testids=%d changed=%d code(+%d/~%d/-%d)"
          % (args.id, inv.get("capture_ok"), len(inv.get("states") or {}),
             sum(len((s.get("testids") or {})) for s in (inv.get("states") or {}).values()),
             len(ediff.get("changed", [])), cdiff.get("n_added", 0),
             cdiff.get("n_modified", 0), cdiff.get("n_removed", 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
