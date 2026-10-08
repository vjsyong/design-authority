# 12 · Authority-driven sites — the gallery and the rc release policy

*Owner directive, 2026-10-08: (1) decouple triage.seanyong.xyz from
hand-written content so an authority update flows to the page automatically;
(2) generalize this into a gallery for every authority, built on the
skeleton, where new records simply plug in; (3) release policy: agents
auto-bump `-rc` versions only, full versions are a human promotion.*

## 1 · Where things stand (recon, 2026-10-08)

- **triage.seanyong.xyz** → Cloudflare tunnel → `127.0.0.1:8102` → docker
  `triage-site` (compose at `~/triage-design-system/docker-compose.yml`),
  running `site/serve.py`, a stdlib server that renders hand-written Python
  pages (`pages_*.py`, `layout.py`, `site_data.py`). Version strings,
  component catalogues and release notes are hard-coded; authority updates
  do not reach it.
- **designauthority.seanyong.xyz** → `127.0.0.1:8420` → `da-review`
  (`docs/synthesis/review-app/app.py`). It **already renders per-authority
  pages from packs** (`/authorities/<name>/audit` ← `_demo_page`: artifacts,
  rules, prohibitions, fallbacks, recipes, golden summary, agent prompt).
  Two hand-holds block true decoupling: `PACK_META` is a hard-coded
  five-pack list, and `_demo_packs` caches packs forever (an updated pack
  needs a service restart to show).
- Authority packs (`packs/<name>`) are the machine-readable records; the
  round-2 flow proves authority updates happen (triage `0.13.1-experiment`).

## 2 · Target architecture

One rule: **the pack is the single source; every site surface is a view; a
pack update is visible without hand edits.**

### 2.1 The gallery (all authorities)

- **Discovery**: auto-discover `packs/*`; no hand-maintained lists. A new
  authority (drop a pack dir) appears without code changes.
- **Freshness**: mtime-based cache invalidation; a rebuilt pack shows on the
  next request, no service restart.
- **Rendering on the skeleton**: per authority — version + status strip
  (rc vs full), counts by kind, release/provenance notes (BUILD.json,
  evolution overlay, CHANGELOG where present), standing disputes, golden
  summary; then sections per kind; then per-artifact cards (title, class,
  states, a11y, aliases, source, provenance). Zero hand-written facts.
- **Skeleton**: the gallery pages wear the Triage shell (the concept site
  already enforces "foundations byte-identical to Triage"; same here), with
  the authority's records as the content. This is what "plug in the pieces"
  means mechanically.
- **Where**: `da-review` routes — `/authorities/` (gallery root) and
  `/authorities/<name>/gallery` (canonical); existing URLs keep working.
  Renderer extracted to its own module so the app does not grow.

### 2.2 triage.seanyong.xyz decoupled

- `site/serve.py` gains authority reads; the container mounts the active
  triage authority pack read-only (compose volume). Version pill, release
  notes and the spec/catalogue surfaces render from the pack
  (`manifest.version`, CHANGELOG, records); the live demo pages stay as
  they are, but their metadata (class, states, a11y) comes from records.
- **Active pack pointer**: `packs/CURRENT.json` maps authority → active pack
  dir (`{"triage": "triage-evolution"}` to start); promotion moves it.
- **Automatic**: agent rebuilds the pack (rc bump) → next request shows the
  new version; a human promotion flips the status chip from rc to released.

### 2.3 Release policy (`-rc`)

- **Agents**: version bumps only as `X.Y.Z-rcN` (triage repo
  VERSION/package.json/spec sync, pack labels, overlay release labels).
  This happens automatically inside the governed loop.
- **Humans**: promotion `X.Y.Z-rcN → X.Y.Z`, recorded with the reviewer and
  date (CHANGELOG + release note). Only human reviewers bump full versions.
- **Mechanics**: triage repo gains `tools/release.py` (`rc` and `promote`
  subcommands); `build.py check` accepts the `-rcN` pattern and keeps the
  sync check strict; the design-authority spec text lands in the next spec
  rc (`0.6.0-rc1`, demonstrating the policy); skills updated.
- **Grandfathering**: `0.13.0`/`0.13.1-experiment` predate the policy and
  stay as historical. The first human promotion available is the current
  line itself.

## 3 · Stages and acceptance

- **S1 · Gallery renderer — DONE (2026-10-08).** `authority_gallery.py` +
  app.py routes: `/authorities/` (root) and `/authorities/<name>/gallery`.
  Discovery is filesystem-driven (8 packs found, triage-evolution included);
  mtime-based freshness verified (touching a pack reloads it with no
  restart); `PACK_META` removed, no hand-maintained pack lists remain; the
  pages wear the skeleton (concept-site foundations + chrome) and render
  version/status chips, release strip (BUILD.json), provenance, golden
  table, and per-kind sections down to per-record cards. Live on
  designauthority.seanyong.xyz. Acceptance met: all packs listed; pack
  update visible without restart; no hand lists.
