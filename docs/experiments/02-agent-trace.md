# Experiment 02 · How an agent works with the authority (semantic search on)

Companion to experiment 01. Two traces show the interaction pattern with the
retrieval assist available: a scripted session through the real MCP server
(part A, complete), and an independent agent given a build task (part B,
complete; its raw log is `agent-session-workspace/subagent-log.md`).

## Part A · A session through the MCP server

Driver: `tools/trace_agent_session.py` (spawns `tools/da-mcp.py` with the
project venv, one JSON-RPC call per step). Transcript with full arguments:
`02-agent-session-transcript.json`. The server wrote its own
`.design-authority/decision-log.jsonl` and the gap record into
`agent-session-workspace/`; both ship with this document.

The task: add a way to flip one setting on or off, with a status chip, on a
settings page.

| # | call | what came back | ms |
|---|---|---|---|
| 1 | `authority_overview` | triage 0.12.1, counts, policy | 4.3 |
| 2 | `resolve` "let people flip one preference on or off right away" | `UNDEFINED` (approximate wording, structured) | 9.8 |
| 3 | `discover_candidates` same wording | `component/px-sw` (lex #6, cos 0.616), then fallback/motion-reduction, pattern/settings | 673.6 (cold) |
| 4 | `inspect_artifact` `component/px-sw` | Switch record: class px-sw, ok | 3.6 |
| 5 | `resolve` "a switch" | `RESOLVED component/px-sw`, score 17.5, margin held | 2.6 |
| 6 | `resolve` "a filterable status field" `assist=semantic` | `UNDEFINED`, assist attached: dot, field-err, tl | 16.2 |
| 7 | `discover_candidates` "labels that show a record's state" | `component/badge` (lex #4, cos 0.666), then guideline/voice, component/chip | 15.4 (warm) |
| 8 | `search_authority` "filter chip" | chip 13.0, cb 5.0, brand 1.5 | 2.9 |
| 9 | `inspect_artifact` `component/chip` | Chip record: class chip, ok | 3.4 |
| 10 | `resolve` "a status chip with text padding" | `UNDEFINED` (no composition rule covers it) | 3.3 |
| 11 | `report_gap` settings-page preference rows | `gap/20261008-122256-74707e` stored in the session workspace | 3.6 |

Total 11 calls, 0.7 s client-side. Cold discovery pays one model load
(673 ms); warm discovery is 15 ms and resolves stay at single-digit
milliseconds.

### What the trace shows

1. **The retrieval gap is real, and the flow absorbs it.** The first ask is a
   paraphrase; the resolver rightly returns UNDEFINED; discovery puts the
   right record (`px-sw`) in the candidate list; the agent inspects it and
   adopts it under canonical vocabulary; the second resolve is RESOLVED with
   citations. Retrieval proposed, the record decided.
2. **The assist block is not an answer, and the trace proves it.** Step 6's
   attach proposed dot, field-err and tl for "filterable status field": two
   neighbours and one miss. The agent did not accept them; it reworded its
   discovery (step 7) and the right record (badge) surfaced. Similarity
   ranked; wording and inspection decided.
3. **Both engines cooperate.** Discovery is what surfaced badge in step 7;
   plain lexical search is what confirmed chip in step 8. The agent used each
   for what it is good at.
4. **Undefined stays a first-class outcome.** Step 10 found no record for the
   composed ask, and the session closed by filing a gap. Nothing was
   silently invented; nothing was left unrecorded.
5. **Latency is an afterthought at this scale.** Every authority call in the
   session, including retrieval, lands between 2.6 ms and 16.2 ms warm. The
   only visible cost is the one-time model load.

## Part B · An independent agent with the same task class

A fresh agent (separate context, no knowledge of this document; driving the
CLI, not MCP) was given the same class of task: build a settings section with
a toggle and a state display, logging every authority command it ran. Its raw
evidence: `agent-session-workspace/subagent-log.md` (24 numbered commands
with trimmed outputs) and `build-settings.html`.

What it did, in order: three natural-language resolves (all UNDEFINED,
closest scores 4.0 to 5.5); discovery for both needs (`discover "flip a
setting on or off"` surfaced pattern/settings and component/px-sw;
`discover "a chip showing status"` surfaced component/chip and
component/dot); inspect for every adopted record; canonical-phrasing
confirmations ("a switch", "a chip", "a settings page", "a status dot" all
RESOLVED); seven probes of the status-chip need; a reasoned decline of
component/badge (a static micro-label, not a chip); the build; validate
(0 errors / 0 warnings / spec score 100); and one gap filed from the
workspace: `gap/20261008-122731-8112d8`.

Two findings from the run:

1. **The assist carried the phrasing gap.** "Let people flip a preference on
   or off" misses the threshold (px-sw at 4.0 vs 6.5 needed); discovery puts
   px-sw at rank 3 (lex #5, sem #3, cos 0.625); the canonical confirmation
   then resolves cleanly. That is the designed division of labour: retrieval
   proposes, canonical wording adopts.
2. **The distribution ships more than the catalogue records.** The agent
   found a `.status-chip` class shipping in `dist/triage/patterns.css`
   (dashboard block, with a `.off` variant) that has zero catalogue presence:
   search returns nothing and the pattern/dashboard record does not mention
   it. It declined to treat an unrecorded class as canon, assembled the state
   display from recorded pieces (chip + dot, dot paired with text), and filed
   the gap with the shipped class as evidence. That is the loop working in
   the wild, and a candidate for upstream review.

The log is honest by construction: non-command checks are separated into a
supplementary section (a headless browser run showed the toggle flipping the
preference with the chip and aria-label following), and it flags a
phrasing-recall note it did not file as a gap because the record exists.

Verification pass (this document's author): the discovery result, the
UNDEFINED probes, the validator score of 100 and the `.status-chip` finding
were all re-run or re-checked and reproduce. The artifact carries its adopted
ids in a header comment and implements the px-sw markup contract exactly
(hidden twin, label-wrapped checkbox, verb-carrying aria-label).
