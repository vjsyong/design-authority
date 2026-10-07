# 06 · Final report — did the loop close?

**Authority Evolution Experiment — complete.** A Design Authority built around
Triage 0.12.1 absorbed real downstream pressure (8 gap records from 4
benchmark runs → 3 consolidated needs), improved itself through a governed
upstream process (triage → candidates → independent adversarial review →
CI → experimental release), and was then re-tested against fresh downstream
agents. The loop closed on every need it targeted, with zero new primitives,
zero new CSS, and no measured regressions.

## 1 · What ran (pointer index)

| phase | artifact | result |
|---|---|---|
| P1 evidence | `00-gap-evidence.md` | 8 records / 3 needs / 5 prior proposals |
| P2 triage | `01-triage-decisions.md` | all needs at doc-fix + recipe level; 0 primitives |
| P3 candidates | `proposals/evolution/cand-01…05` + `02-candidates.md` | 5 candidates |
| P4 review | `03-review.md` | **REVISE ×5** — independent reviewer, executed checks |
| P5 CI | `04-authority-ci.md` | 34/34 convergence; all Triage gates green |
| P6 release | `packs/triage-evolution` (`0.13.0-experiment`, branch `32e680b`) | published beside the intact 0.12.1 |
| P7 re-runs | `benchmark/runs/e1..e3` + §2 below | **zero gaps re-filed; all needs sanctioned** |
| P8 migration | `05-migration.md` | 7 usages: 5 direct, 2 manual-review |
| P9 inflation | `data/inflation.json` + §4 | +2 components(beta), +2 recipes, 1 extension |

## 2 · P7 — the core test: fresh downstream runs under the new authority

Same Procura brief, same model, same frozen harness — only the authority pack
changed (`--pack triage-evolution`). Requirements phrased semantically; no new
artifact names leaked.

| run | exit | dur (s) | resolves | outcomes | gaps filed | interact | lint delta |
|---|---|---|---|---|---|---|---|
| e1 | 0 | 751.9 | 8 | 7 R · 1 C | **0** | 13/13 | 0 |
| e2 | 0 | 210.8 | 8 | 5 R · 3 C | **0** | 8/13 † | 0 |
| e3 | 0 | 808.7 | 6 | 3 R · 3 C | **0** | 13/13 | 0 |

† e2 flagged: agent-side Jinja defect (`{{ steps|last.actor }}` — malformed
filter chain) 500s the detail route. Reproduced via Flask test client;
**authority-independent** (e1/e3 clean under the same pack). Kept as a
flagged rep; e3 restores n=2 clean.

### Need-by-need closure

| need | old authority (c1–c4) | new authority (e1–e3) |
|---|---|---|
| reviewer picker | 4/4 runs filed gaps; misroutes / UNDEFINED | **`component/select`** resolved in all 3 runs; 0 gaps |
| job progress | 3/3 runs filed gaps; FALLBACK(plain-content) | **`recipe/job-progress`** composed (e2, e3); e1 got `badge` first, then inspected `component/progress` + `recipe/job-progress` and built per the recipe; 0 gaps |
| reason-bearing decision | c3 filed a gap; UNDEFINED on exact wording | sanctioned in all runs (`recipe/high-stakes-confirm` or its `guideline`); 0 gaps |

**Phrasing convergence:** the 34-case battery (04 §3) plus the agents' *own,
unseen* phrasings converged on the same artifacts. Observed sanctioned
variance: e1's job phrasing resolved to `component/badge` (state label) before
inspection; e2/e3's decision phrasing resolved to the guideline — all within
sanctioned space, none produced a gap or a block. Efficiency: e-runs used
39/37/52 authority calls (vs 50–67 in c-runs) with fewer searches — answers
arrived more directly.

**Side effects:** lint delta 0, zero console errors, functional 13/13 on both
clean reps, containment clean. No unintended authority side effects observed.

## 3 · P8 — migration (detail in `05-migration.md`)

7 real improvised usages across c1/c3/c4 → all identified and mapped
(5 direct replacements, 2 behavioral manual-reviews, 0 unrelated changes).
The markers the old agents left are precisely the seam the new authority
grips.

## 4 · P9 — authority inflation (raw dimensions)

All consolidated outcomes: **3 needs closed by 5 changes — 0 new primitives,
0 new patterns, 0 project-local, 0 rejected, 0 existing-solution.**

| dimension | 0.12.1 | 0.13.0-experiment | Δ |
|---|---|---|---|
| artifacts | 73 | 75 | **+2** (`component/select`, `component/progress`, both `beta`) |
| components | 35 | 37 | +2 |
| recipes | 15 | 17 | +2 (`assign-picker`, `job-progress`) |
| rules / fallbacks / prohibitions / patterns | 15 / 3 / 9 / 7 | identical | 0 |
| guidelines | 13 | 13 | 0 new; 1 extended |
| aliases | 48 keys / 214 terms | 50 / 226 | +12 terms |
| recipe needs | 54 | 72 | +18 phrases |
| new CSS declarations / visual language | — | **0 / 0** | — |
| existing entries modified | — | 3 (`component/cb` alias-only; `guideline/high-stakes-confirm` do-line; `recipe/high-stakes-confirm` needs/ingredients/constraints) | — |

