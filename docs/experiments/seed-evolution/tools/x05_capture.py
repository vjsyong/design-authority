#!/usr/bin/env python3
"""x05 capture harness — deterministic fixture states, screenshots, probes.

Runs OUTSIDE the sandbox on the host. Serves a sealed workspace with its own
dev server, drives the frozen fixture states (localStorage seeds + scripted
interactions over the QA-hook testids), screenshots both viewports, and
records DOM/computed-style/behavioral probes. Never reads agent self-reports:
every measured artifact here is produced by this script.

Usage: x05_capture.py --ws WS --out CAPTURE_DIR [--port N]
"""
import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone

os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH",
                      os.path.expanduser("~/.cache/ms-playwright"))

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from x05_common import REPO, VENV_PY, read_json  # noqa: E402

FIXTURES = os.path.join(HERE, "..", "annexes", "fixtures", "bookmarks-seed.json")

VIEWPORTS = [("desktop", {"width": 1280, "height": 900}, False),
             ("phone", {"width": 390, "height": 844}, True)]

MAX_ACTION_MS = 2500

# ---------------------------------------------------------------- probe JS
INVENTORY_JS = r"""() => {
  const styles = (el) => {
    const cs = getComputedStyle(el);
    return {
      color: cs.color, bg: cs.backgroundColor,
      borderTop: [cs.borderTopWidth, cs.borderTopStyle, cs.borderTopColor].join(' '),
      borderLeft: [cs.borderLeftWidth, cs.borderLeftStyle, cs.borderLeftColor].join(' '),
      radius: [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomRightRadius, cs.borderBottomLeftRadius].join(' '),
      font: [cs.fontFamily, cs.fontSize, cs.fontWeight, cs.lineHeight].join(' | '),
      padding: [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].join(' '),
      margin: [cs.marginTop, cs.marginRight, cs.marginBottom, cs.marginLeft].join(' '),
      gap: cs.gap, shadow: cs.boxShadow, display: cs.display,
      position: cs.position, z: cs.zIndex, opacity: cs.opacity,
      textAlign: cs.textAlign, letterSpacing: cs.letterSpacing,
      textTransform: cs.textTransform, transition: cs.transitionDuration,
    };
  };
  const describe = (el) => {
    const r = el.getBoundingClientRect();
    return {
      tag: el.tagName.toLowerCase(),
      testid: el.getAttribute('data-testid'),
      classes: el.getAttribute('class') || '',
      role: el.getAttribute('role'),
      aria: {invalid: el.getAttribute('aria-invalid'), modal: el.getAttribute('aria-modal'),
             expanded: el.getAttribute('aria-expanded'), disabled: el.getAttribute('aria-disabled')},
      id: el.id || null,
      text: (el.innerText || el.value || el.getAttribute('aria-label') || '').slice(0, 160),
      rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
      styles: styles(el),
    };
  };
  const byId = {};
  for (const el of document.querySelectorAll('[data-testid]')) {
    const t = el.getAttribute('data-testid');
    (byId[t] = byId[t] || []).push(describe(el));
  }
  const all = [...document.querySelectorAll('*')];
  const bump = (o, k) => { if (k && !['none','auto','0px','normal','rgba(0, 0, 0, 0)'].includes(k)) o[k]=(o[k]||0)+1; };
  const counts = {elements: all.length, buttons: 0, links: 0, inputs: 0, tables: 0,
                  forms: 0, svgs: 0, dialogs: 0, h1: 0, h2: 0, cards: 0};
  const bg = {}, fg = {}, radius = {}, fonts = {}, padding = {};
  for (const el of all) {
    const cs = getComputedStyle(el); const tag = el.tagName.toLowerCase();
    if (tag === 'button') counts.buttons++;
    if (tag === 'a') counts.links++;
    if (['input','select','textarea'].includes(tag)) counts.inputs++;
    if (tag === 'table') counts.tables++;
    if (tag === 'form') counts.forms++;
    if (tag === 'svg') counts.svgs++;
    if (tag === 'h1') counts.h1++;
    if (tag === 'h2') counts.h2++;
    if (tag === 'dialog' || el.getAttribute('role') === 'dialog') counts.dialogs++;
    bump(bg, cs.backgroundColor); bump(fg, cs.color);
    bump(radius, [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomRightRadius, cs.borderBottomLeftRadius].join(' '));
    bump(fonts, cs.fontFamily); bump(padding, [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].join(' '));
  }
  const top = (o) => Object.entries(o).sort((a,b)=>b[1]-a[1]).slice(0, 40);
  return {testids: byId, counts,
          unique: {bg: top(bg), fg: top(fg), radius: top(radius), fonts: top(fonts), padding: top(padding)},
          bodyText: (document.body ? document.body.innerText : '').slice(0, 6000)};
}"""

