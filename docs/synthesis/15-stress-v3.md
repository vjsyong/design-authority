# 15 — Stress Test v3: rebuilt on the codified authorities

Third Cadence build, same spec, run against `packs/* @ 0.2.0` (11 accepted
proposals compiled) + the 25 negative precedents. This closes the loop:
verdict → canon or precedent → **the next build consumes both**.

## Headline numbers (42 asks per pack)

| | v1 (gaps) | v2 (fixes) | **v3 (codified + precedents)** |
|---|---|---|---|
| wink — R / F / U | 4(+6) / 5 / 27 | 5 / 8 / 30 | **12 / 8 / 22** |
| leader — R / C / F / U | 6 / – / 8 / 28 | 9 / 1 / 10 / 18* | **14 / 0 / 10 / 18** |
| dominion — R / C / F / X / U | 5 / – / 6 / 3 / 28 | 6 / 2 / 7 / 3 / 24 | **11 / 2 / 7 / 3 / 19** |
| gaps filed | 48 | 40 | **17** (wink 6 · leader 5 · dominion 6) |

\* v2 leader figure from its own log (17 improvised + 5 adapted).

## What the new canon did

- **wink**: the delete flow resolves through `pattern/destructive-confirm`
  (no more improvised modal); `dialog-overlay`, `empty-state`,
  `inline-notice`, `pattern/progress` all consumed; RESOLVED calls more than
  doubled (5 → 12).
- **leader**: `pattern/data-charts` (bar chart, month grid, heatmap,
  sparkline), `pattern/data-readouts` (streak/stat), `component/tag` all
  resolve — the six chart/readout/tag asks that were fully improvised in v2
  are now canon; R 9 → 14.
- **dominion**: `component/status`, `component/ledger`, `component/notice`,
  `pattern/plain-chart` consumed; the retire recipe composes; R 6 → 11;
  UNDEFINED down to 19.

## What the precedents did (negative feedback, measured)

**49 precedent attachments across the three builds**, every try-list followed
and marked:

- wink — 15 attachments, 7 precedents fired (charts, imagery/glyphs, native
  controls, pager/drag, status-pill, csv, dark-mode)
- leader — 17 attachments, **all 10** precedents fired (incl. both rejected
  proposals: destructive-confirm and ledger — builders routed to ruled-panel
  confirms and composed tables with the warnings in hand)
- dominion — 17 attachments, **all 7** precedents fired (ring→meter,
  motion→static ceremony + notice, imagery→initials/statements,
  pictograms→ordinals, tabs→masthead states, dark→light fallback)

Agents met declined asks and instead of re-inventing them, received the
reason + the sanctioned alternative at resolve time, and the gap/proposal
flows warned on re-treads. Gaps filed dropped 40 → 17 and none overlap the
declined set.

## Verification

- All three serve via `/stress3/*`; independent Playwright pass: zero console
  errors, ◌ marks toggle works, marked nodes present (wink 74 / leader 41 /
  dominion 42).
- Builders' self-tests: wink 90/90 (its final run landed before the task was
  interrupted — only the closing report was lost; artifacts complete and
  re-verified here), leader 106/106, dominion 110/110. Ports killed.
- Battery after the run: drift ✓ · kernel 15/15 · triage 19/19 · synthesis
  goldens 18/14/17 · precedents probe 18/18 · MCP 18/18.

## Kernel fix from this run (found by the dominion builder)

Precedent matching counted **stemmed** token length, so "tabs" → "tab"
(3 chars) slid under the strong-token bar and missed its precedent. Fixed:
single-word `matches` entries now record the original word length; a probe
case covers it (`tabs …` → `precedent/declined-view-tabs-paging`).

## Residual observations

- Search/query dilution remains: short asks inside long sentences score low
  (`select`, `banner` at 4.0 in-sentence vs 9.0 alone) — a known search
  property, thresholds stay frozen.
- dominion's generic details/empty-state/onboarding flows stay in-page per the
  rejected-dialog precedent — reconciliation is explicit and marked.
- leader/dominion builds keep a corner ◌ chip (marks toggle) that reads as a
  stray spinner to fresh eyes; intended.
