#!/usr/bin/env python3
"""Concept-site gate - the consumer verification loop, mechanically enforced.

Run after EVERY change to examples/designauthority-site (also wired into
tools/check.sh). Fails loudly on any of:
  1. lint            pack validator over the site: 0 errors / 0 warnings / score 100
  2. marks           every data-improv carries a reason + the standard title;
                     count matches the ledger's "N marked"
  3. gaps            ledger gap ids exist in the workspace store; count matches
  4. copy rules      zero em dashes in page + site css; the word "obey" absent
  5. foundations     tokens/base/patterns + fonts byte-identical to ~/triage-design-system
  6. recorded usage  every family the ledger claims "used as recorded" still
                     resolves (button, chip, status dot, table, version timeline)

Proposals in the workspace are informational (listed, not gated).
"""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = os.path.join(ROOT, "examples", "designauthority-site")
WS = os.path.join(ROOT, "workspaces", "designauthority-site")
TRIAGE = os.path.expanduser("~/triage-design-system")

fails = []
def ck(name, ok, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, ("  " + detail) if detail else ""))
    if not ok:
        fails.append(name)

def run(*args):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "da.py")] + list(args),
                       capture_output=True, text=True, cwd=ROOT)
    return (r.stdout or "") + (r.stderr or "")

# 1) lint
out = run("--pack", "packs/triage", "validate", SITE)
ck("lint 0 errors / 0 warnings / score 100",
   "errors=0" in out and "warnings=0" in out and "spec score=100" in out)

# 2) marks + 3) gaps vs the ledger
html = open(os.path.join(SITE, "index.html")).read()
marks = re.findall(r'data-improv="([^"]+)"', html)
titles = html.count('title="Improvised (no authority record; gap filed)"')
m = re.search(r"(\d+) marked . (\d+) gaps filed", html)
ck("every mark carries a reason + standard title", bool(marks) and len(marks) == titles,
   "%d marks / %d titles" % (len(marks), titles))
ck("ledger marked count matches page", bool(m) and int(m.group(1)) == len(marks),
   "ledger=%s page=%d" % (m.group(1) if m else "?", len(marks)))
store = [json.loads(l) for l in open(os.path.join(WS, ".design-authority", "gaps.jsonl")) if l.strip()]
ids = set(g["id"] for g in store)
led_sec = html[html.find('id="ledger"'):]
led_sec = led_sec[:led_sec.find("</section>")]
led = set(re.findall(r"gap/\d{8}-\d{6}-[0-9a-f]{6}", led_sec))  # ledger section only; the case-study gap id belongs to the Dominion build
ck("ledger gap ids all exist in store", led <= ids, "%d listed / %d in store" % (len(led), len(ids)))
ck("ledger gap count matches store", bool(m) and int(m.group(2)) == len(ids),
   "ledger=%s store=%d" % (m.group(2) if m else "?", len(ids)))

# 4) copy rules
cou = open(os.path.join(SITE, "assets", "css", "da-site.css")).read()
ck("zero em dashes (page + site css)", (html + cou).count("\u2014") == 0)
ck("the word 'obey' is absent", re.search(r"\bobey", html, re.I) is None)

# 5) foundations byte-identical
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
if os.path.isdir(TRIAGE):
    drift = []
    for a, b in [("assets/tokens/tokens.css", "tokens/tokens.css"),
                 ("assets/core/base.css", "core/base.css"),
                 ("assets/core/patterns.css", "core/patterns.css")]:
        if sha(os.path.join(SITE, a)) != sha(os.path.join(TRIAGE, b)):
            drift.append(a)
    fa, fb = os.path.join(SITE, "assets", "fonts"), os.path.join(TRIAGE, "fonts")
    if os.path.isdir(fa) and os.path.isdir(fb):
        fs = set(os.listdir(fa)) - set(os.listdir(fb))
        fd = [f for f in (set(os.listdir(fa)) & set(os.listdir(fb)))
              if os.path.isfile(os.path.join(fb, f)) and sha(os.path.join(fa, f)) != sha(os.path.join(fb, f))]
        if fs or fd:
            drift.append("fonts: extra %s / differs %s" % (sorted(fs), sorted(fd)))
    else:
        drift.append("fonts dir missing")
    ck("foundations byte-identical to Triage", not drift, "; ".join(drift))
else:
    print("SKIP foundations (source repo not present on this machine)")

# 6) recorded usage resolves
bad = [q for q in ["a button", "a chip", "a status dot", "a table", "a version timeline"]
       if "OUTCOME: UNDEFINED" in run("--pack", "packs/triage", "resolve", q)]
ck("recorded usage probes resolve (5/5)", not bad, ", ".join(bad) if bad else "all resolve")

props = os.path.join(WS, ".design-authority", "proposals")
if os.path.isdir(props):
    pj = sorted(f for f in os.listdir(props) if f.endswith(".json"))
    print("INFO proposals in workspace: %d (%s)" % (len(pj), ", ".join(pj)))

print()
if fails:
    print("concept-site gate: FAIL (%d)" % len(fails))
    sys.exit(1)
print("concept-site gate: OK")
