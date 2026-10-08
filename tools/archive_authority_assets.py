#!/usr/bin/env python3
"""Archive an authority-built site's static assets and emit its audit manifest.

For each build under examples/authority-sites/<auth>/:
  1. Extracts inline <style> blocks into a first-class styles.css (so the CSS
     is an auditable artifact, not bytes buried in HTML) and links it.
  2. Verifies every font file byte-for-byte against its known source.
  3. Writes archive-manifest.json + MANIFEST.md: sha256 of every file in the
     build (page, stylesheet, fonts, log, audit trail, gap store) with roles
     and provenance, plus the authority identity (pack + version).

Idempotent: a build that already has styles.css and a manifest is refreshed,
not duplicated. Served as-is under /authorities/<name>/site/.

    python3 tools/archive_authority_assets.py [--auth NAME ...]
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES = os.path.join(ROOT, "examples", "authority-sites")
PACKS = os.path.join(ROOT, "packs")

# known font sources per authority (name -> [candidate dirs])
FONT_SOURCES = {
    "wink": [os.path.join(ROOT, "docs/synthesis/wink/tile/fonts")],
    "leader": [os.path.join(ROOT, "docs/synthesis/leader/tile/fonts")],
    "dominion": [os.path.join(ROOT, "docs/synthesis/dominion/tile/fonts")],
    "phantom": [os.path.join(ROOT, "examples/phantom-audit/assets/fonts")],
    "indaba": [],
    "orbit": [],
}

STYLE_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S)

ROLE_BY_NAME = {
    "index.html": "page",
    "styles.css": "stylesheet",
    "log.md": "build log (agent, 1:1 with audit.jsonl)",
    "audit.jsonl": "machine-recorded authority call trace",
    "brief.md": "build brief",
    "run-authority": "audited runner (build-time tool)",
    "archive-manifest.json": "this manifest",
    "MANIFEST.md": "human-readable manifest",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_css(build):
    """Inline <style> -> styles.css (idempotent). Returns True if rewritten."""
    page = os.path.join(build, "index.html")
    html = open(page).read()
    blocks = STYLE_RE.findall(html)
    if not blocks:
        return False
    css = "\n\n".join(b.strip() for b in blocks)
    header = ("/* styles.css - extracted verbatim from index.html by\n"
              "   tools/archive_authority_assets.py so the stylesheet is an\n"
              "   auditable artifact (see archive-manifest.json). */\n\n")
    open(os.path.join(build, "styles.css"), "w").write(header + css + "\n")
    # replace the first block with the link, drop the rest (same content)
    first = True
    def _sub(m):
        nonlocal first
        if first:
            first = False
            return '<link rel="stylesheet" href="styles.css">'
        return ""
    html = STYLE_RE.sub(_sub, html)
    open(page, "w").write(html)
    return True


def verify_fonts(auth, build):
    """Compare each local font file against its known source; return notes."""
    notes = {}
    fdir = os.path.join(build, "fonts")
    local = []
    for base, _, files in os.walk(build):
        for f in files:
            if f.lower().endswith((".woff2", ".ttf", ".otf")):
                local.append(os.path.join(base, f))
    for path in local:
        name = os.path.basename(path)
        src = None
        for cand in FONT_SOURCES.get(auth, []):
            p = os.path.join(cand, name)
            if os.path.isfile(p):
                src = p
                break
        if src is None:
            notes[os.path.relpath(path, build)] = {"source": None,
                                                   "match": None,
                                                   "note": "no known source for this file name"}
        else:
            notes[os.path.relpath(path, build)] = {
                "source": os.path.relpath(src, ROOT),
                "match": sha256(src) == sha256(path),
            }
    return notes


def archive(auth):
    build = os.path.join(SITES, auth)
    if not os.path.isfile(os.path.join(build, "index.html")):
        print("skip %s (no build)" % auth)
        return None
    rewrote = extract_css(build)
    pack_path = os.path.join(PACKS, auth, "authority.json")
    pack_version = ""
    if os.path.isfile(pack_path):
        pack_version = json.load(open(pack_path)).get("version", "")

    files = []
    for base, dirs, names in os.walk(build):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for name in sorted(names):
            if name in ("archive-manifest.json", "MANIFEST.md"):
                continue
            p = os.path.join(base, name)
            rel = os.path.relpath(p, build)
            role = ROLE_BY_NAME.get(name)
            if role is None:
                if name.lower().endswith((".woff2", ".ttf", ".otf")):
                    role = "brand font file"
                elif rel.startswith(".design-authority"):
                    role = "gap store (filed gaps)"
                else:
                    role = "asset"
            files.append({"path": rel, "sha256": sha256(p),
                          "size": os.path.getsize(p), "role": role})

    fonts = verify_fonts(auth, build)
    external = 0
    html = open(os.path.join(build, "index.html")).read()
    for m in re.finditer(r"https?://[A-Za-z0-9./-]+", html):
        if "w3.org" not in m.group(0):
            external += 1

    manifest = {
        "build": auth,
        "authority": {"pack": "packs/%s" % auth, "version": pack_version},
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "checks": {
            "external_references": external,
            "css_extracted": True if rewrote or os.path.isfile(os.path.join(build, "styles.css")) else False,
            "fonts_verified": fonts,
        },
        "files": files,
        "verify": "python3 tools/archive_authority_assets.py --verify %s" % auth,
    }
    with open(os.path.join(build, "archive-manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
        fh.write("\n")

    lines = ["# Archive manifest - %s" % auth, "",
             "Authority: `%s` @ %s - generated %s UTC"
             % (manifest["authority"]["pack"], pack_version,
                manifest["generated_at"]),
             "",
             "| file | role | sha256 (first 16) | size |",
             "|---|---|---|---|"]
    for f in files:
        lines.append("| `%s` | %s | `%s` | %d |" % (f["path"], f["role"], f["sha256"][:16], f["size"]))
    lines += ["", "External references: %d (must be 0)." % external, ""]
    for path, note in fonts.items():
        if note.get("source"):
            lines.append("- `%s`: byte-identical to `%s` -> %s"
                         % (path, note["source"], note["match"]))
        else:
            lines.append("- `%s`: %s" % (path, note.get("note")))
    lines += ["", "Verify: `%s`" % manifest["verify"], ""]
    open(os.path.join(build, "MANIFEST.md"), "w").write("\n".join(lines))
    print("archived %s: %d files, fonts %d" % (auth, len(files), len(fonts)))
    return manifest


def verify(auth):
    """Recompute and compare every hash in the manifest."""
    build = os.path.join(SITES, auth)
    mp = os.path.join(build, "archive-manifest.json")
    if not os.path.isfile(mp):
        print("no manifest for %s" % auth)
        return False
    manifest = json.load(open(mp))
    bad = []
    for f in manifest["files"]:
        p = os.path.join(build, f["path"])
        if not os.path.isfile(p) or sha256(p) != f["sha256"]:
            bad.append(f["path"])
    regen = extract_css(build)
    print("%s: %d files, %d mismatches%s" % (auth, len(manifest["files"]), len(bad),
                                             " (css re-extracted)" if regen else ""))
    for b in bad:
        print("  MISMATCH:", b)
    return not bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth", nargs="*", default=None)
    ap.add_argument("--verify", nargs="*", default=None)
    args = ap.parse_args()
    if args.verify:
        ok = True
        for a in args.verify:
            ok = verify(a) and ok
        sys.exit(0 if ok else 1)
    auths = args.auth or [d for d in sorted(os.listdir(SITES))
                          if os.path.isfile(os.path.join(SITES, d, "index.html"))]
    for a in auths:
        archive(a)


if __name__ == "__main__":
    main()
