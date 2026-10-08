# phantom-audit — build notes (a design-system review of zhenyoyo.github.io)

**What this is.** A four-view review console — Overview · The system · Gaps ·
Adaptations — that audits **zhenyoyo.github.io** (Zhen Wu / Yoyo, HKUST ISD
PhD candidate; projects ILightUUp, Tame, Unlogical Instrument, FAFA, Orchid,
SoundMorphTPU) against a Design Authority derived from the interface system
her site actually deploys: the **HTML5 UP “Phantom” template**, codified as
`packs/phantom` 0.1.0. The console is built in that same system’s language —
the review wears what it reviews.

**Authority.** `packs/phantom` — 19 artifacts · 5 rules · 3 prohibitions ·
3 fallbacks · 1 declined precedent · 2 candidates; goldens **17/17**.
Canon = the template system (upstream sources archived; corroborated by live
computed styles). The deployment’s value edits are recorded as improvisations,
never canon — reframed, where sensible, as pathways (the pink-accent candidate
takes her pink affinity seriously: the template’s own accent is pink #f2849e).
Derivation ledger + deviation inventory (CSS line-by-line, HTML deltas, link
probes): `docs/synthesis/phantom/synthesis-notes.md`, `_raw/` (incl.
`css-diff.txt` — 152 lines, deployment vs upstream).

**Method** (house pattern). 30 review elements resolved against the pack:
**21 RESOLVED · 8 UNDEFINED · 1 FALLBACK** (`_evidence/resolves.jsonl`).
Resolved → built per the cited artifact; UNDEFINED → improvised in character,
marked in the DOM (◌ toggle, bottom-right), and filed: **10 gap records**
(`workspaces/phantom/.design-authority/gaps.jsonl`, copy in
`_evidence/gaps.jsonl`).

**What the review reports** (site under review; nothing on it was modified):
- **27 gaps** in four families — system coherence (the neon re-ink/radius
  flattening/hover-system edits), craft (nested doctype in body, dead
  `.table-wrapper` rule from a comment edit, broken `</S>` title, duplicated
  id=main, double icon kit), content (lorem leftovers, reused generic.html,
  “la la la”, empty captions), patterns (carousel, project-detail, CJK
  typography, current-section mark).
- **6 adaptations** with live demos: the pink-accent **candidate** (AA
  contrast computed in-browser), a marked **project-detail improvisation**, a
  **controlled carousel** (candidate preview), **menu normalisation**
  (before/after), **defect repairs** (before/after sources), and **content
  scaffolding** (before/after copy shapes).

**Console kit = improvisations** (all marked, all filed): stat row, chips,
filter bar, ledger presentation, provenance panel, demo frames, before/after
view, AA check table, anchor nav, marks toggle, JS-only rendering.

**Verification.** `packs/phantom/verification.json` (17 checks) run over this
app with `tools/da_verify.py`: **17/17 PASS** (raw:
`docs/verification/raw/phantom-app/`; published here with covers-hashes as
`_evidence/verification/phantom-verification.json`). Calibration caught two
contract over-assertions corrected against source truth: fields are **flat
(radius 0)**, and table heads are **900-weight but not uppercase** — the pack
now records both faithfully.

**Self-test.** `docs/synthesis/phantom/tools/app_test.py` — **20/20** (cards,
ledger, filters, panel + crosslinks, menu, marks census, carousel, intro
replay, fonts, zero console errors). Screenshots `_evidence/screens/`.

**Credits & licence.** Phantom by HTML5 UP (html5up.net, CCA 3.0 — attribution
kept; the audit’s `assets/css/main.css` is a faithful derivation of the system
with a vendored Source Sans Pro @font-face block; Font Awesome from the
template kit). Source Sans Pro: SIL OFL. The reviewed site remains its
author’s; this review is constructive commentary from public sources, and no
site imagery is redistributed (placeholders are generated).

**Serve.** Review surface: `/audit/phantom/` on the synthesis review app
(tailnet: https://gpu-vm1.bigscale-snapper.ts.net:8420/audit/phantom/), linked
from the `/demo` hub.
