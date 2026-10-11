#!/usr/bin/env python3
"""P4 prepare — one-shot materials build for the maintenance-economics run.

Creates under ~/p4-maint/:
  materials/briefs/h1..h4.md        the shared per-handoff briefs
  materials/relnotes/c1..c4.md      the canonical changes as conventional
                                    release notes (baseline reference)
  materials/design-doc.md           the static design contract rendered as
                                    prose (baseline reference)
  materials/protocol-rev2.md        (copied from the x05 materials)
  materials/wrapper/run-authority   (copied from the x05 materials)
  materials/da/{tools,kernel}       frozen current tooling for the sandbox
  materials/packs/p4-da-0..4        the DA pack evolutions (change k lands in
                                    p4-da-k)
  seal/seed                         the verified seed fork, sealed

Idempotent-ish: refuses to overwrite an existing seal/seed; other outputs are
rebuilt in place. Run:  python3 docs/experiments/tools/p4_prepare.py
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p4_common import MATS, P4_ROOT, REPO, materials  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "seed-evolution", "tools"))
from x05_seal import create as seal_create, verify as seal_verify  # noqa: E402

X05_MATS = os.path.expanduser("~/x05/materials")
SRC_PACK = os.path.join(X05_MATS, "packs", "base-0.1.1-experiment")

BRIEFS = {
"h1": """# Bookmarks — this session: collections

The product exists — source in the workspace, `HANDOFF.md` for how it was
left. This session adds collections and the surrounding polish:

- **Collections.** Named groups of bookmarks. A bookmark belongs to at most
  one collection; the list screen gains a filter row of collection chips
  plus *All*, and each bookmark's editor lets the collection be chosen.
  Deleting a collection never deletes bookmarks (they return to All).
- **Import merge mode.** Re-open the import wizard's validation step and add
  a *Merge with existing* option: rows that already exist (same URL) update
  the existing entry's title/tags instead of being skipped. The skipped
  table says which rows merge and why.
- **Bulk delete undo.** Bulk delete currently asks for confirmation; after
  a bulk delete the user gets a short window to undo it. Decide and
  implement a deliberate mechanism, in the product's own character.

Everything existing keeps working. Where you deliberately change an existing
treatment, say so in your handoff. Finish runnable with `HANDOFF.md`
updated and a commit.
""",
"h2": """# Bookmarks — this session: search and tag editing

The product exists — source in the workspace, `HANDOFF.md` for how it was
left. This session adds search and reworks tag editing:

- **Search.** A search field on the list screen filters across title, URL
  and tags as the user types; combined with the collection filter it scopes
  within the active collection. An empty result is a visible state with the
  search term named and a way back.
- **Multi-select tag editing.** The bookmark editor's tag field becomes a
  proper multi-select: existing tags offered, new tags creatable inline,
  removals possible. Keep the tags data shape (`tags: []`).
- **Share/export a single collection.** From a collection's context, export
  just that collection in the existing export format, and a copy-to-
  clipboard variant of the same payload.

Everything existing keeps working. Where you deliberately change an existing
treatment, say so in your handoff. Finish runnable with `HANDOFF.md`
updated and a commit.
""",
"h3": """# Bookmarks — this session: pinning and search operators

The product exists — source in the workspace, `HANDOFF.md` for how it was
left. This session adds pinning and grows search:

- **Pin/unpin.** Bookmarks can be pinned; pinned entries sort first in
  every list context and carry a visible pin affordance. Pinning is
  available per row and in the palette as commands.
- **Search operators.** The search field understands `tag:name` (and keeps
  plain text working), combinable with the collection filter. Malformed
  operators degrade gracefully to plain text.
- **Bulk tag rename.** From the list, select several bookmarks and rename
  one of their shared tags in place (or remove it), with a confirmation
  that shows exactly what will change.

Everything existing keeps working. Where you deliberately change an existing
treatment, say so in your handoff. Finish runnable with `HANDOFF.md`
updated and a commit.
""",
"h4": """# Bookmarks — this session: favourites and conflicts

The product exists — source in the workspace, `HANDOFF.md` for how it was
left. This session is the finishing pass:

- **Pinned favourites section.** A *Favourites* section at the top of the
  list groups the pinned bookmarks with quick unpin; empty favourites show
  nothing at all (no vacant header).
