# Agent brief: build under the Dominion Interface System authority

Authority: `packs/dominion` v0.2.0 (format 0.1). An austere civic interface system derived from the Government of Canada FIP standard and the live Canada.ca web layer for the Design Authority synthesis experiment. Bilingual, structured, calm; no government marks reproduced.

Reference build (what "look like this" means for this authority):
  https://designauthority.seanyong.xyz/authorities/dominion/site/
Every recorded selector, state and note, in one directory:
  https://designauthority.seanyong.xyz/authorities/dominion/site/#artefacts

Build an interface that conforms to THIS authority alone.

## Setup (public repo, MIT; stdlib-only CLI, no installs)

    git clone --depth 1 https://github.com/vjsyong/design-authority.git /tmp/design-authority
    cd /tmp/design-authority

## The loop, for every design decision

1. Orient once:
   python3 tools/da.py --pack packs/dominion overview
2. Resolve each need in natural language:
   python3 tools/da.py --pack packs/dominion resolve "primary button" --json
3. Inspect every record before adopting it:
   python3 tools/da.py --pack packs/dominion inspect <id>
4. Adopt only records from packs/dominion. Never borrow another authority's
   components, values or classes.
5. When the authority is silent: build from the nearest recorded pieces, keep
   the improvisation visible (an HTML comment plus data-improv="<reason>"),
   and file it:
   python3 tools/da.py --pack packs/dominion gap-add --need "<need>" \
     --context '{"source":"<your app>"}' --workspace .design-authority

## House rules

- Quote recorded values (colours, sizes, radii, type) from the records; never
  invent values that a record can give you.
- Copy selectors and states from the artefacts directory, not from memory.
- Plain HTML/CSS is enough; the authority requires no framework.
- An agent's own report is evidence, not proof. Re-read the artifacts.

## Take it away

- Download the reference build in one file (page, styles, fonts, the pack, the
  full audit trail):
  https://designauthority.seanyong.xyz/authorities/dominion/site/download/dominion-site.zip
- Inside the zip, `site/` is the shipped build and `pack/` is the same authority
  data this CLI reads; `site/MANIFEST.md` lists sha256 hashes for everything.
