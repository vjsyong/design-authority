# Archive manifest - wink

Authority: `packs/wink` @ 0.2.0 - generated 2026-10-08T17:20:54+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `.site-state.json` | refresh state (pack hash, version, artifact set) | `9256c4da3c76ddcf` | 1090 |
| `audit.jsonl` | machine-recorded authority call trace | `9a914fce9b352d3a` | 86360 |
| `brief.md` | build brief | `3d10e0db45c1e1b3` | 2272 |
| `index.html` | page | `9ce33b8048552645` | 35914 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `c98f0a0abc03940d` | 25626 |
| `refresh-log.md` | refresh log (generated layers vs pack) | `012031ee46997ee6` | 245 |
| `run-authority` | audited runner (build-time tool) | `e8aa85be1b6de165` | 1027 |
| `styles.css` | stylesheet | `4bf4b9cfe0664f61` | 12013 |
| `fonts/Fraunces-Italic-VF.ttf` | brand font file | `b24448c43702fac4` | 414904 |
| `fonts/Fraunces-VF.ttf` | brand font file | `177ff6c0f14e5550` | 360440 |
| `fonts/Inter-VF.ttf` | brand font file | `29160a80ff49ddca` | 876576 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `832a97de25d5a841` | 2281 |

External references: 0 (must be 0).

- `fonts/Fraunces-Italic-VF.ttf`: byte-identical to `docs/synthesis/wink/tile/fonts/Fraunces-Italic-VF.ttf` -> True
- `fonts/Inter-VF.ttf`: byte-identical to `docs/synthesis/wink/tile/fonts/Inter-VF.ttf` -> True
- `fonts/Fraunces-VF.ttf`: byte-identical to `docs/synthesis/wink/tile/fonts/Fraunces-VF.ttf` -> True

Verify: `python3 tools/archive_authority_assets.py --verify wink`
