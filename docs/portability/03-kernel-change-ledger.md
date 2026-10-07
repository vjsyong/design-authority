# Portability Spike · 03 · Kernel change ledger

Every time the second authority suggests the kernel needs modification, the
entry is recorded here **before** any change. Outcomes:
`PACK-SOLVABLE` · `GENERIC-KERNEL-DEFICIENCY` · `TRIAGE-ASSUMPTION` · `DEFER`.

Strong bias per protocol: solve differences in the authority pack, not in the
kernel. A kernel change is justified only if it improves the abstraction for
multiple possible authorities. Any authority-specific branch is a portability
failure unless explicitly documented and justified.

---

## KCL-001 · Validators cannot reference their own pack

- **Problem:** `validators.json` commands are executed with a `workdir` that
  supports exactly one substitution: `{snapshot}` (the pinned reference-system
  checkout). Orbit *has no snapshot repository* — it is derived from a
  document, not compiled from a code repo — so there is no honest value for
  `{snapshot}` and no way to point the validator at a pack-local script.
- **Why the pack cannot express it:** the pack format has no mechanism to say
  “this validator lives inside the pack” (`{pack}` is not a supported
  substitution in `workdir` or `command`).
- **Current kernel assumption:** validators live inside the pinned snapshot
  repository and are invoked from its directory (`validate.py: _run_one`).
- **Is it genuinely generic?** Yes — “a pack may ship its own validator
  scripts” is a first-class need for any self-contained authority, not a
  Triage-ism. The *assumption* that validation runs over a snapshot repo
  tree, however, is **Triage-derived** (its linter lives in the design
  repo by construction).
- **Could the authority pack solve it instead?** Partially — a pack can point
  `workdir` at a literal absolute path (non-portable, machine-specific) or
  depend on `DA_SNAPSHOT` being set to an arbitrary directory (dishonest —
  there is no snapshot). Neither is a real solution.
- **Proposed change:** support `{pack}` substitution in validator `workdir`
  and `command` arguments (`workdir.replace("{pack}", pack.path)`), additive
  and generic; `{snapshot}` keeps working for Triage. No authority-specific
  code, no branching.
- **Impact on Triage:** none (its validators use `{snapshot}`, unchanged
  behaviour; the substitution is added alongside).
- **Decision:** `GENERIC-KERNEL-DEFICIENCY` — **implemented** as proposed, in the
  minimal additive form: `{pack}` (pack directory) is now substituted in
  validator `workdir` and `command` args, alongside `{snapshot}` and
  `{target}`. No authority-specific branching; Triage's `{snapshot}` path is
  byte-identical in behaviour. A second, smaller generic fix rode along: the
  parser name `"lint-json"` is now accepted as the shape name (the legacy
  name `"triage-lint-json"` still works — it describes the same report
  shape, which is SARIF-aligned and produced by both authorities' linters).
  Evidence: kernel unit tests 10/10 after the change; Orbit validator runs
  end-to-end through `da validate` (`packs/orbit/validators/orbit_lint.py`,
  workdir `{pack}`), and the Triage path is unaffected (same substitution
  semantics; its validators still use `{snapshot}`).
- **Ledger ref:** this entry is the spike's only required kernel change so
  far; both edits live in `kernel/design_authority/validate.py`.

## KCL-002 · Required `kind` fields hidden by the curation pipeline

- **Problem:** hand-authoring a pack directly (Orbit's route) requires
  explicit `"kind"` on `recipe`, `fallback`, and `prohibition` entries. The
  Triage pipeline never surfaces this: curation files omit `kind` and
  `build_pack_triage.py` injects it, so first-pass Orbit entries silently
  loaded as `kind: "?"` — recipes never COMPOSEd and fallbacks leaked into
  artifact search.
- **Why the pack cannot express it:** n/a — the pack *must* express it; the
  format (spec `02-pack-format.md`) already requires `kind`. This was an
  authoring defect on our side, not a format gap.
- **Is it genuinely generic?** The requirement is format-level and correct.
  The confusion is tooling ergonomics: a curation format that differs from
  the built format.
- **Could the authority pack solve it instead?** Yes — corrected in the pack
  (all entries now carry `kind`).
- **Proposed change:** none to the kernel. Optional future ergonomics: the
  loader could *warn* on entries with missing `kind` instead of defaulting to
  `"?"`. Not proposed now (would not change semantics).
- **Impact on Triage:** none.
- **Decision:** `PACK-SOLVABLE` (resolved; pack fixed, golden re-verified).

## Watchlist (probe targets for Phases 6–7, not kernel findings yet)

Differences from Triage worth deliberately probing later:

- **Feedback semantics:** Orbit has no `recipe/status-with-text` analogue;
  status = `component/indicator` + `pattern/job-view` (different vocabulary
  and shape for the same need).
- **Destructive actions:** Orbit routes deletes through
  `recipe/destructive-confirm` (dialog), Triage through armed-entity-delete —
  the kernel must say “this authority says dialog confirm”, not “Triage says
  arms”.
- **Motion:** Orbit has none (deliberate UNDEFINED); Triage ships motion
  tokens. A motion request against Orbit should UNDEFINE cleanly.
- **Radius:** both systems are square (Triage by prohibition, Orbit by
  derivation) — radius cannot differentially probe them; the *phrasing*
  probes (e.g. “rounded buttons”) must still CONFLICT per this authority’s
  own signals.
- **Vocabulary:** Orbit elements are named `command/entry/chooser/…` —
  nothing may assume Triage codes (`btn`, `cb`, `tbl`).
