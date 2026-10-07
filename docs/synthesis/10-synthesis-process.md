# Phase 3 — Authority Synthesis: the method

The question this phase asked: *can a machine-guided process turn messy, incomplete
design evidence into candidate Design Authorities that stay faithful to their
sources, without collapsing into one generic design language?*

Answer after three full passes: **yes, with named failure modes and a fixed set of
guardrails** — the pipeline below is the deliverable, not the three packs (those are
its output and its proof).

## The pipeline (as actually executed)

1. **Source selection.** Candidates scored on two axes: *maximum stylistic
   divergence* and *evidence access* (live product + public documentation). Evidence
   access was a first-class criterion — sources that could not be observed directly
   or that resisted polite programmatic access were dropped (TfL bot-walled,
   Duolingo/Headspace not officially public). Selected: Mailchimp (wink),
   The Economist (leader), Canada FIP (dominion).
2. **Quarantine.** One isolated derivation context per source; fresh fetches only;
   never feed Triage/Indaba visuals; source-positive prompts (never "avoid X" —
   negative priming is a leak channel); memory house-style directives explicitly
   excluded. Result: zero cross-source references in all three packs (audited).
3. **Evidence before design.** Every claim tagged OBSERVED / INFERRED / AUTHORED /
   UNDEFINED from the start; raw extracts archived; the reviewer's Gate-2
   screenshots treated as first-class evidence.
4. **Gestalt before anatomy.** Per source: gestalt model → style tile → reviewer
   gate on named axes (corners · contrast posture · marker shapes · palette warmth ·
   density) *before* any component work. Anatomy gates cannot repair a gestalt
   collision.
5. **Decision extraction.** `decisions.json` per source: id, area, decision text,
   status, evidence, confidence, alternatives, review flag — the machine-readable
   source of truth for everything downstream.
6. **Review.** Interactive review app (per-card verdicts + notes + image evidence,
   autosave). Two working passes caught **19 misfits** across the three systems;
   every correction was applied, re-verified, and re-checked.
7. **Compilation.** `tools/compile_pack.py` transforms *accepted* decisions into
   kernel-format packs — artifacts, rules, recipes, prohibitions, fallbacks, golden
   sets. The compiler **refuses to compile any decision that was not accepted**;
   undefined decisions ship as honest gaps (UNDEFINED/fallback behaviour).
8. **Verification.** Per-pack golden sets (29 cases total, 100%) + the standing
   battery (kernel tests, triage golden, MCP smoke, pack drift) with the kernel
   **unmodified**.

## Lessons that were paid for (in order of cost)

- **Fetch the product layer, not just the brand layer.** The single biggest fidelity
  failure: deriving from brand documents (austere, square, restrained) while the
  living products use soft radii, blue interactive layers and component realism.
  Marber *does* publish components/shadows/errors/spacing — we hadn't fetched them.
  Mitigation now standard: fetch the component/spec layer **and** probe live
  computed styles. Probe borders and box-shadows explicitly — the wink CTA's 1px
  ring and hard offset shadow were invisible to the first probe because only
  fill/radius/colour were captured.
- **Reviewer screenshots are evidence, not opinions.** Gate-2 rejections
  ("The Economist uses rounded corners", "has a blue glow and rounded corners")
  were factual corrections with receipts. The right response is to re-ground and
  revise, never to defend the derivation.
- **Reviewer language is directive — apply it literally and flag it.** "Rounded
  corners, sans-serif font, no border highlighting" (L-11) means exactly that for
  the field under review. Where a note is ambiguous, apply the most literal reading,
  mark it, and invite correction — do not average it with your own earlier guess.
- **Autosave everything, everywhere.** A review instrument that can be "completed"
  without saving will be: the reviewer finished wink on a build with per-card Save,
  nothing persisted, and a mid-repair cleanup wiped the one item that had been
  saved. Instruments must persist per action (verdict → POST, notes debounced,
  images on attach). Never run CLI resets against a live review surface; tests must
  not write to live review IDs.
- **The compiler should refuse to lie.** Assertions in the compile step (every
  emitted decision must be Gate-2-accepted) are cheap and turn the pipeline's
  honesty principle into executable policy.
- **Tune goldens against the matcher, not the other way round.** Golden phrasings
  exercise the real resolution path (alias phrases, signal substrings, scope
  tokens); where a case missed, the fix was in the pack lexicon or signals — the
  kernel stayed frozen.

## What generalizes vs. what stays artisan

- **Generalizes:** the pipeline order (select → quarantine → evidence → gestalt gate
  → decisions → review → compile → golden), the quarantine rules, the decision
  schema, the compiler scaffolding, the review instrument, the refusal-to-compile
  assertion, the golden-tuning loop.
- **Artisan, for now:** the mapping tables (decision → artifact/rule/fallback
  structure) are authored judgment, per source, ~1 hour each. This is the honest
  boundary: the machine formalizes what a human decided is true, and it can verify
  it, but deciding the mapping still needs taste plus the source in front of you.

## Revision economy (honesty check)

Per source: gestalt gate 1 pass; decision review 2–4 passes concentrated on
rejections (leader needed three rounds on corners/colour because the first two
revisions under-rotated toward the live product); zero re-opened items after final
acceptance. 8 reviewer screenshots + 2 live-style probes carried every correction.
