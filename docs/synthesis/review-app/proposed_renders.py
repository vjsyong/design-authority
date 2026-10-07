"""Rendered previews of the proposed canon elements (adjudication proposals).

Each entry keyed by the 6-char suffix of the proposal id. Rendered in the
authority's own styling (fonts served from /fonts/<src>/tile/fonts).
"""

RENDER_CSS = """
@font-face { font-family:'Fraunces'; src:url('/fonts/wink/Fraunces-VF.ttf'); font-weight:100 900; }
@font-face { font-family:'Fraunces'; font-style:italic; src:url('/fonts/wink/Fraunces-Italic-VF.ttf'); font-weight:100 900; }
@font-face { font-family:'Inter'; src:url('/fonts/wink/Inter-VF.ttf'); font-weight:100 900; }
@font-face { font-family:'Gelasio'; src:url('/fonts/leader/Gelasio-VF.ttf'); font-weight:400 700; }
@font-face { font-family:'ArchivoBlack'; src:url('/fonts/leader/ArchivoBlack-Regular.ttf'); }
@font-face { font-family:'Arimo'; src:url('/fonts/dominion/Arimo-VF.ttf'); font-weight:100 900; }
.renderwrap { margin: 4px 0 2px; }
.renderwrap .cap { font: 11px system-ui; color: #999; margin: 0 0 6px; }
.rn { border: 1px dashed #d8d8d8; border-radius: 8px; padding: 18px; background: #fff; overflow: hidden; }
.rn style-note { display: none; }
.rn button { cursor: default; }
/* ---- wink ---- */
.rn-w { font-family:'Inter'; color:#241C15; }
.rn-w .cta { font-family:'Inter'; font-size:12.5px; font-weight:500; color:#241C15; background:#FFE01B; border:none; border-radius:26px; padding:10px 20px; box-shadow: inset 0 0 0 1px #241C15; }
.rn-w .cta.dark { background:#241C15; color:#fff; box-shadow:none; }
.rn-w .cta.outline { background:transparent; box-shadow: inset 0 0 0 2px #241C15; }
.rn-w .serif { font-family:'Fraunces'; font-variation-settings:'SOFT' 80,'WONK' 1,'opsz' 40; }
.rn-w .pill { display:inline-block; font-size:12px; font-weight:500; border-radius:999px; padding:5px 12px; }
.rn-w .p-n { background:#F6F6F4; box-shadow: inset 0 0 0 1px #DEDDDC; }
.rn-w .p-a { background:#E7B75F; }
.rn-w .p-p { background:rgba(191,64,85,.14); color:#8c2c40; }
.rn-w .card1 { background:#fff; border-radius:16px; box-shadow:0 8px 32px rgba(35,30,21,.2); padding:26px; }
.rn-w .scrim { background:rgba(35,30,21,.35); border-radius:12px; padding:22px; }
.rn-w .note { background:#F6F6F4; border-radius:12px; padding:13px 15px; font-size:13px; }
.rn-w .track { background:#F6F6F4; border-radius:999px; height:12px; overflow:hidden; }
.rn-w .track i { display:block; height:100%; width:70%; background:#FFE01B; }
/* ---- leader ---- */
.rn-l { font-family:'Inter'; color:#1A1A1A; }
.rn-l .serif { font-family:'Gelasio'; }
.rn-l .btn { font-family:'Inter'; font-size:13px; font-weight:500; border:none; padding:9px 16px; border-radius:8px; }
.rn-l .b-navy { background:#2E45B8; color:#fff; }
.rn-l .b-red { background:#E3120B; color:#fff; }
.rn-l .b-out { background:#fff; box-shadow: inset 0 0 0 2px #1A1A1A; }
.rn-l .tag2 { display:inline-block; font-size:10.5px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; padding:5px 10px; border:2px solid #1A1A1A; border-radius:8px; }
.rn-l .tag2.red { background:#E3120B; border-color:#E3120B; color:#fff; }
.rn-l table { width:100%; border-collapse:collapse; font-size:13px; }
.rn-l th { font-size:10px; letter-spacing:.07em; text-transform:uppercase; text-align:left; padding:6px 8px; border-bottom:2px solid #1A1A1A; font-weight:700; }
.rn-l td { padding:9px 8px; border-bottom:1px solid #D9D9D9; font-family:'Gelasio'; }
.rn-l tr.hov td { background:#FEE7E7; }
/* ---- dominion ---- */
.rn-d { font-family:'Arimo'; color:#000; }
.rn-d .btn { font-size:13px; border:none; padding:9px 16px; border-radius:4px; }
.rn-d .b-slate { background:#26374A; color:#fff; }
.rn-d .b-out { background:#fff; box-shadow: inset 0 0 0 2px #26374A; }
.rn-d .frame { background:#fff; border:2px solid #000; padding:18px; }
.rn-d .band { background:#F4F4F4; }
.rn-d .st { padding:5px 10px; display:inline-block; font-size:12.5px; }
.rn-d .st-a { border:1px solid #000; }
.rn-d .st-c { border-left:4px solid #000; background:#F4F4F4; font-weight:700; }
.rn-d .glow { outline:1px solid #66AFE9; box-shadow:0 0 8px 0 rgba(102,175,233,.6); }
"""


