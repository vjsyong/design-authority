#!/usr/bin/env python3
"""da_verify — independent conformance verifier (Design Authority verification experiment).

Consumes a pack's verification.json contract and a built app directory.
Establishes results from observable implementation evidence — source files,
rendered DOM, computed styles, scripted interaction — never from the
implementation agent's claims. Agent annotations (data-* marks) are usable
only as locator hints, never as proof.

Usage:
  python3 tools/da_verify.py --pack authorities/wink --target examples/cadence3-wink \
      --out docs/verification/raw/wink-clean [--json] [--no-shots]

Statuses: PASS · VIOLATION · UNVERIFIABLE · NOT_APPLICABLE · REVIEW_REQUIRED.
Ambiguous checks are never silently turned into PASS: a check whose target is
absent fails when the contract says missing=fail, otherwise it is UNVERIFIABLE.

Consumer mapping: a target may declare verify.map.json at its root to help the
contract engage a build that uses its own class names and file names:

  {
    "note": "optional",
    "files":     {"css": ["styles.css"], "html": ["index.html"], "js": ["app.js"]},
    "selectors": {".dlg": ".dialog", ".cta.outline": [".btn-outline"]},
    "ignore":    {"wink/ledger-head": "no table in this app"}
  }

  - files: substitutes for contract file names that do not exist (static scans).
    With no map, a missing app.css falls back to the target's own *.css files.
  - selectors: contract selector -> this app's selector (string or list).
  - ignore: check ids deliberately exempted here; they report NOT_APPLICABLE.

Playwright is required only for browser-backed modes (DOM / COMPUTED_STYLE /
INTERACTION); without it those checks report UNVERIFIABLE and STATIC checks
still run. Install for the full pass:
  pip install playwright && python -m playwright install chromium
"""
import argparse
import json
import os
import re
import socket
import subprocess
import sys
import time
import unicodedata

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
    PLAYWRIGHT_AVAILABILITY_ERR = ""
except Exception as _pw_exc:
    sync_playwright = None
    PLAYWRIGHT_AVAILABLE = False
    PLAYWRIGHT_AVAILABILITY_ERR = str(_pw_exc)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------- colours ----

def parse_color(s):
    """'rgb(1, 2, 3)' | 'rgba(1,2,3,.4)' | '#ffe01b' | 'hsl(146, 50%, 36%)' -> (r, g, b) | None"""
    c = parse_color4(s)
    return None if c is None else c[:3]


def hsl_to_rgb(h, s, l):
    """h in [0,360), s/l in [0,1] -> (r,g,b) floats."""
    def f(n):
        k = (n + h / 30.0) % 12
        a = s * min(l, 1 - l)
        return l - a * max(-1, min(k - 3, 9 - k, 1))
    return (f(0) * 255, f(8) * 255, f(4) * 255)


def parse_color4(s):
    """Parse hex / rgb() / rgba() / hsl() / hsla() -> (r, g, b, a) | None."""
    if not s:
        return None
    s = s.strip().lower()
    m = re.match(r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+%?))?\s*\)", s)
    if m:
        a = 1.0
        if m.group(4):
            g4 = m.group(4)
            a = float(g4[:-1]) / 100.0 if g4.endswith("%") else float(g4)
        return (float(m.group(1)), float(m.group(2)), float(m.group(3)), a)
    m = re.match(r"hsla?\(\s*([\d.]+)(?:deg)?[,\s]+([\d.]+)%?[,\s]+([\d.]+)%?(?:[,\s/]+([\d.]+%?))?\s*\)", s)
    if m:
        h, sat, l = float(m.group(1)), float(m.group(2)) / 100.0, float(m.group(3)) / 100.0
        a = 1.0
        if m.group(4):
            g4 = m.group(4)
            a = float(g4[:-1]) / 100.0 if g4.endswith("%") else float(g4)
        r, g, b = hsl_to_rgb(h % 360, sat, l)
        return (r, g, b, a)
    if s.startswith("#"):
        h = s[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) == 8:
            h = h[:6]
        if len(h) == 6:
            return (float(int(h[0:2], 16)), float(int(h[2:4], 16)), float(int(h[4:6], 16)), 1.0)
    return None


def colors_equal(a, b, tol=2.0):
    return a is not None and b is not None and all(abs(x - y) <= tol for x, y in zip(a, b))


def color_family(rgb):
    """Coarse hue family: red | blue | green | amber | neutral."""
    if rgb is None:
        return "unknown"
    r, g, b = [x / 255.0 for x in rgb]
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return "neutral"
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn) if (mx + mn) else 0
    if s < 0.12 or l < 0.06 or l > 0.95:
        return "neutral"
    if mx == r:
        h = (60 * ((g - b) / d)) % 360
    elif mx == g:
        h = 60 * ((b - r) / d) + 120
    else:
        h = 60 * ((r - g) / d) + 240
    if h < 25 or h > 335:
        return "red"
    if 25 <= h <= 70:
        return "amber"
    if 70 < h < 165:
        return "green"
    if 165 <= h <= 265:
        return "blue"
    return "other"


# ------------------------------------------------------------------ utils ----

def px(v, default=None):
    m = re.match(r"^\s*(-?[\d.]+)px", str(v))
    return float(m.group(1)) if m else default


