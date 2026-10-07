#!/usr/bin/env python3
"""Generic style-tile renderer for synthesis sources.

Usage:
  .venv/bin/python3 docs/synthesis/tools/render_tile.py \
      --dir docs/synthesis/wink/tile [--expect-font "Means Web"] [--width 1280]

Renders tile.html (full page) to <dir>/out/style-tile.png.
--expect-font is a font-fidelity gate (lesson from the G1 review): if the
named family fails to load, the render aborts rather than shipping a
silently-substituted tile. Omit it only when a substitute is a conscious,
recorded decision.
"""
import argparse
import os

from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--dir", required=True, help="folder containing tile.html")
ap.add_argument("--expect-font", default=None)
ap.add_argument("--width", type=int, default=1280)
ap.add_argument("--out", default=None)
args = ap.parse_args()

BASE = os.path.abspath(args.dir)
OUT = args.out or os.path.join(BASE, "out")
os.makedirs(OUT, exist_ok=True)
URL = "file://" + os.path.join(BASE, "tile.html")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": args.width, "height": 1000})
    pg.goto(URL, wait_until="load")
    pg.evaluate("document.fonts.ready")
    if args.expect_font:
        ok = pg.evaluate("document.fonts.check('16px %s')" % args.expect_font)
        print("font check (%s):" % args.expect_font, ok)
        assert ok, "expected font failed to load - aborting render"
    out = os.path.join(OUT, "style-tile.png")
    pg.screenshot(path=out, full_page=True)
    print("rendered", out)
    b.close()
