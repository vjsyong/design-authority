# Phase 3b — "Cadence" stress test: report

Three quarantined builds of the same habit-tracker spec (42 required elements), one
per authority. Every element resolved through its pack first; fallbacks imposed;
undefined improvised in character, marked, and gap-filed; conflicts adapted and
documented. All three apps are complete, working, and independently re-verified
(real-browser passes, zero console errors).

## Results at a glance

| metric | wink | leader | dominion |
|---|---|---|---|
| direct resolves (incl. search-assisted) | 4 (+6) | 6 | 5 |
| fallbacks applied | 5 | 8 | 6 |
| undefined → improvised | 27 | 28 | 28 |
| conflicts → adapted | 0 | 0 | 3 · photo/illustration/iconography |
| improvised/adapted elements (types · DOM nodes) | 33 · 70 | 36 · 42 | 33 · 33 |
| gaps filed | 16 | 17 | 15 |
| self-tests | 46/46 + 19/19 | 45/45 | 71/71 |
| independent re-verification | ✓ clean | ✓ clean | ✓ clean |

**48 gaps filed across the three builds.** Every improvisation is traceable three
ways — `data-improvised`/`data-adapted` in the DOM (revealed by the in-app ◌
toggle), a row in each `NOTES.md` decision table, and a `gaps.jsonl` record with
need, scope, and context.

## The coverage finding

For an app of this kind, the authorities directly codify roughly **10–15%** of the
required surface. Everything else went through the fallback/improvise/gap path —
with **zero silent invention**: the loop's whole job is exactly this case, and it
held under pressure. The stress test did not break the system; it exercised it.

## The holes (ranked, and what they suggest)

1. **Data visualisation** — bar chart, calendar heatmap, sparkline, progress ring:
   absent from ALL THREE authorities (the single biggest shared void).
2. **Overlay vessels** — modal, dialog, wizard: only leader has a home for these
   (fallback/ruled-panel, in-flow panels, no scrim, no motion); wink and dominion
   improvise every one.
3. **Feedback & transients** — toast, saving spinner, weekly banner: absent
   everywhere (dominion's canon even argues *against* toasts; its build adapted).
4. **Non-text controls** — slider, stepper, search field, date/time pickers: only
   partially covered ("pick a date" routes to three *different* fallbacks).
5. **Gamification** — streak counters, achievement badges: wink has badges only;
   streaks don't exist anywhere.
6. **Small utilities** — empty states, iconography, CSV export, dark mode,
   pagination, drag-reorder, celebration motion.

## Resolver findings (evidence for pack maintenance)

- **`resolve` alone under-reports canon.** Single-token or short natural asks
  ("a badge", "a table", "a select") fall below the direct-match threshold even
  where canon exists; the mandatory `search` → `inspect` step rescued them in
  every case. The resolve→search pairing isn't a convenience — it's the workflow.
- **Phrase-level misses worth aliasing:** leader "banner" missed the notice alias
  (scored 9.0 on one-word search); dominion "delete a ritual" missed
  `recipe/retire-confirm` (needs item-centric phrasing); "stepper"/"wizard" fall
  through all fallback scopes; dominion decisions D-10/13/16/17/18 are unreachable
  from natural phrasings.
- These are **pack-maintenance candidates, not kernel bugs** — exactly what the
  gap loop is for. Not applied; listed here as proposed follow-ups.

## Divergence (same screens, three products)

- **wink** — mustard ring, cream ground, pill everything, chunky rounded cards,
  serif+sans mix, playful copy, drag handles, onboarding modal in character.
- **leader** — white ground, red ring + `TODAY` label, navy CTA, blue active-nav
  underline, serif-led editorial voice — and a *structural* adaptation: every
  dialog became an in-flow ruled panel (per the fallback), changing the app's
  bones, not just its skin.
- **dominion** — austere bilingual (Today | Aujourd'hui), numbered rows,
  words-only status ("On track" / "Slipping"), slate CTAs + focus glow, red only
  as the masthead mark, no imagery anywhere (adapted to initials/ordinals/ruled
  statements), flat structure.

Cosmetic AND structural divergence held: the same spec did not converge on one
generic app.

## Artifacts

- Apps: `examples/cadence-{wink,leader,dominion}/` (index.html · app.css · app.js ·
  fonts/ · NOTES.md · .design-authority/gaps.jsonl)
- Live: `/stress/<pack>/` on the review server (linked from `/demo`)
- Method + sweep: `docs/synthesis/12-stress-plan.md`,
  `docs/synthesis/data/stress-sweep.json`
