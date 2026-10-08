# Runtime profile: the kernel, the CLI, the MCP server, and would Rust make sense?

Measured 2026-10-08 on the dev workstation (CPython 3.14.7) at the public release
state. Reproduce with `python3 tools/bench_kernel.py` (read-only; prints to stdout).

## What the system actually serves

Three consumer paths, in order of expected use:

1. **MCP calls** from a long-lived agent session (resolve, search, inspect, validate, gaps).
2. **CLI invocations** by agents or humans (`da.py resolve ...`).
3. **CI validation** (`da.py validate <project>` runs the pack's pinned linter).

## Numbers (battery n = 137 asks: 54 golden + 83 coverage)

| path | metric | value |
|---|---|---|
| pack load | 109 KB JSON, 80 artifacts | 1.6 ms mean (2.1 ms p95) |
| resolve | per ask, warm | 0.30 ms mean · 0.25 ms p50 · 0.36 ms p95 (first call 5.4 ms) |
| search | per query | 0.23 ms |
| inspect | by_id lookup | below 1 microsecond |
| scaling | 80 to 320 to 800 artifacts | resolve 0.34 to 1.17 to 2.71 ms (near-linear); load 1.4 to 8.2 to 8.8 ms |
| validate | concept site, end to end | 387 ms, dominated by the pinned linter subprocess (itself `python3`) |
| CLI cold start | `da.py resolve "a primary button"` | 73 ms wall: interpreter boot 17.5 ms, imports + load about 30 ms, kernel work under 1 ms |
| MCP server | startup + 20 tool checks | 785 ms total (startup once per session; calls are then kernel time plus JSON-RPC) |
| memory | peak RSS, one CLI invocation | 18 MB |

Where resolve time goes (cProfile over the battery): 0.096 s of 0.111 s sits in
`pack.search`, the deterministic tokenize-and-score loop over artifacts (79,725
scoring iterations). Everything else is microseconds.

## Reading the numbers

- **The kernel is not a bottleneck at any plausible pack size.** Resolve is
  sub-millisecond at 80 artifacts and about 3 ms at ten times that. The only
  O(pack) step is the scoring loop.
- **The dominant costs around the kernel are process and protocol overhead:**
  Python interpreter boot, imports, and for validate the linter subprocess.
  None of these scale with the kernel's logic.
- **The consumers are latency-insensitive.** An LLM agent turn is seconds; a
  sub-millisecond resolve inside it is invisible. A 387 ms CI validate is noise
  against build times. A 73 ms human CLI invocation is imperceptible.

## Would a Rust rewrite make sense?

**Verdict: no, not for runtime performance as the system exists and is used.**

What Rust would win:

- resolve 0.3 ms to roughly 0.01 to 0.05 ms (a 10 to 30 times constant factor);
- CLI cold start 73 ms to about 2 to 5 ms (the one dramatic win: it deletes the
  interpreter boot);
- RSS 18 MB to roughly 3 MB;
- single static binary distribution.

Why those wins do not matter here:

- The only structurally large number (CLI cold start) disappears for the primary
  consumer: the MCP server is long-lived, so startup is paid once per session.
  If CLI-heavy use ever appears, cheaper steps come first: a batch mode (one
  process, many asks), trimming CLI imports, and staying in-process.
- Headroom: at the observed near-linear scaling, the kernel crosses 100 ms per
  resolve around 30,000 artifacts, and even that only matters if the consumer
  budget is interactive (keystroke time) or high-QPS. Neither is the case.
- A rewrite would have to be parity-exact against the **frozen 0.2.0 semantics**
  (deterministic pipeline, scoring weights, precedents, variants). Under this
  project's own rules that is a governance event: a reimplementation, a parity
  battery, and a fresh freeze, plus a permanent two-language maintenance
  surface.
- Distribution for the one-instruction install story gets **worse**: instead of
  "python3 only", a cross-platform binary matrix for agent machines.

When to revisit (thresholds, in order of likelihood):

1. Packs grow to six figures of artifacts and a sub-10 ms budget appears.
   Before Rust: an inverted token index makes resolve near-constant in pack
   size, and that is a small Python change.
2. A shared sidecar serves many concurrent agent sessions at high QPS.
3. The kernel gets embedded inside a non-Python toolchain.
4. Single-binary, zero-dependency distribution becomes a product requirement
   (a packaging argument, not a performance one).

## Re-run

```bash
python3 tools/bench_kernel.py
```
