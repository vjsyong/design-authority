# Portability Spike · 10 · Indaba derived system (“Ubuntu”, v3)

Second authority, **third attempt**: after the NASA/“Orbit” line was rejected
twice and the contamination audit (`08`) landed, the source kit was swapped to
the **Ubuntu brand guidelines (Canonical)** — see `09-ubuntu-source-audit.md`
for the source audit. Derivation ran under quarantine (no incumbent context,
no Triage-content skills, fresh source fetches). **Gates passed:** style tile
approved (with two revision rounds: dark grey banner; dot stripe removed) and
screens approved by the reviewer — “Ok approved. Close enough.”

## 1 · Foundations

**Palette (OBSERVED values + OBSERVED usage notes; role mapping INFERRED):**

| token | value | role |
|---|---|---|
| Orange | `#E95420` | actions, highlights (brand: “community engagement”) |
| Aubergine | `#77216F` | identity, headings (brand: “commercial involvement”) |
| Deep aubergine | `#2C001E` | destructive, heaviest surfaces |
| Warm grey | `#AEA79F` | balance: surfaces, rules, graphics |
| Warm tint | `#F6F4F2` | surface backgrounds (“tints may be used as backgrounds”) |
| Cool grey | `#333333` | masthead banner (brand's dark grey) |
| Text | `#111111` | body copy — “black is harsh with aubergine; grey delivers more balance” |

**Type (OBSERVED family; sizes AUTHORED for screen):** Ubuntu font family
(Dalton Maag for Canonical; Ubuntu Font Licence 1.0), vendored weights
Light/Regular/Medium/Bold. Display 28–30 **Light** aubergine · headings 17–20
Medium aubergine · body 16 Regular `#111` · labels 14 Medium · meta 13 muted ·
line-height 1.5.

**Shape (INFERRED from brand evidence):** rounded language — surfaces radius
12–16, controls and status as **pills**; soft shadows for gentle separation;
no hard rules as devices, no square corners. Dot pattern retained only as a
brand graphic device (never applied as a banner stripe).

**Density/contrast:** generous, airy rows in the ledger (subtle alternating
warm tint + hover tint rather than hard rules); grey-balanced text (never
pure black); orange as the single hot accent, deep aubergine for destructive.

## 2 · Ledger classification

- **OBSERVED:** palette values and usage statements; font family/licence;
  brand values (voice); cool-grey banner practice.
- **INFERRED:** UI role mapping; rounded/pill form language; ledger row
  treatment; community-leaning emphasis; word-first status.
- **AUTHORED:** hover shades; shadow softness; screen type sizes; notice
  tints; dialog structure.
- **UNDEFINED (carried deliberately):** motion; searchable selection beyond
  small sets; multi-hue data coding; busy states.

## 3 · Elements → pack (summary; full specs in `packs/indaba/artifacts.json`)

Components (12): `masthead` · `action` (pill; primary/secondary/destructive) ·
`field` · `choice` (small sets only) · `status` (word-first pill) · `label`
(soft pill) · `surface` (soft shadow / tinted) · `ledger` (airy soft list) ·
`meter` (rounded, readout) · `notice` (warm / orange tint) · `dialog`
(rounded confirm over warm scrim) · `section`.

Patterns (4): `shell` · `register-view` · `form-flow` · `activity-view`.
Token-sets (2): `palette` · `type`. Guidelines (2): `roundness` · `voice`.
Reference (1): `ubuntu-brand`.

**Rules:** IND-1 rounded-language (errors on square corners) · IND-2
palette-only colours · IND-3 text never pure black · IND-4 status word-first.
**Prohibitions:** `prohibit/square-corners` · `prohibit/off-palette-colours`.
**Fallbacks:** `platform-controls` · `plain-region`. **Recipes:**
`retire-confirm` · `import-progress` · `item-intake`. **Validator:**
`indaba-lint` (pack-local, kernel-orchestrated via `{pack}` — the KCL-001
mechanism from `03`).

## 4 · Gate record

1. **ST (style tile)** — tile v0.1 → reviewer: “Looks good.” (after two
   revisions: masthead enlarged to a full-bleed dark grey banner `#333333`;
   the invented dot stripe under the banner removed as not-Ubuntu).
2. **Screens (pre-build)** — register/detail/form/activity/confirm + mobile,
   rendered with font-gated real Ubuntu fonts → reviewer: “Ok approved.
   Close enough.”
3. **Pack** — `packs/indaba/` encoded by hand; golden **10/10** across all
   five resolution outcomes on the **unmodified kernel**.
4. **Agent build test** — `benchmark/runs/indaba-a1/` (fresh agent, sandbox
   mounts ONLY `packs/indaba`), then host validation + probes + report
   (`11`, `12`).
