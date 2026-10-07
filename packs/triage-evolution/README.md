# Triage Authority Pack

Generated from the pinned snapshot `vjsyong/triage-design-system @ e374f38`
(v0.12.1). **Do not edit the generated files by hand** — edit `curation/` and
rerun:

```bash
python3 tools/build_pack_triage.py            # build
python3 tools/build_pack_triage.py --check    # drift gate (CI-style)
```

## Contents

| File | Kind | Notes |
|---|---|---|
| `authority.json` | manifest | id, format_version, snapshot pin, capabilities, policy |
| `artifacts.json` | 73 artifacts | components 35 · patterns 7 · guidelines 13 · token-sets 6 · examples 7 · references 5 |
| `rules.json` | 15 rules | pass-through of `spec/rules.json` + enforcement binding |
| `recipes.json` | 14 recipes | sanctioned compositions extracted from INTERACTION.md / docs |
| `fallbacks.json` | 3 fallbacks | sanctioned generic fallbacks (plain-content, native-control, omit-and-report) |
| `prohibitions.json` | 9 prohibitions | CONFLICT triggers (rules + interaction standard) |
| `validators.json` | 1 validator | `triage-lint` command adapter |
| `scoring.json` | — | score formula + gate from the snapshot |
| `BUILD.json` | receipt | counts, curation hashes, warnings, build time |

`curation/` holds the hand-authored inputs: per-artifact aliases and notes,
docs mapping, recipes, guidelines, fallbacks, prohibitions, token sets,
pattern registry, references. Cross-references are validated at build time
(an unknown ingredient/reference fails the build).

## Known approximations (recorded in BUILD.json + docs/04-gap-log.md)

- `docs-map.json` maps components to docs *group pages* approximately.
- Full DTCG schema conformance is pending (D-015); structural sanity only.
