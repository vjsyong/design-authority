# 05 · Mutation results — detection performance

Protocol recap (fixed in `04`): the injector is a **separate process**
(`tools/inject_mutations.py`); it copied the three completed apps, applied the
catalogue, and sealed 31 entries in `mutations/manifest.sealed.json` printing
only counts. `tools/da_verify.py` ran against the poisoned copies with **no
code path that could read the manifest**. Only after all three runs did
`tools/mutation_metrics.py` open the ground truth. Raw outputs:
`raw/mutant-{wink,leader,dominion}/raw.json`.

## Detection matrix

**wink — 5 seeded violations, 5 detected (all error-severity)**

| seed | expected check | verifier | evidence |
|---|---|---|---|
| W-V1 | wink/action-pill-radius | **VIOLATION** | `border-radius: 8px` (square primary button) |
| W-V2 | wink/action-ink-ring | **VIOLATION** | `box-shadow: none` (ring removed) |
| W-V3 | wink/palette-literals | **VIOLATION** | `#2e8b57` in `.status.slip` (unsupported green) |
| W-V4 | wink/no-floating-surfaces | **VIOLATION** | floating `.toast` surface present |
| W-V5 | wink/card-vessel | **VIOLATION** | `border-radius: 2px; border-top-width: 1px` |

**leader — 7 seeded violations, 6 expected, 6 detected** (1 designed miss)

| seed | expected check | verifier | evidence |
|---|---|---|---|
| L-V1 | leader/no-glow | **VIOLATION** | `box-shadow: 0 8px 24px rgba(17,17,17,.12)` on `.panel` |
| L-V2 | leader/red-not-surface | **VIOLATION** | red block `rgb(227,18,11)` over the area bound |
| L-V3 | leader/rounded-interactive | **VIOLATION** | `border-radius: 999px` on `.btn` |
| L-V4 | leader/no-glow | **VIOLATION** | second shadow (`rgba(0,0,0,.08)` on rows) |
| L-V5 | *(none — designed miss)* | not flagged | `.headline` de-serifed; no method exists (declared in `04`, classified in `07`) |
| L-V6 | leader/no-emoji-bang | **VIOLATION** | `bang=True emoji=['🎉']` |
| L-V7 | leader/palette-literals | **VIOLATION** | `#008080` teal on `.standfirst` |

**dominion — 8 seeded violations, 8 detected**

| seed | expected check | verifier | evidence |
|---|---|---|---|
| D-V1 | dominion/no-red-status | **VIOLATION** | red in `.err` colour + left rule |
| D-V2 | dominion/bilingual-pairing | **VIOLATION** | `4/5 pairs; bad: ['Today']` |
| D-V3 | dominion/no-shadows | **VIOLATION** | `box-shadow: 0 4px 14px rgba(0,0,0,.15)` |
| D-V4 | dominion/radius-discipline | **VIOLATION** | `border-radius: 8px` outside the 0/4px set |
| D-V5 | dominion/no-imagery | **VIOLATION** | injected `<img>` found |
| D-V6 | dominion/focus-glow | **VIOLATION** | focus signal lost `102, 175, 233` |
| D-V7 | dominion/no-keyframes | **VIOLATION** | `@keyframes grow` + meter animation |
| D-V8 | dominion/status-neutral (+cascade) | **VIOLATION** | green status chip; also flagged by the palette audit (corroboration, see below) |

## Metrics

| metric | value |
|---|---|
| True positives (detectable seeds) | **19 / 19 — recall 100%** |
| False negatives | **0** (+1 *designed* miss: L-V5, no method — declared before injection) |
| False positives | **0** — every flagged check is attributable to a seeded change |
| Cascades (corroborating double-detections) | 1 (D-V8: status scan + palette audit) |
| Control edits & undefined-region changes (12) | **0 flags** — no false rejection of legitimate freedom |
| Sanctioned-red controls | both kept PASS on poisoned builds (tag attention, masthead accent) |
| Screenshots captured per violation | 19 (`raw/mutant-*/screens/`) |

Per verification mode, detection on its seeds: COMPUTED_STYLE 4/4 · STATIC 7/7
· INTERACTION 5/5 · DOM 3/3.

## Findings from the mutation phase

1. **The toast check earned its keep.** W-V4's toast is palette-legal and
   textually benign — only the floating-surface scan could catch it; it did.
2. **Two independent methods agreed** on D-V8 (scan + literal audit) — the
   contract's redundancy is a feature, not noise; it is reported as a
   *cascade*, not a duplicate violation.
3. **The blind verifier found every detectable violation without being told
   anything.** No hints, no markers, no manifest access — detection came from
   files, DOM, computed style, and behaviour.
4. **The designed miss behaved exactly as declared.** The hierarchy
   de-serifing (L-V5) is real drift that this system cannot see; it stands as
   the sharpest illustration of the coverage boundary (see `06`, `07`).
5. **Zero false positives** across 12 legitimate changes — including both
   edits *inside* explicitly undefined regions — is the strongest evidence
   that the contracts discriminate between authority and freedom.

## Integrity ledger

- `grep -c manifest tools/da_verify.py` → 0 (verifier cannot read the ground
  truth; no hints present in any mutated app).
- Verifier raw outputs predate the metrics step; the sealed manifest was opened
  by `tools/mutation_metrics.py` only after all runs (and the run set was
  reproduced identically after a benign verifier field addition).
- Residual limitation (stated, not hidden): the same designer authored the
  mutation catalogue and the contracts. Mitigations: sealed manifest, blind
  run, exact-string assertions in the injector, post-hoc metrics. A stronger
  variant for a future pass: an independent agent authors the mutations.
