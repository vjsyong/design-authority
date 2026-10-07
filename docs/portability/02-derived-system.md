# Portability Spike · 02 · Derived system — “Orbit”

**Parts:** A · Foundations (§1–7, below) · B · Core UI elements (§8) · C · Compositions (§9).
Every decision carries a ledger status per the spike protocol §Phase 2:
OBSERVED · INFERRED · AUTHORED · UNDEFINED.

*Working name; carries no NASA marks.* Derived from the NASA Graphics Standards
Manual (NHB 1430.2, January 1976), public domain, verified live at
`nasa.gov/.../nasa_graphics_manual_nhb_1430-2_jan_1976.pdf`.*

**Ledger legend (per the portability spike brief):**
`OBSERVED` = stated in the source (page-cited) · `INFERRED` = derived from
source logic, not stated · `AUTHORED` = new interface-level decision with no
source basis · `UNDEFINED` = deliberately left open (tests the kernel’s
UNDEFINED path).

---

## 1 · Color roles

| # | decision | value | status | evidence / rationale |
|---|---|---|---|---|
| C1 | Primary accent | “NASA red” — a **warm red** | OBSERVED | p8–9: logotype color rules; p9 Color Standards: “the formula for NASA red is solid red plus solid yellow” (4-color process) |
| C2 | Accent hex for screens | `--accent: #E03C31` | AUTHORED | print formula has no screen value; the classic “warm red” printing ink is the closest documented match; flagged revisable |
| C3 | Neutral pair | **Solid black** / **solid white** | OBSERVED | p8, p10: “always be shown in solid black… or solid NASA red”; solid white on dark |
| C4 | Secondary neutral | **NASA warm gray** (middle-value gray) | OBSERVED | p8: logotype may appear in warm gray on white; publications: “NASA gray or another middle value gray… as a second color for duo tones” |
| C5 | Warm gray hex | `--gray-mid: #6F6F6F` | AUTHORED | screen rendering of “middle value gray” |
| C6 | Ink / paper | `--ink: #101010`, `--paper: #FFFFFF` | INFERRED | screen rendering of “solid black/white” (pure print black is impractical on displays) |
| C7 | Accent role in UI | actions + identification accents only, **never a reading surface** | INFERRED | p8 rules: red is allowed on white/very-light backgrounds and on nothing else; “never… against a medium-value background”; “never… against a background of NASA red” |
| C8 | Contrast-value policy | explicit **value threshold** governs black/white switching (40% gray-scale value) | OBSERVED | p47: vehicle identification flips black↔white at the “40% value on a gray scale” — a documented contrast rule |
| C9 | Extended color coding | **deferred** | UNDEFINED | publications allow “a range of bright, primary and secondary colors… to aid in the presentation of information,” but specify none; the derived system ships single-accent and defers multi-color coding (candidate for a governed extension later) |
| C10 | Pastels | excluded | OBSERVED | publications: “The use of pale, pastel colors is discouraged in all NASA publications.” |

**Roles shipped:** `paper` (background), `ink` (text), `gray-mid` (secondary
text/rules), `accent` (actions/identification), `accent-ink` (white-on-red),
plus a `surface-dark` (= ink) for inverted regions per C3/C8.

## 2 · Typography roles

| # | decision | value | status | evidence |
|---|---|---|---|---|
| T1 | Family | **Helvetica** is the keystone; Light for text, Medium for headings, Bold as occasional alternative | OBSERVED | p27–30: “Helvetica is the most important family of type…”; headings “set in Helvetica Medium”; “Headings are set in upper and lower case” |
| T2 | Screen implementation | system stack beginning `“Helvetica Neue”, Helvetica, Arial` with free fallbacks | INFERRED | licensed face cannot ship; metric-compatible stack preserves the observed letterforms’ register |
| T3 | Setting | **flush left, ragged right**; normal (never tight) letterspacing; no justified text | OBSERVED | p30: “flush left, ragged right column setting… minimum one-point line spacing”; p46 signage: “‘normal’ rather than ‘tight’ letterspacing” |
| T4 | Base size / leading | screen `15px / 21px` (≈ the manual’s 10pt-on-14pt setting, ratio 1.4) | AUTHORED | anchored on observed 10/14 (p27) and “minimum one-point line spacing” (p30) |
| T5 | Scale | 5 steps: `24 / 18 / 15 / 13 / 12` medium-weights at headings, light/regular for body | AUTHORED | screen adaptation; heading = Medium per T1 |
| T6 | Serif voice | reserved for long-form/editorial surfaces (Garamond-register); not used in controls | INFERRED | p29–30: Garamond for “high quality publications”; Times for “news-oriented” — roles that map to content surfaces, not UI chrome |
| T7 | Case policy | sentence/upper-lower case; no all-caps strings (signage caps are physical-format specific) | INFERRED | T1 headings upper+lower; caps observed only on signage/vehicles where legibility demands it |

