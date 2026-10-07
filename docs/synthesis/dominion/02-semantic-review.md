# dominion · Semantic review (Gate 2)

Generated 2026-10-07 from `decisions.json` — **22 decisions**: 5 settled · 17 needing judgment · 0 open.

Legend — status: OBSERVED / INFERRED / AUTHORED / UNDEFINED. Review outcome (fill at Gate 2): ACCEPT / MODIFY / REJECT / LEAVE UNDEFINED.


## Settled (high-confidence — shown for context, no action needed)

### D-02 · shape · OBSERVED · confidence: high
**Decision:** Zero radius anywhere. No shadows. Structure carried by rules: 2px black section rules, 1px pewter hairlines for tables. Everything rectilinear.

**Evidence:** all figures rectilinear; no corner/shadow language anywhere in the standard

**Reasoning:** Absence is itself the evidence; the standard defines a ruled, measured world.

**Alternatives:** hairline soft rules (rejected)

### D-03 · typography · OBSERVED · confidence: high
**Decision:** One family (Helvetica-class stand-in: Arimo), weights as roles: Light = quiet formal accents, Regular = default text, Medium = headings and key labels (web role per the standard), Bold = reserved for signage-style emphasis (rare).

**Evidence:** weight→use mapping quoted from the standard; website rule (medium for identity zone)

**Reasoning:** Direct mapping from the standard, extended conservatively to screens.

**Alternatives:** none

### D-07 · hierarchy · OBSERVED · confidence: high
**Decision:** Task-first order (most important first), titles short (2–4 words principle extended to screens), structure over decoration; reading order explicit in markup.

**Evidence:** content style guide: intuitive/targeted/consistent; applied-title limits; plain language mandate

**Reasoning:** Quoted requirements applied to interface structure.

**Alternatives:** none

### D-19 · voice · OBSERVED · confidence: high
**Decision:** Plain, non-bureaucratic, task-first; gender-inclusive by default; no jargon, no sloganising; French rendered with equal care (never machine-dumped).

**Evidence:** plain-language mandate + style guide principles quoted

**Reasoning:** Directly mandated and quoted.

**Alternatives:** none

### D-22 · prohibitions · INFERRED · confidence: high
**Decision:** Never: corner radii; shadows; decorative colour; red for status/errors/decoration; imagery; pictograms (undefined in source); slogan-style headings; playful shapes; Crown marks reproduced.

**Evidence:** stated absences + legal protection posture

**Reasoning:** Codifies the closed grammar.

**Alternatives:** none


## Needing judgment (authored or low-confidence)

