# Prohibited / conflict triggers (9)

Requests that contradict these must not be implemented as stated;
follow the referenced rule instead.

- **prohibit/rounded-corners** (rule TDS003) — Non-zero border-radius anywhere — zero radius is a system policy (enforced globally).
- **prohibit/remove-focus-ring** (rule TDS004) — Removing focus outlines without an equivalent visible :focus-visible replacement.
- **prohibit/raw-color** (rule TDS002) — Raw colour literals where tokens exist; off-palette colours must be added to the token source deliberately, not inlined.
- **prohibit/off-system-font** (rule TDS008) — Off-system font stacks (Geist / Geist Mono or inherit only).
- **prohibit/token-override** (rule TDS009) — Redefining a system custom property (--bg, --acc, --surface-*, …) in product CSS.
- **prohibit/color-only-status** — Conveying status by colour alone.
- **prohibit/custom-confirm-for-entity-delete** — A confirm() dialog or custom modal to delete a listed entity — entity deletes use the armed two-step pattern instead.
- **prohibit/page-local-toast** — Page-local toast markup or query-param toasts — the shared toast host owns feedback.
- **prohibit/ad-hoc-chart-colors** — Chart colours chosen ad hoc instead of the dataviz palette (CVD-checked, greyscale-safe).
