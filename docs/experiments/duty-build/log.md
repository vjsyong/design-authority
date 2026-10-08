# Duty build — authority command log

Every authority command for the Duty demo build (workspace `docs/experiments/duty-build/`),
in execution order, run through the audited runner `./run-authority` (each call is also
machine-recorded in `audit.jsonl` beside this file).

### 1. ./run-authority overview --json
```json
{
 "authority": {"authority": "triage", "version": "0.12.1", "commit": "ec490bb7f336b8105698f7f92a1be8cbce97d7ff"},
 "counts": {"artifacts": {"token-set": 7, "guideline": 10, "component": 56, "pattern": 7},
            "rules": 19, "recipes": 0, "fallbacks": 3, "prohibitions": 6},
 "capabilities": {"search": true, "resolve": true, "validators": [], "gap_reporting": true,
                  "extension_proposals": true, "resolution_assist": "off"},
 "policy": {"on_undefined": "Implement per the consuming project's fallback policy, mark the improvisation, and report a gap. Never present improvisation as canonical.",
            "on_conflict": "Do not implement as requested; the request violates an explicit constraint (see the cited rule/prohibition)."},
 "resolution_semantics": ["CONFLICT: request contradicts an explicit constraint (prohibition/rule).",
   "RESOLVED: a direct artifact defines the solution.", "COMPOSE: a sanctioned recipe composes existing artifacts.",
   "FALLBACK: a sanctioned generic fallback applies.", "UNDEFINED: no adequate authority answer exists (structured, not an error)."]
}
```
Why + conclusion: Orientation first — authority is Triage v0.12.1 (80 artifacts), and its
UNDEFINED policy is explicit: mark improvisations and file a gap. That is exactly this
build's working protocol, so I now resolve every UI need in natural language before writing markup.

### 2. ./run-authority --help
```
usage: da [-h] [--pack PACK]
          {overview,search,discover,inspect,resolve,validate,golden,gaps,gap-add,propose,review,precedents,precedent-check,candidates} ...
da — Design Authority CLI. `discover` and `resolve --assist semantic` are optional
retrieval extensions; retrieval only proposes, it never establishes authority.
```
Why + conclusion: Confirmed the exact surface I may use (resolve / discover / inspect /
validate / gap-add); there is no override or bypass surface, so every adoption will go
through resolve + inspect as the protocol demands.
### 3. ./run-authority resolve "an incident list page with a header, filters and a table of records" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "component/page-head", "title": "Page header",
   "class": "page-head", "status": "stable", "source": {"path": "core/base.css (.page-head)"},
   "summary": "The title row at the top of a page: title, description and actions."}},
 "alternatives": [{"id": "pattern/viewer", "score": 13.0}, {"id": "component/tbl", "score": 5.5},
                  {"id": "component/audit-row", "score": 4.0}],
 "evidence": {"score": 18.0, "matched": ["pag", "header", "~pag header"], "threshold": 6.5}}
```
Why + conclusion: The page-level ask landed on the recorded Page header; the alternatives
named the call's other needs (detail-page pattern, table) so I split the rest into per-element
resolves instead of building on one vague hit.

### 4. ./run-authority resolve "a data table" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "component/tbl", "title": "Table", "class": "tbl",
   "states": ["default", "row hover", "selected", "reflowed (mcards)"],
   "a11y": ["th scope where the header is meaningful; row checkbox needs aria-label.",
            "Hover-revealed row actions must also be reachable by keyboard focus."]}},
 "evidence": {"score": 13.0, "matched": ["tabl", "data", "~data tabl"], "threshold": 6.5}}
```
Why + conclusion: Canonical-wording confirmation for the list table: component/tbl is
recorded with a phone reflow state (mcards), so the incident table will adopt `.tbl` and
its recorded reflow rather than any improvised responsive scheme.

### 5. ./run-authority resolve "a row of filter chips to narrow a list" --json
```json
{"outcome": "UNDEFINED",
 "why": "No artifact met the direct-match threshold (top candidate component/chip scored 13.00 vs 6.50 needed); no recipe matched; no scoped fallback applies.",
 "closest": [{"id": "component/chip", "score": 13.0, "matched": ["filter", "chip", "~filter chip"]},
             {"id": "component/index-row", "score": 13.0, "matched": ["list", "row", "~list row"]},
             {"id": "component/audit-row", "score": 8.0}]}
```
Why + conclusion: UNDEFINED because chip and index-row tie at 13.0 (no 2.0 lead) — the
authority will not pick between them; per protocol I run `discover`, inspect the candidates,
and treat the filter-row composition honestly as needing a mark if the records do not cover it.

