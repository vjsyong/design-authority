# Pilot report — A vs B vs C (single-shot, PRELIMINARY)

**Status: preliminary.** One run per condition (a1 / b1 / c1), produced while
the instrument was still being hardened (deviations D-1…D-4 in
`docs/06-preregistration.md`). Production = 3 fresh runs per condition under
the frozen protocol; this report is directional and will be superseded.
No composite score — dimensions are reported independently, as designed.

- Model: `deepseek/deepseek-flash` · App: Procura (frozen starter + seed data)
- Pristine starter baseline: lint 10 (1 error / 9 warning) · 6 hex · 4 px ·
  3 classes · 0 inline styles
- All three runs: exit 0 · functional checks 13/13 · 0 console errors ·
  UI files 7 · backend files 0

## D1 · Design compliance (triage-lint, introduced findings)

| run | authored (e/w/i) | delta vs baseline | by rule |
|---|---|---|---|
| A | 158 (44/103/11) | +154 | TDS002 72 · TDS003 40 · TDS013 30 · TDS006 8 · TDS007 3 · TDS009 2 · TDS005/8/12 1 each |
| B | **0** | −10 (baseline eliminated) | — |
| C | **0** | −10 (baseline eliminated) | — |

A built a coherent but wholly bespoke UI (0 system classes used); B and C
leave the linter with nothing to say, matching the system's own dogfood bar
(100/100).

## D2 · Design drift

| metric | A | B | C |
|---|---|---|---|
| unique hex colours | 36 | 1 | 0 |
| px spacing values | 27 | 0 | 0 |
| border-radius decls | 10 | 0 | 0 |
| `!important` decls | 6 | 0 | 0 |
| inline style attrs | 36 | 18 | 3 |
| distinct classes (scanner) | 198 | 150 | 134 |
| system classes used (templates) | 0 / 161 | 116 / 139 | 102 / 112 |
| custom classes introduced | 161 | ~12 | ~3 |

B's single hex is `<meta name="theme-color" content="#fafafa">` — the system's
paper colour as a necessary literal, not drift. B's 18 inline styles are all
token-referencing (e.g. `style="width:{{ percent }}%"`); C has 3.

## D3 · Authority behaviour (C only; availability differs by design)

43 tool calls: `resolve_design_problem` 16 · `inspect_artifact` 13 ·
`search_authority` 7 · `validate_implementation` 2 · `report_gap` 2 ·
`propose_extension` 2 · `authority_overview` 1 · resource 1.

Resolve outcomes: **7 RESOLVED · 6 COMPOSE · 1 FALLBACK · 2 UNDEFINED · 0
CONFLICT**. Validations: twice on its own build, 0 findings each. Gaps +
proposals: a job-progress meter (independently rediscovering G-004) and an
entity-picker recipe — both with composition checks, dependency lists, no new
primitives, compliance tests.

Resolver calibration signals found in C's log (improvement tickets):
1. false-positive COMPOSE — "choose one reviewer from a fixed list" →
   `recipe/entity-delete-armed` (off-target; same class as the P2 adversarial
   review finding);
2. the job-progress need phrased two ways → FALLBACK vs UNDEFINED
   (imprecise boundary between sanctioned fallback and void);
3. C did not follow the false positive: it used the native-control fallback
   and still filed the gap.

## D4 · Engineering / process

| metric | A | B | C |
|---|---|---|---|
| duration | 825.6 s | 649.0 s | 452.4 s |
| tool calls | 83 | 91 | 96 |
| scope | UI-only | UI-only | UI-only |
| containment | sandboxed (pre-fix flags) | sandboxed | sandboxed (7 permission denials during raw-file probe; interface used thereafter) |

## Case studies (under-the-hood texture)

1. **Job progress (deliberately underspecified).** B silently invented a rich
   composite (progress + stall detector + connection-lost note), consistent
   across two pages — competent but unrecorded; nothing marks it as
   improvisation. C composed canonical pieces (`spinner`, `progress` with
   `role=progressbar`/`aria-valuenow`, `status-chip`, text-carried states) and
   labelled the improvisation in-code with `TODO(authority-undefined)` citing
   the resolution result, then filed gap + proposal.
2. **Reviewer picker.** B wired the system combobox (`.cb`) as a picker —
   defensible per the component docs, but no assign recipe exists and the
   choice leaves no trace. C used the sanctioned native-control fallback,
   then filed the missing recipe gap and proposed `recipe/entity-picker`.

## Observations

1. **B ≈ C at the surface.** Both produce a coherent, system-conformant
   product; the measured lint/drift dimensions are at or near zero for both.
2. **The B/C difference lives at the edges:** provenance. C records every
   resolution, marks improvisation, declines bad resolutions, uses sanctioned
   fallbacks, self-validates, and routes gaps upstream. B does none of this —
   its improvisations are invisible future drift seeds.
3. **The authority generated calibration data about itself** (D3 signals) —
   a capability structurally unavailable to passive documentation.
4. Instrumentation behaved: sandbox + audit held; captures/interact/scan all
   produced clean data.

## Threats to validity (preliminary)

- n = 1 per condition; single model; single app.
- Pilot runs were made while containment evolved: a1 saw the `.bench` leak and
  old `run.sh`; b1 ran old `run.sh`; c1 ran the final environment. Production
  reruns all conditions fresh under the frozen protocol.
- Class-adoption figures are static-analysis approximations (template tokens,
  Jinja tokens removed) — treat as direction, not exact counts.
- The user's holistic look (B/C "pretty good") is informal and unblinded;
  blind review (D5) is scheduled on production captures only.
- B's and C's information parity is argued by construction (kit rendered from
  the pack; 115/115 parity) — not proven identical in effect.
- C's resolve distribution includes some resolver imprecision (see D3.1) —
  with n=16 calls this is calibration signal, not a reliable rate.

## Status

Production in flight: 3 fresh runs per condition (a2–a4 / b2–b4 / c2–c4),
round-robin, frozen instruments. Full report + blind review when complete.
