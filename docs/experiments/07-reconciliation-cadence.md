# 07 · Reconciliation lifecycle test — the Cadence portfolio

**Status:** executed 2026-10-11, prototype level, deterministic matching,
including the full closure cycle (section 5: a real revision modified,
migrated, independently verified, obligation closed). This is the first
milestone of the reconciliation capability (D-030, `docs/14-reconciliation.md`):
not a test of interfaces, but of Design Authority as a system of persistent
design governance across generations of a product.

**Artifacts:** tool `tools/da_sweep.py`; fixtures
`docs/experiments/reconcile-cadence/` (portfolio manifests, sandbox
authorities, findings stores, reports, the closure test); the closure build
`examples/cadence-wink-r2/` (revisions r2a and r2b with prototype receipts).

## 1 · The lifecycle, replayed on recorded data

The owner's scenario - an agent encounters an undefined need, implements a
provisional solution, a human later establishes precedent, and the system
determines whether the original implementation needs modification - exists in
recorded form in this repository already.

**Step 1, the undefined need (wink 0.1.0).** The `cadence-wink` build resolves
"delete a ritual permanently" against wink 0.1.0: outcome **U** (undefined).
The build improvises in character - an outline pill with the error ring
requiring confirmation, and a rounded white dialog on a 35% ink scrim - marks
both elements (`data-improvised`), and files
`gap/20261007-145139-ad4b85` ("destructive action affordance + confirmation +
undo flow for deleting a ritual"). Its NOTES.md records exactly this: *U
undefined -> improvised in character, marked, gap filed.*

**Step 2, the precedent.** That gap went through the documented loop:
adjudication -> proposal `prop/...9ff839` (accepted) -> codified into wink
0.2.0 as `pattern/destructive-confirm`. The same path produced twelve records
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
(receipts, P1.1, will make this self-describing). The closure test (section
5) adds two further revisions of the cadence-wink line, `r2a` and `r2b`.

## 3 · Method

- `tools/da_sweep.py` (prototype): deterministic level only - it follows
  recorded cases and prototype decision receipts; it never infers. Findings
  are idempotent by identity (application, decision, target version,
  revision). Read-only over application trees.
- Transition decisions are the **owner's real policies** (decision page,
  2026-10-11; D-033/D-034): `required` by 0.3.0 for wink
  `pattern/destructive-confirm` and `pattern/progress`; `review` for
  dominion `component/status`; `prospective` for `pattern/empty-state`
  (wink), `pattern/data-readouts` (leader), `component/ledger` and
  `component/notice` (dominion); `when_touched` for the remaining five.
  The fixtures previously carried a simulated mix (nine `when_touched`,
  two `prospective`, one `required`); the rulings replaced it and every
  result below was regenerated.
- A defaults variant (transition blocks stripped) exercises the owner-set
  default: legacy records -> `review`.
- Adoption = recorded resolution evidence, or a receipt's `decisions_applied`
  list; a recorded deviation overrides a bare resolve. DOM-level adoption
  assessment is the conformance role's job (`da_verify`), deliberately out of
  scope here.
- Prototype receipts are declarations until confirmed: a separate script
  (`examples/cadence-wink-r2/_evidence/confirm-receipts.py`) confirms the
  claimed modification scope against source diffs and hashes, and findings
  that used a receipt carry `receipt_status: confirmed | unconfirmed`.
- Findings carry the tightened semantics from the owner review (D-031):
  tri-state `trigger_state` (`occurred` | `not_occurred` | `unknown`, with
  evidence - missing evidence is never treated as "not occurred") and an
  `obligation` object on rectify findings (`scheduled` | `due` | `overdue` |
  `closed`, with `closed_by` + verification when a later receipt migrates).

## 4 · Results

**Policy run - 36 findings: 10 conforms · 18 grandfathered · 4 rectify · 4 review**, with 4 obligations (all `scheduled`: the `required` deadline 0.3.0
is later than the target 0.2.0, so none is presented as already due).

| Application | Class | Decisions |
|---|---|---|
| cadence-wink / cadence2-wink (v1/v2) | grandfathered | dialog-overlay, empty-state, inline-notice |
| cadence-wink / cadence2-wink (v1/v2) | rectify | destructive-confirm, progress |
| cadence3-wink (v3) | conforms | destructive-confirm, dialog-overlay, empty-state, progress |
| cadence3-wink (v3) | review | inline-notice |
| cadence-leader / cadence2-leader | grandfathered | data-charts, data-readouts, tag |
| cadence3-leader | conforms | data-charts, data-readouts, tag |
| cadence-dominion / cadence2-dominion | grandfathered | ledger, notice, plain-chart |
| cadence-dominion / cadence2-dominion | review | status |
| cadence3-dominion | conforms | ledger, plain-chart, status |
| cadence3-dominion | review | notice |

