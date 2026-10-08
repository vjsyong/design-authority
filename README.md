# Design Authority

**Version 0.2.0 — FROZEN** (tag `v0.2.0`; supersedes 0.1.0, tag `v0.1.0`). The
normative specification lives in [`docs/spec/`](docs/spec/00-index.md); this
README is the entry point.

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
rules, recipes, fallbacks, precedents, candidates, resolutions, gaps, and
proposals — nothing about buttons, colours, or any particular design system. A
design system enters only as a pack.

## Specification (0.2, frozen)

| file | contents |
|---|---|
| [`docs/spec/00-index.md`](docs/spec/00-index.md) | status, scope, conformance |
| [`docs/spec/01-definitions.md`](docs/spec/01-definitions.md) | normative glossary |
| [`docs/spec/02-pack-format.md`](docs/spec/02-pack-format.md) | architecture + pack data model |
| [`docs/spec/03-resolution-semantics.md`](docs/spec/03-resolution-semantics.md) | resolution pipeline, scoring, outcomes |
| [`docs/spec/04-interfaces.md`](docs/spec/04-interfaces.md) | MCP tools, CLI, records, validator runner |
| [`docs/spec/05-governance-and-freeze.md`](docs/spec/05-governance-and-freeze.md) | evolution loop, versioning, the freeze declarations |
| [`docs/spec/freeze-0.2.0.sha256`](docs/spec/freeze-0.2.0.sha256) | checksums of the frozen surface (current) |
| [`docs/spec/freeze-0.1.0.sha256`](docs/spec/freeze-0.1.0.sha256) | the 0.1.0 manifest (historical) |

## Layout

```
kernel/design_authority/   kernel (pack, search, resolve, validate, records, CLI, MCP)
tools/                     da CLI + MCP entrypoints, pack builder, kit renderer,
                           convergence battery, migration checker
packs/triage/              reference Authority Pack — Triage 0.12.1 @ e374f38 (pinned)
packs/triage-evolution/    0.13.0-experiment release (authority-evolution outcome)
packs/wink · leader · dominion/   synthesized authorities (0.2.0, codified)
packs/orbit · indaba/             portability-spike authorities (0.1.0)
docs/spec/                 the frozen specification
docs/evolution/            the evolution experiment record (00…06 + data)
docs/portability/          the second-authority spike record (00…12)
docs/synthesis/            the synthesis experiment record (00…16) + review app
examples/                  Cadence builds (v1–v3, wink/leader/dominion) + reference apps
benchmark/                 Procura starter, briefs, harness, runs (experiments)
```

## Quickstart

```bash
# CLI (default pack: packs/triage)
python3 tools/da.py resolve "A compact picker for assigning a reviewer from a small fixed list"
python3 tools/da.py --pack packs/triage-evolution golden --file packs/triage-evolution/golden.json

# The pre-deviation check (negative precedents with scope verdicts):
python3 tools/da.py --pack packs/wink precedent-check --ask "a check control to log a ritual"

# MCP (stdio) — configure your agent with:
#   command: python3 tools/da-mcp.py
#   env: DA_PACK=<pack dir>  DA_WORKSPACE=<consumer workspace>
```

## Ground rules

- Deterministic validation is kept separate from agent judgment; the authority
  never fabricates: every answer cites pack IDs the server validates.
- UNDEFINED is a legitimate, useful outcome — the correct response is to
  implement per policy, mark the improvisation, and report a gap.
- Declines are policy-only (lenient adjudication, `docs/spec/05` §1):
  evidence-poor asks defer to UNDEFINED or become *candidates*; a precedent
  `outside` verdict means the ask is explicitly not governed.
- Consumers never modify packs; proposals are reviewed upstream. See
  `docs/spec/05-governance-and-freeze.md` for how releases are made.

## Provenance

Completed experiments document this system: the A/B/C authority benchmark
(`docs/08`–`docs/10`), the authority-evolution loop (`docs/evolution/`), the
second-authority portability spike (`docs/portability/`), and the authority
synthesis experiment (`docs/synthesis/`). The **0.1.0 freeze** (2026-10-07)
crowned the first two; the **0.2.0 freeze** (2026-10-08) formalizes the
post-freeze era on the same frozen surface.

## 0.2.0 — what the bump formalizes (2026-10-08)

The work after 0.1.0 is now formalized as the **0.2.0** minor bump (justified
in D-023): negative precedents + candidates as optional pack records,
precedent scope verdicts (`governs` / `outside` / `ambiguous`), the lenient
adjudication doctrine, and the tool-contract additions (see
`docs/spec/05` §3). The era also produced the portability spike (Ubuntu
"Indaba"), the synthesis experiment with its in-browser Gates 1–2, three
Cadence stress rebuilds (gaps 48 → 17), and the build review window that
records owner verdicts against decision records. Full consolidated record:
[`docs/11-consolidation-since-0.1.0.md`](docs/11-consolidation-since-0.1.0.md).
