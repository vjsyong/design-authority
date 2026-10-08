# Archive manifest - phantom

Authority: `packs/phantom` @ 0.2.0 - generated 2026-10-08T17:18:25+00:00 UTC

| file | role | sha256 (first 16) | size |
|---|---|---|---|
| `audit.jsonl` | machine-recorded authority call trace | `80a3ab40fc318868` | 91708 |
| `brief.md` | build brief | `480a1d1e37f09ad0` | 2276 |
| `index.html` | page | `1c65f947d65f1d6d` | 75159 |
| `log.md` | build log (agent, 1:1 with audit.jsonl) | `fb51b6ca47075014` | 22753 |
| `run-authority` | audited runner (build-time tool) | `e0ee73c745af26be` | 1036 |
| `source-sans-pro-300-latin.woff2` | brand font file | `a327a082ad3f8b9d` | 14692 |
| `source-sans-pro-700-latin.woff2` | brand font file | `45c6a51457cd1a53` | 14628 |
| `source-sans-pro-900-latin.woff2` | brand font file | `2eaf3ae2fe28e9aa` | 14092 |
| `styles.css` | stylesheet | `e33eedfbc77736e4` | 13282 |
| `.design-authority/gaps.jsonl` | gap store (filed gaps) | `eda32cd8002b1e31` | 1277 |

External references: 0 (must be 0).

- `source-sans-pro-700-latin.woff2`: byte-identical to `examples/phantom-audit/assets/fonts/source-sans-pro-700-latin.woff2` -> True
- `source-sans-pro-300-latin.woff2`: byte-identical to `examples/phantom-audit/assets/fonts/source-sans-pro-300-latin.woff2` -> True
- `source-sans-pro-900-latin.woff2`: byte-identical to `examples/phantom-audit/assets/fonts/source-sans-pro-900-latin.woff2` -> True

Verify: `python3 tools/archive_authority_assets.py --verify phantom`
