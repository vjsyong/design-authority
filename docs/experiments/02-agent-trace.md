# Experiment 02 · How an agent works with the authority (semantic search on)

Companion to experiment 01. Two traces show the interaction pattern with the
retrieval assist available: a scripted session through the real MCP server
(part A, complete), and an independent agent given a build task (part B,
running; its raw log lands in `agent-session-workspace/subagent-log.md`).

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

A fresh agent (separate context, no knowledge of this document) was asked to
build a small settings section under the Triage authority using the CLI, with
a standing instruction to log every authority command it ran, inspect every
record it adopted, use discovery whenever a resolve came back UNDEFINED, and
file a gap for anything genuinely undefined. Its log and artifact will be
committed here alongside its raw files in `agent-session-workspace/`:
`subagent-log.md` (its own numbered command log) and `build-settings.html`.

(The run was dispatched at the time part A was recorded; its digest is
appended when it returns.)
