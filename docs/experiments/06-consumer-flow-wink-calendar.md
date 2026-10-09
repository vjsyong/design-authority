# Experiment 06 · Consumer flow test — a fresh agent builds "Wink Calendar" from the public entry point

Status: **findings record** (owner-directed test, 2026-10-09). The owner ran a
fresh Telegram agent (the `qwen` profile bot) through the public wink entry
path: *"Fetch the agent-brief and follow it to build my app under the Wink
Interface System."* The agent built a calendar app
(`/home/xrim/wink-calendar/`, deployed at `/var/www/wink`, served via Caddy at
`/wink`), the owner design-reviewed it in-the-loop (three catches), and this
document records what the flow and the build actually did.

Evidence: session `20261009_073833_efcb5350` (qwen profile state.db, msgs
599–883; extracted to `…/scratch/wink-session.jsonl`), the unpacked bundle
(`…/qwen/cache/scratch/wink/`), the da_verify run
(`…/scratch/wink-verify/`), screenshots (`…/scratch/wink-shots/`; key shots
copied to `docs/experiments/assets/06-wink-calendar-app.png` and
`06-wink-reference.png`).

## 1 · What worked (receipts)

- **Bundle is genuinely self-contained** for a good build: agent-brief +
  reference build + fonts + full pack + manifests in one zip; 8/8 hashed files
  verified by the agent on unpack (the 3 "missing" are at zip root, see F-2).
- **The agent behaved**: inspected the CLI before executing it, checked the
  pack for auto-run code (`validators: []`), resolved/inspected before
  adopting, wrote a PLAN quoting recorded values, filed **4 gaps** at the
  right moments, browser-exercised every flow (found and fixed its own TDZ
  and `[hidden]` bugs), and ran a record-by-record self-audit when challenged.
- **The reference `styles.css` ("extracted verbatim") carried the build** —
  the agent quoted tokens/selectors from it directly.
- Post-fix state is measurably conformant on the core identity: probe table
  (computed styles) — `.cta` pill radius 999px / `#FFE01B` fill / 1px ink
  ring; `.brand` ink 13/500 Inter; headline Fraunces 35; today-cell brand
  yellow; chip single ring (`border:0` + 1px ring); card radius 16 + recorded
  warm shadow; both fonts loaded; zero console errors.

## 2 · Flow friction (the "clunky" part)

**F-1 — The brief's commands are stale post-refactor (blocking as written).**
`tools/bundle_authority_site.py` `AGENT_BRIEF` (L36–83) still uses
`--pack packs/{auth}` everywhere, but a fresh clone of the meta repo contains
`packs/` = **0 tracked files** and `authorities/*` is **gitignored**
(`git check-ignore authorities/wink` → ignored; only `CURRENT.json`,
`README.md`, `bootstrap.sh` are tracked there). So after the documented
`git clone`, *every* example command fails, and the pack has no path from the
repo at all. Receipt: the agent had to discover this itself ("the Wink pack
isn't in the repo") and improvise.
*Fix:* rewrite the Setup section: (a) one-liner zip route — download
`{auth}-site.zip`, use `--pack ./pack`; (b) or `git clone --depth 1
https://github.com/vjsyong/authority-wink.git` and point `--pack` at it
(pack records at the repo root). Keep both paths explicit with working paths.

**F-2 — The pack source is buried.** The zip is only mentioned under "Take it
away" (as the reference build download), never as *the* pack source. The agent
pieced it together; the archive-manifest scope note ("MISSING: 3" for
root-level files) caused a moment of doubt. *Fix:* name the zip in Setup, and
say the root-level files (`agent-brief.md`, `run-authority`, workspace gaps)
live at the zip root by design.

**F-3 — No one-shot path.** Even after the fix, the working recipe is
3 commands + a zip; add a `quickstart.sh` to the bundle that does it all
(download handled by the reader; unzip, wire `--pack`, print `overview`).

## 3 · Verification gap (the big pick)

**V-1 — The verification layer exists and the brief never routes to it.**
The wink pack ships `verification.json` — **32 checks**, including
`wink/action-pill-radius` ("Buttons are pills", severity error, selector
`.cta`), and `tools/da_verify.py` sits in the very repo the brief tells
agents to clone (shipped 2026-10-08, `daae5b1`; hardened `89b2590`). The
brief's loop has *orient → resolve → inspect → adopt → file gaps* and **no
verification step at all**; the agent even reasoned "pack ships no validators
(`validators: []`), so verification is manual" — it never saw the contract.

**The owner's first catch was literally a machine check.** "Sharp corners
really?" → `wink/action-pill-radius`; the check engages `.cta` and passes
today at 999px — pre-fix it would have failed mechanically. Catch #2 (chip
double-ring) and #3 (purple brand link — a missing `a{color:ink}` rule) have
**no** corresponding check. *Fix:* add a "## Verify before you claim done"
section to the brief (run `da_verify`; note the browser-dep requirement), and
consider brief guidance to keep contract-covered selectors (`.cta`, `.card`,
`.dlg`, `.ledger`, `.badge`) so the contract can engage.

