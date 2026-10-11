# 14 · Reconciliation — retroactive assessment of authority evolution

**Status:** specification complete and adopted (D-029); no reconciliation
engine exists yet. Implementation is staged after the canonical Case model
(P0.2) and the project decision receipts (P1.1), per section 12 - except the
end-to-end lifecycle test on the Cadence corpus
(`docs/experiments/07-reconciliation-cadence.md`), which exercises this
design at prototype level. Operation names (`da sweep`, `da reconcile`) are
reserved by this document.

> Authority evolves prospectively. Its consequences may be assessed
> retrospectively. Historical decisions remain intact, while current
> implementations may require reconciliation.

Three responsibilities, three questions:

| Responsibility | Question | What it produces |
|---|---|---|
| Governance | What becomes canon? | Approved, versioned decisions |
| Conformance | Does this implementation follow canon? | Verifiable implementation evidence |
| Reconciliation | What happens when canon changes? | Controlled migration over time |

## 1 · The third question

The system answers two questions today: what an agent does when a design need
is unresolved (the resolve/gap/proposal loop), and how an approved resolution
becomes authority (compile/codify). Reconciliation adds the third: **when the
authority evolves, what obligations does that create for applications built
under earlier versions?**

The recorded data already assumes this question without answering it. Gap
records carry the authority identity they were filed under
(`authority: {authority, version, commit}`); in this repository 36 of 53
recorded consumer stores pin their build version, several at versions their
authority has since left behind (the cadence builds at wink 0.1.0 and
dominion 0.1.0 against authorities now at 0.2.0). Nothing today computes what
that difference means.

The canonical illustration: three applications implement pagination while the
authority has no pagination recipe. They are not violating anything; the need
was UNDEFINED. When a later version promotes a pagination pattern, their
historical status must remain intact. They may now diverge from the newer
standard, but that is a different claim.

## 2 · Three concepts that must not be conflated

- **Precedent** — a design question has received an authoritative resolution.
- **Impact** — existing applications may contain implementations affected by
  that resolution.
- **Migration policy** — the authority owner determines whether and when
  those implementations should change. Agents do not infer it.

*Terminology note:* in this repository `precedents.json` holds NEGATIVE
precedents (declined requests). This document uses "precedent" in the owner's
sense, a newly authoritative positive decision; where ambiguity matters,
write "new canon".

Do not rewrite historical compliance. Every finding records the version an
application was built under and the target version; classification is always
against the target, never retroactively against the build.

## 3 · Transition policy on the decision

Retroactivity is a property of the approved decision, not a separate
governance subsystem. A record promoted into canon may carry a `transition`
block (additive to the record envelope; validated by the compiler like other
record fields):

```json
"transition": {
  "policy": "when_touched",            // prospective | when_touched | required | review
  "by": "next minor release",          // required only when policy = required
  "supersedes": [],
  "resolves_cases": ["case/0018"],     // previously unanswerable cases this decision answers
  "scope": "actions",                  // optional; additional restriction only when needed
  "rationale": "Existing compositions remain acceptable until the affected interface is modified.",
  "exceptions": "allowed_with_review"  // allowed_with_review | none
}
```

| Policy | Meaning | Typical application |
|---|---|---|
| `prospective` | Only new implementations must adopt the decision | Optional stylistic patterns |
| `when_touched` | Existing implementations migrate when the affected area is modified | Most design consistency improvements |
| `required` | Existing implementations must migrate before a defined release or deadline | Significant interaction or accessibility corrections |
| `review` | Existing implementations need assessment before a migration decision | Context-sensitive or potentially breaking changes |

Semantics:

