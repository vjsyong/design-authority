# log.md — Dominion Interface System catalogue build (audited authority calls)

Workspace: `examples/authority-sites/dominion/`. Every authority call below went through the audited runner `./run-authority` and is machine-recorded, same order, in `audit.jsonl` (44 records). Outputs are trimmed; the wrapper's full stdout per call sits in `audit.jsonl`.

Call budget: 44 total — 14 orientation/enumeration (incl. 5 `--help` checks), 4 needs resolves, 22 record inspections (14 artifacts + 2 rules + 4 prohibitions + 2 fallbacks), 1 manifest JSON read, 3 gap filings.

Deliverables: `index.html`, `fonts/Arimo-VF.ttf`, this log. Gaps filed in `.design-authority/gaps.jsonl`.

---

### 1. `./run-authority overview`

```
dominion — 0.2.0 (format 0.1)
snapshot: FIP design standard + canada.ca live web layer @ n/a - deri
artifacts: component=8, guideline=3, pattern=1, token-set=2
rules=2 recipes=1 fallbacks=2 prohibitions=4
resolution: CONFLICT -> RESOLVED -> COMPOSE -> FALLBACK -> UNDEFINED
```

**Why + conclusion:** orient on the authority before any work (identity, counts, policy, resolution semantics). Conclusion: dominion 0.2.0 (format 0.1); 14 artifacts (component 8 / guideline 3 / pattern 1 / token-set 2), 2 rules, 4 prohibitions, 2 fallbacks, 1 recipe; resolution CONFLICT → RESOLVED → COMPOSE → FALLBACK → UNDEFINED.

### 2. `./run-authority --help`

```
usage: da [-h] [--pack PACK]
          {overview,search,discover,inspect,resolve,validate,golden,gaps,gap-add,propose,dispute-add,disputes,dispute-replay,review,precedents,precedent-check,candidates} ...

da — Design Authority CLI. Same library the MCP server exposes. da overview |
search Q | discover Q | inspect ID | resolve PROBLEM | validate TARGET da
golden | gaps | gap-add | propose | dispute-add | disputes | dispute-replay
`discover` and `resolve --assist semantic` are optional retrieval extensions
(install extras: pip install fastembed numpy; build the index once with
tools/da_sem.py build). Retrieval only proposes; it never establishes
authority. Without the extras every lexical surface is unchanged.

positional arguments:
  {overview,search,discover,inspect,resolve,validate,golden,gaps,gap-add,propose,dispute-add,disputes,dispute-replay,review,precedents,precedent-check,candidates}

options:
  -h, --help            show this help message and exit
  --pack PACK
```

**Why + conclusion:** learn the CLI surface so every later call uses valid syntax. Conclusion: overview / search / inspect / resolve / validate / golden / gaps / gap-add / propose / precedents / candidates (plus dispute and review verbs).

### 3. `./run-authority search --help`

```
usage: da search [-h] [--kinds KINDS] [--limit LIMIT] [--json] query

positional arguments:
  query

options:
  -h, --help     show this help message and exit
  --kinds KINDS
  --limit LIMIT
  --json
```

**Why + conclusion:** confirm search flags (kinds filter, limit, JSON) before probing for record ids. Conclusion: search QUERY [--kinds KIND,...] [--limit N] [--json].

### 4. `./run-authority inspect --help`

```
usage: da inspect [-h] id

positional arguments:
  id

options:
  -h, --help  show this help message and exit
```

**Why + conclusion:** confirm inspect takes a single id. Conclusion: inspect ID — one record per call.

### 5. `./run-authority resolve --help`

```
usage: da resolve [-h] [--context CONTEXT] [--json] [--assist {off,semantic}]
                  [--assist-k ASSIST_K] [--assist-index ASSIST_INDEX]
                  problem [problem ...]

positional arguments:
  problem

options:
  -h, --help            show this help message and exit
  --context CONTEXT
  --json
  --assist {off,semantic}
                        optional retrieval assist (attaches candidates on
                        UNDEFINED; never changes outcomes)
  --assist-k ASSIST_K
  --assist-index ASSIST_INDEX
```

**Why + conclusion:** confirm resolve flags for scripting the needs. Conclusion: resolve PROBLEM ... [--json] [--context JSON].

### 6. `./run-authority gap-add --help`

