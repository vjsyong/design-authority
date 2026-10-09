# Experiment 05 — pre-flight rehearsal record (Phase 0)

Status: **PASS** — all three conditions rehearsed end to end on 2026-10-09.
Rehearsal artifacts live under `/home/xrim/x05/pilot/` (excluded from all
analysis). This record is the pre-flight evidence required by plan §6.8.

## What ran

- **Sandbox probe** (condition-B profile, plus the A-profile check):
  toolchains import (Python 3.14.7, Node 26.7.0), chromium launches through
  Playwright, the authority wrapper resolves against the mounted pack and
  writes its audit trail, `git` works, and the isolation probe shows
  `/home/xrim/x05` and the meta repository invisible from inside; `/opt/da`
  is absent in the A profile.
- **Dry pipeline, no agent** (stage → schedule → f1 → f2): byte-verified
  seal copies, capture, extraction, chain diff, seals — all green.
- **Three throwaway sessions**, one per condition, reduced budget (300 s
  configured, trivial task), executed through the production path
  (bubblewrap sandbox, per-session systemd unit, capture + extraction + seal
  + leakage audit + kill forensics).

## Results per condition

- **A**: exit 0, 36 s, 106 k tokens, capture 24/24, seal verified,
  HANDOFF.md + commit present, zero containment flags. No wrapper — correct
  for A.
- **B**: exit 0, 274 s, 142 k tokens; wrapper used (resolve + gap-add;
  audit.jsonl = 2 calls); one gap filed into `.design-authority/`; HANDOFF
  + commit; seal verified; zero containment flags.
- **C**: exit 0, 36 s, 136 k tokens; wrapper used (overview + resolve +
  gap-add; 3 audit lines); one gap filed; seal verified; zero flags.

## Findings fixed during rehearsal

1. **Self-kill class (P1, fixed).** Pilot A attempt 1 died at 56 s with
   exit 143: the agent's `pkill -f 'serve.py --port 8080'` matched
   opencode's own process, because the prompt was passed in argv (the
   documented argv/self-kill failure mode). Fix: the brief now goes to
   opencode via **stdin, never argv**; kill-command forensics are recorded
   per session (`opencode.kill_commands`). Rehearsed after fix: agent uses
   `kill $PID`; exit 0.
2. **Port collision and host services (P2, mitigated).** The sandbox shares
   the host network namespace (required for model API access), so port 8080
   is the host's taildash; the agent collided with it and host loopback
   services are technically reachable. Mitigations: briefs point at port
   8090; the leakage scan flags host-service names; residual risk carried
   into the threats section.
3. **Tool-access friction (P3, mitigated).** opencode denied routine writes
   to `/tmp/...` outside its own tool-output dir; `/tmp/*` added to the
   tool-access allowlist (workspace + tmp only; everything else stays
   denied to keep interface discipline).
4. **Capture action parsing (P4, fixed).** `click-menu`/`fill` state
   actions were unpacked incorrectly (4 states failed on the first dry
   run); fixed and re-verified, 24/24 in every run since.

## Checklist (plan §6.8)

- [x] containment: filesystem fence + audit; zero attempts across pilots
- [x] wrappers: audited CLI exercised in B and C; records + audit lines correct
- [x] capture: 24/24 state-viewports per pilot, 0 console errors
- [x] sealing: manifests created and verified for all three pilots
- [x] auditing: leakage scan + kill forensics recorded per session
- [x] sandbox probes: toolchains import, browser launches, isolation clean
- [x] production execution path: per-session systemd units; conductor unit
  installed (`x05-conductor.service`, boot-persistent)

## Residual risks carried into the run

- Shared network namespace: host loopback services reachable; audited and
  flagged, not eliminated.
- Host stability (the documented SIGTERM-cluster / VM-restart class):
  one-session-at-a-time execution, conductor pause rails, replacement
  policy per revision 5.
- Model endpoint availability: transport failures classify as
  infrastructure; replacements logged.