### 6. ./run-authority resolve "a small coloured dot for severity" --json
```json
{"outcome": "UNDEFINED",
 "why": "No artifact met the direct-match threshold (top candidate component/dot scored 5.50 vs 6.50 needed); no recipe matched; no scoped fallback applies.",
 "closest": [{"id": "component/dot", "title": "Status dot", "score": 5.5, "matched": ["color", "dot"]},
             {"id": "component/btn", "score": 4.0}]}
```
Why + conclusion: Thin — my phrasing fell under the threshold; a status dot clearly exists
(component/dot) so I run `discover` and will re-ask with the record's own canonical wording.

### 7. ./run-authority resolve "a text badge for the incident status" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "component/badge", "title": "Badge", "class": "badge",
   "states": ["neutral", "ok", "warn", "err", "acc", "solid"],
   "a11y": ["Uppercase micro-label; never the only signal - pair with text that says the same thing."]}},
 "evidence": {"score": 14.5, "matched": ["status", "text", "badg", "~status badg"], "threshold": 6.5}}
```
Why + conclusion: Status text will be a recorded Badge; its a11y note is binding, so every
badge will sit next to plain text saying the same thing (and match the severity dot).

### 8. ./run-authority discover "a row of filter chips to narrow a list" --k 5
```
candidates (retrieval signal only; NOT authority):
  rrf 0.03252  component/chip         artifact     Chip        lex#1 sem#2 cos 0.629
  rrf 0.03178  component/index-row    artifact     Index row   lex#5 sem#1 cos 0.629
  rrf 0.03150  component/kv           artifact     Key-value rows
  rrf 0.03126  component/cb           artifact     Combobox
  rrf 0.03105  component/audit-row    artifact     Audit rows
```
Why + conclusion: Retrieval agrees chip is the leading candidate for the filter control;
nothing here is authority, so next I inspect component/chip (and index-row) before use.

### 9. ./run-authority discover "a small coloured dot for severity" --k 5
```
candidates (retrieval signal only; NOT authority):
  rrf 0.03279  component/dot          artifact     Status dot   lex#1 sem#1 cos 0.723
  rrf 0.03128  token-set/colour       artifact     Colour - paper, ink, one accent, ...
  rrf 0.03125  TDS002                 rule
  rrf 0.03002  component/notif        artifact     Notifications
  rrf 0.02988  pattern/misc           artifact     Index & eval
```
Why + conclusion: component/dot leads both retrieval legs decisively; I inspect it and will
re-ask with canonical wording ("status dot") to turn the thin phrasing into a clean sanction.
### 10. ./run-authority resolve "an app shell with a sidebar, brand and navigation" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "component/shell", "title": "App shell", "class": "app",
   "note": "The page skeleton: sidebar, main column and content frame (.app / .side / .main)."}},
 "alternatives": [{"id": "component/nav-item", "score": 8.0}, {"id": "component/topbar", "score": 7.0},
                  {"id": "component/bottom-nav", "score": 4.0}]}
```
Why + conclusion: Both pages share one recorded skeleton; I adopt exactly its scope (.app / .side /
.main / .content) plus the brand and nav furniture, and keep the chrome identical on both pages.

### 11. ./run-authority resolve "a skip link to jump past the navigation" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "component/nav-item", "title": "Nav item", "class": "nav-item"}},
 "evidence": {"score": 8.0, "threshold": 6.5},
 "alternatives": [{"id": "component/bottom-nav", "score": 4.0}, {"id": "guideline/voice", "score": 3.0}]}
```
Why + conclusion: A lexical misfire: a skip link is not a nav item, so I do NOT treat this as a
sanction. The shipped core class `.skip` has no catalogue record anywhere in the pack, so the skip
link is built from core CSS and reported as a gap (command 33); the misfire is itself evidence.

### 12. ./run-authority resolve "a detail page for a single record" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "pattern/viewer", "title": "Detail page",
   "summary": "Two-column detail: plain/HTML body and queue controls left, sticky metadata and audit right."}}}
```
Why + conclusion: The case page adopts the recorded viewer pattern: events and notes left,
sticky Details column right (grid .detail-grid / .stickycol from patterns.css).

