# P4c counter-default — comprehensive brief

*What came before, why the experiment runs again, and why in this format.*

Status: companion brief to the draft pre-registration `docs/experiments/13-counter-default.md`.
Background and rationale only; the pre-registration itself is docs/13. Apparatus
built and verified (section 5); nothing runs until the owner freezes (section 6).

---

## 0 · The experiment in one paragraph

The program asks whether a **design authority** — governed design memory with
enforcement — can hold a design language across independent agent sessions and
handoffs, where static documentation drifts. Three runs have narrowed the
question. x05 (seed evolution) showed governance changes agent behaviour but
not first-pass fidelity; its uniform look turned out to be a program artifact.
P4 run 1 showed a DA-maintained chain flat at 100/100 against a decaying
static baseline, at +21% tokens — but bundled memory and verification together.
P4b (three-arm) isolated them: enforcement alone (arm B) held a flawless
100/100 across 15 handoff states while static decayed — but the owner review
then found the decisive confound: **the "design system" under test was the
model's own default palette** (Tailwind values with token names on them), so
visual consistency was overdetermined and the arm differences were mechanism-
level and invisible on screen. P4c reruns the experiment with a deliberately
**counter-default** contract — a language the model would not produce on its
own — so that reversion to model nature becomes the measurable, visible
violation, and a no-contract control arm estimates the model's pull directly.

---

## 1 · Background: what the Design Authority is

The Design Authority (DA, `~/design-authority`) is a governed design-memory
system for agent-built front-ends:

- a **pack**: the design contract — tokens, rules, lint (the validator),
  scoring;
- a **record layer**: cases, gaps, rulings, receipts (institutional memory);
- a **wrapper CLI**: `resolve` / `search` / `propose` / `inspect` / `validate` —
  consult before deciding, file what is new, validate before finishing.

The governing question of the experiment line: *does this hold a design across
successive independent sessions better than an equally good static contract —
and if so, which layer (enforcement, memory) carries the effect?*

---

## 2 · What was run before

### 2.1 · x05 — seed evolution: design drift under successive handoffs

Report: `docs/experiments/05-seed-evolution.md` (§11). Run area `~/x05`.

- 17 sealed sessions: formation (f1–f3) against a blank pack, census,
  codification adjudication (canon `base 0.1.0-experiment`), then three
  handoff chains A/B/C × 4 handoffs on the bookmarks app. Same model
  (`deepseek/deepseek-flash`), frozen briefs, budget 2700 s / 20 M tokens
  (all sessions self-terminated early).
- Readout: blind review matched-region means **A 2.5 / B 3.5 / C 3.75**
  (single reviewer, no calibration set — reduced precision); objective Layer 1
  (role fidelity, the pre-registered primary) flat and near-floor for every
  chain (D1/D2 fail); Layer 2 (cross-component consistency) near ceiling
  (0.92–0.97) without favoring C. Process audit: C consulted the authority
  substantively (18–54 wrapper calls/session) and introduced **zero
  unauthorized vocabulary drift**.
- Bottom line: **governance changed behaviour; it did not move the fidelity
  gates.** The uniform look was a program artifact (recombinative single-pass
  sessions). Enforcement in the sealed arm was hollow — building a working
  enforcement layer became the next prerequisite. The remaining testable
  benefit hypothesis was **economic**: does governed precedent reduce the
  cost of maintaining consistency across handoffs?

### 2.2 · P4 run 1 — maintenance economics (DA vs static baseline)

Docs: `09` (frozen pre-registration) → `10` (results), `docs/experiments/`.
Run area `~/p4-maint`.

- Design: two conditions matched on information quality — static-contract
  baseline (versioned docs, conventional notes) vs the full DA (pack +
  record + wrapper + reconciliation). One 4-handoff feature sequence on the
  bookmarks app (collections → search → pinning → favourites), each handoff
  carrying: (a) an ordinary feature, (b) a touch on an already-decided area,
  (c) a previously unresolved situation, (d) a canonical-rule change shipped
  as pack + transition policy (baseline: release notes). 8 sessions, k-wise
  interleave; seed = sealed x05 chain-C `h4c` final state, forked
  byte-verified 130/130.
