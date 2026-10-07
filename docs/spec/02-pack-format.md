# 02 · Architecture and pack format

## System architecture

```
reference design system (snapshot, pinned commit)
        │  build (tools/build_pack_triage.py; curation layer composed in)
        ▼
Authority Pack  ──────────────► served by tools
 (JSON directory)               ├─ da CLI            (humans, scripts)
        ▲                       ├─ da-mcp            (MCP stdio server, agents)
        │ governance            └─ validators         (declared commands)
        │ (see 05)
curation layer (human-authored: aliases, recipes, guidelines, maps,
                evolution provenance overlay)

consumer workspace
 └─ .design-authority/   ← gap records, proposals, decision log  (never touches the pack)
```

- The kernel MUST NOT contain system-specific knowledge; all design content
  lives in the pack.
- Consumers interact through the tool surface only. Records are written to the
  **consuming workspace**, never to the pack (see `04-interfaces.md`).
- The reference implementation is stdlib-only Python (3.12); packs are plain
  JSON directories; there is no database.

## Pack directory

Required files (relative to the pack root; the manifest's `entrypoints` MAY
rename them):

| file | top-level key | required | contents |
|---|---|---|---|
| `authority.json` | — | ✓ | manifest (below) |
| `artifacts.json` | `artifacts` | ✓ | citable artifacts |
| `rules.json` | `rules` | ✓ | enforceable rules |
| `scoring.json` | — | ✓ | scoring formula + gate description |
| `recipes.json` | `recipes` | opt | sanctioned compositions |
| `fallbacks.json` | `fallbacks` | opt | scoped fallbacks |
| `prohibitions.json` | `prohibitions` | opt | explicit prohibitions |
| `validators.json` | `validators` | opt | declared validator commands |
| `golden.json` | — | opt | golden set (conformance evidence) |
| `BUILD.json` | — | opt | build receipt (volatile; excluded from drift checks) |
| `curation/` | — | opt | hand-authored inputs (not resolved at runtime) |

## Manifest — `authority.json`

| field | type | required | meaning |
|---|---|---|---|
| `id` | string | ✓ | authority id (e.g. `triage`) |
| `name` | string | ✓ | human name |
| `format_version` | string | ✓ | pack data-model version; `0.1` here |
| `version` | string | ✓ | content version of this pack |
| `snapshot` | object | ✓ | `{repo, commit, branch, version, path_hint}` of the reference system |
| `description` | string | opt | one-line purpose |
| `kinds` | string[] | opt | declared artifact kinds |
| `capabilities` | object | opt | `{search, resolve, validators[], gap_reporting, extension_proposals, resolution_assist}` — `resolution_assist` MUST be `"off"` in 0.1 |
| `policy` | object | opt | `{on_undefined, on_conflict, proposals}` — human-readable policy strings surfaced with the respective outcomes |
| `entrypoints` | object | opt | file overrides for the standard entrypoint names |

## Artifacts — `artifacts.json`

`{"artifacts": [ … ]}`. Entry fields:

| field | type | required | meaning |
|---|---|---|---|
| `id` | string | ✓ | `<kind>/<slug>`, globally unique across the pack |
| `kind` | string | ✓ | one of the manifest kinds |
| `title` | string | ✓ | short name |
| `summary` | string | opt | one-sentence description |
| `status` | string | opt | lifecycle: `stable` / `beta` / `experimental` / `deprecated` |
| `aliases` | string[] | opt | search terms; multi-word entries are phrases |
| `body` | object | opt | kind-specific payload: `class`, `states`, `verify`, `a11y`, `do`, `dont`, `quote`, `statement`, `group`, … |
| `relations` | object | opt | links to other ids |
| `source` | object | opt | `{repo, commit, path}` — where in the snapshot it comes from |
| `provenance` | object | opt | provenance block (governance; see `05`) |

Rules — `rules.json`: `{id, name, severity (error|warning|info), applies_to[],
summary, why, fix, enforcement}`. Rule ids are short symbols (`TDS001`).

Recipes — `recipes.json`: `{id, kind: "recipe", title, summary, needs[],
ingredients[], constraints[], evidence{source, quote}, provenance?}`. Every
`ingredients` id MUST exist in the pack (the builder refuses to emit unknown
ingredients).

Fallbacks — `fallbacks.json`: `{id, title, statement, scope[], constraints[]}`.
`scope` tokens are matched against normalized query tokens; the wildcard `*`
is allowed in `scope` but never participates in matching (fallbacks are
non-catch-all by construction).

Prohibitions — `prohibitions.json`: `{id, statement, signals[],
signals_all[]?, detect?, rule?}`. `detect` supports `color_literal`; `signals`
are substring-matched against the lowercased problem; `signals_all` entries
are token-groups that must all be present.

Validators — `validators.json`: `{name, title, kind, workdir, command[],
parser, applies_to[], rules_source, notes}`; `{snapshot}` and `{target}` are
substituted at run time (see `04-interfaces.md`).

## Provenance extension (format 0.1, additive)

`0.1` permits two additive extensions used by the governance process:

1. **Provenance block** on any pack entry (usually attached by the pack
   builder from the curation overlay `curation/evolution.json`):
   `{introduced_in|extended_in, triggering_gaps[], review_decision,
   source_commit, tests[]}`.
2. **Release metadata** in `BUILD.json`: `release: {label, kind, experiment,
   based_on, source_branch, evidence, review}`.

Consumers MUST ignore unknown keys in pack files; they MUST NOT require
provenance blocks for resolution.

## Build and drift

- The pack builder composes snapshot + curation deterministically; the receipt
  (`BUILD.json`) records the snapshot, counts, curation hashes, warnings, and
  (when present) release metadata.
- A **drift gate** re-runs the build and compares generated files (excluding
  `BUILD.json`) against the committed pack; a pinned pack MUST pass with zero
  drift.
- `BUILD.json` is volatile (timestamps) and excluded from drift comparison.
