# Authority log — r-a1 (release notes page, lexical cell)

All authority calls went through `./run-authority` (audited wrapper; machine record in `audit.jsonl`).
Cell condition: `lexical` — `discover` and `resolve --assist` are unavailable by design.
40 calls recorded in total: 38 succeeded, 2 failed (multi-ID inspect, malformed gap context) and were retried.

---

1. `./run-authority overview`
   → triage 0.12.1 (format 0.1); artifacts: component=56, guideline=10, pattern=7, token-set=7; rules=19 recipes=0 fallbacks=3 prohibitions=6; resolution: CONFLICT -> RESOLVED -> COMPOSE -> FALLBACK -> UNDEFINED.
   Why + conclusion: orient first — the pack is components + guidelines + patterns with a defined fallback policy, so the release-notes screen must be resolved/answered from the catalogue or fall back deliberately.

2. `./run-authority --help`
   → subcommands available: overview, search, discover, inspect, resolve, validate, golden, gaps, gap-add, propose, review, precedents, precedent-check, candidates.
   Why + conclusion: learn the verbs; discover/--assist are excluded in this cell, so search → resolve → inspect is the discovery surface.

3. `./run-authority search "release notes"`
   → hits ≤2.0: candidate/behavioural-verification 2.0, candidate/rendered-verification 2.0, component/bubble 1.5, component/chip 1.5, component/dlg 1.5, component/savebar 1.5, guideline/accessibility 1.5, crumbs 1.0 — nothing topical.
   Why + conclusion: "release notes" is not directly recorded; the content list will need composition. Keep looking for chrome/status/filter pieces.

4. `./run-authority search "badge"`
   → component/badge 19.0 (dominant); candidate/behavioural-verification 2.0.
   Why + conclusion: releases must show stable/beta — component/badge is the status-label record; adopt.

5. `./run-authority search "filter tabs segmented"`
   → component/bottom-nav 4.0, component/cb 4.0, component/chip 4.0, component/seg 4.0, component/tabs 4.0, fallback/no-js 1.5.
   Why + conclusion: "narrow list to one channel" needs a filter control; seg/tabs/chip are candidates to resolve.

6. `./run-authority search "sidebar navigation shell"`
   → component/shell 9.5, component/nav-item 8.0, component/bottom-nav 4.0, component/kv 1.5, component/topbar 1.5, component/btn 1.0.
   Why + conclusion: the page must sit in app chrome; shell + nav-item are the recorded chrome, topbar/bottom-nav are its responsive variants.

7. `./run-authority search "list feed rows"`
   → component/index-row 13.0, component/audit-row 8.0, component/kv 8.0, component/menu-item 4.0, component/notif 4.0, component/tbl 4.0, crumbs 1.5, logpanel 1.5.
   Why + conclusion: looking for a recorded anatomy for the release list; no list-of-releases record exists — index-row/audit-row/tl are the nearest shapes.

8. `./run-authority search "release version changelog"`
   → component/diff 4.0, component/tl 4.0, candidate/provenance-contract 2.0, guideline/consumption 1.0.
   Why + conclusion: release-specific vocabulary lands on diff and tl — a timeline is the closest recorded shape for version history.

9. `./run-authority search "status date"`
   → component/badge 4.0, component/dot 4.0, component/dp 4.0, component/msg 4.0, token-set/colour 3.0, pattern/dashboard 1.5.
   Why + conclusion: stable/beta marker + date presentation — badge and dot are the status records; the date picker is irrelevant for display-only dates.

10. `./run-authority search "page pattern layout"`
    → component/shell 8.0, pattern/misc 5.5, token-set/spacing 5.5, pattern/dashboard 5.0, pattern/settings 5.0, pattern/viewer 5.0, component/page-head 4.0, component/page-state 4.0.
    Why + conclusion: enumerate page patterns — viewer/settings/dashboard exist, none is release-notes; page-head is the recorded title row.

11. `./run-authority search "segmented control"`
    → component/seg 18.0 (dominant).
    Why + conclusion: the segmented control is a distinct stable record; candidate for the channel filter.

12. `./run-authority search "empty state"`
    → component/empty 18.0, component/page-state 8.0, guideline/voice 8.0, component/stat 4.0, component/cmd 3.0, guideline/interaction-standard 3.0.
    Why + conclusion: structural states are covered if the list empties; noted, not needed on the happy path. (guideline/interaction-standard flagged for later — it is binding.)

