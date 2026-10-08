#!/usr/bin/env python3
"""Generate provenance.js for examples/cadence3-wink — the click-to-provenance registry.

Sources (all inside this repo):
  - NOTES.md (the 42-row decision log + v3.1 revision section)
  - packs/wink/{artifacts,precedents,fallbacks,candidates}.json
  - .design-authority/gaps.jsonl
  - _evidence/{resolves.jsonl,v31-revision.jsonl}
  - docs/synthesis/16-lenient-adjudication.md (+ data/lenient.json posture summary)

Output: examples/cadence3-wink/provenance.js  (const PROV = {...}; — valid JS object literal)
Re-run after the decision log or the pack changes; the app reads PROV at click time.
"""
import json
import re
from pathlib import Path

EX = Path(__file__).resolve().parents[1]          # examples/cadence3-wink
REPO = EX.parents[1]                              # repo root

notes = (EX / "NOTES.md").read_text(encoding="utf-8")

# ---- 1. the 42-row table ----------------------------------------------------
section = notes.split("## The 42-row decision log", 1)[1].split("GAP id shorthand", 1)[0]

def strip_md(s: str) -> str:
    s = s.replace("—", "—").strip()
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()

rows = {}
for line in section.splitlines():
    m = re.match(r"^\|\s*(\d+)\s*\|(.*)\|\s*$", line.strip())
    if not m:
        continue
    cells = [c.strip() for c in m.group(2).split("|")]
    # cells now: [element, outcome, resolution, precedents, built, marked]  (6)
    assert len(cells) == 6, (m.group(1), len(cells))
    n = int(m.group(1))
    element, outc, res, prec, built, marked = cells

    search_assisted = "search-assisted" in outc
    outcome = re.sub(r"^UNDEFINED\s*→\s*", "", outc) if search_assisted else outc
    outcome = strip_md(outcome.split("→")[-1]) if "→" in outcome else strip_md(outcome)

    ids = re.findall(r"`([a-z-]+(?:/[a-z0-9-]+)?)`", res)
    resolution, closest = None, None
    if "closest" in res:
        closest = ids[-1] if ids else None
    else:
        resolution = ids[0] if ids else None

    prec_ids = []
    for tok in re.findall(r"`([^`]+)`", prec):
        if re.match(r"^(declined-[a-z-]+|status-pill-rejected)$", tok):
            prec_ids.append("precedent/" + tok)

    kind_m = re.search(r"data-(improvised|adapted|fallback)", marked)
    gap_suffixes = re.findall(r"…([0-9a-f]{6})", marked)

    rows[str(n)] = {
        "n": n,
        "ask": strip_md(element),
        "outcome": outcome,
        "search_assisted": search_assisted,
        "resolution": resolution,
        "closest": closest,
        "precedents": prec_ids,
        "precedents_raw": strip_md(prec).rstrip("."),
        "built": strip_md(built),
        "kind": kind_m.group(1) if kind_m else None,
        "gap_suffixes": gap_suffixes,
    }

assert len(rows) == 42, f"expected 42 rows, parsed {len(rows)}"

# ---- 2. gaps ----------------------------------------------------------------
gaps = {}
for ln in (EX / ".design-authority" / "gaps.jsonl").read_text(encoding="utf-8").splitlines():
    if ln.strip():
        g = json.loads(ln)
        gaps[g["id"]] = g

for r in rows.values():
    r["gap"] = None
    for suf in r.pop("gap_suffixes"):
        hit = [gid for gid in gaps if gid.endswith("-" + suf)]
        assert len(hit) == 1, suf
        # sanity: gap's element_n should match, where recorded
        gn = gaps[hit[0]].get("context", {}).get("element_n")
        if gn is not None:
            assert gn == r["n"], (r["n"], gn)
        r["gap"] = hit[0]

# lenient re-classification: the combined avatars/glyphs decline was split —
# photo asks are still governed by the LIVE imagery precedent; add it ahead of
# the retired combined id so the panel shows the current authority first.
for r in rows.values():
    if "precedent/declined-photographic-avatars-glyphs" in r["precedents"]:
        r["precedents"] = ["precedent/declined-photographic-imagery"] + r["precedents"]