- **S1b · Doc-site shells — DONE (2026-10-08).** Each authority's gallery is
  now a multi-page site in the Triage doc-site shape: the system's own shell
  (side nav with per-kind counts, active states, mobile drawer, theme and
  density toggles), an overview, a page per catalogue kind
  (`/gallery/components`, `/patterns`, `/guidelines`, `/tokens`, `/recipes`,
  `/examples`, `/references`), and a spec page (rules, prohibitions,
  fallbacks). Every page renders from pack records only. Verified: all
  routes 200 across all 8 packs, 404 for unknown pages, drawer + scrim +
  theme toggles exercised live, desktop and 390px screenshots reviewed.
- **S1c · Per-authority retheming — DONE (2026-10-08).** Each gallery
  site wears its own authority's visual language (`authority_themes.json`):
  wink (yellow mark, Fraunces, kale links, pills), leader (red mark + rule,
  Archivo Black wordmark, Gelasio serif, Chicago blue), dominion (FIP red,
  Arimo, squared), phantom (pink ink, lime panel mark, blue dotted links,
  900 caps), indaba (aubergine, orange, warm tint, Ubuntu stack), orbit
  (ink/gray/red plates, Helvetica, squared). Values traced to each pack's
  token-set records + build archives; fonts served via `/authority-fonts/`
  (declared faces only). CSS-variable overrides over the shared shell.
- **S1d · Authority-built sites — DONE (2026-10-08).** Six agent builds,
  one per authority (wink, leader, dominion, phantom, indaba, orbit), each
  executed UNDER its own pack through an audited wrapper
  (`examples/authority-sites/<auth>/`): resolve/inspect/adopt, fallback +
  visible marking + filed gaps where the authority is silent. Served at
  `/authorities/<name>/site/`. Verified: audit-vs-log counts match
  (48/41/44/57/61/43), no external references, no foreign-system markers,
  2-3 gaps each; pages reviewed at desktop. The earlier variable-override
  retheme (S1c) stands only as the generated records view; these builds are
  the authority-conformant sites.
- **S1e · Static-asset archives — DONE (2026-10-08).** Every authority
  build's CSS is extracted to a first-class `styles.css` (linked from the
  page) and each build carries `archive-manifest.json` + `MANIFEST.md`:
  sha256 of every file (page, stylesheet, fonts, log, audit.jsonl, gap
  store) with roles, font provenance (byte-identical checks against known
  sources), and the external-reference count. Tool:
  `tools/archive_authority_assets.py` (idempotent; `--verify NAME` re-hashes
  and compares). Manifests serve alongside the builds under
  `/authorities/<name>/site/`.
- **S1f · Artefacts directory — DONE (2026-10-08).** Every authority build
  gains a generated `section#artefacts` (inserted before Specification, with
  a nav entry cloned from the page's own Catalogue link): every artifact
  grouped by kind with title / id / status / summary, a USE block carrying
  the recorded selector, states and a11y/verify notes, aliases, and a copy
  button that yields a ready-to-use snippet; live filter over name, alias
  and kind with a live count. Styled per authority from the traced values in
  `tools/add_artefacts_section.py` (idempotent). Serving fixes: site files
  now send `Cache-Control: no-cache`, stylesheet links are cache-busted, and
  the stale Cloudflare edge copies were purged (the edge had cached the old
  `.css` by extension) - lesson: any update to a served `.css` on the
  designauthority host needs an edge purge or a URL change.
- **S2 · triage.seanyong.xyz — DONE (2026-10-08).** `site/authority.py`
  (reads `TRIAGE_AUTHORITY_DIR` or the `/authority` mount, then
  `CURRENT.json`) + `layout.py` version surfaces (brand-sub, side-foot,
  topbar status, footer) + compose read-only mount + `packs/CURRENT.json`.
  Verified live: all four surfaces render v0.13.1-experiment; flipping the
  pointer to the pinned pack flips every surface to v0.12.1 and back, with
  no restart. Known remainder: the home page's hand-written "What's new"
  card (content-level; the next release-notes surface should render from
  CHANGELOG).
- **S3 · Release tooling**: `tools/release.py`, check updates, spec rc text,
  skill updates.
- **S4 · Promotion demo**: human promotes the current line end-to-end
  (rc → full), recorded.

## 4 · Defaults (flag if wrong)

- Gallery canonical URL `/authorities/<name>/gallery`; the existing `/audit`
  pages stay reachable.
- The active triage authority surfaced publicly is the evolution line (where
  agents' rc updates live); the pinned 0.12.1 pack remains frozen for
  experiments.
- rc numbering per change batch: `-rc1`, `-rc2`, ...
