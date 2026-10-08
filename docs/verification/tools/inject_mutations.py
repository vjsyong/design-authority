#!/usr/bin/env python3
"""inject_mutations — the separate mutation process (verification experiment).

Copies the completed apps, applies the catalogued plausible violations and
control edits (exact-string edits with count assertions), and writes the
SEALED ground truth to mutations/manifest.sealed.json. Prints only counts.

The verifier (tools/da_verify.py) has no code path that reads the manifest;
only tools/mutation_metrics.py opens it, after all verification runs.
"""
import hashlib
import json
import os
import pathlib
import shutil
import time

REPO = "/home/xrim/design-authority"
SRC = {p: os.path.join(REPO, "examples", f"cadence3-{p}") for p in ("wink", "leader", "dominion")}
DST = {p: os.path.join(REPO, "docs", "verification", "mutations", f"mutated-{p}") for p in SRC}


def edit(path, old, new, count=1):
    t = pathlib.Path(path).read_text(encoding="utf-8")
    n = t.count(old)
    assert n == count, f"{path}: expected {count} occurrence(s), found {n}: {old[:80]!r}"
    pathlib.Path(path).write_text(t.replace(old, new), encoding="utf-8")


def append(path, text):
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(text)


def sha(path):
    h = hashlib.sha256()
    h.update(open(path, "rb").read())
    return h.hexdigest()


MANIFEST = []


def record(build, mid, kind, desc, expected, files):
    MANIFEST.append({"id": mid, "build": build, "kind": kind, "desc": desc,
                     "expected_check": expected,
                     "files": [os.path.relpath(f, REPO) for f in files] + [f"sha256:{sha(f)[:16]}" for f in files]})