- The block is set at promotion time (with the reviewer's verdict) and
  travels with the record. **Applicability is determined by the policy
  itself**: `prospective` applies to new implementations only; `when_touched`
  `required` and `review` apply to existing and new. A narrower reach is an
  optional `scope` restriction, never a second applicability switch - there
  is no `applies_to` to contradict the policy, and no invalid combination
  left for the compiler to reject.
- **Newly approved norms must declare a policy** (compiler-enforced, added to
  the compile invariants). Legacy records without a block default to
  `review`: no silent migration obligation for older applications, and every
  report row shows which policy applied and whether it was explicit or
  defaulted.
- The compiler validates every present block: policy enum, `by` if and only
  if `required`, list-typed `supersedes`/`resolves_cases`, `exceptions`
  enum. No invalid combination survives validation, so downstream consumers
  never meet one.
- `required` is only enforceable when it names its trigger (`by`: a release
  or date, non-empty). A `required` policy without a trigger is refused at
  compile time; it degrades to nothing, and governance is not allowed to
  pretend otherwise.
- `supersedes` names earlier RECORDS this one replaces; following the chain
  is how the sweep finds deterministic matches, which implies a record
  lifecycle (active -> superseded) added with the envelope work.
- `resolves_cases` names the previously UNADDRESSABLE cases this decision now
  answers. `supersedes` cannot express this link (no authoritative record
  existed when the need was filed); this is the sweep's deterministic hook
  into applications affected by a newly resolved gap - recorded cases first,
  semantic matching only as the fallback. Until the Case model lands,
  recorded gap ids serve as case references.
- Grandfathering is a deliberate outcome of policy, never something an agent
  infers from the age of an implementation. Explicit, scoped exemptions
  remain available where migration is inappropriate (`exceptions`), and
  every exemption is reviewed.

## 4 · The authority impact sweep

    da sweep --from 0.5.0 --to 0.6.0 [--portfolio <dirs>]

Compares the version diff (records added, amended, superseded - each with its
transition block) against the portfolio's recorded provenance. Two matching
levels, deliberately distinct:

- **Deterministic.** An application that recorded the original unresolved
  case, the authority reference, or the affected recipe is identified
  directly. Decision receipts (section 5) make this the norm for new builds;
  it already works today for the 36 version-pinned stores.
- **Inferred.** Older applications without complete provenance are searched
  through code analysis, screenshots, or semantic discovery. These findings
  are **review candidates, never confirmed violations** - the existing
  doctrine that retrieval never establishes authority extends to impact
  matching.

Finding classes, per application and changed decision:

- `conforms` - already matches the new decision;
- `grandfathered` - diverges; the transition policy permits it, and the
  finding preserves the reason and the trigger;
- `rectify` - the policy requires migration (now, or at the named
  release/deadline);
- `review` - uncertain match or context-sensitive; a human rules.

Three properties every finding carries:

- **Trigger state, tri-state.** `occurred | not_occurred | unknown`, each
  with an evidence reference and a basis. Missing evidence is never treated
  as "not occurred": `unknown` is the honest state unless the system can
  establish the modification history (receipts covering the application's
  post-decision builds, none touching the affected area). A `when_touched`
  permission ends the moment the trigger is recorded, and the obligation
  rides the revision that performed the modification.
- **Obligations carry state.** A rectify finding carries an `obligation`:
  `scheduled` (a `required` deadline later than the target version - a future
  obligation, not one already due), `due` (trigger recorded, or the deadline
  met), `overdue` (deadline passed), `closed` (a later receipt migrated the
  affected implementation; `closed_by` and the verification result ride
  along, and the migrated revision carries its own `conforms` finding).
  Re-assessments supersede findings while the store keeps the previous class
  and obligation, so the whole grandfathered -> rectify -> closed -> conforms
  trail stays auditable.
- **A stable identity.** Findings are keyed by (application, decision, target
  authority version, assessed build revision). Repeated sweeps are
  idempotent: an unchanged assessment reuses the existing finding, a
  re-assessment supersedes it. Reconciliation running after every release
  therefore adds signal, never duplicate noise.

Report shape (illustrative):

```json
{"authority": "wink", "from": "0.1.0", "to": "0.6.0",
 "counts": {"usages": 18, "review_candidates": 6, "required_changes": 2},
 "findings": [
   {"application": "examples/cadence-wink", "basis": "deterministic",
    "decision": "recipe/pagination", "policy": "when_touched",
    "class": "grandfathered", "built_under": "0.1.0",
    "reason": "built while pagination was UNDEFINED (gap gap/...)",
    "trigger": "next modification of the list surface"}]}
```

## 5 · Decision receipts

Extends the P1.1 project contract with the outcome half:

    .design-authority/
      authority.lock.json   # pinned {authority, version, commit}
      design-plan.json      # intent (written by `da plan`)
      receipt.json          # outcome (written when the build completes)
      cases/  verification/

A receipt captures consequential decisions only, not component invocations:
the authority version used; which authoritative decisions were applied; which
needs remained unresolved (case refs); which provisional solutions were
implemented (marked improvisations); any reviewed exceptions or explicit
deviations; and the verification result reference. Receipts are what let a
sweep identify affected applications without rediscovering everything from
source code.

Discipline: the receipt is written by the implementing agent at completion
and **confirmed by the verifier** - self-report is evidence, not proof. The
sweep trusts the confirmed variant and says so on every row it uses.

Granularity (owner-set): **one immutable receipt per published build** -
receipts are append-only, corrections are new receipts - with a pointer at
the store root to the latest.

Fields a receipt carries (prototype `prototype-0.1`, used by the closure
test; P1.1 formalizes): authority version; `decisions_applied`;
`unresolved_needs`; `provisional_solutions`; `deviations[]`;
`areas_modified[]` (the trigger surface for `when_touched`); `migration_for[]`
(closes earlier obligations for the named decisions); and a `verification`
reference (result + check count + the fresh verifier run).

Receipts are declarations, not proof: their claims are confirmed against
evidence before the sweep treats them as settled - source diffs and hashes
for the modification scope (`areas_modified`), the fresh verifier run for
applied decisions - and every finding that used receipt evidence carries
`receipt_status: confirmed | unconfirmed`. The confirmer runs separately
from the implementer.

## 6 · Grandfathering should not mean forgetting

Three states, kept distinct:

- **Historical compliance** - the implementation complied with the version
  under which it was built.
- **Current alignment** - the implementation matches the latest relevant
  authority.
- **Migration obligation** - the implementation is required to change, either
  now or upon a defined trigger.

An application can be historically compliant, currently divergent, and
legitimately grandfathered at the same time. A grandfathered finding preserves
its reason and its trigger ("deferred until the next modification of this
component"), never "accepted forever". The same machinery answers the
reversal case: when an authority later reverses a decision, findings can
distinguish applications that followed the old canon, intentionally deviated
(a recorded dispute or reviewed exception), or had already adopted the newly
preferred approach.

## 7 · Two directions of evolution

| | Forward evolution | Retroactive reconciliation |
|---|---|---|
| Trigger | New evidence or unresolved need | New authoritative decision |
| Question | What should become canonical? | What existing implementations are affected? |
| Output | New authority version | Impact findings and migration decisions |
| Verification | Is the decision valid and publishable? | Does the updated application conform? |

**The rigid boundary:** publishing a new precedent automatically triggers
assessment, never automatic code modification. Modification happens only as a
new build under the target version, with its own plan, its own receipts, and
its own verification. A new precedent is information, not a command to
rewrite the past - the same doctrine as "agents may improvise; they may not
confuse improvisation with authority", extended through time.

## 8 · Cases integration (no new lifecycle)

Impact findings and migration decisions are **events on existing Cases**,
attached to the same lifecycle rather than founding another:

- reserved event kinds for the P0.2 Case model: `impact_finding` (a sweep's
  assessment of a subject) and `migration_decision` (rectify / defer with
  trigger / exempt, with the reviewer recorded);
- the sweep opens a case only where a subject has none (e.g. an inferred
  candidate); otherwise it appends events.

Operations: `da sweep` is the scan/report; `da reconcile --authority X --to
latest` is sweep + policy evaluation + migration plan (changes required,
changes recommended, grandfathered implementations, uncertain matches) +
case events. The reconcile output is a plan; it never edits an application.

## 9 · What already exists to build on (inventory, 2026-10-11)

- 53 consumer `.design-authority` stores in this repository: 198 recorded
  gaps, 4 disputes, 24 proposals, 14 decision logs.
- **36 stores pin the authority version they were built under**, so
  deterministic version matching works today: the duty build at triage
  0.12.1; the adversarial and mutation fixtures at wink/leader/dominion
  0.2.0; the cadence builds spanning two generations (v1/v2 at 0.1.0, v3 at
  0.2.0). Several of those gaps are exactly the "undefined then" needs this
  capability must adjudicate.
- Decision receipts did not exist before this work; the closure test ships
  the first ones (prototype format, `examples/cadence-wink-r2/`), and P1.1
  formalizes them for every build.
- The estate's own example builds are the natural first sweep corpus: a real
  portfolio spanning two authority generations.

## 10 · Defaults and remaining details

**Settled (owner, 2026-10-11):**

- **Missing transition policy:** legacy records default to `review` - no
  silent migration obligation for older applications - while newly approved
  norms must carry an explicit policy (compiler-enforced).
- **Receipt granularity:** one immutable receipt per published build, with a
  pointer to the latest (section 5).
- **Real transition policies:** set for the twelve cadence records via the
  owner's decision page (D-034); `required` names its trigger (`by 0.3.0`
  where chosen). The fixtures carry them and the pinned sweep reflects them.

**Remaining details (resolvable at implementation time):**

1. Record lifecycle for supersession: the envelope work adds the superseded
   status so `supersedes` chains are explicit and audits can tell "followed
   old canon" from "never re-checked".
2. Who owns a `review`-class migration decision. Proposal: the same human
   seat as proposal verdicts, recorded as a case event.
3. Applications with no store at all fall to the inferred level only; every
   report must state that limitation.

## 11 · Acceptance criteria (pre-registered for the phase)

1. A version diff produces a report whose findings cite decisions, policy and
   the version pair; counts reconcile with the findings.
2. Deterministic: a store that recorded the original case is matched to the
   new decision without code analysis.
3. Grandfathered: an implementation built while a need was UNDEFINED
   classifies as grandfathered (not a violation) under `when_touched`, with
   reason and trigger preserved.
4. `rectify` is emitted only when the policy requires it, and for `required`
   only when a named trigger exists.
5. Inferred findings are review candidates; none is emitted as a confirmed
   violation.
6. Nothing in this capability writes to an application tree; `reconcile`
   outputs a migration plan and case events only (assert via untouched tree
   hashes, the existing wrapper discipline).
7. Historical compliance intact: every finding records the built-under
   version and the target version.
8. First real corpus: the estate's example builds (cadence v1-v3 across
   wink/leader/dominion) swept from their recorded versions to the current
   ones.
