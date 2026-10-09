# CI contract verification (verify-estate)

`contract-targets.json` maps each authority that ships a verification
contract to the build the contract is calibrated against (committed in this
repo) plus any KNOWN findings that are tolerated.

`python3 tools/ci_verify.py [--auth NAME]` runs `da_verify` per entry and
fails on any finding outside the recorded baseline. The meta CI job
`verify-contracts` runs it as a matrix (one leg per authority) on every
push, nightly, and on demand.

Baseline discipline: an entry in `expected_findings` is a recorded, known
state - never a way to silence a new problem. New findings fail CI; adding
to the baseline is a deliberate edit with a stated reason. Current entry:
leader's `focus-visible` - the v3.1 build's search input suppresses its
outline without an alternative; recorded as a true finding since the
verification era, and the build is a sealed artifact, so it stays visible
in the baseline rather than patched away.
