# Census rubric — classifying the project's established conventions

Used by the standalone census session (first application) and mirrored by the
deterministic checkpoint census on the development chains. Everything here is
frozen: classes, dimensions, pass rules, and schemas. Classifications are
made from frozen evidence only, timestamped, and never re-chosen once later
results exist.

## The six roles

| role | what it covers |
|---|---|
| `primary-action` | the main affirmative action of a surface (add / save / apply) |
| `destructive` | the confirmation pattern guarding a destructive action |
| `empty-state` | the treatment when there is no content (first run, no matches, cleared) |
| `form-validation` | how forms signal and recover from invalid input |
| `tags-status` | the chip/label vocabulary for tags and statuses |
| `surfaces` | card / panel / bar treatments — radius, borders, shadows, elevation |

Recorded opportunities (from the frozen opportunity matrix):

- `primary-action`: F1 add bookmark · F2 bulk apply action · F3 save in edit flow
- `destructive`: F2 bulk delete confirmation · F3 single delete confirmation
- `empty-state`: F1 first-run empty list · F2 no filter matches · F3 collection empty after cleanup
- `form-validation`: F2 add-bookmark form · F3 edit form
- `tags-status`: F2 tag filter chips · F3 tag editing
- `surfaces`: F1 bookmark cards · F2 bulk-selection surfaces · F3 edit panel

## Classes

| classification | operational meaning |
|---|---|
| **Established** | Repeated compatible use across at least two distinct opportunities, supported by a traceable record |
| **Observed once** | One clear implementation, insufficient evidence of stability |
| **Inconsistent** | Multiple incompatible treatments without a documented exception |
| **Absent** | No usable evidence of a convention |

"Compatible" is decided with the pass rules below applied instance-to-instance
(and, when an exemplar already exists, against the exemplar). "Traceable
record" means a record in `.design-authority/` (a gap, proposal, or decision
log entry) that covers the decision — the record does not have to match the
implementation exactly, but it must show the decision was made deliberately.

## Dimension pass rules (frozen)

Visual dimensions — pass when:

- **palette**: the same colour role and a value within CIELAB ΔE2000 ≤ 5 (computed from sRGB)
- **radius**: absolute difference ≤ 2 px, or both are pill class (≥ 999 px)
- **typography**: same recorded role (display/heading/body) and same generic family class (sans/serif/mono)
- **spacing rhythm**: matched pairs within ±20%, ordering of scale steps preserved
- **border & treatment**: same category — `none` / `hairline` / `strong` / `shadow`

Behavioral dimensions — discrete categories, pass only on the same category:

| dimension | categories |
|---|---|
| trigger placement (destructive) | row action / toolbar / menu |
| confirmation pattern | dialog / inline / undo |
| destructive emphasis | colour emphasis / outline / neutral with copy |
| cancel-first default | cancel focused / confirm focused |
| post-action feedback | message / undo affordance / none |
| validation timing | on submit / on blur / live |
| error placement | inline field / summary / toast |
| message treatment | colour plus icon / text only / plain |
| invalid-field signaling | border / colour / icon |
| recovery affordance | auto-clear / manual / none |

Inapplicable dimensions are frozen per exemplar (say why) and removed from
both sides of any comparison.

## Output schemas (exact)

`census.json`:

```json
{
 "roles": {
  "<role>": {
   "classification": "Established | Observed once | Inconsistent | Absent",
   "opportunities": [
    {"where": "<screen/state>", "session": "<f1|f2|f3>", "evidence": "<file, screenshot, or record id>"}
   ],
   "record": "<record id, or null>",
   "notes": "<short justification>"
  }
 },
 "established": ["<role>", "..."],
 "K_established": 0,
 "classifier": "standalone census session, evidence-only",
 "completed": "<ISO-8601 UTC>"
}
```

`exemplars.json`:

```json
{
 "exemplars": {
  "<role>": {
   "source_session": "<f1|f2|f3>",
   "testid": "<data-testid of the exemplar element, or a file/selector description>",
   "state": "<screenshot state: empty | populated | filtered | invalid | confirm | ...>",
   "measured": {"<dimension>": "<value or category>"},
   "dimension_signature": {
    "palette_bg": "<rgb(...)>|null",
    "palette_fg": "<rgb(...)>",
    "radius": "<px or pill>",
    "font_class": "sans | serif | mono",
    "border": "none | hairline | strong | shadow",
    "padding": ["<px>", "..."],
    "behavior": {"<dimension>": "<category>"}
   },
   "notes": "<what makes this the exemplar>"
  }
 },
 "frozen": "<ISO-8601 UTC>"
}
```

For each Established role freeze the latest instance (the session-3 instance
where the role appears in session 3, otherwise the latest one), with both the
raw measured values and the normalized `dimension_signature`. If a dimension
is inapplicable for an exemplar, record `"n/a"` and a one-line reason in
`notes`; that dimension is then excluded from comparisons against it.
