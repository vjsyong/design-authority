#!/usr/bin/env python3
"""Render a source's decisions.json into Gate-2 review artifacts:

  <src>/02-semantic-review.md   — grouped record with outcome slots (fill at Gate 2)
  <src>/review.html             — self-contained, neutrally-styled review page

The JSON is the single source of truth (machine-heavy commitment; the same JSON
feeds the pack compiler after review). Stdlib only.

Usage: python3 render_decisions.py docs/synthesis/wink/decisions.json
"""
import argparse
import html
import json
import os
from datetime import date

SETTLED = "settled"
JUDGMENT = "judgment"
OPEN = "open"


def level(d):
    return {"none": SETTLED, "confirm": JUDGMENT, "open": OPEN}.get(d.get("review", "confirm"), JUDGMENT)


def md_for(src, data):
    lines = []
    dec = data["decisions"]
    n = {k: sum(1 for d in dec if level(d) == k) for k in (SETTLED, JUDGMENT, OPEN)}
    lines.append(f"# {src} · Semantic review (Gate 2)\n")
    lines.append(f"Generated {date.today().isoformat()} from `decisions.json` — "
                 f"**{len(dec)} decisions**: {n[SETTLED]} settled · {n[JUDGMENT]} needing judgment · {n[OPEN]} open.\n")
    lines.append("Legend — status: OBSERVED / INFERRED / AUTHORED / UNDEFINED. "
                 "Review outcome (fill at Gate 2): ACCEPT / MODIFY / REJECT / LEAVE UNDEFINED.\n")
    for grp, title in ((SETTLED, "Settled (high-confidence — shown for context, no action needed)"),
                       (JUDGMENT, "Needing judgment (authored or low-confidence)"),
                       (OPEN, "Open (genuinely undefined — may remain so)")):
        rows = [d for d in dec if level(d) == grp]
        lines.append(f"\n## {title}\n")
        if not rows:
            lines.append("_None._")
            continue
        for d in rows:
            lines.append(f"### {d['id']} · {d['area']} · {d['status']} · confidence: {d['confidence']}")
            lines.append(f"**Decision:** {d['decision']}\n")
            lines.append(f"**Evidence:** {d['evidence']}\n")
            lines.append(f"**Reasoning:** {d['reasoning']}\n")
            lines.append(f"**Alternatives:** {d['alternatives']}\n")
            if grp != SETTLED:
                lines.append("**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED\n")
    return "\n".join(lines) + "\n"


def esc(s):
    return html.escape(str(s))


def html_for(src, data):
    dec = data["decisions"]
    n = {k: sum(1 for d in dec if level(d) == k) for k in (SETTLED, JUDGMENT, OPEN)}
    cards = []
    for grp, title, hint in ((JUDGMENT, "Needing judgment", "ACCEPT · MODIFY · REJECT · LEAVE UNDEFINED"),
                             (SETTLED, "Settled", "No action needed — shown for context"),
                             (OPEN, "Open", "May remain undefined")):
        rows = [d for d in dec if level(d) == grp]
        if not rows:
            continue
        cards.append(f"<h2>{esc(title)} <span class='count'>{len(rows)}</span></h2>")
        cards.append(f"<p class='hint'>{esc(hint)}</p>")
        for d in rows:
            cards.append(f"""
<article class="card {grp}">
  <header><span class="id">{esc(d['id'])}</span><span class="chip">{esc(d['area'])}</span>
    <span class="chip st">{esc(d['status'])}</span><span class="chip conf">{esc(d['confidence'])}</span></header>
  <p class="decision">{esc(d['decision'])}</p>
  <dl><dt>Evidence</dt><dd>{esc(d['evidence'])}</dd>
      <dt>Reasoning</dt><dd>{esc(d['reasoning'])}</dd>
      <dt>Alternatives</dt><dd>{esc(d['alternatives'])}</dd></dl>
  {"<p class='outcome'>Review: ACCEPT · MODIFY · REJECT · LEAVE UNDEFINED</p>" if grp != SETTLED else ""}
</article>""")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{esc(src)} — semantic review (Gate 2)</title>
<style>
 :root {{ --ink:#141414; --mut:#5a5a5a; --line:#dcdcdc; --bg:#ffffff; --soft:#f6f6f6; }}
 * {{ box-sizing:border-box; }}
 body {{ font:15px/1.5 system-ui,-apple-system,'Segoe UI',sans-serif; color:var(--ink); background:var(--bg);
        max-width:860px; margin:0 auto; padding:40px 24px 80px; }}
 h1 {{ font-size:26px; font-weight:650; margin:0 0 6px; }}
 .sub {{ color:var(--mut); margin:0 0 26px; }}
 h2 {{ font-size:18px; margin:38px 0 4px; border-top:2px solid var(--ink); padding-top:14px; }}
 .count {{ color:var(--mut); font-weight:400; }}
 .hint {{ color:var(--mut); font-size:13px; margin:0 0 14px; }}
 .card {{ border:1px solid var(--line); border-radius:6px; padding:14px 16px; margin:0 0 12px; background:#fff; }}
 .card.judgment {{ border-left:4px solid var(--ink); }}
 .card header {{ margin-bottom:8px; }}
 .id {{ font-weight:700; margin-right:8px; }}
 .chip {{ display:inline-block; font-size:11.5px; background:var(--soft); border-radius:4px; padding:2px 7px; margin-right:6px; color:var(--mut); }}
 .chip.st {{ color:var(--ink); }}
 .decision {{ margin:0 0 8px; }}
 dl {{ margin:0; }} dt {{ font-size:11.5px; text-transform:uppercase; letter-spacing:.05em; color:var(--mut); margin-top:6px; }}
 dd {{ margin:2px 0 0; }}
 .outcome {{ margin:10px 0 0; font-size:12.5px; color:var(--mut); border-top:1px dashed var(--line); padding-top:8px; }}
 footer {{ margin-top:44px; color:var(--mut); font-size:12.5px; }}
</style></head><body>
<h1>{esc(src)} — semantic review</h1>
<p class="sub">Authority Synthesis · Gate 2 · {date.today().isoformat()} ·
 {len(dec)} decisions: {n[JUDGMENT]} needing judgment · {n[SETTLED]} settled · {n[OPEN]} open.<br>
 Reply in chat with ACCEPT / MODIFY / REJECT / LEAVE UNDEFINED per item (by ID). No forms to fill.</p>
{''.join(cards)}
<footer>Generated from decisions.json (single source of truth). Status tags: OBSERVED · INFERRED · AUTHORED · UNDEFINED.</footer>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    args = ap.parse_args()
    data = json.load(open(args.file))
    src = data["source"]
    base = os.path.dirname(args.file)
    with open(os.path.join(base, "02-semantic-review.md"), "w") as fh:
        fh.write(md_for(src, data))
    with open(os.path.join(base, "review.html"), "w") as fh:
        fh.write(html_for(src, data))
    print(f"rendered {src}: 02-semantic-review.md + review.html")


if __name__ == "__main__":
    main()