def norm_ws(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def read_file(target, name):
    p = os.path.join(target, name)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None


# --------------------------------------------------- consumer mapping ---------

def load_verify_map(target):
    """Optional consumer-side mapping (verify.map.json at the target root)."""
    p = os.path.join(target, "verify.map.json")
    if not os.path.isfile(p):
        return None
    try:
        data = json.load(open(p))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    ign = data.get("ignore")
    if isinstance(ign, list):
        data["ignore"] = {str(x): "" for x in ign}
    return data


def map_selector(vmap, selector):
    """Resolve a contract selector through the consumer map (contract -> app)."""
    if not selector or not vmap:
        return selector
    m = (vmap.get("selectors") or {}).get(selector)
    if m is None:
        return selector
    if isinstance(m, list):
        return ", ".join(str(x) for x in m)
    return str(m)


def resolve_static_files(explicit, vmap, target):
    """Pick the files a static scan should read.

    An explicit contract file that EXISTS wins. A missing explicit file is
    substituted by the map's files of the same kind; with no map, by the
    target's own same-extension files at the root. If nothing exists, the
    original name is kept so the report still says what was expected.
    """
    def kind_of(f):
        if f.endswith(".css"):
            return "css"
        if f.endswith((".html", ".htm")):
            return "html"
        if f.endswith(".js"):
            return "js"
        return None

    def glob_kind(kind):
        ext = {"css": ".css", "html": ".html", "js": ".js"}.get(kind)
        if not ext:
            return []
        return sorted(f for f in os.listdir(target)
                      if f.endswith(ext) and os.path.isfile(os.path.join(target, f)))

    if not explicit:
        if vmap and (vmap.get("files") or {}):
            fl = []
            for kind in ("css", "html"):
                fl.extend(x for x in (vmap["files"].get(kind) or [])
                          if os.path.exists(os.path.join(target, x)))
            if fl:
                return fl
        if os.path.exists(os.path.join(target, "app.css")):
            return ["app.css"]
        gl = glob_kind("css")
        return gl or ["app.css"]

    resolved = []
    for f in explicit:
        if os.path.exists(os.path.join(target, f)):
            resolved.append(f)
            continue
        kind = kind_of(f)
        subs = ((vmap or {}).get("files") or {}).get(kind) if kind else None
        if subs:
            resolved.extend(s for s in subs if os.path.exists(os.path.join(target, s)))
            continue
        if not vmap and kind:
            gl = glob_kind(kind)
            if gl:
                resolved.extend(gl)
                continue
        resolved.append(f)  # keep the expectation visible
    existing = [f for f in resolved if os.path.exists(os.path.join(target, f))]
    return existing or resolved or ["app.css"]


def resolve_params(vmap, params):
    """Resolve selectors inside an INTERACTION check's params through the map."""
    if not vmap or not params:
        return params, {}
    mp = json.loads(json.dumps(params))
    notes = {}
    for key in ("trigger", "destructive", "selector"):
        if mp.get(key):
            res = map_selector(vmap, mp[key])
            if res != mp[key]:
                notes[key] = res
                mp[key] = res
    if mp.get("selectors"):
        mp["selectors"] = [map_selector(vmap, x) for x in mp["selectors"]]
    for step in mp.get("pre_steps") or []:
        if isinstance(step, list) and len(step) > 1 and step[0] in ("click", "fill"):
            res = map_selector(vmap, step[1])
            if res != step[1]:
                notes["step:%s" % step[1]] = res
                step[1] = res
    return mp, notes


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


# ----------------------------------------------------- static assertions ----

def strip_comments(text, kind="css"):
    """Remove comments before scanning: CSS never renders them, and an adversary
    hides decoys in prose (or breaks property:col scans with them)."""
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    if kind == "html":
        text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    return text


def strip_matching_rules(text, sel_regex):
    """Blank out entire CSS rules whose SELECTOR matches sel_regex.

    Only the instrument's own selectors are excluded (marks-on body scope,
    .mark-*, #provPanel, [data-mark]) — never a generic '[data-' prefix, which
    an adversary can satisfy from an ordinary element.
    """
    if not sel_regex:
        return text
    spans = [(m.start(), m.end()) for m in re.finditer(r"([^{}]*)\{([^{}]*)\}", text)
             if re.search(sel_regex, m.group(1))]
    for s, e in reversed(spans):
        text = text[:s] + " " * (e - s) + text[e:]
    return text


def static_assert(assertion, target, files):
    rel = assertion.get("relation")
    texts = {}
    for f in files or ["app.css"]:
        t = read_file(target, f)
        if t is None:
            return ("UNVERIFIABLE", f"file {f} not found")
        kind = "html" if f.endswith((".html", ".htm")) else "css"
        t = strip_comments(t, kind)
        texts[f] = strip_matching_rules(t, assertion.get("exclude_line_regex"))

    def effective_lines(text, except_re):
        if not except_re:
            return text.splitlines()
        return [ln for ln in text.splitlines() if not re.search(except_re, ln)]

    if rel == "no_match":
        pat = re.compile(assertion["pattern"], re.MULTILINE)
        for f, t in texts.items():
            for ln in effective_lines(t, assertion.get("except_line_regex")):
                if pat.search(ln):
                    return ("VIOLATION", f"{f}: '{norm_ws(ln)[:120]}'")
        return ("PASS", "no match")
    if rel == "present":
        pat = re.compile(assertion["pattern"], re.MULTILINE)
        for f, t in texts.items():
            if pat.search(t):
                return ("PASS", f"matched in {f}")
        return ("VIOLATION", f"pattern not found: {assertion['pattern']}")
    if rel == "declarations":
        prop = re.escape(assertion["property"])
        allow = re.compile(assertion["allow_regex"])
        found = 0
        for f, t in texts.items():
            for ln in effective_lines(t, assertion.get("except_line_regex")):
                for m in re.finditer(prop + r"\s*:\s*([^;}]*)", ln):
                    val = norm_ws(m.group(1))
                    if val in ("inherit", "initial", "unset", "revert"):
                        continue
                    found += 1
                    if not allow.search(val):
                        return ("VIOLATION", f"{f}: {assertion['property']}: {val[:120]}")
        return ("PASS", f"{found} declaration(s), all allowed")
    if rel == "color_literals":
        # every colour is parsed to (r,g,b,a); notation (hex / rgb / hsl) is irrelevant
        allows = []
        for hx in assertion.get("allow", []):
            c = parse_color4(hx)
            if c:
                allows.append(c)
        for rs in assertion.get("allow_rgb", []):
            parts = [p.strip() for p in rs.split(",")]
            if len(parts) >= 3:
                a4 = float(parts[3]) if len(parts) > 3 else None
                allows.append((float(parts[0]), float(parts[1]), float(parts[2]), a4))

        def allowed(rgba):
            r, g, b, a = rgba
            for ar, ag, ab, aa in allows:
                if abs(r - ar) <= 2 and abs(g - ag) <= 2 and abs(b - ab) <= 2:
                    if aa is None:
                        return True
                    if aa <= 0.05:
                        if a < 0.1:
                            return True
                    elif abs(a - aa) <= 0.1 or (aa >= 0.95 and a >= 0.1):
                        return True
            return False

        seen_ok, bad = 0, []
        tok_re = r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)"
        for f, t in texts.items():
            for ln in effective_lines(t, assertion.get("exclude_line_regex")):
                for m in re.finditer(tok_re, ln):
                    c = parse_color4(m.group(0))
                    if c is None:
                        continue
                    if allowed(c):
                        seen_ok += 1
                    else:
                        bad.append((f, m.group(0)[:32], norm_ws(ln)[:100]))
        if bad:
            return ("VIOLATION", "; ".join(f"{f}: {tok} in '{ln}'" for f, tok, ln in bad[:4]))
        return ("PASS", f"{seen_ok} literals, all allowlisted")
    if rel == "no_css_url_images":
        allow = re.compile(assertion.get("allow_regex", r"$^"))
        for f, t in texts.items():
            for m in re.finditer(r"url\(([^)]*)\)", t):
                if not allow.search(m.group(1)):
                    return ("VIOLATION", f"{f}: url({norm_ws(m.group(1))[:80]})")
        return ("PASS", "no image url() references")
    return ("UNVERIFIABLE", f"unknown static relation {rel}")


