# Portability Spike · 09 · Ubuntu source audit & derivation basis (“Indaba”)

**Swap approved** (reviewer, 2026-10-07) after the NASA kit was retired
(`06`–`08`). Source: **Ubuntu brand guidelines, design.ubuntu.com (Canonical)**,
fetched fresh 2026-10-07. Derived with quarantine in effect: no Triage-content
skills loaded, no incumbent CSS read, Vanilla explicitly excluded.

**Working name:** “Indaba” (Zulu: a gathering). No Ubuntu marks are reproduced;
no Ubuntu trademark is used as a product name; Ubuntu used nominatively in
provenance only.

## 1 · Rights

- Brand guidelines/identity: nominative experimental use; the logo and marks
  are not reproduced (same discipline as NASA).
- Fonts: **Ubuntu Font Family** (Dalton Maag for Canonical), **Ubuntu Font
  Licence 1.0** — freely usable; four weights vendored into the tile
  (`tile-ubuntu/fonts/`).
- Explicit exclusion: **Vanilla** (Canonical’s component system) is *not* a
  source for this derivation — the brief needs identity-level formalization,
  not API translation.

## 2 · Verified colour palette (OBSERVED)

| colour | value | stated usage (quotes from the brand page) |
|---|---|---|
| Ubuntu orange | `#E95420` | “a signal of community engagement”; community emphasis |
| Aubergine | `#77216F` | “indicates commercial involvement”; “rich, mature” |
| Aubergine variants | `#5E2750` · `#2C001E` | supporting palette depth |
| White | `#FFFFFF` | “clean, fresh and light feel” |
| Warm grey | `#AEA79F` | “for backgrounds, graphics, **dot patterns**, charts and diagrams”; large-size text |
| Text grey | `#111111` | small headings, sub-headings, body copy — “black can be quite harsh in combination with aubergine, but grey delivers more balance” |
| Cool grey | `#333333` | charts and diagrams |
| Tints | — | “tints of the above palette colours can be used as background colours” |

Emphasis scale (OBSERVED): community-weighted work leans white + orange with
warm grey; commercial-weighted work leans aubergine-core. Derived system takes
a **community-leaning** stance (orange actions, aubergine identity, warm
balance) — appropriate for the lending-register domain.

## 3 · Typography (OBSERVED)

- Ubuntu font family, commissioned by Canonical, by Dalton Maag: “contemporary
  style… convey a precise, reliable and free attitude”; libre/open; used by
  default. Weights used in the tile: Light (display) · Regular (body) ·
  Medium (labels/emphasis).
- Sizes are screen-authored (no print sizes specified by the brand) — AUTHORED:
  display 30/300, heading 22/400, body 16/400, label 14/500, meta 13.

## 4 · Form language (INFERRED, from brand evidence)

- The brand’s forms are **circular and soft**: the logo’s circles, the
  typeface’s rounded terminals, warm-grey dot patterns.
- Derived: radius 12 for surfaces/fields; **pill shape for controls and
  status**; soft shadows for gentle separation; dot pattern as a graphic
  motif (circles, warm grey — per the stated usage).

## 5 · Values / tone (OBSERVED)

“Humanity towards others”; a growing community working together; professional
but warm. Copy stays plain and kind.

## 6 · Classification (ledger, carried forward)

- **OBSERVED:** palette values + stated usage; font family/licence; values.
- **INFERRED:** UI role mapping (orange=actions, aubergine=identity/headings,
  warm grey=balance/rules/dot patterns, tints=surfaces); rounded/pill form
  language; community-leaning emphasis; status = word-first pills.
- **AUTHORED:** hover shades, shadow softness, screen type sizes,
  dot-pattern band implementation.
- **UNDEFINED (carried):** motion; multi-hue data coding beyond the brand
  palette; busy states; searchable selection.

## 7 · Why Ubuntu (vs the earlier ranking)

`00` ranked Ubuntu “weakest formalization test” for a *component-library*
derivation. That criterion is superseded: the spike now needs a **gestalt
inversion** of the rejected axes (square corners → rounded; monochrome +
alarm red → warm aubergine/orange; max contrast → grey-balanced; square
markers → word-first pills). Ubuntu inverts all four with brand-grounded
evidence. NYCTA retained as backup only.

## 8 · ST gate artifact

`tile-ubuntu/out/style-tile.png` — palette, type, controls, status, fields,
surfaces, dot pattern. Reviewed by the author (renders real Ubuntu fonts;
no square/pilled conflicts) and now with the reviewer **before any screen
design**, per `08` §2.3.
