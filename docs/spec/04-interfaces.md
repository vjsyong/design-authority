# 04 · Interfaces: MCP tools, CLI, records, validators

## 1 · MCP server (stdio)

Entrypoint: `tools/da-mcp.py` (wraps `kernel/design_authority/mcp_server.py`).
Environment: `DA_PACK` (pack directory; required), `DA_WORKSPACE` (consumer
workspace for records; defaults to the pack-adjacent workspace). Transport:
stdio, JSON-RPC via the MCP SDK (`mcp<2`).

### Tools (7)

| tool | parameters | returns |
|---|---|---|
| `authority_overview` | — | identity, counts, capabilities, policy, entrypoints, usage guide |
| `search_authority` | `query: str`, `kinds: str = ""` (comma list), `limit: int = 12` | ranked `{id, kind, title, score, matched}` |
| `inspect_artifact` | `id: str` | full artifact entry (body, aliases, source, relations) or structured not-found |
| `resolve_design_problem` | `problem: str`, `context: dict?` | the resolution output of `03-resolution-semantics.md` |
| `validate_implementation` | `target: str`, `validators: str = ""` | findings + counts + score + per-validator meta |
| `report_gap` | `need: str`, `context: dict?`, `attempted_resolution: dict?`, `fallback_used: str = ""`, `evidence: list?`, `scope_hint: str = "unknown"` | the stored gap record |
| `propose_extension` | `gap_id: str`, `proposal: dict` | the stored proposal record (+ review checklist) |

### Resources (3)

`da://overview` (manifest + usage), `da://rules` (rule catalogue), and
`da://artifact/{id}` (artifact detail).

### Guarantees

- Tool responses MUST cite only pack-validated ids.
- `report_gap` / `propose_extension` MUST write only under the consumer
  workspace's `.design-authority/` directory and MUST NOT modify the pack.
- A decision log (`.design-authority/decision-log.jsonl`) SHOULD be written on
  every tool call: entries carry timestamp, tool name, parameters, and a
  summary. It is best-effort audit data — **never load-bearing**, failures are
  swallowed, and no logic may depend on it.

## 2 · CLI (`da`)

Entrypoint: `tools/da.py`. Global option: `--pack PATH` (pack directory;
default: the repository's `packs/triage`).

| command | args | purpose |
|---|---|---|
| `overview` | `[--json]` | manifest + counts |
| `search` | `QUERY [--kinds] [--limit] [--json]` | ranked search |
| `inspect` | `ID` | full artifact |
| `resolve` | `PROBLEM… [--context] [--json]` | resolution |
| `validate` | `TARGET [--snapshot PATH] [--json]` | run declared validators |
| `golden` | `[--file PATH] [--json]` | run the pack's golden set (defaults to the repository-pinned golden file) |
| `gaps` | `[--workspace] [--json]` | list gap records |
| `gap-add` | `--need X [--context] [--scope] [--workspace]` | record a gap |
| `propose` | `--gap ID --file JSON [--workspace]` | file a proposal |
| `review` | `--proposal ID --verdict {accept,reject,needs-info} [--note] [--notes FILE] [--workspace]` | record a consumer review verdict |

The CLI and MCP server MUST share one library (`kernel/design_authority/`).

## 3 · Records (consumer workspace)

Location: `<workspace>/.design-authority/`. Records are noncanonical by
construction; they never touch published packs.

### Gap record (`gaps.jsonl`, one JSON object per line)

```
{ id: "gap/<utcstamp>-<hex6>", need, context{}, authority{authority,version,commit},
  searched?, closest?, why_insufficient?, fallback_used?, evidence[], scope_hint,
  status: "open", created }
```

`attempted_resolution` (when supplied to `report_gap`) enriches `searched`,
`closest`, and `why_insufficient`.

### Proposal record (`proposals/<id-safe>.json`)

Required (creation fails without them): `problem`, `insufficiency`,
`reuse_case`, `composition_check`, `proposed`, `tests`. Plus: `gap_id`
(must reference a stored gap), `depends_on[]` (every id must exist in the
pack), `new_primitives[]`, `status` (`candidate` → `accepted` | `rejected` |
`needs-info`), and `review {verdict, notes, evidence?, reviewed_at}`.

Each stored proposal receives a 7-item review checklist (necessity, reuse,
composition, dependencies, new primitives, compliance tests, deterministic
checks) as review scaffolding.

### Consumer review verdicts

`accept` | `reject` | `needs-info`. Recording a verdict updates `status`;
**nothing is ever auto-applied to any pack** from this surface.

## 4 · Validator runner

Declared in `validators.json`; executed against a target path with:

- `workdir`: `{snapshot}` substituted by the snapshot directory
  (`--snapshot` > `DA_SNAPSHOT` > manifest `snapshot.path_hint`); a missing
  workdir is a structured error with a fix hint;
- `command[]`: each argument gets `{target}` substituted with the absolute
  target path;
- `parser`: `triage-lint-json` (0.1 reference parser). Unknown parsers are
  structured errors.

Normalized finding: `{rule, severity, message, location{path,line}, fix,
excerpt}`. Summary: severity counts, total, per-rule counts, and a score:

```
score = max(0, round(100 − (errors×8 + warnings×2 + infos×0.5)))
```

The score formula and gate description live in the pack's `scoring.json`;
0.1 defines no cross-pack composite metric beyond this per-run score.

## 5 · Error semantics

Structured, non-throwing errors are preferred over exceptions on all consumer
surfaces (missing pack files, unknown ids, missing workdir, unparseable
validator output). Tool/CLI failures MUST NOT corrupt records or packs.
