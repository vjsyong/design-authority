# AGENTS.md

This repository ships a **Design Authority**: a versioned, machine-readable design contract for coding agents, plus the MCP server that serves it.

- **If you are an agent asked to install it:** follow the **Use now** block in [`README.md`](README.md) top to bottom, check every expected output, and stop to report if a step fails. Do not improvise around a failed step; the long-form reference is the "Install (for agents)" section there.
- **If you are an agent asked to build under it:** read [`packs/triage/AGENT-PROMPT.md`](packs/triage/AGENT-PROMPT.md) first. Resolve before you build; build the recorded way; when the authority has no answer, mark the improvisation and report a gap; verify before claiming done. When an ask is paraphrased and `resolve` returns UNDEFINED, `da discover "..."` (or the `discover_candidates` MCP tool) proposes candidates; inspect them before adopting; retrieval never establishes authority.
- **If you are an agent asked to build out a new authority from a brand kit or other precedent:** load [`skills/synthesize-authority/SKILL.md`](skills/synthesize-authority/SKILL.md); the extraction phase is [`skills/extract-design-evidence/SKILL.md`](skills/extract-design-evidence/SKILL.md).
- **Repository self-check:** `./tools/check.sh` (expected: `gates: OK`).
- **Live authorities:** <https://designauthority.seanyong.xyz>
