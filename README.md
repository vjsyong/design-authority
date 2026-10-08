# Design Authority

A versioned, machine-readable design contract that lets coding agents work under a real design system instead of guessing at it. Agents resolve design problems against the authority (RESOLVED · COMPOSE · FALLBACK · UNDEFINED · CONFLICT), build against cited rules, check their work with explicit validators, and report gaps upstream instead of silently inventing canon. The kernel is completely kit-agnostic: it knows artifacts, rules, recipes, fallbacks, precedents, candidates, resolutions, gaps and proposals, and nothing about buttons or colours. A design system enters only as a pack.

**Status:** the specification is frozen at 0.2.0 (tag `v0.2.0`).

**For humans:** click **Use now** (or scroll to the block below) and copy it into your coding agent on the machine that will do the work. The agent installs everything, proves it works, and validates what it builds.
**For agents:** the Use now block below is your task. Do it in order, verify every expected output, and stop to report if one of them fails. The long-form reference for each step follows under "Install (for agents)".

## Use now

Copy the whole block into your coding agent (Claude Code, Cursor, opencode, Hermes). Nothing else is required from you.

```text
Set up the Design Authority on this machine, then work under it. Steps, in order, verifying each expected output:

0. If `git` or `python3` is missing, stop and tell me. `python3 --version` must be 3.12 or newer.

1. Clone the repository:
   git clone https://github.com/vjsyong/design-authority.git ~/design-authority
   If ~/design-authority already exists, run git -C ~/design-authority pull instead.

2. Set up the MCP server environment:
   python3 -m venv ~/design-authority/.venv
   ~/design-authority/.venv/bin/pip install 'mcp<2'

3. Prove the authority works:
   python3 ~/design-authority/tools/da.py overview
   Expected: triage 0.12.1, 80 artifacts (component=56, guideline=10, pattern=7, token-set=7), and the resolution ladder printed.
   python3 ~/design-authority/tools/da.py resolve "a primary button"
   Expected: OUTCOME: RESOLVED citing component/btn.
   If either fails, stop and paste the output to me.

4. Adopt the consumption protocol: append ~/design-authority/packs/triage/AGENT-PROMPT.md to this project's agent rules (AGENTS.md or CLAUDE.md). From now on you resolve before building, mark what has no authority record, and report gaps instead of inventing canon.

5. Pull the Triage foundations into this project when you start building: copy ~/design-authority/dist/triage/ (tokens.css, base.css, patterns.css, fonts/) into the project, load them in that order, and take every visual value from the tokens. Do not hand-roll colours, spacing, or type.

6. Connect the MCP server if your host supports MCP (Claude Code/Cursor: .mcp.json; Hermes: hermes mcp add; opencode: opencode.json; the blocks are under "Install (for agents)" in ~/design-authority/README.md). Set DA_PACK to ~/design-authority/packs/triage and DA_WORKSPACE to this project. If your host has no MCP support, use the step-3 commands for every design question instead.

7. Before claiming any build is done, validate it:
   python3 ~/design-authority/tools/da.py --pack ~/design-authority/packs/triage validate .
   Target: 0 errors. Fix findings at their source; never suppress them. Re-run until clean.

Then report back to me: the two proof outputs from step 3, whether MCP is connected, and the final validate score. I will then tell you what to build.
```

## Install (for agents)

### 0. Requirements and stop conditions

- Python 3.12 or newer (kernel and CLI are stdlib-only).
- The `mcp` package, pinned `<2`, in a venv, for the MCP server.
- Optional: Playwright browsers, needed only by `tools/da_verify.py`.

Stop and report to the human instead of improvising if: Python is older than 3.12, pip cannot install the `mcp` package, or your host has no MCP support (then use the CLI path only and say so explicitly).

### 1. Clone and prove the CLI (no dependencies)

```bash
git clone https://github.com/vjsyong/design-authority.git
cd design-authority
python3 tools/da.py overview
```

Expected: triage 0.12.1, 80 artifacts (component=56, guideline=10, pattern=7, token-set=7), and the resolution ladder printed. Then:

```bash
python3 tools/da.py resolve "a primary button"
```

