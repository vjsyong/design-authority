# Patterns (7)

Page-level compositions (CSS in `design/core/patterns.css`, real
screens in `design/examples/`). Patterns are documented; unlike
components they carry no states contract.

## Dashboard / overview

Landing overview: hero metric strip, status/automation chips, recent-activity feed, follow-up cards.

Sources: docs page `/patterns/dashboard`, example `examples/dashboard.html`

## Detail / record page

Single-record page: page head with actions, fields, related lists, timeline.

Sources: docs page `/patterns/detail`, example `examples/viewer.html`

## Settings

Task-sectioned settings cards with scoped partial saves.

Sources: docs page `/patterns/settings`, example `examples/form.html`

## Flow / automation builder

Builder canvas for trigger → filter → action chains (node spine, insert-on-connector).

Sources: docs page `/patterns/flows`, example `examples/components.html`

## Dry-run / simulator report

Two-column draft|report layout for previewing what an automated pipeline would do.

Sources: docs page `/patterns/dry-run`, example `examples/components.html`

## Stepper / wizard

Multi-step task flow with step rail and per-step actions.

Sources: docs page `/patterns/stepper`, example `examples/form.html`

## Index & eval queue

Work-queue page: progress stats, per-item review rows, blind-labelling flow.

Sources: docs page `/patterns/index-eval`, example `examples/list.html`
