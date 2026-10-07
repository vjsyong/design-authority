# Production report — A vs B vs C (n = 3 per condition)

**Status: production set complete (2026-10-07 07:00 UTC). Blind human review
pending (gallery served at `https://gpu-vm1.bigscale-snapper.ts.net:9110/`,
mapping sealed).** This report covers the nine production runs; pilot runs
(a1/b1/c1) remain excluded from headline metrics per the pre-registration,
with one exception noted in §2 (c2b, supplementary).

- Model: `deepseek/deepseek-flash` (pinned) · App: Procura (frozen starter)
- Instrument: frozen per docs/06 (deviations D-1…D-9 recorded there; every
  affected run is individually flagged below — none are hidden)
- No composite score. Dimensions reported independently, as pre-registered.

## 1 · Per-run status

| run | cond | exit | dur (s) | status | note |
|---|---|---|---|---|---|
| a2 | A | 0 | 467.6 | clean | |
| a3 | A | 0 | 591.1 | clean | |
| a4 | A | 0 | 633.2 | clean | |
| b2 | B | 0 | 865.9 | clean | |
| b3 | B | −15 | 471.2 | flagged | host-instability SIGTERM during wrap-up; build complete + measured |
| b4 | B | timeout | 1800.0 | flagged | hit the 30-min wall mid-iteration; build complete + measured |
| c2 | C | −15 | 509.9 | flagged | SIGTERM during late verification; build complete + measured |
| c3 | C | 0 | 770.6 | clean | |
| c4 | C | 0 | 646.8 | clean | |

All nine runs produced complete measurement artifacts (capture ×24 shots,
interact, scan, workspace archive). Flag distribution: A 0/3, B 2/3, C 1/3 —
with n=3 this is not interpretable; flagged runs' *builds* are complete, so
all dimension metrics below come from finished workspaces.

## 2 · D1 — Design compliance (triage-lint, agent-introduced)

| run | authored (e/w/i) | delta | | run | authored | | run | authored |
|---|---|---|---|---|---|---|---|---|
| a2 | 164 (48/110/6) | +154 | | b2 | **0** | | c2 | **0** |
| a3 | 127 (31/88/8) | +117 | | b3 | **0** | | c3 | **0** |
| a4 | 162 (37/116/9) | +152 | | b4 | **0** | | c4 | **0** |

By rule (A runs only; B/C produced none): TDS002 raw colours 99/62/80 ·
TDS003 border-radius 37/27/33 · TDS013 physical directions 16/23/32 · TDS006
8 more rules in single digits.

**Reading:** B and C are 6/6 clean sweeps — every run, zero findings, while
also eliminating the starter's own baseline. A is consistently and heavily
non-conformant (124–169 findings per run) while remaining functional. This
dimension separates A from {B, C} decisively and does **not** separate B from
C.

## 3 · D2 — Design drift

| metric | A (3 runs) | B (3 runs) | C (3 runs) |
|---|---|---|---|
| unique hex colours | 57/40/43 | 1/1/0 | 1/0/1 |
| px spacing values | 28/24/27 | 1/0/0 | 0/0/1 |
| border-radius decls | 14/13/10 | 0/0/0 | 0/0/0 |
| `!important` | 3/1/4 | 0/0/0 | 0/0/0 |
| inline styles | 15/33/31 | 25/10/7 | 15/10/4 |
| distinct classes | 181/125/172 | 183/142/159 | 132/140/141 |

The residual B/C hexes are the `<meta theme-color="#fafafa">` paper literal
(necessary, system-valued); c4's two 10px values are the single deviation to
watch. **Reading:** same shape as D1 — A drifts freely; B and C both stay in
system space. B vs C: indistinguishable on this dimension.

## 4 · D3 — Authority behaviour (condition C only)