Expected: `OUTCOME: RESOLVED` citing `component/btn`.

### 2. Install and launch the MCP server

```bash
python3 -m venv .venv && .venv/bin/pip install 'mcp<2'
```

The stdio launcher is `tools/da-mcp.py`. Environment: `DA_PACK` selects the pack (default `packs/triage`); `DA_WORKSPACE` is where gaps, proposals and the decision log are written. Set `DA_WORKSPACE` to the project you are working on, so its records travel with it.

### 3. Register with your host

Claude Code / Cursor (`.mcp.json` in the project being worked on):

```json
{"mcpServers": {"design-authority": {
  "command": "/path/to/design-authority/.venv/bin/python",
  "args": ["/path/to/design-authority/tools/da-mcp.py"],
  "env": {"DA_PACK": "/path/to/design-authority/packs/triage",
          "DA_WORKSPACE": "/path/to/your/project"}}}}
```

Hermes:

```bash
hermes mcp add design-authority \
  --command /path/to/design-authority/.venv/bin/python \
  --env DA_PACK=/path/to/design-authority/packs/triage \
  --env DA_WORKSPACE=/path/to/your/project \
  --args /path/to/design-authority/tools/da-mcp.py
```

opencode (project `opencode.json`):

```json
{"mcp": {"design-authority": {"type": "local",
  "command": ["/path/to/design-authority/.venv/bin/python", "/path/to/design-authority/tools/da-mcp.py"],
  "environment": {"DA_PACK": "/path/to/design-authority/packs/triage", "DA_WORKSPACE": "/path/to/your/project"}}}}
```

### 4. Verify over MCP

Call `authority_overview`; expected `"status": "ok"`. Then `resolve_design_problem("a primary button")`; expected RESOLVED citing `component/btn`. If the tools do not appear in your host, reload the client session. If they still do not appear, report the launcher path and any error output to the human.

### 5. Pull the foundations for building

Consumers build from the Triage foundations shipped in [`dist/triage/`](dist/triage/): `tokens.css`, `base.css`, `patterns.css` and `fonts/`, byte-identical to the pinned source. Load them in that order and wire the fonts per [`dist/triage/README.md`](dist/triage/README.md). Every visual value must come from the tokens.

### 6. Adopt the protocol (required)

Copy [`packs/triage/AGENT-PROMPT.md`](packs/triage/AGENT-PROMPT.md) into the project's agent rules (for example `CLAUDE.md` or `AGENTS.md`). It is the consumption protocol: resolve before building; build the recorded way; when the authority has no answer, mark the improvisation and report a gap; verify before claiming done. [`AGENTS.md`](AGENTS.md) at this repository's root repeats the machine entry point.

### 7. Make conformance binding

Add to CI:

```bash
python3 tools/da.py --pack packs/triage validate <project directory>
```

The lint gate fails on any error (score = `100 - 8·errors - 2·warnings - 0.5·infos`), so nonconforming work cannot merge.

### 8. Self-check this repository

```bash
./tools/check.sh
```

Expected: `gates: OK` (pack drift, coverage sweep, unit tests, goldens, MCP smoke, concept-site gate).

## Build out a new authority (skills for agents)

The upstream half of the loop, turning design precedent into a new pack, ships as agent skills:

- [`skills/synthesize-authority/SKILL.md`](skills/synthesize-authority/SKILL.md): source selection, quarantine, the gestalt gate, `decisions.json`, the review instrument, compilation (`docs/synthesis/tools/compile_pack.py`), calibration to 100% goldens, stress testing, and the governance path (gaps, adjudication, proposals, codification).
- [`skills/extract-design-evidence/SKILL.md`](skills/extract-design-evidence/SKILL.md): the evidence layer. Renderable mirror, screenshot-first protocol with interaction states, evidence tags with BASE/OVERRIDE, domain-partitioned teams, merge and re-verification rules.

Both are plain `SKILL.md` files an agent loads directly. The full working records, including the three completed derivations, are under `docs/synthesis/`.

