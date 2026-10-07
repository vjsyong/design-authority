# Orbit reference app — “Depot”

Phase 5 deliverable of the Design Authority **portability spike**
(see `docs/portability/05-portability-report.md`).

**Depot** is a small equipment-lending register (community tool library) used
to exercise the second authority (`packs/orbit/`) end to end: navigation,
forms, repeated content, status/feedback, a destructive action, responsive
behaviour, and one deliberately ambiguous requirement (borrower selection at
scale — the authority defines small-set choosers only).

## Layout

```
app.py              Flask backend (trivial, prebuilt — JSON storage under data/)
data/               seed data: items, members, activity log
templates/          starter templates (unstyled; the agent refines these)
static/orbit.css    interface layer (empty in the starter; implemented from the authority)
brief.md            the build brief handed to the agent in the Phase 6 run
reference-build/    (added after the run) the agent's finished interface, archived for comparison
```

## Run

```
python3 app.py --port 8300
```

Then open `http://127.0.0.1:8300/items`.

## Provenance

- Starter authored for the spike (Phase 5); backend deliberately trivial.
- The design material comes from `packs/orbit/`, itself derived from the
  NASA Graphics Standards Manual (NHB 1430.2, 1976 — public domain).
- No NASA marks are used anywhere in this app.
