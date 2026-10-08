# Blind review protocol

You review 8 artifacts (review/blind/ART-01 ... ART-08), each an HTML page
built under the Triage design authority (repo /home/xrim/design-authority).
manifest.json says which of the two briefs (briefs.md) each artifact answers.
You do NOT know how any artifact was produced. Do not try to infer it and do
not read anything outside this review directory.

For each artifact, work through the brief's UI needs:

1. Enumerate the needs (brief S: the preference control; the current-state
   display; the page chrome. brief R: the release list; the stable/beta
   marker; the channel narrowing; the page chrome.)
2. For each need, determine the record that should govern it. Use the
   authority: ./run-authority resolve "canonical wording" / search / inspect.
   Where no record can govern it, note that (it is then a case for the
   fallback policy: nearest recorded pieces, marked improvisation, gap).
3. Inspect the artifact's HTML to see what it actually used (classes, gap
   comments, what it says is improvised). For each need record:
   {"need": ..., "implemented_as": short, "record_id": cited id or null,
    "record_covers": true/false, "correct": true/false,
    "notes": one line}
   correct = the right record was used, OR the need is genuinely uncovered
   and the artifact handled it per the fallback policy (nearest pieces,
   visible improvisation, gap filed).
4. false_authority: any place the artifact uses a record for a need that
   record does NOT cover, presented as if covered.
5. unnecessary_gaps: any gap the artifact claims for a need that a record
   actually covers.
6. gap_detection: genuinely uncovered needs, and whether the artifact
   marked/filed them (filed_correctly) or missed them (missed).
7. corrections_required: the concrete changes a reviewer would ask for to
   make the artifact authority-conformant (list of short strings).

Rules: do not modify the artifacts; keep calls efficient; every call through
./run-authority with the workspace as cwd is fine.

Output: write review/score.json with
{"artifacts": [{"id": "ART-01", "brief": "S|R",
  "needs": [...], "false_authority": [...], "unnecessary_gaps": [...],
  "gap_detection": {"filed_correctly": [...], "missed": [...]},
  "corrections_required": [...]}, ...]}
and reply with a compact summary (per artifact: needs correct/total,
false_authority count, unnecessary_gaps count, corrections count).