```
usage: da gap-add [-h] --need NEED [--context CONTEXT] [--scope SCOPE]
                  [--workspace WORKSPACE]

options:
  -h, --help            show this help message and exit
  --need NEED
  --context CONTEXT
  --scope SCOPE
  --workspace WORKSPACE
```

**Why + conclusion:** confirm gap-add fields so the filed gaps are well-formed. Conclusion: gap-add --need TEXT [--context JSON] [--scope HINT] [--workspace DIR] (defaults to this workspace).

### 7. `./run-authority search --json --limit 100 ""`

```
[]
```

**Why + conclusion:** probe whether an empty query enumerates the catalogue. Conclusion: empty query tokenises to nothing and returns [] — no enumeration path via empty search.

### 8. `./run-authority search --json --limit 100 the`

```
[]
```

**Why + conclusion:** probe whether a stopword query enumerates. Conclusion: stopworded to nothing, [] again.

### 9. `./run-authority search --json --limit 100 "*"`

```
[]
```

**Why + conclusion:** probe whether a wildcard enumerates the catalogue. Conclusion: no wildcard support, [] — enumeration must come from targeted probes and the golden battery.

### 10. `./run-authority search --json --limit 100 component`

```
[
 {
  "id": "precedent/dialog-empty-state-rejected",
  "kind": "precedent",
  "title": "Dialog vessel & empty state (proposal rejected at review)",
  "score": 3.0,
  "matched": [
   "component"
  ]
 },
 {
  "id": "component/ledger",
  "kind": "component",
  "title": "Ledger (ruled register)",
  "score": 1.0,
  "matched": [
   "component"
  ]
 }
]
```

**Why + conclusion:** probe common terms for record ids. Conclusion: matched component/ledger and one precedent; search is term-bound, not a listing tool — ids are gathered per record and each record is inspected before adoption.

### 11. `./run-authority search --json --limit 100 canada`

```
[
 {
  "id": "component/action",
  "kind": "component",
  "title": "Action (slate rounded)",
  "score": 1.5,
  "matched": [
   "canada"
  ]
 },
 {
  "id": "guideline/interaction-states",
  "kind": "guideline",
  "title": "Focus & interaction states",
  "score": 1.5,
  "matched": [
   "canada"
  ]
 }
]
```

**Why + conclusion:** probe colour/token vocabulary for the token sets. Conclusion: surfaced component/action and guideline/interaction-states.

### 12. `./run-authority golden`

```
MISS  RESOLVED   (want RESOLVED  ) a primary button  -> component/action
MISS  UNDEFINED  (want RESOLVED  ) an icon-only button
MISS  FALLBACK   (want RESOLVED  ) a switch  -> fallback/platform-controls
MISS  UNDEFINED  (want RESOLVED  ) a menu item
MISS  UNDEFINED  (want RESOLVED  ) a nav item
MISS  UNDEFINED  (want RESOLVED  ) a chip
MISS  UNDEFINED  (want RESOLVED  ) a data table
MISS  UNDEFINED  (want RESOLVED  ) a version timeline
MISS  UNDEFINED  (want RESOLVED  ) a bulk action bar
MISS  UNDEFINED  (want RESOLVED  ) a save bar
MISS  UNDEFINED  (want RESOLVED  ) a flash message
MISS  RESOLVED   (want RESOLVED  ) a banner  -> component/notice
… (output trimmed)
agreement: 1/56 (2%)
```

**Why + conclusion:** run the golden battery to learn which needs this authority answers. Conclusion: against the 56-case battery dominion answers only a sparse set (action, notice, meter, platform-controls, large-selection — agreement 1/56); this confirms the pack's UNDEFINED discipline and the component id base.

### 13. `./run-authority search --json --limit 100 design`

```
[]
```

**Why + conclusion:** probe for type/token records. Conclusion: no matches — proceed via per-kind probes and the golden output.

### 14. `./run-authority search --json --limit 100 system`

```
[
 {
  "id": "component/masthead",
  "kind": "component",
  "title": "Masthead",
  "score": 1.5,
  "matched": [
   "system"
  ]
 },
 {
  "id": "fallback/platform-controls",
  "kind": "fallback",
  "title": "Platform defaults for uncovered controls",
  "score": 1.5,
  "matched": [
   "system"
  ]
 },
 {
  "id": "guideline/bilingual",
  "kind": "guideline",
  "title": "Bilingual pairings",
  "score": 1.5,
  "matched": [
   "system"
  ]
 },
 {
  "id": "precedent/declined-photographic-imagery",
… (output trimmed)
```

