#!/usr/bin/env python3
"""Functional + tolerant UI checks against a running Procura app.

    python3 interact.py --url http://127.0.0.1:8107 --out DIR

HTTP checks exercise the frozen routes through the agent's rendered forms
(approve / reject / bulk / assign / settings / jobs). One tolerant UI probe
uses a browser to drive the bulk-selection flow the way a person would.
Writes interact.json; exits 0 even on failures (results are data).
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


def http(url, data=None):
    """GET/POST without following redirects (302s are expected results)."""
    body = None
    if data is not None:
        body = urllib.parse.urlencode(data, doseq=True).encode()
    req = urllib.request.Request(url, data=body,
                                 method="POST" if data is not None else "GET")
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(req, timeout=15) as r:
            return r.status, r.geturl(), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, url, exc.read().decode("utf-8", "replace")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def run(url, out):
    checks = []

    def check(name, ok, detail=""):
        checks.append({"name": name, "ok": bool(ok), "detail": str(detail)[:300]})

    # read-only
    st, _, body = http(url + "/healthz")
    check("healthz", st == 200 and '"ok":true' in body.replace(" ", ""), st)
    st, _, body = http(url + "/")
    check("dashboard loads", st == 200 and "pending" in body.lower(), st)
    st, _, body = http(url + "/requests")
    n_cb = len(re.findall(r'type="checkbox"', body))
    check("list renders checkboxes", st == 200 and n_cb >= 10, "checkboxes=%d" % n_cb)
    st, _, body = http(url + "/requests?status=pending&category=Software")
    check("filtered list loads", st == 200, st)
    st, _, body = http(url + "/requests/2")
    check("detail loads", st == 200 and "Standing desks" in body, st)

    # mutations (fresh DB assumed)
    st, loc, _ = http(url + "/requests/1/approve", {"back": "/requests/1"})
    st2, _, body = http(url + "/requests/1")
    check("approve persists", st == 302 and "approved" in body.lower(),
          "post=%s get=%s" % (st, st2))
    st, loc, _ = http(url + "/requests/2/reject",
                      {"back": "/requests/2", "reason": "Over budget"})
    st2, _, body = http(url + "/requests/2")
    check("reject persists with reason", st == 302 and "rejected" in body.lower()
          and "Over budget" in body, "post=%s get=%s" % (st, st2))
    st, loc, _ = http(url + "/requests/bulk",
                      {"action": "approve", "ids": ["3", "4"], "back": "/requests"})
    _, _, b3 = http(url + "/requests/3")
    _, _, b4 = http(url + "/requests/4")
    check("bulk approve persists", st == 302 and "approved" in b3.lower()
          and "approved" in b4.lower(), st)
    st, loc, _ = http(url + "/requests/5/assign",
                      {"reviewer": "Priya Natarajan", "back": "/requests/5"})
    _, _, body = http(url + "/requests/5")
    check("assign persists", st == 302 and "Priya Natarajan" in body, st)
    st, loc, _ = http(url + "/settings", {"digest": "weekly",
                                          "auto_approve_threshold": "800"})
    _, _, body = http(url + "/settings")
    check("settings persist", st == 302 and "weekly" in body and "800" in body, st)
    st, loc, _ = http(url + "/jobs/triage/start", {})
    _, _, api = http(url + "/api/jobs")
    check("job start + api", st == 302 and '"state": "running"' in api.replace(" ", "")
          or '"state":"running"' in api.replace(" ", ""), st)
    _, _, body = http(url + "/jobs?job=running")
    check("jobs page reflects running", "running" in body.lower(), "")

    # tolerant browser probe: select first row + approve via the rendered UI
    ui = {"ran": False}
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.goto(url + "/requests", wait_until="load", timeout=15000)
            page.wait_for_timeout(400)
            boxes = page.query_selector_all('input[type="checkbox"]')
            ui["checkboxes_found"] = len(boxes)
            clicked = False
            if boxes:
                boxes[0].check()
                clicked = True
            btn = page.evaluate("""() => {
                const cand = [...document.querySelectorAll('button, input[type=submit]')]
                  .find(b => /approve/i.test((b.textContent||'') + ' ' + (b.value||'')));
                if (cand) { cand.click(); return true; } return false; }""")
            page.wait_for_timeout(1500)
            ui.update({"ran": True, "selected_first": clicked,
                       "approve_control_clicked": bool(btn),
                       "url_after": page.url})
            browser.close()
    except Exception as exc:
        ui["error"] = str(exc)[:300]
    check("ui bulk probe", ui.get("ran") and ui.get("approve_control_clicked"),
          json.dumps(ui)[:280])

    result = {"url": url, "checks": checks,
              "passed": sum(1 for c in checks if c["ok"]), "total": len(checks)}
    with open(out, "w") as fh:
        json.dump({"result": result, "ui_probe": ui}, fh, indent=1)
    print("interact: %d/%d checks passed" % (result["passed"], result["total"]))
    return result


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    run(args.url, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
