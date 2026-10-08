# S-A2 build log — Brief S: Settings section

Every authority call ran from this workspace through `./run-authority` (machine trace: `audit.jsonl`, 39 invocations, execution order below).
Adopted records: `component/px-sw` · `pattern/settings` · `component/shell` · `component/nav-item` · `component/topbar` · `component/badge` · `component/dot` · `component/page-head` · `component/btn` · `component/iconbtn` · `component/toast2` · `guideline/interaction-standard`
Deliverables: `index.html` (validated) · `log.md`. Gaps filed: `gap/20261008-131750-380ecf`, `gap/20261008-131750-a8d536`.

---

1. `./run-authority overview`
   Output: `triage — 0.12.1 (format 0.1)`; artifacts `component=56, guideline=10, pattern=7, token-set=7`; `rules=19 fallbacks=3 prohibitions=6`; resolution `CONFLICT -> RESOLVED -> COMPOSE -> FALLBACK -> UNDEFINED`.
   Why + conclusion: map the authority before touching anything. The resolution chain sets my build policy — resolve first, compose from nearest records + gap report only on UNDEFINED.

2. `./run-authority --help`
   Output: subcommands `overview | search | discover | inspect | resolve | validate | golden | gaps | gap-add | propose | review | precedents …`; `discover`/`--assist` are the optional semantic extensions.
   Why + conclusion: learn the exact CLI surface for this lexical-only cell. Plan: search → resolve → inspect every adoption → validate → gap-add.

3. `./run-authority search "switch toggle boolean control"`
   Output (top): `8.0 component/px-sw Switch`; `8.0 component/seg Segmented control`.
   Why + conclusion: find the recorded boolean control for the brief's on/off preference. `px-sw` is the switch; `seg` is the alternative to disambiguate via resolve.

4. `./run-authority search "settings section preference row"`
   Output (top): `9.5 pattern/settings Settings` (then acc, audit-row, index-row, kv…).
   Why + conclusion: the brief is a settings section; pattern/settings is the page-level answer to inspect and adopt.

5. `./run-authority search "sidebar navigation app shell chrome"`
   Output (top): `23.5 component/shell App shell`; `8.0 component/nav-item`; `7.0 component/topbar`; `4.0 component/bottom-nav`.
   Why + conclusion: the brief wants the page in the app's usual chrome. Shell + nav-item + topbar are the recorded chrome pieces.

6. `./run-authority search "status indicator badge state"`
   Output (top): `14.5 component/badge Badge`; `8.0 component/dot Status dot`.
   Why + conclusion: candidates for the brief's compact state display. badge and dot are the nearest recorded pieces; inspect both.

7. `./run-authority search "toggle"`
   Output (top): `9.0 component/px-sw Switch`.
   Why + conclusion: cross-check the brief's word against the catalogue. "toggle" is a recorded alias of px-sw, so resolving with that vocabulary should land.

8. `./run-authority inspect component/px-sw`
   Output: states `checked, unchecked, disabled, focus-visible`; a11y: "visible label wraps a real checkbox; hidden twin carries the off value", "aria-label carries the verb: Enable/Disable <object>", "coarse pointers get a 44px hit area".
   Why + conclusion: never adopt a record uninspected. Contract is clear: label-wrapped checkbox + `.px-tr` track, verb aria-label, hidden twin — adopt px-sw as the control.

9. `./run-authority inspect pattern/settings`
   Output: "Task sections with a sticky side nav, scoped setting-row forms and per-card save bars" (sticky side nav + `.settings-grid`/`.setting-row` in patterns.css).
   Why + conclusion: adopt the settings harness — settings-grid / settings-nav / settings-body / setting-row — as the section skeleton.

10. `./run-authority inspect component/shell`
    Output: "The page skeleton: sidebar, main column and content frame (.app / .side / .main), with the shell contract on /components/navigation".
    Why + conclusion: the shell is the recorded chrome; adopt `.app > .side / .main / .content` as the page frame.

11. `./run-authority inspect component/badge`
    Output: states `neutral, ok, warn, err, acc, solid`; a11y: "Uppercase micro-label; never the only signal — pair with text that says the same thing."
    Why + conclusion: candidate for the compact state readout. Its own text carries the state, satisfying the pairing rule — keep for the state display.

12. `./run-authority inspect component/dot`
    Output: "7px square status dot; neutral by default, with ok / warn / err variants paired with text (never colour alone)."
    Why + conclusion: alternative for state display (dot + text). dot fits status lines (side-foot/topbar); badge fits a compact labelled readout — use dot for sync status, keep badge as main candidate.

13. `./run-authority inspect component/nav-item`
    Output: states `default, hover, active(selected), focus-visible`; a11y: `aria-current="page"` on the active item; active rail is border-inline-start.
    Why + conclusion: adopt for sidebar entries; mark Settings with `active` + `aria-current="page"`.

