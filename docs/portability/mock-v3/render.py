#!/usr/bin/env python3
"""Render the Indaba (Depot) screens to PNGs — element shots + mobile."""
import os

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
URL = "file://" + os.path.join(HERE, "indaba-mock.html")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 1000})
    pg.goto(URL, wait_until="load")
    pg.evaluate("document.fonts.ready")
    # font-fidelity gate (lesson from G1): real Ubuntu, not a substitute
    checks = {
        "ubuntu-regular": pg.evaluate("document.fonts.check('16px Ubuntu')"),
        "ubuntu-light-300": pg.evaluate("document.fonts.check('300 28px Ubuntu')"),
    }
    print("font checks:", checks)
    assert all(checks.values()), "Ubuntu font failed to load — aborting render"

    for sid, name in [("s1", "1-register"), ("s2", "2-detail"),
                      ("s3", "3-form"), ("s4", "4-activity"), ("s5", "5-dialog")]:
        pg.locator("#" + sid).screenshot(path=os.path.join(OUT, name + ".png"))
        print("rendered", name)
    pg.close()

    m = b.new_page(viewport={"width": 390, "height": 900})
    m.goto(URL, wait_until="load")
    m.evaluate("document.fonts.ready")
    m.locator("#s1").screenshot(path=os.path.join(OUT, "1-register-mobile.png"))
    print("rendered 1-register-mobile")
    b.close()

print("out:", OUT)
