#!/usr/bin/env python3
"""Authority sites — every page a view over its pack (docs/12).

Each authority gets a small documentation site in the Triage doc-site shape:
the system's own shell (side nav, topbar, content column), a page per
catalogue kind, a specification page, and links to the audit. All content is
rendered from the pack records: discovery is filesystem-driven and freshness
is mtime-based, so rebuilding a pack (or adding one) updates every page with
no edits and no restart.

Consumed by app.py:
  /authorities/                     gallery root (all authorities)
  /authorities/<name>/gallery       overview
  /authorities/<name>/gallery/<p>   components | patterns | guidelines |
                                    tokens | recipes | examples |
                                    references | spec
  /authorities/<name>/audit         the existing audit page
"""
import json
import os
import sys
from html import escape as _esc

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
PACKS_DIR = os.path.join(_REPO, "packs")
sys.path.insert(0, os.path.join(_REPO, "kernel"))

from design_authority.pack import Pack, PackError  # noqa: E402
from design_authority.resolve import resolve_golden  # noqa: E402

_FRESH_FILES = ("authority.json", "artifacts.json", "rules.json", "recipes.json",
                "fallbacks.json", "prohibitions.json", "precedents.json",
                "candidates.json", "golden.json")

# Presentation-only description overrides (membership is always discovered).
DESC_OVERRIDES = {
    "triage": "The app-agnostic paper-and-ink design authority behind triage.seanyong.xyz.",
    "triage-evolution": "The governed evolution line of Triage: agent updates land here first, as release candidates awaiting promotion.",
    "phantom": "The deployed language of zhenyoyo.github.io (extracted screenshot-first).",
    "wink": "Mailchimp brand + live product.",
    "leader": "Marber (The Economist) + live product.",
    "dominion": "Canada FIP + live Canada.ca web layer.",
}

_KIND_TITLES = {"component": "Components", "pattern": "Patterns",
                "guideline": "Guidelines", "token-set": "Token sets",
                "recipe": "Recipes", "example": "Examples", "reference": "References"}
_KIND_ORDER = ["component", "pattern", "guideline", "token-set", "recipe",
               "example", "reference"]
# nav slug -> artifact kind
_PAGE_KINDS = {"components": "component", "patterns": "pattern",
               "guidelines": "guideline", "tokens": "token-set",
               "recipes": "recipe", "examples": "example",
               "references": "reference"}
_PAGE_TITLES = {"overview": "Overview", "spec": "Rules & prohibitions"}
for _slug, _kind in _PAGE_KINDS.items():
    _PAGE_TITLES[_slug] = _KIND_TITLES[_kind]

_cache = {}


def _sig(d):
    sig = []
    for f in _FRESH_FILES:
        p = os.path.join(d, f)
        try:
            st = os.stat(p)
            sig.append((f, st.st_mtime_ns, st.st_size))
        except OSError:
            pass
    return tuple(sig)


def names():
    """All pack names, ordered: the triage lines first, then alphabetical."""
    if not os.path.isdir(PACKS_DIR):
        return []
    found = sorted(n for n in os.listdir(PACKS_DIR)
                   if os.path.isfile(os.path.join(PACKS_DIR, n, "authority.json")))
    first = ["triage", "triage-evolution"]
    return [n for n in first if n in found] + [n for n in found if n not in first]


def get(name):
    """{pack, golden, desc, sig} with mtime freshness; None if not a pack."""
    if not name or "/" in name or "\\" in name or name.startswith("."):
        return None
    d = os.path.join(PACKS_DIR, name)
    if not os.path.isfile(os.path.join(d, "authority.json")):
        return None
    sig = _sig(d)
    hit = _cache.get(name)
    if hit is not None and hit["sig"] == sig:
        return hit
    try:
        pack = Pack(d)
    except PackError:
        return None
    golden = None
    gp = os.path.join(d, "golden.json")
    if os.path.exists(gp):
        try:
            with open(gp) as fh:
                golden = resolve_golden(pack, json.load(fh)["cases"])
        except Exception:
            golden = None
    desc = DESC_OVERRIDES.get(name) or pack.manifest.get("description") or ""
    entry = {"pack": pack, "golden": golden, "desc": desc, "sig": sig}
    _cache[name] = entry
    return entry


