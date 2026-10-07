#!/usr/bin/env python3
"""Build the Triage Authority Pack from a pinned snapshot (stdlib only).

    python3 tools/build_pack_triage.py                 # build packs/triage from the default snapshot
    python3 tools/build_pack_triage.py --check         # fail if the generated pack drifts from the snapshot+curation
    python3 tools/build_pack_triage.py --snapshot DIR --out DIR --allow-drift

The generated files (authority.json, artifacts.json, rules.json, recipes.json,
fallbacks.json, prohibitions.json, validators.json, scoring.json, BUILD.json)
are committed next to the hand-authored curation/ inputs. Edit curation/*,
never the generated files; rerun this script.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import NoReturn

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_SNAPSHOT = os.path.expanduser("~/triage-design-system-demo")
DEFAULT_OUT = os.path.join(ROOT, "packs", "triage")
EXPECTED_COMMIT = "e374f3803d5a4e2a5f4fee7b1ba6e41e73b0e11b"

GENERATED = ["authority.json", "artifacts.json", "rules.json", "recipes.json",
             "fallbacks.json", "prohibitions.json", "validators.json",
             "scoring.json", "BUILD.json"]


def die(msg: str) -> NoReturn:
    print("ERROR: %s" % msg, file=sys.stderr)
    sys.exit(1)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def count_token_nodes(node):
    n = 0
    if isinstance(node, dict):
        for k, v in node.items():
            if k.startswith("$"):
                continue
            if isinstance(v, dict) and "$value" in v:
                n += 1
            elif isinstance(v, dict):
                n += count_token_nodes(v)
    return n


def docg_sanity(tokens):
    """Placeholder for the D-015 conformance gate (structural checks only for now)."""
    return []


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", default=DEFAULT_SNAPSHOT)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--allow-drift", action="store_true")
    args = ap.parse_args(argv)

    snap = os.path.abspath(args.snapshot)
    out = os.path.abspath(args.out)
    cur = os.path.join(out, "curation")
    for p in (snap, cur):
        if not os.path.isdir(p):
            die("missing path: %s" % p)

    # -- snapshot identity -----------------------------------------------------
    try:
        commit = subprocess.check_output(
            ["git", "-C", snap, "rev-parse", "HEAD"], text=True).strip()
    except Exception as exc:
        die("cannot read snapshot commit: %s" % exc)
    warnings = []
    if commit != EXPECTED_COMMIT:
        msg = "snapshot commit %s != expected %s" % (commit[:10], EXPECTED_COMMIT[:10])
        if not args.allow_drift:
            die(msg + " (use --allow-drift to build anyway and record it)")
        warnings.append(msg)

    states = load_json(os.path.join(snap, "spec", "states.json"))
    rules_doc = load_json(os.path.join(snap, "spec", "rules.json"))
    tokens = load_json(os.path.join(snap, "tokens", "tokens.json"))
    version = open(os.path.join(snap, "VERSION")).read().strip()

    aliases = load_json(os.path.join(cur, "aliases.json"))
    notes = load_json(os.path.join(cur, "component-notes.json"))
    docs_map = load_json(os.path.join(cur, "docs-map.json"))
    recipes_in = load_json(os.path.join(cur, "recipes.json"))["recipes"]
    fallbacks_in = load_json(os.path.join(cur, "fallbacks.json"))["fallbacks"]
    prohibitions_in = load_json(os.path.join(cur, "prohibitions.json"))["prohibitions"]
    guidelines_in = load_json(os.path.join(cur, "guidelines.json"))["guidelines"]
    tokensets_in = load_json(os.path.join(cur, "token-sets.json"))["token_sets"]
    references_in = load_json(os.path.join(cur, "references.json"))["references"]
    patterns_in = load_json(os.path.join(cur, "patterns.json"))["patterns"]

    # -- artifacts -------------------------------------------------------------
    artifacts = []
    for c in states["components"]:
        cid = "component/%s" % c["class"]
        artifacts.append({
            "id": cid,
            "kind": "component",
            "title": c["name"],
            "summary": notes.get(cid, "%s component (see source for states/a11y)." % c["name"]),
            "status": c.get("status", "stable"),
            "aliases": aliases.get(cid, []),
            "body": {
                "class": c["class"],
                "states": c.get("states", []),
                "verify": c.get("verify", []),
                "a11y": c.get("a11y", []),
                "source_file": c.get("source", ""),
            },
            "relations": ([{"rel": "documented-at", "url": docs_map[cid]}]
                          if cid in docs_map else []),
            "source": {"repo": "vjsyong/triage-design-system", "commit": commit,
                       "path": "spec/states.json", "pointer": c["class"]},
        })

    for p in patterns_in:
        artifacts.append({
            "id": p["id"], "kind": "pattern", "title": p["title"],
            "summary": p["summary"], "status": "documented",
            "aliases": aliases.get(p["id"], []),
            "body": {"sources": p["sources"], "note": "no states/verify contract (see gap G-003)"},
            "relations": [],
            "source": {"repo": "vjsyong/triage-design-system", "commit": commit,
                       "path": "site/ + src/core/patterns.css"},
        })

    for g in guidelines_in:
        artifacts.append({
            "id": g["id"], "kind": "guideline", "title": g["title"],
            "summary": g["summary"], "status": "normative",
            "aliases": aliases.get(g["id"], []),
            "body": {"do": g.get("do", []), "dont": g.get("dont", []),
                     "quote": g.get("quote"), "enforced_by": g.get("enforced_by")},
            "relations": [],
            "source": {"repo": "vjsyong/triage-design-system", "commit": commit,
                       "path": g["source"]},
        })

    for t in tokensets_in:
        artifacts.append({
            "id": t["id"], "kind": "token-set", "title": t["title"],
            "summary": t["summary"], "status": "source-of-truth",
            "aliases": aliases.get(t["id"], []),
            "body": {"group": t["group"]},
            "relations": [],
            "source": {"repo": "vjsyong/triage-design-system", "commit": commit,
                       "path": t["source"]},
        })

    example_dir = os.path.join(snap, "examples")
    for name in sorted(os.listdir(example_dir)):
        if not name.endswith(".html"):
            continue
        text = open(os.path.join(example_dir, name)).read()
        m = re.search(r"<title>(.*?)</title>", text, re.S)
        title = (m.group(1).strip() if m else name)
        classes = set()
        for cm in re.finditer(r'class="([^"]+)"', text):
            classes.update(cm.group(1).split())
        eid = "example/%s" % name[:-5]
        artifacts.append({
            "id": eid, "kind": "example", "title": "Example: %s" % title,
            "summary": "Reference screen (%d classes used)." % len(classes),
            "status": "reference",
            "aliases": [],
            "body": {"path": "examples/" + name, "classes_used": len(classes)},
            "relations": [],
            "source": {"repo": "vjsyong/triage-design-system", "commit": commit,
                       "path": "examples/" + name},
        })

    for r in references_in:
        artifacts.append({
            "id": r["id"], "kind": "reference", "title": r["title"],
            "summary": r["summary"], "status": "documented",
            "aliases": r.get("aliases", []),
            "body": {},
            "relations": [],
            "source": {"repo": "vjsyong/triage-design-system", "commit": commit,
                       "path": r["path"]},
        })

    # -- rules (pass-through + enforcement) -------------------------------------
    rules = []
    for r in rules_doc["rules"]:
        rules.append({
            "id": r["id"], "name": r["name"], "severity": r["severity"],
            "applies_to": r.get("applies_to", []),
            "summary": r["summary"], "why": r["why"], "fix": r["fix"],
            "enforcement": {"mode": "validator", "validator": "triage-lint"},
        })

    # -- recipes / fallbacks / prohibitions -------------------------------------
    recipes = []
    for rec in recipes_in:
        recipes.append({"id": rec["id"], "kind": "recipe", "title": rec["title"],
                        "summary": rec["summary"], "needs": rec["needs"],
                        "ingredients": rec["ingredients"],
                        "constraints": rec["constraints"],
                        "evidence": rec["evidence"]})
    fallbacks = [dict(f, kind="fallback") for f in fallbacks_in]
    prohibitions = [dict(p, kind="prohibition") for p in prohibitions_in]

    # -- evolution provenance overlay (experimental; absent in the pinned pack,
    #    where this is a no-op) --------------------------------------------------
    prov_path = os.path.join(cur, "evolution.json")
    release_meta = None
    if os.path.exists(prov_path):
        prov = load_json(prov_path)
        release_meta = prov.get("release")
        by_id = {it["id"]: it for it in (artifacts + recipes + fallbacks + prohibitions)}
        for aid, block in prov.get("provenance", {}).items():
            if aid in by_id:
                by_id[aid]["provenance"] = block
            else:
                warnings.append("provenance references unknown id: %s" % aid)

    # -- cross-validation --------------------------------------------------------
    ids = [a["id"] for a in artifacts] + [r["id"] for r in recipes] + \
          [f["id"] for f in fallbacks] + [p["id"] for p in prohibitions]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        die("duplicate ids: %s" % dupes)
    idset = set(ids)

    problems = []
    for rec in recipes:
        for ing in rec["ingredients"]:
            if ing not in idset:
                problems.append("recipe %s: unknown ingredient %s" % (rec["id"], ing))
    for p in prohibitions:
        for rel in p.get("related", []):
            if rel not in idset:
                problems.append("prohibition %s: unknown related %s" % (p["id"], rel))
    for t in tokensets_in:
        if t["group"] not in tokens:
            problems.append("token-set %s: group %r missing in tokens.json" % (t["id"], t["group"]))
    if problems:
        die("cross-validation failed:\n  " + "\n  ".join(problems))

    for c in states["components"]:
        cid = "component/%s" % c["class"]
        if cid not in docs_map:
            warnings.append("no docs mapping for %s" % cid)
        if not aliases.get(cid):
            warnings.append("no aliases for %s" % cid)

    # -- outputs -----------------------------------------------------------------
    manifest = {
        "id": "triage",
        "name": "Triage Design System",
        "format_version": "0.1",
        "version": version,
        "snapshot": {"repo": "vjsyong/triage-design-system", "commit": commit,
                     "branch": "tds-fix-wrap", "version": version,
                     "path_hint": "~/triage-design-system-demo"},
        "description": "The central, app-agnostic UI design authority for these products.",
        "kinds": ["component", "pattern", "token-set", "guideline", "recipe",
                  "example", "reference"],
        "capabilities": {"search": True, "resolve": True,
                          "validators": ["triage-lint"],
                          "gap_reporting": True, "extension_proposals": True,
                          "resolution_assist": "off"},
        "policy": {
            "on_undefined": "Implement per the consuming project's fallback policy, mark the improvisation, and report a gap. Never present improvisation as canonical.",
            "on_conflict": "Do not implement as requested; the request violates an explicit constraint (see the cited rule/prohibition).",
            "proposals": "Noncanonical. The authority is never modified by a consumer; proposals are reviewed upstream.",
        },
        "entrypoints": {"artifacts": "artifacts.json", "rules": "rules.json",
                         "recipes": "recipes.json", "fallbacks": "fallbacks.json",
                         "prohibitions": "prohibitions.json",
                         "validators": "validators.json", "scoring": "scoring.json"},
    }

    validators = {"validators": [{
        "name": "triage-lint",
        "title": "Triage lint engine",
        "kind": "command",
        "workdir": "{snapshot}",
        "command": ["python3", "lint/triage_lint.py", "{target}", "--json"],
        "parser": "triage-lint-json",
        "applies_to": ["css", "html", "js"],
        "rules_source": "rules.json",
        "notes": "Runs the pinned snapshot's linter over the target path. --json report shape: findings[{rule,severity,file,line,message,excerpt,fix}], counts, by_rule, score.",
    }]}

    scoring = {"formula": rules_doc.get("score", {}).get("formula",
               "score = max(0, 100 - (errors*8 + warnings*2 + infos*0.5))"),
               "gate": rules_doc.get("score", {}).get("gate", ""),
               "source": "spec/rules.json#score"}

    token_counts = {k: count_token_nodes(v) for k, v in tokens.items()
                    if not k.startswith("$") and isinstance(v, dict)}

    receipt = {
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "snapshot": {"path": snap, "commit": commit, "version": version},
        "counts": {
            "artifacts": len(artifacts), "rules": len(rules),
            "recipes": len(recipes), "fallbacks": len(fallbacks),
            "prohibitions": len(prohibitions),
            "components": sum(1 for a in artifacts if a["kind"] == "component"),
            "patterns": sum(1 for a in artifacts if a["kind"] == "pattern"),
            "guidelines": sum(1 for a in artifacts if a["kind"] == "guideline"),
            "examples": sum(1 for a in artifacts if a["kind"] == "example"),
            "token_sets": sum(1 for a in artifacts if a["kind"] == "token-set"),
            "references": sum(1 for a in artifacts if a["kind"] == "reference"),
        },
        "token_nodes": token_counts,
        "curation_sha256": {f: sha256(os.path.join(cur, f))
                             for f in sorted(os.listdir(cur)) if f.endswith(".json")},
        "warnings": warnings,
        **({"release": release_meta} if release_meta is not None else {}),
        "notes": [
            "DTCG full-schema conformance check pending (D-015); structural sanity only.",
            "docs-map.json is approximate (site group pages).",
        ],
    }

    outputs = {
        "authority.json": manifest,
        "artifacts.json": {"artifacts": artifacts},
        "rules.json": {"$note": "Pass-through of spec/rules.json with enforcement added.",
                       "rules": rules},
        "recipes.json": {"recipes": recipes},
        "fallbacks.json": {"fallbacks": fallbacks},
        "prohibitions.json": {"prohibitions": prohibitions},
        "validators.json": validators,
        "scoring.json": scoring,
        "BUILD.json": receipt,
    }

    if args.check:
        drift = []
        for name, data in outputs.items():
            if name == "BUILD.json":   # volatile receipt (built_at timestamp)
                continue
            path = os.path.join(out, name)
            if not os.path.exists(path) or load_json(path) != data:
                drift.append(name)
        if drift:
            die("pack drift: %s (run the builder without --check)" % ", ".join(drift))
        print("pack is up to date (%d files checked)" % len(outputs))
        return 0

    for name, data in outputs.items():
        with open(os.path.join(out, name), "w") as fh:
            json.dump(data, fh, indent=1, sort_keys=False)
            fh.write("\n")
    print("built %s" % out)
    for k, v in receipt["counts"].items():
        print("  %-12s %d" % (k, v))
    if warnings:
        print("  warnings: %d (see BUILD.json)" % len(warnings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
