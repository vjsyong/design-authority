# Triage design kit

The design system this product follows: **Triage 0.12.1** (snapshot `e374f3803d`).
Everything here comes from the same authority the system is built from.

## Layout

```
design/tokens/      token source (tokens.css is what you load)
design/core/        the stylesheets + behaviour scripts
design/fonts/       Geist / Geist Mono (self-hosted)
design/icons/       icon registry + sprite
design/examples/    seven real example screens (open them in a browser)
design-docs/        this documentation
```

## Quickstart (load order)

```html
<link rel="stylesheet" href="/design/tokens/tokens.css">
<link rel="stylesheet" href="/design/core/base.css">
<link rel="stylesheet" href="/design/core/patterns.css">   <!-- page patterns -->
<script src="/design/core/components.js" defer></script>
```

Theme: `data-theme="light|dark"` on `<html>` (light default). Density:
`data-density="compact"` (comfortable default).

## How to decide (read this first)

1. **A component exists for it** → use it. See `components.md`; a component's
   class is the only canonical implementation of that idea.
2. **No dedicated component, but a sanctioned composition** → follow a recipe
   in `recipes.md` (they compose existing components and carry constraints).
3. **Nothing specific** → follow the fallback policy in `fallbacks.md`:
   plain content on system surfaces, tokens only, clearly not canonical.
4. **Never invent new canonical UI.** Improvisation is allowed when necessary,
   but it must stay marked as an improvisation, never presented as canon.
5. **Some things are prohibited outright** — see `prohibitions.md`.

Rules (`rules.md`) are the enforceable contract; `guidelines.md` covers the
normative-but-human parts (interaction, copy, accessibility); `tokens.md`
explains the value tiers; `patterns.md` the page-level compositions.
