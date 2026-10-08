# Brief — build the Indaba Interface System documentation site, under its own authority

Build ONE self-contained page (`index.html`) that presents the **Indaba Interface System**
(Ubuntu-derived system (portability spike).) in ITS OWN visual language.

You are building UNDER this authority. Every visual decision must come from
its records:

- Orient: `./run-authority overview` (JSON manifest: counts, policy).
- Resolve each UI need in natural language: `./run-authority resolve "..." --json`.
- Inspect EVERY record before adopting it: `./run-authority inspect <id>`.
- The authority's token sets carry the values (colours with hexes, type
  rules, spacing, shape language). Quote them exactly; do not invent values.
- When the authority is silent (a doc page may need things it does not
  record): follow its fallback policy — build from the nearest recorded
  pieces, keep the improvisation visible (HTML comment + data-improv attr),
  and file a gap: `./run-authority gap-add` (run from this workspace).
- Never adopt anything from another pack. No external frameworks, no
  network, no borrowed CSS. The only styles are the ones you write from
  this authority's values.

Fonts available to copy into this workspace (copy the files you use):
  none local — use the recorded family (Ubuntu) as a stack: 'Ubuntu', system-ui, sans-serif

Page content (all generated from records, from this pack only):
1. A masthead: name, version, one-line description.
2. A catalogue: EVERY artifact in the pack, grouped by kind, each with its
   title and summary (use the authority's own list/card/cell components if
   it records any).
3. A specification summary: rules and prohibitions (titles/counts;
   quote a couple verbatim), fallbacks if present.
4. A footer line: "built under the indaba authority" + the pack version.

Rules of record:
- Cap about 35 authority calls; log EVERY call in `log.md` (numbered, exact
  syntax, trimmed output, one "Why + conclusion:" line each, in order).
- Deliver exactly `index.html` + any font files + `log.md`.
- The page must be readable at 1280px and 390px without horizontal scroll.

Success = a page that unmistakably wears THIS authority's language, with an
audit trail showing every adoption and every improvisation.
