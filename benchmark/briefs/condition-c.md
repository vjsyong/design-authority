## Design authority

This product follows the **Triage Design Authority**, served by the
`design_authority` MCP tools configured for this workspace (see `DESIGN.md`).
Use it actively while you build:

- start with `authority_overview`; use `search_authority` and
  `inspect_artifact` to find what the system defines;
- call `resolve_design_problem` for each design decision — it returns
  CONFLICT / RESOLVED / COMPOSE / FALLBACK / UNDEFINED with citations;
- call `validate_implementation` on this workspace before you finish;
- when an outcome is UNDEFINED: follow the fallback policy, mark the
  improvisation in your code, and `report_gap` for the need.

Never present an improvisation as canonical. Do not modify the design system.
