#!/usr/bin/env python3
"""Cadence (examples/cadence3-dominion) self-test — Playwright, headless.

Run (from repo root, with the static server already up on :8483):
  PLAYWRIGHT_BROWSERS_PATH=~/.cache/ms-playwright .venv/bin/python3 \
    examples/cadence3-dominion/_evidence/selftest.py

Checks: canon render (status labels, ledger, notice, charts exact values,
bilingual pairs incl. <560px collapse), no shadows/motion/imagery, marks
toggle, interactions (log/save meter, delete→dialog→undo, reorder, empty
state), persistence, data-el coverage of all 42 asks, zero console errors,
same-origin only (no external requests).
"""
import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8483/"
APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(APP, "_evidence", "selftest-report.txt")

RESULTS = []
def check(name, cond, extra=""):
    RESULTS.append({"name": name, "ok": bool(cond), "extra": str(extra)})
    print(("PASS  " if cond else "FAIL  ") + name + ("" if cond else ("   [" + str(extra) + "]")))

def main():
    console_errors = []
    page_errors = []
    requests = []
    responses = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.on("request", lambda r: requests.append(r.url))
        page.on("response", lambda r: responses.append((r.url, r.status)))

        page.goto(BASE, wait_until="networkidle")
        page.wait_for_selector("#ritual-list li")

        # ---------- boot state ----------
        check("title", page.title() == "Cadence — dominion build", page.title())
        check("nav active = Today", page.get_attribute("a[data-view='today']", "aria-current") == "page")
        check("five rituals", page.locator("#ritual-list li").count() == 5)
        check("meter readout exact", page.inner_text("#meter-readout") == "2 of 5 rituals · 45 of 100 minutes",
              page.inner_text("#meter-readout"))
        check("meter fill 40%", page.get_attribute("#meter-fill", "style") == "width: 40%;",
              page.get_attribute("#meter-fill", "style"))
        wb = page.inner_text("#week-band-line")
        check("week band exact", wb == "This week: 6 of 15 ritual slots logged · 135 minutes · streak 7 days", wb)

        # status labels (component/status): word-first, structure emphasis
        chip1 = page.locator('#ritual-list li[data-rit="r1"] .st')
        check("status r1 word", chip1.inner_text() == "On track", chip1.inner_text())
        chip3 = page.locator('#ritual-list li[data-rit="r3"] .st')
        check("status r3 word", chip3.inner_text() == "Slipping", chip3.inner_text())
        bw = chip3.evaluate("el => getComputedStyle(el).borderLeftWidth")
        check("status slippage = left rule 2px", bw == "2px", bw)
        check("ordinals not icons", page.locator('#ritual-list li[data-rit="r1"] .ordinal').inner_text() == "01")
        check("no <img> anywhere", page.evaluate("document.querySelectorAll('img').length") == 0)

        # one primary per view (Today, editor closed)
        prim = page.evaluate("""() => Array.from(document.querySelectorAll('.b-slate'))
            .filter(b => b.offsetParent !== null).length""")
        check("Today: one primary (row)", prim == 1, prim)

        # ---------- History: charts exact values ----------
        page.click("a[data-view='history']")
        page.wait_for_selector("#bar-cols .bcol")
        vals = page.eval_on_selector_all("#bar-cols .bval", "els => els.map(e => e.textContent)")
        check("bar values exact", vals == ["25", "20", "0", "25", "20", "35", "20"], vals)
        days = page.eval_on_selector_all("#bar-days .day", "els => els.map(e => e.textContent)")
        check("bar day labels", days == ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], days)
        h0 = page.evaluate("""() => { const bars = document.querySelectorAll('#bar-cols .bar');
            return getComputedStyle(bars[2]).height; }""")
        check("zero-value bar is empty", h0 == "0px", h0)

        cells = page.eval_on_selector_all("#heat-grid .hcell:not(.wd):not(.blank)",
                                          "els => els.map(e => ({t: e.textContent, c: e.className}))")
        check("heatmap 31 day cells", len(cells) == 31, len(cells))
        levels = [c["c"] for c in cells[:7]]
        expected_levels = ["hcell l2", "hcell l1", "hcell l2", "hcell l1", "hcell l2", "hcell l3", "hcell l2 today"]
        check("heat levels days 1-7 exact", levels == expected_levels, levels)
        check("today cell = 2px black border",
              page.evaluate("""() => { const c = document.querySelector('.hcell.today');
                  const s = getComputedStyle(c); return s.borderTopWidth + ' ' + s.borderTopColor; }""")
              == "2px rgb(0, 0, 0)")
        check("heat legend 5 items", page.locator("#heat-legend .lg").count() == 5)

        spark = page.inner_text("#spark-labels")
        check("sparkline labels exact", spark == "25 · 20 · 35 · 20 · 35 · 55 · 45 minutes", spark)
        check("sparkline markers 7", page.locator("#spark-svg rect").count() == 7)
        check("sparkline polyline", page.locator("#spark-svg polyline").count() == 1)

        # ledger
        check("ledger page1 rows 7", page.locator("#ledger-rows tr").count() == 7,
              page.locator("#ledger-rows tr").count())
        check("pager readout", page.inner_text("#page-readout") == "Page 1 of 2",
              page.inner_text("#page-readout"))
        check("prev disabled on page1", page.is_disabled("#page-prev"))
        page.click("#page-next")
        check("page2 readout", page.inner_text("#page-readout") == "Page 2 of 2")
        check("page2 rows 7", page.locator("#ledger-rows tr").count() == 7)
        check("next disabled on page2", page.is_disabled("#page-next"))
        miss_n = page.evaluate("""() => Array.from(document.querySelectorAll('#ledger-rows .st'))
            .filter(e => e.textContent === 'Missed').length""")
        check("one Missed row on page 2", miss_n == 1, miss_n)
        miss_cls = page.evaluate("""() => { const els = Array.from(document.querySelectorAll('#ledger-rows .st'));
            const m = els.find(e => e.textContent === 'Missed'); return m ? m.className + '|' +
            getComputedStyle(m).borderLeftWidth : 'none'; }""")
        check("Missed chip attn", miss_cls == "st attn|2px", miss_cls)
        page.click("#page-prev")
        page.fill("#ledger-search", "read")
        check("search 'read' -> 4 rows", page.locator("#ledger-rows tr").count() == 4,
              page.locator("#ledger-rows tr").count())
        page.fill("#ledger-search", "")
        check("search cleared -> 7 rows", page.locator("#ledger-rows tr").count() == 7)

        # ---------- Achievements ----------
        page.click("a[data-view='achievements']")
        check("streak numeral 7", page.inner_text("#streak-value") == "7")
        check("streak sub", page.inner_text("#streak-sub") == "days in a row")
        check("7-day tile achieved", page.inner_text("#tile7-meta") == "7 of 7 days")
        check("entries tile 14", page.inner_text("#tile-entries-num") == "14")
        check("week tile 145", page.inner_text("#tile-week-num") == "145")

        # ---------- bilingual pairs + collapse ----------
        for view in ["today", "history", "achievements", "settings"]:
            page.click("a[data-view='%s']" % view)
            pair = page.eval_on_selector("#view-%s .page-title" % view,
                """el => ({en: el.querySelector('.en').textContent,
                          fr: el.querySelector('.fr').textContent})""")
            check("bilingual %s" % view, bool(pair["en"]) and bool(pair["fr"]) and pair["en"] != pair["fr"], pair)
        cols = page.eval_on_selector("#view-settings .page-title",
                                     "el => getComputedStyle(el).gridTemplateColumns.split(' ').length")
        check("bilingual side-by-side @1280", cols == 3, cols)
        page.set_viewport_size({"width": 500, "height": 900})
        cols = page.eval_on_selector("#view-settings .page-title",
                                     "el => getComputedStyle(el).gridTemplateColumns.split(' ').length")
        check("bilingual collapses @500", cols == 1, cols)
        check("collapse is marked", page.get_attribute("#view-settings .page-title", "data-mark") == "adapted")
        page.set_viewport_size({"width": 1280, "height": 900})

        # ---------- Settings presence ----------
        page.click("a[data-view='settings']")
        check("goal slider 20", page.input_value("#goal-slider") == "20")
        check("goal readout", page.inner_text("#goal-readout") == "20 minutes")
        check("reminders checked", page.is_checked("#reminders-check"))
        check("quiet unchecked", not page.is_checked("#quiet-toggle"))
        check("freq radios 3", page.locator("input[name='freq']").count() == 3)
        check("category select 4 options", page.locator("#ritual-category option").count() == 4)
        check("notes textarea", page.locator("#ritual-notes").count() == 1)
        check("initials plate", page.inner_text("#initials-plate") == "AM")
        check("theme declined statement", "not defined" in page.inner_text("#theme-row"))
        check("export action", "CSV" in page.inner_text("#export-csv"))
        check("onboarding step 1", page.inner_text("#onb-readout") == "Step 1 of 3")
        page.click("#onb-next")
        check("onboarding step 2", page.inner_text("#onb-readout") == "Step 2 of 3")
        page.click("#onb-back")
        check("onboarding back to 1", page.inner_text("#onb-readout") == "Step 1 of 3")
        check("photo row declined", "not available" in page.inner_text("#photo-row"))

        # ---------- marks toggle ----------
        page.click("#marks-toggle")
        check("marks-on class", page.evaluate("document.body.classList.contains('marks-on')"))
        outline = page.eval_on_selector("#week-band", "el => getComputedStyle(el).outlineStyle")
        check("marked outline dashed", outline == "dashed", outline)
        amber = page.eval_on_selector("#week-band", "el => getComputedStyle(el).outlineColor")
        check("marked outline amber", amber == "rgb(183, 121, 31)", amber)
        label = page.eval_on_selector("#week-band", "el => getComputedStyle(el, '::after').content")
        check("mark label text", "improvised" in label and "weekly summary" in label, label)
        page.click("#marks-toggle")
        check("marks-off", page.evaluate("!document.body.classList.contains('marks-on')"))

        # ---------- data-el coverage (all 42 asks) ----------
        found = page.evaluate("""() => {
            const s = new Set();
            document.querySelectorAll('[data-el]').forEach(n =>
                n.getAttribute('data-el').split(/\\s+/).forEach(x => s.add(Number(x))));
            return Array.from(s).sort((a, b) => a - b);
        }""")
        check("data-el covers 1..42", found == list(range(1, 43)), [x for x in range(1, 43) if x not in found])

        # ---------- no shadows / no motion (computed) ----------
        page.evaluate("document.activeElement && document.activeElement.blur()")
        shadows = page.evaluate("""() => Array.from(document.querySelectorAll('*'))
            .map(el => getComputedStyle(el).boxShadow)
            .filter(v => v && v !== 'none')""")
        check("no shadows anywhere (blurred)", shadows == [], shadows[:3])
        motion = page.evaluate("""() => Array.from(document.querySelectorAll('*')).filter(el => {
            const s = getComputedStyle(el);
            return (s.animationName && s.animationName !== 'none') ||
                   (s.transitionDuration && s.transitionDuration.split(',').some(d => parseFloat(d) > 0));
        }).length""")
        check("no animation / transition", motion == 0, motion)
        # focus glow exists and is the blue halo (D-21)
        page.focus("#marks-toggle")
        glow = page.eval_on_selector("#marks-toggle", "el => getComputedStyle(el).boxShadow")
        check("focus glow present", "102, 175, 233" in glow, glow)
        page.evaluate("document.activeElement.blur()")
        # red is ceremonial only
        reds = page.evaluate("""() => Array.from(document.querySelectorAll('*'))
            .filter(el => { const c = getComputedStyle(el).backgroundColor;
                            return c === 'rgb(235, 45, 55)'; }).map(el => el.className)""")
        check("red only in two ceremony nodes", sorted(reds) == ["acc", "acc-red"], reds)

        # per-view primary audit
        for view in ["today", "history", "achievements", "settings"]:
            page.click("a[data-view='%s']" % view)
            n = page.evaluate("Array.from(document.querySelectorAll('.b-slate')).filter(b => b.offsetParent !== null).length")
            check("<=1 primary on %s" % view, n <= 1, n)

        # ---------- interaction: log flow + saving meter + notice + ceremony ----------
        page.click("a[data-view='today']")
        page.click('#ritual-list li[data-rit="r3"] .r-log')
        check("editor opens w/ title", page.inner_text("#log-title") == "Log — Practice guitar")
        check("editor date default", page.input_value("#log-date") == "2026-10-07")
        check("minutes default target", page.input_value("#log-minutes") == "30")
        check("one primary w/ editor open",
              page.evaluate("Array.from(document.querySelectorAll('.b-slate')).filter(b => b.offsetParent !== null).length") == 1)
        page.click("#log-save")
        page.wait_for_function("document.querySelector('#save-readout').textContent.indexOf('Saved') === 0")
        check("saving meter final readout", page.inner_text("#save-readout") == "Saved · 1 of 1 steps")
        check("notice says logged", page.inner_text("#notice-logged-text").startswith("Logged — 30 minutes for Practice guitar"))
        check("ceremony accent visible", page.is_visible("#ceremony-accent"))
        check("meter updated 3 of 5", page.inner_text("#meter-readout") == "3 of 5 rituals · 75 of 100 minutes",
              page.inner_text("#meter-readout"))
        check("week band updated", page.inner_text("#week-band-line") ==
              "This week: 7 of 15 ritual slots logged · 165 minutes · streak 7 days",
              page.inner_text("#week-band-line"))
        page.click("#log-cancel")

        # ---------- interaction: delete → confirm dialog → undo ----------
        page.click("a[data-view='settings']")
        page.click('.admin-edit[data-rid="r3"]')
        page.click("#remove-ritual")
        check("dialog visible", page.is_visible("#confirm-dialog"))
        check("dialog not pre-focused on confirm",
              page.evaluate("document.activeElement && document.activeElement.id") == "confirm-dialog",
              page.evaluate("document.activeElement && document.activeElement.id"))
        check("dialog title bilingual", "Retirer" in page.inner_text("#confirm-title"))
        check("dialog consequence sentence", "Practice guitar" in page.inner_text("#confirm-body"))
        page.click("#confirm-cancel")
        check("dialog closes on cancel", not page.is_visible("#confirm-dialog"))
        page.click("#remove-ritual")
        page.click("#confirm-remove")
        check("ritual removed (4 left)", page.locator("#ritual-list li").count() == 4)
        check("removed notice", "Practice guitar" in page.inner_text("#notice-removed-text"))
        page.click("#undo-btn")
        check("undo restores (5)", page.locator("#ritual-list li").count() == 5)
        check("undo notice text", "Restored" in page.inner_text("#notice-removed-text"))

        # ---------- interaction: reorder (move buttons, not drag) ----------
        page.click('.admin-edit[data-rid="r1"]')
        page.click("#move-down")
        first = page.get_attribute("#ritual-list li:first-child", "data-rit")
        check("reorder moves r1 down", first == "r2", first)
        page.click("#move-up")
        first = page.get_attribute("#ritual-list li:first-child", "data-rit")
        check("reorder restored", first == "r1", first)
        # name error (#9)
        page.fill("#ritual-name", "")
        page.click("#editor-save")
        check("name error shows", page.is_visible("#name-error"))
        err_l = page.eval_on_selector("#name-error", "el => getComputedStyle(el).borderLeftWidth")
        check("error has left rule", err_l == "2px", err_l)
        page.fill("#ritual-name", "Morning walk")
        page.click("#editor-cancel")

        # ---------- persistence ----------
        page.check("#quiet-toggle")
        page.reload(wait_until="networkidle")
        page.click("a[data-view='settings']")
        check("quiet persisted", page.is_checked("#quiet-toggle"))
        page.evaluate("""() => { const s = document.querySelector('#goal-slider');
            s.value = 30; s.dispatchEvent(new Event('input', {bubbles: true})); }""")
        check("goal readout 30", page.inner_text("#goal-readout") == "30 minutes")
        page.reload(wait_until="networkidle")
        page.click("a[data-view='settings']")
        check("goal persisted", page.input_value("#goal-slider") == "30")

        # ---------- export CSV (on-page blob; no network) ----------
        page.click("#export-csv")
        csv = page.evaluate("window.__lastExport || ''")
        nlogs = page.evaluate("window.cadence.state().logs.length")
        check("csv header", csv.splitlines()[0].startswith('"date","ritual","category","minutes","status"'),
              csv.splitlines()[0] if csv else "empty")
        check("csv rows = logs + header", len(csv.splitlines()) == nlogs + 1, len(csv.splitlines()))

        # ---------- empty state ----------
        ids = page.evaluate("window.cadence.state().rituals.map(r => r.id)")
        for rid in ids:
            page.click('.admin-edit[data-rid="%s"]' % rid)
            page.click("#remove-ritual")
            page.click("#confirm-remove")
        page.click("a[data-view='today']")
        check("empty state visible", page.is_visible("#empty-state"))
        check("empty sentence", "No rituals yet" in page.inner_text("#empty-state"))
        page.click("#empty-add")
        check("empty action opens add editor", page.is_visible("#ritual-editor") and
              page.inner_text("#editor-title") == "Add a ritual")
        page.click("#editor-cancel")

        # ---------- reset to fixtures ----------
        page.evaluate("window.cadence.reset()")
        page.reload(wait_until="networkidle")
        check("fixtures restored", page.locator("#ritual-list li").count() == 5 and
              page.inner_text("#meter-readout") == "2 of 5 rituals · 45 of 100 minutes")

        # ---------- fonts + network ----------
        page.evaluate("() => document.fonts.ready.then(() => true)")
        fonts = page.evaluate("() => document.fonts.check('16px Arimo')")
        check("Arimo font loaded", fonts)
        ext = [u for u in requests if not u.startswith(BASE)]
        check("same-origin only (no external requests)", ext == [], ext[:5])
        for asset in ["app.css", "app.js", "fonts/Arimo-VF.ttf"]:
            ok = any(u.endswith(asset) and s == 200 for (u, s) in responses)
            check("asset 200: " + asset, ok)

        # ---------- console ----------
        check("zero console errors", console_errors == [], console_errors[:5])
        check("zero page errors", page_errors == [], page_errors[:5])

        ctx.close()
        browser.close()

    passed = sum(1 for r in RESULTS if r["ok"])
    total = len(RESULTS)
    with open(REPORT, "w") as fh:
        fh.write("Cadence dominion build — self-test report\n")
        fh.write("pass %d / %d\n\n" % (passed, total))
        for r in RESULTS:
            fh.write(("PASS  " if r["ok"] else "FAIL  ") + r["name"] +
                     ("" if r["ok"] else "   [" + r["extra"] + "]") + "\n")
    print("\n%d/%d checks passed — report: %s" % (passed, total, REPORT))
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
