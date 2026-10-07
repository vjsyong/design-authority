# Portability Spike · 08 · Contamination audit (reviewer hypothesis check)

**Trigger:** reviewer rejected Orbit v2 as well (“still leaking… the dots are
triage so are the sharp corners and high contrast”) and asked whether
**subagent prompts** or **skills** may be leaking through.

**Verdict up front:** the reviewer’s instinct is substantially correct.
There is no sandbox leak — but there *is* a verified **skills-layer channel**
(including an active, auto-distilling curator subsystem) plus a **memory
house-style directive**, plus **same-session context** and, structurally, a
**gestalt collision** between this kit’s fundamentals and the incumbent.
Details, receipts, and fixes below.

## 1 · Channel-by-channel findings

### 1.1 Sandbox / agent run — CLEAN (verified)
The orbit-a1 build ran with only `packs/orbit` mounted; the string “triage”
appears 0 times in its transcript. Not a channel. (Established in `06`.)

### 1.2 Subagent prompts — review-only; NOT a design-authorship channel
Every design artifact in this spike was authored by **(a)** me (derivation
docs, Orbit v1/v2 specs, v2 mock) or **(b)** the sandboxed opencode agent
(the Depot build — context contained no Triage). Subagents were used only for
**reviews** (evolution-experiment reviewer; G1 now). They cannot have leaked
designs into artifacts they never wrote. Secondary effect, real but minor:
my review prompts describe Triage to reviewers, biasing *verdicts* (not
artifacts), and reviewer subagents can *read* the skill library (G1 loaded
`authority-portability` mid-review).

### 1.3 Skills — CONFIRMED CHANNEL, with an active auto-distiller
**Pre-existing corpus (standing Triage-convention reservoir):**
`design-authority` (tags include “Triage”; ships `references/triage-map.md`,
a full Triage corpus map), `web-ui-conventions`, `ui-improvement-loop`,
`mail-triage`, `design-kit-extraction` (related). Any derivation step that
loads these inherits Triage-shaped conventions.

**Live auto-distillation (new finding):** two skills were created
*from this working session* while it was still running, without my
`skill_manage` calls:

| file | created | note |
|---|---|---|
| `software-development/authority-portability` | 09:21:44 | distills this session’s portability state (NASA, `packs/orbit`, ledger open) |
| `software-development/anti-leak-design-derivation` (+`references/`) | 10:05:08 | distills the v1-rejection→v2 process **including my internal critic-filtering notes — material that existed only in live session context** |
| `design-authority/SKILL.md` (updated) | 09:22:02 | project-resume skill refreshed |

**Mechanism:** a Hermes background subsystem with LLM backing — the skills
**curator** (`curator:` section in `~/.hermes/config.yaml`;
`skills.creation_nudge_interval: 15`; backups in `~/.hermes/.curator_backups/`
whose blobs at 09:44–10:05 match these and my own skill writes). The curator
is enabled and operating **in near-real time on live session state**.
**Exclusions checked:** G1 subagent did not write them (0 `skill_manage`
calls; it only `skill_view`ed them); no delegation was alive at 09:21; no
cron job other than the curator matches.

**Implication:** the skill library grows from whatever sessions contain. In a
Triage-fluent working context, that grows Triage-shaped conventions into
evergreen context. For “derive something new” work this layer must be
quarantined.

### 1.4 Memory — CONFIRMED CHANNEL (standing directive)
Persistent memory carried: *“UI: mail-triage design system for ALL apps…”* —
a standing instruction aligning **all** UI work to the Triage design system.
**Fixed this session:** re-scoped to “for apps” + explicit *“EXCLUDED from
design-authority derivations”*.

### 1.5 Same-session context — LIKELY CONTRIBUTOR
The leak audit (`06`) required reading Triage’s actual CSS (`.btn`, `.chip`,
`.tbl`, `.dlg`) in-session; the v2 mock was authored **minutes later in the
same context**. No firewall existed between “stare at incumbent’s anatomy”
and “design the alternative”.

