# Depot — build brief

**Depot** is a small **equipment-lending register** for a community workshop:
volunteers catalogue tools, lend them to members, and record returns.

This workspace contains a Flask starter whose backend is complete and must
keep working end to end (you may make small backend adjustments only if
strictly needed). The interface layer is intentionally unstyled:
`templates/` and `static/app.css`.

## Your task

Implement the interface so the app is coherent, consistent, and finished.

A **design authority** is available to you through the `design_authority`
MCP tools. Query it for anything you need. If the authority does not define
something, respect its resolution states (including `UNDEFINED` and
`FALLBACK`) and **record gaps through its tools** — never turn a local
improvisation into apparent canon silently. Consult the authority before
inventing any pattern, and do not invent design material that contradicts it.

## Screens to complete (4)

1. **Items register** (`/items`) — all items with name, category, status
   (`Available` / `On loan` / `Overdue`), borrower; a way to reach the
   new-item form and each item's detail.
2. **New item form** (`/items/new`).
3. **Item detail** (`/items/<id>`) — shows the item, allows editing, lending
   actions (check out to a member with a loan length; return), and a
   destructive action **Retire item** that permanently retires it.
4. **Activity** (`/activity`) — an import job that can be started, plus
   progress and a log while it runs; users must be able to follow progress
   without leaving the page.

## Requirements

- Style everything through `static/app.css` following the authority. No
  libraries, frameworks, or CDNs; no JavaScript beyond what is strictly
  needed (progressive enhancement only).
- **Borrower selection must stay quick as the member list grows** (small in
  the seed data; assume it can grow).
- Retiring an item is **permanent** — the interface must make the consequence
  clear before it happens.
- Item status must be **unambiguous at a glance** in the register.
- The app must be **usable at phone width (~380px)** and on desktop.
- All flows must work end to end: create, edit, checkout, return, retire,
  import.

## Acceptance hooks (keep these — they are checked automatically)

- `<main>` on every screen carries `data-view="register|form|detail|activity"`.
- Register rows keep `data-item="<id>"`; status cells keep
  `data-status="available|on_loan|overdue"`.
- Item detail keeps a button with `data-action="retire"`.
- Activity keeps `[role="progressbar"]` visible while a job is running, with
  `aria-valuenow` / `aria-valuemax` correct.

Work autonomously. When done, verify the app still serves (for example with
`python3 app.py --port 8300`).