| run | calls | RESOLVED | COMPOSE | FALLBACK | UNDEFINED | gaps | proposals | validate |
|---|---|---|---|---|---|---|---|---|
| c2 | 50 | 2 | 1 | 0 | 1 | 1 | 0 | 2 |
| c3 | 67 | 5 | 4 | 1 | 2 | 3 | 3 | 2 |
| c4 | 60 | 2 | 4 | 1 | 3 | 2 | 0 | 1 |

Tool mixes (same order): c2 inspect-heavy (32 inspects / 4 resolves);
c3 balanced (34/12); c4 resolve-forward (35 inspects / 10 resolves). Three
distinct usage styles — the interface supports several strategies.

**Gap themes across runs (all three C runs filed ≥1 gap):**
1. *Reviewer picker recipe* — filed by c2, c3, c4 (100%). Closest artifacts
   cited: `component/cb` + `fallback/native-control`; why insufficient: no
   documented single-select assign recipe.
2. *Determinate job progress* — filed by c3 and c4; closest: `spinner`
   (indefinite only), `progress`, `status-chip`; proposed as a composition
   with no new primitives.
3. *Irreversible decision requiring typed reason* (c3 only).

Proposals: c3 filed 3 (all three themes); c2 and c4 filed none (gaps only).
So the gap channel fired on 3/3 runs (6 gaps total); the proposal channel
fired on 1/3 runs (c3, 3 proposals). **The picker theme now has 4 independent
reports (pilot c1 … c4) and the job-progress theme 3; both reproduce the
pilot-era G-004 hole independently.**

## 5 · D4 — Engineering quality

- Functional: **13/13 interact checks in all nine runs**; 0 console errors in
  all nine captures; backend untouched in all nine (UI-only discipline held).
- Durations: A 468/591/633 · B 866/471/1800 · C 510/771/647 (s)
- Containment: clean across the board (attempts 0/0/0 for A and B; C runs
  probed `/opt/da` at start — da_zone 9/5/1 — then used the MCP interface;
  no condition saw another condition or the benchmark).

## 6 · Under-the-hood contrast (B vs C) in production

- **B runs (all three):** reviewer picker = the `.cb` combobox pattern,
  chosen silently — no recipe exists for it; job progress = a hand-rolled
  composite in templates. Consistent, competent, and **completely
  unrecorded**: no provenance markers, no gaps, no proposals. If merged,
  nothing distinguishes canon from improvisation.
- **C runs (all three):** same surfaces, but marked and routed — in-code
  `authority-undefined` annotations (request detail / jobs / CSS), 6 filed
  gaps, 3 filed proposals, 4–5 validation calls, every decision in the
  decision log with citations.

## 7 · Threats to validity

- n=3 per condition; single model; single app; single host (which was
  operationally unstable overnight — see D-1…D-9; per-run flags above).
- Flag distribution (B 2/3, C 1/3) is not interpretable at this n; flagged
  runs' builds are complete and measured, but *wrap-up completeness* differs.
- Static-analysis approximations in class counts; inline-style counts include
  data-driven values.
- Observer effects: prompts were fixed and identical; the experimenter
  (me) did not touch run workspaces; agents ran sandboxed.
- Human review (D5) still pending — this report deliberately omits any
  "which looks better" judgement.

## 8 · Deliverables & next steps

- Blind gallery (9 anonymized builds + questionnaire):
  `https://gpu-vm1.bigscale-snapper.ts.net:9110/` — mapping sealed at
  `benchmark/runs/_gallery-mapping-SEALED.json` (do not open before review).
- Raw per-run data: `benchmark/runs/<id>/` (run.json, scan.json,
  interact.json, capture/, ws/ archive). Generated tables:
  `benchmark/runs/_summary.md` (regenerate: `tools`/`report.py --include …`).
- After the human review: unseal mapping, fold D5 scores into the final
  synthesis (per-dimension table + case studies), and record the design
  decisions Triage must formalize (the picker + job-progress themes are the
  first two candidates for authority extensions).