def _current_map():
    """CURRENT.json: which pack is the active line per authority (docs/12)."""
    try:
        with open(os.path.join(PACKS_DIR, "CURRENT.json")) as fh:
            m = json.load(fh) or {}
        return {k: v for k, v in m.items()
                if not k.startswith("_") and isinstance(v, str)}
    except Exception:
        return {}


def _status(version):
    v = version or ""
    if "-rc" in v:
        return ("release candidate", "cand")
    if "-experiment" in v:
        return ("experimental", "cand")
    return ("released", "rel")


def _chip(t, cls=""):
    return "<span class='gal-chip %s'>%s</span>" % (cls, _esc(t))


def _abbr(name):
    words = [w for w in name.replace("-", " ").split() if w]
    if len(words) > 1:
        return "".join(w[0] for w in words)[:2].upper()
    return name[:2].upper()


def _counts(pack):
    kinds = {}
    for a in pack.artifacts:
        kinds[a["kind"]] = kinds.get(a["kind"], 0) + 1
    bits = ["%d %s" % (v, k) for k, v in sorted(kinds.items())]
    if pack.rules:
        bits.append("%d rules" % len(pack.rules))
    if pack.recipes:
        bits.append("%d recipes" % len(pack.recipes))
    return " · ".join(bits)


def _groups(pack):
    g = {}
    for a in pack.artifacts:
        g.setdefault(a["kind"], []).append(a)
    return g


_PRESCRIPT = ("<script>try{var d=document.documentElement,"
              "t=localStorage.getItem('triage_theme');"
              "if(t==='dark'||t==='light')d.setAttribute('data-theme',t);"
              "if(localStorage.getItem('triage_density')==='compact')d.setAttribute('data-density','compact');"
              "}catch(err){}</script>")

_GAL_CSS = """
.gal-head{padding:0 0 var(--space-14);border-bottom:1px solid var(--border-default);margin-bottom:var(--space-20)}
.gal-head h1{margin:var(--space-4) 0 0}
.gal-strip{display:flex;flex-wrap:wrap;gap:var(--space-8);margin-top:var(--space-12)}
.gal-chip{display:inline-flex;align-items:center;border:1px solid var(--border-default);padding:2px var(--space-8);
  font-size:var(--fs-pre-log);font-family:var(--mono);color:var(--text-secondary);background:var(--surface-card);
  text-decoration:none}
.gal-chip.rel{border-color:var(--ok-line);color:var(--ok)}
.gal-chip.cand{border-color:var(--warn-line);color:var(--warn)}
.gal-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:var(--space-12);margin-top:var(--space-14)}
.gal-art{border:1px solid var(--border-default);background:var(--surface-card);padding:var(--space-12) var(--space-card)}
.gal-art a{text-decoration:none;color:inherit}
.gal-art .mono{font-size:var(--fs-pre-log);color:var(--text-secondary);font-family:var(--mono)}
.gal-art p{margin:var(--space-4) 0 0;font-size:var(--fs-pre-log);color:var(--text-soft)}
.gal-sub{color:var(--text-secondary);font-size:var(--fs-pre-log);margin:0 0 var(--space-4)}
.gal-prov{margin-top:var(--space-8);border-top:1px solid var(--border-default);padding-top:var(--space-6)}
.gal-links{display:flex;gap:var(--space-8);margin-top:var(--space-10);flex-wrap:wrap}
.gal-kv{margin:0;font-size:var(--fs-pre-log);color:var(--text-soft);font-family:var(--mono)}
.gal-navcount{margin-inline-start:auto;color:var(--text-secondary);font-size:var(--fs-pre-log);font-family:var(--mono)}
.gal-sec{padding:var(--space-20) 0 0}
.gal-sec h2{margin:0 0 var(--space-4)}
.da-kick{font-size:var(--fs-pre-log);letter-spacing:.12em;text-transform:uppercase;color:var(--text-secondary);margin-bottom:var(--space-8)}
details.gal-golden{margin-top:var(--space-10)}
details.gal-golden table{border-collapse:collapse;font-size:var(--fs-pre-log);margin-top:var(--space-8)}
details.gal-golden td,details.gal-golden th{border:1px solid var(--border-default);padding:4px 8px;text-align:left}
"""

