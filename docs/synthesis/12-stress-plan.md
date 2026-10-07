# Phase 3b — "Cadence": stress-testing the three authorities

Purpose: the three candidates were compiled mostly against their own evidence
vocabulary. This phase pressure-tests the *system* — kernel + packs + gap loop —
with a deliberately different app whose required elements sit far outside the
codified canon, then builds that app **once per authority, under quarantine**.
Questions: does the system stay honest when stretched? Do the authorities produce
substantively different products? What does the gap machinery surface?

## The app (same spec for all three builds)

**Cadence** — a personal ritual tracker. Nothing like the library/register/mail
apps before it. Views: Today · History · Achievements · Settings; overlays for
detail/confirm/onboarding; toasts; celebration moments. Fixed copy + fixtures so
variants are comparable. Chosen BECAUSE its core surface — charts, rings, heatmaps,
gamification — is absent from all three packs, and because imagery/dialogs/motion/
status each land differently in each authority.

## The hole measurement (42 elements × 3 packs)

Method: every element the app needs, resolved through each pack
(`docs/synthesis/data/stress-sweep.json`; rerun:
`python3 ~/.hermes/cache/scratch/stress_sweep2.py` after editing
`docs/synthesis/data/stress-items.json`).

Counts of 42: **wink** R4 · F5 · U33 — **leader** R6 · F8 · U28 — **dominion**
R5 · F6 · **X3** · U28. (`~id` marks a search-reachable near-miss.)

```
ask                                                        | wink        | leader      | dominion
a primary button for the main action                       | R/action-…  | R/action    | R/action
a secondary button and a text link                         | R/action-…  | R/action    | R/action
delete a ritual permanently                                | U           | U           | U
a confirmation dialog before deleting                      | U           | F/ruled-…   | U
a modal with ritual details                                | U           | F/ruled-…   | U
a toast notification saying logged                         | U           | U(~notice)  | U
a banner summarizing the week                              | U           | U(~notice)  | U
an empty state when no rituals exist                       | U(~card)    | U(~field)   | U
an error message under the field                           | U(~field-…) | R/field     | R/field
a loading spinner while saving                             | U           | U           | U
a circular progress ring of today's completion             | U(~action-…)| U(~meter)   | U(~meter)
a bar chart of weekly minutes                              | U(~navbar)  | U(~meter)   | U(~masthead)
a calendar heatmap of the month                            | U           | U           | U
a tiny sparkline trend of the last week                    | U           | U           | U
a big streak counter                                       | U           | U           | U
an achievement badge for seven days                        | U(~badge)   | U           | U
a status label on track or slipping                        | U(~badge)   | U(~hierarchy)| U(~select)
a profile avatar photo                                     | U           | U           | X/imagery-…
an icon for each ritual                                    | U           | U           | U
a toggle switch in settings                                | F/platform  | F/platform  | F/platform
a slider for daily goal minutes                            | U           | F/platform  | F/platform
a date picker for the log entry                            | F/platform  | F/selection | F/large-…
a number stepper for minutes                               | U           | U           | U
a text field for the ritual name                           | R/field-…   | R/field     | R/field
a select for ritual category                               | U(~field-…) | F/selection | U(~select)
a checkbox for reminders                                   | F/platform  | F/platform  | F/platform
radio buttons for frequency                                | F/platform  | F/platform  | F/platform
a text area for notes                                      | U(~field-…) | U(~field)   | U(~field)
tabs for today history achievements                        | U           | U           | U
a bottom navigation bar on mobile                          | R/navbar    | R/navbar    | R/masthead
a table of logged entries                                  | U(~ledger)  | U           | U
pagination for older entries                               | U           | U           | U
a search box to filter rituals                             | U           | R/navbar    | F/large-…
a small category tag                                       | U(~badge)   | U(~field)   | U(~select)
drag to reorder rituals                                    | U           | U           | U
an undo button after deleting                              | U(~action-…)| U(~action)  | U(~action)
a three-step onboarding wizard                             | U           | U           | U
export the data as csv                                     | U           | U           | U
a dark mode theme                                          | F/light-only| U           | U
a celebration animation when checking off                  | U           | U(~motion)  | U
an illustration in the empty state                         | U           | U           | X/imagery-…
upload a photo for the ritual                              | U           | U           | X/imagery-…
```

Already observable divergence under identical asks: the slider is only a gap in
wink; dark mode is sanctioned only in wink; dialogs have a home only in leader;
search resolves only in leader; photos/illustration are **forbidden** only in
dominion; the same date-picker need routes to three different fallbacks.

## Handling policy (the packs' own manifests)

- **RESOLVED / COMPOSE** → implement per the cited artifact/recipe (inspect for values).
- **FALLBACK** → apply the fallback's constraints; mark the improvisation; file a
  gap if the need will recur (it will — these are core screens).
- **UNDEFINED** → search synonyms, inspect near-misses; if still open: improvise in
  character, mark `data-improvised`, file a gap with context.
- **CONFLICT** → do not implement as requested; adapt per the cited rule; document.

In-app traceability: a floating "◌" toggle reveals dashed amber outlines + notes on
every improvised/adapted element (`data-improvised` / `data-adapted`).

## Build setup

Three quarantined builds (one per authority; isolated contexts, same spec/copy):
`examples/cadence-wink/` · `examples/cadence-leader/` · `examples/cadence-dominion/`
Each: self-contained static app + `NOTES.md` (42-row decision table: outcome, cited
id, searches tried, action, mark, gap id) + `gaps.jsonl` (filed via
`da.py gap-add`). Then: served at `/stress/<pack>` on the review server, plus a
stress report comparing behaviour (outcome mix, gap themes, conflict adaptations,
and how different the three renderings actually are).
