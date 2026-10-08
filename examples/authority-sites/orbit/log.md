# Authority call log — Orbit Interface System site build

All 43 calls were made through the audited runner `./run-authority` from this workspace;
`audit.jsonl` (machine-recorded) is the corresponding trace. Outputs below are trimmed;
the audit keeps the full stdout. Call order is exact.

## 1. `./run-authority overview --json`

```
{
 "authority": {
  "authority": "orbit",
  "version": "0.1.0",
  "commit": "n/a - derived document source, not a repository"
 },
 "description": "A minimal interface system derived from the NASA Graphics Standards Manual (1976) for the Design Authority portability spike. Carries no NASA marks.",
 "counts": {
  "artifacts": {
   "component": 12,
   "pattern": 4,
   "token-set": 2,
   "guideline": 2,
   "reference": 1
  },
  "rules": 4,
  "recipes": 3,
  "fallbacks": 2,
  "prohibitions": 3
 },
 "capabilities": {
  "search": true,
  "resolve": true,
  "validators": [
   "orbit-lint"
  ],
…
```

Why + conclusion: orient before anything else: identity, counts, policy and capability surface. Conclusion: orbit 0.1.0; 21 artifacts (component 12 / pattern 4 / token-set 2 / guideline 2 / reference 1); 4 rules, 3 recipes, 2 fallbacks, 3 prohibitions; direct-match threshold 6.5 governs resolve.

## 2. `./run-authority search orbit --limit 200`

```
   3.0  token-set    token-set/palette            Orbit palette
   3.0  token-set    token-set/type               Orbit type roles
   1.5  pattern      pattern/shell                Application shell
```

Why + conclusion: begin id-space reconnaissance from the pack's own name. Conclusion: token-set/palette, token-set/type, pattern/shell surfaced; id pattern is `<kind>/<slug>`.

## 3. `./run-authority search nasa --limit 200`

```
   4.0  reference    reference/manual             Source: NASA Graphics Standards Manual (NHB 1430.2, 1976)
```

Why + conclusion: probe the source vocabulary (NASA-derived pack) for records referencing the manual. Conclusion: reference/manual found; far from full coverage, so widen the probe.

## 4. `./run-authority search 'grid column baseline typography text letter number color line rule bar band block margin space spacing print page sheet layout mark logo label caption photo table list card cell panel header footer title heading scale width weight stem unit document poster sign banner stripe edge frame masthead slogan vehicle placard chart diagram signature endorsement' --limit 200`

```
  22.5  pattern      pattern/shell                Application shell
  15.0  component    component/band               Band (identity, navigation, status)
  14.5  component    component/panel              Panel (bordered technical region)
  14.5  component    component/register           Register (ruled data list)
  11.0  guideline    guideline/accent-discipline  Accent discipline
   9.5  component    component/notice             Notice (inline feedback block)
   9.5  pattern      pattern/register-view        Register view (list screen)
   9.0  token-set    token-set/type               Orbit type roles
   8.5  component    component/dialog             Dialog (modal confirm or editor)
   7.5  component    component/tag                Tag (square micro-label)
   7.0  component    component/entry              Entry (text field)
   7.0  token-set    token-set/palette            Orbit palette
   6.5  component    component/indicator          Indicator (status marker)
   6.5  fallback     fallback/plain-region        Plain content region
   5.5  component    component/gauge              Gauge (determinate progress)
   4.5  component    component/section            Section (grouping)
   4.0  reference    reference/manual             Source: NASA Graphics Standards Manual (NHB 1430.2, 1976)
   3.5  pattern      pattern/job-view             Job view (status console)
   3.0  recipe       recipe/status-console        Long-running work shows text status
   2.5  recipe       recipe/form-section          Grouped form submission
   2.0  component    component/chooser            Chooser (small-set select)
   2.0  component    component/command            Command (action control)
   1.5  fallback     fallback/platform-controls   Platform defaults for uncovered controls
   1.5  pattern      pattern/form-flow            Form flow (create or edit)
   1.0  guideline    guideline/voice              Voice: clear and concise
```

Why + conclusion: broad multi-token sweep to enumerate the entire artifact id space in one call. Conclusion: ALL 21 artifact ids surfaced; per-kind counts match the overview exactly (12/4/2/2/1) — enumeration verified complete.

