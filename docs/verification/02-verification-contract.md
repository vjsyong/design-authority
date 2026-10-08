# 02 · The verification contract — format and runner

**Design goal (per brief):** the smallest representation that can test the
three current authorities. No generic DSL, no formal language. A contract is
*data*; the verifier is generic. Nothing in the verifier branches on
authority identity — everything authority-specific lives in the pack's
contract file (success criterion 6).

## Where contracts live

`packs/<authority>/verification.json` — an **optional additive pack
artifact** of this experiment (pack version untouched; 0.2.0 kernel paths
ignore it). A pack without a contract simply has nothing to verify — the
runner reports that honestly rather than guessing.

## Entry schema

```json
{
  "contract_version": "0.1",
  "authority": "wink",
  "pack_version": "wink 0.2.0",
  "scope_note": "…what is excluded (instrument styling) and why…",
  "checks": [
    {
      "id": "wink/action-pill-radius",          // unique; <authority>/<slug>
      "item": "rule/W-R1",                       // the authority item it verifies
      "title": "Buttons are pills (radius = half height)",
      "classification": "MECHANICALLY_VERIFIABLE",   // audit class (01)
      "severity": "error",                        // error | warning | info | review
      "mode": "COMPUTED_STYLE",                   // see modes below
      "selector": ".cta",                         // DOM/COMPUTED/INTERACTION target
      "assertions": [ {"property": "border-radius", "relation": "pill"} ],
      "missing": "fail",                          // fail -> VIOLATION if absent; skip -> UNVERIFIABLE
      "note": "optional human note"
    }
  ]
}
```

One check = one authority item (or one clause of it) and one honest result.
The brief's illustrative shape maps 1:1; nothing else was invented.

## Modes

| mode | inspects | typical assertions |
|---|---|---|
| `STATIC` | source files (`app.css`, `app.js`, `index.html`) | `no_match`, `present`, `declarations`, `color_literals`, `no_css_url_images` |
| `DOM` | rendered document (whole-page scans where selector-less) | `exists`/`absent`, `text_len_min`, `page_text_no_match`, `bil_pairs_ok` |
| `COMPUTED_STYLE` | `getComputedStyle` of a resolved element (+ its box height) | property relations below |
| `INTERACTION` | scripted scenarios returning evidence | evidence relations below |
| `REVIEW` | nothing machine — emitted as `REVIEW_REQUIRED` | — |

**Interaction scenarios** (named, small, generic — not authority-branching):
`tab-focus` · `open-delete` (params: trigger, destructive) · `focus-input`
(params: selector) · `red-area-scan` · `red-status-scan` ·
`status-colour-scan` · `fixed-scan` (params: allow_regex). Each returns
evidence values; assertions then test the evidence. Scenarios restore state
after themselves (e.g. close what they opened).

**Property relations** (computed): `equals`, `not_equals`, `one_of`,
`not_in`, `contains` (fragment list — order-insensitive), `not_contains`,
`min`/`max` (numeric, px-aware), `pill` (radius ≥ half the element height),
`color_is`, `color_in`, `color_family` (red/blue/green/amber/neutral via HSL),
`transition_max`.
**Evidence relations**: `equals`, `not_equals`, `min`/`max`, `count_eq`,
`contains`.

## Runner

```bash
python3 tools/da_verify.py --pack packs/wink --target examples/cadence3-wink \
    --out docs/verification/raw/wink-clean
```

The runner: serves the target on a loopback port, normalises deterministic
state (clears localStorage, dismisses the onboarding overlay, reveals hidden
views for whole-app scans — recorded in the raw output), runs every check,
and writes `raw.json` + `summary.txt` (+ violation screenshots).

**Result statuses:** `PASS` · `VIOLATION` · `UNVERIFIABLE` · `NOT_APPLICABLE`
· `REVIEW_REQUIRED`. Aggregation is worst-of; ambiguous observations are
never silently converted to PASS (a missing target is VIOLATION only when the
contract says `missing: fail`, otherwise UNVERIFIABLE).

## Anti-evasion posture (what the contract is not allowed to rely on)

- Agent annotations (`data-improvised` etc.) are **locator hints only** —
  no check asserts "the agent said it was canonical".
- No hand-authored special markers are required for detection; every check
  reads files, DOM, computed style, or behaviour.
- The verifier never reads the mutation manifest (see `04`); the injector is
  a separate process whose output the verifier cannot see.

## Honest boundaries (recorded, not hidden)

- Palette checks are allowlist+heuristic: known-off hues are caught; a
  *new* shade between allowed hues can pass (PARTIAL — by design).
- `red-area-scan` is a ≤10%-of-viewport heuristic, not a semantics engine.
- Pictorial svg can hide behind the sanctioned `.spark` class (recorded in
  the dominion check's note).
- Everything REVIEW goes to humans (`07` closes the loop with the review
  queue in the lens integration).
