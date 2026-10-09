#!/usr/bin/env python3
"""x05_score.py — objective scoring per the frozen method.

Frozen spec: docs/experiments/seed-evolution/analysis/objective-scoring-spec.md
(committed a763410 BEFORE this tool was run).

Layer 1: role fidelity of new/changed elements (diff ∩ ROLE_HOOKS) vs the
seed exemplars, §7 dimensions, 2/1/0 per decision point.
Layer 2: cross-component consistency of added visible components vs the
seed vocabulary (styles.css tokens + f3 observations + exemplar palettes),
plus a pattern-reuse observation log.

Deterministic; reads only the runner-written extraction bundles, the seed
stylesheet, and the seed exemplars. Writes objective-scores.{json,md}.

Usage: python3 x05_score.py [--x05 /home/xrim/x05] [--out DIR]
"""
import argparse
import hashlib
import json
import os
import re
import statistics
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from x05_census import parse_color, delta_e2000, radius_class, font_class  # noqa: E402
from x05_common import read_json  # noqa: E402

X05 = os.environ.get("X05_ROOT", "/home/xrim/x05")
STATES = ["empty", "populated", "filtered", "filtered-none", "invalid", "confirm",
          "confirm-bulk", "post-delete", "analytics", "palette", "wizard-1", "wizard-2"]
CHAINS = ("a", "b", "c")
EXEMPLAR_ROLES = ("primary-action", "destructive", "empty-state",
                  "form-validation", "tags-status", "surfaces")

# Layer-1 decision points per the frozen enumeration (element, role).
L1_POINTS = {
    (1,): [("filter-empty", "empty-state")],
    (2,): [("tag-filter", "tags-status"), ("bookmark-card", "surfaces")],
    (3,): [("command-palette", "surfaces")],
    (4,): [("import-submit", "primary-action"), ("import-wizard", "surfaces")],
}
L1_EXTRA_B = {(4,): [("command-palette", "surfaces")]}  # h4b re-modified palette


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def border_class_fixed(styles):
    """Frozen border categories with the documented transparency correction:
    a fully transparent border renders as `none` (mirrors the cen classifier's
    own 'none' judgments for .btn borders)."""
    sh = (styles or {}).get("shadow") or "none"
    bt = (styles or {}).get("borderTop") or "0px none"
    if sh and sh not in ("none", ""):
        return "shadow"
    m = re.match(r"([\d.]+)px", bt)
    w = float(m.group(1)) if m else 0.0
    if w == 0:
        return "none"
    cm = re.search(r"rgba?\(([^)]+)\)", bt)
    if cm:
        parts = [p.strip() for p in cm.group(1).split(",")]
        try:
            if len(parts) > 3 and float(parts[3]) == 0:
                return "none"
        except ValueError:
            pass
    if "transparent" in bt:
        return "none"
    return "hairline" if w <= 1.5 else "strong"


def font_class2(text):
    """Family-class extraction for composite CSS font strings.

    Correction #2 (spec limits): the frozen helper took the raw composite
    ('stack | size | weight | line-height') and its serif heuristic mis-read
    'sans-serif' stacks as serif. Compare only the family portion; treat
    'sans-serif' as sans."""
    fam = ((text or "").split("|")[0]).lower()
    if not fam:
        return None
    if "mono" in fam:
        return "mono"
    stripped = fam.replace("sans-serif", "").replace("sans", "")
    serif_names = ("serif", "georgia", "times", "garamond", "playfair", "fraunces",
                   "gelasio", "charter", "cambria")
    if any(n in stripped for n in serif_names):
        return "serif"
    return "sans"


def border_color(styles):
    bt = (styles or {}).get("borderTop") or ""
    m = re.search(r"rgba?\(([^)]+)\)", bt)
    if not m:
        return None
    parts = [p.strip() for p in m.group(1).split(",")]
    return parse_color("rgb(" + ",".join(parts[:3]) + ")")


def hex_rgb(text):
    t = (text or "").strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", t)
    if not m:
        return None
    h = m.group(1)
    return (float(int(h[0:2], 16)), float(int(h[2:4], 16)), float(int(h[4:6], 16)))


