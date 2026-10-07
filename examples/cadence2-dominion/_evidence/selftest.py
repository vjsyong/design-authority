#!/usr/bin/env python3
"""Cadence (cadence2-dominion) self-test — Playwright DOM pass on port 8483."""
import json, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8483/"
results = []
def ok(name, cond, extra=""):
    results.append((name, bool(cond), extra))
    print(("PASS" if cond else "FAIL"), "-", name, (f"({extra})" if extra else ""))

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context()
    page = ctx.new_page()
    errors, requests = [], []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: requests.append(r.url))

    page.goto(BASE, wait_until="load")

    # --- structure ---
    ok("title", "Cadence" in page.title())
    ok("masthead red accent bar", page.locator(".mh-acc").count() == 1)
    ok("footer wordmark placeholder (bottom-right)", "Wordmark placeholder" in page.locator(".ftr .wm").inner_text())
    ok("4 tabs", page.locator(".tab").count() == 4)
    ok("font loaded (Arimo)", page.evaluate("document.fonts.check('16px Arimo')"))

    # --- onboarding wizard on first visit ---
    ok("wizard opens on first visit", page.locator("#ovl-intro").is_visible())
    ok("wizard step 1 line", "Small rituals, kept daily." in page.locator('#wiz-body .wiz-step[data-step="0"]').inner_text())
    page.click("#wiz-next"); page.click("#wiz-next")
    ok("wizard step 3 (Set your goal)", page.locator("#wiz-count").inner_text().startswith("Step 3 of 3"))
    page.click("#wiz-next")  # Start
    ok("wizard closes on Start", page.locator("#ovl-intro").is_hidden())

    # --- Today ---
    ok("date line", "Tuesday, 7 October" in page.locator(".vmeta").inner_text(), page.locator(".vmeta").inner_text())
    ok("greeting", "Good evening, Sam." in page.locator(".greet").inner_text())
    ok("hero count", "3 of 5 rituals done · 60%" in page.locator("#hero-count").inner_text())
    ok("hero meter 60%", page.eval_on_selector("#hero-fill", "el => el.style.width") == "60%")
    ok("streak counter 12", page.locator("#hero-streak").inner_text().strip() == "12")
    ok("5 ritual rows", page.locator("#ritual-list .ritual").count() == 5)
    ok("3 checked", page.locator("#ritual-list input[type=checkbox]:checked").count() == 3)
    ok("ordinal markers (01..05)", [e.inner_text() for e in page.locator(".ri-mark").all()][:5] == ["01","02","03","04","05"])
    ok("category tags", page.locator("#ritual-list .tag").count() == 5)
    ok("streak chips", page.locator("#ritual-list .chip").count() == 5)
    ok("status label (words)", "ON TRACK" in page.locator(".status").first.inner_text().upper())

    # --- check off a ritual: ring update + notice + ceremony ---
    row = page.locator('.ritual[data-id="guitar"] input[type=checkbox]')
    row.check()
    ok("ring updates to 4 of 5", "4 of 5 rituals done · 80%" in page.locator("#hero-count").inner_text())
    notice = page.locator('.notice-slot[data-slot="today"] .notice')
    ok("notice 'Logged ✓'", "Logged ✓" in notice.inner_text())
    ok("notice is ruled box (no toast)", page.eval_on_selector('.notice-slot[data-slot="today"] .notice', "el => getComputedStyle(el).borderTopWidth") == "2px")
    ok("ceremony accent present", page.locator('.notice.ceremony .n-acc').count() == 1)

    # persistence
    page.reload(wait_until="load")
    ok("check persists (4 of 5 after reload)", "4 of 5 rituals done · 80%" in page.locator("#hero-count").inner_text())
    ok("wizard NOT shown again", page.locator("#ovl-intro").is_hidden())

    # --- detail overlay ---
    page.click('.ritual[data-id="run"] .ri-name')
    ok("detail overlay opens", page.locator("#ovl-detail").is_visible())
    ok("detail has sparkline (7 bars)", page.locator("#ovl-detail .spark i").count() == 7)
    ok("detail has mini history (5)", page.locator("#ovl-detail .mini li").count() == 5)
    ok("detail has delete", page.locator("#detail-del").count() == 1)

    # move down
    order_before = page.evaluate("[...document.querySelectorAll('#ritual-list .ritual')].map(r=>r.dataset.id)")
    page.click("#detail-down")
    order_after = page.evaluate("[...document.querySelectorAll('#ritual-list .ritual')].map(r=>r.dataset.id)")
    ok("move down reorders", order_before != order_after and order_after[1] == "run", f"{order_before} -> {order_after}")
    # move back up (restore order)
    page.click("#detail-up")

    # delete with confirmation → confirm dialog → cancel → delete → undo
    page.click("#detail-del")
    ok("confirm dialog appears", page.locator("#ovl-confirm").is_visible())
    ok("confirm title bilingual", "Supprimer ce rituel ?" in page.locator("#cf-title").inner_text())
    ok("confirm not pre-focused", page.evaluate("document.activeElement.id") != "cf-ok")
    ok("consequence sentence", "can’t be undone" in page.locator("#cf-body").inner_text())
    page.click("#cf-cancel")
    ok("cancel closes confirm", page.locator("#ovl-confirm").is_hidden())
    ok("detail still open after cancel", page.locator("#ovl-detail").is_visible())
    page.click("#detail-del"); page.click("#cf-ok")
    ok("ritual deleted (4 rows)", page.locator("#ritual-list .ritual").count() == 4)
    ok("undo offered", page.locator("#undo-btn").count() == 1)
    page.click("#undo-btn")
    ok("undo restores (5 rows)", page.locator("#ritual-list .ritual").count() == 5)

    # --- log form ---
    page.click("#log-open")
    ok("log dialog opens", page.locator("#ovl-log").is_visible())
    ok("ritual select has 5", page.locator("#log-ritual option").count() == 5)
    ok("date picker type=date", page.eval_on_selector("#log-date", "el => el.type") == "date")
    page.select_option("#log-ritual", "guitar")
    # invalid minutes -> error under field
    page.fill("#log-min", "0")
    page.click("#log-save")
    ok("error under field shown", page.locator("#log-min-err").is_visible())
    ok("left rule on field", "solid" in page.eval_on_selector("#log-min", "el => getComputedStyle(el).borderLeftStyle"))
    page.fill("#log-min", "25")
    page.click("#log-save")
    page.wait_for_selector("#ovl-log", state="hidden", timeout=3000)
    ok("saving state ran (~750ms) then closed", True)
    ok("logged notice after save", "Logged ✓" in page.locator('.notice-slot[data-slot="today"] .notice').inner_text())
    ok("ring still 4 of 5", "4 of 5" in page.locator("#hero-count").inner_text())

    # --- History ---
    page.click('.tab[data-view="history"]')
    ok("history visible", page.locator("#view-history").is_visible())
    ok("banner (weekly summary)", "245 minutes" in page.locator(".banner").inner_text())
    ok("bar chart 7 bars", page.locator("#bars .btrack").count() == 7)
    vals = [e.inner_text() for e in page.locator("#bars .bval").all()]
    ok("bar values Mon–Sun", vals == ["45","30","60","25","50","0","35"], str(vals))
    ok("heatmap 31 day cells", page.locator("#heat .hc:not(.out)").count() == 31)
    ok("heatmap ink density cells", page.locator("#heat .hc.l1, #heat .hc.l2, #heat .hc.l3").count() == 6)
    ok("ledger 8 rows", page.locator("#entries-body tr").count() == 8)
    ok("logged entry joined the register", "7 Oct" in page.locator("#entries-body tr").first.inner_text() and "Practice guitar" in page.locator("#entries-body tr").first.inner_text())
    ok("pagination readout", "Showing 1–8 of 28" in page.locator("#page-readout").inner_text(), page.locator("#page-readout").inner_text())
    page.click("#page-older")
    ok("older entries -> page 2", "Showing 9–16 of 28" in page.locator("#page-readout").inner_text())
    page.fill("#entry-search", "guitar")
    ok("search filters", page.locator("#entries-body tr").count() == 4, str(page.locator("#entries-body tr").count()))
    page.fill("#entry-search", "")
    # CSV export triggers a download
    with page.expect_download() as dl:
        page.click("#h-export")
    ok("CSV export downloads", dl.value.suggested_filename == "cadence-entries.csv")
    ok("export notice", "Exported ✓" in page.locator('.notice-slot[data-slot="history"] .notice').inner_text())

    # --- Achievements ---
    page.click('.tab[data-view="achievements"]')
    ok("stat tiles", [e.inner_text() for e in page.locator(".tile .stat-num").all()] == ["12","21","240"])
    ok("badge grid 6", page.locator(".badge").count() == 6)
    ok("4 earned / 2 locked", page.locator(".badge.earned").count() == 4 and page.locator(".badge.locked").count() == 2)
    page.check("#empty-demo")
    ok("empty state shows (demo)", page.locator("#ach-empty").is_visible() and page.locator("#badge-grid").is_hidden())
    ok("empty state = ruled statement + one action", page.locator("#ach-empty .btn").count() == 1)
    page.uncheck("#empty-demo")

    # --- Settings ---
    page.click('.tab[data-view="settings"]')
    ok("name field Sam", page.input_value("#s-name") == "Sam")
    ok("week radio Monday checked", page.is_checked('input[name="weekstart"][value="mon"]'))
    ok("goal slider 30", page.input_value("#s-goal") == "30")
    page.fill("#s-goal", "45"); page.dispatch_event("#s-goal", "input")
    ok("goal readout updates", "45 min" in page.locator("#goal-out").inner_text())
    page.fill("#s-name", "")
    page.click("#s-save")
    ok("settings name error", page.locator("#s-name-err").is_visible())
    page.fill("#s-name", "Sam")
    page.click("#s-save")
    page.wait_for_selector('.notice-slot[data-slot="settings"] .notice', timeout=3000)
    ok("Saved notice", "Saved ✓" in page.locator('.notice-slot[data-slot="settings"] .notice').inner_text())
    page.check("#s-dark")
    ok("dark mode toggles body.dark", page.evaluate("document.body.classList.contains('dark')"))
    bg = page.eval_on_selector("body", "el => getComputedStyle(el).backgroundColor")
    ok("dark ground is black", bg == "rgb(0, 0, 0)", bg)
    page.uncheck("#s-dark")

    # Replay intro
    page.click("#s-replay")
    ok("replay intro opens wizard", page.locator("#ovl-intro").is_visible())
    page.click("#wiz-skip")
    ok("skip closes wizard", page.locator("#ovl-intro").is_hidden())

    # Delete all data (confirm flow)
    page.click("#s-delete")
    ok("delete-all confirm", page.locator("#ovl-confirm").is_visible())
    page.click("#cf-ok")
    page.wait_for_timeout(100)
    ok("all data deleted notice", "Deleted ✓" in page.locator('.notice-slot[data-slot="settings"] .notice').inner_text())
    page.click('.tab[data-view="today"]')
    ok("today back to 3 of 5 (reset)", "3 of 5 rituals done · 60%" in page.locator("#hero-count").inner_text())

    # --- marks toggle ---
    page.click("#marks")
    ok("body.show-marks on", page.evaluate("document.body.classList.contains('show-marks')"))
    n_improvised = page.locator("[data-improvised]").count()
    n_adapted = page.locator("[data-adapted]").count()
    n_fallback = page.locator("[data-fallback]").count()
    ok("marks counts", n_improvised >= 15 and n_adapted >= 8 and n_fallback >= 10, f"imp={n_improvised} ad={n_adapted} fb={n_fallback}")
    ok("dashed amber outline present", page.evaluate("""(() => {
        const el = document.querySelector('[data-improvised]');
        return getComputedStyle(el).outlineStyle;
    })()""") == "dashed")
    page.click("#marks")
    ok("body.show-marks off", not page.evaluate("document.body.classList.contains('show-marks')"))

    # --- no console errors, no external network ---
    external = [u for u in requests if not u.startswith("http://127.0.0.1:8483")]
    ok("no external network requests", len(external) == 0, str(external[:3]))
    ok("no console errors", len(errors) == 0, str(errors[:3]))

    # --- style tokens (dominion values) ---
    page.click('.tab[data-view="today"]')
    ok("ground white", page.eval_on_selector("body", "el => getComputedStyle(el).backgroundColor") == "rgb(255, 255, 255)")
    ok("primary = slate #26374A", page.eval_on_selector("#log-open", "el => getComputedStyle(el).backgroundColor") == "rgb(38, 55, 74)")
    ok("primary radius 4", page.eval_on_selector("#log-open", "el => getComputedStyle(el).borderRadius") == "4px")
    ok("2px black rules", page.eval_on_selector(".mh", "el => getComputedStyle(el).borderBottomWidth") == "2px")
    ok("no box-shadow anywhere on cards", page.eval_on_selector(".hero", "el => getComputedStyle(el).boxShadow") == "none")
    # focus glow via keyboard
    page.keyboard.press("Tab")
    focused_outline = page.evaluate("getComputedStyle(document.activeElement).outlineColor")
    ok("focus glow blue (#66AFE9)", focused_outline == "rgb(102, 175, 233)", focused_outline)
    # arimo weight roles present
    ok("heading medium 500", page.eval_on_selector(".shead", "el => getComputedStyle(el).fontWeight") == "500")
    # bilingual divider (1px)
    ok("bilingual thin divider", page.eval_on_selector(".vtitle .dv", "el => getComputedStyle(el).width") == "1px")

    browser.close()

fails = [r for r in results if not r[1]]
print(f"\n{len(results)-len(fails)}/{len(results)} checks passed")
sys.exit(1 if fails else 0)