FOCUS_JS = r"""() => {
  const a = document.activeElement;
  if (!a) return null;
  return {tag: a.tagName.toLowerCase(), testid: a.getAttribute('data-testid'),
          text: (a.innerText || a.value || '').slice(0, 100),
          classes: a.getAttribute('class') || ''};
}"""


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def free_port(start=8560):
    for port in range(start, start + 300):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("no free port")


def wait_http(url, timeout=25):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            time.sleep(0.4)
    return False


def seed_script(items):
    data = json.dumps(items)
    return ("localStorage.clear();"
            "localStorage.setItem('bookmarks.v1', JSON.stringify(%s));" % data)


CLEAR_SCRIPT = "localStorage.clear();"

INVALID_URL = "not a url"
SEARCH_TERM = "design"


class Driver:
    def __init__(self, page, log):
        self.page = page
        self.log = log

    def shot_ready(self, ms=700):
        self.page.wait_for_timeout(ms)

    def try_click(self, testid, ms=MAX_ACTION_MS):
        sel = "[data-testid=%s]" % json.dumps(testid)
        try:
            self.page.locator(sel).first.click(timeout=ms)
            return True
        except Exception as exc:
            self.log.append("click %s failed: %s" % (testid, str(exc)[:160]))
            return False

    def count(self, testid):
        sel = "[data-testid=%s]" % json.dumps(testid)
        try:
            return self.page.locator(sel).count()
        except Exception:
            return 0

    def fill_first(self, testid, value):
        sel = "[data-testid=%s]" % json.dumps(testid)
        try:
            loc = self.page.locator(sel).first
            loc.click(timeout=MAX_ACTION_MS)
            loc.fill(value, timeout=MAX_ACTION_MS)
            return True
        except Exception as exc:
            self.log.append("fill %s failed: %s" % (testid, str(exc)[:160]))
            return False

    def press(self, key):
        try:
            self.page.keyboard.press(key)
            return True
        except Exception:
            return False


def run_actions(driver, actions):
    """actions: list of ("click", testid) / ("click-menu", (menu, item))
    / ("fill", (testid, value)) / ("press", key) / ("wait", ms)."""
    for act in actions:
        kind = act[0]
        payload = act[1] if len(act) > 1 else None
        if kind == "click":
            driver.try_click(payload)
        elif kind == "click-menu":
            menu, item = payload
            if driver.count(item) == 0 and driver.count(menu) > 0:
                driver.try_click(menu)
                driver.page.wait_for_timeout(300)
            driver.try_click(item)
        elif kind == "fill":
            tid, value = payload
            driver.fill_first(tid, value)
        elif kind == "press":
            driver.press(payload)
        elif kind == "wait":
            driver.page.wait_for_timeout(payload)
        driver.page.wait_for_timeout(150)