14. `./run-authority inspect component/topbar`
    Output: "tablet and phone chrome header (menu, title, theme and density toggles, status); hidden on desktop where the sidebar carries the brand."
    Why + conclusion: adopt the topbar for the shell's ≤1023px chrome (menu button + title + status).

15. `./run-authority search "saved state confirmation feedback"`
    Output: no direct feedback component; nearest `candidate/behavioural-verification`, `empty`, `page-state`, `stat`.
    Why + conclusion: check how "change applied" feedback is recorded before improvising one. Nothing direct — feedback must come from the interaction-standard channels (checked next).

16. `./run-authority search "page header title description"`
    Output (top): `23.5 component/page-head Page header`.
    Why + conclusion: page title row for the content frame; page-head is the recorded furniture.

17. `./run-authority resolve --help`
    Output: `resolve PROBLEM [PROBLEM ...] [--context CTX] [--json] [--assist {off,semantic}]`.
    Why + conclusion: `--json` gives structured outcomes for the log; `--assist` is blocked in this cell.

18. `./run-authority inspect component/page-head`
    Output: "The title row at the top of a page: title, description and actions."
    Why + conclusion: adopt as `h1.page-title` + `.page-desc` wrapper for "Settings".

19. `./run-authority inspect guideline/interaction-standard`
    Output (binding for every screen): armed two-step deletes; confirm() only for one-way actions; show-the-reverse for reversible mutations; three-channel feedback (banner / toast / empty state); save bars for editors; copy rules.
    Why + conclusion: a preference flip is a reversible mutation → show-the-reverse (Undo) + toast feedback are mandated, not extra. This shapes the page's JS.

20. `./run-authority resolve "build a settings section for a preferences screen" --json`
    Output: `RESOLVED → pattern/settings` (score 18.5; alternatives: acc 4.0, accessibility 4.0).
    Why + conclusion: primary UI need resolved to the settings pattern — adopt it as the section structure.

21. `./run-authority resolve "control to flip one preference on or off right away" --json`
    Output: `UNDEFINED`; closest px-sw 4.0 vs 6.5 threshold.
    Why + conclusion: phrasing missed the lexical surface. Retry with the record's own vocabulary instead of falling back.

22. `./run-authority resolve "toggle a boolean preference on and off with a switch" --json`
    Output: `RESOLVED → component/px-sw` (score 17.0; matched: toggle, switch, "off").
    Why + conclusion: with authority vocabulary the control resolves cleanly — px-sw adopted.

23. `./run-authority precedents`
    Output: 1 negative precedent — do NOT keep the pre-0.1.0 (mail-triage era) class/id vocabulary; "one public vocabulary keeps the contract checkable".
    Why + conclusion: use only current recorded class names in the build (no legacy aliases).

24. `./run-authority resolve "show the current state of a preference compactly next to its control" --json`
    Output: `UNDEFINED`; closest pager-num 4.5; no scoped fallback applies; policy: compose from nearest records, mark improvisation, report a gap.
    Why + conclusion: the brief's "compact display of current state" is NOT canonically recorded. Fallback path activated: nearest recorded piece = `.badge` inside `.setting-control`, marked noncanonical, gap to be filed.

25. `./run-authority resolve "page sits in app chrome with sidebar navigation" --json`
    Output: `RESOLVED → component/shell` (score 13.5; alternatives nav-item 9.5, topbar 7.0).
    Why + conclusion: chrome need resolved to the shell; adopt shell + nav-item + topbar together.

26. `./run-authority search "status chip current value label on off"`
    Output (top): `8.0 component/badge`; `7.0 component/px-sw`; `5.5 chip`; `5.5 kv`.
    Why + conclusion: double-check there is a better "current value" piece. badge remains the top recorded piece for the state readout composition.

27. `./run-authority gaps`
    Output: `no gaps recorded in …/s-a2`.
    Why + conclusion: check the gap register before filing so I don't duplicate — register empty, my two gaps will be new.

28. `./run-authority resolve "show a short confirmation after changing a setting" --json`
    Output: `UNDEFINED`; closest pattern/settings 4.0.
    Why + conclusion: no single artifact covers change-confirmation. Compose from the binding interaction standard's toast channel + recorded `.toast2`, and file a gap.

29. `./run-authority inspect component/toast2`
    Output: states `ok, warn, err, auto-dismiss`; a11y: "#toasts is aria-live=polite; one toast at a time."
    Why + conclusion: the confirmation channel. Build the container as `#toasts` with `aria-live="polite"`, one toast at a time, auto-dismiss — exactly the recorded contract.

