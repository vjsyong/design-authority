# 01 · Definitions

Normative glossary for Design Authority 0.2. Terms appear in the form used by
the specification; code and file names may use snake_case equivalents.

## Authority and packs

- **Authority** — a design system expressed as a governed, machine-readable
  contract (a *pack*) served by tooling, rather than as prose documentation
  alone.
- **Authority Pack (pack)** — a directory of JSON files conforming to the
  data model; the unit of publication, versioning, and citation.
- **Manifest (`authority.json`)** — the pack's self-description: identity,
  `format_version`, content `version`, the pinned **snapshot**, declared kinds,
  capabilities, policy, and entrypoints.
- **Reference System / Snapshot** — the real design system a pack is compiled
  from, pinned by repository, branch, and commit (`snapshot` block). The
  snapshot is immutable for the lifetime of a pack version.
- **Curation Layer** — hand-authored inputs (`curation/`) composed with the
  snapshot by the pack builder (aliases, recipes, fallbacks, guidelines notes,
  docs maps, and the evolution provenance overlay). Curation is the human
  editorial surface; it MUST NOT contradict the snapshot.
- **Kernel** — the kit-agnostic implementation of the format and semantics
  (load, search, resolve, validate, records, MCP, CLI).
- **Format Version** — the schema version of the pack data model; `0.1` for
  this specification (including its additive extensions). Declared in the
  manifest as `format_version`.

## Artifact vocabulary

- **Artifact** — any citable entry in the pack. Top-level kinds: `component`,
  `pattern`, `token-set`, `guideline`, `example`, `reference` — plus the
  governance kinds `rule`, `recipe`, `fallback`, `prohibition`. The pack
  additionally defines two guidance entry kinds outside `artifacts.json`:
  `precedent` and `candidate` (0.2).
- **Component** — a concrete UI element with a class contract, states, and
  accessibility notes (e.g. `component/select`).
- **Pattern** — a recurring page- or flow-level arrangement (e.g.
  `pattern/detail`).
- **Token-set** — a named group of design tokens (colour, spacing, motion).
- **Guideline** — a rule of practice with do/don't lists and a source quote
  (e.g. `guideline/high-stakes-confirm`).
- **Example / Reference** — worked examples and external references.
- **Rule** — a deterministic, enforceable constraint with severity, scope,
  rationale, and fix (e.g. `TDS003`). Rules are enforced by validators.
- **Recipe** — a sanctioned composition of existing artifacts that answers a
  recurring *need* (e.g. `recipe/assign-picker`): `needs` phrases, `ingredients`
  (cited artifact ids), `constraints`, and `evidence` (source + quote).
- **Fallback** — a scoped, sanctioned degrade path for a stated scope of needs
  (e.g. `fallback/native-control`).
- **Prohibition** — an explicit "never" with detection signals; triggers the
  CONFLICT outcome (e.g. `prohibit/rounded-corners`).
- **Negative Precedent** — a *policy decline* recorded as guidance, not a dead
  end: `{id, title, request, matches, decision, grounds, reason,
  scope{domains, boundary}, try[], citation?}`. `grounds`, `scope.domains` and
  `scope.boundary` are mandatory and non-empty; `try` lists the routes to take
  instead (see `02-pack-format.md`). Precedents are attached to resolutions and
  warnings with a **scope verdict** — they never change an outcome.
- **Candidate** — a provisional direction with partial evidence. Explicitly
  NOT authority: consumers may adopt it only as a *marked* starting point.
  Carries `promote_when` — the named evidence whose capture turns it into a
  proposal (see `05-governance-and-freeze.md`).
- **Validator** — a declared command that produces findings over a target path,
  with a normalized output shape (see `04-interfaces.md`).
- **Finding** — one normalized validator result: rule, severity
  (error|warning|info), message, location, fix, excerpt.

## Resolution vocabulary

- **Need** — a design problem stated in natural language by a consumer.
- **Resolution** — the deterministic, cited answer to a need: exactly one of
  the outcomes CONFLICT, RESOLVED, COMPOSE, FALLBACK, UNDEFINED (evaluated in
  that order), plus optional precedent/candidate *attachments* (0.2).
- **Outcome**
  - **CONFLICT** — the need violates a prohibition; do not implement as
    requested; the answer cites the prohibition and its rule.
  - **RESOLVED** — one artifact directly defines the answer; the answer cites
    it with evidence (score, matched tokens, threshold).
  - **COMPOSE** — no single artifact defines it, but a sanctioned recipe does;
    the answer cites the recipe, its constraints, and its ingredients.
  - **FALLBACK** — a scoped fallback covers the need; implement per the
    fallback and mark the improvisation.
  - **UNDEFINED** — no sanctioned answer exists. This is a *structured
    success*, not an error: the answer carries closest candidates, a search
    trace, the fallback policy, and the gap-report instruction.
