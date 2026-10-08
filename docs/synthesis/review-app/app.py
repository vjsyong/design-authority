#!/usr/bin/env python3
"""Gate 2 review server — interactive decision cards with verdicts, comments and
image uploads. Transforms the static sheet.html files into review pages, serves
them on 127.0.0.1:8420, and stores feedback under data/ + uploads/.

Run:  .venv/bin/python3 docs/synthesis/review-app/app.py
"""
import json
import os
import re
import time

from bs4 import BeautifulSoup
from flask import (Flask, Response, abort, jsonify, redirect,
                   render_template_string, request, send_from_directory)

ROOT = os.path.dirname(os.path.abspath(__file__))
SYN = os.path.dirname(ROOT)                      # docs/synthesis
DATA = os.path.join(ROOT, "data")
UPLOADS = os.path.join(ROOT, "uploads")
PAGES = os.path.join(ROOT, "pages")
FEEDBACK = os.path.join(DATA, "feedback.json")
os.makedirs(DATA, exist_ok=True)
os.makedirs(UPLOADS, exist_ok=True)
os.makedirs(PAGES, exist_ok=True)

SOURCES = {
    "wink": {"name": "wink — Mailchimp", "pre": "W", "cards": 26},
    "leader": {"name": "leader — The Economist", "pre": "L", "cards": 24},
    "dominion": {"name": "dominion — Canada FIP", "pre": "D", "cards": 22},
}
ID_RE = re.compile(r"^[WLD]-\d{2}$")
SAFE_RE = re.compile(r"[^A-Za-z0-9._-]")

# ---- candidate pack demo (Phase 3 compilation) ----
import sys as _sys
from html import escape as _escape


def _esc(s):
    return _escape(str(s if s is not None else ""))

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(ROOT)))
_sys.path.insert(0, os.path.join(_REPO, "kernel"))
from design_authority.pack import Pack, PackError          # noqa: E402
from design_authority.resolve import resolve, resolve_golden  # noqa: E402
from design_authority import records as da_records         # noqa: E402

PACKS_DIR = os.path.join(_REPO, "packs")
import authority_gallery as _gal          # discovery + mtime freshness (docs/12)


def pack_names():
    return _gal.names()


def pack_desc(name):
    e = _gal.get(name)
    return e["desc"] if e else ""


def is_pack(name):
    return _gal.get(name) is not None


def get_pack(name):
    e = _gal.get(name)
    if not e:
        abort(404)
    return e["pack"]


def golden_summary(name):
    e = _gal.get(name)
    if not e or not e["golden"]:
        abort(404)
    return e["golden"]


def render_resolution(pack, r):
    o = r.get("outcome")
    res = r.get("resolution") or {}
    ident = "%s %s" % (_esc(pack.manifest.get("id")), _esc(pack.manifest.get("version")))
    out = ["<div class='out out-%s'><div class='ohead'><span class='obadge'>%s</span> "
           "<span class='oid'>%s</span></div>" % (o.lower(), o, ident)]
    if o == "CONFLICT":
        p = res.get("prohibition") or {}
        rule = res.get("rule") or {}
        out.append("<p class='main'><b>Do not implement as requested.</b> %s</p>" % _esc(p.get("statement")))
        out.append("<p class='dim'>detected: %s</p>" % _esc(res.get("detected")))
        if rule:
            out.append("<p class='main'><b>%s · %s</b> — %s</p>" % (_esc(rule.get("id")), _esc(rule.get("severity")), _esc(rule.get("summary"))))
            out.append("<p class='dim'>fix: %s</p>" % _esc(rule.get("fix")))
    elif o == "RESOLVED":
        a = res.get("artifact") or {}
        out.append("<p class='main'><b>%s</b> <span class='dim'>(%s)</span></p>" % (_esc(a.get("title")), _esc(a.get("id"))))
        out.append("<p class='main'>%s</p>" % _esc(a.get("summary")))
        for st in (a.get("states") or []):
            out.append("<p class='dim'>· %s</p>" % _esc(st))
        for st in (a.get("a11y") or []):
            out.append("<p class='dim'>a11y: %s</p>" % _esc(st))
    elif o == "COMPOSE":
        rec = res.get("recipe") or {}
        out.append("<p class='main'><b>%s</b> <span class='dim'>(%s)</span></p>" % (_esc(rec.get("title")), _esc(rec.get("id"))))
        out.append("<p class='main'>%s</p>" % _esc(rec.get("summary")))
        for c in (rec.get("constraints") or []):
            out.append("<p class='dim'>· %s</p>" % _esc(c))
        ing = [i.get("id") for i in (res.get("ingredients") or [])]
        if ing:
            out.append("<p class='dim'>ingredients: %s</p>" % _esc(", ".join(ing)))
    elif o == "FALLBACK":
        fb = res.get("fallback") or {}
        out.append("<p class='main'><b>%s</b></p>" % _esc(fb.get("title")))
        out.append("<p class='main'>%s</p>" % _esc(fb.get("statement")))
        for c in (fb.get("constraints") or []):
            out.append("<p class='dim'>· %s</p>" % _esc(c))
    else:
        out.append("<p class='main'>%s</p>" % _esc(r.get("why")))
        closest = r.get("closest") or []
        if closest:
            out.append("<p class='dim'>closest: %s</p>" % _esc(", ".join("%s (%s)" % (c["id"], c["score"]) for c in closest[:3])))
        pol = (r.get("fallback_policy") or {}).get("note")
        if pol:
            out.append("<p class='dim'>policy: %s</p>" % _esc(pol))
    alts = r.get("alternatives") or []
    if alts:
        out.append("<p class='dim'>also considered: %s</p>" % _esc(", ".join(a.get("id") for a in alts)))
    out.append("</div>")
    return "".join(out)

DEMO_CSS = """
body{font-family:system-ui,-apple-system,sans-serif;color:#141414;background:#fff;margin:0}
.dwrap{max-width:960px;margin:0 auto;padding:26px 18px 60px}
h1{font-size:22px;margin:0 0 4px} h2{font-size:15px;margin:26px 0 10px;border-bottom:2px solid #141414;padding-bottom:6px}
.sub{color:#555;font-size:13.5px;margin:0 0 18px}
.meta{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0 4px}
.chip{font:600 11px system-ui;padding:4px 10px;border-radius:999px;background:#f2f2f2;color:#444}
.chip.gold{background:#087830;color:#fff}.chip.src{background:#141414;color:#fff}
.src-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
a.src{display:block;border:1.5px solid #141414;border-radius:10px;padding:14px 16px;text-decoration:none;color:inherit}
a.src b{font-size:15px} a.src p{margin:6px 0 0;font-size:12.5px;color:#555}
.ask{display:flex;gap:8px;margin:10px 0}
.ask input{flex:1;font:13.5px system-ui;padding:11px 13px;border:1.5px solid #141414;border-radius:8px}
.ask button{font:600 13px system-ui;padding:11px 20px;border:none;background:#141414;color:#fff;border-radius:8px;cursor:pointer}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 4px}
.chips button{font:12px system-ui;padding:6px 11px;border:1.2px solid #b9b9b9;background:#fafafa;border-radius:999px;cursor:pointer}
.out{border:2px solid #141414;border-radius:10px;padding:14px 16px;margin-top:12px;background:#fff}
.out .ohead{margin-bottom:8px}.out .main{font:13.5px/1.5 system-ui;margin:5px 0}
.out .dim{font:12px/1.5 system-ui;color:#666;margin:3px 0}.oid{font:12px system-ui;color:#888}
.obadge{font:700 11px system-ui;letter-spacing:.08em;padding:4px 10px;border-radius:999px;color:#fff;background:#141414}
.out-resolved .obadge{background:#087830}.out-conflict .obadge{background:#b3261e}
.out-compose .obadge{background:#2E45B8}.out-fallback .obadge{background:#8a5a00}.out-undefined .obadge{background:#666}
.art{border:1px solid #dcdcdc;border-radius:8px;padding:12px 14px;margin-bottom:10px}
.art .t{font-size:13.5px}
.art .s{font-size:12.5px/1.5;color:#333;margin:6px 0 0}
.kd{font:600 10px system-ui;letter-spacing:.06em;text-transform:uppercase;background:#141414;color:#fff;border-radius:4px;padding:3px 7px;margin-right:6px}
.sts{font:12px/1.5 system-ui;color:#555;margin:4px 0 0}
.mono{font:11.5px ui-monospace,monospace;color:#555}
details{margin-top:8px} summary{cursor:pointer;font:600 13px system-ui}
table{border-collapse:collapse;font:12.5px system-ui;margin-top:8px;width:100%}
td,th{border-bottom:1px solid #e4e4e4;padding:6px 8px;text-align:left;vertical-align:top}
.ok{color:#087830;font-weight:700}.miss{color:#b3261e;font-weight:700}
.back{font:600 12.5px system-ui;color:#2E45B8;text-decoration:none}
"""

