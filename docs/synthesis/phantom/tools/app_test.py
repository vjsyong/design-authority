#!/usr/bin/env python3
"""phantom-audit selftest (v2) — the app must WEAR the deployed language it reviews:
pink reading ink, green links on dotted blue, blue code ground, lime menu, red
checks, the override toggle, the evidence gallery. Plus the console machinery."""
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
    pg.wait_for_timeout(800)

    check("no page errors", not errs)
    check("preload removed", pg.evaluate("!document.body.classList.contains('is-preload')"))
    check("29 system cards", pg.evaluate("document.querySelectorAll('#systemCards > li').length") == 29)
    check("36 gap rows", pg.evaluate("document.querySelectorAll('#gapRows tr').length") == 36)
    check("gaps stat shows 36", pg.inner_text("#statGaps") == "36")
    check("6 adaptations", pg.evaluate("document.querySelectorAll('#adaptList .adapt').length") == 6)
    check("AA rows rendered", pg.evaluate("document.querySelectorAll('.aa').length") >= 6)
    check("fonts loaded (300 body)", pg.evaluate("document.fonts.check('300 16px \"Source Sans Pro\"')"))

    # explainer accordion
    check("explainer starts collapsed", pg.evaluate("!document.querySelector('details.explainer').open"))
    pg.click("details.explainer > summary")
    pg.wait_for_timeout(150)
    exp_txt = pg.evaluate("document.querySelector('details.explainer').innerText")
    check("explainer expands with content", pg.evaluate("document.querySelector('details.explainer').open") and "machine-readable" in exp_txt and "Extraction" in exp_txt)
    check("explainer poster embedded", pg.evaluate("!!document.querySelector('details.explainer img') && document.querySelector('details.explainer img').getAttribute('src').indexOf('design-authority.png') > -1"))
    pg.screenshot(path=os.path.join(T, "_evidence", "screens", "audit2-explainer.png"))
    pg.click("details.explainer > summary")
    pg.wait_for_timeout(80)
    check("explainer collapses back", pg.evaluate("!document.querySelector('details.explainer').open"))

    # --- the deployed language, as rendered by the app itself ---
    check("body ink is pink #ff6bbc", pg.evaluate("getComputedStyle(document.querySelector('#overview p')).color") == "rgb(255, 107, 188)")
    check("h1 is pink", pg.evaluate("getComputedStyle(document.querySelector('h1')).color") == "rgb(255, 107, 188)")
    lk = pg.evaluate("""(() => { const cs = getComputedStyle(document.querySelector('#overview p a'));
        return cs.color + '|' + cs.borderBottomStyle + '|' + cs.borderBottomColor; })()""")
    check("links green + dotted blue underline", lk == "rgb(107, 255, 44)|dotted|rgb(32, 163, 245)")
    check("code ground is blue", pg.evaluate("getComputedStyle(document.querySelector('p code')).backgroundColor") in ("rgba(46, 90, 249, 0.984)", "rgba(46, 90, 249, 0.986)"))
    check("menu ground is lime", pg.evaluate("getComputedStyle(document.querySelector('#menu')).backgroundColor") == "rgb(62, 249, 0)")
    cbf = pg.evaluate("""(() => { const l = document.querySelector('label[for="demo-cb"]');
        return getComputedStyle(l, '::before').backgroundColor; })()""")
    check("checked box fills red", cbf == "rgb(245, 22, 22)")
    lbf = pg.evaluate("getComputedStyle(document.querySelector('label[for=\"demo-cb\"]')).color")
    check("control label is purple", lbf == "rgb(136, 51, 227)")

    # evidence gallery (scroll in first — images are lazy)
    n_img = pg.evaluate("document.querySelectorAll('#evGrid img').length")
    pg.evaluate("document.querySelector('#evidence').scrollIntoView()")
    pg.wait_for_timeout(1200)
    broken = pg.evaluate("[...document.querySelectorAll('#evGrid img')].filter(i => !i.complete || i.naturalWidth === 0).length")
    check("14 evidence images, none broken", n_img == 14 and broken == 0)
    pg.evaluate("window.scrollTo(0,0)")
    pg.wait_for_timeout(150)

    # override toggle (the deployed black-body override)
    pg.click("#overrideToggle")
    pg.wait_for_timeout(120)
    bc = pg.evaluate("getComputedStyle(document.body).color")
    bb = pg.evaluate("getComputedStyle(document.body).backgroundColor")
    check("override: black text on #fbfbfb", bc == "rgb(0, 0, 0)" and bb == "rgb(251, 251, 251)")
    pg.screenshot(path=os.path.join(T, "_evidence", "screens", "audit2-override.png"))
    pg.click("#overrideToggle")
    pg.wait_for_timeout(80)
    check("override toggles back", pg.evaluate("getComputedStyle(document.body).color") == "rgb(255, 107, 188)")

    # filter
    pg.click("#gapFilters [data-f='craft']")
    check("craft filter -> 10 rows", pg.evaluate("document.querySelectorAll('#gapRows tr').length") == 10)
    pg.click("#gapFilters [data-f='all']")

    # gap row -> panel
    pg.click("#gapRows tr:first-child")
    pg.wait_for_timeout(150)
    check("panel opens on gap", pg.evaluate("!document.getElementById('panel').hidden"))
    check("panel shows G01", "G01" in pg.inner_text("#panelId"))
    check("panel crosslinks present", pg.evaluate("!!document.querySelector('#panelBody [data-open]')"))
    pg.click("#panelClose")

    # artifact card -> panel
    pg.click("#systemCards li:nth-child(1) .card-inner h3")
    pg.wait_for_timeout(150)
    check("panel opens on artifact", "token-set/colour" in pg.inner_text("#panelId"))
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
    check("marks layer shows > 40 marked nodes", n_marks > 40)
    pg.screenshot(path=os.path.join(T, "_evidence", "screens", "audit2-marks.png"))
    pg.click("#marksToggle")

    # carousel + replay
    pg.evaluate("document.querySelector('#AD3').scrollIntoView()")
    pg.wait_for_timeout(200)
    pg.click("#carNext")
    check("carousel advances", "2 / 3" in pg.inner_text("#carPos"))
    pg.click("#carPrev"); pg.click("#carPrev")
    check("carousel wraps", "3 / 3" in pg.inner_text("#carPos"))
    pg.click("#demoReplay")
    pg.wait_for_timeout(300)
    check("no errors after replay", not errs)

    # screenshots
    pg.evaluate("window.scrollTo(0,0)")
    pg.wait_for_timeout(250)
    pg.screenshot(path=os.path.join(T, "_evidence", "screens", "audit2-top.png"))
    pg.evaluate("document.querySelector('#gaps').scrollIntoView()")
    pg.wait_for_timeout(200)
    pg.screenshot(path=os.path.join(T, "_evidence", "screens", "audit2-gaps.png"))
    pg.evaluate("document.querySelector('#evidence').scrollIntoView()")
    pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(T, "_evidence", "screens", "audit2-evidence.png"))
    b.close()

print(f"\n{ok}/{ok+fail} passed" + (f" · errors: {errs[:3]}" if errs else ""))
proc.terminate()
