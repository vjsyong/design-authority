# Design Authority (prototype)

Prototype + experiment for the **Design Authority** concept: a versioned,
machine-readable contract that lets coding agents

1. discover what a design system defines,
2. resolve a design problem (RESOLVED · COMPOSE · FALLBACK · UNDEFINED · CONFLICT),
3. inspect artifacts it can cite,
4. validate an implementation against explicit rules,
5. report gaps upstream instead of silently inventing canon, and
6. propose (noncanonical) extensions.

Triage (`vjsyong/triage-design-system`) is the first/reference authority, pinned
at commit `e374f38` (v0.12.1). The kernel is kit-agnostic: it knows artifacts,
rules, recipes, fallbacks, resolutions, gaps and proposals — nothing about
buttons, colours, or Triage.

**Status: Phase 0 — audit + proposal.** No implementation yet.

## Docs

| File | Contents |
|---|---|
| `docs/00-audit.md` | Part 1: what Triage contains, classified as explicit authority / inferable / undefined. |
| `docs/01-proposal.md` | The first deliverable: kernel, tool surface, benchmark app, three-condition design, metrics, architecture, phased plan. |
| `docs/02-decisions.md` | Running decision log, assumptions, open questions, deferred scope. |
| `docs/04-gap-log.md` | Triage gaps found + codification decisions made during the sprint. |

## Layout (target)

```
kernel/design_authority/   kernel package (pack loader, search, resolve, validate, records, MCP, CLI)
tools/                     pack builder (snapshot → pack) + kit renderer (pack → Condition-B docs)
packs/triage/              generated Authority Pack (manifest pins the snapshot)
benchmark/                 Procura starter app, briefs, harness, runs
docs/                      this documentation
```

## Ground rules

- Smallest thing that tests the hypothesis; everything else deferred (see
  `docs/02-decisions.md` § Deferred).
- Deterministic validation is kept separate from agent judgment; the authority
  never fabricates: every answer cites pack IDs the server validates.
- UNDEFINED is a legitimate, useful outcome.
