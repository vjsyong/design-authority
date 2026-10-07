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

*(next deviations appended below)*
