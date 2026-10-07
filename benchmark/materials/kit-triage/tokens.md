# Tokens

All values live in `design/tokens/tokens.css` (generated from
`design/tokens/tokens.json`, the source of truth). Never hardcode a
colour/spacing/duration that has a token.

## Colour tokens

Primitives plus semantic aliases (surface-*, text-*, status-*, interactive-*, ink), tints and solid status surfaces; both themes.

## Typography tokens

Geist / Geist Mono families, relative --base-size root, --fs-* scale, weights and line-heights.

## Spacing tokens

Preferred scale 2/4/8/12/16/24/32/48 + semantic roles --space-page/card/field/control + legacy steps (compatibility).

## Motion tokens

Duration set (100–400ms) and easings; ad-hoc durations are off-token.

## System constants

Radius policy 0, breakpoint set, z-index ladder, fixed layout widths (--layout-sidebar/content-max/dock).

## Dataviz palette

Eight categorical series (Okabe-Ito derived), CVD-checked, for downstream chart code.

Theme via `data-theme` (light/dark); density via `data-density`
(comfortable/compact). Fixed chrome widths live as `--layout-*`.
