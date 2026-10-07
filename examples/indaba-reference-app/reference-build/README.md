# Indaba reference app — “Depot”

Reference app for the Design Authority **portability spike, second
authority** (`packs/indaba`, derived from the Ubuntu brand guidelines;
see `docs/portability/09-ubuntu-source-audit.md`).

**Depot** is a small equipment-lending register (community tool library) used
to exercise the authority end to end: navigation, forms, repeated content,
status/feedback, a destructive action, responsive behaviour, and one
deliberately ambiguous requirement (borrower selection at scale).

## Layout

```
app.py              Flask backend (trivial, prebuilt — JSON storage under data/)
data/               seed data: items, members, activity log
templates/          starter templates (unstyled; the agent refines these)
static/app.css      interface layer (empty in the starter; implemented from the authority)
brief.md            the build brief handed to the agent in the build run
```

## Run

```
python3 app.py --port 8300
```

Then open `http://127.0.0.1:8300/items`.

## Provenance

- Starter authored for the spike; backend deliberately trivial.
- Design material comes from `packs/indaba/`, derived from the Ubuntu brand
  guidelines (Canonical). No Ubuntu marks are used anywhere in this app.
- The archived first attempt (NASA/“Orbit”, retired after review) lives in
  `../orbit-v1-reference-build-archive/` and `benchmark/runs/orbit-a1/`.