**Why + conclusion:** probe the word 'system' for remaining records. Conclusion: surfaced component/masthead, fallback/platform-controls, guideline/bilingual, precedent/declined-photographic-imagery.

### 15. `./run-authority resolve --json "a masthead at the top of the page with the system name, its version and a one-line description"`

```
{
 "outcome": "RESOLVED",
 "problem": "a masthead at the top of the page with the system name, its version and a one-line description",
 "context": {},
 "resolution": {
  "artifact": {
   "id": "component/masthead",
   "kind": "component",
   "title": "Masthead",
   "summary": "Top bar: white, black bottom rule, identity zone at left (red accent bar + title \u2014 generic, no Crown marks), nav links regular with medium active state underlined in black (not red \u2014 red stays ce … (line trimmed)
   "status": "beta",
   "class": "mh",
   "states": [
    "default (white, 2px black rule, red accent bar)",
    "active nav item: medium + underline"
… (output trimmed)
```

**Why + conclusion:** resolve the masthead need (name, version, one-line description) in natural language. Conclusion: RESOLVED → component/masthead (evidence 9.5, matched masthead/top/system); the record even reserves the footer wordmark zone — adopted as the page masthead.

### 16. `./run-authority resolve --json "a ruled register listing every record of the catalogue, grouped by kind, with its title and summary"`

```
{
 "outcome": "RESOLVED",
 "problem": "a ruled register listing every record of the catalogue, grouped by kind, with its title and summary",
 "context": {},
 "resolution": {
  "artifact": {
   "id": "component/ledger",
   "kind": "component",
   "title": "Ledger (ruled register)",
   "summary": "Status carries state through words (bilingual pairs over-under under 560px); statuses render as ruled chips, and registers/tables stay ruled: 2px header rule, hairline rows, pewter de-emphasis.",
   "status": "beta",
   "class": "ledger",
   "states": [
    "2px black header rule over medium caps labels",
    "1px pewter row hairlines; no zebra",
… (output trimmed)
```

**Why + conclusion:** resolve the catalogue need in natural language before designing it. Conclusion: RESOLVED → component/ledger (8.0, matched ruled/register) — the catalogue is built as ruled registers; alternatives surface component/status (word-first chips).

### 17. `./run-authority resolve --json "a standing notice block quoting a policy sentence from the specification"`

```
{
 "outcome": "UNDEFINED",
 "problem": "a standing notice block quoting a policy sentence from the specification",
 "context": {},
 "resolution": null,
 "alternatives": [],
 "evidence": {},
 "authority": {
  "authority": "dominion",
  "version": "0.2.0",
  "commit": "n/a - derived from public sources, not a repository"
 },
 "closest": [
  {
   "id": "component/notice",
   "kind": "component",
   "title": "Notice (ruled box)",
   "score": 5.5,
   "matched": [
    "notic",
… (output trimmed)
```

**Why + conclusion:** resolve the spec-quote treatment before building it. Conclusion: UNDEFINED (top candidate component/notice 5.5 < 6.5) — no direct record for quoted notice blocks; the spec quotes are instead presented inside ruled registers (a recorded vehicle) rather than a new element.

### 18. `./run-authority resolve --json "a footer line crediting the authority and its pack version"`

```
{
 "outcome": "UNDEFINED",
 "problem": "a footer line crediting the authority and its pack version",
 "context": {},
 "resolution": null,
 "alternatives": [],
 "evidence": {},
 "authority": {
  "authority": "dominion",
  "version": "0.2.0",
  "commit": "n/a - derived from public sources, not a repository"
 },
 "closest": [
  {
   "id": "pattern/plain-chart",
   "kind": "pattern",
   "title": "Plain chart (bars, month grid, sparkline)",
   "score": 4.0,
   "matched": [
    "lin"
… (output trimmed)
```

**Why + conclusion:** resolve the footer need. Conclusion: UNDEFINED (top candidate component/masthead 1.5 — it merely reserves a bottom-right plain-text zone) — so the credit line is built from that recorded zone, marked as an improvisation, and filed as a gap.

### 19. `./run-authority inspect component/action`

