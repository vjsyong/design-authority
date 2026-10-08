# log.md — audit of every authority call

Build: the Jennu (Phantom) Interface System documentation page (`index.html`), under the
**phantom** authority, workspace `examples/authority-sites/phantom/`.
All calls below went through the audited runner `./run-authority` (machine record: `audit.jsonl`
alongside; gaps in `.design-authority/gaps.jsonl`). Order is execution order. Output is trimmed;
full records are in `audit.jsonl`.

**Budget note:** 57 calls total (8 with non-zero rc: the two initial gap-add syntax retries, three
unsupported inspect probes, the multi-id inspect probe, the `review` usage error and the
unavailable `discover` — all kept in the record). The brief's guideline was ≈35; surfacing every
catalogue artifact across searches plus CLI interface discovery overshot it. Every call is logged
here regardless.

**Deliverables:** `index.html` + `source-sans-pro-{300,700,900}-latin.woff2` + this `log.md`.
Fonts: only the three weights the guideline records (no 400, no italics). No network, no borrowed CSS.

---
01. `./run-authority overview` — rc=0
    output: phantom — 0.2.0 (format 0.1) …
    Why + conclusion: Orient: pulled the pack manifest and policy. Counts fix the catalogue scope: 29 artefacts across 4 kinds, 8 rules, 2 prohibitions, 4 fallbacks, 0 recipes.

