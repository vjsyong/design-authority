# 11 · Consolidation — everything since Design Authority 0.1.0

*Compiled 2026-10-08 at the owner's request ("consolidate what has been done
since version 0.1"). Baseline: tag `v0.1.0` — freeze commit `fecafb1`
(2026-10-07 08:47), the formal specification (`docs/spec/00–05`), freeze
manifest `docs/spec/freeze-0.1.0.sha256`, VERSION `0.1.0`. Scope: everything
after that freeze — **53 commits** (10-07 08:58 → 10-08 02:43 UTC) plus the
uncommitted decision-review tail.*

## 0 · Baseline (what v0.1.0 froze)

Frozen surface (16 manifest files): spec `00–05` · kernel
`design_authority/*` · `tools/{da.py, da-mcp.py, build_pack_triage.py}`.
Prior episodes complete *before* the freeze: the A/B/C benchmark (D-021 blind
review: condition means of 25 — A 15.0 · B 21.3 · C 21.7) and the
authority-evolution loop (`packs/triage-evolution` 0.13.0-experiment). The
freeze declared its own change control (`docs/spec/05`): *editorial* edits →
0.1.x patch; *semantic* changes (pipeline order, thresholds, record formats,
tool contracts, governance taxonomies) → **0.2 + fresh freeze**.

## 1 · The five eras since

### Era 1 · Portability proved on the frozen kernel — 10-07 09:04–11:00

- First candidate **Orbit** (NASA manual) built, then **reviewer-rejected on
  the leak audit** — its element layer reproduced Triage anatomy. Follow-up
  contamination audit identified the cause (auto-distillation + same-session
  context); remediation = quarantine rules + a gestalt gate as hard-fail.
- Kit swap to Ubuntu: source audit → style tile (gated) → derived system →
  **Indaba pack** (21 artifacts + `indaba-lint`), loading and resolving on the
  **unmodified kernel** — golden 10/10.
- Agent run `indaba-a1`: 15/15 interact, lint 100/100, zero triage exposure →
  **PORTABLE-WITH-GENERIC-CHANGES upheld**.
- Kernel-change ledger: KCL-001 (validator `{pack}` substitution) — the
  spike's only required kernel change, implemented minimally; KCL-002 —
  pack-solvable, no kernel change.
- Also landed: benchmark **token-economics** baseline (B ≈ C at parity, both
  ≈ 3× A) · `token_report.py`.
- Record: `docs/portability/00–12`; build archive
  `examples/orbit-v1-reference-build-archive`; `examples/indaba-reference-app`.

### Era 2 · Authority Synthesis experiment — 10-07 11:55–14:30

- Sources + common protocol: **wink** (Mailchimp) · **leader** (Economist /
  Marber system) · **dominion** (Canada FIP); quarantine extended,
  machine-heavy compile commitment.
- Evidence inventories → gestalt models + style tiles → **Gate 1 approved**
  (all three tiles).
- Decision sets as the machine source of truth: **72 decisions** (W-26 ·
  L-24 · D-22) — `render_decisions.py` (JSON → semantic-review + review.html).
- **Gate 2** (interactive, in-browser): per-decision sheets → review server on
  `:8420` (verdicts, notes, image uploads, full autosave) → reviewed to
  completion — wink 26/26 (8 accept · 4 modify · 2 reject · 12 undefined),
  leader 24/24, dominion 22/22 → revisions v2–v4 with live-measured styles →
  **Gate 2 CLOSED across all three**.
- Record: `docs/synthesis/00–12`.

### Era 3 · Stress tests + adjudication + codification — 10-07 14:41–16:19

- `/demo` authority explorer (ask box + golden + contents per pack).
- **Cadence v1**: three quarantined app builds × 42 elements against the
  candidate authorities — 48 gaps filed (`docs/synthesis/12–13`).
- Adjudication pass: 48/48 dispositions → **17 proposals → 12 fixes applied**
  (`14-adjudication-pass.md`); **`/proposals` review gate** with rendered
  previews of every proposed element and the adjudicator's record.
- **Cadence v2** rebuilds on the fixes (gaps 13/13/14).
- **Codification**: 11 accepted proposals compiled into the packs (all →
  **0.2.0**); 25 negative precedents (5 reviewer-rejected + 20 adjudication
  declines) wired **kernel-generic** (resolve attachment · search kind ·
  gap/propose warnings · CLI `precedents` · MCP `list_precedents`); synthesis
  goldens 29 → **49** (`14-codification.md`).
- **Cadence v3**: rebuilt on the codified authorities — RESOLVED 5→12 (wink) /
  9→14 (leader) / 6→11 (dominion); **49 precedent attachments, every try-list
  followed**; gaps 48 → 40 → **17** (`15-stress-v3.md`).

### Era 4 · Lenient adjudication doctrine — 10-08 02:43

- Owner doctrine applied across the three packs: lenient with denies —
  **candidates** (provisional, `promote_when`) · **undefined deferral** ·
  declines reserved for grounded policy (mandatory grounds + scope +
  boundary).
- Precedent **scope verdicts** per ask: `governs` · `outside`
  (boundary-exempt → ordinary marked improvisation) · `ambiguous` — surfaced
  in resolve / search / gap / propose / CLI `precedent-check` / MCP
  `check_precedent`.
- 20 declines re-classified: **5 kept (policy) · 2 split · 2 promoted to
  candidates · 11 deferred to undefined**. Regression case #1: the tick
  ("a check control to log a ritual" → `outside`). Precedent probe 18/18 →
  **31/31**; gate shows the lenient ledger (`16-lenient-adjudication.md`).

