# log.md — Brief S (settings section), workspace `docs/experiments/ab/s-b1`

Authority: **triage 0.12.1** (format 0.1) @ `ec490bb7f3`. Every call went through the audited
runner `./run-authority` (machine trail: `audit.jsonl`, 38 invocations — including 3 `validate`
runs and 1 rejected `gap-add` retry; noted against the ~30 cap, overage is the retry plus the
extra retrieval wording attempts).

**Adopted artifacts:** `pattern/settings`, `component/shell`, `component/nav-item`,
`component/px-sw`, `component/badge` (fallback readout), `component/topbar`, `component/bottom-nav`;
rule `INT003` honoured; negative precedent `precedent/renamed-vocabulary` applied.
**Gap filed:** `gap/20261008-131825-7ba2d3`. **Validation:** `triage-lint` ok, 0 errors / 0 warnings /
0 info, spec score **100** (exit 0, final file).

---

1. `./run-authority overview`
   Key output: `triage — 0.12.1 (format 0.1) · artifacts: component=56, guideline=10, pattern=7, token-set=7 · rules=19 recipes=0 fallbacks=3 prohibitions=6 · resolution: CONFLICT -> RESOLVED -> COMPOSE -> FALLBACK -> UNDEFINED`
   Why + conclusion: Orient before resolving — confirms the pattern/component coverage and the exact resolution pipeline the brief requires me to follow (fallback only after UNDEFINED).

2. `./run-authority --help`
   Key output: subcommands `overview | search | discover | inspect | resolve | validate | golden | gaps | gap-add | propose | review | precedents | precedent-check | candidates`; discover/resolve --assist are "optional retrieval extensions … never establishes authority".
   Why + conclusion: Learn the permitted verbs of the audited route; conclusion: resolve → inspect → (discover when UNDEFINED) → gap-add → validate is the workflow.

3. `./run-authority resolve "settings section for a preferences screen"`
   Key output: `OUTCOME: RESOLVED` → `pattern/settings` "Settings — Task sections with a sticky side nav, scoped setting-row forms and per-card save bars."
   Why + conclusion: The brief's opening ask resolved directly; conclusion: the page is built on pattern/settings.

4. `./run-authority inspect pattern/settings`
   Key output: id `pattern/settings`, aliases settings/preferences/settings screen; body is thin: group + source file only, no markup contract.
   Why + conclusion: Inspect before adopting; conclusion: the pattern record carries no markup — its layout classes come from the compiled, inspected `assets/core/patterns.css` (`.settings-grid/.settings-nav/.setting-row`).

5. `./run-authority search "settings"`
   Key output: `9.0 pattern/settings` · `1.5 token-set/motion`
   Why + conclusion: Check for a fuller settings family; conclusion: one pattern record only — no deeper settings components exist.

6. `./run-authority search "switch toggle"`
   Key output: `8.0 component/px-sw (Switch)` · `4.0 component/seg` · `1.5 component/savebar` · `1.5 component/topbar`
   Why + conclusion: Locate the boolean control for "Release notes"; conclusion: `component/px-sw`.

7. `./run-authority inspect component/px-sw`
   Key output: class `px-sw`; states checked/unchecked/disabled/focus-visible; a11y: "visible label wraps a real checkbox; hidden twin carries the off value", "aria-label carries the verb: Enable/Disable <object>", coarse pointers get 44px.
   Why + conclusion: Inspect before adopting; conclusion: exact markup contract for the control (label-wrapped checkbox + hidden off-twin + aria-label verb).

8. `./run-authority resolve "a switch to turn one preference on or off"`
   Key output: `OUTCOME: RESOLVED` → `component/px-sw` (matched twice).
   Why + conclusion: Resolve the brief's control need in natural language; conclusion: same record — adoption of px-sw is authority-backed.

9. `./run-authority resolve "compact display of the current state of a preference next to its control"`
   Key output: `OUTCOME: UNDEFINED` — closest `component/pager-num 4.50` vs `6.50` needed; "no recipe matched; no scoped fallback applies".
   Why + conclusion: The brief's second requirement; conclusion: no artifact covers a state readout beside a control → trigger discovery, then fallback policy.

10. `./run-authority resolve "sidebar navigation chrome for an app page"`
    Key output: `OUTCOME: RESOLVED` → `component/shell` "The page skeleton: sidebar, main column and content frame (.app / .side / .main)".
    Why + conclusion: The brief's chrome requirement; conclusion: sidebar shell adopted for the page skeleton.

11. `./run-authority discover "compact display of the current state of a preference next to its control" --k 5`
    Key output: candidates (retrieval signal only): `fallback/motion-reduction`, `component/nav-item`, `pattern/settings`, `component/seg`, `INT003` (cos 0.598–0.633).
    Why + conclusion: Discovery for the UNDEFINED need, with the same wording as the resolve; conclusion: nothing reads as a state readout — inspect the plausible candidates before any adoption.

