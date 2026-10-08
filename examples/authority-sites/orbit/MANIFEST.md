# Archive manifest - orbit

Authority: `packs/orbit` @ 0.1.0 - generated 2026-10-08T17:20:41+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `audit.jsonl` | machine-recorded authority call trace | `1fb633c5722cb391` | 39692 |
| `brief.md` | build brief | `6c6d5d4122ee3d9d` | 2289 |
| `index.html` | page | `2288f4f6c048a369` | 54783 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `f8a8dc335ddbaef6` | 30455 |
| `run-authority` | audited runner (build-time tool) | `6820fc2e2533a95e` | 1030 |
| `styles.css` | stylesheet | `7940090821fe7aec` | 9880 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `ff3c62d888d6c0ee` | 1576 |

External references: 0 (must be 0).


Verify: `python3 tools/archive_authority_assets.py --verify orbit`
