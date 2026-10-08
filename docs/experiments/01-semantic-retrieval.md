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

The frozen pre-registration above was committed at the start of the runs.
The hybrid model remains subject to one more empirical test: a real agent
trace (experiment 02), which will show whether candidates in top-3 actually
help an agent do the right thing, and whether forbidden records ever get
mistaken for authority in practice.

(Results appended after the runs; see below.)
