# leader · Semantic review (Gate 2)

Generated 2026-10-07 from `decisions.json` — **24 decisions**: 8 settled · 16 needing judgment · 0 open.

Legend — status: OBSERVED / INFERRED / AUTHORED / UNDEFINED. Review outcome (fill at Gate 2): ACCEPT / MODIFY / REJECT / LEAVE UNDEFINED.


## Settled (high-confidence — shown for context, no action needed)

### L-02 · shape · OBSERVED · confidence: high
**Decision:** Zero radius everywhere. Controls, cards, fields, dialogs are strict rectangles; the only shapes are rectangles, rules and glyph marks.

**Evidence:** rectangle motif native to the identity; no radius ever mentioned; crisp-lines language

**Reasoning:** The shape vocabulary is explicitly rectilinear across static and animated assets.

**Alternatives:** hairline-radius softening (rejected: unevidenced and against the crisp register)

### L-04 · typography · OBSERVED · confidence: high
**Decision:** Three registers by role: Serif = headlines and body text; Sans = navigation, metadata, datelines, captions; Sans Headline = display-only moments (page mastheads, big statics), used sparingly.

**Evidence:** Marber typography roles, verbatim

**Reasoning:** Directly documented roles.

**Alternatives:** none

### L-06 · colour · OBSERVED · confidence: high
**Decision:** Red #E3120B is punctuation: section labels, active nav underline, single solid blocks, emphasis rules, primary controls. Everything else is ink (#1A1A1A/#333), white, or the London grey ramp. City palettes stay in reserve (data/sections only; not core chrome).

**Evidence:** Marber colour tokens; 'red thread' theme; red retained through refreshes

**Reasoning:** Token-level evidence.

**Alternatives:** red as large background fields (reserved for very few moments only)

### L-07 · surfaces · INFERRED · confidence: high
**Decision:** White ground; section separation via 2px ink rules, hairlines (London 85), and red-95/grey-95 canvas washes. No shadows, no elevation, no soft chrome.

**Evidence:** crisp lines/typing cursors/search bars language; no shadow evidence anywhere

**Reasoning:** The surface discipline is flat and ruled.

**Alternatives:** subtle card elevation (rejected: unevidenced)

### L-09 · hierarchy · OBSERVED · confidence: high
**Decision:** Section label (sans caps, red) → serif headline → one-line standfirst (muted serif). Repeats strictly; no decorative sub-heads.

**Evidence:** homepage module pattern; standfirst cadence

**Reasoning:** Recurring observed unit.

**Alternatives:** none

### L-20 · voice · OBSERVED · confidence: high
**Decision:** Terse, declarative, fact-forward; dry wit allowed in one clause, never exclamatory; headline + one-line standfirst cadence in UI copy too.

**Evidence:** standfirst samples; 'sharp writing style' named as identity

**Reasoning:** Quoted register.

**Alternatives:** none

### L-21 · imagery · OBSERVED · confidence: high
**Decision:** No imagery in the reference build. Blur→focus is a documented device but belongs to story layouts; absence here is honest, not a gap.

**Evidence:** imagery described as purposeful/story-bound

**Reasoning:** Scoped to what a data register needs.

**Alternatives:** decorative imagery (rejected)

### L-24 · prohibitions · INFERRED · confidence: high
**Decision:** Never: rounded corners; soft shadows; pills; decorative colour; red as large background for reading content; invented hues; emoji; exclamation marks.

**Evidence:** absences across all fetched material + stated 'less is more' principles

**Reasoning:** Codifies what the system never does.

**Alternatives:** none


## Needing judgment (authored or low-confidence)

### L-01 · actions · AUTHORED · confidence: medium
**Decision:** Primary action = solid Economist Red #E3120B rectangle with white label; secondary = 2px ink outline rectangle; tertiary = underlined text link. Labels sentence-case, sans, 14/500.

**Evidence:** red block + white text observed (covers/logo contexts); no live buttons observable (site blocked)

**Reasoning:** Red is punctuation; a solid red control is the strongest on-brand expression of a primary action without inventing shapes.

**Alternatives:** ink-fill primary with red only as accent; underlined red text-actions

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-03 · events · AUTHORED · confidence: medium
**Decision:** Interaction transitions are near-instant (≤0.15s colour swaps); no bounce, spring or decorative movement in UI chrome. Motion stays native to brand assets, not interface controls.

**Evidence:** motion is identity-native (animated rectangles) but UI timings are UNDEFINED

**Reasoning:** 'Less is more' + restraint suggest crisp swaps; springs would contradict the register.

**Alternatives:** subtle 0.2s fades; hold everything instant

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-05 · typography · AUTHORED · confidence: medium
**Decision:** Screen rhythm: serif headline 30–34/1.15; standfirst sans? no — serif standfirst 16–17 muted; body serif 17/1.55; metadata sans 12.5–13 with 0.06em caps for section labels; display 44 at tracking −1.

**Evidence:** cadence observed (headline + one-line dek); numeric scale UNDEFINED in sources

**Reasoning:** Plain editorial rhythm; values kept modest to avoid inventing a scale with false precision.

**Alternatives:** larger display scale; all-sans metadata weight games

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-08 · motifs · AUTHORED · confidence: medium
**Decision:** The red thread appears as a hairline red rule device (headers/footers/section breaks) — a connective mark, never a border for content blocks. Rhythm glyphs (small black squares of graded size) may punctuate list ends or step markers.

