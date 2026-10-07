# Portability Spike · 04 · Agent build test (Phase 6)

**Run:** `orbit-a1` — one fresh coding agent (opencode, `deepseek/deepseek-flash`),
sandboxed with **only the Orbit authority** visible. No Triage content existed
anywhere in the sandbox (it was never mentioned once in the transcript).

**Evidence bundle:** `benchmark/runs/orbit-a1/`
→ `transcript.jsonl` (206 events) · `prompt.md` (the brief) · `ws/` (final
workspace archive, incl. `.design-authority/decision-log.jsonl`) ·
`validate-host.txt` · `interact.json` · `capture/` (5 screenshots) · `run.json`.

## Setup

- Workspace: the Depot starter (`examples/orbit-reference-app`), unstyled.
- Mounts: kernel + a filtered `da-tools` (MCP launcher only) + `packs/orbit`
  — nothing else; strict permissions; bwrap; per-run XDG.
- Interaction surface: the standard Design Authority MCP interface
  (`authority_overview`, `search_authority`, `inspect_artifact`,
  `resolve_design_problem`, `validate_implementation`, `report_gap`,
  `propose_extension`).

## Outcome: the agent built the app end to end

- **15/15** interactive checks passed (register renders + statuses; nav;
  checkout→on-loan; return→available; create; retire confirm gate; activity
  start→progress advances→completes; mobile 380px with zero horizontal
  overflow) — `interact.json`.
- **orbit-lint: 100/100, zero findings** on the built app, run through the
  kernel (`validate-host.txt`) and directly by the agent.
- Duration ≈ 4.4 min agent phase (246.9 s) + capture/interact. 121 tool
  calls. Tokens: 2.39 M total (2.29 M cache-read), 106 K peak, $0.045.

## Authority usage (from the decision log — 75 calls)

| tool | calls | | resolve outcomes | n |
|---|---|---|---|---|
| authority_overview | 1 | | RESOLVED | 8 |
| search_authority | 18 | | COMPOSE | 6 |
| inspect_artifact | 26 | | CONFLICT | 2 |
| resolve_design_problem | 28 | | UNDEFINED | 12 |
| validate_implementation | 2 | | | |

Highlights from the 28 resolves:

- **The seeded ambiguous requirement resolved exactly as designed:**
  *“Select a borrower from a member list that can grow large…”* →
  **UNDEFINED**, closest `component/chooser` (6.5). The agent used the native
  datalist control (fallback/platform-controls), marked it in markup
  (`data-fallback="platform-controls"`).
- “Confirm retiring an item permanently” → **COMPOSE
  recipe/destructive-confirm**; the built page uses the Orbit dialog with a
  consequence sentence, and the interact suite verified the confirm gate.
- “Show an import job's progress with state, gauge and log” → **RESOLVED
  pattern/job-view**.
- “Rounded corners and drop shadows” → **CONFLICT**; “drop shadow or
  elevation to separate a panel” → **CONFLICT** — the agent did not ship
  either (lint confirms zero radius/shadow findings).
- The 12 UNDEFINEDs cover motion, letter-spacing, 12px text, uppercase
  labels, decorative gradients, etc. The build contains **no** improvisation
  beyond the two marked fallbacks.

## Observations (kept honestly, per protocol)

1. **Gap tool unused (0 `report_gap` calls).** Two template comments claim
   “Recorded as a gap against the authority”, and the improvisations are
   marked in markup, but no gap records were filed anywhere. The channel
   exists and is proven for this authority by a separate mechanical demo
   (`docs/portability/data/gap-demo-gaps.jsonl`: `gap/20261007-094303-d575c8`).
   This is an agent-instruction/behavior finding, not a representational one.
2. **The MCP validator returned `validators: []` early in the run** — a
   staging artifact: the sandboxed MCP server loaded the pack **before**
   `validators.json` was written mid-session (packs are loaded once per
   server process; the pack file later became visible through the live
   bind). The agent worked around it by running the pack's linter script
   directly (it had read the pack's `validators.json` + `orbit_lint.py`).
   The host-side rerun closes the loop properly (`validate-host.txt`).
3. **Direct pack reads (da_zone = 16 inputs):** the agent read authority
   files from `/opt/da/packs/orbit` directly in addition to the MCP
   interface. Permitted here (the authority is not secret); recorded for
   transparency. The MCP interface remained the primary channel (75 calls).
4. **Exit code −15:** self-inflicted — the agent SIGTERM'd its own sandbox
   session while stopping its background test server during cleanup, after
   writing “All flows pass.” All artifacts intact; harness unaffected.
5. **Containment audit:** attempts 0, mentions 0, denied events 13,
   **“triage” word count: 0**. The build was produced with zero Triage
   exposure or reference.

## Visual verification

Screenshots in `capture/` (desktop register/form/detail/activity + mobile
register). Independent review of the captures: square forms throughout,
single-accent discipline (active tab, primary action, overdue marker only),
marker+text status pattern, ruled register with folio footer, destructive
control as a 1px accent-bordered button with the consequence sentence, and a
clean stacked label-value adaptation at 380px.

## Where the built app lives

- Final interface archived at `examples/orbit-reference-app/reference-build/`
  (app.py, templates, `static/orbit.css` — 9.5 KB, `_smoke.py`).
- The agent's own smoke test (`_smoke.py`, 3.4 KB) is preserved as artifact.