### D-01 · actions · AUTHORED · confidence: medium
**Decision:** Primary action = solid FIP red (#EB2D37) square button, white regular-weight label; secondary = 2px black outline square; tertiary = underlined black text link. One primary per view; red is ceremony, so it is used sparingly even for actions.

**Evidence:** rectilinear standard + red-as-ceremony role; no UI controls exist in the standard

**Reasoning:** Squares from the standard's geometry; red for the single ceremonial action keeps 'one red' discipline visible.

**Alternatives:** black-fill primary with red reserved for identity only (still live option)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-04 · typography · AUTHORED · confidence: medium
**Decision:** Screen rhythm (AUTHORED interpretation, no sizes exist in source): page title 32/400; section headings 20/500; body 16/1.6; metadata 13 grey; bilingual pairings same size both languages.

**Evidence:** sizes UNDEFINED in the standard; rhythm authored to a plain, generous reading

**Reasoning:** Declared interpretation; equality rule honored (both languages equal size/weight).

**Alternatives:** larger official-document scale

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-05 · colour · AUTHORED · confidence: medium
**Decision:** FIP red strictly for ceremony: masthead accent device, the single primary action, identity zone marks. Black = text/structure; white = ground; pewter = de-emphasis (metadata, secondary labels). Status and errors are NOT colour-coded (see D-10).

**Evidence:** standard restricts red to flag/identity; pewter reserved to ministerial arms there — we extend it to de-emphasis

**Reasoning:** Keeps the one-red discipline; avoids importing alarm semantics the source never had.

**Alternatives:** pewter for all secondary text; red also for errors (rejected: alarm semantics are unevidenced and collide with other systems' conventions)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-06 · surfaces · AUTHORED · confidence: medium
**Decision:** White ground; #F4F4F4 grey band for section separation; black 2px rules as structural events; no elevation anywhere.

**Evidence:** white/black standard colourways; bands authored as the plainest separator

**Reasoning:** Ruled, flat, formal.

**Alternatives:** rules only (no bands)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-08 · navigation · AUTHORED · confidence: medium
**Decision:** Top bar: white, black bottom rule, identity zone at left (red accent bar + title — generic, no Crown marks), nav links regular with medium active state underlined in black (not red — red stays ceremonial). Footer: bottom-right zone reserved for the system's wordmark placeholder (plain text).

**Evidence:** website bookends rule (signature TL header / wordmark BR footer) applied with generic placeholders

**Reasoning:** Bookends are observed doctrine; substitution of marks with placeholders is our policy.

**Alternatives:** red active underline (rejected: ceremony spill)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-09 · bilingual · AUTHORED · confidence: medium
**Decision:** The signature structural device: primary page titles and key labels render bilingually (English | French, side-by-side, thin divider; over-under when narrow). Body content stays in the app's own language. Where a string exists in one language only, no signposting line is fabricated (that rule governs official publications, not this derived app) — carried as system nuance.

**Evidence:** side-by-side bilingual + over-under fallback are core observed rules; scope intensity is our choice

**Reasoning:** This is the system's most structural trait; applying it at title/label level expresses identity without breaking app usability.

**Alternatives:** bilingual everywhere; bilingual nowhere (both rejected)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-10 · status · AUTHORED · confidence: medium
**Decision:** Status is word-first, never colour-coded: plain text labels in a ruled box — 'Available' (black on white), 'On loan' (black on #F4F4F4), 'Overdue' (black text with 2px black left rule — emphasis by structure, not hue). Words carry meaning; structure carries emphasis.

**Evidence:** no status semantics in the standard; safety red explicitly signage-only

**Reasoning:** Deliberately inverts the usual colour-coded status convention; keeps red pure and prevents Triage-style red-state reading.

**Alternatives:** red for overdue (rejected for ceremony purity and collision risk)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-11 · forms · AUTHORED · confidence: medium
**Decision:** Fields: square, 1.5px black border, label above (medium, 13), helper text pewter; focus = border thickens to 2px + offset outer 1px black line; error = 2px black left rule on a grey field + plain-language sentence under it.

**Evidence:** no form evidence; ruled/measured register extended

**Reasoning:** High-contrast structural focus (no colour), consistent with D-05.

**Alternatives:** red focus ring (rejected: ceremony spill)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-12 · selection · AUTHORED · confidence: low
**Decision:** Small fixed sets (≤ ~12) = native select squared like a field. Larger/filtered selection out of scope; platform fallback, marked as improvisation.

**Evidence:** none captured

**Reasoning:** Same honesty rule as the platform; no invented combobox.

**Alternatives:** invent searchable picker (rejected)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-13 · feedback · AUTHORED · confidence: medium
**Decision:** Notices = ruled boxes (2px black top rule, grey ground) with plain, non-bureaucratic sentences; what happened + what happens next in one or two sentences; no toasts.

**Evidence:** plain-language mandate quoted; no feedback component exists in the standard

**Reasoning:** Ruled box as vessel; plain-language rule governs copy.

**Alternatives:** coloured alerts (rejected)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-14 · destructive · AUTHORED · confidence: medium
**Decision:** High-consequence flow confirms in a square dialog: 2px black frame, consequence sentence in plain words, confirm = solid black square labelled with the verb, cancel = outline square. Never pre-focused.

**Evidence:** no pattern in source; register derived

**Reasoning:** Black severity keeps red ceremonial; structural emphasis.

**Alternatives:** red confirm (rejected: red purity)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-15 · progress · AUTHORED · confidence: medium
**Decision:** Meter = square track in #F4F4F4 with black fill and a plain readout ('7 of 10 steps'); restart = outline square. Static only; nothing decoratively animates (motion gated, per the standard's animation doctrine).

**Evidence:** gated-motion doctrine observed; primitives attested

**Reasoning:** Composes attested primitives; honours the motion doctrine.

**Alternatives:** red fill (rejected: ceremony purity)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-16 · empty · AUTHORED · confidence: medium
**Decision:** Empty state = plain ruled statement + one action; no imagery (imagery absence is a system property).

**Evidence:** no imagery style defined; protectionist posture observed

**Reasoning:** Absence, honestly expressed.

**Alternatives:** flag-coloured decorative blocks (rejected: mark-adjacent)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-17 · repeated-content · AUTHORED · confidence: medium
**Decision:** Ledger = ruled register: 2px black header rule over medium labels, 1px pewter hairlines between rows, no zebra; row hover = #F4F4F4; status labels inline per D-10.

**Evidence:** ruled/measured register; table structures implied by document culture

**Reasoning:** Documents are the system's native form.

**Alternatives:** zebra rows (rejected)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-18 · overlays · AUTHORED · confidence: medium
**Decision:** Dialog = square white sheet, 2px black frame, black scrim at 55%, instant; no motion.

**Evidence:** flat ruled language; motion gated

**Reasoning:** Same doctrine as D-02/D-15.

**Alternatives:** fade (rejected)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-20 · responsive · OBSERVED · confidence: medium
**Decision:** Bilingual side-by-side collapses to over-under (the observed fallback rule); nav collapses to a plain row; scaling is quiet (no mobile-specific scale invented).

**Evidence:** over-and-under fallback quoted from the standard; collapse behavior authored minimally

**Reasoning:** The observed fallback IS the responsive doctrine; applied honestly.

**Alternatives:** none

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED

### D-21 · focus · AUTHORED · confidence: medium
**Decision:** Focus = 2px black outer ring offset 2px (visible on any ground); no colour used for focus. Merged implementation with D-11 field focus.

**Evidence:** none captured

**Reasoning:** Structural, colour-free focus matches the doctrine.

**Alternatives:** red ring (rejected: ceremony purity)

**Review outcome:** ☐ ACCEPT ☐ MODIFY ☐ REJECT ☐ LEAVE UNDEFINED


## Open (genuinely undefined — may remain so)

_None._
