# x05 · Objective scoring — frozen method (Layer 1 + Layer 2)

- **Frozen:** 2026-10-09, before the score tables are produced (this file is
  committed first; the results file records its commit).
- **Author:** program runner. Deterministic rules stated below; the few
  judgment items are fixed here, applied uniformly to all conditions, and
  finalized before any per-condition comparison was computed.
- **Sources (read-only):** extraction bundles `x05/run/<id>/extraction/`
  (written by the runner on the sealed checkpoints), the seed workspace
  `x05/run/f3/ws/styles.css`, the seed census exemplars
  (`x05/run/cen/extraction/exemplars.json`). Seals verified 2026-10-09
  (17/17 manifests OK).

## Context fixed by the plan (§5.2, §7)

Primary measure: **convention fidelity of new and modified decisions** —
reproduction of established conventions, scored with the frozen dimension
rubric; departures score as non-reproduction whether or not documented.
Secondary: **cross-component consistency** for new components with no
applicable precedent (the hard-continuity cases), plus a pattern-reuse
observation log. Reference exemplars: frozen per checkpoint — as executed,
every checkpoint inherited the seed exemplar set and froze no new exemplars
(verified across all 17 extraction bundles).

## Layer 1 — role fidelity (primary)

- **Decision points** (per chain, per handoff): elements in
  `diff.element.added ∪ diff.element.changed` that appear under any role in
  that session's `roles.json` (the extraction's frozen ROLE_HOOKS mapping).
  Enumerated point lists:
  - H1 — every chain: `filter-empty` (empty-state)
  - H2 — every chain: `tag-filter` (tags-status), `bookmark-card` (surfaces)
  - H3 — every chain: `command-palette` (surfaces)
  - H4 — a & c: `import-submit` (primary-action), `import-wizard` (surfaces);
    b additionally `command-palette` (surfaces, re-modified)
- **Representative instance:** the element's entry with maximum
  `rect.w·rect.h`; ties → earliest in the capture state order.
- **Applicability exclusion:** a point whose representative instance is
  structurally unstyled (transparent bg AND border none/0 AND radius 0 AND
  shadow none) **or** unrendered in every captured state (all areas 0) is
  recorded as *not measurable at element level* and removed from the
  denominator. (Applies here to `analytics-view`; `mapping-table`.)
- **Dimensions** (§7, as frozen): palette-bg (ΔE2000 ≤ 5, or both
  transparent), radius (absolute diff ≤ 2 px, or both pill), typography
  (generic family class equal), border & treatment (same category — with
  fully transparent borders classified as `none`; correction documented).
  Spacing is tracked informationally only (the frozen helper treats it as
  secondary / non-veto) and does not contribute to the score.
- **Score per point:** 2 = all four pass; 1 = at least half pass (≥ 2);
  0 otherwise. **Fidelity per handoff** = Σscore / (2 × applicable count).
- Reference set: the seed exemplars (frozen at `cen`).

## Layer 2 — cross-component consistency (secondary, hard-continuity)

- **Components:** elements in `diff.element.added` that have a visible
  instance (max area > 0), are not already Layer-1 points, and are not
  structurally unstyled (same exclusion rule as Layer 1). H1–H4 included
  (D3 evaluates the H2–H4 subset).
- **Vocabulary (frozen):** union of (a) the seed's `:root` custom
  properties (colors; `--radius`; shadow), (b) the six seed exemplar
  palette values, (c) every distinct value observed across the seed's
  extracted inventory (bg / fg / border color / radius / font class).
- **Dimensions** (same rubric, vocabulary variant): palette-bg — pass if
  transparent (structural, exempt) or within ΔE2000 ≤ 5 of a vocabulary
  color; typography — family class ∈ vocabulary classes; radius — within
  ±2 px of a vocabulary radius or both pill; border — exempt when none /
  fully transparent, else border color within ΔE ≤ 5 of a vocabulary color.
- **Score per component:** 2 / 1 / 0 as Layer 1. **Consistency per
  handoff** = Σscore / (2 × visible component count).
- **Pattern-reuse observation log (no score):** per component, whether any
  CSS class token is shared with the seed's class vocabulary (classes seen
  on seed testid elements + class selectors in the seed stylesheet);
  reported as reuse share per handoff / chain.

## Gate-evaluation rules (fixed)

- **D1 (primary gate, Layer 1):** per-handoff deltas C − B; pass = "C
  exceeds B in at least 3 of 4 handoffs" AND "median per-handoff delta ≥
  1 / n*", where `n*` = the minimum applicable decision count across chains
  at the median handoff (counts reported; the threshold is fixed as
  1/n* before computing deltas). A handoff with zero applicable points in
  every chain is excluded from "exceeds" counting and from the median
  (recorded). Blind corroboration: from the single-reviewer run — all-items
  median diff +1.0 (at threshold), matched-regions-only +0.5.
- **D2 (secondary):** the same construction for B − A.
- **D3 (secondary):** "favors C" = C strictly highest on the Layer-2 mean
  over H2–H4 AND C ≥ B on at least 2 of those 3 handoffs.
- **D4 (correction burden):** not executable as specified — requires an
  independent reviewer corrections pass that was not resourced; deferred
  and logged (consistent with the single-reviewer deviation).
- **D5 (mechanism, descriptive):** compiled separately from the C-chain
  records/audits; not part of this scoring pass.

## Logged limits / deviations (apply to the report)

1. Element-level instrumentation measures root testid elements; overlay
   roots (`command-palette`, `import-wizard`) are scored as-rendered (scrim
   backgrounds) uniformly across chains — their inner components are
   covered by Layer 2. No exclusion beyond the stated rule.
2. Layer 2's vocabulary comparison is deliberately conservative: a value
   absent from seed tokens/observations scores as a departure, regardless
   of whether it is an improvement.
3. No chain-frozen exemplars exist (executed census grouping); the
   applicable reference set is the seed's throughout — a conservative
   reading that matches the primary question (fidelity to seed
   conventions).
4. Single reviewer / no calibration (see blind-review record); no
   independent corrections; all rules above are deterministic (no random
   seeds, no sampling).
