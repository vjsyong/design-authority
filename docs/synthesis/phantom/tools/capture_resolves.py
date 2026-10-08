#!/usr/bin/env python3
"""capture_resolves — resolve every phantom-audit element against packs/phantom,
record outcomes (resolves.jsonl), file the console's own gaps (workspace +
app copy), and dump the colour inventory for the verification contract."""
import json
import os
import re
import subprocess
import sys

REPO = "/home/xrim/design-authority"
DA = ["python3", os.path.join(REPO, "tools", "da.py"), "--pack", os.path.join(REPO, "packs", "phantom")]
EVID = os.path.join(REPO, "examples", "phantom-audit", "_evidence")
WS = os.path.join(REPO, "workspaces", "phantom")
os.makedirs(EVID, exist_ok=True)
os.makedirs(WS, exist_ok=True)

ASKS = [
    ("a type scale for headings and body", "canon"),
    ("a colour palette with accents", "canon"),
    ("a primary button", "canon"),
    ("an inline text field", "canon"),
    ("a dropdown select menu", "canon"),
    ("a consent checkbox", "canon"),
    ("a submit button row", "canon"),
    ("a data table", "canon"),
    ("a project gallery grid", "canon"),
    ("a pull quote", "canon"),
    ("a code block", "canon"),
    ("a bulleted list", "canon"),
    ("a full width image", "canon"),
    ("social icons row", "canon"),
    ("a site header with a logo", "canon"),
    ("the slide in menu", "canon"),
    ("a footer with contact info", "canon"),
    ("a page fade in animation", "canon"),
    ("a horizontal rule", "canon"),
    ("a stat row", "console"),
    ("a filter bar", "console"),
    ("a provenance side panel", "console"),
    ("status chips", "console"),
    ("a before and after code comparison", "console"),
    ("a carousel with prev next controls", "console"),
    ("a project detail page", "console"),
    ("an anchor navigation menu", "console"),
    ("a contrast check table", "console"),
    ("a toggle button for annotations", "console"),
    ("a gap ledger table", "console"),
]

out_path = os.path.join(EVID, "resolves.jsonl")
lines = []
counts = {}
with open(out_path, "w") as fh:
    for ask, zone in ASKS:
        r = subprocess.run(DA + ["resolve", ask, "--json"], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
        except Exception as exc:
            d = {"outcome": "ERROR", "problem": ask, "error": str(exc)[:80]}
        outcome = d.get("outcome", "?")
        counts[outcome] = counts.get(outcome, 0) + 1
        res = (d.get("resolution") or {})
        res_id = None
        if isinstance(res, dict):
            for k in ("artifact", "recipe", "fallback"):
                if res.get(k):
                    res_id = res[k].get("id")
                    break
        handling = {
            "RESOLVED": "built per the cited artifact (canon)",
            "COMPOSE": "composed from cited artifacts (canon)",
            "FALLBACK": "fallback constraints applied (marked)",
            "CONFLICT": "adapted to the cited artifact (marked)",
            "UNDEFINED": "improvised in character, marked, gap filed",
        }.get(outcome, "recorded")
        rec = {"ask": ask, "zone": zone, "outcome": outcome, "resolution_id": res_id,
               "candidates": [c.get("id") for c in (d.get("candidates") or [])],
               "precedents": [p.get("id") for p in (d.get("precedents") or [])],
               "handling": handling}
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        lines.append(rec)

print("resolve outcomes:", counts)

GAPS = [
    ("audit console kit — stat row, chips, filters, frames", "review-console", "console"),
    ("provenance side panel for records and evidence", "review-console", "console"),
    ("before/after code comparison view", "review-console", "console"),
    ("carousel composition — controlled, no autoplay", "portfolio", "motion"),
    ("project-detail composition for portfolio works", "portfolio", "layout"),
    ("mixed-script (CJK/EN) typography policy", "typography", "language"),
    ("current-section mark for menus", "navigation", "state"),
    ("contrast (AA) check table", "review-console", "a11y"),
    ("no-script rendering path for the review console", "review-console", "fallback"),
    ("criteria for promotion of review-surface kits", "governance", "process"),
]
for need, scope, dom in GAPS:
    ctx = json.dumps({"from": "phantom-audit", "scope": scope, "domain": dom})
    r = subprocess.run(DA + ["gap-add", "--need", need, "--context", ctx,
                             "--scope", scope, "--workspace", WS],
                       capture_output=True, text=True)
    print("gap:", (r.stdout or r.stderr).strip().splitlines()[-1][:110] if (r.stdout or r.stderr) else "?")

src = os.path.join(WS, ".design-authority", "gaps.jsonl")
if os.path.exists(src):
    with open(src) as fh:
        data = fh.read()
    open(os.path.join(EVID, "gaps.jsonl"), "w").write(data)

# colour inventory for the verification contract
for f in ("assets/css/main.css", "assets/css/console.css"):
    t = open(os.path.join(REPO, "examples", "phantom-audit", f)).read()
    toks = set(re.findall(r"#[0-9a-fA-F]{3,8}\b", t))
    print(f, "hex:", sorted(x.lower() for x in toks))
print("done")
