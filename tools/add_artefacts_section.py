#!/usr/bin/env python3
"""Add a usable 'Artefacts' directory section to every authority-built site.

Owner feedback: a visitor could see prose about the pack but had to guess where
the actual usable stuff was. This inserts, into each build at
examples/authority-sites/<auth>/:

  - a `section#artefacts` (before the Specification section) listing EVERY
    artifact in the pack, grouped by kind: title, id, status, summary, and a
    USE block with the recorded selector (body.class), states, a11y / verify
    notes, and aliases; plus a copy button that copies a ready-to-use snippet;
  - a live filter (name / alias / kind) with a live count;
  - a nav entry 'Artefacts' cloned from the page's existing Catalogue link
    (same classes, so it inherits the page's own nav styling);
  - a stylesheet block appended to styles.css using values traced from the
    authority's own records (the SAME values as the themes/builds);
  - inline JS (filter + copy) - no external anything.

Idempotent: re-runs replace the marked block instead of stacking duplicates.

    python3 tools/add_artefacts_section.py [--auth NAME ...]
"""
import argparse
import hashlib
import html as htmllib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES = os.path.join(ROOT, "examples", "authority-sites")

MARK_S = "<!-- artefacts-directory:start -->"
MARK_E = "<!-- artefacts-directory:end -->"
CSS_MARK_S = "/* artefacts-directory:start */"
CSS_MARK_E = "/* artefacts-directory:end */"

# Style values per authority, traced from each pack's token-set records and
# the authority-faithful builds (same trace as authority_themes.json).
STYLE = {
    "wink": {"ink": "#241C15", "dim": "#5D5245", "line": "#DEDDDC",
             "acc": "#007C89", "acc_ink": "#ffffff", "tint": "rgba(35,30,21,.05)", "label_color": "#231E15",
             "panel_r": "16px", "chip_r": "999px", "btn_r": "999px",
             # action controls: the page's own .cta IS component/action-pill
             # (yellow fill, 1px ink ring, Peppercorn label, pill radius).
             # Secondary (copy) = outline pill, 2px ink inset, per the record.
             "dl_class": "cta",
             "cp_fb": {"border": "2px solid #231E15", "color": "#241C15", "radius": "999px"},
             "_src": "component/action-pill (class .cta); token-set/colour; shape language: pills"},
    "leader": {"ink": "#101010", "dim": "#5A5A5A", "line": "#CFCFCF",
               "acc": "#2E45B8", "acc_ink": "#ffffff", "tint": "transparent", "panel_border": True, "label_color": "#E3120B",
               "panel_r": "8px", "chip_r": "4px", "btn_r": "8px",
               # action: primary solid navy #2E45B8 radius 8; secondary 2px ink outline
               "dl_fb": {"bg": "#2E45B8", "fg": "#ffffff", "radius": "8px"},
               "cp_fb": {"border": "2px solid #101010", "color": "#101010", "radius": "8px"},
               "_src": "component/action (primary navy #2E45B8 r8; secondary 2px ink); token-set/colour"},
    "dominion": {"ink": "#333333", "dim": "#595959", "line": "#E0E0E0",
                 "acc": "#26374A", "acc_ink": "#ffffff", "tint": "#F4F4F4",
                 "panel_r": "4px", "chip_r": "4px", "btn_r": "4px", "label_color": "#333333",
                 # action: primary solid slate #26374A radius 4 (live-measured)
                 "dl_fb": {"bg": "#26374A", "fg": "#ffffff", "radius": "4px"},
                 "cp_fb": {"border": "2px solid #26374A", "color": "#26374A", "radius": "4px"},
                 "_src": "component/action (solid slate #26374A r4); token-set/colour; no shadows"},
    "phantom": {"ink": "#ff6bbc", "dim": "#f2849e", "line": "#585858",
                "acc": "#f2849e", "acc_ink": "#ffffff", "tint": "transparent", "panel_border": True, "label_color": "#ff6bbc", "code_native": True,
                "panel_r": "4px", "chip_r": "4px", "btn_r": "4px", "code_bg": "#20a3f5",
                # action: the page's .button.primary IS the recorded primary
                # (solid #585858, white label); .button default = 2px ring state,
                # used for copies at the recorded small state (0.6em).
                "dl_class": "button primary", "cp_class": "button",
                "_src": "component/action-button (primary solid #585858; ring #585858; small 0.6em)"},
    "indaba": {"ink": "#111111", "dim": "#5F5F5F", "line": "#E5E1DE",
               "acc": "#E95420", "acc_ink": "#ffffff", "tint": "#F6F4F2",
               "panel_r": "12px", "chip_r": "999px", "btn_r": "999px", "label_color": "#77216F",
               # action: record defines .action.primary (orange), but the built
               # page ships no .action rules, so style from the record values.
               "dl_fb": {"bg": "#E95420", "fg": "#ffffff", "radius": "999px"},
               "cp_fb": {"border": "2px solid #E95420", "color": "#E95420", "radius": "999px"},
               "_src": "component/action (orange primary, focus ring); token-set/palette; warm tint"},
    "orbit": {"ink": "#101010", "dim": "#6F6F6F", "line": "#101010",
              "acc": "#D63829", "acc_ink": "#ffffff", "tint": "transparent",
              "panel_r": "0", "chip_r": "0", "btn_r": "0", "label_color": "#101010",
              # action: the page's .command IS the recorded control (primary =
              # solid accent via data-variant; default = ink-outlined square).
              "dl_class": "command", "dl_extra": ' data-variant="primary"',
              "cp_class": "command",
              "_src": "component/command (primary = solid accent); token-set/palette; square forms only"},
}


