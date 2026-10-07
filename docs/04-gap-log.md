# 04 · Triage gap log (codification sprint record)

Gaps found in Triage during this project, and the codification decisions made
while building the Authority Pack. The benchmark is expected to add more
(observed where agents guess); keep entries append-only.

Legend: **[audit]** found while auditing · **[pack]** decided during pack
generation · **[bench]** observed during benchmark runs · **[loop]** improved
by an accepted extension.

| ID | Status | Found | Gap / decision |
|---|---|---|---|
| G-001 | open | [audit] | **No composition layer.** Sanctioned compositions (armed delete, status-with-text, bulkbar-under-selection…) are prose. Pack v0 extracts them as `recipes`; each extraction is a decision recorded here. |
| G-002 | open | [audit] | **No fallback tier.** Nothing between "system" and "fork". Pack v0 declares 2–3 generic fallbacks; policy text lands in the manifest. |
| G-003 | open | [audit] | **Patterns second-class.** 7 patterns documented but not registered vs 35 components. Pack v0 registers patterns as artifacts (kind=pattern) with document/citation links; states/verify remain component-only. Boundary rule decision pending (what makes something a pattern vs component). |
| G-004 | open | [audit] | **Async / long-running work UI undefined.** Spinner + page-state + busy-button only; no canonical progress/job-status treatment. Benchmark UQ1 probes agents' guesses; if C reports it as a real gap, candidate extension. |
| G-005 | open | [audit] | **Consumer-side improvisation protocol absent.** Nothing tells a consuming agent how to mark improvisation, record gaps, or propose extensions. Kernel + `DESIGN.md` provide the protocol; its adoption is what the benchmark measures. |
| G-006 | open | [audit] | **Unenforceable copy rules / no a11y matrix / dataviz token-only / multi-brand & conformance-level semantics undefined.** Out of pack v0 scope except as `guideline` artifacts with citations (no enforcement claims). |
| G-007 | open | [audit] | **Severity override semantics undefined.** `.triagerc.json` allows per-project switching; no formal definition of what conformance means under overrides. Pack records rule defaults + notes the unknown; not solved in v0. |

## Codification decisions made while building the pack (append during P1+)

- **[pack] Patterns registered as artifacts, deliberately without a states/verify
  contract.** The 7 patterns become first-class pack members (kind=pattern,
  sources: docs page + CSS + example) while staying out of the lifecycle matrix.
  The component↔pattern boundary rule remains unresolved (G-003) — recorded, not
  invented.
- **[pack] 14 recipes extracted** from `INTERACTION.md` and two docs pages
  (feedback routing, armed delete, high-stakes confirm, reversible mutations,
  entity toggle, status-with-text, empty-with-CTA, bulk actions, editor savebar,
  row actions, page head, dialog task, paginated list, copy helper). Each recipe
  carries an evidence quote; extraction forced the decision that composition
  belongs to prose→recipe formalisation, not to new component invention.
- **[pack] Guidelines vs rules split by enforceability.** 13 guidelines were
  created for normative-but-unenforceable guidance (colour-not-alone, page
  hierarchy, copy helper, z-order, spacing roles…); only what lint can check
  stays a rule. This keeps "deterministic validation ≠ agent judgment" honest.
- **[pack] Per-artifact aliases are curated (47 artifacts).** Search quality
  depends on them; today they live in this repo's curation, not in Triage.
  Candidate extension: an `aliases` field maintained with each component in
  `spec/states.json`.
- **[pack] Prohibitions are keyword-triggered** (substring signals + one
  `color_literal` detector). Detection breadth is a known limitation; the
  golden set will quantify false positives/negatives before the benchmark.
- **[pack] Docs mapping is approximate** (group pages). Candidate extension:
  canonical page ids per component in the snapshot's docs data.
- **[pack] Golden set v0.2 → 19/19 agreement** (7 RESOLVED · 5 COMPOSE ·
  1 FALLBACK · 2 UNDEFINED · 4 CONFLICT); enforced by unit test. The two
  UNDEFINED cases are real Triage holes (progress/job treatment: G-004; charts:
  token-only) and are *expected* to stay UNDEFINED — they are the benchmark's
  probe targets.
- **[pack] Tokenizer precision incident.** A fuller stemmer ("-ing"/"-ed"/
  "-able") caused wrong direct matches (e.g. "saving" matched the savebar
  component; "enable" reduced to "en"). Fixed by shrinking the stemmer to a
  consistent minimum and letting recipe `needs` carry recall — recorded because
  the failure mode (tokenizer overreach silently reordering resolution
  outcomes) will recur in any future tuning.
- **[pack] `needs` lists are the recall surface.** Resolution quality for
  free-text needs depends on the recipe/artifact vocabulary containing the
  consumer's phrasings ("show the state of a request or item", "show the
  approval status of a record"). This is exactly the kind of knowledge the
  benchmark's Condition C will stress; additions are logged here as curation.
- **[pack] Prohibitions use bare signals + `signals_all` groups**
  (e.g. "confirm dialog" + "delete"); false-positive/negative rates measured
  only against the goldens so far — quantified properly in P3.
- **[loop] Extension-loop e2e exercised (2026-10-07, docs/05):** synthetic
  G-004 proposal reviewed by a second clean agent → verdict **needs-info** with
  four required changes; reviewer found the sanctioned composition covering the
  indeterminate half (spinner + recipe/status-with-text). G-004 stays open.
- **[loop→pack] Resolver precision observation:** `resolve("percent-complete
  progress …")` returned COMPOSE citing `recipe/status-with-text` — a recipe
  matched a need it cannot express (no numeric percent). Candidate mitigations
  for P3: a `disqualifiers` field on recipes, or outcome-level confidence split
  (COMPOSE-strong vs COMPOSE-weak) kept internal to the pack notes; decide with
  benchmark data before adding machinery.

*(more appended as P2/P3 continue — MCP smoke + benchmark scaffold)*