_MENU_JS = """
(function(){
  document.addEventListener('click', function(e){
    var t = e.target.closest && e.target.closest('[data-theme-toggle]');
    if (t) { var r=document.documentElement;
      var cur=r.getAttribute('data-theme')||(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
      var next=cur==='dark'?'light':'dark'; r.setAttribute('data-theme',next);
      try{localStorage.setItem('triage_theme',next);}catch(_){} }
    var d = e.target.closest && e.target.closest('[data-density-toggle]');
    if (d) { var r2=document.documentElement;
      var dens=r2.getAttribute('data-density')==='compact'?'':'compact';
      if(dens){r2.setAttribute('data-density',dens);}else{r2.removeAttribute('data-density');}
      try{localStorage.setItem('triage_density',dens||'comfortable');}catch(_){} }
    var m = e.target.closest && e.target.closest('#menuBtn');
    if (m) { var side=document.getElementById('side'), scrim=document.getElementById('scrim');
      var open=side.classList.toggle('open');
      scrim.classList.toggle('hidden', !open);
      m.setAttribute('aria-expanded', open?'true':'false'); }
    var s = e.target.closest && e.target.closest('#scrim');
    if (s) { document.getElementById('side').classList.remove('open');
      s.classList.add('hidden');
      var mb=document.getElementById('menuBtn'); if(mb){mb.setAttribute('aria-expanded','false');} }
  });
})();
"""


def _kind_nav(pack, name, current):
    base = "/authorities/%s/gallery" % name
    g = _groups(pack)
    out = ['<div class="nav-label">Authority</div>']
    act = ' active" aria-current="page' if current == "overview" else ""
    out.append('<a class="nav-item%s" href="%s">Overview</a>' % (act, base))
    out.append('<div class="nav-label">Catalogue</div>')
    for slug in _PAGE_KINDS:
        kind = _PAGE_KINDS[slug]
        arts = g.get(kind)
        if not arts:
            continue
        act = ' active" aria-current="page' if current == slug else ""
        out.append('<a class="nav-item%s" href="%s/%s">%s<span class="gal-navcount">%d</span></a>'
                   % (act, base, slug, _esc(_KIND_TITLES[kind]), len(arts)))
    if pack.rules or pack.prohibitions or pack.fallbacks:
        act = ' active" aria-current="page' if current == "spec" else ""
        n = len(pack.rules) + len(pack.prohibitions) + len(pack.fallbacks)
        out.append('<div class="nav-label">Specification</div>')
        out.append('<a class="nav-item%s" href="%s/spec">Rules &amp; prohibitions<span class="gal-navcount">%d</span></a>'
                   % (act, base, n))
    out.append('<div class="nav-label">Source</div>')
    out.append('<a class="nav-item" href="/authorities/%s/audit">Audit &amp; provenance</a>' % name)
    out.append('<a class="nav-item" href="/authorities/">All authorities</a>')
    return "".join(out)


def _shell(entry, name, current, body):
    pack = entry["pack"]
    m = pack.manifest
    version = m.get("version") or ""
    label, cls = _status(version)
    dot = "ok" if cls == "rel" else "warn"
    pname = m.get("name") or name
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
%s
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/tokens/tokens.css">
<link rel="stylesheet" href="/assets/core/base.css">
<link rel="stylesheet" href="/assets/core/patterns.css">
<style>%s</style>
</head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="app">
  <div class="scrim hidden" id="scrim"></div>
  <aside class="side" id="side" aria-label="%s navigation">
    <div class="side-top">
      <a class="brand" href="/authorities/%s/gallery"><span class="brand-mark">%s</span><span class="brand-name">%s</span></a>
      <div class="brand-sub">design authority v%s</div>
    </div>
    <nav class="nav">%s</nav>
    <div class="side-foot">
      <div class="sf-row"><span class="dot %s"></span><span>v%s · %s</span></div>
      <div class="sf-row"><span><a href="/authorities/%s/audit">audit &amp; provenance</a></span></div>
      <div class="sf-row">
        <button class="btn small" type="button" data-theme-toggle aria-label="Toggle dark theme">◐ theme</button>
        <button class="btn small" type="button" data-density-toggle aria-label="Toggle compact density">▤ density</button>
      </div>
    </div>
  </aside>
  <div class="main">
    <header class="topbar">
      <button class="iconbtn" id="menuBtn" aria-label="Open navigation" aria-expanded="false" aria-controls="side">☰</button>
      <span class="tb-title">%s</span>
      <button class="iconbtn" type="button" data-theme-toggle aria-label="Toggle dark theme">◐</button>
      <span class="tb-status"><span class="dot %s"></span>v%s</span>
    </header>
    <main id="main" class="content">
