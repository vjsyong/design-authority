# Phase 3 — the three candidate authorities

Compiled from Gate-2-accepted decisions by `docs/synthesis/tools/compile_pack.py`.
Pack format: the kernel's standard JSON directory; kernel unchanged (same code that
serves triage, orbit and indaba).

## Contents

| pack | source | artifacts | rules | prohibitions | fallbacks | recipes | golden |
|---|---|---|---|---|---|---|---|
| `packs/wink` | Mailchimp brand + live product | 12 (6 component, 4 guideline, 2 token-set) | 2 | 2 | 2 | 0 | 9/9 |
| `packs/leader` | Marber (Economist) + live product | 12 (5 component, 5 guideline, 2 token-set) | 2 | 5 | 3 | 0 | 10/10 |
| `packs/dominion` | Canada FIP + live Canada.ca web layer | 10 (5 component, 3 guideline, 2 token-set) | 2 | 4 | 2 | 1 | 10/10 |

Signature content (what makes each one itself):

- **wink** — pill actions with the 1px ink ring and the *measured* hover (lift
  −4.875px + hard `0 4.875px 0 0` shadow, zero blur); warm ink palette; chevron nav
  with grey hover fills; Fraunces/Inter registers.
- **leader** — navy Chicago-45 actions (radius ~8), Chicago blues as the interactive
  layer, red as brand punctuation; rules-and-hairline surfaces (no washes); serif
  text with sans apparatus; no-border-highlight fields.
- **dominion** — slate `#26374A` actions and fields (radius 4), the live blue focus
  glow (`1px #66AFE9 + 8px rgba(102,175,233,.6)`), ceremonial red out of all
  status/action roles, bilingual EN|FR pairing guidance, retire-with-confirmation
  recipe.

## Deliberate gaps (undefined at review, shipped as gaps — not glossed)

- wink: status system, motion, notices/toasts, destructive/dialog, progress,
  empty states, responsive detail, focus treatment (12 undefined items).
- leader: motifs detail, selection, status tags, destructive/dialog, progress
  copy, empty, responsive, imagery, focus ring detail (11 undefined items).
- dominion: shape prohibitions (no explicit square ban), status words, notices,
  empty, repeated-content detail, overlays/motion (8 undefined items).

## Are they substantially different? (divergence probes, real outputs)

Same ask resolved against each authority:

| ask | wink | leader | dominion |
|---|---|---|---|
| "make the buttons square" | **CONFLICT** square-buttons | **CONFLICT** square-interactive | UNDEFINED (not prohibited) |
| "add a soft blue glow to the button" | UNDEFINED | **CONFLICT** ambient-glow | **RESOLVED** field (glow is its focus language) |
| "use rounded pills for the primary action" | RESOLVED action-pill | RESOLVED action (navy) | RESOLVED action (slate) |
| "add a photograph to the empty state" | UNDEFINED | UNDEFINED | **CONFLICT** imagery-pictograms |

Four asks, three authorities, three genuinely different stances — no shared
colours, shapes or signals across the pack contents (audit: zero cross-source
references; source names appear only in each pack's own provenance fields).

## Verification

- Per-pack golden: 9/9, 10/10, 10/10 (29 cases, 100%) — positive resolves,
  conflicts, fallbacks, deliberate UNDEFINEDs.
- Standing battery green and unchanged: pack drift ✓ · kernel tests 10/10 ·
  triage golden 19/19 · indaba golden 10/10 · MCP smoke 17/17.
- Traceability: every artifact/rules/fallback carries `compiled_from` decision IDs;
  the compiler asserts Gate-2 acceptance before emitting.

## Limitations (held honestly)

- n=1 reviewer, n=3 sources; small packs are *by design* (the experiment tests the
  method, not catalog size).
- No lint validators authored for the three (capabilities.validators = []); lint
  is the natural next hardening step per pack.
- The three candidates have passed kernel goldens but have **not** been through the
  build-harness benchmark (the orbit/indaba-style agent build). That run is the
  obvious next experiment if wanted.
- The compile mapping tables remain authored judgment (see 10-synthesis-process.md,
  "what generalizes vs. what stays artisan").

## Files

- Compiler: `docs/synthesis/tools/compile_pack.py`
- Packs: `packs/{wink,leader,dominion}/`
- Source evidence + decisions: `docs/synthesis/{wink,leader,dominion}/`
- Review instrument + verdict data: `docs/synthesis/review-app/`