30. `./run-authority inspect component/btn`
    Output: states incl. hover/active/focus-visible/disabled/busy(guardApply); a11y: "Use a real <button> or <a>; never a clickable div"; icon-only needs aria-label.
    Why + conclusion: the Undo affordance is a real `<button>` — `.btn.small` adopted; no clickable divs anywhere.

31. `./run-authority inspect component/iconbtn`
    Output: a11y: "aria-label is mandatory (the glyph is aria-hidden)"; min 44px on coarse pointers.
    Why + conclusion: the topbar menu button uses `.iconbtn` with `aria-label="Open navigation"` + `aria-hidden` glyph — contract satisfied.

32. `./run-authority gap-add --help`
    Output: `gap-add --need NEED [--context CONTEXT] [--scope SCOPE] [--workspace WORKSPACE]`.
    Why + conclusion: learn exact gap syntax before filing.

33. `./run-authority validate index.html`
    Output: `validator triage-lint: ok` — `findings: 0  errors=0 warnings=0 info=0  spec score=100`.
    Why + conclusion: verify the finished build against the authority's own validators — clean on the first run, nothing to fix.

34. `./run-authority gap-add --need "Compact display of a preference's current…" --context "<prose>"`
    Output: crash — `json.decoder.JSONDecodeError: Expecting value`; `--context` must be JSON.
    Why + conclusion: syntax lesson — context is parsed with `json.loads`. Retry with a JSON object (no file written by the failure).

35. `./run-authority gap-add --need "Confirmation + show-the-reverse…" --context "<prose>"`
    Output: same JSONDecodeError crash.
    Why + conclusion: same fix — re-run both with JSON context strings.

36. `./run-authority gaps`
    Output: still `no gaps recorded…` (the two crashed calls wrote nothing).
    Why + conclusion: confirms the failures were non-destructive; safe to re-file.

37. `./run-authority gap-add --need "Compact display of a preference current state, placed with its control (settings screen)" --context '{"brief":"S - settings section","attempted":"resolve: … => UNDEFINED","fallback":"nearest recorded piece .badge (ok / neutral) placed in .setting-control; improvisation marked noncanonical in index.html"}' --scope "settings"`
    Output: `gap/20261008-131750-380ecf` [open].
    Why + conclusion: first UNDEFINED need recorded with attempted resolve + fallback used.

38. `./run-authority gap-add --need "Confirmation + show-the-reverse affordance for an immediate-apply preference change" --context '{"brief":"S - settings section","attempted":"resolve: … => UNDEFINED","fallback":"interaction standard toast channel; .toast2 (ok, auto-dismiss, one at a time); .btn.small Undo per show-the-reverse"}' --scope "settings"`
    Output: `gap/20261008-131750-a8d536` [open].
    Why + conclusion: second UNDEFINED need recorded.

39. `./run-authority gaps`
    Output: both gaps listed `[open]` — `gap/20261008-131750-380ecf`, `gap/20261008-131750-a8d536`.
    Why + conclusion: read-back verification — the gap register is the durable trace of the improvisations.

---

## Build summary (decisions at a glance)

- **Frame**: `.app` shell (`.side` sidebar w/ brand, nav-items incl. active Settings + `aria-current="page"`, side-foot; `.main` + `.topbar` tablet chrome + `.content`). Recorded: shell / nav-item / topbar.
- **Section**: pattern/settings — `settings-grid` → sticky `settings-nav` (one "Updates" item, `.on`, `aria-current="true"`) + `settings-body` section `#updates` with one `setting-row`.
- **Control**: `.px-sw` inside `form.px-swf` — label wraps the real checkbox; hidden twin (`value="off"`) always submits a state; verb aria-label (`Disable…`/`Enable Release notes`) swaps with state; default On.
- **State readout** (noncanonical, gap 380ecf): `.badge ok` "On" ↔ `.badge` "Off" placed in `.setting-control`; marked with an HTML comment in `index.html`.
- **Immediate apply feedback** (from binding interaction standard; gap a8d536): `#toasts` (`aria-live="polite"`, one toast at a time, auto-dismiss) + `.toast2.ok` "…turned on/off." + `.btn.small` Undo (show-the-reverse); undo restores the switch, re-renders the badge and confirms.
- **Styling**: only the three workspace sheets linked (tokens → base → patterns); zero `<style>` blocks, zero inline styles, no external requests; all classes are current recorded names (per precedent).
- **Icons**: inline Lucide glyphs (the recorded icon set) — `inbox`, `mail`, `settings-2`, `menu` — sized by `.icon .icon-16`; decorative (`aria-hidden`).
- **QA**: html well-formed (no unclosed tags); browser smoke test on `file://` passed — 3 sheets load, Geist loads, `--acc` token applies, track 36px, toggle flips badge On→Off→On, toast + Undo work, drawer opens (scrim + `aria-expanded=true`) and Escape closes it. `validate`: 0 errors, 0 warnings, spec score 100.
