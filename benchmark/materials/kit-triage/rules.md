# Rules (15)

The enforceable contract (checked by the Triage linter). Severities:
error / warning / info. A rule's `fix` is the remedy.

## TDS001 · error — deprecated-name

**What:** Uses a pre-Triage (mail-triage era) class, id or global instead of the renamed vocabulary.

**Why:** The 0.1.0 rename sweep defined the public vocabulary; old names are no longer styled by core.css and silently fall back to browser defaults.

**Fix:** Rename via /RENAME-MAP.md (or run: python3 tools/assemble_from_pack.py --apply-map <files>).

## TDS002 · warning — raw-colour

**What:** A colour literal appears where a token exists (palette match = error) or that is not in the palette (off-system colour = warning).

**Why:** Colour is tokenised in tokens/tokens.json; literals fork the theme and bypass the semantic alias tier.

**Fix:** Use var(--token) (prefer semantic aliases: --surface-*, --text-*, --status-*) or add the colour to tokens.json.

## TDS003 · error — non-zero-radius

**What:** A non-zero border-radius (CSS property or JS style key).

**Why:** Zero radius is a design-system token (misc.radius = 0px), enforced globally by *{border-radius:0 !important}.

**Fix:** Remove the radius, or fork the system deliberately by changing the token and deleting the global rule.

## TDS004 · error — focus-removed

**What:** outline:none / outline:0 without a visible focus replacement in the same rule.

**Why:** The global :focus-visible ring is accessibility-critical (WCAG 2.4.7/1.4.11); removing it without replacement fails the system's a11y gate.

**Fix:** Keep the global ring, or provide :focus-visible with a 2px+ ring or a compensating box-shadow/border change.

## TDS005 · warning — off-scale-spacing

**What:** Margin/padding/gap/inset px values outside the normalised spacing scale.

**Why:** Triage ships a 2/4px-grid spacing scale (tokens.json spacing group); ad-hoc values are the measured drift the system exists to stop.

**Fix:** Snap to the nearest scale value or extend the scale in tokens.json deliberately.

## TDS006 · info — off-token-motion

**What:** Transition/animation duration not in the motion token set.

**Why:** Durations are tokens (motion.duration); ad-hoc values break the motion feel and the Material-3-derived ranges.

**Fix:** Use a motion duration token value (100/120/150/180/200/240/250/280/400ms).

## TDS007 · info — off-ladder-zindex

**What:** z-index outside the documented ladder.

**Why:** The z-index ladder (bulkbar 6 … toasts 300) is a contract; anything full-screen must clear 180 or the mobile tab bar punches through.

**Fix:** Use a ladder value or extend misc.zindex in tokens.json.

## TDS008 · error — off-system-font

**What:** font-family declaration not using Geist / Geist Mono (or inherit).

**Why:** Typography is part of the system identity and the variable-font loading strategy.

**Fix:** Use the system stacks (or var(--mono)), or change the token in tokens.json for a deliberate rebrand.

## TDS009 · error — token-override

**What:** A project stylesheet redefines a Triage custom property (--bg, --acc, --surface-* …).

**Why:** Tokens are the source of truth; local overrides fork the theme invisibly and break contrast guarantees.

**Fix:** Edit tokens/tokens.json and regenerate, or use a distinct non-system variable name for local values.

## TDS010 · info — unknown-class

**What:** A class used in markup that core.css / patterns.css do not define (opt-in, may be a project class).

**Why:** Design elements should come from the system catalogue; unknown classes are how bespoke one-offs creep in.

**Fix:** Use a system class, or allowlist the project class in .triagerc.json.

## TDS011 · error — contrast

**What:** A defined token pair fails WCAG contrast (4.5:1 text / 3:1 non-text).

**Why:** The token set is the contrast contract; theme overrides can silently break it.

**Fix:** Adjust the token value(s) so the pair meets the threshold, or extend .triagerc.json contrastPairs for intentional exceptions.

## TDS012 · warning — primitive-use

**What:** A product stylesheet consumes a primitive token directly where a semantic alias exists.

**Why:** The alias tier is what makes retheming possible without touching components; primitive use forks the theme.

**Fix:** Use the alias (e.g. var(--surface-card) instead of var(--card)). Definitions inside tokens.css are exempt.

## TDS013 · warning — physical-direction

**What:** Physical direction property (margin-left, left:, text-align:left …) instead of logical properties.

**Why:** The system supports RTL via logical properties; physical properties double the stylesheet and break direction switching.

**Fix:** Use margin-inline-start/end, padding-inline-*, border-inline-*, inset-inline-*, text-align:start/end.

## TDS014 · error — image-alt

**What:** <img> without an alt attribute.

**Why:** Alt text is the accessibility contract for images; decorative images still need alt="".

**Fix:** Add alt with a description, or alt="" when the image is decorative.

## TDS015 · error — accessible-name

**What:** Interactive element with no accessible name (empty button/link, no aria-label), or a positive tabindex.

**Why:** Icon-only controls without labels are unusable with assistive tech; positive tabindex breaks natural order (WCAG 2.4.3).

**Fix:** Add text or aria-label; never use tabindex > 0.