def esc(s):
    return htmllib.escape(str(s), quote=True)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def selector_for(body):
    cls = (body or {}).get("class")
    if not cls:
        return None
    cls = cls.strip()
    if re.fullmatch(r"[A-Za-z_][\w-]*", cls):
        return "." + cls
    return cls


def use_parts(rec):
    """Everything usable from a record: selector, states, notes."""
    b = rec.get("body") or {}
    parts = {}
    sel = selector_for(b)
    if sel:
        parts["selector"] = sel
    for key in ("states",):
        v = b.get(key)
        if v:
            parts[key] = [str(x) for x in v] if isinstance(v, list) else [str(v)]
    for key in ("a11y", "verify"):
        v = b.get(key)
        if v:
            parts[key] = v if isinstance(v, list) else [str(v)]
    return parts


def snippet_for(rec, parts):
    lines = ["%s - %s" % (rec["id"], rec.get("title", ""))]
    if parts.get("selector"):
        lines.append("selector: %s" % parts["selector"])
    if parts.get("states"):
        lines.append("states:")
        lines += ["- %s" % s for s in parts["states"]]
    for k in ("a11y", "verify"):
        if parts.get(k):
            lines.append("%s: %s" % (k, "; ".join(parts[k])))
    if not any(parts.get(k) for k in ("selector", "states")):
        lines.append("summary: %s" % rec.get("summary", ""))
    return "\n".join(lines)


