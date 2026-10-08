# Agent brief: build under the Jennu authority

Authority: `packs/phantom` v0.2.0 (format 0.1). The Jennu design authority — the interface system of zhenyoyo.github.io as deployed: Source Sans Pro 300/700/900, pink reading ink #ff6bbc with neon-green links #6bff2c on a dotted blue underline, blue-ground code, a lime slide-in menu, red checked marks with purple labels, radius flattened to 0 on marks/boxes/images/chips, ink-ring buttons, underline fields, a tiles-only load-in and one interaction pink #f2849e. Contrast failures are recorded as measured observations (pass 2 extracted what the site IS; pass 1's grey-ink canon was reversed). Per-page black-body overrides are part of the system.

Reference build (what "look like this" means for this authority):
  https://designauthority.seanyong.xyz/authorities/phantom/site/
Every recorded selector, state and note, in one directory:
  https://designauthority.seanyong.xyz/authorities/phantom/site/#artefacts

Build an interface that conforms to THIS authority alone.

## Setup (public repo, MIT; stdlib-only CLI, no installs)

    git clone --depth 1 https://github.com/vjsyong/design-authority.git /tmp/design-authority
    cd /tmp/design-authority

## The loop, for every design decision

1. Orient once:
   python3 tools/da.py --pack packs/phantom overview
2. Resolve each need in natural language:
   python3 tools/da.py --pack packs/phantom resolve "primary button" --json
3. Inspect every record before adopting it:
   python3 tools/da.py --pack packs/phantom inspect <id>
4. Adopt only records from packs/phantom. Never borrow another authority's
   components, values or classes.
5. When the authority is silent: build from the nearest recorded pieces, keep
   the improvisation visible (an HTML comment plus data-improv="<reason>"),
   and file it:
   python3 tools/da.py --pack packs/phantom gap-add --need "<need>" \
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
  https://designauthority.seanyong.xyz/authorities/phantom/site/download/phantom-site.zip
- Inside the zip, `site/` is the shipped build and `pack/` is the same authority
  data this CLI reads; `site/MANIFEST.md` lists sha256 hashes for everything.
