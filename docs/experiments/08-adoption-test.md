# 08 · Independent adoption test — a fresh agent discovers and runs the whole workflow

Status: **findings record** (2026-10-11). Owner memo (da_nextsteps.md
section 4): repeat the consumer-flow test after the integration work, with
stronger isolation — public repository, installation instructions, and a
short brief only; no internal history, no walkthroughs.

## Protocol

- **Runner:** `docs/experiments/tools/x06_run.py` (bubblewrap containment
  with no internal mounts, no tools, no packs; network only). Brief:
  `docs/experiments/adoption/BRIEF.md` — clone the public repo you are told
  about, set it up, build a recipe-box app under it (list, empty state, save
  confirmation, mark-tried, a confetti burst that "feels like the app's own
  character"), handle anything undefined the way its docs prescribe, write
  DONE.md.
- **Run:** `run1`, model `deepseek/deepseek-flash` (same as x05), wall 935 s,
  exit 0, transcript 276 events (75 bash, 24 read, 9 write, 3 edit).
  Workspace archived at `~/x06-adoption/run1/`.
- **Containment audit:** zero host-only path hits in tool inputs; the
  sandbox never saw the meta repo, packs, skills, or any internal
  material. Both public clones were left untouched (`git status` clean).

## What it did (verified)

1. Followed the public **Use now** flow exactly (clone, venv + `mcp<2`,
   clone the Triage pack, run the pack's proof commands, note the version).
2. Found and used the whole **consumer workflow** (docs/17), unprompted:
   `da init` -> `da plan` (9 RESOLVED with record ids, 3 UNDEFINED with
   case stubs) -> build on the pack's byte-identical `dist/` foundations ->
   `da receipt-new` + filled claims -> `da receipt-check` ok ->
   `da reconcile` (9 conforms, 0 rectify).
3. Handled three genuinely undefined needs exactly as the protocol
   prescribes: a card and a text field (classes ship, no catalog record),
   and the confetti burst — for which it designed an in-character
   improvisation (square ink flecks, radius 0, the app's own palette and
   motion tokens, `prefers-reduced-motion` honoured), marked it in code and
   recorded it as a provisional solution. No candidates existed; it said so
   instead of inventing authority.
4. Filed **five gaps**, including two real product gaps (below). It
   refused to fake either: it ran the authority's `validate` as-is (honest
   error), wrote a clearly *labelled substitute* linter, and substituted
   the missing verifier with its own honest checks.
5. Verified its build for real: 21/21 headless-DOM checks and a Chromium
   render/interaction pass (computed styles match the tokens; light/dark;
   armed delete; toasts; confetti particles: 18; zero console errors), with
   screenshots in `build-notes/`.

**Independent re-check (this record's evidence):** the contract artifacts
(lock, plan, cases, receipt, reconciliation, gaps) re-parse and match its
claims; the app was re-run through the **real** authority linter from a
pack copied to a neutral path with no snapshot available: **0 findings,
score 100**. Its substitute checker was truthful for the app; the two
errors a full-workspace scan shows are TDS014 false positives on the
checker's own regex literals (a scanner-versus-its-own-source nit, noted
upstream).

## Findings and fixes

- **F-1 (fixed same day): the pack's lint validator was unusable for
  consumers.** `validators.json` ran the lint from the design-system
  checkout (`{snapshot}`), which is not public, so `da validate` errored
  out for every consumer while printing a vacuous score. Fix: the pack now
  ships a **self-contained lint bundle** (`lint/`, `spec/rules.json`,
  `tokens/tokens.json`, `rename-map.json`, `core/`, `VERSION`) and runs it
  with `workdir {pack}`; the generator emits the bundle and the drift gate
  covers it (16 files + `core/`). Verified from a copied pack with no
  snapshot: validator ok, real findings.
- **F-2 (queued): the Triage pack ships no verification contract**, so the
  workflow's `da verify` step aborts (`FileNotFoundError`). The run's gap
  records it. Fix queued: author and calibrate a Triage contract
  (references/verification.md discipline: calibrate against a clean build,
  never loosen checks) and ship it in the pack.
- **F-3 (noted): semantic extras off by default** — `da discover` is
  unavailable without `fastembed`/`numpy`; the agent used the documented
  recovery (paraphrase -> UNDEFINED -> canonical vocabulary -> RESOLVED).
  No change; behaviour matches the docs.
- **F-4 (noted): the README quotes pack version 0.12.1 while the pack
  ships 0.12.2**; harmless, folded into the next docs pass.
- **F-5 (noted): shipped-but-uncatalogued classes** ("a card", "a text
  field") — real corpus gaps the run filed; candidates for the Triage
  repo's normal review route alongside the recipes promotion batch.

## Verdict against the memo's axes

- **Did it consult the authority?** Yes, heavily and correctly: 16 CLI
  calls including resolutions it then cited in the build.
- **Are its claims valid?** Yes — every headline claim re-verified
  independently (artifacts parse, app clean under the real lint, checks and
  screenshots reproducible from the archive).
- **Human intervention:** zero. Headless, brief-only; unlike the earlier
  consumer-flow test, no owner in the loop.
- **Tooling-failure recovery:** yes — three degraded paths (broken
  validator, missing contract, missing semantic extras) handled with
  honest substitutes and filed gaps, never faked green.

This run is evidence for the memo's distinction: a fresh agent, given only
the public repo and a brief, found and completed the intended workflow
without help. The two blockers it hit were product gaps, not comprehension
problems — and one of them is already fixed.

## Materials

- Brief: `docs/experiments/adoption/BRIEF.md` · runner/eval:
  `docs/experiments/tools/x06_run.py`, `x06_eval.py` · run archive:
  `~/x06-adoption/run1/` (DONE.md, build-notes with raw logs + screenshots,
  `.design-authority/` with the full contract).
