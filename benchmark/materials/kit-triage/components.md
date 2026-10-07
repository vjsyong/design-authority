# Components (35)

Each entry: class, what it is, states it ships, accessibility notes,
docs page. Source: `design/core/`.

## Button — `.btn`

Action trigger. Use a real button or link; variants (primary/ghost/danger/small), busy state via guardApply. Never a clickable div.

States: default, hover, active, focus-visible, disabled, busy (guardApply)

Accessibility:
- Use a real <button> or <a>; never a clickable div.
- Icon-only buttons need aria-label.
- guardApply freezes and relabels the submit button until navigation.

Docs page (in the system site): `/components/buttons`

## Icon button — `.iconbtn`

Square icon-only control for compact toolbars and rows; must carry an aria-label.

States: default, hover, active, focus-visible

Accessibility:
- aria-label is mandatory (the glyph is aria-hidden).
- Minimum 44px on coarse pointers.

Docs page (in the system site): `/components/buttons`

## Switch — `.px-sw`

The one boolean control for enabling/disabling an entity; auto-submits and announces.

States: checked, unchecked, disabled, focus-visible

Accessibility:
- The visible label wraps a real checkbox; hidden twin carries the off value.
- aria-label carries the verb: Enable/Disable <object>.
- Coarse pointers get a 44px hit area.
- Disabled state dims the track and blocks interaction.

Docs page (in the system site): `/components/forms`

## Menu item — `.menu-item`

Item inside a dropdown menu; sentence case; destructive items carry 'menu-item danger arm-del'.

States: default, hover, danger, armed, focus-visible

Accessibility:
- Destructive items use .arm-del with data-arm-label naming the object.
- Escape and outside click disarm; details close disarms.

Docs page (in the system site): `/components/navigation`

## Nav item — `.nav-item`

Sidebar/navigation link with icon, active rail state and aria-current.

States: default, hover, active(selected), focus-visible

Accessibility:
- aria-current="page" on the active item.
- Active rail is border-inline-start (mirrors in RTL).

Docs page (in the system site): `/components/navigation`

## Chip — `.chip`

Compact filter/selection token used in filter rows; distinct from badge (not a status).

States: default, hover, active(selected), focus-visible

Accessibility:
- Counts live in .n; the whole chip is the target (not just the label).

Docs page (in the system site): `/components/data`

## Index row — `.index-row`

Standard row for list/index pages: primary text, meta, optional actions.

States: default, hover, active, focus-visible

Accessibility:
- 54px minimum height; one row = one destination.

Docs page (in the system site): `/components/data`

## Table — `.tbl`

Data table with sticky headers; collapses to card rows (.mcards) on phones.

States: default, row hover, selected, reflowed (mcards)

Accessibility:
- th scope where the header is meaningful; row checkbox needs aria-label.
- Hover-revealed row actions must also be reachable by keyboard focus.

Docs page (in the system site): `/components/data`

## Bulk bar — `.bulkbar`

Selection-only toolbar for batch operations; hidden until rows are selected.

States: hidden, shown with selection

Accessibility:
- role=region with aria-label; count is text, not colour.

Docs page (in the system site): `/components/data`

## Save bar — `.savebar`

Sticky footer for editors: primary Save plus Cancel; validation renders above, focused.

States: sticky, keyboard-lifted (JS transform)

Accessibility:
- Lifts above the mobile keyboard via keyboard-fit.js (transform), not a class toggle.
- One primary action per card.

Docs page (in the system site): `/components/forms`

## Flash message — `.msg`

Banner for server/redirect feedback; exactly ok/warn/err kinds.

States: ok, warn, err

Accessibility:
- role=status (or role=alert for errors) on the rendered banner.
- Colour is always paired with text.

Docs page (in the system site): `/components/feedback`

## Toast — `.toast2`

Transient in-place feedback (one at a time) from the shared toast host.

States: ok, warn, err, auto-dismiss

Accessibility:
- #toasts is aria-live=polite; one toast at a time.

Docs page (in the system site): `/components/feedback`

## Badge — `.badge`

Compact status label (uppercase micro-badge); pair colour with text, never colour alone.

States: neutral, ok, warn, err, acc, solid

Accessibility:
- Uppercase micro-label; never the only signal — pair with text that says the same thing.

Docs page (in the system site): `/components/data`

## Empty state — `.empty`

Empty state anatomy: title, one-line reason, at most one primary CTA.

States: default

Accessibility:
- h4 + one-line reason + at most one action; never a bare blank area.

Docs page (in the system site): `/components/feedback`

## Dialog (native) — `.dlg`

Native dialog element for modals/confirms; static-backdrop variant available; dialog is the confirm primitive.

States: open (showModal), backdrop, wide variant

Accessibility:
- Native <dialog> + showModal(): top layer, inert background, Escape, focus restore — do not hand-roll a focus trap.
- aria-labelledby points at the heading; autofocus the first meaningful control, not the close button.
- Backdrop click closes unless the dialog is destructive.
- Backdrop close is suppressed for [data-dlg-static] / [data-danger] dialogs.

Docs page (in the system site): `/components/overlays`

## Tooltip — `.tip`

Tooltip for supplementary hints; hover/focus triggered.

States: hover, focus-visible

Accessibility:
- Decorative tips only; essential text must be in the DOM. Pair with aria-describedby for screen readers.

Docs page (in the system site): `/components/overlays`

## Spinner — `.spinner`

Loading indicator for waiting states; pair with text describing what is loading.

States: spinning, reduced-motion (slowed)

Accessibility:
- Indeterminate progress: keep the action label honest ('Queued…'), and slow to 1s under prefers-reduced-motion.

Docs page (in the system site): `/components/feedback`

