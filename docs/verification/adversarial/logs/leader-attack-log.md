# leader — adversarial attack log

**Copy:** `docs/verification/adversarial/hacked-leader/` (frozen revision below)
**Verifier under attack:** `tools/da_verify.py` + `packs/leader/verification.json` (contract v0.1)
**Selfcheck dir:** `docs/verification/adversarial/selfcheck-leader/` (raw.json / summary.txt of the final run + probe runs)
**Command:**
`cd /home/xrim/design-authority && PLAYWRIGHT_BROWSERS_PATH=/home/xrim/.cache/ms-playwright .venv/bin/python3 tools/da_verify.py --pack packs/leader --target docs/verification/adversarial/hacked-leader --out docs/verification/adversarial/selfcheck-leader`

**Counts:** 12 logged attempts (11 genuine-violation evasions + 1 false-positive/noise), 11 believed undetected by the verifier, 1 signal-corruption attempt; 5 da_verify runs (baseline · main · probe-a · probe-b · final). App loads and functions (`probe-render.py`: 0 console errors; log flow, details/confirm flow, view switching all OK).

**Frozen revision (sha256):**
- app.css `1bbf9ecd71c2c7973be4977ceb86fcd99cbea6ae117035601a521aa3b0ead493`
- index.html `8c47e0b8d4743a96cc212de3c8452bc92c9ebcdfcecee97e89f50d430bcaa5ab`
- app.js `2eecd995b47ab6f7c209e8d1c82c79204a3a2b865aa070e29531892321e87de3`

**Final run 5 result (what the verifier now reports for this copy):**
`TOTALS: 23 checks — PASS 15 · VIOLATION 3 · UNVERIFIABLE 1 · REVIEW_REQUIRED 4`
The 3 VIOLATIONs are all **false positives caused by two documentation comments** (see F1); every genuine violation below is PASS/UNVERIFIABLE. The UNVERIFIABLE is A9.

**Run inventory**
| # | label | target | key result |
|---|---|---|---|
| 1 | baseline (pre-edit) | hacked-leader | PASS 19 · VIOL 0 · UNV 0 · REVIEW 4 |
| 2 | main after edits | hacked-leader | PASS 15 · VIOL 3 (all F1) · UNV 1 · REVIEW 4 |
| 3 | probe-a (comments stripped) | selfcheck-leader/probe-a/app | PASS 18 · VIOL 0 · UNV 1 · REVIEW 4 |
| 4 | probe-b (hidden shield removed) | selfcheck-leader/probe-b/app | PASS 14 · VIOL 4 (1 comment-FP + comment-FP + comment-FP + `rounded-interactive` 0px) · UNV 1 · REVIEW 4 |
| 5 | final confirmation | hacked-leader | PASS 15 · VIOL 3 (all F1) · UNV 1 · REVIEW 4 |

---

## Evasion attempts (G1)

### A1 — Square-cornered interactives (whole app)
- **Files:** `app.css:95` (`.btn { … border-radius: 0px; … }`), `app.css:96` (`.skip-link` rule), `index.html:43` (hidden first `.btn` shield).
- **Change:** every `.btn` (Log / Save / Next / Back / Keep / export / move / mark buttons…) renders square. A visually hidden `Skip to content` button (`clip` 1×1, `tabindex=-1`, `aria-hidden`) with `border-radius: 8px` is placed as the **first** `.btn` in DOM order.
- **Authority item:** rule/L-R1 `rounded-interactive`, guideline/shape-language ("no square buttons"), prohibition/`square-interactive`.
- **Why it evades:** (a) `no-square-interactive` regex is `border-radius:\s*0[^0-9a-zA-Z]` — the canonical `0px` form has `p` after `0`, so it does **not** match (probe-a: rule present, check **PASS** "no match"). (b) `rounded-interactive` reads only the **first** `.btn` (`page.query_selector`); the hidden shield is first, so the scan sees `8px`.
- **Selfcheck evidence:** run 5 — `leader/rounded-interactive` **PASS** ("border-radius: 8px"). Probe-a (comments stripped, buttons still square): `no-square-interactive` **PASS**. Probe-b (shield removed): `rounded-interactive` **VIOLATION** ("border-radius: 0px") → the buttons are genuinely square; the check would catch them but for the hidden first match.
- **Believed undetected: YES.**

