#!/usr/bin/env python3
"""Render Orbit v2 mock screens to PNGs (desktop + mobile register)."""
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
MOCK = os.path.join(HERE, "orbit-v2-mock.html")
OUT = os.path.join(HERE, "out")

os.makedirs(OUT, exist_ok=True)
url = "file://" + MOCK

with sync_playwright() as p:
    browser = p.chromium.launch()
    pg = browser.new_page(viewport={"width": 1440, "height": 1000})
    pg.goto(url, wait_until="load")
    for sid, name in [("s1", "1-register"), ("s2", "2-detail"),
                      ("s3", "3-form"), ("s4", "4-activity"), ("s5", "5-dialog")]:
        el = pg.locator("#" + sid)
        el.screenshot(path=os.path.join(OUT, name + ".png"))
        print("rendered", name)
    pg.close()

    m = browser.new_page(viewport={"width": 380, "height": 900})
    m.goto(url, wait_until="load")
    m.locator("#s1").screenshot(path=os.path.join(OUT, "1-register-mobile.png"))
    print("rendered 1-register-mobile")
    browser.close()

print("out:", OUT)
sys.exit(0)