## 3 · Spacing, layout, and density

| # | decision | value | status | evidence |
|---|---|---|---|---|
| S1 | Spatial unit | **modular rectangles**: layouts are built from equal subdivisions (observed 6-rectangle page; 2–3 column systems) | OBSERVED | p41: “Single page has been divided into 6 equal rectangles”; p41–44: two/three-column format families |
| S2 | Screen base unit | `4px` unit; scale `4 · 8 · 12 · 16 · 24 · 32 · 48` | AUTHORED | smallest screen translation of the modular logic |
| S3 | Header band | a **white band** at the top carries identity/status (“folios and an occasional important headline”) | OBSERVED | p41; maps to the app’s status/identity bar |
| S4 | Separation | **rules** (1px hairlines in ink/gray) separate regions; no decorative dividers | OBSERVED | p41: “Rules are employed to separate articles”; p46: “Avoid the use of borders or other types of artificial embellishment” |
| S5 | Boxes | outline boxes are **reserved for technical content** (figures/diagrams), never decorative | OBSERVED | p41: “Outline boxes should be used around all technical diagrams” |
| S6 | Alignment | headings and text align to the top of their field; captions sit under figures, left-aligned | OBSERVED | p41: “Top alignment of headings and text”; “Captions are positioned under photographs” |
| S7 | Measure | ragged-right text blocks capped ≈66ch; wide margins preferred over dense edge-to-edge text | INFERRED | p44: “wide margins” formats; flush-left setting |
| S8 | Density | compact middle: 15/21 body, 12–16px control heights scaled to the 4px unit | AUTHORED | screen translation |

## 4 · Form, border, radius, elevation

| # | decision | value | status | evidence |
|---|---|---|---|---|
| F1 | Corner radius | **0** (square everywhere) | INFERRED | the entire source system is rectilinear; no rounded form appears in any application. (Triage independently prohibits radius — this derivation arrives at square-ness from its own evidence, which the portability comparison will note.) |
| F2 | Borders | 1px solid ink or gray-mid; weight never decorative | OBSERVED/INFERRED | S4/S5 rules; signage: no ornament |
| F3 | Elevation / shadow | **none**; layering via inversion (black bands) and rules only | INFERRED | print medium has no elevation; “simple, functional, contemporary” (p45) |
| F4 | Inversion | dark regions are solid ink with white text (observed header/vehicle schemes) | OBSERVED | p8 dark-background rule; p47 vehicle schemes |

## 5 · Responsive assumptions

| # | decision | value | status | evidence |
|---|---|---|---|---|
| R1 | Breakpoints | single column < 720px; two columns ≥ 720px; content max-width 1080px | AUTHORED | the manual is format-fixed (print); interface responsiveness has no source basis |
| R2 | Degradation | the white header band and rules persist at all widths; columns collapse to one; the 4px unit is preserved | AUTHORED | consistent with S1–S3 |

## 6 · Motion

| # | decision | value | status | evidence |
|---|---|---|---|---|
| M1 | Motion | **left UNDEFINED by design** | UNDEFINED | the source predates interface motion and specifies none. The derived system ships no transitions; anything the test app genuinely needs will be filed as a **gap** through the authority’s own protocol — a deliberate exercise of the UNDEFINED path. |
| M2 | Interaction feedback | instant state change (color/inversion) only | INFERRED | source feedback is physical (paint, signage), not temporal |

## 7 · Iconography note (minimal)

