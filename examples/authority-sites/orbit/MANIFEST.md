# Archive manifest - orbit

Authority: `packs/orbit` @ 0.1.0 - generated 2026-10-08T22:39:16+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `.site-state.json` | refresh state (pack hash, version, artifact set) | `c3c3ac80a84dd148` | 1192 |
| `audit.jsonl` | machine-recorded authority call trace | `1fb633c5722cb391` | 39692 |
| `brief.md` | build brief | `6c6d5d4122ee3d9d` | 2289 |
| `index.html` | page | `adf9cea9a7c339b6` | 55724 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `f8a8dc335ddbaef6` | 30455 |
| `refresh-log.md` | refresh log (generated layers vs pack) | `d88a627012bb1909` | 252 |
| `run-authority` | audited runner (build-time tool) | `6820fc2e2533a95e` | 1030 |
| `styles.css` | stylesheet | `5c3a29b4ca13487d` | 10565 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `ff3c62d888d6c0ee` | 1576 |

External references: 1 (must be 0).


Verify: `python3 tools/archive_authority_assets.py --verify orbit`
