# log.md — Brief R (release notes page), workspace r-b2

All authority access went through the audited runner `./run-authority` (wrapper over
`/home/xrim/design-authority/tools/da.py`); every call is machine-recorded in `audit.jsonl`
(52 calls: 1×overview, 1×--help, 21×inspect, 13×resolve, 9×search, 3×discover, 1×gaps,
1×gap-add help, 1×gap-add failed (bad syntax), 1×gap-add ok, 1×validate).
Condition file: `lexical+semantic` — semantic `discover` allowed; used only where resolve
was UNDEFINED/thin, and only as a retrieval signal (each proposed artifact inspected before adoption).
Authority: triage 0.12.1 @ ec490bb7. Every command below is in execution order.

---

**1. `./run-authority overview`**
`out:` triage 0.12.1; component=56 guideline=10 pattern=7 token-set=7; rules=19 fallbacks=3 prohibitions=6; ladder CONFLICT→RESOLVED→COMPOSE→FALLBACK→UNDEFINED.
`Why + conclusion:` establish surface and counts before building; snapshot pinned @ ec490bb7.

**2. `./run-authority --help`**
`out:` subcommands overview/search/discover/inspect/resolve/validate/golden/gaps/gap-add/propose/review/precedents/precedent-check/candidates.
`Why + conclusion:` learn exact syntax; discover is an optional retrieval extension — retrieval only, never authority.

**3. `./run-authority resolve "release notes page with a list of past releases, each showing version, date, summary and a stable/beta status" --json`**
`out:` FALLBACK → fallback/scoped-embedding (matched scope "pag").
`Why + conclusion:` the whole-page ask has no artifact; scoped-embedding does not apply (we style the whole page) — decompose into recorded pieces.

**4. `./run-authority resolve "app shell with sidebar navigation" --json`**
`out:` RESOLVED component/shell (.app / .side / .main); alternatives nav-item, topbar, bottom-nav.
`Why + conclusion:` the app chrome is covered — adopt the recorded shell rather than inventing layout.

**5. `./run-authority resolve "page header with title and description" --json`**
`out:` RESOLVED component/page-head (.page-head / .page-title / .page-desc).
`Why + conclusion:` page title block is recorded — use it verbatim.

**6. `./run-authority resolve "status badge for stable or beta" --json`**
`out:` RESOLVED component/badge; states neutral/ok/warn/err/acc/solid; a11y "never the only signal — pair with text".
`Why + conclusion:` stable/beta status = badge; its own text carries the meaning (dots stay decorative).

**7. `./run-authority resolve "feed of releases with version, date and a one-line summary" --json`**
`out:` UNDEFINED; closest diff/dp/tl each 4.0 (threshold 6.5); fallback policy note: mark improvisation, report gap.
`Why + conclusion:` no "release feed" artifact — candidate row shapes must be inspected individually.

**8. `./run-authority resolve "tabs to narrow a list to one channel" --json`**
`out:` UNDEFINED; closest index-row 5.5, tabs 5.0.
`Why + conclusion:` tabs not directly resolved for filtering — check alternatives (seg / chip) before choosing a control.

**9. `./run-authority resolve "release notes" --json`**
`out:` UNDEFINED; closest ~1.5.
`Why + conclusion:` no release-notes concept in the catalogue at all — confirms this screen is a composition job.

**10. `./run-authority discover "feed of releases with version, date and a one-line summary" --k 5`**
`out:` dashboard, tl, dp, notif, diff (rrf-scored; retrieval only).
`Why + conclusion:` semantic neighbour for a release feed is component/tl (aliases "version timeline") — inspect it.

**11. `./run-authority discover "tabs to narrow a list to one channel" --k 5`**
`out:` tabs #1, then rule INT003, bottom-nav, crumbs, notif.
`Why + conclusion:` retrieval points at tabs; resolve said no — inspect tabs and INT003 before deciding.

**12. `./run-authority discover "release notes" --k 5`**
`out:` accessibility, TDS008, philosophy, bulkbar, chip.
`Why + conclusion:` nothing screen-level; note TDS008 (font rule) as a constraint to honour.

**13. `./run-authority inspect component/tl`**
`out:` Timeline; aliases incl. "version timeline", "version history"; states default/status-dots; verify .tl/.tl-item/.tl-dot.ok/.tl-dot.err; a11y: ordered list, dots decorative.
`Why + conclusion:` exactly the release-history shape — adopt tl as the list; dots may carry channel colour but text must too (badges).

**14. `./run-authority inspect component/tabs`**
`out:` Tabs; roving focus "wired by components.js"; panels hidden not unmounted; one tab always selected.
`Why + conclusion:` tabs are a panel switcher whose behaviour layer is not shipped here — weaker fit than a filter control; keep looking.

**15. `./run-authority inspect component/audit-row`**
`out:` flat provenance rows (time/actor/detail) for accountable actions.
`Why + conclusion:` audit rows are for action provenance, wrong semantics for releases — rejected.

