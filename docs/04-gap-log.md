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

*(none yet)*
