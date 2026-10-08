#!/usr/bin/env python3
"""lens_check — verify the v3.1d verification surface in the wink lens."""
import json
import os
import subprocess
import sys
import socket
import time

from playwright.sync_api import sync_playwright

REPO = "/home/xrim/design-authority"
T = os.path.join(REPO, "examples", "cadence3-wink")
s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
proc = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1",
                         "--directory", T], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.7)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(viewport={"width": 1440, "height": 950}).new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"http://127.0.0.1:{port}/index.html", wait_until="load")
    pg.wait_for_timeout(250)
    pg.evaluate("localStorage.clear()")
    pg.reload(wait_until="load")
    pg.wait_for_timeout(350)
    pg.evaluate("""(() => { const d = document.querySelector('dialog[open]');
        if (!d) return; const sk = d.querySelector('#wizSkip'); if (sk) sk.click(); else d.close(); })()""")
    pg.wait_for_timeout(200)
    # marks on, then click the status chip (#17)
    pg.click("#marksToggle")
    pg.wait_for_timeout(200)
    pg.click('.status[data-decision="17"]')
    pg.wait_for_timeout(800)
    assert not pg.evaluate("document.getElementById('provPanel').hidden"), "panel did not open"
    txt = pg.inner_text("#provBody").lower()
    checks = {
        "has verification section": "independent verification" in txt,
        "shows build totals": "verified" in txt and "no violations" in txt,
        "shows check row": "status conveys meaning" in txt,
        "shows PASS": "pass" in txt,
        "keeps claim separate": "the label says" in txt,
    }
    for k, v in checks.items():
        print(("OK  " if v else "FAIL") + " " + k)
    print("pageerrors:", errs[:3] if errs else "none")
    # evidence link present?
    foot = pg.inner_text("#provFoot")
    print("footer has verification JSON link:", "verification JSON" in foot)
    os.makedirs(os.path.join(T, "_evidence", "screens"), exist_ok=True)
    shot = os.path.join(T, "_evidence", "screens", "v31d-verification-lens.png")
    pg.screenshot(path=shot)
    print("screenshot:", shot)
    b.close()
proc.terminate()
