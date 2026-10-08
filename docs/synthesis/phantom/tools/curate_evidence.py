#!/usr/bin/env python3
"""curate_evidence — copy a curated set of extraction screenshots into the app
as resized evidence images (assets/evidence/) and emit a manifest."""
import json
import os

from PIL import Image

REPO = "/home/xrim/design-authority"
SRC = os.path.join(REPO, "docs/synthesis/phantom/evidence/screens")
DST = os.path.join(REPO, "examples/phantom-audit/assets/evidence")
os.makedirs(DST, exist_ok=True)

CURATED = [
    ("colour-index-1280.png", "col", "index @1280", "The deployed default: pink reading ink on white; pink tracked-caps heads"),
    ("colour-elements-1280.png", "col", "elements @1280", "The component set in situ: blue code chips, red checks, purple labels, grey buttons"),
    ("colour-light-1280.png", "col", "light @1280", "Per-page override: black body on #fbfbfb with a pink h1; green links"),
    ("colour-elements-1280-menu-open.png", "col", "menu open @1280", "The lime #3ef900 rail with black text over the dimmed page"),
    ("type-index-heading-1280.png", "type", "wordmark @1280", "The 900 tracked-caps wordmark — and 圳 falling to the OS font"),
    ("comp-elements-btn-hover-1280.png", "comp", "button hover", "Default button mid-hover: label + ring flip to #f2849e"),
    ("comp-elements-field-focus-1280.png", "comp", "field focus", "Focused field: the 2px pink underline replaces the grey line"),
    ("comp-elements-form-1280.png", "comp", "form @1280", "Checked marks: red fill, white checkmark (radio too); purple labels"),
    ("comp-elements-table-1280.png", "comp", "table @1280", "900-weight mixed-case heads, 2px rules, tinted odd rows"),
    ("comp-index-tile-hover-1280.png", "comp", "tile hover", "The opaque #eb84da veil: the photograph disappears under flat pink"),
    ("comp-index-carousel-a-1280.png", "comp", "carousel state A", "The autoplay carousel — all six image sources 404 in production"),
    ("layout-index-nesteddoctype-1280.png", "layout", "nested doctype", "A whole document skeleton nested mid-body on index (renders as whitespace)"),
    ("layout-index-390.png", "layout", "index @390", "Mobile overflow: document is 700px wide at a 390px viewport"),
    ("layout-publication-1280.png", "layout", "publication @1280", "The .publication class: black main text while the shell stays pink"),
]

manifest = []
for fn, tag, label, caption in CURATED:
    src = os.path.join(SRC, fn)
    if not os.path.exists(src):
        print("missing:", fn)
        continue
    out = os.path.join(DST, fn)
    im = Image.open(src).convert("RGB")
    if im.width > 1000:
        rs = getattr(Image, "Resampling", Image)
        im = im.resize((1000, round(im.height * 1000 / im.width)), rs.LANCZOS)
    im.save(out, "PNG", optimize=True)
    manifest.append({"file": fn, "tag": tag, "label": label, "caption": caption})
    print(f"{fn}: {im.size[0]}x{im.size[1]}")

json.dump(manifest, open(os.path.join(DST, "manifest.json"), "w"), indent=1)
print(f"{len(manifest)} evidence images in {DST}")
