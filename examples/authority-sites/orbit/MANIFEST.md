# Archive manifest - orbit

Authority: `packs/orbit` @ 0.1.0 - generated 2026-10-08T22:51:46+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `.site-state.json` | refresh state (pack hash, version, artifact set) | `78782af1720e3154` | 1192 |
| `agent-brief.md` | asset | `d014204c8021117b` | 2216 |
| `audit.jsonl` | machine-recorded authority call trace | `1fb633c5722cb391` | 39692 |
| `brief.md` | build brief | `6c6d5d4122ee3d9d` | 2289 |
| `index.html` | page | `b1db735246a69a88` | 55938 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `f8a8dc335ddbaef6` | 30455 |
| `refresh-log.md` | refresh log (generated layers vs pack) | `1aab1d3d243f3a51` | 1932 |
| `run-authority` | audited runner (build-time tool) | `6820fc2e2533a95e` | 1030 |
| `styles.css` | stylesheet | `8338eac07da19115` | 10366 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `ff3c62d888d6c0ee` | 1576 |

External references: 1 (must be 0).


Verify: `python3 tools/archive_authority_assets.py --verify orbit`
