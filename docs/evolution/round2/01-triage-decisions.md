# Round 2 · 01 — Triage decisions

Assume no extension; try the existing authority first; prefer documentation
< recipe < pattern < primitive. Every claim below was verified by execution
against the real packs (stdlib resolver, evolution pack 0.13.0-experiment).

## N-1 · Skip link → **catalogue entry** (documentation layer)

- *Existing authority first:* nothing addresses skip links; `nav-item`'s
  multi-word alias "navigation link" wins because the query carries both
  tokens ("navigation", "link") — a phrase-bonus collision, the exact
  pitfall the round-1 review flagged. Removing the alias was considered and
  **rejected**: "navigation link" is legitimate vocabulary for nav items and
  deleting it risks regressing honest nav queries.
- *Chosen layer:* a first-class catalogue entry — the class is shipped,
  documented in three places, and predates every release. `component/skip`
  added at the triage-snapshot level (`spec/states.json`), mirroring the
  existing minimal-contract entries, plus curation notes/aliases/docs-map.
- *Verified fix (scratch):* with the record present,
  "a skip link to jump past the navigation" → **RESOLVED component/skip**;
  "a navigation link in the sidebar" and "a sidebar link with an active
  state" still → `component/nav-item`.

## N-2 · Sliding panel → **vocabulary fix** (aliases)

- *Existing authority first:* `component/sheet-end` already carries "side
  sheet", "end sheet", "slide-over panel", "side panel" — none fires for
  "panel sliding in from the edge" (tokens present but no phrase bonus);
  `pattern/detail` wins on "record" + "details". The right owner is the
  slide-over component; the pattern is a full page.
- *Chosen layer:* aliases only: `component/sheet-end` += "sliding panel",
  "slide-in panel". Rejected: a bare "panel" alias (too broad), trimming
  `pattern/detail` aliases (legitimate vocabulary).
- *Verified fix (scratch):* the query → **RESOLVED component/sheet-end**;
  "open an end sheet for secondary details", "a side panel with filters",
  "a detail view of a record", "a record page for one item" unchanged.

## N-3 · State label → **no change** (already consistent with canon)

- Evolution already answers with `recipe/status-with-text`, which is the
  pack's own golden mapping for status-display phrasings. Boosting
  `component/badge` above it via a new alias was considered and **rejected**:
  it would fight a recorded golden semantic for no demonstrated benefit.
  The dispute is resolved on the evolution line; documented, not edited.

## N-4 · Row-actions chevron → **vocabulary fix** (recipe needs)

- *Existing authority first:* `recipe/row-actions` exists and describes the
  exact `.menu-pop` row-menu pattern; `recipe/bulk-actions` hijacks the
  query because it is about batch operations and shares "actions" tokens.
- *Chosen layer:* extend `recipe/row-actions` needs with the observed
  phrasings ("the chevron that reveals actions for a single row", "reveal
  the actions for one row", "open a row's action menu"). No artifact
  aliases touched; no new ingredients.
- *Verified fix (scratch):* the query → COMPOSE **recipe/row-actions**;
  "batch delete selected" / "act on many selected records" still →
  `recipe/bulk-actions`; "per-row actions" / "more menu on a row" unchanged.

## N-5 · Status chips → **note + docs-map, alias pending battery**

- *Existing authority first:* `component/badge` legitimately owns the
  "status chip" phrase for state labels; `pattern/dashboard` already says
  "status/automation chips" in its summary but does not name the classes.
- *Chosen layer:* name the classes in `pattern/dashboard`'s note and
  docs-map (addressability of the shipped pattern furniture). An alias
  ("status chips" on the pattern) is tested against the battery and kept
  only if it does not steal badge queries; otherwise note-only.

## Execution evidence (scratch battery, 18 probes)

| query | baseline (0.13.0) | with candidates |
|---|---|---|
| a skip link to jump past the navigation | RESOLVED component/nav-item | **RESOLVED component/skip** |
| a panel sliding in from the edge with a record's details | RESOLVED pattern/detail | **RESOLVED component/sheet-end** |
| a small label showing a record's state such as Draft | COMPOSE recipe/status-with-text | COMPOSE recipe/status-with-text |
| the chevron that reveals actions for a single row | COMPOSE recipe/bulk-actions | **COMPOSE recipe/row-actions** |
| (14 regression probes: nav, detail, sheet, bulk, row, picker, progress, status, timeline) | — | **all unchanged** |

Scratch artifacts: `docs/evolution/data/r2-scratch/` (built from the exact
record edits the candidates propose; regenerated for the review).
