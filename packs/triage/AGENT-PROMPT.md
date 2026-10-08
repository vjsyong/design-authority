# Implementing with the Triage authority — a prompt for coding agents

You are building an interface with the **Triage design authority** (`packs/triage`,
v0.12.1) — the app-agnostic, paper-and-ink UI system with one token source, one
component runtime, and one enforceable lint gate. This prompt is for *consuming*
the authority in a product build. (Working *inside* the triage repository itself
is governed by its own `AGENTS.md`.)

Paste everything below into the agent's context before it writes UI.

---

## The brief

Build the requested screens using the Triage design authority at `packs/triage`.
Do not invent visual decisions the authority already records, and do not silently
skip ones it does not.

## How to work (the consumption protocol)

1. **Resolve before you design.** For every element you need, ask the authority
   first and follow its answer:

   ```
   python3 tools/da.py --pack packs/triage resolve "a primary button" --json
   python3 tools/da.py --pack packs/triage resolve "a settings page" --json
   ```

   Outcomes:
   - `RESOLVED` → build exactly what the cited record defines (states, class,
     a11y notes included).
   - `CONFLICT` (e.g. asking for rounded corners) → do **not** build it as asked;
     use the sanctioned alternative the answer names.
   - `FALLBACK` → build the documented fallback variant.
   - `UNDEFINED` → build in the system's character, then follow step 3.

2. **Load the system the sanctioned way** (global path):

   ```html
   <link rel="stylesheet" href="tokens/tokens.css">
   <link rel="stylesheet" href="core/base.css">
   <link rel="stylesheet" href="core/patterns.css">   <!-- if you use page patterns -->
   <script src="core/components.js" defer></script>
   ```

   Or the scoped path (`.triage` wrapper + `core/scoped.css` + `core/reset.css`)
   when embedding into a host page — see `guideline/consumption`.

3. **Mark what is not covered.** When the authority is silent (`UNDEFINED`),
   build the closest in-character thing, mark the spot in the DOM, and file a
   gap record. Never present improvisation as canon.

4. **Verify before you claim done.** Render the result and check it: the
   verifier inspects the artifact, not your summary. Run the pack's golden set
   and any project verification before reporting.

## House rules that must survive your build

- **Tokens only.** No raw hex/rgb/hsl, no off-scale spacing, no ad-hoc
  durations. Values change in `tokens/tokens.json` and nowhere else
  (TDS002 / TDS005 / TDS006 / TDS009).
- **Squarely squared.** Corner radius stays 0; any rounded request is a
  `CONFLICT` (TDS003 / `prohibit/off-radius`).
- **Focus always visible.** Never remove focus outlines; `:focus-visible`
  affordances are mandatory (TDS004).
- **System fonts only** (TDS008) and **every control has an accessible name** —
  icon-only means `aria-label` (TDS015, TDS014 for images).
- **Destructive actions are never one-click.** Armed two-step delete, or
  `confirm()` for one-way actions (INT001 / INT002).
- **Feedback uses the three sanctioned channels** — banner / toast / empty
  state — nothing ad hoc (INT003).
- **Editors keep a save bar** with explicit unsaved state (INT004).
- **Degrade without JS.** Every component must work as plain markup; the
  behaviour layer is additive (`fallback/no-js`).

## What good output looks like

- Components instantiated with their documented classes and states (check each
  `component/*` record for the exact `class`, `states`, `verify` selectors and
  `a11y` notes).
- Layouts composed from the sanctioned patterns (`pattern/dashboard`,
  `pattern/viewer`, `pattern/settings`, …) rather than invented shells.
- A short build note listing: every ask you resolved (with outcome), every
  improvisation you marked, every gap you filed.

## Quick reference (most-used records)

| Need | Resolves to |
|---|---|
| button / cta | `component/btn` |
| switch / toggle | `component/px-sw` |
| table | `component/tbl` |
| dialog / modal | `component/dlg` (native dialog) |
| toast / flash | `component/toast2` / `component/msg` |
| empty state | `component/empty` |
| date picker / combobox | `component/dp` / `component/cb` |
| command palette | `component/cmd` |
| dashboard / settings / detail page | `pattern/*` |
| colour / spacing / type tokens | `token-set/*` |

The full catalogue: `packs/triage/artifacts.json` (51 records), the enforceable
rules: `packs/triage/rules.json` (TDS001–TDS015 + INT001–INT004), the
conformance questions: `packs/triage/golden.json` (36 cases, all passing).
