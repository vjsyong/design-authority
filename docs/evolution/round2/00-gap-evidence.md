# Round 2 · 00 — Gap evidence (disputes and codification failures)

**Date:** 2026-10-08. **Source of evidence:** the design-authority side of the
project, not a benchmark generation: the disputed-resolution fixture set
(`docs/experiments/disputes/`, four records seeded from experiments 01 and
03), the `.skip` gap filed during the Duty build (experiment 03,
`gap/20261008-124813-ac670b`), the `.status-chip` finding from experiment 02
(part B), and the framing result of experiment 04 (the agent-level A/B):
the binding failures were **codification failures**, not retrieval ones.

Processed against the **evolution line** (`packs/triage-evolution`,
0.13.0-experiment @ 32e680b), which is the governed improvement path. The
pinned authority (`packs/triage`, 0.12.1) stays frozen; its standing
disputes remain pinned by `dispute-replay --expect-standing 4`.

## Consolidated needs

### N-1 · Skip link (dispute + codification)
- `dispute/20261008-134355-5a90bd`: "a skip link to jump past the
  navigation" resolved to `component/nav-item` (a false RESOLVED; caught by
  the Duty agent, which used the shipped `.skip` class and filed
  `gap/20261008-124813-ac670b`).
- Codification: `.skip` ships in `core/base.css` (hidden until focused,
  jumps to `#main`), is named in `provenance/references/css-catalog.md`
  ("`.skip` — skip-link"), in `components.md` ("`.skip` link first in
  body"), and in the site's own Shell contract card. The catalogue has no
  entry for it in any pack.
- Status on the wired packs (verified by execution):
  pinned 0.12.1 → `component/nav-item`; evolution 0.13 → `component/nav-item`.
  Misfire persists.

### N-2 · Sliding panel (dispute)
- `dispute/20261008-134400-bcea20`: "a panel sliding in from the edge with
  a record's details" resolved to `pattern/viewer` on pinned (expected
  `component/sheet-end`).
- Status: pinned → `pattern/viewer`; evolution → `pattern/detail`
  (mis-route narrowed but still not the slide-over component;
  `component/sheet-end` scored 4.0 as a runner-up).

### N-3 · State label (dispute)
- `dispute/20261008-134400-193be0`: "a small label showing a record's state
  such as Draft" resolved to `guideline/voice` on pinned.
- Status: pinned → `guideline/voice`; evolution → **`recipe/status-with-text`**
  (COMPOSE). That recipe is the pack's own golden answer for status-display
  phrasings ("show whether a request is waiting for approval" →
  `recipe/status-with-text`), so the evolution behaviour is consistent with
  recorded canon. Assessed as **resolved by evolution**; no further change.

### N-4 · Row-actions chevron (dispute)
- `dispute/20261008-134400-9b284e`: "the chevron that reveals actions for a
  single row" resolved to `component/menu-item` on pinned (the wanted
  family is the row action menu; `component/menu-pop` on pinned).
- Status: pinned → `component/menu-item`; evolution → COMPOSE
  **`recipe/bulk-actions`** (wrong recipe; the correct neighbour
  `recipe/row-actions` exists with needs "per-row actions", "actions for a
  list item", "more menu on a row", and its evidence quotes exactly the
  `.menu-pop` row-menu pattern).

### N-5 · Status chips (codification)
- Experiment 02 (part B) finding: `.status-chips`/`.status-chip` ship in
  `core/patterns.css` and appear on the system's own patterns page, with no
  catalogue record naming the class; the agent refused the uncatalogued
  class and filed a gap.
- Status: evolution routes every "status chip" phrasing to
  `component/badge` (phrase alias, 13.0); `pattern/dashboard`'s summary
  says "status/automation chips" but does not name the classes and has no
  alias for them. Addressability is partial: the concept resolves to badge,
  the shipped pattern furniture is not addressable by name.

## Why this round is scoped small

Four of the five needs are **applicability/addressability** issues on the
evolution line: one missing catalogue entry, two vocabulary gaps, one
already fixed by the previous round. No new visual language is proposed, no
kernel semantics are touched (the resolution thresholds, precedence and
margin rules are frozen). Experiment 04's lesson is used as the scope
filter: only fixes that close codification and applicability gaps, never
"more retrieval machinery."