An exact grandfathered finding (from `findings.jsonl`):

    finding/cadence-wink/pattern~dialog-overlay/0.2.0/v1
      class: grandfathered (policy when_touched, explicit)
      built_under: 0.1.0 · target: 0.2.0
      link: gap/20261007-145938-a0e2b0 (via proposal chain / resolves_cases)
      trigger_state: {state: unknown, basis: "complete modification history
        not established (no receipts covering the window)"}
      reason: "built while the need was UNDEFINED; policy 'when_touched'
        permits until overlays is next modified"

And a rectify row (wink, owner-set `required`):

    finding/cadence-wink/pattern~destructive-confirm/0.2.0/v1
      class: rectify (policy required, by 0.3.0)
      obligation: {state: scheduled, by: 0.3.0}
      reason: "policy 'required': migration obligation is not yet due
        (scheduled for 0.3.0); the implementation has not adopted the decision"

Properties demonstrated:

- **Historical compliance intact.** Every finding carries `built_under` and
  `target_version`; no v1/v2 row is a violation of anything. Their class is a
  permission (with an obligation where `required`), not a judgment.
- **Grandfathering carries reason + trigger, tri-state.** The v1/v2 rows name
  the trigger that would end the permission and record trigger state
  honestly: `unknown` where no receipts cover the window - absence of
  evidence is not evidence of absence.
- **Policy decided the outcome.** The same non-adoption splits into
  grandfathered (`when_touched`), review (non-adopted builds at the new
  version, or affected builds under `review`), and rectify (`required`)
  purely by policy - and the owner's rulings (D-034) chose which policy
  each record carries.
- **Future obligations are not presented as due.** The wink
  `destructive-confirm`/`progress` rows are rectify with
  `obligation.state = scheduled` (by 0.3.0), never "overdue".
- **Genuine review candidates surfaced.** `cadence3-wink` did not adopt
  `pattern/inline-notice` at 0.2.0 (no recorded resolution) and
  `cadence3-dominion` built `component/notice` at the new version without a
  recorded adoption; both are `review`, not violations. Whether they are
  sanctioned deviations, pending work, or real gaps is a human call - the
  same shapes as the pagination examples in the owner's canvas. The owner
  disposed the wink row as pending work (adopt at the next revision;
  D-034). The dominion `status` rows sit under the owner-set `review`
  policy: each affected build's labels are reviewed before adoption.
- **Idempotent re-sweep.** Second run: `0 new, 36 reused` - finding identity
  working as specified; reconciliation after every release adds signal, not
  noise. (The semantics tightening from D-031 re-assessed 21 rows; the store
  keeps every superseded class/obligation as history.)
- **Link robustness.** With explicit `resolves_cases` stripped entirely, the
  sweep derived every link from the recorded proposal chain and produced
  identical findings (36/36, same classes, same reasons).
- **Defaults behaviour.** Without any transition blocks: 36 findings =
  10 conforms + 26 review. No silent migration obligation on legacy records;
  every row says its policy source is the legacy default.
- **Containment.** The sweep wrote nothing to any application tree (verified
  via `git status` scoped to `examples/`).

## 5 · The closure: modified, migrated, verified, closed

The main corpus never re-touches its applications after the precedent ships,
so the final state transition - grandfathered -> trigger -> rectify ->
migration -> verification -> closure - needed a real modification. The
closure test takes the cadence-wink v1 line and modifies one affected area
for real: `examples/cadence-wink-r2/`, a genuine next revision of the build.

**Revision r2a - the modification, without migration.** The settings-save
confirmation is reworked (v1's improvised `showToast("Saved")` becomes a
persistent ad-hoc text echo). The rework's resolution session ran against the
live resolver ("a saved confirmation after saving settings" -> RESOLVED
`pattern/inline-notice`) and the canonical treatment was **not** adopted; the
deviation is recorded in the r2a prototype receipt
(`.design-authority/receipts/2026-10-11-r2a-modification.json`), with
`areas_modified: ["feedback / save confirmation (settings)"]`.

Sweep at this point (`closure/report-1.json`, 2 findings):

    cadence-wink  v1   grandfathered  trigger {state: occurred,
      evidence: [r2a receipt]}  "...permission ended: trigger recorded;
      the obligation rides the modified revision"
    cadence-wink-r2  r2a  RECTIFY  obligation {state: due}  trigger {occurred}
      "the affected area (feedback) was modified without migrating..."

**Revision r2b - the migration, independently verified.** The save
confirmation is migrated to the canonical inline notice (parsnip fill,
rounded 12, bold lead sentence plus a plain supporting line, in flow near the
save control). The verification is independent and fresh: a separate script
(`_evidence/verify-notice-migration.py`) serves the app, drives the save
flow in headless Chromium, and re-derives every claim from the served DOM and
computed styles against the record's own states - **9/9 checks pass**
(`_evidence/verification/notice-migration.json`). The verification is bound
to the exact record (a `record_hash` makes staleness detectable) and its
coverage is disclosed against the record's normative items: 3 of 4
mechanically covered, the copy register (`copy is plain, non-blaming,
question-first`) listed as a human-review item rather than implied. The
migration receipt (`...-r2b-migration.json`) declares
`migration_for: ["pattern/inline-notice"]` and carries the verification
reference.

**Both receipts are confirmed, not trusted.** A separate confirmer
(`_evidence/confirm-receipts.py`) checks the claims against source evidence:
the r2a modification is confined to the claimed area (10 changed lines:
removes the improvised save toast, adds the ad-hoc echo), the r2b migration
changes that area toward the notice (15 changed lines) and removes the echo,
and hashes of the v1, r2a (committed snapshot, `_evidence/snapshots/r2a/`)
and r2b states are recorded (`_evidence/verification/receipt-confirmation.json`).
Every finding that used receipt evidence carries
`receipt_status: confirmed`.

Sweep at this point (`closure/report-2.json`, 3 findings):

    cadence-wink-r2  r2b  conforms (receipt: decisions_applied)
    cadence-wink-r2  r2a  rectify, obligation {state: closed,
      closed_by: [r2b receipt], verification: {result: pass, checked: 8/8},
      previous: {state: due}}          <- superseded, history retained
    cadence-wink     v1   unchanged (grandfathered, trigger occurred)

That is the complete cycle the owner asked for: **historical build ->
grandfathered -> affected area modified -> rectify -> approved migration
applied -> independently verified -> conforms**, without any operation
writing to an application tree.

## 6 · Acceptance criteria exercised (docs/14 section 11)

Executed: **2** (deterministic match on recorded cases), **3** (full cycle:
grandfathered classification with reason/trigger, and the real transition
through trigger and migration), **4** (`required` carries its named trigger),
**6** (no operation writes to application trees), **7** (both versions on
every finding), **9** (resolution links, both explicit and chain-derived),
**10** (idempotent re-sweep), **11** (trigger transition: recorded,
detected, and closed by a verified migration receipt), **12** (receipt claims
confirmed against source evidence; freshness bound by hashes and enforced by
the regression gate).

Not yet exercised: **1** (the full human-facing report), **5** (the inferred
level is specified - review candidates only - but not built), **8** (the
portfolio wiring across authorities is exercised; a fresh sweep corpus from
a live product is still ahead).

## 7 · Honesty notes and limits

- The transition blocks in the fixture are the **owner's real policies**
  (decision page, 2026-10-11; D-034). The pre-ruling simulated mix (nine
  `when_touched`, two `prospective`, one `required`) remains described in
  section 3 and in git history.
- The r2 revisions are a genuine modification of the v1 build, made for this
  test; their receipts use the prototype format (`prototype-0.1`; P1.1
  formalizes) and are confirmed against source evidence (diffs + hashes; the
  r2a state is preserved as a committed snapshot,
  `_evidence/snapshots/r2a/`). The r2a/r2b sequence was executed live in this
  session: stage 1's report (`closure/report-1.json`) is the assessment at
  the trigger point; stage 2 is the final state. Re-running the sweep over
  the final tree reproduces stage 2.
- The lineage declaration in the manifest stands in for decision receipts;
  it is a recorded premise, stated in `portfolio.json`, not an inference.
- Deterministic level only. Older applications with no recorded cases will
  need the inferred level (code analysis / semantic discovery), which stays
  review-candidate-only by doctrine and is not built yet.
- Adoption in the main corpus is a proxy (recorded resolution evidence);
  the closure revision's adoption carries a receipt + independent
  verification instead.
- The tested lifecycle is pinned for refactoring:
  `tools/reconcile_regression.py` runs inside `check.sh` and re-derives the
  pinned counts, idempotency, chain-derived links, the defaults behaviour,
  the full closure cycle, and evidence freshness (record-hash and
  build-hash binding: if the record or the build drifts from its
  verification, the gate fails and the verifier must be re-run). The browser
  verifier itself is not executed in the gate; its committed outputs are
  re-checked instead.

## 8 · What this unlocks / what is next

- The findings store is the natural feed for the Case events reserved in
  P0.2 (`impact_finding`, `migration_decision`) - no fifth lifecycle.
- `da reconcile` (sweep + policy evaluation + migration plan) becomes a thin
  layer over this result once receipts (P1.1) upgrade the deterministic
  level portfolio-wide.
- Owner decisions: **landed** (2026-10-11, decision page). The twelve
  transition policies are set and the `review` row is disposed as pending
  work (adopt at the next revision of cadence3-wink; D-034).

## References

- Spec: `docs/14-reconciliation.md` (D-029; tightenings and defaults D-030;
  tri-state trigger and obligation states D-031).
- Fixtures and stores: `docs/experiments/reconcile-cadence/` (main portfolio
  and `closure/`).
- Closure build: `examples/cadence-wink-r2/` (revisions r2a, r2b; receipts;
  verification).
- Tool: `tools/da_sweep.py`.