def build_states(seed_items):
    """state name -> (storage script, actions). Actions run after load."""
    s = seed_script(seed_items)
    c = CLEAR_SCRIPT
    return {
        "empty":       (c, []),
        "populated":   (s, []),
        "filtered":    (s, [("click-menu", ("tag-chip", "tag-chip"))]),
        "filtered-none": (s, [("fill", ("search-input", "zzzz-no-match-zzzz")),
                              ("press", "Enter"), ("wait", 500)]),
        "invalid":     (s, [("click", "btn-add-bookmark"), ("click", "submit-add"),
                            ("wait", 500)]),
        "confirm":     (s, [("click-menu", ("bookmark-actions", "bookmark-delete")),
                            ("wait", 400)]),
        "confirm-bulk": (s, [("click", "bulk-select"), ("click", "bulk-select"),
                             ("click", "bulk-delete"), ("wait", 400)]),
        "post-delete": (s, [("click-menu", ("bookmark-actions", "bookmark-delete")),
                            ("wait", 300), ("click", "confirm-accept"), ("wait", 500)]),
        "analytics":   (s, [("click", "nav-analytics"), ("wait", 400)]),
        "palette":     (s, [("click", "btn-palette"), ("wait", 400)]),
        "wizard-1":    (s, [("click", "btn-import"), ("wait", 400)]),
        "wizard-2":    (s, [("click", "btn-import"), ("click", "wizard-next"),
                            ("wait", 400)]),
    }


def capture(ws, out, port=None, seed_items=None):
    from playwright.sync_api import sync_playwright

    ws = os.path.abspath(ws)
    os.makedirs(os.path.join(out, "screens"), exist_ok=True)
    result = {"ws": ws, "started": now_iso(), "states": {}, "probes": {},
              "console_errors": []}
    port = port or free_port()
    url = "http://127.0.0.1:%d" % port
    result["url"] = url
    seed_items = seed_items or read_json(FIXTURES) or []
    result["fixture"] = {"items": len(seed_items), "path": os.path.abspath(FIXTURES)}
    states = build_states(seed_items)

    server = subprocess.Popen(
        [VENV_PY, "serve.py", "--port", str(port)], cwd=ws,
        stdout=open(os.path.join(out, "server.log"), "w"),
        stderr=subprocess.STDOUT)
    try:
        if not (wait_http(url + "/healthz") or wait_http(url + "/")):
            result["error"] = "dev server never came up"
            return result
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for state, (storage_js, actions) in states.items():
                entry = {"viewports": {}}
                for vp_name, viewport, mobile in VIEWPORTS:
                    vp = {"actions": [], "console_errors": []}
                    try:
                        ctx = browser.new_context(viewport=viewport, is_mobile=mobile,
                                                  has_touch=mobile, device_scale_factor=1)
                        ctx.add_init_script(storage_js)
                        page = ctx.new_page()
                        page.on("pageerror", lambda e, v=vp: v["console_errors"].append(str(e)[:300]))
                        page.on("console", lambda m, v=vp: v["console_errors"].append(m.text[:300])
                                if m.type == "error" else None)
                        page.goto(url + "/", wait_until="load", timeout=15000)
                        page.wait_for_timeout(700)
                        drv = Driver(page, vp["actions"])
                        run_actions(drv, actions)
                        drv.shot_ready()
                        shot = os.path.join(out, "screens", "%s-%s.png" % (state, vp_name))
                        page.screenshot(path=shot, full_page=True)
                        vp["shot"] = os.path.relpath(shot, out)
                        vp["ok"] = True
                        if vp_name == "desktop":
                            probe = page.evaluate(INVENTORY_JS)
                            probe["focus"] = page.evaluate(FOCUS_JS)
                            if state in ("invalid",):
                                probe["invalid_timing"] = _timing_probe(page, url, storage_js)
                            result["probes"][state] = probe
                        ctx.close()
                    except Exception as exc:
                        vp["ok"] = False
                        vp["error"] = str(exc)[:300]
                    entry["viewports"][vp_name] = vp
                result["states"][state] = entry
            browser.close()
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except Exception:
            server.kill()
    result["finished"] = now_iso()
    return result


