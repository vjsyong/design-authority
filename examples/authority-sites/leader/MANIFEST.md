# Archive manifest - leader

Authority: `packs/leader` @ 0.2.0 - generated 2026-10-08T22:39:16+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `.site-state.json` | refresh state (pack hash, version, artifact set) | `5007c9e70ee8123a` | 946 |
| `audit.jsonl` | machine-recorded authority call trace | `f7da1d1de4e6142f` | 59041 |
| `brief.md` | build brief | `df3478fd0113ece0` | 2259 |
| `index.html` | page | `9ed4a306176e107e` | 35515 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `fc60e498bf67f5f8` | 30662 |
| `refresh-log.md` | refresh log (generated layers vs pack) | `951006f53cdecc3e` | 252 |
| `run-authority` | audited runner (build-time tool) | `8c8eb36c2f2b22d7` | 1033 |
| `styles.css` | stylesheet | `c916c73146a06824` | 12768 |
| `fonts/ArchivoBlack-Regular.ttf` | brand font file | `dd9a89a019b4849f` | 90988 |
| `fonts/Gelasio-VF.ttf` | brand font file | `4daecea457258c9e` | 168556 |
| `fonts/Inter-VF.ttf` | brand font file | `29160a80ff49ddca` | 876576 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `cbf4c571d4c0c687` | 1915 |

External references: 1 (must be 0).

- `fonts/ArchivoBlack-Regular.ttf`: byte-identical to `docs/synthesis/leader/tile/fonts/ArchivoBlack-Regular.ttf` -> True
- `fonts/Inter-VF.ttf`: byte-identical to `docs/synthesis/leader/tile/fonts/Inter-VF.ttf` -> True
- `fonts/Gelasio-VF.ttf`: byte-identical to `docs/synthesis/leader/tile/fonts/Gelasio-VF.ttf` -> True

Verify: `python3 tools/archive_authority_assets.py --verify leader`
