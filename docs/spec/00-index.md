# Design Authority — Specification, version 0.1

**Status: FROZEN.** This document set declares **Design Authority 0.1.0**
(repository tag `v0.1.0`). The semantics defined here are the normative
contract; changes follow the change-control rules in `05-governance-and-freeze.md`.

## What Design Authority is

A Design Authority is a **versioned, machine-readable design contract** plus
the tooling that serves it to coding agents and the governance process that
evolves it. It lets agents (1) discover what a design system defines, (2)
resolve a design problem, (3) inspect citable artifacts, (4) validate an
implementation, (5) report gaps upstream instead of silently inventing canon,
and (6) propose noncanonical extensions — under a process that converts
downstream evidence into governed upstream releases.

The kernel is **kit-agnostic**: it knows artifacts, rules, recipes, fallbacks,
resolutions, gaps and proposals; nothing about buttons, colours, or any
particular design system. A design system enters only as a **pack**.

## Scope of this specification

| normative | informative / out of scope |
|---|---|
| the pack format (schema version `0.1`) | the contents of any specific pack |
| resolution semantics and outcome taxonomy | the benchmark and its results |
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
| `05-governance-and-freeze.md` | the evolution process, versioning, the 0.1.0 freeze declaration |
| `freeze-0.1.0.sha256` | SHA-256 of every file in the frozen surface at the tagged commit |

## Conformance

An implementation is **conformant with Design Authority 0.1** if it:

1. loads packs conforming to `02-pack-format.md` with `format_version` `0.1`;
2. reproduces the resolution behaviour of `03-resolution-semantics.md` — in
   particular the outcome pipeline order, the thresholds (6.5 / 2.0 / 5.0),
   the citation rule (every cited id exists in the pack), and the determinism
   rule (no network, stable ordering, no volatility in output);
3. exposes the record formats of `04-interfaces.md` without mutating published
   packs;
4. can execute the governance requirements of `05-governance-and-freeze.md`
   when evolving packs.

**Conformance evidence** for the reference implementation: the unit tests
(`kernel/tests/`), the golden suites (pinned pack 19/19; evolution pack 23/23),
the convergence battery (`tools/evolution_convergence.py`, 34/34), and the two
completed experiments documented under `docs/` and `docs/evolution/`
(informative).