| # | decision | value | status | evidence |
|---|---|---|---|---|
| I1 | Symbols | prefer standard symbol signs (DOT library) over bespoke icons; arrows for direction | OBSERVED | p45: “‘P’ is from D.O.T. Symbol/Signs library”; p46: “DOT Symbol/Signs employed rather than unnecessary words” |
| I2 | Icon rendering | flat, single-color, inherits text color; no outlines beyond the letterform register | INFERRED | source usage of solid marks only |

## 8 · Core UI elements (12)

Orbit's own vocabulary — deliberately not Triage's codes (`btn`, `tbl`, `dlg`
…). Each element below: purpose · anatomy · states · rules with provenance ·
ledger status.

### 8.1 `command` — action control
- **Purpose:** trigger an action. Variants `primary` (solid accent, white
  text, allowed only on paper per C7), `secondary` (paper bg, 1px ink border),
  `destructive` (paper bg, 1px accent border + accent text — reserved).
- **States:** hover (border emphasis only — no motion, M1), focus (2px ink
  outline, offset 1px; white on inverted regions), active (inverted: ink bg /
  paper text), disabled (gray-mid text + border). `busy` is **UNDEFINED**.
- **Ledger:** primary/secondary INFERRED (accent-as-action, C7; rectilinear
  form, F1); destructive AUTHORED (no source semantics — flagged for the
  probe); focus treatment AUTHORED (accessibility, no source basis).
- **Provenance:** p8 color-use rules; p45 “simple, functional”.

### 8.2 `entry` — single-line text field
- **Anatomy:** `label` above (sentence case, Medium 13) + `input` + `error`
  line below (accent text, concise message).
- **States:** default (1px ink border), focus (same ring as 8.1), invalid
  (accent border + error line), disabled, readonly.
- **Ledger:** label/error placement INFERRED (top-alignment §S6; signage
  brevity p45–46); aria wiring AUTHORED (no source basis).
- **Provenance:** p30 typographic style; p45 “language clear and concise”.

### 8.3 `chooser` — small-set single select
- **Anatomy:** labelled native `<select>`; small fixed sets only (≈ ≤12
  options). Larger or filtered selection is deliberately **out of scope** —
  the app must file a gap if it needs one (an intentional probe surface).
- **States:** default, focus, invalid, disabled.
- **Ledger:** INFERRED (form language from §4 forms + rectilinear base);
  the size limit and the out-of-scope rule AUTHORED.

### 8.4 `panel` — bordered technical region
- **Anatomy:** `panel` (1px ink border) + optional title (Medium, top
  aligned) + body; optional footer row above a rule.
- **Rule:** boxes are reserved for technical/diagrammatic content (S5) —
  ordinary prose lives in `section` regions separated by rules, not boxes.
- **Ledger:** OBSERVED basis (S5, “outline boxes … around all technical
  diagrams”), INFERRED as the UI analogue.
- **Provenance:** p41.

### 8.5 `band` — identity, navigation, status
- **Anatomy:** full-width white band (S3), 1px ink bottom rule; left:
  identity placeholder (no NASA marks); center/right: nav links (Medium
  text); current item = 2px accent underline; far right: environment/status
  text (gray-mid). Variant `band--inverted` (ink bg, white text, F4).
- **Ledger:** band OBSERVED (S3, folios/headline band); nav semantics
  AUTHORED (publication/signage systems have no nav component); inverted
  variant INFERRED (observed dark/white inversions p8, p47).

### 8.6 `register` — ruled data list
- **Anatomy:** header row (Medium 12, upper-lower, top aligned) + rows
  separated by 1px gray-mid hairlines; cells top-aligned (S6); actions sit
  right as text `command`s; optional outer border only when the table is
  “technical content” (S5). No zebra striping, no elevation.
- **States:** default; empty → replaced by `notice` standby pattern (§9.2).
- **Ledger:** INFERRED (rules-over-decoration S4; top alignment S6; compact
  print tabular register tradition).
- **Provenance:** p41–44 formats; p46 signage clarity.

### 8.7 `indicator` — status marker
- **Anatomy:** 6×6px **square** marker + text label; tones: `neutral`
  (gray-mid), `ok` (ink), `alert` (accent). Status is always readable as
  text; the marker never carries meaning alone.
