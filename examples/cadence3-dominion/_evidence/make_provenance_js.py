#!/usr/bin/env python3
"""Generate provenance.js for examples/cadence3-dominion — the click-to-
provenance registry for the lens (marks layer companion).

Sources (all inside this repo):
  - NOTES.md (the 42-row decision log + the gaps table)
  - packs/dominion/{artifacts,precedents,fallbacks,candidates}.json
  - .design-authority/gaps.jsonl
  - _evidence/resolves.jsonl

Output: examples/cadence3-dominion/provenance.js  (const PROV = {...};)
The lens reads PROV at click time, keyed by each marked node's data-el.
Re-run after the decision log or the pack changes.
"""
import json
import re
from pathlib import Path

EX = Path(__file__).resolve().parents[1]          # examples/cadence3-dominion
REPO = EX.parents[1]                              # repo root

notes = (EX / "NOTES.md").read_text(encoding="utf-8")


def strip_md(s):
    s = s.strip().replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


# ---- 1. the 42-row table ------------------------------------------------------
section = notes.split("## The 42-row decision log", 1)[1].split("## Gaps filed", 1)[0]

rows = {}
for line in section.splitlines():
    m = re.match(r"^\|\s*(\d+)\s*\|(.*)\|\s*$", line.strip())
    if not m:
        continue
    cells = [c.strip() for c in m.group(2).split("|")]
    assert len(cells) == 6, (m.group(1), len(cells))
    element, outc, res, prec, built, marked = cells
    n = int(m.group(1))

    outcome = strip_md(outc.split("\u2192")[-1]) if "\u2192" in outc else strip_md(outc)
    ids = re.findall(r"`([a-z-]+(?:/[a-z0-9-]+)?)`", res)
    resolution, closest = None, None
    if "closest" in res:
        closest = ids[-1] if ids else None
    else:
        resolution = ids[0] if ids else None

    prec_clean = re.sub(r"\([^)]*\)", "", prec)          # attached only
    prec_ids = []
    for tok in re.findall(r"`([^`]+)`", prec_clean):
        if re.match(r"^(declined-[a-z-]+|[a-z-]+-rejected)$", tok):
            prec_ids.append("precedent/" + tok)

    kind_m = re.search(r"data-(improvised|adapted|fallback)", marked)
    gap_m = re.search(r"\[(G\d+)\]", marked)
    cand_m = re.search(r"(candidate/[a-z0-9-]+)", " | ".join(cells))

    rows[str(n)] = {
        "n": n,
        "ask": strip_md(element),
        "outcome": outcome,
        "search_assisted": False,
        "resolution": resolution,
        "closest": closest,
        "precedents": prec_ids,
        "precedents_raw": strip_md(prec).rstrip("."),
        "built": strip_md(built),
        "kind": kind_m.group(1) if kind_m else None,
        "gap_key": gap_m.group(1) if gap_m else None,
        "candidate": cand_m.group(1) if cand_m else None,
        "gap": None,
    }

assert len(rows) == 42, "expected 42 rows, parsed %d" % len(rows)

# ---- 2. gaps -----------------------------------------------------------------
gaps = {}
for ln in (EX / ".design-authority" / "gaps.jsonl").read_text(encoding="utf-8").splitlines():
    if ln.strip():
        g = json.loads(ln)
        gaps[g["id"]] = g

gap_table = {}
gsec = notes.split("## Gaps filed", 1)[1].split("\n## ", 1)[0]
for line in gsec.splitlines():
    m = re.match(r"^\|\s*(G\d+)\s*\|\s*`(gap/[0-9-]+-[0-9a-f]+)`", line.strip())
    if m:
        gap_table[m.group(1)] = m.group(2)
assert len(gap_table) == 6, gap_table

for r in rows.values():
    key = r.pop("gap_key", None)
    if key:
        gid = gap_table[key]
        assert gid in gaps, gid
        r["gap"] = gid