def _bars(color, heights, gap=6, w=16):
    return "".join(
        '<div style="width:%dpx;height:%dpx;background:%s"></div>' % (w, h, color)
        for h in heights
    ), '<div style="display:flex;gap:%dpx;align-items:flex-end;height:78px">' % gap


def _grid(shades, cell=13, gap=3):
    cells = "".join('<div style="width:%dpx;height:%dpx;background:%s"></div>' % (cell, cell, s)
                    for s in shades)
    return ('<div style="display:grid;grid-template-columns:repeat(7,%dpx);gap:%dpx">%s</div>'
            % (cell, gap, cells))


W_BARS = [57, 38, 76, 32, 63, 3, 44]
L_MONTH = (["#F2F2F2", "#D9D9D9", "#1A1A1A", "#666", "#D9D9D9", "#F2F2F2", "#1A1A1A",
            "#D9D9D9", "#F2F2F2", "#666", "#F2F2F2", "#D9D9D9", "#1A1A1A", "#F2F2F2",
            "#D9D9D9", "#666", "#1A1A1A", "#F2F2F2", "#D9D9D9", "#F2F2F2", "#1A1A1A",
            "#D9D9D9", "#666", "#F2F2F2", "#D9D9D9", "#1A1A1A", "#F2F2F2", "#666",
            "#D9D9D9", "#F2F2F2", "#1A1A1A", "#D9D9D9", "#666", "#F2F2F2", "#D9D9D9"])
D_MONTH = (["#F4F4F4", "#C9C9C9", "#000", "#969696", "#C9C9C9", "#F4F4F4", "#26374A",
            "#C9C9C9", "#F4F4F4", "#969696", "#F4F4F4", "#C9C9C9", "#000", "#F4F4F4",
            "#C9C9C9", "#969696", "#26374A", "#F4F4F4", "#C9C9C9", "#F4F4F4", "#000",
            "#C9C9C9", "#969696", "#F4F4F4", "#C9C9C9", "#26374A", "#F4F4F4", "#969696",
            "#C9C9C9", "#F4F4F4", "#000", "#C9C9C9", "#969696", "#F4F4F4", "#C9C9C9"])

_wbars, _wopen = _bars("#1A1A1A", W_BARS)
_lbars, _lopen = _bars("#1A1A1A", W_BARS)
_dbars, _dopen = _bars("#000000", W_BARS)

