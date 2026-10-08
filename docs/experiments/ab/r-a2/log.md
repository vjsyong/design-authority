# Build log — R: Release notes page (cell r-a2, lexical retrieval)

Deliverable: `index.html` — one self-contained release notes page for the Mail Triage app, styled only from `assets/tokens/tokens.css`, `assets/core/base.css`, `assets/core/patterns.css`.
Every command below was run from this workspace through the audited runner (`./run-authority`); the machine trace is `audit.jsonl` (34 calls, execution order).
Final result: `./run-authority validate index.html` → triage-lint ok, **0 errors / 0 warnings / 0 info, spec score 100**.

Adopted records: `component/shell`, `component/nav-item`, `component/page-head`, `component/chip`, `component/tl`, `component/badge`.
Gap filed: `gap/20261008-131736-f4ac7b` — narrowing a list to one channel has no recorded pattern.

---

1. `./run-authority overview`
   Key output: triage — 0.12.1; artifacts: component=56, guideline=10, pattern=7, token-set=7; rules=19 fallbacks=3 prohibitions=6; resolution: CONFLICT → RESOLVED → COMPOSE → FALLBACK → UNDEFINED.
   *Why + conclusion:* Start with the mandated orientation. The catalogue is large and resolution is a staged pipeline, so some needs will legitimately end UNDEFINED and must be handled via the fallback policy.

2. `./run-authority --help`
   Key output: surfaces = overview, search, discover, inspect, resolve, validate, golden, gaps, gap-add, propose, review, precedents, precedent-check, candidates; `discover` and `resolve --assist` are optional retrieval extensions.
   *Why + conclusion:* Map the allowed surfaces before querying. Stay on search/inspect/resolve (+ golden/validate/gap-add); `discover`/`--assist` are semantic and blocked in this lexical cell.

3. `./run-authority search "release"`
   Key output: (no matches).
   *Why + conclusion:* Probe for release-specific artifacts. None exist under this word — search is literal, so UI needs must go through natural-language `resolve`.

4. `./run-authority search "changelog"`
   Key output: 1.0 guideline/consumption only.
   *Why + conclusion:* No changelog artifact; the release list will have to resolve to a general list/timeline component.

5. `./run-authority search "badge"`
   Key output: 19.0 component/badge — "Badge".
   *Why + conclusion:* A recorded status indicator exists for the stable/beta channel marker; adopt candidate.

6. `./run-authority search "channel"`
   Key output: (no matches).
   *Why + conclusion:* No channel-specific artifact; filtering will need a general control (chips) plus fallback reporting.

7. `./run-authority search "sidebar"`
   Key output: component/nav-item (4.0), component/shell (4.0), component/kv (1.5), component/topbar (1.5).
   *Why + conclusion:* Chrome candidates identified; confirm via `resolve` with the full need wording.

8. `./run-authority search ""`
   Key output: (no matches — empty query returns nothing).
   *Why + conclusion:* No catalogue dump via search; must probe with terms.

9. `./run-authority search "component"`
   Key output: candidates (behavioural-verification, provenance-contract, rendered-verification) + component/shell (1.5), component/tabs (1.5), fallback/no-js (1.5), fallback/scoped-embedding (1.5).
   *Why + conclusion:* Term-only search is noisy; the reliable route for needs is `resolve` (per brief).

10. `./run-authority resolve --help`
    Key output: `resolve problem [--context] [--json] [--assist {off,semantic}]`.
    *Why + conclusion:* Confirm flags before the main query round — `--json` for machine-readable output; `--assist` is blocked in this cell, so plain lexical resolve only.

11. `./run-authority validate --help`
    Key output: `validate target [--snapshot] [--json]`.
    *Why + conclusion:* Confirm the closing validator interface before building.

12. `./run-authority gap-add --help`
    Key output: `gap-add --need NEED [--context CONTEXT] [--scope SCOPE] [--workspace WORKSPACE]`.
    *Why + conclusion:* Confirm how to file the fallback gap for unrecorded needs.

