#!/usr/bin/env python3
"""Fetch Source Sans Pro woff2 (latin + latin-ext) + vendor FA assets for phantom-audit."""
import os
import re
import shutil
import urllib.request

REPO = "/home/xrim/design-authority"
RAW = os.path.join(REPO, "docs", "synthesis", "phantom", "_raw")
APP = os.path.join(REPO, "examples", "phantom-audit")
FONTS = os.path.join(APP, "assets", "fonts")
os.makedirs(FONTS, exist_ok=True)

css = open(os.path.join(RAW, "fonts", "google.css")).read()
# blocks: optional /* comment */ then @font-face
blocks = re.findall(r"(?:/\*\s*([a-z-]+)\s*\*/)?\s*@font-face\s*\{(.*?)\}", css, re.S)
wanted = {"latin", "latin-ext"}
seen = set()
for subset, body in blocks:
    if subset not in wanted:
        continue
    w = re.search(r"font-weight:\s*(\d+)", body)
    u = re.search(r"url\((https://[^)]+\.woff2)\)", body)
    if not (w and u):
        continue
    key = (w.group(1), subset)
    if key in seen:
        continue
    seen.add(key)
    dest = os.path.join(FONTS, f"source-sans-pro-{w.group(1)}-{subset}.woff2")
    urllib.request.urlretrieve(u.group(1), dest)
    print("font:", os.path.basename(dest), os.path.getsize(dest), "bytes")

# Font Awesome from the upstream template zip
up = os.path.join(RAW, "upstream", "assets")
os.makedirs(os.path.join(APP, "assets", "css"), exist_ok=True)
os.makedirs(os.path.join(APP, "assets", "webfonts"), exist_ok=True)
shutil.copy(os.path.join(up, "css", "fontawesome-all.min.css"), os.path.join(APP, "assets", "css", "fontawesome-all.min.css"))
for f in ("fa-solid-900.woff2", "fa-brands-400.woff2", "fa-regular-400.woff2"):
    src = os.path.join(up, "webfonts", f)
    if os.path.exists(src):
        shutil.copy(src, os.path.join(APP, "assets", "webfonts", f))
        print("fa:", f, os.path.getsize(src), "bytes")
    else:
        print("fa MISSING:", f)
print("done")