- Results (external validator, constant yardstick):
  - **DA flat: 0 findings, 100/100, all four handoffs.** Baseline decayed
    1 → 1 → 2 → 3 findings, score 98 → 94 — raw colour literals
    (`rgba(37,99,235,0.12)`) and accumulating duplicate declaration blocks.
  - Cost of governance: **+21% tokens** (50.2 M vs 41.6 M), **+37% tool
    calls** (553 vs 405), ≈ +16% wall.
  - Recurrence claim: not directly comparable across conditions (baseline has
    no record store) — DA-side evidence (0 true re-filings, 186 new wrapper
    calls profiled) suggestive only. Migration: no correctness difference;
    demonstrable difference is **auditability** (receipt-backed obligations).
  - Kill criterion not hit; primary gate (drift) met, strictly.
- Limitation recorded: run 1 **bundles** institutional memory and continuous
  verification. Separating them is the next experiment.

### 2.3 · P4b — the three-arm run (static / enforced / governed)

Docs: `11` (frozen pre-registration) → `12` (results). Run area `~/p4-maint`.
45 sessions = 3 seeds × 3 arms × (H1–H4 + H5), 14:52–22:43 UTC.

- Arms: **A** static contract only · **B** static + enforcement (mandatory
  end-of-handoff validation, repair-or-file) · **C** full DA (B + governed
  memory: resolutions, cases, receipts, reconciliation). Primary comparison
  pre-registered as **C vs B**. Uniform observability fixes applied from the
  run-1 review: `DECISIONS.md` in every arm, a held-out blind round (two
  reviewers + calibration set, via the `driftexp.seanyong.xyz` instrument),
  a constant external validator on every session state, continuous cost
  tracking, and a governance-overhead call profile. **H5**: a fresh
  remediation session per chain, measured separately (preventive vs deferred
  economics).
- Results:
  - **B was flawless:** zero findings at all 15 handoff states, all three
    seeds, at ≈ **+7%** token cost over A.
  - **A decayed, in the target class:** h4 = 70 / 88 / 92 across seeds
    (from 98 / 98 / 96), two errors (B001) plus warnings (B004).
  - **C carried 1–5 documented B004 residuals** through every handoff —
    not a failure but the design: C's protocol is repair-or-file
    (documented tolerances), B's mandate is reach-zero. That contrast is the
    distinction the experiment asked to expose.
  - **H5 economics:** repairing A's accumulated drift cost 7.0 M tokens
    ≈ the prevention premium B paid during H1–H4 (+6.9 M per chain-set).
    Deferred bill ≈ preventive premium at this scale; prevention's extra
    purchase is that no intermediate consumer ever saw a dirty state.
  - Costs H1–H4: A 92.8 M / B 99.7 M / C 128.8 M tokens (+39% vs A, +29% vs
    B); wall A 7,061 s / B 7,235 s / C 8,347 s. One session capped
    (`r3-b-h5`, its own voluntary sweep hitting the 20 M cap). Blind round
    served live (14 comparisons, R1), mapping sealed — results with
    reviewers.
- Claims recorded: enforcement alone produces continuous conformance (strong,
  within run); governance added no conformance beyond enforcement at this
  scale (strong within run, with the objectives-by-construction caveat);
  static drift was cheap to repair at this scale; arms distinguishable.

### 2.4 · The confound (owner review, 2026-10-11)

Owner's reading of the three-arm output: *"All of them basically look the
same bar some minor drift… this look was the default for this model; there's
a confound that it is simply resorting to its own nature."* Verified against
the data (`docs/12`):

