# 05 · Governance, versioning, and the freezes

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

### Lenient adjudication (0.2)

Owner doctrine, adopted with 0.2: **be lenient with denies.** Three rungs
replace the blunt decline:

| rung | when | what happens |
|---|---|---|
| **Candidate** | partial evidence; a direction exists but is not canon | recorded provisional (`candidates.json`, mandatory `promote_when`); NOT authority; promotion requires the named evidence, then proposal → owner verdict → codification |
| **Undefined deferral** | insufficient evidence | the ask stays UNDEFINED; no negative precedent; improvise in character, mark it; a gap remains open |
| **Decline** | grounded policy only (asset law, motion doctrine, prohibitions, off-grammar geometry) AND a sanctioned alternative exists | a precedent with `grounds`, scope domains, a mandatory **boundary**, and the try-list |

Hard requirements (enforced by `tools/precedent_probe.py`): every precedent
carries non-empty `grounds` + `scope.domains` + `scope.boundary`; every
candidate carries `promote_when`. Reviewer rejections are owner decisions and
are never re-classified by this leniency. Precedent matching is
scope-verdict'd (`governs` | `outside` | `ambiguous`, see `03`), so a decline
cannot silently cover asks outside its declared scope — the boundary makes
each decline's edge explicit, and `outside` means *proceed as an ordinary
marked improvisation*.

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
| **System** (this spec) | `0.3.0` | the frozen semantics/interfaces change |
| **Format** (pack schema) | `0.1` | the data model changes (manifest `format_version`; 0.2 adds only optional additions under it) |
| **Authority** (pack content) | `0.12.1` → `0.13.0-experiment` | content/governance releases |
| **Snapshot** (reference system pin) | `e374f38` / v0.12.1 | never within one pack version |

Consumers MUST ignore unknown keys. A kernel SHOULD refuse packs whose
`format_version` it does not support; a pack version is immutable once tagged
or released — corrections ship as a new version.

**Version history:** `0.1.0` — 2026-10-07, initial freeze. `0.2.0` —
2026-10-08, first minor bump under the change-control rule (negative
precedents + candidates, scope verdicts, lenient adjudication, tool-contract
additions; justified in D-023). `0.3.0` — 2026-10-08, second minor bump (the
lexical normalisation layer; justified in D-024).

## 3 · The freezes

### 3.1 · The 0.3.0 freeze (current)

**Design Authority 0.3.0** is frozen by this declaration, effective
2026-10-08, carried by the repository tag **`v0.3.0`** and the checksum
manifest `docs/spec/freeze-0.3.0.sha256` (SHA-256 of every frozen file at the
tagged commit). Frozen surface: the same set as 3.2, plus
`kernel/design_authority/lex.py`.

**Changes from 0.2.0 (why this bump).** One semantic addition under the
change-control rule below:

1. **Lexical normalisation layer** (`lex.py`, layer version 1). A curated
   US/UK spelling-variant table canonicalises tokens during tokenisation
   (`03`, "Tokenization and stemming"), applied identically to queries and
   index text, BEFORE stemming. Retrieval-side only: the outcome taxonomy,
   thresholds, precedence and citation rules are unchanged. Guarded,
   table-bounded reductions; canonical forms idempotent; the table is
   conflict-validated at import; every query rewrite is reported in the
   `normalized` output field. Justified in D-024.

### 3.2 · The 0.2.0 freeze (historical)

**Design Authority 0.2.0** is frozen by this declaration, effective
2026-10-08, carried by the repository tag **`v0.2.0`** and the checksum
manifest `docs/spec/freeze-0.2.0.sha256` (SHA-256 of every frozen file at the
tagged commit).

**Frozen surface:**

- `docs/spec/00-index.md` … `05-governance-and-freeze.md` (this spec set);
- `kernel/design_authority/*.py` (pack, lex, resolve, validate, records, cli,
  mcp_server — the semantics of sections 1–3 of the spec);
- `tools/da.py`, `tools/da-mcp.py` (entrypoints);
- `tools/build_pack_triage.py` (reference pack builder, incl. the provenance
  overlay semantics).

**Changes from 0.1.0 (why this bump).** All are semantic additions under the
change-control rule below:

1. **Negative precedents** (`precedents.json`): policy declines with mandatory
   grounds + scope + boundary, matched with scope verdicts
   (`governs`/`outside`/`ambiguous`) and attached to resolutions and to
   gap/proposal records (`precedent_warnings`).
2. **Candidates** (`candidates.json`): provisional directions with a mandatory
   `promote_when` evidence bar; attached to UNDEFINED resolutions
   (`candidate_hints` on records); lifecycle in §1.
3. **Lenient adjudication doctrine** (§1): declines reserved for grounded
   policy; the incumbent decline set re-classified (recorded in
   `docs/synthesis/16-lenient-adjudication.md`).
4. **Tool-contract additions:** CLI `precedents` / `precedent-check` /
   `candidates`; MCP `list_precedents` / `check_precedent` / `list_candidates`
   (10 tools); validator `{pack}` substitution and the `lint-json` parser
   name; MCP resources under the `authority://` scheme.

Thresholds, pipeline order and the outcome taxonomy are **unchanged** from
0.1.0.

**Remains evolvable without a spec change:** pack contents and new packs;
curation layers; new validators declared per pack; golden/convergence test
additions; benchmark, experiments, and documentation; bug fixes that preserve
the frozen semantics (patch releases `0.2.x`).

**Change control:**

- *Editorial* clarifications to this spec → patch release (`0.2.x`), noted in
  the repo changelog.
- *Semantic* changes (pipeline order, thresholds, record formats, tool
  contracts, governance taxonomies) → new minor version, justified in the
  decision log (`docs/02-decisions.md`), with a fresh freeze and manifest.
  (The 0.1.0 → 0.2.0 bump is the first application of this rule — D-023.)
- The frozen reference implementation MUST keep passing the conformance
  evidence of `00-index.md` (unit tests, golden suites, convergence battery,
  precedent probe, MCP smoke) for as long as the freeze is claimed.

**Evidence base (informative):** the freeze crowns four completed episodes —
the A/B/C authority benchmark (`docs/08`–`docs/10`), the authority-evolution
loop (`docs/evolution/`), the second-authority portability spike
(`docs/portability/` — Ubuntu "Indaba", PORTABLE-WITH-GENERIC-CHANGES on the
unmodified kernel, one additive kernel change, KCL-001), and the authority
synthesis experiment (`docs/synthesis/` — three candidate authorities, Gates
1–2 reviewed in-browser, Cadence stress v1–v3, adjudication + codification).
The post-freeze record is consolidated in `docs/11-consolidation-since-0.1.0.md`.

### 3.3 · The 0.1.0 freeze (historical)

**Design Authority 0.1.0** was frozen 2026-10-07, carried by tag `v0.1.0` and
the manifest `docs/spec/freeze-0.1.0.sha256`; same frozen surface as 3.2. It
was superseded by 0.2.0 on 2026-10-08. The 0.1.0 manifest preserves the exact
frozen bytes of that release.

## 4 · Non-goals (0.1–0.2)

Explicitly out of scope: public catalogue/marketplace; authority authoring
studios or GUIs; Figma or design-tool integrations; multi-user collaboration;
generic Git governance UI; site reverse engineering; authority inheritance;
theme swapping; organisation/RBAC models; multi-authority arbitration; a
universal design ontology. These MAY be proposed in future versions; they MUST
NOT be silently folded into 0.1 or 0.2 semantics.
