---
name: extract-design-evidence
description: Use when deriving design evidence from a live product, a deployed site, or a brand kit. Screenshot-first, domain-partitioned extraction with verified renders, evidence tags, and merge rules.
---

# Extract Design Evidence (screenshot-first, domain-partitioned)

Use when an authority (or a design kit) must be derived or refreshed from a live artifact (site, app) or a brand kit, and fidelity to what is ACTUALLY rendered is the point. Proven in the phantom derivation (a deployed site → authority) and the three-source synthesis.

## 0. Renderable mirror (the gate)

- Build a local mirror with the FULL asset tree (the css/js/fonts/images cited by every page) so renders are faithful and offline.
- VERIFY a styled render before extracting: `document.styleSheets` non-empty, one known computed colour correct, screenshots at both widths. An unstyled render fabricates measurements; a whole pass once fooled itself exactly this way.
- Keep the heavy image mirror out of git; keep the evidence archive (pages, probes, screenshots) in-repo.

## 1. Screenshot protocol (primary evidence)

- Full-page captures per page at 1280x900 and 390x844, named `<domain>-<page>-<width>.png`.
- Trigger interaction states BEFORE capture: hover with a real pointer move, focus, open menus, carousel states as pairs, tab-walks. Rest-state-only scans miss every born-on-interaction element.
- READ every screenshot (vision) and record what it shows, cited by filename, before writing any finding against it.
- Exact values come from computed-style probes and are never quoted from stylesheet text. Deployed values diverge: flattened radii, mixed-case headings, removed zoom, and tiles-only motion were all found this way.

## 2. Evidence tags + BASE/OVERRIDE

- Tag observations OBSERVED-CSS (measured) · OBSERVED-VISUAL (seen, cite the file) · INFERRED.
- Tag every value BASE (substrate value still live) vs OVERRIDE (the deployment's own). Overrides are the design decisions under study; flaws inside them are recorded as measured observations, never silently corrected.

## 3. Domain teams (parallel subagents)

- Partition into four: A colour-and-surfaces · B typography-and-language · C components-and-states (capture hover/focus) · D layout-pages-motion (plus the WIP/gap sweep).
- Each team: read the shared brief; serve the mirror; screenshot; vision-read; measure; append PROGRESSIVELY to `domains/<x>-<domain>.md` (long runs must not lose work); return a compact report (domain · count · top findings · path).
- Hard rules per team: writes confined to `domains/` and `evidence/`; sources read-only; no invented numbers; no fix recommendations during extraction.
- Budget 30 to 45 minutes per team. The dispatch context must be self-contained (paths, tooling, protocol, deliverable); teams cannot ask questions.

## 4. Merge → pack entries

- Consolidate proposed entries; dedupe across teams; reconcile against the existing pack's id space (supersede in place when the subject matches).
- A canon reversal becomes a pack PRECEDENT (request · decision · grounds · try[] · citation).
- Regenerate goldens after merging and re-run the resolver against the refreshed pack; report outcome stats honestly (RESOLVED / COMPOSE / CONFLICT / FALLBACK / UNDEFINED).

## 5. Downstream app + re-verification

- The demo or audit app must WEAR the new canon: derive its css from the deployed stylesheet; keep instrument css separate.
- Refresh the verification contract to the new tokens; run the verifier and the app self-test; fix GENUINE findings, including your own demo content drifting from spec (fix the demo, never the check).
- Assertion traps: computed alpha values quantize (accept the quantized form); lazy images report `naturalWidth 0` until scrolled into view (scroll and settle before asserting); verify every serve hop.