**V-2 — The contract assumes the reference build's own structure (adaptation
layer needed).** Running `da_verify` over the current (fixed) app today:
**9 PASS · 13 VIOLATION · 6 UNVERIFIABLE · 4 REVIEW**. Adjudicated: the
violations are overwhelmingly *input adaptation*, not app defects —
`.cta.dark`/`.cta.outline` not found (app: `.btn-ink`/`.btn-outline`);
`.card` not found (app vessels are `.month`/`.daypanel`); `.dlg` not found
(app: `.dialog`); `.badge`/`#emptyState`/`.status` render only in states the
default capture doesn't reach; `.ledger th` (app renders div-rows);
`no-floating-surfaces` + `destructive-not-focused` failed because the
interaction script drives *reference* controls (`.log-tick`) and can't open a
foreign app's dialogs — the app's actual behaviour was verified correct in
isolation (scrims `display:none` at rest; confirm opens alone; focus lands on
`conf-cancel`). The 6 UNVERIFIABLEs are STATIC checks hard-coding the
reference filename (`app.css`; consumer app = `styles.css`). Passes include
the identity checks that matter (pill trio, body ink, focus-visible, censuses).
*Fix directions (owner decision):* a consumer-side mapping file (selector +
filename hints, e.g. `wink-verify.map.json`), or mandate recorded selectors,
plus seed/open-dialog fixture hooks the verifier can call. Until then,
consumer builds get ~28% signal from a check-mapped verifier.

**V-3 — Value-level miss already visible once mapping is fixed:** `.dialog`
padding is 32 in the app vs the record's 48 (the side-panel scale-down is
documented as a construction; the dialog's is not) — an example of what the
contract will start catching and what "construction, marked" should cover.

**V-4 — The REVIEW tier has no consumer path.** Four checks
(tone/harmony/typography registers/hover) plus `status-words`,
`tick-marked` need a human; the consumer flow has no reviewer step.

## 4 · Build residuals worth a look (owner's "looks a bit off")

Post-fix, the measured values conform; these are composition/polish
observations for the owner:
- Nav: brand far left, all controls knotted far right with the 35px
  "October 2026" title *sandwiched between* buttons — unusual composition.
- Right column: day panel doesn't stretch; large whitespace under it beside
  the tall grid.
- Chips truncate at cell width ("2pm Design r…"); the today-cell background
  is full brand-yellow (deliberate construction, brand-field reading — taste
  call).
- Improvisation marks are incomplete in the DOM: month grid carries
  `data-improv`; nav arrows, chips, drag do not (their notes live in
  styles.css comments only) — partial compliance with the brief's marking
  rule.

## 5 · Proposed changes (for owner sign-off)

1. **Brief template** (`tools/bundle_authority_site.py` L36–83; regenerate
   all eight bundles via `refresh_authority_sites.py`): fix Setup paths (F-1),
   name the pack source (F-2), add the Verify section (V-1).
2. **Wink contract additions** (authority-wink `verification.json`): link-ink
   check (nav links render ink, not UA default) covering catch #3;
   ring/border double-stroke check covering catch #2; glob filenames for the
   static scans (V-2).
3. **Adaptation decision** (V-2/V-3): consumer mapping file vs
   recorded-selector mandate — this is the same open question as the
   verification-levels/provenance-contract proposals already queued.
4. **Bundle quickstart** (F-3) + manifest scope note (F-2).

## 6 - Fixes landed (same day)

All four items were implemented and gated the same day (`./tools/check.sh`
green):

1. **Brief v2** (`tools/bundle_authority_site.py`): working Setup routes (bundle
   zip / authority-repo git), `$PACK` throughout, the recorded-selector
   mandate, and a "Verify before you claim done" section; a `quickstart.sh`
   now ships in every bundle; all six authority briefs + zips regenerated via
   the refresh tool (commits land per authority repo).
2. **Verifier v2** (`tools/da_verify.py`): Playwright is optional (browser
   checks degrade to UNVERIFIABLE, STATIC still runs); static scans resolve
   file names (map, else glob); consumer `verify.map.json` (files / selectors
   / ignore) maps a foreign app onto the contract; INTERACTION params resolve
   through the map; new `border-ring-scan` scenario; summary reports N/A.
3. **Wink contract 0.2**: `wink/brand-link-ink` + `wink/no-double-stroke`
   added; `dialog-scrim` / `error-colour` patterns made spelling-tolerant
   (claims, not one build's spellings).
4. **Option (a)**: mandate + escape hatch. wink-calendar now carries
   `verify.map.json`; its re-run: 34 checks -> PASS 23 / VIOLATION 0 / N/A 7 /
   REVIEW 4 (was 9 / 13 / 6 / 4 over 32). Dialog padding corrected to the
   recorded 48 (the one genuine value miss the mapping surfaced).

Also fixed: the last `packs/` stragglers (`compile_pack.py` output dir; the
`synthesize-authority` skill's commands).

**Follow-ups (open):** mutation runs for the two new checks (pending an
approval-blocked command); deploy the dialog-padding fix to the live
`/var/www/wink` copy (needs sudo); reconcile the wink contract with the
current reference docs site (~13 checks target the fuller build: `.dlg`,
`#ringFill`, `.log-tick`, `app.css`-era layout) - its own pass, owner decides
scope.
