#!/usr/bin/env python3
"""Headless render + functional probe + deliverable screenshot for hacked-dominion."""
import os, subprocess, sys, time, socket

REPO = "/home/xrim/design-authority"
TARGET = os.path.join(REPO, "docs/verification/adversarial/hacked-dominion")
SHOT = os.path.join(TARGET, "_evidence/screens/adversarial-dominion.png")

s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
proc = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", TARGET],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
from playwright.sync_api import sync_playwright
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        page.goto(f"http://127.0.0.1:{port}/index.html", wait_until="load")
        page.wait_for_timeout(500)
        # render sanity
        print("title:", page.title())
        print("b-slate bgImage:", page.eval_on_selector(".b-slate", "el => getComputedStyle(el).backgroundImage")[:80])
        print("b-slate bgColor:", page.eval_on_selector(".b-slate", "el => getComputedStyle(el).backgroundColor"))
        print("initials radius/bg:", page.eval_on_selector(".initials", "el => [getComputedStyle(el).borderRadius, getComputedStyle(el).backgroundColor]"))
        print("tile shadow:", page.eval_on_selector(".tile", "el => getComputedStyle(el).boxShadow"))
        print("fr title textContent len:", page.eval_on_selector("#view-today h1 .fr", "el => el.textContent.length"))
        os.makedirs(os.path.dirname(SHOT), exist_ok=True)
        page.screenshot(path=SHOT)
        print("screenshot:", SHOT)
        # functional probe: detail -> red chip
        page.click('#ritual-list li[data-rit="r3"] .r-details')
        page.wait_for_timeout(200)
        print("detail visible:", page.is_visible("#ritual-detail"))
        print("detail chip:", page.eval_on_selector("#ritual-detail .st.alert", "el => [el.textContent, getComputedStyle(el).color]"))
        # export -> floating chip
        page.click("a[data-view='settings']")
        page.click("#export-csv")
        page.wait_for_timeout(200)
        print("export chip:", page.eval_on_selector("#export-chip", "el => [getComputedStyle(el).position, el.textContent.trim()]"))
        # search focus ring
        page.click("a[data-view='history']")
        page.eval_on_selector("#ledger-search", "el => el.focus()")
        page.wait_for_timeout(150)
        print("search focus outline:", page.eval_on_selector("#ledger-search", "el => [getComputedStyle(el).outlineColor, getComputedStyle(el).outlineWidth]"))
        # save meter red (open log editor + save)
        page.click("a[data-view='today']")
        page.click('#ritual-list li[data-rit="r1"] .r-log')
        page.click("#log-save")
        page.wait_for_timeout(600)
        print("save fill:", page.eval_on_selector("#save-fill", "el => [getComputedStyle(el).backgroundColor, el.style.width]"))
        print("console/page errors:", errs)
        b.close()
finally:
    proc.terminate()
print("DONE")
