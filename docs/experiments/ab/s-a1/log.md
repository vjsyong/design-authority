# Authority log — brief S (settings section), cell s-a1 (lexical retrieval)

Every command below ran from this workspace through the audited runner `./run-authority`
(each call is machine-recorded in `audit.jsonl`, 41 records, in this exact order).
`discover` and `resolve --assist` are blocked in this cell (lexical retrieval only).

---

1. `./run-authority overview`
   Key output: `triage — 0.12.1 (format 0.1) · snapshot triage-design-system @ ec490bb7f3 · artifacts: component=56, guideline=10, pattern=7, token-set=7 · rules=19 recipes=0 fallbacks=3 prohibitions=6 · resolution: CONFLICT -> RESOLVED -> COMPOSE -> FALLBACK -> UNDEFINED`
   Why + conclusion: Orientation before any build decision. The catalogue is component-heavy; the resolution ladder (CONFLICT → RESOLVED → COMPOSE → FALLBACK → UNDEFINED) is the contract to follow, fallback only when resolve fails.

2. `./run-authority --help`
   Key output: `usage: da {overview,search,discover,inspect,resolve,validate,golden,gaps,gap-add,propose,review,precedents,precedent-check,candidates}`
   Why + conclusion: Learn the command surface first. Noted that `discover`/`--assist` are optional retrieval extensions — not usable here (lexical cell).

3. `./run-authority search --help`
   Key output: `flags: --kinds --limit --json`
   Why + conclusion: Flag syntax check before real searches; search takes a query plus optional kind filter.

4. `./run-authority inspect --help`
   Key output: `positional: id`
   Why + conclusion: Confirm inspect takes one artifact id.

5. `./run-authority resolve --help`
   Key output: `resolve [--context CONTEXT] [--json] [--assist {off,semantic}] problem [problem ...]`
   Why + conclusion: Confirm resolve shape; try later without `--context` first (it expects JSON).

6. `./run-authority validate --help`
   Key output: `validate [--snapshot SNAPSHOT] [--json] target`
   Why + conclusion: The validator takes a file target — `index.html` will be validated at the end.

7. `./run-authority gap-add --help`
   Key output: `gap-add --need NEED [--context CONTEXT] [--scope SCOPE] [--workspace WORKSPACE]`
   Why + conclusion: Only `--need` is required; context/scope optional.

8. `./run-authority search "switch toggle preference" --limit 12`
   Key output: `8.0 component/px-sw Switch · 4.0 component/seg · 4.0 pattern/settings · 1.5 component/savebar · 1.5 component/topbar`
   Why + conclusion: Find the boolean control for the "Release notes" preference. `component/px-sw` is the switch.

9. `./run-authority search "settings" --limit 12`
   Key output: `9.0 pattern/settings Settings · 1.5 token-set/motion`
   Why + conclusion: Locate the settings/frame pattern. One clean hit: `pattern/settings`.

10. `./run-authority search "sidebar navigation" --limit 12`
   Key output: `8.0 component/nav-item · 5.5 component/shell · 4.0 component/bottom-nav · 1.5 component/topbar`
   Why + conclusion: Chrome candidates for "sit in the app's usual chrome". nav-item + shell lead.

11. `./run-authority search "badge status state" --limit 12`
   Key output: `14.5 component/badge Badge · 5.5 component/msg · 4.0 component/dot Status dot · 4.0 component/empty`
   Why + conclusion: Candidates for the compact state display. badge and dot go on the shortlist.

12. `./run-authority search "nav rail" --limit 12`
   Key output: `5.0 component/nav-item · 4.0 component/bottom-nav · 4.0 pattern/learning · 1.5 pattern/settings`
   Why + conclusion: Alternative chrome vocabulary probe; nothing new beyond nav-item/bottom-nav.

13. `./run-authority search "header toolbar" --limit 10`
   Key output: `4.0 component/page-head Page header · 4.0 component/topbar · 1.5 component/tbl`
   Why + conclusion: Page-level header candidates; page-head and topbar shortlisted.

14. `./run-authority search "on off enabled disabled indicator" --limit 12`
   Key output: `5.5 component/px-sw · 4.0 component/dot · 4.0 component/progress · 2.0 component/dp`
   Why + conclusion: State-indicator vocabulary probe; px-sw + dot again — consistent with entries 8/11.

15. `./run-authority inspect component/px-sw`
   Key output: `Switch — base.css; states: checked, unchecked, disabled, focus-visible; a11y: visible label wraps a real checkbox; hidden twin carries the off value; aria-label carries the verb (Enable/Disable <object>); 44px coarse hit area`
   Why + conclusion: Inspect before adopting the control. Conclusion: adopt px-sw — checkbox inside the label, hidden twin for the off value, verb in aria-label.