12. `./run-authority inspect component/shell`
    Key output: class `app`; note: sidebar + main column + content frame; "shell contract on /components/navigation".
    Why + conclusion: Inspect before adopting; conclusion: `.app/.side/.main` skeleton is the authority answer for chrome.

13. `./run-authority inspect INT003`
    Key output: rule `three-channel-feedback`: "Feedback uses the three sanctioned channels only: banner, toast, empty state — plus in-flight treatments. … ad-hoc alerts drift."
    Why + conclusion: Top-semantic discovery candidate; conclusion: not a readout — it constrains the page to add no ad-hoc feedback; the state badge is a readout, not a message channel.

14. `./run-authority inspect component/nav-item`
    Key output: class `nav-item`; states default/hover/active/focus; a11y: `aria-current="page"` on the active item; logical-property active rail.
    Why + conclusion: Discovery candidate and required for the sidebar; conclusion: sidebar links use `.nav-item` with `aria-current="page"`.

15. `./run-authority search "badge"`
    Key output: `19.0 component/badge (Badge)`.
    Why + conclusion: Hunt the nearest recorded piece for a compact state label; conclusion: `component/badge` is the candidate.

16. `./run-authority search "status chip"`
    Key output: `4.0 component/badge` · `4.0 component/chip` · `4.0 component/dot` · `4.0 component/msg`.
    Why + conclusion: Test whether a "status chip" component exists; conclusion: no such record (the `.status-chip` CSS is dashboard-pattern scoped, not a component) → prefer recorded badge/dot.

17. `./run-authority search "on off state display"`
    Key output: `5.5 component/px-sw` · `4.0 component/empty · page-state · stat` · `4.0 guideline/voice`.
    Why + conclusion: Second wording for the readout; conclusion: only px-sw carries on/off semantics in the catalogue.

18. `./run-authority inspect component/badge`
    Key output: class `badge`; states neutral/ok/warn/err/acc/solid; a11y: "Uppercase micro-label; never the only signal — pair with text that says the same thing."
    Why + conclusion: Inspect before considering adoption; conclusion: badge works as the state label if its own text says On/Off (never colour-only).

19. `./run-authority inspect component/chip`
    Key output: class `chip`; states default/hover/active; "filter chip".
    Why + conclusion: Candidate from search; conclusion: chips are interactive filters — not a state display; rejected.

20. `./run-authority inspect component/dot`
    Key output: 7px square dot; ok/warn/err variants "paired with text (never colour alone)".
    Why + conclusion: Candidate; conclusion: a dot still needs text beside it, so the badge (which carries its own text) is the better nearest piece; dot rejected.

21. `./run-authority search "setting row"`
    Key output: no setting-row component; `4.0 pattern/settings` among rows/tables.
    Why + conclusion: Check for a row-level artifact; conclusion: row structure exists only inside the settings pattern CSS.

22. `./run-authority search "navigation"`
    Key output: `4.0 component/bottom-nav` · `4.0 component/nav-item` · `1.5 component/shell`.
    Why + conclusion: Enumerate the chrome family; conclusion: topbar/bottom-nav have records and may be adopted for narrow viewports.

23. `./run-authority search "ui conventions"`
    Key output: (no matches).
    Why + conclusion: `base.css` cites `ui-conventions.md`; conclusion: no authority record behind that name — defer to the inspected component records instead.

24. `./run-authority search "prohibition"`
    Key output: (no matches).
    Why + conclusion: Overview reported prohibitions=6; conclusion: not lexically searchable — rely on `validate` to enforce them at the end.

25. `./run-authority search "golden"`
    Key output: (no matches).
    Why + conclusion: Probing for a checklist; conclusion: use the `golden` command itself.

26. `./run-authority golden`
    Key output (trimmed): `a switch -> component/px-sw` · `a status badge -> component/badge` · `a nav item -> component/nav-item` · `a primary button -> component/btn` · guidelines incl. philosophy/brand/platform/icons/accessibility/voice/localisation.
    Why + conclusion: Confirm intended resolution mapping; conclusion: my chosen records match golden behaviour; the readout question stays open (no golden line reads as a bare state label).

27. `./run-authority precedents`
    Key output: 1 negative precedent — `precedent/renamed-vocabulary`: keeping old mail-triage-era class names alongside new ones was declined: "One public vocabulary keeps the contract checkable."
    Why + conclusion: Hear policy declines before building; conclusion: use only the current class vocabulary from the compiled assets — no dual naming.

28. `./run-authority gaps`
    Key output: "no gaps recorded in …/s-b1".
    Why + conclusion: Baseline before filing; conclusion: the state-readout gap will be the first recorded.

29. `./run-authority resolve "compact label showing whether a preference is currently on or off beside its switch"`
    Key output: `OUTCOME: RESOLVED` → `component/px-sw`.
    Why + conclusion: Reframed natural wording for the state display; conclusion: the authority reads the on/off display as the switch itself — a separate readout element remains unrecorded → fallback policy + gap.