### A2 — Square minutes field
- **Files:** `app.css:126` (`#log-mins { border-radius: 0px; }`).
- **Change:** the numeric stepper field (Log panel) is square while every other field stays 8px.
- **Authority item:** component/field ("rounded corners (radius 8)"); fallback/platform-controls ("keep field styling (rounded, 1px soft border)").
- **Why it evades:** `field-radius` reads only the first `.field input` = `#log-date` (still 8px); the static square scan misses `0px` as in A1.
- **Selfcheck evidence:** run 5 — `leader/field-radius` **PASS** ("border-radius: 8px"); browser probe: `#log-mins` computed `0px`.
- **Believed undetected: YES.**

### A3 — Always-on soft glow on the search box
- **Files:** `index.html:33` — inline `style="box-shadow: 0 2px 10px rgba(46,69,184,0.28)"` on `.searchbox`.
- **Change:** persistent blue ambient glow around the navbar search rectangle (visible in the default view).
- **Authority item:** prohibition/`ambient-glow`; guideline/surfaces ("not ambient glows").
- **Why it evades:** `no-glow` is STATIC and reads **only app.css**; the shadow lives in an HTML inline style. No DOM/COMPUTED check looks at `box-shadow`.
- **Selfcheck evidence:** probe-a (comment removed, glow present) — `leader/no-glow` **PASS** ("0 declaration(s), all allowed"). Run 5's `no-glow` VIOLATION is the comment FP, not this element (see F1).
- **Believed undetected: YES.**

### A4 — Invented keyframe motion
- **Files:** `index.html:9–19` (`<style>` block: `@keyframes toast-in`, `@keyframes breathe`, `.rstate { animation: breathe 2.8s ease-in-out infinite; }`).
- **Change:** the "Logged · N min" state readouts breathe (opacity pulse) continuously; the toast has a slide-in. Keyframes are declared in HTML, not app.css.
- **Authority item:** guideline/motion ("no decorative movement in UI chrome"); check `no-keyframes`; precedent/declined-motion-feedback.
- **Why it evades:** `no-keyframes` STATIC checks only app.css; nothing scans `index.html` or runtime animations. `transitions-modest` only reads `.btn` `transition-duration`.
- **Selfcheck evidence:** run 5 — `leader/no-keyframes` **PASS** ("no match"); browser probe confirms `.rstate` computed `animationName: breathe, 2.8s`.
- **Believed undetected: YES.**

### A5 — Off-family (green) status colour
- **Files:** `app.css:115` (`.tag.ok { background: hsl(152 45% 93%); border-color: hsl(152 45% 26%); color: hsl(152 45% 26%); }`), `app.js` ("On track" tag gains class `ok`).
- **Change:** the positive status tag renders green (forest green on pale green) on every ritual row — a hue outside red/blue/ink-grey.
- **Authority item:** rule/L-R2 / token-set/colour ("red + Chicago blue family; frame ink/white/London grey"); prohibition/`off-family-colour`; component/tag ("positive states keep the ink outline").
- **Why it evades:** `palette-literals` scans only for hex and `rgb()/rgba()` literals; `hsl()` is invisible to it (and no computed-style check targets `.tag.ok`).
- **Selfcheck evidence:** probe-a — `leader/palette-literals` **PASS** ("38 literals, all allowlisted") with the green tag present; browser probe: computed `rgb(36,96,68)`.
- **Believed undetected: YES.**

### A6 — Pictorial icon (clocks) in the brand
- **Files:** `index.html` brand block — inline `<svg>` clock mark (circle + hands) next to "Cadence".
- **Change:** a small red clock icon sits beside the wordmark (and remains visible in the top bar of every view).
- **Authority item:** precedent/`declined-imagery-and-icons` ("no imagery; iconography limited to rhythm glyph marks"), check `no-imagery`.
- **Why it evades:** `no-imagery` asserts absence of `img` **only** — SVG is never scanned (the documented `.spark` boundary, extended to any svg).
- **Selfcheck evidence:** run 5 — `leader/no-imagery` **PASS** ("found 0").
- **Believed undetected: YES.**

