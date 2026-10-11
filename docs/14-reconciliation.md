# 14 · Reconciliation — retroactive assessment of authority evolution

**Status:** design adopted (D-029). Implementation is staged after the
canonical Case model (P0.2) and the project decision receipts (P1.1), per the
dependency analysis in section 12. Operation names (`da sweep`,
`da reconcile`) are reserved by this document.

> Authority evolves prospectively. Its consequences may be assessed
> retrospectively. Historical decisions remain intact, while current
> implementations may require reconciliation.

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
  "applies_to": "existing_and_new",    // existing_and_new | new_only
  "supersedes": [],
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
  travels with the record.
- `required` is only enforceable when it names its trigger (`by`: a release
  or date, non-empty). A `required` policy without a trigger is refused at
  compile time; it degrades to nothing, and governance is not allowed to
  pretend otherwise.
- `supersedes` names records this one replaces. Following the chain is how
  the sweep finds deterministic matches, which implies a record lifecycle
  (active -> superseded) added with the envelope work.
- Grandfathering is therefore a deliberate outcome of policy, never something
  an agent infers from the age of an implementation. Explicit, scoped
  exemptions remain available where migration is inappropriate
  (`exceptions`), and every exemption is reviewed.
- Default for records without a block: see open question 1 (the one
  governance default this document does not set by itself).

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
Granularity and location: open question 2.

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
- No decision receipts exist anywhere yet; they arrive with P1.1, upgrading
  the deterministic level from "recorded cases" to "recorded decisions
  applied".
- The estate's own example builds are the natural first sweep corpus: a real
  portfolio spanning two authority generations.

## 10 · Open questions for the owner

1. **Default transition policy for records without a block.** Legacy records
   have none; new records may omit it. Proposal: `when_touched`, with the
   default shown on every report row; alternative: `review` (assess before
   any obligation). This is a governance default, so it is the owner's call.
2. **Receipt granularity and location.** Proposal: one receipt per published
   build under `.design-authority/receipts/<date>-<slug>.json`, with
   `receipt.json` at the store root pointing at the latest. Confirm when
   P1.1 lands.
3. **Record lifecycle for supersession.** The envelope work should add the
   superseded status so `supersedes` chains are explicit and audits can tell
   "followed old canon" from "never re-checked".
4. **Who owns a `review`-class migration decision.** Proposal: the same
   human seat as proposal verdicts, recorded as a case event.
5. **Applications with no store at all.** Screenshot-only builds fall to the
   inferred level only; every report must state that limitation.

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

## 12 · Dependencies and placement

- **Depends on:** P0.2 Case model (event kinds, case links) and P1.1 project
  contract + decision receipts. Without receipts, sweeps depend on
  reinterpreting old code, which weakens traceability - so this ships after
  them, as the owner specified.
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
