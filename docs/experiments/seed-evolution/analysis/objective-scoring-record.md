# x05 · Objective scoring — record

- **Spec:** `analysis/objective-scoring-spec.md` @ `a763410` — method frozen
  before any scores were computed.
- **Tool:** `tools/x05_score.py` (deterministic; input hashes recorded in
  `objective-scores.json`). Raw outputs: `objective-scores.json` /
  `objective-scores.md`.
- **Scope:** the drift-test chains h1–h4 × a/b/c, scored on the frozen
  extraction bundles (sealed checkpoints; 17/17 seal manifests verified).

## Corrections applied before finalizing (implementation-level, uniform across all conditions)

1. **Border transparency.** Fully transparent borders (`rgba(…,0)` /
   `transparent`) classify as `none`. Rationale: renders as no border and
   matches the cen classifier's own `none` judgments for exactly these
   elements (e.g. `.btn` borders). Without this, every `.btn`-derived
   element would false-fail the border dimension.
2. **Typography parsing.** Composite font strings (`stack | size | weight |
   line-height`) are parsed to the family portion; `sans-serif` stacks are
   no longer mis-read as serif (a quirk of the frozen helper when given the
   composite string). Pre-correction, every scored point failed typography
   uniformly; corrected before results were interpreted.
3. **Unrendered clause enforced.** Decision points with no rendered
   instance in any captured state are excluded as not measurable (spec
   limb). Effect: `import-submit` excluded in all chains — its class-level
   reuse of the seed's `.btn-primary` is a positive qualitative
   observation, not a scored point.

No other changes; the tool's edit history is in git.

## Results

**Layer 1 — role fidelity** (new/changed elements vs seed exemplars; 2/1/0 per point; fidelity = Σ/(2n)):

| chain | H1 | H2 | H3 | H4 |
|---|---|---|---|---|
| A | 1.000 (n=1) | 0.500 (n=1) | 0.000 (n=1) | 0.000 (n=1) |
| B | 1.000 (n=1) | 0.500 (n=1) | 0.000 (n=1) | 0.000 (n=2) |
| C | 1.000 (n=1) | 0.500 (n=1) | 0.000 (n=1) | 0.000 (n=1) |

**Layer 2 — cross-component consistency** (added visible components vs seed vocabulary; same rubric shape):

| chain | H1 | H2 | H3 | H4 | mean H2–H4 | reuse (H1–H4) |
|---|---|---|---|---|---|---|
| A | 1.000 (n=3) | 1.000 (n=2) | 1.000 (n=3) | 0.900 (n=5) | 0.967 | 0.00 / 0.50 / 0.67 / 0.80 |
| B | 1.000 (n=3) | 1.000 (n=5) | 0.833 (n=3) | 0.929 (n=7) | 0.921 | 0.00 / 0.40 / 0.67 / 0.71 |
| C | 1.000 (n=3) | 1.000 (n=5) | 1.000 (n=2) | 0.900 (n=5) | 0.967 | 0.00 / 0.40 / 1.00 / 0.80 |

## Gates (pre-registered)

- **D1 (C > B):** deltas C−B = [0, 0, 0, 0] · exceeds **0/4** · median 0.0 <
  threshold 1.0 → **not met**.
- **D2 (B > A):** deltas B−A = [0, 0, 0, 0] · exceeds **0/4** → **not met**.
- **D3 (cross-component, H2–H4):** C ≥ B on 2/3 handoffs (H4: B 0.929 > C
  0.900) · C not strictly highest on the mean (A ties C at 0.967) →
  **favors-C condition not met**.
- **D4 (correction burden):** not executable as specified — an independent
  reviewer-corrections pass was never resourced. **Deferred, logged** (joins
  the single-reviewer deviation).
- **D5 (mechanism, descriptive):** C-chain enforcement notes pending; not
  part of this scoring pass.

## Observations (descriptive, per the spec's log)

- **Uniform micro-departure:** all three chains render import source paths
  in a **monospace** font family (absent from the seed's vocabulary, which
  contains no mono usage). Identical across conditions — not a
  differentiator.
- **B's single scored departure:** one kbd chip at **5 px** corner radius
  (radius vocabulary allows ±2 px of the 8 px small radius; A's equivalent
  chip used 6 px, C's variant was unrendered). Sub-point scale, single
  element.
- **Overlay roots** (`command-palette`, `import-wizard`) are scored
  as-rendered (scrim backgrounds vs the surface exemplar) and read 0 in
  every condition identically — an instrument-scope artifact, documented.
- **Excluded points** (identical treatment in all chains): `tag-filter`
  (structurally unstyled container pick), `analytics-view` (ditto),
  `mapping-table` (unrendered), `import-submit` (unrendered; class reuse
  noted).

## Reading — objective vs blind

- **Objective half (this record):** no condition separation on any
  measurable, rubric-scored dimension. The seed's six role conventions and
  the style vocabulary survived all chains essentially intact (L1 flat;
  L2 near-ceiling with A = C and B a hair below).
- **Blind half (single reviewer, `blind-review.md`):** C > B > A with A
  collapsing at H2–H3 (2 → 1 of 5); C ≥ B at every handoff; corroboration
  at/below the 1.0-point bar depending on counting read.
- **Why they diverge (attributable, not hand-waved):** the frozen rubric
  scores element-level dimensions (palette/radius/typography/border +
  behavioral) and **excludes composition, layout, density, and the
  presence/absence of surface treatment** — exactly the classes of
  difference the reviewers' gestalt reacts to (e.g. the feature views'
  submitted structures differ markedly across chains while their scored
  style dimensions conform). Element capture is additionally root-level for
  overlays and misses unrendered internals.
- **Net:** the pre-registered primary gate is **not met**; no condition
  effect can be claimed from the objective layers. The blind layer leans
  C > B > A at reduced precision and stands as exploratory evidence only.

## Limits carried to the program report

- Single reviewer; no calibration; no independent corrections (D4 deferred).
- Element-level instrumentation scope as above; component sets differ in
  membership across chains (implementations differ), and Layer-2
  denominators reflect that (normalized per chain).
- All rules deterministic; no sampling; corrections listed above were
  applied uniformly before results were interpreted.
