# 14 — Codification & Negative Precedents

The reviewer assessed the 17 adjudication proposals (2026-10-07). This records
what happened to each verdict: accepts compiled into the packs, rejections —
plus the adjudicator's own declines — codified as **negative precedents** that
guide the next agent run instead of silently blocking it.

## Verdicts → outcomes

| Outcome | Count | What it became |
|---|---|---|
| Accepted | 11 | Compiled into `packs/{wink,leader,dominion}` → version **0.2.0** |
| Rejected | 5 | Negative precedents (reviewer-rejection provenance) |
| Needs info | 1 | Pending (leader `81e020` empty-state) — untouched |

### Accepted → canon (11)

Tool: `tools/apply_proposals.py` (refuses non-accepted; idempotent; bumps the
pack version; folds `tests.golden` and derives further goldens from each
proposal's own `resolve('X') cites ID` checks; alias reconciliation included).
Provenance on every entry: `provenance.proposal` + `reviewed_at`.

- **wink 0.2.0** (+5 entries): `pattern/dialog-overlay`, `pattern/empty-state`,
  `pattern/destructive-confirm`, `pattern/inline-notice`, `pattern/progress`
- **leader 0.2.0** (+3): `pattern/data-charts`, `pattern/data-readouts`,
  `component/tag`
- **dominion 0.2.0** (+4): `component/status`, `component/ledger`,
  `component/notice`, `pattern/plain-chart`

Golden sets grew 29 → **49 cases** (wink 18 · leader 14 · dominion 17), all
green. Codification fixes applied along the way: leader entries had empty
aliases (reconciled from their own checks); wink dialog-overlay gained
wizard/modal vocabulary; dominion gained its 7 check-derived cases.

## Negative precedents (the rejected ones, put to work)

`packs/<p>/precedents.json` — **25 records** = 20 adjudication declines
(no-action) + 5 reviewer-rejected proposals. Each record carries:
`request` (what was asked), `matches` (vocabulary), `decision: declined`,
`reason` (why, citing the adjudication), `try[]` (what to try instead), and
`citation`/`provenance` (gap or proposal id + date).

The concept is **kernel-generic**: an optional pack file; packs without it load
`[]`. Nothing about any authority's character is hardcoded.

### Where precedents reach agents

1. **`resolve`** attaches matching precedents (`precedents: [...]`) on
   vocabulary overlap — including alongside FALLBACK / CONFLICT outcomes, so a
   declined ask that has a sanctioned fallback returns *both* the fallback and
   the negative guidance ("here is what we do instead, and why the direct ask
   was declined").
2. **`search`** indexes them (`kind: "precedent"`) so the guide is visible while
   exploring, not only at resolve time.
3. **`report_gap` / `propose_extension`** attach `precedent_warnings` and add a
   checklist line ("justify against the recorded precedent") when a new ask
   re-treads a declined area — negative feedback at the moment of proposing.
4. **CLI** `da precedents [--query]` and **MCP** `list_precedents` for direct
   inspection.

### Matching rule

Single-word `matches` entries contribute stemmed tokens (a shared token of
length ≥ 4 required); multi-word entries contribute **only as phrases**. Generic
phrase-internal words never match alone ("export **button**", "radio
**button**" false-positived on "add a primary button" until this rule was
introduced — caught by the probe's negative cases).

## Verification

- `bash tools/check.sh`: drift ✓ · kernel unit tests **15/15** · triage golden
  **19/19** · synthesis goldens **18/18 · 14/14 · 17/17** · precedents probe
  **17/17** · MCP smoke **18/18**.
- `tools/precedent_probe.py`: register counts (8/10/7), attach cases (incl.
  FALLBACK + CONFLICT coexistence), no-attach on benign asks, search surfacing,
  gap/proposal warnings.
- Review gate (`/proposals`) now shows per-card outcomes — "codified ✓ → pack
  X 0.2.0" / "filed as `precedent/…` (negative precedent)" — and the record rows
  mark declines that became precedents; `data/codified.json` is the ledger.

## Consequence for the next rebuild

Declined asks no longer come back empty: an agent meeting them receives the
decline reason and the sanctioned alternatives (compose route, fallback, or
evidence bar to clear). Gaps and proposals landed in declined areas surface
warnings at filing time. The acceptance loop is now: verdict → canon
(rebuild uses it) or precedent (rebuild is steered away from it).