# -------------------------------------------------------- value checking ----

def check_computed_assertion(a, value, el_h):
    rel = a["relation"]
    v = a.get("value")

    def num(x):
        f = px(x)
        return f if f is not None else None

    if rel == "equals":
        if isinstance(v, str) and v.endswith("px") and num(value) is not None:
            return abs(num(value) - num(v)) <= 0.6
        c1, c2 = parse_color(v), parse_color(value)
        if c1 and c2:
            return colors_equal(c1, c2)
        return norm_ws(value).lower() == norm_ws(v).lower()
    if rel == "not_equals":
        if isinstance(v, str) and v.endswith("px") and num(value) is not None:
            return abs(num(value) - num(v)) > 0.6
        c1, c2 = parse_color(v), parse_color(value)
        if c1 and c2:
            return not colors_equal(c1, c2)
        return norm_ws(value).lower() != norm_ws(v).lower()
    if rel == "one_of":
        return any(check_computed_assertion({"relation": "equals", "value": x}, value, el_h) for x in v)
    if rel == "not_in":
        return all(not check_computed_assertion({"relation": "equals", "value": x}, value, el_h) for x in v)
    if rel == "contains":
        frags = v if isinstance(v, list) else [v]
        return all(frag.lower() in str(value).lower() for frag in frags)
    if rel == "not_contains":
        frags = v if isinstance(v, list) else [v]
        return all(frag.lower() not in str(value).lower() for frag in frags)
    if rel in ("min", "max"):
        f = num(value)
        if f is None:
            return None  # unverifiable
        return f >= float(v) if rel == "min" else f <= float(v)
    if rel == "pill":
        if "50%" in str(value):
            return True
        radii = [px(t) for t in re.split(r"[,\s]+", str(value)) if t]
        radii = [r for r in radii if r is not None]
        if not radii or not el_h:
            return None
        return max(radii) >= (el_h / 2.0) - 1.0
    if rel == "color_is":
        c = parse_color(value)
        return colors_equal(c, parse_color(v))
    if rel == "color_in":
        c = parse_color(value)
        return any(colors_equal(c, parse_color(x)) for x in v)
    if rel == "color_family":
        return color_family(parse_color(value)) == v
    if rel == "transition_max":
        durs = [float(x) for x in re.findall(r"([\d.]+)s", str(value))]
        return (max(durs) if durs else 0.0) <= float(v)
    return None  # unknown -> unverifiable


def check_evidence_assertion(a, evidence):
    rel = a["relation"]
    ev = evidence.get(a.get("evidence"))
    v = a.get("value")
    if ev is None:
        return None
    if rel == "equals":
        return ev == v
    if rel == "not_equals":
        return ev != v
    if rel in ("min", "max"):
        return ev >= v if rel == "min" else ev <= v
    if rel == "count_eq":
        return ev == v
    if rel == "contains":
        return str(v).lower() in str(ev).lower()
    if rel == "not_matches":
        return not re.search(str(v), str(ev), re.IGNORECASE)
    if rel == "all_contains":
        vals = ev if isinstance(ev, list) else [ev]
        return all(str(v).lower() in str(x).lower() for x in vals)
    if rel == "all_color_in":
        vals = ev if isinstance(ev, list) else [ev]
        allowed = [parse_color(x) for x in v]
        allowed = [x for x in allowed if x]
        for x in vals:
            c = parse_color(x)
            if c is None or not any(colors_equal(c, al) for al in allowed):
                return False
        return True
    return None


# ------------------------------------------------------- page scenarios ----

JS_RED = """
(r,g,b) => {
  r/=255; g/=255; b/=255;
  const mx = Math.max(r,g,b), mn = Math.min(r,g,b);
  if (mx === mn) return false;
  const d = mx - mn, l = (mx + mn) / 2;
  const s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn);
  if (s < 0.25 || l < 0.06 || l > 0.95) return false;
  let h; const rm = mx === r, gm = mx === g;
  if (rm) h = (60 * ((g - b) / d)) % 360;
  else if (gm) h = 60 * ((b - r) / d) + 120;
  else h = 60 * ((r - g) / d) + 240;
  if (h < 0) h += 360;
  return h < 25 || h > 335;
}
"""


def scenario_tab_focus(page, params):
    ev = {}
    for _ in range(6):
        page.keyboard.press("Tab")
        page.wait_for_timeout(40)
        info = page.evaluate("""(() => {
          const el = document.activeElement;
          if (!el || el === document.body || el === document.documentElement) return null;
          const cs = getComputedStyle(el);
          return { tag: el.tagName.toLowerCase(),
                   cls: (el.className || '').toString().slice(0, 60),
                   outline_style: cs.outlineStyle,
                   outline_width: parseFloat(cs.outlineWidth) || 0,
                   outline_color: cs.outlineColor };
        })()""")
        if info:
            ev["focus_element"] = f"{info['tag']}.{info['cls']}"
            ev["focus_outline_style"] = info["outline_style"]
            ev["focus_outline_width"] = info["outline_width"]
            ev["focus_outline_color"] = info["outline_color"]
            return ev
    ev.update({"focus_outline_style": "none", "focus_outline_width": 0,
               "focus_element": "(nothing focusable found)"})
    return ev


