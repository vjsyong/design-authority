# Archive manifest - indaba

Authority: `packs/indaba` @ 0.1.0 - generated 2026-10-08T17:07:39+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `audit.jsonl` | machine-recorded authority call trace | `7323866f1d482d8b` | 75235 |
| `brief.md` | build brief | `931327d447f25d72` | 2265 |
| `index.html` | page | `004d9206a10f1593` | 17733 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `6e40af137226d2a1` | 56176 |
| `run-authority` | audited runner (build-time tool) | `15ae6227c5f323dc` | 1033 |
| `styles.css` | stylesheet | `4893438c30b1265c` | 5486 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `a23e332fddfe93a5` | 1726 |

External references: 0 (must be 0).


Verify: `python3 tools/archive_authority_assets.py --verify indaba`