- **Citation** — an id that exists in the pack; the kernel MUST validate every
  cited id before returning an answer (ids are never fabricated).
- **Alias** — an authored search term for an artifact. Multi-word aliases are
  also **phrases**.
- **Need Phrase** — an entry in a recipe's `needs`; matches as tokens (3.0
  weight) and as a phrase (+5.0 when all its tokens are present in the query).
- **Search Score** — the sum of per-token weights (max weight per token over
  all fields) plus phrase bonuses; deterministic, rounded to 2 decimals.
- **Phrase Bonus** — +5.0 awarded when a phrase's tokens all occur in the
  query (or the whole query equals a single-token phrase).
- **Stopword / Stem** — tokenization normalizations applied identically to
  queries and index (see `03-resolution-semantics.md`).
- **Scope Verdict** — the per-ask relationship between a negative precedent
  and a need: `governs` (inside the decline's scope — may be treated as
  declined; follow the try list) · `outside` (the ask touches only the
  decline's *boundary* vocabulary — explicitly NOT governed; proceed as an
  ordinary marked improvisation) · `ambiguous` (scope domains and boundary
  both touched — improvised unless a human rules).
- **Precedent Attachment** — matching precedents (≤2) attached to any
  resolution as annotation; each brief carries `{id, verdict, title, grounds,
  reason, try, boundary, citation?}`. Attachments annotate; they NEVER change
  the outcome.
- **Candidate Attachment** — matching candidates (≤2) attached on UNDEFINED
  only; they mark the provisional direction alongside the structured
  undefined answer.

## Records and governance vocabulary

- **Gap Record** — a recorded, noncanonical statement that the authority does
  not (adequately) cover a need: need, context, authority identity, attempted
  resolution, fallback used, evidence (see `04-interfaces.md`). Since 0.2 it
  also carries `precedent_warnings` / `candidate_hints` when the need touches
  a decline or a candidate.
- **Proposal Record** — a noncanonical extension candidate attached to a gap;
  required fields: problem, insufficiency, reuse_case, composition_check,
  proposed, tests. Since 0.2 it also carries `precedent_warnings` /
  `candidate_hints`.
- **Consumer Review Verdict** — the verdict surface for proposals reported by
  consumers: `accept` | `reject` | `needs-info`. Recording a verdict updates
  the proposal's `status` and `review` block; nothing is ever auto-applied.
- **Upstream Review Verdict** — the verdict surface for the governance loop's
  adversarial review: `ACCEPT` | `REVISE` | `REJECT` | `DOWNGRADE`
  (DOWNGRADE = valid in spirit, move one rung down the abstraction ladder).
- **Precedent Warning** — on gap/proposal records: the negative precedents the
  need or proposal matched at creation time (`{id, verdict}` pairs), so the
  filer — and the loop — see the decline before acting.
- **Candidate Hint** — on gap/proposal records: the candidates the need or
  proposal matched at creation time.
- **Lenient Adjudication** — the owner doctrine (2026-10-07, adopted in 0.2):
  declines are a last resort reserved for grounded policy (asset law, motion
  doctrine, prohibitions, off-grammar geometry) with a sanctioned alternative;
  evidence-insufficient asks DEFER to undefined; partial evidence becomes a
  candidate. Reviewer rejections stand and are never re-classified.
- **Candidate Lifecycle** — candidate → capture the evidence named in
  `promote_when` → proposal → owner verdict → codified in a new pack version.
  A candidate is never presented as canonical.
- **Classification** — the upstream triage's category for a consolidated gap:
  `EXISTING-SOLUTION` | `DOCUMENTATION-FIX` | `RECIPE` | `PATTERN` |
  `PRIMITIVE` | `PROJECT-LOCAL` | `REJECT`. Preference order is the
  **abstraction ladder**: documentation < recipe < pattern < primitive.
- **Provenance Block** — the audit attachment on a changed pack entry:
  `introduced_in`/`extended_in`, `triggering_gaps`, `review_decision`,
  `source_commit`, `tests`. Answers "why does this artifact exist?".
- **Release Metadata** — `BUILD.json.release`: label, kind, experiment, based_on,
  source_branch, evidence, review.
- **Authority Inflation** — growth in normative surface area required to close
  observed gaps, reported as raw dimensions (counts, modified entries,
  vocabulary width). No composite score is defined in 0.1 or 0.2.
- **Golden Set** — a list of `{problem, expect, expect_id?, note?}` cases; the
  agreement rate is part of conformance evidence.
- **Convergence Battery** — a full-phrasing assertion set run against a
  candidate release (per-group expected outcome+id mapping), including
  non-regression and delete-probe batteries.
- **Freeze** — a tagged, checksummed state of this specification and the
  reference kernel; see `05-governance-and-freeze.md`.
