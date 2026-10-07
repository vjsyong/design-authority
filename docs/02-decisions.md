# 02 · Decision log (running)

Rules for this log: one entry per durable decision; record the *why* and what
evidence would overturn it. Append-only; supersede with new entries.

---

**D-001 · Project home.** `~/design-authority` as a new repository, separate
from Triage. The kernel is kit-agnostic; Triage is the first *pack*, generated
from a pinned snapshot and never edited in place by consumers.

**D-002 · Snapshot pin = `e374f38`** (Triage 0.12.1, branch `tds-fix-wrap` ==
local `demo`; newest complete state; stacked PRs #1–#6 + fix not yet merged to
`origin/main`). The pack manifest records repo+commit everywhere; if upstream
advances, regeneration creates a new pack version (that's the loop).

**D-003 · Thin kernel.** Audit evidence: Triage is already ~70% machine-
readable (tokens/rules/states/enforcement). The kernel only adds access +
uncertainty layers (search, resolution, recipes, fallbacks, gaps, proposals).
Anything that re-models tokens or re-implements lint is rejected by default.

**D-004 · Kernel tech.** Python 3.12 stdlib-first; packs are JSON directories;
no database; one library exposing both a CLI (`da`) and a stdio MCP server
(`fastmcp`, consistent with existing local MCP servers); server state limited
to the consuming workspace (`.design-authority/`).

**D-005 · Resolution = deterministic-first.** Alias + lexical matching over
pack artifacts; optional LLM assist may only select among retrieved candidates
and must cite pack IDs (server-validated). Outcome classes must not depend on
the assist. A committed golden set (~25 problems, incl. ≥5 UNDEFINED, ≥3
COMPOSE) gates P1.

**D-006 · Benchmark app = "Procura"**, a procurement approvals console.
Backend + routes prebuilt and frozen; agents implement UI only. Deterministic
state forcing via `?empty=1`, `?error=1`, `?job=running|done`.

**D-007 · Benchmark model = single pinned model for all runs.** Candidates
(from opencode providers): `opencode-go/deepseek-v4-flash` (draft default),
`opencode-go/glm-5.3-flash`, `opencode-go/gpt-5.6-luna`. Final pick after a
short capability probe in P3; recorded here. No model changes mid-experiment.

**D-008 · Parity by construction.** Condition B's static kit is *rendered from
the same pack* that Condition C serves via MCP; a generated parity checklist
fails the build if the two representations diverge in content.

**D-009 · Repetitions.** 3 runs per condition (9 total) for v1. Pre-registered
trigger: if within-condition spread dominates the C−B gap on a primary
dimension, extend to 5 per condition before interpreting.

**D-010 · Metrics discipline.** Per-dimension reporting only; no composite
score. Instruments frozen and pre-registration committed after the pilot,
before any comparative interpretation.

**D-011 · Materials per condition.** A: starter only. B: starter + vendored
system assets (`tokens/ core/ fonts/ icons/ examples/` from the snapshot) +
`design/` rendered docs. C: starter + same vendored assets + `DESIGN.md` +
MCP authority. The only B↔C delta is access mode (static docs vs active
authority) — plus C's validation loop and gap protocol, which are the
treatment. Package README/AGENTS/INTERACTION are NOT vendored as files for B/C;
their content enters via the pack render (B) / authority (C).

---

## Assumptions to verify

- **A-1** opencode runs can be isolated per run (dedicated config dir,
  plugins/mem disabled, fresh session id, fresh workdir). Verify in P3.
- **A-2** `fastmcp`/`mcp` installable in the kernel venv. Verify in P2.
- **A-3** Headless Chrome (Playwright cache, cf. `chromium-1234`, v151) is the
  capture engine for apps and docs. Verified present on this host.
- **A-4** Benchmark agents need no network beyond model calls; web-fetch
  availability, if any, is identical across conditions (config-controlled).
- **A-5** One human reviewer (Sean) suffices for v1 blind review; a second
  reviewer is a bonus, not a gate.

## Open questions (resolve in P1–P3)

- Q-1 Model choice (D-007) — probe + decide.
- Q-2 B kit format: markdown corpus + vendored assets (proposed) vs also a
  static snapshot of the docs site. Current lean: markdown only; note the site
  exists in C's citations.
- Q-3 C validation is agent-triggered only (the treatment), never pushed.
- Q-4 Lint scans for D1/D2 exclude vendored assets and the backend; only
  run-authored files count. Confirm wording in pre-registration.
- Q-5 Questionnaire wording + gallery design (P3).
- Q-6 Push to GitHub (`vjsyong/design-authority`, private) at end of P1.

## Deferred (do not build now)

Public catalogue · multi-tenant hosting · Studio · Figma integration · site
reverse-engineering · RBAC · Git governance product · framework breadth ·
universal ontology · HTTP MCP transport · authn · multi-pack arbitration ·
automatic pack regeneration · LLM-authored authority content.
