# Phase 3c — Adjudication pass: the judge seat, filled

The stress test left 48 gap requests with nobody judging them. This pass fills that
seat: independent adjudicators (one per authority, separate from the builders)
reviewed every request and produced the codified pathway from **agent request →
verdict → canon (or reasoned no)**.

## Taxonomy (fixed before adjudication)

Every gap classified into exactly one class, judged against **source evidence**
(never invented), smallest-change first:

- **LEXICON-FIX** — canon already covers it; `resolve` missed on phrasings. Exact
  machine-readable fix + the search hit that proves coverage.
- **SCOPE-FIX** — a fallback's scope list should cover it; exact fix.
- **PROPOSAL** — a legitimate new-canon need. Kernel schema enforced
  (`problem · insufficiency · reuse_case · composition_check · proposed · tests`,
  real `depends_on` ids) and filed via `da.py propose`.
- **NO-ACTION** — correctly undefined; cite the policy line; canon does NOT expand.
- **INVALID** — mis-filed. (None found: 0/48.)

## Outcome (48/48 judged)

| | wink | leader | dominion | total |
|---|---|---|---|---|
| proposals filed | 6 | 6 | 5 | **17** |
| lexicon/scope fixes | 3 | 4 | 5 | **12** |
| no-action | 7 | 8 | 5 | **20** |
| invalid | 0 | 0 | 0 | **0** |

**All 12 mechanical fixes applied** (10 compiler edits) — each was simulation-proven
by its adjudicator (before → after resolve, goldens preserved), and the applied set
was re-verified here: synthesis goldens 9/9 · 10/10 · 10/10, indaba 10/10, kernel
tests 10/10, triage 19/19, MCP smoke 17/17.

**Two real bugs surfaced by adjudication** (both fixed here):

1. **Kernel** (`resolve.py`): fallback scopes were matched raw against *stemmed*
   query tokens — scope words like `date`/`toggle`/`file` were silently dead in
   every pack (indaba included). Fixed: both sides now run through the same
   tokeniser. All goldens unchanged.
2. **Compiler** (`compile_pack.py`): `emit` built the shaped artifacts
   (`summary`/`status`/`source`/`compiled_from`) but wrote the *raw* mapping dicts
   to disk — the canonical decision text was never in the packs (and the wink W-13
   "carry" question was a symptom of this). Fixed; decision text now verified
   present in all three packs.

## Coverage delta (same 42×3 stress sweep, before → after)

| | wink | leader | dominion |
|---|---|---|---|
| undefined | 33 → **29** | 28 → **24** | 28 → **24** |
| resolved/compose | 4 → 5 | 6 → 8 | 5 → 8 (incl. 2 compose) |
| fallback | 5 → 8 | 8 → 10 | 6 → 7 |

14 outcome flips recorded (`docs/synthesis/data/stress-sweep-before.json` vs
`stress-sweep.json`), incl.: dominion "delete a ritual" → **COMPOSE**
`recipe/retire-confirm`; leader "banner" → **RESOLVED** notice; sliders/steppers →
sanctioned fallbacks in all three; textareas → resolved fields.

## Proposals awaiting verdict (the owner's seat)

17 kernel proposals sit `candidate` (workspaces under
`examples/cadence-*/».design-authority/proposals/`). Most cite decisions that Gate 2
left *undefined* — accepting one is the codified way to close that call with
evidence. Verdicts via `da.py review --proposal <id> --verdict accept|reject|
needs-info`; accepted → compile → goldens → sweep re-run (the "try again" loop).

**wink** — `pattern/destructive-confirm` (W-16) · `pattern/dialog-overlay` (W-17) ·
`pattern/inline-notice` (W-15; floating toast explicitly *not* canonized) ·
`pattern/empty-state` (W-19) · `pattern/progress` (W-18) · `component/status-pill` (W-14).

**leader** — `pattern/destructive-confirm` (L-15; rounded per accepted L-02 v4) ·
`pattern/empty-state` (L-17) · `pattern/data-charts` (rectilinear, no rings) ·
`pattern/data-readouts` (L-04 "big statics") · `component/tag` (L-13) ·
`pattern/ledger` (L-18).

**dominion** — compile `component/dialog` (D-18) + `component/empty-state` (D-16) ·
compile `component/status` (D-10) + `component/ledger` (D-17) · compile
`component/notice` (D-13; toast stays declined) · `pattern/plain-chart` ·
`token-set` reversed colourway (dark surfaces).

Honest notes filed by the adjudicators: borderline calls documented (wink neutral
tag; dominion G2/G6 small-compile reads), stale wordings flagged (leader L-15/L-19
"square" phrasing predates L-02 v4), and the wording-vs-pack drift recorded rather
than forced.
