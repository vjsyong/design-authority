# Experiment 05 — implementation decisions (Phase 0)

Decisions taken while implementing the revision-7 mechanics layer, recorded
per the plan's evidence discipline. These are implementation-level choices
below the plan's specification; anything that would change the registered
design is flagged as a deviation in the program report instead.

Status: draft until Phase 0 freeze (after rehearsal). Each decision gets a
stable id; later corrections append, never rewrite.

- **I-01 · Sessions.** Every session is an `opencode run --pure` session,
  model pinned to `deepseek/deepseek-flash` (owner-confirmed 2026-10-09;
  matches the benchmark pin), fresh workdir, fresh session, strict
  permissions, per-run XDG config; MCP off; the audited CLI wrapper is the
  authority path (per plan §6.3).
- **I-02 · Run area.** `/home/xrim/x05/` with the §6.1 layout. Tooling in
  the repo at `docs/experiments/seed-evolution/tools/`; frozen agent-facing
  inputs in `docs/experiments/seed-evolution/annexes/`, staged by
  `x05_materials.py` into `x05/materials/` (hashed; the sandbox mounts only
  staged copies). The repository stays invisible to sessions.
- **I-03 · App shape.** The seed is a client-side single-page app served by
  a provided stdlib `serve.py --port N` with `/healthz`; data in
  localStorage under `bookmarks.v1`; no build step, no CDN. Frozen in the
  starter + `QA.md`.
- **I-04 · QA hooks.** Deterministic capture needs stable selectors: briefs
  require `data-testid` hooks per stage (additive only; never renamed).
  This is a plain automation contract presented as project convention; it
  is identical across conditions and constrains only how elements are
  labeled, never how they look or behave.
- **I-05 · Seal scope.** Sealed = the whole workspace except the
  runner-managed reference layer: `reference/`, `opencode.json`,
  `run-authority`. Records = `.design-authority/**`. The seal is a SHA-256
  manifest + read-only copy; every downstream consumer reads seals only.
- **I-06 · Archive for B/C.** The formation archive is the sealed
  `.design-authority/` tree, copied with the checkpoint into chain
  workspaces; chain filings accumulate in the same workspace store. The
  matrix's "read-only" for the archive is realized as: historical records
  are never mutated (audited by seal comparison); new records are the
  agent's own.
- **I-07 · Chain checkpoints.** After every chain session, `x05_extract.py`
  freezes deterministic evidence (inventory, element diff, code diff, role
  instances) and `x05_census.py` classifies the six roles with the frozen
  pass rules and freezes exemplars per established role, timestamped and
  only from this chain's checkpoints so far (plus the inherited seed
  census). The conductor orders freezes before the next chain session.
  Judgment edge cases are retained as raw evidence with review flags; the
  seed census proper is the `cen` session's agent-judged output (same
  schema).
- **I-08 · Budgets.** Wall budget enforced by the runner on the opencode
  child at 2700 s (cap hit named); token cap 20M `sum_total` monitored from
  transcript `step_finish` events, session stopped at the cap. A
  `RuntimeMaxSec=5400` unit backstop covers the post-processing phases.
- **I-09 · Execution units.** Sessions run as transient systemd user units
  (`x05-<id>`), one at a time, launched by the conductor (`x05-conductor`
  user unit, boot-persistent, restart-safe); MemoryMax 6G per session unit
  (D-7 lesson). Replacements only for infrastructure failures; failed
  attempts moved to `<id>-aN`, never deleted; completed-but-unsuccessful
  runs advance and stay in the analysis.
- **I-10 · Containment hardening.** bwrap adds `--unshare-pid`,
  `--unshare-ipc`, `--unshare-uts`, `--new-session` on top of the
  recipe's minimal filesystem, opaque `/opt` mounts, cleared env, and
  per-run config home; workspace mounted at `/opt/ws`; the wrapper and the
  tooling live at opaque `/opt/da` paths.
- **I-11 · Capture fixtures.** Fixed 12-bookmark dataset
  (`annexes/fixtures/bookmarks-seed.json`); states: empty, populated,
  filtered, filtered-none, invalid (+ timing/recovery probe), confirm,
  confirm-bulk, post-delete, analytics, palette, wizard-1/2, at 1280 and
  390. States whose hooks are absent are recorded as unavailable — absence
  is data, never an error.
- **I-12 · Screens to sessions.** The predecessor checkpoint's capture
  screens are copied into each session's `reference/screens/` (all
  conditions) as the frozen current-state reference.
- **I-13 · Rehearsal.** Three pilot sessions (one per condition) at a 300 s
  budget with a trivial task (`briefs/pilot.md`), run through the real
  unit path, against scratch copies under `x05/pilot/`; excluded from all
  analysis; the pass/fail checklist is recorded as pre-flight evidence.
- **I-14 · Freeze.** Briefs and control hashes freeze into `schedule.json`
  at commit time (after rehearsal fixes); any later post-freeze fix is a
  logged deviation and does not invalidate completed sessions.
- **I-15 · Calibration & model-prior material.** The controlled variant
  set (base, faithful, altered with frozen change list) is constructed
  after the chains, before the blind set is assembled, from the seed's
  vocabulary; reviewers remain to be confirmed (owner skipped; re-request
  before blind assembly).
- **I-16 · Session identity.** Commits by sessions use a stable local
  identity (`x05 <x05@local>`); histories remain part of the sealed state.
- **I-17 · Git hygiene for records.** `.design-authority/`, `reference/`,
  `opencode.json`, `run-authority` are gitignored so the archive never
  leaks into git history (condition A's code + history stay archive-clean).
- **I-18 · Network namespace.** The sandbox shares the host network
  namespace (required for model API access), so host loopback services
  (taildash :8080, triage-site :8102, da-review :8420) are technically
  reachable. Mitigations: briefs steer the dev server to port 8090 (free),
  and the leakage scan flags host-service names in transcripts. Residual
  risk recorded in the threats section.
- **I-19 · Prompt delivery.** The brief is fed to opencode via stdin, never
  argv — a rehearsal pilot proved the self-kill class (an agent's
  `pkill -f 'serve.py --port 8080'` matched its own opencode process, whose
  argv contains the prompt; exit 143 at 56 s). Kill commands are recorded
  per session (`opencode.kill_commands`).
- **I-20 · Tool-access allowlist.** opencode `external_directory` allows
  `/tmp/*` on top of the workspace so routine logging/redirects inside the
  sandbox do not hit denials; everything else outside the workspace stays
  denied (interface-bypass discipline).