# ---- 3. resolves alignment ---------------------------------------------------
rl = [json.loads(l) for l in (EX / "_evidence" / "resolves.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
assert len(rl) == 42


def _norm_ask(s):
    return s.lower().strip().replace("\u2019", "'").replace("\u2018", "'")


for i, d in enumerate(rl, 1):
    a, b = _norm_ask(d["problem"]), _norm_ask(rows[str(i)]["ask"])
    assert a == b, "row %d: resolve='%s' vs ask='%s'" % (i, a, b)
    rows[str(i)]["resolve_line"] = i

# ---- 4. pack records ----------------------------------------------------------
arts_all = json.loads((REPO / "packs" / "dominion" / "artifacts.json").read_text())["artifacts"]
arts_by_id = {a["id"]: a for a in arts_all}
prec_all = json.loads((REPO / "packs" / "dominion" / "precedents.json").read_text())
fall_all = json.loads((REPO / "packs" / "dominion" / "fallbacks.json").read_text())
cand_all = json.loads((REPO / "packs" / "dominion" / "candidates.json").read_text())

artifacts = {}
for r in rows.values():
    for aid in filter(None, [r["resolution"], r["closest"]]):
        if aid in arts_by_id and aid not in artifacts:
            a = arts_by_id[aid]
            summary = re.sub(r"\s+", " ", a.get("summary", ""))
            if len(summary) > 320:
                summary = summary[:317].rsplit(" ", 1)[0] + "\u2026"
            src = a.get("source", {})
            artifacts[aid] = {"id": a["id"], "title": a.get("title", ""), "summary": summary,
                              "source_path": src.get("path", ""), "compiled_from": a.get("compiled_from", [])}

precedents = {p["id"]: {"title": p["title"], "kind": p.get("kind"), "decision": p.get("decision"),
                        "grounds": p.get("grounds", ""), "reason": p.get("reason", ""),
                        "try": p.get("try", []), "citation": p.get("citation", "")}
              for p in prec_all["precedents"]}
precedents_note = prec_all.get("note", "")
fallbacks = {f["id"]: f for f in fall_all["fallbacks"]}
candidates = {c["id"]: c for c in cand_all["candidates"]}

# cross-checks
marked_rows = {str(r["n"]) for r in rows.values() if r["kind"]}
cand_rows = {str(r["n"]): r["candidate"] for r in rows.values() if r["candidate"]}
print("marked rows:", sorted(marked_rows, key=int))
print("candidate mentions:", cand_rows)
missing_prec = sorted({p for r in rows.values() for p in r["precedents"] if p not in precedents})
print("cited precedents not in pack:", missing_prec)
missing_cand = sorted({c for c in cand_rows.values() if c not in candidates})
print("cited candidates not in pack:", missing_cand)

meta = {
    "authority": "dominion", "pack_version": "0.2.0", "generated": "2026-10-08",
    "generated_by": "_evidence/make_provenance_js.py",
    "sources": [
        "NOTES.md \u00b7 the 42-row decision log",
        "packs/dominion/artifacts.json \u00b7 precedents.json \u00b7 fallbacks.json \u00b7 candidates.json",
        ".design-authority/gaps.jsonl",
        "_evidence/resolves.jsonl",
    ],
    "precedents_note": precedents_note,
}

prov = {"meta": meta, "rows": rows, "artifacts": artifacts,
        "precedents": precedents, "retired": {}, "fallbacks": fallbacks,
        "candidates": candidates, "gaps": gaps}

out = EX / "provenance.js"
out.write_text(
    "/* provenance.js \u2014 GENERATED, do not hand-edit. Regenerate: python3 _evidence/make_provenance_js.py\n"
    "   Decision records for the lens (click a dashed node \u2192 see the provenance). */\n"
    "const PROV = " + json.dumps(prov, ensure_ascii=False) + ";\n", encoding="utf-8")
print("wrote", out, "| rows:", len(rows))