PROPOSED_RENDERS = {
    # ---------------- wink ----------------
    "9ff839": (  # destructive-confirm
        "<div class='rn rn-w'><div class='scrim'><div class='card1' style='max-width:330px;padding:26px'>"
        "<div class='serif' style='font-size:19px;font-weight:600'>Retire &ldquo;Practice guitar&rdquo;?</div>"
        "<p style='font-size:13px;margin:8px 0 16px;color:#5d5245'>It leaves your rituals for good. Your logged history stays.</p>"
        "<button class='cta dark'>Retire</button> <button class='cta outline'>Keep it</button>"
        "</div></div></div>"),
    "0510d7": (  # dialog-overlay
        "<div class='rn rn-w'><div class='scrim'><div class='card1' style='max-width:330px;padding:26px'>"
        "<div class='serif' style='font-size:17px;font-weight:600'>Ritual details</div>"
        "<p style='font-size:12.5px;color:#5d5245;margin:8px 0 0'>White 16px vessel, warm ink scrim, instant appearance &mdash; no motion invented.</p>"
        "</div></div></div>"),
    "d08fa9": (  # inline-notice
        "<div class='rn rn-w'><div class='note'><b style='font-size:13px'>Two rituals need a nudge.</b>"
        "<p style='font-size:12.5px;color:#5d5245;margin-top:3px'>Nothing to fix right now &mdash; they&rsquo;ll show up in tomorrow&rsquo;s list. "
        "<a style='color:#241C15'>See them</a></p></div></div>"),
    "74dedc": (  # empty-state
        "<div class='rn rn-w'><div class='note' style='text-align:center;padding:26px 18px'>"
        "<div class='serif' style='font-size:17px;font-weight:600'>Nothing logged yet</div>"
        "<p style='font-size:12.5px;color:#5d5245;margin:6px 0 14px'>Start with one small ritual &mdash; a ten-minute walk counts.</p>"
        "<button class='cta'>Add your first ritual</button></div></div>"),
    "58de37": (  # progress
        "<div class='rn rn-w'><div class='serif' style='font-size:15px;font-weight:600;margin-bottom:10px'>Importing your week&hellip;</div>"
        "<div class='track'><i></i></div>"
        "<p style='font-size:12px;color:#5d5245;margin:8px 0 12px'>7 of 10 steps &middot; reconciling dates&hellip;</p>"
        "<button class='cta outline'>Restart import</button></div>"),
    "44d062": (  # status-pill
        "<div class='rn rn-w'><span class='pill p-n'>New</span> "
        "<span class='pill p-a'>Due soon</span> "
        "<span class='pill p-p'>Missed &middot; 2 days</span>"
        "<p style='font-size:11.5px;color:#5d5245;margin-top:10px'>The word carries the state; colour only supports it.</p></div>"),
    # ---------------- leader ----------------
    "45862b": (  # destructive-confirm
        "<div class='rn rn-l'><div style='background:rgba(26,26,26,.62);border-radius:8px;padding:18px'>"
        "<div style='background:#fff;border-radius:8px;padding:22px;max-width:350px'>"
        "<b class='serif' style='font-size:16px'>Retire &ldquo;Practice guitar&rdquo;?</b>"
        "<p class='serif' style='font-size:12.5px;color:#444;margin:8px 0 14px'>It leaves the register permanently. Logged sessions stand.</p>"
        "<button class='btn b-red'>Retire</button> <button class='btn b-out'>Cancel</button>"
        "</div></div></div>"),
    "81e020": (  # empty-state
        "<div class='rn rn-l'><div style='border-top:2px solid #1A1A1A;padding:16px 2px'>"
        "<p class='serif' style='font-size:15px;font-weight:600'>Nothing is registered yet.</p>"
        "<p style='font-size:12.5px;color:#666;margin:6px 0 12px'>Add the first entry to open the register.</p>"
        "<button class='btn b-out'>Add an entry</button></div></div>"),
    "916eda": (  # data-charts
        "<div class='rn rn-l'><div style='display:flex;gap:30px;flex-wrap:wrap'>"
        "<div><p style='font-size:10px;letter-spacing:.07em;font-weight:700;color:#666;margin-bottom:8px'>MINUTES &middot; THIS WEEK</p>"
        + _lopen + _lbars + "</div></div>"
        "<div><p style='font-size:10px;letter-spacing:.07em;font-weight:700;color:#666;margin-bottom:8px'>MONTH</p>"
        + _grid(L_MONTH) + "</div>"
        "<div><p style='font-size:10px;letter-spacing:.07em;font-weight:700;color:#666;margin-bottom:8px'>SPARKLINE</p>"
        "<svg width='150' height='34' viewBox='0 0 150 34'><polyline points='0,20 21,24 42,12 63,27 84,8 105,22 126,30 150,16' "
        "fill='none' stroke='#E3120B' stroke-width='2'/></svg></div>"
        "</div><p style='font-size:11px;color:#666;margin-top:10px'>Rectilinear bars, month grid, hairline sparkline. No rings; red only as a single accent.</p></div>"),
    "91ef4b": (  # data-readouts
        "<div class='rn rn-l'><div style='display:flex;gap:40px;align-items:baseline'>"
        "<div><div style='font-family:ArchivoBlack;font-size:42px;line-height:1'>12</div>"
        "<div style='font-size:10px;letter-spacing:.09em;font-weight:700;color:#666;margin-top:4px'>DAY STREAK</div></div>"
        "<div><div style='font-family:ArchivoBlack;font-size:42px;line-height:1'>240</div>"
        "<div style='font-size:10px;letter-spacing:.09em;font-weight:700;color:#666;margin-top:4px'>MINUTES &middot; WEEK</div></div>"
        "</div><p style='font-size:11px;color:#666;margin-top:12px'>Big statics: display numeral + sans caps label. Archivo Black reserved for these moments.</p></div>"),
    "992c62": (  # tag
        "<div class='rn rn-l'><span class='tag2'>Available</span> <span class='tag2 red'>Overdue</span>"
        "<p style='font-size:11px;color:#666;margin-top:10px'>Ink-outline tag, caps sans; attention flips it solid red. No pills, no dots as the sole signal.</p></div>"),
    "25306d": (  # ledger
        "<div class='rn rn-l'><table><tr><th>Item</th><th>Status</th><th>Borrower</th></tr>"
        "<tr><td>Torque wrench 200Nm</td><td><span class='tag2' style='padding:3px 7px;font-size:9.5px'>Available</span></td><td>S. Ho</td></tr>"
        "<tr class='hov'><td>Cordless drill 18V</td><td><span class='tag2' style='padding:3px 7px;font-size:9.5px'>On loan</span></td><td>K. Lam</td></tr>"
        "<tr><td>Spirit level 60cm</td><td><span class='tag2 red' style='padding:3px 7px;font-size:9.5px'>Overdue</span></td><td>J. Wong</td></tr>"
        "</table><p style='font-size:11px;color:#666;margin-top:10px'>Editorial table: 2px ink header rule, hairline rows, serif names, sans numbers, red95 hover.</p></div>"),
    # ---------------- dominion ----------------
    "e09f12": (  # dialog + empty-state
        "<div class='rn rn-d'><div style='background:rgba(0,0,0,.55);padding:16px'>"
        "<div class='frame' style='max-width:350px;margin:0 auto'><b style='font-size:14px'>Retirer &laquo; Practice guitar &raquo;? | Retire &ldquo;Practice guitar&rdquo;?</b>"
        "<p style='font-size:12.5px;margin:8px 0 14px'>Il quitte le registre d&eacute;finitivement. | It leaves the register permanently.</p>"
        "<button class='btn b-slate'>Retirer</button> <button class='btn b-out'>Annuler</button></div></div>"
        "<p style='margin:16px 0 0;border-top:2px solid #000;padding-top:12px;font-size:13px'>"
        "Rien n&rsquo;est encore inscrit. | Nothing is registered yet. "
        "<button class='btn b-out' style='margin-left:8px;padding:6px 12px;font-size:12px'>Ajouter une entr&eacute;e</button></p></div>"),
    "522030": (  # status + ledger
        "<div class='rn rn-d'><span class='st st-a'>En r&egrave;gle | On track</span> "
        "<span class='st st-c'>En retard | Overdue &middot; 3 days</span>"
        "<table style='width:100%;border-collapse:collapse;font-size:13px;margin-top:14px'>"
        "<tr><th style='font-size:10px;letter-spacing:.06em;text-transform:uppercase;text-align:left;padding:6px 8px;border-bottom:2px solid #000'>Article</th>"
        "<th style='font-size:10px;letter-spacing:.06em;text-transform:uppercase;text-align:left;padding:6px 8px;border-bottom:2px solid #000'>&Eacute;tat | Status</th></tr>"
        "<tr><td style='padding:9px 8px;border-bottom:1px solid #C9C9C9'>Corde &agrave; sauter | Skipping rope</td><td style='padding:9px 8px;border-bottom:1px solid #C9C9C9'>En r&egrave;gle</td></tr>"
        "<tr><td style='padding:9px 8px;border-bottom:1px solid #C9C9C9'>Bloc-notes | Notebook</td><td style='padding:9px 8px;border-bottom:1px solid #C9C9C9'>En retard</td></tr>"
        "</table><p style='font-size:11px;color:#555;margin-top:10px'>Words carry status; the register stays ruled and quiet.</p></div>"),
    "72cc3e": (  # notice
        "<div class='rn rn-d'><div class='band' style='border-top:2px solid #000;padding:12px 14px;font-size:13px'>"
        "Deux s&eacute;ances en attente. Les rappels partent ce soir. | Two sessions pending. Reminders go out tonight.</div></div>"),
    "bd08f2": (  # plain-chart
        "<div class='rn rn-d'><div style='display:flex;gap:30px;flex-wrap:wrap'>"
        "<div><p style='font-size:10px;letter-spacing:.06em;text-transform:uppercase;font-weight:700;color:#555;margin-bottom:8px'>Minutes | this week</p>"
        + _dopen + _dbars + "</div></div>"
        "<div><p style='font-size:10px;letter-spacing:.06em;text-transform:uppercase;font-weight:700;color:#555;margin-bottom:8px'>Mois | month</p>"
        + _grid(D_MONTH) + "</div>"
        "<div><p style='font-size:10px;letter-spacing:.06em;text-transform:uppercase;font-weight:700;color:#555;margin-bottom:8px'>Tendance | trend</p>"
        "<svg width='150' height='34' viewBox='0 0 150 34'><polyline points='0,20 21,24 42,12 63,27 84,8 105,22 126,30 150,16' "
        "fill='none' stroke='#26374A' stroke-width='2'/></svg></div>"
        "</div><p style='font-size:11px;color:#555;margin-top:10px'>Bars, month grid and sparkline in the rule-and-grid idiom &mdash; no rings, no new colours.</p></div>"),
    "0cf7b9": (  # reversed colourway
        "<div class='rn rn-d'><div style='background:#0b0b0b;color:#fff;border-radius:4px;padding:16px'>"
        "<b style='font-size:13px'>Reversed colourway &mdash; dark surfaces</b>"
        "<p style='font-size:12px;color:#c9c9c9;margin:6px 0 12px'>Ground flips; structure stays: white rules, band #1a1a1a, slate actions keep contrast, focus glow reads on dark.</p>"
        "<button class='btn b-slate glow'>Primaire | Primary</button> "
        "<button class='btn' style='background:#1a1a1a;color:#fff;box-shadow:inset 0 0 0 1px #444'>Secondaire</button>"
        "</div></div>"),
}
