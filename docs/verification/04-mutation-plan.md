# 04 · Mutation plan — deliberate violations, blind to the verifier

**Purpose:** separate *obedience* from *enforceability*. The clean builds came
from cooperative agents; the mutation experiment poisons copies of the same
apps and asks whether an independent system detects authority violations it
was never told about.

## Protocol (discipline, fixed before injection)

1. **Fresh copies** — `mutations/mutated-{wink,leader,dominion}` are byte
   copies of `examples/cadence3-*` at the baseline revision (post-clean-run).
2. **Separate process** — `tools/inject_mutations.py` applies the catalog below
   (deterministic, exact-string edits with count assertions) and writes
   `mutations/manifest.sealed.json` (id, build, kind, expected check, file
   hashes). The injector prints only counts.
3. **Blind verifier** — `tools/da_verify.py` runs against the poisoned copies
   with *no knowledge of the manifest* (it cannot read it; there is no code
   path). No hints are placed in the apps.
4. **Sealed ground truth** — the manifest is opened only by
   `tools/mutation_metrics.py`, after all verifier runs are complete.
5. **Purity rule for metrics** — TP = expected check observed as VIOLATION;
   FN = expected check not flagged; anything flagged that was not expected is
   reviewed individually (cascade vs false positive) with evidence.

## The catalog

Each build gets violation mutations, benign mutations (must NOT raise flags),
and one "undefined-region" mutation (allowed freedom). Benign/undefined
changes test the false-positive side; violations test recall.

### wink (5 violations · 3 control)

| id | kind | change | expected detection |
|---|---|---|---|
| W-V1 | violation | `.cta` radius 26px → 8px (square pill) | `wink/action-pill-radius` |
| W-V2 | violation | `.cta` ink ring (box-shadow) removed | `wink/action-ink-ring` |
| W-V3 | violation | `.status.slip` coloured unsupported green `#2E8B57` | `wink/palette-literals` |
| W-V4 | violation | floating toast surface added (off-canon, W-15) | `wink/no-floating-surfaces` |
| W-V5 | violation | `.card` radius → 2px + 1px `#999999` border (generic sharp card) | `wink/card-vessel` (+ palette) |
| W-C1 | benign | copy edit in the week banner | none |
| W-C2 | benign | variable rename + CSS rule reorder (visual no-op) | none |
| W-C3 | undefined | `.bar-rule` chart rule 3px → 4px (composed region) | none |

### leader (7 violations · 4 control)

| id | kind | change | expected detection |
|---|---|---|---|
| L-V1 | violation | `.panel` gains radius + ambient shadow (soft elevated panels) | `leader/no-glow` |
| L-V2 | violation | full-width red hero block `#E3120B` added | `leader/red-not-surface` |
| L-V3 | violation | `.btn` forced to pills (radius 999) | `leader/rounded-interactive` |
| L-V4 | violation | `.srow` gains soft drop shadow | `leader/no-glow` |
| L-V5 | violation | `.headline` de-editorialised (sans, smaller) — *designed coverage miss* | none expected (verification gap) |
| L-V6 | violation | "!" + emoji injected into copy | `leader/no-emoji-bang` |
| L-V7 | violation | `.standfirst` recoloured teal `#008080` (off-family) | `leader/palette-literals` |
| L-C1 | benign | copy edit | none |
| L-C2 | benign | rename + reorder | none |
| L-C3 | undefined | chart bar width detail adjusted | none |
| L-C4 | control-red | a *sanctioned* red element (attention tag) kept working; must still pass | `leader/tag-attention-red` stays PASS |

### dominion (8 violations · 4 control)

| id | kind | change | expected detection |
|---|---|---|---|
| D-V1 | violation | `.err` recoloured ceremonial red | `dominion/no-red-status` |
| D-V2 | violation | FR half of one bilingual pair stripped | `dominion/bilingual-pairing` |
| D-V3 | violation | `.summary-band` gains elevation shadow | `dominion/no-shadows` |
| D-V4 | violation | `.notice` rounded (8px) | `dominion/radius-discipline` |
| D-V5 | violation | decorative `<img>` injected | `dominion/no-imagery` |
| D-V6 | violation | focus glow removed from inputs | `dominion/focus-glow` |
| D-V7 | violation | `@keyframes` + meter animation added | `dominion/no-keyframes` |
| D-V8 | violation | status chip coloured green | `dominion/status-neutral` (+ palette) |
| D-C1 | benign | copy edit | none |
| D-C2 | benign | rename + reorder | none |
| D-C3 | undefined | meter height 16px → 18px (unspecified detail) | none |
| D-C4 | control-ceremony | masthead red accent retained; must still pass | `dominion/masthead-accent` stays PASS |

**Expected ceiling:** 20 seeded violations → 19 expected TP (L-V5 is a
*designed* miss, reported honestly), 9 control edits — 0 expected flags.
Anything else flagged gets reviewed; anything flagged that is legitimate
freedom becomes the false-positive record.

## Why these mutations are plausible

Every violation is the kind of drift a careless, fast, mistaken-but-not-
malicious implementer produces: a rounded-button shortcut, a stray shadow, a
"nicer" red for errors, a cover image, one language dropped for space, copy
with enthusiasm. None relies on breaking the app: all mutated builds must
still load and run (verified per-build before verification runs finish).