```
{
 "id": "component/action",
 "kind": "component",
 "title": "Action (slate rounded)",
 "summary": "Primary = solid slate button (#26374A, 4px radius \u2014 live-measured on Canada.ca), white label; secondary = 2px slate outline; tertiary = underlined link. One primary per view. Red stays ceremonial, out o … (line trimmed)
 "status": "beta",
 "aliases": [
  "button",
  "cta",
  "primary button",
  "action",
  "submit button",
… (output trimmed)
```

**Why + conclusion:** inspect component/action before adopting it for links and actions. Conclusion: primary = solid slate #26374A radius 4, white label; secondary = 2px slate outline; tertiary = underlined link; red is out of action roles.

### 20. `./run-authority inspect component/masthead`

```
{
 "id": "component/masthead",
 "kind": "component",
 "title": "Masthead",
 "summary": "Top bar: white, black bottom rule, identity zone at left (red accent bar + title \u2014 generic, no Crown marks), nav links regular with medium active state underlined in black (not red \u2014 red stays cere … (line trimmed)
 "status": "beta",
 "aliases": [
  "masthead",
  "header",
  "top bar",
  "navigation",
  "identity zone"
… (output trimmed)
```

**Why + conclusion:** inspect component/masthead before adopting it as the page masthead. Conclusion: white, 2px black bottom rule, red accent bar, nav links regular with medium + black underlined active state; footer zone reserved for a plain-text wordmark — adopted.

### 21. `./run-authority inspect component/field`

```
{
 "id": "component/field",
 "kind": "component",
 "title": "Field (soft border, blue glow focus)",
 "summary": "Fields: soft border (1px #E0E0E0), soft radius 4; label above (medium caps); focus = blue glow (1px #66AFE9 outline + 8px rgba(102,175,233,.6) halo \u2014 live-measured); error = left rule + plain sentence u … (line trimmed)
 "status": "beta",
 "aliases": [
  "field",
  "input",
  "form field",
  "text field",
  "error message",
… (output trimmed)
```

**Why + conclusion:** inspect component/field (form vocabulary; reference for the spec list). Conclusion: 1px #E0E0E0 soft border, radius 4, blue-glow focus, left-rule error treatment; not instantiated on this page but catalogued.

### 22. `./run-authority inspect component/select`

```
{
 "id": "component/select",
 "kind": "component",
 "title": "Select (small sets)",
 "summary": "Small fixed sets (\u2264 ~12) = native select squared like a field. Larger/filtered selection out of scope; platform fallback, marked as improvisation.",
 "status": "beta",
 "aliases": [
  "select",
  "dropdown",
  "choice",
  "small select"
 ],
… (output trimmed)
```

**Why + conclusion:** inspect component/select for the catalogue. Conclusion: small fixed sets only; larger selection defers to the fallback — no selects needed on this page.

### 23. `./run-authority inspect component/meter`

```
{
 "id": "component/meter",
 "kind": "component",
 "title": "Progress meter",
 "summary": "Meter = square track in #F4F4F4 with black fill and a plain readout ('7 of 10 steps'); restart = outline square. Static only; nothing decoratively animates (motion gated, per the standard's animation doctrin … (line trimmed)
 "status": "beta",
 "aliases": [
  "meter",
  "progress",
  "progress bar",
  "import progress",
  "readout"
… (output trimmed)
```

**Why + conclusion:** inspect component/meter before adopting it for the coverage readout. Conclusion: square #F4F4F4 track, black fill, plain readout ('7 of 10 steps' idiom), static — adopted as '14 of 14 records inspected'.

### 24. `./run-authority inspect component/status`

```
{
 "id": "component/status",
 "kind": "component",
 "title": "Status label (word-first)",
 "summary": "Status carries state through words (bilingual pairs over-under under 560px); statuses render as ruled chips, and registers/tables stay ruled: 2px header rule, hairline rows, pewter de-emphasis.",
 "status": "beta",
 "aliases": [
  "status",
  "status label",
  "state label",
  "on track",
  "slipping",
… (output trimmed)
```

**Why + conclusion:** inspect component/status before adopting ruled chips in the registers. Conclusion: word-first plain label in a ruled box; emphasis by structure, never hue; bilingual pairs over-under under 560px — adopted for 'beta' chips.

### 25. `./run-authority inspect component/ledger`

