# 02 · Candidate authority changes

**Phase 3 output.** Five candidates, stored separately from the published
authority under `proposals/evolution/`. None of them touches the pinned 0.12.1
pack; implementation happens on a candidate branch/version (Phase 5) and only
what survives review (Phase 4) gets built. **Update: all five candidates were
independently reviewed (`docs/evolution/03-review.md`; verdict REVISE ×5) and
every required action was applied — see each candidate's `review` block.**

| # | candidate | gap | classification | layer |
|---|---|---|---|---|
| 01 | `cand/01-select-catalogue` | G-01 | DOCUMENTATION-FIX | triage snapshot + curation |
| 02 | `cand/02-progress-catalogue` | G-02 | DOCUMENTATION-FIX | triage snapshot + curation |
| 03 | `cand/03-recipe-assign-picker` | G-01 | RECIPE | curation |
| 04 | `cand/04-recipe-job-progress` | G-02 | RECIPE | curation |
| 05 | `cand/05-confirm-reason-extension` | G-03 | DOCUMENTATION-FIX (recipe alt. held) | curation |

Machine-readable files (full template: problem · evidence · existing
authority considered · why insufficient · proposed change · dependencies ·
scope · compatibility · validation · migration):
`proposals/evolution/cand-01…05-*.json`.

## What the candidate package does, in plain terms

1. **Makes two already-shipped primitives citable** — the styled native
   `<select>` (new explicit `.select` class alias, additive selectors only)
   and the existing `.progress` bar (spec entry + a11y contract, zero CSS
   changes). Both enter the spec/states.json matrix at status **beta** (their
   honest level: shipped + dogfooded + example usage, no dedicated behavioural
   regression yet — upgrading to stable with browser coverage is a follow-up,
   deliberately out of scope here).
2. **Adds two sanctioned recipes** — `recipe/assign-picker` and
   `recipe/job-progress` — each composed strictly of existing artifacts, each
   carrying `needs` vocabulary taken from the actual downstream phrasings and
   evidence pointing back at the gap records.
3. **Extends one existing recipe** (`high-stakes-confirm`) with
   reason-bearing coverage (Option A), with a small dedicated recipe held as
   the reviewed alternative (Option B).

Net new *visual language*: **zero**. Net new CSS declarations: **zero** (only
selector aliases on five existing rules). The hierarchy of changes:

```
documentation fixes   2   (select, progress catalogued)
recipes               2   (+1 documented extension)
patterns              0
primitives            0
new tokens/rules      0
```

## Compatibility & migration notes

- All changes additive; bare `<select>` and existing `.progress` markup keep
  working identically; c1–c4 fallback implementations remain valid markup that
  upgrades to a citation on next touch.
- `component/cb` remains the large/filtered-set option; nothing in the
  candidates changes its behaviour (non-regression checks cover it).
- The resolver mis-route defect (pattern/detail on assignment phrasings) is
  addressed through vocabulary only — scoring/kernel stay untouched; if the
  mis-route survives the rebuild, the failsafe is (a) tune needs phrasing
  coverage, and only if that fails would a scoring change be proposed as a
  separate decision.

## Validation plan (executed in Phase 5)

Per candidate, as recorded in the JSON files:

1. Triage gates on the candidate branch: `build.py check` (incl. verify.py
   states matrix at 37 components), strict lint 100/100, unit tests, browser
   suite where available.
2. Pack rebuild parity + drift gate for the evolution pack; 0.12.1 pack must
   stay byte-identical.
3. **Convergence tests** — every baseline phrasing from
   `docs/evolution/data/baseline-resolves-0.12.1.json` for the three gaps must
   land on one sanctioned answer per the **verified contracts** in the
   candidate files (G-01: 7 → component/select + 1 → recipe/assign-picker;
   G-02: 5 → recipe/job-progress + 2 → component/progress; G-03: 4 →
   recipe/high-stakes-confirm), with the exact old failures re-tested
   (pattern/detail mis-routes, stray COMPOSEs, UNDEFINEDs) plus the
   delete-probe battery (all → entity-delete-armed).
4. **Non-regression battery** — the baseline regression set (combobox, date
   picker, loading spinner, toast, banner, delete, empty, pagination) must
   keep its 0.12.1 answers.
