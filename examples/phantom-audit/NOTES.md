# Jennu (phantom-audit v2) — build notes (the deployed language, screenshot-first)

**What this is.** A five-section review console — Overview · The system · The
ledger · Adaptations · Evidence — auditing **zhenyoyo.github.io** (Zhen Wu /
Yoyo; ILightUUp, Tame, FAFA, Unlogical Instrument, Orchid, SoundMorphTPU)
against the **Jennu authority** (`packs/phantom` 0.2.0): the site's *deployed* interface language,
extracted pass-2 from rendered evidence. The console is built in that same
language — it wears what it reviews (pink reading ink, green links on the
dotted blue underline, the blue code chip, the lime rail).

**Why v2 (the redo).** Pass 1 (0.1.0) canonised the *template's* grey ink and
misfiled the deployment's pink type as deviations — while the site that exists
runs pink reading text on six pages. It also extracted from CSS text with
almost no visual evidence, and its local renders were unstyled (an assets-path
bug). Owner verdict: reject. Pass 2: **four domain teams** (colour, typography,
components, layout/motion) extracted from the renderable mirror with
**screenshots as primary evidence** — 64 captures, every one read before a
finding was written, every value tagged `BASE` (template) vs `OVERRIDE`
(deployment). Reports: `docs/synthesis/phantom/domains/a–d`; charter:
`redo-brief.md`.

**Authority (v0.2.0).** 29 artifacts · 8 rules · 2 prohibitions · 4 fallbacks ·
**1 reversal precedent** · **3 candidates**; goldens **21/21**. Key reframe:
the pink/neon ink layer IS the system (`precedent/pink-ink-canonised`;
pass-1's declination formally reversed). Its measured contrast failures
(pink 2.60:1, links 1.32:1, code 1.99:1, per-page h1s 1.92–2.51:1) are recorded
as observations and bounded by `prohibit/unreadable-accent-ink` — extraction,
not correction.

**What the review reports.** 36 ledger items across five families — system
(measured risks), craft (nested doctype mid-body, duplicated `id="main"`,
comment-damaged rules, double icon kit…), assets (six 404 carousel images, two
404 project files, 700–1020px mobile overflow), content (lorem survivors, alt
text, favicon/OG, "la la la"), patterns (carousel policy, project-detail
composition, CJK stack, current-section mark).

**Adaptations (6, all with live demos).** Pink-ink AA dossier (ratios computed
in-browser); mixed-script fallback demonstration (圳 under the deployed stack
vs a proposed one); carousel repair dossier (controlled demo — no autoplay);
project-gallery responsive fix (before/after); marked project-detail
improvisation; handbook normalisation (menu/wordmark/copy deltas).

**Evidence view.** Fourteen curated screenshots ship inside the app
(`assets/evidence/`, resized, captioned, tag-chipped) — the same captures the
findings cite. The full 64-shot set lives in
`docs/synthesis/phantom/evidence/screens/`.

**Console kit = improvisations** (all marked; console-kit gap records carried
from pass 1 in the review workspace, copy in `_evidence/gaps.jsonl`): stat row,
chips, filters, ledger chrome, provenance panel, override toggle ("view as
project page" applies the deployment's own black-body override to this app —
the P-R7 demo), marks layer (◌ bottom-right), evidence gallery, JS-only
rendering.

**Method artefacts.** 30 elements resolved against the pack: **21 RESOLVED ·
7 UNDEFINED · 1 FALLBACK · 1 CONFLICT** (`_evidence/resolves.jsonl`).

**Verification.** `packs/phantom/verification.json` v0.2 (15 checks, rewritten
for the deployed language) → `da_verify`: **15/15 PASS** (raw:
`docs/verification/raw/phantom-app/`; published here with covers-hashes as
`_evidence/verification/phantom-verification.json`). Self-test: **29/29**
(`docs/synthesis/phantom/tools/app_test.py`) — including the deployed tokens
asserted on this app itself (pink ink, green links, lime menu, red checks) and
the override toggle. The verifier caught one real slip during calibration (an
improvisation demo used 0.2em tracking; corrected to the system's 0.35em caps).

**Credits & licence.** Phantom by HTML5 UP (html5up.net, CCA 3.0 — attribution
kept; `assets/css/main.css` is a verbatim derivation of the deployment's
stylesheet with the Google-Fonts import vectorised to vendored @font-face).
Source Sans Pro: SIL OFL. The reviewed site remains its author's; this review
is constructive commentary from public sources; no site imagery is
redistributed beyond the captured evidence shots.

**Serve.** `/designAuthority/jenmu/` on the synthesis review app (tailnet:
https://gpu-vm1.bigscale-snapper.ts.net:8420/designAuthority/jenmu/; public once the
tunnel lands: https://audit.seanyong.xyz/designAuthority/jenmu). The host serves
`X-Robots-Tag: noindex` on everything and a disallow-all robots.txt. Named **Jennu**
2026-10-08.