def scenario_open_delete(page, params):
    ev = {}
    trigger = params.get("trigger")
    node = page.query_selector(trigger) if trigger else None
    if node:
        node.click()
        page.wait_for_timeout(250)
    ev["dialog_open"] = bool(page.evaluate("!!document.querySelector('dialog[open]')"))
    dest = params.get("destructive", "")
    if dest:
        ev["destructive_found"] = bool(page.evaluate("!!document.querySelector(%s)" % json.dumps(dest)))
        ev["focus_is_destructive"] = bool(page.evaluate(
            "(() => { const a = document.activeElement; return a && a.matches(%s); })()" % json.dumps(dest)))
    else:
        ev["destructive_found"] = None
        ev["focus_is_destructive"] = None
    info = page.evaluate("""(() => { const a = document.activeElement;
        if (!a) return { tag: '', text: '' };
        return { tag: a.tagName.toLowerCase(), text: (a.textContent || '').trim().slice(0, 40) }; })()""")
    labels = params.get("destructive_labels", ["delete", "remove", "discard", "erase", "destroy", "forget", "clear"])
    ev["focus_text"] = info["text"]
    ev["focus_is_button"] = info["tag"] == "button"
    ev["focus_destructive_like"] = bool(info["tag"] == "button" and any(l in info["text"].lower() for l in labels))
    # restore state: close whatever we opened
    page.evaluate("document.querySelectorAll('dialog[open]').forEach(d => d.close())")
    page.wait_for_timeout(80)
    return ev


def scenario_focus_input(page, params):
    ev = {}
    sels = params.get("selectors") or ([params["selector"]] if params.get("selector") else ["input"])
    signals = []
    for sel in sels:
        page.evaluate("(() => { const el = document.querySelector(%s); if (el) el.focus(); })()" % json.dumps(sel))
        page.wait_for_timeout(140)
        sig = page.evaluate("""(() => {
          const el = document.querySelector(%s);
          if (!el) return '(not found: ' + %s + ')';
          const cs = getComputedStyle(el);
          return cs.boxShadow + ' | ' + cs.borderTopColor + ' | ' + cs.outlineColor + ' ' + cs.outlineStyle + ' ' + cs.outlineWidth;
        })()""" % (json.dumps(sel), json.dumps(sel)))
        signals.append(sig)
    ev["focus_signals"] = signals
    ev["focus_signal"] = " || ".join(signals)
    ev["focus_selector_count"] = len(sels)
    return ev


def scenario_red_area_scan(page, params):
    out = page.evaluate("""(() => {
      const isRed = %s;
      const vw = innerWidth, vh = innerHeight;
      let maxPct = 0, worst = '';
      let textPct = 0, textWorst = '';
      for (const el of document.querySelectorAll('*')) {
        const cs = getComputedStyle(el);
        const colors = [];
        if (cs.backgroundColor && !/rgba?\\(0, 0, 0, 0\\)/.test(cs.backgroundColor)) colors.push(cs.backgroundColor);
        if (cs.backgroundImage && cs.backgroundImage !== 'none') {
          const mm = cs.backgroundImage.match(/rgba?\\([^)]*\\)|#[0-9a-fA-F]{3,8}/g) || [];
          colors.push.apply(colors, mm);
        }
        let red = false;
        for (const col of colors) {
          const m = col.match(/rgba?\\((\\d+)[,\\s]+(\\d+)[,\\s]+(\\d+)(?:[,\\s]+([\\d.]+))?\\)/);
          if (m) {
            const a = m[4] === undefined ? 1 : parseFloat(m[4]);
            if (a >= 0.2 && isRed(+m[1], +m[2], +m[3])) { red = true; break; }
          } else if (col[0] === '#') {
            let h = col.slice(1); if (h.length === 3) h = h.split('').map(c => c + c).join('');
            if (h.length >= 6 && isRed(parseInt(h.slice(0,2),16), parseInt(h.slice(2,4),16), parseInt(h.slice(4,6),16))) { red = true; break; }
          }
        }
        if (!red) continue;
        const r = el.getBoundingClientRect();
        const pct = (r.width * r.height) / (vw * vh) * 100;
        if (pct > maxPct) { maxPct = pct; worst = (el.className || el.tagName) + ' ' + (cs.backgroundColor || '') + ' ' + (cs.backgroundImage || '').slice(0, 60); }
        const txt = (el.innerText || '').trim().length;
        if (txt >= 24 && r.height >= 20 && pct > textPct) { textPct = pct; textWorst = (el.className || el.tagName) + ' txt=' + txt; }
      }
      return { maxPct: Math.round(maxPct * 10) / 10, worst: String(worst).slice(0, 100),
               textPct: Math.round(textPct * 10) / 10, textWorst: String(textWorst).slice(0, 100) };
    })()""" % JS_RED)
    return {"red_max_area_pct": out["maxPct"], "red_worst": out["worst"],
            "red_text_surface_pct": out["textPct"], "red_text_worst": out["textWorst"]}


def scenario_red_status_scan(page, params):
    out = page.evaluate("""(() => {
      const isRed = %s;
      const sel = '.st, .err, .status, .notice, .error, .field-error';
      const hits = [];
      for (const el of document.querySelectorAll(sel)) {
        const cs = getComputedStyle(el);
        const checks = [['color', cs.color], ['border', cs.borderTopColor], ['border-left', cs.borderLeftColor], ['background', cs.backgroundColor]];
        for (const [prop, val] of checks) {
          const m = val && val.match(/rgba?\\((\\d+)[,\\s]+(\\d+)[,\\s]+(\\d+)(?:[,\\s]+([\\d.]+))?\\)/);
          if (!m) continue;
          const a = m[4] === undefined ? 1 : parseFloat(m[4]);
          if (a < 0.2) continue;
          if (isRed(+m[1], +m[2], +m[3])) {
            hits.push({ cls: String(el.className).slice(0, 50), prop, val });
          }
        }
      }
      return hits;
    })()""" % JS_RED)
    return {"red_role_hits": len(out), "red_role_detail": json.dumps(out[:3])[:220]}