```
{
 "id": "component/ledger",
 "kind": "component",
 "title": "Ledger (ruled register)",
 "summary": "Status carries state through words (bilingual pairs over-under under 560px); statuses render as ruled chips, and registers/tables stay ruled: 2px header rule, hairline rows, pewter de-emphasis.",
 "status": "beta",
 "aliases": [
  "ledger",
  "register",
  "table",
  "entries table",
  "ruled table",
… (output trimmed)
```

**Why + conclusion:** inspect component/ledger before adopting it for the catalogue. Conclusion: 2px black header rule over medium caps labels, 1px pewter row hairlines, no zebra, row hover #F4F4F4, inline status labels — adopted as the register structure.

### 26. `./run-authority inspect component/notice`

```
{
 "id": "component/notice",
 "kind": "component",
 "title": "Notice (ruled box)",
 "summary": "Notices are full-width banded rows (#F4F4F4) under a 2px rule; sentence only, no icon, no toast.",
 "status": "beta",
 "aliases": [
  "notice",
  "message",
  "confirmation",
  "save confirmation",
  "announcement",
… (output trimmed)
```

**Why + conclusion:** inspect component/notice before adopting it for the build disclosure. Conclusion: full-width #F4F4F4 band under a 2px rule, sentence only, no icon, no toast (toast vocabulary deliberately absent) — adopted as the notice band.

### 27. `./run-authority inspect guideline/typography`

```
{
 "id": "guideline/typography",
 "kind": "guideline",
 "title": "Typography (one family)",
 "summary": "One family (Helvetica-class stand-in: Arimo), weights as roles: Light = quiet formal accents, Regular = default text, Medium = headings and key labels (web role per the standard), Bold = reserved for signage … (line trimmed)
 "status": "beta",
 "aliases": [
  "typography",
  "font",
  "weights",
  "helvetica"
 ],
… (output trimmed)
```

**Why + conclusion:** inspect guideline/typography before setting the page's type. Conclusion: one family (Helvetica-class stand-in: Arimo), weights as roles — Light quiet accents, Regular default, Medium headings/labels, Bold rare signage; Arimo-VF.ttf copied in and used.

### 28. `./run-authority inspect guideline/bilingual`

```
{
 "id": "guideline/bilingual",
 "kind": "guideline",
 "title": "Bilingual pairings",
 "summary": "The signature structural device: primary page titles and key labels render bilingually (English | French, side-by-side, thin divider; over-under when narrow). Body content stays in the app's own language. Wh … (line trimmed)
 "status": "beta",
 "aliases": [
  "bilingual",
  "french",
  "english",
  "bilingual titles"
 ],
… (output trimmed)
```

**Why + conclusion:** inspect guideline/bilingual — the signature structural device. Conclusion: primary titles and key labels pair English | French side-by-side with a thin divider, over-under when narrow (<560px); body stays in one language — adopted for the page title pair.

### 29. `./run-authority inspect guideline/interaction-states`

```
{
 "id": "guideline/interaction-states",
 "kind": "guideline",
 "title": "Focus & interaction states",
 "summary": "Focus does change colour: blue glow \u2014 1px #66AFE9 outline + 8px rgba(102,175,233,.6) halo (live-measured on Canada.ca). Exclusive to focus; reads on any ground.",
 "status": "beta",
 "aliases": [
  "focus",
  "focused",
  "focus ring",
  "focus glow",
  "interaction states"
… (output trimmed)
```

**Why + conclusion:** inspect guideline/interaction-states for the focus treatment. Conclusion: focus = 1px #66AFE9 outline + 8px rgba(102,175,233,.6) halo, exclusive to focus — adopted on links and controls.

### 30. `./run-authority inspect token-set/type-scale`

```
{
 "id": "token-set/type-scale",
 "kind": "token-set",
 "title": "Screen type rhythm",
 "summary": "Screen rhythm (AUTHORED interpretation, no sizes exist in source): page title 32/400; section headings 20/500; body 16/1.6; metadata 13 grey; bilingual pairings same size both languages.",
 "status": "beta",
 "aliases": [
  "type scale",
  "font size",
  "title size",
  "body size"
 ],
… (output trimmed)
```

**Why + conclusion:** inspect token-set/type-scale for exact sizes. Conclusion: page title 32/400, section headings 20/500, body 16/1.6, metadata 13 grey, bilingual pairs same size both languages — quoted exactly in the CSS.

### 31. `./run-authority inspect token-set/colour`

