# Portability Spike · 11 · Agent build test v3 (Indaba)

**Run:** `indaba-a1` — fresh opencode agent (`deepseek/deepseek-flash`),
sandboxed with **only `packs/indaba`** mounted (kernel + filtered MCP
launcher; no other authority present). Same Depot brief and starter as the
retired NASA run, so results are comparable across attempts.

**Evidence bundle:** `benchmark/runs/indaba-a1/` → `transcript.jsonl`,
`prompt.md`, `ws/` (as-left workspace incl. `.design-authority/decision-log.jsonl`),
`interact.json`, `capture/` (5 screenshots), `run.json` + notes.

## Results

| metric | value |
|---|---|
| build completed | ✓ status ok, 278 s agent phase |
| authority calls | **84** (1 overview · 23 search · 26 inspect · 31 resolve · 3 validate) |
| resolve outcomes | RESOLVED 16 · UNDEFINED 11 · CONFLICT 2 · COMPOSE 2 |
| tool calls | 132 · tokens 3.49 M (3.38 M cache) · cost $0.048 |
| containment | attempts 0 · mentions 0 · **“triage” word count 0** · da_zone 4 |
| interactive checks | **15/15** (register + statuses · nav · checkout→on-loan · return→available · create · retire confirm gate · import start→progress→complete · mobile no-overflow) |
| authority lint | **indaba-lint 100/100, zero findings** (host kernel-orchestrated) |
| deliverable | `examples/indaba-reference-app/reference-build/` (app.css 439 lines · app.js 144 lines) |

## Observations (honest, kept on record)

1. **The ambiguous requirement resolved exactly as designed.** The agent
   queried the borrower-at-scale need; the authority returned UNDEFINED with
   `closest: component/choice`; the agent implemented a **native text input +
   datalist**, styled as a system field, and **explicitly marked it**
   (`data-fallback="platform-controls"`) with a code comment citing both the
   out-of-scope rule and the fallback — textbook authority usage.
2. **Progressive enhancement done right:** `app.js` (144 lines) only adds the
   retire dialog and live progress; the no-JS path still works (meta-refresh
   while importing; inline retire warning). This is the fallback/platform
   discipline made concrete.
3. **All five outcomes exercised again**, including CONFLICT (2 wrongness
   probes) — same model, different authority, its own answers throughout.
4. **Harness rigidity, not build faults (process note).** The first
   post-run interact failed silently; on investigation the *build was fine*
   and the checks were wrong for this authority's choices: (a) the borrower
   control is a text+datalist (checks only filled selects); (b) the
   detail-page status pill carries no `data-status` (the brief only mandates
   register hooks — register rows do keep them); (c) the import button is
   state-dependent ("Run import again" when complete) and reload-racing the
   page's own auto-refresh could crash the runner. Fixes landed in the
   harness: borrower fill for text inputs, status checks via `.status` text
   OR data-status, state-aware `[data-job-button]` matching, goto-based
   navigation, exception-safe sections, always-write output, and interact
   stderr captured to `interact-stderr.log` so failures can never be silent
   again. `interact.json` was regenerated after the fixes: **15/15**.
5. **Exit −15 again** — the agent terminated its own sandboxed test server
   during cleanup (same benign artifact seen in `orbit-a1`); all artifacts
   intact.
6. The workspace retains the agent's own testing leftovers (two “Test drill”
   rows, log entries) — kept as evidence; the `reference-build/` copy ships
   with seed data restored.
