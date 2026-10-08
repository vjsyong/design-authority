# Archive manifest - dominion

Authority: `packs/dominion` @ 0.2.0 - generated 2026-10-08T22:43:49+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `.site-state.json` | refresh state (pack hash, version, artifact set) | `eb3b3c5da1d76b14` | 905 |
| `agent-brief.md` | asset | `3c29043fc99cf80a` | 2326 |
| `audit.jsonl` | machine-recorded authority call trace | `7d48d3ccc4215654` | 45467 |
| `brief.md` | build brief | `5dc7fad11d7f981b` | 2223 |
| `index.html` | page | `77bf4df69ea1d87d` | 38932 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `948345edc036543f` | 33797 |
| `refresh-log.md` | refresh log (generated layers vs pack) | `7e9aef8a4f49fa05` | 820 |
| `run-authority` | audited runner (build-time tool) | `e22276930fe7da67` | 1039 |
| `styles.css` | stylesheet | `e1b2ff7884364154` | 13301 |
| `fonts/Arimo-VF.ttf` | brand font file | `e43898b143ec826a` | 496268 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `ff7688dd4c575f0d` | 2441 |

External references: 1 (must be 0).

- `fonts/Arimo-VF.ttf`: byte-identical to `docs/synthesis/dominion/tile/fonts/Arimo-VF.ttf` -> True

Verify: `python3 tools/archive_authority_assets.py --verify dominion`