### 13. ./run-authority resolve "an incident header with an id and current state" --json
```json
{"outcome": "UNDEFINED",
 "why": "No artifact met the direct-match threshold (top candidate component/empty scored 4.00 vs 6.50 needed); no recipe matched; no scoped fallback applies.",
 "closest": [{"id": "component/empty", "score": 4.0}, {"id": "component/page-head", "score": 4.0},
             {"id": "component/page-state", "score": 4.0}]}
```
Why + conclusion: The id-plus-state header is not a recorded composite; per protocol I run
`discover` before deciding how to compose it.

### 14. ./run-authority discover "an incident header with an id and current state" --k 5
```
candidates (retrieval signal only; NOT authority):
  rrf 0.03154  component/page-head    artifact   Page header   lex#1 sem#6 cos 0.602
  rrf 0.03042  component/pager-num    artifact   Numbered pagination
  rrf 0.03008  component/nav-item     artifact   Nav item
  rrf 0.02920  component/page-state   artifact   Full-page state
  rrf 0.02837  component/tbl          artifact   Table
```
Why + conclusion: Retrieval points at page-head as the header anchor; I compose the marked
composite (page-head + badge + dot) and file a gap rather than present it as a direct record.

### 15. ./run-authority resolve "key-value metadata rows for a record" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "component/kv", "title": "Key-value rows", "class": "kv",
   "note": "A two-column metadata grid (label -> value) for detail panes and sidebars."}},
 "alternatives": [{"id": "pattern/viewer", "score": 5.5}]}
```
Why + conclusion: The case page's metadata rows adopt component/kv exactly as recorded.

### 16. ./run-authority resolve "an event timeline" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "component/tl", "title": "Timeline", "class": "tl",
   "states": ["default", "status-dots"],
   "a11y": ["Ordered list; dots are decorative (the text carries the meaning)."]}}}
```
Why + conclusion: The event timeline adopts component/tl with its status-dots state; copy stays
in the list text so the dots remain decorative per the record.

### 17. ./run-authority resolve "a log panel with timestamped entries" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "component/logpanel", "title": "Log panel", "class": "logpanel",
   "note": "An ink terminal panel for logs and streamed output; rows colour by kind."}}}
```
Why + conclusion: The notes/activity panel adopts component/logpanel; entries follow the recorded
row idiom (mono time, kind badge, message).

### 18. ./run-authority resolve "a primary action button" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "component/btn", "title": "Button", "class": "btn",
   "states": ["default", "hover", "active", "focus-visible", "disabled", "busy (guardApply)"],
   "a11y": ["Use a real <button> or <a>; never a clickable div."]}}}
```
Why + conclusion: Page actions adopt component/btn as real anchors/buttons only; the recorded
a11y line rules out any clickable div.

### 19. ./run-authority resolve "filter chips" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "component/chip", "title": "Chip", "class": "chip",
   "states": ["default", "hover", "active(selected)", "focus-visible"],
   "a11y": ["Counts live in .n; the whole chip is the target (not just the label)."]}},
 "evidence": {"score": 13.0, "matched": ["filter", "chip", "~filter chip"], "threshold": 6.5}}
```
Why + conclusion: Canonical-wording confirmation: the earlier UNDEFINED was my phrasing, not a
missing record - "filter chips" resolves cleanly and the active(selected) state is recorded.

### 20. ./run-authority resolve "status dot" --json
```json
{"outcome": "RESOLVED",
 "resolution": {"artifact": {"id": "component/dot", "title": "Status dot", "class": "dot",
   "note": "A 7px square status dot; neutral by default, with ok / warn / err variants paired with text (never colour alone)."}},
 "evidence": {"score": 18.0, "matched": ["status", "dot", "~status dot"], "threshold": 6.5}}
```
Why + conclusion: Canonical confirmation for the second UNDEFINED; severity dots adopt
component/dot and always sit next to the severity text.

### 21. ./run-authority inspect component/shell
```json
{"id": "component/shell", "body": {"class": "app",
 "note": "The page skeleton: sidebar, main column and content frame (.app / .side / .main), with the shell contract on /components/navigation."}}
