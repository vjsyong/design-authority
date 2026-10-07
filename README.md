# Design Authority

**Version 0.1.0 — FROZEN** (tag `v0.1.0`). The normative specification lives in
[`docs/spec/`](docs/spec/00-index.md); this README is the entry point.

A **Design Authority** is a versioned, machine-readable design contract that
lets coding agents:

1. discover what a design system defines,
2. resolve a design problem (RESOLVED · COMPOSE · FALLBACK · UNDEFINED · CONFLICT),
3. inspect artifacts they can cite,
4. validate an implementation against explicit rules,
5. report gaps upstream instead of silently inventing canon, and
6. propose (noncanonical) extensions —

all under a governance process that converts downstream evidence into
governed upstream releases. The kernel is kit-agnostic: it knows artifacts,
rules, recipes, fallbacks, resolutions, gaps, and proposals — nothing about
buttons, colours, or any particular design system. A design system enters only
as a pack.

## Specification (0.1, frozen)

| file | contents |
|---|---|
| [`docs/spec/00-index.md`](docs/spec/00-index.md) | status, scope, conformance |
| [`docs/spec/01-definitions.md`](docs/spec/01-definitions.md) | normative glossary |
| [`docs/spec/02-pack-format.md`](docs/spec/02-pack-format.md) | architecture + pack data model |
| [`docs/spec/03-resolution-semantics.md`](docs/spec/03-resolution-semantics.md) | resolution pipeline, scoring, outcomes |
| [`docs/spec/04-interfaces.md`](docs/spec/04-interfaces.md) | MCP tools, CLI, records, validator runner |
| [`docs/spec/05-governance-and-freeze.md`](docs/spec/05-governance-and-freeze.md) | evolution loop, versioning, freeze declaration |
| [`docs/spec/freeze-0.1.0.sha256`](docs/spec/freeze-0.1.0.sha256) | checksums of the frozen surface |

## Layout

```
kernel/design_authority/   kernel (pack, search, resolve, validate, records, CLI, MCP)
tools/                     da CLI + MCP entrypoints, pack builder, kit renderer,
                           convergence battery, migration checker
packs/triage/              reference Authority Pack — Triage 0.12.1 @ e374f38 (pinned)
packs/triage-evolution/    0.13.0-experiment release (authority-evolution outcome)
docs/spec/                 the frozen specification
docs/evolution/            the evolution experiment record (00…06 + data)
benchmark/                 Procura starter, briefs, harness, runs (experiments)
```

## Quickstart

```bash
# CLI (default pack: packs/triage)
python3 tools/da.py resolve "A compact picker for assigning a reviewer from a small fixed list"
python3 tools/da.py --pack packs/triage-evolution golden --file packs/triage-evolution/golden.json

# MCP (stdio) — configure your agent with:
#   command: python3 tools/da-mcp.py
#   env: DA_PACK=<pack dir>  DA_WORKSPACE=<consumer workspace>
```

## Ground rules

- Deterministic validation is kept separate from agent judgment; the authority
  never fabricates: every answer cites pack IDs the server validates.
- UNDEFINED is a legitimate, useful outcome — the correct response is to
  implement per policy, mark the improvisation, and report a gap.
- Consumers never modify packs; proposals are reviewed upstream. See
  `docs/spec/05-governance-and-freeze.md` for how releases are made.

## Provenance

Two completed experiments document this system: the A/B/C authority benchmark
(`docs/08`–`docs/10`) and the authority-evolution loop (`docs/evolution/`).
The 0.1.0 freeze crowns both; the checksum manifest fixes the frozen surface.