DEMO_LANDING = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Authority synthesis — candidates</title><style>__CSS__</style></head><body>
<div class="dwrap">
<h1>Authority Synthesis — the three candidates</h1>
<p class="sub">Compiled from your Gate-2 verdicts by the pack compiler, verified against the
frozen kernel. Open a candidate and ask it anything — each one answers in its own character.</p>
<div class="src-grid">__CARDS__</div>
<h2 style="margin-top:26px">Stress test — "Cadence", one app × three authorities</h2>
<p class="sub">Same habit-tracker spec, built three times under quarantine. 42 required elements
were resolved against each authority first; improvised/adapted elements are marked in-app (tap ◌).</p>
<div class="src-grid">__STRESS__</div>
<h2 style="margin-top:26px">Stress test v2 — rebuilt on the updated authorities</h2>
<p class="sub">Same spec, rebuilt after the adjudication pass (12 fixes applied + kernel/compiler fixes).
Result: fewer pure improvisations, more sanctioned fallbacks — and the first recipes composing.</p>
<div class="src-grid">__STRESS2__</div>
<h2 style="margin-top:26px">Stress test v3 — rebuilt on the codified authorities</h2>
<p class="sub">Third build, same spec: packs at 0.2.0 (the 11 accepted proposals are now canon) and the 25
negative precedents steering declined asks toward their sanctioned alternatives.</p>
<div class="src-grid">__STRESS3__</div>
<h2 style="margin-top:26px">Proposal gate</h2>
<p class="sub">The adjudication pass filed proposals for canon changes — inspect and rule on each.
Accepted proposals are codified into the packs; rejected ones are filed as negative precedents (reasons + guidance for future asks).</p>
<p><a class="src" style="max-width:420px" href="/proposals"><b>Proposal gate &rarr;</b><p>verdicts write to the kernel records</p></a></p>
<p class="sub" style="margin-top:22px">Review sheets: <a class="back" href="/">Gate 2 review</a></p>
</div></body></html>"""

DEMO_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title><style>__CSS__</style></head><body>
<div class="dwrap">
<p><a class="back" href="/demo">&larr; all candidates</a></p>
<h1>__TITLE__</h1>
<p class="sub">__DESC__</p>
<div class="meta">__META__</div>

<h2>Ask this authority</h2>
<div class="ask"><input id="q" placeholder="e.g. make the buttons square" autocomplete="off">
<button onclick="ask()">Ask</button></div>
<div class="chips" id="chips">__CHIPS__</div>
<div id="out"></div>

<h2>Golden set</h2>
__GOLDEN__

<h2>Artifacts</h2>
__ARTS__

<h2>Rules</h2>
__RULES__

<h2>Prohibitions</h2>
__PROH__

<h2>Fallbacks</h2>
__FB__

__RECIPES__

</div>
<script>
var PACK = "__PACK__";
function ask(q) {
  var input = document.getElementById('q');
  var problem = q || input.value.trim();
  if (!problem) return;
  if (q) input.value = q;
  var out = document.getElementById('out');
  out.innerHTML = "<p class='sub'>asking\u2026</p>";
  fetch('/api/demo/resolve', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({pack: PACK, problem: problem})})
    .then(function (r) { return r.json(); })
    .then(function (j) { out.innerHTML = j.html || ("error: " + (j.error || "unknown")); })
    .catch(function () { out.innerHTML = "<p class='sub'>request failed</p>"; });
}
document.getElementById('q').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') ask(); });
</script>
</body></html>"""

DEMO_EXAMPLES = [
    "make the buttons square",
    "add a soft blue glow to the button",
    "use rounded pills for the primary action",
    "add a photograph to the empty state",
]

FB_CSS = """
.fb { margin-top:12px; border-top:1px dashed #c9c9c9; padding-top:10px; }
.fb .vb { display:flex; gap:6px; flex-wrap:wrap; margin-bottom:8px; }
.fb .vb button { font:600 11.5px system-ui; letter-spacing:.04em; padding:7px 12px;
  border:1.5px solid #444; background:#fff; border-radius:6px; cursor:pointer; }
.fb .vb button.sel { background:#141414; color:#fff; border-color:#141414; }
.fb textarea { width:100%; min-height:52px; font:13px/1.4 system-ui; padding:8px 10px;
  border:1.5px solid #cfcfcf; border-radius:6px; resize:vertical; }
.fb .row2 { display:flex; gap:10px; align-items:center; margin-top:8px; flex-wrap:wrap; }
.fb .upl { font:12.5px system-ui; color:#333; border:1.5px dashed #b9b9b9; border-radius:6px;
  padding:7px 10px; cursor:pointer; }
.fb .upl input { display:none; }
.fb .save { font:600 12.5px system-ui; padding:8px 16px; border:none; background:#141414;
  color:#fff; border-radius:6px; cursor:pointer; }
.fb .status { font:12px system-ui; color:#087830; }
.fb .status.err { color:#b3261e; }
.fb .thumbs { display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
.fb .thumbs a img { width:74px; height:74px; object-fit:cover; border:1px solid #cfcfcf; border-radius:6px; }
.fb .pending { display:flex; gap:6px; flex-wrap:wrap; margin-top:8px; }
.fb .pchip { display:inline-flex; gap:6px; align-items:center; font:12px system-ui; background:#f3f3f3;
  border:1px solid #ddd; border-radius:6px; padding:4px 8px; }
.fb .pchip button { border:none; background:none; cursor:pointer; font-weight:700; color:#888; }
.fb .thumbwrap { position:relative; display:inline-block; }
.fb .thumbdel { position:absolute; top:-7px; right:-7px; width:21px; height:21px; border-radius:50%;
  border:none; background:#141414; color:#fff; font:700 11px system-ui; cursor:pointer; }
.fb .thumbdel.confirm { width:auto; border-radius:11px; padding:0 7px; height:22px; background:#b3261e; }
#fb-toast { position:fixed; right:16px; bottom:16px; background:#141414; color:#fff;
  font:600 13px system-ui; padding:11px 17px; border-radius:9px; opacity:0; pointer-events:none;
  transition:opacity .25s; z-index:99; max-width:80vw; }
#fb-toast.on { opacity:1; }
.filterbar .hint { font:12px system-ui; color:#777; margin-left:6px; }
.card[data-verdict] { outline:1px solid #e4e4e4; }
.filterbar { position:sticky; top:0; z-index:9; background:#fff; border-bottom:2px solid #141414;
  padding:10px 0 10px; display:flex; gap:8px; align-items:center; width:100%; }
.filterbar button { font:600 12px system-ui; padding:7px 13px; border-radius:999px;
  border:1.5px solid #141414; background:#fff; cursor:pointer; }
.filterbar button.sel { background:#141414; color:#fff; }
.filterbar .prog { margin-left:auto; font:12.5px system-ui; color:#555; }
@media (max-width: 900px) {
  .part { width:auto !important; padding:12px !important; }
  .grid { grid-template-columns:1fr !important; }
  .card[style] { grid-column:auto !important; }
}
"""

