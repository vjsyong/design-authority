# 03 · Resolution semantics

Normative algorithm of `resolve(pack, problem, context)`. Thresholds and
ordering are **frozen** (unchanged since 0.1; the 0.3 freeze added the lexical
normalisation step to tokenisation only). The kernel MUST be
deterministic: no network, no time/locale dependence, stable ordering, and
every cited id validated against the pack before the answer is returned.

## Tokenization and stemming

Applied identically to queries and index text:

1. lowercase; extract tokens matching `[a-z0-9][a-z0-9-]*`;
2. drop STOPWORDS (articles, pronouns, modals, and common request verbs such
   as add/show/need; the full frozen list lives in `pack.py`) and any
   single-character token;
3. canonicalise (0.3): rewrite common English spelling variants to one form
   (chiefly US/UK pairs; canonical direction US) via the curated table in
   `lex.py`. Only the token itself or a guarded reduction (plural `s`;
   `-ing` / `-ed` / `-able`, each with an `e`-restore retry) can fire, so the
   table's curated space bounds every rewrite; canonical forms are idempotent
   and the table is conflict-validated at import;
4. stem (`_stem`): if length > 3 — strip trailing `able` when length > 7
   (`searchable → search`); else strip a trailing `s` unless the token ends
   `ss|us|is`; then strip a trailing `e` when length > 3.

Single-token queries containing stopwords (`"combobox"`) are unaffected; long
queries lose their glue words by design.

The normalisation layer is **retrieval-side only**: it changes token forms,
never the outcome taxonomy, the thresholds, the precedence or the citation
rules, and it cannot widen vocabulary beyond what the pack carries. Every
query rewrite is reported in the output's `normalized` field (raw → canonical
token map) so the mapping stays auditable; queries already in canonical
spelling carry no such field.

## Scoring

Per entry, the index weights fields as follows (maximum weight wins per token):

| entry type | field | weight |
|---|---|---|
| artifact | title | 3.0 |
| artifact | summary | 1.5 |
| artifact | alias | 4.0 |
| artifact | body.class | 2.5 |
| artifact | body.{states,a11y,do,dont,quote,statement} | 1.0 |
| artifact | body.group, source.path | 1.0 |
| recipe | title | 3.0 |
| recipe | summary | 1.5 |
| recipe | need | 3.0 |
| recipe | constraint | 1.0 |
| fallback | title | 2.0 |
| fallback | statement | 1.5 |
| fallback | scope token | 2.5 |
| precedent | title / request | 3.0 |
| precedent | matches (vocabulary) | 4.5 |
| precedent | reason / try | 1.5 / 1.0 |
| candidate | title | 3.0 |
| candidate | summary / request | 2.0 / 2.0 |
| candidate | matches (vocabulary) | 4.0 |

`score = Σ token weights + 5.0 × (number of phrases whose all tokens occur in
the query)`. Single-token phrases match only by exact query equality. Scores
are rounded to 2 decimals; results sort by `(−score, id)` — **id is the tie
breaker**, giving byte-stable output. Precedent and candidate entries are
indexed and searchable (kind filters `precedent` / `candidate`); the RESOLVED
stage excludes them from artifact hits.

## Outcome pipeline (evaluated strictly in order)

### 1 · CONFLICT

If any prohibition matches the problem — `detect: color_literal` regex, a
`signals` substring, or a full `signals_all` group — the outcome is CONFLICT:
cite the prohibition (+ its rule with severity/summary/fix when present), the
detection reason, and the manifest's `policy.on_conflict`. Stop.

### 2 · RESOLVED

Search all entries (limit 8). **Artifact hits** exclude recipes, fallbacks,
prohibitions, precedents and candidates. Let `a_best` be the top artifact hit
and `runner` the second. RESOLVED requires:

```
a_best.score >= DIRECT_MIN (6.5)  AND
(no runner-up OR a_best.score − runner.score >= DIRECT_MARGIN (2.0))
```

A dedicated artifact wins over a recipe by spec order: a sanctioned recipe is
the answer only when no artifact directly defines the need.

### 3 · COMPOSE

Otherwise, search recipes only. COMPOSE requires `r_best.score >= COMPOSE_MIN
(5.0)`. The answer carries the recipe (id, title, summary, constraints,
evidence) and the resolved **ingredients** (brief views; unknown ingredient
ids are omitted defensively — the builder prevents them at publish time).

### 4 · FALLBACK