def scenario_status_colour_scan(page, params):
    out = page.evaluate("""(() => {
      const els = [...document.querySelectorAll('.st')];
      const hits = [];
      let ok = els.length > 0;
      for (const el of els) {
        if (!el.textContent.trim()) ok = false;
        const cs = getComputedStyle(el);
        const m = cs.color.match(/rgba?\\((\\d+)[,\\s]+(\\d+)[,\\s]+(\\d+)/);
        if (!m) continue;
        const r = +m[1]/255, g = +m[2]/255, b = +m[3]/255;
        const mx = Math.max(r,g,b), mn = Math.min(r,g,b), l = (mx+mn)/2;
        const d = mx-mn;
        const s = (mx===mn) ? 0 : (l > 0.5 ? d/(2-mx-mn) : d/(mx+mn));
        if (s >= 0.25 && l > 0.15) { ok = false; hits.push({text: el.textContent.trim().slice(0,30), color: cs.color}); }
      }
      return { ok, hits, n: els.length };
    })()""")
    return {"status_colour_ok": out["ok"], "status_hits": out["n"],
            "status_detail": json.dumps(out["hits"][:3])[:200]}


def scenario_fixed_scan(page, params):
    import re as _re
    allow = _re.compile(params.get("allow_regex", "$^"))
    out = page.evaluate("""(() => {
      const rows = [];
      for (const el of document.querySelectorAll('*')) {
        if (el.closest('dialog')) continue;   // dialogs are a sanctioned overlay type
        const cs = getComputedStyle(el);
        if (cs.position !== 'fixed') continue;
        const r = el.getBoundingClientRect();
        rows.push({ cls: (el.className || '').toString() || el.tagName, id: el.id || '',
                    w: Math.round(r.width), h: Math.round(r.height),
                    vis: cs.visibility, disp: cs.display, op: cs.opacity });
      }
      return rows;
    })()""")
    unexpected = [r for r in out if not allow.search(r["cls"] + " " + r["id"]) and r["disp"] != "none"]
    return {"fixed_unexpected": len(unexpected), "fixed_detail": json.dumps(unexpected[:3])[:220]}


def run_steps(page, steps):
    """Execute a tiny deterministic scripted sequence (click / wait / press / fill)."""
    failed = []
    for step in steps or []:
        try:
            op = step[0]
            if op == "click":
                el = page.query_selector(step[1])
                if not el:
                    failed.append(f"click {step[1]}: not found")
                    continue
                try:
                    el.click(timeout=3000)
                except Exception:
                    el.evaluate("e => e.click()")  # JS fallback (headless hit-testing quirks)
            elif op == "wait":
                page.wait_for_timeout(int(step[1]))
            elif op == "press":
                page.keyboard.press(step[1])
            elif op == "fill":
                page.fill(step[1], step[2], timeout=3000)
            else:
                failed.append(f"unknown op {op}")
        except Exception as exc:
            failed.append(f"{step[0]} {step[1] if len(step) > 1 else ''}: {str(exc)[:70]}")
    return failed


def scenario_tab_walk(page, params):
    """Keyboard-walk up to N tab stops; every focused control needs a visible ring."""
    stops = int(params.get("stops", 20))
    samples, seen = [], set()
    for _ in range(stops):
        page.keyboard.press("Tab")
        page.wait_for_timeout(32)
        info = page.evaluate("""(() => {
          const el = document.activeElement;
          if (!el || el === document.body || el === document.documentElement) return null;
          const cs = getComputedStyle(el);
          const oc = (cs.outlineColor || '').match(/rgba?\\((\\d+)[,\\s]+(\\d+)[,\\s]+(\\d+)(?:[,\\s]+([\\d.]+))?\\)/);
          return { tag: el.tagName.toLowerCase(), cls: (el.className || '').toString().slice(0, 44),
                   style: cs.outlineStyle, width: parseFloat(cs.outlineWidth) || 0,
                   color: cs.outlineColor, alpha: oc && oc[4] ? parseFloat(oc[4]) : 1.0 };
        })()""")
        if info is None:
            continue
        label = f"{info['tag']}.{info['cls']}"
        if label in seen:
            continue
        seen.add(label)
        visible = info["style"] != "none" and info["width"] >= 1 and info["alpha"] >= 0.15
        samples.append({"el": label, "outline": f"{info['style']} {info['width']}px {info['color']}", "ok": bool(visible)})
    bad = [s for s in samples if not s["ok"]]
    return {"tab_samples": len(samples), "tab_bad": len(bad),
            "tab_bad_detail": json.dumps(bad[:5])[:280], "tab_sampled": json.dumps([s["el"] for s in samples])[:280]}


def scenario_shadow_census(page, params):
    import re as _re
    allow = _re.compile(params.get("allow_regex", "$^"))
    rows = page.evaluate("""(() => {
      const out = [];
      for (const el of document.querySelectorAll('*')) {
        const s = getComputedStyle(el).boxShadow;
        if (s && s !== 'none') out.push({ el: (el.className || el.tagName).toString().slice(0, 48), v: s.slice(0, 90) });
      }
      return out;
    })()""")
    unexpected = [r for r in rows if not allow.search(r["v"])]
    return {"shadow_found": len(rows), "shadow_unexpected": len(unexpected),
            "shadow_detail": json.dumps(unexpected[:3])[:240]}


def scenario_animation_census(page, params):
    rows = page.evaluate("""(() => {
      const out = [];
      for (const el of document.querySelectorAll('*')) {
        const s = getComputedStyle(el);
        if (s.animationName && s.animationName !== 'none') out.push({ el: (el.className || el.tagName).toString().slice(0, 48), v: s.animationName });
      }
      return out;
    })()""")
    return {"animations_found": len(rows), "animation_detail": json.dumps(rows[:4])[:240]}


def scenario_background_scan(page, params):
    import re as _re
    allow = _re.compile(params.get("allow_regex", "$^"))
    rows = page.evaluate("""(() => {
      const out = [];
      for (const el of document.querySelectorAll('*')) {
        const b = getComputedStyle(el).backgroundImage;
        if (b && b !== 'none' && b.indexOf('url(') !== -1 && out.length < 40) {
          out.push({ el: (el.className || el.tagName).toString().slice(0, 48), v: b.slice(0, 110) });
        }
      }
      return out;
    })()""")
    unexpected = [r for r in rows if not allow.search(r["v"])]
    return {"bg_url_found": len(rows), "bg_url_unexpected": len(unexpected),
            "bg_url_detail": json.dumps(unexpected[:3])[:240]}


