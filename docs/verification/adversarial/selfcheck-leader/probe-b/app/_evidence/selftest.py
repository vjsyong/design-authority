#!/usr/bin/env python3
"""Cadence v3 self-test — Playwright pass over all views, flows, marks, persistence."""
import sys
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8482/'
results = []
def check(name, cond, extra=''):
    results.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), '-', name, ('| ' + repr(extra) if extra != '' else ''))

errors = []
req_fail = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
    page = ctx.new_page()
    page.on('console', lambda m: errors.append('console.error: ' + m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))
    page.on('requestfailed', lambda r: req_fail.append(r.url))
    page.goto(BASE)
    page.wait_for_load_state('networkidle')
    page.evaluate("document.fonts.ready")

    # 0. fonts + wizard on first run
    page.evaluate("""async () => { await Promise.all([
        document.fonts.load('16px "Gelasio"'),
        document.fonts.load('16px "Inter"'),
        document.fonts.load('16px "Archivo Black"')]); }""")
    fonts = page.evaluate("""() => ({
        gelasio: document.fonts.check('16px "Gelasio"'),
        inter: document.fonts.check('16px "Inter"'),
        archivo: document.fonts.check('16px "Archivo Black"')})""")
    check('three registers load (Gelasio/Inter/Archivo Black)', all(fonts.values()), fonts)
    check('wizard auto-opens on first run', page.is_visible('#wizard-panel'))
    check('wizard shows Step 1 of 3', page.text_content('#wizard-steplab').strip() == 'Step 1 of 3')
    page.click('#wz-next')
    check('wizard step 2 shows ritual radios', page.is_visible('input[name="wz-ritual"]'))
    page.check('input[name="wz-ritual"][value="w3"]')
    page.click('#wz-next')
    check('wizard step 3 shows goal slider', page.is_visible('#wz-goal'))
    page.eval_on_selector('#wz-goal', "el => { el.value = '60'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
    page.click('#wz-finish')
    check('wizard closes after finish', page.is_hidden('#wizard-panel'))
    st = page.evaluate("window.__cadence.state()")
    check('wizard added the chosen ritual', any(r['name'] == 'Room reset' for r in st['rituals']) and len(st['rituals']) == 6)
    check('wizard set the goal (60)', st['prefs']['goal'] == 60)
    check('setup notice shown', page.is_visible('#setup-notice'))

    # 1. state + fixtures
    check('week sums = [66, 84, 37, 0, 0, 0, 0]', page.evaluate("window.__cadence.weekSums()") == [66, 84, 37, 0, 0, 0, 0])
    check('streak = 12', page.evaluate("window.__cadence.streak()") == 12)
    check('total logs = 101', page.evaluate("window.__cadence.totalLogs()") == 101)

    # 2. Today view
    check('meter readout 2 of 5', page.text_content('#meter-readout').strip() == '2 of 5 rituals \u00b7 37 minutes logged', page.text_content('#meter-readout'))
    check('week notice numbers', '187 minutes' in page.text_content('#week-notice-text') and '12' in page.text_content('#week-notice-text'))
    check('week notice is a ruled notice', page.eval_on_selector('#week-notice', "e => getComputedStyle(e).borderTop") == '2px solid rgb(26, 26, 26)')
    rows = page.eval_on_selector_all('#ritual-list .rrow', "els => els.map(e => e.id)")
    check('six ritual rows', rows == ['row-r1', 'row-r2', 'row-r3', 'row-r4', 'row-r5', 'row-r6'], rows)
    slip = page.eval_on_selector_all('#ritual-list .tag.attn', "els => els.map(e => ({t: e.textContent.trim(), bg: getComputedStyle(e).backgroundColor}))")
    check('one SLIPPING tag (Piano), solid red', len(slip) == 1 and slip[0]['t'].lower() == 'slipping' and slip[0]['bg'] == 'rgb(227, 18, 11)', slip)
    ontrack = page.eval_on_selector_all('#ritual-list .tag:not(.attn)', "els => els.map(e => e.textContent.trim().toLowerCase())")
    check('ON TRACK tags present', ontrack.count('on track') >= 4, ontrack)
    check('glyph marks render per ritual', page.eval_on_selector_all('#ritual-list .glyph', "els => els.length") == 6)
    check('search cursor motif in navbar', page.is_visible('.searchbox .cursor'))

    # 3. History — bar chart exact values
    page.click('.tab[data-view="history"]')
    check('history tab switches view', page.is_visible('#view-history') and page.is_hidden('#view-today'))
    bars = page.eval_on_selector_all('#chart-area .bar', "els => els.map(e => e.getAttribute('data-value'))")
    check('bar data-values exact', bars == ['66', '84', '37', '0', '0', '0', '0'], bars)
    check('today bar red', page.eval_on_selector('#chart-area .bar.today', "e => getComputedStyle(e).backgroundColor") == 'rgb(227, 18, 11)')
    check('series bars Chicago blue', page.eval_on_selector('#chart-area .barcol:nth-child(1) .bar', "e => getComputedStyle(e).backgroundColor") == 'rgb(46, 69, 184)')
    check('chart baseline is 2px ink origin rule', page.eval_on_selector('#chart-area', "e => getComputedStyle(e).borderBottom") == '2px solid rgb(26, 26, 26)')

    # 4. History — heatmap
    check('month grid 35 cells', page.eval_on_selector_all('#month-grid .mcell', "els => els.length") == 35)
    today_cell = page.eval_on_selector('#month-grid .mcell[data-date="2026-10-07"]', "e => ({cls: e.className, bg: getComputedStyle(e).backgroundColor, mn: e.getAttribute('data-min')})")
    check('today cell red with 37 min', 'todayc' in today_cell['cls'] and today_cell['bg'] == 'rgb(227, 18, 11)' and today_cell['mn'] == '37', today_cell)
    check('outside-month cells dimmed (4)', page.eval_on_selector_all('#month-grid .mcell.outside', "els => els.length") == 4)
    check('intensity classes present (i1/i2/i3)', page.evaluate("['i1','i2','i3'].every(c => document.querySelector('#month-grid .' + c))"))

    # 5. sparkline + ledger + pager
    spark = page.eval_on_selector_all('#spark-main i', "els => els.map(e => e.getAttribute('data-value'))")
    check('sparkline 7 columns exact', spark == ['52', '88', '37', '39', '66', '84', '37'], spark)
    check('sparkline readout 403', page.text_content('#spark-readout').strip().startswith('403 minutes'))
    check('ledger sub = 101 entries', page.text_content('#ledger-sub').strip().startswith('101 entries'))
    check('ledger page shows 8 rows', page.eval_on_selector_all('#ledger-body tr', "els => els.length") == 8)
    check('pager = Page 1 of 13', page.text_content('#pg-readout').strip() == 'Page 1 of 13', page.text_content('#pg-readout'))
    first = page.eval_on_selector('#ledger-body tr', "tr => Array.from(tr.children).map(td => td.textContent.trim())")
    check('newest entry is 7 Oct / Morning stretch / 12', first[:3] == ['7 Oct 2026', 'Morning stretch', '12'], first)
    page.click('#pg-older')
    check('pager advances to page 2', page.text_content('#pg-readout').strip() == 'Page 2 of 13')
    page.click('#pg-newer')

    # 6. Achievements
    page.click('.tab[data-view="achievements"]')
    check('streak display shows 12', page.text_content('#streak-num').strip() == '12')
    check('streak note names 26 September', '26 September' in page.text_content('#streak-note'))
    badges = page.eval_on_selector_all('#badges .badge', "els => els.map(e => ({t: e.textContent, earned: e.classList.contains('earned'), bg: getComputedStyle(e).backgroundColor}))")
    check('three badges render', len(badges) == 3, badges)
    check('7 DAYS badge earned, solid ink', badges[0]['earned'] and badges[0]['bg'] == 'rgb(26, 26, 26)' and '7 Days' in badges[0]['t'], badges[0])
    check('30 DAYS in progress (12 of 30)', (not badges[1]['earned']) and '12 of 30' in badges[1]['t'])
    check('150 LOGS in progress (101 of 150)', '101 of 150' in badges[2]['t'])

    # 7. marks toggle
    page.click('.tab[data-view="today"]')
    n_marked = page.evaluate("document.querySelectorAll('[data-improvised],[data-adapted],[data-fallback]').length")
    check('marked nodes exist (>= 25)', n_marked >= 25, n_marked)
    page.click('#marks-toggle')
    page.wait_for_timeout(120)
    n_labels = page.evaluate("document.querySelectorAll('.mark-lbl').length")
    check('toggle labels every marked node', n_labels == n_marked, (n_marked, n_labels))
    lbl = page.text_content('#completion .mark-lbl')
    check('completion label reads adapted · ring → meter', lbl.startswith('adapted') and 'ring \u2192 meter' in lbl, lbl)
    put = page.eval_on_selector('#completion', "e => getComputedStyle(e).outlineStyle + ' ' + getComputedStyle(e).outlineColor")
    check('dashed amber outline on marked node', put == 'dashed rgb(178, 106, 0)', put)
    check('toggle aria-pressed true', page.get_attribute('#marks-toggle', 'aria-pressed') == 'true')
    page.click('#marks-toggle')

    # 8. save flow (log ritual)
    page.click('#row-r3 [data-log]')
    check('log panel opens', page.is_visible('#log-panel'))
    check('date prefilled today', page.input_value('#log-date') == '2026-10-07')
    check('minutes prefilled target 30', page.input_value('#log-mins') == '30')
    page.fill('#log-mins', '')
    page.click('#log-save')
    check('error shows under field on empty minutes', page.is_visible('#log-mins-err'))
    check('no save happened on error', page.evaluate("window.__cadence.state().logs['2026-10-07']['r3']") is None)
    page.fill('#log-mins', '34')
    page.fill('#log-notes', 'Around the park')
    page.click('#log-save')
    page.wait_for_selector('#save-readout:has-text("Saving")', timeout=2000)
    page.wait_for_selector('#save-readout:has-text("Saved")', timeout=3000)
    check('saved readout shown', '34 min' in page.text_content('#save-readout'))
    check('state records 34 min', page.evaluate("window.__cadence.state().logs['2026-10-07']['r3']") == 34)
    check('note stored', page.evaluate("window.__cadence.state().notes['2026-10-07|r3']") == 'Around the park')
    check('meter now 3 of 5 · 71 minutes', page.text_content('#meter-readout').strip() == '3 of 5 rituals \u00b7 71 minutes logged', page.text_content('#meter-readout'))
    check('bar today now 71', page.eval_on_selector('#chart-area .bar.today', "e => e.getAttribute('data-value')") == '71')
    check('log notice ruled + copy', '34 minutes' in page.text_content('#log-notice-text') and '12 days' in page.text_content('#log-notice-text'))
    check('celebration static-flip node on r3 row', 'celebration' in page.eval_on_selector_all('#row-r3 [data-adapted]', "els => els.map(e => e.getAttribute('data-note')).join('|')"))
    page.click('#log-cancel')
    check('log panel closes', page.is_hidden('#log-panel'))

    # 9. details flow + destructive + undo
    page.click('#row-r4 [data-details]')
    check('details panel opens', page.is_visible('#details-panel'))
    check('category select prefilled Mind', page.input_value('#d-cat') == 'Mind')
    page.select_option('#d-cat', 'Craft')
    page.wait_for_timeout(80)
    check('category edit persists to state', page.evaluate("window.__cadence.state().rituals.find(r => r.id === 'r4').cat") == 'Craft')
    check('updated notice appears', page.text_content('#log-notice-lab') == 'Updated')
    check('frequency radios present (3)', page.eval_on_selector_all('#details-body .radio-set input', "els => els.length") == 3)
    page.check('input[name="d-freq"][value="weekdays"]')
    check('frequency edit persists', page.evaluate("window.__cadence.state().rituals.find(r => r.id === 'r4').freq") == 'weekdays')
    page.uncheck('#d-rem')
    check('reminders checkbox edit persists', page.evaluate("window.__cadence.state().rituals.find(r => r.id === 'r4').remind") == False)
    check('details sparkline 7 cols', page.eval_on_selector_all('#details-body .spark i', "els => els.length") == 7)
    page.click('#remove-start')
    check('confirm zone appears inline', page.is_visible('#confirm-zone'))
    focus = page.evaluate("document.activeElement ? document.activeElement.id : ''")
    check('destructive control not pre-focused', focus != 'confirm-remove', focus)
    page.click('#confirm-keep')
    check('keep hides the confirm', page.is_hidden('#confirm-zone'))
    page.click('#remove-start')
    page.click('#confirm-remove')
    check('ritual removed from state', page.evaluate("window.__cadence.state().rituals.length") == 5)
    check('undo notice shows', page.is_visible('#undo-notice'))
    check('details panel closed after removal', page.is_hidden('#details-panel'))
    page.click('#undo-btn')
    check('undo restores the ritual', page.evaluate("window.__cadence.state().rituals.length") == 6)
    check('undo notice dismissed', page.is_hidden('#undo-notice'))

    # 10. Settings
    page.click('.tab[data-view="settings"]')
    check('toggle checked by default', page.is_checked('#pref-remind'))
    page.uncheck('#pref-remind')
    check('toggle flip persists', page.evaluate("window.__cadence.state().prefs.remind") == False)
    page.eval_on_selector('#pref-goal', "el => { el.value = '75'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
    check('goal readout updates', page.text_content('#goal-readout').strip() == '75 min')
    check('goal persists to state', page.evaluate("window.__cadence.state().prefs.goal") == 75)
    check('theme readout states Light only', 'Light only' in page.text_content('#theme-readout'))
    order_before = page.evaluate("window.__cadence.state().rituals.map(r => r.id)")
    page.click('#order-list li:nth-child(3) [data-move="-1"]')
    order_after = page.evaluate("window.__cadence.state().rituals.map(r => r.id)")
    check('move-up control reorders', order_after[1] == 'r3' and order_after[2] == 'r2', order_after)
    page.click('.tab[data-view="today"]')
    today_ids = page.eval_on_selector_all('#ritual-list .rrow', "els => els.map(e => e.id)")
    check('today list follows new order', today_ids[:3] == ['row-r1', 'row-r3', 'row-r2'], today_ids)
    page.click('.tab[data-view="settings"]')
    g_before = page.evaluate("window.__cadence.state().rituals.find(r => r.id === 'r1').glyph")
    page.click('#marks-list li:nth-child(1) [data-mark]')
    g_after = page.evaluate("window.__cadence.state().rituals.find(r => r.id === 'r1').glyph")
    check('mark cycler advances glyph', g_after == (g_before + 1) % 6, (g_before, g_after))
    with page.expect_download() as dl:
        page.click('#export-csv')
    check('CSV download fires (cadence-log.csv)', dl.value.suggested_filename == 'cadence-log.csv')

    # 11. search + empty state
    page.click('.tab[data-view="today"]')
    page.fill('#search', 'walk')
    rows = page.eval_on_selector_all('#ritual-list .rrow', "els => els.map(e => e.id)")
    check('search filters to the walk ritual', rows == ['row-r3'], rows)
    page.fill('#search', 'zzz')
    check('empty state appears when nothing matches', page.is_visible('#empty-state'))
    check('empty copy is declarative', 'Nothing matches' in page.text_content('#empty-line'))
    page.click('#empty-clear')
    check('clear search restores list', page.eval_on_selector_all('#ritual-list .rrow', "els => els.length") == 6)
    check('search input cleared', page.input_value('#search') == '')

    # 12. persistence across reload
    page.reload()
    page.wait_for_load_state('networkidle')
    check('wizard stays closed after first run', page.is_hidden('#wizard-panel'))
    st2 = page.evaluate("window.__cadence.state()")
    check('log persisted (34)', st2['logs']['2026-10-07']['r3'] == 34)
    check('note persisted', st2['notes']['2026-10-07|r3'] == 'Around the park')
    check('goal persisted (75)', st2['prefs']['goal'] == 75)
    check('order persisted', st2['rituals'][1]['id'] == 'r3')
    check('category edit persisted', [r for r in st2['rituals'] if r['id'] == 'r4'][0]['cat'] == 'Craft')
    check('streak still 12', page.evaluate("window.__cadence.streak()") == 12)
    page.click('.tab[data-view="history"]')
    check('bars persisted (today 71)', page.eval_on_selector_all('#chart-area .bar', "els => els.map(e => e.getAttribute('data-value'))") == ['66', '84', '71', '0', '0', '0', '0'])

    # 13. mobile collapse (L-22)
    page.set_viewport_size({'width': 700, 'height': 900})
    page.wait_for_timeout(60)
    check('mobile: ledger head hides (stacked rows)', page.eval_on_selector('#ledger thead', "e => getComputedStyle(e).display") == 'none')
    check('mobile: nav row still visible', page.is_visible('#tabs'))
    page.set_viewport_size({'width': 1280, 'height': 900})

    # 13b. no-rituals empty state (same ruled block)
    page.click('.tab[data-view="today"]')
    page.evaluate("window.__cadence.state().rituals.splice(0)")
    page.evaluate("window.__cadence.render()")
    check('empty block covers the no-rituals case', page.is_visible('#empty-state') and 'No rituals yet' in page.text_content('#empty-line'))
    check('empty action becomes Run setup', page.text_content('#empty-clear').strip() == 'Run setup')
    page.click('#empty-clear')
    check('Run setup reopens the wizard', page.is_visible('#wizard-panel'))
    page.click('#wz-skip')
    check('wizard dismisses again', page.is_hidden('#wizard-panel'))

    # 14. console/page errors
    check('zero console errors', len(errors) == 0, errors[:6])
    check('zero failed requests', len(req_fail) == 0, req_fail[:6])

    browser.close()

fails = [n for n, ok in results if not ok]
print('\n%d checks, %d passed, %d failed' % (len(results), len(results) - len(fails), len(fails)))
if fails:
    print('FAILED:', fails)
sys.exit(1 if fails else 0)
