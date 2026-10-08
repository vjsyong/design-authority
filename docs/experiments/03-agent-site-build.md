# Experiment 03 · Building a demo site under the authority (audited trace)

Sean's brief: build a new demo site using Triage and the updated (0.4)
system, and trace what the agent does. So this one came with an instrument:
every authority call from the building agent went through `run-authority`, a
wrapper that runs the real CLI and appends the call, its output and timing to
`audit.jsonl`. The trace is machine-recorded, not self-reported.

- Build: **Duty**, a two-page incident console (list + case view), Triage
  v0.12.1, artifacts in `duty-build/` (`index.html`, `case.html`, `log.md`,
  `audit.jsonl`, `run-authority`).
- Agent: a fresh subagent (separate context, CLI only), same model class as
  experiment 02 part B.
- Published: <https://designauthority.seanyong.xyz/authorities/triage/demo/duty/>
  (deployed as `examples/triage-duty/`, route registered in the review app,
  and linked from the catalogue card for Triage).

## 1 · The numbers (audit.jsonl is ground truth)

- 37 authority calls, 0 non-zero exits, 5.7 s total authority time.
- Breakdown: 1 overview, 1 `--help`, 15 resolve, 3 discover, 12 inspect,
  3 gap-add, 2 validate.
- Adopted records (12): `component/shell`, `component/page-head`,
  `component/tbl`, `component/chip`, `component/dot`, `component/badge`,
  `component/kv`, `component/tl`, `component/logpanel`, `component/btn`,
  `component/nav-item` (carries the sidebar nav; separately rejected for the
  skip link, see the misfire finding), `pattern/viewer`.
- Both pages validated at **0 errors / 0 warnings / spec score 100**, first
  run, one validate call per page.
- 3 gaps filed, each with rich context in the record (ask, outcome, detail,
  built_with).

The narrative log (`log.md`) reproduces the audit exactly: 37 numbered
sections against 37 audit entries, in order, no omissions and no additions.
The agent's full live transcript was also scanned afterwards: it contains no
authority invocation outside the wrapper (every mention of the tool file is
a read). The wrapper records what passes through it; exclusivity for future
runs needs containment, not instructions.

## 2 · How the agent worked

Natural-language resolves first. Most needs met canonical vocabulary and
resolved outright (table, shell, timeline, key-value rows, log panel). Where
the resolver is blind, the agent switched to discovery, three times:

1. "a row of filter chips to narrow a list" resolved to a **tie** (13.0 chip
   vs 13.0 index-row, a direct match needs a 2.0 lead), so UNDEFINED.
   Discovery put `component/chip` first. Built from it, marked the composite
   row, filed the gap.
2. "a small coloured dot for severity" surfaced `component/dot`.
3. "an incident header with an id and current state" resolved UNDEFINED (all
   candidates at 4.0); discovery's top leg pointed at `component/page-head`.
   Built as page-head + badge + dot, marked, gap filed.

It inspected all 12 adopted records before use, ran canonical confirmations
("filter chips", "status dot" resolve outright), and closed with the
validator.

## 3 · Two findings worth keeping

**A false RESOLVED, caught by the agent.** The ask "a skip link to jump past
the navigation" returned `RESOLVED component/nav-item` (8.0). A skip link is
not a nav item; the agent inspected nav-item, judged the resolution wrong,
used the shipped `.skip` class from `core/base.css` instead, marked the
element as improvised, and filed a gap whose recorded outcome is literally
`RESOLVED (misfire)`. That is the inspection doctrine doing its job on a
resolver edge, and it is the second observed instance of an agent-side catch
(the first was the unrecorded `.status-chip` class in experiment 02).

**Composite ties are a distinct UNDEFINED flavor.** The chip-row case shows a
new failure shape: both candidates individually match, but the recorded
margin rule (a direct match must lead by 2.0) correctly refuses to pick. The
outcome was UNDEFINED, discovery surfaced the right primary record, and the
composite was built, marked and reported upstream. No threshold was loosened.

## 4 · Published artifact

- `examples/triage-duty/` (self-contained: pages plus a byte-identical copy
  of the Triage distribution under `assets/`).
- Live: list at `/authorities/triage/demo/duty/`, detail at
  `/authorities/triage/demo/duty/case.html`; both pages and assets serve 200
  and the catalogue card for Triage now links the demo.

## 5 · Verification pass (this document's author)

- Audit against narrative log: 37/37, in order, no drift.
- Re-ran validate on both pages: 0/0/100 (matches the agent's claim).
- Browser pass on the live URL: filter chips narrow the table (1 of 4 rows
  visible under "Mitigated"), the case page renders 6 timeline entries and 8
  key-value rows, the note composer appends a row; zero page errors.
- Nothing outside the workspace was touched by the agent (`git status`
  checked at completion).

Limits, stated plainly: n=1 agent run, one small site, same task family as
experiment 02 part B, and discovery was exercised three times, so this is a
quality trace rather than a sample for statistics. The instruments (audited
wrapper, mark-and-gap discipline, validator gate) are the reusable part, and
they are what makes the next run comparable.
