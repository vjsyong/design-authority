# 13 · Counter-default contract — holding a design language the model would not choose (draft pre-registration)

Owner review of docs/12 (2026-10-11): *"…this look was the default for
this model; there's a confound that it is simply resorting to its own
nature."* This experiment makes the model's nature the opposite of the
contract, so that reversion becomes measurable and visible.

## Question

Does a design authority hold a deliberately counter-default design language
across independent sessions and handoffs — and is the hold attributable to
the contract rather than the model's default aesthetic?

## Premise (calibrated by evidence, docs/12)

The P4/P4b "system" was the model's default palette with token names on it
(Tailwind values: `#2563eb`, `#6b7280`, …); visual consistency was
overdetermined and the arm differences were mechanism-level, invisible.
The counter-design: choose a language the model would NOT produce on its
own, so falling back to nature becomes the violation — visible on screen
and lint-able.

## The counter-default contract

The estate's flagship language, adopted at value level (Triage Design
System, `~/triage-design-system/tokens/tokens.css`):

- **Ink & paper**: text `#000000` (pure ink), page `#fafafa`, cards
  `#ffffff`, lines `#e5e5e5`, muted `#666666`, black ink panels.
- **Accent**: `#0057d9` (distinctly not the Tailwind blue), tint `#dbeafe`,
  danger `#c81e2c`.
- **Squared everywhere**: `--radius: 0px`; any nonzero border-radius is a
  violation.
- **Type**: Geist / Geist Mono (vendored woff2; no external resources).
- The bookmarks app keeps its semantic slot names (`--color-*`); all values
  move to the counter-default vocabulary. The seed ships restyled and
  validating clean.

The lint gains teeth (pack-side, stdlib, deterministic):

- **B006 default-vocabulary ban** — any Tailwind-default-family value
  appearing anywhere (`#2563eb`, `#1d4ed8`, `#6b7280`, `#b91c1c`,
  `#f4f5f7`, `#e2e5ea`, `#1c2024`, `#eff4ff`, `#eff6ff`, and their rgba
  forms) is an error, new or inherited.
- **B007 squared corners** — any `border-radius` with a nonzero value is an
  error.
- **B008 type whitelist** — `font-family` declarations must resolve through
  the contract stack (Geist / Geist Mono / var(--font-sans|mono)); system
  and third-party stacks are warnings.
- B001–B004 (delta-based token/testid/storage/reuse checks) unchanged.

## Arms (to freeze)

| arm | materials | enforcement |
|---|---|---|
| **C1 · contract only** | counter-default design-doc + token record + release-notes channel | none in the loop |
| **C2 · contract + enforcement** | C1 + mandatory end-of-session validate (as arm B in P4b) | validator, repair to zero |
| **C3 · no-contract control** | the same restyled seed, no design instructions at all | none |

C3 measures the model's natural pull directly: given a counter-default app,
does a session left to its own devices continue the language or convert new
work toward model defaults? P4b already isolated governance, so the
governed layer sits out this round.

## Sequence, budget, measures

- Same four handoffs' feature set as P4b (collections → search → pinning →
  favourites), 2 seeds × 3 arms × 4 sessions = 24 sessions on the P4b
  harness (sandbox, budgets, seals, captures). H5 remediation optional
  (deferred unless the spread invites it).
- **Primary measure — reversion**, per session end-state, external and
  constant: (a) B006/B007/B008 findings under the frozen counter-default
  lint; (b) reversion events in the session diff (default-family literals
  added, nonzero radii added, foreign font declarations added); (c) the
  blind round, now with visible stakes (corner treatment, chips, colour
  family are plain to see).
- Secondary: B001–B004 continuity, costs (tokens/wall/calls), DECISIONS.md
  trace (uniform log as in P4b).
- **Gates**: predicted ordering C2 ≤ C1 < C3 on reversion; kill criterion —
  if C3 shows no pull to default (sessions continue the counter-default
  language unprompted), the single-model-nature confound resolves the other
  way (nature is contextual/imitative here), and that is the finding.

## Blind round

Same instrument and format as the P4b round, restricted to items with
visible stakes (squared vs rounded corners, ink vs blue, chip treatment);
each arm's h4 and h2 states against its own h1; calibration stage first.

## Open decisions (resolve at freeze)

1. Feature briefs: reuse P4b's four or author new ones.
2. H5 remediation phase in or out.
3. Second model for attribution (in or as amendment).
4. Freeze on the owner's go.

Status: draft; freeze + pre-registration committed on the owner's go.
Nothing below is executed until frozen.

## Build log (apparatus, owner-directed 2026-10-11)

- Counter-default pack built from the frozen base: pack `p4c-cd-0` under
  `~/p4c/materials/packs/` — counter-default token values, B006/B007/B008
  added to the shipped lint, baseline regenerated from the restyled seed.
  Builder: `docs/experiments/tools/p4c_build.py` (idempotent).
- Seed restyled: `~/p4c/seed` — the P4 bookmarks line moved onto the
  counter-default vocabulary (ink/paper/squared/Geist; Triage token values;
  vendored woff2 fonts).
- **Verified:** the restyled seed validates **0 findings / 100** under the
  v2 lint; the pre-restyle seed (the old model-default look) validates
  **53 findings / 51 errors / score 0** under the same lint — the
  discrimination is direct: the model's default output is, by
  construction, a violation of the contract. Visual smoke (headless
  chromium): squared corners, ink text, #0057d9 accent, Geist — assessed
  as "a highly deliberate, opinionated design language" (vs the previous
  round's "generic default" reading).
- Harness: the P4 toolchain re-parametrised (P4_ROOT env) rather than
  rebuilt; schedules for C1–C3 land after freeze.