def _timing_probe(page, url, storage_js):
    """Validation-timing observation: on a fresh page, type an invalid value
    into the URL field without submitting and sample when / where an error
    first appears. Raw observations only; classification is downstream."""
    out = {"steps": []}
    try:
        ctx = page.context
        page2 = ctx.new_page()
        page2.goto(url + "/", wait_until="load", timeout=15000)
        page2.wait_for_timeout(500)
        if page2.locator("[data-testid=btn-add-bookmark]").count():
            page2.locator("[data-testid=btn-add-bookmark]").first.click(timeout=MAX_ACTION_MS)
        fld = page2.locator("[data-testid=input-url]").first
        fld.click(timeout=MAX_ACTION_MS)
        fld.type(INVALID_URL, delay=15)
        out["steps"].append({"when": "after-type", "errors": _snapshot_errors(page2)})
        page2.wait_for_timeout(900)
        out["steps"].append({"when": "after-wait-900ms", "errors": _snapshot_errors(page2)})
        fld.evaluate("el => el.blur()")
        page2.wait_for_timeout(400)
        out["steps"].append({"when": "after-blur", "errors": _snapshot_errors(page2)})
        submit = page2.locator("[data-testid=submit-add]")
        if submit.count():
            submit.first.click(timeout=MAX_ACTION_MS)
        page2.wait_for_timeout(400)
        out["steps"].append({"when": "after-submit", "errors": _snapshot_errors(page2)})
        # recovery affordance: type a valid value, do errors clear without resubmit?
        try:
            fld.fill("https://example.com/fixed", timeout=MAX_ACTION_MS)
            page2.wait_for_timeout(400)
            out["steps"].append({"when": "after-fix-typing", "errors": _snapshot_errors(page2)})
        except Exception as exc:
            out["recovery_error"] = str(exc)[:200]
        page2.close()
    except Exception as exc:
        out["error"] = str(exc)[:300]
    return out


def _snapshot_errors(page):
    """Visible error-ish nodes: [data-testid=form-error], aria-invalid fields,
    and elements whose text/classes smell like an error, with placement info."""
    js = r"""() => {
      const out = {form_error_nodes: [], invalid_fields: [], suspicious: []};
      for (const el of document.querySelectorAll('[data-testid=form-error], .error, .field-error, [role=alert], [aria-live]')) {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        out.form_error_nodes.push({tag: el.tagName.toLowerCase(), testid: el.getAttribute('data-testid'),
          cls: (el.getAttribute('class')||'').slice(0,80), text: (el.innerText||'').slice(0,120),
          rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
          color: cs.color, display: cs.display, visible: !!(r.width && r.height)});
      }
      for (const el of document.querySelectorAll('[aria-invalid=true], [aria-invalid=True], .invalid, .is-invalid')) {
        const cs = getComputedStyle(el);
        out.invalid_fields.push({tag: el.tagName.toLowerCase(), testid: el.getAttribute('data-testid'),
          border: cs.borderTopColor + ' ' + cs.borderTopWidth, outline: cs.outlineColor,
          color: cs.color, bg: cs.backgroundColor});
      }
      for (const el of document.querySelectorAll('[role=alert], [role=status]')) {
        out.suspicious.push({role: el.getAttribute('role'), text: (el.innerText||'').slice(0,120)});
      }
      return out;
    }"""
    try:
        return page.evaluate(js)
    except Exception as exc:
        return {"error": str(exc)[:200]}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--port", type=int, default=None)
    ap.add_argument("--fixtures", default=None)
    args = ap.parse_args(argv)
    seed_items = None
    if args.fixtures and os.path.exists(args.fixtures):
        seed_items = read_json(args.fixtures)
    res = capture(args.ws, args.out, args.port, seed_items=seed_items)
    with open(os.path.join(args.out, "capture.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    with open(os.path.join(args.out, "probes.json"), "w") as fh:
        json.dump(res.get("probes", {}), fh, indent=1)
    n_err = sum(len(vp.get("console_errors", []))
                for st in res["states"].values() for vp in st["viewports"].values())
    avail = sum(1 for st in res["states"].values()
                for vp in st["viewports"].values() if vp.get("ok"))
    print("capture: %d/%d state-viewports ok, %d console errors%s"
          % (avail, len(res["states"]) * len(VIEWPORTS), n_err,
             "  ERROR: " + res["error"] if res.get("error") else ""))
    return 0 if not res.get("error") else 1


if __name__ == "__main__":
    sys.exit(main())