**Live:** the concept explainer and five authority implementations are served at <https://designauthority.seanyong.xyz>. The reference design system itself, Triage, is at <https://triage.seanyong.xyz>.

**Headline:** in a controlled three-condition experiment (3 runs per condition, identical briefs, fresh agent context), agents working with the authority over MCP produced measurably better interfaces than agents given the same design system as a well-made static kit, which in turn beat agents with no design material at all. Blind review condition means of 25: **A 15.0** (naive) · **B 21.3** (static kit) · **C 21.7** (active authority).

## What's in the release

| # | Component | Status | Where |
|---|-----------|--------|-------|
| 1 | Frozen specification, 0.2.0 (tag `v0.2.0`) | frozen | [`docs/spec/`](docs/spec/00-index.md) + [freeze manifest](docs/spec/freeze-0.2.0.sha256) |
| 2 | Kit-agnostic kernel, CLI and MCP server | stable | `kernel/`, `tools/da.py`, `tools/da-mcp.py` |
| 3 | Reference authority: Triage 0.12.1 | 80 artifacts · 19 rules · coverage 134/134 · goldens 54/54 | `packs/triage/` |
| 4 | A/B/C authority benchmark | complete | `docs/08`–`docs/11`, `benchmark/` |
| 5 | Authority-evolution loop | complete | `docs/evolution/` |
| 6 | Second-authority portability spike | complete | `docs/portability/` |
| 7 | Authority synthesis: one brief, three authorities | complete | `docs/synthesis/` |
| 8 | Independent verification experiment | complete | `docs/verification/` |
| 9 | Public concept site and review estate | live | `examples/designauthority-site/`, `docs/synthesis/review-app/` |
| 10 | Synthesis skills: brand kit to authority | shipped | [`skills/`](skills/) |
| 11 | Triage foundations distribution | shipped | [`dist/triage/`](dist/triage/) |

## Headline results

**The benchmark.** Three conditions, three runs each: A, no design material; B, the Triage design system as a static kit; C, the same system as an active authority over MCP. Every run built the same brief in a sandboxed workspace; a blind human review scored the deliverables. C 21.7, B 21.3, A 15.0 out of 25. The finding is not just that access mode beats documentation mode. The transcripts show why: agents with the authority check before they build, and when the authority is silent they surface the decision instead of burying it. Reports: [`docs/08-production-report.md`](docs/08-production-report.md), [`docs/09-final-synthesis.md`](docs/09-final-synthesis.md), [`docs/10-final-report.md`](docs/10-final-report.md).

**Synthesis: one brief, three design languages.** The same habit-tracker brief was built three times under three authorities synthesized from very different precedent (expressive, editorial, institutional). Eleven accepted proposals became canon; twenty-five recorded declines steer later asks toward sanctioned alternatives. The three builds share functionality and diverge on every visual and structural decision. Record: [`docs/synthesis/`](docs/synthesis/).

**Verification: agent self-report is evidence, not proof.** An independent verifier inspects the artifact, never the agent's claims. A blind verifier was calibrated with mutants (planted violations it must catch), then hardened against its own failure modes. A fresh verifier run is the only trusted confirmation. Record: [`docs/verification/`](docs/verification/).

**The reference conversion.** The Triage pack was converted 1:1 from the design system's own machine-readable spec files, then matured through outside review and an element-by-element coverage sweep (134/134 natural-language asks resolve to the right element). The sweep exists because a golden set written by the same extractor shares its blind spots: coverage must come from the system's own information architecture, or whole classes of misses stay silent.

**Limits.** Level 2 of the four-level verification contract is partial and declared per component; levels 3 and 4 are proposed. And nobody has yet shown that compliant builds behave better in users' hands. That experiment is next.

## Specification (0.2, frozen)

