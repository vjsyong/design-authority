# Portability Spike · 12 · Final portability report (v3, Indaba)

**Decision: `PORTABLE-WITH-GENERIC-CHANGES` — upheld, now against a
reviewer-approved authority.** This report supersedes `05` (whose verdict was
withdrawn after the two rejections of the NASA line). The v3 authority
(“Indaba”) passed every human gate the earlier attempts failed, and the run
repeated the mechanical results on a system that shares nothing with the
incumbent — not even its gestalt.

## 1 · Representation

**Yes — no core schema change.** Indaba 0.1 was hand-authored in the existing
pack format: 21 artifacts (12 components, 4 patterns, 2 token-sets, 2
guidelines, 1 reference), 4 rules, 3 recipes, 2 fallbacks, 2 prohibitions,
a pack-local validator, scoring, golden. Separate identity; no Triage
imports; its own vocabulary (`masthead`, `action`, `field`, `choice`,
`status`, `label`, `surface`, `ledger`, `meter`, `notice`, `dialog`,
`section`). Same representation lessons as before (KCL-002: hand-authored
packs must carry `kind`).

## 2 · Resolution

**Same model, same usefulness — all five outcomes again** (agent run:
RESOLVED 16 / UNDEFINED 11 / CONFLICT 2 / COMPOSE 2; golden 10/10):
- CONFLICT — “make it sharp, serious, square and black-and-white” →
  `prohibit/square-corners` (on Triage the same request is mundane — the
  polarity inversion is proven in `data/divergence-probes-v3.json`).
- COMPOSE — “retire an item with confirmation” → `recipe/retire-confirm`.
- RESOLVED / FALLBACK / UNDEFINED — as designed, including the seeded
  ambiguous requirement → UNDEFINED with the fallback path explicitly marked.

## 3 · Triage leakage

- **Mechanical:** zero (0 “triage” mentions; only `packs/indaba` mounted;
  divergence probes show zero cross-references).
- **Authorial process:** the v1/v2 leak channels found in `08` were closed
  for this derivation: fresh source fetches, no incumbent CSS in derivation
  context, no Triage-content skills loaded, memory house-style directive
  scoped out, and **human gates placed before effort** (style tile, then
  screens). The reviewer approved the vocabulary and screens with two
  corrections (dark banner; dot stripe removed) — both incorporated.
- **Kernel:** no authority-specific code anywhere; v3 required **zero**
  additional kernel changes beyond the two generic substitutions from KCL-001
  (which now demonstrably serve a third pack: `{pack}` validator workdir +
  `lint-json` parser).

## 4 · Kernel changes

Unchanged from `03`: two additive generic substitutions in
`validate.py`, both ledgered, both re-verified for the third authority
(`indaba-lint` runs through the kernel; fixture catches all four rule
families; the built app scores 100/100).

## 5 · Agent behavior

Built end to end: 15/15 interactive checks, lint 100/100, 84 authority
calls, ~4.6 minutes, $0.048. It respected UNDEFINED (marked the borrower
fallback in markup and comments), exercised CONFLICT correctly, and shipped
progressive enhancement with a working no-JS path. Full record: `11`.

## 6 · Unknowns

Exposed cleanly again: 11 UNDEFINEDs organically; the deliberate out-of-scope
(searchable selection) and motion gaps surfaced as such; no improvisation
became apparent canon. (Zero `report_gap` calls this run as well — the same
behavioral finding as `04`; the channel itself remains proven.)

## 7 · Validation

`indaba-lint` (pack-local, kernel-orchestrated via `{pack}`): fixture → all
four rule families fire (score 80); built app → **100/100, zero findings**.
Triage validators unaffected (regression suite green: kernel tests 10/10,
MCP smoke 17/17, triage pinned 19/19, evolution 23/23, indaba 10/10).

## 8 · Human effort

The v3 cycle (Ubuntu audit → tile → screens → pack → run → report) inside
one session; ≈1.5 k lines authored for v3 on top of the v1/v2 corpus.
Dominant cost again: design formalisation and pack content — not adapter
code. Kernel delta across the entire spike remains ~15 lines, both generic.

---

## Success criteria (protocol) — all met, with reviewer gates

1. Visually different authority — **yes, and verified by the reviewer**
   (two rejection cycles on the previous attempt produced exactly this
   discipline: gestalt gates before anatomy, human sign-off before build).
2. Same kernel loads and serves it — yes (golden 10/10; zero new changes).
3. Same agent-facing interface — yes (84 MCP calls; 132 tool calls).
4. Authority-specific rules stay in the pack — yes (rules, prohibitions,
   recipes, validator; all pack-local).
5. Agent builds a coherent small app — yes (15/15; lint 100/100).
6. Missing knowledge surfaced as missing — yes (11 UNDEFINEDs; marked
   fallbacks; no invented canon).
7. No Triage-specific branches — yes.

**Failure conditions:** none triggered. The earlier failure — a
Triage-shaped derivation — was caught by the reviewer, diagnosed in `06`/
`08`, and eliminated by source swap + gates; that cycle is itself the
spike's most reusable methodology finding.

## Final decision

**`PORTABLE-WITH-GENERIC-CHANGES`** — a second authority that is not Triage
by anatomy *or* gestalt, approved by the human reviewer at three gates,
encodes, serves, validates, and passes the agent test end to end on the same
kernel, with only two small additive generic substitutions (a pack may ship
its own validators; the lint report shape has a name). Honest residuals are
kept on the record: no `report_gap` usage by agents (channel proven
separately), harness tolerance lessons (`11` §4), and the resolution-model
nuances documented in `05` §2 — none of which are authority-specific.

**Spike outcome artifacts:** `docs/portability/00–12` · `packs/indaba/` ·
`examples/indaba-reference-app/` (starter + `reference-build/`) ·
`benchmark/runs/indaba-a1/` · retired-line evidence in `mock-v2/`,
`packs/orbit/`, `benchmark/runs/orbit-a1/`, and `06`–`08`.
