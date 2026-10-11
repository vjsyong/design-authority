# 12 · Static vs enforced vs governed — three-arm results (R1–R3)

Pre-registration: `docs/experiments/11-static-enforced-governed.md` (frozen
2026-10-11; run log there). Raw evidence: `~/p4-maint/run/<id>/` (45
sessions, seals verified), `validation-external.json`, `checkpoint-r*.json`,
captures under `run/<id>/capture/`.

## Run summary

45 sessions (3 seeds × 3 arms × H1–H4 + H5), 14:52–22:43 UTC. All seals
verified. One session capped: `r3-b-h5` (hit the 20 M token cap during its
self-directed guidance sweep — see H5 below).

| arm | H1–H4 tokens | H1–H4 wall | H5 tokens | H5 wall | enforcement usage |
|---|---|---|---|---|---|
| A static | 92.8 M | 7,061 s | 7.0 M | 1,362 s | none |
| B enforced | 99.7 M (+7%) | 7,235 s | 43.0 M* | 2,438 s | `check-design` 3–23×/session |
| C governed | 128.8 M (+39% vs A, +29% vs B) | 8,347 s | 20.7 M | 1,604 s | 23–65 wrapper calls/session |

\* B's H5 states were already at 100 under the final validator, so its H5
spend is a voluntary guidance-application sweep, NOT remediation — excluded
from the repair economics below.

## Primary measure — external validator, constant final pack (p4-da-4)

Every session-end state of every arm, validated externally with the complete
guidance:

| state | A (static) | B (enforced) | C (governed) |
|---|---|---|---|
| r1 h1–h4 | 98 → 72 → 70 → 70 (e0–3, w1–3) | **100 ×4** | 98 ×4 (w1) |
| r2 h1–h4 | 98 → 90 → 90 → 88 (e0–1, w1–2) | **100 ×4** | 90 ×4 (w5) |
| r3 h1–h4 | 96 → 96 → 94 → 92 (w2–4) | **100 ×4** | 98 ×4 (w1) |
| all h5 (post-repair) | 100 | 100 | 100 |

- **A decayed, in the target class.** Its errors are raw colour literals
  (B001: `rgba(37,99,235,0.12)`, `rgba(20,24,33,0.18)`) plus accumulating
  duplicate declaration blocks (B004). 70/88/92 at h4 across seeds.
- **B was flawless:** zero findings at every one of its 15 handoff states,
  all three seeds — enforcement (validate-and-repair at each session end)
  held the surface clean continuously.
- **C carried residuals:** 1 B004 warning in r1/r3, 5 in r2, through every
  handoff — documented-not-repaired under the protocol's repair-or-file
  stance. (One of them, `.add-form-error`/`.wizard-error`, is inherited from
  the seed's baseline; B cleaned it, C and A kept it.)

## Claims, at confidence levels

1. **Enforcement alone produces continuous conformance** — strong
   (3 seeds × 15 states; B never left a finding at any handoff, at ≈ +7%
   cost over static).
2. **Governance added no conformance beyond enforcement at this scale** —
   strong within this run, with an important honest caveat: the endpoints
   optimize different objectives by construction — B's mandate is "reach
   zero findings"; C's protocol is "repair-or-file", which is itself a
   governance feature (documented tolerances). C's residuals are partly the
   design, not a failure. That is exactly the distinction the experiment
   asked to expose.
3. **Static drift was cheap to repair at this scale** — the H5 repair of
   A's accumulated drift cost 7.0 M tokens total (≈2.3 M per chain) versus
   the +6.9 M/chain-set that prevention (B) cost during H1–H4. At four
   handoffs the deferred bill ≈ the preventive premium; what prevention
   additionally bought is that no intermediate consumer ever saw a dirty
   state (A's drift was visible at hands 2–4 of every seed).
4. **Kill criterion not hit** — arms are distinguishable.

## The blind round (held-out, live)

The instrument serves 14 comparisons (5 pre-scored calibration + 9 live):
per arm, the h2 editor rework vs h1, the h3 list state vs h1, and the h5
post-repair state vs h1 — one narrow question each, arm mapping sealed
server-side (`~/p4-maint/analysis/blindset-key.json`). The held-out question
this answers: does the repaired-to-pass lineage (A) look as internally
consistent as the never-drifted (B) and governed (C) ones — i.e. does
"repaired to zero findings" diverge visibly where the linter is coarse.
Note: arm A's h5 render is pixel-identical to its h3 (its repair changed
CSS tokens to visually-equal values), so the set carries an accidental
test-retest pair for A.

## Limits

- One chain per arm per seed (3 seeds); single pinned model.
- The conformance metric structurally favors B's mandate over C's
  repair-or-file stance (stated above; both are the conditions as designed).
- B's H5 spend is voluntary sweep, not repair; B's deferred bill is 0 by
  construction.
- Captured fixture states do not surface h4's features (empty favourites,
  absent import conflicts).
- Blind round covers R1 only; calibration spread is 1–4 on the 1–5 scale.

## Confirmed confound (owner review, 2026-10-11)

The owner's reading: "All of them basically look the same bar some minor
drift… this look was the default for this model; there's a confound that it
is simply resorting to its own nature." Verified against the data:

- **The design system under test WAS the model's default palette.** The
  seed's token set is Tailwind's defaults with names on them:
  `--color-accent: #2563eb` (blue-600), `--color-muted: #6b7280` (gray-500),
  `--color-danger: #b91c1c` (red-700), `--color-accent-hover: #1d4ed8`
  (blue-700). No distinctive design opinion was ever at stake, so
  "consistency" required no arm to overcome any model nature — and the
  code-imitation signal (every session reads the existing CSS) was
  available to all arms equally.
- **The measured arm differences are mechanism-level, not visual.** A's
  B001 "raw colour" findings are `rgba(37, 99, 235, 0.12)` — the same
  accent blue at 12% opacity written as a literal instead of a token.
  The outcome variable was HOW values got written, not WHICH values; that
  is invisible on a screen and therefore structurally unmeasurable by the
  blind instrument. The reviewer's "requires a lot of interpretation" is
  the correct read of the instrument, not a reviewer failure.

Consequences for interpretation:

- The three-arm result stands **as a process finding** (enforcement held
  token discipline across handoffs where static did not) and is reframed
  accordingly. It is NOT evidence about visible design consistency, and
  the blind round as served cannot provide that evidence — its face
  validity fails for this subject.
- Attribution to the Authority (as opposed to model nature) is
  overdetermined on the visual plane for this lineage. The de-confounded
  version needs: (1) a deliberately **counter-default** contract (falling
  back to the model's palette becomes the measurable violation, and the
  lint can ban default-palette values explicitly); (2) a no-contract
  control arm to estimate model nature directly; (3) blind items only
  where counter-default stakes are visible, plus a "reversion to default"
  metric (default-palette / standard-radius / system-font appearances
  over handoffs); (4) optionally a second model to break single-model
  attribution. Recommended as the next pre-registration (docs/13) on the
  owner's go.
