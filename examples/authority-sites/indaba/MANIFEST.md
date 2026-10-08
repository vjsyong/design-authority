# Archive manifest - indaba

Authority: `packs/indaba` @ 0.1.0 - generated 2026-10-08T22:39:16+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `.site-state.json` | refresh state (pack hash, version, artifact set) | `0d46950c5ccc9259` | 1200 |
| `audit.jsonl` | machine-recorded authority call trace | `7323866f1d482d8b` | 75235 |
| `brief.md` | build brief | `931327d447f25d72` | 2265 |
| `index.html` | page | `1c637407003fbdbd` | 51130 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `6e40af137226d2a1` | 56176 |
| `refresh-log.md` | refresh log (generated layers vs pack) | `d88a627012bb1909` | 252 |
| `run-authority` | audited runner (build-time tool) | `15ae6227c5f323dc` | 1033 |
| `styles.css` | stylesheet | `d0181eaa391de0f7` | 9436 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `a23e332fddfe93a5` | 1726 |

External references: 1 (must be 0).


Verify: `python3 tools/archive_authority_assets.py --verify indaba`