### 1.6 Structural — the gestalt collision (why v2 still failed)
v1 → v2 fixed the **component-anatomy layer** (border family, chips, dialog
skeleton — all now provably divergent). The reviewer reads a different
layer: **gestalt** — the axes he named are *square corners*, *high contrast*,
*marker-dot vocabulary*. On those axes, NASA-reported fundamentals
(black/white/red, rectilinear, maximal contrast) sit in the **same visual
region as the incumbent** — and both sit in the region LLM-default minimal
systems collapse into. Anatomy gates cannot fix a gestalt collision. This is
the layer error in v1/v2: I gated the wrong layer.

## 2 · Consequence

- v2 is **rejected** on record (07 banner added); the pre-registered
  escalation stands: **swap the source kit — do not iterate on these priors.**
- Recommendation: **Ubuntu brand guidelines** (Canonical). Rationale: it
  inverts all three named axes with brand-grounded evidence —
  *corners:* Ubuntu type/identity support rounded, humanist form language
  (vs. rectilinear); *contrast/colour:* warm aubergine–orange–warm-grey
  palette (vs. near-black + single alarm red); *markers:* circular motif
  vocabulary (vs. square dots). Alternative: NYCTA (multi-hue wayfinding) —
  held as backup because it retains the black/white/Helvetica high-contrast
  base, which risks the same gestalt read.
- Derivation rules change (quarantine + gates):
  1. **No Triage-content when deriving:** do not load `design-authority`,
     `triage-map.md`, `web-ui-conventions`, `ui-improvement-loop`,
     `mail-triage` into derivation contexts; never read the incumbent’s CSS
     during derivation (audits only, deliberately separated).
  2. **Source-first kit reads** (Ubuntu brand pages fetched fresh, judged on
     their own evidence).
  3. **ST gate — style tile first:** palette/type/shape-vocabulary tile goes
     to the reviewer **before any screen design** (cheapest place to catch a
     gestalt miss).
  4. Gestalt checklist for review, using the reviewer’s own vocabulary:
     corners · contrast posture · marker shapes · palette breadth/warmth ·
     density.
  5. Skills-curator note: curator writes are acceptable for project memory
     but must never be treated as derivation input; consider pausing it for
     spike work if it proves noisy.

## 3 · Evidence index

- Skill mtimes/content: `~/.hermes/skills/software-development/{authority-portability,anti-leak-design-derivation,design-authority}`
- Curator backups: `~/.hermes/.curator_backups/blobs/` (matched to skill writes)
- G1 log (skill reads only, no writes): `~/.hermes/cache/delegation/live/deleg_aa7c81b8/task-0.log`
- Config: `~/.hermes/config.yaml` (`curator:` enabled; `skills.creation_nudge_interval`)
- Prior: `06-leak-audit.md`, `07-orbit-v2.md`

## Addendum — G1 adversarial result (Orbit v2), 10:15

G1 returned **PASS-WITH-FIXES** (zero structural twins — verified by live-DOM
computed styles + pixel sampling; eight WEAK residuals; ~75–80% confidence
the gate would pass after three fixes). Crucially, it **independently flagged
two of the reviewer's three named axes** — the 5px square marker (= the
incumbent dot+label device) and the high-contrast black plates (= the
incumbent's primary paint) — but graded them *fixable WEAK residuals* while
the reviewer failed the same artifact instantly on gestalt. Lesson, now a
hard rule in the skill: **anatomy gates under-weight gestalt; the reviewer's
named axes are hard-fail criteria in any internal gate, and gestalt is
settled before anatomy work.** Full verdict + 44 KB trace:
`data/g1-orbit-v2-verdict.md`, `data/g1-orbit-v2-transcript.log`.
(Its render-fidelity notes — font substitution in the old mocks; scrim
covering only the content column — are moot for the retired NASA line and
carried into the v3 renderer checklist.)