def scenario_svg_census(page, params):
    max_count = int(params.get("max_count", 0))
    rows = page.evaluate("""(() => [...document.querySelectorAll('svg')].map(s => ({
        cls: (s.getAttribute('class') || ''), id: s.id || '' })))()""")
    return {"svg_count": len(rows), "svg_max": max_count,
            "svg_excess": max(0, len(rows) - max_count), "svg_detail": json.dumps(rows[:8])[:260]}


def scenario_computed_list(page, params):
    sel = params.get("selector", "body")
    prop = params.get("property", "background-color")
    vals = page.evaluate("""(args => [...document.querySelectorAll(args[0])].slice(0, 30).map(e => getComputedStyle(e)[args[1]]))""", [sel, prop])
    return {"values": vals, "values_count": len(vals)}


def scenario_border_ring_scan(page, params):
    """Outer ink rings (box-shadow 0 0 0 Npx) must not sit on a visible border —
    the classic double-stroke (a UA-default border under the ring)."""
    out = page.evaluate("""(() => {
      const rows = { ringed: 0, double: [] };
      for (const el of document.querySelectorAll('*')) {
        const cs = getComputedStyle(el);
        const sh = cs.boxShadow;
        if (!sh || sh === 'none' || sh.indexOf('inset') !== -1) continue;
        const i = sh.indexOf(' 0px 0px 0px ');
        if (i === -1) continue;
        const m = sh.slice(i + 13).match(/^([0-9.]+)px/);
        if (!m || parseFloat(m[1]) < 1) continue;
        rows.ringed++;
        const w = ['borderTopWidth','borderRightWidth','borderBottomWidth','borderLeftWidth'].map(p => parseFloat(cs[p]) || 0);
        const s = ['borderTopStyle','borderRightStyle','borderBottomStyle','borderLeftStyle'].map(p => cs[p]);
        const c = ['borderTopColor','borderRightColor','borderBottomColor','borderLeftColor'].map(p => cs[p]);
        const visible = w.some(x => x > 0) && s.some(x => x && x !== 'none') &&
                        c.some(x => x && x !== 'rgba(0, 0, 0, 0)' && x !== 'transparent');
        if (visible) rows.double.push({ el: (el.className || el.tagName).toString().slice(0, 48),
                                        ring: sh.slice(0, 50), border: w.join('/') + ' ' + c[0] });
      }
      return rows;
    })()""")
    return {"ringed_elements": out["ringed"], "double_stroke": len(out["double"]),
            "double_stroke_detail": json.dumps(out["double"][:3])[:240]}


SCENARIOS = {
    "border-ring-scan": scenario_border_ring_scan,
    "tab-focus": scenario_tab_focus,
    "tab-walk": scenario_tab_walk,
    "open-delete": scenario_open_delete,
    "focus-input": scenario_focus_input,
    "red-area-scan": scenario_red_area_scan,
    "red-status-scan": scenario_red_status_scan,
    "status-colour-scan": scenario_status_colour_scan,
    "fixed-scan": scenario_fixed_scan,
    "shadow-census": scenario_shadow_census,
    "animation-census": scenario_animation_census,
    "background-scan": scenario_background_scan,
    "svg-census": scenario_svg_census,
    "computed-list": scenario_computed_list,
}


# ------------------------------------------------------------------ main ----

