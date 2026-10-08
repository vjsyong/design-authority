#!/usr/bin/env python3
"""Traceability gate for the generated artefacts-directory CSS block.

The generated chrome (chips, labels, panels, controls) must not introduce any
value that the authority does not already carry. This tool extracts every
colour, radius and font declaration from the generated block
(/* artefacts-directory:start */ ... :end */) in each build's styles.css and
asserts each one is traceable to either:

  - the page's own stylesheet outside the block (the built, audited language),
  - the pack's own JSON text (recorded values), or
  - a trivial CSS keyword (transparent, inherit, none, 0...).

Fonts: only `inherit` is allowed (no register the authority does not record),
except for builds whose page defines native code styling, where the block
declares no font at all.

    python3 tools/check_artefacts_css.py [--auth NAME ...]     # exit 1 on violations
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES = os.path.join(ROOT, "authorities")
PACKS = os.path.join(ROOT, "authorities")

MARK_S = "/* artefacts-directory:start */"
MARK_E = "/* artefacts-directory:end */"
TRIVIAL = {"transparent", "inherit", "none", "currentcolor", "0", "0px", "auto", "100%"}

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGBA = re.compile(r"rgba?\(\s*[0-9]+(?:\s*,\s*[0-9.]+){2,3}\s*\)")
RADIUS = re.compile(r"border-radius:\s*([^;}]+)")
FONT = re.compile(r"font-family:\s*([^;}]+)")


def expand_hex(m):
    h = m.group(1)
    if len(h) == 3:
        return "#" + "".join(c * 2 for c in h)
    return "#" + h


def rgb_to_hex(m):
    r, g, b = (int(m.group(i)) for i in (1, 2, 3))
    for v in (r, g, b):
        if v > 255:
            return m.group(0)
    return "#%02x%02x%02x" % (r, g, b)


def norm(s):
    s = re.sub(r"\s+", "", s).lower()
    s = re.sub(r"#([0-9a-f]{3})\b", expand_hex, s)
    s = re.sub(r"rgb\((\d+),(\d+),(\d+)\)", rgb_to_hex, s)
    return s


def pack_text_dir(packdir):
    parts = []
    for f in sorted(os.listdir(packdir)):
        if f.endswith(".json"):
            parts.append(open(os.path.join(packdir, f)).read())
    return norm("".join(parts))


def check(auth):
    build = os.path.join(SITES, auth, "site") if os.path.isdir(os.path.join(SITES, auth, "site")) else os.path.join(SITES, auth)
    return check_dir(build, os.path.join(PACKS, auth), auth)


def check_dir(build, packdir, label):
    css_p = os.path.join(build, "styles.css")
    if not os.path.isfile(css_p):
        print("%s: no styles.css" % label)
        return []
    css = open(css_p).read()
    i, j = css.find(MARK_S), css.find(MARK_E)
    if i < 0 or j < 0:
        print("%s: no generated block found" % label)
        return []
    block = css[i:j + len(MARK_E)]
    page_css = norm(css[:i] + css[j + len(MARK_E):])
    pack = pack_text_dir(packdir)

    violations = []
    values = set(HEX.findall(block))
    values |= set(m.group(0) for m in RGBA.finditer(block))
    for v in sorted(values):
        n = norm(v)
        if n in TRIVIAL:
            continue
        if n in page_css or n in pack:
            continue
        violations.append("colour %s (not in page CSS or pack)" % v)

    for m in RADIUS.finditer(block):
        for part in m.group(1).split():
            n = norm(part)
            if n in TRIVIAL:
                continue
            if n in page_css or n in pack:
                continue
            violations.append("radius %s (not in page CSS or pack)" % part)

    for m in FONT.finditer(block):
        if norm(m.group(1)) != "inherit":
            violations.append("font-family %s (only inherit is allowed)" % m.group(1).strip())

    if violations:
        print("%s: %d violation(s)" % (label, len(violations)))
        for v in violations:
            print("   -", v)
    else:
        print("%s: clean (%d colour values checked)" % (label, len(values)))
    return violations


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth", nargs="*", default=None)
    ap.add_argument("--build", default=None,
                    help="explicit site build dir (used from an authority repo checkout)")
    ap.add_argument("--pack", default=None,
                    help="explicit pack dir (with --build)")
    args = ap.parse_args()
    if args.build and args.pack:
        v = check_dir(args.build, args.pack, os.path.basename(os.path.abspath(args.build)))
        sys.exit(1 if v else 0)
    auths = args.auth or [d for d in sorted(os.listdir(SITES))
                          if os.path.isfile(os.path.join(SITES, d, "site", "index.html"))]
    bad = 0
    for a in auths:
        bad += len(check(a))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
