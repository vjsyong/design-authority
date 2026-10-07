# 06 · Pre-registration — benchmark instruments & analysis plan

**Status: DRAFT — freezes after the pilot review (no comparative
interpretation before the freeze).** Committed timestamp = freeze point.

This document fixes the instruments, the exact metrics, and the interpretation
rules *before* any production runs are looked at. Deviations discovered during
runs are appended to §Deviations, dated, with rationale; the frozen parts are
never silently edited.

## 1 · What is being compared

Three conditions, one app, one brief (identical base text; the condition block
is the only prompt delta):

- **A — naive.** Starter app only; brief says "use your own judgment".
- **B — passive kit.** Starter + vendored system package (`design/`) + the
  rendered kit (`design-docs/`, 115/115 parity vs the Authority Pack).
- **C — design authority.** Starter + vendored system package + `DESIGN.md` +
  the `design_authority` MCP server (7 tools, decision log on).

Model: pinned per run (`deepseek/deepseek-flash` for the pilot; final model
recorded in the decision log before the production runs). Same agent config
(`opencode run --pure`, build agent, no plugins), same wall-clock budget
(`--timeout 1800`), fresh workspace + fresh session per run.

## 2 · Runs

- Pilot: 1 × (A, B, C) — instrument shake-out; **not** used for conclusions
  (except where a pilot finding triggers an instrument fix, which is recorded).
- Production: 3 × (A, B, C) = 9 runs.
- Extension trigger (pre-registered): if, on any primary dimension, the
  within-condition spread (max−min) is ≥ the C−B difference on that dimension,
  add 2 more runs per condition and report medians over 5.
- Execution: serial, one machine; each run fully recorded (`prompt.md`,
  `transcript.jsonl`, `opencode-stderr.log`, `run.json`, `interact.json`,
  `scan.json`, `capture/` screenshots + DOM probes, `.design-authority/` logs
  for C).

## 3 · Instruments (frozen definitions)

### D1 · Design compliance — `scan.py:lint`
triage-lint (pinned snapshot `e374f38`), run over the whole workspace with
findings filtered to the authored surface (`templates/`, `static/` minus
`static/design/`). Reported: severity counts, by-rule counts, **and delta vs
the pristine starter** (multiset difference on `(rule, message)` — the
agent-introduced findings). The baseline is identical across conditions.

### D2 · Design drift — `scan.py:drift` + `capture.py` probes
- Code-level: unique raw hex colours; unique off-token px spacing values;
  distinct class names; `!important` count; inline `style=` count;
  durations/radii/font-family declarations.
- DOM-level (computed styles over every element, desktop viewports): unique
  background colours, text colours, border-radius tuples, font families,
  padding tuples (top-60 lists, counts reported).
One-off visual treatments proxy = unique-value counts; cross-screen
consistency is left to human review (D5). No composite score.

### D3 · Authority behaviour — C only
From the server decision log: tool calls by name; resolve outcomes
(CONFLICT/RESOLVED/COMPOSE/FALLBACK/UNDEFINED counts); gaps reported;
proposals created. From transcript + artifacts (manual audit, rubric below):
whether UNDEFINED was treated as UNDEFINED (not silently invented); whether
CONFLICT items were not implemented as stated; fallback-policy conformance;
unauthorised inventions (new canonical-looking components without gap/proposal).
Rubric anchors: golden set (`packs/triage/golden.json`) as the expected
outcome vocabulary; "incorrect resolution audit" is manual and marked as such.

### D4 · Engineering quality
- Functional: `interact.py` pass fraction (13 checks, same for all conditions).
- Console errors + page errors during capture (count).
- Scope discipline: changed files vs starter commit, split UI/backend/other
  (`scan.py:scope`); backend files changed is a violation count.
- Reuse/duplication: class inventory size; (duplication counted manually in
  review if needed — not automated in v0; noted).

### D5 · Human review (blind)
- Gallery: anonymised screenshots (random codes, shuffled) at fixed routes ×
  {desktop, phone}; mapping sealed until review completes.
- Questionnaire (per build): consistency; coherence; obvious design mistakes;
  confidence another page could be added consistently; manual cleanup needed
  (1–5 + free text). Reviewer(s): Sean (+ optional additional reviewer).
