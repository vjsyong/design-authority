# 06 · Coverage — semantic vs verification, measured

Two different questions, kept apart (per the brief):

- **Semantic authority coverage** — how much of the design problem does the
  authority define?
- **Verification coverage** — how much of that defined authority can be
  checked independently?

No single number; no optimization. This is the discovered boundary.

## Verification coverage of the audited surface

| authority | checks | mechanical | partial | review | not-currently |
|---|---|---|---|---|---|
| wink | 29 | 21 | 4 | 3 | 1 |
| leader | 23 | 16 | 3 | 3 | 1 |
| dominion | 22 | 17 | 2 | 2 | 1 |
| **total** | **74** | **54 (73%)** | **9 (12%)** | **8 (11%)** | **3 (4%)** |

Interpretation: **73% of the audited normative surface is independently
checkable today**; 12% is partially checkable with declared judgement edges;
15% is honestly not machine-checkable (humans or nothing). Mutation recall on
the mechanical/partial surface: 19/19.

## Entry-level coverage (named items in each pack)

Approximate direct mapping (some entries are covered through their governing
rules rather than by an entry-named check):

| authority | named entries | entries directly referenced by checks | notes |
|---|---|---|---|
| wink | 26 | 18 (69%) | uncovered incl. navbar, field-select, type-scale; fallbacks/precedent/candidate are resolver-level (covered by the golden + battery, not the DOM contracts) |
| leader | 29 | 14 (48%) | uncovered incl. meter, navbar, data-readouts, type/colour token-sets, shape-language (partial via checks), 3 rejected-proposal precedents (resolver-level) |
| dominion | 32 | 14 (44%) | uncovered incl. select, masthead (covered via rule/D-R2 check), plain-chart, interaction-states, 6 precedents + 3 candidates (resolver-level) |

Resolver-level entries (precedents, candidates, fallbacks, recipes) are
verified where they act — through the resolution batteries (goldens 19/23/
18·14·17, convergence 34/34, precedent probe 31/31) — not through
implementation scanning. The contracts verify the **implementation surface**,
which is what the build agents actually produce.

## Semantic coverage (carried from stress v3, for the pairing)

42 asks per authority, build v3 on the codified packs — defined answers
(RESOLVED + COMPOSE + FALLBACK) vs UNDEFINED:

| authority | defined | undefined | defined share |
|---|---|---|---|
| wink | 20 | 22 | 48% |
| leader | 24 | 18 | 57% |
| dominion | 20 (+3 conflict) | 19 | 48% |

So the pairing for wink looks like: **~48% of the problem space defined;
~73% of the audited definition independently checkable; ~100% of detectable
seeded drift caught.** Different denominators, deliberately separate.

## What remains outside machine verification (the honest residue)

1. **Character and register** — tone, harmony, editorial restraint, ceremony
   character, chart character: emitted as `REVIEW_REQUIRED` (8 items) and
   routed to humans. Mutation L-V5 (hierarchy de-serif) is the live proof of
   this blind spot.
2. **Felt motion** — hover spring character; the transform value is
   checkable in principle (not yet contracted), the feel is not.
3. **Language quality** — bilingual tone parity (pairing presence IS
   checked; quality is not); hierarchy calibration across views.
4. **Resolution judgment** — whether UNDEFINED should have been RESOLVED, or
   a candidate adopted: resolver batteries bound this, but "right answer for
   a novel ask" stays human adjudication (the review window exists for it).
5. **Evasion classes found during design (recorded as boundaries):**
   pictorial svg behind the sanctioned `.spark` class; a new shade between
   allowlisted hues; a floating surface rendered non-`fixed` (e.g. absolute)
   would elude the current scan.

## Coverage additions made during the experiment

- `no-floating-surfaces` (all three) — closes an unstated gap; validated by
  catching W-V4.
- Instrument scoping rules — otherwise every marks-layer colour would
  false-positive; tooling vs app UI is now explicit in every contract.
- `declarations` and `color_literals` static primitives — they carried the
  palette/shadow/motion classes of rules.

Do not read these as targets to maximize: they are what the current
authorities and the current three builds made measurable.