Otherwise, scan fallbacks: `scope` (excluding `*`) intersected with the
normalized query token set. A non-empty intersection selects the fallback;
the evidence records the matched scope tokens. Consumers implement per the
fallback, mark the improvisation, and SHOULD report a gap if the need is
likely to recur.

### 5 · UNDEFINED

Otherwise the outcome is UNDEFINED — a structured success. The answer carries:

- `closest`: top-3 artifact hits;
- `search_trace`: queries, hits considered, top score, the threshold applied;
- `why`: human-readable account (including the top candidate's score when one
  existed);
- `fallback_policy`: allowed fallbacks + the manifest's `policy.on_undefined`;
- `next`: implement per policy, mark the improvisation, report a gap.

## Precedent and candidate attachments (0.2)

After the outcome is computed, two optional annotations attach. They NEVER
change the outcome — they record the precedent guidance and provisional
direction surrounding it.

**Precedents** (`precedents`). Scope-aware matching runs over the problem
text. A precedent matches when its `matches` vocabulary scores ≥1 under the
alias rules (single tokens ≥4 authored characters, measured before stemming;
multi-word entries only as phrases) OR when any `scope.boundary` entry hits by
the same rules. The per-ask **scope verdict** is:

- `outside` — boundary hits, no scope-domain hits: explicitly NOT governed;
  proceed as an ordinary marked improvisation;
- `ambiguous` — boundary and domain both hit: treat as improvisation unless a
  human rules;
- `governs` — otherwise (inside the decline's scope): may be treated as
  declined; follow the try-list.

Up to 2 precedents attach, ordered governs → ambiguous → outside, then by
score, then by id, briefed as `{id, verdict, title, grounds, reason, try,
boundary, citation?}`. Precedents are guidance, never a block.

**Candidates** (`candidates`). Attached on UNDEFINED only: up to 2 matching
candidates ordered by score then id, briefed as `{id, title, summary, status,
promote_when, emerges_from?}`. A candidate is provisional — consumers may
adopt it only as a marked starting point, never as canonical.

## Output shape

All outcomes return: `outcome`, `problem`, `context` (echoed), `resolution`,
`alternatives` (top-3 artifact hits, never including the cited item),
`evidence`, `authority` (`{authority, version, commit}` identity), and `next`
guidance. When the query contained spelling variants, the answer additionally
carries `normalized` (raw → canonical token map; see Tokenization and
stemming). `resolution` holds exactly one primary key: `artifact`, `recipe`
(+`ingredients`), `fallback`, or `prohibition` (+`rule`, `detected`), except
UNDEFINED which holds `closest` instead. Resolutions MAY additionally carry
`precedents` and (on UNDEFINED) `candidates` attachment arrays. Every id in
an answer MUST exist in the pack.

## Golden sets

`resolve_golden(pack, cases)` runs `{problem, expect, expect_id?, note?}`
cases and reports agreement (rate + per-row detail). Golden sets are
conformance evidence, not part of the algorithm; they live with the pack.

## Frozen constants (0.3)

```
DIRECT_MIN    = 6.5   direct artifact hit threshold
DIRECT_MARGIN = 2.0   lead over the runner-up required for RESOLVED
COMPOSE_MIN   = 5.0   recipe threshold for COMPOSE
PHRASE_BONUS  = 5.0   per fully-matched phrase
```

## Retrieval assist (0.4, optional)

0.4 adds an OPTIONAL retrieval-side assist. It is off by default and it never
establishes authority.

- `discover` (CLI) and `discover_candidates` (MCP) return candidate ids from a
  fused retrieval index (SQLite FTS5 BM25 + a local embedding model, RRF
  fusion). Candidates carry retrieval evidence only (ranks, similarity,
  fusion score). They are NOT outcomes: a similarity of 0.9 means "inspect
  this candidate", never RESOLVED.
- `resolve --assist semantic` attaches a `retrieval_assist` block when the
  outcome is UNDEFINED. The block carries the same retrieval candidates and
  an inspect-first note. The outcome, its class, its evidence and every
  citation are computed exactly as without the assist; enabling the assist
  MUST NOT change outcome classes (verified end-to-end in
  `docs/experiments/01-semantic-retrieval.md`).
- The assist searches canonical records by default; precedents and candidates
  are searched separately (`--class history`) and are never binding.
- The index is derived data: rebuilt from the pack, keyed by pack version and
  content hash, stored in the consumer's cache, never in the pack. The kernel
  itself stays stdlib-only; the assist requires optional extras (`fastembed`,
  `numpy`), and every lexical surface is unchanged without them.

