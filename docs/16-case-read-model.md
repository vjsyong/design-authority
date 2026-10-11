# 16 · The Case read model

One interface for the complete, causally connected history of one decision.
Owner direction (`da_nextsteps.md` section 2): implement the canonical Case
model as a normalized, append-only event view over the existing records, and
prove it against the current corpus BEFORE changing any storage. This is the
logical boundary for the 0.6 specification freeze.

## What a Case is

A Case is a governance thread rooted at the record that opened it. The roots
today:

- a **gap** (`gap/...`, recorded in `gaps.jsonl` workspace stores): a need
  the authority could not answer when it was raised;
- a **disputed resolution** (`dispute/...`, recorded in `disputes.jsonl`): a
  resolution a consumer refused, kept distinct from an ordinary gap.

Proposals, publications, receipts, reconciliation findings and obligations
attach to their root as EVENTS, ordered by their recorded timestamps. Cases
are addressed by their root id; numbering (`case/NNNN`) and a first-class
recorded event store are reserved for the 0.6 integration freeze.

## The view, not a store

- Nothing is copied, migrated or rewritten; every event is derived on read
  from a named source file and record id.
- The tool is read-only. Existing resolution behavior cannot change through it.
- Output is deterministic: stable ordering (timestamp, then event kind, then
  source record), stable JSON.

## Event vocabulary

Derived today, all from recorded data:

- `gap_reported` — the need, its context, the authority state it was raised
  against (`gaps.jsonl`).
- `evidence_attached` — the gap's recorded evidence, when present.
- `proposal_submitted` — a proposal against the gap, with its proposed
  entries (`proposals/*.json`).
- `proposal_reviewed` — the recorded verdict (accepted, rejected,
  needs-info) with the adjudication rationale when one is recorded.
- `authority_published` — the codification ledger row: pack, version,
  entries (`docs/synthesis/data/codified.json`).
- `precedent_recorded` — a rejected proposal that became a negative
  precedent.
- `receipt_recorded` — a decision receipt whose `decisions_applied` /
  `migration_for` touch this thread's entries (revisions, deviations,
  verification result).
- `impact_assessed` — a reconciliation finding on one of the thread's
  entries (application, revision, class, policy, reason).
- `migration_required` — an obligation from an impact finding
  (`scheduled | due | overdue`, with its trigger).
- `migration_verified` / `obligation_closed` — a closed obligation, with
  `closed_by` and the verification result.
- `dispute_raised` — a disputed resolution, with its standing state.

Reserved for the recorded-case era (docs/14 section 10; not produced here):
case numbering and first-class `impact_finding` / `migration_decision`
events.

## Stores scanned

Repo-wide discovery: every `<workspace>/.design-authority` store that
contains governance records, plus the cross-cutting ledgers and the
authority packs.

- `gaps.jsonl`, `proposals/*.json`, `disputes.jsonl`, `receipts/*.json` in
  every `.design-authority` store (examples, workspaces, authority sites,
  benchmark runs, experiment workspaces, verification probes);
- `docs/synthesis/data/codified.json` and `adjudication.json` (the
  codification ledger plus review rationales);
- the reconciliation finding stores (`docs/experiments/reconcile-cadence/`
  main and `closure/`; the `findings-defaults` store is a scenario check,
  not an assessment of any build, and is deliberately excluded);
- every authority pack (`authorities/*/{artifacts,rules,prohibitions,
  fallbacks,recipes}.json`) for `why` views;
- the local decision ledgers (`docs/synthesis/{wink,leader,dominion}/
  decision.json`) for decision text and rejected alternatives;
- the recorded dispute replay (`docs/experiments/disputes/replay-*.json`)
  decorates live dispute rows with their standing state.

Excluded by design: sealed experiment materials
(`docs/experiments/seed-evolution/annexes/`, frozen fixtures, not history)
and evidence copies (`examples/phantom-audit/_evidence/gaps.jsonl`, an
artifact of that audit, not a store).

## Addressing and output

    python3 tools/da_case.py list [--json]
    python3 tools/da_case.py show <gap/… | dispute/… | prop/…> [--json]
    python3 tools/da_case.py why <record id> [--json]

- `list` — one row per case: unique gap ids with their proposal and finding
  counts, plus disputes. A gap id recorded in several stores (derived probe
  workspaces re-file the same id) renders once, with an occurrence count and
  the full store list; the primary recording is the first non-verification
  store.
- `show` — the full event timeline of one case (gap, dispute, or proposal
  root; a proposal root renders that proposal's events in its gap context).
- `why` — the record view: its published provenance route (`compiled_from`
  decisions or the exception block), the decisions behind it with their
  rejected alternatives, the proposal -> gap chain, every reconciliation
  finding on it, disputes touching it, and its receipts.

## Provenance discipline

- Every event names `source.file` (a path that exists in the repository) and
  `source.record` (the record id it was derived from).
- Only recorded fields are shown; absent fields are omitted, never
  defaulted into claims.
- Timestamps are the records' own; events without a recorded timestamp
  carry `null` and sort stably.

## Completion evidence (2026-10-11)

At landing, through the one interface: **173 unique gaps** (217 store
occurrences across 61 stores), **4 disputes**, **24 proposals**, **38
reconciliation findings**, **2 decision receipts**; every finding attaches
to a case, every proposal resolves through its gap thread.

`tools/check_case_model.py` pins this inside `check.sh` with 20 checks: the
corpus is re-derived independently of the tool (coverage equality), every
proposal and dispute is retrievable, the golden threads are pinned (the
destructive-confirm chain; the closure cycle with its verified close), every
event carries a live source reference, the vocabulary is closed, and output
is deterministic across runs.

## What this does not do (yet)

- No write path: cases are not a storage system, and no existing store is
  migrated.
- No case numbering; roots are addressed directly.
- Decision logs (`decision-log.jsonl` agent traces) and review verdict
  stores are not yet sources; they can attach later without schema changes.
- Compatibility adapters and the recorded-event store land with the 0.6
  integration freeze (docs/13 section 4, P0.2).