def inject(pack):
    d = DST[pack]
    css, html, js = (os.path.join(d, x) for x in ("app.css", "index.html", "app.js"))

    if pack == "wink":
        edit(css, "border-radius: 26px;                 /* pill: radius = half height */",
             "border-radius: 8px;")
        record("wink", "W-V1", "violation", "primary button squared (8px)", "wink/action-pill-radius", [css])
        edit(css, "box-shadow: 0 0 0 1px var(--ink-live);   /* 1px ink ring (live-measured) */",
             "box-shadow: none;")
        record("wink", "W-V2", "violation", "ink ring removed", "wink/action-ink-ring", [css])
        append(css, "\n.status.slip { color: #2E8B57; }\n")
        record("wink", "W-V3", "violation", "unsupported green on slipping status", "wink/palette-literals", [css])
        append(css, "\n.toast { position: fixed; right: 18px; top: 18px; z-index: 70; background: #fff;\n"
                    "  color: var(--ink); border-radius: 12px; padding: 12px 16px;\n"
                    "  box-shadow: 0 8px 32px rgba(35,30,21,.2); }\n")
        edit(html, "</body>", '<div class="toast">Logged.</div>\n</body>')
        record("wink", "W-V4", "violation", "floating toast surface added", "wink/no-floating-surfaces", [css, html])
        edit(css, "background: #fff;\n  border-radius: 16px;\n  box-shadow: var(--shadow);      /* borderless vessel, warm-tinted elevation */",
             "background: #fff;\n  border-radius: 2px;\n  border: 1px solid #999999;\n  box-shadow: var(--shadow);")
        record("wink", "W-V5", "violation", "generic sharp bordered card", "wink/card-vessel", [css])
        edit(js, '"Your steadiest seven days yet. Keep it comfortable.";',
             '"Your steadiest stretch in weeks. Keep it comfortable.";')
        record("wink", "W-C1", "benign", "copy edit in week banner", None, [js])
        edit(css, ".streakline { font-size: 13px; color: var(--muted); }\n"
                  ".ritual-actions { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; justify-content: flex-end; }",
             ".ritual-actions { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; justify-content: flex-end; }\n"
             ".streakline { font-size: 13px; color: var(--muted); }")
        record("wink", "W-C2", "benign", "CSS rule reorder (visual no-op)", None, [css])
        edit(css, ".bar-rule { width: 3px; background: var(--ink); border-radius: 999px; }",
             ".bar-rule { width: 4px; background: var(--ink); border-radius: 999px; }")
        record("wink", "W-C3", "undefined-region", "chart rule width 3->4px (composed region)", None, [css])

    if pack == "leader":
        edit(css, ".panel { border-top: 2px solid var(--ink); padding: 16px 0 6px; margin: 22px 0; max-width: 760px; }",
             ".panel { border-top: 2px solid var(--ink); padding: 16px 0 6px; margin: 22px 0; max-width: 760px; border-radius: 8px; box-shadow: 0 8px 24px rgba(17, 17, 17, .12); }")
        record("leader", "L-V1", "violation", "panels rounded + ambient shadow", "leader/no-glow", [css])
        append(css, "\n.mnr-hero { background: #E3120B; color: #fff; padding: 96px 20px; text-align: center; font-size: 20px; }\n")
        edit(html, "</body>", '<div class="wrap"><div class="mnr-hero">Editor\u2019s pick \u2014 the week in numbers</div></div>\n</body>')
        record("leader", "L-V2", "violation", "full-width red hero block", "leader/red-not-surface", [css, html])
        append(css, "\n.btn { border-radius: 999px; }\n")
        record("leader", "L-V3", "violation", "buttons forced to pills", "leader/rounded-interactive", [css])
        edit(css, ".srow { display: flex; align-items: center; gap: 16px; padding: 11px 0; border-bottom: 1px solid var(--l95); flex-wrap: wrap; }",
             ".srow { display: flex; align-items: center; gap: 16px; padding: 11px 0; border-bottom: 1px solid var(--l95); flex-wrap: wrap; box-shadow: 0 2px 8px rgba(0,0,0,.08); }")
        record("leader", "L-V4", "violation", "soft drop shadow on rows", "leader/no-glow", [css])
        edit(css, ".headline { font-family: 'Gelasio', serif; font-size: 32px; font-weight: 700; line-height: 1.15; letter-spacing: -0.3px; }",
             ".headline { font-family: 'Inter', sans-serif; font-size: 20px; font-weight: 600; line-height: 1.2; }")
        record("leader", "L-V5", "violation", "editorial hierarchy de-serifed (DESIGNED MISS — no method)", None, [css])
        edit(html, "</body>", '<div style="padding:8px 0">Great work this week! \U0001F389</div>\n</body>')
        record("leader", "L-V6", "violation", "emoji + exclamation injected into copy", "leader/no-emoji-bang", [html])
        edit(css, ".standfirst { font-family: 'Gelasio', serif; font-size: 16px; color: var(--l20); margin-top: 8px; max-width: 68ch; }",
             ".standfirst { font-family: 'Gelasio', serif; font-size: 16px; color: #008080; margin-top: 8px; max-width: 68ch; }")
        record("leader", "L-V7", "violation", "off-family teal on standfirst", "leader/palette-literals", [css])
        edit(html, "</body>", '<p class="b-note" style="padding:6px 0">Fresh this week: a calmer routine.</p>\n</body>')
        record("leader", "L-C1", "benign", "additive copy sentence", None, [html])
        edit(css, ".readout { font-size: 12.5px; color: var(--l20); }\n.sr-only { position: absolute; width: 1px; height: 1px; clip: rect(0 0 0 0); overflow: hidden; }",
             ".sr-only { position: absolute; width: 1px; height: 1px; clip: rect(0 0 0 0); overflow: hidden; }\n.readout { font-size: 12.5px; color: var(--l20); }")
        record("leader", "L-C2", "benign", "CSS rule reorder (visual no-op)", None, [css])
        edit(css, ".bar { width: min(44px, 72%); background: var(--chicago); }",
             ".bar { width: min(50px, 72%); background: var(--chicago); }")
        record("leader", "L-C3", "undefined-region", "chart bar width detail (pattern leaves width open)", None, [css])
        record("leader", "L-C4", "control-pass", "sanctioned red attention tag must still pass", "leader/tag-attention-red", [])

    if pack == "dominion":
        edit(css, "border-left: 2px solid var(--black); padding: 3px 0 3px 10px;\n       font-size: 15px; color: var(--black); }",
             "border-left: 2px solid var(--red); padding: 3px 0 3px 10px;\n       font-size: 15px; color: var(--red); }")
        record("dominion", "D-V1", "violation", "error recoloured ceremonial red", "dominion/no-red-status", [css])
        edit(html, '<span class="fr">Aujourd\'hui</span>', '<span class="fr"></span>')
        record("dominion", "D-V2", "violation", "FR half of one bilingual pair stripped", "dominion/bilingual-pairing", [html])
        edit(css, "padding: 14px 16px; margin: 16px 0; }",
             "padding: 14px 16px; margin: 16px 0; box-shadow: 0 4px 14px rgba(0, 0, 0, .15); }")
        record("dominion", "D-V3", "violation", "elevation shadow on summary band", "dominion/no-shadows", [css])
        edit(css, "padding: 12px 16px; margin: 14px 0; display: flex; align-items: center;\n          gap: 14px; flex-wrap: wrap; }",
             "padding: 12px 16px; margin: 14px 0; display: flex; align-items: center;\n          gap: 14px; flex-wrap: wrap; border-radius: 8px; }")
        record("dominion", "D-V4", "violation", "notice rounded (8px)", "dominion/radius-discipline", [css])
        edit(html, "</body>", '<img src="data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" width="160" height="90" alt="cover" style="display:block">\n</body>')
        record("dominion", "D-V5", "violation", "decorative image injected", "dominion/no-imagery", [html])
        edit(css, "  outline: 1px solid var(--glow);\n  box-shadow: 0 0 8px rgba(102, 175, 233, .6);",
             "  outline: none;\n  box-shadow: none;")
        record("dominion", "D-V6", "violation", "focus glow removed", "dominion/focus-glow", [css])
        append(css, "\n@keyframes grow { from { width: 0; } to { width: 100%; } }\n.meter i { animation: grow 2s infinite; }\n")
        record("dominion", "D-V7", "violation", "decorative motion added", "dominion/no-keyframes", [css])
        append(css, "\n.st.attn { color: #1B7F4B; }\n")
        record("dominion", "D-V8", "violation", "status chip coloured green", "dominion/status-neutral", [css])
        edit(html, "<p class=\"empty-sentence\">No rituals yet. Add your first ritual to start tracking.</p>",
             "<p class=\"empty-sentence\">Nothing here yet \u2014 add your first ritual to start tracking.</p>")
        record("dominion", "D-C1", "benign", "copy edit in empty state", None, [html])
        edit(css, ".meter { height: 16px; background: var(--greyband); width: 100%; max-width: 520px; }\n.meter i { display: block; height: 100%; width: 0; background: var(--black); }",
             ".meter i { display: block; height: 100%; width: 0; background: var(--black); }\n.meter { height: 16px; background: var(--greyband); width: 100%; max-width: 520px; }")
        record("dominion", "D-C2", "benign", "CSS rule reorder (visual no-op)", None, [css])
        edit(css, ".meter { height: 16px;", ".meter { height: 18px;")
        record("dominion", "D-C3", "undefined-region", "meter height detail (unspecified)", None, [css])
        record("dominion", "D-C4", "control-pass", "masthead ceremony red must still pass", "dominion/masthead-accent", [])


def main():
    os.makedirs(os.path.join(REPO, "docs", "verification", "mutations"), exist_ok=True)
    for pack in SRC:
        if os.path.exists(DST[pack]):
            shutil.rmtree(DST[pack])
        shutil.copytree(SRC[pack], DST[pack])
        inject(pack)
    manifest = {"sealed": time.strftime("%Y-%m-%d %H:%M:%S"),
                "source_rev": "2a913da (v0.2.0)",
                "note": "Ground truth for the mutation experiment. Opened only by mutation_metrics.py after all verifier runs.",
                "mutations": MANIFEST}
    out = os.path.join(REPO, "docs", "verification", "mutations", "manifest.sealed.json")
    with open(out, "w") as fh:
        json.dump(manifest, fh, indent=1, ensure_ascii=False)
    kinds = {}
    for m in MANIFEST:
        kinds[m["kind"]] = kinds.get(m["kind"], 0) + 1
    print(f"sealed manifest: {len(MANIFEST)} mutations across 3 builds -> {kinds}")
    print("mutation process done (specifics withheld by design)")


if __name__ == "__main__":
    main()
