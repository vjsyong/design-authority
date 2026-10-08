# Experiment 01 · Semantic discovery for authority records

Status: **pre-registered**. The plan, datasets and decision rules below were
frozen before any hybrid (FTS5 + embeddings) result was produced. Results are
appended in section 6 after the runs. Any addition made after seeing results is
marked `post-hoc`.

## 1. Question

The frozen resolver is deterministic and lexical. It is exact, citable and
byte-recomputable, and it deliberately returns UNDEFINED rather than guessing.
The known cost is recall on paraphrase: a consumer who describes a need in
different words gets a structured miss. This experiment asks whether an
optional, non-authoritative retrieval layer can close that gap without ever
changing what counts as authority.

Stack under test (as proposed in review):

- lexical leg: SQLite FTS5 (BM25) over rendered search documents
- semantic leg: FastEmbed `BAAI/bge-small-en-v1.5` (ONNX, CPU, 384-d), cosine
  over an in-memory matrix (brute force; the packs are small)
- fusion: Reciprocal Rank Fusion (RRF, k=60) of the two ranked lists
- determination: unchanged. The existing resolver decides RESOLVED, COMPOSE,
  FALLBACK, UNDEFINED, CONFLICT. Retrieval proposes; it never establishes.

## 2. Engines compared

- **E0 · lexical (baseline)**: the kernel's weighted lexical search
  (`pack.search`) and the frozen resolver, exactly as shipped.
- **E1 · FTS5 only**: the new index's BM25 leg alone (informational).
- **E2 · hybrid**: RRF(FTS5, semantic) top-k candidates (the feature).
- **E2+ · assist**: `resolve --assist semantic`; the frozen outcome plus a
  retrieval block (attached on UNDEFINED). Outcome classes must be identical
  to E0 for every query; only the payload grows.

## 3. Datasets

- **D1 goldens** (`packs/triage/golden.json`, 56 cases): expected outcome and
  id, hand-written and shipped with the pack.
- **D2 coverage sweep** (`docs/synthesis/triage/coverage.json`, 134 cases):
  element-by-element asks with expected ids.
- **D3 paraphrase (held out, new)**: 24 purpose-phrased asks, authored for
  this experiment, expected ids assigned without running any engine. Wording
  deliberately avoids the canonical vocabulary (aliases, titles).
- **D4 hard negatives (new)**: 8 asks with ids that must NOT appear in top-3
  (destructive controls for benign selection, scheduling and delivery surfaces
  for out-of-band messaging, non-canon patterns for common asks).

D3 and D4 are frozen in `datasets/paraphrase.json` and
`datasets/hard-negatives.json` in this directory.

## 4. Metrics

- **top-3 recall**: fraction of labeled cases where the expected id is in the
  engine's top-3. Primary comparison: E0 vs E2 on D3 (paired, same queries).
- **false RESOLVED**: resolver returns RESOLVED with an id the label
  contradicts. Must stay 0 in every arm.
- **rescuable UNDEFINED**: cases where E0 resolves UNDEFINED (a miss) and E2
  surfaces the expected id in its top-3. Reported as a rate over D3 and as a
  per-case list. This is what an agent could recover by inspecting candidates.
- **assist class safety**: for every query in D1 to D4, the outcome class with
  `--assist semantic` must equal the outcome class without it. Any difference
  fails the experiment (hard gate, no threshold).
- **negative retrieval**: forbidden ids in top-3 on D4 (E0 and E2 both
  reported; the assist must not add any new violations).
- **latency**: E0 search ms; E2 query ms warm (sidecar), one cold-start number;
  index build seconds; index size MB. Budgets below.

## 5. Hypotheses and decision rules

- **H1 (recall)**: E2 top-3 recall on D3 exceeds E0 by at least 10 percentage
  points (absolute).
- **H2 (safety, hard gate)**: assist class safety holds with zero exceptions,
  and false RESOLVED stays 0 in both arms on D1 to D4.
- **H3 (rescue)**: at least a quarter of E0's UNDEFINED cases on D3 have their
  expected id inside E2's top-3.
- **H4 (budget)**: warm E2 query p50 <= 60 ms and p95 <= 120 ms; cold first
  query (model load included) <= 8 s; index build <= 120 s; index <= 30 MB.

**Decision**: ship the assist as an optional, off-by-default extension iff H2
holds absolutely and (H1 or H3) holds and H4 is within budget. If H2 fails, do
not ship, regardless of recall. If H1 and H3 both fail, document the negative
result and keep the lexical path as the only retrieval.

