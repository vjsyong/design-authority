# log.md — Leader Interface System site build (leader 0.2.0)

Every authority call made for this build, in order, through the audited runner `./run-authority` (the only route to the authority; its machine trace is `audit.jsonl`).
Format per call: exact syntax · trimmed output · one `Why + conclusion:` line. Outputs are trimmed from the audited stdout; nothing is paraphrased.

---

**[1]** `./run-authority overview`

```
leader — 0.2.0 (format 0.1)
snapshot: marber.economist.com + economist.com live product @ n/a - deri
artifacts: component=6, guideline=5, pattern=2, token-set=2
rules=2 recipes=0 fallbacks=3 prohibitions=5
resolution: CONFLICT -> RESOLVED -> COMPOSE -> FALLBACK -> UNDEFINED
```

Why + conclusion: Orientation first: the manifest fixes the catalogue scope — 15 artifacts in 4 kinds, 2 rules, 5 prohibitions, 3 fallbacks, 0 recipes; resolution order CONFLICT -> RESOLVED -> COMPOSE -> FALLBACK -> UNDEFINED.

---

**[2]** `./run-authority overview --json`

```
{
 "authority": {
  "authority": "leader",
  "version": "0.2.0",
  "commit": "n/a - derived from public sources, not a repository"
 },
 "description": "An editorial interface system derived from The Economist's Marber design system and live product for the Design Authority synthesis experiment. Serif-led, rules-based, blue interactive layer; no Economist marks reproduced.",
 "counts": {
  "artifacts": {
   "component": 6,
   "guideline": 5,
   "token-set": 2,
   "pattern": 2
  },
  "rules": 2,
  "recipes": 0,
  "fallbacks": 3,
  "prohibitions": 5
 },
 "capabilities": {
  "search": true,
  "resolve": true,
  "validators": [],
  "gap_reporting": true,
  "extension_proposals": true,
  "resolution_assist": "off"
 },
 "policy": {
  "on_undefined": "Implement per the consuming project's fallback policy, mark the improvisation, and report a gap. Never present improvisation as canonical.",
  "on_conflict": "Do not implement as requested; the request violates an explicit constraint (see the cited rule/prohibition).",
  "proposals": "Noncanonical. The authority is never modified by a consumer; proposals are reviewed upstream."
 },
 "resolution_semantics": [
  "CONFLICT: request contradicts an explicit constraint (prohibition/rule).",
  "RESOLVED: a direct artifact defines the solution.",
  "COMPOSE: a sanctioned recipe composes existing artifacts.",
  "FALLBACK: a sanctioned generic fallback applies.",
  "UNDEFINED: no adequate authority answer exists (structured, not an error)."
 ]
}
```

Why + conclusion: The masthead needs name, version and a one-line description, and the build needs the fallback policy text. Adopted: the description line and version 0.2.0; note validators:[] — this pack has no post-build validation route.

---

**[3]** `./run-authority search 'marber economist' --limit 50`

```
4.0  token-set    token-set/colour             Colour roles (red + Chicago blue)
```

Why + conclusion: Probe whether brand/source tokens enumerate the pack: only one hit, so a wider vocabulary sweep is required.

---

**[4]** `./run-authority search 'button link card list table header footer nav navigation masthead tag badge label quote blockquote story article tease teaser byline caption image figure dataviz chart grid layout hero banner rule divider section column panel form input search menu dropdown tabs accordion icon logo wordmark typography type font serif sans spacing scale palette color editorial interface system web print digital news page template screen home product motion animation accessibility focus states imagery photography illustration principles brand tone voice kicker standfirst pull deck subhead red blue black white chicago' --limit 60`