## Field error — `.field-err`

Inline field validation message; form-level summary focuses at top.

States: message, aria-invalid input

Accessibility:
- Focusable summary at the top + inline message per field, linked with aria-describedby; aria-invalid=true on the control (W3C ARIA21).

Docs page (in the system site): `/components/forms`

## Tabs — `.tabs`

In-place view switcher; roving tabindex + arrow keys via components.js.

States: selected, hover, focus-visible, overflow-scroll

Accessibility:
- tablist/tab/tabpanel roles wired by components.js with roving tabindex and Arrow/Home/End.
- Panels are hidden, not unmounted; one tab is always selected.

Docs page (in the system site): `/components/navigation`

## Breadcrumbs — `.crumbs`

Breadcrumb trail for hierarchical navigation.

States: default, current

Accessibility:
- nav[aria-label=Breadcrumb] wraps an ordered list; plain text + separators.
- aria-current on the leaf; the last item is not a link.

Docs page (in the system site): `/components/navigation`

## Radio — `.radio`

Square single-choice control.

States: checked, unchecked, focus-visible, disabled

Accessibility:
- Native input inside the label; group with fieldset/radiogroup and a shared name.

Docs page (in the system site): `/components/forms`

## Slider — `.slider`

Range control with numeric readout.

States: default, focus-visible, disabled

Accessibility:
- aria-label on the range; the readout mirrors the value; keyboard steps come from the native input.

Docs page (in the system site): `/components/forms`

## Combobox — `.cb`

Combobox: type-to-filter select, optionally multi-select with chips and a mirror input.

States: closed, open, filtered, selected, multi-chips

Accessibility:
- aria-activedescendant listbox: focus stays in the input; options are filtered in place.
- Multi-select mirrors values into a hidden input and announces chips via aria-live.

Docs page (in the system site): `/components/forms`

## Date picker — `.dp`

Date picker: text input plus calendar popover; min/max supported.

States: open, today, selected, out-of-month, disabled-day, roving-focus (one tabbable cell)

Accessibility:
- ISO value on the input; month/weekday names and full-date day labels via Intl (locale-aware).
- Roving tabindex: exactly one day cell is tabbable — the selected day in view, else today, else the first enabled day.
- Arrow keys move ±1/±7 days, Home/End to week start/end, PageUp/PageDown change month; disabled days are skipped.
- Escape from anywhere inside the popup closes it and returns focus to the input; selecting a day does the same.
- min/max disable days; today carries aria-current=date.
- Clicking the input reopens the picker after a selection (the input is already focused, so no focus event fires).

Docs page (in the system site): `/components/forms`

## Accordion — `.acc`

Accordion/disclosure for collapsible sections.

States: closed, open, focus-visible

Accessibility:
- Native details/summary — keyboard and find-in-page work for free; group with the details name attribute for exclusivity.

Docs page (in the system site): `/components/data`

## Avatar — `.avatar-sq`

Square avatar chip for people. (avatar-sq)

States: initials, image, ink, group

Accessibility:
- Decorative avatars are aria-hidden; meaningful ones need alt/label. Groups carry an aria-label with the count.

Docs page (in the system site): `/components/data`

## Image — `.img`

Image presentation with system borders; always alt text.

States: 16:9, 4:3, 1:1, contain, caption

Accessibility:
- alt is mandatory (TDS014); the frame reserves space so loading never shifts layout.

Docs page (in the system site): `/components/data`

## Upload / dropzone — `.drop`

Dropzone + file input for uploads; dispatches triage:files.

States: idle, dragover, focus-visible, file-list

Accessibility:
- role=button + Enter/Space; announces files with name and size; removal is a labelled button.

Docs page (in the system site): `/components/forms`

## Notifications — `.notif`

Notifications panel with unread dot and mark-all-read.

States: unread, read, empty, mark-all

Accessibility:
- The summary's accessible name carries the unread count; unread uses background + a dot, never colour alone.

Docs page (in the system site): `/components/feedback`

## Command palette — `.cmd`

Command palette dialog (cmd-k style) with input, items and triggers.

States: closed, open, filtered, active-item, empty

Accessibility:
- Native dialog; Arrow/Enter/Escape inside, cmd/ctrl+K opens; items are buttons with listbox roles.
- A click executes the clicked item (both data-href and data-cmd-action paths); Enter executes the highlighted item.

Docs page (in the system site): `/components/overlays`

## Full-page state — `.page-state`

Full-page state (e.g. fatal/empty app shell) with message and action.

States: 404, 500, 403, offline, maintenance

Accessibility:
- One h2 per page state; the code is secondary; actions are the only focusable elements.

Docs page (in the system site): `/components/feedback`

## Numbered pagination — `.pager-num`

Numbered pagination with page-size control; phone-trimmed.

States: first, middle, current, gap, disabled

Accessibility:
- aria-current marks the active page; range labels on prev/next; page-size select is labelled.

Docs page (in the system site): `/components/data`

## Timeline — `.tl`

Timeline for histories (e.g. approval steps): ordered entries with markers, time, actor.

States: default, status-dots

Accessibility:
- Ordered list; dots are decorative (the text carries the meaning).

Docs page (in the system site): `/components/data`

## Diff — `.diff`

Diff presentation for before/after comparison.

States: context, added, removed, empty

Accessibility:
- role=table with labelled columns; +/- expressed as background tints plus repeated line numbers.

Docs page (in the system site): `/components/data`

## Sheet dialog — `.sheet-end`

End sheet: slide-over dialog variant for secondary panels.

States: side, bottom

Accessibility:
- Same native-dialog contract as .dlg (top layer, Escape, focus restore); data-dlg-static still blocks backdrop close.

Docs page (in the system site): `/components/overlays`
