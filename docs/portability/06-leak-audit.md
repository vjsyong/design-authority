# Portability Spike · 06 · Leak audit & rejection record

**Reviewer outcome (2026-10-07): REJECTED.**

> “Definitely looks like triage is leaking through. From the buttons to the
> layout and the chips. Reject”

This audit verifies the rejection, identifies exactly what leaked and why,
withdraws the spike’s portability verdict, and sets the remediation path.

---

## 1 · What is *excluded* (so the diagnosis is precise)

The rejection is **not** mechanical contamination:

- Sandbox mounts: only `packs/orbit` (+ kernel + MCP launcher). Triage files
  were absent from the run.
- Transcript: the string “triage” appears **0 times**; containment attempts 0;
  cross-reference probes across all three authorities show zero cross-cites
  (`data/divergence-probes.json`).

So the leak did not come *through the kernel*. It came **through the authoring
of the second authority itself** — i.e., through me, the person who also
knows Triage by heart.

## 2 · Anatomy diff — Orbit v1 vs the incumbent (Triage) {#anatomy}

Compared against Triage’s actual CSS (`src/core/base.css`,
`src/core/additions.css`) and the Procura screenshots
(`benchmark/runs/c2/capture/screens/`):

| Orbit v1 element | Orbit v1 specification | Triage actual | verdict |
|---|---|---|---|
| `command` | secondary = 1px ink-border button; primary = solid fill; destructive = accent-text + accent-border outline button | `.btn` = 1px border button; `.btn.primary` = solid fill; `.btn.danger` = status-color text, border on hover; `.btn.ghost` | **structural twin** |
| `tag` | square micro-label, 1px gray border | `.chip` = inline border label, hover border; `.badge` family same anatomy | **twin** |
| `panel` | 1px border content region | `.card` = 1px border container | **twin** |
| `register` | header row + 1px hairline row separation + right-aligned actions | `.tbl` = hairline `border-bottom` rows, right-align class; `.tbl.mcards` = stacked label/value on mobile | **twin** (incl. the mobile stacked-table pattern) |
| `dialog` | 1px border, header band (title + Close), body, right-aligned footer commands | `.dlg`/`.dlg-h`/`.dlg-b`/`.dlg-f` = border + header w/ border-bottom + footer right-aligned | **twin skeleton** |
| `entry` | label above, 1px border input, focus ring, error line | bordered inputs, `label` block above, focus border + ring | **twin** |
| `indicator` | 6px square marker + text label (tones: ink/gray/accent) | colored square dot + text (status squares) | **twin** |
| `notice` | bordered block, kind variants | `.toast2` = dark plate, status-colored edge | close family |
| `band` | white top band: brand left, nav, meta right | `.topbar`/sidebar: same generic appbar grammar | genre-typical |
| `gauge` | bordered track + fill | — (no direct twin) | genuine

Two visuals side by side settle it: the Depot register (capture
`orbit-a1/capture/register.png`) reads as a **re-skin of the same system** as
the Procura screens (`c2/capture/screens/dashboard-desktop.png`) — same
button hierarchy, same bordered micro-labels, same hairline tables, same
stacked mobile adaptation, same page-head title+action pattern. The
differences are paint: accent hue, type family, square vs slightly rounded.

## 3 · Root cause

1. The source manual grounds **color, type, and grid** — extensively, with
   page cites (foundations are genuinely source-derived).
2. The manual says *nothing* about buttons, chips, cards, dialogs, inputs.
   Those blanks were filled **from the author’s priors** while Triage-fluent,
   then labeled INFERRED/AUTHORED — an epistemically honest label applied to
   a **design-unverified** decision. Honest labels are not a distinctness
   argument.
3. Every one of those priors defaulted to the incumbent’s grammar: border
   controls, bordered micro-labels, hairline tables, header/body/footer
   dialogs. Not one element was forced to argue “here is why this is *not*
   Triage.”
4. A convergence risk was even noted in passing during derivation (ledger F1:
   “Triage independently prohibits radius…”) and was **not escalated to a
   gate**. Process gap.

**Consequence:** success criterion #1 (“a visually different authority can be
represented”) **fails**. A Triage-shaped second authority cannot test the
research question (“kit-agnostic kernel, or Triage machinery behind a generic
interface?”) — if authority #2 is Triage’s skeleton in NASA paint, the kernel
being able to serve it proves little. The `05` verdict is **withdrawn**;
operational status is **INCONCLUSIVE / rejected test premise** until a
genuinely distinct authority #2 exists.

## 4 · Remediation plan — Orbit v2 with enforcement gates

Keep the (source-grounded) foundations; re-derive the **element layer and
layout grammar** under anti-leak constraints, exploiting manual material not
yet mined (this is both more faithful to the manual *and* structurally
different from Triage):

**Ground rules to exploit (manual-cited):**

- “Avoid the use of borders or other types of artificial embellishment”
  (p46) + “outline boxes… around technical diagrams” only (p41) → **no
  decorative borders**: separation by rules, bands, spacing.
- White-on-dark application rules (p8) → inversion as a primary device.
- Signage classes: identification / directional / informational / regulatory
  (p45–46) → feedback and navigation semantics.
- Publication grid grammar: white band for folios/headlines (p41), numbered
  sections, captions under figures (§5.x), 2–3 column format families
  (p41–44) → page composition.
- §4 forms (not yet extracted) → input/field grammar.

**Concrete divergences to derive (each needs its own evidence line):**

- actions: filled plates + text-command grammar — **not** a border-button
  family; no outlined buttons at all;
- inputs: **ruled-line fields** (rule-based, paper-form grammar) — not boxes;
- feedback: **full-width bands** (signage zones) — not floating bordered
  boxes;
- data: numbered register with section rules, folio line — not zebra/tile
  tables;
- boxed content only as **captioned figures**;
- modal: **darker plate** (white-on-dark rule) rather than white card dialog;
- gauge: segmented block meter;
- typography-led hierarchy (Light display / Medium labels).

**Gates (the actual fix — process, not taste):**

- **G1 anatomy diff:** every element ships with an explicit “not the
  incumbent” divergence argument against Triage’s anatomy table (§2), and is
  reviewed by an adversarial subagent (assume-rejection, as in the evolution
  experiment).
- **G2 reviewer gate:** mock screens go to the reviewer **before any agent
  run**. Pre-registered: if it fails the reviewer’s eye again, the source kit
  is swapped (NYCTA / EPA) rather than iterated further.
- **G3 lesson out:** “square + monochrome + minimal” is not distinctness;
  convergence findings block until resolved. Added to the skill and to the
  derivation protocol.

**Also fixed for the record:** the previous `05` decision
(`PORTABLE-WITH-GENERIC-CHANGES`) is re-scoped to *mechanical* portability
(load/serve/resolve/validate — still evidenced) but **may not be cited** as
the spike’s final verdict until v2 passes the reviewer gate.
