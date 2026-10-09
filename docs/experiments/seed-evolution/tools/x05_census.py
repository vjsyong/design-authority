#!/usr/bin/env python3
"""x05 census — classify the six frozen roles at a checkpoint and freeze the
reference exemplars for that chain.

Runs after every chain session (and its extraction). Deterministic wherever
possible: compatibility uses the frozen dimension pass rules, records are
matched by fixed keyword sets, and every raw observation is retained. The
output schema matches the seed census the `cen` session produces, so chains
inherit the seed exemplars by file. Anything the rules cannot decide is left
as evidence with a review flag, never silently upgraded.

Marks the freeze with timestamps; the conductor only schedules the next
session of a chain after this has completed, so the frozen set always
predates the next handoff.

Usage: x05_census.py --id SID [--root X05_ROOT] [--schedule PATH]
"""
import argparse
import json
import math
import os
import re
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from x05_common import read_json, write_json_atomic  # noqa: E402

ROLE_RECORD_KEYWORDS = {
    "primary-action": ["primary", "add bookmark", "add button", "save", "submit"],
    "destructive": ["delete", "destructive", "confirm", "remove"],
    "empty-state": ["empty", "first-run", "no matches", "no bookmarks"],
    "form-validation": ["validat", "invalid", "error", "required", "url"],
    "tags-status": ["tag", "chip", "filter"],
    "surfaces": ["card", "border", "surface", "panel", "radius"],
}


# ------------------------------------------------------------------ colours
def parse_color(text):
    if not text:
        return None
    m = re.match(r"rgba?\(([^)]+)\)", text.strip())
    if not m:
        return None
    parts = [p.strip() for p in m.group(1).split(",")]
    try:
        vals = [float(p) for p in parts[:3]]
        a = float(parts[3]) if len(parts) > 3 else 1.0
    except ValueError:
        return None
    if a == 0:
        return None
    return tuple(vals)


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lab(rgb):
    r, g, b = (_lin(c) for c in rgb)
    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e2000(rgb1, rgb2):
    if rgb1 is None or rgb2 is None:
        return None
    L1, a1, b1 = lab(rgb1)
    L2, a2, b2 = lab(rgb2)
    kL = kC = kH = 1.0
    C1 = math.hypot(a1, b1)
    C2 = math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7))) if Cb > 0 else 0.5
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0.0
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180:
            dhp -= 360
        elif dhp < -180:
            dhp += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)
    Lbp = (L1 + L2) / 2
    Cbp = (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    else:
        if abs(h1p - h2p) <= 180:
            hbp = (h1p + h2p) / 2
        else:
            hbp = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30))
         + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6))
         - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dTh = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    RC = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7)) if Cbp > 0 else 0
    SL = 1 + (0.015 * (Lbp - 50) ** 2) / math.sqrt(20 + (Lbp - 50) ** 2)
    SC = 1 + 0.045 * Cbp
    SH = 1 + 0.015 * Cbp * T
    RT = -math.sin(math.radians(2 * dTh)) * RC
    return math.sqrt((dLp / (kL * SL)) ** 2 + (dCp / (kC * SC)) ** 2
                     + (dHp / (kH * SH)) ** 2 + RT * (dCp / (kC * SC)) * (dHp / (kH * SH)))


# --------------------------------------------------------------- dimensions
def radius_class(text):
    vals = [float(x) for x in re.findall(r"([\d.]+)px", text or "")]
    if not vals:
        return None
    v = vals[0]
    if v >= 100:
        return "pill"
    return round(v, 1)


def font_class(text):
    fam = (text or "").lower()
    if not fam:
        return None
    if "mono" in fam:
        return "mono"
    serif_names = ("serif", "georgia", "times", "garamond", "playfair", "fraunces",
                   "gelasio", "charter", "cambria")
    if any(n in fam for n in serif_names) and "sans" not in fam.split(",")[0]:
        return "serif"
    return "sans"


def border_class(styles):
    sh = (styles or {}).get("shadow") or "none"
    bt = (styles or {}).get("borderTop") or "0px none"
    if sh and sh != "none":
        return "shadow"
    m = re.match(r"([\d.]+)px", bt)
    w = float(m.group(1)) if m else 0.0
    if w == 0:
        return "none"
    if w <= 1.5:
        return "hairline"
    return "strong"


def padding_tuple(text):
    vals = re.findall(r"([\d.]+)px", text or "")
    return [round(float(v), 1) for v in vals]