def build_section(auth, pack, notice=None):
    arts = pack["artifacts"]["artifacts"] if isinstance(pack.get("artifacts"), dict) else pack["artifacts"]
    kind_order = pack.get("kinds") or []
    groups = {}
    for a in arts:
        groups.setdefault(a.get("kind", "other"), []).append(a)

    def kind_key(k):
        return (kind_order.index(k) if k in kind_order else 99, k)
    ordered = sorted(groups.items(), key=lambda kv: kind_key(kv[0]))

    st = STYLE[auth]
    dlc = (" " + st["dl_class"]) if st.get("dl_class") else ""
    dlextra = st.get("dl_extra", "")
    cpc = (" " + st["cp_class"]) if st.get("cp_class") else ""

    snippets = {}
    rows = []
    for kind, recs in ordered:
        label = kind.replace("-", " ").title() + ("s" if not kind.endswith("s") else "")
        rows.append('<h3 class="af-kindhead"><span class="af-lab">%s</span>'
                    '<span class="af-n">%d</span></h3>' % (esc(label), len(recs)))
        for r in sorted(recs, key=lambda x: x["id"]):
            rid = "a-" + slug(r["id"])
            parts = use_parts(r)
            snippets[rid] = snippet_for(r, parts)
            use = []
            if parts.get("selector"):
                use.append('<div class="af-line"><span class="af-key">selector</span>'
                           '<code class="af-sel">%s</code></div>' % esc(parts["selector"]))
            if parts.get("states"):
                items = "".join("<li>%s</li>" % esc(s) for s in parts["states"])
                use.append('<div class="af-line"><span class="af-key">states</span>'
                           '<ul class="af-states">%s</ul></div>' % items)
            for k in ("a11y", "verify"):
                if parts.get(k):
                    use.append('<div class="af-line"><span class="af-key">%s</span>'
                               '<span class="af-note">%s</span></div>'
                               % (k, esc("; ".join(parts[k]))))
            use_html = '<div class="af-use">%s</div>' % "".join(use) if use else ""
            aliases = r.get("aliases") or []
            alias_html = ('<span class="af-alias">also: %s</span>' % esc(" · ".join(aliases[:10]))) if aliases else ""
            status = r.get("status") or ""
            rows.append(
                '<article class="af-row" id="%s">'
                '<header class="af-head">'
                '<span class="af-kind">%s</span>'
                '<h4 class="af-title">%s</h4>'
                '<span class="af-status">%s</span>'
                '<code class="af-id">%s</code>'
                '</header>'
                '<p class="af-sum">%s</p>'
                '%s'
                '<div class="af-foot">%s'
                '<button type="button" class="af-copy%s" data-target="%s">copy</button>'
                '</div></article>'
                % (rid, esc(r.get("kind", "")), esc(r.get("title", "")), esc(status),
                   esc(r["id"]), esc(r.get("summary", "")), use_html, alias_html, cpc, rid))

    n = len(arts)
    ver = str(pack.get("version") or "")
    aname = pack.get("name") or auth
    agent_line = ("Fetch https://designauthority.seanyong.xyz/authorities/%s/site/agent-brief.md "
                  "and follow it to build my app under the %s authority." % (auth, aname))
    notice_html = ('<p class="af-notice">%s</p>' % esc(notice)) if notice else ""
    section = f"""{MARK_S}
<section id="artefacts" class="artefacts" data-added="artefacts-directory">
  <div class="af-kick">Artefacts · v{esc(ver)}</div>
  <h2 class="af-h2">All {n} artefacts, ready to use</h2>
  {notice_html}
  <p class="af-intro">Everything this authority records, in one place. Filter by name,
  alias or kind; every row carries its recorded selector and states, and the copy
  button yields a snippet you can drop straight into work. Full records live in the
  pack (<code>{esc(auth)}</code>) and its gallery.</p>
  <input class="af-filter" type="search" placeholder="filter: button, cta, colour, radius..." aria-label="Filter artefacts">
  <p class="af-count" id="af-count">showing all {n}</p>
  <div class="af-list">
  {''.join(rows)}
  </div>
  <div class="af-take">
    <h3 class="af-sub">Take it away</h3>
    <div class="af-take-row">
      <a class="af-dl{dlc}"{dlextra} href="download/{auth}-site.zip" download>Download everything (.zip)</a>
      <span class="af-note">The page, its styles and fonts, the whole pack, and the full audit trail in one file.</span>
    </div>
    <div class="af-take-row">
      <span class="af-key">one line for your agent</span>
      <code class="af-line-code" id="af-agentline">{agent_line}</code>
      <button type="button" class="af-copy af-copy-line{cpc}" data-copytext="af-agentline">copy</button>
    </div>
  </div>
  <script>
  (function() {{
    var SNIPPETS = {json.dumps(snippets)};
    var list = document.querySelector('#artefacts .af-list');
    var input = document.querySelector('#artefacts .af-filter');
    var count = document.getElementById('af-count');
    var rows = Array.from(list.querySelectorAll('.af-row'));
    var heads = Array.from(list.querySelectorAll('.af-kindhead'));
    function refresh() {{
      var q = (input.value || '').trim().toLowerCase();
      var shown = 0;
      rows.forEach(function(r) {{
        var hit = !q || r.textContent.toLowerCase().indexOf(q) !== -1;
        r.style.display = hit ? '' : 'none';
        if (hit) shown++;
      }});
      heads.forEach(function(h) {{
        var el = h.nextElementSibling, any = false;
        while (el && !el.classList.contains('af-kindhead')) {{
          if (el.classList.contains('af-row') && el.style.display !== 'none') any = true;
          el = el.nextElementSibling;
        }}
        h.style.display = any ? '' : 'none';
      }});
      count.textContent = q ? ('showing ' + shown + ' of {n}') : ('showing all {n}');
    }}
    input.addEventListener('input', refresh);
    list.addEventListener('click', function(e) {{
      var b = e.target.closest('.af-copy');
      if (!b) return;
      var text;
      if (b.getAttribute('data-copytext')) {{
        var el = document.getElementById(b.getAttribute('data-copytext'));
        text = el ? el.textContent : '';
      }} else {{
        text = SNIPPETS[b.getAttribute('data-target')] || '';
      }}
      function done() {{ b.textContent = 'copied'; b.classList.add('ok'); setTimeout(function() {{ b.textContent = 'copy'; b.classList.remove('ok'); }}, 1400); }}
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(text).then(done, done);
      }} else {{
        var ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta); ta.select();
        try {{ document.execCommand('copy'); }} catch (err) {{}}
        document.body.removeChild(ta); done();
      }}
    }});
  }})();
  </script>
</section>
{MARK_E}"""

    nat = st.get("code_native")
    chip_border = (" border: 1px solid %s;" % st["line"]) if (st["tint"] == "transparent" and not nat) else ""
    # non-native authorities: no monospace register exists in their records,
    # so strip the UA default and inherit the page's own font.
    ff = "" if nat else " font-family: inherit;"
    sel_rule = (".artefacts .af-sel { padding: .1rem .45rem; border-radius: %s;%s%s%s }"
                % (st["chip_r"], "" if nat else " background: %s;" % st["tint"], chip_border, ff))
    id_rule = (".artefacts .af-id { font-size: .78rem; color: %s; padding: .12rem .45rem; "
               "border-radius: %s;%s%s%s }"
               % (st["dim"], st["chip_r"], "" if nat else " background: %s;" % st["tint"], chip_border, ff))
    lc_rule = (".artefacts .af-line-code { font-size: .82rem; padding: .45rem .6rem; "
               "border-radius: %s;%s%s max-width: 100%%; overflow-wrap: anywhere; }"
               % (st["chip_r"], "" if nat else (" background: %s;%s" % (st["tint"], chip_border)), ff))
    use_rule = (".artefacts .af-use { background: %s;%s border-radius: %s; padding: .6rem .8rem; "
                "margin: .5rem 0 .6rem; }"
                % (st["tint"], " border: 1px solid %s;" % st["line"] if st.get("panel_border") else "",
                   st["panel_r"]))
    if st.get("dl_class"):
        dl_rule = (".artefacts .af-dl { display: inline-block; text-decoration: none; }"
                   " /* action treatment comes from the page's own recorded class */")
    else:
        fb = st["dl_fb"]
        dl_rule = (".artefacts .af-dl { display: inline-block; padding: .5rem 1.1rem; "
                   "background: %s; color: %s; border-radius: %s; text-decoration: none; "
                   "font-weight: 600; }" % (fb["bg"], fb["fg"], fb["radius"]))
    dl_rule += "\n.artefacts .af-dl:hover { opacity: .88; }"
    if st.get("cp_class"):
        cp_rule = (".artefacts .af-copy { margin-left: auto; font: inherit; font-size: .6em; "
                   "cursor: pointer; } /* recorded small state of the pack's action control */"
                   "\n.artefacts .af-copy:hover, .artefacts .af-copy.ok { opacity: .7; }")
    else:
        fb = st["cp_fb"]
        cp_rule = (".artefacts .af-copy { margin-left: auto; font: inherit; font-size: .82rem; "
                   "padding: .3rem .9rem; border: %s; border-radius: %s; background: transparent; "
                   "color: %s; cursor: pointer; }" % (fb["border"], fb["radius"], fb["color"]))
        cp_rule += "\n.artefacts .af-copy:hover, .artefacts .af-copy.ok { opacity: .7; }"
    css = f"""{CSS_MARK_S} /* styled from {auth} records: {st['_src']} */
.artefacts {{ margin: 3.5rem 0 1rem; padding-top: 1.5rem; border-top: 1px solid {st['line']}; }}
.artefacts .af-kick {{ font-size: .78rem; letter-spacing: .14em; text-transform: uppercase; color: {st['label_color']}; font-weight: 700; margin-bottom: .5rem; }}
.artefacts .af-h2 {{ font-size: 1.6rem; margin: 0 0 .6rem; }}
.artefacts .af-intro {{ color: {st['dim']}; max-width: 62ch; }}
.artefacts .af-notice {{ border-inline-start: 3px solid {st['label_color']}; padding: .5rem .8rem; margin: .6rem 0; background: {st['tint']}; border-radius: {st['panel_r']}; max-width: 76ch; }}
.artefacts .af-filter {{ width: 100%; max-width: 34rem; padding: .6rem .8rem; border: 1px solid {st['line']}; border-radius: {st['panel_r']}; background: transparent; color: inherit; font: inherit; margin: .6rem 0 .2rem; }}
.artefacts .af-count {{ font-size: .82rem; color: {st['dim']}; margin: .2rem 0 1.2rem; }}
.artefacts .af-kindhead {{ display: flex; align-items: baseline; gap: .6rem; margin: 1.8rem 0 .6rem; padding-bottom: .35rem; border-bottom: 1px solid {st['line']}; }}
.artefacts .af-kindhead .af-lab {{ font-size: .8rem; letter-spacing: .12em; text-transform: uppercase; color: {st['label_color']}; font-weight: 700; }}
.artefacts .af-kindhead .af-n {{ font-size: .8rem; color: {st['dim']}; }}
.artefacts .af-row {{ padding: .9rem 0 1rem; border-bottom: 1px solid {st['line']}; }}
.artefacts .af-head {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: .5rem .7rem; margin-bottom: .35rem; }}
.artefacts .af-kind {{ font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; color: {st['label_color']}; }}
.artefacts .af-title {{ font-size: 1.08rem; margin: 0; }}
.artefacts .af-status {{ font-size: .72rem; padding: .08rem .5rem; border: 1px solid {st['line']}; border-radius: {st['chip_r']}; color: {st['dim']}; }}
{id_rule}
.artefacts .af-sum {{ margin: .3rem 0 .6rem; max-width: 76ch; }}
{use_rule}
.artefacts .af-line {{ display: flex; flex-wrap: wrap; gap: .5rem; margin: .25rem 0; align-items: baseline; }}
.artefacts .af-key {{ font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; color: {st['label_color']}; min-width: 4.6rem; }}
{sel_rule}
.artefacts .af-states {{ margin: .1rem 0; padding-left: 1.1rem; font-size: .9rem; }}
.artefacts .af-note {{ font-size: .9rem; color: {st['dim']}; max-width: 70ch; }}
.artefacts .af-foot {{ display: flex; flex-wrap: wrap; align-items: center; gap: .8rem; }}
.artefacts .af-alias {{ font-size: .8rem; color: {st['dim']}; }}
{cp_rule}
.artefacts .af-take {{ margin-top: 2.2rem; padding-top: 1.2rem; border-top: 2px solid {st['line']}; }}
.artefacts .af-sub {{ font-size: 1.15rem; margin: 0 0 .8rem; }}
.artefacts .af-take-row {{ display: flex; flex-wrap: wrap; align-items: center; gap: .7rem; margin: .6rem 0; }}
{dl_rule}
{lc_rule}
{CSS_MARK_E}"""
    return section, css


