# Bookmarks

A small personal bookmarks manager. Client-side app; data in localStorage.

## Run

    python3 serve.py --port 8090

Open http://127.0.0.1:8090 (or whichever port you chose; 8080 is often busy on this machine). `/healthz` answers 200 while it is up.

## Project notes

- No build step and no external dependencies; plain HTML/CSS/JS.
- The automated checks drive the app through the QA hooks — see `QA.md`.
  Keep every existing `data-testid` intact.
- Development happens session by session; each session ends with the app
  runnable and `HANDOFF.md` updated.

## Layout

    index.html      the app page
    app.js          application logic
    styles.css      styles
    serve.py        dev server
    QA.md           QA hook conventions
    HANDOFF.md      written at the end of each session (once created)
