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

## Setup (public repos, MIT; stdlib-only CLI)

Get the pack - either route works; the zip also carries this authority's
reference build, fonts and manifests:

Route A - bundle zip (one download):

    curl -fsSL -o {auth}-site.zip https://designauthority.seanyong.xyz/authorities/{auth}/site/download/{auth}-site.zip
    python3 -c "import zipfile; zipfile.ZipFile('{auth}-site.zip').extractall('{auth}-authority')"

Route B - git (the pack is its own repository):

    git clone --depth 1 https://github.com/vjsyong/authority-{auth}.git /tmp/authority-{auth}

Tooling (same for both routes):

    git clone --depth 1 https://github.com/vjsyong/design-authority.git /tmp/design-authority
    cd /tmp/design-authority
    export PACK=/tmp/authority-{auth}      # Route B
    # or, from where you unzipped:  export PACK="$PWD/{auth}-authority/pack"   # Route A

Sanity check (prints the authority overview):

    python3 tools/da.py --pack "$PACK" overview

## The loop, for every design decision

1. Resolve each need in natural language:
   python3 tools/da.py --pack "$PACK" resolve "primary button" --json
2. Inspect every record before adopting it:
   python3 tools/da.py --pack "$PACK" inspect <id>
3. ADOPT THE RECORDED SELECTOR along with the recorded values: the
   verification contract below addresses elements by their recorded class
   names (.cta, .card, .dlg, .ledger, .badge, ...). Keep those names on the
   elements you build; if you must deviate, declare it in verify.map.json
   (see Verify below).
4. Adopt only records shipped by this authority. Never borrow another's
   components, values or classes.
5. When the authority is silent: build from the nearest recorded pieces, keep
   the improvisation visible (an HTML comment plus data-improv="<reason>"),
   and file it:
   python3 tools/da.py --pack "$PACK" gap-add --need "<need>" \\
     --context '{{"source":"<your app>"}}' --workspace .design-authority

## Verify before you claim done

The pack ships a verification contract (`verification.json`): mechanically
checkable assertions for this authority's records (computed-style, DOM,
static, interaction). It is a separate layer from `validators` (the lint
path, which may be empty). Run it over your build:

    python3 tools/da_verify.py --pack "$PACK" --target <your-app-dir> --out .verify

Reading the result: PASS / VIOLATION (fix it) / UNVERIFIABLE (could not run,
usually a missing selector or file) / N/A (declared ignore) / REVIEW_REQUIRED
(human item). Browser-backed checks need Playwright:

    python3 -m venv .venv && .venv/bin/pip install playwright && .venv/bin/playwright install chromium
    .venv/bin/python3 tools/da_verify.py --pack "$PACK" --target <your-app-dir> --out .verify

If your build cannot keep a recorded selector (or uses different file names),
declare it in `verify.map.json` in your app root:

    {{"files": {{"css": ["styles.css"], "html": ["index.html"]}},
      "selectors": {{".dlg": ".dialog"}},
      "ignore": {{"authority/check-id": "why this build is exempt"}}}}

## House rules

- Quote recorded values (colours, sizes, radii, type) from the records; never
  invent values that a record can give you.
- Copy selectors and states from the artefacts directory, not from memory.
- Plain HTML/CSS is enough; the authority requires no framework.
- An agent's own report is evidence, not proof. Re-read the artifacts, then
  run the verification contract.

## Take it away

- Download the reference build in one file (page, styles, fonts, the pack, the
  full audit trail):
  https://designauthority.seanyong.xyz/authorities/{auth}/site/download/{auth}-site.zip
- Inside the zip, `site/` is the shipped build and `pack/` is the same authority
  data this CLI reads; `site/MANIFEST.md` lists sha256 hashes for everything.
- `quickstart.sh` wires the pack and prints the first commands.
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
        "  agent-brief.md   paste-ready brief for a coding agent\n"
        "  quickstart.sh    wires the pack and prints the first commands\n\n"
        "Use it\n"
        "  Open site/index.html in a browser to see the reference build.\n"
        "  Point your coding agent at agent-brief.md and ask it to build under\n"
        "  this authority. Verify any file by recomputing its sha256 against\n"
        "  site/MANIFEST.md. Before a build is called done, run the pack's\n"
        "  verification contract (tools/da_verify.py - see agent-brief.md).\n"
        % (name, auth, version, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))
    )

    quickstart = (
        "#!/usr/bin/env bash\n"
        "# %s authority quickstart - wires the pack and prints the first commands.\n"
        "# Run from the unzipped bundle directory: bash quickstart.sh\n"
        "set -euo pipefail\n"
        "HERE=\"$(cd \"$(dirname \"$0\")\" && pwd)\"\n"
        "if [ ! -d \"$HERE/pack\" ]; then\n"
        "  echo \"error: pack/ not found - run me from the unzipped bundle\" >&2\n"
        "  exit 1\n"
        "fi\n"
        "echo \"Pack: $HERE/pack\"\n"
        "echo\n"
        "echo 'Tooling (once):'\n"
        "echo '  git clone --depth 1 https://github.com/vjsyong/design-authority.git /tmp/design-authority'\n"
        "echo '  cd /tmp/design-authority'\n"
        "echo\n"
        "echo 'First commands (inside /tmp/design-authority):'\n"
        "echo \"  export PACK=$HERE/pack\"\n"
        "echo '  python3 tools/da.py --pack \"$PACK\" overview'\n"
        "echo '  python3 tools/da.py --pack \"$PACK\" resolve \"primary button\" --json'\n"
        "echo\n"
        "echo 'Before claiming done, verify (see agent-brief.md):'\n"
        "echo '  python3 tools/da_verify.py --pack \"$PACK\" --target <your-app-dir> --out .verify'\n"
        % name
    )

    n = 0
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.txt", readme)
        z.writestr("agent-brief.md", brief)
        qinfo = zipfile.ZipInfo("quickstart.sh")
        qinfo.external_attr = 0o755 << 16
        z.writestr(qinfo, quickstart)
        n += 3
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
