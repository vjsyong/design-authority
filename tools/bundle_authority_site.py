#!/usr/bin/env python3
"""Bundle an authority-built site into ONE download, and write its agent brief.

Per build (authorities/<auth>/site/):

  - agent-brief.md: a paste-ready brief for a coding agent ("build my app under
    the <Name> authority"), served next to the site and inside the bundle;
  - download/<auth>-site.zip: everything in one file - the reference page with
    its styles, fonts and manifests, the build log, the machine-recorded audit
    trail, the refresh log, the gap store, and the whole authority pack
    (plus AGENT-PROMPT.md when the pack ships one), with a README.txt.

Stable URL: /authorities/<name>/site/download/<auth>-site.zip (the zip is
rebuilt by tools/refresh_authority_sites.py whenever the generated layers
refresh, so it never goes stale silently).

    python3 tools/bundle_authority_site.py [--auth NAME ...]
"""
import argparse
import hashlib
import io
import json
import os
import zipfile
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES = os.path.join(ROOT, "authorities")
PACKS = os.path.join(ROOT, "authorities")

SITE_FILES = [
    "index.html", "styles.css", "MANIFEST.md", "archive-manifest.json",
    "log.md", "audit.jsonl", "refresh-log.md", "brief.md",
]

AGENT_BRIEF = """# Agent brief: build under the {name} authority

Authority repo: `authority-{auth}` (v{version}, format {fmt}). {desc}

Reference build (what "look like this" means for this authority):
  https://designauthority.seanyong.xyz/authorities/{auth}/site/
Every recorded selector, state and note, in one directory:
  https://designauthority.seanyong.xyz/authorities/{auth}/site/#artefacts

Build an interface that conforms to THIS authority alone.

## Setup (public repo, MIT; stdlib-only CLI, no installs)

    git clone --depth 1 https://github.com/vjsyong/design-authority.git /tmp/design-authority
    cd /tmp/design-authority

## The loop, for every design decision

1. Orient once:
   python3 tools/da.py --pack packs/{auth} overview
2. Resolve each need in natural language:
   python3 tools/da.py --pack packs/{auth} resolve "primary button" --json
3. Inspect every record before adopting it:
   python3 tools/da.py --pack packs/{auth} inspect <id>
4. Adopt only records shipped by this authority. Never borrow another's
   components, values or classes.
5. When the authority is silent: build from the nearest recorded pieces, keep
   the improvisation visible (an HTML comment plus data-improv="<reason>"),
   and file it:
   python3 tools/da.py --pack packs/{auth} gap-add --need "<need>" \\
     --context '{{"source":"<your app>"}}' --workspace .design-authority

## House rules

- Quote recorded values (colours, sizes, radii, type) from the records; never
  invent values that a record can give you.
- Copy selectors and states from the artefacts directory, not from memory.
- Plain HTML/CSS is enough; the authority requires no framework.
- An agent's own report is evidence, not proof. Re-read the artifacts.

## Take it away

- Download the reference build in one file (page, styles, fonts, the pack, the
  full audit trail):
  https://designauthority.seanyong.xyz/authorities/{auth}/site/download/{auth}-site.zip
- Inside the zip, `site/` is the shipped build and `pack/` is the same authority
  data this CLI reads; `site/MANIFEST.md` lists sha256 hashes for everything.
"""


def agent_brief(auth):
    pack = json.load(open(os.path.join(PACKS, auth, "authority.json")))
    return AGENT_BRIEF.format(
        auth=auth,
        name=pack.get("name") or auth,
        version=pack.get("version") or "",
        fmt=pack.get("format_version") or "",
        desc=pack.get("description") or "",
    )


def build_bundle(auth):
    build = os.path.join(SITES, auth, "site")
    if not os.path.isfile(os.path.join(build, "index.html")):
        return None
    pack = json.load(open(os.path.join(PACKS, auth, "authority.json")))
    name = pack.get("name") or auth
    version = pack.get("version") or ""

    brief = agent_brief(auth)
    open(os.path.join(build, "agent-brief.md"), "w").write(brief)

    ddir = os.path.join(build, "download")
    os.makedirs(ddir, exist_ok=True)
    zpath = os.path.join(ddir, "%s-site.zip" % auth)

    readme = (
        "%s authority site bundle\n"
        "Built from the authority-%s repo v%s - %s UTC\n\n"
        "Contents\n"
        "  site/            the reference build as shipped: index.html, styles.css,\n"
        "                   fonts/, MANIFEST.md (sha256 of everything), build log,\n"
        "                   audit.jsonl (every authority call), refresh-log.md\n"
        "  pack/            the authority records the build was written from (JSON)\n"
        "  agent-brief.md   paste-ready brief for a coding agent\n\n"
        "Use it\n"
        "  Open site/index.html in a browser to see the reference build.\n"
        "  Point your coding agent at agent-brief.md and ask it to build under\n"
        "  this authority. Verify any file by recomputing its sha256 against\n"
        "  site/MANIFEST.md.\n"
        % (name, auth, version, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))
    )

    n = 0
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.txt", readme)
        z.writestr("agent-brief.md", brief)
        n += 2
        for fn in SITE_FILES:
            p = os.path.join(build, fn)
            if os.path.isfile(p):
                z.write(p, "site/" + fn)
                n += 1
        fdir = os.path.join(build, "fonts")
        if os.path.isdir(fdir):
            for f in sorted(os.listdir(fdir)):
                z.write(os.path.join(fdir, f), "site/fonts/" + f)
                n += 1
        gaps = os.path.join(build, ".design-authority", "gaps.jsonl")
        if os.path.isfile(gaps):
            z.write(gaps, "site/gaps.jsonl")
            n += 1
        pdir = os.path.join(PACKS, auth)
        for f in sorted(os.listdir(pdir)):
            if f.endswith(".json") or f == "AGENT-PROMPT.md":
                z.write(os.path.join(pdir, f), "pack/" + f)
                n += 1

    data = open(zpath, "rb").read()
    info = {"path": os.path.relpath(zpath, ROOT), "files": n,
            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth", nargs="*", default=None)
    args = ap.parse_args()
    auths = args.auth or [d for d in sorted(os.listdir(SITES))
                          if os.path.isfile(os.path.join(SITES, d, "index.html"))]
    for a in auths:
        info = build_bundle(a)
        if info is None:
            print("%s: skip (no build)" % a)
        else:
            print("%s: %s (%d files, %d bytes)" % (a, info["path"], info["files"], info["bytes"]))


if __name__ == "__main__":
    main()
