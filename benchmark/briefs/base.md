# Procura — UI brief

You are building the user interface for **Procura**, an internal procurement
approvals console for an operations team. The backend is already built and
frozen: routes, data and query parameters are fixed (see `README.md`). Your
job is to implement the UI: `templates/` and `static/` only.

## Users and jobs to be done

Reviewers and ops staff use Procura daily. They need to:

1. **See the state of the work at a glance** (dashboard): how many requests
   are pending and for how much, what was approved recently, what was
   rejected, and what the background machinery is doing.
2. **Work through the request queue**: filter by status/category, search by
   title, page through the list, open a request.
3. **Decide on requests**: approve or reject a request (with a reason for
   rejection), assign a reviewer, see the approval history of each request.
4. **Act on many requests at once**: select several requests and approve or
   reject them together.
5. **Watch long-running background work**: an AI triage scan runs in the
   background; users need to see the status of a long-running background
   operation — how far it has come and whether it is stuck or failed.
6. **Configure notifications and auto-approval** in settings.
7. **Keep working on a phone**: reviewers check requests from their phones.

## Functional requirements (all must keep working)

- Every route in `README.md` responds as described; forms actually submit and
  persist (approve / reject / bulk / assign / settings).
- Deterministic state forcing keeps working: `?empty=1`, `?error=1`,
  `?job=running|done|failed`.
- Interactions give clear feedback: after an action the user can tell what
  happened; empty / loading / error states are visible states, not blank areas.
- A rejection is effectively irreversible for the requester; make that
  consequence clear at the point of action.

## Deliberately underspecified

- "Users need to see the status of a long-running background operation."
- "Users should be able to approve or reject many selected requests at once."
- "Show a compact history of recent approval steps on each request."
- "We probably need something like a compact picker for assigning a reviewer."

## Constraints

- Do not modify `app.py` or the data layer; do not change routes, response
  shapes, or query parameters. UI only: `templates/`, `static/`.
- The app must run with `./run.sh` and every route responds after your changes.
- Frontend stays dependency-free (no build step, no CDN): plain HTML/CSS/JS
  served from `static/`.

## Definition of done

- The UI covers all pages in `README.md`, desktop and phone.
- You exercised the app: ran it and clicked through the flows you touched.
- The workspace is left in a runnable state.
