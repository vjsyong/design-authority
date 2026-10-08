#!/usr/bin/env python3
"""Headless render + functional probe for the adversarial leader copy.
Captures: console errors, computed-style evidence for each attack, screenshots.
Run: PLAYWRIGHT_BROWSERS_PATH=... .venv/bin/python3 probe-render.py
"""
import json, os, socket, subprocess, sys, time
from playwright.sync_api import sync_playwright

REPO = '/home/xrim/design-authority'
TARGET = os.path.join(REPO, 'docs/verification/adversarial/hacked-leader')
SHOTS = os.path.join(TARGET, '_evidence/screens')
os.makedirs(SHOTS, exist_ok=True)

s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
proc = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1',
                         '--directory', TARGET], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
url = f'http://127.0.0.1:{port}/index.html'
for _ in range(50):
    try:
        import urllib.request; urllib.request.urlopen(url, timeout=1); break
    except Exception:
        time.sleep(0.1)

errors = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_context(viewport={'width': 1280, 'height': 900}).new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda m: errors.append('console:' + m.text) if m.type == 'error' else None)
    page.goto(url, wait_until='load')
    page.wait_for_timeout(400)

    ev = page.evaluate("""(() => {
      const firstBtn = document.querySelector('.btn');
      const skip = document.querySelector('.skip-link');
      const cs = e => e ? getComputedStyle(e) : null;
      const onTrack = document.querySelector('.tag.ok');
      const okcs = cs(onTrack);
      const wn = document.querySelector('#week-notice');
      const wncs = cs(wn);
      const sb = document.querySelector('.searchbox');
      const toast = document.querySelector('#toast');
      const rstate = document.querySelector('.rstate');
      return {
        first_btn_class: firstBtn && firstBtn.className,
        first_btn_radius: cs(firstBtn) && cs(firstBtn).borderRadius,
        skip_radius: cs(skip) && cs(skip).borderRadius,
        skip_rect: skip ? skip.getBoundingClientRect().width + 'x' + skip.getBoundingClientRect().height : null,
        log_mins_radius: cs(document.querySelector('#log-mins')) && cs(document.querySelector('#log-mins')).borderRadius,
        other_btn_radius: (() => { const b = document.querySelector('#log-save') || document.querySelectorAll('.btn')[2]; return b ? cs(b).borderRadius : null; })(),
        ontrack_visible: !!onTrack,
        ontrack_color: okcs && okcs.color,
        ontrack_bg: okcs && okcs.backgroundColor,
        week_notice_bgcolor: wncs && wncs.backgroundColor,
        week_notice_bgimage: wncs && wncs.backgroundImage.slice(0, 90),
        week_notice_color: wncs && wncs.color,
        searchbox_shadow: cs(sb) && cs(sb).boxShadow,
        placeholder: document.querySelector('#search').placeholder,
        avatar_title: document.querySelector('.avatar').title,
        brand_svg: !!document.querySelector('.brand svg'),
        toast_display: cs(toast) && cs(toast).display,
        rstate_animation: cs(rstate) && cs(rstate).animationName + ' ' + (cs(rstate) && cs(rstate).animationDuration),
        focus_outline_global: (() => { return getComputedStyle(document.documentElement).getPropertyValue('--x') || 'n/a'; })(),
        ferr_present: !!document.querySelector('.ferr'),
        err_present: !!document.querySelector('.err'),
      };
    })()""")
    ev['page_title'] = page.title()

    # dismiss wizard (normal user flow)
    page.evaluate("document.querySelector('#wz-skip') && document.querySelector('#wz-skip').click()")
    page.wait_for_timeout(300)
    # screenshot the default view as the deliverable
    shot1 = os.path.join(SHOTS, 'adversarial-leader.png')
    page.screenshot(path=shot1)

    # functional check 1: log flow -> toast
    page.evaluate("document.querySelector('#row-r3 [data-log]').click()")
    page.wait_for_timeout(200)
    page.evaluate("document.querySelector('#log-save').click()")
    page.wait_for_timeout(1100)
    toast_state = page.evaluate("""(() => { const t = document.querySelector('#toast');
        const cs = getComputedStyle(t); return {display: cs.display, text: t.textContent, position: cs.position,
        bottom: cs.bottom, shadow: cs.boxShadow, anim: cs.animationName}; })()""")
    shot2 = os.path.join(SHOTS, 'toast-visible.png')
    page.screenshot(path=shot2)

    # functional check 2: details panel + red confirm flow
    page.wait_for_timeout(3000)  # let toast auto-hide
    toast_after = page.evaluate("getComputedStyle(document.querySelector('#toast')).display")
    page.evaluate("document.querySelector('#row-r1 [data-details]').click()")
    page.wait_for_timeout(250)
    details_open = page.evaluate("!document.getElementById('details-panel').hidden")
    page.evaluate("document.getElementById('remove-start').click()")
    page.wait_for_timeout(150)
    confirm_open = page.evaluate("!document.getElementById('confirm-zone').hidden")
    page.evaluate("document.getElementById('confirm-keep').click()")

    # functional check 3: view switch
    page.evaluate("document.querySelector('[data-view=history]').click()")
    page.wait_for_timeout(200)
    hist_visible = page.evaluate("!document.getElementById('view-history').hidden && document.getElementById('view-today').hidden")
    page.evaluate("document.querySelector('[data-view=achievements]').click()")
    page.wait_for_timeout(200)
    ach_visible = page.evaluate("!document.getElementById('view-achievements').hidden")

    # computed border-radius sanity for a revealed view button
    btn_r2 = page.evaluate("getComputedStyle(document.querySelector('#export-csv')).borderRadius")

    browser.close()
proc.terminate()

print(json.dumps({
    'evidence': ev,
    'functional': {'details_open': details_open, 'confirm_open': confirm_open,
                   'history_visible': hist_visible, 'achievements_visible': ach_visible,
                   'export_btn_radius': btn_r2, 'toast_after_timeout': toast_after},
    'toast': toast_state,
    'console_errors': errors[:10],
    'screenshots': [shot1, shot2],
}, indent=1))
