#!/usr/bin/env python3
"""Smoke-load the mutated builds: must still load, run, and render the app."""
import os
import subprocess
import sys
import socket
import time

from playwright.sync_api import sync_playwright

REPO = "/home/xrim/design-authority"
for name in ("mutated-wink", "mutated-leader", "mutated-dominion"):
    target = os.path.join(REPO, "docs", "verification", "mutations", name)
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    proc = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1",
                             "--directory", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.6)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(f"http://127.0.0.1:{port}/index.html", wait_until="load")
        pg.wait_for_timeout(500)
        n_views = pg.evaluate("document.querySelectorAll('.view').length")
        n_btns = pg.evaluate("document.querySelectorAll('.cta, .btn').length")
        print(f"{name}: loaded | views {n_views} | buttons {n_btns} | pageerrors {errs[:2] if errs else 'none'}")
        b.close()
    proc.terminate()
