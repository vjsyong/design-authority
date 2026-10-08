# Triage foundations (consumer distribution)

Byte-identical copy of the Triage v0.12.1 foundations, shipped so you can build
under the `triage` pack without access to the source repository.

- `tokens.css` - the design tokens (colour, type, spacing, radius, motion)
- `base.css` - element styles and core components
- `patterns.css` - layout and page patterns
- `fonts/` - Geist and Geist Mono (woff2, OFL)

Load order: tokens.css, then base.css, then patterns.css. Wire the fonts with
@font-face:

```css
@font-face{font-family:Geist;src:url('fonts/geist.woff2') format('woff2');font-weight:100 900;font-display:swap}
@font-face{font-family:'Geist Mono';src:url('fonts/geist-mono.woff2') format('woff2');font-weight:100 900;font-display:swap}
```

Every visual value must come from the tokens. Validate your build with
`python3 tools/da.py --pack packs/triage validate <your project>` (0 errors is
the bar). The repository gate (`tools/check_concept_site.py`) re-checks these
files byte-for-byte against the pinned source; do not edit them by hand.
