#!/usr/bin/env python3
"""p4_blindset.py — build the three-arm review set from R1 captures.

    python3 docs/experiments/tools/p4_blindset.py [--root ~/p4-maint] [--seed N]

Live items (kind "match", 9): each arm's controls band (default screen,
y 130-360) at h1 (established) vs h2/h3/h4 (current work) — one narrow
question, orientation shuffled with the recorded seed.

Calibration items (kind "cal", 5): pre-scored pairs from the x05 round
(R13=1, R11=2, R04=3, R12=4, R05=4 on the 1-5 same-design-system scale),
served first; their images already live in the app's img/ directory.

The code -> (arm, k, orientation) mapping is written ONLY to key.json
(server-side, never served) with a sealed copy under the run area.
"""
import argparse
import json
import os
import random
import shutil
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p4_common import P4_ROOT, run_dir  # noqa: E402

BAND = (0, 130, 1280, 700)
ARMS = ("a", "b", "c")
# (state, k) per live item — the comparisons where visible change exists:
#   h2 rework is visible in the editor state; h3 in the default list surface;
#   h5 is the post-repair final state. (h4 shows no visible change in the
#   captured states for these fixtures — favourites empty, conflicts absent.)
LIVE_SPEC = (("editor", 2), ("default", 3), ("default", 5))
MATCH_PROMPT = ("How likely is it that these two elements were built as "
                "parts of one design system?")
CAL = [("R13", 1), ("R11", 2), ("R04", 3), ("R12", 4), ("R05", 4)]

DEFAULT_OUT = os.path.join(
    os.path.dirname(HERE), "seed-evolution", "blind-app", "data", "blindset")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=P4_ROOT)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--seed", type=int, default=20261011)
    ap.add_argument("--keys-copy", default=None,
                    help="additional sealed key copy (default: <root>/analysis)")
    args = ap.parse_args()
    root = os.path.abspath(os.path.expanduser(args.root))
    out = os.path.abspath(os.path.expanduser(args.out))
    img = os.path.join(out, "img")
    os.makedirs(img, exist_ok=True)

    from PIL import Image

    # live crops: for each arm, the (state, k) comparisons vs the h1 state
    files = {}
    for arm in ARMS:
        for st, k in LIVE_SPEC:
            ref = Image.open(os.path.join(run_dir("r1-%s-h1" % arm, root),
                                          "capture", "%s.png" % st)).convert("RGB")
            cur = Image.open(os.path.join(run_dir("r1-%s-h%d" % (arm, k), root),
                                          "capture", "%s.png" % st)).convert("RGB")
            files[(arm, st, k)] = (ref.crop(BAND), cur.crop(BAND))

    rng = random.Random(args.seed)
    items = list(files.items())
    live_codes = ["L%02d" % (i + 1) for i in range(len(items))]
    rng.shuffle(live_codes)

    comparisons = []
    key_items = []
    for code, (rk, val) in zip(["C%02d" % (i + 1) for i in range(len(CAL))], CAL):
        comparisons.append({
            "code": code, "kind": "cal", "prompt": MATCH_PROMPT,
            "left": "%s-a.png" % rk, "right": "%s-b.png" % rk, "scale": 5})
        key_items.append({"code": code, "kind": "cal", "source": rk,
                          "pre_score": val})

    shuffled = list(items)
    rng.shuffle(shuffled)
    live_order = []
    for code, ((arm, st, k), (a_im, b_im)) in zip(live_codes, shuffled):
        flipped = rng.random() < 0.5
        fa, fb = ("%s-a.png" % code, "%s-b.png" % code)
        first, second = (b_im, a_im) if flipped else (a_im, b_im)
        first.save(os.path.join(img, fa))
        second.save(os.path.join(img, fb))
        same = a_im.tobytes() == b_im.tobytes()
        comparisons.append({
            "code": code, "kind": "match", "prompt": MATCH_PROMPT,
            "left": fa, "right": fb, "scale": 5})
        key_items.append({"code": code, "kind": "match", "arm": arm,
                          "state": st, "k": k, "flipped": flipped,
                          "identical_pixels": same,
                          "file_a": fa, "file_b": fb})
        live_order.append((code, arm, st, k, flipped, same))

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    setp = os.path.join(out, "set.json")
    if os.path.exists(setp):
        shutil.copy2(setp, os.path.join(out, "set-prev-round.json"))
    setdata = {
        "version": 2, "placeholder": False, "created": now,
        "title": "Design review — maintenance run",
        "blurb": ("Pairs of interface elements from products in development — "
                  "sometimes a whole screen, sometimes one element shown twice. "
                  "Rate the single narrow question above each pair. This is a "
                  "guided, private review."),
        "comparisons": comparisons,
    }
    with open(setp, "w") as fh:
        json.dump(setdata, fh, indent=1, ensure_ascii=False)
    keyp = os.path.join(out, "key.json")
    if os.path.exists(keyp):
        shutil.copy2(keyp, os.path.join(out, "key-prev-round.json"))
    keydata = {"version": 3, "rev": "p4b-r1", "placeholder": False,
               "created": now, "seed": args.seed,
               "note": ("Server-side code->(arm, handoff, orientation) mapping; "
                        "sealed until scoring completes; never served."),
               "calibration": [c for c in key_items if c["kind"] == "cal"],
               "items": [c for c in key_items if c["kind"] == "match"]}
    with open(keyp, "w") as fh:
        json.dump(keydata, fh, indent=1, ensure_ascii=False)
    copy = args.keys_copy or os.path.join(root, "analysis", "blindset-key.json")
    os.makedirs(os.path.dirname(copy), exist_ok=True)
    with open(copy, "w") as fh:
        json.dump(keydata, fh, indent=1, ensure_ascii=False)
    print("set written: %d comparisons (5 cal + %d live)" %
          (len(comparisons), len(live_order)))
    for code, arm, st, k, flipped, same in sorted(live_order):
        print("   %s -> arm %s, %s h%d, flipped=%s%s" %
              (code, arm, st, k, flipped, "  [IDENTICAL PIXELS]" if same else ""))


if __name__ == "__main__":
    main()
