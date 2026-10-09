# x05 · Retrospective validation sweep (base-lint v1 over the sealed 17)

- **Status:** exploratory / post-hoc. Added after the pre-registered analysis
  closed; the primary record (blind review, objective scoring, process audit)
  is unchanged. This pass calibrates the new declared validator (pack
  `base-0.1.1-experiment`, linter `bookmarks-lint v1`) against real material
  and gives a mechanical read of colour-vocabulary drift.
- **Method:** `tools/x05_validate.py sweep` → the authority kernel runs the
  pack's declared validator over each `seal/<id>/tree`; findings normalized
  by the kernel. Raw data: `retrospective-validation.json` (copy of
  `x05/analysis/validation-sweep.json`). No tuning was applied after seeing
  results; every finding was inspected and judged (notes below).
- **Baseline semantics (calibration decisions):** B001 is a *delta* rule —
  the literal set of the sealed seed (f3) is the established vocabulary;
  only NEW literals are errors (absolute purity would flag the seed itself
  10× and was rejected). B002 preserves the seed's 27 QA hooks (missing →
  error; new hooks ignored). B003 checks the canonical storage key. B004 is
  warning-level (tokens outside :root; new duplicated treatment blocks).

## Results

| checkpoint | errors | warnings | score | note |
|---|---|---|---|---|
| f1 | 13 | 0 | 0 | all B002: hooks not yet created (bulk/confirm/filter arrived in F2/F3); expected — f1 predates the baseline epoch |
| f2 | 0 | 0 | 100 | |
| f3 | 0 | 0 | 100 | baseline source |
| cen | 0 | 0 | 100 | |
| cod | 0 | 0 | 100 | |
| h1a / h1b / h1c | 0 / 0 / 0 | 0 / 0 / 0 | 100 | |
| h2a | 0 | 1 | 98 | new dup: `.analytics-subtitle` ≡ `.app-tagline` |
| h2b | 0 | 1 | 98 | same dup |
| h2c | 0 | 0 | 100 | |
| h3a | **1** | 1 | 90 | new literal `rgba(20, 24, 33, 0.28)` @714 |
| h3b | 0 | 1 | 98 | |
| h3c | 0 | 0 | 100 | |
| h4a | **2** | 5 | 74 | literal @714 + @846; 5 new dups |
| h4b | 0 | 2 | 96 | |
| h4c | 0 | 1 | 98 | |

Chain totals over the drift window (h1–h4): **A 3e/7w · B 0e/4w · C 0e/1w.**

## Reading

- **Only the A chain introduced new raw colour literals** (a new shadow
  value, `rgba(20, 24, 33, 0.28)`, first at H3, extended at H4) — a concrete,
  mechanical divergence from the token vocabulary, directionally consistent
  with the blind review's C ≥ B > A ordering. Label: exploratory corroboration,
  not a pre-registered measure.
- B004 duplicate-treatment warnings appear in every chain but concentrate in
  A's H4 (5). Each chain introduced ≥1 new duplicated block somewhere
  (`.analytics-subtitle` dup in A/B; `.add-form-error` dups in B/C's H4).
- f1's 13 B002 findings are the baseline working as specified (preserve the
  *final* seed's hooks); they are not a drift signal and f1/f2 sit before the
  comparable window.

## Limitations

Static file scan only (no computed styles); regex-based CSS/JS parsing;
duplicate-block detection is heuristic (≥ 3 declarations, order-insensitive);
B001 normalization folds hex shorthand and whitespace only. A v2 could add
computed-style artifact checks (the objective scorer's machinery); none of
this changes the frozen primary analysis.

**Provenance:** pack `base-0.1.1-experiment` (canon byte-identical to
`base-0.1.0-experiment` + `validators.json`, `lint/bookmarks_lint.py`,
`lint/baseline.json`); linter + baseline generation live in
`tools/bookmarks_lint.py` / `tools/x05_build_validated_pack.py`; sweep tool
`tools/x05_validate.py`.
