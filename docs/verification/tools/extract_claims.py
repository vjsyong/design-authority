#!/usr/bin/env python3
"""Extract agent claims (marks) for contract targets + fixed-element inventory.

For each build, serves it, normalizes state, then for every contract check with
a selector records the claim carried by the target node: its own data-* mark or
the nearest marked ancestor ("CANONICAL" = unmarked). Also inventories
position:fixed elements (to scope the no-floating-surfaces check allowlists).

Claims are evidence about what the agent SAID — never used as proof by the
verifier's own checks.
"""
import json
import os
import subprocess
import sys
import time
import socket

from playwright.sync_api import sync_playwright

REPO = "/home/xrim/design-authority"
PAIRS = [
    ("wink", "examples/cadence3-wink"),
    ("leader", "examples/cadence3-leader"),
    ("dominion", "examples/cadence3-dominion"),
]


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


out = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    for pack, target in PAIRS:
        contract = json.load(open(os.path.join(REPO, "packs", pack, "verification.json")))
        port = free_port()
        proc = subprocess.Popen([sys.executable, "-m", "http.server", str(port),
                                 "--bind", "127.0.0.1", "--directory", os.path.join(REPO, target)],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.6)
        page = browser.new_context(viewport={"width": 1280, "height": 900}).new_page()
        page.goto(f"http://127.0.0.1:{port}/index.html", wait_until="load")
        page.wait_for_timeout(300)
        page.evaluate("localStorage.clear()")
        page.reload(wait_until="load")
        page.wait_for_timeout(320)
        page.evaluate("""(() => { const d = document.querySelector('dialog[open]');
            if (!d) return; const s = d.querySelector('#wizSkip, [data-skip]'); if (s) s.click(); else d.close(); })()""")
        page.wait_for_timeout(200)
        if page.evaluate("!!document.querySelector('dialog[open]')"):
            page.keyboard.press("Escape")
            page.wait_for_timeout(150)
        page.evaluate("document.querySelectorAll('[hidden]').forEach(e => { if (e.tagName !== 'DIALOG') e.hidden = false; })")
        page.wait_for_timeout(150)

        claims = {}
        for c in contract["checks"]:
            sel = c.get("selector")
            if not sel:
                continue
            info = page.evaluate("""(sel) => {
                const starts = [...document.querySelectorAll(sel)];
                const el = starts.find(e => e.getClientRects().length > 0) || starts[0];
                if (!el) return {found: false};
                let node = el, claim = null, note = null, owner = null;
                while (node && node !== document.body) {
                    for (const k of ['improvised', 'adapted', 'fallback']) {
                        if (node.hasAttribute('data-' + k)) {
                            return {found: true, claim: k, note: node.getAttribute('data-' + k),
                                    owner: node.className.toString().slice(0, 70),
                                    literal: node === el};
                        }
                    }
                    if (node.hasAttribute('data-note')) {
                        return {found: true, claim: 'annotated-note', note: node.getAttribute('data-note'),
                                owner: node.className.toString().slice(0, 70), literal: node === el};
                    }
                    node = node.parentElement;
                }
                return {found: true, claim: 'CANONICAL', note: null, owner: el.className.toString().slice(0, 70), literal: true};
            }""", sel)
            claims[c["id"]] = {"selector": sel, **info}

        fixed = page.evaluate("""(() => {
            const out = [];
            for (const el of document.querySelectorAll('*')) {
                const cs = getComputedStyle(el);
                if (cs.position === 'fixed') {
                    const r = el.getBoundingClientRect();
                    out.push({ cls: el.className.toString().slice(0, 60) || el.tagName,
                               id: el.id || '', w: Math.round(r.width), h: Math.round(r.height) });
                }
            }
            return out;
        })()""")
        out[pack] = {"claims": claims, "fixed_elements": fixed}
        proc.terminate()
        print(f"== {pack}: {len(claims)} claim rows; fixed elements:")
        for f in fixed:
            print("   ", f)

    browser.close()

with open(os.path.join(REPO, "docs", "verification", "raw", "claims-and-fixed.json"), "w") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
print("saved docs/verification/raw/claims-and-fixed.json")
