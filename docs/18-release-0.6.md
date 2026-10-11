# Release 0.6 — Integrated Governance (2026-10-11)

The memo's roadmap (`da_nextsteps.md`) closed. This document is the release
record: what P0–P5 delivered, the evidence for each, and what remains open.

## What 0.6 is

The transition the reproduction brief called for: from "the mechanisms work"
to "they work together as a product", with the benefit question answered by a
pre-registered experiment rather than asserted.

## Roadmap closure, item by item

**P0 · Resolve outstanding owner decisions — done.** The one-page ruling
instrument (34 judgments, 5 sections) was ruled by the owner; the renderings
are in `workspaces/owner-decisions-0.6/` with the applied reconciliation.

**P1 · Canonical Case model — done.** One event lifecycle replaces separate
governance interfaces internally (`docs/16-case-read-model.md`; 20 case-model
checks pin the corpus: 174 gaps / 4 disputes / 24 proposals / 38 findings
retrieved through one interface).

**P1.1/P1.2 · Project contracts and verified receipts — done.** A new app
can be planned, built, verified, and reconciled through stable interfaces:
the wink-notes acceptance vehicle is gated end to end (35 project-flow
checks; init → plan → receipt → verify → reconcile pinned).

**P2 · Pack integration — done.** The three Triage proposals merged
(0.12.2/0.13.0), the Triage verification contract shipped and
mutation-tested (14 checks; `docs/verification/10`), the 17 round-2 recipes
promoted -> pack 0.14.0, F-5's needs filed as candidates (0.14.1). Verified
source-system finals: triage 0.13.0; authority finals registered in
`docs/synthesis/data/releases.json`.

**P3 · Simplified installation and consumption — done and tested.** The
independent adoption run (x06) completed under bubblewrap: a fresh agent,
public clone only, 15.6 min, 16 authority calls, zero containment hits. Its
two findings were fixed the same day: F-1 validator portability (lint bundle
shipped in-pack; `da validate` works from a bare copy) and F-2 the
verification contract. The build it produced was independently verified
(`docs/experiments/08-adoption-test.md`).

**P4 · Longitudinal comparative experiment — run and read out.** The
pre-registration (docs/09) froze the design; run 1 executed 8 sandboxed
sessions (2 conditions × 4 handoffs) over the sealed bookmarks line. Result
(`docs/experiments/10`): governed precedent held a flat 100/100 against the
constant validator while the equally-good static-contract baseline decayed
98→96→94 across handoffs; migration handling was receipt-backed; zero human
interventions both conditions. The measurable cost of governance at this
scale: +21% tokens, +37% tool calls, ≈+16% wall. Primary gates met; kill
criterion not hit.

**P5 · Repository consolidation and release — this document.** One package,
generated documentation, compatibility gates, stable specification: each is
evidenced below.

## P5 evidence

- **One package.** The meta repository (`~/design-authority`) carries the
  kernel, CLI/MCP entrypoints, tools, spec, docs and the synthesis pipeline;
  the published authorities are the eight repos in the README's estate table
  (authority-triage at 0.14.1; wink/leader/dominion 0.3.0; phantom 0.2.0;
  indaba/orbit 0.1.0; triage-design-system tagged v0.13.0). All repositories:
  working trees clean, every commit pushed (verified at release).
- **Generated documentation.** README onboarding + the docs corpus
  (`docs/00`–`18`), the concept site, the authority sites (regenerated with
  version stamps at each final), and the review instrument; the release
  registry records owner-finalized versions and is read by the gates.
- **Compatibility gates.** `tools/check.sh` is the single entry: kernel
  tests, pack drift (17 files), compile invariants (164), compile parity,
  reconciliation regression (26), case model (20), project flow (35),
  golden agreement (all packs), concept-site byte-identity, MCP smoke (25),
  semantic self-test. Plus per-consumer contracts (5 verification contracts
  calibrated and mutation-tested). Green at this release.
- **Stable specification.** The spec remains frozen at 0.5.0 (tag `v0.5.0`,
  SHA-256 manifest in `docs/spec/freeze-0.5.0.sha256`). The record-layer
  additions landed during 0.6 (transition policies, verification contracts,
  provenance) are additive under the frozen change control; folding them
  into a formal 0.6.0 spec freeze is a deliberate owner decision, not
  implied by this release.

## Open items (recorded, not blocked)

- Optional P4 extension: a second chain per condition (dated amendment to
  docs/09) if the run-1 spread invites replication.
- The deferred fully-versioned release layout (D-036 follow-up), kept out so
  existing consumers stay untouched.
- A future spec freeze (0.6.0) to formalize the record-layer additions.

## Release marker

Tag `release-0.6.0` on this commit (an estate release, distinct from the
spec-freeze tag series v0.1.0…v0.5.0).