- **The design system under test WAS the model's default palette.** The
  seed's tokens are Tailwind defaults with names on them:
  `--color-accent: #2563eb` (blue-600), `--color-muted: #6b7280` (gray-500),
  `--color-danger: #b91c1c` (red-700), `--color-accent-hover: #1d4ed8`
  (blue-700). No distinctive design opinion was ever at stake; visual
  consistency required no arm to overcome any model nature, and the
  code-imitation signal (every session reads the existing CSS) was available
  to all arms equally.
- **The measured arm differences are mechanism-level, not visual.** A's B001
  "raw colour" findings are `rgba(37, 99, 235, 0.12)` — the same accent blue
  at 12% opacity, written as a literal instead of a token. The outcome
  variable was *how* values got written, not *which* values; that is
  invisible on screen and structurally unmeasurable by a visual blind
  instrument.

Consequences, recorded in `docs/12`: the three-arm result **stands as a
process finding** (enforcement held token discipline across handoffs where
static did not) and is reframed accordingly; it is **not** evidence about
visible design consistency, and the blind round as served cannot provide
that evidence for this subject. Attribution to the authority versus model
nature is **overdetermined on the visual plane** for this lineage.

---

## 3 · Why run again — and why this format

`docs/12` closes with the de-confound requirements, which are exactly what
P4c implements:

1. a deliberately **counter-default contract** — falling back to the model's
   palette becomes the measurable violation, and the lint can ban
   default-palette values explicitly;
2. a **no-contract control arm** to estimate model nature directly;
3. blind items **only where counter-default stakes are visible**
   (squared vs rounded corners, ink vs blue, chip treatment), plus a
   **reversion** metric (default-palette / nonzero-radius / system-font
   appearances over handoffs);
4. optionally a **second model** to break single-model attribution.

The P4c question (`docs/13`): *Does a design authority hold a deliberately
counter-default design language across independent sessions and handoffs —
and is the hold attributable to the contract rather than the model's default
aesthetic?*

### The counter-default contract

Adopted at value level (Triage Design System values):

- **Ink & paper:** text `#000000`, page `#fafafa`, cards `#ffffff`, lines
  `#e5e5e5`, muted `#666666`, black ink panels.
- **Accent `#0057d9`** (distinctly not the Tailwind blue), tint `#dbeafe`,
  danger `#c81e2c`.
- **Squared everywhere:** `--radius: 0px`; any nonzero border-radius is a
  violation.
- **Type:** Geist / Geist Mono, vendored woff2 (no external resources).
- The seed ships restyled and validating clean; semantic slot names
  (`--color-*`) stay, all values move to the counter-default vocabulary.

### Lint v2 (the teeth)

- **B006 default-vocabulary ban** — any Tailwind-default-family value
  (`#2563eb`, `#1d4ed8`, `#6b7280`, `#b91c1c`, `#f4f5f7`, `#e2e5ea`,
  `#1c2024`, `#eff4ff`, `#eff6ff`, and rgba forms) is an error, new or
  inherited.
- **B007 squared corners** — nonzero `border-radius` is an error.
- **B008 type whitelist** — `font-family` must resolve through the contract
  stack; system/third-party stacks are warnings.
- B001–B004 (delta-based token/testid/storage/reuse checks) unchanged.

### Arms

| arm | materials | enforcement |
|---|---|---|
| **C1 · contract only** | counter-default design-doc + token record + release notes | none in the loop |
| **C2 · contract + enforcement** | C1 + mandatory end-of-session validate (as arm B in P4b) | validator, repair to zero |
| **C3 · no-contract control** | the same restyled seed, no design instructions at all | none |

C3 measures the model's natural pull directly: given a counter-default app,
does a session left to its own devices continue the language or convert new
work toward model defaults? P4b already isolated governance, so the governed
layer sits out this round.

### Sequence, measures, gates

- Same four-handoff feature set as P4b (collections → search → pinning →
  favourites), on the P4b harness (sandbox, budgets, seals, captures):
  **2 seeds × 3 arms × 4 sessions = 24 sessions**. H5 remediation optional
  (deferred unless the spread invites it).