13. `./run-authority inspect --help`
    Key output: `inspect id`.
    *Why + conclusion:* Confirm the single-record inspection interface used to vet every adoptable record.

14. `./run-authority resolve "release notes page: a chronological list of past releases, each row showing version number, release date and a one-line summary" --json`
    Key output: RESOLVED → component/index-row (evidence 13.0; matched row/list). Alternatives: audit-row, kv, diff.
    *Why + conclusion:* First-candidate for the release list (index row in an index list); keep as candidate and compare before adopting — "one row = one destination" may not fit a read-only list.

15. `./run-authority resolve "a control to filter a list down to one channel: stable or beta" --json`
    Key output: UNDEFINED (top candidate index-row 5.5 < 6.5; fallback policy attached: build from nearest recorded pieces, mark improvisation, report a gap).
    *Why + conclusion:* No recorded filterable-list pattern for this phrasing; retry with sharper control wording before declaring a gap.

16. `./run-authority resolve "a small labelled indicator showing whether a release is stable or beta" --json`
    Key output: UNDEFINED (top candidate btn 4.0).
    *Why + conclusion:* Wording missed the catalogue vocabulary; rephrase using "status badge" (found in search #5) rather than "indicator".

17. `./run-authority resolve "app shell with sidebar navigation for a page in the app" --json`
    Key output: RESOLVED → component/shell (evidence 32.5; matched sidebar/shell/app/navigation). Alternatives: nav-item (9.5), topbar (5.5), bottom-nav (4.0).
    *Why + conclusion:* Chrome resolved: the app shell (`.app/.side/.main` + content frame). Adopt shell; nav-item also needed for the sidebar list.

18. `./run-authority resolve "filter chips row to narrow a list by channel" --json`
    Key output: UNDEFINED — two candidates tied (component/chip 13.0, component/index-row 13.0), no clean single match.
    *Why + conclusion:* Mixed object words split the match; simplify the query to just the control.

19. `./run-authority resolve "chips that filter content to one category" --json`
    Key output: RESOLVED → component/chip (evidence 13.0; matched filter/chip/"filter chip").
    *Why + conclusion:* The filter control is recorded: chips. Adopt chip for the channel filter; the *behaviour* of filtering a list stays unrecorded → fallback + gap.

20. `./run-authority resolve "status badge for a release item" --json`
    Key output: RESOLVED → component/badge (matched "status badge").
    *Why + conclusion:* Stable/beta markers are badges (`.badge.ok` / `.badge.warn`), with text labels per the record's a11y note.

21. `./run-authority resolve "page header with a title and a short description" --json`
    Key output: RESOLVED → component/page-head (`.page-head` — title, description and actions).
    *Why + conclusion:* Page title block recorded; adopt.

22. `./run-authority inspect component/index-row`
    Key output: class `.index-row` (patterns.css); states default/hover/active/focus-visible; a11y: 54px minimum height; one row = one destination.
    *Why + conclusion:* Inspected before any adoption. Viable, but each row demands a destination and the timeline vocabulary (golden) points elsewhere — keep as alternative.

23. `./run-authority inspect component/shell`
    Key output: class `.app`; page skeleton: sidebar, main column, content frame (`.app/.side/.main`); shell contract on /components/navigation.
    *Why + conclusion:* Adopt for the page chrome (sidebar + topbar + content frame), per brief "usual chrome".

24. `./run-authority inspect component/nav-item`
    Key output: class `.nav-item`; a11y: aria-current="page" on the active item; active rail is border-inline-start.
    *Why + conclusion:* Adopt for sidebar links; mark the Release notes item with `.active` + `aria-current="page"`.

25. `./run-authority inspect component/badge`
    Key output: class `.badge`; states neutral/ok/warn/err/acc/solid; a11y: uppercase micro-label; never the only signal — pair with text.
    *Why + conclusion:* Adopt: `.badge.ok` = Stable, `.badge.warn` = Beta, each carrying its own text label.

26. `./run-authority inspect component/chip`
    Key output: class `.chip`; states default/hover/active(selected)/focus-visible; a11y: counts live in `.n`; the whole chip is the target.
    *Why + conclusion:* Adopt for the channel filter row (`All/Stable/Beta` + counts in `.n`, selected = `.active`).

27. `./run-authority inspect component/page-head`
    Key output: class `.page-head`; "the title row at the top of a page: title, description and actions".
    *Why + conclusion:* Adopt for the "Release notes" title + description block.

28. `./run-authority golden`
    Key output: agreement 56/56 (100%); notable mappings: "a version timeline" → component/tl, "a status badge" → badge, "a chip" → chip; prohibitions: rounded corners → CONFLICT.
    *Why + conclusion:* The authority's own vocabulary pairs *version* with the timeline component — probe `component/tl` as a better release-list fit than index-row.

29. `./run-authority resolve "release notes as a version timeline: each entry shows version, date and a one-line summary" --json`
    Key output: RESOLVED → component/tl (aliases: "version timeline", "version history").
    *Why + conclusion:* Confirmed: the release list is a version timeline. Switch from index-row to tl.

30. `./run-authority inspect component/tl`
    Key output: class `.tl`; states default/status-dots; verify `.tl`, `.tl-item`, `.tl-dot.ok`, `.tl-dot.err`; a11y: ordered list; dots are decorative (the text carries the meaning).
    *Why + conclusion:* Adopt: `<ol class="tl">` with `.tl-item` per release, decorative aria-hidden dots (ok/warn), version + badge, date in `.tl-time`, summary in `.tl-d`.

31. `./run-authority validate index.html`
    Key output: validator triage-lint: ok; findings: 0 errors=0 warnings=0 info=0; spec score=100.
    *Why + conclusion:* First validation pass after building with only recorded classes — clean, so no fixes needed.

32. `./run-authority gap-add --need "filter a list of releases down to one channel (stable or beta)" --context "r-a2 release notes page. resolve('a control to filter a list down to one channel: stable or beta') returned UNDEFINED - no recorded filterable-list pattern. Built from nearest recorded pieces: component/chip (filter chip) over component/tl (version timeline), filtering behaviour via a small, marked inline script in index.html; improvisation marked per fallback policy." --scope pattern`
    Key output: rc=1 — JSONDecodeError: `--context` must be a JSON value.
    *Why + conclusion:* First gap-add attempt; re-run with a JSON object for `--context`.

33. `./run-authority gap-add --need "filter a list of releases down to one channel (stable or beta)" --context '{"page":"release notes page (r-a2, docs/experiments/ab/r-a2)","attempted":"resolve(\"a control to filter a list down to one channel: stable or beta\") -> UNDEFINED; built from nearest recorded pieces component/chip (filter chip) over component/tl (version timeline) with a small marked inline script in index.html"}' --scope pattern`
    Key output: created `gap/20261008-131736-f4ac7b` (status: open; stored at `.design-authority/gaps.jsonl` in this workspace).
    *Why + conclusion:* Fallback policy satisfied for the unrecorded channel-filtering behaviour: nearest recorded pieces used, improvisation marked in `index.html`, gap reported.

34. `./run-authority validate index.html`
    Key output: validator triage-lint: ok; findings: 0 errors=0 warnings=0 info=0; spec score=100.
    *Why + conclusion:* Final closing run after all changes — 0 errors, 0 warnings, spec score 100 confirmed as the end state.

---

### Notes (non-authority checks, not part of the audited trail)

- File read-back: `<title>Release notes · Mail Triage</title>`; the three stylesheet links resolve to the workspace assets; no inline styles, no raw colours.
- Browser smoke test on `file://…/r-a2/index.html`: 9 release items render; sidebar width 236px (tokens active); channel filter works (Beta → 2 visible; reset → 9); no console errors observed.
- Content: 9 releases (7 stable, 2 beta) as a newest-first version timeline; the only improvisation is the inline filter script (gap above), marked in a comment in `index.html`.
