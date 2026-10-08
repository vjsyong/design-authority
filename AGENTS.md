# AGENTS.md

This repository ships a **Design Authority**: a versioned, machine-readable design contract for coding agents, plus the MCP server that serves it.

- **If you are an agent asked to install it:** follow "Install (for agents)" in [`README.md`](README.md) top to bottom, check every expected output, and stop to report if a step fails. Do not improvise around a failed step.
- **If you are an agent asked to build under it:** read [`packs/triage/AGENT-PROMPT.md`](packs/triage/AGENT-PROMPT.md) first. Resolve before you build; build the recorded way; when the authority has no answer, mark the improvisation and report a gap; verify before claiming done.
- **Repository self-check:** `./tools/check.sh` (expected: `gates: OK`).
- **Live authorities:** <https://designauthority.seanyong.xyz>
