# Design Authority — rules of engagement

This workspace is governed by the **Triage Design Authority** (v0.12.1,
snapshot `e374f38`), available through the `design_authority` MCP server
configured for this project.

- Before choosing UI patterns, ask the authority: `resolve_design_problem`,
  `search_authority`, `inspect_artifact`.
- Where you follow an artifact, cite its id in a comment when it is not
  obvious from the class names used.
- `CONFLICT` outcomes: do not implement the request as stated; follow the
  cited rule/fix.
- `UNDEFINED` outcomes: implement per the fallback policy, mark the
  improvisation in a comment (`TODO(authority-undefined): ...`), and then
  `report_gap` so the need is recorded upstream.
- Run `validate_implementation` on this workspace before you finish and fix
  what it reports.
- The authority is read-only for consumers. Extensions go through
  `propose_extension` and are noncanonical until reviewed upstream.
