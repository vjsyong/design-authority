---
name: synthesize-authority
description: Use when building a Design Authority pack from a brand kit, a live product, or other design precedent. The full synthesis pipeline: evidence, human gates, compilation, calibration, and governance.
---

# Synthesize an Authority (brand kit → enforceable pack)

Use this when asked to turn design precedent (a brand kit, a live product, a documented system, a deployed site) into a Design Authority pack under `authorities/<name>/` (each authority is its own repository; see `authorities/README.md`). The deliverable is a pack agents resolve against, not a style guide for humans.

The method was proven three times (Mailchimp → wink, The Economist → leader, Canada FIP → dominion). Working records: `docs/synthesis/10-synthesis-process.md` (the method), `docs/synthesis/01-synthesis-protocol.md` (stage table and gate formats). Read both before starting a derivation.

## Hard rules

- **Quarantine.** One isolated context per source. Fresh fetches only. Never feed the incumbent system's visuals into the derivation; never prompt "avoid X" (negative priming is itself a leak). Never mix one source's evidence into another's derivation.
- **Evidence before design.** Tag every claim OBSERVED / INFERRED / AUTHORED / UNDEFINED and cite the URL or screenshot. Weak evidence becomes UNDEFINED, not filler.
- **Fetch the product layer, not just the brand layer.** Brand documents are austere and aspirational; the live product shows the real radii, interactive colour, focus states, rings and shadows. Probe computed styles; capture borders and box-shadow explicitly (a fill-and-radius-only probe once missed a 1px ring and a hard hover shadow).
- **Humans own the gates.** Machines do evidence, derivation, compilation, CI. The reviewer decides at three gates and never writes schema; the machine never self-approves a gate.
- **The compiler refuses unaccepted decisions.** UNDEFINED ships as gaps or fallbacks, never as canon.

## Pipeline

1. **Source selection.** Score candidates on maximum stylistic divergence AND evidence access (live product reachable, docs public). Drop bot-walled or unobservable sources up front.
2. **Evidence inventory.** Screenshot-first, domain-partitioned extraction: load the companion skill `skills/extract-design-evidence/SKILL.md`. Output: `docs/synthesis/<src>/00-evidence-inventory.md`.
3. **Gestalt model + Gate 1.** Model the character (principles, colour/type/shape/density/surface/motion, and what the system avoids), render a style tile (`docs/synthesis/tools/render_tile.py`), and get APPROVE / REVISE / REJECT on named axes (corners · contrast posture · marker shapes · palette warmth · density) BEFORE any component work. Anatomy gates cannot repair a gestalt collision. Record corrections verbatim.
4. **Decision extraction.** `docs/synthesis/<src>/decisions.json`: every semantic decision carries Decision · Status · Evidence · Confidence · Reasoning · Alternatives · human-confirmation flag. This file is the machine source of truth for everything downstream.
5. **Semantic review + Gate 2.** Render the grouped decisions for review (`docs/synthesis/tools/render_decisions.py`, review app in `docs/synthesis/review-app/`). Per uncertain decision: ACCEPT / MODIFY / REJECT / LEAVE UNDEFINED. Autosave every verdict; a sheet that can be "completed" without saving will be.
6. **Compile.** `python3 docs/synthesis/tools/compile_pack.py --src <name|all>` reads the source's `decisions.json`, checks acceptance against the review app's `data/feedback.json`, and emits `authorities/<name>/` (artifacts, rules, recipes, prohibitions, fallbacks, goldens). It asserts every compiled decision was accepted.
7. **Calibrate.** `python3 tools/da.py --pack authorities/<name> golden --file authorities/<name>/golden.json` to 100% agreement by tuning the PACK (aliases, recipe `needs`), never the kernel or the thresholds. Then run a coverage sweep: an element-by-element file of natural-language asks authored from the SOURCE's own information architecture, asserting every ask reaches its element. Golden sets share the extractor's blind spots; only an assertion-driven sweep makes misses loud.
8. **Reference build + Gate 3.** Build one reference app under the new authority (same brief across sources), capture it, get APPROVE / REVISE AUTHORITY / REJECT SYNTHESIS. Ship a verification contract with the pack (`verification.json`; method in `docs/verification/`) and run `python3 tools/da_verify.py --pack authorities/<name> --target <reference-build> --out .verify` to 0 violations. Corrections are factual evidence: re-ground and revise, never defend the derivation.
9. **Stress the pack (optional but proven).** Pick an app whose required elements sit outside the canon; resolve every required element against the pack; for each UNDEFINED, search synonyms and inspect before declaring a gap; then build one variant per authority with identical copy and fixtures, marking improvisations (`data-improvised` + a gap file). Expect 10 to 15% direct coverage on off-domain apps and rely on the mark-and-gap loop for the rest.
10. **Governance.** After shipping: gaps (filed by agents) → independent adjudication → proposals (`python3 tools/da.py propose`, six required fields including `tests`) → owner verdicts (`python3 tools/da.py review --verdict accept|reject|needs-info`) → codify accepted work with `python3 tools/apply_proposals.py --workspace <ws> --pack authorities/<name>`. Rejections and no-actions become negative precedents with reasons, alternatives, and scope verdicts (`governs` / `outside` / `ambiguous`).

## Pitfalls (each paid for once)

- A text-only, single-context pass extracts "canon" from stylesheet text instead of from the artifact as rendered; it fabricates. Screenshot-first, computed-style probes, evidence tags, always.
- Prohibition signals are substring matches: cover real phrasings ("make the buttons square" does not contain "square buttons").
- Run the pack validator and goldens after every compile; a pack that passes goldens can still fail the full battery (`./tools/check.sh`).
- Reviewer corrections are evidence with receipts. Apply directive notes literally and flag them; do not average them with earlier guesses.
- Never reset a shared review surface mid-session, and tests must never write to live review records.
- Codification aliases: derived goldens fail when an entry lacks the phrases its own checks promise. Extend aliases faithfully to the entry's intent; never loosen kernel thresholds to make goldens pass.
