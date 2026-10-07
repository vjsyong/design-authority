# SPIKE · 00 · Candidate research — public brand kits for the portability spike

**Purpose:** select an external, non-Triage source for the second Design
Authority. Criteria per the spike brief: publicly accessible; reasonable
experimental/research use; enough visual guidance to infer an interface
language; meaningfully different from Triage; not itself a complete
component-heavy web design system; requires real design-system formalization.

**Method:** web research (multi-engine search) + primary-source verification
by fetching the actual manuals/guidelines. All URLs below verified live on
2026-10-07 unless noted.

## Comparison

| candidate | year | rights posture | material quality | distance from Triage | formalization work | verdict |
|---|---|---|---|---|---|---|
| **NASA Graphics Standards Manual** | 1976 | **Public domain (US Gov work) + official PDF** | ★★★★☆ (60pp official scan; color standards, type program, grid chapters) | High (red/black/white; Helvetica/Futura; aero-precision) | High (print identity → interface) | **RECOMMENDED** |
| EPA Graphic Standards System | 1977 | Public domain (US Gov) + NEPIS text | ★★★☆☆ | High (environmental/inst. palette) | High | Runner-up |
| NYCTA Graphics Standards Manual | 1970 | Grey (original unclear; reprint commercial) | ★★★★☆ (scans, reprint) | High (transit signage) | High | Good, rights caveat |
| British Rail Corporate Identity Manual | 1965 | Grey (legacy entities; reprint) | ★★☆☆☆ (reprint book; fansite) | High (Rail Blue/Aphabet) | High | Good, materials caveat |
| Ubuntu Brand Guidelines | current | Community/trademark terms | ★★★☆☆ (web-first) | Med-High (aubergine/orange humanist) | **Low-Med** (already web-oriented) | Good, weakest formalization test |

## 1 · NASA Graphics Standards Manual (NHB 1430.2, January 1976) — **RECOMMENDED**

- **Source:** designed by Danne & Blackburn for NASA. Official PDF hosted by
  NASA (publicly released 2015): `nasa.gov/.../nasa_graphics_manual_nhb_1430-2_jan_1976.pdf` —
  verified live, 60 pages, high-quality scan (text extraction quality 0.996).
- **Licensing/usage:** US Government work → public domain (17 U.S.C. §105);
  NASA itself released the original PDF for free. Carve-out to respect: NASA
  name, logotype ("worm"), and insignia are protected identifiers (14 CFR
  1221) — the spike **derives a new interface language and does not reproduce
  NASA marks**; attribution is nominative (provenance records the source).
- **Available materials (from the verified TOC):** §1.3–1.5 *The NASA Color*,
  *Color Standards*, logotype color use; §2.14 NASA Red color swatches; §5.3–5.6
  typography specifications for **Helvetica, Futura, Garamond, Times Roman**;
  §5.14–5.20 the **Grid** (cover and interior grid formats, format relations);
  §4 Forms; §6 Signage; plus stationery, vehicles, publications.
- **Visual characteristics:** black/white with a single disciplined red accent;
  geometric sans (Helvetica/Futura) display program with serif companions;
  strict grid discipline; tone of "unity, precision, thrust" — 1970s aerospace
  futurism.
- **Distance from Triage:** high on every axis that matters — accent colour
  (red vs. Triage's blue), type program (specified geometric faces vs. system
  stack), tonal register (aero-precision vs. utilitarian-everyday). Both are
  light/minimal at base, which keeps the comparison honest rather than
  caricatured.
- **Likely difficulty:** medium. Source material is excellent; the work is
  genuine formalization (a print identity has no buttons — the derivations to
  controls, surfaces, status, and empty states are real design decisions).
- **Portability-test fit:** ★★★★★ — exercises the kernel on a system whose
  vocabulary shares nothing with Triage except the pack schema.

## 2 · EPA Graphic Standards System (1977)

- **Source:** US EPA; manual designed under Bruce Blackburn's firm following
  the Federal Design Improvement Program; reprint published 2017.
- **Licensing:** US Government work → public domain; a text rendition is
  available officially via EPA's NEPIS archive (`nepis.epa.gov`, DocKey
  P101HJQ2: "This manual establishes and delineates the graphic standards…").
