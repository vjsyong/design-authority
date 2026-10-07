# Portability Spike · 01 · Source audit — NASA Graphics Standards Manual

What the source actually contains, how it was verified, and what it can and
cannot support — in the framing of the original Triage audit (explicit
authority / inferable / undefined).

## 1 · Source and rights

- **Document:** *NASA Graphics Standards Manual*, NHB 1430.2, January 1976.
  Designed by **Danne & Blackburn** for the National Aeronautics and Space
  Administration; rescinded by NASA in 1992; the original PDF was released
  publicly by NASA in 2015.
- **Location (verified live 2026-10-07):**
  `https://www.nasa.gov/wp-content/uploads/2015/01/nasa_graphics_manual_nhb_1430-2_jan_1976.pdf`
  — 60 pages, scan quality score 0.986–0.998 (text-extractable).
- **Rights posture:** US Government work → **public domain** (17 U.S.C. §105);
  NASA hosts the original for free.
- **Carve-out respected:** the NASA name, the “worm” logotype, and the seal
  are protected identifiers (14 CFR 1221). The derived system **carries no
  NASA marks**, does not reproduce the logotype, and records attribution as
  nominative provenance only. Working name “Orbit”.
- **Experimental use:** fully permissible within the carve-out; no licence
  negotiation required.

## 2 · Section inventory (what exists → what it can support)

| § | contents (verified) | interface-derivation value |
|---|---|---|
| 1 · Logotype | identity rules; **color-use rules** (white/light/dark/medium backgrounds; red restrictions); grid drawing for large applications | accent logic + the value-based contrast policy (foundations C1–C8) |
| 2 · Reproduction art | camera-ready marks; **NASA Red color swatches** | source color references (C2/C5 anchors) |
| 3 · Stationery | letterheads; **typing style**; margins establish the typing margin; warm-gray ink schemes | typographic base settings (T3/T4); margin logic |
| 4 · Forms | the agency's own form standards (partially extracted) | form structure cues (field grouping → `section`) |
| 5 · Publications | **typography program** (Helvetica/Futura/Garamond/Times, roles + settings); cover design; **the grid** (6-rectangle modular page; 2–3 column format families; white band for folios/headlines; rules; outline boxes for diagrams; caption practice) | the typographic program + spacing/layout approach (foundations T1–T7, S1–S7) |
| 6 · Signage | general principles (“simple, functional, contemporary”; message clarity; flush-left/ragged-right; no decoration); exterior/interior models; modular sign systems | feedback/status semantics; tone rules; brevity |
| 7 · Vehicles | identification configuration; **40% gray-scale value rule** for black↔white switching; flush-left handling; white/blue special-vehicle scheme | the contrast-value policy (C8); inversion patterns (F4) |
| 8 · Certificates & awards | seal usage; traditional vs contemporary registers | formality registers (minor) |
| 9 · Supplementary guides | vinylcals, uniform patches (list only) | minor |

## 3 · Classification

**Explicit authority (directly usable, quoted):** color definitions and usage
rules; typographic program (families, weights, settings, case policy); grid
and format system; signage principles; identity scale relations; the 40%
value threshold; brevity/voice standards; the box-reserved-for-technical rule.

**Inferable (repeated evidence, needs translation):** spacing scale from the
modular grid; rectilinear/square form language (zero radius); rules-over-
decoration separation; inversion for emphasis; status-as-message patterns;
tag separation from “patches get their own visual space”.

**Undefined in the source (nothing to observe):** interface motion; responsive
behavior; interactive states (hover/focus/disabled); loading/progress;
dialogs/modals; destructive-action semantics; multi-color data coding;
iconography beyond standard symbol signs (DOT library).

## 4 · Verified quotes (page-cited; used in 02)

- p8: “Against a white background the logotype may be shown in NASA red and
  black, black, or NASA warm gray.” · “The logotype should never be shown in
  NASA red against a medium-value background.”
- p9: “The formula for NASA red is solid red plus solid yellow.” (4-color
  process)
- p27: “Helvetica is the most important family of type in the NASA Unified
  Visual Communications System.”
- p30: “flush left, ragged right column setting… minimum one-point line
  spacing in text setting.” · “The use of pale, pastel colors is discouraged
  in all NASA publications.”
- p41: “Single page has been divided into 6 equal rectangles.” · “Rules are
  employed to separate articles.” · “Outline boxes should be used around all
  technical diagrams.”
- p45: “Simple, functional, contemporary.” · p46: “‘normal’ rather than
  ‘tight’ letterspacing.” · “Keep the signs simple.”
- p47: “…darker than a 40% value on a gray scale…” (identification flips
  black↔white).

## 5 · Extraction log

- 2026-10-07 — candidate research fetch (TOC + overview).
- 2026-10-07 — focused extractions: pages 8–9 (color standards), 10–14
  (logotype rules, grid drawing, seal), 27–30 (typography 5.3–5.6), 41–49
  (grid formats, signage, vehicles), 53–58 (aircraft/spacecraft/certificates).
- Tooling: hound `smart_fetch` (PDF, focused BM25 extraction; cached).
- Not yet extracted: §4 forms pages (noted gap — relevant fields are
  INFERRED/AUTHORED anyway; can be pulled if the derivation needs grounding).

## 6 · Implication

The source supports **foundations richly** (color/type/grid are explicit) and
**elements only indirectly** — it predates interfaces, so every control,
state, and composition is a derivation. That distribution is exactly what the
ledger in `02-derived-system.md` records: most element-level decisions are
INFERRED or AUTHORED, several are deliberately UNDEFINED, and the pack will
say so.
