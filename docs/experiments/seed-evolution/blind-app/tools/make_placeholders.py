#!/usr/bin/env python3
"""Generate the PLACEHOLDER review set for driftexp (until the real blind set
is built from sealed captures).

    python3 tools/make_placeholders.py

Writes data/blindset/set.json, data/blindset/key.json and 6 pairs of PNGs
into data/blindset/img/. The placeholder set is excluded from any analysis.
"""
import json
import os
import random
from datetime import datetime, timezone

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "data", "blindset")
IMG = os.path.join(OUT, "img")
W, H = 1280, 880

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def font(size, bold=False):
    paths = FONT_CANDIDATES if not bold else [FONT_CANDIDATES[1], FONT_CANDIDATES[0]]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def hexc(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


# restrained near-neutral palettes; the placeholder must not look like canon
STYLES_A = {"ink": "#1a1a1a", "bg": "#fafafa", "card": "#ffffff", "line": "#e2e2e2",
            "accent": "#2b6cb0", "chip": "#eef2f7"}
STYLES_B = {"ink": "#20232a", "bg": "#f4f6f5", "card": "#ffffff", "line": "#d8dcd8",
            "accent": "#0f766e", "chip": "#e6f2f0"}


def draw_shot(path, label, style, variant):
    img = Image.new("RGB", (W, H), hexc(style["bg"]))
    d = ImageDraw.Draw(img)
    # top bar
    d.rectangle([0, 0, W, 64], fill=hexc(style["card"]))
    d.line([0, 64, W, 64], fill=hexc(style["line"]), width=1)
    d.rectangle([24, 18, 52, 46], fill=hexc(style["ink"]))
    d.text((64, 22), "Bookmarks", font=font(22, True), fill=hexc(style["ink"]))
    d.text((W - 260, 24), label, font=font(16), fill=hexc(style["ink"]))
    # content rows
    y = 104
    for i in range(6):
        pad = 20 if variant == 0 else 14
        d.rectangle([40, y, W - 40, y + 96], fill=hexc(style["card"]),
                    outline=hexc(style["line"]), width=1)
        d.text((40 + pad, y + 18), "A saved page about %s" %
               ["design", "reading", "engineering", "tools", "data", "cooking"][i],
               font=font(20, True), fill=hexc(style["ink"]))
        d.text((40 + pad, y + 52), "https://example.org/%s" % (i + 1),
               font=font(15), fill=hexc("#666666" if variant == 0 else "#5a5a5a"))
        for j, tag in enumerate(["design", "reading"][: 2 - (variant % 2)]):
            x0 = W - 240 + j * 90
            d.rectangle([x0, y + 20, x0 + 78, y + 44], fill=hexc(style["chip"]))
            d.text((x0 + 12, y + 24), tag, font=font(13), fill=hexc(style["accent"]))
        y += 116
    # footer note
    d.text((40, H - 40), "PLACEHOLDER IMAGE — generated for build testing; "
           "not part of the review data", font=font(14), fill=hexc(style["ink"]))
    img.save(path, "PNG")


def main():
    os.makedirs(IMG, exist_ok=True)
    rng = random.Random(20261009)
    comparisons = []
    for n in range(1, 7):
        code = "P%02d" % n
        a_file, b_file = "%s-a.png" % code, "%s-b.png" % code
        # pairs 1-3: same style both sides; pairs 4-6: drifted style on B
        drift = n >= 4
        variant_b = 1 if drift else 0
        draw_shot(os.path.join(IMG, a_file), "PLACEHOLDER · %s · A" % code, STYLES_A, 0)
        draw_shot(os.path.join(IMG, b_file), "PLACEHOLDER · %s · B" % code, STYLES_B, variant_b)
        left, right = (a_file, b_file) if rng.random() < 0.5 else (b_file, a_file)
        comparisons.append({
            "code": code, "kind": "placeholder",
            "prompt": "How likely are these two interfaces to belong to the same design system?",
            "left": left, "right": right, "scale": 5,
        })
    set_obj = {
        "version": 1, "placeholder": True,
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "title": "Design drift review",
        "blurb": "Compare pairs of interface screenshots from an evolving product and rate one narrow question per pair. This is a guided, private review.",
        "comparisons": comparisons,
    }
    with open(os.path.join(OUT, "set.json"), "w") as fh:
        json.dump(set_obj, fh, indent=1)
    with open(os.path.join(OUT, "key.json"), "w") as fh:
        json.dump({"placeholder": True,
                   "note": "Placeholder set — no condition mapping exists; "
                           "excluded from analysis. The real set is generated "
                           "from sealed captures by the experiment pipeline.",
                   "created": set_obj["created"]}, fh, indent=1)
    print("placeholder set written: %d pairs -> %s" % (len(comparisons), OUT))


if __name__ == "__main__":
    main()
