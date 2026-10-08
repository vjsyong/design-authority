#!/usr/bin/env python3
"""Keep every authority-built site's generated layers current with its pack.

Built sites (examples/authority-sites/<auth>/) are agent-authored pages plus
generated layers. This tool re-runs the generated layers whenever the pack's
authority.json / artifacts.json change:

  - section#artefacts is re-rendered from the pack (new/removed artefacts,
    counts, selectors, states; its kicker carries the pack version);
  - the previous pack version string is updated wherever the page stamped it;
  - a stale notice appears (and clears) when the artefact SET has moved on
    since the page was authored: the article sections cannot self-heal, so
    the page says so instead of quietly rotting;
  - the archive manifest is re-hashed and a line lands in refresh-log.md.

No change -> no-op. State lives in .site-state.json per build. Run from the
authority-site-refresh timer; served routes are no-cache, so a refresh shows
on the next request.

    python3 tools/refresh_authority_sites.py [--auth NAME ...] [--force]
"""
import argparse
import hashlib
import importlib.util
import json
import os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES = os.path.join(ROOT, "examples", "authority-sites")
TOOLS = os.path.join(ROOT, "tools")

HASH_FILES = ["authority.json", "artifacts.json"]


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(TOOLS, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


aas = _load("add_artefacts_section", "add_artefacts_section.py")
aaa = _load("archive_authority_assets", "archive_authority_assets.py")


def pack_state(auth):
    """(content hash, version, sorted artifact ids) for the generated layers."""
    base = os.path.join(ROOT, "packs", auth)
    h = hashlib.sha256()
    for f in HASH_FILES:
        p = os.path.join(base, f)
        if os.path.isfile(p):
            h.update(f.encode())
            h.update(open(p, "rb").read())
    auth_json = json.load(open(os.path.join(base, "authority.json")))
    arts = json.load(open(os.path.join(base, "artifacts.json")))["artifacts"]
    return h.hexdigest(), str(auth_json.get("version") or ""), sorted(a["id"] for a in arts)


def replace_version(html, old, new):
    if not old or not new or old == new:
        return html, 0
    return html.replace(old, new), html.count(old)


def notice_for(authored, ids):
    cur = set(ids)
    aut = set(authored.get("ids") or [])
    if cur == aut:
        return None
    added, removed = sorted(cur - aut), sorted(aut - cur)
    bits = []
    if added:
        bits.append("%d added" % len(added))
    if removed:
        bits.append("%d removed" % len(removed))
    return ("This page's article sections were written for pack %s with %d artefacts. "
            "The records now hold %d artefacts (%s). The directory below is current; "
            "the article sections may lag."
            % (authored.get("version") or "?", len(aut), len(cur), ", ".join(bits)))


def refresh(auth, force=False):
    build = os.path.join(SITES, auth)
    page = os.path.join(build, "index.html")
    if not os.path.isfile(page):
        return "skip (no build)"
    h, version, ids = pack_state(auth)
    sp = os.path.join(build, ".site-state.json")
    state = json.load(open(sp)) if os.path.isfile(sp) else None
    if state and state.get("pack_hash") == h and not force:
        return "unchanged"

    replaced = 0
    if state and state.get("version") and state["version"] != version:
        html = open(page).read()
        html, replaced = replace_version(html, state["version"], version)
        if replaced:
            open(page, "w").write(html)

    authored = (state or {}).get("authored_for") or {"version": version, "ids": ids}
    notice = notice_for(authored, ids)
    aas.inject(auth, notice=notice)
    aaa.archive(auth)

    line = ("- %s UTC: pack %s -> %s; artefacts %d -> %d; version stamps updated: %d; "
            "stale notice: %s\n"
            % (datetime.now(timezone.utc).isoformat(timespec="seconds"),
               (state or {}).get("version") or "-", version,
               len(authored.get("ids") or []), len(ids), replaced,
               "shown" if notice else "none/cleared"))
    with open(os.path.join(build, "refresh-log.md"), "a") as fh:
        fh.write(line)
    json.dump({"pack_hash": h, "version": version, "ids": ids,
               "authored_for": authored,
               "refreshed_at": datetime.now(timezone.utc).isoformat(timespec="seconds")},
              open(sp, "w"), indent=1)
    return "refreshed (v%s, %d artefacts%s)" % (version, len(ids),
                                                ", notice shown" if notice else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth", nargs="*", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--mark-authored", action="store_true",
                    help="after a manual page rebuild: mark the authored sections as "
                         "written for the CURRENT pack (resets the stale notice)")
    args = ap.parse_args()
    auths = args.auth or [d for d in sorted(os.listdir(SITES))
                          if os.path.isfile(os.path.join(SITES, d, "index.html"))]
    for a in auths:
        if args.mark_authored:
            sp = os.path.join(SITES, a, ".site-state.json")
            if os.path.isfile(sp):
                st = json.load(open(sp))
                st["authored_for"] = {"version": st.get("version"), "ids": st.get("ids")}
                json.dump(st, open(sp, "w"), indent=1)
                print("%s: authored sections marked for v%s (%d artefacts)"
                      % (a, st.get("version"), len(st.get("ids") or [])))
        print("%s: %s" % (a, refresh(a, force=args.force or args.mark_authored)))


if __name__ == "__main__":
    main()
