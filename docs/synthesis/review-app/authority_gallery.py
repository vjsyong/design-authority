#!/usr/bin/env python3
"""Authority gallery — every page a view over its pack (docs/12).

Discovery is filesystem-driven (`packs/*/authority.json`): dropping a pack
directory adds it everywhere, there is no list to edit. Freshness is
mtime-based: rebuild a pack and the next request renders the new content,
no service restart.

Consumed by app.py:
  /authorities/                gallery root (all authorities)
  /authorities/<name>/gallery  one authority, rendered from its records
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


def _status(version):
    v = version or ""
    if "-rc" in v:
        return ("release candidate", "cand")
    if "-experiment" in v:
        return ("experimental", "cand")
    return ("released", "rel")


def _chip(t, cls=""):
    return "<span class='gal-chip %s'>%s</span>" % (cls, _esc(t))


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


_HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<script>try{var d=document.documentElement,t=localStorage.getItem('triage_theme');if(t==='dark'||t==='light')d.setAttribute('data-theme',t);if(localStorage.getItem('triage_density')==='compact')d.setAttribute('data-density','compact');}catch(err){}</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__TITLE__</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/tokens/tokens.css">
<link rel="stylesheet" href="/assets/core/base.css">
<link rel="stylesheet" href="/assets/core/patterns.css">
<link rel="stylesheet" href="/assets/css/da-site.css">
<style>
.gal-wrap{max-width:var(--da-col);margin-inline:auto;padding:0 var(--space-20) var(--space-33)}
.gal-head{padding:var(--space-24) 0 var(--space-12);border-bottom:1px solid var(--border-default)}
.gal-head h1{margin:var(--space-4) 0 0}
.gal-strip{display:flex;flex-wrap:wrap;gap:var(--space-8);margin-top:var(--space-12)}
.gal-chip{display:inline-flex;align-items:center;border:1px solid var(--border-default);padding:2px var(--space-8);
  font-size:var(--fs-pre-log);font-family:var(--mono);color:var(--text-secondary);background:var(--surface-card);
  text-decoration:none}
.gal-chip.rel{border-color:var(--ok-line);color:var(--ok)}
.gal-chip.cand{border-color:var(--warn-line);color:var(--warn)}
.gal-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:var(--space-12);margin-top:var(--space-14)}
.gal-art{border:1px solid var(--border-default);background:var(--surface-card);padding:var(--space-12) var(--space-card)}
.gal-art h3,.gal-art b{font-size:var(--fs-sub)}
.gal-art .mono{font-size:var(--fs-pre-log);color:var(--text-secondary);font-family:var(--mono)}
.gal-art p{margin:var(--space-4) 0 0;font-size:var(--fs-pre-log);color:var(--text-soft)}
.gal-sec{padding:var(--space-20) 0 0;border-bottom:1px solid var(--border-default);margin-bottom:var(--space-20)}
.gal-sec:last-child{border-bottom:0}
.gal-sec h2{margin:0 0 var(--space-4)}
.gal-sub{color:var(--text-secondary);font-size:var(--fs-pre-log);margin:0 0 var(--space-10)}
.gal-prov{margin-top:var(--space-8);border-top:1px solid var(--border-default);padding-top:var(--space-6)}
.gal-links{display:flex;gap:var(--space-8);margin-top:var(--space-10);flex-wrap:wrap}
details.gal-golden{margin-top:var(--space-10)}
details.gal-golden table{border-collapse:collapse;font-size:var(--fs-pre-log);margin-top:var(--space-8)}
details.gal-golden td,details.gal-golden th{border:1px solid var(--border-default);padding:4px 8px;text-align:left}
.gal-kv{margin:0;font-size:var(--fs-pre-log);color:var(--text-soft);font-family:var(--mono)}
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
<main id="main" class="gal-wrap">__BODY__</main>
</body></html>"""


def _page(title, body):
    return _HEAD.replace("__TITLE__", _esc(title)).replace("__BODY__", body)


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
    if body.get("sources"):
        srcs = body["sources"]
        s.append("<p class='mono'>sources: %s</p>" % _esc(
            ", ".join("%s %s" % (k, v) for k, v in sorted(srcs.items()) if v)))
    if a.get("aliases"):
        s.append("<p class='mono'>aliases: %s</p>" % _esc(", ".join(a["aliases"])))
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