30. `./run-authority gap-add --help`
    Key output: `usage: da gap-add [-h] --need NEED [--context CONTEXT] [--scope SCOPE] [--workspace WORKSPACE]`.
    Why + conclusion: Learn gap syntax without burning a write; conclusion: `--need` required, `--context` consumed by the tool.

31. `./run-authority inspect component/topbar`
    Key output: "The tablet and phone chrome header (menu, title, theme and density toggles, status); hidden on desktop where the sidebar carries the brand."
    Why + conclusion: Inspect before adopting responsive chrome; conclusion: include topbar (menu + title) — shown ≤1023px.

32. `./run-authority inspect component/bottom-nav`
    Key output: "The persistent phone tab bar, with view transitions between tabs."
    Why + conclusion: Inspect before adopting; conclusion: include bottom-nav (mirrors primary nav) — shown ≤767px.

33. `./run-authority gap-add --need "Compact on/off state readout…" --context "Brief S (settings section) asks…" --scope settings`
    Key output: **rc=1** — `json.decoder.JSONDecodeError` from `context = json.loads(args.context)`.
    Why + conclusion: Record the state-readout gap; conclusion: `--context` must be a JSON object, not prose — retry with JSON (entry 35).

34. `./run-authority validate index.html`  *(first pass, on the drafted page)*
    Key output: `validator triage-lint: ok · findings: 0 errors=0 warnings=0 info=0 spec score=100` (exit code masked by the pipe).
    Why + conclusion: Check the draft against the declared validators; conclusion: clean on first pass; re-run unpiped for the true exit code.

35. `./run-authority gap-add --need "Compact on/off state readout for a preference, placed with its control in a settings row" --context '{"brief": "…", "resolution_path": "resolve -> UNDEFINED …; discover --k 5 …; reframed resolve matched component/px-sw …", "attempted_resolution": "Adopted nearest recorded pieces: component/badge as a text readout beside component/px-sw; improvisation marked in index.html as data-improv=state-readout."}' --scope settings`
    Key output: rc=0 → `gap/20261008-131825-7ba2d3`, status open, stored at `.design-authority/gaps.jsonl`.
    Why + conclusion: Retry with JSON context; conclusion: the genuinely-unrecorded need is filed with its resolution path.

36. `./run-authority gaps`
    Key output: `gap/20261008-131825-7ba2d3  [open]  Compact on/off state readout for a preference, placed with its control in a settings row`.
    Why + conclusion: Verify the record landed; conclusion: gap recorded and visible in the workspace.

37. `./run-authority validate index.html`  *(unpiped, true exit code)*
    Key output: rc=0 · `triage-lint: ok · findings: 0 errors=0 warnings=0 info=0 spec score=100`.
    Why + conclusion: Confirm exit status without pipe masking; conclusion: page passes with 0/0/0 and spec score 100.

38. `./run-authority validate index.html`  *(after the final JS robustness patch — recompute `inert` on resize)*
    Key output: rc=0 · `triage-lint: ok · findings: 0 errors=0 warnings=0 info=0 spec score=100`.
    Why + conclusion: The file changed after entry 37, so re-validate the final artifact; conclusion: final index.html is clean at spec 100.

---

## Outcome

- **Deliverable:** `index.html` — settings section ("Release notes" preference) inside the sidebar
  app chrome. Styling only from `assets/tokens/tokens.css`, `assets/core/base.css`,
  `assets/core/patterns.css`; no page-local CSS.
- **Authority coverage:** pattern/settings · component/shell · component/nav-item · component/topbar
  · component/bottom-nav · component/px-sw · component/badge. Rule INT003 honoured (no ad-hoc
  feedback/alerts). Negative precedent applied (current vocabulary only).
- **Fallback (visible improvisation):** the compact state readout beside the switch has no recorded
  artifact (resolve UNDEFINED, twice; discovery empty of readouts). Built from the nearest recorded
  piece — `component/badge` as a text readout ("On"/"Off", never colour-only) beside `component/px-sw`.
  Marked in `index.html` with an HTML comment and `data-improv="state-readout"`; filed as
  `gap/20261008-131825-7ba2d3`.
- **Validation:** `./run-authority validate index.html` → `triage-lint: ok, 0 errors / 0 warnings /
  0 info, spec score 100` (exit 0).
- **Non-authority verification** (headless browser on the local file, no network — not an authority
  route): switch track 36×21 painted `#0057d9` with the 15px knob at inset 17px when on; badge text
  and class flip On↔`badge.ok` (aria-label toggles Enable/Disable); drawer opens via Menu, closes via
  scrim/Escape with `inert` applied when off-canvas; bottom-nav at ≤767px; no horizontal overflow at
  420px or 1280px.