**16. `./run-authority inspect component/index-row`**
`out:` 54px min height; "one row = one destination" (menu rows).
`Why + conclusion:` these are navigation destinations; releases are not destinations — rejected.

**17. `./run-authority inspect INT003`**
`out:` rule: feedback via banner/toast/empty state only.
`Why + conclusion:` no ad-hoc alerts on the page; a filter needs no flash (no mutation).

**18. `./run-authority inspect TDS008`**
`out:` error rule: font-family must be Geist / Geist Mono / inherit.
`Why + conclusion:` any improvised control must not introduce an off-system font — noted for chip buttons.

**19. `./run-authority search "filter"`**
`out:` cb 4.0, chip 4.0 — no decisive hit.
`Why + conclusion:` lexical search alone is inconclusive; try the control names directly.

**20. `./run-authority search "segmented"`**
`out:` component/seg (Segmented control) 9.0.
`Why + conclusion:` a segmented control exists — resolve it against the exact need.

**21. `./run-authority search "chip"`**
`out:` component/chip 19.0.
`Why + conclusion:` chip is a strong candidate for the channel filter — compare against seg.

**22. `./run-authority resolve "segmented control to narrow the list to one channel" --json`**
`out:` RESOLVED component/seg; "inline segmented selector for mutually exclusive views".
`Why + conclusion:` seg is sanctioned for the exact need — but inspect its states before betting the filter on it.

**23. `./run-authority inspect component/seg`**
`out:` no states-matrix entry; class .seg; no selected-state contract recorded.
`Why + conclusion:` .seg has no documented selected state (CSS has only .seg + .btn seam) — a filter UI needs a visible selected state, so prefer a control that records one.

**24. `./run-authority search "feed"`**
`out:` only pattern/dashboard 1.5.
`Why + conclusion:` the .feed row styles are dashboard-scoped, not a public component — do not adopt them as a component.

**25. `./run-authority search "empty state"`**
`out:` component/empty 18.0; page-state 8.0; guideline/voice 8.0.
`Why + conclusion:` empty state exists if a channel ever has no releases; note for completeness (not needed with this data).

**26. `./run-authority search "release"`**
`out:` no hits.
`Why + conclusion:` confirms the gap: "release" is absent from the catalogue's vocabulary.

**27. `./run-authority inspect guideline/interaction-standard`**
`out:` binding; three feedback channels (banner persistent / toast transient / empty structural); exceptions register.
`Why + conclusion:` keep the page mute (no banner/toast needed); the filter is not a mutation.

**28. `./run-authority resolve "stacked list of releases each with a status badge and date" --json`**
`out:` RESOLVED component/badge.
`Why + conclusion:` re-confirms badge for status per release; still need the row container.

**29. `./run-authority resolve "timeline of past release versions with dates and summaries" --json`**
`out:` RESOLVED component/tl.
`Why + conclusion:` direct RESOLVED for the release list → adopt tl as the release-history container.

**30. `./run-authority inspect fallback/no-js`**
`out:` behaviour layer is additive; never require JS for content; prefer native elements.
`Why + conclusion:` filter + drawer may be scripted only additively; full list must render without JS.

**31. `./run-authority inspect component/nav-item`**
`out:` states default/hover/active; a11y aria-current="page" on the active item; active rail via border-inline-start.
`Why + conclusion:` nav items need aria-current on "Release notes" — recorded contract for the sidebar.

**32. `./run-authority inspect component/empty`**
`out:` h4 + one-line reason + at most one action; never a bare blank area.
`Why + conclusion:` only if a filtered channel could be empty; our channels always have items so not rendered.

**33. `./run-authority resolve "chips to narrow a list to one channel" --json`**
`out:` UNDEFINED; closest index-row 5.5, audit-row 4.0, chip 4.0.
`Why + conclusion:` chip not resolved under this wording — inspect the chip artifact itself for its recorded states.

**34. `./run-authority inspect component/chip`**
`out:` Chip; alias "filter chip"; states default/hover/active(selected)/focus-visible; verify .chip.active; a11y: counts live in .n, whole chip is the target.
`Why + conclusion:` the chip records a selected state and a count slot — strong candidate for the channel filter.

**35. `./run-authority gaps`**
`out:` no gaps recorded in this workspace.
`Why + conclusion:` nothing pre-filed; expected to file one for the release-notes screen.

**36. `./run-authority gap-add --help`**
`out:` --need, --context (JSON), --scope, --workspace.
`Why + conclusion:` learn the exact schema (context is a JSON object, not free text).

**37. `./run-authority inspect guideline/brand`**
`out:` mark = 24×24 ink square; never theme by overriding components; tokens are the source.
`Why + conclusion:` brand mark is a plain .brand-mark square — use it as recorded; no per-component overrides anywhere.

**38. `./run-authority resolve "filter chips in a toolbar to narrow a list" --json`**
`out:` RESOLVED component/chip.
`Why + conclusion:` the filter-chip reading of the toolbar idiom is sanctioned → chip + .active is the channel filter (over seg, which lacks a selected state).