def inject(auth, notice=None):
    build = os.path.join(SITES, auth)
    page_p = os.path.join(build, "index.html")
    if not os.path.isfile(page_p):
        print("skip %s (no build)" % auth)
        return False
    html = open(page_p).read()
    pack = json.load(open(os.path.join(ROOT, "packs", auth, "authority.json")))
    pack["artifacts"] = json.load(open(os.path.join(ROOT, "packs", auth, "artifacts.json")))
    section, css = build_section(auth, pack, notice=notice)

    # idempotency: strip previous block(s)
    html = re.sub(re.escape(MARK_S) + r".*?" + re.escape(MARK_E), "", html, flags=re.S)
    html = re.sub(r'<a[^>]*href="#artefacts"[^>]*>Artefacts</a>', "", html)

    # nav: clone the page's Catalogue link (same attrs/classes), new target
    m = re.search(r'<a([^>]*href="#catalogue"[^>]*)>(.*?)</a>', html, re.S)
    if m:
        attrs = re.sub(r'\s*href="#catalogue"', "", m.group(1))
        nav_link = '<a%s href="#artefacts">Artefacts</a>' % attrs
        html = html[:m.end()] + nav_link + html[m.end():]
        nav = "nav link cloned"
    else:
        nav = "NAV NOT FOUND (section only)"

    # insertion point: before the specification section, else before footer
    for pat in (r'<section[^>]*id="specification"', r"</main>", r"<footer"):
        mm = re.search(pat, html)
        if mm:
            html = html[:mm.start()] + section + "\n" + html[mm.start():]
            break
    else:
        html = html.replace("</body>", section + "\n</body>")

    open(page_p, "w").write(html)

    # css: strip old block, append new
    css_p = os.path.join(build, "styles.css")
    styles = open(css_p).read() if os.path.isfile(css_p) else ""
    styles = re.sub(re.escape(CSS_MARK_S) + r".*?" + re.escape(CSS_MARK_E), "", styles, flags=re.S)
    open(css_p, "w").write(styles.rstrip() + "\n\n" + css + "\n")

    # content-hash the stylesheet URL so every CSS change is a new URL for
    # every cache in the path (edge, browser, phone). No purges needed.
    css_sha = hashlib.sha256(open(css_p, "rb").read()).hexdigest()[:10]
    html = open(page_p).read()
    html = re.sub(r'href="styles\.css(\?[^"]*)?"',
                  'href="styles.css?v=%s"' % css_sha, html)
    open(page_p, "w").write(html)
    print("%s: section added (%s), %d artefacts" % (auth, nav, len(pack["artifacts"]["artifacts"])))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth", nargs="*", default=None)
    args = ap.parse_args()
    auths = args.auth or [d for d in sorted(os.listdir(SITES))
                          if os.path.isfile(os.path.join(SITES, d, "index.html"))]
    for a in auths:
        inject(a)


if __name__ == "__main__":
    main()