# ---- 3. resolves.jsonl alignment + line numbers -----------------------------
rl = [json.loads(l) for l in (EX / "_evidence" / "resolves.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
assert len(rl) == 42
for i, d in enumerate(rl, 1):
    a, b = d["problem"].lower().strip(), rows[str(i)]["ask"].lower().strip()
    assert a == b, f"row {i}: resolve='{a}' vs ask='{b}'"
    rows[str(i)]["resolve_line"] = i

# ---- 4. pack records --------------------------------------------------------
arts_all = json.loads((REPO / "packs" / "wink" / "artifacts.json").read_text())["artifacts"]
arts_by_id = {a["id"]: a for a in arts_all}
prec_all = json.loads((REPO / "packs" / "wink" / "precedents.json").read_text())
fall_all = json.loads((REPO / "packs" / "wink" / "fallbacks.json").read_text())
cand_all = json.loads((REPO / "packs" / "wink" / "candidates.json").read_text())

artifacts = {}
for r in rows.values():
    for aid in filter(None, [r["resolution"], r["closest"]]):
        if aid in arts_by_id and aid not in artifacts:
            a = arts_by_id[aid]
            summary = re.sub(r"\s+", " ", a.get("summary", ""))
            if len(summary) > 320:
                summary = summary[:317].rsplit(" ", 1)[0] + "…"
            src = a.get("source", {})
            artifacts[aid] = {
                "id": a["id"],
                "title": a.get("title", ""),
                "summary": summary,
                "source_path": src.get("path", ""),
                "compiled_from": a.get("compiled_from", []),
            }

precedents = {p["id"]: {
    "title": p["title"], "kind": p.get("kind"), "decision": p.get("decision"),
    "grounds": p.get("grounds", ""), "reason": p.get("reason", ""),
    "try": p.get("try", []), "citation": p.get("citation", ""),
} for p in prec_all["precedents"]}
precedents_note = prec_all.get("note", "")

fallbacks = {f["id"]: f for f in fall_all["fallbacks"]}
candidates = {c["id"]: c for c in cand_all["candidates"]}

# retired precedents (lenient re-classification, docs/synthesis/16-lenient-adjudication.md)
retired = {
    "precedent/declined-chart-treatments": {
        "title": "Chart treatments (retired)",
        "now": "deferred to undefined",
        "note": "Blanket decline retired 2026-10-07: chart treatments defer to undefined — any composed treatment stays a marked improvisation. The minimal data blocks built here remain the sanctioned compose.",
    },
    "precedent/declined-photographic-avatars-glyphs": {
        "title": "Photographic avatars & icon glyphs (superseded)",
        "now": "split — imagery kept, glyphs deferred to undefined",
        "note": "The imagery part survives as precedent/declined-photographic-imagery (asset policy); the glyph/icon-set part was retired — icon asks defer to undefined (monograms remain the sanctioned route).",
    },
    "precedent/declined-native-form-controls": {
        "title": "Native form controls (retired)",
        "now": "deferred to undefined",
        "note": "Retired 2026-10-07: native controls defer to undefined; fallback/platform-controls still answers the need. Field-level styling only — no new control language invented.",
    },
    "precedent/declined-pager-and-drag": {
        "title": "Pager & drag reorder (re-classified)",
        "now": "pager → candidate; drag deferred",
        "note": "Pager promoted to candidate/pager-composition (outline pill + readout); drag-to-reorder deferred to undefined — the build uses explicit Move actions anyway.",
    },
    "precedent/declined-csv-export-affordance": {
        "title": "CSV export affordance (retired)",
        "now": "deferred to undefined",
        "note": "Retired 2026-10-07: export defers to undefined; the action-pill affordance + app-utility file flow remain the marked route.",
    },
    "precedent/declined-dark-mode": {
        "title": "Dark mode (retired)",
        "now": "deferred to undefined",
        "note": "Retired 2026-10-07: dark mode defers to undefined; fallback/light-only still answers the surface. Build stays light-only, marked.",
    },
    "precedent/declined-neutral-tag-variant": {
        "title": "Neutral tag variant (retired)",
        "now": "deferred to undefined",
        "note": "Retired 2026-10-07: the neutral tag defers to undefined; the plain text pill (parsnip/ink) remains the marked composition. At resolve it never attached — the 3-char token rule — and was reached via the queries “neutral tag”/“chip” instead.",
    },
}

# ---- 5. v3.1 + fallback-family entries ---------------------------------------
v31 = json.loads((EX / "_evidence" / "v31-revision.jsonl").read_text(encoding="utf-8").splitlines()[0])
rows["v31t"] = {
    "n": "v3.1",
    "ask": "row log control — a check control to log a ritual",
    "outcome": "UNDEFINED",
    "outcome_note": "boundary-exempt — an ordinary marked improvisation",
    "search_assisted": False,
    "resolution": None,
    "closest": None,
    "precedents": ["precedent/declined-photographic-imagery"],
    "precedent_verdicts": {"precedent/declined-photographic-imagery": "outside"},
    "precedents_raw": "precedent-check verdict: outside — explicitly not governed (boundary: check control · log control · log a ritual)",
    "built": "round 28px check control — 1px #231E15 ink ring on white; #FFE01B yellow fill + ink check (#241C15) when logged; click toggles log/unlog; no motion",
    "kind": "improvised",
    "gap": None,
}
rows["fb"] = {
    "n": "—",
    "ask": "platform fallbacks — native controls where the pack defines none",
    "outcome": "FALLBACK",
    "search_assisted": False,
    "resolution": "fallback/platform-controls",
    "closest": None,
    "precedents": ["precedent/declined-native-form-controls"],
    "precedents_raw": "retired — native controls defer to undefined; the fallback still answers",
    "built": "the platform's native element in the wink field language (radius 8, warm ink) — sliders, checkboxes, radios, pickers; the wizard step-1 checklist is one instance",
    "kind": "fallback",
    "gap": None,
}

# row 32 — candidate alignment (v3.1)
rows["32"]["candidate"] = "candidate/pager-composition"

meta = {
    "authority": "wink",
    "pack_version": "0.2.0",
    "generated": "2026-10-08",
    "generated_by": "_evidence/make_provenance_js.py",
    "sources": [
        "NOTES.md · the 42-row decision log",
        "packs/wink/artifacts.json · precedents.json · fallbacks.json · candidates.json",
        ".design-authority/gaps.jsonl",
        "_evidence/resolves.jsonl · v31-revision.jsonl",
        "docs/synthesis/16-lenient-adjudication.md (lenient re-classification, 2026-10-07)",
    ],
    "lenient_note": "Lenient doctrine (2026-10-07): evidence-poor declines defer to UNDEFINED or become candidates; declines are reserved for grounded policy. Wink: photographic imagery kept; pager → candidate; charts, glyphs, neutral tag, native controls, csv, dark mode deferred.",
    "precedents_note": precedents_note,
}

prov = {
    "meta": meta,
    "rows": rows,
    "artifacts": artifacts,
    "precedents": precedents,
    "retired": retired,
    "fallbacks": fallbacks,
    "candidates": candidates,
    "gaps": gaps,
}

out = EX / "provenance.js"
payload = json.dumps(prov, ensure_ascii=False, separators=(",", ":"))
out.write_text(
    "/* provenance.js — GENERATED, do not hand-edit. Regenerate: python3 _evidence/make_provenance_js.py\n"
    "   Decision records for the marks layer (click a dashed node → see the provenance). */\n"
    "const PROV = " + payload + ";\n",
    encoding="utf-8",
)
print(f"wrote {out} ({out.stat().st_size} bytes)")
print("rows:", len(rows), "| artifacts:", len(artifacts), "| precedents:", len(precedents),
      "| retired:", len(retired), "| fallbacks:", len(fallbacks), "| candidates:", len(candidates), "| gaps:", len(gaps))