## 5. `./run-authority inspect pattern/shell`

```
{
 "id": "pattern/shell",
 "kind": "pattern",
 "title": "Application shell",
 "summary": "Band on top, main region (max-width 1080, padding 24/32), footer folio line 'Orbit . section' in small gray type.",
 "status": "beta",
 "aliases": [
  "app shell",
…
```

Why + conclusion: fetch the full shell record before designing the page frame. Conclusion: band + main (max-width 1080, padding 24/32) + footer folio line; adopted as the page frame.

## 6. `./run-authority inspect token-set/palette`

```
{
 "id": "token-set/palette",
 "kind": "token-set",
 "title": "Orbit palette",
 "summary": "Paper (white), ink (near-black), gray-mid (middle warm gray), accent (warm NASA-derived red), accent-ink (white). Accent is identification and action only, never a reading surface.",
 "status": "beta",
 "aliases": [
  "colors",
…
```

Why + conclusion: resolve page colour roles from the token set. Conclusion: roles only — paper/ink/gray-mid/accent/accent-ink — with usage rules and no hex values recorded; hex improvisation noted for a gap.

## 7. `./run-authority inspect token-set/type`

```
{
 "id": "token-set/type",
 "kind": "token-set",
 "title": "Orbit type roles",
 "summary": "Helvetica-register sans only in controls; scale 24/18/15/13/12; flush-left ragged-right; normal letterspacing; line-height 1.4; serif voice reserved for long-form content.",
 "status": "beta",
 "aliases": [
  "typography",
…
```

