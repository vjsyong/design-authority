#!/usr/bin/env python3
"""Focused independent verification for the reconciliation closure test:
the settings-save confirmation of cadence-wink-r2 conforms to the recorded
pattern/inline-notice contract (wink 0.2.0).

Checks derive from the record's own recorded states ("inline notice: rounded
12, tinted fill (palette roles)"; "copy is plain, non-blaming, question-first")
plus the pattern's dont ("floating toast stacks are not canon") and the
in-flow placement rule. Self-report is evidence, never proof: the checks are
re-derived from the served DOM and computed styles, never trusted from the
build."""

import functools
import hashlib
import http.server
import json
import os
import socketserver
import sys
import threading
from datetime import datetime, timezone

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(DIR))
PACK = os.path.join(REPO, "authorities", "wink", "artifacts.json")
OUT = os.path.join(DIR, "_evidence", "verification", "notice-migration.json")


def serve():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIR)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def main():
    from playwright.sync_api import sync_playwright
    httpd, port = serve()
    checks = []

    def check(cid, desc, ok, detail, ref):
        checks.append({"id": cid, "desc": desc, "pass": bool(ok), "detail": detail, "record_ref": ref})

    # bind the verification to the exact record it checks (staleness is detectable)
    pack = json.load(open(PACK))
    record = next((a for a in pack["artifacts"] if a["id"] == "pattern/inline-notice"), None)
    rhash = (hashlib.sha256(json.dumps(record, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
             if record else None)
    check("record-bound", "verifies against the recorded pattern/inline-notice (wink 0.2.0)",
          record is not None, "record_hash=%s" % rhash, "record: pattern/inline-notice")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("http://127.0.0.1:%d/index.html" % port)
            page.wait_for_load_state("load")
            page.wait_for_timeout(300)
            skip = page.query_selector("#wzSkip")
            if skip and skip.is_visible():
                skip.click()          # dismiss the first-run onboarding wizard
                page.wait_for_timeout(250)
            page.click('button[data-view="settings"]')
            page.fill("#setName", "Sam")
            page.click("#saveBtn")
            page.wait_for_timeout(900)

            notice = page.query_selector("#saveNotice")
            check("notice-exists", "a notice element appears after saving settings",
                  notice is not None, "present" if notice else "absent", "pattern/inline-notice")
            if notice:
                style = page.evaluate("() => { const s = getComputedStyle(document.getElementById('saveNotice')); return {bg: s.backgroundColor, radius: s.borderRadius, pos: s.position}; }")
                box = notice.bounding_box() or {}
                check("notice-visible", "visible in the page flow", (box.get("height") or 0) > 0, str(box),
                      "do: near the element that changed")
                check("notice-fill", "tinted fill = parsnip (#F6F6F4)",
                      style["bg"] == "rgb(246, 246, 244)", style["bg"],
                      "states[0]: rounded 12, tinted fill (palette roles)")
                check("notice-radius", "rounded 12", style["radius"] == "12px", style["radius"],
                      "states[0]: rounded 12")
                check("notice-in-flow", "not a floating/toast surface",
                      style["pos"] in ("static", "relative"), style["pos"],
                      "dont: floating toast stacks are not canon")
                lead = page.evaluate("() => { const b = document.querySelector('#saveNotice b'); return b ? b.textContent.trim() : null; }")
                check("notice-lead", "bold lead sentence present", lead == "Saved.", repr(lead),
                      "record summary: bold lead sentence + plain supporting line")

            toast_shown = page.evaluate("() => document.getElementById('toast').classList.contains('show')")
            check("no-save-toast", "the save flow no longer raises the improvised toast",
                  toast_shown is False, "toast.show=%s" % toast_shown,
                  "canon: the notice is the sanctioned substitute for toasts")
            stale = page.evaluate("() => !!document.getElementById('saveEcho')")
            check("stale-echo-gone", "the r2a ad-hoc echo no longer exists",
                  stale is False, "saveEcho=%s" % stale, "migration scope")
            browser.close()
    finally:
        httpd.shutdown()

    verdict = "pass" if all(c["pass"] for c in checks) else "violation"
    coverage = [
        {"requirement": "states[0]: inline notice rounded 12, tinted fill (palette roles)",
         "checks": ["notice-fill", "notice-radius"], "covered": True},
        {"requirement": "states[1]: copy is plain, non-blaming, question-first",
         "checks": [], "covered": False,
         "note": "register/voice is a human-review item; not mechanically checked here"},
        {"requirement": "do[0]: prefer inline notices near the changed element",
         "checks": ["notice-visible", "notice-in-flow"], "covered": True},
        {"requirement": "dont[0]: floating toast stacks are not canon",
         "checks": ["notice-in-flow", "no-save-toast"], "covered": True},
    ]
    out = {"verifier": "_evidence/verify-notice-migration.py",
           "target": "examples/cadence-wink-r2",
           "decision": "pattern/inline-notice",
           "authority": {"authority": "wink", "version": "0.2.0"},
           "record": {"id": "pattern/inline-notice", "record_hash": rhash},
           "ran_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "verdict": verdict, "checks": checks, "coverage": coverage,
           "note": "Focused independent verification for the reconciliation closure test (docs/experiments/07 section 5). Coverage is bound to the record's normative items; uncovered items are disclosed, not implied. Fresh run only; artifact-local results are never proof."}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("%s: %s (%d/%d checks; coverage %d/%d normative items)"
          % (verdict, OUT, sum(c["pass"] for c in checks), len(checks),
             sum(1 for c in coverage if c["covered"]), len(coverage)))
    for c in checks:
        print("  %s %s - %s" % ("PASS" if c["pass"] else "FAIL", c["id"], c["detail"]))
    for c in coverage:
        if not c["covered"]:
            print("  (uncovered) %s - %s" % (c["requirement"], c.get("note", "")))
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
