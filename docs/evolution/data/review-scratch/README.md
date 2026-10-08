# Review scratch — adversary's executed evidence (round 2)

This directory holds the measurement artifacts from the independent
adversarial review of round-2 candidates (`../round2/03-review.md`). The
reviewer re-created packs from the real builder and ran 112 probes,
the round-1 convergence battery (34 assertions) and the golden sets against
10 pack variants.

Kept here (small, evidence-grade):

- `results/probes-*.json` — the reviewer's full probe batteries per variant
  (`base`, `v06`…`v09alias`, `vall`, `vall_alias`, `ALL`, plus focused
  `orig`/`extra` sets).
- `hashes-evo-start.txt`, `hashes-pinned-start.txt` — sha256 manifests
  proving both packs were byte-identical before the review.

Pruned (reconstructible, kept the repo light): the reviewer's snapshot and
pack copies (`evo-snap*`, `packs`, `base`, `scratch-build`) — rebuild them
with `tools/build_pack_triage.py --snapshot ~/triage-design-system-evo` and
the committed curation; the triage snapshot copies come from
`~/triage-design-system-evo` at `2c701d2`.
