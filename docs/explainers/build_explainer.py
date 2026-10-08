#!/usr/bin/env python3
"""build_explainer — render docs/explainers/design-authority.html to a PNG poster.

Serves the repo root (so the vendored fonts resolve), screenshots with Chromium
at deviceScaleFactor=2, full page.
"""
import os
import socket
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

REPO = "/home/xrim/design-authority"
TARGETS = [("docs/explainers/design-authority.html", "docs/explainers/design-authority.png"),
           ("docs/explainers/design-authority-hero.html", "docs/explainers/design-authority-hero.png")]

s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
proc = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", REPO],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.7)
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_context(viewport={"width": 1240, "height": 900}, device_scale_factor=2).new_page()
        for src, out in TARGETS:
            pg.goto(f"http://127.0.0.1:{port}/{src}", wait_until="load")
            pg.wait_for_timeout(900)
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(REPO, out), full_page=True)
            h = pg.evaluate("document.body.scrollHeight")
            print(f"rendered {src} -> {out} (logical {h}px tall, @2x)")
        b.close()
finally:
    proc.terminate()