- **Materials:** NEPIS text; reprint scans (commercial) + secondary sources;
  photographic program (Documerica) documented.
- **Visual:** modular, flexible system; environmental/institutional register;
  strong imagery rules; distinctive from both Triage and NASA.
- **Difficulty:** medium-plus — official material is thinner in clean form
  than NASA's, though entirely sufficient.
- **Verdict:** the ready runner-up; same rights posture as NASA, less famous,
  slightly harder sourcing.

## 3 · NYCTA Graphics Standards Manual (1970)

- **Source:** Unimark International (Massimo Vignelli, Bob Noorda); authorized
  reprint (Standards Manual, 2014; scans from Vignelli's personal library).
- **Licensing:** grey — original rights historically unclear (successor
  entities/estate); reprint is commercial. Circulation of scans is abundant
  but usage for a derived-system spike should be reviewed before use.
- **Visual:** Helvetica + high-contrast black/white + a vivid line-colour
  coding system; signage/wayfinding architecture (insert cards, directional
  logic) that translates unusually well to navigation and list artifacts.
- **Difficulty:** medium; rights caution is the main tax.

## 4 · British Rail Corporate Identity Manual (1965)

- **Source:** Design Research Unit; double-arrow symbol (Gerald Barney); Rail
  Alphabet (Jock Kinneir & Margaret Calvert); four volumes, 1965–1970.
- **Licensing:** grey (legacy corporate entities; 2016 reprint via
  crowdfunding). Fine for study; derivation use needs care.
- **Materials:** reprint (book), fan archives (`doublearrow.co.uk`), partial
  scans — the most fragmented of the set.
- **Visual:** Rail Blue, pearl grey, signal red; Rail Alphabet; a signage-first
  system with strong livery logic.
- **Difficulty:** medium-hard (sourcing) — appealing but least convenient.

## 5 · Ubuntu Brand Guidelines (Canonical, current)

- **Source:** official, live: `design.ubuntu.com/brand` (colour palette,
  typography, pictograms, usage guidance).
- **Licensing:** community-friendly trademark/usage terms; Ubuntu font freely
  licensed — but brand assets remain under Canonical policy.
- **Visual:** aubergine + orange, humanist sans (Ubuntu), pictogram system —
  warm and humanist against Triage's cool utilitarianism.
- **Formalization fit:** **weakest of the set** — it is contemporary and
  web-ready, and its component-system cousin (Vanilla) exists, so the spike
  risks translating an existing API instead of performing real derivation.
- **Verdict:** a legitimate diversity option (non-government, open-source),
  but it dilutes the experiment's core question.

## Recommendation

**Build the spike on the NASA Graphics Standards Manual (1976).**

1. **Cleanest rights posture** of the set — public domain, officially hosted,
   with a clearly delimited trademark carve-out that the spike respects by
   deriving a new (unbranded-nominatively) interface language.
2. **Richest single-document source** — colour standards, a typed program
   (four faces with roles), and explicit grid chapters: enough surface for
   ~10 core artifacts plus compositions, while leaving real INFERRED and
   AUTHORED decisions (and likely a genuine UNDEFINED class, e.g. motion).
3. **Maximal productive distance from Triage** — red accent, geometric
   display type, aerospace register — so a kernel that carries both systems
   is credibly kit-agnostic, not just flexible within one taste.
4. **Source-rich and famous** — later review/verification by third parties is
   easy; the corpus is stable.
5. Good test-app theme for the eventual small application (a "mission
   console" register) without touching NASA's protected marks.

Expected epistemic spread when we build it (per the spike's ledger):

```
OBSERVED   — colour roles and values, type roles, grid/spacing logic (all explicit in the manual)
INFERRED   — control/input/surface treatments derived from the print/grid language
AUTHORED   — interaction patterns (the manual predates interfaces), status/feedback semantics
UNDEFINED  — motion; possibly iconography beyond reproduction art
```

**No implementation has begun** (per the spike brief: candidate choice is
justified here, implementation waits on approval). If NASA is accepted, the
next step is Phase 1: derive the minimal system (foundations + 8–12 artifacts
+ 2–4 compositions) with the OBSERVED/INFERRED/AUTHORED/UNDEFINED ledger
attached to every decision.