*Authority inflation* (working definition): growth in normative surface area
required to close observed gaps. Here: +2 beta catalogue entries over already
shipped CSS, +2 curated recipes, +1 extension — proportionate to evidence
(4/3/1 independent runs) and *smaller* than what the downstream agents
proposed (two component proposals downgraded, one recipe rename adopted). The
one real inflation surface is **vocabulary breadth**, quantified above,
bounded by the delete/regression batteries.

## 5 · P10 — evaluation against the protocol's questions

1. **Gap closure — yes.** Every accepted change resolves the need that
   triggered it (battery 34/34; fresh agents: zero re-files).
2. **Convergence — yes,** with disclosed variance: semantically equivalent
   phrasings land on the same artifact family; two variants landed on adjacent
   sanctioned siblings (badge/guideline) without degrading outcomes.
3. **Recurrence — none observed.** Three fresh runs, zero duplicate gaps for
   any closed need.
4. **Regression — none measured.** Pinned pack byte-identical; 19/19 pinned
   golden; browser suite 248/248; UI baseline zero-drift; delete and
   regression batteries unchanged.
5. **Inflation — measured and small** (§4). The headline number: **0 new
   primitives** across all pressure.
6. **Review value — material.** The adversarial pass rejected the package
   as-drafted (a stated criterion was unachievable under the frozen kernel; a
   vocabulary collision was flipping delete queries), forced 5 revisions, and
   a second pass caught 2 more tuning issues. Without review, the release
   would have shipped with a false success criterion and a hijacked
   frozen-golden semantic.
7. **Provenance — complete.** Every change carries triggering gap IDs, review
   decision, source branch, tests; BUILD.json carries release metadata. The
   chain "why does this pattern exist?" is answerable end-to-end from the
   pack alone.
8. **Migration — workable** (§3). Semi-automated; the residual manual cost is
   behavioral review, not markup.
9. **Human usefulness:** all evidence artifacts are written for a designer's
   eye (evidence records, decision rationales, review verdicts, the exact
   numbers) — the judgement call on "useful vs bureaucratic" is left to the
   human, as it should be.

## 6 · The final research question, answered directly

> *Can a Design Authority absorb real downstream implementation pressure,
> improve itself through a governed upstream process, and eliminate previously
> unresolved design decisions without uncontrolled growth or regression?*

**Within this experiment's scope: yes.**
- *Absorbed:* 8 raw records → 3 consolidated needs, none dismissed.
- *Governed:* independent adversarial review changed the package's substance;
  deterministic CI gated everything; the pinned authority was never touched.
- *Eliminated:* the exact phrasings that previously mis-routed, fell back, or
  went UNDEFINED now resolve to sanctioned answers — confirmed both
  mechanically (34/34) and behaviorally (fresh agents: zero gaps).
- *Without uncontrolled growth:* 0 primitives, 0 CSS, +2 beta catalogue
  entries, +2 recipes.
- *Without regression:* all regression surfaces unchanged, including the two
  frozen-golden semantics that the tuning pass preserved.

## 7 · Threats to validity (all protocol-listed items, addressed)

- One reference system (Triage), one app (Procura), one model family; gap set
  from one benchmark generation — external generality untested.
- Human judgment influenced upstream classification (mine) — mitigated by the
  independent reviewer, not eliminated.
- Review may be biased by knowledge of the original experiment — the reviewer
  ran in a clean context and re-verified claims by execution; residual
  familiarity bias unknown.
- Accepting changes may overfit Procura — countered by generic ingredient
  reuse and non-regression, but not proven.
- **Resolver improvement is partly alias-driven by design** — vocabulary IS
  the retrieval mechanism; the guardrails were the delete/regression batteries
  and the preserved frozen-golden semantics. The kernel was not modified.
- Small n (3 needs; 3 fresh runs); single round — recurrence across time/
  versions untested.
- No independent human designers in the loop yet.
- Runs measured under the same host caveats as the production experiment
  (containment clean; flags disclosed).

## 8 · Deliverables

`docs/evolution/`: `00-gap-evidence` · `01-triage-decisions` · `02-candidates`
· `03-review` · `04-authority-ci` · `05-migration` · `06` (this) · `data/`
(baseline + evolution resolve sets, inflation, migration JSON) ·
`proposals/evolution/cand-01…05` · release `packs/triage-evolution` (+
provenance overlay, README, 23-case golden) · branch
`evolution/0.13-experiment` (pushed) · fresh run artifacts
`benchmark/runs/e1…e3` · tools: `evolution_convergence.py`,
`migration_check.py`, harness `--pack` switch.
