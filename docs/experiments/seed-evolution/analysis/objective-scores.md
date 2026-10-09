# x05 · Objective scores (Layer 1 + Layer 2)

Generated 2026-10-09T08:40:15+00:00 · spec commit a763410 · inputs: schedule `aaeee2422a2a…`, styles.css `aac8a6153263…`, exemplars `2e32e5fdc9a4…`

## Layer 1 — role fidelity

| chain | H1 | H2 | H3 | H4 |
|---|---|---|---|---|
| A | 1.000 (1) | 0.500 (1) | 0.000 (1) | 0.000 (1) |
| B | 1.000 (1) | 0.500 (1) | 0.000 (1) | 0.000 (2) |
| C | 1.000 (1) | 0.500 (1) | 0.000 (1) | 0.000 (1) |

Per-point detail (score / dims shown compactly):
- A H1: filter-empty (empty-state, filtered-none) → 2 [+palette +radius +typography +border]
- A H2: bookmark-card (surfaces, populated) → 1 [+palette +radius +typography -border]
- A H2: tag-filter → EXCLUDED (not-measurable (structurally unstyled))
- A H3: command-palette (surfaces, palette) → 0 [-palette -radius +typography -border]
- A H4: import-wizard (surfaces, wizard-1) → 0 [-palette -radius +typography -border]
- A H4: import-submit → EXCLUDED (unrendered in all captured states)
- B H1: filter-empty (empty-state, filtered-none) → 2 [+palette +radius +typography +border]
- B H2: bookmark-card (surfaces, populated) → 1 [+palette +radius +typography -border]
- B H2: tag-filter → EXCLUDED (not-measurable (structurally unstyled))
- B H3: command-palette (surfaces, palette) → 0 [-palette -radius +typography -border]
- B H4: import-wizard (surfaces, wizard-1) → 0 [-palette -radius +typography -border]
- B H4: command-palette (surfaces, palette) → 0 [-palette -radius +typography -border]
- B H4: import-submit → EXCLUDED (unrendered in all captured states)
- C H1: filter-empty (empty-state, filtered-none) → 2 [+palette +radius +typography +border]
- C H2: bookmark-card (surfaces, populated) → 1 [+palette +radius +typography -border]
- C H2: tag-filter → EXCLUDED (not-measurable (structurally unstyled))
- C H3: command-palette (surfaces, palette) → 0 [-palette -radius +typography -border]
- C H4: import-wizard (surfaces, wizard-1) → 0 [-palette -radius +typography -border]
- C H4: import-submit → EXCLUDED (unrendered in all captured states)

## Layer 2 — cross-component consistency

| chain | H1 | H2 | H3 | H4 |
|---|---|---|---|---|
| A | 1.000 (3) | 1.000 (2) | 1.000 (3) | 0.900 (5) |
| B | 1.000 (3) | 1.000 (5) | 0.833 (3) | 0.929 (7) |
| C | 1.000 (3) | 1.000 (5) | 1.000 (2) | 0.900 (5) |

| chain | reuse H1 | reuse H2 | reuse H3 | reuse H4 |
|---|---|---|---|---|
| A | 0.00 | 0.50 | 0.67 | 0.80 |
| B | 0.00 | 0.40 | 0.67 | 0.71 |
| C | 0.00 | 0.40 | 1.00 | 0.80 |

## Gates

- D1 (C>B): deltas {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0} · exceeds 0/4 · median 0.0 · threshold 1.0 · PASS=False
- D2 (B>A): deltas {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0} · exceeds 0/4 · median 0.0 · threshold 1.0 · PASS=False
- D3 (Layer 2, H2–H4): means {'a': 0.9667, 'b': 0.9206, 'c': 0.9667} · C≥B handoffs 2/3 · favors C=False

Per-layer per-handoff component tables are in objective-scores.json.
