# G1 adversarial verdict — Orbit v2 (NASA line, retired)

Dispatched 2026-10-07 10:03 (deleg_aa7c81b8, leaf, 708s). Full trace:
`g1-orbit-v2-transcript.log` (same directory).

**Verdict: PASS-WITH-FIXES** — zero structural twins (verified by live-DOM
computed styles + pixel sampling: no borders, no radius, exactly one box in
the mock — the captioned figure; all five v1 twins demonstrably gone).
Confidence ~75–80% that the reviewer gate passes after three fixes.

**Eight WEAK residuals** (none TWIN; genre-floor or relocated devices).
Top three risks as ranked by G1:

1. **Register residue** — hairline row separation + dedicated right-aligned
   action column + stacked-blocks mobile adaptation (all named in the v1
   rejection record). Fix suggested: delete the redundant "Open" column.
2. **Micro-label vocabulary relocated, not retired** — the 5px ink square
   before tags is the incumbent's dot+label device, shrunk and monochrome;
   filled status plates occupy the badge slot. Fix: dash instead of square;
   benign states as plain text.
3. **Ink-filled action plate ≡ incumbent's primary paint** — same fill/text/
   height as `.btn.primary` in a different slot. Fix: accent-underlined text
   command or a sign band for the destructive action.

## The layer-gap, on the record

G1 independently flagged **two of the reviewer's three named axes** — the
square "dots" (residual #2) and the high-contrast black plates (#3) — but
graded them *fixable WEAK residuals* rather than disqualifiers, and rated the
anatomy as likely passing. The human reviewer failed the same artifact on
gestalt instantly. Conclusion: **adversarial anatomy gates systematically
under-weight gestalt**; the reviewer's named axes must be hard-fail criteria
in any internal gate, and gestalt screening must occur before anatomy work
(the ST style-tile gate, `08` §2.3). This under-line is itself the spike's
most reusable process finding.

## Render-fidelity caveats (moot for the live line; retained as checklist)

- Mock PNGs were set in a fontconfig substitute (Liberation Sans metrics), so
  the intended Light display weight collapsed — the v3 pipeline renders with
  vendored real fonts (Ubuntu family) and a font check step.
- Dialog scrim covered only the content column in the static mock (white
  gutters) — future screen renders must dim the full page.

NASA/Orbit v2 is retired (`07` banner); these findings apply to the process
record and to the v3 (Ubuntu / “Indaba”) renderer checklist.
