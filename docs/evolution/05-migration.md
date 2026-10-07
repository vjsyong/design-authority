# 05 · Migration experiment (Phase 8)

**Question:** can the new authority (0.13.0-experiment) be pointed at
implementations built under 0.12.1 and identify (a) which local
implementations are now superseded, (b) which new authority artifact applies,
(c) what needs to change, (d) whether that migration can be automated or
semi-automated?

**Method:** `tools/migration_check.py` — a report-grade scanner (no framework,
per protocol) that walks a workspace, finds the deliberate
`TODO(authority-undefined)` provenance markers the C-condition agents left,
classifies each usage into a gap group, re-resolves the canonical need
*against the new pack*, and emits per-usage records. Raw outputs:
`docs/evolution/data/migration-{c1,c3,c4}.json`.

## Results — three archived 0.12.1 workspaces

| workspace | real usages found | superseded by | change type |
|---|---|---|---|
| c1 (pilot) | reviewer picker (`templates/request_detail.html:75`) | **RESOLVED component/select** | direct (citation swap + `class="select"`) |
| | job progress (`templates/jobs.html:5`) | **COMPOSE recipe/job-progress** | direct (citation swap + aria contract) |
| | job progress logic (`static/app.js:67`) | **COMPOSE recipe/job-progress** | **manual review** (keep polling; align stall/announce semantics) |
| c3 | reviewer picker (`request_detail.html:86`) | **RESOLVED component/select** | direct |
| | reason-bearing reject form (`request_detail.html:67`) | **COMPOSE recipe/high-stakes-confirm** | direct (citation + constraint check) |
| c4 | reviewer picker (`request_detail.html:93`) | **RESOLVED component/select** | direct |
| | job progress logic (`static/app.js:58`) | **COMPOSE recipe/job-progress** | **manual review** |

**Totals: 7 real usages — 5 direct replacements, 2 requiring manual review.**
(The remaining marker hits are `DESIGN.md`/header text that *documents the
marker convention* — correctly surfaced, classified as non-usages.)

Ideal-shape check from the protocol:

```
Previous:  local background-job progress implementation  → linked to G-02
New:       recipe/job-progress
Migration: 4 usages detected · 2 direct · 2 needs manual review · 0 unrelated
           changes required
```

## Findings

1. **Identification works end-to-end.** The markers the agents left under
   0.12.1 are exactly the seam the new authority can grip: every marked usage
   resolved to a sanctioned replacement on the first pass, with zero false
   positives among real usages.
2. **The citation swap is mechanically simple** (`TODO(authority-undefined)`
   → the artifact citation; `class="select"` added to reviewer selects; the
   progress markup already matches the recipe's aria contract in c4/e2 because
   the agents derived it independently — the recipe formalises what they
   converged on).
3. **The genuinely manual part is behavioral only**: the polling/stall logic
   in `app.js` must be checked against the recipe's stated semantics
   (stall = count not advancing → text label; announcement mechanism; retry on
   failure). No markup or CSS change is required for it.
4. **No unrelated changes surfaced** — nothing in the migration targets
   forces edits outside the marked usages.
5. A full framework (codemod, AST rewrite) is **not warranted** at this scale
   and was deliberately not built; the report plus the scanner is sufficient,
   per protocol.