16. `./run-authority inspect pattern/settings`
   Key output: `"Task sections with a sticky side nav, scoped setting-row forms and per-card save bars." (source site/pages_patterns.py)`
   Why + conclusion: Inspect before adopting the settings frame. Conclusion: setting-row forms are the pattern's core; with a single section the sticky settings-nav column adds nothing, so it is scoped out (noted in markup).

17. `./run-authority inspect component/badge`
   Key output: `states: neutral, ok, warn, err, acc, solid; a11y: uppercase micro-label; never the only signal — pair with text`
   Why + conclusion: Verify the state-display candidate before committing. Kept as alternative; decided against: a badge is a label, not a state readout.

18. `./run-authority inspect component/dot`
   Key output: `7px square status dot; neutral by default; ok/warn/err variants paired with text (never colour alone)`
   Why + conclusion: Second state-display candidate. Conclusion: viable readout piece — must be paired with text.

19. `./run-authority inspect component/shell`
   Key output: `page skeleton: sidebar, main column and content frame (.app / .side / .main); shell contract on /components/navigation`
   Why + conclusion: Inspect before adopting the chrome frame. Conclusion: adopt .app/.side/.main as the page skeleton.

20. `./run-authority inspect component/nav-item`
   Key output: `states: default/hover/active/focus-visible; a11y: aria-current="page" on the active item; active rail is border-inline-start`
   Why + conclusion: Inspect before adopting nav items. Conclusion: mark Settings active with class + aria-current="page".

21. `./run-authority search "ui conventions" --limit 10`
   Key output: (no hits)
   Why + conclusion: Hunt for a conventions guideline referenced in CSS comments. Conclusion: not recorded under that name; proceed with the records at hand.

22. `./run-authority search "shell contract" --limit 10`
   Key output: `5.5 component/shell · 4.0 candidate/provenance-contract · 1.5 component/proposal`
   Why + conclusion: Look for the shell contract document. Conclusion: no separate artifact retrievable; the shell record is the contract surface.

23. `./run-authority inspect component/topbar`
   Key output: `tablet/phone chrome header (menu, title, theme and density toggles, status); hidden on desktop where the sidebar carries the brand`
   Why + conclusion: Chrome completeness. Conclusion: adopt as small-screen chrome (title only; no JS behaviours).

24. `./run-authority golden`
   Key output: `agreement 56/56 (100%). e.g. "a switch" -> component/px-sw; "a settings page" -> pattern/settings; "a status badge" -> component/badge; "a carousel" -> UNDEFINED; "rounded corners on the cards" -> CONFLICT prohibit/off-radius`
   Why + conclusion: Calibrate expected outcomes/examples. Conclusion: my switch/settings resolutions match golden; UNDEFINED is a legitimate recorded outcome.

25. `./run-authority precedents`
   Key output: `1 negative precedent: renamed-vocabulary — keep pre-0.1.0 names? accepted: no; one public vocabulary, rename map exists for migration`
   Why + conclusion: Check policy declines before writing markup. Conclusion: use only current class vocabulary (no legacy names, no invented classes where recorded ones exist).

26. `./run-authority resolve "a switch to turn a preference on and off" --context "settings section of a preferences screen" --json`
   Key output: `rc=1 — JSONDecodeError: --context expects JSON`
   Why + conclusion: First resolve attempt for the control. Conclusion: `--context` takes a JSON object, not prose.

27. `./run-authority resolve "a switch to turn a preference on and off" --context '{"screen":"settings","preference":"Release notes"}' --json`
   Key output: `RESOLVED -> component/px-sw; evidence 13.0 (threshold 6.5); alternatives: component/bubble 4.0, pattern/settings 4.0, component/check 1.5`
   Why + conclusion: Formal resolution for the on/off control. Conclusion: component/px-sw is the authority's answer for the Release notes control.

28. `./run-authority resolve "a compact display of the preference's current on or off state placed with the control" --json`
   Key output: `UNDEFINED; closest: component/px-sw 5.5, component/empty 4.0, component/page-state 4.0; fallback policy returned (no-js, scoped-embedding, motion-reduction)`
   Why + conclusion: Formal resolution for the state display. Conclusion: no direct match at this phrasing — re-phrase and retest; keep the fallback policy in hand.

29. `./run-authority resolve "a compact display of the preference's current on or off state placed with the control" --json`
   Key output: `UNDEFINED (same result as #28, full raw output captured)`
   Why + conclusion: Re-run to capture the full untruncated outcome after a local parse slip. Conclusion: UNDEFINED confirmed for this phrasing.

