# Authorities

Every authority lives in its own folder here, and each folder is its own git
repository. An authority repo owns everything about that authority: the pack
(records at the repo root), the shipped site build (`site/`), its archive
manifest and audit trail, its changelog, and its CI.

| folder | repo | version |
|---|---|---|
| `triage/` | `vjsyong/authority-triage` | 0.12.1 (pinned production line; generated from `~/triage-design-system`) |
| `triage-evolution/` | `vjsyong/authority-triage-evolution` | 0.13.1-experiment (governed evolution line) |
| `wink/` | `vjsyong/authority-wink` | 0.2.0 |
| `leader/` | `vjsyong/authority-leader` | 0.2.0 |
| `dominion/` | `vjsyong/authority-dominion` | 0.2.0 |
| `phantom/` | `vjsyong/authority-phantom` | 0.2.0 |
| `indaba/` | `vjsyong/authority-indaba` | 0.1.0 |
| `orbit/` | `vjsyong/authority-orbit` | 0.1.0 |

## Layout of an authority repo

    <authority>/
      authority.json, artifacts.json, rules.json, prohibitions.json,
      fallbacks.json, recipes.json, golden.json, candidates.json,
      precedents.json, scoring.json, verification.json   <- the pack (records)
      site/            the reference build (page, styles, fonts, manifests,
                       build log, machine-recorded audit trail, refresh log)
      CHANGELOG.md     one entry per version bump
      .github/workflows/ci.yml   the authority's own CI
      README.md        use + rollback in one screen

## Getting them

    bash authorities/bootstrap.sh     # clone/pull all of them here

The repos are public. The meta repo (kernel, tools, docs, the review app)
does not track their contents; `authorities/*/` is gitignored so the two
layers version independently.

## Versioning and rollback

`authority.json` carries the version; each release is tagged (`v0.2.0`).
To see what changed between bumps: `git log --oneline v0.2.0..v0.3.0`, or
diff the pack: `git diff v0.2.0 v0.3.0 -- '*.json'`. To roll back:
`git checkout v0.2.0` (pin) or `git revert` the bump commit (move forward
honestly). Site refreshes are committed to `site/` automatically, so the
served page has the same history discipline as the records.

## CI

Every authority repo runs its own CI on push: pack parses, golden agreement,
site manifest verification and the generated-chrome traceability gate (the
site steps run for authorities that ship a site). The meta repo's CI clones
all authorities and runs the integration gates (kernel tests, goldens, the
dispute fixtures, manifests + gates per site).

## Phase 2 (open)

Authority-specific evidence still lives in the meta repo: synthesis tiles
(`docs/synthesis/<auth>/`), the cadence builds (`examples/cadence3-*`), the
phantom audit console (`examples/phantom-audit`), portability docs, and the
font sources served by the `/authority-fonts` route. Moving them needs route
rewiring in the review app first; tracked as the remaining step of the
consolidation.
