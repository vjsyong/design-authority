# Sanctioned compositions (recipes, 15)

When there is no single component for a need, compose using these.
Ingredients are components/guidelines you must use; constraints are
binding.

## Redirect feedback is a banner

After a server round-trip / redirect, announce the outcome with a .msg banner at the top of the content.

Use when: show the result of a form submit; confirm settings saved; announce an action after redirect; show a success message; show the result of saving a form

Build from: `component/msg` (Flash message)

Constraints:
- redirect flows only; in-place actions use the toast host
- kinds exactly ok|warn|err
- past tense and name the object

> Server / redirect → an `.msg` banner at the top of the content.  
> — INTERACTION.md#feedback

## In-place feedback is a toast

JS/fetch actions announce via toast() from the shared host; one toast at a time.

Use when: announce an action without navigation; confirm an async result; show transient confirmation; announce that something was removed; show a toast message; show a success toast after an action

Build from: `component/toast2` (Toast)

Constraints:
- host it once per page (toasts aria-live)
- no page-local toast markup, no query-param toasts

> In-place (JS / fetch) → `toast(msg, kind)` from `core/shell.js` … One toast at a time.  
> — INTERACTION.md#feedback

## Entity delete is armed, two-step, in place

Deleting a listed entity (rule, flow, classifier, template, chat, record) is a two-step armed action; never a confirm() dialog.

Use when: delete a rule; remove an item from a list; destructive item action; delete a record

Build from: `component/btn` (Button), `component/menu-item` (Menu item), `guideline/armed-delete` (Armed two-step delete)

Constraints:
- first activation arms, second deletes
- auto-disarm 4s / Escape / outside click
- announce the result afterwards

> Deleting an entity listed in the UI … is a two-step, in-place action. No `confirm()` dialog, ever, for these.  
> — INTERACTION.md#item-deletes

## High-stakes actions keep a native confirm()

Irreversible, security-relevant, or multi-item actions confirm with a sentence naming the object and consequence.

Use when: confirm an irreversible action; confirm account removal; confirm enabling auto-apply; confirm rebuild

Build from: `guideline/high-stakes-confirm` (High-stakes confirmations)

Constraints:
- native confirm() on the form; sentence names object + consequence
- only the listed set

> Actions that are irreversible, security-relevant, or affect more than the clicked item keep a native `confirm()`.  
> — INTERACTION.md#one-way-actions

## Entity on/off is the switch, not a button

Every boolean enable/disable of an entity uses .px-sw; verbs are Enable/Disable; the route announces the new state.

Use when: enable or disable an entity; turn a setting on or off; pause a rule

Build from: `component/px-sw` (Switch)

Constraints:
- verbs Enable / Disable only (never Pause/Resume or On/Off)
- auto-submit announces

> Use `.px-sw` for every boolean enable/disable of an entity.  
> — INTERACTION.md#state-controls

## Status is never colour-only

State of an item is shown with a compact label/cell plus text (or icon); colour alone is prohibited.

Use when: show the state of an item; waiting for approval indicator; approved or rejected marker; status of a job; show the state of a request or item; show the approval status of a record

Build from: `component/badge` (Badge), `token-set/color` (Colour tokens), `guideline/colour-not-alone` (Colour is never the only signal)

Constraints:
- pair colour with text or an icon
- one status treatment per row cell

> Colour is never the only signal — pair it with text or an icon.  
> — INTERACTION.md#labels-accessibility

## Empty areas use the empty anatomy

Any list or card with nothing to show gets title + one line of reason + at most one CTA.

Use when: nothing to show yet; no results found; first-run empty area; no activity

Build from: `component/empty` (Empty state)

Constraints:
- never a bare blank area or a bare 'failed'
- specific reason + one recovery action

> `.empty` anatomy: optional icon, an `h4` title, one line of reason, and at most one CTA.  
> — INTERACTION.md#empty-states

## Bulk actions live in the selection bar

Batch operations on selected rows appear in .bulkbar only with a selection; triggers in .tactions.

Use when: act on many selected records; select rows then approve; batch delete selected

Build from: `component/bulkbar` (Bulk bar), `component/tbl` (Table)

Constraints:
- appears only with a selection
- announce the count/result afterwards

> Bulk actions live in `.bulkbar`, which appears only with a selection.  
> — INTERACTION.md#lists-row-actions

## Editors end in a save bar

Editors (forms that configure something) end in .savebar with primary Save plus Cancel; Cancel is the way out.

Use when: edit form with save and cancel; settings editor; configuration form

Build from: `component/savebar` (Save bar), `component/field-err` (Field error)

Constraints:
- Server-side validation renders at the top of the form and receives focus
- settings cards keep scoped partial saves

> Editors end in a `.savebar`: primary **Save \<thing>** plus **Cancel**.  
> — INTERACTION.md#save-bars

## Row actions: inline + menu variants

Record actions appear on hover/focus with .ra-inline for the key few and a details.menu for the rest; touch shows the menu.

Use when: per-row actions; actions for a list item; more menu on a row

Build from: `component/menu-item` (Menu item), `component/btn` (Button)

Constraints:
- sentence case; destructive item is menu-item danger arm-del
- every .rowacts ships both variants

> Desktop: relevant actions inline with `.ra-inline`; the rest in a `details.menu` with `.ra-menu` and a `.menu-pop`.  
> — INTERACTION.md#lists-row-actions

## Pages open with a page head

Page title + one-line description + actions; hierarchy levels are not skipped.

Use when: page title with actions; screen header for a view

Build from: `guideline/page-hierarchy` (Page hierarchy)

Constraints:
- don't shrink a page title to fit a long subject; let it wrap
- section headings and card headings mark different scopes

> Don't shrink a page title with inline font-size to fit a long subject — let it wrap at --fs-page-title.  
> — site/pages_foundations.py#typography

## Modal tasks use the native dialog

Popups/modals are built on the native dialog element (.dlg), with static-backdrop when closing must be deliberate.

Use when: modal task or form; popup with fields; dialog with confirmation

Build from: `component/dlg` (Dialog (native))

Constraints:
- autofocus the first meaningful control
- Esc/backdrop behavior deliberate

> Dialog (native)  
> — spec/states.json#dlg

## Long lists paginate with numbered pager

Long result sets page with the numbered pager plus page-size control; phone view trims chrome.

Use when: long list with pages; page through results

Build from: `component/pager-num` (Numbered pagination), `component/tbl` (Table)

> Numbered pagination  
> — spec/states.json#pager-num

## Copy affordances use the shared helper

Copy-to-clipboard goes through cp()/.copy so fallback and labelling stay consistent.

Use when: copy to clipboard button; copy a value

Build from: `guideline/copy-helper` (Copy helper owns the clipboard)

Constraints:
- never call navigator.clipboard from page code

> Never call `navigator.clipboard` from page code — the helper owns the fallback and the confirmation labelling.  
> — INTERACTION.md#copy

## Filtering a list is a chip row over the table

Narrow a list with a row of chips above the table; chips are selection tokens, not status badges.

Use when: filter a list; narrow results by category; filter rows by status; search and filter records

Build from: `component/chip` (Chip), `component/tbl` (Table)

Constraints:
- chips mark selection, badges mark status — do not conflate
- active filters stay visible with a clear affordance

> Filter chip  
> — spec/states.json#chip
