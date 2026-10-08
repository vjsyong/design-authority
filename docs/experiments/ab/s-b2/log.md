# log.md — Brief S (settings section) — build log

Workspace: `docs/experiments/ab/s-b2/` · condition: `lexical+semantic` (discovery allowed).
Deliverable: one self-contained `index.html` (styling only from `assets/tokens/tokens.css`, `assets/core/base.css`, `assets/core/patterns.css`) + this log.
Every call below went through the audited runner `./run-authority` (wrapper → repo venv `tools/da.py`; all recorded in `audit.jsonl`, 37 lines).
Result: `./run-authority validate index.html` → **0 errors, 0 warnings, spec score 100**; one gap filed (`gap/20261008-131653-da8ec0`).

Adopted authority records: `pattern/settings`, `component/px-sw`, `component/badge`, `component/shell`, `component/nav-item`, `component/topbar`, `fallback/no-js`, `guideline/voice`, `guideline/accessibility`.
Count note: 37 calls vs the ~30 cap — overage came from exploratory `search`/`--help` reconnaissance, one `gap-add` format retry (JSON arg), and a late `component/topbar` contract inspection.

---

1. `./run-authority overview`
   Out: triage 0.12.1 (format 0.1); snapshot triage-design-system @ ec490bb7f3; artifacts: component=56, guideline=10, pattern=7, token-set=7; rules=19 fallbacks=3 prohibitions=6; "resolution: CONFLICT -> RESOLVED -> COMPOSE -> FALLBACK -> UNDEFINED".
   Why + conclusion: baseline — authority reachable through the audited route; the 5-step resolution policy frames every answer that follows.

2. `./run-authority resolve "settings section for a preferences screen" --json`
   Out: RESOLVED → `pattern/settings` ("Task sections with a sticky side nav, scoped setting-row forms and per-card save bars", stable); evidence 18.5 ≥ 6.5.
   Why + conclusion: the brief's core element maps to a recorded stable pattern — adopt it as the page skeleton (`.settings-grid` / `.settings-nav` / `.setting-row`).

3. `./run-authority resolve "control to flip one preference on or off" --json`
   Out: UNDEFINED; closest `component/px-sw` (Switch) 4.0 < 6.5; fallback policy note: implement from nearest pieces, mark, report gap.
   Why + conclusion: natural wording missed the gate — do not improvise yet; inspect the nearest candidate and re-probe before deciding.

4. `./run-authority resolve "compact display of a preference's current state" --json`
   Out: UNDEFINED; closest empty/page-state/stat (all 4.0, "stat" token match) — none on-target.
   Why + conclusion: no direct match for a setting state display; likely genuine gap — keep probing (discovery/search) before concluding.

5. `./run-authority resolve "app chrome sidebar navigation" --json`
   Out: UNDEFINED; top candidate `component/shell` scored 9.5 (reported as below the 6.5 gate — engine quirk), plus nav-item 8.0, topbar 7.0.
   Why + conclusion: shell artifacts clearly exist; verify via discovery + inspect before adopting (resolve alone did not grant them here).

6. `./run-authority inspect pattern/settings`
   Out: stable; source site/pages_patterns.py; body thin (group + source_file) — the executable form is the CSS: `.settings-grid/.settings-nav/.setting-row` live in `assets/core/patterns.css`.
   Why + conclusion: pattern is real and thin on paper; build against its shipped CSS classes verbatim.

