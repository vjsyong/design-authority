#!/usr/bin/env python3
"""build_app_css_v2 — derive examples/phantom-audit/assets/css/main.css from the
DEPLOYED stylesheet (_raw/site/assets/css/main.css), so the review app wears the
site's actual language (pink ink, neon links, blue code, lime menu).

Only two edits to the deployed source:
  1. the Google-Fonts @import is replaced by vendored @font-face blocks
     (same faces: SSP 300/700/900, latin + latin-ext, served from assets/fonts/)
  2. nothing else — the deployment's overrides are the point this time.
"""
import os
import re

REPO = "/home/xrim/design-authority"
SRC = os.path.join(REPO, "docs/synthesis/phantom/_raw/site/assets/css/main.css")
DST = os.path.join(REPO, "examples/phantom-audit/assets/css/main.css")

t = open(SRC).read()
head = "\n".join(t.splitlines()[:4])
print("deployed css head:\n" + head + "\n---")

# drop the Google Fonts import (any line), keep the FontAwesome import
t = re.sub(r'@import\s+url\([^)]*fonts\.googleapis\.com[^)]*\);?\s*\n', '', t)

# vendored faces (skip any that are missing on disk)
FACES = []
FONTS = os.path.join(REPO, "examples/phantom-audit/assets/fonts")
for w in ("300", "400", "700", "900"):
    for sub in ("latin", "latin-ext"):
        f = f"source-sans-pro-{w}-{sub}.woff2"
        if os.path.exists(os.path.join(FONTS, f)):
            FACES.append(
                "@font-face {\n"
                f"\tfont-family: 'Source Sans Pro';\n\tfont-style: normal;\n\tfont-weight: {w};\n"
                "\tfont-display: swap;\n"
                f"\tsrc: url('../fonts/{f}') format('woff2');\n}}")
faces = "\n".join(FACES)

# insert faces right after the leading @import block (imports must stay first)
lines = t.splitlines(keepends=True)
i = 0
while i < len(lines) and (lines[i].strip().startswith("@import") or lines[i].strip().startswith("@charset")
                          or lines[i].strip() == ""):
    i += 1
out = "".join(lines[:i]) + "\n/* vendored Source Sans Pro (was fonts.googleapis.com import) */\n" + faces + "\n\n" + "".join(lines[i:])

header = "/* phantom-audit — derived from the DEPLOYED main.css of zhenyoyo.github.io\n   (HTML5 UP Phantom deployment; template CCA 3.0). Google-Fonts import vectorised\n   to vendored @font-face; no other change. */\n"
open(DST, "w").write(header + out)
print(f"wrote {DST} ({len(out)} bytes, {len(FACES)} faces inserted)")
print("contains pink ink:", "#ff6bbc" in out, "| green links:", "#6bff2c" in out, "| lime menu:", "#3ef900" in out)