def run_contract(pack_dir, target, out_dir, shots=True):
    contract = json.load(open(os.path.join(pack_dir, "verification.json")))
    vmap = load_verify_map(target)
    os.makedirs(out_dir, exist_ok=True)
    if shots:
        os.makedirs(os.path.join(out_dir, "screens"), exist_ok=True)
    results = []
    needs_browser = any(c["mode"] in ("DOM", "COMPUTED_STYLE", "ACCESSIBILITY", "INTERACTION")
                        for c in contract["checks"])
    server, proc, page, browser = None, None, None, None
    if needs_browser and not PLAYWRIGHT_AVAILABLE:
        print("note: playwright not available (%s) — browser-backed checks will "
              "report UNVERIFIABLE; static checks still run."
              % (PLAYWRIGHT_AVAILABILITY_ERR or "not installed"))
        needs_browser = False
    if needs_browser:
        port = free_port()
        proc = subprocess.Popen([sys.executable, "-m", "http.server", str(port),
                                 "--bind", "127.0.0.1", "--directory", os.path.abspath(target)],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        url = f"http://127.0.0.1:{port}/index.html"
        for _ in range(50):
            try:
                import urllib.request
                urllib.request.urlopen(url, timeout=1)
                break
            except Exception:
                time.sleep(0.1)
        pw = sync_playwright().start()
        browser = pw.chromium.launch()
        page = browser.new_context(viewport={"width": 1280, "height": 900}).new_page()
        page.on("pageerror", lambda e: None)
        page.goto(url, wait_until="load")
        page.wait_for_timeout(300)
        page.evaluate("localStorage.clear()")
        page.reload(wait_until="load")
        page.wait_for_timeout(350)
        # deterministic app state: dismiss the onboarding overlay if it opened
        page.evaluate("""(() => {
          const d = document.querySelector('dialog[open]');
          if (!d) return;
          const skip = d.querySelector('#wizSkip, [data-skip]');
          if (skip) skip.click(); else d.close();
        })()""")
        page.wait_for_timeout(250)
        if page.evaluate("!!document.querySelector('dialog[open]')"):
            page.keyboard.press("Escape")
            page.wait_for_timeout(150)
        # reveal hidden views once: geometry checks (pill radii, areas, text scans)
        # must see the whole app, not only the default view
        page.evaluate("document.querySelectorAll('[hidden]').forEach(e => { if (e.tagName !== 'DIALOG' && e.id !== 'provPanel') e.hidden = false; })")
        page.wait_for_timeout(150)

    try:
        for check in contract["checks"]:
            r = {"id": check["id"], "item": check.get("item"), "title": check.get("title"),
                 "classification": check["classification"], "severity": check.get("severity"),
                 "mode": check["mode"], "selector": check.get("selector"),
                 "status": None, "observed": [], "expected": [],
                 "evidence": {}, "screenshot": None, "note": check.get("note")}
            mode = check["mode"]

            ign = (vmap or {}).get("ignore") or {}
            if check["id"] in ign:
                r["status"] = "NOT_APPLICABLE"
                r["observed"] = ["consumer-mapped ignore: %s" % (ign.get(check["id"]) or "no reason given")]
                results.append(r)
                continue

            if mode == "REVIEW":
                r["status"] = "REVIEW_REQUIRED"
                results.append(r)
                continue

            if mode in ("DOM", "COMPUTED_STYLE", "ACCESSIBILITY", "INTERACTION") and page is None:
                r["status"] = "UNVERIFIABLE"
                r["observed"] = ["browser not available (%s) — install with: pip install playwright "
                                 "&& python -m playwright install chromium" % (PLAYWRIGHT_AVAILABILITY_ERR or "not installed")]
                results.append(r)
                continue

            outcomes = []
            evidence = {}

            if mode == "STATIC":
                static_files = resolve_static_files(check.get("files"), vmap, target)
                for a in check.get("assertions", []):
                    st, detail = static_assert(a, target, static_files)
                    outcomes.append((st, detail))
                    r["expected"].append(json.dumps(a)[:140])
                    r["observed"].append(detail)

            elif mode in ("DOM", "COMPUTED_STYLE") or (mode in ("INTERACTION",)):
                if mode == "INTERACTION":
                    scen = check.get("scenario")
                    fn = SCENARIOS.get(scen)
                    if fn is None:
                        outcomes.append(("UNVERIFIABLE", f"unknown scenario {scen}"))
                    else:
                        params, map_notes = resolve_params(vmap, check.get("params", {}) or {})
                        failed = run_steps(page, params.get("pre_steps", []))
                        evidence = fn(page, params)
                        if map_notes:
                            evidence["mapped_from"] = map_notes
                        if failed:
                            evidence["steps_failed"] = failed
                            if params.get("steps_required"):
                                outcomes.append(("UNVERIFIABLE", f"pre-steps failed: {json.dumps(failed)[:160]}"))
                        r["evidence"] = evidence
                        for a in check.get("assertions", []):
                            ok = check_evidence_assertion(a, evidence)
                            outcomes.append(("PASS" if ok else "VIOLATION", json.dumps(evidence)[:200]) if ok is not None
                                            else ("UNVERIFIABLE", "evidence key missing"))
                            r["expected"].append(json.dumps(a)[:140])
                else:
                    sel = map_selector(vmap, check.get("selector"))
                    if mode == "DOM" and not sel:
                        # page-level DOM assertions
                        for a in check.get("assertions", []):
                            rel = a["relation"]
                            if rel == "absent" and a.get("selector"):
                                n = page.evaluate("document.querySelectorAll(%s).length" % json.dumps(map_selector(vmap, a["selector"])))
                                outcomes.append(("PASS" if n == 0 else "VIOLATION", f"found {n}"))
                            elif rel == "page_text_no_match":
                                text = page.evaluate("""(() => {
                                  let t = document.body.innerText;
                                  for (const el of document.querySelectorAll('[placeholder],[title],[alt]')) {
                                    t += '\\n' + (el.getAttribute('placeholder') || '') + ' ' +
                                         (el.getAttribute('title') || '') + ' ' + (el.getAttribute('alt') || '');
                                  }
                                  return t;
                                })()""")
                                bad = "!" in text
                                emoji = [ch for ch in text if ord(ch) >= 0x1F000 or 0x2600 <= ord(ch) <= 0x27BF or 0xFE0F == ord(ch)]
                                if bad or emoji:
                                    outcomes.append(("VIOLATION", f"bang={bad} emoji={emoji[:5]}"))
                                else:
                                    outcomes.append(("PASS", "clean text + attributes"))
                            elif rel == "bil_pairs_ok":
                                out = page.evaluate("""(() => {
                                  const zw = s => (s || '').replace(/[\\u200B-\\u200F\\u2060\\uFEFF]/g, '').trim();
                                  const pairs = [...document.querySelectorAll('.bil')];
                                  let ok = 0; const bad = [];
                                  for (const p of pairs) {
                                    const en = p.querySelector('.en'), fr = p.querySelector('.fr');
                                    if (en && fr && zw(en.textContent) && zw(fr.textContent)) ok++;
                                    else bad.push(p.textContent.trim().slice(0, 40));
                                  }
                                  return { total: pairs.length, ok, bad: bad.slice(0,3) };
                                })()""")
                                r["evidence"] = out
                                if out["total"] >= 1 and out["ok"] == out["total"]:
                                    outcomes.append(("PASS", f"{out['ok']}/{out['total']} pairs"))
                                else:
                                    outcomes.append(("VIOLATION", f"{out['ok']}/{out['total']} pairs; bad: {out['bad']}"))
                            elif rel == "exists":
                                n = page.evaluate("document.querySelectorAll(%s).length" % json.dumps(map_selector(vmap, a["selector"])))
                                outcomes.append(("PASS" if n >= 1 else "VIOLATION", f"found {n}"))
                            elif rel == "no_css_url_images":
                                for f in resolve_static_files(a.get("files") or ["app.css"], vmap, target):
                                    st, detail = static_assert(a, target, [f])
                                    if st != "PASS":
                                        outcomes.append((st, detail))
                                        break
                                else:
                                    outcomes.append(("PASS", "no image url() references"))
                            else:
                                outcomes.append(("UNVERIFIABLE", f"unknown DOM relation {rel}"))
                        r["observed"] = [o[1] for o in outcomes]
                    else:
                        count = page.evaluate("document.querySelectorAll(%s).length" % json.dumps(sel)) if sel else 0
                        if count == 0:
                            sel_label = sel if sel == check.get("selector") else "%s (mapped to %s)" % (check.get("selector"), sel)
                            if check.get("missing") == "fail":
                                outcomes.append(("VIOLATION", f"selector '{sel_label}' not found"))
                            else:
                                outcomes.append(("UNVERIFIABLE", f"selector '{sel_label}' not found"))
                            r["observed"] = [o[1] for o in outcomes]
                        else:
                            if mode == "DOM":
                                for a in check.get("assertions", []):
                                    rel = a["relation"]
                                    a_sel = map_selector(vmap, a.get("selector", ""))
                                    scope_sel = (sel + " " + a_sel) if (sel and a_sel) else a_sel
                                    if rel == "text_len_min":
                                        tl = page.evaluate("""(sel => {
                                          const els = [...document.querySelectorAll(sel)].slice(0, 30);
                                          if (!els.length) return 0;
                                          const zw = s => (s || '').replace(/[\\u200B-\\u200F\\u2060\\uFEFF]/g, '').trim();
                                          return Math.min(...els.map(e => zw(e.textContent).length));
                                        })""", sel)
                                        outcomes.append(("PASS" if tl >= a["value"] else "VIOLATION", f"text length min {tl} of {min(count, 30)}"))
                                    elif rel == "absent":
                                        n = page.evaluate("document.querySelectorAll(%s).length" % json.dumps(scope_sel))
                                        outcomes.append(("PASS" if n == 0 else "VIOLATION", f"found {n} of {scope_sel}"))
                                    elif rel == "exists":
                                        n = page.evaluate("document.querySelectorAll(%s).length" % json.dumps(scope_sel))
                                        outcomes.append(("PASS" if n >= 1 else "VIOLATION", f"found {n} of {scope_sel}"))
                                    else:
                                        outcomes.append(("UNVERIFIABLE", f"unknown DOM relation {rel}"))
                                    r["expected"].append(json.dumps(a)[:140])
                            else:
                                n_cap = min(count, 30)
                                for a in check.get("assertions", []):
                                    prop = a["property"]
                                    worst, detail = None, ""
                                    for i in range(n_cap):
                                        res = page.evaluate(
                                            "(args => { const els = document.querySelectorAll(args[0]); if (args[1] >= els.length) return null; const e = els[args[1]]; const cs = getComputedStyle(e); let h = e.getBoundingClientRect().height; if (!h) { h = (parseFloat(cs.fontSize) || 12) * 1.2 + (parseFloat(cs.paddingTop) || 0) + (parseFloat(cs.paddingBottom) || 0) + (parseFloat(cs.borderTopWidth) || 0) + (parseFloat(cs.borderBottomWidth) || 0); } return { v: cs[args[2]], h }; })",
                                            [sel, i, prop])
                                        if res is None:
                                            continue
                                        ok = check_computed_assertion(a, res["v"], res["h"])
                                        if ok is False:
                                            worst, detail = "VIOLATION", f"[el {i + 1}/{count}] {prop}: {res['v']}"
                                            break
                                        if ok is None:
                                            if worst != "VIOLATION":
                                                worst, detail = "UNVERIFIABLE", f"[el {i + 1}/{count}] {prop}: {res['v']}"
                                        elif worst is None:
                                            worst, detail = "PASS", f"{prop}: {res['v']}" + (f" (all {count} ok)" if count > 1 else "")
                                    if worst is None:
                                        worst, detail = "UNVERIFIABLE", f"{prop}: no elements evaluated"
                                    outcomes.append((worst, detail))
                                    r["expected"].append(json.dumps(a)[:140])
                            r["observed"] = [o[1] for o in outcomes]
            else:
                outcomes.append(("UNVERIFIABLE", f"unknown mode {mode}"))

            # aggregate
            sts = [o[0] for o in outcomes]
            if not sts:
                r["status"] = "UNVERIFIABLE"
            elif "VIOLATION" in sts:
                r["status"] = "VIOLATION"
            elif "UNVERIFIABLE" in sts:
                r["status"] = "UNVERIFIABLE"
            else:
                r["status"] = "PASS"

            if r["status"] == "VIOLATION" and shots and page is not None:
                try:
                    shot = os.path.join(out_dir, "screens", re.sub(r"[^a-z0-9]+", "-", check["id"].lower()) + ".png")
                    page.screenshot(path=shot, full_page=False)
                    r["screenshot"] = os.path.relpath(shot, REPO)
                except Exception:
                    pass
            results.append(r)
    finally:
        if browser:
            browser.close()
        if proc:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()

    summary = {"total": len(results)}
    for key in ("PASS", "VIOLATION", "UNVERIFIABLE", "NOT_APPLICABLE", "REVIEW_REQUIRED"):
        summary[key] = sum(1 for r in results if r["status"] == key)
    by_mode = {}
    for r in results:
        m = by_mode.setdefault(r["mode"], {"PASS": 0, "VIOLATION": 0, "UNVERIFIABLE": 0, "REVIEW_REQUIRED": 0})
        m[r["status"]] = m.get(r["status"], 0) + 1

    raw = {"pack": contract["authority"], "contract_version": contract["contract_version"],
           "target": os.path.relpath(os.path.abspath(target), REPO),
           "generated": time.strftime("%Y-%m-%d %H:%M:%S"), "summary": summary,
           "by_mode": by_mode, "verify_map": vmap, "checks": results}
    with open(os.path.join(out_dir, "raw.json"), "w") as fh:
        json.dump(raw, fh, indent=1, ensure_ascii=False)

    na = summary.get("NOT_APPLICABLE", 0)
    lines = [f"# da_verify — {contract['authority']} on {raw['target']}",
             f"generated {raw['generated']}",
             f"TOTALS: {summary['total']} checks — PASS {summary['PASS']} · VIOLATION {summary['VIOLATION']} · "
             f"UNVERIFIABLE {summary['UNVERIFIABLE']} · REVIEW_REQUIRED {summary['REVIEW_REQUIRED']}"
             + (f" · N/A {na}" if na else ""), ""]
    for r in results:
        mark = {"PASS": "PASS ", "VIOLATION": "VIOL ", "UNVERIFIABLE": "UNV  ", "REVIEW_REQUIRED": "REVIEW",
                "NOT_APPLICABLE": "N/A  "}[r["status"]]
        obs = "; ".join(str(x) for x in r["observed"][:2])[:150]
        lines.append(f"{mark} [{r['severity']:7s}] {r['id']} — {obs}")
    report = "\n".join(lines)
    with open(os.path.join(out_dir, "summary.txt"), "w") as fh:
        fh.write(report + "\n")
    print(report)
    return raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-shots", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    raw = run_contract(args.pack, args.target, args.out, shots=not args.no_shots)
    if args.json:
        print(json.dumps(raw["summary"]))
    return 0 if raw["summary"]["VIOLATION"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
