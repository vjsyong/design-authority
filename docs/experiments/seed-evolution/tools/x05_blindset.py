#!/usr/bin/env python3
"""x05_blindset.py — generate the REAL driftexp review set from sealed captures.

For each drift chain (a, b, c) and handoff k = 1..4, the adjacent checkpoints
are paired: f3 -> h1x, h1x -> h2x, h2x -> h3x, h3x -> h4x. Three items per
pair, all from the 'populated' desktop capture (viewport 1280x900):

  pair    — the full desktop viewport of both checkpoints
  primary — matched crop of the primary action (btn-add-bookmark) both sides
  card    — matched crop of the first bookmark card both sides

Element crops use each side's OWN recorded rect (probes.json), so the crops
are matched by element, not by fixed coordinates. Item order and left/right
orientation are shuffled with a recorded seed; the code -> (chain, k, kind)
mapping is written ONLY to key.json (server-side, never served) and a copy
under the x05 analysis area. The mapping stays sealed until scoring ends.

Usage:
  python3 x05_blindset.py [--root /home/xrim/x05] [--out DIR] [--seed N]
"""
import argparse
import copy
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
MARGIN = 10  # px around element crops
CHAINS = ("a", "b", "c")
PROMPTS = {
    "pair": "How likely is it that these two screens belong to the same "
            "product, with one consistent design language?",
    "primary": "How likely is it that these two versions of the primary "
               "action share one consistent treatment?",
    "card": "How likely is it that these two versions of the same bookmark "
            "card share one consistent treatment?",
}
REGION_TIDS = {"primary": "btn-add-bookmark", "card": "bookmark-card"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def rect_of(root, sid, tid):
    pr = json.load(open(os.path.join(root, "run", sid, "capture", "probes.json")))
    els = pr["populated"]["testids"].get(tid) or []
    if not els or not els[0].get("rect"):
        return None
    r = els[0]["rect"]
    if not r.get("w") or not r.get("h"):
        return None
    return (r["x"], r["y"], r["w"], r["h"])


def shot_path(root, sid):
    return os.path.join(root, "run", sid, "capture", "screens", "populated-desktop.png")


def crop_to(path, box, out):
    img = Image.open(path)
    x, y, w, h = box
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(img.width, x + w), min(img.height, y + h)
    if x1 - x0 < 40 or y1 - y0 < 20:
        raise SystemExit("degenerate crop %s in %s" % (box, path))
    img.crop((x0, y0, x1, y1)).save(out, "PNG")


def viewport_crop(path, out):
    img = Image.open(path)
    if img.width < VIEWPORT[0] or img.height < VIEWPORT[1]:
        raise SystemExit("shot smaller than viewport: %s (%s)" % (path, img.size))
    img.crop((0, 0, VIEWPORT[0], VIEWPORT[1])).save(out, "PNG")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=X05)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--seed", type=int, default=20261009)
    args = ap.parse_args()
    root, out = args.root, args.out
    img_dir = os.path.join(out, "img")
    os.makedirs(img_dir, exist_ok=True)

    # ---- build the item list -------------------------------------------------
    pairs = []  # (chain, k, prev_sid, cur_sid)
    for c in CHAINS:
        for k in range(1, 5):
            prev = "f3" if k == 1 else "h%d%s" % (k - 1, c)
            cur = "h%d%s" % (k, c)
            pairs.append((c, k, prev, cur))

    items = []
    for c, k, prev, cur in pairs:
        for kind in ("pair", "primary", "card"):
            items.append({"kind": kind, "chain": c, "k": k,
                          "prev": prev, "cur": cur})

    rng = random.Random(args.seed)
    rng.shuffle(items)

    # ---- render images --------------------------------------------------------
    comparisons, key_items = [], []
    for n, it in enumerate(items, 1):
        code = "R%02d" % n
        sides = [it["prev"], it["cur"]]
        if rng.random() < 0.5:
            sides = sides[::-1]  # orientation randomized; recorded below
        files = {}
        for pos, sid in zip(("a", "b"), sides):
            fn = "%s-%s.png" % (code, pos)
            dst = os.path.join(img_dir, fn)
            if it["kind"] == "pair":
                viewport_crop(shot_path(root, sid), dst)
            else:
                r = rect_of(root, sid, REGION_TIDS[it["kind"]])
                if r is None:
                    raise SystemExit("no rect for %s in %s (%s)"
                                     % (REGION_TIDS[it["kind"]], sid, code))
                box = (r[0] - MARGIN, r[1] - MARGIN, r[2] + 2 * MARGIN, r[3] + 2 * MARGIN)
                crop_to(shot_path(root, sid), box, dst)
            files[pos] = fn
        comparisons.append({"code": code, "kind": it["kind"],
                            "prompt": PROMPTS[it["kind"]],
                            "left": files["a"], "right": files["b"], "scale": 5})
        key_items.append({"code": code, "kind": it["kind"], "chain": it["chain"],
                          "k": it["k"], "condition": it["chain"].upper(),
                          "state": "populated",
                          "file_a": files["a"], "session_a": sides[0],
                          "file_b": files["b"], "session_b": sides[1],
                          "sha256_a": sha256(os.path.join(img_dir, files["a"])),
                          "sha256_b": sha256(os.path.join(img_dir, files["b"]))})

    created = datetime.now(timezone.utc).isoformat(timespec="seconds")
    set_obj = {
        "version": 2, "placeholder": False, "created": created,
        "title": "Design drift review",
        "blurb": "Pairs of interface screenshots from products in development "
                 "— sometimes a whole screen, sometimes one element shown "
                 "twice. Rate the single narrow question above each pair. "
                 "This is a guided, private review.",
        "comparisons": comparisons,
    }
    key_obj = {
        "version": 2, "placeholder": False, "created": created,
        "seed": args.seed, "source": "sealed captures, %s" % root,
        "note": "Server-side code->(condition, chain, handoff, kind) mapping. "
                "SEALED until scoring completes; never served by the app.",
        "counts": {"items": len(key_items),
                   "pairs": sum(1 for i in key_items if i["kind"] == "pair")},
        "items": key_items,
    }

    # keep the placeholder set aside (first run only)
    for name, backup in (("set.json", "set-placeholder.json"),
                         ("key.json", "key-placeholder.json")):
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

    print("real set written: %d items (%d pair + %d region) -> %s"
          % (len(comparisons), key_obj["counts"]["pairs"],
             len(comparisons) - key_obj["counts"]["pairs"], out))
    for i in key_items:
        print("  %s %-7s chain=%s k=%d  a=%s  b=%s"
              % (i["code"], i["kind"], i["chain"], i["k"], i["session_a"], i["session_b"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
