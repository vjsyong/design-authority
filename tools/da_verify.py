#!/usr/bin/env python3
"""da_verify — independent conformance verifier (Design Authority verification experiment).

Consumes a pack's verification.json contract and a built app directory.
Establishes results from observable implementation evidence — source files,
rendered DOM, computed styles, scripted interaction — never from the
implementation agent's claims. Agent annotations (data-* marks) are usable
only as locator hints, never as proof.

Usage:
  python3 tools/da_verify.py --pack packs/wink --target examples/cadence3-wink \
      --out docs/verification/raw/wink-clean [--json] [--no-shots]

Statuses: PASS · VIOLATION · UNVERIFIABLE · NOT_APPLICABLE · REVIEW_REQUIRED.
Ambiguous checks are never silently turned into PASS: a check whose target is
absent fails when the contract says missing=fail, otherwise it is UNVERIFIABLE.
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

from playwright.sync_api import sync_playwright

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------- colours ----

def parse_color(s):
    """'rgb(1, 2, 3)' | 'rgba(1,2,3,.4)' | '#ffe01b' -> (r, g, b) | None"""
    if not s:
        return None
    s = s.strip().lower()
    m = re.match(r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)", s)
    if m:
        return (float(m.group(1)), float(m.group(2)), float(m.group(3)))
    if s.startswith("#"):
        h = s[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) == 8:
            h = h[:6]
        if len(h) == 6:
            return (float(int(h[0:2], 16)), float(int(h[2:4], 16)), float(int(h[4:6], 16)))
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


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


# ----------------------------------------------------- static assertions ----

def strip_matching_rules(text, sel_regex):
    """Blank out entire CSS rules whose SELECTOR matches sel_regex.

    Property lines inside a matching rule would otherwise escape line-based
    exclusion (e.g. instrument rules whose selector is on the previous line).
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
        allow = {c.lower() for c in assertion.get("allow", [])}
        allow_rgb = [tuple(float(x) for x in s.split(",")) for s in assertion.get("allow_rgb", [])]
        seen_ok, bad = 0, []
        for f, t in texts.items():
            for ln in effective_lines(t, assertion.get("exclude_line_regex")):
                for m in re.finditer(r"#[0-9a-fA-F]{3,8}\b", ln):
                    tok = m.group(0).lower()
                    if len(tok) == 4:  # expand shorthand #abc -> #aabbcc
                        tok = "#" + "".join(c * 2 for c in tok[1:])
                    if tok in allow:
                        seen_ok += 1
                        continue
                    h = tok[1:]
                    if len(h) in (3, 6):
                        bad.append((f, tok, norm_ws(ln)[:100]))
                for m in re.finditer(r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)", ln):
                    triple = (float(m.group(1)), float(m.group(2)), float(m.group(3)))
                    if any(all(abs(a - b) <= 2 for a, b in zip(triple, ref)) for ref in allow_rgb):
                        seen_ok += 1
                        continue
                    bad.append((f, "rgb%s" % (triple,), norm_ws(ln)[:100]))
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
    ev["focus_is_destructive"] = bool(page.evaluate(
        "(() => { const a = document.activeElement; return a && %s ? a.matches(%s) : false; })()"
        % ("true", json.dumps(dest))))
    ev["focus_element"] = page.evaluate("(document.activeElement && (document.activeElement.id || document.activeElement.className || document.activeElement.tagName)) + ''")
    # restore state: close whatever we opened
    page.evaluate("document.querySelectorAll('dialog[open]').forEach(d => d.close())")
    page.wait_for_timeout(80)
    return ev


def scenario_focus_input(page, params):
    ev = {}
    sel = params.get("selector", "input")
    page.evaluate("(() => { const el = document.querySelector(%s); if (el) el.focus(); })()" % json.dumps(sel))
    page.wait_for_timeout(160)
    sig = page.evaluate("""(() => {
      const el = document.querySelector(%s);
      if (!el) return null;
      const cs = getComputedStyle(el);
      return { shadow: cs.boxShadow, border: cs.borderTopColor, outline: cs.outlineColor + ' ' + cs.outlineStyle + ' ' + cs.outlineWidth };
    })()""" % json.dumps(sel))
    if sig is None:
        ev["focus_signal"] = "(input not found)"
    else:
        ev["focus_signal"] = f"{sig['shadow']} | {sig['border']} | {sig['outline']}"
    return ev


def scenario_red_area_scan(page, params):
    out = page.evaluate("""(() => {
      const isRed = %s;
      const vw = innerWidth, vh = innerHeight;
      let maxPct = 0, worst = '';
      for (const el of document.querySelectorAll('*')) {
        const cs = getComputedStyle(el);
        const m = cs.backgroundColor.match(/rgba?\\((\\d+)[,\\s]+(\\d+)[,\\s]+(\\d+)(?:[,\\s]+([\\d.]+))?\\)/);
        if (!m) continue;
        const a = m[4] === undefined ? 1 : parseFloat(m[4]);
        if (a < 0.2) continue;
        if (!isRed(+m[1], +m[2], +m[3])) continue;
        const r = el.getBoundingClientRect();
        const pct = (r.width * r.height) / (vw * vh) * 100;
        if (pct > maxPct) { maxPct = pct; worst = el.className || el.tagName; }
      }
      return { maxPct: Math.round(maxPct * 10) / 10, worst: String(worst).slice(0, 80) };
    })()""" % JS_RED)
    return {"red_max_area_pct": out["maxPct"], "red_worst": out["worst"]}


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