```
{
 "id": "token-set/colour",
 "kind": "token-set",
 "title": "Colour roles (ceremony + web layer)",
 "summary": "FIP red strictly for ceremony: masthead accent device, the single primary action, identity zone marks. Black = text/structure; white = ground; pewter = de-emphasis (metadata, secondary labels). Status and er … (line trimmed)
 "status": "beta",
 "aliases": [
  "palette",
  "colour",
  "color",
  "fip red",
  "slate",
… (output trimmed)
```

**Why + conclusion:** inspect token-set/colour for the palette codes. Conclusion: red ceremony-only (accent/identity, never status); black = text/structure, white = ground, pewter = de-emphasis; status/errors not colour-coded. Note: no hexes recorded for FIP red or pewter — handled as a marked stand-in and gap.

### 32. `./run-authority inspect pattern/plain-chart`

```
{
 "id": "pattern/plain-chart",
 "kind": "pattern",
 "title": "Plain chart (bars, month grid, sparkline)",
 "summary": "Charts render in the rule-and-grid idiom: black bars on rules, a month grid, and a slate trend line; no rings, no shadows, no new colours.",
 "status": "beta",
 "aliases": [
  "chart",
  "bar chart",
  "graph",
  "plot",
  "data figure",
… (output trimmed)
```

**Why + conclusion:** inspect pattern/plain-chart for the catalogue. Conclusion: rule-and-grid charts (black bars on rules, month grid, slate trend line), no new colours — catalogued; not instantiated (nothing to chart on this page).

### 33. `./run-authority inspect D-R1`

```
{
 "id": "D-R1",
 "name": "web-layer-interaction",
 "severity": "warning",
 "applies_to": [
  "css",
  "html"
 ],
 "summary": "Interactive layer follows the live web layer: slate actions (#26374A, radius 4), blue focus glow (#66AFE9), soft borders.",
 "why": "Live measurements on Canada.ca accepted at Gate 2 (D-01, D-11, D-21).",
 "fix": "Use the measured slate/blue values for interactive elements."
}
```

