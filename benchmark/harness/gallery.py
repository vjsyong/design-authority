#!/usr/bin/env python3
"""Build a blind review gallery from benchmark run captures (D5).

    python3 gallery.py --runs ../runs --out /tmp/da-gallery [--seed 7]

For every run with a capture dir, this copies a fixed set of screenshots into
an anonymised gallery directory (random 4-letter codes), writes an index.html
to browse them, a questionnaire template, and `_mapping.json` (SEALED — do not
open or share until the human review is complete).
"""
import argparse
import json
import os
import random
import shutil

ROUTES = [("dashboard", "desktop"), ("dashboard", "phone"),
          ("requests", "desktop"), ("requests", "phone"),
          ("request-detail", "desktop"), ("request-detail", "phone"),
          ("jobs-running", "desktop"), ("jobs", "phone"),
          ("settings", "desktop"),
          ("dashboard-error", "desktop"), ("requests-empty", "desktop"),
          ("dashboard-job-running", "phone")]

INDEX_HTML = """<!doctype html><meta charset="utf-8">
<title>Procura review gallery</title>
<style>
body{font-family:system-ui;margin:24px;background:#f5f5f5}
h1{font-size:20px} section{background:#fff;border:1px solid #ddd;margin:16px 0;padding:12px}
.imgs{display:flex;flex-wrap:wrap;gap:12px}
figure{margin:0;max-width:440px} img{width:100%;border:1px solid #ccc}
figcaption{font-size:12px;color:#666}
</style>
<h1>Procura review gallery — builds</h1>
<p>Each build is labelled with a code only. Review each build independently and
fill in <code>questionnaire.md</code> per code. Do not try to guess conditions.</p>
{body}
"""

QUESTIONNAIRE = """# Procura blind review — questionnaire

For each build code below, answer (1 = poor, 5 = excellent) plus free text:

1. **Consistency** — do the pages feel like one product?
2. **Coherence** — do the pieces hang together as a system (navigation, feedback, states)?
3. **Obvious design mistakes** — anything visibly broken or wrong?
4. **Confidence a new page could be added consistently** — how easy would it be
   to extend this UI without breaking its look?
5. **Manual cleanup needed** — how much would a designer have to fix before
   shipping?

{codes}

Notes / anything else:
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs"))
    ap.add_argument("--out", default="/tmp/da-gallery")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    runs = []
    for name in sorted(os.listdir(args.runs)):
        cap = os.path.join(args.runs, name, "capture", "screens")
        if os.path.isdir(cap):
            runs.append((name, cap))
    if not runs:
        raise SystemExit("no runs with captures found under %s" % args.runs)

    alphabet = "BCDFGHJKLMNPQRSTVWXZ"
    codes = set()
    while len(codes) < len(runs):
        codes.add("".join(rng.choice(alphabet) for _ in range(4)))
    codes = sorted(codes)
    rng.shuffle(codes)

    if os.path.exists(args.out):
        shutil.rmtree(args.out)
    os.makedirs(args.out)

    mapping = {}
    sections = []
    for (run, cap), code in zip(runs, codes):
        mapping[code] = run
        dest = os.path.join(args.out, code)
        os.makedirs(dest)
        figs = []
        for route, viewport in ROUTES:
            src = os.path.join(cap, "%s-%s.png" % (route, viewport))
            if not os.path.exists(src):
                continue
            fname = "%s-%s.png" % (route, viewport)
            shutil.copy2(src, os.path.join(dest, fname))
            figs.append('<figure><img src="%s/%s"><figcaption>%s · %s</figcaption></figure>'
                        % (code, fname, route, viewport))
        sections.append('<section><h2>Build %s</h2><div class="imgs">%s</div></section>'
                        % (code, "".join(figs)))

    with open(os.path.join(args.out, "index.html"), "w") as fh:
        fh.write(INDEX_HTML.format(body="\n".join(sections)))
    with open(os.path.join(args.out, "questionnaire.md"), "w") as fh:
        fh.write(QUESTIONNAIRE.format(
            codes="\n".join("## Build %s\n- Consistency:\n- Coherence:\n- Mistakes:\n"
                            "- Confidence to extend:\n- Cleanup needed:\n" % c
                            for c in codes)))
    with open(os.path.join(args.out, "_mapping.json"), "w") as fh:
        json.dump({"_sealed": "Do not open until the human review is complete.",
                   "mapping": mapping}, fh, indent=1)
    print("gallery: %d builds, codes %s -> %s" % (len(runs), ",".join(codes), args.out))


if __name__ == "__main__":
    main()
