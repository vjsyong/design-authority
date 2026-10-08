# log.md — R-B1 "Release notes page" build (audited authority calls)

Workspace: `/home/xrim/design-authority/docs/experiments/ab/r-b1` · condition: `lexical+semantic`
Deliverable: `index.html` (one self-contained page, styled only from `assets/`). Every authority call went through `./run-authority` (wrapper records audit.jsonl).
Adopted records: component/shell, component/nav-item, component/topbar, component/bottom-nav, component/page-head, component/chip, component/badge, component/tl, guideline/voice.
33 calls executed in order below (cap ~30; overage is 3 syntax-recovery calls: #11, #30, #31 — all logged honestly).

1. `./run-authority overview`
   → triage 0.12.1 @ ec490bb7f3; artifacts: component=56, guideline=10, pattern=7, token-set=7; rules=19, fallbacks=3, prohibitions=6; chain CONFLICT→RESOLVED→COMPOSE→FALLBACK→UNDEFINED.
   Why + conclusion: Establish the authority's scope before retrieval. Enough coverage to attempt every need in the brief.

2. `./run-authority --help`
   → subcommands: overview/search/discover/inspect/resolve/validate/golden/gaps/gap-add/propose/precedents/candidates.
   Why + conclusion: Learn the exact CLI surface. Working set: resolve + inspect + validate + gap-add.

3. `./run-authority resolve "app shell page chrome with a fixed sidebar navigation for the whole app" --json`
   → RESOLVED → component/shell (.app/.side/.main; alternatives: nav-item 9.5, topbar 7.0).
   Why + conclusion: Brief requires the app's usual chrome; the shell is recorded — adopt it for the page skeleton.

4. `./run-authority resolve "release notes page listing past releases: each entry has a version, a date and a one-line summary" --json`
   → FALLBACK → fallback/scoped-embedding (embedding Triage into a host page — not applicable); no alternatives.
   Why + conclusion: No page pattern covers release notes. Follow fallback policy: build from nearest recorded pieces, keep improvisation visible, report a gap (#32).

5. `./run-authority resolve "badge showing whether a release is stable or beta" --json`
   → UNDEFINED; closest component/badge scored 4.0 vs threshold 6.5; fallback policy says mark improvisation + report gap.
   Why + conclusion: Badge component exists but stable/beta semantics are unrecorded — adopt badge with a marked mapping, file gap (#33).

6. `./run-authority resolve "filter chips to narrow a list to a single channel" --json`
   → RESOLVED → component/chip (13.0; a11y: counts in `.n`, whole chip is the target).
   Why + conclusion: The "narrow to one channel" need has a sanctioned pattern — filter chips. Adopt.

7. `./run-authority discover "release notes page listing past releases: each entry has a version, a date and a one-line summary" --k 5`
   → candidates: component/tl (rrf .032 retr, sem#1), component/dp, guideline/voice, component/diff, pattern/dashboard.
   Why + conclusion: #4 was thin (FALLBACK), so use the sanctioned discovery extension. Timeline is the strongest signal — inspect it (#12).

8. `./run-authority search "release notes changelog version history"`
   → 13.0 component/tl Timeline; 4.0 component/diff.
   Why + conclusion: Cross-check discovery. Version-history wording lands on tl; feed/diff candidates fall away.

9. `./run-authority search "feed list of dated entries"`
   → audit-row/index-row/kv/notif all 4.0; pattern/dashboard 1.5.
   Why + conclusion: Test the dashboard feed alternative. Generic row components, no version semantics — weaker than tl.

10. `./run-authority search "timeline"`
    → 14.0 component/tl.
    Why + conclusion: Direct-term check. Confirmed.

11. `./run-authority inspect component/tl --json`
    → rc=2: "unrecognized arguments: --json".
    Why + conclusion: inspect takes no `--json`. Rerun bare (#12).

12. `./run-authority inspect component/tl`
    → class `.tl`; ordered list; verify `.tl/.tl-item/.tl-dot.ok/.tl-dot.err`; aliases incl. "version timeline".
    Why + conclusion: Read the record before adopting. Ordered list + documented dot states fit a release history — adopt tl for the list.

13. `./run-authority inspect component/shell`
    → `.app/.side/.main` skeleton with `.brand/.nav/.nav-item` inside; stable.
    Why + conclusion: Adopt exact skeleton classes; no improvisation needed for chrome.

14. `./run-authority inspect component/badge`
    → states neutral/ok/warn/err/acc/solid; a11y: "never the only signal — pair with text".
    Why + conclusion: Adopt badge for channel labels; visible text ("stable"/"beta") keeps it compliant.

15. `./run-authority inspect component/chip`
    → states default/hover/active(selected)/focus-visible; counts live in `.n`.
    Why + conclusion: Adopt chips as the channel filter with count spans; selected state = `.active`.

16. `./run-authority resolve "page header with a page title and a short description" --json`
    → RESOLVED → component/page-head (`.page-head/.page-title/.page-desc`).
    Why + conclusion: Recorded title-row block; adopt for the page head.

17. `./run-authority resolve "sidebar navigation menu items with icons and labels, grouped under a section label" --json`
    → RESOLVED → component/menu-item (nav-item alternative 12.0).
    Why + conclusion: menu-item is the dropdown/overflow row (armed delete etc.) — off-target for sidebar links. Re-resolve with sharper wording (#18).

18. `./run-authority resolve "navigation links in the sidebar, each with an icon and a label, current page highlighted" --json`
    → RESOLVED → component/nav-item (23.5).
    Why + conclusion: Correct artifact for sidebar links; adopt nav-item + nav-label groups.

19. `./run-authority inspect component/nav-item`
    → a11y: `aria-current="page"` on the active item; active rail is border-inline-start.
    Why + conclusion: Contract for the current-page link; follow it in markup.

20. `./run-authority search "shell contract navigation"`
    → shell 7.0; bottom-nav 4.0; nav-item 4.0.
    Why + conclusion: Chase the shell record's "/components/navigation" pointer. Mobile chrome = topbar/bottom-nav — inspect both (#26, #27).

21. `./run-authority precedents`
    → 1 negative precedent: do not keep pre-0.1.0 (mail-triage era) vocabulary alongside new names.
    Why + conclusion: Check prohibitions before writing markup. Use only current class names — as planned.

22. `./run-authority inspect guideline/voice`
    → sentence case for buttons/links/menu items; flash kinds ok/warn/err only; empty states = title + one-line reason + at most one action.
    Why + conclusion: Copy rules for labels and the empty state; apply sentence case throughout.

23. `./run-authority search "toolbar filter chips row above a list"`
    → chip 13.0, index-row 13.0, audit-row/kv 8.0, …
    Why + conclusion: Look for a dedicated filter-row pattern. None exists — the chip row itself is the sanctioned form.

24. `./run-authority golden`
    → 56/56; "a version timeline → component/tl"; "a status badge → component/badge"; "a nav item → component/nav-item"; "a chip → component/chip".
    Why + conclusion: Independent confirmation of the adoption set. Version timeline is a golden path — tl choice is safe.

25. `./run-authority search "queuebar chip row filters above a list"`
    → chip 13.0 top; no queuebar/toolbar artifact.
    Why + conclusion: Probe sheet idioms (.queuebar/.tchips) for a container name. None recorded — use the sheet's own chip-row classes.

26. `./run-authority inspect component/topbar`
    → tablet/phone chrome header (menu, title, status); hidden on desktop.
    Why + conclusion: Confirm topbar scope before using it for tablet chrome.

27. `./run-authority inspect component/bottom-nav`
    → persistent phone tab bar.
    Why + conclusion: Confirm phone chrome contract; include bottom-nav for phone widths.

28. `./run-authority validate index.html`
    → validator triage-lint: ok; findings: 0 errors=0 warnings=0 info=0; spec score=100.
    Why + conclusion: Mandated end check — clean on the first pass. index.html not edited afterwards, so this result stands.

29. `./run-authority gap-add --help`
    → usage: `--need NEED [--context CONTEXT] [--scope SCOPE] [--workspace WORKSPACE]`.
    Why + conclusion: Get exact gap-add syntax before filing.

30. `./run-authority gap-add --need "A release-notes / changelog page pattern: …" --context "resolve returned FALLBACK (scoped-embedding, not applicable to this page); …"`
    → rc=1: JSONDecodeError — `--context` must be a JSON object.
    Why + conclusion: Plain-text context rejected by the tool; refile with JSON (#32).

31. `./run-authority gap-add --need "Recorded status semantics for a release channel: …" --context "resolve was UNDEFINED (component/badge scored 4.0 vs 6.5 threshold). …"`
    → rc=1: same JSONDecodeError.
    Why + conclusion: Same fix required for the second gap; refile (#33).

32. `./run-authority gap-add --need "A release-notes / changelog page pattern: a dated list of releases (version, date, one-line summary) with a channel filter" --context '{"attempted": "resolve returned FALLBACK (scoped-embedding, not applicable to this page); no pattern artifact covers release notes", "built_from": ["component/shell","component/page-head","component/chip","component/tl"], "outcome": "FALLBACK"}'`
    → gap/20261008-131837-656b2d recorded (status open; stored in .design-authority/gaps.jsonl).
    Why + conclusion: FALLBACK outcome from #4 reported per the fallback policy.

33. `./run-authority gap-add --need "Recorded status semantics for a release channel: which badge/dot states should mean stable vs beta" --context '{"attempted": "resolve was UNDEFINED (component/badge scored 4.0 vs 6.5 threshold)", "improvisation": "stable maps to ok, beta maps to warn; adopted component/badge and component/tl dots", "outcome": "UNDEFINED"}'`
    → gap/20261008-131838-de75ef recorded (stored in .design-authority/gaps.jsonl).
    Why + conclusion: UNDEFINED outcome from #5 reported; the improvisation itself is marked in index.html.

---

Build notes (non-command): page = component/shell skeleton + nav-item sidebar groups, topbar (tablet) + bottom-nav (phone) chrome, page-head, chip filter row (All/Stable/Beta with counts in `.n`), release list as ordered `.tl` timeline (8 releases: 5 stable → `badge ok`/`tl-dot ok`, 3 beta → `badge warn`/`tl-dot warn`), hidden empty state (title + reason + one action per voice), footer. Improvised pieces: stable/beta → ok/warn mapping (marked with an HTML comment at the chip row and reported as gap/20261008-131838-de75ef); inline Lucide-style SVGs (the system's icon sprite is not present in the workspace's assets/). Verified in a local browser: fonts load, sidebar fixed, chips filter 8→5→3→8 with aria-current, no JS errors.