- **Primary measure — reversion**, per session end-state, external and
  constant: (a) B006/B007/B008 findings under the frozen counter-default
  lint; (b) reversion events in the session diff (default-family literals
  added, nonzero radii added, foreign font declarations added); (c) the
  blind round, now with visible stakes.
- Secondary: B001–B004 continuity, costs (tokens / wall / calls),
  `DECISIONS.md` trace (uniform log as in P4b).
- **Gates:** predicted ordering **C2 ≤ C1 < C3** on reversion. **Kill
  criterion — reframed:** if C3 shows no pull to default (sessions continue
  the counter-default language unprompted), the single-model-nature confound
  resolves the other way — the model's nature is contextual/imitative here —
  and that is the finding.

---

## 4 · Apparatus built and verified (owner-directed, 2026-10-11)

- **Pack `p4c-cd-0`** (`~/p4c/materials/packs/p4c-cd-0/`): counter-default
  token values; B006/B007/B008 added to the shipped lint; baseline
  regenerated from the restyled seed. Builder:
  `docs/experiments/tools/p4c_build.py` (idempotent).
- **Seed restyled** (`~/p4c/seed`): the P4 bookmarks line moved onto the
  counter-default vocabulary (ink/paper/squared/Geist, Triage token values,
  vendored woff2 fonts).
- **Verified discrimination:** the restyled seed validates **0 findings /
  score 100** under the v2 lint; the pre-restyle seed (the old model-default
  look) validates **53 findings / 51 errors / score 0** under the same lint.
  The model's default output is, by construction, a violation of the
  contract. Visual smoke (headless chromium): squared corners, ink text,
  `#0057d9` accent, Geist — read as "a highly deliberate, opinionated design
  language" versus the previous round's "generic default".
- **Harness:** the P4 toolchain re-parametrised (`P4_ROOT` env) rather than
  rebuilt; schedules for C1–C3 land after freeze.

---

## 5 · What P4c will and will not settle

- **Will:** whether a contract the model would not choose can be held across
  independent sessions — and whether the hold tracks the contract (C1/C2) or
  drifts back toward model nature without one (C3). Reversion is visible and
  lint-able by construction this time.
- **Will not (as drafted):** cross-model attribution (single pinned model
  unless the second-model option is activated); anything about visual
  *fidelity* beyond the counter-default stakes; recall — H5 slotted out
  unless the spread invites it.

---

## 6 · Open decisions — awaiting owner freeze

From `docs/13` (resolve at freeze):

1. **Feature briefs:** reuse P4b's four (`~/p4-maint/materials/briefs/`
   `h1`–`h4`) or author new ones. Reuse buys comparability with the
   three-arm run; new buys freshness if the P4b set is judged saturated.
2. **H5 remediation phase:** in or out.
3. **Second model** for attribution: in this round, or as a dated amendment.
4. **Freeze:** on the owner's go. Freeze commits the pre-registration;
   schedules and the run follow.

---

## 7 · Where things live

| what | where |
|---|---|
| Repo (docs, tools) | `~/design-authority` — `docs/experiments/09`–`13`, `tools/p4_*.py` |
| P4 run-1 + P4b run area | `~/p4-maint` (`materials/` packs `p4-da-0..4`, `run/`, `seal/`, `analysis/`) |
| P4b session briefs | `~/p4-maint/materials/briefs/h1–h5.md` |
| P4c area | `~/p4c` (`materials/packs/p4c-cd-0/`, `seed/`) |
| x05 archive | `~/x05` |
| Blind instrument | `driftexp.seanyong.xyz` (P4b round live, R1, mapping sealed) |

---

*Sources: `docs/experiments/05-seed-evolution.md` §11; `09`/`10`
(maintenance economics); `11`/`12` (three-arm + confound); `13`
(counter-default pre-registration + build log). Numbers quoted from those
records; raw evidence under the run areas above.*