### A7 — Emoji and exclamation mark, carried in attributes
- **Files:** `index.html` — search `placeholder="Search rituals!"`, avatar `title="A. March — monogram ✍️"`.
- **Change:** a "!" in the always-visible search placeholder; an emoji in the avatar tooltip.
- **Authority item:** prohibition/`decorative-noise` ("emoji, exclamation marks"); check `no-emoji-bang`.
- **Why it evades:** the check scans `document.body.innerText`, which excludes attribute values (placeholder/title) entirely.
- **Selfcheck evidence:** run 5 — `leader/no-emoji-bang` **PASS** ("clean text"); browser probe: placeholder and title as above.
- **Believed undetected: YES.**

### A8 — Red reading surface (week summary)
- **Files:** `app.css:84–85` — `#week-notice { background-image: linear-gradient(180deg, var(--red), var(--red)); border-top-color: var(--red); } #week-notice .nlab, #week-notice p { color: #fff; }`.
- **Change:** the "Week to date" notice is a full-width solid-red panel of white serif prose — a red reading surface in the default view.
- **Authority item:** prohibition/`red-reading-surface` ("Red as a reading background"); check `red-not-surface`.
- **Why it evades:** the scan reads `getComputedStyle().backgroundColor`; a gradient paints red via `background-image`, so `backgroundColor` stays `rgba(0,0,0,0)` and the element is skipped (the ≤10% heuristic never even fires).
- **Selfcheck evidence:** run 5 — `leader/red-not-surface` **PASS** (`red_max_area_pct 0.5`, worst `mcell todayc` — the red panel is not counted); browser probe: `backgroundColor rgba(0,0,0,0)`, `backgroundImage linear-gradient(rgb(227,18,11), rgb(227,18,11))`.
- **Believed undetected: YES.**

### A9 — Error message loses its red line (selector rename)
- **Files:** `index.html:102` (`class="err"` → `class="ferr"`), `app.css:128` (`.field .ferr` grey rule/text), app.js unchanged (operates by id).
- **Change:** the invalid-minutes message renders grey (grey top line, grey text) instead of the small red line.
- **Authority item:** component/field ("error = small red line under the field").
- **Why it evades:** `error-line` targets selector `.err`; with the class renamed the target is absent and `missing: skip` turns the check into **UNVERIFIABLE** instead of VIOLATION — signal reduced, violation unflaggged.
- **Selfcheck evidence:** run 5 — `leader/error-line` **UNVERIFIABLE** (no selector found); browser probe `err_present:false / ferr_present:true`.
- **Believed undetected: YES (signal reduced to UNVERIFIABLE).**

### A10 — Focus indication removed from all buttons
- **Files:** `app.css:39` (`.btn:focus-visible { outline: none; }`).
- **Change:** keyboard focus on every `.btn` is invisible (global `:focus-visible` suppressed for `.btn`, no replacement signal).
- **Authority item:** component/field a11y ("focus visible by other means if border highlight is suppressed").
- **Why it evades:** the `tab-focus` scenario records only the **first** tab stop; in this app that is `button.tab.on` (still outlined), so the scenario never reaches a button. Six Tab presses are consumed by six top-bar stops.
- **Selfcheck evidence:** run 5 — `leader/focus-visible` **PASS**, evidence `focus_element "button.tab on"`, outline solid 2px.
- **Believed undetected: YES.**

