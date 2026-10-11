# 07 · Reconciliation lifecycle test — the Cadence portfolio

**Status:** executed 2026-10-11, prototype level, deterministic matching.
This is the first milestone of the reconciliation capability (D-030,
`docs/14-reconciliation.md`): not a test of interfaces, but of Design
Authority as a system of persistent design governance across generations of a
product.

**Artifacts:** tool `tools/da_sweep.py`; fixtures
`docs/experiments/reconcile-cadence/` (portfolio manifest, sandbox
authorities, findings stores, reports).

## 1 · The lifecycle, replayed on recorded data

The owner's scenario — an agent encounters an undefined need, implements a
provisional solution, a human later establishes precedent, and the system
determines whether the original implementation needs modification — exists in
recorded form in this repository already.

**Step 1, the undefined need (wink 0.1.0).** The `cadence-wink` build resolves
"delete a ritual permanently" against wink 0.1.0: outcome **U** (undefined).
The build improvises in character — an outline pill with the error ring
requiring confirmation, and a rounded white dialog on a 35% ink scrim — marks
both elements (`data-improvised`), and files
`gap/20261007-145139-ad4b85` ("destructive action affordance + confirmation +
undo flow for deleting a ritual"). Its NOTES.md records exactly this: *U
undefined → improvised in character, marked, gap filed.*

**Step 2, the precedent.** That gap went through the documented loop:
adjudication -> proposal `prop/...9ff839` (accepted) -> codified into wink
0.2.0 as `pattern/destructive-confirm`. The same path produced eleven records
across the three authorities: five in wink, three in leader, four in dominion.
Each record carries its provenance; each originated in a case a real build
filed when the need was UNDEFINED.

**Step 3, the determination.** The sweep links each new decision to its
recorded cases (explicit `resolves_cases` links in the fixture; the recorded
proposal chain otherwise), then assesses every generation of the product
against the target version and classifies by the transition policy.

## 2 · The portfolio

Nine applications: three generations (v1, v2, v3) of Cadence under each of
wink, leader and dominion. v1/v2 were built at 0.1.0; v3 was rebuilt at
0.2.0 and carries adoption evidence (`_evidence/resolves.jsonl`). The
manifest (`portfolio.json`) declares each build as an application plus a
`lineage` so the flagship build's recorded cases reach its generations
(receipts, P1.1, will make this self-describing).

## 3 · Method

- `tools/da_sweep.py` (prototype): deterministic level only - it follows
  recorded cases; it never infers. Findings are idempotent by identity
  (application, decision, target version, revision). Read-only over
  application trees.
- Transition decisions are **simulated fixtures, clearly labelled**: the
  policy mix a reviewer would set at publication. Nine `when_touched`, two
  `prospective`, one `required` (`component/notice`, by 0.3.0). The real
  choices for these records belong to the review that publishes them.
- A defaults variant (transition blocks stripped) exercises the owner-set
  default: legacy records -> `review`.
- Adoption = recorded resolution evidence (the build RESOLVED the need to
  that record). DOM-level adoption assessment is the conformance role's job
  (`da_verify`), deliberately out of scope here.

## 4 · Results

**Policy run — 36 findings: 10 conforms · 22 grandfathered · 3 rectify · 1 review.**

| Application | Class | Decisions |
|---|---|---|
| cadence-wink / cadence2-wink (v1/v2) | grandfathered | destructive-confirm, dialog-overlay, empty-state, inline-notice, progress |
| cadence3-wink (v3) | conforms | destructive-confirm, dialog-overlay, empty-state, progress |
| cadence3-wink (v3) | review | inline-notice |
| cadence-leader / cadence2-leader | grandfathered | data-charts, data-readouts, tag |
| cadence3-leader | conforms | data-charts, data-readouts, tag |
| cadence-dominion / cadence2-dominion | grandfathered | status, ledger, plain-chart |
| cadence-dominion / cadence2-dominion / cadence3-dominion | rectify | notice |
| cadence3-dominion | conforms | status, ledger, plain-chart |

An exact grandfathered finding (from `findings.jsonl`):

    finding/cadence-wink/pattern~destructive-confirm/0.2.0/v1
      class: grandfathered (policy when_touched, explicit)
      built_under: 0.1.0 · target: 0.2.0
      link: gap/20261007-145139-ad4b85 (via proposal chain / resolves_cases)
      trigger_state: {occurred: false, basis: "no modification recorded after
        the decision shipped"}
      reason: "built while the need was UNDEFINED; policy 'when_touched'
        permits until destructive flows is next modified"

And the rectify row:

    finding/cadence-dominion/component~notice/0.2.0/v1
      class: rectify (policy required, by 0.3.0)
      reason: "policy 'required': migration obligation is live (by 0.3.0);
        the implementation has not adopted the decision"

Properties demonstrated:

- **Historical compliance intact.** Every finding carries `built_under` and
  `target_version`; no v1/v2 row is a violation of anything. Their class is a
  permission, not a judgment.
- **Grandfathering carries reason + trigger.** The v1/v2 rows name the
  trigger that would end the permission ("next modification of the
  destructive flows"); trigger state is recorded, so the permission cannot
  silently become permanent.
- **Policy decided the outcome.** The same non-adoption splits into
  grandfathered (`when_touched`), review (non-adopted builds at the new
  version), and rectify (`required`) purely by policy.
- **A genuine review candidate surfaced.** `cadence3-wink` did not adopt
  `pattern/inline-notice` at 0.2.0 (no recorded resolution); the finding is
  `review`, not a violation. Whether that is a sanctioned deviation, pending
  work, or a real gap is a human call - the same shapes as the pagination
  examples in the owner's canvas.
- **Idempotent re-sweep.** Second run: `0 new, 36 reused` - finding identity
  working as specified; reconciliation after every release adds signal, not
  noise.
- **Link robustness.** With explicit `resolves_cases` stripped entirely, the
  sweep derived every link from the recorded proposal chain and produced
  identical findings (36/36, same classes, same reasons).
- **Defaults behaviour.** Without any transition blocks: 36 findings =
  10 conforms + 26 review. No silent migration obligation on legacy records;
  every row says its policy source is the legacy default.
- **Containment.** The sweep wrote nothing to any application tree (verified
  via `git status` scoped to `examples/`).

## 5 · Acceptance criteria exercised (docs/14 section 11)

Executed: **2** (deterministic match on recorded cases), **4** (`required`
carries its named trigger), **6** (no operation writes to application trees),
**7** (both versions on every finding), **9** (resolution links, both
explicit and chain-derived), **10** (idempotent re-sweep), and the
grandfathering half of **3** and **11** (class + reason + trigger state
recorded; the trigger-occurrence transition itself needs a real "area
touched" event and is deferred with receipts).

Not yet exercised: **1** (the full human-facing report), **5** (the inferred
level is specified - review candidates only - but not built), **8**/
remaining half of **11** (require receipts and a live product to re-touch).

## 6 · Honesty notes and limits

- The transition blocks in the fixture are **simulated and labelled**; they
  demonstrate the mechanism, not the owner's decisions. The real policies for
  these eleven records should be set through the review that publishes them.
- The lineage declaration in the manifest stands in for decision receipts;
  it is a recorded premise, stated in `portfolio.json`, not an inference.
- Deterministic level only. Older applications with no recorded cases will
  need the inferred level (code analysis / semantic discovery), which stays
  review-candidate-only by doctrine and is not built yet.
- Adoption is a proxy: recorded resolution evidence, not DOM verification.
- The prototype is not wired into `check.sh`; a proper gate lands with P1.4.

## 7 · What this unlocks / what is next

- The findings store is the natural feed for the Case events reserved in
  P0.2 (`impact_finding`, `migration_decision`) - no fifth lifecycle.
- `da reconcile` (sweep + policy evaluation + migration plan) becomes a thin
  layer over this result once receipts (P1.1) upgrade the deterministic
  level.
- Owner decisions to fold in: the real transition policies for the eleven
  records, and the disposition of the two `review` rows surfaced here.

## References

- Spec: `docs/14-reconciliation.md` (D-029; tightenings and defaults D-030).
- Fixtures and stores: `docs/experiments/reconcile-cadence/`.
- Tool: `tools/da_sweep.py`.
