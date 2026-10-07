# 03 · Resolution semantics

Normative algorithm of `resolve(pack, problem, context)`. Thresholds and
ordering are **frozen** in 0.1. The kernel MUST be deterministic: no network,
no time/locale dependence, stable ordering, and every cited id validated
against the pack before the answer is returned.

## Tokenization and stemming

Applied identically to queries and index text:

1. lowercase; extract tokens matching `[a-z0-9][a-z0-9-]*`;
2. drop STOPWORDS (articles, pronouns, modals, and common request verbs such
   as add/show/need; the full frozen list lives in `pack.py`) and any
   single-character token;
3. stem (`_stem`): if length > 3 — strip trailing `able` when length > 7
   (`searchable → search`); else strip a trailing `s` unless the token ends
   `ss|us|is`; then strip a trailing `e` when length > 3.

Single-token queries containing stopwords (`"combobox"`) are unaffected; long
queries lose their glue words by design.

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

`score = Σ token weights + 5.0 × (number of phrases whose all tokens occur in
the query)`. Single-token phrases match only by exact query equality. Scores
are rounded to 2 decimals; results sort by `(−score, id)` — **id is the tie
breaker**, giving byte-stable output.

## Outcome pipeline (evaluated strictly in order)

### 1 · CONFLICT

If any prohibition matches the problem — `detect: color_literal` regex, a
`signals` substring, or a full `signals_all` group — the outcome is CONFLICT:
cite the prohibition (+ its rule with severity/summary/fix when present), the
detection reason, and the manifest's `policy.on_conflict`. Stop.

### 2 · RESOLVED

Search all entries (limit 8). **Artifact hits** exclude recipes, fallbacks and
prohibitions. Let `a_best` be the top artifact hit and `runner` the second.
RESOLVED requires:

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

## Output shape

All outcomes return: `outcome`, `problem`, `context` (echoed), `resolution`,
`alternatives` (top-3 artifact hits, never including the cited item),
`evidence`, `authority` (`{authority, version, commit}` identity), and `next`
guidance. `resolution` holds exactly one primary key: `artifact`, `recipe`
(+`ingredients`), `fallback`, or `prohibition` (+`rule`, `detected`), except
UNDEFINED which holds `closest` instead. Every id in an answer MUST exist in
the pack.

## Golden sets

`resolve_golden(pack, cases)` runs `{problem, expect, expect_id?, note?}`
cases and reports agreement (rate + per-row detail). Golden sets are
conformance evidence, not part of the algorithm; they live with the pack.

## Frozen constants (0.1)

```
DIRECT_MIN    = 6.5   direct artifact hit threshold
DIRECT_MARGIN = 2.0   lead over the runner-up required for RESOLVED
COMPOSE_MIN   = 5.0   recipe threshold for COMPOSE
PHRASE_BONUS  = 5.0   per fully-matched phrase
```
