#!/usr/bin/env python3
"""Screenshots for the Depot reference app (desktop set + mobile register)."""
import argparse
import os

from playwright.sync_api import sync_playwright

PAGES = [("register", "/items"), ("form", "/items/new"),
         ("detail", "/items/3"), ("activity", "/activity")]


def capture(url, out):
    os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page(viewport={"width": 1440, "height": 900})
        for name, path in PAGES:
            pg.goto(url + path, wait_until="load")
            pg.screenshot(path=os.path.join(out, "%s.png" % name), full_page=True)
        m = browser.new_page(viewport={"width": 380, "height": 820})
        m.goto(url + "/items", wait_until="load")
        m.screenshot(path=os.path.join(out, "register-mobile.png"), full_page=True)
        browser.close()
    print("captured to", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    capture(args.url, args.out)
