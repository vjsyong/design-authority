# 05 · Governance, versioning, and the 0.1.0 freeze

## 1 · The evolution loop (normative process)

Downstream gaps are **evidence, not commands**. The governance loop converts
evidence into governed releases through ten phases; each phase names its
required output.

| # | phase | required output |
|---|---|---|
| 1 | **Evidence** — reconstruct gap/proposal records from consumer workspaces | `docs/evolution/00-gap-evidence.md`: per-need records (need, context, runs reporting, closest artifacts, fallback used, proposals, conflicts) + semantic consolidation rules (phrasing ≠ separate need) |
| 2 | **Triage** — assume no extension; attempt existing-authority solutions first | `01-triage-decisions.md`: per-gap evaluation against the seven questions (existing solution? docs/aliases? recipe? pattern? primitive? project-local? conflict?) + classification |
| 3 | **Candidates** — smallest change per gap | `proposals/evolution/cand-*.json` + `02-candidates.md`; candidates stored separately from any published pack |
| 4 | **Adversarial review** — independent, clean-context reviewer instructed to *assume rejection* | `03-review.md`: per-candidate verdict + rationale + required actions; the reviewer re-verifies claims by execution |
| 5 | **Authority CI** — candidate applied to a candidate branch/version only | `04-authority-ci.md`: all reference-system gates, pack build + drift, convergence battery (incl. delete probes), golden sets, non-regression evidence |
| 6 | **Release** — publish beside the pinned pack, never over it | new pack directory + provenance overlay + release metadata; both the pinned and candidate packs remain comparable |
| 7 | **Re-runs** — fresh consumers against the new release, needs phrased semantically (never by new artifact names) | run records: outcomes, call counts, whether previously unresolved needs now resolve, whether duplicate gaps are filed |
| 8 | **Migration** — point the new authority at old implementations | `05-migration.md`: per-usage mapping (superseded local → applying artifact, direct vs manual) |
| 9 | **Inflation** — measure growth | raw dimensions: counts before/after, modified entries, vocabulary width; **no composite score** |
| 10 | **Evaluation** — close or falsify the loop | `06-final-report.md`: gap closure, convergence, recurrence, regression, inflation, review value, provenance, migration, usefulness; threats to validity disclosed |

### Classification taxonomy (phase 2)

`EXISTING-SOLUTION` | `DOCUMENTATION-FIX` | `RECIPE` | `PATTERN` |
`PRIMITIVE` | `PROJECT-LOCAL` | `REJECT` — preference strictly follows the
**abstraction ladder**: documentation < recipe < pattern < primitive. A gap
MUST NOT be classified above the smallest rung that can close it.

### Upstream review verdicts (phase 4)

`ACCEPT` | `REVISE` | `REJECT` | `DOWNGRADE` — where DOWNGRADE moves a valid
proposal one rung down the abstraction ladder. (Distinct from the consumer
proposal verdicts `accept|reject|needs-info` of `04-interfaces.md`.)

### Provenance requirements

Every pack entry introduced or modified by the loop MUST carry a provenance
block: `introduced_in`/`extended_in`, `triggering_gaps` (record ids),
`review_decision`, `source_commit`, `tests`. The release as a whole MUST carry
release metadata in `BUILD.json.release`. The system MUST make it possible to
answer, from the pack alone: *why does this artifact exist?*

### Release requirements (phase 5 gate list)

1. reference-system gates green on the candidate branch (build checks,
   strict lint, unit tests, browser suite — zero drift on additive changes);
2. pack builds deterministically from the candidate snapshot, drift gate
   passes, and the pinned pack remains byte-identical;
3. convergence battery passes with its defined per-group contract, including
   non-regression and delete-probe batteries;
4. golden sets: pinned set passes against the pinned pack; the candidate pack
   carries its own extended set;
5. the release is additive by preference; any semantic change to existing
   entries is enumerated and justified in review notes.

## 2 · Version layers

| layer | example | changes when |
|---|---|---|
| **System** (this spec) | `0.1.0` | the frozen semantics/interfaces change |
| **Format** (pack schema) | `0.1` | the data model changes (manifest `format_version`) |
| **Authority** (pack content) | `0.12.1` → `0.13.0-experiment` | content/governance releases |
| **Snapshot** (reference system pin) | `e374f38` / v0.12.1 | never within one pack version |

Consumers MUST ignore unknown keys. A kernel SHOULD refuse packs whose
`format_version` it does not support; a pack version is immutable once tagged
or released — corrections ship as a new version.

## 3 · The 0.1.0 freeze

**Design Authority 0.1.0** is frozen by this declaration, effective
2026-10-07, carried by the repository tag **`v0.1.0`** and the checksum
manifest `docs/spec/freeze-0.1.0.sha256` (SHA-256 of every frozen file at the
tagged commit).

**Frozen surface:**

- `docs/spec/00-index.md` … `05-governance-and-freeze.md` (this spec set);
- `kernel/design_authority/*.py` (pack, resolve, validate, records, cli,
  mcp_server — the semantics of sections 1–3 of the spec);
- `tools/da.py`, `tools/da-mcp.py` (entrypoints);
- `tools/build_pack_triage.py` (reference pack builder, incl. the provenance
  overlay semantics).

**Remains evolvable without a spec change:** pack contents and new packs;
curation layers; new validators declared per pack; golden/convergence test
additions; benchmark, experiments, and documentation; bug fixes that preserve
the frozen semantics (patch releases `0.1.x`).

**Change control:**

- *Editorial* clarifications to this spec → patch release (`0.1.x`),
  noted in the repo changelog.
- *Semantic* changes (pipeline order, thresholds, record formats, tool
  contracts, governance taxonomies) → new minor version (`0.2`) justified in
  the decision log (`docs/02-decisions.md`), with a fresh freeze and manifest.
- The frozen reference implementation MUST keep passing the conformance
  evidence of `00-index.md` (unit tests, golden suites, convergence battery)
  for as long as the freeze is claimed.

**Evidence base (informative):** the freeze crowns two completed experiments —
the A/B/C authority benchmark (`docs/08`–`docs/10`) and the authority-evolution
loop (`docs/evolution/00`–`06`), which produced the reference 0.13-experiment
pack with provenance intact.

## 4 · Non-goals for 0.1

Explicitly out of scope: public catalogue/marketplace; authority authoring
studios or GUIs; Figma or design-tool integrations; multi-user collaboration;
generic Git governance UI; site reverse engineering; authority inheritance;
theme swapping; organisation/RBAC models; multi-authority arbitration; a
universal design ontology. These MAY be proposed in future versions; they MUST
NOT be silently folded into 0.1 semantics.
