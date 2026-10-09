#!/usr/bin/env python3
"""Build the validation-bearing pack: base-0.1.1-experiment.

Inputs: the sealed canon pack (base-0.1.0-experiment), the sealed seed tree
(f3 — used to generate the lint baseline), and the linter source
(tools/bookmarks_lint.py).

Outputs: a complete pack directory with the canon byte-identical plus:
  lint/bookmarks_lint.py    (copy of the linter, pack-local)
  lint/baseline.json        (testids, allowed literals, allowed custom
                             props, allowed duplicate hashes — generated
                             from the sealed seed with the SAME scanner
                             the enforcement uses)
  validators.json           (declares base-lint)
  authority.json            (version 0.1.1-experiment; capabilities
                             validators cited)
  BUILD.json                (build note appended)

Everything else is copied untouched; the sealed 0.1.0 pack is never
modified. Re-runnable: delete the output and rerun.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bookmarks_lint as bl  # noqa: E402

SEED_FILES = ("index.html", "styles.css", "app.js")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-pack", required=True)
    ap.add_argument("--out-pack", required=True)
    ap.add_argument("--seed-tree", required=True,
                    help="sealed f3 tree directory")
    ap.add_argument("--lint-src", default=os.path.join(HERE,
                                                       "bookmarks_lint.py"))
    args = ap.parse_args()

    # ---- scan the sealed seed with the enforcement scanner
    scan = bl.scan_tree(args.seed_tree)
    allowed_literals = sorted({bl.norm_literal(l)
                               for _, _, l in scan["literals"]})
    allowed_props = sorted({name for _, _, name in scan["custom_props"]})
    allowed_dups = sorted(bl.dup_groups(scan["blocks"]).keys())
    baseline = {
        "source": {"seal": os.path.basename(
                       os.path.dirname(args.seed_tree.rstrip("/"))),
                   "files": {f: sha256(os.path.join(args.seed_tree, f))
                             for f in SEED_FILES
                             if os.path.exists(os.path.join(args.seed_tree, f))}},
        "generated_by": "x05_build_validated_pack.py / bookmarks-lint v1",
        "testids": scan["testids"],
        "allowed_literals": allowed_literals,
        "allowed_custom_props": allowed_props,
        "allowed_dup_hashes": allowed_dups,
    }

    # ---- assemble the new pack
    if os.path.exists(args.out_pack):
        shutil.rmtree(args.out_pack)
    shutil.copytree(args.src_pack, args.out_pack)
    os.makedirs(os.path.join(args.out_pack, "lint"), exist_ok=True)
    shutil.copy2(args.lint_src,
                 os.path.join(args.out_pack, "lint", "bookmarks_lint.py"))
    with open(os.path.join(args.out_pack, "lint", "baseline.json"), "w") as fh:
        json.dump(baseline, fh, indent=1, sort_keys=True)

    validators = {
        "validators": [{
            "name": "base-lint",
            "title": "Bookmarks lint engine",
            "kind": "command",
            "workdir": "{pack}",
            "command": ["python3", "lint/bookmarks_lint.py", "{target}",
                        "--json"],
            "parser": "lint-json",
            "applies_to": ["css", "html", "js"],
            "rules_source": "rules.json",
            "notes": ("Runs the pack-local linter over the target "
                      "workspace. Delta-based against lint/baseline.json "
                      "(generated from sealed seed f3): B001 new raw "
                      "colour literals outside :root; B002 baseline QA "
                      "hooks missing; B003 canonical storage key absent; "
                      "B004 (warnings) token definitions outside :root "
                      "and new duplicated treatment blocks. Report shape: "
                      "findings[{rule,severity,file,line,message,excerpt,"
                      "fix}], counts, by_rule, score."),
        }]
    }
    with open(os.path.join(args.out_pack, "validators.json"), "w") as fh:
        json.dump(validators, fh, indent=1)

    # ---- patch authority.json + BUILD.json
    a_path = os.path.join(args.out_pack, "authority.json")
    auth = json.load(open(a_path))
    auth["version"] = "0.1.1-experiment"
    auth["description"] = (auth.get("description", "") +
                           " Version 0.1.1-experiment adds declared "
                           "validators (base-lint).")
    auth.setdefault("capabilities", {})["validators"] = ["base-lint"]
    with open(a_path, "w") as fh:
        json.dump(auth, fh, indent=1)
        fh.write("\n")

    b_path = os.path.join(args.out_pack, "BUILD.json")
    build = {}
    if os.path.exists(b_path):
        build = json.load(open(b_path))
    build["derived"] = {
        "from": "base-0.1.0-experiment", "to": "base-0.1.1-experiment",
        "built_at": datetime.now(timezone.utc).isoformat(),
        "builder": "x05_build_validated_pack.py",
        "adds": ["lint/bookmarks_lint.py", "lint/baseline.json",
                 "validators.json"],
        "notes": ("Canon files copied byte-identical from 0.1.0; only the "
                  "three files above plus version/capabilities fields "
                  "changed. Baseline generated from sealed seed f3."),
    }
    with open(b_path, "w") as fh:
        json.dump(build, fh, indent=1)

    print("built:", args.out_pack)
    print("baseline: %d testids, %d allowed literals, %d allowed props, "
          "%d allowed dup-groups" % (len(baseline["testids"]),
                                     len(allowed_literals),
                                     len(allowed_props), len(allowed_dups)))


if __name__ == "__main__":
    main()
