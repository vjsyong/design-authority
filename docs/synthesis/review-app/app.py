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
from flask import (Flask, abort, jsonify, render_template_string, request,
                   send_from_directory)

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
<p class="sub">Review each decision card: verdict, notes, and image attachments save straight to disk. Safe to reload; come back any time.</p>
{{cards|safe}}
</body></html>"""


@app.route("/")
def index():
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


if __name__ == "__main__":
    ensure_pages()
    app.run(host="127.0.0.1", port=8420, debug=False)