## 6. Results

Run of 2026-10-08 against `packs/triage` v0.12.1, index built 2026-10-08
(`~/.design-authority/search/triage@0.12.1.sqlite`, 0.56 MB, 114 docs:
108 canonical + 6 history). Raw evidence:
`01-semantic-retrieval-results.json` and `01-semantic-retrieval-d3-detail.json`
in this directory. Two D3 cases were used as implementation probes before the
run and are excluded from the formal statistics (amendment 1, recorded in the
dataset file).

### 6.1 Top-3 recall (paired, same queries)

- D1 goldens, n=53: E0 53 / E1 53 / E2 53
- D2 sweep, n=134: E0 134 / E1 133 / E2 134
- D3 paraphrase, n=24 (formal n=22): E0 13 / E1 10 / E2 11

**H1 fails.** On paraphrase, the hybrid does not beat lexical top-3 recall by
10 points; it trails it (11 vs 13 of 22, both far from the 22 ceiling). The
hybrid caught two records lexical search missed (combobox, avatar) and dropped
four lexical had found, all below-threshold cases where the resolver stays
UNDEFINED either way. The paraphrase gap at this scale is not fixed by a
33M-parameter embedding model. A post-hoc spot check with `bge-base-en-v1.5`
(768-d) scored 95.7% vs 96.8% for the small model on D1+D2 and did not repair
the probes, so the pinned small model was kept.

### 6.2 Authority safety (assist on) and false resolutions

24 end-to-end runs (`da resolve --assist semantic`, one per D3 query, real
CLI): **zero outcome-class changes** and zero assist-induced false
resolutions. H2 holds with one caveat the metric surfaced: the frozen resolver
itself resolved three new wordings to a wrong record (panel→`pattern/viewer`
instead of `component/sheet-end`; status label→`guideline/voice` instead of
`component/badge`; row chevron→`component/menu-item` instead of
`component/menu-pop`). The assist arm inherited exactly those three and added
none. That is resolver behaviour on unseen phrasing, pre-existing and now
measured; the assist cannot create or suppress an outcome class.

Baseline on D3: 18 UNDEFINED, 6 RESOLVED (3 wanted, 3 not).

### 6.3 Rescue of UNDEFINED cases

For 10 of the 18 baseline-UNDEFINED cases (56%) the wanted record appears in
the assist's candidate list, including pure semantic captures lexical search
never reached (switch, armed delete, combobox, avatar, stepper, topbar, diff,
keycap, dropzone, segmented control). **H3 holds** (threshold was 25%). Five
cases neither engine finds (empty state, tooltip, audit trail, progress,
command palette); those are the honest remaining tail.

### 6.4 Hard negatives

Top-3 forbidden-id hits: E0 2, E1 1, E2 3. The hybrid introduced two the
lexical engines did not have, and they are exactly the reviewed risk:
"pick a reviewer from the team directory" surfaced `component/bulkbar`, and
"scheduled message" surfaced `component/msg`. Both are plausible neighbours,
jurisdictionally wrong, and they are why the assist is retrieval-only,
canonical-only by default, and every response carries an inspect-first note.
E0's own two ("auto-save"→savebar; "carousel"→img) show the lexical engine is
not clean on negatives either.

### 6.5 Latency and footprint

E0 search 0.37 ms avg; E2 warm p50 12.6 ms, p95 17.7 ms; cold CLI query 1.02 s
(model load included); index build 3.6 s; index size 0.56 MB. **H4 fully met.**
The modelled cost is per-workspace, not per-query: build once per pack release,
reuse a warm embedder in long-lived servers.

### 6.6 Decision

Per the pre-registered rule: H2 held (zero assist-induced changes; caveat
recorded), H3 held (56% rescue), H4 met; H1 failed. **Ship as an optional,
off-by-default retrieval extension** — `da discover`, `da resolve --assist
semantic`, and the `discover_candidates` MCP tool — with H1's failure stated
prominently: this does not fix paraphrase recall at the top-3 level, it gives
an inspector-facing candidate list that rescues a majority of resolve-level
misses. The lexical path remains the default everywhere, and the D4 failure
mode is part of the shipped documentation.

Threats to validity: two D3 probes seen during implementation (excluded from
formal stats); D3 labels authored by the same person who built the pack;
single pack, single corpus size; embedding models compared only as a spot
check; RRF constant and k fixed a priori and not tuned.