**Evidence:** red thread named as connective theme; glyphs 'reborn as a visual language' (rhythm, emphasis)

**Reasoning:** Direct application of the two documented motifs to interface chrome, kept minimal.

**Alternatives:** rule-only (no glyphs); glyphs in body copy (rejected)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-10 · navigation · INFERRED · confidence: medium
**Decision:** Top bar: white, 2px ink bottom rule; wordless-brand zone left (name in serif), nav links sans 13/500, active = red underline; a crisp search rectangle with a static typing-cursor motif at the right.

**Evidence:** nav + search bar + typing cursor all named in identity coverage; live layout unobservable

**Reasoning:** Composes documented cues; search is a signature cue of the identity.

**Alternatives:** no search in reference app

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-11 · forms · AUTHORED · confidence: low
**Decision:** Fields: white, 2px ink border, square, label above in sans caps 11; focus = 2px ink border plus a 1px offset outer ink line; error message set small in red beneath the field.

**Evidence:** no form evidence; register derived

**Reasoning:** Squared-off bureaucratic honesty; keeps red for emphasis only.

**Alternatives:** red focus border; background tint on focus

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-12 · selection · AUTHORED · confidence: low
**Decision:** Small sets (≤ ~12) = native select squared like a field. Larger/filtered = out of scope; platform fallback, marked.

**Evidence:** none captured

**Reasoning:** Same honesty rule as elsewhere: no invented combobox.

**Alternatives:** invent a searchable listbox (rejected)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-13 · status · AUTHORED · confidence: medium
**Decision:** Status = rectangular ink-outline tag, word inside (uppercase sans 11, 0.06em). Attention states turn the tag solid red with white word. No pills, no dots as sole signal.

**Evidence:** no status component observed; rectangle + caps languages observed

**Reasoning:** Rectangular tags extend the geometry; red-for-attention matches red-as-punctuation.

**Alternatives:** text-only status; coloured left rules

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-14 · feedback · AUTHORED · confidence: medium
**Decision:** Notices = ruled boxes (2px ink top or left rule) with terse declarative copy; no toasts (none evidenced); problem copy names the fact and the next step.

**Evidence:** no feedback observed; declarative voice observed

**Reasoning:** Ruled box is the natural vessel of a ruled system.

**Alternatives:** tinted wash box; floating banner

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-15 · destructive · AUTHORED · confidence: medium
**Decision:** Destructive flows confirm in a square dialog: 2px ink frame, consequence sentence (terse, no euphemism), confirm = solid red rectangle labelled with the verb, cancel = outline rectangle. Destructive is never pre-focused.

**Evidence:** no destructive pattern; register derived

**Reasoning:** Seriousness via plain statement + solid red verb button.

**Alternatives:** ink-black confirm (considered); two-step inline reveal

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-16 · progress · AUTHORED · confidence: medium
**Decision:** Progress = crisp rectangle track (London 85) with red fill; readout as sans metadata ('7 of 10 steps'); restart = outline rectangle. Static updates only.

**Evidence:** no meter observed; rectangle/grey/red primitives attested

**Reasoning:** Composes attested primitives; animation stays out of UI.

**Alternatives:** striped fill; percentage-only

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-17 · empty · AUTHORED · confidence: medium
**Decision:** Empty state = ruled statement block with one action (outline or red rectangle); no illustration.

**Evidence:** no imagery needed per 'purposeful imagery' rule; register derived

**Reasoning:** Imagery is purposeful; an empty list has no story to illustrate.

**Alternatives:** photographic hero (rejected)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-18 · repeated-content · INFERRED · confidence: medium
**Decision:** Ledger = editorial table: 2px ink header rule over sans-caps labels, hairline row rules (London 85), serif names, sans numbers; row hover = red-95 wash; no zebra; right-aligned numeric column feel.

**Evidence:** editorial rules + type registers; comparison-table structure implied by register

**Reasoning:** Table as newspaper furniture: rules do the separating.

**Alternatives:** bordered box grid; zebra rows

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-19 · overlays · AUTHORED · confidence: medium
**Decision:** Dialog = square white sheet with 2px ink frame; scrim = ink at 62%; instant appearance; no entrance motion.

**Evidence:** no dialog studied; flat ruled language attested

**Reasoning:** Consistent with flat surfaces + instant transitions (L-03).

**Alternatives:** slide/fade (rejected: motion undefined)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-22 · responsive · AUTHORED · confidence: low
**Decision:** Single-column collapse; display scale steps down (44→34); table becomes stacked rows with sans labels; nav collapses to a text row. Minimal, honest.

**Evidence:** no responsive evidence (live site blocked)

**Reasoning:** Least-invention collapse.

**Alternatives:** full responsive canon (rejected)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### L-23 · focus · AUTHORED · confidence: low
**Decision:** Focus ring = 2px red outline offset 2px on white; on red fills, switch to white inner + ink outer ring.

**Evidence:** none captured

**Reasoning:** Red punctuation makes focus legible; switch rule mirrors contrast logic.

**Alternatives:** ink-only double ring

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED


## Open (genuinely undefined — may remain so)

_None._