def is_structural(styles, radius_cls):
    bg = parse_color((styles or {}).get("bg"))
    bc = border_class_fixed(styles)
    sh = (styles or {}).get("shadow") or "none"
    r = radius_cls
    return (bg is None) and (bc == "none") and (r in (None, 0, 0.0)) and (sh in ("none", ""))


def pick_entry(entries, key="measured"):
    """Max area; ties -> earliest capture-state order."""
    best, best_area, best_idx = None, -1, 10**9
    for e in entries:
        m = e.get(key) or {}
        r = (m.get("rect") or {})
        a = (r.get("w") or 0) * (r.get("h") or 0)
        sidx = STATES.index(e["state"]) if e.get("state") in STATES else 10**6
        if a > best_area or (a == best_area and sidx < best_idx):
            best, best_area, best_idx = e, a, sidx
    return best


def exemplar_dims(sig):
    pal = sig.get("palette_bg")
    pal = parse_color(pal) if isinstance(pal, str) else None
    r = sig.get("radius")
    if r == "pill":
        rcls = "pill"
    else:
        rcls = radius_class(r) if isinstance(r, str) else None
    return {"bg": pal, "radius": rcls, "font": sig.get("font_class"), "border": sig.get("border")}


def l1_score_decision(entry, ex):
    st = (entry.get("measured") or {}).get("styles") or {}
    rcls = radius_class(st.get("radius"))
    if is_structural(st, rcls):
        return None, "not-measurable (structurally unstyled)"
    dims = []
    # palette-bg
    ib = parse_color(st.get("bg"))
    if ib is None and ex["bg"] is None:
        dims.append(("palette", True))
    elif (ib is None) != (ex["bg"] is None):
        dims.append(("palette", False))
    else:
        dims.append(("palette", delta_e2000(ib, ex["bg"]) <= 5))
    # radius
    if rcls == "pill" or ex["radius"] == "pill":
        dims.append(("radius", rcls == ex["radius"]))
    elif rcls is None or ex["radius"] is None:
        dims.append(("radius", False))
    else:
        dims.append(("radius", abs(rcls - ex["radius"]) <= 2))
    # typography
    fc = font_class2(st.get("font"))
    dims.append(("typography", fc == ex["font"]))
    # border & treatment
    dims.append(("border", border_class_fixed(st) == ex["border"]))
    passed = sum(1 for _, ok in dims if ok)
    score = 2 if passed == 4 else (1 if passed >= 2 else 0)
    return score, dims


def build_vocab(x05):
    tokens, radii, fonts, colors, classes = set(), set(), set(), set(), set()
    css = open(os.path.join(x05, "run", "f3", "ws", "styles.css"), encoding="utf-8").read()
    m = re.search(r":root\s*\{(.*?)\}", css, re.S)
    if m:
        for name, val in re.findall(r"--([\w-]+)\s*:\s*([^;]+);", m.group(1)):
            v = val.strip()
            c = hex_rgb(v)
            if c:
                colors.add(c)
            if name == "radius":
                rr = radius_class(v)
                if rr is not None:
                    radii.add(rr)
    for sel in re.findall(r"\.([a-zA-Z][\w-]*)", css):
        classes.add(sel)
    inv = read_json(os.path.join(x05, "run", "f3", "extraction", "inventory.json"), {}) or {}
    for sname, s in (inv.get("states") or {}).items():
        for tid, els in (s.get("testids") or {}).items():
            for e in els or []:
                st = e.get("styles") or {}
                for k in ("bg", "color"):
                    c = parse_color(st.get(k))
                    if c:
                        colors.add(c)
                bc = border_color(st)
                if bc:
                    colors.add(bc)
                rr = radius_class(st.get("radius"))
                if rr is not None:
                    radii.add(rr)
                fc = font_class(st.get("font"))
                if fc:
                    fonts.add(fc)
                for tok in (e.get("classes") or "").split():
                    classes.add(tok)
    ex = read_json(os.path.join(x05, "run", "cen", "extraction", "exemplars.json"), {}) or {}
    for rn, sig in (ex.get("exemplars") or {}).items():
        for k in ("palette_bg", "palette_fg"):
            c = parse_color(sig.get(k)) if isinstance(sig.get(k), str) else None
            if c:
                colors.add(c)
        rr = sig.get("radius")
        if rr == "pill":
            radii.add("pill")
        else:
            rr2 = radius_class(rr) if isinstance(rr, str) else None
            if rr2 is not None:
                radii.add(rr2)
    return {"colors": colors, "radii": radii, "fonts": fonts or {"sans"}, "classes": classes}