30. `./run-authority resolve "app chrome with a sidebar navigation" "a settings section for a preferences screen" --json`
   Key output: `RESOLVED -> pattern/settings; alternatives: component/shell 9.5, component/nav-item 8.0, component/topbar 7.0 (note: multiple problem args are treated as one joined query)`
   Why + conclusion: Resolve the settings section and the chrome together. Conclusion: pattern/settings holds; chrome pieces are the adjacent alternatives.

31. `./run-authority resolve "app chrome with a sidebar navigation" --json`
   Key output: `UNDEFINED; closest: component/shell 9.5 (navigation, sidebar, app), component/nav-item 8.0, component/topbar 7.0`
   Why + conclusion: Resolve the chrome as a single need. Conclusion: no direct one-artifact match — re-phrase toward the recorded shell vocabulary.

32. `./run-authority resolve "a small badge showing whether the setting is on or off" --json`
   Key output: `UNDEFINED; closest: component/badge 4.0, component/btn 4.0, component/px-sw 4.0`
   Why + conclusion: Test the badge as the state display. Conclusion: undershoots the threshold — try dot phrasing.

33. `./run-authority resolve "a status dot showing whether the setting is on" --json`
   Key output: `RESOLVED -> component/dot; evidence 18.0; alternatives: component/badge 4.0, component/msg 4.0, pattern/settings 4.0`
   Why + conclusion: State display, re-phrased. Conclusion: component/dot is the recorded state indicator — adopt it, paired with text per its a11y note.

34. `./run-authority resolve "a sidebar" --json`
   Key output: `UNDEFINED; closest: component/nav-item 4.0, component/shell 4.0`
   Why + conclusion: Minimal chrome phrasing probe. Conclusion: "a sidebar" alone is not a unit — try the shell phrasing.

35. `./run-authority resolve "an app shell with a sidebar layout" --json`
   Key output: `RESOLVED -> component/shell; evidence 36.0; alternatives: component/topbar 5.5, component/nav-item 4.0, token-set/spacing 4.0`
   Why + conclusion: Chrome, re-phrased. Conclusion: the authority covers the sidebar chrome (shell + nav-item + topbar are recorded); no chrome gap needed.

36. `./run-authority inspect fallback/no-js`
   Key output: `"Every component degrades to its plain markup; the behaviour layer is additive… never require JS for content; prefer native elements (dialog, details, input)"`
   Why + conclusion: The toggle must flip "right away"; check the no-JS policy. Conclusion: build with the native checkbox switch and no scripting; plain markup only.

37. `./run-authority inspect component/page-head`
   Key output: `"The title row at the top of a page: title, description and actions."`
   Why + conclusion: Verify before adopting the page header. Conclusion: adopt .page-head + .page-title + .page-desc for the Settings title row.

38. `./run-authority validate index.html --json`
   Key output: `triage-lint: error=0, warning=0, info=0; spec_score=100 (files_scanned 1, spec_version 0.12.1)`
   Why + conclusion: The spec gate on the built page. Conclusion: first pass clean — 0 errors, 0 warnings, score 100; no fixes needed.

39. `./run-authority gap-add --need "A compact readout of a boolean preference's current state, placed with its control (state shown inline with the switch)." --context "Settings section, 'Release notes' preference row on a preferences screen. Resolve returned UNDEFINED for this need; implemented per fallback by composing nearest recorded pieces: component/dot + text, inside the setting-row control column (.setting-control)." --scope "settings"`
   Key output: `rc=1 — JSONDecodeError: --context expects JSON` (prose context rejected)
   Why + conclusion: File the gap for the one genuinely unrecorded composition (state readout with control). Conclusion: pass structured JSON context.

40. `./run-authority gap-add --need "A compact readout of a boolean preference's current state, placed with its control (state shown inline with the switch)." --context '{"screen":"settings section","preference":"Release notes","resolve_outcome":"UNDEFINED","nearest_pieces":["component/dot","component/px-sw"],"composed_with":".setting-control"}'`
   Key output: `gap/20261008-131927-3a5c1d recorded; status open; stored at .design-authority/gaps.jsonl`
   Why + conclusion: Report the fallback improvisation (also marked in the page markup). Conclusion: gap filed — the readout composition is composed from nearest recorded pieces, never presented as canonical.

41. `./run-authority validate index.html --json`
   Key output: `triage-lint: error=0, warning=0, info=0; spec_score=100 — RC=0`
   Why + conclusion: Closing gate re-run on the frozen file (nothing changed since entry 38). Conclusion: the final artifact validates clean — 0 errors, 0 warnings, score 100.

---

Result: `validate index.html` → 0 errors / 0 warnings / spec score 100 (entry 38 first pass; entry 41 as the closing gate on the unchanged final file).
Gap on record: `gap/20261008-131927-3a5c1d`. Adopted records (all inspected before adoption): component/px-sw,
component/dot, component/shell, component/nav-item, component/topbar, component/page-head, pattern/settings,
fallback/no-js.