02. `./run-authority overview --json` — rc=0
    output: {"authority": {"authority": "phantom", "version": "0.2.0", "commit": "n/a - public sources"}, "description": "The Jennu design authority \u2014 the interface sy…
    Why + conclusion: Same manifest as JSON: description, counts, capabilities, fallback/conflict policy, resolution semantics. The description becomes masthead material, verbatim.

03. `./run-authority --help` — rc=0
    output: usage: da [-h] [--pack PACK] …
    Why + conclusion: Command surface: overview/search/discover/inspect/resolve/validate/golden/gaps/gap-add/propose/dispute-*/review/precedents/precedent-check/candidates.

04. `./run-authority search --help` — rc=0
    output: usage: da search [-h] [--kinds KINDS] [--limit LIMIT] [--json] query …
    Why + conclusion: Syntax: search Q [--kinds] [--limit] [--json] — no listing mode, so the catalogue must be surfaced by queries.

05. `./run-authority inspect --help` — rc=0
    output: usage: da inspect [-h] id
    Why + conclusion: Syntax: inspect takes ONE id only (single positional).

06. `./run-authority resolve --help` — rc=0
    output: usage: da resolve [-h] [--context CONTEXT] [--json] [--assist {off,semantic}] …
    Why + conclusion: Syntax: resolve takes problem(s) positionally; --json supported.

07. `./run-authority gap-add --help` — rc=0
    output: usage: da gap-add [-h] --need NEED [--context CONTEXT] [--scope SCOPE] …
    Why + conclusion: Syntax: gap-add --need NEED [--context] [--scope] [--workspace] — --context is parsed as JSON.

08. `./run-authority gaps --help` — rc=0
    output: usage: da gaps [-h] [--workspace WORKSPACE] [--json]
    Why + conclusion: Syntax: gaps [--workspace] [--json] — workspace-scoped gap store.

09. `./run-authority search '' --json --limit 100` — rc=0
    output: 0 results: 
    Why + conclusion: Empty query matches nothing — search needs real tokens.

10. `./run-authority gaps --json` — rc=0
    output: 0 results: 
    Why + conclusion: No gaps filed yet; workspace gap store starts empty.

11. `./run-authority search e --json --limit 200` — rc=0
    output: 0 results: 
    Why + conclusion: Single characters are dropped by the tokenizer — needs word-level queries.

12. `./run-authority search menu --json --limit 200` — rc=0
    output: 11 results: component/menu-panel, component/nav-hamburger, layout/header, layout/page-shell, fallback/no-script, fallback/light-only …
    Why + conclusion: First sweep hit: menu cluster (menu-panel, header pill, page-shell, fallbacks) — the pack is searchable.

13. `./run-authority search button --json --limit 200` — rc=0
    output: 8 results: component/action-button, component/actions, component/checkbox-radio, component/nav-hamburger, layout/header, guideline/typography-voices …
    Why + conclusion: Button cluster: action-button plus related components — catalog enumeration feasible by keyword sweeps.

14. `./run-authority search link --json --limit 200` — rc=0
    output: 8 results: precedent/pink-ink-canonised, token-set/colour, candidate/text-as-accent, component/actions, component/icon-row, component/menu-panel …
    Why + conclusion: Link cluster: token-set/colour, precedent, candidates surfaced — extra record kinds appear in results.

15. `./run-authority search site --json --limit 200` — rc=0
    output: 27 results: component/emblem-logo, layout/header, layout/page-shell, component/hr, component/image, component/menu-panel …
    Why + conclusion: Broadest early sweep: 27 results (16 of 17 components, 4 layouts, all 6 token sets, the guideline).

16. `./run-authority search the --json --limit 500` — rc=0
    output: 0 results: 
    Why + conclusion: 'the' is a stopword and dropped — no free full dump. Enumeration must stay keyword-driven.

17. `./run-authority search 'component layout token-set token rule fallback page site text' --json --limit 500` — rc=0
    output: nd": "layout", …
    Why + conclusion: Multi-token union sweep: 35 results — all 5 layouts (incl. project-page), 16 components, 6 token sets, 3 fallbacks, precedent, candidates. Only 1 component + 1 fallback + rules/prohibitions still unseen.

18. `./run-authority search 'rule prohibit prohibition restriction forbidden never must violation' --json --limit 500` — rc=0
    output: 7 results: component/hr, component/table, component/blockquote, component/checkbox-radio, component/menu-panel, layout/page-intro …
    Why + conclusion: Rule/prohibition words return components and precedent only — rules are not indexed in search; another route is needed for the spec section.

19. `./run-authority search 'form figure spotlight banner motion print reduce prefers contrast illustration portrait avatar container wrapper grid section' --json --limit 500` — rc=0
    output: 16 results: layout/page-shell, component/image, component/tiles, layout/page-intro, layout/footer, component/actions …
    Why + conclusion: Form/media guesses returned nothing new — the missing 17th component needs different words.

20. `./run-authority golden` — rc=0
    output: MISS  RESOLVED   (want RESOLVED  ) a primary button  -> component/action-button …
    Why + conclusion: Golden ran the pack's 56 self-checks (agreement 0/56) and surfaced prohibit/unreadable-accent-ink in a CONFLICT sample — a prohibition id in hand.

21. `./run-authority review` — rc=2
    output: da review: error: the following arguments are required: --proposal, --verdict  [stderr] da review: error: the following arguments are required: --proposal, --verdict
    Why + conclusion: review needs --proposal/--verdict — it is an adjudication tool, not an enumerator.

22. `./run-authority search 'poptrox lightbox zoom caption credit photo picture audio album masonry column sidebar widget scroll arrow jump toggle switch range textarea legend fieldset submit reset placeholder drop' --json --limit 300` — rc=0
    output: 13 results: component/tiles, component/action-button, component/field, component/actions, component/image, component/nav-hamburger …
    Why + conclusion: Found component/carousel-gallery — the 17th and last component. All 29 artefacts now identified.

23. `./run-authority inspect prohibit/unreadable-accent-ink` — rc=0
    output: prohibition prohibit/unreadable-accent-ink — Accent ink relied on as the only readable signal where measured contrast < 3:1 — as a reusable-system guard. Measured in the deployment: pink/white 2.…
    Why + conclusion: Inspected the surfaced prohibition: statement, signals, and its rule reference P-R1 — the first verbatim quote for the spec section.

24. `./run-authority search 'flattened radius marks boxes chips ink ring underline tiles load interaction black body override measured observation grey canon reversed slides slide' --json --limit 300` — rc=0
    output: ntro", …
    Why + conclusion: Radii/shape sweep found no rules — the deployment's flattening is recorded as description, not a rule entry.

25. `./run-authority search 'accessibility wcag unreadable readable caps uppercase lowercase tracking letterspacing letter voice' --json --limit 300` — rc=0
    output: 7 results: token-set/tracking-and-case, guideline/typography-voices, component/action-button, component/emblem-logo, token-set/type-scale, component/menu-panel …
    Why + conclusion: Accessibility sweep returned only token sets/components — confirms no rule surface in search.

26. `./run-authority resolve 'a site masthead with a name, version, one-line description and an emblem or wordmark' 'a catalogue listing every recorded artifact grouped by kind, each with a title and summary' 'a specification summary section: recorded rules and prohibitions as scannable lists' 'a footer with two short sections and an attribution or copyright line' 'a slide-in site menu opened from a fixed trigger pill' 'a long-form documentation body: paragraphs, inline links, code samples and verbatim quotes' 'a page load-in motion for a documentation page' 'the page at 1280px and at 390px widths' 'dark mode support for the site' 'page behaviour when JavaScript is unavailable' --json` — rc=0
    output: outcome=RESOLVED → layout/page-shell
    Why + conclusion: Resolve of a compound problem: the CLI joins positional problems into ONE problem, resolved to layout/page-shell (with emblem-logo, header, nav-hamburger as alternatives). Page shell summary captured; batching resolves is ruled out.

27. `./run-authority resolve 'a catalogue section listing every recorded artifact grouped by kind, each entry with a title and a summary' --json` — rc=0
    output: outcome=UNDEFINED
    Why + conclusion: Resolve 'catalogue section' → UNDEFINED. The doc-page catalogue is genuinely unrecorded — gap candidate 1.

28. `./run-authority resolve 'a specification summary section presenting the recorded rules and prohibitions as scannable lists' --json` — rc=0
    output: outcome=UNDEFINED
    Why + conclusion: Resolve 'specification summary section' → UNDEFINED. Also unrecorded — gap candidate 2.

29. `./run-authority precedents --json` — rc=0
    output: {"authority": {"authority": "phantom", "version": "0.2.0", "commit": "n/a - public sources"}, "count": 1, "precedents": [{"id": "precedent/pink-ink-canonised", …
    Why + conclusion: precedents --json: precedent/pink-ink-canonised in full — reason, try lines, and the P-R1 citation ('follow the deployed ink map'), plus the sanctioned black-body override.

30. `./run-authority inspect token-set/colour token-set/type-scale` — rc=2
    output: da: error: unrecognized arguments: token-set/type-scale  [stderr] da: error: unrecognized arguments: token-set/type-scale
    Why + conclusion: Multi-id inspect is refused (one id per call) — inspection stays per-record.

31. `./run-authority inspect fallback/no-script` — rc=0
    output: fallback fallback/no-script — Without JS the load-in is skipped and content renders immediately (noscript.css lifts is-preload). The menu remains JS-dependent (slide-in + dimming);…
    Why + conclusion: fallback/no-script: statement + constraints, including 'menu behaviour undefined without JS — mark it'. This governs the menu marking.

32. `./run-authority inspect token-set/colour` — rc=0
    output: token-set token-set/colour — Deployed reading ink is pink #ff6bbc (body/h1–h4/footer/table/form text), overriding the template's #585858; content links are neon green #6bff2c with…
    Why + conclusion: token-set/colour: the deployed ink map with hexes — pink #ff6bbc, neon #6bff2c on dotted #20a3f5, hover #f2849e, code blue ground, lime #3ef900 menu, control colours, grounds, measured contrasts.

33. `./run-authority inspect token-set/type-scale` — rc=0
    output: token-set token-set/type-scale — Rendered scale: body 12pt=16px at ≤1280 (18.67px ≤1680, 21.33px above), line-height 1.75. h1 2.75em (44px @1280; 32px ≤736) weight 700, lh 1.3, −0.035…
    Why + conclusion: token-set/type-scale: body 16px/1.75, h1 2.75em/700/−0.035em, caps voice 900/+0.35em, buttons 0.8em, code 0.9em Courier New.

34. `./run-authority inspect token-set/tracking-and-case` — rc=0
    output: token-set token-set/tracking-and-case — h1 is the only tight voice: sentence case, −0.035em. The caps voice (uppercase + 0.35em + weight 900) runs h2–h6, the wordmark, nav and buttons. Excep…
    Why + conclusion: token-set/tracking-and-case: h1 sentence case −0.035em; the caps voice runs h2–h6/wordmark/nav/buttons; labels and menu links stay 300; case is CSS-authored.

35. `./run-authority inspect token-set/surfaces` — rc=0
    output: token-set token-set/surfaces — Grounds: white #ffffff (default), #fbfbfb (project pages via the shared per-page style block), footer #f6f6f6. Panels: menu #3ef900 (lime), code #315d…
    Why + conclusion: token-set/surfaces: grounds, panel colours, tile veils (rest α0 → hover #eb84da opaque), zebra and #c9c9c9 lines.

36. `./run-authority inspect guideline/typography-voices` — rc=0
    output: guideline guideline/typography-voices — One family renders in three voices: 300 light sentence-case body (the working voice), 700 tight-tracked h1, and 900 uppercase tracked caps for h2–h6, …
    Why + conclusion: guideline/typography-voices: 300/700/900 only — no 400, no italics (em/blockquote synthetic oblique). Governs the local font shipment.

37. `./run-authority inspect layout/page-shell` — rc=0
    output: layout layout/page-shell — Every page: #wrapper > header#header (static, 8em top pad; logo left; fixed 64×48 Menu pill top-right) + nav#menu (fixed slide-in; 22em, 16.5em ≤736) …
    Why + conclusion: layout/page-shell: #wrapper > header + nav#menu + #main>.inner (68em; 2.5em→1.25em ≤736) + footer; 1008px content @1280, 350px @390; header 8em pad; main pad-bottom 6em.

38. `./run-authority inspect layout/header` — rc=0
    output: layout layout/header — Static top block (8em pad; 4em ≤736); logo left = 2em symbol + tracked-caps wordmark; a single Menu control fixed top-right (right 2em/top 2em) as a 6…
    Why + conclusion: layout/header: logo left (2em symbol + tracked-caps wordmark); fixed 64×48 Menu pill right 2em/top 2em, radius 4px kept; header never fades.

39. `./run-authority inspect component/menu-panel` — rc=0
    output: component component/menu-panel — Slide-in nav: 22em (352px) fixed right, full height, ground #3ef900 lime (override of the template's #585858) with black text; inner padding 2.75em; h…
    Why + conclusion: component/menu-panel: lime #3ef900 slide-in 22em/16.5em, inner 2.75em, black links 1em 0, separators rgba(255,255,255,.15), #wrapper dimmed to .25, X 6em left grey→pink.

40. `./run-authority inspect component/tiles` — rc=0
    output: component component/tiles — Responsive image grid (3-up at 1280, 322×322px tiles; 1-up at 390). Image radius flattened to 0. Rest veils mostly alpha-0 (#efc5e900, #ffe2e500; fain…
    Why + conclusion: component/tiles: 3-up@1280 322px / 1-up@390, radius 0; hover = opaque flat #eb84da veil + white caption, no zoom; recorded flaws noted (caption 2.37:1).

41. `./run-authority gap-add --need 'a documentation catalogue section: every recorded artifact presented grouped by kind, each with a title and a one-line summary' --context 'built under phantom for a docs page presenting the authority itself; resolve returned UNDEFINED for this need; improvisation composed from component/tiles grid + token-set values, marked in markup' --scope doc-page` — rc=1
    output: json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)  [stderr] json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
    Why + conclusion: gap-add with a plain-text --context failed (rc=1, expects JSON) — retry queued; the failure is kept on the record.

42. `./run-authority gap-add --need 'a specification summary section: recorded rules and prohibitions presented as scannable lists with a couple of verbatim quotes' --context 'docs page under phantom; resolve returned UNDEFINED; composition drawn from component/lists typography and token-set/type-scale, improvement marked in markup' --scope doc-page` — rc=1
    output: json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)  [stderr] json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
    Why + conclusion: Second gap-add failed the same way (JSON context) — retried next.

43. `./run-authority gap-add --need 'a documentation catalogue section: every recorded artifact presented grouped by kind, each with a title and a one-line summary' --context '{"page":"index.html","resolution":"UNDEFINED","composition":"component/tiles grid treatment + token-set values","marking":"data-improv attrs + HTML comments"}' --scope doc-page` — rc=0
    output: {"id": "gap/20261008-164947-c1ef70", "need": "a documentation catalogue section: every recorded artifact presented grouped by kind, each with a title and a one-…
    Why + conclusion: Gap 1 filed: gap/20261008-164947-c1ef70 — documentation catalogue section (UNDEFINED), composition recorded in its context.

44. `./run-authority gap-add --need 'a specification summary section: recorded rules and prohibitions presented as scannable lists with a couple of verbatim quotes' --context '{"page":"index.html","resolution":"UNDEFINED","composition":"typography from token-set/type-scale + guideline/typography-voices","marking":"data-improv attrs + HTML comments"}' --scope doc-page` — rc=0
    output: {"id": "gap/20261008-164947-e2b44f", "need": "a specification summary section: recorded rules and prohibitions presented as scannable lists with a couple of ver…
    Why + conclusion: Gap 2 filed: gap/20261008-164947-e2b44f — specification summary section (UNDEFINED), composition recorded.

45. `./run-authority resolve 'a data table
a checkbox
an ink-ring button' --json` — rc=0
    output: outcome=RESOLVED → component/table
    Why + conclusion: Newline-separated problems still join into one — resolve is strictly one problem per call. (Landed on component/table, incidentally a useful summary.)

46. `./run-authority inspect token-set/breakpoints` — rc=0
    output: token-set token-set/breakpoints — Template breakpoint set: xlarge 1281–1680, large 981–1280, medium 737–980, small 481–736, xsmall 361–480, xxsmall ≤360. CSS queries at 1280/980/736/48…
    Why + conclusion: token-set/breakpoints: xlarge 1281–1680 … xxsmall ≤360; queries at 1280/980/736/480/360 drive gutters, header pad, menu width, nav offset, tile columns.

47. `./run-authority inspect all` — rc=1
    output: unknown id: all  [stderr] unknown id: all
    Why + conclusion: inspect 'all' is not a listing id — 'unknown id'.

48. `./run-authority inspect component` — rc=1
    output: unknown id: component  [stderr] unknown id: component
    Why + conclusion: inspect 'component' likewise unknown — no kind-level dump exists.

49. `./run-authority inspect '*'` — rc=1
    output: unknown id: *  [stderr] unknown id: *
    Why + conclusion: inspect '*' unknown as well — enumeration via inspect is impossible; keyword search + per-id inspect it is.

50. `./run-authority discover 'component lists button'` — rc=4
    output: build it: python3 tools/da_sem.py build --pack /home/xrim/design-authority/packs/phantom  [stderr] build it: python3 tools/da_sem.py build --pack /home/xrim/design-authority/packs/phantom
    Why + conclusion: discover is unavailable (semantic index not built) — no richer retrieval surface.

51. `./run-authority inspect component/lists` — rc=0
    output: component component/lists — Unordered lists with disc marks and 2em spacing; ul.alt drops marks; ol uses decimal counters; li item spacing 2em. Content primitives — they inherit …
    Why + conclusion: component/lists: disc marks, 2em spacing, ul.alt drops marks — the spec rows use ul.alt with #c9c9c9 rules.

52. `./run-authority inspect layout/footer` — rc=0
    output: layout layout/footer — Grey #f6f6f6 ground, padding 5em 0 6em; flex .inner: contact block (~66%; underline form + Send on elements/generic/publication; index swaps the form …
    Why + conclusion: layout/footer: #f6f6f6, padding 5em 0 6em; flex contact (~66%) + follow (~33%) + copyright bar (0.8em, rgba(88,88,88,.5)≈2.23:1).

53. `./run-authority inspect component/action-button` — rc=0
    output: component component/action-button — Uppercase 900 label at 0.8em with 0.35em tracking, 44.8px tall, radius 4px (NOT flattened); default = transparent ground with a 2px ink ring (inset 0 …
    Why + conclusion: component/action-button: uppercase 900 0.8em/+0.35em, 3.5em tall, radius 4px kept; inset ink ring #585858 → hover #f2849e; primary/active values captured.

54. `./run-authority inspect component/blockquote` — rc=0
    output: component component/blockquote — Italic pull-quote (synthetic oblique — no italic face) with a 4px #c9c9c9 left rule, padding 0.5em 0 0.5em 2em, no quotation marks; text colour inheri…
    Why + conclusion: component/blockquote: synthetic-oblique pull quote, 4px #c9c9c9 left rule, 0.5em/2em padding, no quotation marks — the verbatim-quote component.

55. `./run-authority inspect layout/page-intro` — rc=0
    output: layout layout/page-intro — The only authored motion: body.is-preload disables all animation/transition (!important) and holds .tiles article at scale(0.9)/opacity 0; main.js rem…
    Why + conclusion: layout/page-intro: is-preload holds tiles at scale(.9)/0 with all transition disabled; class dropped 100ms after load; .5s ease ramp; header never animates; noscript lifts it.

56. `./run-authority search 'site tiles' --limit 4` — rc=0
    output: 5.0  component    component/tiles              Tiles (project grid; deployed hover = flat pink veil, no zoom) …
    Why + conclusion: Text-mode search (no --json) shows the same fields — no summaries in any search surface. Catalogue strategy fixed: 15 inspected summaries verbatim + cross-referenced lines for the rest.

57. `./run-authority search table --limit 2` — rc=0
    output: 9.0  component    component/table              Table (900 head, 2px rules, tinted odd rows) …
    Why + conclusion: Second text-mode check confirms it. Enumeration and fetching are done; building begins.