def nearest_de(c, colors):
    return min(delta_e2000(c, v) for v in colors) if colors else 10**6


def l2_score_component(el, vocab):
    st = el.get("styles") or {}
    rcls = radius_class(st.get("radius"))
    if is_structural(st, rcls):
        return None, "not-measurable (structurally unstyled)"
    dims = []
    ib = parse_color(st.get("bg"))
    dims.append(("palette", True if ib is None else nearest_de(ib, vocab["colors"]) <= 5))
    fc = font_class2(st.get("font"))
    dims.append(("typography", fc in vocab["fonts"]))
    if rcls == "pill":
        dims.append(("radius", "pill" in vocab["radii"]))
    elif rcls is None:
        dims.append(("radius", False))
    else:
        dims.append(("radius", any(abs(rcls - v) <= 2 for v in vocab["radii"] if isinstance(v, (int, float)))))
    bc = border_class_fixed(st)
    if bc == "none":
        dims.append(("border", True))
    else:
        c = border_color(st)
        dims.append(("border", c is not None and nearest_de(c, vocab["colors"]) <= 5))
    passed = sum(1 for _, ok in dims if ok)
    score = 2 if passed == 4 else (1 if passed >= 2 else 0)
    return score, dims


def reuse(el, vocab):
    toks = set((el.get("classes") or "").split())
    return bool(toks & vocab["classes"])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--x05", default=X05)
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(HERE), "analysis"))
    args = ap.parse_args(argv)
    x05 = args.x05

    vocab = build_vocab(x05)
    seed_ex = read_json(os.path.join(x05, "run", "cen", "extraction", "exemplars.json"), {}) or {}
    exdims = {r: exemplar_dims(seed_ex["exemplars"][r]["dimension_signature"])
              for r in EXEMPLAR_ROLES}

    out = {
        "version": 1,
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "spec": "analysis/objective-scoring-spec.md (commit a763410)",
        "inputs_sha256": {
            "schedule.json": sha256_file(os.path.join(x05, "schedule.json")),
            "f3/ws/styles.css": sha256_file(os.path.join(x05, "run", "f3", "ws", "styles.css")),
            "cen/exemplars.json": sha256_file(os.path.join(x05, "run", "cen", "extraction", "exemplars.json")),
        },
        "vocab_sizes": {"colors": len(vocab["colors"]), "radii": sorted(vocab["radii"], key=str),
                        "fonts": sorted(vocab["fonts"]), "classes": len(vocab["classes"])},
        "layer1": {}, "layer2": {}, "gates": {},
    }

    # ---------------- Layer 1
    l1 = {}
    for c in CHAINS:
        l1[c] = {}
        for k in (1, 2, 3, 4):
            sid = f"h{k}{c}"
            roles = read_json(os.path.join(x05, "run", sid, "extraction", "roles.json"), {}) or {}
            points = list(L1_POINTS[(k,)]) + (L1_EXTRA_B.get((k,), []) if c == "b" else [])
            rows, excluded = [], []
            for tid, role in points:
                block = (roles.get("roles") or {}).get(role) or {}
                entries = [e for e in block.get("entries", []) if e["testid"] == tid]
                if not entries:
                    excluded.append({"element": tid, "role": role, "why": "no entries"})
                    continue
                picked = pick_entry(entries)
                areas = [(e.get("measured") or {}).get("rect") or {} for e in entries]
                if all(((r.get("w") or 0) * (r.get("h") or 0)) == 0 for r in areas):
                    excluded.append({"element": tid, "role": role,
                                     "why": "unrendered in all captured states"})
                    continue
                score, detail = l1_score_decision(picked, exdims[role])
                if score is None:
                    excluded.append({"element": tid, "role": role, "state": picked["state"],
                                     "why": detail})
                    continue
                rows.append({"element": tid, "role": role, "state": picked["state"],
                             "dimensions": detail, "score": score})
            n = len(rows)
            fid = (sum(r["score"] for r in rows) / (2 * n)) if n else None
            l1[c][k] = {"rows": rows, "excluded": excluded, "n": n, "sum": sum(r["score"] for r in rows),
                        "fidelity": fid}
    out["layer1"] = l1

    # D1 / D2
    def deltas(x, y):
        d = {}
        for k in (1, 2, 3, 4):
            fx, fy = l1[x][k]["fidelity"], l1[y][k]["fidelity"]
            d[k] = None if (fx is None or fy is None) else round(fx - fy, 4)
        return d
    cb, ba = deltas("c", "b"), deltas("b", "a")
    out["gates"]["deltas_C_minus_B"] = cb
    out["gates"]["deltas_B_minus_A"] = ba

    def gate(dd):
        vals = [(k, v) for k, v in dd.items() if v is not None]
        exceeds = sum(1 for _, v in vals if v > 0)
        if not vals:
            return {"exceeds": 0, "median": None, "threshold": None, "pass": False}
        med = statistics.median(v for _, v in vals)
        med_ks = [k for k, v in vals if v == med]
        n_star = None
        for k in med_ks:
            counts = [l1[c][k]["n"] for c in CHAINS if l1[c][k]["n"]]
            if counts:
                n_star = min(counts) if n_star is None else min(n_star, min(counts))
        thr = (1.0 / n_star) if n_star else None
        return {"exceeds": exceeds, "median": med, "threshold": thr,
                "pass": bool(exceeds >= 3 and thr is not None and med >= thr)}
    out["gates"]["D1"] = gate(cb)
    out["gates"]["D2"] = gate(ba)

    # ---------------- Layer 2
    l2 = {}
    for c in CHAINS:
        l2[c] = {}
        for k in (1, 2, 3, 4):
            sid = f"h{k}{c}"
            diff = read_json(os.path.join(x05, "run", sid, "extraction", "diff.json"), {}) or {}
            inv = read_json(os.path.join(x05, "run", sid, "extraction", "inventory.json"), {}) or {}
            l1_tids = {tid for tid, _ in (L1_POINTS.get((k,), []) + (L1_EXTRA_B.get((k,), []) if c == "b" else []))}
            added = [t for t in (diff.get("element", {}).get("added") or []) if t not in l1_tids]
            rows, excluded, reuse_hits = [], [], 0
            for tid in added:
                cands = []
                for sname, s in (inv.get("states") or {}).items():
                    for e in (s.get("testids") or {}).get(tid, []) or []:
                        cands.append((sname, e))
                vis = []
                for sname, e in cands:
                    r = e.get("rect") or {}
                    a = (r.get("w") or 0) * (r.get("h") or 0)
                    if a > 0:
                        vis.append((sname, e, a))
                if not vis:
                    excluded.append({"element": tid, "why": "unrendered in all captured states"})
                    continue
                vis.sort(key=lambda t: (-t[2], STATES.index(t[0]) if t[0] in STATES else 10**6))
                sname, el, _ = vis[0]
                score, dims = l2_score_component(el, vocab)
                if score is None:
                    excluded.append({"element": tid, "state": sname, "why": dims})
                    continue
                if reuse(el, vocab):
                    reuse_hits += 1
                rows.append({"element": tid, "state": sname, "dimensions": dims, "score": score})
            n = len(rows)
            cons = (sum(r["score"] for r in rows) / (2 * n)) if n else None
            l2[c][k] = {"rows": rows, "excluded": excluded, "n": n,
                        "sum": sum(r["score"] for r in rows), "consistency": cons,
                        "reuse_share": (reuse_hits / n) if n else None}
    out["layer2"] = l2

    # D3
    def l2_mean(c, ks):
        vals = [l2[c][k]["consistency"] for k in ks if l2[c][k]["consistency"] is not None]
        return round(statistics.mean(vals), 4) if vals else None
    means = {c: l2_mean(c, (2, 3, 4)) for c in CHAINS}
    ge = sum(1 for k in (2, 3, 4)
             if l2["c"][k]["consistency"] is not None and l2["b"][k]["consistency"] is not None
             and l2["c"][k]["consistency"] >= l2["b"][k]["consistency"])
    out["gates"]["D3"] = {"means_H2_H4": means,
                          "favors_C": bool(means["c"] is not None and
                                           all(means["c"] > means[x] for x in ("a", "b") if means[x] is not None)
                                           and ge >= 2)}
    out["gates"]["D3"]["C_ge_B_handoffs"] = ge

    # ---------------- outputs
    os.makedirs(args.out, exist_ok=True)
    jpath = os.path.join(args.out, "objective-scores.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True, default=str)

    lines = ["# x05 · Objective scores (Layer 1 + Layer 2)", "",
             f"Generated {out['generated']} · spec commit a763410 · inputs: schedule `{out['inputs_sha256']['schedule.json'][:12]}…`, styles.css `{out['inputs_sha256']['f3/ws/styles.css'][:12]}…`, exemplars `{out['inputs_sha256']['cen/exemplars.json'][:12]}…`", ""]
    lines += ["## Layer 1 — role fidelity", "", "| chain | H1 | H2 | H3 | H4 |", "|---|---|---|---|---|"]
    for c in CHAINS:
        vals = []
        for k in (1, 2, 3, 4):
            f_ = l1[c][k]["fidelity"]
            vals.append("n/a" if f_ is None else f"{f_:.3f} ({l1[c][k]['n']})")
        lines.append(f"| {c.upper()} | " + " | ".join(vals) + " |")
    lines += ["", "Per-point detail (score / dims shown compactly):"]
    for c in CHAINS:
        for k in (1, 2, 3, 4):
            for r in l1[c][k]["rows"]:
                dims = " ".join(("+" if ok else "-") + nm for nm, ok in r["dimensions"])
                lines.append(f"- {c.upper()} H{k}: {r['element']} ({r['role']}, {r['state']}) → {r['score']} [{dims}]")
            for r in l1[c][k]["excluded"]:
                lines.append(f"- {c.upper()} H{k}: {r['element']} → EXCLUDED ({r.get('why')})")
    lines += ["", "## Layer 2 — cross-component consistency", "",
              "| chain | H1 | H2 | H3 | H4 |", "|---|---|---|---|---|"]
    for c in CHAINS:
        vals = []
        for k in (1, 2, 3, 4):
            v = l2[c][k]["consistency"]
            vals.append("n/a" if v is None else f"{v:.3f} ({l2[c][k]['n']})")
        lines.append(f"| {c.upper()} | " + " | ".join(vals) + " |")
    lines += ["", "| chain | reuse H1 | reuse H2 | reuse H3 | reuse H4 |", "|---|---|---|---|---|"]
    for c in CHAINS:
        vals = []
        for k in (1, 2, 3, 4):
            v = l2[c][k]["reuse_share"]
            vals.append("n/a" if v is None else f"{v:.2f}")
        lines.append(f"| {c.upper()} | " + " | ".join(vals) + " |")
    lines += ["", "## Gates", "",
              f"- D1 (C>B): deltas {cb} · exceeds {out['gates']['D1']['exceeds']}/4 · median {out['gates']['D1']['median']} · threshold {out['gates']['D1']['threshold']} · PASS={out['gates']['D1']['pass']}",
              f"- D2 (B>A): deltas {ba} · exceeds {out['gates']['D2']['exceeds']}/4 · median {out['gates']['D2']['median']} · threshold {out['gates']['D2']['threshold']} · PASS={out['gates']['D2']['pass']}",
              f"- D3 (Layer 2, H2–H4): means {means} · C≥B handoffs {ge}/3 · favors C={out['gates']['D3']['favors_C']}",
              "", "Per-layer per-handoff component tables are in objective-scores.json.", ""]
    mpath = os.path.join(args.out, "objective-scores.md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("wrote", jpath)
    print("wrote", mpath)
    for c in CHAINS:
        print(c.upper(), "L1:", [l1[c][k]["fidelity"] for k in (1, 2, 3, 4)],
              "L2:", [l2[c][k]["consistency"] for k in (1, 2, 3, 4)])
    print("D1:", out["gates"]["D1"])
    print("D2:", out["gates"]["D2"])
    print("D3:", out["gates"]["D3"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