- **Orphaned collections on delete.** Deleting a collection while its
  members exist must leave an obvious, recoverable state; whichever way
  you decide, the user is told what happened to the members.
- **Import conflict resolution.** When the import merge mode meets an
  entry that was edited since its last import, the wizard shows the
  conflict (both versions) and lets the user keep theirs, take the
  imported one, or skip, per row.

Everything existing keeps working. Where you deliberately change an existing
treatment, say so in your handoff. Finish runnable with `HANDOFF.md`
updated and a commit.
""",
}

RELNOTES = {
"c1": """## Design guidance change 1 — empty states are required

From this release on, **every list surface ships its empty state**: the
centered empty-state card with a title, a one-line explanation and one
action (the filter-empty variant names the active filter). Existing
surfaces are brought into line as part of normal upkeep; a list surface
without its empty state counts as unfinished work.
""",
"c2": """## Design guidance change 2 — form validation is required

Form validation is now **required** wherever users submit data: inline
error text next to the field, the danger colour role for the message, and
no reliance on console or alert noise. Screens that predate this rule get
their validation completed as they are touched.
""",
"c3": """## Design guidance change 3 — focus rings on dense rows

Dense interactive rows (bookmark rows, chip rows) must show the focus ring
on the row itself when keyboard-focused, not only on the inner controls.
Existing dense rows gain the row-level ring in this pass.
""",
"c4": """## Design guidance change 4 — tag/status chips settle