**Why + conclusion:** inspect rule D-R1 to quote it verbatim in the specification summary. Conclusion: interactive layer = slate actions (#26374A, radius 4), blue focus glow (#66AFE9), soft borders — quoted.

### 34. `./run-authority inspect D-R2`

```
{
 "id": "D-R2",
 "name": "ceremonial-red",
 "severity": "warning",
 "applies_to": [
  "css",
  "html"
 ],
 "summary": "FIP red is ceremony only \u2014 never status, errors, or reading surfaces.",
 "why": "FIP standard + Gate 2 (D-05, D-22).",
 "fix": "Remove red from status/error/background roles."
}
```

**Why + conclusion:** inspect rule D-R2 to quote it verbatim. Conclusion: 'FIP red is ceremony only — never status, errors, or reading surfaces' — constrains the page (red appears only in the accent bar).

### 35. `./run-authority inspect prohibit/red-status`

```
{
 "id": "prohibit/red-status",
 "statement": "Red for status or errors \u2014 red is ceremonial (D-R2).",
 "signals": [
  "red error",
  "red errors",
  "red for errors",
  "red for the error",
  "red status",
  "red for status",
  "red errors",
  "red alerts",
  "red for alerts"
 ],
 "rule": "D-R2",
 "kind": "prohibition"
}
```

**Why + conclusion:** inspect prohibit/red-status for the spec list (titles/counts). Conclusion: red banned for status/errors; governed by D-R2 — listed.

### 36. `./run-authority inspect prohibit/elevation-shadows`

```
{
 "id": "prohibit/elevation-shadows",
 "statement": "Elevation or drop shadows \u2014 structure is flat, only the focus glow exists (D-22).",
 "signals": [
  "drop shadow",
  "elevation",
  "box shadow",
  "soft shadow"
 ],
 "rule": "D-R1",
 "kind": "prohibition"
}
```

**Why + conclusion:** inspect prohibit/elevation-shadows. Conclusion: 'structure is flat, only the focus glow exists' — the page ships zero non-focus shadows (verified).

### 37. `./run-authority inspect prohibit/imagery-pictograms`

```
{
 "id": "prohibit/imagery-pictograms",
 "statement": "Imagery, pictograms or illustrative decoration (D-22).",
 "signals": [
  "imagery",
  "photo",
  "photograph",
  "illustration",
  "pictogram",
  "clip art"
 ],
 "rule": "D-R1",
 "kind": "prohibition"
}
```

**Why + conclusion:** inspect prohibit/imagery-pictograms. Conclusion: no imagery, pictograms or illustration — the page is text and rules only.

### 38. `./run-authority inspect prohibit/decorative-colour`

```
{
 "id": "prohibit/decorative-colour",
 "statement": "Decorative colour outside the FIP families (D-22).",
 "signals": [
  "decorative colour",
  "decorative color",
  "vibrant colours",
  "vibrant colors",
  "invented colour",
  "invented color",
  "neon"
 ],
 "rule": "D-R1",
 "kind": "prohibition"
}
```

**Why + conclusion:** inspect prohibit/decorative-colour. Conclusion: no decorative colour outside the FIP families — palette stays black/white/greys/slate + ceremonial red.

### 39. `./run-authority inspect fallback/platform-controls`

```
{
 "id": "fallback/platform-controls",
 "title": "Platform defaults for uncovered controls",
 "statement": "If the system defines no control for a need, use the platform's native element with the field styling; keep native semantics.",
 "scope": [
  "checkbox",
  "radio",
  "date",
  "toggle",
  "switch",
  "slider",
  "check",
  "stepper"
 ],
 "constraints": [
  "field styling (soft border, radius 4)",
  "blue glow focus",
  "mark the improvisation and report a gap"
 ],
 "kind": "fallback"
}
```

**Why + conclusion:** inspect fallback/platform-controls for the spec list. Conclusion: uncovered controls fall to platform-native elements with field styling, marked — listed with constraints.

### 40. `./run-authority inspect fallback/large-selection`

```
{
 "id": "fallback/large-selection",
 "title": "Selection beyond small sets",
 "statement": "Small fixed sets use the select; larger or filtered selection uses the platform default, marked.",
 "scope": [
  "picker",
  "combobox",
  "autocomplete",
  "filter",
  "listbox",
  "search"
 ],
 "constraints": [
  "keep field styling",
  "mark the improvisation"
 ],
 "kind": "fallback"
}
```

**Why + conclusion:** inspect fallback/large-selection for the spec list. Conclusion: small sets use the select; larger/filtered selection is a marked platform fallback — listed.

### 41. `./run-authority overview --json`

```
{
 "authority": {
  "authority": "dominion",
  "version": "0.2.0",
  "commit": "n/a - derived from public sources, not a repository"
 },
 "description": "An austere civic interface system derived from the Government of Canada FIP standard and the live Canada.ca web layer for the Design Authority synthesis experiment. Bilingual, structured, calm; no govern … (line trimmed)
 "counts": {
  "artifacts": {
   "component": 8,
   "guideline": 3,
   "token-set": 2,
   "pattern": 1
  },
  "rules": 2,
  "recipes": 1,
  "fallbacks": 2,
  "prohibitions": 4
 },
 "capabilities": {
  "search": true,
  "resolve": true,
  "validators": [],
  "gap_reporting": true,
  "extension_proposals": true,
  "resolution_assist": "off"
… (output trimmed)
```

**Why + conclusion:** read the manifest JSON for the exact one-line description, counts and policy quotes used on the page. Conclusion: description quoted verbatim in the masthead; counts (2/4/2/1) and the on_undefined / on_conflict policy sentences used in the specification summary.

### 42. `./run-authority gap-add --need "a footer credit line for pages built under the authority: 'built under the dominion authority' plus the pack version" --context "{\"source\": \"examples/authority-sites/dominion\", \"page\": \"index.html\", \"observed\": \"resolve UNDEFINED; top candidate component/masthead 1.50 vs 6.50 threshold\", \"built_with\": \"masthead's recorded footer zone: plain text, bottom-right, metadata grey\", \"note\": \"the masthead record reserves the zone; the credit line itself is unrecorded\"}" --scope component/masthead`

```
{
 "id": "gap/20261008-165141-a9a135",
 "need": "a footer credit line for pages built under the authority: 'built under the dominion authority' plus the pack version",
 "context": {
  "source": "examples/authority-sites/dominion",
  "page": "index.html",
  "observed": "resolve UNDEFINED; top candidate component/masthead 1.50 vs 6.50 threshold",
  "built_with": "masthead's recorded footer zone: plain text, bottom-right, metadata grey",
  "note": "the masthead record reserves the zone; the credit line itself is unrecorded"
 },
 "authority": {
  "authority": "dominion",
  "version": "0.2.0",
  "commit": "n/a - derived from public sources, not a repository"
 },
 "searched": null,
… (output trimmed)
```

**Why + conclusion:** file the footer-line improvisation (resolve returned UNDEFINED; the brief mandates the line). Conclusion: gap/20261008-165141-a9a135 stored in this workspace's .design-authority store.

### 43. `./run-authority gap-add --need "exact colour codes for roles the pack names but does not value: FIP red (ceremonial accent device) and pewter (de-emphasis grey / row hairlines)" --context "{\"source\": \"examples/authority-sites/dominion\", \"page\": \"index.html\", \"observed\": \"token-set/colour records the roles; no hexes for FIP red or pewter\", \"built_with\": \"marked stand-in #EA2D2E for the ceremonial accent bar; de-emphasis text stand-in #5C5C5C; greys otherwise mapped from recorded #F4F4F4 and #E0E0E0\"}" --scope token-set/colour`

```
{
 "id": "gap/20261008-165141-acb94d",
 "need": "exact colour codes for roles the pack names but does not value: FIP red (ceremonial accent device) and pewter (de-emphasis grey / row hairlines)",
 "context": {
  "source": "examples/authority-sites/dominion",
  "page": "index.html",
  "observed": "token-set/colour records the roles; no hexes for FIP red or pewter",
  "built_with": "marked stand-in #EA2D2E for the ceremonial accent bar; de-emphasis text stand-in #5C5C5C; greys otherwise mapped from recorded #F4F4F4 and #E0E0E0"
 },
 "authority": {
  "authority": "dominion",
  "version": "0.2.0",
  "commit": "n/a - derived from public sources, not a repository"
 },
 "searched": null,
 "closest": null,
… (output trimmed)
```

**Why + conclusion:** file the unrecorded colour codes (FIP red, pewter) used as marked stand-ins. Conclusion: gap/20261008-165141-acb94d stored.

### 44. `./run-authority gap-add --need "a page-level spacing rhythm for documentation pages: vertical steps between masthead, sections and registers (no spacing tokens are recorded)" --context "{\"source\": \"examples/authority-sites/dominion\", \"page\": \"index.html\", \"observed\": \"token sets carry colour roles and type rhythm only; inter-block spacing is unrecorded\", \"built_with\": \"composed from the screen type rhythm (16px body / 32px title steps)\"}" --scope system-wide`

```
{
 "id": "gap/20261008-165141-150790",
 "need": "a page-level spacing rhythm for documentation pages: vertical steps between masthead, sections and registers (no spacing tokens are recorded)",
 "context": {
  "source": "examples/authority-sites/dominion",
  "page": "index.html",
  "observed": "token sets carry colour roles and type rhythm only; inter-block spacing is unrecorded",
  "built_with": "composed from the screen type rhythm (16px body / 32px title steps)"
 },
 "authority": {
  "authority": "dominion",
  "version": "0.2.0",
  "commit": "n/a - derived from public sources, not a repository"
 },
 "searched": null,
 "closest": null,
… (output trimmed)
```

**Why + conclusion:** file the documentation-page spacing rhythm (no spacing tokens recorded). Conclusion: gap/20261008-165141-150790 stored; the three gap ids appear on the page's notice band and beside every mark.

---

## Result

- Page: `index.html` — masthead (bilingual pair, red accent device, nav), catalogue of all 14 artifacts as ruled registers grouped by kind (ledger + status chips + meter readout), specification summary (2 rules, 4 prohibitions, 2 fallbacks, resolution order + policy, quoted verbatim), build-disclosure notice band, footer credit line.

- Font: `fonts/Arimo-VF.ttf` (copied per brief; declared via @font-face; verified loaded).

- Improvisations (marked, dashed outlines on the page, toggle in the notice band): ceremonial accent code, grey value mappings, page rhythm, footer line.

- Gaps filed: `gap/20261008-165141-a9a135` (footer line) · `gap/20261008-165141-acb94d` (colour codes) · `gap/20261008-165141-150790` (spacing rhythm).

- Verification: headless render at 1280px and 390px — no horizontal scroll, font loaded, recorded values in computed styles (slate #26374A, band #F4F4F4, soft #E0E0E0, radius 4, 32/400 · 20/500 · 16/1.6 · 13 grey), zero non-focus shadows, marks toggle works, bilingual pair stacks under 560px.
