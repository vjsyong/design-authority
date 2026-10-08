# 04 · Interfaces: MCP tools, CLI, records, validators

## 1 · MCP server (stdio)

Entrypoint: `tools/da-mcp.py` (wraps `kernel/design_authority/mcp_server.py`).
Environment: `DA_PACK` (pack directory; required), `DA_WORKSPACE` (consumer
workspace for records; defaults to the pack-adjacent workspace). Transport:
stdio, JSON-RPC via the MCP SDK (`mcp<2`).

### Tools (11)

| tool | parameters | returns |
|---|---|---|
| `authority_overview` | — | identity, counts, capabilities, policy, entrypoints, usage guide |
| `search_authority` | `query: str`, `kinds: str = ""` (comma list), `limit: int = 12` | ranked `{id, kind, title, score, matched}` |
| `discover_candidates` | `query: str`, `k: int = 8`, `include_history: bool = false` | fused-retrieval candidates `{id, kind, class, title, lex_rank, bm25, sem_rank, cos, rrf}` — a retrieval signal, NOT an outcome; canonical by default (0.4, optional; degrades to `status: unavailable` without the extras) |
| `inspect_artifact` | `id: str` | full artifact entry (body, aliases, source, relations) or structured not-found |
| `resolve_design_problem` | `problem: str`, `context: dict?`, `assist: str = ""` | the resolution output of `03-resolution-semantics.md`, incl. precedent/candidate attachments; `assist="semantic"` adds a `retrieval_assist` block on UNDEFINED (retrieval only, outcome classes unchanged) |
| `list_precedents` | `query: str = ""` | negative precedents (policy declines) with grounds, scope boundary and try-list; a `query` filters with scope verdicts |
| `check_precedent` | `ask: str`, `precedent_id: str = ""` | how the precedents apply to an ask **before deviating**: per-ask verdicts (`governs`/`outside`/`ambiguous`) + boundary hits + matching candidates |
| `list_candidates` | `query: str = ""` | provisional directions with `promote_when`; NOT authority |
| `validate_implementation` | `target: str`, `validators: str = ""` | findings + counts + score + per-validator meta |
| `report_gap` | `need: str`, `context: dict?`, `attempted_resolution: dict?`, `fallback_used: str = ""`, `evidence: list?`, `scope_hint: str = "unknown"` | the stored gap record (+ `precedent_warnings` / `candidate_hints` when matched) |
| `propose_extension` | `gap_id: str`, `proposal: dict` | the stored proposal record (+ review checklist, + `precedent_warnings` / `candidate_hints` when matched) |

`search_authority` kind filters: `component`, `pattern`, `guideline`,
`token-set`, `example`, `reference`, `recipe`, `precedent`, `candidate`.

### Resources (3)

`authority://overview` (manifest + usage), `authority://rules` (rule
catalogue), and `authority://artifact/{artifact_id}` (artifact detail).

### Guarantees

- Tool responses MUST cite only pack-validated ids.
- `report_gap` / `propose_extension` MUST write only under the consumer
  workspace's `.design-authority/` directory and MUST NOT modify the pack.
- A decision log (`.design-authority/decision-log.jsonl`) SHOULD be written on
  every tool call: entries carry timestamp, tool name, parameters, and a
  summary. It is best-effort audit data — **never load-bearing**, failures are
  swallowed, and no logic may depend on it.
- The retrieval assist (0.4) is optional and off by default: it adds retrieval
  candidates only, never outcomes; enabling it MUST NOT change outcome
  classes, and every returned id is still validated against the pack.

## 2 · CLI (`da`)

