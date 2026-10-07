#!/usr/bin/env python3
"""Render the Indaba style tile to PNG."""
import os

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 1400}, device_scale_factor=1)
    pg.goto("file://" + os.path.join(HERE, "tile.html"), wait_until="load")
    pg.wait_for_timeout(400)  # let fonts settle
    pg.screenshot(path=os.path.join(OUT, "style-tile.png"), full_page=True)
    print("rendered", os.path.join(OUT, "style-tile.png"))
    b.close()