```
Why + conclusion: Inspected before adoption - confirms .app / .side / .main as the sanctioned
skeleton; both pages are built on exactly this frame.

### 22. ./run-authority inspect component/page-head
```json
{"id": "component/page-head", "body": {"class": "page-head",
 "note": "The title row at the top of a page: title, description and actions."}}
```
Why + conclusion: Adopted for both page headers; its documented slots (title, description,
actions) are exactly what the two pages need.

### 23. ./run-authority inspect component/tbl
```json
{"id": "component/tbl", "body": {"class": "tbl",
 "states": ["default", "row hover", "selected", "reflowed (mcards)"],
 "verify": [".tbl", ".tbl tr:hover", ".tbl tr.selected", ".tbl.mcards", ".tbl-records"],
 "a11y": ["th scope where the header is meaningful; row checkbox needs aria-label.",
          "Hover-revealed row actions must also be reachable by keyboard focus."]}}
```
Why + conclusion: The incident table adopts `.tbl` with the recorded reflowed (mcards) phone
state, th scope on every column, and no hover-revealed actions (nothing to keyboard-trap).

### 24. ./run-authority inspect component/chip
```json
{"id": "component/chip", "body": {"class": "chip",
 "states": ["default", "hover", "active(selected)", "focus-visible"],
 "a11y": ["Counts live in .n; the whole chip is the target (not just the label)."]}}
```
Why + conclusion: Confirms the chip idiom for the filter row: `.chip.active` for the selected
filter and counts in `.n`, as in the shipped examples.

### 25. ./run-authority inspect component/dot
```json
{"id": "component/dot", "body": {"class": "dot",
 "note": "A 7px square status dot; neutral by default, with ok / warn / err variants paired with text (never colour alone)."}}
```
Why + conclusion: Severity dots use only the recorded variants (err / warn / acc here) and every
dot is accompanied by text.

### 26. ./run-authority inspect component/badge
```json
{"id": "component/badge", "body": {"class": "badge",
 "states": ["neutral", "ok", "warn", "err", "acc", "solid"],
 "a11y": ["Uppercase micro-label; never the only signal - pair with text that says the same thing."]}}
```
Why + conclusion: Status badges use recorded states only (warn for Investigating, acc for Open,
ok for Mitigated, neutral for Resolved) and never carry the meaning alone.

### 27. ./run-authority inspect component/kv
```json
{"id": "component/kv", "body": {"class": "kv",
 "note": "A two-column metadata grid (label -> value) for detail panes and sidebars."}}
```
Why + conclusion: The case page's Details card is a .kv grid exactly as recorded for detail panes.

### 28. ./run-authority inspect component/tl
```json
{"id": "component/tl", "body": {"class": "tl",
 "states": ["default", "status-dots"],
 "verify": [".tl", ".tl-item", ".tl-dot.ok", ".tl-dot.err"],
 "a11y": ["Ordered list; dots are decorative (the text carries the meaning)."]}}
```
Why + conclusion: Timeline markup follows the recorded list structure (tl / tl-item / tl-dot /
tl-time / tl-t / tl-d); the sequence is an ordered list.

### 29. ./run-authority inspect component/logpanel
```json
{"id": "component/logpanel", "body": {"class": "logpanel",
 "note": "An ink terminal panel for logs and streamed output; rows colour by kind (green / amber / red / dim / time)."}}
```
Why + conclusion: Notes/activity entries use the recorded row anatomy (mono time, kind badge,
lmsg message) inside .logpanel.

### 30. ./run-authority inspect component/btn
```json
{"id": "component/btn", "body": {"class": "btn",
 "states": ["default", "hover", "active", "focus-visible", "disabled", "busy (guardApply)"],
 "a11y": ["Use a real <button> or <a>; never a clickable div.", "Icon-only buttons need aria-label."]}}
```
Why + conclusion: Actions are real elements (`a.btn`, `button.btn.primary`); no icon-only controls
exist in the build, so no aria-label debt.

### 31. ./run-authority inspect pattern/viewer
```json
{"id": "pattern/viewer", "kind": "pattern", "title": "Detail page",
 "summary": "Two-column detail: plain/HTML body and queue controls left, sticky metadata and audit right."}