Entrypoint: `tools/da.py`. Global option: `--pack PATH` (pack directory;
default: the repository's `packs/triage`).

| command | args | purpose |
|---|---|---|
| `overview` | `[--json]` | manifest + counts |
| `search` | `QUERY [--kinds] [--limit] [--json]` | ranked search (incl. precedent/candidate kinds) |
| `discover` | `QUERY [--k] [--class canonical\|history\|all] [--index] [--legs] [--json]` | optional semantic discovery (retrieval signal only; needs the extras + a built index) |
| `inspect` | `ID` | full artifact |
| `resolve` | `PROBLEM… [--context] [--assist off\|semantic] [--assist-k] [--assist-index] [--json]` | resolution (+ attachments; optional retrieval hint on UNDEFINED) |
| `validate` | `TARGET [--snapshot PATH] [--json]` | run declared validators |
| `golden` | `[--file PATH] [--json]` | run the pack's golden set (defaults to the repository-pinned golden file) |
| `gaps` | `[--workspace] [--json]` | list gap records |
| `gap-add` | `--need X [--context] [--scope] [--workspace]` | record a gap |
| `propose` | `--gap ID --file JSON [--workspace]` | file a proposal |
| `review` | `--proposal ID --verdict {accept,reject,needs-info} [--note] [--notes FILE] [--workspace]` | record a consumer review verdict (updates the workspace proposal record) |
| `precedents` | `[--query Q] [--json]` | list negative precedents (with scope verdicts when filtering) |
| `precedent-check` | `--ask TEXT [--json]` | the pre-deviation check: verdicts + boundary hits + candidates |
| `candidates` | `[--query Q] [--json]` | list provisional candidates |

The CLI and MCP server MUST share one library (`kernel/design_authority/`).

## 3 · Records (consumer workspace)

Location: `<workspace>/.design-authority/`. Records are noncanonical by
construction; they never touch published packs.

### Gap record (`gaps.jsonl`, one JSON object per line)

```
{ id: "gap/<utcstamp>-<hex6>", need, context{}, authority{authority,version,commit},
  searched?, closest?, why_insufficient?, fallback_used?, evidence[], scope_hint,
  precedent_warnings?, candidate_hints?, status: "open", created }
```

`attempted_resolution` (when supplied to `report_gap`) enriches `searched`,
`closest`, and `why_insufficient`. Since 0.2, `precedent_warnings` records the
matched negative precedents (`{id, verdict}`) and `candidate_hints` the
matched candidates at creation time — the filer sees the decline before the
loop does.

### Proposal record (`proposals/<id-safe>.json`)

Required (creation fails without them): `problem`, `insufficiency`,
`reuse_case`, `composition_check`, `proposed`, `tests`. Plus: `gap_id`
(must reference a stored gap), `depends_on[]` (every id must exist in the
pack), `new_primitives[]`, `status` (`candidate` → `accepted` | `rejected` |
`needs-info`), `review {verdict, notes, evidence?, reviewed_at}`, and (0.2)
`precedent_warnings?` / `candidate_hints?` recorded at creation time.

Each stored proposal receives a 7-item review checklist (necessity, reuse,
composition, dependencies, new primitives, compliance tests, deterministic
checks) as review scaffolding.

### Consumer review verdicts

`accept` | `reject` | `needs-info`. Recording a verdict updates `status` and
the `review` block; **nothing is ever auto-applied to any pack** from this
surface.

## 4 · Validator runner

Declared in `validators.json`; executed against a target path with:

- `workdir`: `{snapshot}` substituted by the snapshot directory
  (`--snapshot` > `DA_SNAPSHOT` > manifest `snapshot.path_hint`); `{pack}`
  substituted by the authority's own pack directory (pack-local validator
  scripts; no snapshot repository required); a missing workdir is a
  structured error with a fix hint naming both substitutions;
- `command[]`: each argument gets `{target}` (absolute target path),
  `{snapshot}` and `{pack}` substituted;
- `parser`: `lint-json` (the SARIF-aligned report shape; the legacy name
  `triage-lint-json` remains accepted). Unknown parsers are structured errors.

Normalized finding: `{rule, severity, message, location{path,line}, fix,
excerpt}`. Summary: severity counts, total, per-rule counts, and a score:

```
score = max(0, round(100 − (errors×8 + warnings×2 + infos×0.5)))
```

The score formula and gate description live in the pack's `scoring.json`;
0.1 and 0.2 define no cross-pack composite metric beyond this per-run score.

## 5 · Error semantics

Structured, non-throwing errors are preferred over exceptions on all consumer
surfaces (missing pack files, unknown ids, missing workdir, unparseable
validator output). Tool/CLI failures MUST NOT corrupt records or packs.