13. `./run-authority resolve "release notes page listing past app releases with version, date and one-line summary, showing stable or beta channel, in the app shell with sidebar navigation" --json`
    → RESOLVED: component/shell (score 32.5); alternatives nav-item 9.5, topbar 5.5, bottom-nav 4.0.
    Why + conclusion: the page's chrome resolves to component/shell (sidebar + main + content frame); adopt the shell contract.

14. `./run-authority resolve "list of past releases showing version number, release date and one-line summary" --json`
    → UNDEFINED; closest diff/notif/tl 5.5 vs threshold 6.5. Fallback policy: build per consuming project's policy, mark the improvisation, report a gap.
    Why + conclusion: the core list has no direct record — this is the fallback case; compose from nearest pieces and file a gap.

15. `./run-authority resolve "narrow a list to one channel by selecting a filter option" --json`
    → UNDEFINED; closest cb 5.5, index-row 5.5 vs threshold 6.5.
    Why + conclusion: the filter interaction as phrased is unrecorded; component/seg remains a stable record for mutually-exclusive views, so use it as the nearest piece.

16. `./run-authority resolve "mark each release as stable or beta with a small status label" --json`
    → UNDEFINED; closest badge 8.0, guideline/brand 8.0, pattern/misc 5.5 (direct-match threshold not met at 6.5).
    Why + conclusion: resolve does not settle it, but component/badge is inspectable and stable — adopt it as the nearest recorded status label.

17. `./run-authority inspect component/shell`
    → stable; class `.app`; "the page skeleton: sidebar, main column and content frame (.app / .side / .main)"; source core/base.css.
    Why + conclusion: adopt — shell markup is `.app` > `.side` + `.main` > `.content`.

18. `./run-authority inspect component/nav-item`
    → stable; states default/hover/active(selected)/focus-visible; a11y: `aria-current="page"` on the active item.
    Why + conclusion: adopt for the sidebar; mark Release notes active with aria-current="page".

19. `./run-authority inspect component/badge`
    → stable; states neutral/ok/warn/err/acc/solid; a11y: "never the only signal — pair with text that says the same thing".
    Why + conclusion: adopt `.badge.ok` for Stable and `.badge.warn` for Beta; the badge text itself carries the channel word (not colour-only).

20. `./run-authority inspect component/seg`
    → stable; "the inline segmented selector for mutually exclusive views"; class `.seg`.
    Why + conclusion: adopt for the All/Stable/Beta filter (base.css composes it from `.btn` children).

21. `./run-authority inspect component/page-head`
    → stable; "title row at the top of a page: title, description and actions".
    Why + conclusion: adopt — page-title + page-desc on the left, the seg actions on the right.

22. `./run-authority inspect component/tl`
    → stable; states default/status-dots; a11y: "ordered list; dots are decorative (the text carries the meaning)"; aliases include "version timeline", "version history".
    Why + conclusion: adopt — `ol.tl` with tl-item/tl-dot/tl-time/tl-t/tl-d is the recorded shape for version history.

23. `./run-authority inspect pattern/misc`
    → stable; "Two small page patterns: the phone overflow index and blind-label review."
    Why + conclusion: not a fit for release notes; discarded.

24. `./run-authority resolve "version history" --json`
    → RESOLVED: component/tl (score 13.0, alias match "~version history").
    Why + conclusion: the list concept resolves to the timeline once phrased in the record's own vocabulary — adopt tl as the sanctioned release-history shape.

25. `./run-authority resolve "segmented control" --json`
    → RESOLVED: component/seg (score 18.0).
    Why + conclusion: filter control confirmed as a sanctioned record.

26. `./run-authority resolve "badge stable beta label" --json`
    → RESOLVED: component/badge (score 8.0).
    Why + conclusion: status label confirmed; pair with visible channel text per its a11y note.

27. `./run-authority inspect fallback/no-js`
    → "Every component degrades to its plain markup; the behaviour layer (components.js) is additive. Without JS, interactive widgets show their static forms... never require JS for content."
    Why + conclusion: the channel filter must be additive only — all releases render without JavaScript; filtering degrades to the full list.

28. `./run-authority gaps`
    → "no gaps recorded in .../r-a1".
    Why + conclusion: the missing release-notes pattern is not already filed; a new gap is warranted.