```
35.5  token-set    token-set/colour             Colour roles (red + Chicago blue)
  30.5  component    component/navbar             Top bar
  27.5  token-set    token-set/type-scale         Screen type scale
  25.5  guideline    guideline/hierarchy          Section rhythm
  23.0  guideline    guideline/typography         Typography (three registers)
  22.0  component    component/action             Action (navy rounded)
  18.0  precedent    precedent/declined-imagery-and-icons Photographic imagery & pictorial icon sets (policy)
  17.0  component    component/field              Field (rounded, sans text)
  12.5  guideline    guideline/motion             Motion
  12.5  pattern      pattern/data-charts          Data charts (rectilinear register)
  12.5  precedent    precedent/ledger-rejected    Ledger table pattern (proposal rejected at review)
  12.0  guideline    guideline/shape-language     Shape language (rounded product)
   9.5  component    component/tag                Tag (status / category)
   7.5  precedent    precedent/declined-motion-feedback Loading spinner, toast motion (motion policy)
   5.5  component    component/notice             Notice (ruled box)
   5.5  guideline    guideline/surfaces           Surfaces & separation
   5.5  pattern      pattern/data-readouts        Data readouts (sparkline trend, stat counter)
   3.5  fallback     fallback/ruled-panel         Interstitials become ruled panels
   3.0  component    component/meter              Progress meter
   3.0  precedent    precedent/destructive-confirm-rejected Destructive confirm pattern (proposal rejected at review)
   2.5  fallback     fallback/selection           Selection beyond small sets
   1.5  fallback     fallback/platform-controls   Platform defaults for uncovered controls
```

Why + conclusion: One wide sweep to enumerate the whole catalogue. Output reconciles exactly with the manifest — all 6 components, 5 guidelines, 2 patterns and both token sets, plus all 3 fallbacks — discovery complete (15/15 artifacts).

---

**[5]** `./run-authority inspect component/navbar`

