#!/usr/bin/env python3
"""apply_proposals.py — codify reviewer-ACCEPTED proposals into a pack.

Reads <workspace>/.design-authority/proposals/*.json where status == "accepted"
and merges each proposal's `proposed` entry into the pack's artifacts.json, its
tests.golden cases into the pack golden set, and bumps the pack version.
Idempotent (skips artifact ids already present); non-accepted proposals are
never touched. Rejected proposals are NOT codified — they become precedents
(see build_precedents / precedents.json).

    python3 tools/apply_proposals.py --workspace examples/cadence-wink --pack packs/wink
"""
import argparse
import glob
import json
import os
import re
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RESOLVE_CITES = re.compile(r"resolve\('([^']+)'\)\s+(?:still\s+)?cites\s+([\w/-]+)")


def _norm_proposed(prop):
    """Proposal payloads are one entry, or {'add': [entries], 'extend': ...}."""
    if isinstance(prop, dict) and "add" in prop:
        items = prop["add"]
        return items if isinstance(items, list) else [items]
    return [prop] if isinstance(prop, dict) else []


def _norm_tests(tests):
    """tests is {golden: [...], checks: [...]} or a plain list of checks."""
    if isinstance(tests, dict):
        return (tests.get("golden") or [], tests.get("checks") or [])
    if isinstance(tests, list):
        return ([], tests)
    return ([], [])


def _derive_golden(checks, entry_ids):
    """Derive golden cases from the proposal's own `resolve('X') cites ID` checks."""
    out = []
    for c in checks:
        m = RESOLVE_CITES.search(str(c))
        if m and m.group(2) in entry_ids:
            out.append({"problem": m.group(1), "expect": "RESOLVED",
                        "expect_id": m.group(2),
                        "note": "Derived from the proposal's own compliance checks."})
    return out

# Hand-written summaries for the codified entries (search text quality; a
# summary is what consumers read first). Keyed by proposal id suffix.
SUMMARY = {
    # wink
    "9ff839": "High-consequence actions route through a rounded 16px confirm dialog with a consequence sentence in the warm voice; confirm = ink-filled pill labelled with the concrete verb (never 'OK'); cancel = outline pill; the destructive action never receives default focus.",
    "0510d7": "Dialog/overlay vessel: white 16px-rounded card on a warm ink scrim, instant appearance (no motion invented), content composed from existing primitives.",
    "74dedc": "Empty states are a centered notice card: serif headline, one plain warm sentence, one primary pill action.",
    "d08fa9": "Inline notices: parsnip-filled rounded block with a bold lead sentence and a plain supporting line; no toast pattern observed.",
    "58de37": "Progress: yellow fill (#FFE01B) on a parsnip track, fully rounded; pair with a short step caption; no indeterminate motion.",
    # leader
    "916eda": "Charts are rectilinear and editorial: ink bars on hairline baselines (2px ink origin rule, grey/ink gridlines), a month grid of square cells, and a hairline sparkline. Red appears only as a single accent; no rings, no decorative chart styling.",
    "91ef4b": "Big statics: an Archivo (display) numeral with a sans-caps label beneath; reserved for year-to-date totals and headline counts.",
    "992c62": "Tags: ink-outline caps rectangle (8px radius); attention flips it solid red; never a pill, never colour-alone.",
    # dominion
    "522030": "Status carries state through words (bilingual pairs over-under under 560px); statuses render as ruled chips, and registers/tables stay ruled: 2px header rule, hairline rows, pewter de-emphasis.",
    "72cc3e": "Notices are full-width banded rows (#F4F4F4) under a 2px rule; sentence only, no icon, no toast.",
    "bd08f2": "Charts render in the rule-and-grid idiom: black bars on rules, a month grid, and a slate trend line; no rings, no shadows, no new colours.",
}


def _bump(version):
    try:
        a, b, c = (int(x) for x in version.split("."))
        return "%d.%d.%d" % (a, b + 1, c)
    except Exception:
        return version


def codify(workspace, pack_dir):
    prop_dir = os.path.join(os.path.abspath(workspace), ".design-authority", "proposals")
    files = sorted(glob.glob(os.path.join(prop_dir, "*.json")))
    arts_path = os.path.join(pack_dir, "artifacts.json")
    gold_path = os.path.join(pack_dir, "golden.json")
    auth_path = os.path.join(pack_dir, "authority.json")
    with open(arts_path) as fh:
        arts = json.load(fh)
    with open(gold_path) as fh:
        gold = json.load(fh)
    with open(auth_path) as fh:
        auth = json.load(fh)

    existing = {a.get("id") for a in arts["artifacts"]}
    applied, skipped = [], []
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    repo = (auth.get("snapshot") or {}).get("repo", "")

    for f in files:
        with open(f) as fh:
            rec = json.load(fh)
        if rec.get("status") != "accepted":
            continue
        pid, suf = rec["id"], rec["id"].split("-")[-1]
        entries = _norm_proposed(rec.get("proposed"))
        if not entries:
            skipped.append(pid)
            continue
        golden_cases, checks = _norm_tests(rec.get("tests"))
        new_ids = [e.get("id") for e in entries if e.get("id")]
        derived = _derive_golden(checks, set(new_ids))
        applied_here = False
        for prop in entries:
            if not prop.get("id") or prop["id"] in existing:
                continue
            applied_here = True
            body = dict(prop.get("body") or {})
            if prop.get("group") and "group" not in body:
                body["group"] = prop["group"]
            summary = SUMMARY.get(suf) or (prop.get("note") or rec.get("problem", ""))[:160]
            entry = {
                "id": prop["id"],
                "kind": prop.get("kind", "component"),
                "title": prop.get("title") or prop["id"],
                "summary": summary,
                "status": "beta",
                "aliases": prop.get("aliases", []),
                "body": body,
                "source": {"repo": repo,
                           "path": "Reviewer-accepted proposal %s (adjudicated 2026-10-07)" % pid},
                "compiled_from": [pid],
                "provenance": {
                    "proposal": pid, "gap": rec.get("gap_id"), "verdict": "accept",
                    "reviewed_at": (rec.get("review") or {}).get("reviewed_at"),
                    "codified_at": now,
                },
                "checks": checks,
            }
            if prop.get("note"):
                entry["notes"] = prop["note"]
            arts["artifacts"].append(entry)
            existing.add(prop["id"])
        if applied_here:
            applied.append(pid)
            gold["cases"].extend(golden_cases)
            gold["cases"].extend(derived)
        else:
            skipped.append(pid)

    if applied:
        old = auth.get("version", "0.0.0")
        new = _bump(old)
        auth["version"] = new
        gold["pack_version"] = "%s %s" % (auth.get("id"), new)
        with open(auth_path, "w") as fh:
            json.dump(auth, fh, indent=2)
            fh.write("\n")
        with open(arts_path, "w") as fh:
            json.dump(arts, fh, indent=2)
            fh.write("\n")
        with open(gold_path, "w") as fh:
            json.dump(gold, fh, indent=2)
            fh.write("\n")
    return {"pack": auth.get("id"), "applied": applied, "skipped": skipped,
            "version": auth.get("version")}


def main():
    ap = argparse.ArgumentParser(prog="apply_proposals.py")
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--pack", required=True)
    args = ap.parse_args()
    report = codify(args.workspace, os.path.join(ROOT, args.pack))
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
