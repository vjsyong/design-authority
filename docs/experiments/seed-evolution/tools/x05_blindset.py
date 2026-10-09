#!/usr/bin/env python3
"""x05_blindset.py — generate the driftexp review set from sealed captures. REV 2.

Rev 1 (every adjacent-checkpoint pair, three ways) produced largely
pixel-identical comparisons: from the first handoff onward the established
surfaces render byte-identical, so the informative comparisons are

  pair  (x3)  — the seed -> first-handoff step, whole screens; and
  match (x12) — each handoff's newest elements against established elements
                of the same app ("matched role and component regions"):
                  k=1  the new list-controls band  vs the seed's tag-filter band
                  k=2  the tag-analytics view      vs the app's own card
                  k=3  the command palette         vs the app's own card
                  k=4  the import wizard           vs the app's own card

Item order and left/right orientation are shuffled with a recorded seed;
the code -> (condition, chain, handoff, kind) mapping is written ONLY to
key.json (server-side, never served) and a copy under the x05 analysis
area. The mapping stays sealed until scoring ends.

Usage:
  python3 x05_blindset.py [--root /home/xrim/x05] [--out DIR] [--seed N]
"""
import argparse
import hashlib
import json
import os
import random
import shutil
import sys
from datetime import datetime, timezone

from PIL import Image

X05 = os.environ.get("X05_ROOT", "/home/xrim/x05")
DEFAULT_OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "blind-app", "data", "blindset")