- A vision-LLM pre-pass may be run as an instrument check; it never replaces
  the human score.

### D6 · Process
- Durations, exit status, timeouts, incidents, per-run token/event counts from
  `transcript.jsonl` (best-effort parse).

## 4 · Analysis plan

- Report **individual dimensions**; no composite score.
- Primary comparison: **C vs B** per dimension (paired by run index: c1–b1,
  c2–b2, c3–b3). Secondary: B vs A.
- Report each run's value + median + range; state direction and size in raw
  units (e.g. "unique hex colours: B {7,6,8} vs C {2,3,2}").
- No significance testing at n=3; language stays descriptive ("consistent
  with", "no detectable difference at this n").
- Pre-committed reading rules: (a) if C−B is smaller than within-condition
  spread on a dimension → "no detectable difference" for that dimension;
  (b) the extension trigger in §2 applies; (c) UNDEFINED handling in C is
  judged against the golden vocabulary, not free-form.

## 5 · Threats to validity (standing list)

1. Single model; single app; one brief.
2. n small; descriptive only.
3. Resolver quality (authors' curation) shapes C — bounded by goldens; audited.
4. Kit authorship shapes B — mitigated by generation-from-pack + parity gate.
5. Access-mode asymmetry (tools vs files) is the treatment, not a flaw; costs
   (tool round-trips) are recorded in D6.
6. Reviewer bias/familiarity (Sean knows the systems); blinding is code-based,
   mapping sealed; mixed presentation order.
7. Screenshot determinism (relative timestamps differ between runs); fixed
   routes/viewports/machines; animation settling wait; seeds fixed.
8. Session history: opencode global state is shared across runs (sessions
   tagged `bench-<run-id>`); per-run directories are isolated.
9. Agent may modify backend despite instructions — measured (scope) not
   prevented.

## 5 · Pilot review checklist (post-pilot, pre-freeze)

When the pilot (1×A/B/C) completes, inspect before freezing:

1. `containment.refs_outside == 0` and `denied_events == 0` for every run; any
   breach → rerun (per D-020) and log a deviation.
2. Every run produced: `transcript.jsonl`, `run.json` with `interact` counts,
   `scan.json`, `capture/` (24 screenshots), archived `ws/`.
3. Instrument sanity: interact checks sensible for each condition (baseline
   13/13 expected pre-edit; expect A/B/C to differ only by *their* work);
   scan baseline delta ≈ 0 for a fresh workspace; DOM probes parse.
4. Agent sanity: `opencode.exit == 0` (or recorded timeout), tool mix shows
   real building work (writes/edits), no unfinished runaway loop.
5. C only: `authority.calls` > 0 and `resolve_outcomes` look coherent;
   decision log exists in archived ws.
6. Screenshots: open two or three per condition (vision check) — pages render,
   fonts load (B/C should show Geist if they adopted the system), states exist.
7. Model adequacy (D-007): if the pilot model fails sanity 3–4, probe an
   alternative model on one condition before freezing.

Record outcomes (fixes → deviations D-n; clean → freeze stamp below).

### Pilot review record

- **a1 (A, naive) — 2026-10-07, ACCEPTED.** exit 0, 825.6 s, 83 tool calls; interact
  13/13; all artifacts present; no breach attempts (audit v2 recompute: 0
  attempts; the raw 46 were `.bench` file-read mentions + opencode scratch
  text — see D-2); screenshots confirm a coherent, finished custom UI.
  Measured: **154 agent-introduced lint findings** (44 error / 103 warning /
  11 info): TDS002 raw colours ×72, TDS003 radii ×40, TDS013 physical
  directions ×30, TDS009 token overrides ×2, plus TDS005/6/7/8/12. Drift:
  36 unique hex colours · 27 px spacing values · 198 classes · 6 `!important`
  · 36 inline styles. Scope: UI-only (7 files), backend untouched.
- **b1 (B, kit) — 2026-10-07, ACCEPTED.** exit 0, 649 s, 91 tool calls
  (43 read / 32 bash / 9 write / 5 edit); interact 13/13. Lint: **0 findings
  in the entire workspace** — it eliminated even the pristine starter's
  baseline 10 (scan reports authored=0 / delta=0). Drift: 1 hex · 0 px
  spacing values · 0 border radii · 0 `!important` · 18 inline styles · 150
  classes. Screenshot review: fully system-conformant (zero-radius, paper
  aesthetic, restrained status accents only). One `./run.sh` denial (the
  denylist rejected the command form; agent retried via `python3` — fine).
- **c1 (C, authority) — rerun ACCEPTED (2026-10-07).** exit 0, 452 s, 96 tool
  calls; interact 13/13; lint 0; hex 0; px 0; classes 134; backend untouched.
  Authority usage: 43 calls — resolve ×16 (**7 RESOLVED / 6 COMPOSE / 1
  FALLBACK / 2 UNDEFINED**), inspect ×13, search ×7, validate ×2, overview ×1,
  **report_gap ×2, propose_extension ×2**, 1 MCP resource read. The two
  UNDEFINED resolutions produced two structured gaps + noncanonical proposals
  (a job-progress meter — independently rediscovering G-004; a single-entity
  picker recipe built on the canonical combobox) — both with composition
  checks, dependency lists, **no new primitives**, and compliance tests.
  Containment: it probed `/home/xrim` and attempted raw pack reads at
  `/opt/da` (da_zone 8) — denied by the permission layer (4 read denials + 1
  bash) — then used the MCP interface throughout. The sanctioned route held.

### Verdict: pilot COMPLETE — all three conditions accepted.

## FREEZE — production protocol (2026-10-07)

Pilot complete; deviations D-1..D-4 addressed. **Instruments frozen**: capture /
scan / interact / report / gallery, briefs, starter, kit, pack, kernel, and the
sandbox configuration as of this commit. No changes to instruments, materials,
thresholds, or briefs until production analysis is complete; any fix found
mid-production is logged as a deviation, affects no completed run retroactively,
and if it invalidates a run that run is rerun under a new id and excluded.

- **Model**: `deepseek/deepseek-flash` for every run (D-007 resolved by pilot
  adequacy: full custom UI in ~14 min for A; system-conformant builds for B/C).
- **Production set**: 3 fresh runs per condition (9 total): ids a2/a3/a4,
  b2/b3/b4, c2/c3/c4; executed round-robin (A,B,C)×3 to balance temporal drift.
- **Pilot runs are excluded from headline metrics** (a1/b1/c1 retained as
  method evidence; `c1-broken-pilot` archive kept).
- **Analysis**: per-dimension metrics only (§2 doc 01 / §2 doc 02), no composite
  score; D5 blind review over production captures only; reviewers get the
  gallery + questionnaire, mapping sealed until review completes.
- **Reporting**: raw distributions shown alongside any aggregate; threats to
  validity mandatory. *Analysis tooling (report.py / gallery.py) may be
  extended during production — run instruments and thresholds are what is
  frozen, not the report renderer.*

## 6 · Deviations log (append during runs)

**D-1 · 2026-10-07 — Containment breach in pilot runs a1/b1; both invalidated.**
Observed: the condition-A agent walked up from its workspace (then inside the
repo tree), read `benchmark/` (all three condition briefs, the harness code,
other runs' outputs), attempted access to the Triage repo, and loaded a
globally installed opencode skill named `triage-design-system`; it built
nothing in 54 s. Condition B showed the same exploration pattern (23
experiment-referencing lines). Root cause: workspaces lived under the repo and
opencode defaults are permissive (unrestricted bash; skills loaded from
`~/.config/opencode`, `~/.claude`, `~/.agents`; global plugins/config active;
`external_directory` did not intercept bash).

Fixes applied before any production run; the pilot restarted from scratch:

1. Workspaces moved to `/tmp/da-ws/<run-id>/ws` — outside the repo entirely.
2. Agent runs inside **bubblewrap** with a minimal filesystem; the benchmark
   repo and unrelated home paths are invisible, and external access fails at
   the filesystem level (verified: `ls /home/xrim/design-authority` →
   "No such file or directory", bash included).
3. Per-run `XDG_CONFIG_HOME` (no global config/skills/plugins/agents) plus
   strict opencode permissions (skill / webfetch / websearch /
   external_directory **deny**; edit/bash/read allowed inside the workspace).
4. Transcript **containment audit** recorded per run
   (`run.json.containment`: `refs_outside`, `denied_events`); runs with
   `refs_outside > 0` are flagged and rerun.
5. Ops note: Ubuntu 24.04 blocks unprivileged user namespaces; installed the
   targeted AppArmor profile `/etc/apparmor.d/bwrap` (userns granted to
   `bwrap` only). This host-config change is recorded here deliberately.

Implications: C runs can still read `tools/`, `kernel/`, `packs/` (the
authority server needs them; the pack is legitimately C's information sphere).
Web fetch/search is disabled for every condition equally. Residual risk:
`~/.local/share/opencode` stays shared for auth/session storage; agents cannot
see other sessions from within a run.

**D-2 · 2026-10-07 — `.bench/materials.json` leaked experiment context into
workspaces; removed.** During the pilot, run a1 read its workspace's
`.bench/materials.json`, which contained the condition label, the starter path
and the snapshot path (`/home/xrim/triage-design-system-demo`). The sandbox
blocked any access, and the agent made no escape attempts, but the file is a
hint agents must not receive. Fix: the materials manifest is now written to
`benchmark/runs/<id>/materials.json` (run dir) and never into the workspace;
pilot runs that already saw it are pilot-only (`b1`/`c1` rerun if they started
pre-fix).

**D-3 · 2026-10-07 — run.sh path friction inside the sandbox; audit
refinement.** The starter's `run.sh` defaulted to a literal
`/home/xrim/design-authority/.venv/bin/python`; opencode's
`external_directory: deny` blocked two `nohup env … ./run.sh` invocations
(an inline variant with the same path was permitted). The agent worked around
it and verified its build thoroughly (ran the app, curl'd every route, POSTed
the flows, wrote its own Playwright checks). Fix: `run.sh` resolves the
interpreter from PATH (`python3`), which works inside and outside the sandbox.
The containment audit was also refined to separate protected-path **attempts**
(tool inputs — the signal) from passive **mentions** (results / permission
text).

**D-4 · 2026-10-07 — sandbox mounts moved to opaque /opt paths; clean env;
Playwright cache bound; c1 rerun.** Findings from the first c1 attempt:
(a) the agent read the authority pack files raw via bash (`cat rules.json`,
copying `prohibitions.json` into its workspace for a self-lint) — C's content
sphere, but it bypasses the MCP interface and went unmonitored; (b) its
Playwright self-test hung because the browser cache was invisible in the
sandbox → opencode's shell-tool timeout fired → opencode terminated its own
session (exit -15). Fixes (all conditions): every non-system mount now lives
at an opaque `/opt` path (`/opt/py/venv`, `/opt/node`, `/opt/playwright`;
condition C adds `/opt/da/{tools,kernel,packs}`), so the project tree cannot
be probed (`ls /home/xrim` shows none of it). The sandbox environment is
constructed with `--clearenv` + explicit vars (kills inherited `TMPDIR`
leakage — the root cause of the Playwright hang class). Browsers bound
read-only via `PLAYWRIGHT_BROWSERS_PATH=/opt/playwright`. Containment audit
gains a `da_zone` counter: raw `/opt/da` reads from tool inputs vs MCP calls
(recorded per run; expected interpretation: interface adoption). The first
c1 run is archived as `runs/c1-broken-pilot/`; c1 was rerun. Kit review for
meta-leaks: `PARITY.md` (rendered-from-pack receipt) retained — it documents
the same-information guarantee and reveals no mechanism.

**D-5 · 2026-10-07 — production execution switched from sequential round-robin
to parallel (user request, wall-clock).** Runs a2, b2, c2, a3 completed
sequentially; the remaining five (b3, c3, a4, b4, c4) were launched as one
parallel batch (5 concurrent). Threats to validity considered: shared host and
model-API contention could slow individual runs (timeout risk), but contention
is symmetric across conditions and, if anything, temporal-drift balance
improves because all conditions' remaining repetitions execute in the same
wall-clock window. The partial sequential b3 (≈11 s in) was discarded and
relaunched fresh in the batch. No run that completes (in either mode) is
rerun; any timeout- or contention-marked run is flagged in the report.

*(next deviations appended below)*