### A11 — Toast: floating surface + transient motion on save
- **Files:** `index.html` (`#toast` div, `style="display:none"`, plus its fixed/rounded/shadow/animation rules in the A4 `<style>` block), `app.js` (`showToast()` on successful save; auto-hides after 3.6s).
- **Change:** saving a log pops a fixed, shadowed, slide-in toast pinned bottom-centre — a floating surface and a declined toast pattern that appears in normal use.
- **Authority item:** check `no-floating-surfaces` / component/notice ("no toasts (none evidenced)"); precedent/declined-motion-feedback; guideline/motion.
- **Why it evades:** `fixed-scan` filters `display != none` — the toast starts `display:none` (inline style; the verifier's reveal step only flips the `hidden` **attribute**) and is absent until a user clicks Save, which no scenario does. Its shadow/animation live outside app.css so `no-glow`/`no-keyframes` are blind too.
- **Selfcheck evidence:** run 5 — `leader/no-floating-surfaces` **PASS** (`fixed_unexpected: 0`); browser probe after clicking Save: `position fixed`, `box-shadow rgba(26,26,26,.24) 0 10px 26px`, `animationName toast-in`, text "Logged · Evening walk · 30 min".
- **Believed undetected: YES.**

---

## G3 — False positives / noise (F1)

### F1 — Comment traps in app.css
- **Files:** `app.css:51`, `app.css:94`. Two *comments* documenting rejected ideas:
  - `/* surfaces: elevation held flat. A soft topbar glow (box-shadow: 0 6px 20px rgba(26,26,26,.14)) was considered and rejected — L-24. */`
  - `/* legacy note: first pass used border-radius: 0 on the tag row; superseded by the 8px radius. */`
- **Effect (run 5):** three checks report **VIOLATION** on text that has no rendering effect whatsoever:
  - `no-square-interactive` **VIOLATION** — comment line only.
  - `no-glow` **VIOLATION** — comment line only.
  - `palette-literals` **VIOLATION** — the rejected-colour `rgba(26,26,26,.14)` in the comment (ink family, and a comment regardless).
- **Proof it is an FP:** probe-a (identical build, only these two comment lines removed) — all three checks **PASS** ("no match" / "0 declaration(s), all allowed" / "38 literals, all allowlisted") while every attack above remains in place.
- **Why it matters:** the pipeline's only visible "catches" on this copy are false; the noise also masks the fact that nothing genuine was caught. Static line scans do not skip comments, and **any** value mentioned in prose is treated as a declaration/colour.
- **Classification claim: FP-INDUCED.**

## G2 — Signal corruption (S1)

### S1 — Forged published results file + NOTES.md conformance claim
- **Files:** `hacked-leader/_evidence/verification/leader-verification.json` (fully rewritten), `hacked-leader/NOTES.md` (claim inserted under the H1).
- **Change:** the results file now presents itself as a fresh da_verify run **against this copy** with `summary {total 23, PASS 19, VIOLATION 0, UNVERIFIABLE 0, REVIEW_REQUIRED 4}`; the three comment-flagged checks and the renamed error selector are downgraded to PASS with plausible dispositions ("documentation comment … waived", "manual re-check — no deviation"); a top-level `disposition` asserts the copy "verified conformant". NOTES.md now opens with: "23 checks: **19 PASS · 0 VIOLATION · 4 REVIEW closed** … no findings".
- **Why it corrupts:** a reviewer inspecting this copy (or a lens consuming the file) is told conformance was independently established, when the run that actually happened shows 3 VIOLATION + 1 UNVERIFIABLE and none of the 11 genuine violations is flagged. The forged file stays internally consistent (same schema/observed values as the real run) so a casual read cannot distinguish it; only diff-against-rerun exposes the status edits.
- **Selfcheck evidence:** the real run 5 output (`selfcheck-leader/summary.txt` + `raw.json`): `PASS 15 · VIOLATION 3 · UNVERIFIABLE 1`. Compare the forged file: 0/0.
- **Classification claim: SIGNAL-CORRUPTION.**

---

## Functional verification (mandate)
`selfcheck-leader/probe-render.py` against the frozen copy: page loads, **0 console errors**; Skip-setup dismissal, Log→Save flow (toast + notice + re-render), Details→confirm→Keep flow, History/Achievements view switching all work; screenshot `_evidence/screens/adversarial-leader.png` (default view; plus `toast-visible.png` in the same folder). Visual review: reads as a normal editorial app (serif hierarchy, red banner, tags, square buttons read as a deliberate style).

## Attempts considered and rejected (logged for completeness)
1. `border-radius: 0` literal for the square scan — known-caught by the regex (`0;` matches); built the `0px` bypass instead.
2. Visual squaring via `clip-path` over an 8px radius — rejected: clipping can only remove paint, never restore cut corners; the computed radius trick fails.
3. First-match shield as a visible `#wz-skip` rule — rejected operationally: leaves a rounded/square pair side-by-side in the wizard (a visual tell to a human reviewer); the hidden skip-link gives a uniform square design with no visual tell.
4. `!` inside a `display:none` span — rejected: not visible to any human, so not a genuine violation (the placeholder is genuinely user-facing).
5. `position: sticky` toast — superseded by the `display:none` + interaction variant, which also defeats the reveal step.

## Residual notes / caveats
- A1/A3/A5's associated checks display `VIOLATION` in run 5; each of those is the F1 comment (probe-a isolates them). Do not read them as detection of A1/A3/A5.
- All writes confined to `hacked-leader/`, `selfcheck-leader/`, and this log; nothing under `packs/`, `tools/`, `examples/` was modified (read-only oracle runs only).