```
{
 "id": "component/navbar",
 "kind": "component",
 "title": "Top bar",
 "summary": "Top bar: white, 2px ink bottom rule; name in serif left; sans links; active = blue underline (Chicago 45) per review; crisp search rectangle with typing-cursor motif right.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. Top bar adopted for the page masthead header: white, 2px ink bottom rule, serif name left, sans links, active = blue underline, crisp search rectangle with typing-cursor motif right.

---

**[6]** `./run-authority inspect component/action`

```
{
 "id": "component/action",
 "kind": "component",
 "title": "Action (navy rounded)",
 "summary": "Primary = solid navy-blue rounded rectangle (Chicago 45 #2E45B8, radius ~8px — live-observed CTA), white label; secondary = 2px ink outline; tertiary = underlined blue link (live-observed). Red steps back to brand/attention duty.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. Navy #2E45B8 at radius ~8 recovered for the interactive layer; 'red steps back to brand/attention duty' noted as a colour rule for the page.

---

**[7]** `./run-authority inspect component/field`

```
{
 "id": "component/field",
 "kind": "component",
 "title": "Field (rounded, sans text)",
 "summary": "Fields: white, 1px soft border, rounded corners (radius 8), sans-serif field text (reviewer-directed); label above in caps; focus adds no border highlight; error = small red line under the field.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. Field record committed to the catalogue (this static page has no forms, so its styling is presented, not instantiated).

---

**[8]** `./run-authority inspect component/tag`

```
{
 "id": "component/tag",
 "kind": "component",
 "title": "Tag (status / category)",
 "summary": "Tags: ink-outline caps rectangle (8px radius); attention flips it solid red; never a pill, never colour-alone.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. The tag spec — 2px ink-outline caps rectangle at 8px radius, uppercase sans 11 at 0.06em, strictly one line — drives the page's kind labels and severity stamps.

---

**[9]** `./run-authority inspect component/notice`

```
{
 "id": "component/notice",
 "kind": "component",
 "title": "Notice (ruled box)",
 "summary": "Notices = ruled boxes (2px ink top or left rule) with terse declarative copy; no toasts (none evidenced); problem copy names the fact and the next step.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. Ruled-box treatment (2px ink top or left rule, terse copy) adopted for the specification panels.

---

**[10]** `./run-authority inspect component/meter`

```
{
 "id": "component/meter",
 "kind": "component",
 "title": "Progress meter",
 "summary": "Progress = crisp rectangle track (London 85) with red fill; readout as sans metadata ('7 of 10 steps'); restart = outline rectangle. Static updates only.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. London 85 confirmed as the track/rule grey; the page shows no progress element — record presented only.

---

**[11]** `./run-authority inspect guideline/hierarchy`

```
{
 "id": "guideline/hierarchy",
 "kind": "guideline",
 "title": "Section rhythm",
 "summary": "Section label (sans caps, red) → serif headline → one-line standfirst (muted serif). Repeats strictly; no decorative sub-heads.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. The section rhythm — label (sans caps, red) -> serif headline -> one-line standfirst — structures every section of the page, repeated strictly.

---

**[12]** `./run-authority inspect guideline/typography`

```
{
 "id": "guideline/typography",
 "kind": "guideline",
 "title": "Typography (three registers)",
 "summary": "Three registers by role: Serif = headlines and body text; Sans = navigation, metadata, datelines, captions; Sans Headline = display-only moments (page mastheads, big statics), used sparingly.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. Three registers mapped to the copied fonts: Serif -> Gelasio, Sans -> Inter, Sans Headline -> Archivo Black (display only).

---

**[13]** `./run-authority inspect guideline/motion`

```
{
 "id": "guideline/motion",
 "kind": "guideline",
 "title": "Motion",
 "summary": "Interaction transitions are near-instant (≤0.15s colour swaps); no bounce, spring or decorative movement in UI chrome. Motion stays native to brand assets, not interface controls.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. Motion stays at near-instant colour swaps (<=0.15s); the page uses no bounce, spring or decorative movement.

---

**[14]** `./run-authority inspect guideline/shape-language`

```
{
 "id": "guideline/shape-language",
 "kind": "guideline",
 "title": "Shape language (rounded product)",
 "summary": "The live product uses soft rounded corners throughout: interactive components (buttons, toggles, inputs) and container surfaces (cards, panels) all carry radius ~8. Only rules, hairlines and editorial glyph marks stay crisp — no square buttons, no square cards.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. Radius ~8 for interactive components and container surfaces; only rules, hairlines and glyph marks stay crisp.

---

**[15]** `./run-authority inspect guideline/surfaces`

```
{
 "id": "guideline/surfaces",
 "kind": "guideline",
 "title": "Surfaces & separation",
 "summary": "White ground; separation via 2px ink rules and hairlines below (wash separation removed per review). Elevation, where needed, uses defined shadow tokens — not ambient glows.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. White ground; separation via 2px ink rules and hairlines — the page's separator logic.

---

**[16]** `./run-authority inspect pattern/data-charts`

```
{
 "id": "pattern/data-charts",
 "kind": "pattern",
 "title": "Data charts (rectilinear register)",
 "summary": "Charts are rectilinear and editorial: ink bars on hairline baselines (2px ink origin rule, grey/ink gridlines), a month grid of square cells, and a hairline sparkline. Red appears only as a single accent; no rings, no decorative chart styling.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. Rectilinear newspaper furniture noted — the character reference for the page's rules-and-columns catalogue treatment.

---

**[17]** `./run-authority inspect pattern/data-readouts`

```
{
 "id": "pattern/data-readouts",
 "kind": "pattern",
 "title": "Data readouts (sparkline trend, stat counter)",
 "summary": "Big statics: an Archivo (display) numeral with a sans-caps label beneath; reserved for year-to-date totals and headline counts.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. Display numerals are one-per-screen: the masthead keeps the page's single display moment, so no stat counters are added.

---

**[18]** `./run-authority inspect token-set/colour`

```
{
 "id": "token-set/colour",
 "kind": "token-set",
 "title": "Colour roles (red + Chicago blue)",
 "summary": "Red #E3120B = brand/editorial punctuation (labels, rules, single blocks). The Chicago blue family = the interactive layer (CTAs, active nav, links) — copious, per live review. Frame: ink, white, London grey ramp.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. Red #E3120B and the Chicago blue family confirmed; frame colours are recorded by name only — frame hexes will need a filed gap.

---

**[19]** `./run-authority inspect token-set/type-scale`

```
{
 "id": "token-set/type-scale",
 "kind": "token-set",
 "title": "Screen type scale",
 "summary": "Screen rhythm: serif headline 30–34/1.15; standfirst sans? no — serif standfirst 16–17 muted; body serif 17/1.55; metadata sans 12.5–13 with 0.06em caps for section labels; display 44 at tracking −1.",
 "status": "beta"
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect before adopting. Every size on the page comes from here: headline 30-34/1.15, standfirst 16-17, body 17/1.55, metadata 12.5-13 caps 0.06em, display 44 / -1.

---

**[20]** `./run-authority golden --file /home/xrim/design-authority/packs/leader/golden.json`

```
ok   RESOLVED   (want RESOLVED  ) add a primary button to the page  -> component/action
ok   RESOLVED   (want RESOLVED  ) the top navigation bar  -> component/navbar
ok   RESOLVED   (want RESOLVED  ) a form field for the borrower  -> component/field
ok   RESOLVED   (want RESOLVED  ) show import progress with steps  -> component/meter
ok   RESOLVED   (want RESOLVED  ) a notice message about overdue items  -> component/notice
ok   CONFLICT   (want CONFLICT  ) square corners on the primary button  -> prohibit/square-interactive
ok   CONFLICT   (want CONFLICT  ) make it a red background for reading  -> prohibit/red-reading-surface
ok   CONFLICT   (want CONFLICT  ) add an emoji to the headline  -> prohibit/decorative-noise
ok   FALLBACK   (want FALLBACK  ) a dialog for confirmation  -> fallback/ruled-panel
ok   UNDEFINED  (want UNDEFINED ) animate the hero with a bounce
ok   RESOLVED   (want RESOLVED  ) bar chart  -> pattern/data-charts
ok   RESOLVED   (want RESOLVED  ) sparkline  -> pattern/data-readouts
ok   RESOLVED   (want RESOLVED  ) streak counter  -> pattern/data-readouts
ok   RESOLVED   (want RESOLVED  ) status label  -> component/tag
agreement: 14/14 (100%)
```

Why + conclusion: Check the pack's own resolution fixtures before probing further. Three prohibition ids surfaced (square-interactive, red-reading-surface, decorative-noise) and fallback/ruled-panel confirmed for dialogs; agreement 14/14.

---

**[21]** `./run-authority resolve 'use photographic imagery and pictorial icons for the catalogue entries' --json`

```
outcome: UNDEFINED
why: No artifact met the direct-match threshold; no recipe matched; no scoped fallback applies.
normalized: {'catalogue': 'catalog'}
precedent [governs] precedent/declined-imagery-and-icons — L-21: no imagery; iconography is limited to rhythm glyph marks. The absence is honest, not a gap.
fallback policy: fallback/platform-controls, fallback/selection, fallback/ruled-panel
```

Why + conclusion: Probe governance of imagery and icons: UNDEFINED — the decline is policy carried by a governing precedent (L-21, imagery-policy), not a prohibition. Page conclusion: no imagery, no icons.

---

**[22]** `./run-authority resolve 'add a loading spinner and toast feedback to the page' --json`

```
outcome: UNDEFINED
why: No artifact met the direct-match threshold (top candidate guideline/hierarchy scored 4.00 vs 6.50 needed); no recipe matched; no scoped fallback applies.
closest: guideline/hierarchy (4.0), component/notice (2.5), guideline/typography (1.5)
precedent [governs] precedent/declined-motion-feedback — Transient persist is terminal feedback; the register answers it (static readout, L-16; notices, L-14). No spinner or toast canon — motion patterns stay deliberately UNDEFINED.
fallback policy: fallback/platform-controls, fallback/selection, fallback/ruled-panel
```

Why + conclusion: Probe governance of spinner/toast feedback: UNDEFINED — the motion precedent keeps transient feedback deliberately UNDEFINED; sanctioned route is a static readout or ruled notice.

---

**[23]** `./run-authority resolve 'paint the masthead background #004B87 to match the brand' --json`

```
outcome: UNDEFINED
why: No artifact met the direct-match threshold (top candidate guideline/surfaces scored 4.00 vs 6.50 needed); no recipe matched; no scoped fallback applies.
closest: guideline/surfaces (4.0), component/action (1.5), guideline/motion (1.5)
fallback policy: fallback/platform-controls, fallback/selection, fallback/ruled-panel
```

Why + conclusion: Probe whether a raw hex value triggers a colour-literal prohibition: UNDEFINED — no such prohibition exists in this pack.

---

**[24]** `./run-authority resolve 'reproduce the Economist wordmark and logo in the masthead' --json`

```
outcome: UNDEFINED
why: No artifact met the direct-match threshold (top candidate token-set/colour scored 4.00 vs 6.50 needed); no recipe matched; no scoped fallback applies.
closest: token-set/colour (4.0), guideline/typography (1.5)
fallback policy: fallback/platform-controls, fallback/selection, fallback/ruled-panel
```

Why + conclusion: Probe for a brand-marks prohibition: clean UNDEFINED — none recorded. The page reproduces no Economist marks regardless, per the pack description.

---

**[25]** `./run-authority resolve 'use fully rounded pill buttons with a drop shadow' --json`

```
outcome: UNDEFINED
why: No artifact met the direct-match threshold (top candidate component/action scored 7.00 vs 6.50 needed); no recipe matched; no scoped fallback applies.
closest: component/action (7.0), guideline/shape-language (5.5), component/field (3.0)
fallback policy: fallback/platform-controls, fallback/selection, fallback/ruled-panel
```

Why + conclusion: Probe for pill-rounding or shadow discouragement: UNDEFINED — none recorded; rounding discipline is rule L-R1's domain instead.

---

**[26]** `./run-authority resolve 'square corners on the primary button' --json`

```
outcome: CONFLICT
prohibition: prohibit/square-interactive — Square-cornered interactive components or cards — the live system is rounded (L-02, L-24).
rule: L-R1 (severity: error) — Interactive components and container surfaces are soft-rounded (radius ~8); only rules, hairlines and glyph marks stay crisp.
detected: signal 'square corners'
```

Why + conclusion: Capture prohibition #1 and rule L-R1 verbatim from the recorded conflict case ('square corners'). L-R1 severity: error.

---

**[27]** `./run-authority resolve 'add an emoji to the headline' --json`

```
outcome: CONFLICT
prohibition: prohibit/decorative-noise — Emoji and exclamation marks (L-24).
rule: L-R2 (severity: warning) — Red is brand/editorial punctuation; the Chicago blue family carries the interactive layer; frame is ink/white/London grey.
detected: signal 'emoji'
```

Why + conclusion: Capture prohibition 'emoji' verbatim — prohibit/decorative-noise via its recorded signal.

---

**[28]** `./run-authority resolve 'make it a red background for reading' --json`

```
outcome: CONFLICT
prohibition: prohibit/red-reading-surface — Red as a reading background (L-24).
rule: L-R2 (severity: warning) — Red is brand/editorial punctuation; the Chicago blue family carries the interactive layer; frame is ink/white/London grey.
detected: signal 'red background'
```

Why + conclusion: Capture prohibition 'red background' verbatim — prohibit/red-reading-surface; also confirms L-R2 governs colour duty (severity: warning).

---

**[29]** `./run-authority resolve 'set the article body copy in all caps sans and add a bright gradient ribbon with a glow behind it' --json`

```
outcome: CONFLICT
prohibition: prohibit/ambient-glow — Ambient glow shadows — elevation uses defined shadow tokens only (L-24).
rule: L-R1 (severity: error) — Interactive components and container surfaces are soft-rounded (radius ~8); only rules, hairlines and glyph marks stay crisp.
detected: signal 'glow'
```

Why + conclusion: Combined signal probe (caps/gradient/glow). Surfaced the fourth prohibition: prohibit/ambient-glow, detected via signal 'glow'.

---

**[30]** `./run-authority inspect fallback/ruled-panel`

```
{
 "id": "fallback/ruled-panel",
 "kind": "fallback",
 "title": "Interstitials become ruled panels",
 "statement": "No dialog canon: interstitials render as plain ruled panels in the page flow (L-07); mark the improvisation.",
 "scope": [
  "dialog",
  "modal",
  "overlay",
  "popup",
  "interstitial",
  "wizard",
  "onboarding"
 ],
 "constraints": [
  "2px ink rules, hairline detail",
  "no scrim, no motion",
  "mark the improvisation"
 ]
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect the fallback records for the specification section. ruled-panel: interstitials become plain ruled panels; constraints noted (2px ink rules, no scrim, no motion).

---

**[31]** `./run-authority inspect fallback/selection`

```
{
 "id": "fallback/selection",
 "kind": "fallback",
 "title": "Selection beyond small sets",
 "statement": "Small sets use a native select styled like a field; larger or filtered selection uses the platform default, marked.",
 "scope": [
  "select",
  "dropdown",
  "picker",
  "combobox",
  "listbox",
  "filter"
 ],
 "constraints": [
  "keep field styling",
  "mark the improvisation",
  "report a gap if the need recurs"
 ]
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect fallback statements; selection beyond small sets routes to a native select styled like a field, marked.

---

**[32]** `./run-authority inspect fallback/platform-controls`

```
{
 "id": "fallback/platform-controls",
 "kind": "fallback",
 "title": "Platform defaults for uncovered controls",
 "statement": "If the system defines no control for a need, use the platform's native element with the leader field styling; keep native semantics.",
 "scope": [
  "checkbox",
  "radio",
  "date",
  "toggle",
  "switch",
  "slider",
  "stepper"
 ],
 "constraints": [
  "field styling (rounded, 1px soft border)",
  "mark the improvisation and report a gap"
 ]
}
... (balance of the record elided; full stdout in audit.jsonl)
```

Why + conclusion: Inspect fallback statements; platform-controls confirms the field-styling route for uncovered controls, native semantics kept.

---

**[33]** `./run-authority resolve 'a zebra-striped boxed table, a gradient banner, an auto-playing carousel, justified stretched type, and status shown only as coloured dots' --json`

```
outcome: UNDEFINED
why: No artifact met the direct-match threshold (top candidate component/notice scored 4.00 vs 6.50 needed); no recipe matched; no scoped fallback applies.
normalized: {'coloured': 'color'}
closest: component/notice (4.0), component/tag (4.0), token-set/colour (4.0)
precedent [governs] precedent/ledger-rejected — Rejected at gate review (no reviewer note recorded); the table styling exists only in the sheet layer (L-18) and was declined as canon.
fallback policy: fallback/platform-controls, fallback/selection, fallback/ruled-panel
```

Why + conclusion: Final prohibition sweep (zebra / gradient / carousel / justified / dots): clean UNDEFINED. Four of five prohibitions surfaced in total — the specification section presents exactly that (count stated).

---

**[34]** `./run-authority resolve 'a masthead top bar for the documentation page with the system name and section links' --json`

```
outcome: RESOLVED
artifact: component/navbar — Top bar (score 16.0, threshold 6.5)
alternatives: guideline/hierarchy (8.0), component/action (4.0), component/meter (4.0)
```

Why + conclusion: Resolve the page's masthead need in natural language: RESOLVED -> component/navbar, a direct match leading its alternatives.

---

**[35]** `./run-authority resolve 'a section label above a serif headline with a one-line standfirst for each part of the page' --json`

```
outcome: RESOLVED
artifact: guideline/hierarchy — Section rhythm (score 28.0, threshold 6.5)
alternatives: guideline/typography (9.5), token-set/type-scale (7.5), component/tag (4.0)
```

Why + conclusion: Resolve the section-heading need: RESOLVED -> guideline/hierarchy (section label -> serif headline -> standfirst).

---

**[36]** `./run-authority resolve 'the colour roles for links, rules and attention marks across the page' --json`

```
outcome: RESOLVED
artifact: token-set/colour — Colour roles (red + Chicago blue) (score 10.0, threshold 6.5)
normalized: {'colour': 'color'}
alternatives: component/action (5.5), guideline/hierarchy (4.0), guideline/surfaces (4.0)
```

Why + conclusion: Resolve the colour-role need: RESOLVED -> token-set/colour — links and accents navy, red as punctuation.

---

**[37]** `./run-authority resolve 'small labels marking each record kind in the catalogue' --json`

```
outcome: UNDEFINED
why: No artifact met the direct-match threshold (top candidate component/tag scored 4.00 vs 6.50 needed); no recipe matched; no scoped fallback applies.
normalized: {'catalogue': 'catalog'}
closest: component/tag (4.0), guideline/hierarchy (4.0), component/field (3.0)
fallback policy: fallback/platform-controls, fallback/selection, fallback/ruled-panel
```

Why + conclusion: Resolve the kind-label need: UNDEFINED as phrased — vocabulary miss (top hit component/tag scored only 4.0 against the 6.5 threshold). Conclusion: retry with the record's own term.

---

**[38]** `./run-authority resolve 'a status label for each record group in the catalogue' --json`

```
outcome: RESOLVED
artifact: component/tag — Tag (status / category) (score 13.0, threshold 6.5)
normalized: {'catalogue': 'catalog'}
alternatives: guideline/hierarchy (4.0), component/action (1.5), component/field (1.5)
```

Why + conclusion: Retry with the pack's vocabulary ('status label'): RESOLVED -> component/tag — exactly the component the record's own checks predict. Labels adopted for the catalogue.

---

**[39]** `./run-authority gap-add --need 'Spacing scale for a documentation page: vertical rhythm values (gaps between sections, blocks, rows) — spatial distances are unrecorded.' --context '{"use":"Leader docs page layout","checked":["token-set/colour","token-set/type-scale"],"note":"no spatial token set exists in the pack"}' --scope page-layout`

```
{
 "id": "gap/20261008-165057-d11062",
 "need": "Spacing scale for a documentation page: vertical rhythm values (gaps between sections, blocks, rows) — spatial distances are unrecorded.",
 "scope_hint": "page-layout",
 "status": "open"
}
stored_at: /home/xrim/design-authority/examples/authority-sites/leader/.design-authority/gaps.jsonl
```

Why + conclusion: The authority is silent on spatial values (no spacing token set exists). Nearest recorded pieces: the type scale and radius/rule weights; improvisation kept visible via data-improv='spacing-scale'. Gap filed.

---

**[40]** `./run-authority gap-add --need 'Footer treatment for a documentation page: a metadata footer line presenting the authority and version, with no footer artifact recorded.' --context '{"use":"Leader docs page footer","nearest":"metadata register (sans 12.5-13), 2px ink rules, guideline/surfaces"}' --scope page-layout`

```
{
 "id": "gap/20261008-165057-148318",
 "need": "Footer treatment for a documentation page: a metadata footer line presenting the authority and version, with no footer artifact recorded.",
 "scope_hint": "page-layout",
 "status": "open"
}
stored_at: /home/xrim/design-authority/examples/authority-sites/leader/.design-authority/gaps.jsonl
```

Why + conclusion: No footer treatment is recorded anywhere in the pack. Nearest pieces: the metadata register and the 2px ink rule; footer improvised, marked via data-improv='colophon'. Gap filed.

---

**[41]** `./run-authority gap-add --need 'Concrete hex values for frame colours recorded by name only: ink and the London grey ramp (e.g. London 85) — the colour token-set records hexes for red #E3120B and Chicago 45 #2E45B8 but not the frame.' --context '{"use":"composing page CSS","checked":["token-set/colour"]}' --scope colour`

```
{
 "id": "gap/20261008-165057-c554c7",
 "need": "Concrete hex values for frame colours recorded by name only: ink and the London grey ramp (e.g. London 85) — the colour token-set records hexes for red #E3120B and Chicago 45 #2E45B8 but not the frame.",
 "scope_hint": "colour",
 "status": "open"
}
stored_at: /home/xrim/design-authority/examples/authority-sites/leader/.design-authority/gaps.jsonl
```

Why + conclusion: Frame colours are recorded by name only (ink, London grey ramp / London 85). Hexes improvised for the CSS, marked via data-improv='frame-values'. Gap filed.
