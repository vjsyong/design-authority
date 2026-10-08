# Archive manifest - orbit

Authority: `packs/orbit` @ 0.1.0 - generated 2026-10-08T22:49:18+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `.site-state.json` | refresh state (pack hash, version, artifact set) | `591b180a78b7b2ba` | 1192 |
| `agent-brief.md` | asset | `d014204c8021117b` | 2216 |
| `audit.jsonl` | machine-recorded authority call trace | `1fb633c5722cb391` | 39692 |
| `brief.md` | build brief | `6c6d5d4122ee3d9d` | 2289 |
| `index.html` | page | `c2d49464b9f098b9` | 55937 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `f8a8dc335ddbaef6` | 30455 |
| `refresh-log.md` | refresh log (generated layers vs pack) | `00642a71121f8380` | 1652 |
| `run-authority` | audited runner (build-time tool) | `6820fc2e2533a95e` | 1030 |
| `styles.css` | stylesheet | `c8fc9e07691ba627` | 10366 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `ff3c62d888d6c0ee` | 1576 |

External references: 1 (must be 0).


Verify: `python3 tools/archive_authority_assets.py --verify orbit`