FB_JS = """
const API = '/api/feedback';
let FB = {};
const esc = s => (s||'').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let toastT = null;
function toast(msg) {
  let t = document.getElementById('fb-toast');
  if (!t) { t = document.createElement('div'); t.id = 'fb-toast'; document.body.appendChild(t); }
  t.textContent = msg; t.classList.add('on');
  clearTimeout(toastT);
  toastT = setTimeout(() => t.classList.remove('on'), 2400);
}
function counts() {
  let tot = 0, done = 0;
  document.querySelectorAll('.card').forEach(c => { tot++; if (c.dataset.verdict) done++; });
  document.querySelectorAll('.prog').forEach(p => p.textContent = done + ' / ' + tot + ' decided');
}
function stLine(card) { return card.querySelector('.fb .status'); }
function paintThumbs(card) {
  const e = FB[card.dataset.did] || {};
  const th = card.querySelector('.thumbs');
  th.innerHTML = (e.images||[]).map(p =>
    `<span class="thumbwrap" data-path="${p}"><a href="/${p}" target="_blank"><img src="/${p}" title="${esc(p.split('/').pop())}"></a><button class="thumbdel" title="delete image">×</button></span>`
  ).join('');
  th.querySelectorAll('.thumbdel').forEach(btn => {
    btn.addEventListener('click', () => {
      if (!btn.classList.contains('confirm')) {
        btn.classList.add('confirm'); btn.textContent = 'delete?';
        setTimeout(() => { btn.classList.remove('confirm'); btn.textContent = '×'; }, 4000);
        return;
      }
      const fd = new FormData();
      fd.append('id', card.dataset.did);
      fd.append('path', btn.closest('.thumbwrap').dataset.path);
      btn.textContent = '…';
      fetch('/api/image/delete', {method:'POST', body:fd}).then(r => r.json()).then(e => {
        if (e.error) { btn.textContent = '×'; return; }
        FB[card.dataset.did] = e; paintThumbs(card); toast('image deleted');
      }).catch(() => { btn.textContent = '×'; });
    });
  });
}
function applyEntry(card, e) {
  FB[card.dataset.did] = e;
  card.dataset.verdict = e.verdict || '';
  paintThumbs(card); counts();
  const st = stLine(card);
  st.textContent = 'saved ✓ ' + (new Date()).toLocaleTimeString();
  st.classList.remove('err');
}
function push(card, files, pre) {
  if (card._busy) { card._queued = {files, pre}; return; }
  const fb = card.querySelector('.fb');
  const fd = new FormData();
  fd.append('id', card.dataset.did);
  fd.append('verdict', card._sel || '');
  fd.append('comment', fb.querySelector('textarea').value);
  (files || []).forEach(f => fd.append('images', f));
  card._busy = true;
  const st = stLine(card);
  st.classList.remove('err');
  st.textContent = pre || 'saving…';
  fetch(API, {method:'POST', body:fd}).then(r => r.json()).then(e => {
    card._busy = false;
    if (e.error) { st.textContent = e.error; st.classList.add('err'); return; }
    applyEntry(card, e);
    if (files && files.length) toast('uploaded ✓ ' + files.length + ' image(s)');
    if (card._queued) { const q = card._queued; card._queued = null; push(card, q.files, q.pre); }
  }).catch(() => {
    card._busy = false;
    st.textContent = 'save failed — make any change to retry';
    st.classList.add('err');
  });
}
function render(card) {
  const e = FB[card.dataset.did] || {};
  const fb = card.querySelector('.fb');
  fb.querySelectorAll('.vb button').forEach(b => b.classList.toggle('sel', b.dataset.v === (e.verdict||'')));
  const ta = fb.querySelector('textarea');
  if (document.activeElement !== ta) ta.value = e.comment || '';
  paintThumbs(card);
  card.dataset.verdict = e.verdict || '';
}
function hydrate() {
  fetch(API).then(r => r.json()).then(m => { FB = m; document.querySelectorAll('.card').forEach(render); counts(); });
}
function init() {
  document.querySelectorAll('.card').forEach(card => {
    const fb = card.querySelector('.fb');
    const inp = fb.querySelector('input[type=file]');
    inp.addEventListener('change', () => {
      const files = Array.from(inp.files); inp.value = '';
      if (files.length) push(card, files, 'uploading ' + files.length + ' file(s)…');
    });
    fb.querySelectorAll('.vb button').forEach(b => b.addEventListener('click', () => {
      const next = (card._sel === b.dataset.v) ? '' : b.dataset.v;
      card._sel = next;
      fb.querySelectorAll('.vb button').forEach(x => x.classList.toggle('sel', x.dataset.v === next));
      push(card);
    }));
    card._sel = '';
    const ta = fb.querySelector('textarea');
    ta.addEventListener('input', () => { clearTimeout(card._t); card._t = setTimeout(() => push(card, null, 'saving notes…'), 900); });
    ta.addEventListener('blur', () => { clearTimeout(card._t); push(card); });
    fb.querySelector('.save').addEventListener('click', () => push(card));
  });
  document.querySelectorAll('.filterbar button').forEach(b => b.addEventListener('click', () => {
    document.querySelectorAll('.filterbar button').forEach(x => x.classList.toggle('sel', x === b));
    const f = b.dataset.f;
    document.querySelectorAll('.card').forEach(c => {
      const att = c.classList.contains('att');
      const dec = !!c.dataset.verdict;
      let show = true;
      if (f === 'call') show = att;
      if (f === 'rev') show = c.classList.contains('rev');
      if (f === 'undecided') show = !dec;
      if (f === 'decided') show = dec;
      c.style.display = show ? '' : 'none';
    });
  }));
}
function boot() { hydrate(); init(); }
document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', boot) : boot();
"""

BAR = """
<div class="filterbar">
  <button data-f="all" class="sel">All</button>
  <button data-f="call">Your call</button>
  <button data-f="rev">Revised v2</button>
  <button data-f="undecided">Undecided</button>
  <button data-f="decided">Decided</button>
  <span class="hint">autosaves as you go</span>
  <span class="prog"></span>
</div>
"""


