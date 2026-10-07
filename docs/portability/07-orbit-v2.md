# Portability Spike · 07 · Orbit v2 — element re-derivation (anti-leak)

**Status:** green-lit by the reviewer (2026-10-07) after the v1 rejection
(`06-leak-audit.md`). Foundations carry over; the **element layer and layout
grammar are re-derived under anti-leak gates**. Mock screens await reviewer
sign-off (G2) before any agent run.

## Governing move

v1 leaked because the manual’s silence about controls was filled from
Triage-shaped priors (borders everywhere). v2 flips the manual’s own
prohibitions into the design law:

> “Avoid the use of borders or other types of artificial embellishment.”
> (p46) · “Outline boxes should be used around all technical diagrams.”
> (p41) · “Line spaces are to be used instead of paragraph indents.” (p21) ·
> “Keep the signs simple.” (p46)

**System law: no decorative borders anywhere.** Separation = rules, bands,
plates, spacing; boxes are reserved for technical figures; interaction
affordance = type (Plates for actions, underlines for links/commands).

## Newly mined source material (this revision)

| source | fact | use |
|---|---|---|
| p21 Typing Style | left typing margin; **line spaces instead of paragraph indents**; official sizes 10/11 + 7/8 Helvetica Light/Medium, upper & lower case | layout law (spacing, alignment), small typography (≈13px small / ≈15px large on screen) |
| p19–20 Letterheads | two-line identity grammar (name + descriptor), two standard color schemes | band identity (name + descriptor), inversion scheme |
| p24–26 Forms | the manual **declines to redesign forms** (“existing forms… redesign at a later date”) — form anatomy is out of its scope | field anatomy tagged INFERRED (paper-form rules + typing law), not claimed as observed |
| p41–44 (already held) | white band for folios/headlines, rules, caption-under-figure | masthead band, folio line, captions |

## Palette / tokens delta

- `--accent` re-authored `#E03C31 → #D63829` — **a11y revision**: white
  text on the plate surface now meets 4.5:1 (4.71:1); the old value failed at
  small sizes (4.32:1). Documented as a deliberate AUTHORED change.
- New: `--rule #D9D9D9` (print hairline rendered on screen), `--off #E6E6E6`
  (unfilled meter segments). Both AUTHORED renderings of print conventions.

## Element divergence table (G1 artifact)

| element | Triage anatomy (incumbent) | v1 (twin) | **v2 decision** | grounding | why not-Triage |
|---|---|---|---|---|---|
| `command` | `.btn` family: 1px border buttons; solid-ink primary; outline danger; wash hovers | border-button family | **plates + text commands**: primary = solid red plate; destructive = solid ink plate; all other actions = underlined text commands; hover = underline only (no washes) | red = action/ID (p8); regulatory/ID plates (p45–46); no borders (p46) | zero outlined buttons; zero hover washes; affordance via type, not boxes |
| `entry` | bordered input box, label above | bordered input | **ruled-line field**: label above, 1px ink base rule; focus = 2px base rule; error = red base rule + note | typing law p21; forms outside scope → INFERRED paper-form grammar | no boxes at all; fields are lines |
| `chooser` | bordered select | bordered select | ruled-line select (base rule only, native arrow) | same | same |
| `tag` | `.chip` bordered micro-label | bordered chip | **marked text**: 5px ink square + 12px text (classification mark) | publication list markers (INFERRED) | no chip box exists |
| `indicator` | colored dot + text | square marker + text | **status plates**: 12px word on solid tone plate (ink / gray-mid / red), white text; value-chosen per the 40% rule | painted markings, p47 value rule; p8 white-on-dark | status is a painted plate, not a dot |
| `register` | `.tbl` hairline rows (+ bordered stacked mobile cards) | hairline rows | **numbered register**: thick 2px header rule, index numerals column, hairlines as rules, caption BELOW the table; mobile = rule-separated stacked blocks (no cards) | publication tabulars p41–44; captions under figures; “large scale numerals” (p44) | numeral column + caption-under + no card boxes |
| `panel` | bordered `.card` | bordered panel | **figures only**: 1px box only around technical content, with caption “Figure n — …” beneath; ordinary content = sections + rules | p41 boxes-for-diagrams rule | boxes become meaningful (figures), not container chrome |
| `dialog` | white card: border, header rule, footer | same skeleton | **dark plate**: solid ink, white type, white plate for the final action, white underlined cancel; backdrop = ink 40% | white-on-dark rule p8; 40% value rule p47 | inverted, borderless, no header/footer chrome |
| `notice` | floating bordered toast w/ status edge | bordered block | **full-width sign bands**: info = ruled band; warning = ink band, white text; alert = red band, white text | signage zones p45–46; “announce, warn, restrict” classes | bands, not boxes: no radius, no stripe, no float |
| `gauge` | (none) | bordered track | **segmented block meter** (10 segments; ink or red fill on `--off`; mandatory “n of m” readout; inside a figure when standalone) | modular rectangles p41 (INFERRED) | segmented, not continuous |
| `band` | topbar/sidebar | generic appbar | **masthead**: two-line identity (name + descriptor, letterhead grammar), nav = underlined text commands (active = red underline), strong bottom rule; folio line at column bottom | letterhead p19–20; white band & folios p41 | no icon rail; type-only nav; folio |
| `section` | fieldset w/ border | heading + rule | **numbered section**: “1 · Item” Medium + hairline rule; line-spaces law | publication numbering (p44 numerals); p21 | numbering + rules as structure |

## Gates

- **G1 (this doc):** anatomy diff above; adversarial subagent review
  dispatched over mock CSS/HTML — verdict recorded before the agent run.
- **G2:** mock screenshots → reviewer sign-off. Pre-registered: on failure,
  swap source kit (NYCTA / EPA), no further iteration on NASA.
- **G3:** the no-border law + divergence table methodology added to the
  derivation skill.

Mock: `docs/portability/mock-v2/` (5 screens + mobile; renderer:
`mock-v2/render.py`; PNGs in `mock-v2/out/`).