29. `./run-authority inspect component/topbar component/bottom-nav`
    → rc=2 "unrecognized arguments: component/bottom-nav".
    Why + conclusion: inspect takes a single ID — re-run the two records separately (next two entries).

30. `./run-authority inspect component/topbar`
    → stable; "tablet and phone chrome header (menu, title, theme and density toggles, status); hidden on desktop".
    Why + conclusion: adopt for the ≤1023px header; menu button + page title + status only (no theme/density toggles requested).

31. `./run-authority inspect component/bottom-nav`
    → stable; "the persistent phone tab bar".
    Why + conclusion: adopt for phone chrome (≤767px), with Releases marked `.on` + aria-current="page".

32. `./run-authority inspect guideline/interaction-standard`
    → binding; armed two-step deletes, confirm() only for one-way actions, show-the-reverse, three-channel feedback (banner/toast/empty state), save bars, copy rules.
    Why + conclusion: no mutations exist on this page (read-only list), so nothing needs arming/confirm; the list + status line are the feedback surface.

33. `./run-authority precedents`
    → 1 negative precedent: precedent/renamed-vocabulary — keep only the new (post-0.1.0) class vocabulary.
    Why + conclusion: nothing here contradicts the build; use current class names only (no mail-triage-era names).

34. `./run-authority inspect component/btn`
    → stable; states default/hover/active/focus-visible/disabled/busy; a11y: "Use a real <button> or <a>; never a clickable div. Icon-only buttons need aria-label."
    Why + conclusion: seg is composed of `.btn` children; buttons are real <button> elements and the icon-only menu button gets an aria-label.

35. `./run-authority validate index.html`
    → "validator triage-lint: ok; findings: 0 errors=0 warnings=0 info=0 spec score=100".
    Why + conclusion: required end check passed on the first run — the page conforms with no findings.

36. `./run-authority gap-add --help`
    → usage: `gap-add --need NEED [--context CONTEXT] [--scope SCOPE] [--workspace WORKSPACE]`.
    Why + conclusion: learn exact syntax before filing the gap.

37. `./run-authority gap-add --need ... --context "Brief R ... (plain text)" ...`
    → rc=1; JSONDecodeError: `--context` must be JSON.
    Why + conclusion: retry with a JSON object as the context argument.

38. `./run-authority gap-add --need "Release-notes / changelog page pattern: ..." --context '{"brief": "ab/r-a1 Brief R - release notes page", "resolve_attempts": [...UNDEFINED...], "resolution_used": ["component/tl", "component/badge", "component/seg", "component/shell + component/nav-item + component/topbar + component/bottom-nav"], "improvised": "release-list composition and filter wiring, marked in index.html"}' --scope "page pattern / release notes"`
    → gap/20261008-132312-da4853, status open, stored at `.design-authority/gaps.jsonl`.
    Why + conclusion: the unrecorded release-notes composition is now reported per the fallback policy.

39. `./run-authority search "card container panel"`
    → component/dock 4.0, component/logpanel 4.0, component/notif 4.0, component/proposal 4.0, pattern/learning 4.0, component/composer 1.5, component/stat 1.5, component/savebar 1.0, component/tabs 1.0 — no dedicated card record.
    Why + conclusion: `.card` is a base stylesheet utility (already in the provided assets), not a standalone record; no further resolution needed for wrapping the list.

40. `./run-authority validate index.html`
    → "validator triage-lint: ok; findings: 0 errors=0 warnings=0 info=0 spec score=100" (re-run on the frozen final state).
    Why + conclusion: final confirmation after log.md was written — no regressions, deliverable frozen at 0/0/100.

---

## Outcome

- Build: `index.html` — release notes in the app shell (sidebar + topbar + bottom-nav), `ol.tl` timeline list (date, version, one-line summary, Stable/Beta badge per release), `component/seg` channel filter (All/Stable/Beta) with a role="status" count line; filter is additive behaviour, all 7 releases render without JS.
- Adopted records (inspected): component/shell, component/nav-item, component/topbar, component/bottom-nav, component/page-head, component/seg, component/badge, component/tl, component/btn; policies: fallback/no-js, guideline/interaction-standard.
- Fallback: release-list composition + filter wiring are unrecorded → composed from nearest records, marked as improvisation in an HTML comment, gap filed (gap/20261008-132312-da4853).
- Validator: `./run-authority validate index.html` → 0 errors, 0 warnings, spec score 100.
