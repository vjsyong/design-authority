#!/usr/bin/env python3
"""Capture screenshots + DOM probes for a running benchmark app (Playwright).

    python3 capture.py --url http://127.0.0.1:8107 --out DIR

Writes DIR/capture.json + DIR/screens/<route>-<viewport>.png.
"""
import argparse
import json
import os
import sys

from playwright.sync_api import sync_playwright

ROUTES = [
    ("dashboard", "/"),
    ("dashboard-empty", "/?empty=1"),
    ("dashboard-error", "/?error=1"),
    ("dashboard-job-running", "/?job=running"),
    ("requests", "/requests"),
    ("requests-filtered", "/requests?status=pending&category=Software"),
    ("requests-page2", "/requests?page=2"),
    ("requests-empty", "/requests?empty=1"),
    ("request-detail", "/requests/2"),
    ("jobs", "/jobs"),
    ("jobs-running", "/jobs?job=running"),
    ("settings", "/settings"),
]
VIEWPORTS = [("desktop", {"width": 1440, "height": 900}, False),
             ("phone", {"width": 390, "height": 844}, True)]

PROBE_JS = r"""() => {
  const out = {bg:{}, fg:{}, radius:{}, fonts:{}, padding:{}, gap:{}, inline:0,
               buttons:0, links:0, inputs:0, tables:0, forms:0, elements:0,
               classes:{}};
  const bump = (o,k) => { if(k && k !== 'none' && k !== 'auto' && k !== '0px' && k !== 'normal') o[k]=(o[k]||0)+1; };
  for (const el of document.querySelectorAll('*')) {
    out.elements++;
    const cs = getComputedStyle(el);
    if (cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)') bump(out.bg, cs.backgroundColor);
    bump(out.fg, cs.color);
    bump(out.radius, [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomLeftRadius, cs.borderBottomRightRadius].join(' '));
    bump(out.fonts, cs.fontFamily);
    bump(out.padding, [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].join(' '));
    bump(out.gap, cs.gap);
    if (el.getAttribute('style')) out.inline++;
    const tag = el.tagName.toLowerCase();
    if (tag === 'button') out.buttons++;
    if (tag === 'a') out.links++;
    if (tag === 'input' || tag === 'select' || tag === 'textarea') out.inputs++;
    if (tag === 'table') out.tables++;
    if (tag === 'form') out.forms++;
    const cls = el.getAttribute('class');
    if (cls) for (const c of cls.split(/\s+/)) if (c) bump(out.classes, c);
  }
  const top = o => Object.entries(o).sort((a,b)=>b[1]-a[1]).slice(0,60);
  for (const k of ['bg','fg','radius','fonts','padding','gap','classes']) out[k] = top(out[k]);
  return out;
}"""


def capture(url, out):
    os.makedirs(os.path.join(out, "screens"), exist_ok=True)
    result = {"url": url, "routes": {}, "errors": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for vp_name, viewport, mobile in VIEWPORTS:
            ctx = browser.new_context(viewport=viewport, is_mobile=mobile,
                                      has_touch=mobile, device_scale_factor=1)
            page = ctx.new_page()
            console_errors = []
            page.on("pageerror", lambda e, ce=console_errors: ce.append(str(e)[:300]))
            page.on("console", lambda m, ce=console_errors: (
                ce.append(m.text[:300]) if m.type == "error" else None))
            for route_name, path in ROUTES:
                entry = result["routes"].setdefault(route_name, {})
                errs_before = len(console_errors)
                try:
                    page.goto(url + path, wait_until="load", timeout=15000)
                    page.wait_for_timeout(600)
                    shot = os.path.join(out, "screens",
                                        "%s-%s.png" % (route_name, vp_name))
                    page.screenshot(path=shot, full_page=True)
                    entry[vp_name] = {"shot": os.path.relpath(shot, out),
                                      "title": page.title()[:120],
                                      "text_len": len(page.inner_text("body")[:5000])
                                      if page.query_selector("body") else 0}
                    if vp_name == "desktop":
                        entry["probe"] = page.evaluate(PROBE_JS)
                except Exception as exc:
                    entry[vp_name] = {"error": str(exc)[:300]}
                entry.setdefault("console_errors", [])
                entry["console_errors"] += console_errors[errs_before:]
            ctx.close()
        browser.close()
    with open(os.path.join(out, "capture.json"), "w") as fh:
        json.dump(result, fh, indent=1)
    n_err = sum(len(e.get("console_errors", [])) for e in result["routes"].values())
    print("capture: %d routes x %d viewports, %d console errors"
          % (len(ROUTES), len(VIEWPORTS), n_err))
    return result


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    capture(args.url, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