```
Why + conclusion: Case page adopts the viewer pattern's two-column shape: timeline and notes in
the main column, sticky Details (kv) column on the side.

### 32. ./run-authority inspect component/nav-item
```json
{"id": "component/nav-item", "body": {"class": "nav-item",
 "states": ["default", "hover", "active(selected)", "focus-visible"],
 "a11y": ["aria-current=\"page\" on the active item.", "Active rail is border-inline-start (mirrors in RTL)."]}}
```
Why + conclusion: Sidebar entries adopt .nav-item with the active state; the recorded a11y rule
(aria-current on the active item) is applied on both pages. Also doubles as due diligence on the
command-11 misfire: the record is plainly a sidebar link, not a skip link.

### 33. ./run-authority gap-add --need "a row of filter chips that narrows a list by state" --scope "list views" --context '{"source":"docs/experiments/duty-build","ask":"a row of filter chips to narrow a list","outcome":"UNDEFINED","detail":"component/chip (13.0) tied component/index-row (13.0); a direct match needs a 2.0 lead. Canonical phrasing resolves to component/chip; the row carrier itself has no record.","built_with":"component/chip in core .row.chiprow"}'
```json
{"id": "gap/20261008-124813-d5c424", "need": "a row of filter chips that narrows a list by state",
 "scope_hint": "list views", "status": "open",
 "stored_at": ".../duty-build/.design-authority/gaps.jsonl"}
```
Why + conclusion: The first UNDEFINED (commands 5, 8) is reported properly: the chip itself is
sanctioned, the row carrier is not - the gap records the tie and what was built instead.

### 34. ./run-authority gap-add --need "an incident header that shows the record id, severity and current state above a detail view" --scope "detail views" --context '{"source":"docs/experiments/duty-build","ask":"an incident header with an id and current state","outcome":"UNDEFINED","detail":"closest candidates component/empty, component/page-head, component/page-state all scored 4.0, below the 6.5 threshold; retrieval top leg suggests page-head","built_with":"component/page-head + component/badge + component/dot"}'
```json
{"id": "gap/20261008-124813-366586", "need": "an incident header that shows the record id, severity and current state above a detail view",
 "scope_hint": "detail views", "status": "open",
 "stored_at": ".../duty-build/.design-authority/gaps.jsonl"}
```
Why + conclusion: The second UNDEFINED (commands 13, 14) is reported: composing page-head +
badge + dot satisfies the need, but the composite itself has no record.

### 35. ./run-authority gap-add --need "a skip link that jumps past the navigation to the main content" --scope "app shell / accessibility" --context '{"source":"docs/experiments/duty-build","ask":"a skip link to jump past the navigation","outcome":"RESOLVED (misfire)","detail":"resolved to component/nav-item (8.0) although a skip link is not a nav item; core/base.css ships a .skip class with no catalogue record","built_with":".skip anchor from core/base.css"}'
```json
{"id": "gap/20261008-124813-ac670b", "need": "a skip link that jumps past the navigation to the main content",
 "scope_hint": "app shell / accessibility", "status": "open",
 "stored_at": ".../duty-build/.design-authority/gaps.jsonl"}
```
Why + conclusion: The misfired resolve from command 11 is reported as a gap: skip links ride on
the shipped .skip class with no catalogue record, and the misfire is itself evidence.

### 36. ./run-authority validate index.html --json
```json
{"target": ".../duty-build/index.html",
 "validators": [{"validator": "triage-lint", "status": "ok", "exit": 0}],
 "summary": {"counts": {"error": 0, "warning": 0, "info": 0}, "total": 0,
             "score": {"value": 100, "gate": "Authority CI fails on any error; --max-warnings can tighten warnings."}},
 "meta": {"files_scanned": 1, "spec_score": 100, "spec_version": "0.12.1"}}
```
Why + conclusion: index.html is clean: 0 errors, 0 warnings, 0 info, spec score 100 against
Triage v0.12.1 - no fix pass was needed after the build.

### 37. ./run-authority validate case.html --json
```json
{"target": ".../duty-build/case.html",
 "validators": [{"validator": "triage-lint", "status": "ok", "exit": 0}],
 "summary": {"counts": {"error": 0, "warning": 0, "info": 0}, "total": 0,
             "score": {"value": 100}},
 "meta": {"files_scanned": 1, "spec_score": 100, "spec_version": "0.12.1"}}
```
Why + conclusion: case.html is clean: 0 errors, 0 warnings, 0 info, spec score 100 against
Triage v0.12.1 - both pages are conformant and the build is complete.
