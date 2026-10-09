# QA hooks — conventions the automated checks rely on

Small automated checks run against this project. Keep these conventions
intact; never rename or remove an existing `data-testid`.

1. **Dev server.** `python3 serve.py --port <N>` serves the app on
   127.0.0.1:<N>; `/healthz` returns 200. Do not rename `serve.py`.
2. **Data.** All app data lives in localStorage under `bookmarks.v1`: a JSON
   array of `{id, title, url, tags: [], createdAt}` (createdAt ISO-8601).
   The app renders from localStorage on load and persists every change.
   Fixture data is written into `bookmarks.v1` directly before the checks
   run.
3. **Hooks.** Interactive elements and key regions carry `data-testid`
   attributes. The set required for each stage is listed in the session
   brief; all existing hooks must keep working.
4. **States.** The checks reach states by seeded data plus plain clicks
   (`[data-testid=...]`); nothing else. No network calls and no external
   resources (no CDN); the app must work fully offline.