9. Resolve links: a decision that answered a recorded case links to it
   (`resolves_cases` or the recorded chain) and the sweep reaches the
   affected applications through that link, not through semantic matching.
10. Idempotent re-sweep: running the sweep twice over unchanged inputs
    reuses every finding - zero duplicates, zero changes.
11. Trigger transition: a grandfathered `when_touched` finding records its
    trigger state, and once the trigger occurs without migration the finding
    reclassifies as rectifiable.
12. Receipt claims are confirmed against evidence (source diffs + hashes;
    the fresh verification for applied decisions), and stale evidence fails
    loudly: record-hash and build-hash binding turn drift into a gate
    failure instead of silent decay.

The Cadence lifecycle test (`docs/experiments/07-reconciliation-cadence.md`)
executes criteria 2, 4, 6, 7, 9, 10 and - through the closure test - 3 and 11
in full: a real revision modified without migrating, the trigger detected,
the obligation due, the migration applied, independently verified (9/9 checks,
coverage disclosed), and the obligation closed by the confirmed receipt.
`tools/reconcile_regression.py` (inside `check.sh`) re-runs these criteria
from committed fixtures - pinned counts, idempotency, link derivation, the
defaults behaviour, the full closure cycle, and evidence freshness - so the
tested lifecycle survives refactoring.

## 12 · Dependencies and placement

- **Depends on:** P0.2 Case model (event kinds, case links) and P1.1 project
  contract + decision receipts. Without receipts, sweeps depend on
  reinterpreting old code, which weakens traceability - so the full engine
  ships after them, as the owner specified.
- **The first milestone (owner direction, 2026-10-11):** an end-to-end
  lifecycle test on the existing Cadence builds across wink/leader/dominion -
  an agent encounters an undefined need, implements a provisional solution, a
  human establishes precedent, and the system determines whether the original
  implementation needs modification. Prototype-level, on recorded data, ahead
  of the full engine; the write-up lands in
  `docs/experiments/07-reconciliation-cadence.md`.
- **Then:** the `transition` block enters the record layer (spec bump), then
  `da sweep`, then `da reconcile`, then portfolio wiring over the example
  builds.
- `docs/13-simplification.md` carries the phase row (P1.4).

## References

- Owner memo, reconciliation, 2026-10-11 (recorded as D-029).
- Existing lifecycle this attaches to: `docs/13-simplification.md` sections
  3-4 (the Case) and the records in `kernel/design_authority/records.py`.
- Retrieval doctrine the inferred level preserves: `docs/spec/03`, and the
  semantic-discovery findings in `docs/experiments/01`.
