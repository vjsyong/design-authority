# x05 · Enforcement rebuild — making validation real and mandatory (pilot-validated)

- **Date:** 2026-10-09. Builds on `process-audit.md` §3 (hollow enforcement:
  the canon shipped zero validators, so `validate` was vacuous; the protocol
  never required it).
- **Scope:** additive only. The sealed run, its pre-registration, and every
  sealed checkpoint are untouched; the authority kernel is untouched. New
  files and new pack version only.
- **Owner decision:** stricter-than-advisory — *repair-or-file*: validate
  runs as the last step of a session; every error finding must be repaired
  (re-validated) or filed as a gap, or the session is recorded
  non-compliant.

## What was built

1. **`bookmarks-lint v1`** (`tools/bookmarks_lint.py`) — the authority's
   first real validator: a stdlib-only scanner emitting the kernel's
   lint-json shape. Checks: **B001** new raw colour literals outside
   `:root` (delta rule, see calibration); **B002** baseline QA hooks
   (missing → error; new hooks ignored); **B003** canonical storage key
   `bookmarks.v1`; **B004** warnings — token definitions outside `:root`,
   new duplicated treatment blocks.
2. **Pack `base-0.1.1-experiment`** (`annexes/packs/base-0.1.1-experiment`,
   staged in `x05/materials/packs/`) — canon files **byte-identical** to
   `0.1.0-experiment`, plus `validators.json`, `lint/bookmarks_lint.py`,
   `lint/baseline.json`. Built deterministically by
   `tools/x05_build_validated_pack.py` (baseline generated from sealed seed
   f3 with the same scanner the enforcement uses).
3. **Protocol rev2** (`annexes/protocol-rev2.md`) — rev1 plus a new §4
   "Validate before handing off": run `./run-authority validate .` last;
   repair-or-file every error; record the summary under `## Validation` in
   HANDOFF. Diff vs rev1 = pure addition.
4. **Runner additions** (`tools/x05_run.py`, all optional fields; absent =
   old behavior): `--pack canon-v` mounts the validated pack; `--from-seal`
   starts a pilot from any sealed checkpoint; `--protocol2` stages rev2;
   `--enforce` runs the post-seal validation pass + compliance check and
   records both in `run.json` and `extraction/`.
5. **`tools/x05_validate.py`** — validate (one checkpoint, `--write`
   records `extraction/validation.json`), sweep (all seals), and
   compliance modes. Compliance = (a) ≥1 `validate` call inside the session
   window (from the wrapper's audit trail) **and** (b) every error finding
   on the sealed workspace is repaired (gone) or matched by a gap filed
   after session start. Computed from sealed artifacts, never from
   self-reports.

## Calibration decisions (recorded)

- B001 is a **delta** rule against the seed's literal set — absolute purity
  would flag the seed itself 10× (seed genuinely contains
  `#fff`/`#991b1b`/`#fef2f2`/`rgba(20,24,33,…)` literals) and score every
  checkpoint ≤ 0. The delta form is the enforceable reading of B001 and
  produced a clean signal (only the A chain introduces new literals).
- B002 baseline = the seed's 27 hooks; extras ignored (briefs add hooks by
  design). f1 legitimately predates those hooks (see sweep doc).
- No tuning was applied after seeing sweep or pilot results.

## Verification

**Unit/mutation battery (all pass):** clean copy → 0 findings; injected raw
colour → B001 caught with line; hook removed → B002 caught; storage key
broken → B003 caught; compliance cases — no validate call → NON-compliant;
validate+clean → compliant; validate+unrepaired error → NON-compliant;
validate+error+**filed gap** → compliant; pre-session gap or pre-session
validate call → correctly ignored.

**Sandbox smoke:** the exact runner `bwrap` invocation runs
`./run-authority validate .` inside containment: `validator base-lint: ok`,
score 100, audit line written.

**Retrospective sweep (17 seals):** see `retrospective-validation.md` —
only chain A accumulates new-literal drift (h3×1, h4×2, score 74 at h4a).

**Live pilot (`x05/pilot/run/pv1`, excluded from analysis):** condition C,
from sealed seed f3, protocol rev2, validated pack, budget 600 s.
- Session: exit 0, 94 s, 39 tool calls, 1.1 M tokens (mostly cache).
- Agent complied with rev2 exactly: todos listed "Run ./run-authority
  validate and handle findings"; authority sequence
  `resolve → inspect ×2 → search ×2 → gap-add → validate → propose →
  validate` (final authority action = validate); both validate calls rc 0,
  output `validator base-lint: ok / findings: 0 … score=100`; added the
  `list-count` hook + "Showing X of Y" line; committed (ad7875d);
  `### Validation` section in HANDOFF quoting the output.
- Runner (independent): post-seal validation — 0 findings, score 100;
  **compliance: YES (validate_calls=2, unfiled_errors=0)**, recorded in
  `extraction/compliance.json`.
- Dry run `pv0` (skip-agent) exercised the same pipeline and correctly
  produced NON-compliant ("no validate call in the session window").
- Evidence copies: `analysis/enforcement-pilot/` (validation.json +
  compliance.json for pv0/pv1). Raw run tree remains in `x05/pilot/`.

## Breakage guarantees (checked)

- Kernel untouched → triage authority smoke passes (overview loads,
  0.12.2); no MCP/review-app impact.
- Old pack `base-0.1.0-experiment` behavior unchanged (still validator-less
  by design — that stays the sealed experiment's pack).
- Runner changes are opt-in fields/flags; every pre-existing entry type
  renders with identical behavior (defaults preserved).
- Sealed 17 + all prior analyses byte-untouched.

## Using it next

For a future enforced arm: sessions mount pack `canon-v`, stage
`protocol-rev2.md`, and set `enforce_validation: true` (pilot flags
`--pack canon-v --protocol2 --enforce`); after each seal run
`x05_validate.py validate --write` + `compliance` (the runner does this
automatically when enforced). A full enforced drift arm (4 handoffs) needs
its own pre-registration addendum before it runs — not yet written,
not yet run.

Residual notes: pilots carry no chain-diff stats (extraction reports
`prev: null`, "first of chain") — irrelevant to enforcement, noted for
completeness.
