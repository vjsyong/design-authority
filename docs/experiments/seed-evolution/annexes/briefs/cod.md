# Adjudication session: turn the project record into a canonical pack

You are given: a frozen application workspace (the bookmarks manager) with
its records (`.design-authority/`: gaps, proposals, decision logs), the
census of its established conventions (`census/`), the pack-format and
governance specifications (`reference/`), and the authority tooling mounted
at `/opt/da` (CLI: `python3 /opt/da/tools/da.py`; the kernel lives at
`/opt/da/kernel`).

Task: produce **`base 0.1.0-experiment`** — a compact authority pack for
this project — in a new directory `pack/` at the workspace root.

Process (run it like a governance review):

- Read every gap and proposal in the records and everything in the census.
  For each item decide: **resolve** (codify a canonical record into the
  pack), **decline** (with grounds), or **defer** (with a reason). Never
  silently drop an item.
- Codify only conventions that are genuinely established and project-wide.
  The pack must be small and precise: records point at concrete treatments
  (classes, values, behaviours, states), not prose.
- Every resolved record cites what it was compiled from (record ids, census
  entries, files in the frozen workspace).

Deliverables at the workspace root:

- `pack/` — a valid pack directory per the format spec (`authority.json`,
  `artifacts.json`, `rules.json`, `scoring.json`, plus the optional files
  you actually need). Its version must be `0.1.0-experiment`; identity
  `id: base`, `name: Base`.
- `adjudication.md` — one line per gap/proposal: id → resolved (record id) /
  declined (grounds) / deferred (reason).
- `HANDOFF.md` — a short summary.

Validation — the pack must load and answer (iterate until it does):

    python3 /opt/da/tools/da.py --pack ./pack overview
    python3 /opt/da/tools/da.py --pack ./pack resolve "<one of the established conventions>"

Check at least three resolves, each phrased in plain words, and confirm the
outcome is RESOLVED (or COMPOSE/FALLBACK) with the record you intended.

Rules: do not modify the application source, the records, or the mounted
tooling; your writes are `pack/`, `adjudication.md`, `HANDOFF.md` only.