7. `./run-authority discover "control to flip one preference on or off" --k 5`
   Out: `component/px-sw` top (sem#1, cos 0.654), then settings / seg / prohibit/label-less-controls.
   Why + conclusion: discovery confirms px-sw as the switch; the label-less-controls prohibition reminds me the checkbox must carry an accessible name.

8. `./run-authority inspect component/px-sw`
   Out: stable; class `.px-sw`; states checked/unchecked/disabled/focus-visible; a11y: visible label wraps a real checkbox, aria-label carries the verb "Enable/Disable <object>", coarse pointers get 44px.
   Why + conclusion: adopt `.px-sw` as the toggle — markup `label.px-sw > input[checkbox] + span.px-tr`; verb in aria-label flips with state.

9. `./run-authority discover "compact display of a preference's current state" --k 5`
   Out: nav-item / settings / pager-num / motion-reduction — nothing about a setting state display.
   Why + conclusion: confirms no recorded state-display artifact; plan a *marked* composition from the nearest recorded pieces (badge/dot) + gap report.

10. `./run-authority discover "app chrome sidebar navigation" --k 5`
    Out: `component/shell` (cos 0.691), `component/topbar` (0.717), `component/bottom-nav`, `component/nav-item`, breakpoints.
    Why + conclusion: chrome = shell + nav-item (+ topbar for small widths); inspect the two used as structure.

11. `./run-authority inspect component/shell`
    Out: stable; class `.app` — sidebar, main column, content frame (`.app / .side / .main`), source core/base.css.
    Why + conclusion: adopt shell; the three linked assets carry the full class set already.

12. `./run-authority inspect component/nav-item`
    Out: stable; states default/hover/active/focus-visible; a11y: aria-current="page" on the active item; rail is border-inline-start (RTL-safe).
    Why + conclusion: sidebar nav items get aria-current="page"; Settings item is the active one.

13. `./run-authority resolve "status chip showing a setting is on or off" --json`
    Out: UNDEFINED; closest badge / chip / dot (all 4.0).
    Why + conclusion: still no status indicator; shortlist badge vs dot for the composition and confirm via inspect which is text-capable.

14. `./run-authority --help`
    Out: commands = overview search discover inspect resolve validate golden gaps gap-add propose review precedents precedent-check candidates; "discover ... retrieval only proposes; it never establishes authority".
    Why + conclusion: locks exact syntax for validate/gap-add; discovery is a signal, authority still comes from the recorded artifacts.

15. `./run-authority search "status chip"`
    Out: badge/chip/dot/msg at 4.0 — no status-chip artifact.
    Why + conclusion: reconfirms the gap is genuine; choose the recorded piece that can carry text (badge).

16. `./run-authority search "chip"`
    Out: `component/chip` 19.0 (filter/interaction chip).
    Why + conclusion: chip is an interactive filter unit, not a state display — badge remains the fit.

17. `./run-authority search "state"`
    Out: stat / empty / page-state / voice — no setting-state display.
    Why + conclusion: same conclusion; stop searching, proceed to policy reads.

18. `./run-authority inspect fallback/no-js`
    Out: "Every component degrades to its plain markup; the behaviour layer is additive"; constraints: never require JS for content; prefer native elements.
    Why + conclusion: the toggle is a native checkbox (works without JS); the state text update is additive JS only; content fully readable with JS off.

19. `./run-authority gaps`
    Out: "no gaps recorded in …/s-b2".
    Why + conclusion: baseline before filing; one gap will be added for the state display.

20. `./run-authority precedents`
    Out: 1 negative precedent (policy declines only) — old mail-triage names retired; one public vocabulary + rename map.
    Why + conclusion: build only with current 0.12.1 class vocabulary; no legacy names.

21. `./run-authority inspect component/badge`
    Out: stable; states neutral/ok/warn/err/acc/solid; a11y "uppercase micro-label; never the only signal — pair with text that says the same thing".
    Why + conclusion: badge as the state display basis works only because it *carries text* — "Enabled"/"Disabled" is the signal, colour is not relied on.

22. `./run-authority inspect component/dot`
    Out: stable; 7px square dot; variants "paired with text (never colour alone)".
    Why + conclusion: dot alone cannot carry the state text — badge (verbatim text) chosen for the compact display.

23. `./run-authority search "improvised"`
    Out: no results.
    Why + conclusion: no recorded marker convention for improvisations — mark it in-file (source comment), in this log, and via the gap record.

24. `./run-authority search "gap"`
    Out: only token-set/spacing.
    Why + conclusion: gap reporting is a CLI action (gap-add), not an artifact; proceed.

25. `./run-authority golden`
    Out: 56/56 agreement; key rows: "a switch"→px-sw, "a status badge"→badge, "a settings page"→settings, "a nav item"→nav-item; "a carousel"→UNDEFINED (expected); "rounded corners…"→CONFLICT prohibit/off-radius.
    Why + conclusion: canonical wordings exist for my pieces — re-resolve with them for clean records; radius must stay 0 (prohibition).

26. `./run-authority resolve "a switch" --json`
    Out: RESOLVED → `component/px-sw` (evidence 14.0).
    Why + conclusion: the control IS recorded; adopting px-sw is legitimate authority, not improvisation.

27. `./run-authority resolve "a status badge" --json`
    Out: RESOLVED → `component/badge`.
    Why + conclusion: the state display's *basis* is recorded; only the composition (badge as a live setting-state indicator) is improvised and stays marked.

28. `./run-authority resolve "a sidebar layout" --json`
    Out: RESOLVED → `component/shell`.
    Why + conclusion: chrome is recorded; adopt `.app/.side/.main` (+ `.topbar` for tablet/phone).

29. `./run-authority inspect guideline/accessibility`
    Out: WCAG 2.2 scorecard — focus visible / not obscured, non-text contrast, target size, contrast, animation, forced colours, resize, reflow all pass; "4.1.3 Status Messages - pass"; focus ring global, never removed.
    Why + conclusion: keep focus styles untouched (no custom CSS) and ship a status message for the toggle change (4.1.3).

30. `./run-authority inspect guideline/voice`
    Out: rules — sentence case; "Enable/Disable for entity state — never Pause/Resume or On/Off"; "announce mutations in past tense, naming the object"; name the object in aria-labels.
    Why + conclusion: state text must be Enabled/Disabled (not On/Off); live announcement "Release notes enabled/disabled"; aria-label "Enable/Disable Release notes" flips with state — all built so.

31. `./run-authority validate index.html`
    Out: validator triage-lint: ok; findings 0 — errors=0 warnings=0 info=0; spec score=100.
    Why + conclusion: the single-file build (recorded classes only, assets-only styling) passes clean on the first run; artifact complete.

32. `./run-authority gap-add --help`
    Out: usage — `--need NEED [--context CONTEXT] [--scope SCOPE] [--workspace WORKSPACE]`.
    Why + conclusion: need is required; context is a separate argument (discovered next to be JSON).

33. `./run-authority gap-add --need "Compact display of a setting's current enabled/disabled state, placed with its switch control" --context "…plain text…" --scope settings`
    Out: rc=1 — traceback: `json.decoder.JSONDecodeError` in cmd_gap_add (`context = json.loads(args.context)`).
    Why + conclusion: `--context` must be a JSON object; retry with JSON.

34. `./run-authority gaps`
    Out: still "no gaps recorded" — the failed call left no partial record.
    Why + conclusion: safe to retry; verified nothing was half-written.

35. `./run-authority gap-add --need "Compact display of a setting current enabled/disabled state, placed with its switch control" --context '{"surface": "settings section for a preferences screen (pattern/settings + component/px-sw)", "attempted_resolution": "resolve of a compact display of the current state of a preference -> UNDEFINED; resolve of a status chip showing a setting is on or off -> UNDEFINED; closest recorded pieces: component/badge, component/chip, component/dot", "outcome": "marked improvisation composed from component/badge beside the px-sw switch; Enabled/Disabled vocabulary per guideline/voice (never On/Off)", "note": "no recorded setting-row variant pairs a boolean switch with a current-state display"}' --scope settings`
    Out: created `gap/20261008-131653-da8ec0` (status open; stored at `.design-authority/gaps.jsonl`).
    Why + conclusion: the improvisation is now formally reported per the fallback policy — never presented as canonical.

36. `./run-authority gaps`
    Out: `gap/20261008-131653-da8ec0  [open]  Compact display of a setting current enabled/disabled state…`
    Why + conclusion: gap record verified in the workspace; reporting chain complete.

37. `./run-authority inspect component/topbar`
    Out: stable; "tablet and phone chrome header (menu, title, theme and density toggles, status); hidden on desktop where the sidebar carries the brand".
    Why + conclusion: late contract check — the built topbar (menu button + title) matches; theme/density toggles are out of the brief's scope, not added.

---

## Build summary

- `index.html`: shell (`.app/.side/.nav/.topbar`), `pattern/settings` skeleton (`.settings-grid/.settings-nav/.setting-row`), Release notes row = `component/px-sw` switch + improvised state display composed from `component/badge` (marked in-file), `role="status"` live region (`.vh`) announcing "Release notes enabled/disabled" per `guideline/voice`; JS additive per `fallback/no-js` (native checkbox works without it).
- Improvisation kept visible: HTML comment in `index.html`, entry 35's gap record, and this log.
- Verification: `./run-authority validate index.html` → triage-lint ok, 0 errors, 0 warnings, spec score 100 (index.html unchanged since that run).