| file | contents |
|---|---|
| [`docs/spec/00-index.md`](docs/spec/00-index.md) | status, scope, conformance |
| [`docs/spec/01-definitions.md`](docs/spec/01-definitions.md) | normative glossary |
| [`docs/spec/02-pack-format.md`](docs/spec/02-pack-format.md) | architecture + pack data model |
| [`docs/spec/03-resolution-semantics.md`](docs/spec/03-resolution-semantics.md) | resolution pipeline, scoring, outcomes |
| [`docs/spec/04-interfaces.md`](docs/spec/04-interfaces.md) | MCP tools, CLI, records, validator runner |
| [`docs/spec/05-governance-and-freeze.md`](docs/spec/05-governance-and-freeze.md) | evolution loop, versioning, the freeze declarations |
| [`docs/spec/freeze-0.2.0.sha256`](docs/spec/freeze-0.2.0.sha256) | checksums of the frozen surface (current) |
| [`docs/spec/freeze-0.1.0.sha256`](docs/spec/freeze-0.1.0.sha256) | the 0.1.0 manifest (historical) |

## Repository layout

```
kernel/design_authority/   kernel (pack, search, resolve, validate, records, CLI, MCP)
tools/                     da CLI + MCP entrypoint, pack builders, verifier (da_verify), gates
dist/triage/               Triage foundations for consumers (tokens, base, patterns, fonts; byte-identical)
packs/triage/              reference authority: Triage 0.12.1 (pinned commit, drift-gated)
packs/triage-evolution/    0.13.0-experiment release (authority-evolution outcome)
packs/wink · leader · dominion/   synthesized authorities (codified)
packs/orbit · indaba/             portability-spike authorities
docs/spec/                 the frozen specification
docs/evolution/            the evolution experiment record (00…06 + data)
docs/portability/          the second-authority spike record (00…12)
docs/synthesis/            the synthesis experiment record (00…16) + review app + concept site data
docs/verification/         the independent-verification experiment record
examples/                  Cadence builds (wink/leader/dominion, v1–v3) + the concept site
benchmark/                 Procura starter, briefs, harness, reports (runs are archived locally)
workspaces/                consumer workspaces; the concept site's ledger records ship with it
```

## Research discipline notes

- Deterministic validation is kept separate from agent judgment; the authority never fabricates: every answer cites pack IDs the server validates.
- UNDEFINED is a legitimate, useful outcome. The correct response is to implement per policy, mark the improvisation, and report a gap.
- Declines are policy-only (lenient adjudication, [`docs/spec/05`](docs/spec/05-governance-and-freeze.md) §1): evidence-poor asks defer to UNDEFINED or become candidates; a precedent `outside` verdict means the ask is explicitly not governed.
- Consumers never modify packs; proposals are reviewed upstream. See [`docs/spec/05-governance-and-freeze.md`](docs/spec/05-governance-and-freeze.md) for how releases are made.
- Thresholds and acceptance rules are pre-registered before runs; criteria that failed as first written stay in the record.
- Negative and null results are reported as such (a pruning study NO-GO, a null on frontier feedback) and invalid or truncated runs stay archived, never deleted.
- Every compliance claim cites rule id, component, implementation, and evidence. Lint scores are gates, never proof.

## Provenance

Completed experiments document this system: the A/B/C authority benchmark (`docs/08`–`docs/11`), the authority-evolution loop (`docs/evolution/`), the second-authority portability spike (`docs/portability/`), the authority synthesis experiment (`docs/synthesis/`), and the independent verification experiment (`docs/verification/`). The **0.1.0 freeze** (2026-10-07) crowned the first two; the **0.2.0 freeze** (2026-10-08) formalizes the post-freeze era (negative precedents + candidates as optional records, precedent scope verdicts, lenient adjudication) on the same frozen surface. Full record: [`docs/11-consolidation-since-0.1.0.md`](docs/11-consolidation-since-0.1.0.md).

Authority packs compile from their source systems with recorded provenance: the Triage pack from the `triage-design-system` repository's own spec files (the compiled pack is included here; rebuilding it needs that repository), and the phantom, wink, leader and dominion authorities from screenshot-first extraction and synthesis. The concept site consumes Triage's token and core styles byte-identical; its Authority ledger, gaps and proposal live under `workspaces/designauthority-site/`.

## License

Code in this repository is released under the MIT License (see [`LICENSE`](LICENSE)). Design-system extracts and evidence material under `docs/synthesis/phantom/` derive from a third-party site and remain subject to its own terms.
