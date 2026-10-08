# Archive manifest - dominion

Authority: `packs/dominion` @ 0.2.0 - generated 2026-10-08T17:20:41+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `audit.jsonl` | machine-recorded authority call trace | `7d48d3ccc4215654` | 45467 |
| `brief.md` | build brief | `5dc7fad11d7f981b` | 2223 |
| `index.html` | page | `5d0dc9775763b959` | 37980 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `948345edc036543f` | 33797 |
| `run-authority` | audited runner (build-time tool) | `e22276930fe7da67` | 1039 |
| `styles.css` | stylesheet | `db520a2c9c8be351` | 12712 |
| `fonts/Arimo-VF.ttf` | brand font file | `e43898b143ec826a` | 496268 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `ff7688dd4c575f0d` | 2441 |

External references: 0 (must be 0).

- `fonts/Arimo-VF.ttf`: byte-identical to `docs/synthesis/dominion/tile/fonts/Arimo-VF.ttf` -> True

Verify: `python3 tools/archive_authority_assets.py --verify dominion`