def spacing_compatible(a, b):
    pa, pb = a, b
    if not pa or not pb or len(pa) != len(pb):
        return False, "missing"
    ratios = []
    for x, y in zip(pa, pb):
        if x == 0 and y == 0:
            ratios.append(1.0)
        elif x == 0 or y == 0:
            return False, "zero-mismatch"
        else:
            ratios.append(max(x, y) / min(x, y))
    ok = max(ratios) <= 1.2
    return ok, "ratio %.2f" % max(ratios)


def instance_dims(measured):
    st = measured.get("styles") or {}
    return {
        "bg": parse_color(st.get("bg")),
        "fg": parse_color(st.get("color")),
        "radius": radius_class(st.get("radius")),
        "font_class": font_class(st.get("font")),
        "font_raw": st.get("font"),
        "border": border_class(st),
        "padding": padding_tuple(st.get("padding")),
        "_raw": {"bg": st.get("bg"), "color": st.get("color"),
                 "radius": st.get("radius"), "borderTop": st.get("borderTop"),
                 "shadow": st.get("shadow"), "padding": st.get("padding")},
    }


def dims_compatible(d1, d2):
    """Frozen pass rules (§7) applied instance-to-instance."""
    detail = {}
    ok = True
    if d1["bg"] and d2["bg"]:
        de = delta_e2000(d1["bg"], d2["bg"])
        detail["palette_deltaE"] = round(de, 2)
        if de > 5:
            ok = False
    elif bool(d1["bg"]) != bool(d2["bg"]):
        detail["palette"] = "one-side-transparent"
        ok = False
    if d1["radius"] is not None and d2["radius"] is not None:
        if d1["radius"] == "pill" or d2["radius"] == "pill":
            if not (d1["radius"] == "pill" and d2["radius"] == "pill"):
                detail["radius"] = "%s vs %s" % (d1["radius"], d2["radius"])
                ok = False
        else:
            diff = abs(d1["radius"] - d2["radius"])
            detail["radius_diff"] = diff
            if diff > 2:
                ok = False
    if d1["font_class"] and d2["font_class"] and d1["font_class"] != d2["font_class"]:
        detail["font_class"] = "%s vs %s" % (d1["font_class"], d2["font_class"])
        ok = False
    if d1["border"] and d2["border"] and d1["border"] != d2["border"]:
        detail["border"] = "%s vs %s" % (d1["border"], d2["border"])
        ok = False
    sp_ok, sp_detail = spacing_compatible(d1["padding"], d2["padding"])
    detail["spacing"] = sp_detail
    # spacing is secondary here (paddings vary by element size); do not veto
    return ok, detail


# ------------------------------------------------------------------- records
def records_matching(ws, role):
    kws = ROLE_RECORD_KEYWORDS.get(role, [])
    n = 0
    recdir = os.path.join(ws, ".design-authority")
    if not os.path.isdir(recdir):
        return 0
    texts = []
    gaps = os.path.join(recdir, "gaps.jsonl")
    if os.path.exists(gaps):
        for line in open(gaps, encoding="utf-8", errors="replace"):
            texts.append(line.lower())
    propt = os.path.join(recdir, "proposals")
    if os.path.isdir(propt):
        for name in os.listdir(propt):
            try:
                texts.append(open(os.path.join(propt, name), encoding="utf-8",
                                  errors="replace").read().lower())
            except OSError:
                continue
    for t in texts:
        if any(k in t for k in kws):
            n += 1
    return n


# -------------------------------------------------------------------- census
def chain_sessions(schedule, sid):
    entry = None
    for s in schedule.get("sessions", []):
        if s["id"] == sid:
            entry = s
            break
    if not entry:
        return None, None, []
    chain = entry.get("chain")  # [idx, cond]
    if not chain:
        return entry, None, []
    members = [s for s in schedule["sessions"]
               if s.get("chain") == chain and s.get("k", 0) <= entry.get("k", 0)]
    members.sort(key=lambda s: s.get("k", 0))
    return entry, chain, members


