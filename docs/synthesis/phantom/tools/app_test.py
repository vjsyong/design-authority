#!/usr/bin/env python3
"""phantom-audit selftest: load + interactions + screenshot."""
import os
import subprocess
import sys
import socket
import time

from playwright.sync_api import sync_playwright

REPO = "/home/xrim/design-authority"
T = os.path.join(REPO, "examples", "phantom-audit")
s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
proc = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", T],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.7)
ok = fail = 0
def check(name, cond):
    global ok, fail
    ok += cond; fail += not cond
    print(("OK  " if cond else "FAIL") + " " + name)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"http://127.0.0.1:{port}/index.html", wait_until="load")
    pg.wait_for_timeout(700)

    check("no page errors", not errs)
    check("preload removed", pg.evaluate("!document.body.classList.contains('is-preload')"))
    check("19 system cards", pg.evaluate("document.querySelectorAll('#systemCards > li').length") == 19)
    check("27 gap rows", pg.evaluate("document.querySelectorAll('#gapRows tr').length") == 27)
    check("6 adaptations", pg.evaluate("document.querySelectorAll('#adaptList .adapt').length") == 6)
    check("AA rows rendered", pg.evaluate("document.querySelectorAll('.aa').length") >= 5)
    check("fonts loaded (300 body)", pg.evaluate("document.fonts.check('300 16px \"Source Sans Pro\"')"))

    # filter
    pg.click("#gapFilters [data-f='craft']")
    n = pg.evaluate("document.querySelectorAll('#gapRows tr').length")
    check("craft filter -> 8 rows", n == 8)
    pg.click("#gapFilters [data-f='all']")

    # gap row -> panel
    pg.click("#gapRows tr:first-child")
    pg.wait_for_timeout(150)
    check("panel opens on gap", pg.evaluate("!document.getElementById('panel').hidden"))
    check("panel shows G01", "G01" in pg.inner_text("#panelId"))
    check("panel body has evidence", "css-diff" in pg.inner_text("#panelBody"))

    # crosslink inside panel (precedent chip)
    has_link = pg.evaluate("!!document.querySelector('#panelBody [data-open]')")
    check("panel crosslinks present", has_link)
    pg.click("#panelClose")

    # artifact card -> panel
    pg.click("#systemCards li:nth-child(3) .card-inner h3")
    pg.wait_for_timeout(150)
    check("panel opens on artifact", "action-button" in pg.inner_text("#panelId"))
    check("demo present in panel", pg.evaluate("!!document.querySelector('#panelBody .button.primary')"))
    pg.click("#panelClose")

    # menu
    pg.click('a[href="#menu"]')
    pg.wait_for_timeout(150)
    check("menu opens", pg.evaluate("document.body.classList.contains('is-menu-visible')"))
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(100)
    check("menu closes on Esc", not pg.evaluate("document.body.classList.contains('is-menu-visible')"))

    # marks
    pg.click("#marksToggle")
    pg.wait_for_timeout(120)
    n_marks = pg.evaluate("document.querySelectorAll('body.marks-on [data-improvised]').length")
    check("marks layer shows > 30 marked nodes", n_marks > 30)
    os.makedirs(os.path.join(T, "_evidence", "screens"), exist_ok=True)
    pg.screenshot(path=os.path.join(T, "_evidence", "screens", "audit-marks.png"))
    pg.click("#marksToggle")

    # carousel
    pg.evaluate("document.querySelector('#AD3').scrollIntoView()")
    pg.wait_for_timeout(200)
    pg.click("#carNext")
    check("carousel advances", "2 / 3" in pg.inner_text("#carPos"))
    pg.click("#carPrev"); pg.click("#carPrev")
    check("carousel wraps", "3 / 3" in pg.inner_text("#carPos"))

    # replay intro
    pg.click("#demoReplay")
    pg.wait_for_timeout(300)
    check("no errors after replay", not errs)

    os.makedirs(os.path.join(T, "_evidence", "screens"), exist_ok=True)
    pg.evaluate("window.scrollTo(0,0)")
    pg.wait_for_timeout(250)
    pg.screenshot(path=os.path.join(T, "_evidence", "screens", "audit-top.png"))
    pg.evaluate("document.querySelector('#gaps').scrollIntoView()")
    pg.wait_for_timeout(200)
    pg.screenshot(path=os.path.join(T, "_evidence", "screens", "audit-gaps.png"))
    pg.evaluate("document.querySelector('#adaptations').scrollIntoView()")
    pg.wait_for_timeout(200)
    pg.screenshot(path=os.path.join(T, "_evidence", "screens", "audit-adaptations.png"))
    b.close()

print(f"\n{ok}/{ok+fail} passed" + (f" · errors: {errs[:3]}" if errs else ""))
proc.terminate()
