# Archive manifest - indaba

Authority: `packs/indaba` @ 0.1.0 - generated 2026-10-08T22:49:18+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `.site-state.json` | refresh state (pack hash, version, artifact set) | `cbd67f60ef083270` | 1200 |
| `agent-brief.md` | asset | `189701fefefbe90a` | 2248 |
| `audit.jsonl` | machine-recorded authority call trace | `7323866f1d482d8b` | 75235 |
| `brief.md` | build brief | `931327d447f25d72` | 2265 |
| `index.html` | page | `b981405df2d54512` | 51136 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `6e40af137226d2a1` | 56176 |
| `refresh-log.md` | refresh log (generated layers vs pack) | `0f1857fe107aa294` | 1657 |
| `run-authority` | audited runner (build-time tool) | `15ae6227c5f323dc` | 1033 |
| `styles.css` | stylesheet | `57e20375f7373268` | 9235 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `a23e332fddfe93a5` | 1726 |

External references: 1 (must be 0).


Verify: `python3 tools/archive_authority_assets.py --verify indaba`