The tag/status chip treatment is final: chips keep their current look and
grow a muted count badge where sets repeat. Screens using one-off chip
variants converge on the shared treatment.
""",
}


def sh(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def copy_da_tooling():
    dst_tools = materials("da", "tools")
    dst_kernel = materials("da", "kernel")
    for d in (dst_tools, dst_kernel):
        os.makedirs(d, exist_ok=True)
    for f in sorted(os.listdir(os.path.join(REPO, "tools"))):
        if f.endswith(".py"):
            shutil.copy2(os.path.join(REPO, "tools", f), os.path.join(dst_tools, f))
    src_k = os.path.join(REPO, "kernel", "design_authority")
    dst_k = os.path.join(dst_kernel, "design_authority")
    if os.path.isdir(dst_k):
        shutil.rmtree(dst_k)
    shutil.copytree(src_k, dst_k,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print("da tooling frozen into materials/da (%d tools)" %
          len([f for f in os.listdir(dst_tools) if f.endswith('.py')]))


def write_reference_files():
    for name, body in BRIEFS.items():
        with open(materials("briefs", name + ".md"), "w") as fh:
            fh.write(body)
    for cid, body in RELNOTES.items():
        with open(materials("relnotes", cid + ".md"), "w") as fh:
            fh.write(body)
    # protocol + wrapper from the x05 materials
    for rel in ("protocol-rev2.md",):
        shutil.copy2(os.path.join(X05_MATS, rel), materials(rel))
    wdst = materials("wrapper", "run-authority")
    os.makedirs(os.path.dirname(wdst), exist_ok=True)
    shutil.copy2(os.path.join(X05_MATS, "wrapper", "run-authority"), wdst)
    os.chmod(wdst, 0o755)
    print("briefs, relnotes, protocol, wrapper written")


def write_design_doc():
    arts = json.load(open(os.path.join(SRC_PACK, "artifacts.json")))["artifacts"]
    rules = json.load(open(os.path.join(SRC_PACK, "rules.json")))["rules"]
    lines = ["# Bookmarks — design contract (static)", "",
             "The project's design conventions, as agreed across the sessions.",
             "Follow these when building; where a case is not covered, extend the",
             "nearest convention and note the decision in your handoff.", ""]
    for a in arts:
        lines.append("## %s — %s" % (a["id"], a.get("title", "")))
        lines.append("")
        lines.append(a.get("summary", ""))
        body = a.get("body") or {}
        for k, v in body.items():
            if isinstance(v, list):
                lines.append("- **%s:** %s" % (k, "; ".join(str(x) for x in v)))
            else:
                lines.append("- **%s:** %s" % (k, v))
        lines.append("")
    lines.append("## Rules")
    lines.append("")
    for r in rules:
        lines.append("- **%s (%s, %s)** — %s" % (r["id"], r["name"], r["severity"],
                                                  r.get("summary", "")))
    lines.append("")
    with open(materials("design-doc.md"), "w") as fh:
        fh.write("\n".join(lines))
    print("design-doc.md written (%d artifacts, %d rules)" % (len(arts), len(rules)))


# ---------------------------------------------------------------- pack chain
def _bump(pack_dir, version, note):
    ap = os.path.join(pack_dir, "authority.json")
    au = json.load(open(ap))
    au["version"] = version
    json.dump(au, open(ap, "w"), indent=1, ensure_ascii=False)
    bp = os.path.join(pack_dir, "BUILD.json")
    b = json.load(open(bp))
    b.setdefault("notes", []).append(note)
    json.dump(b, open(bp, "w"), indent=1, ensure_ascii=False)


def _record_add_policy(pack_dir, rid, reason):
    ap = os.path.join(pack_dir, "artifacts.json")
    d = json.load(open(ap))
    for a in d["artifacts"]:
        if a["id"] == rid:
            a["transition"] = {"policy": "required",
                               "reason": reason,
                               "since": "P4" }
            break
    else:
        raise SystemExit("record %s not found" % rid)
    json.dump(d, open(ap, "w"), indent=1, ensure_ascii=False)


def build_pack_chain():
    base = materials("packs")
    os.makedirs(base, exist_ok=True)
    p0 = os.path.join(base, "p4-da-0")
    if os.path.exists(p0):
        shutil.rmtree(p0)
    shutil.copytree(SRC_PACK, p0)
    prev = p0
    steps = [
        ("p4-da-1", "0.1.2-experiment", "empty-state", None,
         "P4 change 1: empty states are mandatory on list surfaces"),
        ("p4-da-2", "0.1.3-experiment", "form-validation", None,
         "P4 change 2: form validation is required"),
        ("p4-da-3", "0.1.4-experiment", None, "focus", 
         "P4 change 3: row-level focus rings on dense interactive rows"),
        ("p4-da-4", "0.1.5-experiment", "tags-status", None,
         "P4 change 4: tag/status chip treatment settled"),
    ]
    for name, ver, rid, kind, note in steps:
        dst = os.path.join(base, name)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(prev, dst)
        if rid:
            _record_add_policy(dst, {"empty-state": "pattern/empty-state",
                                     "form-validation": "pattern/form-validation",
                                     "tags-status": "component/tags-status"}[rid], note)
        if kind == "focus":
            rp = os.path.join(dst, "rules.json")
            d = json.load(open(rp))
            d["rules"].append({
                "id": "B005",
                "name": "Row-level focus on dense rows",
                "severity": "error",
                "applies_to": ["component/*"],
                "summary": "Dense interactive rows (bookmark rows, chip rows) show the focus ring on the row itself when keyboard-focused, not only on inner controls.",
                "why": "P4 change 3: keyboard users must see the focused row at a glance.",
            })
            json.dump(d, open(rp, "w"), indent=1, ensure_ascii=False)
        _bump(dst, ver, note)
        prev = dst
        print("pack built:", name, "->", ver)


def seal_seed():
    seed = os.path.join(P4_ROOT, "seed")
    if os.path.exists(os.path.join(P4_ROOT, "seal", "seed")):
        print("seal/seed exists; leaving as is")
        return
    gd = os.path.join(seed, ".git")
    for dirpath, dirnames, filenames in os.walk(seed):
        os.chmod(dirpath, 0o755)
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                os.chmod(fp, 0o644)
    if os.path.isdir(gd):
        shutil.rmtree(gd)
    seal_create(seed, "seed", root=P4_ROOT)
    bad, info = seal_verify(os.path.join(P4_ROOT, "seal", "seed"))
    if bad:
        raise SystemExit("seed seal failed: %s" % bad[:5])
    print("seal/seed created and verified:", info if isinstance(info, dict) else "")


def main():
    for d in ("run", "seal", "materials/briefs", "materials/relnotes"):
        os.makedirs(materials(*(d.split("/")[1:])) if d.startswith("materials/")
                    else os.path.join(P4_ROOT, d), exist_ok=True)
    copy_da_tooling()
    write_reference_files()
    write_design_doc()
    build_pack_chain()
    seal_seed()
    print("P4 materials ready under", P4_ROOT)


if __name__ == "__main__":
    main()