def classify_role(instances_by_session, records_n):
    """instances_by_session: [(sid, [dims...])] oldest -> newest."""
    sessions_with = [(sid, dims) for sid, dims in instances_by_session if dims]
    if not sessions_with:
        return {"classification": "Absent", "sessions": [], "compat": []}
    if len(sessions_with) == 1:
        return {"classification": "Observed once",
                "sessions": [sessions_with[0][0]], "compat": []}
    compat_pairs = []
    all_ok = True
    for i in range(len(sessions_with)):
        for j in range(i + 1, len(sessions_with)):
            si, di = sessions_with[i]
            sj, dj = sessions_with[j]
            pair_ok = False
            details = []
            for a in di:
                for b in dj:
                    ok, detail = dims_compatible(a, b)
                    details.append(detail)
                    if ok:
                        pair_ok = True
            compat_pairs.append({"a": si, "b": sj, "compatible": pair_ok,
                                 "details": details[:4]})
            if not pair_ok:
                all_ok = False
    if all_ok:
        cls = "Established"
    else:
        cls = "Inconsistent"
    return {"classification": cls, "sessions": [s for s, _ in sessions_with],
            "compat": compat_pairs, "records": records_n}


def run_census(sid, root, schedule):
    entry, chain, members = chain_sessions(schedule, sid)
    ws = os.path.join(root, "run", sid, "ws")
    out = {"id": sid, "chain": chain, "k": (entry or {}).get("k"),
           "step": (entry or {}).get("step"),
           "method": "deterministic rules + retained raw evidence",
           "frozen": datetime.now(timezone.utc).isoformat(timespec="seconds")}

    # seed census (inherited)
    seed = read_json(os.path.join(root, "run", "cen", "extraction", "exemplars.json"))
    out["inherited_seed"] = bool(seed)
    if seed:
        out["seed_exemplars"] = seed.get("exemplars", {})

    # collect instances per role across this chain's sessions so far
    roles_out = {}
    exemplars = {}
    for role in ROLE_RECORD_KEYWORDS:
        instances_by_session = []
        latest = None
        for m in members:
            roles_file = os.path.join(root, "run", m["id"], "extraction", "roles.json")
            data = read_json(roles_file)
            if not data:
                instances_by_session.append((m["id"], []))
                continue
            block = (data.get("roles") or {}).get(role) or {}
            dims_list = []
            for ent in block.get("entries", []):
                measured = ent.get("measured") or {}
                inst = instance_dims(measured)
                inst["_testid"] = ent.get("testid")
                inst["_state"] = ent.get("state")
                dims_list.append(inst)
            instances_by_session.append((m["id"], dims_list))
            if dims_list:
                latest = {"session": m["id"],
                          "entry": block.get("entries", [])[-1],
                          "dims": dims_list[-1]}
        cls = classify_role(instances_by_session, records_matching(ws, role))
        cls["latest"] = ({"session": latest["session"],
                          "testid": latest["entry"].get("testid"),
                          "state": latest["entry"].get("state"),
                          "measured": latest["entry"].get("measured")}
                         if latest else None)
        roles_out[role] = cls
        if cls["classification"] == "Established" and latest:
            exemplars[role] = {
                "source_session": latest["session"],
                "testid": latest["entry"].get("testid"),
                "state": latest["entry"].get("state"),
                "measured": latest["entry"].get("measured"),
                "dimension_signature": {k: v for k, v in latest["dims"].items()
                                        if k != "_raw"},
                "frozen": out["frozen"],
            }
    out["roles"] = roles_out
    out["established"] = [r for r, c in roles_out.items()
                          if c["classification"] == "Established"]
    out["review_flags"] = [r for r, c in roles_out.items()
                           if c["classification"] == "Inconsistent"]
    return out, {"id": sid, "frozen": out["frozen"], "exemplars": exemplars,
                 "inherited_seed": out["inherited_seed"],
                 "seed_exemplars": out.get("seed_exemplars", {})}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--root", default=None)
    ap.add_argument("--schedule", default=None)
    args = ap.parse_args(argv)
    from x05_common import X05_ROOT
    root = args.root or X05_ROOT
    schedule = read_json(args.schedule or os.path.join(root, "schedule.json"), {}) or {}
    census, exemplars = run_census(args.id, root, schedule)
    out_dir = os.path.join(root, "run", args.id, "extraction")
    os.makedirs(out_dir, exist_ok=True)
    write_json_atomic(os.path.join(out_dir, "census.json"), census)
    write_json_atomic(os.path.join(out_dir, "exemplars.json"), exemplars)
    print("census %s: established=%s review=%s"
          % (args.id, ",".join(census["established"]) or "-",
             ",".join(census["review_flags"]) or "-"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
