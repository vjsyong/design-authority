# raw: designsystems.one — Mailchimp Design System
URL: https://www.designsystems.one/design-systems/mailchimp-design
Fetched: 2026-10-07 (hound smart_fetch, http 200; truncated at 9000/10209 chars) | author Kiryl Zhukouski, published 2026-01-15
NOTE (from source itself): "Unofficial, community-authored reference... values are indicative, not canonical", "0/66 fields have an explicit source and 0 have a recorded check date". Official documentation cited: https://mailchimp.com/design/

## Extracted text (verbatim)

Mailchimp — Voice-led marketing platform system with unusual editorial discipline.

[...] Mailchimp's UX team has published their content style guide and patterns publicly since the early 2010s — predating most modern design systems by years. The current design system absorbed those lessons and now spans the campaign builder, automation editor, audience tools, and reporting dashboards used by millions of small businesses.

Mailchimp's central UX team owns the system; product teams contribute through an internal review process. The voice and content guidance is unusually load-bearing — it ships ahead of components and is treated as canonical.

### Color tokens
| Color | Value | CSS variable | Role |
| --- | --- | --- | --- |
| Cavendish Yellow | `#ffe01b` | `--mc-cavendish` | Hero brand color |
| Peppercorn Text | `#241c15` | `--mc-peppercorn` | Primary text (warm black) |
| Secondary Text | `#5d5245` | `--mc-text-secondary` | Secondary text |
| White | `#ffffff` | `--mc-white` | Surfaces |
| Parsnip | `#f6f6f4` | `--mc-parsnip` | Warm subtle background |
| Border | `#dedddc` | `--mc-border` | Borders |
| Kale Link | `#007c89` | `--mc-kale` | Links and interactive (teal) |
| Error Red | `#bf4055` | `--mc-error` | Errors |

### Typography
- **Display:** Means — weights 400 — `Means, Georgia, serif`
- **Body:** Graphik — weights 400, 500, 700 — `Graphik, 'Helvetica Neue', Arial, sans-serif`

### Type scale
| Step | Size | Line height |
| --- | --- | --- |
| display | `48px` | `56px` |
| h1 | `32px` | `40px` |
| h2 | `24px` | `32px` |
| body | `16px` | `24px` |
| small | `14px` | `20px` |

### Spacing
Base unit: `8px`
Scale: `8px` · `16px` · `24px` · `32px` · `48px`

### Corner radius
| Name | Value |
| --- | --- |
| default | `8px` |
| pill | `9999px` |

### Visual character
"Winking-chimp charm: Cavendish yellow with Peppercorn warmth, Means serifs for wit, and small-business friendliness as strategy."

### Known for
- Voice and content guidance that other systems quietly copy from — the content style guide is the reference for friendly, plainspoken product writing.
- Empty-state and onboarding patterns built for the long tail of small businesses, not enterprises with admins.
- Illustration as a system component — house-style, themable, and used consistently across surfaces.

### Underrated
- Their accessibility commitment predates most public design systems; AA-plus targets are baked into component contracts, not retrofitted.
- The campaign-builder pattern (a multi-step editor with previews and pause-and-resume) is one of the better-documented complex flows in marketing tools.

### Watch out for
- Mailchimp's visual identity is distinctive — the illustration system and yellow brand are not lift-and-shift assets.
- Patterns assume self-serve SMB users. Enterprise-style admin patterns (RBAC, multi-org) aren't where the system focuses.

### Components worth studying
- **Wink (illustration system)** — Branded illustration set with documented usage and themable color.
- **Campaign Builder** — Multi-step editor pattern with live preview, save-and-resume, and async send.
- **Empty State Library** — First-run, no-results, and lapsed-user states tuned for SMB onboarding.

### Governance / origin (as stated)
- Owner: Mailchimp's central UX team; product teams contribute via internal review.
- "The public UX pattern library was retired; values reflect current brand guidance."
- Content style guide public since early 2010s; "ships ahead of components and is treated as canonical".
