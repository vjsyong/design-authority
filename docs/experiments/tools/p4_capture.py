#!/usr/bin/env python3
"""P4b capture — session-end screens for the blind round (replication R1).

    python3 docs/experiments/tools/p4_capture.py --id r1-a-h1 --root ~/p4-maint

Serves run/<id>/ws with the project's own serve.py on a loopback port, loads
the app with a fixed fixture dataset (localStorage `bookmarks.v1`, per the
project's QA conventions), walks a fixed set of states with plain clicks on
data-testid hooks, and screenshots each into run/<id>/capture/. Best effort:
a state that cannot be reached still yields its screenshot attempt; every
outcome is recorded in capture.json with the app file hashes.
"""
import argparse
import hashlib
import json
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p4_common import P4_ROOT, VENV_PY, read_json, run_dir, write_json_atomic  # noqa: E402

PLAYWRIGHT_CACHE = os.path.expanduser("~/.cache/ms-playwright")
VIEWPORT = {"width": 1280, "height": 900}

FIXTURES = [
    {"id": "b1", "title": "Design systems in practice", "url": "https://example.org/design-systems",
     "tags": ["design", "reading"], "createdAt": "2026-09-01T09:00:00Z"},
    {"id": "b2", "title": "Charts for dashboards", "url": "https://example.org/charts",
     "tags": ["design", "tools"], "createdAt": "2026-09-02T10:30:00Z"},
    {"id": "b3", "title": "Keyboard shortcuts cheatsheet", "url": "https://example.org/shortcuts",
     "tags": ["reference"], "createdAt": "2026-09-03T11:00:00Z"},
    {"id": "b4", "title": "Colour theory primer", "url": "https://example.org/colour",
     "tags": ["design"], "createdAt": "2026-09-04T12:15:00Z"},
    {"id": "b5", "title": "Reading list backlog", "url": "https://example.org/reading",
     "tags": ["reading", "reference"], "createdAt": "2026-09-05T14:45:00Z"},
    {"id": "b6", "title": "Travel plans", "url": "https://example.org/travel",
     "tags": ["personal"], "createdAt": "2026-09-06T16:00:00Z"},
]

SEARCH_SELECTORS = ['[data-testid*="search"]', 'input[type="search"]',
                    'input[name="search"]', 'input[placeholder*="earch"]']
FILTER_SELECTORS = ['[data-testid*="filter"] button', 'button[data-testid*="filter"]',
                    '[data-testid*="chip"]', 'button[data-testid*="collection"]']
EDIT_SELECTORS = ['[data-testid*="edit"]', '[data-testid*="editor"]',
                  'button[data-testid*="open"]']


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def wait_healthz(port, timeout=25):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d/healthz" % port, timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            time.sleep(0.6)
    return False


def try_click(page, selectors):
    for sel in selectors:
        try:
            loc = page.locator(sel)
            if loc.count() > 0:
                loc.first.click(timeout=2500)
                return sel
        except Exception:
            continue
    return None


def try_fill(page, selectors, text):
    for sel in selectors:
        try:
            loc = page.locator(sel)
            if loc.count() > 0:
                loc.first.fill(text, timeout=2500)
                return sel
        except Exception:
            continue
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--root", default=P4_ROOT)
    args = ap.parse_args()
    root = os.path.abspath(os.path.expanduser(args.root))
    ws = os.path.join(run_dir(args.id, root), "ws")
    if not os.path.isfile(os.path.join(ws, "serve.py")):
        print("no serve.py in %s; skipping capture" % ws)
        return 1
    outdir = os.path.join(run_dir(args.id, root), "capture")
    os.makedirs(outdir, exist_ok=True)

    port = free_port()
    server = subprocess.Popen(["python3", "serve.py", "--port", str(port)],
                              cwd=ws, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL, start_new_session=True)
    report = {"id": args.id, "port": port, "states": {}, "app_sha": {}}
    try:
        if not wait_healthz(port):
            report["error"] = "healthz not ready"
            write_json_atomic(os.path.join(outdir, "capture.json"), report)
            print("healthz not ready; capture aborted")
            return 1

        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = PLAYWRIGHT_CACHE
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(viewport=VIEWPORT, locale="en-US")
            page.add_init_script(
                "localStorage.setItem('bookmarks.v1', %s);"
                % json.dumps(json.dumps(FIXTURES)))
            page.goto("http://127.0.0.1:%d/" % port, wait_until="load", timeout=15000)
            page.wait_for_timeout(700)

            page.screenshot(path=os.path.join(outdir, "default.png"))
            report["states"]["default"] = {"ok": True}

            sel = try_fill(page, SEARCH_SELECTORS, "des")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(outdir, "search.png"))
            report["states"]["search"] = {"ok": bool(sel), "selector": sel}
            if sel:
                try_fill(page, SEARCH_SELECTORS, "")
                page.wait_for_timeout(400)

            sel = try_click(page, FILTER_SELECTORS)
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(outdir, "filter.png"))
            report["states"]["filter"] = {"ok": bool(sel), "selector": sel}
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass

            sel = try_click(page, EDIT_SELECTORS)
            page.wait_for_timeout(600)
            page.screenshot(path=os.path.join(outdir, "editor.png"))
            report["states"]["editor"] = {"ok": bool(sel), "selector": sel}

            browser.close()
    finally:
        try:
            os.killpg(os.getpgid(server.pid), signal.SIGTERM)
            server.wait(timeout=8)
        except Exception:
            try:
                os.killpg(os.getpgid(server.pid), signal.SIGKILL)
            except Exception:
                pass

    for f in ("app.js", "styles.css", "index.html"):
        p = os.path.join(ws, f)
        if os.path.isfile(p):
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
            report["app_sha"][f] = h
    write_json_atomic(os.path.join(outdir, "capture.json"), report)
    ok = sum(1 for s in report["states"].values() if s.get("ok"))
    print("capture %s: %d/%d states reached" % (args.id, ok, len(report["states"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
