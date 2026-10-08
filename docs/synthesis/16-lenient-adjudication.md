# 16 — Lenient Adjudication: Candidates, Undefined Deferral, Scoped Declines

Owner doctrine (2026-10-07): *the adjudicator should be lenient with denies —
defer to UNDEFINED when evidence is insufficient, or promote to **candidate**
rather than authority.* Declines are a last resort, reserved for grounded
policy. This supersedes the decline-heavy posture of the first adjudication
pass (see 14-codification.md).

## The three rungs (replacing the blunt deny)

| Rung | When | What happens | Where it lives |
|---|---|---|---|
| **Candidate** | Partial evidence; a direction exists but is not canon (e.g. a stated composition) | Recorded as a provisional entry. NOT authority. Consumers may adopt it as a *marked* starting point; promotion requires named evidence, then proposal → review | `packs/*/candidates.json` |
| **Undefined deferral** | No/insufficient evidence | The ask stays UNDEFINED. Improvise in character + mark; no negative precedent; gap remains open | nowhere (the default state) |
| **Decline** | Genuine policy (asset law, motion doctrine, prohibitions, off-grammar geometry) AND a sanctioned alternative exists | Precedent with `grounds`, scope domains, mandatory **boundary**, and the try-list | `packs/*/precedents.json` |

Hard requirements, enforced by `tools/precedent_probe.py`:
- every precedent carries `grounds` + `scope.domains` + `scope.boundary` (non-empty);
- every candidate carries `promote_when` (the evidence bar);
- reviewer rejections are owner decisions and are never re-classified by this
  leniency (all 5 rejected proposals still stand).

## Scope is forced, not blanket (the tick lesson)

`precedent_matches` now returns a **verdict** per precedent:
- `governs` — inside the declared scope; may be treated as declined (follow try-list)
- `outside` — boundary vocabulary hit; **explicitly not governed** → proceed as an
  ordinary marked improvisation
- `ambiguous` — domains + boundary both hit → improvisation unless a human rules

Consumers: `resolve` attachments (with verdict + boundary), search results,
`report_gap` / `propose_extension` warnings, CLI `precedent-check --ask`,
MCP `check_precedent`. The tick incident is regression case #1: “a check
control to log a ritual” now returns `outside` (functional controls are
boundary-exempt), while “photo upload for the ritual” still `governs`.

## Re-classification of the 20 adjudication declines

KEPT as grounded declines (5): wink photographic imagery (asset policy);
leader loading/spinner motion + imagery/icons; dominion photographic imagery +
celebration motion/toasts.

SPLIT (2): dominion ring/streak/badges → ring kept (off-grammar D-02), streak
+ badges → candidate; dominion pictograms/tags → pictograms kept (D-22), tags
→ candidate.

PROMOTED to candidates (2 gaps): wink pager/drag → pager composition candidate;
dominion view-tabs/paging → paging composition candidate.

DEFERRED to undefined (11): chart treatments, glyph sets, neutral tag,
native controls, csv, dark mode (wink); drag, csv, dark mode, toggle/slider,
checkbox/radio, date/select (leader); view tabs (dominion). No negative
precedent remains for these — agents improvise in character and mark.

Final registers: wink 2 (1 policy + 1 reviewer) / leader 4 (2 + 2) /
dominion 6 (4 + 2) precedents; candidates: wink 1 / leader 0 / dominion 3.

## Verification

- `tools/precedent_probe.py`: **31/31** (counts, schema, governs, outside
  regressions, deferrals, candidates, search kinds, gap/proposal warnings).
- Kernel unit tests **17/17**; MCP smoke **20/20** (2 new tools:
  `check_precedent`, `list_candidates`); goldens unchanged (19/18/14/17).
- Gate `/proposals` record rows now show the lenient outcome per decline:
  *deferred to undefined* (11) · *promoted to candidate* (2) · *split* (2) ·
  *declined — policy* (5), via `data/lenient.json`.

## Candidate lifecycle (for the next rebuild)

`candidates.json` is kernel-generic and optional; candidates surface in
search, attach on UNDEFINED in resolve, and warn gap/proposal filings
(`candidate_hints`). A candidate moves to canon only by the normal path:
capture the named evidence → proposal → owner verdict → codify. If a consumer
adopts a candidate, it must be marked as such — never presented as canonical.
