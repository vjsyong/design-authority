# Design Authority — Specification, version 0.5

**Status: FROZEN.** This document set declares **Design Authority 0.5.0**
(repository tag `v0.5.0`). It supersedes **0.4.0** (tag `v0.4.0`, frozen
2026-10-08), **0.3.0** (tag `v0.3.0`, frozen 2026-10-08), **0.2.0** (tag
`v0.2.0`, frozen 2026-10-08) and **0.1.0** (tag `v0.1.0`, frozen
2026-10-07); the changes
between each pair of freezes are recorded in `05-governance-and-freeze.md` §3
and justified in the decision log (`docs/02-decisions.md`, D-023 to
D-026). The
semantics defined here are the normative contract; changes follow the
change-control rules in `05-governance-and-freeze.md`.

## What Design Authority is

A Design Authority is a **versioned, machine-readable design contract** plus
the tooling that serves it to coding agents and the governance process that
evolves it. It lets agents (1) discover what a design system defines, (2)
resolve a design problem, (3) inspect citable artifacts, (4) validate an
implementation, (5) report gaps upstream instead of silently inventing canon,
and (6) propose noncanonical extensions — under a process that converts
downstream evidence into governed upstream releases.

The kernel is **kit-agnostic**: it knows artifacts, rules, recipes, fallbacks,
precedents, candidates, resolutions, gaps and proposals; nothing about
buttons, colours, or any particular design system. A design system enters
only as a **pack**.

## Scope of this specification

| normative | informative / out of scope |
|---|---|
| the pack format (schema version `0.1`, incl. its additive extensions) | the contents of any specific pack |
| resolution semantics and outcome taxonomy (incl. precedent/candidate attachments) | the benchmark and its results |
| the tool surface (MCP, CLI) and record formats | curation editorial policy of a reference system |
| the evolution/governance process and provenance requirements | the reference design system itself (Triage) |

## Conventions

- **RFC 2119 keywords** are used normatively: MUST, MUST NOT, SHOULD, SHOULD
  NOT, MAY.
- "The kernel" refers to the reference implementation in `kernel/design_authority/`.
- "Pack" refers to a directory conforming to `02-pack-format.md`.
- Identifiers are stable strings of the form `<kind>/<slug>` (e.g.
  `component/select`).

## Documents

| file | contents |
|---|---|
| `00-index.md` | this file — status, scope, conformance |
| `01-definitions.md` | normative glossary |
| `02-pack-format.md` | system architecture + the pack data model |
| `03-resolution-semantics.md` | the resolution pipeline, scoring, outcomes, determinism |
| `04-interfaces.md` | MCP tools, CLI, records, validator runner |
| `05-governance-and-freeze.md` | the evolution process, versioning, the freeze declarations |
| `freeze-0.5.0.sha256` | SHA-256 of every file in the frozen surface at tag `v0.5.0` (current) |
| `freeze-0.4.0.sha256` | the same manifest for tag `v0.4.0` (historical) |
| `freeze-0.3.0.sha256` | the same manifest for tag `v0.3.0` (historical) |
| `freeze-0.2.0.sha256` | the same manifest for tag `v0.2.0` (historical) |
| `freeze-0.1.0.sha256` | the same manifest for tag `v0.1.0` (historical) |

## Conformance

An implementation is **conformant with Design Authority 0.3** if it:

1. loads packs conforming to `02-pack-format.md` with `format_version` `0.1`
   (including the additive negative-precedent and candidate extensions);
2. reproduces the resolution behaviour of `03-resolution-semantics.md` — in
   particular the outcome pipeline order, the thresholds (6.5 / 2.0 / 5.0),
   the citation rule (every cited id exists in the pack), the determinism
   rule (no network, stable ordering, no volatility in output), the lexical
   normalisation step in tokenisation (its guarded, table-bounded rewrite
   rules), and the precedent/candidate attachment rules;
3. exposes the record formats and tool surface of `04-interfaces.md` without
   mutating published packs;
4. can execute the governance requirements of `05-governance-and-freeze.md`
   when evolving packs — including the lenient adjudication rules and the
   candidate lifecycle.

**Conformance evidence** for the reference implementation: the unit tests
(`kernel/tests/`, 23/23), the golden suites (pinned pack 56/56; evolution
pack 23/23; synthesized packs 18/18 · 14/14 · 17/17), the convergence battery
(`tools/evolution_convergence.py`, 34/34), the precedent probe
(`tools/precedent_probe.py`, 31/31), the MCP smoke suite
(`tools/mcp_smoke.py`, 20/20), and the completed experiments documented
under `docs/` (benchmark · evolution · portability · synthesis · verification —
informative).