%s
      <div class="foot">%s · design authority v%s — rendered live from <span class="mono">packs/%s</span>; updates when the pack updates.</div>
    </main>
  </div>
</div>
<script>%s</script>
</body></html>""" % (_PRESCRIPT, _esc("%s · %s" % (pname, _PAGE_TITLES.get(current, current))),
                    _GAL_CSS, _esc(pname), name, _esc(_abbr(name)), _esc(pname),
                    _esc(version), _kind_nav(pack, name, current),
                    dot, _esc(version), _esc(label), name,
                    _esc(pname), dot, _esc(version), body,
                    _esc(pname), _esc(version), _esc(name), _MENU_JS)


def _art_card(a):
    body = a.get("body") or {}
    s = ["<article class='gal-art'>"]
    s.append("<div><span class='gal-chip'>%s</span></div>" % _esc(a.get("kind")))
    s.append("<p><b>%s</b></p>" % _esc(a.get("title")))
    s.append("<div class='mono'>%s</div>" % _esc(a.get("id")))
    if a.get("summary"):
        s.append("<p>%s</p>" % _esc(a["summary"]))
    if body.get("class"):
        s.append("<p class='mono'>class .%s</p>" % _esc(body["class"]))
    if body.get("path") and not body.get("sources"):
        s.append("<p class='mono'>file: %s</p>" % _esc(body["path"]))
    if body.get("states"):
        s.append("<p class='mono'>states: %s</p>" % _esc(" · ".join(body["states"])))
    if body.get("verify"):
        s.append("<p class='mono'>verify: %s</p>" % _esc("  ".join(body["verify"])))
    if body.get("a11y"):
        s.append("<p>a11y: %s</p>" % _esc(" ".join(body["a11y"])))
    if body.get("do"):
        s.append("<p class='mono'>do: %s</p>" % _esc(" · ".join(body["do"][:4])))
    if body.get("dont"):
        s.append("<p class='mono'>don't: %s</p>" % _esc(" · ".join(body["dont"][:4])))
    if body.get("quote"):
        s.append("<p>&ldquo;%s&rdquo;</p>" % _esc(body["quote"]))
    if body.get("sources"):
        srcs = body["sources"]
        s.append("<p class='mono'>sources: %s</p>" % _esc(
            ", ".join("%s %s" % (k, v) for k, v in sorted(srcs.items()) if v)))
    if a.get("aliases"):
        s.append("<p class='mono'>aliases: %s</p>" % _esc(", ".join(a["aliases"])))
    if a.get("relations"):
        s.append("<p class='mono'>%s</p>" % _esc(" · ".join(
            str(r.get("url") or r.get("id") or r.get("rel", "")) for r in a["relations"])))
    src = a.get("source") or {}
    if src.get("path"):
        tail = (" @ %s" % src["commit"][:10]) if src.get("commit") else ""
        s.append("<p class='mono'>source: %s%s</p>" % (_esc(src["path"]), _esc(tail)))
    prov = a.get("provenance")
    if prov:
        s.append("<div class='gal-prov'><p class='mono'>introduced in %s</p>"
                 "<p class='mono'>%s</p>"
                 % (_esc(prov.get("introduced_in", "")), _esc(prov.get("review_decision", ""))))
        for g in (prov.get("triggering_gaps") or [])[:3]:
            s.append("<p class='mono'>triggered by %s</p>" % _esc(g))
        s.append("</div>")
    s.append("</article>")
    return "".join(s)


def _plain_card(kind, title, lines):
    s = ["<article class='gal-art'>"]
    s.append("<div><span class='gal-chip'>%s</span></div>" % _esc(kind))
    s.append("<p><b>%s</b></p>" % _esc(title))
    for ln in lines:
        if ln:
            s.append("<p class='mono' style='color:var(--text-soft)'>%s</p>" % _esc(ln))
    s.append("</article>")
    return "".join(s)


def _release_block(name, pack):
    kv = []
    bj = os.path.join(PACKS_DIR, name, "BUILD.json")
    if os.path.exists(bj):
        try:
            b = json.load(open(bj))
            kv.append("built %s" % b.get("built_at", ""))
            snap = b.get("snapshot") or {}
            if snap.get("commit"):
                kv.append("snapshot %s @ %s" % (snap.get("version", ""), snap.get("commit", "")[:10]))
            if b.get("release"):
                kv.append("release label: %s (%s)" % (b["release"].get("label", ""),
                                                      b["release"].get("kind", "")))
        except Exception:
            pass
    provcount = sum(1 for a in pack.artifacts if a.get("provenance"))
    if provcount:
        kv.append("%d records carry provenance" % provcount)
    if not kv:
        return ""
    return ("<section class='gal-sec'><p class='gal-sub'>release</p>%s</section>"
            % "".join("<p class='gal-kv'>%s</p>" % _esc(x) for x in kv))


def _golden_block(g):
    if not g:
        return ""
    rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td class='gal-chip %s'>%s</td></tr>"
        % (_esc(r.get("problem", "")[:90]), _esc(r.get("expected", "")),
           _esc(r.get("got", "")), "rel" if r.get("ok") else "cand",
           _esc(r.get("resolution_id") or ""))
        for r in (g.get("rows") or []))
    return ("<section class='gal-sec'><h2>Golden set</h2>"
            "<details class='gal-golden'><summary>%d / %d cases pass</summary>"
            "<table><tr><th>ask</th><th>expected</th><th>got</th><th>resolved to</th></tr>%s</table>"
            "</details></section>" % (g["passed"], g["total"], rows))


def render_gallery(name, page="overview"):
    """One authority page; None when the pack or the page is unknown."""
    e = get(name)
    if not e or page not in _PAGE_TITLES:
        return None
    pack, g = e["pack"], e["golden"]
    m = pack.manifest
    version = m.get("version") or ""
    label, cls = _status(version)
    groups = _groups(pack)
    body = []

    if page == "overview":
        chips = [_chip("v%s" % version, cls), _chip(label, cls)]
        if g:
            chips.append(_chip("golden %d/%d" % (g["passed"], g["total"]),
                               "rel" if g["passed"] == g["total"] else "cand"))
        chips.append(_chip("%d artifacts" % len(pack.artifacts)))
        if pack.rules:
            chips.append(_chip("%d rules" % len(pack.rules)))
        body.append("<div class='gal-head'><div class='da-kick'>Authority</div>"
                    "<h1>%s</h1><p class='gal-sub' style='margin-top:var(--space-6);max-width:44rem'>%s</p>"
                    "<div class='gal-strip'>%s</div></div>"
                    % (_esc(m.get("name") or name), _esc(e["desc"]), "".join(chips)))
        body.append(_release_block(name, pack))
        cards = []
        for kind in _KIND_ORDER:
            arts = groups.get(kind)
            if not arts:
                continue
            slug = [s for s, k in _PAGE_KINDS.items() if k == kind][0]
            titles = ", ".join(a.get("title", "") for a in arts[:4])
            cards.append("<a href='/authorities/%s/gallery/%s'><article class='gal-art'>"
                         "<div><span class='gal-chip'>%s</span></div><p><b>%d %s</b></p>"
                         "<p>%s%s</p></article></a>"
                         % (name, slug, _esc(kind), len(arts),
                            _esc(_KIND_TITLES[kind].lower()), _esc(titles),
                            " …" if len(arts) > 4 else ""))
        if cards:
            body.append("<section class='gal-sec'><h2>Browse the catalogue</h2>"
                        "<div class='gal-grid'>%s</div></section>" % "".join(cards))
        body.append(_golden_block(g))

    elif page in _PAGE_KINDS:
        kind = _PAGE_KINDS[page]
        arts = groups.get(kind, [])
        body.append("<div class='gal-head'><div class='da-kick'>Catalogue</div>"
                    "<h1>%s</h1><p class='gal-sub'>%d record%s · %s</p></div>"
                    % (_esc(_KIND_TITLES[kind]), len(arts),
                       "" if len(arts) == 1 else "s", _esc(name)))
        if kind == "recipe":
            cards = "".join(_plain_card("recipe", r.get("title"),
                                        [r.get("summary"),
                                         "needs: %s" % ", ".join(r.get("needs", [])[:6]),
                                         "ingredients: %s" % ", ".join(r.get("ingredients", [])),
                                         "constraints: %s" % ", ".join(r.get("constraints", [])[:4])])
                            for r in pack.recipes)
        else:
            cards = "".join(_art_card(a) for a in arts)
        body.append("<div class='gal-grid'>%s</div>" % cards)

    elif page == "spec":
        body.append("<div class='gal-head'><div class='da-kick'>Specification</div>"
                    "<h1>Rules &amp; prohibitions</h1><p class='gal-sub'>%s</p></div>" % _esc(name))
        if pack.rules:
            cards = "".join(_plain_card("rule", "%s · %s" % (r.get("id"), r.get("name")),
                                        [r.get("summary"), "fix: %s" % r.get("fix", ""),
                                         "severity: %s" % r.get("severity", "")])
                            for r in pack.rules)
            body.append("<section class='gal-sec'><h2>Rules</h2>"
                        "<p class='gal-sub'>%d enforceable checks</p>"
                        "<div class='gal-grid'>%s</div></section>" % (len(pack.rules), cards))
        if pack.prohibitions:
            cards = "".join(_plain_card("prohibition", p.get("id"),
                                        [p.get("statement"),
                                         "signals: %s" % ", ".join(p.get("signals", []))])
                            for p in pack.prohibitions)
            body.append("<section class='gal-sec'><h2>Prohibitions</h2>"
                        "<div class='gal-grid'>%s</div></section>" % cards)
        if pack.fallbacks:
            cards = "".join(_plain_card("fallback", f.get("title"),
                                        [f.get("statement"),
                                         "scope: %s" % ", ".join(f.get("scope", []))])
                            for f in pack.fallbacks)
            body.append("<section class='gal-sec'><h2>Fallbacks</h2>"
                        "<div class='gal-grid'>%s</div></section>" % cards)

    return _shell(e, name, page, "".join(body))


def render_root():
    active = set(_current_map().values())
    cards = []
    for name in names():
        e = get(name)
        if not e:
            continue
        pack, g = e["pack"], e["golden"]
        m = pack.manifest
        version = m.get("version") or ""
        label, cls = _status(version)
        chips = [_chip("v%s" % version, cls), _chip(label, cls)]
        if name in active:
            chips.insert(0, _chip("active"))
        if g:
            chips.append(_chip("golden %d/%d" % (g["passed"], g["total"]),
                               "rel" if g["passed"] == g["total"] else "cand"))
        links = ("<div class='gal-links'>"
                 "<a class='gal-chip' href='/authorities/%s/gallery'>Gallery &rarr;</a>"
                 "<a class='gal-chip' href='/authorities/%s/audit'>Audit &rarr;</a>"
                 "</div>") % (name, name)
        cards.append(
            "<article class='gal-art'><p><b>%s</b></p><p>%s</p>"
            "<p class='mono'>%s</p><div class='gal-strip'>%s</div>%s</article>"
            % (_esc(m.get("name") or name), _esc(e["desc"]), _esc(_counts(pack)),
               "".join(chips), links))
    body = ("<div class='gal-head'><div class='da-kick'>Catalogue</div><h1>Authorities</h1>"
            "<p class='gal-sub' style='margin-top:var(--space-6);max-width:44rem'>"
            "Every authority below is a pack of machine-readable records. "
            "These pages are views over the packs: update a pack and the pages follow.</p></div>"
            "<div class='gal-grid'>%s</div>" % "".join(cards))
    return ("""<!doctype html><html lang="en"><head><meta charset="utf-8">
%s
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Design Authority · Authorities</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/tokens/tokens.css">
<link rel="stylesheet" href="/assets/core/base.css">
<link rel="stylesheet" href="/assets/core/patterns.css">
<link rel="stylesheet" href="/assets/css/da-site.css">
<style>%s
.gal-wrap{max-width:var(--da-col);margin-inline:auto;padding:var(--space-24) var(--space-20) var(--space-33)}
</style></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="da-top">
  <a class="da-brand" href="/" style="text-decoration:none;color:inherit">
    <span class="da-mark">DA</span>
    <div><b>Design Authority</b><span class="da-sub">Fuzzy Concepts to Enforceable Design</span></div>
  </a>
  <div class="da-controls">
    <a class="chip" href="/">Concept</a>
    <a class="chip" href="/authorities/">Authorities</a>
  </div>
</header>
<main id="main" class="gal-wrap">%s</main>
</body></html>""" % (_PRESCRIPT, _GAL_CSS, body))
