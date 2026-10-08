#!/usr/bin/env python3
"""mirror_site — build a complete, offline-renderable mirror of zhenyoyo.github.io.

The first pass served the raw HTML without assets (404 on assets/css/main.css),
which produced unstyled renders and hid the site's true colour identity.
This mirror lays out every page with its full asset tree so the extraction
agents can screenshot and probe the REAL rendered site.
"""
import os
import re
import shutil
import urllib.request

REPO = "/home/xrim/design-authority"
RAW = os.path.join(REPO, "docs", "synthesis", "phantom", "_raw")
SITE = os.path.join(RAW, "site")
UP = os.path.join(RAW, "upstream", "assets")
LIVE = "https://zhenyoyo.github.io/"

PAGES = ["index.html", "elements.html", "generic.html", "publication.html",
         "light.html", "tame.html", "fafa.html", "Unlogical.html", "email.html"]

for sub in ("assets/css", "assets/js", "assets/webfonts", "images", "randomgallery",
            "light", "tame", "fafa", "Unlogical"):
    os.makedirs(os.path.join(SITE, sub), exist_ok=True)

# 1) pages + her css/js
for p in PAGES:
    shutil.copy(os.path.join(RAW, p), os.path.join(SITE, p))
shutil.copy(os.path.join(RAW, "main.css"), os.path.join(SITE, "assets/css/main.css"))
shutil.copy(os.path.join(RAW, "noscript.css"), os.path.join(SITE, "assets/css/noscript.css"))
# 2) FontAwesome kit from the upstream archive (same files her site serves)
shutil.copy(os.path.join(UP, "css/fontawesome-all.min.css"), os.path.join(SITE, "assets/css/fontawesome-all.min.css"))
for f in os.listdir(os.path.join(UP, "webfonts")):
    if f.endswith((".woff2", ".woff")):
        shutil.copy(os.path.join(UP, "webfonts", f), os.path.join(SITE, "assets/webfonts", f))

# 3) fetch every referenced asset (images, project shots, scripts, logo)
refs = set()
for p in PAGES:
    html = open(os.path.join(SITE, p)).read()
    for m in re.finditer(r'(?:src|href)="([^"]+)"', html):
        u = m.group(1)
        if u.startswith(("http", "#", "mailto:", "//", "data:", "/")) or u.endswith(".html") or "${" in u:
            continue
        refs.add(u)
for js in ("jquery.min.js", "browser.min.js", "breakpoints.min.js", "util.js", "main.js"):
    refs.add("assets/js/" + js)
refs.add("images/logo.svg")

ok = miss = 0
for ref in sorted(refs):
    dest = os.path.join(SITE, ref)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest):
        ok += 1
        continue
    try:
        urllib.request.urlretrieve(LIVE + ref, dest)
        ok += 1
    except Exception:
        miss += 1
        print("missing:", ref)

print(f"mirror: {ok} assets in place, {miss} unreachable (referenced only)")
print("site dir:", SITE)