VIEWPORT = (1280, 900)
MARGIN = 10
CHAINS = ("a", "b", "c")
PROMPTS = {
    "pair": "How likely is it that these two screens belong to the same "
            "product, with one consistent design language?",
    "match": "How likely is it that these two elements were built as parts "
             "of one design system?",
}
# fixed viewport windows for the feature views (desktop coordinates)
WINDOWS = {
    "analytics": (180, 131, 920, 400),
    "palette": (355, 100, 570, 350),
    "wizard-2": (280, 95, 720, 510),
}
FEATURE_STATE = {2: "analytics", 3: "palette", 4: "wizard-2"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_rect(root, sid, state, tid):
    pr = json.load(open(os.path.join(root, "run", sid, "capture", "probes.json")))
    for e in (pr.get(state, {}).get("testids") or {}).get(tid) or []:
        r = e.get("rect") or {}
        if r.get("w") and r.get("h"):
            return (r["x"], r["y"], r["w"], r["h"])
    return None


def shot(root, sid, state):
    return os.path.join(root, "run", sid, "capture", "screens",
                        "%s-desktop.png" % state)


def clip(img, box, margin=MARGIN):
    x, y, w, h = box
    x0, y0 = max(0, x - margin), max(0, y - margin)
    x1, y1 = min(img.width, x + w + margin), min(img.height, y + h + margin)
    if x1 - x0 < 40 or y1 - y0 < 20:
        raise SystemExit("degenerate crop %s" % (box,))
    return (x0, y0, x1, y1)


def render(root, dst, sid, state, box):
    img = Image.open(shot(root, sid, state))
    b = clip(img, box)
    img.crop(b).save(dst, "PNG")
    return list(b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=X05)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--seed", type=int, default=20261009)
    args = ap.parse_args()
    root, out = args.root, args.out
    img_dir = os.path.join(out, "img")
    os.makedirs(img_dir, exist_ok=True)

    # ---- item list -----------------------------------------------------------
    items = []
    for c in CHAINS:
        items.append({"kind": "pair", "chain": c, "k": 1,
                      "a": {"sid": "h1" + c, "state": "populated", "box": ("viewport",)},
                      "b": {"sid": "f3", "state": "populated", "box": ("viewport",)},
                      "region": "seed -> h1, whole screens"})
        for k in range(1, 5):
            sid = "h%d%s" % (k, c)
            if k == 1:
                ctl = probe_rect(root, sid, "populated", "list-controls")
                ref = probe_rect(root, "f3", "populated", "tag-filter")
                if ctl is None or ref is None:
                    raise SystemExit("missing rect k=1 %s" % sid)
                a = {"sid": sid, "state": "populated", "box": ctl}
                b = {"sid": "f3", "state": "populated", "box": ref}
                region = "new list-controls vs seed tag-filter"
            else:
                st = FEATURE_STATE[k]
                win = WINDOWS[st]
                card = probe_rect(root, sid, "populated", "bookmark-card")
                if card is None:
                    raise SystemExit("missing card rect %s" % sid)
                a = {"sid": sid, "state": st, "box": win}
                b = {"sid": sid, "state": "populated", "box": card}
                region = "%s view vs own card" % st
            items.append({"kind": "match", "chain": c, "k": k, "a": a, "b": b,
                          "region": region})

    rng = random.Random(args.seed)
    rng.shuffle(items)
    for it in items:
        if rng.random() < 0.5:
            it["a"], it["b"] = it["b"], it["a"]
            it["flipped"] = True

    # ---- render --------------------------------------------------------------
    comparisons, key_items = [], []
    for n, it in enumerate(items, 1):
        code = "R%02d" % n
        sides, boxes = {}, {}
        for pos in ("a", "b"):
            spec = it[pos]
            fn = "%s-%s.png" % (code, pos)
            dst = os.path.join(img_dir, fn)
            if spec["box"][0] == "viewport":
                img = Image.open(shot(root, spec["sid"], spec["state"]))
                if img.width < VIEWPORT[0] or img.height < VIEWPORT[1]:
                    raise SystemExit("shot smaller than viewport: %s" % spec)
                img.crop((0, 0, VIEWPORT[0], VIEWPORT[1])).save(dst, "PNG")
                boxes[pos] = [0, 0, VIEWPORT[0], VIEWPORT[1]]
            else:
                boxes[pos] = render(root, dst, spec["sid"], spec["state"], spec["box"])
            sides[pos] = fn
        comparisons.append({"code": code, "kind": it["kind"],
                            "prompt": PROMPTS[it["kind"]],
                            "left": sides["a"], "right": sides["b"], "scale": 5})
        key_items.append({
            "code": code, "kind": it["kind"], "chain": it["chain"],
            "condition": it["chain"].upper(), "k": it["k"],
            "region": it["region"], "flipped": bool(it.get("flipped")),
            "file_a": sides["a"], "session_a": it["a"]["sid"],
            "state_a": it["a"]["state"], "box_a": boxes["a"],
            "sha256_a": sha256(os.path.join(img_dir, sides["a"])),
            "file_b": sides["b"], "session_b": it["b"]["sid"],
            "state_b": it["b"]["state"], "box_b": boxes["b"],
            "sha256_b": sha256(os.path.join(img_dir, sides["b"])),
        })

    created = datetime.now(timezone.utc).isoformat(timespec="seconds")
    set_obj = {
        "version": 3, "placeholder": False, "created": created,
        "title": "Design drift review",
        "blurb": "Pairs of interface details from products in development: "
                 "sometimes a whole screen, sometimes two elements from the "
                 "same app. Rate the single narrow question above each pair. "
                 "This is a guided, private review.",
        "comparisons": comparisons,
    }
    key_obj = {
        "version": 3, "rev": "real-v2", "placeholder": False, "created": created,
        "seed": args.seed, "source": "sealed captures, %s" % root,
        "note": "Server-side code->(condition, chain, handoff, kind) mapping. "
                "SEALED until scoring completes; never served by the app.",
        "counts": {"items": len(key_items),
                   "pairs": sum(1 for i in key_items if i["kind"] == "pair"),
                   "matches": sum(1 for i in key_items if i["kind"] == "match")},
        "items": key_items,
    }

    # keep earlier revisions aside (once)
    for name, backup in (("set.json", "set-real-v1.json"),
                         ("key.json", "key-real-v1.json")):
        src, dst = os.path.join(out, name), os.path.join(out, backup)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)

    with open(os.path.join(out, "set.json"), "w") as fh:
        json.dump(set_obj, fh, indent=1)
    with open(os.path.join(out, "key.json"), "w") as fh:
        json.dump(key_obj, fh, indent=1)
    ana = os.path.join(root, "analysis")
    os.makedirs(ana, exist_ok=True)
    shutil.copy2(os.path.join(out, "key.json"), os.path.join(ana, "blindset-key.json"))

    print("rev2 set written: %d items (%d pair + %d match) -> %s"
          % (len(comparisons), key_obj["counts"]["pairs"],
             key_obj["counts"]["matches"], out))
    for i in key_items:
        print("  %s %-5s chain=%s k=%d  a=%s/%s  b=%s/%s"
              % (i["code"], i["kind"], i["chain"], i["k"],
                 i["session_a"], i["state_a"], i["session_b"], i["state_b"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