**39. `./run-authority resolve "filter chips to select one release channel" --json`**
`out:` UNDEFINED (cb 14.0 / chip 13.0 listed but under threshold).
`Why + conclusion:` wording-sensitive; entry 38 already RESOLVED the same need — chip stands; note resolution sensitivity for the log.

**40. `./run-authority search "toolbar"`**
`out:` no hits.
`Why + conclusion:` .toolbar is page furniture, not a component — do not lean on it; use .row.chiprow for the chip row.

**41. `./run-authority inspect component/topbar`**
`out:` tablet/phone header (menu, title, status); hidden on desktop.
`Why + conclusion:` include the topbar for <1024px chrome with the menu button.

**42. `./run-authority inspect component/bottom-nav`**
`out:` persistent phone tab bar.
`Why + conclusion:` include bottom-nav for phone chrome; text links fine (sprite icons are not shipped in assets).

**43. `./run-authority inspect guideline/accessibility`**
`out:` WCAG 2.2 scorecard, all pass; focus ring global, never removed; reduced motion honoured; target size floor 24px.
`Why + conclusion:` keep the global focus ring untouched and target sizes ≥24px (chip 29px ok).

**44. `./run-authority inspect guideline/voice`**
`out:` sentence case for buttons/links/menu items; three flash kinds; name the object; empty states title+reason+≤1 action.
`Why + conclusion:` chip/nav labels sentence case; no mutation announcements needed on this page.

**45. `./run-authority search "page"`**
`out:` page-head / page-state / shell; patterns: dashboard, misc, settings, viewer.
`Why + conclusion:` no release-notes page anywhere — confirms the pattern gap.

**46. `./run-authority search "pattern"`**
`out:` the 7 patterns: dashboard, misc (Index & eval), flows, learning, settings, simulator, viewer; candidates listed separately.
`Why + conclusion:` full pattern enumeration — none covers releases; composition + gap report is the correct route.

**47. `./run-authority inspect guideline/consumption`**
`out:` global path = tokens.css + base.css + (patterns.css) + components.js.
`Why + conclusion:` link the three shipped CSS files in that order; components.js is not shipped here (behaviour re-delegated additively, marked in the page).

**48. `./run-authority inspect component/shell`**
`out:` page skeleton .app/.side/.main; contract on /components/navigation.
`Why + conclusion:` final confirmation of shell classes before markup.

**49. `./run-authority inspect pattern/viewer`**
`out:` detail page pattern (two-column detail + audit) — not a releases screen.
`Why + conclusion:` last pattern check; rejected; proceed to compose tl + chip + badge inside the shell.

**50. `./run-authority gap-add --need "Release notes / version-history screen: …" --context "…attempted: resolve(…) -> UNDEFINED…" --scope "pattern"`**
`out:` rc 1 — JSONDecodeError: --context must be a JSON object, not free text.
`Why + conclusion:` syntax fix: pass context as JSON; re-run.

**51. `./run-authority gap-add --need "Release notes / version-history screen: chronological list of releases (version, date, one-line summary) with narrowing to one channel and a stable/beta status per release" --context '{"brief":"R","workspace":"r-b2","condition":"lexical+semantic","attempted":"resolve(\"release notes\") -> UNDEFINED; no pattern covers a releases screen","composed_from":["component/tl","component/chip","component/badge"],"unrecorded":["channel to status-colour semantics (stable/beta) for badge and tl-dot","filter-chip toggle behaviour (additive JS)"]}' --scope "pattern"`**
`out:` filed gap/20261008-131712-22e533, status open.
`Why + conclusion:` fallback policy satisfied — nearest recorded pieces used, improvisation marked in-page, gap reported.

**52. `./run-authority validate index.html`**
`out:` validator triage-lint: ok; findings: 0 errors=0 warnings=0 info=0; spec score=100.
`Why + conclusion:` first run already clean at 0/0/100 — accept the artifact.

---

## Non-authority notes (for completeness)

- Read from the workspace assets only (no authority calls): `assets/tokens/tokens.css`,
  `assets/core/base.css`, `assets/core/patterns.css` — class vocabulary, shell media queries,
  `.chip`/`.tl`/`.badge`/`.seg`/`.toolbar`/`.empty` rules, `@font-face` (`../fonts/*.woff2`).
- Marked improvisations kept visible in `index.html` comments: chip `style="font-family:inherit"`
  (no page stylesheet shipped; system idiom is `font:inherit`; TDS008 allows "inherit"),
  channel→status mapping stable=ok / beta=warn on badge + `.tl-dot`, and the additive inline
  re-delegation of the drawer and filter (components.js/shell.js not shipped in assets).
- Local smoke-test of `index.html` in a browser (file://, no network): 3 stylesheets load, Geist
  resolves on chips, filter switches 8→4 (stable) / 8→4 (beta) with aria-pressed + live status
  updates, drawer opens/closes with `aria-expanded`, no horizontal overflow at 320/390px, no
  console errors. `validate` re-run not needed (no page changes after call 52).