def build_page(src):
    """Transform sheet.html into an interactive review page."""
    sheet = os.path.join(SYN, src, "refs", "sheet.html")
    soup = BeautifulSoup(open(sheet, encoding="utf-8"), "html.parser")
    head = soup.head
    vp = soup.new_tag("meta", attrs={"name": "viewport",
                                     "content": "width=device-width, initial-scale=1"})
    head.append(vp)
    style = soup.new_tag("style")
    style.string = FB_CSS
    head.append(style)
    # rewrite font paths to the app's font route
    for st in soup.find_all("style"):
        if st.string:
            st.string = st.string.replace("../tile/fonts/", f"/fonts/{src}/")
    for card in soup.select(".card"):
        cid = card.select_one(".cid")
        cid = cid.get_text(strip=True) if cid else "??"
        card["data-did"] = cid
        card["style"] = card.get("style", "")  # keep any inline style
        fb = BeautifulSoup(
            f"""<div class="fb">
  <div class="vb">
    <button data-v="accept">ACCEPT</button>
    <button data-v="modify">MODIFY</button>
    <button data-v="reject">REJECT</button>
    <button data-v="undefined">LEAVE UNDEFINED</button>
  </div>
  <textarea placeholder="Notes for this item…"></textarea>
  <div class="row2">
    <label class="upl">Attach image(s) — camera or gallery<input type="file" accept="image/*" multiple></label>
    <button class="save">Save now</button>
    <span class="status"></span>
  </div>
  <div class="thumbs"></div>
</div>""", "html.parser")
        card.append(fb)
    # filter bar before first part
    bar = BeautifulSoup(BAR, "html.parser")
    soup.body.insert(0, bar)
    script = soup.new_tag("script")
    script.string = FB_JS
    soup.body.append(script)
    out = os.path.join(PAGES, f"{src}.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(str(soup))
    return out


def ensure_pages():
    for src in SOURCES:
        build_page(src)


def load_fb():
    if os.path.exists(FEEDBACK):
        with open(FEEDBACK, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_fb(m):
    tmp = FEEDBACK + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1, ensure_ascii=False)
    os.replace(tmp, FEEDBACK)


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 40 * 1024 * 1024

OVERVIEW = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Authority Synthesis — Gate 2 review</title>
<style>body{font:15px/1.5 system-ui;max-width:640px;margin:0 auto;padding:28px 18px;color:#141414}
a.src{display:block;border:2px solid #141414;border-radius:10px;padding:16px 18px;margin:12px 0;text-decoration:none;color:#141414}
a.src b{font-size:17px} a.src p{margin:4px 0 0;color:#555;font-size:13.5px}
.bar{height:8px;background:#eee;border-radius:4px;margin-top:10px;overflow:hidden}
.bar i{display:block;height:100%;background:#141414}
h1{font-size:22px} .sub{color:#555;font-size:13.5px;margin-bottom:18px}</style></head><body>
<h1>Authority Synthesis — Gate 2</h1>
<p class="sub">Review each decision card: verdict, notes, and image attachments save straight to disk. Safe to reload; come back any time. · <a href="/demo" style="color:#2E45B8;font-weight:600">Candidate pack demo &rarr;</a></p>
{{cards|safe}}
</body></html>"""


@app.route("/")
def index():
    if _is_designauthority_host():
        return send_from_directory(DA_SITE, "index.html")
    fb = load_fb()
    cards = []
    for src, meta in SOURCES.items():
        ids = [f"{meta['pre']}-{i:02d}" for i in range(1, meta["cards"] + 1)]
        done = sum(1 for i in ids if fb.get(i, {}).get("verdict"))
        pct = round(100 * done / len(ids))
        cards.append(
            f"<a class='src' href='/review/{src}'><b>{meta['name']}</b>"
            f"<p>{done} / {len(ids)} decided</p>"
            f"<div class='bar'><i style='width:{pct}%'></i></div></a>")
    return render_template_string(OVERVIEW, cards="".join(cards))


@app.route("/review/<src>")
def review(src):
    if src not in SOURCES:
        abort(404)
    ensure_pages()
    return send_from_directory(PAGES, f"{src}.html")


@app.route("/api/feedback", methods=["GET"])
def fb_get():
    return jsonify(load_fb())


@app.route("/api/feedback", methods=["POST"])
def fb_post():
    cid = (request.form.get("id") or "").strip()
    if not ID_RE.match(cid):
        return jsonify({"error": "bad id"}), 400
    verdict = (request.form.get("verdict") or "").strip()
    if verdict not in ("", "accept", "modify", "reject", "undefined"):
        return jsonify({"error": "bad verdict"}), 400
    m = load_fb()
    entry = m.get(cid, {"images": []})
    entry["verdict"] = verdict
    entry["comment"] = request.form.get("comment") or ""
    entry["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    files = request.files.getlist("images")
    for f in files:
        if not f or not f.filename:
            continue
        name = SAFE_RE.sub("_", os.path.basename(f.filename))[:80]
        d = os.path.join(UPLOADS, cid)
        os.makedirs(d, exist_ok=True)
        fn = f"{int(time.time())}_{name}"
        f.save(os.path.join(d, fn))
        entry["images"].append(f"uploads/{cid}/{fn}")
    m[cid] = entry
    save_fb(m)
    entry["id"] = cid
    return jsonify(entry)


@app.route("/api/image/delete", methods=["POST"])
def img_delete():
    cid = (request.form.get("id") or "").strip()
    path = (request.form.get("path") or "").strip()
    prefix = f"uploads/{cid}/"
    if not ID_RE.match(cid) or not path.startswith(prefix) or ".." in path:
        return jsonify({"error": "bad request"}), 400
    fn = os.path.basename(path)
    full = os.path.join(UPLOADS, cid, fn)
    if os.path.exists(full):
        os.remove(full)
    m = load_fb()
    entry = m.get(cid, {"images": []})
    entry["images"] = [p for p in entry.get("images", []) if p != path]
    entry["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    m[cid] = entry
    save_fb(m)
    entry["id"] = cid
    return jsonify(entry)


@app.route("/uploads/<cid>/<fn>")
def uploads(cid, fn):
    if not ID_RE.match(cid):
        abort(404)
    return send_from_directory(os.path.join(UPLOADS, cid), fn)


@app.route("/fonts/<src>/<fn>")
def fonts(src, fn):
    if src not in SOURCES:
        abort(404)
    return send_from_directory(os.path.join(SYN, src, "tile", "fonts"), fn)


@app.route("/demo")
def demo():
    cards = []
    for name in pack_names():
        src = pack_desc(name)
        pack = get_pack(name)
        g = golden_summary(name)
        kinds = {}
        for a in pack.artifacts:
            kinds[a["kind"]] = kinds.get(a["kind"], 0) + 1
        ktxt = " · ".join("%d %s" % (v, k) for k, v in sorted(kinds.items()))
        # every authority page lives on the concept site
        href = "https://designauthority.seanyong.xyz/authorities/%s/audit" % name
        cards.append(
            "<a class='src' href='%s'><b>%s</b><p>%s</p>"
            "<p><span class='chip src'>%s</span> <span class='chip gold'>golden %d/%d</span></p></a>"
            % (href, _esc(pack.manifest.get("name")), _esc(src), _esc(ktxt), g["passed"], g["total"]))
    stress = []
    for name in pack_names():
        d = os.path.join(_REPO, "examples", "cadence-%s" % name)
        if os.path.isdir(d):
            gaps = 0
            gp = os.path.join(d, ".design-authority", "gaps.jsonl")
            if os.path.exists(gp):
                gaps = sum(1 for _ in open(gp))
            stress.append(
                "<a class='src' href='https://designauthority.seanyong.xyz/authorities/%s/demo/cadence-v1/'><b>Cadence · %s</b>"
                "<p>the same tracker, rendered by the %s authority</p>"
                "<p><span class='chip'>%d gaps filed</span> <span class='chip src'>open &rarr;</span></p></a>"
                % (name, name, name, gaps))
    stress2 = []
    for name in pack_names():
        d = os.path.join(_REPO, "examples", "cadence2-%s" % name)
        if os.path.isdir(d):
            gaps = 0
            gp = os.path.join(d, ".design-authority", "gaps.jsonl")
            if os.path.exists(gp):
                gaps = sum(1 for _ in open(gp))
            stress2.append(
                "<a class='src' href='https://designauthority.seanyong.xyz/authorities/%s/demo/cadence-v2/'><b>Cadence v2 · %s</b>"
                "<p>rebuilt on the updated authority</p>"
                "<p><span class='chip'>%d gaps filed</span> <span class='chip src'>open &rarr;</span></p></a>"
                % (name, name, gaps))
    stress3 = []
    for name in pack_names():
        d = os.path.join(_REPO, "examples", "cadence3-%s" % name)
        if os.path.isdir(d):
            gaps = 0
            gp = os.path.join(d, ".design-authority", "gaps.jsonl")
            if os.path.exists(gp):
                gaps = sum(1 for _ in open(gp))
            stress3.append(
                "<a class='src' href='https://designauthority.seanyong.xyz/authorities/%s/demo/cadence-v3/'><b>Cadence v3 · %s</b>"
                "<p>rebuilt on the codified authority (0.2.0 + precedents)</p>"
                "<p><span class='chip'>%d gaps filed</span> <span class='chip src'>open &rarr;</span></p></a>"
                % (name, name, gaps))
    audit = ("<a class='src' href='https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/'><b>System Review &middot; Jennu</b>"
             "<p>the design authority of zhenyoyo.github.io (deployed language). 36 ledger items &amp; the screens behind them</p>"
             "<p><span class='chip'>36 ledger items</span> <span class='chip src'>open &rarr;</span></p></a>")
    audit += ("<a class='src' href='https://designauthority.seanyong.xyz/'><b>Design Authority &middot; the concept</b>"
              "<p>what an authority is, how agents consume it, and how it evolves, a page built on Triage foundations</p>"
              "<p><span class='chip'>concept</span> <span class='chip src'>open &rarr;</span></p></a>")
    return (DEMO_LANDING.replace("__CSS__", DEMO_CSS)
            .replace("__CARDS__", "".join(cards))
            .replace("__STRESS__", "".join(stress))
            .replace("__STRESS2__", "".join(stress2))
            .replace("__STRESS3__", "".join(stress3) + audit))


def _demo_page(name):
    pack = get_pack(name)
    g = golden_summary(name)
    m = pack.manifest
    counts = ("%d artifacts · %d rules · %d prohibitions · %d fallbacks · %d recipes"
              % (len(pack.artifacts), len(pack.rules), len(pack.prohibitions),
                 len(pack.fallbacks), len(pack.recipes)))
    meta = ("<span class='chip src'>pack %s</span><span class='chip'>v%s</span>"
            "<span class='chip'>%s</span><span class='chip'>%s</span>"
            "<span class='chip gold'>golden %d/%d</span>"
            "<a class='chip' href='/authorities/%s/gallery' style='text-decoration:none;color:inherit'>Gallery</a>"
            % (_esc(name), _esc(m.get("version")), _esc(pack_desc(name)),
               _esc(counts), g["passed"], g["total"], _esc(name)))
    chips = "".join("<button onclick=\"ask(&quot;%s&quot;)\">%s</button>" % (_esc(q), _esc(q))
                    for q in DEMO_EXAMPLES)

    rows = g.get("rows") or []
    grow = "".join(
        "<tr><td class='%s'>%s</td><td>%s</td><td>%s</td><td>%s</td><td class='mono'>%s</td></tr>"
        % ("ok" if r.get("ok") else "miss", "pass" if r.get("ok") else "MISS",
           _esc(r.get("problem")), _esc(r.get("expected")), _esc(r.get("got")),
           _esc(r.get("resolution_id") or "")) for r in rows)
    golden_html = ("<details><summary>%d / %d cases pass</summary><table>"
                   "<tr><th></th><th>ask</th><th>expected</th><th>got</th><th>resolved to</th></tr>%s"
                   "</table></details>" % (g["passed"], g["total"], grow))

    def art_html(a):
        body = a.get("body") or {}
        s = ["<div class='art'><span class='kd'>%s</span><b>%s</b> "
             "<span class='mono'>%s</span>" % (_esc(a.get("kind")), _esc(a.get("title")), _esc(a.get("id")))]
        s.append("<p class='s'>%s</p>" % _esc(a.get("summary")))
        if body.get("class"):
            s.append("<p class='sts'>class <span class='mono'>.%s</span></p>" % _esc(body["class"]))
        for st in (body.get("states") or []):
            s.append("<p class='sts'>· %s</p>" % _esc(st))
        return "".join(s) + "</div>"

    arts = "".join(art_html(a) for a in pack.artifacts)
    rules = "".join(
        "<div class='art'><span class='kd'>rule</span><b>%s · %s</b> <span class='mono'>%s</span>"
        "<p class='s'>%s</p><p class='sts'>fix: %s</p></div>"
        % (_esc(r.get("id")), _esc(r.get("name")), _esc(r.get("severity")),
           _esc(r.get("summary")), _esc(r.get("fix"))) for r in pack.rules)
    proh = "".join(
        "<div class='art'><b>%s</b><p class='s'>%s</p><p class='sts mono'>signals: %s</p></div>"
        % (_esc(p.get("id")), _esc(p.get("statement")),
           _esc(", ".join(p.get("signals", [])))) for p in pack.prohibitions)
    fbs = "".join(
        "<div class='art'><b>%s</b><p class='s'>%s</p><p class='sts mono'>scope: %s</p></div>"
        % (_esc(f.get("title")), _esc(f.get("statement")),
           _esc(", ".join(f.get("scope", [])))) for f in pack.fallbacks)
    if pack.recipes:
        recipes = "<h2>Recipes</h2>" + "".join(
            "<div class='art'><b>%s</b> <span class='mono'>%s</span><p class='s'>%s</p>"
            "<p class='sts'>· %s</p></div>"
            % (_esc(r.get("title")), _esc(r.get("id")), _esc(r.get("summary")),
               "</p><p class='sts'>· ".join(_esc(c) for c in r.get("constraints", [])))
            for r in pack.recipes)
    else:
        recipes = ("<h2>Recipes</h2><p class='sub'>None — flow-level behaviour was left "
                   "undefined in this authority (by review decision).</p>")

    prompt_path = os.path.join(PACKS_DIR, name, "AGENT-PROMPT.md")
    if os.path.exists(prompt_path):
        with open(prompt_path) as fh:
            prompt_md = fh.read()
        prompt_html = (
            "<h2>Implement with this authority — agent prompt</h2>"
            "<p class='sub'>A ready-to-send brief for coding agents building on this pack. "
            "Source: <span class='mono'>packs/%s/AGENT-PROMPT.md</span></p>"
            "<pre style=\"white-space:pre-wrap; background:#fff; border:1px solid #ddd; border-radius:0; "
            "padding:14px 16px; max-height:520px; overflow:auto; font-size:12px; line-height:1.55;\">%s</pre>"
            % (_esc(name), _esc(prompt_md)))
    else:
        prompt_html = ""

    page = (DEMO_PAGE
            .replace("__CSS__", DEMO_CSS)
            .replace("__TITLE__", _esc(m.get("name")))
            .replace("__DESC__", _esc(m.get("description")))
            .replace("__META__", meta)
            .replace("__CHIPS__", chips)
            .replace("__GOLDEN__", golden_html)
            .replace("__ARTS__", arts)
            .replace("__RULES__", rules)
            .replace("__PROH__", proh)
            .replace("__FB__", fbs)
            .replace("__RECIPES__", recipes + prompt_html)
            .replace("__PACK__", _esc(name)))
    return page


@app.route("/demo/<name>")
def demo_pack(name):
    if not is_pack(name):
        abort(404)
    return redirect("https://designauthority.seanyong.xyz/authorities/%s/audit" % name, code=308)


@app.route("/authorities/<name>/audit")
def authority_audit(name):
    if not is_pack(name):
        abort(404)
    if not _is_designauthority_host():
        return redirect("https://designauthority.seanyong.xyz/authorities/%s/audit" % name, code=308)
    page = _demo_page(name)
    # on the concept site there is no candidate hub; anchor the back-link home
    page = page.replace('<p><a class="back" href="/demo">&larr; all candidates</a></p>',
                        '<p><a class="back" href="/">&larr; designauthority.seanyong.xyz</a></p>')
    return Response(page, mimetype="text/html")


# ---- every authority's demo apps, one taxonomy: /authorities/<authority>/demo/<app> ----
AUTHORITY_APPS = {
    "triage": {"duty": os.path.join(_REPO, "examples", "triage-duty")},
    "phantom": {"jennu": os.path.join(_REPO, "examples", "phantom-audit")},
    "wink": {"cadence-v1": os.path.join(_REPO, "examples", "cadence-wink"),
             "cadence-v2": os.path.join(_REPO, "examples", "cadence2-wink"),
             "cadence-v3": os.path.join(_REPO, "examples", "cadence3-wink")},
    "leader": {"cadence-v1": os.path.join(_REPO, "examples", "cadence-leader"),
               "cadence-v2": os.path.join(_REPO, "examples", "cadence2-leader"),
               "cadence-v3": os.path.join(_REPO, "examples", "cadence3-leader")},
    "dominion": {"cadence-v1": os.path.join(_REPO, "examples", "cadence-dominion"),
                 "cadence-v2": os.path.join(_REPO, "examples", "cadence2-dominion"),
                 "cadence-v3": os.path.join(_REPO, "examples", "cadence3-dominion")},
}


def _concept_redirect():
    return redirect("https://designauthority.seanyong.xyz" + request.path, code=308)


@app.route("/authorities/")
def gallery_root():
    if not _is_designauthority_host():
        return redirect("https://designauthority.seanyong.xyz/authorities/", code=308)
    return _gal.render_root()


@app.route("/authorities")
def gallery_root_noslash():
    return redirect("/authorities/", code=308)


@app.route("/authorities/<name>/gallery")
def authority_gallery(name):
    if not is_pack(name):
        abort(404)
    if not _is_designauthority_host():
        return redirect("https://designauthority.seanyong.xyz/authorities/%s/gallery" % name, code=308)
    return _gal.render_gallery(name)


@app.route("/authorities/<name>/demo/<app>/")
def authority_demo_index(name, app):
    if not _is_designauthority_host():
        return _concept_redirect()
    d = AUTHORITY_APPS.get(name, {}).get(app)
    if not d or not os.path.isdir(d):
        abort(404)
    return send_from_directory(d, "index.html")


@app.route("/authorities/<name>/demo/<app>")
def authority_demo_noslash(name, app):
    if not _is_designauthority_host():
        return _concept_redirect()
    if app not in AUTHORITY_APPS.get(name, {}):
        abort(404)
    return redirect("/authorities/%s/demo/%s/" % (name, app), code=308)


@app.route("/authorities/<name>/demo/<app>/<path:fn>")
def authority_demo_file(name, app, fn):
    if not _is_designauthority_host():
        return _concept_redirect()
    d = AUTHORITY_APPS.get(name, {}).get(app)
    if not d or not os.path.isdir(d):
        abort(404)
    return send_from_directory(d, fn)


# jennu's learn page: a file page, no trailing-slash home
@app.route("/authorities/phantom/demo/jennu/learn")
def authority_jennu_learn():
    if not _is_designauthority_host():
        return _concept_redirect()
    return send_from_directory(AUTHORITY_APPS["phantom"]["jennu"], "learn.html")


@app.route("/authorities/phantom/demo/jennu/learn/")
def authority_jennu_learn_slash():
    return redirect("https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/learn", code=308)


@app.route("/stress/<name>/")
def stress_index(name):
    return redirect("https://designauthority.seanyong.xyz/authorities/%s/demo/cadence-v1/" % name, code=308)


@app.route("/stress/<name>/<path:fn>")
def stress_file(name, fn):
    return redirect("https://designauthority.seanyong.xyz/authorities/%s/demo/cadence-v1/%s" % (name, fn), code=308)


@app.route("/stress2/<name>/")
def stress2_index(name):
    return redirect("https://designauthority.seanyong.xyz/authorities/%s/demo/cadence-v2/" % name, code=308)


@app.route("/stress2/<name>/<path:fn>")
def stress2_file(name, fn):
    return redirect("https://designauthority.seanyong.xyz/authorities/%s/demo/cadence-v2/%s" % (name, fn), code=308)


@app.route("/stress3/<name>/")
def stress3_index(name):
    return redirect("https://designauthority.seanyong.xyz/authorities/%s/demo/cadence-v3/" % name, code=308)


@app.route("/stress3/<name>/<path:fn>")
def stress3_file(name, fn):
    return redirect("https://designauthority.seanyong.xyz/authorities/%s/demo/cadence-v3/%s" % (name, fn), code=308)


# ---- phantom audit review surface ----
AUDIT_WS = {"phantom": "phantom-audit"}


@app.route("/audit/<name>/")
def audit_index(name):
    if name != "phantom":
        abort(404)
    return redirect("https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/", code=308)


@app.route("/audit/<name>/<path:fn>")
def audit_file(name, fn):
    if name != "phantom":
        abort(404)
    return redirect("https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/" + fn, code=308)


# ---- designauthority.seanyong.xyz: the concept site (own hostname, same server) ----
DA_SITE = os.path.join(_REPO, "examples", "designauthority-site")


def _is_designauthority_host():
    h = (request.host or "").split(":")[0].lower()
    return h == "designauthority.seanyong.xyz"


# ---- the Jennu review at its public path (audit.seanyong.xyz/designAuthority/jennu/) ----
@app.route("/designAuthority/jennu/")
def jennu_index():
    return redirect("https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/", code=308)


@app.route("/designAuthority/jennu")
def jennu_index_noslash():
    return redirect("https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/", code=308)


@app.route("/designAuthority/jennu/<path:fn>")
def jennu_file(fn):
    return redirect("https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/" + fn, code=308)


@app.route("/designAuthority/jennu/learn")
def jennu_learn():
    return redirect("https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/learn", code=308)


@app.route("/designAuthority/jennu/learn/")
def jennu_learn_slash():
    return redirect("https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/learn", code=308)


# legacy spelling (jenmu) — keep old links working
@app.route("/designAuthority/jenmu/")
@app.route("/designAuthority/jenmu")
def jennu_legacy():
    return redirect("https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/", code=308)


@app.route("/designAuthority/jenmu/<path:fn>")
def jennu_legacy_file(fn):
    return redirect("https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/" + fn, code=308)


@app.route("/designAuthority/")
@app.route("/designAuthority")
def jennu_redirect():
    return redirect("https://designauthority.seanyong.xyz/authorities/phantom/demo/jennu/", code=308)


@app.route("/robots.txt")
def robots_txt():
    if _is_designauthority_host():
        return Response("User-agent: *\nAllow: /\n", mimetype="text/plain")
    return Response("User-agent: *\nDisallow: /\n", mimetype="text/plain")


@app.after_request
def _noindex_everything(resp):
    """The review host is noindex; the concept site (designauthority.) is its own public page."""
    if _is_designauthority_host():
        # jennu stays noindex: it is commentary about a third party's site
        if request.path.startswith("/authorities/phantom/demo/jennu"):
            resp.headers["X-Robots-Tag"] = "noindex, nofollow"
        else:
            resp.headers["X-Robots-Tag"] = "index, follow"
        return resp
    resp.headers["X-Robots-Tag"] = "noindex, nofollow"
    return resp


@app.route("/api/demo/resolve", methods=["POST"])
def demo_resolve():
    data = request.get_json(silent=True) or {}
    name = data.get("pack")
    problem = (data.get("problem") or "").strip()
    if not is_pack(name) or not problem:
        return jsonify({"error": "bad request"}), 400
    pack = get_pack(name)
    r = resolve(pack, problem)
    return jsonify({"html": render_resolution(pack, r)})


# ---- proposal gate (adjudication verdicts -> kernel records) ----
try:
    from proposed_renders import PROPOSED_RENDERS, RENDER_CSS
except ImportError:
    PROPOSED_RENDERS, RENDER_CSS = {}, ""
PROP_WS = {"cadence-wink": "wink", "cadence-leader": "leader", "cadence-dominion": "dominion"}
PROP_DRAFTS = os.path.join(DATA, "proposal-notes.json")
PROP_CSS = DEMO_CSS + RENDER_CSS + """
.prop{border:1.5px solid #141414;border-radius:10px;padding:14px 16px;margin:14px 0}
.prop .phead{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:8px}
.chip.st-candidate{background:#eee;color:#333}.chip.st-accepted{background:#087830;color:#fff}
.chip.st-rejected{background:#b3261e;color:#fff}.chip.st-needs-info{background:#8a5a00;color:#fff}
.secl{font:600 10.5px system-ui;letter-spacing:.07em;text-transform:uppercase;color:#888;margin:12px 0 3px}
.vb{display:flex;gap:6px;flex-wrap:wrap;margin-top:12px}
.vb button{font:600 11.5px system-ui;padding:8px 14px;border:1.5px solid #444;border-radius:6px;background:#fff;cursor:pointer}
.vb button.sel-a{background:#087830;color:#fff;border-color:#087830}
.vb button.sel-r{background:#b3261e;color:#fff;border-color:#b3261e}
.vb button.sel-n{background:#8a5a00;color:#fff;border-color:#8a5a00}
.verdict-note{width:100%;min-height:46px;font:13px/1.4 system-ui;padding:8px 10px;border:1.5px solid #cfcfcf;border-radius:6px;margin-top:8px;box-sizing:border-box}
.pstatus{font:12px system-ui;color:#666;margin:6px 0 0}
.fbar{display:flex;gap:6px;margin:10px 0;flex-wrap:wrap}
.fbar button{font:600 12px system-ui;padding:6px 12px;border:1.5px solid #141414;border-radius:999px;background:#fff;cursor:pointer}
.fbar button.sel{background:#141414;color:#fff}
.rec{border:1px solid #e4e4e4;border-radius:8px;padding:10px 12px;margin:8px 0}
.chip.cl-p{background:#087830;color:#fff}.chip.cl-f{background:#2E45B8;color:#fff}.chip.cl-n{background:#666;color:#fff}
.mddoc{margin:6px 0 14px}
.mddoc h1{font-size:17px;margin:12px 0 6px}.mddoc h2{font-size:14.5px;margin:12px 0 5px;border-bottom:1px solid #ddd;padding-bottom:4px}
.mddoc h3{font-size:13.5px;margin:10px 0 4px}
.mddoc p{margin:6px 0;font:13px/1.55 system-ui}.mddoc li{font:13px/1.55 system-ui;margin:3px 0}
.mddoc code{font:12px ui-monospace,monospace;background:#f6f6f6;padding:1px 4px;border-radius:3px}
.mddoc table{border-collapse:collapse;font:12.5px system-ui;margin:8px 0;width:100%}
.mddoc td,.mddoc th{border-bottom:1px solid #e4e4e4;padding:6px 8px;text-align:left;vertical-align:top}
.mddoc ul,.mddoc ol{margin:6px 0;padding-left:22px}
"""

PROV_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Proposal gate</title><style>__CSS__</style></head><body>
<div class="dwrap">
<p><a class="back" href="/demo">&larr; candidates demo</a></p>
<h1>Proposal gate — what the agents are promoting</h1>
<p class="sub">__N__ proposals from the adjudication pass, across three authorities. Inspect the full
record, then rule. Verdicts write straight to the kernel proposal records; accepted proposals are
compiled into the pack (versioned) with goldens + the stress sweep re-run.</p>
<div class="fbar" id="fb">
<button data-f="all" class="sel" onclick="filt(this)">All (__N__)</button>
<button data-f="candidate" onclick="filt(this)">Pending</button>
<button data-f="accepted" onclick="filt(this)">Accepted</button>
<button data-f="rejected" onclick="filt(this)">Rejected</button>
<button data-f="needs-info" onclick="filt(this)">Needs info</button>
</div>
<details id="record"><summary style="cursor:pointer;font:600 13.5px system-ui;padding:10px 0">
The adjudicator's record — all __TOTAL__ dispositions · __REC_SUM__ <span style="color:#2E45B8">(tap to audit every call, including the declines)</span></summary>
<div id="recbody">__RECORD__</div></details>
<h2 style="margin-top:22px">The full adjudication reports — the reasoning behind every call</h2>
<p class="sub">The complete documents the adjudicators wrote: method, per-gap re-verification, fix simulations, proposals, and the policy citations behind each decline.</p>
__REPORTS__
<div id="list">__CARDS__</div>
</div>
<script>
function post(u, b) {
  return fetch(u, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(b)})
    .then(function(r){ return r.json(); });
}
function toast(m) {
  var t = document.getElementById('pg-toast');
  if (!t) { t = document.createElement('div'); t.id = 'pg-toast'; document.body.appendChild(t);
    t.style.cssText = 'position:fixed;right:16px;bottom:16px;background:#141414;color:#fff;padding:11px 17px;'+
      'border-radius:9px;font:600 13px system-ui;opacity:0;transition:opacity .25s;z-index:99'; }
  t.textContent = m; t.style.opacity = 1;
  clearTimeout(t._t); t._t = setTimeout(function(){ t.style.opacity = 0; }, 2400);
}
function refresh(card, prop) {
  var st = prop.status || 'candidate';
  card.dataset.status = st;
  var sc = card.querySelector('.stchip'); sc.className = 'chip stchip st-' + st; sc.textContent = st;
  var v = prop.review && prop.review.verdict ? prop.review.verdict : '—';
  var extra = prop.review && prop.review.reviewed_at ? (' · ' + prop.review.reviewed_at) : '';
  card.querySelector('.pstatus').textContent = 'verdict: ' + v + extra;
  card.querySelectorAll('.vb button').forEach(function(b){
    b.className = (prop.review && b.dataset.v === prop.review.verdict) ? ('sel-' + b.dataset.v[0]) : '';
  });
  if (prop.review && prop.review.notes) { card.querySelector('textarea').value = prop.review.notes; }
}
function pv(btn) {
  var card = btn.closest('.prop');
  var note = card.querySelector('textarea').value;
  btn.disabled = true;
  post('/api/proposal/review', {ws: card.dataset.ws, id: card.dataset.pid, verdict: btn.dataset.v, note: note})
    .then(function(j){
      btn.disabled = false;
      if (j.error) { toast('error: ' + j.error); return; }
      refresh(card, j.prop); toast('recorded \u2713 ' + j.prop.review.verdict);
    }).catch(function(){ btn.disabled = false; toast('request failed'); });
}
function pn(ta) {
  var card = ta.closest('.prop');
  clearTimeout(card._t);
  card._t = setTimeout(function(){
    post('/api/proposal/note', {ws: card.dataset.ws, id: card.dataset.pid, note: ta.value})
      .then(function(j){ if (!j.error) { toast('draft note saved'); } });
  }, 900);
}
function filt(btn) {
  document.querySelectorAll('#fb button').forEach(function(b){ b.classList.toggle('sel', b === btn); });
  var f = btn.dataset.f;
  document.querySelectorAll('.prop').forEach(function(c){
    c.style.display = (f === 'all' || c.dataset.status === f) ? '' : 'none';
  });
}
document.addEventListener('DOMContentLoaded', function(){
  fetch('/api/proposals').then(function(r){ return r.json(); }).then(function(list){
    list.forEach(function(e){
      var card = document.querySelector('.prop[data-pid="' + e.id + '"]');
      if (!card) { return; }
      refresh(card, e);
      var ta = card.querySelector('textarea');
      if ((!e.review || !e.review.notes) && e.draft) { ta.value = e.draft; }
    });
  });
});
</script>
</body></html>"""


def load_adjudication():
    p = os.path.join(SYN, "data", "adjudication.json")
    if os.path.exists(p):
        with open(p) as fh:
            return json.load(fh)
    return []


def load_codified():
    p = os.path.join(SYN, "data", "codified.json")
    if os.path.exists(p):
        with open(p) as fh:
            return json.load(fh)
    return {}


def load_lenient():
    p = os.path.join(SYN, "data", "lenient.json")
    if os.path.exists(p):
        with open(p) as fh:
            return json.load(fh)
    return {}


def precedents_by_gap(src):
    """Map gap suffix -> precedent id, from the pack's precedents.json."""
    p = os.path.join(_REPO, "packs", src, "precedents.json")
    out = {}
    if os.path.exists(p):
        with open(p) as fh:
            for prec in (json.load(fh) or {}).get("precedents", []):
                gap = ((prec.get("provenance") or {}).get("gap_id") or "")
                if gap:
                    out[gap.split("-")[-1]] = prec.get("id")
    return out


def _md_inline(s):
    s = _esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", s)
    return s


def render_md(text):
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            rows = [ln]
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            t = ["<table>"]
            for k, r in enumerate(rows):
                cellsr = [c.strip() for c in r.strip().strip("|").split("|")]
                tag = "th" if k == 0 else "td"
                t.append("<tr>" + "".join("<%s>%s</%s>" % (tag, _md_inline(c), tag) for c in cellsr) + "</tr>")
            t.append("</table>")
            out.append("".join(t))
            continue
        if ln.startswith("# "):
            out.append("<h1>%s</h1>" % _md_inline(ln[2:]))
        elif ln.startswith("## "):
            out.append("<h2>%s</h2>" % _md_inline(ln[3:]))
        elif ln.startswith("### "):
            out.append("<h3>%s</h3>" % _md_inline(ln[4:]))
        elif re.match(r"^\s*[-*] ", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                items.append("<li>%s</li>" % _md_inline(re.sub(r"^\s*[-*] ", "", lines[i])))
                i += 1
            out.append("<ul>%s</ul>" % "".join(items))
            continue
        elif re.match(r"^\s*\d+\. ", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\. ", lines[i]):
                items.append("<li>%s</li>" % _md_inline(re.sub(r"^\s*\d+\. ", "", lines[i])))
                i += 1
            out.append("<ol>%s</ol>" % "".join(items))
            continue
        elif ln.strip():
            out.append("<p>%s</p>" % _md_inline(ln))
        i += 1
    return "".join(out)


def load_reports():
    docs = {}
    for src in ("wink", "leader", "dominion"):
        p = os.path.join(_REPO, "examples", "cadence-%s" % src, "ADJUDICATION.md")
        if os.path.exists(p):
            with open(p) as fh:
                docs[src] = fh.read()
    return docs


def _rec_row(r, prec=None, lin=None):
    ccls = {"PROPOSAL": "cl-p", "LEXICON-FIX": "cl-f", "SCOPE-FIX": "cl-f",
            "NO-ACTION": "cl-n", "INVALID": "cl-n"}.get(r["class"], "cl-n")
    if r.get("prop_id"):
        oc = ("<a class='back' href='#pc-%s'>promoted &rarr; %s</a>"
              % (r["prop_id"].replace("/", "-"), _esc(r.get("entry") or "")))
    elif r.get("outcome") == "fix-applied":
        oc = "<span style='color:#087830;font-weight:700'>fix applied &check; (verified)</span>"
    elif r.get("outcome") == "declined":
        mode = (lin or {}).get("mode", "deferred")
        cand = (lin or {}).get("candidate")
        if mode == "declined" and prec:
            oc = ("<span style='color:#666;font-weight:600'>declined &mdash; policy</span> "
                  "&rarr; <code>%s</code> (negative precedent)" % _esc(prec))
        elif mode == "candidate":
            oc = ("<span style='color:#087830;font-weight:600'>deferred &mdash; promoted to candidate</span> "
                  "<code>%s</code> (provisional, NOT authority)" % _esc(cand))
        elif mode == "split":
            oc = ("split &mdash; partly declined (<code>%s</code>) &middot; partly candidate (<code>%s</code>)"
                  % (_esc(prec), _esc(cand)))
        else:
            oc = ("<span style='color:#666;font-weight:600'>deferred to undefined</span> "
                  "&mdash; no negative precedent (lenient pass)")
    else:
        oc = _esc(r.get("outcome"))
    return ("<div class='rec'><span class='chip src'>%s</span> <span class='mono'>%s</span> "
            "<span class='chip %s'>%s</span> <b style='font-size:12.5px'>%s</b>"
            "<p class='dim' style='margin:5px 0 0'>%s</p>"
            "<p class='sts' style='margin-top:4px'>%s &nbsp; <a class='back' href='#adj-%s'>full reasoning &darr;</a></p></div>"
            % (_esc(r["src"]), _esc(r["suffix"]), ccls, _esc(r["class"]),
               _esc(r["need"]), _esc(r["rationale"]), oc, _esc(r["src"])))


def _prop_card(entry, adj=None, cod=None):
    ws, src, p = entry["ws"], entry["src"], entry["prop"]
    gap = entry.get("gap") or {}
    st = p.get("status") or "candidate"
    h = ["<div class='prop' data-ws='%s' data-pid='%s' data-status='%s'>"
         % (_esc(ws), _esc(p.get("id")), _esc(st))]
    h.append("<div class='phead'><span class='chip src'>%s</span>"
             "<span class='chip stchip st-%s'>%s</span>"
             "<span class='mono'>%s</span></div>"
             % (_esc(src), _esc(st), _esc(st), _esc(p.get("id"))))
    if gap.get("need"):
        h.append("<p class='dim'>from gap: %s — %s</p>"
                 % (_esc((p.get("gap_id") or "").split("/")[-1]), _esc(gap["need"])))
    if cod:
        if cod.get("outcome") == "codified":
            h.append("<p class='sts'><b style='color:#087830'>codified &#10003;</b> &rarr; pack <code>%s %s</code> &mdash; entries: %s</p>"
                     % (_esc(cod.get("pack")), _esc(cod.get("version")),
                        ", ".join("<code>%s</code>" % _esc(x) for x in cod.get("entries", []))))
        elif cod.get("outcome") == "precedent":
            h.append("<p class='sts'><b>rejected</b> &rarr; filed as <code>%s</code> (negative precedent — reaches agents via resolve, search and gap warnings)</p>"
                     % _esc(cod.get("precedent_id")))
        elif cod.get("outcome") == "pending":
            h.append("<p class='sts'><b>needs-info</b> — pending review; not codified</p>")
    if adj and adj.get("rationale"):
        h.append("<p class='secl'>Adjudicator's rationale</p><p class='main'>%s</p>" % _esc(adj["rationale"]))
        if adj.get("evidence"):
            h.append("<p class='dim'>re-verified: %s</p>" % _esc(adj["evidence"]))
        h.append("<p class='dim'><a class='back' href='#adj-%s'>read the full adjudication report &darr;</a></p>" % _esc(src))
    for label, key in (("Problem", "problem"), ("Insufficiency", "insufficiency"),
                       ("Reuse case", "reuse_case"), ("Composition check", "composition_check")):
        if p.get(key):
            h.append("<p class='secl'>%s</p><p class='main'>%s</p>" % (label, _esc(p[key])))
    h.append("<p class='secl'>Proposed — rendered</p>")
    suf = (p.get("id") or "").split("-")[-1]
    rend = PROPOSED_RENDERS.get(suf)
    if rend:
        h.append("<div class='renderwrap'><p class='cap'>rendered preview — as proposed, in this authority's styling</p>%s</div>" % rend)
    h.append("<p class='secl'>Proposed — record</p>")
    prop = p.get("proposed")
    if isinstance(prop, dict):
        h.append("<p class='main'><b>%s</b> <span class='mono'>%s</span> <span class='chip'>%s</span></p>"
                 % (_esc(prop.get("title")), _esc(prop.get("id", "")), _esc(prop.get("kind", ""))))
        for k in ("statement", "summary", "description"):
            if prop.get(k):
                h.append("<p class='main'>%s</p>" % _esc(prop[k]))
        if prop.get("aliases"):
            h.append("<p class='dim'>aliases: %s</p>" % _esc(", ".join(prop["aliases"])))
        body = prop.get("body") or {}
        for key in ("states", "a11y", "do", "dont"):
            for item in (body.get(key) or []):
                h.append("<p class='sts'>· <b>%s</b> — %s</p>" % (key, _esc(item)))
        entries = prop.get("entries") or []
        for e in entries:
            h.append("<p class='sts'>· %s</p>" % _esc(json.dumps(e, ensure_ascii=False)))
        if prop.get("notes"):
            h.append("<p class='dim'>%s</p>" % _esc(prop["notes"]))
    else:
        h.append("<pre class='mono' style='white-space:pre-wrap'>%s</pre>"
                 % _esc(json.dumps(prop, indent=1, ensure_ascii=False)[:2000]))
    if p.get("depends_on"):
        h.append("<p class='dim'>depends on: %s</p>" % _esc(", ".join(p["depends_on"])))
    if p.get("new_primitives"):
        h.append("<p class='dim'>new primitives declared: %s</p>" % _esc(", ".join(p["new_primitives"])))
    tests = p.get("tests") or {}
    if tests:
        h.append("<p class='secl'>Tests</p>")
        if isinstance(tests, list):
            for t in tests:
                if isinstance(t, dict):
                    h.append("<p class='sts'>· %s</p>" % _esc(json.dumps(t, ensure_ascii=False)))
                else:
                    h.append("<p class='sts'>· %s</p>" % _esc(t))
        else:
            for g in (tests.get("golden") or []):
                h.append("<p class='sts'>· golden: %s &rarr; %s%s</p>"
                         % (_esc(g.get("problem")), _esc(g.get("expect")),
                            (" (%s)" % _esc(g.get("expect_id"))) if g.get("expect_id") else ""))
            for c in (tests.get("checks") or []):
                h.append("<p class='sts'>· check: %s</p>" % _esc(c))
    h.append("<details><summary>full proposal JSON</summary>"
             "<pre class='mono' style='white-space:pre-wrap'>%s</pre></details>"
             % _esc(json.dumps(p, indent=1, ensure_ascii=False)))
    h.append("<div class='vb'><button data-v='accept' onclick=\"pv(this)\">ACCEPT &rarr; compile</button>"
             "<button data-v='reject' onclick=\"pv(this)\">REJECT</button>"
             "<button data-v='needs-info' onclick=\"pv(this)\">NEEDS INFO</button></div>")
    h.append("<textarea class='verdict-note' placeholder='review note — draft saves automatically; recorded with your verdict' oninput=\"pn(this)\" onblur=\"pn(this)\"></textarea>")
    h.append("<p class='pstatus'>verdict: —</p></div>")
    return "".join(h)


def _load_drafts():
    if os.path.exists(PROP_DRAFTS):
        with open(PROP_DRAFTS) as fh:
            return json.load(fh)
    return {}


def _save_drafts(d):
    with open(PROP_DRAFTS, "w") as fh:
        json.dump(d, fh, indent=1)


def load_proposals():
    out = []
    for ws, src in PROP_WS.items():
        wsdir = os.path.join(_REPO, "examples", ws)
        pdir = os.path.join(wsdir, ".design-authority", "proposals")
        gmap = {}
        gp = os.path.join(wsdir, ".design-authority", "gaps.jsonl")
        if os.path.exists(gp):
            for line in open(gp):
                try:
                    g = json.loads(line)
                    gmap[g["id"]] = g
                except ValueError:
                    pass
        if os.path.isdir(pdir):
            for fn in sorted(os.listdir(pdir)):
                if fn.endswith(".json"):
                    with open(os.path.join(pdir, fn)) as fh:
                        rec = json.load(fh)
                    out.append({"ws": ws, "src": src, "prop": rec,
                                "gap": gmap.get(rec.get("gap_id"))})
    return out


@app.route("/proposals")
def proposals_page():
    entries = load_proposals()
    adj = load_adjudication()
    codified = load_codified()
    prec_maps = {s: precedents_by_gap(s) for s in ("wink", "leader", "dominion")}
    adj_by_key = {(r["src"], r["suffix"]): r for r in adj}
    cards = "".join(
        _prop_card(e, adj_by_key.get((e["src"], (e["prop"].get("gap_id") or "").split("/")[-1].split("-")[-1])),
                   codified.get(e["prop"].get("id")))
        for e in entries)
    lenient = load_lenient()
    rec = []
    for srcc in ("wink", "leader", "dominion"):
        rows = [r for r in adj if r["src"] == srcc]
        if not rows:
            continue
        rec.append("<h3 style='margin:16px 0 6px;font-size:14px'>%s — %d dispositions</h3>" % (srcc, len(rows)))
        rec.extend(_rec_row(r, prec_maps[srcc].get(r["suffix"]),
                            (lenient.get(srcc) or {}).get(r["suffix"])) for r in rows)
    rec_html = "".join(rec)
    reps = load_reports()
    rep_html = "".join(
        "<details id='adj-%s'><summary style='cursor:pointer;font:600 13px system-ui;padding:8px 0'>"
        "%s — full adjudication report (%d lines, every method, simulation and policy citation)</summary>"
        "<div class='mddoc'>%s</div></details>"
        % (s, s, len(reps[s].split("\n")), render_md(reps[s])) for s in reps)
    n_p = sum(1 for r in adj if r["class"] == "PROPOSAL")
    n_f = sum(1 for r in adj if r["class"] in ("LEXICON-FIX", "SCOPE-FIX"))
    n_n = sum(1 for r in adj if r["class"] == "NO-ACTION")
    page = (PROV_PAGE.replace("__CSS__", PROP_CSS)
            .replace("__N__", str(len(entries)))
            .replace("__TOTAL__", str(len(adj)))
            .replace("__RECORD__", rec_html)
            .replace("__REC_SUM__", "%d promoted · %d fixes applied · %d declined" % (n_p, n_f, n_n))
            .replace("__REPORTS__", rep_html)
            .replace("__CARDS__", cards))
    return page


@app.route("/api/proposals")
def proposals_api():
    drafts = _load_drafts()
    out = []
    for e in load_proposals():
        p = e["prop"]
        out.append({"id": p.get("id"), "ws": e["ws"], "status": p.get("status"),
                    "review": p.get("review") or {},
                    "draft": drafts.get(e["ws"] + "|" + p.get("id", ""), "")})
    return jsonify(out)


@app.route("/api/proposal/review", methods=["POST"])
def proposal_review():
    data = request.get_json(silent=True) or {}
    ws = data.get("ws")
    pid = (data.get("id") or "").strip()
    verdict = (data.get("verdict") or "").strip().lower()
    note = data.get("note") or None
    if ws not in PROP_WS or not pid.startswith("prop/") or verdict not in ("accept", "reject", "needs-info"):
        return jsonify({"error": "bad request"}), 400
    ws_abs = os.path.join(_REPO, "examples", ws)
    try:
        rec = da_records.set_proposal_review(ws_abs, pid, verdict, notes=note)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    drafts = _load_drafts()
    drafts.pop(ws + "|" + pid, None)
    _save_drafts(drafts)
    return jsonify({"prop": {"id": rec.get("id"), "status": rec.get("status"),
                             "review": rec.get("review") or {}}})


@app.route("/api/proposal/note", methods=["POST"])
def proposal_note():
    data = request.get_json(silent=True) or {}
    ws = data.get("ws")
    pid = (data.get("id") or "").strip()
    if ws not in PROP_WS or not pid.startswith("prop/"):
        return jsonify({"error": "bad request"}), 400
    drafts = _load_drafts()
    drafts[ws + "|" + pid] = data.get("note") or ""
    _save_drafts(drafts)
    return jsonify({"ok": True})


# ---- stress-build decision review (cadence3 builds' marks layer) ----
STRESS_VERDICTS = os.path.join(DATA, "stress-verdicts.json")
STRESS_WS = {"wink": "cadence3-wink", "leader": "cadence3-leader", "dominion": "cadence3-dominion"}
STRESS_VOCAB = ("accept", "modify", "reject", "undefined")


def _load_stress_verdicts():
    try:
        with open(STRESS_VERDICTS) as f:
            return json.load(f)
    except Exception:
        return {}


@app.route("/api/stress/verdict", methods=["POST"])
def stress_verdict_post():
    data = request.get_json(silent=True) or {}
    ws = data.get("build")
    rid = str(data.get("id") or "").strip()
    verdict = (data.get("verdict") or "").strip().lower()
    if ws not in STRESS_WS or not rid or len(rid) > 24 or verdict not in STRESS_VOCAB:
        return jsonify({"error": "bad request"}), 400
    m = _load_stress_verdicts()
    key = ws + "|" + rid
    m[key] = {
        "verdict": verdict,
        "note": str(data.get("note") or "")[:2000],
        "ask": str(data.get("ask") or "")[:300],
        "updated": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    tmp = STRESS_VERDICTS + ".tmp"
    with open(tmp, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
    os.replace(tmp, STRESS_VERDICTS)
    return jsonify({"ok": True, "key": key, "verdict": verdict})


@app.route("/api/stress/verdicts")
def stress_verdicts_get():
    ws = request.args.get("build", "")
    if ws not in STRESS_WS:
        return jsonify({"error": "bad build"}), 400
    m = _load_stress_verdicts()
    return jsonify({k.split("|", 1)[1]: v for k, v in m.items() if k.startswith(ws + "|")})


if __name__ == "__main__":
    ensure_pages()
    # ---- files for the concept site, served only on its own hostname ----
@app.route("/<path:fn>")
def designauthority_file(fn):
    if _is_designauthority_host():
        return send_from_directory(DA_SITE, fn)
    abort(404)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8420, debug=False)
