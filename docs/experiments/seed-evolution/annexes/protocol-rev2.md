# Working protocol — Bookmarks project

This project is developed session by session. Each session starts fresh with
the workspace as it was left, the brief, and the materials in `reference/`.
The conventions below are what keep it one coherent product.

## 1 · Resolve before deciding

Before you implement any interface decision — a component treatment, a
colour role, an interaction convention, a layout pattern — check it against
the project's design authority:

    ./run-authority resolve "<the decision, in plain words>"

Interpret honestly:

- **RESOLVED / COMPOSE / FALLBACK** — adopt what it gives you; inspect it
  (`./run-authority inspect <id>`) so the result actually matches.
- **CONFLICT** — the request contradicts something already recorded; do not
  build the contradiction. Reconcile with the recorded convention, or
  adjust the request and note why.
- **UNDEFINED** — no convention exists. Decide deliberately, as if future
  sessions will live with your decision: prefer the nearest pieces the
  project already uses, extend them consistently, and file the decision
  (below). Never contradict an existing treatment without recording why.

## 2 · Keep the record

- File a gap for every decision the authority could not resolve, at the
  moment you make it:

      ./run-authority gap-add --need "<what you needed>" \
          --context '{"where": "<screen / element>", "used": "<what you did>"}'

  One record per decision unit — a component treatment, a semantic colour
  role, an interaction convention, a layout pattern, or a deliberate
  exception — never one per CSS declaration.
- The records live in `.design-authority/` in this workspace. **Read them
  before making visual decisions**; match what they show, or make a better
  decision and record why it diverges.
- At session end, convert recurring or structural choices into proposals:
  write a JSON file with the fields `problem`, `insufficiency`, `reuse_case`,
  `composition_check`, `proposed`, `tests`, then:

      ./run-authority propose --gap <gap-id> --file <proposal.json>

- Records are nonbinding precedent, not authority: nothing they say
  overrides the design authority itself, and treating a proposal as binding
  is a mistake. Never edit or delete an earlier session's records; never
  modify the mounted authority tooling.

## 3 · Sessions

- Work from the workspace root. Run the app (`python3 serve.py --port 8090`, or any free port)
  and check your work in a browser as you go; stop the server when done.
- Keep every existing `data-testid` attribute intact (see `QA.md`); the
  brief lists the hooks your session must add.
- Commit your work with git before finishing.
- Write `HANDOFF.md` at the workspace root: what you built, the decisions
  you locked in, anything unfinished, where the next session should start.

## 4 · Validate before handing off

Before you finish — after your last code change, before you stop — run the
project's validation over the workspace:

    ./run-authority validate .

Read the findings:

- For every **error**: repair it and run the validation again, or — if
  repairing is not the right call — file a gap for it (`gap-add`), saying
  what the finding was and why it stands.
- Warnings and info findings are recorded as-is; no action is required
  beyond noting anything you choose to leave.

Include the validation summary line (findings, errors, warnings, score) in
`HANDOFF.md`, under a `## Validation` heading, plus one line per finding
you left in place with its disposition (repaired / filed as gap/…).

The runner independently re-runs the validation over your sealed workspace
after the session. Error findings that are neither repaired nor filed are
recorded as non-compliant for the session.