def _current_map():
    """CURRENT.json: which pack is the active line per authority (docs/12)."""
    try:
        with open(os.path.join(PACKS_DIR, "CURRENT.json")) as fh:
            m = json.load(fh) or {}
        return {k: v for k, v in m.items()
                if not k.startswith("_") and isinstance(v, str)}
    except Exception:
        return {}


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
            "<p class='da-sub'>Every authority below is a pack of machine-readable records. "
            "These pages are views over the packs: update a pack and the page follows.</p></div>"
            "<div class='gal-grid'>%s</div>" % "".join(cards))
    return _page("Design Authority · Authorities", body)


def render_gallery(name):
    e = get(name)
    if not e:
        return None
    pack, g = e["pack"], e["golden"]
    m = pack.manifest
    version = m.get("version") or ""
    label, cls = _status(version)

    chips = [_chip("v%s" % version, cls), _chip(label, cls)]
    if g:
        chips.append(_chip("golden %d/%d" % (g["passed"], g["total"]),
                           "rel" if g["passed"] == g["total"] else "cand"))
    chips.append(_chip("%d artifacts" % len(pack.artifacts)))
    if pack.rules:
        chips.append(_chip("%d rules" % len(pack.rules)))

    body = ["<div class='gal-head'><div class='da-kick'>Authority</div>"
            "<h1>%s</h1><p class='da-sub'>%s</p><div class='gal-strip'>%s</div></div>"
            % (_esc(m.get("name") or name), _esc(e["desc"]), "".join(chips))]

    # release & provenance strip (views over BUILD.json and the overlay)
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
    if kv:
        body.append("<section class='gal-sec' style='padding-top:var(--space-14)'>"
                    "<p class='gal-sub'>release</p>%s</section>"
                    % "".join("<p class='gal-kv'>%s</p>" % _esc(x) for x in kv))

    if g:
        rows = "".join(
            "<tr><td>%s</td><td>%s</td><td>%s</td><td class='gal-chip %s'>%s</td></tr>"
            % (_esc(r.get("problem", "")[:90]), _esc(r.get("expected", "")),
               _esc(r.get("got", "")), "rel" if r.get("ok") else "cand",
               _esc(r.get("resolution_id") or ""))
            for r in (g.get("rows") or []))
        body.append("<section class='gal-sec'><h2>Golden set</h2>"
                    "<details class='gal-golden'><summary>%d / %d cases pass</summary>"
                    "<table><tr><th>ask</th><th>expected</th><th>got</th><th>resolved to</th></tr>%s</table>"
                    "</details></section>" % (g["passed"], g["total"], rows))

    groups = {}
    for a in pack.artifacts:
        groups.setdefault(a["kind"], []).append(a)
    order = [k for k in _KIND_ORDER if k in groups] + [k for k in groups if k not in _KIND_ORDER]
    for kind in order:
        arts = groups[kind]
        body.append("<section class='gal-sec'><h2>%s</h2>"
                    "<p class='gal-sub'>%d record%s</p><div class='gal-grid'>%s</div></section>"
                    % (_esc(_KIND_TITLES.get(kind, kind.title())), len(arts),
                       "" if len(arts) == 1 else "s",
                       "".join(_art_card(a) for a in arts)))

    if pack.rules:
        cards = "".join(_plain_card("rule", "%s · %s" % (r.get("id"), r.get("name")),
                                    [r.get("summary"), "fix: %s" % r.get("fix", ""),
                                     "severity: %s" % r.get("severity", "")])
                        for r in pack.rules)
        body.append("<section class='gal-sec'><h2>Rules</h2>"
                    "<p class='gal-sub'>%d enforceable checks</p>"
                    "<div class='gal-grid'>%s</div></section>" % (len(pack.rules), cards))

    if pack.recipes:
        cards = "".join(_plain_card("recipe", r.get("title"),
                                    [r.get("summary"),
                                     "needs: %s" % ", ".join(r.get("needs", [])[:6]),
                                     "ingredients: %s" % ", ".join(r.get("ingredients", []))])
                        for r in pack.recipes)
        body.append("<section class='gal-sec'><h2>Recipes</h2>"
                    "<p class='gal-sub'>%d sanctioned compositions</p>"
                    "<div class='gal-grid'>%s</div></section>" % (len(pack.recipes), cards))

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

    body.append("<section class='gal-sec' id='use'><h2>Use this authority</h2>"
                "<p class='gal-sub'>packs/%s · the CLI and MCP serve it with "
                "<span class='mono'>--pack packs/%s</span></p></section>" % (_esc(name), _esc(name)))

    return _page("%s · Authority gallery" % (m.get("name") or name), "".join(body))
