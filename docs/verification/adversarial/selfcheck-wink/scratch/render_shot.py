#!/usr/bin/env python3
"""Scratch: headless render of the adversarial wink copy + deliverable screenshot.

Part 1: functional sanity (app renders, delete dialog opens, panel readout).
Part 2: screenshot choreography — a log action (toast pill) + marks layer on +
        provenance panel open on a marked node (independent-verification readout).
"""
import os, socket, subprocess, sys, time, urllib.request

REPO = "/home/xrim/design-authority"
COPY = os.path.join(REPO, "docs/verification/adversarial/hacked-wink")
OUT = os.path.join(COPY, "_evidence/screens/adversarial-wink.png")

s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
proc = subprocess.Popen(
    [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", COPY],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
url = f"http://127.0.0.1:{port}/index.html"
for _ in range(60):
    try:
        urllib.request.urlopen(url, timeout=1); break
    except Exception:
        time.sleep(0.1)

errors = []
from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(url, wait_until="load"); page.wait_for_timeout(400)
        page.evaluate("localStorage.clear()")
        page.reload(wait_until="load"); page.wait_for_timeout(400)
        page.evaluate("(() => { const d = document.querySelector('dialog[open]'); if (d) { const sk = d.querySelector('#wizSkip'); if (sk) sk.click(); else d.close(); } })()")
        page.wait_for_timeout(300)
        if page.evaluate("!!document.querySelector('dialog[open]')"):
            page.keyboard.press("Escape"); page.wait_for_timeout(150)

        # ---- Part 1: functional sanity ----
        print("render: cards =", page.evaluate("document.querySelectorAll('#ritualList .ritual-card').length"),
              "| ticks =", page.evaluate("document.querySelectorAll('.log-tick').length"),
              "| views =", page.evaluate("document.querySelectorAll('.view').length"))

        page.click("#marksToggle"); page.wait_for_timeout(200)
        print("marks on:", page.evaluate("document.body.classList.contains('marks-on')"))
        page.click("#weekBanner"); page.wait_for_timeout(700)
        panel = page.evaluate("document.getElementById('provBody').innerText")
        print("PANEL READOUT:", " | ".join(panel.splitlines()[:14]))
        print("panel says 'no violations':", "no violations" in panel)
        print("readout line:", [l for l in panel.splitlines() if "verified" in l])
        page.click("#provClose"); page.wait_for_timeout(150)
        page.click("#marksToggle"); page.wait_for_timeout(200)   # marks off again

        # delete-dialog behaviour (destructive default focus)
        page.click(".delete-btn"); page.wait_for_timeout(400)
        print("delete dialog open:", page.evaluate("!!document.querySelector('dialog[open]')"),
              "| activeElement:", page.evaluate("(document.activeElement && (document.activeElement.id || document.activeElement.tagName)) + ''"))
        page.evaluate("document.querySelectorAll('dialog[open]').forEach(d => d.close())")
        page.wait_for_timeout(200)

        # ---- Part 2: screenshot choreography (toast + lens) ----
        page.click(".log-tick[aria-pressed='false']")          # toast fires ~+320ms
        page.wait_for_timeout(120)
        page.click("#marksToggle")                              # marks on
        page.wait_for_timeout(120)
        page.click("#weekBanner")                               # open lens on marked node
        page.wait_for_timeout(900)
        toast = page.evaluate("(() => { const t = document.querySelector('.toast-float'); return t ? { text: t.textContent, position: getComputedStyle(t).position, opacity: getComputedStyle(t).opacity } : null; })()")
        print("toast in shot:", toast)
        lens = page.evaluate("document.getElementById('provBody').innerText")
        print("lens in shot mentions 'no violations':", "no violations" in lens)

        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        page.screenshot(path=OUT, full_page=False)
        print("shot written:", OUT, os.path.getsize(OUT), "bytes")
        b.close()
finally:
    proc.terminate()

print("page errors:", errors if errors else "none")
