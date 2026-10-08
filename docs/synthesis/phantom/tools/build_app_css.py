#!/usr/bin/env python3
"""build_app_css — derive phantom-audit/assets/css/main.css from the upstream system.

Faithful derivation: the audit app wears the phantom system; only the Google
Fonts import is swapped for a vendored @font-face block. All NON-system styling
the app needs lives in assets/css/console.css (marked as improvisation).
"""
import os
import re

REPO = "/home/xrim/design-authority"
src = os.path.join(REPO, "docs", "synthesis", "phantom", "_raw", "upstream", "assets", "css", "main.css")
dst = os.path.join(REPO, "examples", "phantom-audit", "assets", "css", "main.css")

t = open(src).read()
# drop the Google Fonts import (offline build: vendored woff2 instead)
t = re.sub(r'@import url\("https://fonts\.googleapis\.com[^"\)]+"\);\s*', "", t)

face = """/* Vendored locally (offline build). Source Sans Pro, SIL OFL. */
@font-face { font-family: 'Source Sans Pro'; font-style: normal; font-weight: 300;
  src: url('../fonts/source-sans-pro-300-latin-ext.woff2') format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }
@font-face { font-family: 'Source Sans Pro'; font-style: normal; font-weight: 300;
  src: url('../fonts/source-sans-pro-300-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }
@font-face { font-family: 'Source Sans Pro'; font-style: normal; font-weight: 400;
  src: url('../fonts/source-sans-pro-400-latin-ext.woff2') format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }
@font-face { font-family: 'Source Sans Pro'; font-style: normal; font-weight: 400;
  src: url('../fonts/source-sans-pro-400-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }
@font-face { font-family: 'Source Sans Pro'; font-style: normal; font-weight: 700;
  src: url('../fonts/source-sans-pro-700-latin-ext.woff2') format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }
@font-face { font-family: 'Source Sans Pro'; font-style: normal; font-weight: 700;
  src: url('../fonts/source-sans-pro-700-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }
@font-face { font-family: 'Source Sans Pro'; font-style: normal; font-weight: 900;
  src: url('../fonts/source-sans-pro-900-latin-ext.woff2') format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }
@font-face { font-family: 'Source Sans Pro'; font-style: normal; font-weight: 900;
  src: url('../fonts/source-sans-pro-900-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }

"""
open(dst, "w").write(face + t)
print("derived", os.path.relpath(dst, REPO), os.path.getsize(dst), "bytes (font-face + upstream system, Google import removed)")