- **Ledger:** marker+text INFERRED (C7 accent discipline; “message formats”
  p46); tone semantics AUTHORED (source has no status model — flagged for
  the probe).

### 8.8 `tag` — square micro-label
- **Anatomy:** 1px gray-mid border, square, 11–12px Medium text, padding
  4×8; grouped tags separated by 8 (patches occupy “their own visual space”,
  non-competing, p12 — INFERRED analogue).
- **Ledger:** INFERRED.

### 8.9 `gauge` — determinate progress
- **Anatomy:** track (paper, 1px gray-mid border, 8–10px tall) + fill
  (ink; `alert` fill in accent for failed/attention) + mandatory text
  readout (“n of m”) beside or beneath. Updates are static; **no
  animation** (M1).
- **Ledger:** AUTHORED (no source basis — the largest consciously authored
  element; flagged in the probe set).

### 8.10 `notice` — inline feedback
- **Anatomy:** square block, 1px border, kind variant: `info` (gray-mid
  border, ink text), `warning` (ink border + ink heading), `alert` (accent
  border + accent heading); concise sentence copy; top-aligned at the head
  of its region.
- **Ledger:** INFERRED from signage classes (informational / warning /
  regulatory, p45–46) + “clear and concise” language; exact UI mapping
  AUTHORED.
- **Provenance:** p45–46.

### 8.11 `section` — form and content grouping
- **Anatomy:** heading (Medium) + 1px ink rule + stacked `entry`s or
  content; form column max-width 560px (S7 wide-margin logic); top-aligned.
- **Ledger:** INFERRED (publication format logic: bands, rules, columns).

### 8.12 `dialog` — modal confirm / editor
- **Anatomy:** square panel, 1px ink border, ink band header (title +
  `Close` text command), body, footer commands right-aligned; page overlay
  = ink at **40%** opacity (the documented value threshold, C8, reused).
  Destructive confirms state the object and consequence in the sentence.
  No shadow, no motion — appears/disappears instantly.
- **States:** open / closed (no animation); focus trapped inside (AUTHORED).
- **Ledger:** structure **AUTHORED** (source has no dialogs anywhere);
  overlay value INFERRED from C8; sentence rule INFERRED from signage
  clarity. Flagged for the probe set.

## 9 · Compositions (4)

### 9.1 `shell` — application shell
Band (§8.5) + main region (max-width 1080, padding 24/32 per S2) + footer
folio line (“Orbit · <section>”, 12px gray-mid — folios from the white-band
role, p41). **Ledger:** band/folios OBSERVED basis; assembly INFERRED.

### 9.2 `register-view` — list screen
Shell + page head (h1 Medium + primary `command` right-aligned) + `register`
+ empty variant: centered `notice` “standby” block with one secondary
command. **Ledger:** assembly INFERRED; empty-state copy AUTHORED.

### 9.3 `form-flow` — create / edit
Shell + `section`s of `entry`/`chooser` + validation `notice`s above fields
+ footer row: primary submit, secondary cancel; destructive variant routes
through `dialog` (§8.12) naming object + consequence. **Ledger:** assembly
INFERRED; destructive-flow semantics AUTHORED (probe target).

### 9.4 `job-view` — status console
Shell + `indicator` + `gauge` + log `register` (time + message rows).
**Ledger:** AUTHORED (no source analogue); inherits element rules above.

## 10 · Bridging notes for Phase 3 (encoding)

- **Candidate rules:** ORB-1 radius always 0 (F1); ORB-2 accent never a
  reading surface and never alone (C7/C8); ORB-3 no shadows/elevation (F3);
  ORB-4 status always text + marker (8.7).
- **Candidate prohibitions:** rounded forms; drop shadows; pastel colors
  (C10).
- **Carried UNDEFINEDs (intentional):** motion (M1); busy states (8.1);
  searchable selection (8.3); multi-color data coding (C9). The test app is
  expected to touch at least two of these — gaps over guesses.
- **Naming:** element ids will be `component/command`, `component/entry`, …
  under a fully separate authority identity (no Triage inheritance).

---

**Next:** Phase 3 — encode as the Orbit Authority Pack (`packs/orbit/`) in
the existing pack format; kernel stays untouched except via
`docs/portability/03-kernel-change-ledger.md`.
