# Standalone review: catalog the project's established conventions

You are given a frozen copy of a small application (a bookmarks manager),
its workspace records (`.design-authority/`), screenshot captures of its
current states (`reference/screens/`), and a deterministic element inventory
(`reference/extraction/`). Act as an independent cataloguer. **Do not
modify the application** or any file other than your outputs.

Task: apply the census rubric (`reference/census-rubric.md`) to the six
roles it lists. For each role:

1. Classify it — **Established / Observed once / Inconsistent / Absent** —
   strictly per the rubric's definitions, using only the frozen evidence in
   this workspace.
2. For every role classified **Established**, freeze one reference exemplar
   (the latest instance) with its measured values and behavioral categories,
   exactly as the rubric's schema specifies.

Outputs, written at the workspace root:

- `census.json` — the exact schema in the rubric.
- `exemplars.json` — the exact schema in the rubric.

Rules: evidence only — cite where each classification's evidence lives
(which screenshot, which file, which record). Do not consult anything
outside this workspace (no network). When the rubric asks for a judgment
you cannot support from the evidence, record it as observed-once or absent
rather than inflating it. Finish by updating `HANDOFF.md` with a one-line
summary.