SCENARIOS = {
    "tab-focus": scenario_tab_focus,
    "open-delete": scenario_open_delete,
    "focus-input": scenario_focus_input,
    "red-area-scan": scenario_red_area_scan,
    "red-status-scan": scenario_red_status_scan,
    "status-colour-scan": scenario_status_colour_scan,
    "fixed-scan": scenario_fixed_scan,
}


# ------------------------------------------------------------------ main ----

def run_contract(pack_dir, target, out_dir, shots=True):
    contract = json.load(open(os.path.join(pack_dir, "verification.json")))
    os.makedirs(out_dir, exist_ok=True)
    if shots:
        os.makedirs(os.path.join(out_dir, "screens"), exist_ok=True)
    results = []
    needs_browser = any(c["mode"] in ("DOM", "COMPUTED_STYLE", "ACCESSIBILITY", "INTERACTION")
                        for c in contract["checks"])
    server, proc, page, browser = None, None, None, None
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
        from playwright.sync_api import sync_playwright as _sp
        pw = _sp().start()
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

            if mode == "REVIEW":
                r["status"] = "REVIEW_REQUIRED"
                results.append(r)
                continue

            outcomes = []
            evidence = {}

            if mode == "STATIC":
                for a in check.get("assertions", []):
                    st, detail = static_assert(a, target, check.get("files"))
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
                        evidence = fn(page, check.get("params", {}) or {})
                        r["evidence"] = evidence
                        for a in check.get("assertions", []):
                            ok = check_evidence_assertion(a, evidence)
                            outcomes.append(("PASS" if ok else "VIOLATION", json.dumps(evidence)[:200]) if ok is not None
                                            else ("UNVERIFIABLE", "evidence key missing"))
                            r["expected"].append(json.dumps(a)[:140])
                else:
                    sel = check.get("selector")
                    if mode == "DOM" and not sel:
                        # page-level DOM assertions
                        for a in check.get("assertions", []):
                            rel = a["relation"]
                            if rel == "absent" and a.get("selector"):
                                n = page.evaluate("document.querySelectorAll(%s).length" % json.dumps(a["selector"]))
                                outcomes.append(("PASS" if n == 0 else "VIOLATION", f"found {n}"))
                            elif rel == "page_text_no_match":
                                text = page.evaluate("document.body.innerText")
                                bad = "!" in text
                                emoji = [ch for ch in text if ord(ch) >= 0x1F000 or 0x2600 <= ord(ch) <= 0x27BF or 0xFE0F == ord(ch)]
                                if bad or emoji:
                                    outcomes.append(("VIOLATION", f"bang={bad} emoji={emoji[:5]}"))
                                else:
                                    outcomes.append(("PASS", "clean text"))
                            elif rel == "bil_pairs_ok":
                                out = page.evaluate("""(() => {
                                  const pairs = [...document.querySelectorAll('.bil')];
                                  let ok = 0; const bad = [];
                                  for (const p of pairs) {
                                    const en = p.querySelector('.en'), fr = p.querySelector('.fr');
                                    if (en && fr && en.textContent.trim() && fr.textContent.trim()) ok++;
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
                                n = page.evaluate("document.querySelectorAll(%s).length" % json.dumps(a["selector"]))
                                outcomes.append(("PASS" if n >= 1 else "VIOLATION", f"found {n}"))
                            elif rel == "no_css_url_images":
                                for f in a.get("files", ["app.css"]):
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
                        node = page.query_selector(sel) if sel else None
                        if node is None:
                            if check.get("missing") == "fail":
                                outcomes.append(("VIOLATION", f"selector '{sel}' not found"))
                            else:
                                outcomes.append(("UNVERIFIABLE", f"selector '{sel}' not found"))
                        else:
                            el_h = page.evaluate("(sel => { const e = document.querySelector(sel); return e ? e.getBoundingClientRect().height : 0; })", sel)
                            if mode == "DOM":
                                for a in check.get("assertions", []):
                                    rel = a["relation"]
                                    scope_sel = (sel + " " + a.get("selector", "")) if (sel and a.get("selector")) else a.get("selector", "")
                                    if rel == "text_len_min":
                                        tl = page.evaluate("(sel => { const e = document.querySelector(sel); return e ? e.textContent.trim().length : 0; })", sel)
                                        outcomes.append(("PASS" if tl >= a["value"] else "VIOLATION", f"text length {tl}"))
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
                                for a in check.get("assertions", []):
                                    prop = a["property"]
                                    val = page.evaluate(
                                        "(args => { const e = document.querySelector(args[0]); if (!e) return null; const cs = getComputedStyle(e); return cs[args[1]]; })",
                                        [sel, prop])
                                    ok = check_computed_assertion(a, val, el_h)
                                    if ok is None:
                                        outcomes.append(("UNVERIFIABLE", f"{prop}: {val}"))
                                    else:
                                        outcomes.append(("PASS" if ok else "VIOLATION", f"{prop}: {val}"))
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
           "by_mode": by_mode, "checks": results}
    with open(os.path.join(out_dir, "raw.json"), "w") as fh:
        json.dump(raw, fh, indent=1, ensure_ascii=False)

    lines = [f"# da_verify — {contract['authority']} on {raw['target']}",
             f"generated {raw['generated']}",
             f"TOTALS: {summary['total']} checks — PASS {summary['PASS']} · VIOLATION {summary['VIOLATION']} · "
             f"UNVERIFIABLE {summary['UNVERIFIABLE']} · REVIEW_REQUIRED {summary['REVIEW_REQUIRED']}", ""]
    for r in results:
        mark = {"PASS": "PASS ", "VIOLATION": "VIOL ", "UNVERIFIABLE": "UNV  ", "REVIEW_REQUIRED": "REVIEW"}[r["status"]]
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
