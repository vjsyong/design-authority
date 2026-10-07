# Fallbacks — when the system has no answer

Sanctioned generic fallbacks (not canonical components; keep them
plain and token-conformant):

## Plain content on system surfaces

Render plain content using the system type scale, spacing roles and layout tokens: system text styles on a system surface, no new visual language, no invented component skin.

Scope: layout, content, typography, status

Constraints:
- tokens only
- mark the improvisation (code comment or note) so it is not mistaken for canon

## Native control, token-conformant

If no system control fits, use the platform's native element with minimal token-conformant styling; keep native semantics and degrade without JS.

Scope: forms, controls, input

Constraints:
- native semantics first
- no invented component presented as canonical

## Omit and report

When nothing sanctioned fits and any fallback would mislead users, omit the feature area rather than inventing canon, and report a gap.

Scope: *

Constraints:
- never silently invent
- a gap record is required when this fallback is used

## Policy

Implement per the consuming project's fallback policy, mark the improvisation, and report a gap. Never present improvisation as canonical.

Do not implement as requested; the request violates an explicit constraint (see the cited rule/prohibition).

Noncanonical. The authority is never modified by a consumer; proposals are reviewed upstream.