### Era 5 · Decision-review loop — 10-08 (uncommitted)

- `examples/cadence3-wink` revised in place: **v3.1** — row tick restored as a
  marked improvisation per the outside verdict · **v3.1b** — click-to-provenance
  inspector (generated registry `provenance.js`: decision · resolution ·
  proposal trail · precedents incl. retired lenient outcomes · gap ·
  candidate · evidence links) · **v3.1c** — the inspector became a **movable
  review window** with reviewer verdicts **accept · modify · reject ·
  undefined** + notes: local-first, server-synced under the review serve,
  self-healing (`POST /api/stress/verdict` → `data/stress-verdicts.json`,
  keyed `<build>|<row>`; `GET /api/stress/verdicts?build=<name>`).
- **Owner review pass on the wink build: 14 verdicts** (7 accept · 5 modify ·
  1 reject · 1 undefined) — export
  `examples/cadence3-wink/_evidence/cadence3-wink-verdicts-2026-10-08.json`.

## 2 · Version & conformance state (now)

| thing | version |
|---|---|
| Design Authority (VERSION, spec) | **0.1.0** — unchanged since the freeze |
| packs/wink · leader · dominion | **0.2.0** (codified) |
| packs/triage | 0.12.1 (pin `e374f38`) |
| packs/triage-evolution | 0.13.0-experiment |
| packs/orbit · indaba | 0.1.0 |

**Frozen-surface drift** — `sha256sum -c docs/spec/freeze-0.1.0.sha256`:
**10/16 OK · 6 FAILED** (all kernel: `pack.py` · `resolve.py` · `validate.py` ·
`records.py` · `cli.py` · `mcp_server.py`). Kernel + tools diff vs v0.1.0:
**+731 / −13 across 11 files**. Unchanged: spec `00–05`, `__init__.py`, the
three tool wrappers. Conformance is green (below) — but per `docs/spec/05`,
semantic changes (pipeline order · thresholds · **record formats** · **tool
contracts**) call for a **0.2 bump + fresh freeze**, and the post-freeze
deltas include tool-contract additions (`precedent-check` · `precedents` ·
`candidates` · `check_precedent` · `list_candidates`) plus precedent/candidate
record wiring. **→ Owner ruling requested: 0.2 freeze (recommended) or a
logged editorial waiver.**

**Conformance now:** kernel 17/17 · triage goldens 19/19 · synthesis goldens
18 · 14 · 17 (= 49) · precedent probe 31/31 · MCP smoke 20/20 ·
`tools/check.sh` green.

## 3 · Map

| area | where |
|---|---|
| Frozen spec | `docs/spec/00–05` + `freeze-0.1.0.sha256` |
| Portability episode | `docs/portability/00–12` |
| Synthesis episode (incl. stress · adjudication · lenient) | `docs/synthesis/00–16` |
| Benchmark-era reports | `docs/07–10` · `token-economics.md` |
| Builds | `examples/cadence{,-2,-3}-{wink,leader,dominion}` · `indaba-reference-app` · `orbit-v1-reference-build-archive` |
| Review app (live) | `da-review` uid service @ `:8420` — gates · `/demo` · `/proposals` · `/stress{,2,3}/*` · stress-verdict API |

## 4 · Open threads

1. **0.2 freeze ruling** — frozen-surface drift (§2); conformance gate first,
   then tag + fresh manifest per `docs/spec/05`.
2. **v3.2 revision pass** for cadence3-wink from the 14 owner verdicts (chart
   styling · dedicated slider · toggle/pill language · codifying the search
   box · …) — the verdict store is the input.
3. Review window → **leader + dominion** builds (the verdict backend already
   accepts all three).
4. Candidate promotions awaiting named evidence (`candidate/pager-composition`
   + dominion's 3) — capture → proposal → verdict → codify.
5. Era-5 work is **uncommitted** (review-app endpoints · cadence3-wink
   revision + evidence · stress-verdict store).

## 5 · Verify

```bash
tools/check.sh                                   # pack drift + tests + goldens + probes + smoke
sha256sum -c docs/spec/freeze-0.1.0.sha256       # frozen-surface check — expect 6 kernel FAILED
git log --oneline v0.1.0..HEAD                   # the 53-commit arc this doc consolidates
python3 tools/da.py --pack packs/wink precedent-check --ask "a check control to log a ritual"
```

*(History: pre-freeze era in `docs/07–10` + `docs/evolution/`; this doc takes
over from the freeze.)*

## Postscript — formalized as 0.2.0 (2026-10-08, same day)

Per the owner's ruling ("formalise everything now as 0.2"), this consolidation
became the **0.2.0 minor bump**: the spec set (`docs/spec/00–05`) now
documents the semantics this document describes — negative precedents +
candidates (optional format-0.1 records), precedent scope verdicts
(`governs` / `outside` / `ambiguous`), the lenient adjudication doctrine, and
the tool-contract additions. Fresh manifest `docs/spec/freeze-0.2.0.sha256`;
tag `v0.2.0`; justified in D-023. The drift flagged in §2 is thereby
resolved: every file that failed the 0.1.0 manifest check is normative and
re-frozen under 0.2.0.

## Postscript 2 — the owner review pass completed (2026-10-08)

The wink-build review pass closed at **14 verdicts** (7 accept · 5 modify ·
1 reject · 1 undefined) with notes captured verbatim in
`data/stress-verdicts.json` and exported to
`examples/cadence3-wink/_evidence/cadence3-wink-verdicts-2026-10-08.json`.
The v3.2 revision pass works from these.
