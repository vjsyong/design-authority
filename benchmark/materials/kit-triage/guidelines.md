# Guidelines (13)

Normative guidance that humans apply (interaction, feedback, copy,
accessibility, hierarchy). These are part of the system, not advice.

## Armed two-step delete

Deleting an entity listed in the UI is a two-step, in-place action with auto-disarm; no confirm() dialogs for these.

Do:
- carry .arm-del with data-arm-label and a matching aria-label
- arm on first activation (label becomes 'Confirm delete'), delete on second
- auto-disarm after 4s, on Escape, outside click, or menu close
- announce the result afterwards (banner or toast)

Don't:
- no confirm() for entity deletes
- no arming as a substitute for feedback

> No `confirm()` dialog, ever, for these.

## High-stakes confirmations

Irreversible, security-relevant, or multi-item actions keep a native confirm() whose sentence names the object and consequence.

Do:
- name the object and the consequence in the sentence
- keep strings apostrophe-safe

Don't:
- do not route entity deletes through confirm() (use arming)

> Representative set: remove account · reset tokens · rebuild the index · clear a chat · enable auto-apply · approve a risky plugin.

## Reversible mutations show the reverse

Edits undoable in place need no confirmation and no danger styling; put the reverse control next to the action.

Do:
- pair remove ⇄ re-include, snooze ⇄ wake, tag ⇄ untag

Don't:
- no confirms or danger styling for reversible edits

> Put the reverse control next to the action.

## Feedback routing: banner vs toast

Server/redirect results render an .msg banner; in-place JS results call toast(); kinds are exactly ok/warn/err.

Do:
- announce every mutation unless the new state is self-evident in the same viewport
- wording is past tense and names the object

Don't:
- no info kind
- no page-local toast markup or query-param toasts

> There is no `info` kind — use `ok` for a benign outcome and `warn` when only part of it worked.

## Row actions

Clicking a row opens the record; secondary actions live in .rowacts, revealed on hover/focus (always visible on touch).

Do:
- inline the relevant few with .ra-inline; rest in details.menu with .ra-menu
- sentence case menu items; destructive item is 'menu-item danger arm-del'

Don't:
- no physical-direction CSS (use logical properties)
- no grey tags/categories styling here — that's product convention

> Touch (≤767px): `.ra-inline` hides and the `⋯` menu shows.

## Editors end in a save bar

Editors end in .savebar: primary Save <thing> plus Cancel. Cancel is the way out; Back is only for a navigation backlink.

Do:
- render server-side validation at the top of the form and focus it
- settings cards keep scoped partial saves

Don't:
- a card never submits fields it does not own

> Settings cards keep scoped partial saves.

## Empty state anatomy

.empty = optional icon, h4 title, one line of reason, at most one CTA (.btn primary).

Do:
- use for any list or card with nothing to show
- micro-empties inside a feed may be a single .sub line

Don't:
- never a bare blank area or a bare 'failed'

> Give a specific reason and one recovery action.

## Copy helper owns the clipboard

Use the shared cp() helper / .copy element; the helper owns fallback and confirmation labelling.

Do:
- .copy marks the copy affordance

Don't:
- never call navigator.clipboard from page code

> The helper owns the fallback and the confirmation labelling.

## Labels & accessibility baseline

Sentence case for buttons/links/menu items; name the object; keep the global focus ring; 44px touch targets; colour never the only signal; every interactive element has an accessible name.

Do:
- name the object in destructive labels and aria-labels
- keep :focus-visible intact

Don't:
- positive tabindex
- icon-only controls without labels

## Colour is never the only signal

Status and meaning are carried by text or icon as well as colour; charts must survive greyscale and colour-blindness.

Do:
- label status lines directly
- vary dash patterns or annotate in charts

Don't:
- no colour-only dots or fills for meaning

> Do not rely on colour alone: label lines directly, vary dash patterns, or annotate.

## Page hierarchy

One element, one token and one job per level: page title → section heading → card heading → body → meta. Don't skip levels.

Do:
- let a long page title wrap at --fs-page-title

Don't:
- don't shrink a page title with inline font-size
- don't use a section heading as a card label

> Don't skip levels or spend a level you don't need.

## Overlay z-order

New full-screen overlays must clear the mobile tab bar; the ladder is tokenised (misc.zindex).

Do:
- use ladder values from tokens

Don't:
- no arbitrary z-index values

## Spacing by role, not by vibe

Use semantic spacing roles (page/card/field/control) and the preferred scale 2/4/8/12/16/24/32/48; legacy steps remain only for compatibility.

Do:
- snap new work to the preferred scale

Don't:
- no ad-hoc spacing values