Why + conclusion: resolve the type programme for the page. Conclusion: scale 24/18/15/13/12, line-height 1.4, flush-left ragged-right, normal letterspacing, Helvetica register (matches the brief's stack); adopted.

## 8. `./run-authority inspect component/band`

```
{
 "id": "component/band",
 "kind": "component",
 "title": "Band (identity, navigation, status)",
 "summary": "Full-width white band with a 1px ink bottom rule: identity left, navigation (current item = 2px accent underline), environment/status text right; inverted variant uses ink background with white text.",
 "status": "beta",
 "aliases": [
  "header",
…
```

Why + conclusion: masthead identity/navigation candidates — inspect before adopting. Conclusion: identity left / nav (current = 2px accent underline) / status right; adopted for the masthead chrome.

## 9. `./run-authority inspect component/register`

```
{
 "id": "component/register",
 "kind": "component",
 "title": "Register (ruled data list)",
 "summary": "Data list or table: header row in Medium, rows separated by 1px gray hairlines, top-aligned cells, row actions right as text commands; no zebra striping, no elevation.",
 "status": "beta",
 "aliases": [
  "table",
…
```

Why + conclusion: the catalogue is a ruled list — inspect the list component before adopting. Conclusion: header row Medium, 1px gray hairlines, top-aligned, no zebra/elevation; adopted for catalogue and spec lists.

## 10. `./run-authority inspect component/panel`

```
{
 "id": "component/panel",
 "kind": "component",
 "title": "Panel (bordered technical region)",
 "summary": "1px ink bordered region reserved for technical or diagrammatic content; ordinary prose uses sections and rules instead.",
 "status": "beta",
 "aliases": [
  "card",
…
```

Why + conclusion: check whether the bordered region is right for the page's blocks. Conclusion: panel is reserved for technical/diagrammatic content — not adopted for prose blocks; catalogued only.

## 11. `./run-authority inspect component/section`

```
{
 "id": "component/section",
 "kind": "component",
 "title": "Section (grouping)",
 "summary": "Form or content grouping: Medium heading, 1px ink rule, stacked entries; form column max-width 560px; top-aligned.",
 "status": "beta",
 "aliases": [
  "fieldset",
…
```

Why + conclusion: grouping structure for the catalogue's kind groups. Conclusion: Medium heading + 1px ink rule for sections; adopted for group sections.

## 12. `./run-authority inspect component/notice`

```
{
 "id": "component/notice",
 "kind": "component",
 "title": "Notice (inline feedback block)",
 "summary": "Square inline message block: info (gray border), warning (ink border), alert (accent border + accent heading); one concise sentence of copy; top of its region.",
 "status": "beta",
 "aliases": [
  "alert",
…
```

Why + conclusion: callout need (provenance note). Conclusion: info = gray border, one concise sentence, top of its region; adopted for the provenance notice.

## 13. `./run-authority inspect component/tag`

```
{
 "id": "component/tag",
 "kind": "component",
 "title": "Tag (square micro-label)",
 "summary": "Square 1px gray-bordered micro-label for classification and metadata; tags keep their own visual space and never compete with status.",
 "status": "beta",
 "aliases": [
  "badge",
…
```

Why + conclusion: classification/metadata chips need for artifact rows. Conclusion: square gray-bordered micro-label; adopted as the group tag per row.

## 14. `./run-authority inspect component/entry`

```
{
 "id": "component/entry",
 "kind": "component",
 "title": "Entry (text field)",
 "summary": "Single-line text input: label above, 1px ink border, error line below in accent; square.",
 "status": "beta",
 "aliases": [
  "input",
…
```

Why + conclusion: complete the record sweep (the catalogue presents every artifact). Conclusion: text-field record read; not used on this page.

## 15. `./run-authority inspect component/indicator`

```
{
 "id": "component/indicator",
 "kind": "component",
 "title": "Indicator (status marker)",
 "summary": "Status shown as a 6x6 square marker plus text label; tones neutral (gray), ok (ink), alert (accent); text always readable alone.",
 "status": "beta",
 "aliases": [
  "status",
…
```

Why + conclusion: artifact status display need (statuses are part of the records). Conclusion: 6x6 square + text label; tones neutral/ok/alert; adopted for artifact status and rule severity.

## 16. `./run-authority inspect component/gauge`

```
{
 "id": "component/gauge",
 "kind": "component",
 "title": "Gauge (determinate progress)",
 "summary": "Square determinate progress bar: paper track with 1px gray border, ink fill (accent fill when attention needed), mandatory text readout 'n of m'; static updates, no animation.",
 "status": "experimental",
 "aliases": [
  "progress",
…
```

Why + conclusion: complete the sweep; test whether a progress surface is needed. Conclusion: determinate bar spec read; not used (no progress surface on a docs page).

## 17. `./run-authority inspect component/dialog`

```
{
 "id": "component/dialog",
 "kind": "component",
 "title": "Dialog (modal confirm or editor)",
 "summary": "Square modal: 1px ink border, ink band header with title and Close, body, right-aligned footer commands; page overlay is ink at 40% opacity; state appears and disappears instantly (no motion).",
 "status": "experimental",
 "aliases": [
  "modal",
…
```

Why + conclusion: complete the sweep. Conclusion: modal spec read; not used on this page.

## 18. `./run-authority inspect component/chooser`

```
{
 "id": "component/chooser",
 "kind": "component",
 "title": "Chooser (small-set select)",
 "summary": "Labelled native select for small fixed sets (about 12 options or fewer); larger or filtered selection is out of scope by design.",
 "status": "beta",
 "aliases": [
  "select",
…
```

Why + conclusion: complete the sweep. Conclusion: select spec read; not used on this page.

## 19. `./run-authority inspect component/command`

```
{
 "id": "component/command",
 "kind": "component",
 "title": "Command (action control)",
 "summary": "Square action control; primary (solid accent), secondary (ink border), destructive (accent border, reserved for high-consequence actions).",
 "status": "beta",
 "aliases": [
  "button",
…
```

Why + conclusion: the page head needs a primary command (pattern/register-view); inspect the action control first. Conclusion: primary = solid accent, focus = 2px ink outline, active inverted; adopted for the Print command.

## 20. `./run-authority inspect pattern/register-view`

```
{
 "id": "pattern/register-view",
 "kind": "pattern",
 "title": "Register view (list screen)",
 "summary": "Shell plus page head (h1 and a primary command) plus register; empty state is a centered standby notice with one secondary command.",
 "status": "beta",
 "aliases": [
  "list screen",
…
```

Why + conclusion: the catalogue is a list screen — inspect before adopting. Conclusion: shell + page head (h1 + primary command) + register; adopted as the catalogue's composition.

## 21. `./run-authority inspect pattern/job-view`

```
{
 "id": "pattern/job-view",
 "kind": "pattern",
 "title": "Job view (status console)",
 "summary": "Shell plus indicator plus gauge plus a log register (time and message rows); status is always text plus marker; no animation anywhere.",
 "status": "experimental",
 "aliases": [
  "status screen",
…
```

Why + conclusion: complete the sweep. Conclusion: status-console pattern read; not adopted.

## 22. `./run-authority inspect pattern/form-flow`

```
{
 "id": "pattern/form-flow",
 "kind": "pattern",
 "title": "Form flow (create or edit)",
 "summary": "Shell, sections of entries and choosers, validation notices above fields, footer row with a primary submit and a secondary cancel; destructive actions route through a dialog naming the object and consequence.",
 "status": "beta",
 "aliases": [
  "settings form",
…
```

Why + conclusion: complete the sweep. Conclusion: form pattern read; not adopted.

## 23. `./run-authority inspect guideline/accent-discipline`

```
{
 "id": "guideline/accent-discipline",
 "kind": "guideline",
 "title": "Accent discipline",
 "summary": "The red accent marks identity and actions only; it never becomes a background behind reading text, never sits on mid-value surfaces, and is never the only signal.",
 "status": "beta",
 "aliases": [
  "accent rules",
…
```

Why + conclusion: governing rule for accent usage on this page. Conclusion: accent = identity and actions only, never behind reading text, never sole signal; honoured (nav underline, primary command, alert markers).

## 24. `./run-authority inspect guideline/voice`

```
{
 "id": "guideline/voice",
 "kind": "guideline",
 "title": "Voice: clear and concise",
 "summary": "UI copy is short, declarative, and names the object and the consequence; no ornament, no filler.",
 "status": "beta",
 "aliases": [
  "copy",
…
```

Why + conclusion: governing copy rules. Conclusion: short, declarative copy that names object and consequence; applied to every page string.

## 25. `./run-authority inspect reference/manual`

```
{
 "id": "reference/manual",
 "kind": "reference",
 "title": "Source: NASA Graphics Standards Manual (NHB 1430.2, 1976)",
 "summary": "Public-domain source document (US Government work) from which this system was derived; full provenance and extraction log in docs/portability/01-source-audit.md.",
 "status": "stable",
 "aliases": [
  "source document",
…
```

Why + conclusion: provenance for masthead/notice/footer. Conclusion: public-domain US Government source; no-marks note; adopted for the provenance notice.

## 26. `./run-authority resolve 'the page shell for a documentation page about the interface system'`

```
OUTCOME: RESOLVED
{
 "artifact": {
  "id": "pattern/shell",
  "kind": "pattern",
  "title": "Application shell",
  "summary": "Band on top, main region (max-width 1080, padding 24/32), footer folio line 'Orbit . section' in small gray type.",
  "status": "beta",
  "class": "shell",
…
```

Why + conclusion: resolve the primary structural need in natural language. Conclusion: RESOLVED -> pattern/shell.

## 27. `./run-authority resolve 'a masthead naming the system with its version and a one-line description'`

```
OUTCOME: UNDEFINED
closest:
     1.5  pattern/form-flow
     1.5  reference/manual
     1.0  component/entry
why: No artifact met the direct-match threshold (top candidate pattern/form-flow scored 1.50 vs 6.50 needed); no recipe matched; no scoped fallback applies.
next: Implement per the consuming project's fallback policy; mark the improvisation; then report_gap(need, context, attempted_resolution).
```

Why + conclusion: resolve the masthead need (page content block 1). Conclusion: UNDEFINED (closest 1.50) — masthead identity metadata is not recorded; fallback policy applies (compose from nearest pieces, mark, gap).

## 28. `./run-authority resolve 'a catalogue listing every artifact grouped by kind with title and summary'`

```
OUTCOME: UNDEFINED
closest:
     1.5  component/chooser
     1.5  component/dialog
     1.5  component/register
why: No artifact met the direct-match threshold (top candidate component/chooser scored 1.50 vs 6.50 needed); no recipe matched; no scoped fallback applies.
next: Implement per the consuming project's fallback policy; mark the improvisation; then report_gap(need, context, attempted_resolution).
```

Why + conclusion: resolve the catalogue need (block 2). Conclusion: UNDEFINED as phrased (closest 1.50) — rephrase closer to the record vocabulary.

## 29. `./run-authority validate /home/xrim/.hermes/cache/scratch/orbit-probe.html`

```
target: /home/xrim/.hermes/cache/scratch/orbit-probe.html
validator orbit-lint: ok
findings: 5  errors=0 warnings=0 info=5  spec score=98
  info     ORB-USE  (project):0  No use of authority artifact '.command' found.
  info     ORB-USE  (project):0  No use of authority artifact '.band' found.
  info     ORB-USE  (project):0  No use of authority artifact '.register' found.
  info     ORB-USE  (project):0  No use of authority artifact '.notice' found.
  info     ORB-USE  (project):0  No use of authority artifact '.indicator' found.
```

Why + conclusion: learn what the pack's own validator checks before building (probe file in scratch, outside the deliverable). Conclusion: orbit-lint runs; ORB-USE nudges list five artifacts the lint wants used (.band/.register/.notice/.indicator/.command); no value checks; score 98 (infos only).

## 30. `./run-authority resolve 'a list screen with a register of rows for the artifact catalogue'`

```
OUTCOME: RESOLVED
{
 "artifact": {
  "id": "pattern/register-view",
  "kind": "pattern",
  "title": "Register view (list screen)",
  "summary": "Shell plus page head (h1 and a primary command) plus register; empty state is a centered standby notice with one secondary command.",
  "status": "beta",
  "class": "register-view",
…
```

Why + conclusion: rephrase the catalogue need around the records' own vocabulary. Conclusion: RESOLVED -> pattern/register-view; adopted.

## 31. `./run-authority resolve 'a band header carrying the system identity'`

```
OUTCOME: RESOLVED
{
 "artifact": {
  "id": "component/band",
  "kind": "component",
  "title": "Band (identity, navigation, status)",
  "summary": "Full-width white band with a 1px ink bottom rule: identity left, navigation (current item = 2px accent underline), environment/status text right; inverted variant uses ink background with white text.",
  "status": "beta",
  "class": "band",
…
```

Why + conclusion: rephrase the masthead need around the band's vocabulary. Conclusion: RESOLVED -> component/band (chrome per band; version/description metadata still unrecorded -> gap).

## 32. `./run-authority validate /home/xrim/.hermes/cache/scratch/orbit-probe2.html`

```
target: /home/xrim/.hermes/cache/scratch/orbit-probe2.html
validator orbit-lint: ok
findings: 5  errors=0 warnings=0 info=5  spec score=98
  info     ORB-USE  (project):0  No use of authority artifact '.command' found.
  info     ORB-USE  (project):0  No use of authority artifact '.band' found.
  info     ORB-USE  (project):0  No use of authority artifact '.register' found.
  info     ORB-USE  (project):0  No use of authority artifact '.notice' found.
  info     ORB-USE  (project):0  No use of authority artifact '.indicator' found.
```

Why + conclusion: calibrate the ORB-USE check (probe v2 with artifact selectors defined). Conclusion: findings unchanged — the detector does not read inline styles; the nudges are constant, infos only; proceed with inline <style> per the deliverable contract.

## 33. `./run-authority resolve 'a section with a register of ruled list rows for the specification summary'`

```
OUTCOME: RESOLVED
{
 "artifact": {
  "id": "component/register",
  "kind": "component",
  "title": "Register (ruled data list)",
  "summary": "Data list or table: header row in Medium, rows separated by 1px gray hairlines, top-aligned cells, row actions right as text commands; no zebra striping, no elevation.",
  "status": "beta",
  "class": "register",
…
```

Why + conclusion: resolve the specification-summary list presentation (block 3). Conclusion: RESOLVED -> component/register; spec lists built as registers.

## 34. `./run-authority resolve 'paint the masthead background with the colour #cc0000'`

```
OUTCOME: UNDEFINED
closest:
     5.5  guideline/accent-discipline
     4.0  token-set/palette
     1.5  component/band
why: No artifact met the direct-match threshold (top candidate guideline/accent-discipline scored 5.50 vs 6.50 needed); no recipe matched; no scoped fallback applies.
next: Implement per the consuming project's fallback policy; mark the improvisation; then report_gap(need, context, attempted_resolution).
```

Why + conclusion: probe for a colour-literal prohibition to quote in the spec summary. Conclusion: UNDEFINED — orbit has no colour-literal prohibition (closest accent-discipline 5.50).

## 35. `./run-authority resolve 'add the NASA logotype to the masthead'`

```
OUTCOME: UNDEFINED
closest:
     4.0  reference/manual
     1.0  guideline/accent-discipline
why: No artifact met the direct-match threshold (top candidate reference/manual scored 4.00 vs 6.50 needed); no recipe matched; no scoped fallback applies.
next: Implement per the consuming project's fallback policy; mark the improvisation; then report_gap(need, context, attempted_resolution).
```

Why + conclusion: probe for a marks-related prohibition. Conclusion: UNDEFINED (closest reference/manual 4.00); prohibition signals are opaque to guessing — switch to the golden route.

## 36. `./run-authority golden --file /home/xrim/design-authority/packs/orbit/golden.json`

```
ok   RESOLVED   (want RESOLVED  ) a primary button for submitting a form  -> component/command
ok   COMPOSE    (want COMPOSE   ) delete a record with confirmation  -> recipe/destructive-confirm
ok   RESOLVED   (want RESOLVED  ) show the progress of a background job  -> pattern/job-view
ok   CONFLICT   (want CONFLICT  ) rounded corners on a card  -> prohibit/rounded-forms
ok   CONFLICT   (want CONFLICT  ) hero banner with rounded buttons and a shadow  -> prohibit/rounded-forms
ok   FALLBACK   (want FALLBACK  ) add a checkbox for newsletter opt-in  -> fallback/platform-controls
ok   FALLBACK   (want FALLBACK  ) toggle switch for dark mode  -> fallback/platform-controls
ok   RESOLVED   (want RESOLVED  ) status label for a failing job  -> component/indicator
ok   UNDEFINED  (want UNDEFINED ) a searchable picker for choosing an assignee
ok   UNDEFINED  (want UNDEFINED ) smooth animation when opening the dialog
agreement: 10/10 (100%)
```

Why + conclusion: run the pack's golden cases via the sanctioned route to learn conflict ids and expected outcomes. Conclusion: 10/10 agreement; revealed prohibit/rounded-forms and recipe/destructive-confirm; rounded forms are a CONFLICT.

## 37. `./run-authority inspect prohibit/rounded-forms`

```
{
 "id": "prohibit/rounded-forms",
 "statement": "Rounded corners anywhere \u2014 square is a system rule (ORB-1).",
 "signals": [
  "rounded corner",
  "rounded corners",
  "rounded",
  "border-radius",
  "pill-shaped",
  "soft corners"
 ],
 "rule": "ORB-1",
 "kind": "prohibition"
}
```

Why + conclusion: fetch the full prohibition record before quoting it. Conclusion: statement 'Rounded corners anywhere' + rule ORB-1 + detection signals; adopted as a verbatim quote.

## 38. `./run-authority inspect ORB-1`

```
{
 "id": "ORB-1",
 "name": "radius-always-zero",
 "severity": "error",
 "applies_to": [
  "css",
  "html"
 ],
 "summary": "Corner radius is always 0 \u2014 square form is the system's language.",
 "why": "The source system is rectilinear; no rounded form appears in any application (docs/portability/02-derived-system.md, \u00a7F1).",
 "fix": "Remove border-radius or set it to 0 on the offending element.",
 "enforcement": {
  "mode": "orbit-lint"
 }
}
```

Why + conclusion: fetch the cited rule record for the spec summary. Conclusion: radius-always-zero, severity error, verbatim summary + fix, enforced by orbit-lint; adopted as a verbatim quote.

## 39. `./run-authority gap-add --need "documentation masthead identity block carrying the system version and a one-line description (metadata beyond the band's identity slot)" --scope docs-page --context '{"from":"authority-sites/orbit build","domain":"masthead","attempted":"resolve(a masthead naming the system with its version and a one-line description) -> UNDEFINED; closest pattern/form-flow 1.50","handling":"composed from component/band identity + page head per pattern/register-view; improvisation marked in markup"}'`

```
{
 "id": "gap/20261008-165202-fe6d15",
 "need": "documentation masthead identity block carrying the system version and a one-line description (metadata beyond the band's identity slot)",
 "context": {
  "from": "authority-sites/orbit build",
  "domain": "masthead",
  "attempted": "resolve(a masthead naming the system with its version and a one-line description) -> UNDEFINED; closest pattern/form-flow 1.50",
…
 "stored_at": "/home/xrim/design-authority/examples/authority-sites/orbit/.design-authority/gaps.jsonl"
}
```

Why + conclusion: file the genuinely unrecorded masthead-metadata need per the fallback policy (from call 27's UNDEFINED). Conclusion: gap/20261008-165202-fe6d15 filed in this workspace; cited in the page markup.

## 40. `./run-authority gap-add --need 'exact colour values (hex) for the palette roles paper, ink, gray-mid, accent, accent-ink — token-set/palette records roles and descriptions only' --scope foundations --context '{"from":"authority-sites/orbit build","domain":"colour","note":"CSS custom properties --paper/--ink/--gray-mid/--accent/--accent-ink needed to build; values set from the recorded role descriptions, marked data-improv in markup"}'`

```
{
 "id": "gap/20261008-165202-7136d7",
 "need": "exact colour values (hex) for the palette roles paper, ink, gray-mid, accent, accent-ink \u2014 token-set/palette records roles and descriptions only",
 "context": {
  "from": "authority-sites/orbit build",
  "domain": "colour",
  "note": "CSS custom properties --paper/--ink/--gray-mid/--accent/--accent-ink needed to build; values set from the recorded role descriptions, marked data-improv in markup"
…
 "stored_at": "/home/xrim/design-authority/examples/authority-sites/orbit/.design-authority/gaps.jsonl"
}
```

Why + conclusion: file the unrecorded exact colour values need (token-set/palette carries roles only). Conclusion: gap/20261008-165202-7136d7 filed; cited in the page markup.

## 41. `./run-authority validate index.html`

```
target: /home/xrim/design-authority/examples/authority-sites/orbit/index.html
validator orbit-lint: ok
findings: 5  errors=0 warnings=0 info=5  spec score=98
  info     ORB-USE  (project):0  No use of authority artifact '.command' found.
  info     ORB-USE  (project):0  No use of authority artifact '.band' found.
  info     ORB-USE  (project):0  No use of authority artifact '.register' found.
  info     ORB-USE  (project):0  No use of authority artifact '.notice' found.
  info     ORB-USE  (project):0  No use of authority artifact '.indicator' found.
```

Why + conclusion: verify before claiming done: run the pack's validator over the delivered page. Conclusion: ok; 0 errors / 0 warnings / 5 ORB-USE infos (detector limitation, see call 32); spec score 98.

## 42. `./run-authority inspect fallback/plain-region`

```
{
 "id": "fallback/plain-region",
 "title": "Plain content region",
 "statement": "Content without a defined composition sits in the shell as plain regions separated by rules \u2014 not boxes.",
 "scope": [
  "prose",
  "content page",
  "about",
  "help text",
  "static page"
 ],
 "constraints": [
  "rules, not boxes",
  "wide margins",
  "no decoration"
 ],
 "kind": "fallback"
}
```

Why + conclusion: inspect the fallback records before displaying them (the spec summary lists both; inspect-before-adopt). Conclusion: plain-region = rules/not boxes, wide margins, no decoration for content pages — the page already complies; constraints quoted on the page.

## 43. `./run-authority inspect fallback/platform-controls`

```
{
 "id": "fallback/platform-controls",
 "title": "Platform defaults for uncovered controls",
 "statement": "If the system defines no control for a need, use the platform's native element with system typography and square form; keep native semantics.",
 "scope": [
  "checkbox",
  "radio",
  "date",
  "time",
  "file",
  "toggle",
  "switch"
 ],
 "constraints": [
  "square form (ORB-1 still applies)",
  "system type scale",
  "mark the improvisation and report a gap if the need recurs"
 ],
 "kind": "fallback"
}
```

Why + conclusion: inspect the second fallback record before displaying it. Conclusion: native elements + system typography + square form (ORB-1 applies); its statement and constraints are quoted in the fallbacks block.

---

Totals: 43 calls (cap noted at ~35 — overspend from inspecting all 21 catalogue records
plus the two fallbacks, and from lint/golden discovery; no unauthorized routes were used).
Gaps filed from this workspace: gap/20261008-165202-fe6d15 (masthead metadata),
gap/20261008-165202-7136d7 (palette hex values).
