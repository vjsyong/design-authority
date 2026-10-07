#!/usr/bin/env python3
"""Interactive checks for the Depot reference app (Orbit spike, Phase 6)."""
import argparse
import json
import sys

from playwright.sync_api import sync_playwright


def run_checks(url, out):
    checks = []

    def ck(name, ok, detail=""):
        checks.append({"name": name, "ok": bool(ok), "detail": str(detail)[:200]})

    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page(viewport={"width": 1440, "height": 900})
        native_dialogs = []
        pg.on("dialog", lambda d: (native_dialogs.append(d.type), d.dismiss()))

        # 1 · register
        pg.goto(url + "/items", wait_until="load")
        ck("register.main", pg.locator("main[data-view=register]").count() >= 1)
        rows = pg.locator("[data-item]")
        ck("register.rows>=5", rows.count() >= 5, rows.count())
        ck("register.status-overdue-visible", pg.locator("[data-status=overdue]").count() >= 1)

        # 2 · navigation from register to detail
        pg.locator("[data-item] a").first.click()
        pg.wait_for_load_state("load")
        ck("nav.register->detail", pg.locator("main[data-view=detail]").count() >= 1)

        # 3 · checkout + return on an available item (id 5)
        pg.goto(url + "/items/5", wait_until="load")
        sel = pg.locator("select[name=borrower]")
        if sel.count():
            try:
                sel.first.select_option(index=0)
            except Exception:
                pass
        days = pg.locator("input[name=days]")
        if days.count():
            days.first.fill("7")
        co = pg.locator("button[name=checkout]")
        if co.count() == 0:
            co = pg.locator("button", has_text="Check")
        if co.count():
            co.first.click()
            pg.wait_for_load_state("load")
            ck("flow.checkout->on_loan", pg.locator("[data-status=on_loan]").count() >= 1)
            rb = pg.locator("button[name=return]")
            if rb.count() == 0:
                rb = pg.locator("button", has_text="Return")
            if rb.count():
                rb.first.click()
                pg.wait_for_load_state("load")
                ck("flow.return->available", pg.locator("[data-status=available]").count() >= 1)
            else:
                ck("flow.return->available", False, "no return control")
        else:
            ck("flow.checkout->on_loan", False, "no checkout control")

        # 4 · create item
        pg.goto(url + "/items/new", wait_until="load")
        ck("form.main", pg.locator("main[data-view=form]").count() >= 1)
        pg.fill("input[name=name]", "Test drill")
        pg.locator("button[type=submit]").first.click()
        pg.wait_for_load_state("load")
        ck("flow.create", "Test drill" in pg.content())
        created_url = pg.url

        # 5 · retire must confirm before acting (dialog element or native confirm)
        pg.goto(created_url, wait_until="load")
        del native_dialogs[:]
        clickable = pg.locator("[data-action=retire]")
        if clickable.count():
            clickable.first.click()
            pg.wait_for_timeout(500)
            confirm_seen = bool(native_dialogs) or pg.locator("[role=dialog], dialog[open]").count() > 0
            ck("destructive.confirms", confirm_seen,
               "native=%s dom=%s" % (native_dialogs, pg.locator("[role=dialog], dialog[open]").count()))
        else:
            ck("destructive.confirms", False, "no [data-action=retire] control found")

        # 6 · activity: start job, follow progress, complete
        pg.goto(url + "/activity", wait_until="load")
        ck("activity.main", pg.locator("main[data-view=activity]").count() >= 1)
        start = pg.locator("button[name=import]")
        if start.count() == 0:
            start = pg.locator("button", has_text="Start")
        if start.count():
            start.first.click()
            pg.wait_for_load_state("load")
            pg.wait_for_timeout(1500)
            pg.reload(wait_until="load")
            pb = pg.locator("[role=progressbar]")
            ck("activity.progressbar", pb.count() >= 1)
            now1 = pg.locator("[aria-valuenow]").first.get_attribute("aria-valuenow") if pb.count() else None
            pg.wait_for_timeout(4000)
            pg.reload(wait_until="load")
            now2 = pg.locator("[aria-valuenow]").first.get_attribute("aria-valuenow") if pg.locator("[aria-valuenow]").count() else None
            ck("activity.progress-advances", now1 is not None and now2 is not None and int(now2) > int(now1),
               "now1=%s now2=%s" % (now1, now2))
            deadline = 20
            st = ""
            while deadline > 0:
                st = pg.locator("[data-job-state]").first.get_attribute("data-job-state") if pg.locator("[data-job-state]").count() else ""
                if st == "complete":
                    break
                pg.wait_for_timeout(1200)
                pg.reload(wait_until="load")
                deadline -= 1
            ck("activity.completes", st == "complete", st)
        else:
            ck("activity.progressbar", False, "no start control")

        # 7 · mobile width
        m = browser.new_page(viewport={"width": 380, "height": 820})
        m.goto(url + "/items", wait_until="load")
        ck("mobile.register-renders", m.locator("[data-item]").count() >= 5)
        overflow = m.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        ck("mobile.no-horizontal-overflow", overflow <= 4, "overflow=%spx" % overflow)

        browser.close()

    passed = sum(1 for c in checks if c["ok"])
    result = {"passed": passed, "total": len(checks), "checks": checks}
    with open(out, "w") as fh:
        json.dump({"result": result}, fh, indent=1)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    res = run_checks(args.url, args.out)
    print("interact: %s/%s" % (res["passed"], res["total"]))
    for c in res["checks"]:
        if not c["ok"]:
            print("  FAIL", c["name"], "-", c["detail"])
    sys.exit(0 if res["passed"] == res["total"] else 1)
