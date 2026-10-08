# Brief R - Release notes page

Build ONE HTML page: a release notes screen for an app.

- A list of past releases: version, date, and a one-line summary each.
- Each release shows whether it is stable or beta.
- A way to narrow the list to one channel, if a sanctioned pattern exists.
- The page should sit in the app's usual chrome (sidebar or top navigation) if
  the authority covers it.

Rules: one self-contained file (index.html) styled only from the assets copied
into this workspace at assets/ (link assets/tokens/tokens.css,
assets/core/base.css, assets/core/patterns.css). Every UI decision should come
from the design authority (resolve, inspect). When the authority has no answer,
follow its fallback policy: build from the nearest recorded pieces, keep the
improvisation visible, and report a gap.
