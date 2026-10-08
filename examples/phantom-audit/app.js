/* phantom-audit app.js (v2, redo)
   Console behaviour + audit data, pass 2: the authority is the site's DEPLOYED
   language (packs/phantom 0.2.0). Console parts (chips, ledger chrome, panel,
   filters, demos, evidence gallery) are marked improvisations; the reviewed
   system lives in assets/css/main.css (derived verbatim from the deployment). */

/* ============================== DATA ================================== */

const ARTIFACTS = [
  {id: "token-set/colour", title: "Colour — deployed ink", group: "Foundations", place: "override",
   note: "Pink reading ink #ff6bbc (body/heads/footer/forms, 2.6:1 — measured); links neon green #6bff2c on a dotted blue #20a3f5 underline with pink #f2849e hover; code sits on solid blue rgba(46,90,249,.986) in pink; menu lime #3ef900 with black text; labels purple #8833e3; checks red #f51616. Template grey #585858 survives in buttons and table rules.",
   demo: `<div style="display:flex;flex-wrap:wrap;gap:0.6em;">
     <div><div style="width:3.2em;height:3.2em;background:#ff6bbc;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#ff6bbc — ink</p></div>
     <div><div style="width:3.2em;height:3.2em;background:#6bff2c;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#6bff2c — links</p></div>
     <div><div style="width:3.2em;height:3.2em;background:#20a3f5;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#20a3f5 — underline</p></div>
     <div><div style="width:3.2em;height:3.2em;background:#315df9;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">code blue</p></div>
     <div><div style="width:3.2em;height:3.2em;background:#3ef900;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#3ef900 — menu</p></div>
     <div><div style="width:3.2em;height:3.2em;background:#8833e3;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#8833e3 — labels</p></div>
     <div><div style="width:3.2em;height:3.2em;background:#f51616;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#f51616 — checks</p></div>
     <div><div style="width:3.2em;height:3.2em;background:#585858;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#585858 — base ink</p></div>
   </div>`},
  {id: "token-set/surfaces", title: "Surfaces — grounds, tints, panels", group: "Foundations", place: "mixed",
   note: "White grounds default; #fbfbfb on project pages; footer #f6f6f6; menu panel #3ef900; code ground #315df9 composite. Tile veils: mostly alpha-0 at rest; hover = opaque #eb84da. Zebra rgba(144,144,144,.075); lines #c9c9c9.",
   demo: `<div style="display:flex;flex-wrap:wrap;gap:0.6em;">
     <div><div style="width:3.2em;height:3.2em;background:#fff;border:1px solid #c9c9c9;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#fff</p></div>
     <div><div style="width:3.2em;height:3.2em;background:#fbfbfb;border:1px solid #c9c9c9;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#fbfbfb</p></div>
     <div><div style="width:3.2em;height:3.2em;background:#f6f6f6;border:1px solid #c9c9c9;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#f6f6f6</p></div>
     <div><div style="width:3.2em;height:3.2em;background:#3ef900;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">menu</p></div>
     <div><div style="width:3.2em;height:3.2em;background:#eb84da;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">tile hover</p></div>
   </div>`},
  {id: "token-set/type-scale", title: "Type scale — deployed", group: "Type", place: "base",
   note: "Body 12pt=16px (18.67px ≤1680, 21.33px above); h1 2.75em/700/−0.035em sentence case; h2 1.1em/900 caps +0.35em; h3 1em/900; h4 0.8em/900; buttons 0.8em/900; table heads 0.9em/900 mixed case; code Courier New 0.9em. Line-height 1.75.",
   demo: `<h2>Heading two · tracked caps</h2><h3>Heading three</h3><p>Body copy in Source Sans Pro light (300) — the working voice. <code>code samples</code> sit on the blue chip.</p>`},
  {id: "token-set/tracking-and-case", title: "Case & tracking voice", group: "Type", place: "base",
   note: "h1 sentence case −0.035em (the only tight voice); uppercase +0.35em + 900 runs h2–h4, wordmark, nav, buttons. Measured exceptions: table heads (900, mixed case), labels/menu links (300, no tracking)."},
  {id: "token-set/text-measure-and-leading", title: "Measure & leading", group: "Type", place: "base",
   note: "Leading 1.75 throughout. Column 68em — ≈150 characters per line at 16px Light (1008px @1280; ≈53ch at 390). Long measure, kept as-is and noted."},
  {id: "token-set/breakpoints", title: "Breakpoints", group: "Foundations", place: "base",
   note: "xlarge 1281–1680 / large 981–1280 / medium 737–980 / small 481–736 / xsmall 361–480 / xxsmall ≤360. Gutters 2.5em→1.25em, header 8em→4em, menu 22em→16.5em at ≤736; tiles 3-up→1-up."},
  {id: "guideline/typography-voices", title: "Typography — three voices, one family", group: "Type", place: "base",
   note: "Source Sans Pro 300/700/900 via the Google-Fonts import (no 400, no italics — em/blockquote render as synthetic oblique). Light body, tight h1, tracked caps display.",
   demo: `<h1 style="margin-bottom:0.2em;">Sentence-case display</h1><h2>TRACKED CAPS DISPLAY</h2><p>Light body, <strong>900 strong</strong>, <em>synthetic italic</em>.</p>`},
  {id: "component/action-button", title: "Button — ink ring, pink hover", group: "Actions", place: "base",
   note: "Radius 4px kept in the flattening; transparent ground + 2px ink ring; hover flips label + ring to #f2849e; primary solid #585858 white label.",
   demo: `<ul class="actions"><li><button type="button" class="button primary">Primary</button></li><li><button type="button" class="button">Default</button></li><li><button type="button" class="button small">Small</button></li></ul>`},
  {id: "component/field", title: "Field — underline input", group: "Form", place: "override",
   note: "White ground, no box, radius 0, 1px #c9c9c9 bottom line, 48px tall; focus = 2px pink underline. Value text renders in ink pink.",
   demo: `<div class="fields"><div class="field half"><input type="text" placeholder="Name" /></div><div class="field half"><input type="email" placeholder="Email" /></div></div>`},
  {id: "component/select", title: "Select — underline + chevron", group: "Form", place: "base",
   note: "Native select in the field language: radius 0, bottom line, SVG chevron #c9c9c9; focus = pink underline.",
   demo: `<select><option>— Category —</option><option>Installation</option><option>Game</option><option>Framework</option></select>`},
  {id: "component/checkbox-radio", title: "Checkbox & radio — red fill, purple labels", group: "Form", place: "override",
   note: "Checked = #f51616 fill, #f82121 border, white checkmark — the shared rule puts the checkmark inside the radio too (no dot state). Labels purple #8833e3. Checkbox radius flattened to 0; radio stays a circle.",
   demo: `<div><input type="checkbox" id="demo-cb" checked /><label for="demo-cb">Consent</label></div><div><input type="radio" id="demo-r1" name="demo-r" checked /><label for="demo-r1">One</label><input type="radio" id="demo-r2" name="demo-r" /><label for="demo-r2">Two</label></div>`},
  {id: "component/actions", title: "Actions row", group: "Actions", place: "base",
   note: "ul.actions — the standard cluster for buttons in footer/hero blocks.",
   demo: `<ul class="actions"><li><button type="button" class="button primary">Send</button></li><li><button type="button" class="button">Reset</button></li></ul>`},
  {id: "component/table", title: "Table — 900 head, tinted rows", group: "Content", place: "base",
   note: "Heads 0.9em/900 mixed case; 2px #c9c9c9 rules on thead/tfoot; 1px row rules; odd rows rgba(144,144,144,.075). The .table-wrapper scroll rule is dead on the deployment (G17).",
   demo: `<div class="table-wrapper"><table><thead><tr><th>Name</th><th>Year</th></tr></thead><tbody><tr><td>ILightUUp</td><td>2024</td></tr><tr><td>Tame</td><td>2024</td></tr><tr><td>FAFA</td><td>2023</td></tr></tbody></table></div>`},
  {id: "component/tiles", title: "Tiles — pink-veil hover, no zoom", group: "Content", place: "override",
   note: "Image radius flattened to 0; hover paints the opaque #eb84da veil (photo fully hidden, 97.6% of the tile measured) and fades the white caption in (2.37:1); transform stays scale(1) — the template's zoom was removed. Try hovering the demo.",
   demo: `<section class="tiles" style="margin:0;"><article class="style1"><span class="image"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect width='400' height='300' fill='%23e9e9e9'/%3E%3Cpath d='M0 300L400 0M-40 300L360 0M40 300L400 40' stroke='%23d4d4d4' stroke-width='2'/%3E%3C/svg%3E" alt="Placeholder tile" /></span><a href="#system"><h2>ILightUUp</h2><div class="content"><p>Light drives the emergent narrative.</p></div></a></article><article class="style2"><span class="image"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect width='400' height='300' fill='%23ececec'/%3E%3Cpath d='M0 300L400 0M-40 300L360 0' stroke='%23d8d8d8' stroke-width='2'/%3E%3C/svg%3E" alt="Placeholder tile" /></span><a href="#system"><h2>Tame</h2><div class="content"><p>Affection in VR.</p></div></a></article><article class="style6"><span class="image"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect width='400' height='300' fill='%23eaeaea'/%3E%3Cpath d='M0 300L400 0M40 300L400 40' stroke='%23d6d6d6' stroke-width='2'/%3E%3C/svg%3E" alt="Placeholder tile" /></span><a href="#system"><h2>FAFA</h2><div class="content"><p>A plant-based virus attacking AI systems.</p></div></a></article></section>`},
  {id: "component/icon-row", title: "Icon chips — square, pink glyph", group: "Content", place: "override",
   note: "Square chips (radius flattened 4→0), 1px #c9c9c9 border, glyph inherits pink; hover = #f2849e glyph + border. style1 bare icons take the link green.",
   demo: `<ul class="icons"><li><a href="#system" class="icon brands style2 fa-github"></a></li><li><a href="#system" class="icon brands style2 fa-instagram"></a></li><li><a href="#system" class="icon solid style2 fa-envelope"></a></li><li><a href="#system" class="icon solid style2 fa-book"></a></li></ul>`},
  {id: "component/emblem-logo", title: "Emblem & wordmark", group: "Header", place: "mixed",
   note: "Round logo.svg at 2em + 900 tracked-caps wordmark in the page ink. Four wordmark variants ship across the site (G12); the 圳 glyph has no declared CJK font (G39).",
   demo: `<div class="preview" style="display:flex;align-items:center;gap:0.8em;"><span style="display:inline-flex;width:2.6em;height:2.6em;border:2px solid #585858;border-radius:100%;align-items:center;justify-content:center;font-weight:700;">◔</span><span style="font-weight:700;letter-spacing:0.28em;text-transform:uppercase;font-size:0.85em;">Zhen Wu Yoyo <span style="font-family:serif;">圳</span></span></div>`},
  {id: "component/nav-hamburger", title: "Nav trigger — hamburger plate", group: "Header", place: "base",
   note: "Fixed 64×48 plate, white-50% (invisible on white — G06), radius 4px; grey lines → pink on hover; label hidden, no aria-label.",
   demo: `<p class="muted" style="font-size:0.82em;">The real trigger is fixed top-right of this page — hover it. The plate is the deployed one.</p>`},
  {id: "component/menu-panel", title: "Menu panel — neon green slide-in", group: "Navigation", place: "override",
   note: "352px fixed rail #3ef900 with black links (14.76:1); page dims to 25%; close × inherited the link green and sits over the dimmed page (G04). Separators remain white-15% on lime (G05).",
   demo: `<button type="button" class="button small" id="demoOpenMenu">Open the real menu ↗</button>`},
  {id: "component/carousel-gallery", title: "Carousel — autoplay, broken sources", group: "Content", place: "override",
   note: "640×360 fixed frame, 4s autoplay, no controls; all six image sources 404 (G26). The repair dossier is candidate/carousel (see Adaptations).",
   demo: `<div class="car"><div class="frame" style="height:8em;">IMAGE SOURCES 404 — BROKEN IN PRODUCTION</div></div>`},
  {id: "component/blockquote", title: "Blockquote", group: "Content", place: "base",
   note: "Italic (synthetic) pull-quote with a 4px #c9c9c9 left rule; inherits the page ink.",
   demo: `<blockquote>Playful interaction, sensorial interfaces, emergent art — the site's own words for its research.</blockquote>`},
  {id: "component/code-pre", title: "Code — blue chip, pink text", group: "Content", place: "override",
   note: "Inline code on solid rgba(46,90,249,.986) with pink text (1.99:1 — G03); radius 4px kept; pre stays transparent with horizontal scroll (clips at 390).",
   demo: `<p>Inline <code>tick-until-done</code> and a block:</p><pre><code>i = 0\nwhile (!deck.isInOrder()):\n    deck.shuffle()\n    i += 1</code></pre>`},
  {id: "component/hr", title: "Horizontal rule", group: "Content", place: "base",
   note: "1px #c9c9c9 rule, 2em margins.", demo: `<hr />`},
  {id: "component/lists", title: "Lists", group: "Content", place: "base",
   note: "Disc lists, alt lists, ordered lists — inherit the page ink.",
   demo: `<ul><li>Dolor pulvinar etiam.</li><li>Sagittis adipiscing.</li></ul><ul class="alt"><li>Dolor pulvinar etiam.</li><li>Felis enim feugiat.</li></ul>`},
  {id: "component/image", title: "Image treatments", group: "Content", place: "mixed",
   note: ".image.main full-column (radius flattened to 0), .fit content width, .left/.right floats. Project galleries use the .image1 float alternation (candidate/project-gallery). Inline px widths overflow mobile (G29).",
   demo: `<span class="image main" style="margin-bottom:0;"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1000' height='300'%3E%3Crect width='1000' height='300' fill='%23e9e9e9'/%3E%3Cpath d='M0 300L1000 0M-60 300L940 0M60 300L1000 60' stroke='%23d2d2d2' stroke-width='3'/%3E%3C/svg%3E" alt="Placeholder image" /></span>`},
  {id: "layout/page-shell", title: "Page shell", group: "Layout", place: "base",
   note: "Header (logo + fixed Menu pill) → slide-in menu → 68em main column → optional footer. Footer renders on only 4 of 9 pages (G30-adjacent: commented out on the project pages)."},
  {id: "layout/header", title: "Header — no load animation", group: "Layout", place: "base",
   note: "Static 8em top block; logo left, fixed Menu pill right. Measured: header opacity stays 1 during preload — pass-1's '\"header fades\" claim was wrong; corrected in the authority.'",
   demo: `<div class="preview" style="display:flex;align-items:center;gap:0.8em;"><span style="font-weight:700;letter-spacing:0.28em;text-transform:uppercase;font-size:0.85em;">Wordmark</span><span style="margin-left:auto;font-size:0.7em;font-weight:900;letter-spacing:0.28em;text-transform:uppercase;">Menu ☰</span></div>`},
  {id: "layout/footer", title: "Footer — present on 4 of 9 pages", group: "Layout", place: "mixed",
   note: "Grey ground, contact + follow sections (index swaps the form for a plain email line), copyright bar (2.23:1 — G11). Commented out on all four project pages; absent on email.",
   demo: `<div class="preview" style="background:#f6f6f6;"><p style="margin:0; font-size:0.8em;"><strong>Get in touch</strong> · zwuch@connect.ust.hk<br><span style="opacity:.6;">Follow — icon chips row</span></p></div>`},
  {id: "layout/page-intro", title: "Load-in motion — tiles only", group: "Layout", place: "base",
   note: "is-preload holds tiles at scale(0.9)/opacity 0; class drops 100ms after load; ramp ≈350ms. Nothing else animates — header stays opaque (corrects pass 1).",
   demo: `<button type="button" class="button small" id="demoReplay">Replay the load-in ↻</button>`},
  {id: "layout/project-page", title: "Project-detail composition", group: "Layout", place: "override",
   note: "h1 with per-page inline colour + hero + freeform blocks; identical style block on all four pages; fixed px widths overflow mobile (G29); bilibili embeds 800×450.",
   demo: `<ul class="actions"><li><a href="#adaptations" class="button small">See the responsive fix (AD4)</a></li></ul>`},
];

const GAPS = [
  /* SYSTEM — measured risks inside the language */
  {id:"G01", cat:"system", sev:"warning", fw:"candidate", ev:"colour-index-1280.png",
   title:"Pink reading ink measures 2.60:1 on white", ref:"computed probes; colour-elements/colour-index captures",
   detail:"The deployed ink #ff6bbc fails AA for all text sizes (2.6:1). This is canon, not an error — the ledger records the measurement and the pathway: the AA strategy is the promotion bar of candidate/text-as-accent.",
   links:["candidate:text-as-accent","precedent:pink-ink-canonised","adapt:AD1"]},
  {id:"G02", cat:"system", sev:"warning", fw:"candidate", ev:"colour-light-1280.png",
   title:"Link green measures 1.32:1 — the dotted underline is the only cue", ref:"computed probes (border-bottom #20a3f5)",
   detail:"#6bff2c on white 1.32:1, on #fbfbfb 1.27:1. The 1px dotted blue underline (2.76:1) is what makes links findable. Same AA dossier as G01.",
   links:["candidate:text-as-accent","adapt:AD1"]},
  {id:"G03", cat:"system", sev:"warning", fw:"candidate", ev:"colour-elements-1280.png",
   title:"Code text pink-on-blue measures 1.99:1", ref:"pixel histogram + computed (ground rgba(46,90,249,.986))",
   detail:"A solid royal-blue ground with pink text — a reading surface inside body copy at 1.99:1. The dossier proposes either a darker ground with white text or pink text kept only above a size threshold.",
   links:["candidate:text-as-accent","adapt:AD1"]},
  {id:"G04", cat:"system", sev:"warning", fw:"normalise", ev:"colour-elements-1280-menu-open.png",
   title:"Menu close × inherited link green and sits off-panel", ref:"computed: #6bff2c × at left:-6em; 1.32:1 on the page (1.08:1 against the panel)",
   detail:"The template drew a grey × on the panel; the recolour left it green over the dimmed page — near-invisible either way it lands. Normalise: keep the × white-on-lime or ink-on-page, positioned on the panel.",
   links:[]},
  {id:"G05", cat:"system", sev:"info", fw:"normalise",
   title:"Menu separators are white-15% on lime", ref:"computed border-top rgba(255,255,255,.15); separation ≈1.2:1",
   detail:"Template lines tuned for a dark panel, kept on the lime one. Swap to a lime-darkened rule or the base ink at low alpha.",
   links:[]},
  {id:"G06", cat:"system", sev:"warning", fw:"normalise",
   title:"Hamburger plate is white-50% on a white page (no label, no aria-label)", ref:"computed; layout-index-1280 capture",
   detail:"Only the three grey lines identify the control; the plate itself is invisible. Add a visible affordance (line weight or a hairline ring) and an accessible name.",
   links:[]},
  {id:"G07", cat:"system", sev:"info", fw:"note",
   title:"Disabled buttons render at opacity .25 — near-invisible", ref:"computed (opacity .25, pointer-events none)",
   detail:"A disabled state should read as 'off', not as 'missing'. Raise to a legible-off tone.",
   links:[]},
  {id:"G08", cat:"system", sev:"warning", fw:"normalise", ev:"comp-index-tile-hover-1280.png",
   title:"Tile hover hides the work: opaque veil, 2.37:1 caption", ref:"pixel histogram (97.6% flat #eb84da); white caption on veil",
   detail:"Hovering a tile fully covers the photo with flat pink; the caption is the only content and sits at 2.37:1. Either drop the veil alpha so the image reads through, or commit to caption-first hover with a readable veil/text pairing.",
   links:["candidate:text-as-accent","adapt:AD1"]},
  {id:"G09", cat:"system", sev:"info", fw:"defect",
   title:"Four of six tile veils have alpha 0 (#efc5e900, #ffe2e500)", ref:"computed pseudo-element probes",
   detail:"'Pastel + trailing alpha' edits whose alpha digit landed at 00 — the styles read as 'no veil'. Restore intended alphas or delete the dead declarations.",
   links:[]},
  {id:"G10", cat:"system", sev:"warning", fw:"candidate",
   title:"Per-page h1 accents measure 1.92–2.51:1", ref:"computed: #71c3de 1.92, #ff8b80 2.19, #fd77af 2.41, #ff6bbc 2.51 on #fbfbfb",
   detail:"The per-page hues are part of the override system (P-R7); their contrast rides the same AA dossier.",
   links:["candidate:text-as-accent","precedent:pink-ink-canonised"]},
  {id:"G11", cat:"system", sev:"info", fw:"note",
   title:"Copyright line measures 2.23:1", ref:"rgba(88,88,88,.5) on #f6f6f6 (computed composite)",
   detail:"Small print at 12.8px in half-alpha ink. A full-alpha ink at the same size would pass and change nothing visually.",
   links:[]},
  {id:"G12", cat:"system", sev:"info", fw:"normalise",
   title:"Four wordmark variants across the site", ref:"'Zhen Wu YoYo 圳' / 'Phantom' / 'About Zhen' / 'Back to main'",
   detail:"One brand line, site-wide — the current drift includes the untouched template's 'Phantom'.",
   links:["adapt:AD6"]},
  /* CRAFT — markup and wiring defects */
  {id:"G13", cat:"craft", sev:"error", fw:"defect", ev:"layout-index-nesteddoctype-1280.png",
   title:"A whole document skeleton nested mid-body on index", ref:"index.html (source); parses to 2 meta + a second title in <header>",
   detail:"`<!DOCTYPE html><html><head>…</head><body></body></html>` sits inside the page body — invalid, and it renders as whitespace where a heading was meant.",
   links:["adapt:AD6"]},
  {id:"G14", cat:"craft", sev:"warning", fw:"defect",
   title:"Duplicated id=\"main\" on index", ref:"DOM count: 2 elements",
   detail:"Anchor and scripting targets become ambiguous. Rename the nested block's id.",
   links:[]},
  {id:"G15", cat:"craft", sev:"error", fw:"defect",
   title:"Broken title tag: Zhen's publication</S>", ref:"publication.html <title>",
   detail:"A stray closing tag leaks into the title bar verbatim. One-character fix.",
   links:[]},
  {id:"G16", cat:"craft", sev:"error", fw:"defect",
   title:"Dead rule: .table-wrapper scroll path (comment damage)", ref:"main.css Table block; computed overflow-x:visible",
   detail:"Deleting the /* */ markers left the bare word 'Table' before .table-wrapper, so the rule parses as a selector matching nothing. Wide tables lose their mobile scroll.",
   links:["adapt:AD6"]},
  {id:"G17", cat:"craft", sev:"info", fw:"defect",
   title:"Dead rule: .imagemain (5%×1%, unused by any page)", ref:"searched all 9 pages — no matches",
   detail:"Leftover from an edit; safe to remove.",
   links:[]},
  {id:"G18", cat:"craft", sev:"warning", fw:"defect",
   title:"Font Awesome loaded twice (bundled + CDN beta on index only)", ref:"index.html head vs. all other pages",
   detail:"Home and subpages resolve icons from different kits. Keep the bundled set everywhere (as this review does).",
   links:["adapt:AD6"]},
  {id:"G19", cat:"craft", sev:"warning", fw:"defect",
   title:"Stray </h1>, commented-out headings and a commented Chinese prose block on index", ref:"index.html source",
   detail:"Tidy churn from editing: uncomment or delete. The commented Chinese paragraphs are the only other Chinese on the site.",
   links:[]},
  {id:"G20", cat:"craft", sev:"warning", fw:"note",
   title:"light.html carries the FAFA blurb; 'Publication and Exhibition' repeats", ref:"light.html source vs. rendered h2 list",
   detail:"Copy-paste chain from the shared project template: the I Light U Up page describes FAFA in its blurb and lists the section twice (once commented).",
   links:[]},
  {id:"G21", cat:"craft", sev:"info", fw:"defect",
   title:"Video file is a 133-byte git-LFS pointer; iframes titled 'YouTube video player' for bilibili", ref:"light/ILightUUp1080p.mp4; iframe title attrs",
   detail:"The mp4 never plays (its <video> is commented out anyway); the embeds are bilibili with YouTube titles. Cosmetic-adjacent but misleading.",
   links:[]},
  {id:"G22", cat:"craft", sev:"info", fw:"note",
   title:"Comments contradict values (Chinese comments say 'black bg' / 'white text'; values are #fbfbfb / #000)", ref:"shared style block on 4 project pages",
   detail:"The comment set describes an earlier intent. Update comments with the values.",
   links:[]},
  /* ASSETS — files referenced but not served */
  {id:"G23", cat:"assets", sev:"error", fw:"candidate", ev:"comp-index-carousel-a-1280.png",
   title:"All six randomgallery/*.jpg carousel sources 404", ref:"serve log; img.naturalWidth=0 in both captured states",
   detail:"The homepage carousel has been showing the broken-image placeholder in production. Repair (or replace) via candidate/carousel — a working source pipeline, a static fallback, and a motion policy.",
   links:["candidate:carousel","adapt:AD3"]},
  {id:"G24", cat:"assets", sev:"warning", fw:"defect",
   title:"tame/emotion map.jpg 404 (broken placeholder mid-page)", ref:"serve log; layout-tame-390 capture",
   detail:"Referenced by the Tame project page — re-export or remove.",
   links:[]},
  {id:"G25", cat:"assets", sev:"warning", fw:"defect",
   title:"unlogical/BOOKLET-01 - Copy.jpg 404", ref:"serve log; layout-unlogical-390 capture",
   detail:"The filename (with ' - Copy') suggests a local-edits artifact that never shipped.",
   links:[]},
  {id:"G26", cat:"assets", sev:"error", fw:"candidate", ev:"layout-index-390.png",
   title:"Mobile overflow: documents reach 700–1020px wide at a 390px viewport", ref:"measured scrollWidth: index 700 · light 820 · tame/fafa 920 · unlogical 1020",
   detail:"Fixed inline px widths (200–1000px images, 800px iframes) push the layouts past every small screen. The project-gallery responsive policy (candidate/project-gallery) carries the fix.",
   links:["candidate:project-gallery","adapt:AD4"]},
  /* CONTENT — finishing passes */
  {id:"G27", cat:"content", sev:"warning", fw:"normalise",
   title:"Lorem ipsum survivors: stock menus on 7 pages, elements.html byte-identical to the template demo", ref:"DOM: 'Ipsum veroeros / Tempus etiam…'; elements diff vs upstream = empty",
   detail:"The menu contradicts itself across the site (her real set on index/publication; lorem elsewhere), and the 'Game, Design & Development Log' menu item points at an untouched demo page.",
   links:["adapt:AD6"]},
  {id:"G28", cat:"content", sev:"warning", fw:"note",
   title:"alt=\"\" on almost every image (light/tame repeat alt=\"Visual Design\")", ref:"DOM img inventory",
   detail:"Decorative-only assumption applied to content imagery. Content images need real alt text; true decoration keeps empty alt.",
   links:[]},
  {id:"G29", cat:"content", sev:"info", fw:"note",
   title:"No favicon, OG tags or meta description on any page", ref:"head inventory across 9 pages",
   detail:"Tabs and shared links show defaults. This review ships title+description as a baseline example.",
   links:[]},
  {id:"G30", cat:"content", sev:"info", fw:"note",
   title:"'la la la' copyright; © Untitled on the template pages", ref:"footer source on index vs elements/generic/publication",
   detail:"Placeholder copyright strings in production. 'la la la' at least is honest about being a placeholder.",
   links:["adapt:AD6"]},
  {id:"G31", cat:"content", sev:"info", fw:"note",
   title:"Email address is plain text (not a link); email page has no footer", ref:"email.html source",
   detail:"The one contact surface most portfolios optimise: a mailto link and a way back.",
   links:[]},
  {id:"G32", cat:"content", sev:"info", fw:"note",
   title:"'Short description' placeholder h1s remain as comments on the project pages", ref:"source L77/81 ×4 pages; carousel desc fields empty; captions repeat ILightUUp ×4 of 6",
   detail:"Content scaffolding pass: one real line per project, captions written per slide.",
   links:["adapt:AD6"]},
  /* PATTERNS — surfaces the template never defines */
  {id:"G33", cat:"pattern", sev:"warning", fw:"improvise",
   title:"Carousel has no canon: autoplay-only, no controls (showPrev unwired)", ref:"inline script; 'Buttons removed for automatic switching'",
   detail:"The template defines no carousel; the deployment hand-rolled one. The candidate dossier sets the promotion bar: working sources (G23), a motion policy, controls + position readout, static fallback.",
   links:["candidate:carousel","adapt:AD3"]},
  {id:"G34", cat:"pattern", sev:"warning", fw:"improvise",
   title:"Project-detail composition is genuinely undefined (generic.html reused for every tile)", ref:"4 unrelated project tiles all target generic.html",
   detail:"A portfolio needs project pages the template never defines. The dossier drafts the composition; this review improvises one in-character in Adaptations.",
   links:["candidate:project-gallery","adapt:AD5"]},
  {id:"G35", cat:"pattern", sev:"warning", fw:"improvise",
   title:"Mixed CN/EN typography has no declared stack (圳 falls to the OS)", ref:"CDP: WenQuanYi Zen Hei in this render; no CJK family anywhere",
   detail:"The wordmark pairs 900-weight Latin with an arbitrary OS CJK face, differently per visitor. A one-line stack + weight policy would stabilise it; filed as a gap until the owner decides the policy.",
   links:["fallback:cjk-system-fallback","adapt:AD2"]},
  {id:"G36", cat:"pattern", sev:"info", fw:"improvise",
   title:"No current-section mark in menus", ref:"stock menus identical on every page",
   detail:"Nothing says where you are. A small current-section mark is undefined by the template — this review improvises one for its own anchor menu (see Marks).",
   links:[]},
];

const ADAPTATIONS = [
  {id:"AD1", ladder:"candidate", title:"The pink-ink dossier — AA strategy on the table",
   body:"Pink reading ink is canon (the redo decision, recorded as precedent/pink-ink-canonised). What remains open — and what promotion requires — is an accessibility strategy. The numbers below are computed live from the measured values; the options are a role map (which roles may keep the ink), size/weight minimums, or sanctioned black-body pages (already in the system — see AD3).",
   demo:"aa", links:["candidate:text-as-accent","precedent:pink-ink-canonised","gap:G01","gap:G02","gap:G03"]},
  {id:"AD2", ladder:"improvised", title:"Mixed-script typography — the hands-off fallback, demonstrated",
   body:"The system declares no CJK face, so 圳 renders from the OS — differently on every visitor's machine, mismatched to the 900 Latin beside it. The fallback records the constraint; the gap asks the owner for a one-line stack decision. Shown below: the deployed render (serif fallback in this environment) next to the proposed stack.",
   demo:"cjk", links:["fallback:cjk-system-fallback","gap:G35"]},
  {id:"AD3", ladder:"candidate", title:"Carousel repair dossier — sources, policy, controls",
   body:"The deployed carousel is broken in production (six 404 sources) and has no motion policy. The dossier: re-source the images; decide autoplay vs static; add prev/next + a position readout; design the broken-source state. The controlled composition below is the target shape — try it.",
   demo:"carousel", links:["candidate:carousel","gap:G23","gap:G33"]},
  {id:"AD4", ladder:"candidate", title:"Project-gallery responsive fix — from fixed px to fluid",
   body:"The gallery composition (70% floats alternating) is consistent enough to canonise — once its widths survive small screens. The fix shown: replace inline px widths with max-width:100%/height:auto; the same before/after applies to the 800px embeds.",
   demo:"fluid", links:["candidate:project-gallery","gap:G26","gap:G34"]},
  {id:"AD5", ladder:"improvised", title:"Project-detail composition (undefined → marked)",
   body:"The template has no project page; every tile lands on generic.html. This is the review's in-character improvisation — heading, meta row, full-width image, body, back-link — marked in the DOM and covered by the project-gallery dossier.",
   demo:"project", links:["candidate:project-gallery","gap:G34"]},
  {id:"AD6", ladder:"normalise", title:"Handbook repairs — one menu, one wordmark, real strings",
   body:"Normalisation, not invention: her real navigation applied everywhere, one wordmark, copyright made real, placeholder copy scaffolded. Before/after from the ledger items.",
   demo:"content", links:["gap:G12","gap:G27","gap:G30","gap:G32"]},
];

const RECORDS = {
  "precedent/pink-ink-canonised": {title:"Pink/neon reading ink — canonised on redo", kind:"precedent",
   body:"Pass 1 declined the deployment's neon reading ink and canonicalised the template's grey. Pass 2 (owner-directed) reversed the frame: extract what the site IS. Decision: accepted — pink reading ink #ff6bbc is the system's ink; measured contrast failures are recorded as observations and bounded by prohibition/unreadable-accent-ink (do not extend past measured roles; pair with other affordances).",
   meta:"decision: accepted (reversal) · supersedes precedent/declined-neon-reading-ink"},
  "candidate:text-as-accent": {title:"Text-as-accent (pink ink identity) — dossier", kind:"candidate",
   body:"Canonised as observed; promotion asks for a role map (pink vs black per role), an AA strategy (size/weight minimums or darkened ground variants), and owner sign-off. The per-page black-body override already provides an AA path for content pages.",
   meta:"promote when: role map · AA strategy · owner sign-off"},
  "candidate/carousel": {title:"Carousel — repair & controls dossier", kind:"candidate",
   body:"Broken sources (G23), no motion policy (G33). Promote when: images re-sourced or broken-state designed · motion policy agreed (no autoplay, or pause/bounded) · control spec captured · static fallback defined.",
   meta:"component exists; promotion = repair + policy"},
  "candidate/project-gallery": {title:"Project gallery — promotion dossier", kind:"candidate",
   body:"The four project pages apply one consistent composition (identical style block, .image1 70% floats). Promote when: responsive width policy drafted (max-width/height:auto) · shared-block vs class migration decided · one page rebuilt as reference.",
   meta:"pattern in place; promotion = responsive policy"},
  "fallback:cjk-system-fallback": {title:"CJK falls to the OS (no stack declared)", kind:"fallback",
   body:"No CJK family is declared; 圳 renders from the OS (observed: WenQuanYi Zen Hei in this render). Rendering differs per visitor OS. A declared stack + weight match is a new decision — filed as a gap (G35).",
   meta:"scope: chinese · cjk · mixed script"},
};

const EVIDENCE = [
  {file:"colour-index-1280.png", tag:"colour", label:"index @1280", caption:"The deployed default: pink reading ink on white; pink tracked-caps heads."},
  {file:"colour-elements-1280.png", tag:"colour", label:"elements @1280", caption:"The component set in situ: blue code chips, red checks, purple labels, grey buttons."},
  {file:"colour-light-1280.png", tag:"colour", label:"light @1280", caption:"Per-page override: black body on #fbfbfb with a pink h1; green links."},
  {file:"colour-elements-1280-menu-open.png", tag:"colour", label:"menu open @1280", caption:"The lime #3ef900 rail with black text over the dimmed page."},
  {file:"type-index-heading-1280.png", tag:"type", label:"wordmark @1280", caption:"The 900 tracked-caps wordmark — and 圳 falling to the OS font."},
  {file:"comp-elements-btn-hover-1280.png", tag:"component", label:"button hover", caption:"Default button mid-hover: label + ring flip to #f2849e."},
  {file:"comp-elements-field-focus-1280.png", tag:"component", label:"field focus", caption:"Focused field: the 2px pink underline replaces the grey line."},
  {file:"comp-elements-form-1280.png", tag:"component", label:"form @1280", caption:"Checked marks: red fill, white checkmark (radio too); purple labels."},
  {file:"comp-elements-table-1280.png", tag:"component", label:"table @1280", caption:"900-weight mixed-case heads, 2px rules, tinted odd rows."},
  {file:"comp-index-tile-hover-1280.png", tag:"component", label:"tile hover", caption:"The opaque #eb84da veil: the photograph disappears under flat pink."},
  {file:"comp-index-carousel-a-1280.png", tag:"component", label:"carousel state A", caption:"The autoplay carousel — all six image sources 404 in production."},
  {file:"layout-index-nesteddoctype-1280.png", tag:"layout", label:"nested doctype", caption:"A whole document skeleton nested mid-body on index (renders as whitespace)."},
  {file:"layout-index-390.png", tag:"layout", label:"index @390", caption:"Mobile overflow: document is 700px wide at a 390px viewport."},
  {file:"layout-publication-1280.png", tag:"layout", label:"publication @1280", caption:"The .publication class: black main text while the shell stays pink."},
];

/* ========================== CONSOLE HELPERS =========================== */

const $ = (s, r) => (r || document).querySelector(s);
const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const IMP = 'data-improvised data-mk="console kit"';

function chip(kind, text) {
  return '<span class="chip chip--' + kind + '" ' + IMP + ">" + esc(text) + "</span>";
}
const PLACE_CHIP = { "base": ["base", "base value"], "override": ["override", "deployed override"], "mixed": ["canon", "mixed"], "in-system": ["canon", "canon"] };

const panel = $("#panel"), panelTitle = $("#panelTitle"), panelId = $("#panelId"), panelBody = $("#panelBody");

function openPanel(kind, id) {
  let title = "", sub = "", body = "";
  if (kind === "artifact") {
    const a = ARTIFACTS.find((x) => x.id === id); if (!a) return;
    title = a.title; sub = a.id + " · " + a.group;
    body = '<div class="kv"><b>Deployed record</b><p>' + esc(a.note) + "</p></div>" +
      '<div class="kv"><b>Posture</b><p>' + chip(PLACE_CHIP[a.place][0], PLACE_CHIP[a.place][1]) + "</p></div>" +
      '<div class="kv"><b>Authority</b><p><code>' + esc("packs/phantom 0.2.0 · " + a.id) + "</code></p></div>" +
      (a.demo ? '<div class="kv"><b>Live demo</b><div class="demo">' + a.demo + "</div></div>" : "");
  } else if (kind === "gap") {
    const g = GAPS.find((x) => x.id === id); if (!g) return;
    title = g.title; sub = g.id + " · " + g.cat + " · " + g.sev;
    body = '<div class="kv"><b>Evidence</b><p><code>' + esc(g.ref) + "</code></p></div>" +
      '<div class="kv"><b>What this is</b><p>' + esc(g.detail) + "</p></div>" +
      '<div class="kv"><b>Pathway</b><p>' + chip(g.fw === "candidate" ? "candidate" : g.fw === "defect" ? "defect" : g.fw === "improvise" ? "improv" : g.fw === "normalise" ? "canon" : "gap", g.fw) + "</p></div>" +
      (g.ev ? '<div class="kv"><b>Screen</b><p><a href="assets/evidence/' + g.ev + '" target="_blank" rel="noopener">' + g.ev + "</a></p></div>" : "") +
      (g.links && g.links.length ? '<div class="kv"><b>Records</b><p>' + g.links.map(linkBtn).join(" ") + "</p></div>" : "");
  } else if (kind === "adapt") {
    const a = ADAPTATIONS.find((x) => x.id === id); if (!a) return;
    title = a.title; sub = a.id + " · " + a.ladder;
    body = '<div class="kv"><b>Why</b><p>' + esc(a.body) + "</p></div>" +
      '<div class="kv"><b>Records</b><p>' + a.links.map(linkBtn).join(" ") + "</p></div>";
  } else if (kind === "record") {
    const r = RECORDS[id]; if (!r) return;
    title = r.title; sub = id;
    body = '<div class="kv"><b>' + esc(r.kind) + '</b><p>' + esc(r.body) + "</p></div>" +
      '<div class="kv"><b>Meta</b><p><code>' + esc(r.meta) + "</code></p></div>";
  }
  panelTitle.textContent = title;
  panelId.textContent = sub;
  panelBody.innerHTML = body;
  panel.hidden = false;
  bindPanelLinks();
}

function linkBtn(l) {
  const ix = l.indexOf(":");
  const kind = l.slice(0, ix), id = l.slice(ix + 1);
  const label = kind === "adapt" ? "adaptation " + id : kind === "record" ? id : id;
  return '<button type="button" class="button small" data-open="' + (kind === "candidate" || kind === "precedent" || kind === "fallback" ? "record:" : kind + ":") + id + '" ' + IMP + ">" + esc(label) + "</button>";
}

function bindPanelLinks() {
  $$("[data-open]", panelBody).forEach((b) => b.addEventListener("click", () => {
    const ix = b.getAttribute("data-open").indexOf(":");
    openPanel(b.getAttribute("data-open").slice(0, ix), b.getAttribute("data-open").slice(ix + 1));
  }));
}
$("#panelClose").addEventListener("click", () => { panel.hidden = true; });

/* --------------------------- system cards ------------------------------ */
const GROUP_ORDER = ["Foundations", "Type", "Actions", "Form", "Content", "Header", "Navigation", "Layout"];
$("#systemCards").innerHTML = ARTIFACTS.slice().sort((a, b) => GROUP_ORDER.indexOf(a.group) - GROUP_ORDER.indexOf(b.group)).map((a) =>
  '<li><div class="card-inner" data-open="artifact:' + a.id + '" ' + IMP + ">" +
  "<h3>" + esc(a.title) + "</h3>" +
  '<span class="id">' + esc(a.id) + " · " + esc(a.group) + "</span> " +
  chip(PLACE_CHIP[a.place][0], PLACE_CHIP[a.place][1]) +
  '<p class="note">' + esc(a.note) + "</p>" +
  (a.demo ? '<div class="demo"><div class="demo-label">live system demo</div>' + a.demo + "</div>" : "") +
  "</div></li>").join("");

$$("[data-open]", $("#systemCards")).forEach((b) => b.addEventListener("click", (ev) => {
  if (ev.target.closest("a, button, input, select, label, .button")) return;
  const ix = b.getAttribute("data-open").indexOf(":");
  openPanel(b.getAttribute("data-open").slice(0, ix), b.getAttribute("data-open").slice(ix + 1));
}));

const demoMenu = $("#demoOpenMenu");
if (demoMenu) demoMenu.addEventListener("click", () => { document.body.classList.add("is-menu-visible"); });
const demoReplay = $("#demoReplay");
if (demoReplay) demoReplay.addEventListener("click", () => {
  const w = $("#wrapper");
  w.classList.add("is-preload");
  setTimeout(() => { w.classList.remove("is-preload"); }, 80);
});

/* ------------------------------ ledger ---------------------------------- */
let activeFilter = "all";
const FAM_LABEL = { system: "System", craft: "Craft", assets: "Assets", content: "Content", pattern: "Patterns" };
const FAMS = [["all", "All", GAPS.length]].concat(Object.keys(FAM_LABEL).map((k) => [k, FAM_LABEL[k], GAPS.filter((g) => g.cat === k).length]));
$("#gapFilters").innerHTML = FAMS.map(([k, label, n]) =>
  '<li><button type="button" class="button small" data-f="' + k + '"' + (k === "all" ? " data-active" : "") + " " + IMP + ">" + label + " (" + n + ")</button></li>").join("");

function renderGaps() {
  const rows = GAPS.filter((g) => activeFilter === "all" || g.cat === activeFilter);
  $("#gapRows").innerHTML = rows.map((g) =>
    '<tr data-open="gap:' + g.id + '" ' + IMP + ">" +
    "<td><code>" + g.id + "</code></td>" +
    "<td>" + esc(g.title) + "</td>" +
    '<td><span class="chip ' + IMP + '">' + g.cat + "</span></td>" +
    "<td>" + chip(g.sev === "error" ? "defect" : g.sev === "warning" ? "candidate" : "gap", g.sev) + "</td>" +
    '<td><span class="chip ' + IMP + '">' + esc(g.fw) + "</span></td></tr>").join("");
  $$("tr[data-open]", $("#gapRows")).forEach((tr) => tr.addEventListener("click", () => {
    const ix = tr.getAttribute("data-open").indexOf(":");
    openPanel(tr.getAttribute("data-open").slice(0, ix), tr.getAttribute("data-open").slice(ix + 1));
  }));
}
$$("#gapFilters [data-f]").forEach((b) => b.addEventListener("click", () => {
  activeFilter = b.getAttribute("data-f");
  $$("#gapFilters [data-f]").forEach((x) => x.removeAttribute("data-active"));
  b.setAttribute("data-active", "1");
  renderGaps();
}));
renderGaps();
$("#statGaps").textContent = GAPS.length;
$("#gapIntro").innerHTML = GAPS.length + " items across five families: <em>system</em> (measured risks inside the language), " +
  "<em>craft</em> (markup and wiring defects), <em>assets</em> (files the site references but no longer serves), " +
  "<em>content</em> (placeholder text and finishing passes), <em>patterns</em> (surfaces a portfolio needs that the template never defines). " +
  'Each row cites its evidence; the pathway column shows how the system carries it — see <a href="#adaptations">Adaptations</a>.';

/* --------------------------- adaptations ------------------------------- */
const DEMOS = {
  aa: function () {
    const pairs = [["#ff6bbc", "deployed ink — body/heads (canon)"], ["#6bff2c", "deployed link green (canon)"],
                   ["#3ef900", "menu lime — black text on it (canon, 14.76:1)"], ["#8833e3", "form labels (canon, 5.79:1)"],
                   ["#585858", "template ink — buttons (base, 7.11:1)"], ["#b03b72", "candidate: darkened pink for text roles"],
                   ["#0b7285", "candidate: darkened link teal"]];
    return pairs.map(([hex, label]) => {
      const r = contrast(hex, "#ffffff");
      const pass = r >= 4.5 ? "AA ✓" : r >= 3 ? "large-only" : "fails";
      return '<div class="aa"><span class="sw" style="background:' + hex + '"></span><span class="ratio">' + r.toFixed(2) + " : 1 on white</span>" +
        chip(r >= 4.5 ? "canon" : "defect", pass) + ' <span class="muted" style="font-size:0.8em; margin-left:0.6em;">' + esc(label) + "</span></div>";
    }).join("") + '<p class="muted" style="font-size:0.85em;">Text roles need ≥ 4.5 : 1 (large ≥ 3). The deployed inks fail as text; the candidates below them clear the bar while keeping the identity. Promotion = pick a strategy: keep the ink and impose size floors, or move text roles to darkened variants on AA-sensitive pages — the black-body override already does the latter where needed.</p>';
  },
  cjk: function () {
    return '<div class="ba"><div><div class="ba-label">deployed — no stack (OS fallback)</div><div class="demo"><p style="margin:0; font-size:1.4em; font-weight:900; letter-spacing:0.2em; text-transform:uppercase;">Zhen Wu Yoyo <span style="font-family:serif;">圳</span></p><p class="muted" style="font-size:0.8em; margin:0.5em 0 0 0;">this render: a serif face beside 900-weight Latin — unmanaged, per-OS</p></div></div>' +
      '<div><div class="ba-label">proposed stack (gap G35)</div><div class="demo"><p style="margin:0; font-size:1.4em; font-weight:900; letter-spacing:0.2em; text-transform:uppercase;">Zhen Wu Yoyo <span style="font-family:\'Noto Sans SC\', \'PingFang SC\', \'Microsoft YaHei\', sans-serif;">圳</span></p><p class="muted" style="font-size:0.8em; margin:0.5em 0 0 0;">one line in the font stack + a weight policy — owner decision, filed</p></div></div></div>';
  },
  carousel: function () {
    const frames = ["ILightUUp — installation view (sample)", "Sea, Sense and Melody — detail (sample)", "Tame — prototype still (sample)"];
    return '<div class="car" id="carDemo" data-improvised data-mk="carousel candidate preview">' +
      '<div class="frame" id="carFrame">' + esc(frames[0]) + "</div>" +
      '<div class="ctrl"><button type="button" class="button small" id="carPrev">← Prev</button>' +
      '<span class="pos" id="carPos">1 / 3</span>' +
      '<button type="button" class="button small" id="carNext">Next →</button></div></div>' +
      '<p class="muted" style="font-size:0.85em; margin-top:0.6em;">No autoplay by default; arrow buttons in the ink-ring language; a position readout instead of dots. The deployed version rotates every 4s with no controls — and no images.</p>';
  },
  fluid: function () {
    return '<div class="ba">' +
      '<div><div class="ba-label">before — inline px widths</div><pre><code>&lt;img src="light/gallery1.jpg" width="800"&gt;\n&lt;iframe width="800" height="450" …&gt;</code></pre>' +
      '<p class="muted" style="font-size:0.82em;">document scrollWidth 820–1020 at a 390 viewport</p></div>' +
      '<div><div class="ba-label">after — fluid</div><pre><code>&lt;img src="…" style="max-width:100%; height:auto;"&gt;\n&lt;iframe style="width:100%; aspect-ratio:16/9;" …&gt;</code></pre>' +
      '<p class="muted" style="font-size:0.82em;">fits 390 — same composition, no horizontal overflow</p></div></div>';
  },
  project: function () {
    return '<div class="demo"><div class="demo-label">improvised project-detail composition — marked, filed</div>' +
      '<div ' + IMP + ' data-mk="project-detail improvisation"><h2 style="font-size:1em;">Tame — affection in VR</h2>' +
      '<p class="muted" style="font-size:0.8em;">2024 · installation · with collaborators · demo</p>' +
      '<span class="image main" style="margin-bottom:1em;"><img src="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'1000\' height=\'260\'%3E%3Crect width=\'1000\' height=\'260\' fill=\'%23eaeaea\'/%3E%3Cpath d=\'M0 260L1000 0M-50 260L950 0\' stroke=\'%23d5d5d5\' stroke-width=\'3\'/%3E%3C/svg%3E" alt="Project image placeholder" /></span>' +
      '<p>Two sentences of real project prose would sit here — built as a first-class page instead of a generic.html reuse.</p>' +
      '<ul class="actions"><li><a href="#adaptations" class="button small">Back to review</a></li></ul></div></div>';
  },
  content: function () {
    return '<div class="ba"><div><div class="ba-label">before — from the ledger</div><div class="demo"><p style="margin:0; font-size:0.85em;">menu on 7 pages: “Ipsum veroeros / Tempus etiam / Consequat dolor”</p>' +
      '<p style="margin:0.6em 0 0 0; font-size:0.85em;">wordmarks: 4 variants (incl. “Phantom”) · © “la la la” · “Short description”</p></div></div>' +
      '<div><div class="ba-label">after — normalised</div><div class="demo"><p style="margin:0; font-size:0.85em;">one menu: Home / About / Gallery / Publication / Log</p>' +
      '<p style="margin:0.6em 0 0 0; font-size:0.85em;">one wordmark · © 2026 Zhen Wu · a real line per project</p></div></div></div>' +
      '<p class="muted" style="font-size:0.85em; margin-top:0.5em;">Scaffold strings shown for shape, not as her voice — the owner writes the real words.</p>';
  },
};

$("#adaptList").innerHTML = ADAPTATIONS.map((a) => {
  const d = DEMOS[a.demo] ? DEMOS[a.demo]() : "";
  const demoHtml = typeof d === "string" ? d : "";
  return '<section class="adapt" id="' + a.id + '">' +
    "<h3>" + esc(a.title) + " " + chip(a.ladder.indexOf("candidate") >= 0 ? "candidate" : a.ladder === "normalise" ? "canon" : "improv", a.ladder) + "</h3>" +
    '<p style="font-size:0.9em;">' + esc(a.body) + "</p>" +
    '<div class="demo"><div class="demo-label">live — ' + esc(a.demo) + "</div>" + demoHtml + "</div>" +
    '<p style="font-size:0.8em;" class="muted">records: ' + a.links.map(linkBtn).join(" ") + "</p>" +
    "</section>";
}).join("");

$$("#adaptList [data-open]").forEach((b) => b.addEventListener("click", () => {
  const ix = b.getAttribute("data-open").indexOf(":");
  openPanel(b.getAttribute("data-open").slice(0, ix), b.getAttribute("data-open").slice(ix + 1));
}));

/* carousel wiring */
(function carousel() {
  const cf = $("#carFrame"), cp = $("#carPos");
  if (!cf) return;
  const frames = ["ILightUUp — installation view (sample)", "Sea, Sense and Melody — detail (sample)", "Tame — prototype still (sample)"];
  let i = 0;
  function paint() { cf.textContent = frames[i]; cp.textContent = (i + 1) + " / " + frames.length; }
  $("#carPrev").addEventListener("click", () => { i = (i + frames.length - 1) % frames.length; paint(); });
  $("#carNext").addEventListener("click", () => { i = (i + 1) % frames.length; paint(); });
})();

/* contrast helper (WCAG relative luminance) */
function contrast(hex1, hex2) {
  const lum = (hex) => {
    const c = hex.replace("#", "");
    const v = [0, 2, 4].map((k) => parseInt(c.substr(k, 2), 16) / 255).map((u) => (u <= 0.03928 ? u / 12.92 : Math.pow((u + 0.055) / 1.055, 2.4)));
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
  };
  const a = lum(hex1), b = lum(hex2);
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}

/* ----------------------------- evidence -------------------------------- */
$("#evGrid").innerHTML = EVIDENCE.map((e) =>
  '<li><figure class="evcard" ' + IMP + ">" +
  '<img class="evimg" src="assets/evidence/' + e.file + '" alt="' + esc(e.caption) + '" loading="lazy" />' +
  '<figcaption class="evbody"><h4>' + esc(e.label) + " " + chip("gap", e.tag) + "</h4><p>" + esc(e.caption) + "</p></figcaption>" +
  "</figure></li>").join("");

/* ------------------------- override toggle ----------------------------- */
const ovBtn = $("#overrideToggle");
ovBtn.addEventListener("click", () => {
  const on = document.body.classList.toggle("alt-override");
  ovBtn.setAttribute("aria-pressed", on ? "true" : "false");
  ovBtn.textContent = on ? "Back to the pink default" : "View as project page — the black-body override";
});

/* ------------------------------ menu ----------------------------------- */
const menuLink = $('a[href="#menu"]');
menuLink.addEventListener("click", (ev) => { ev.preventDefault(); document.body.classList.toggle("is-menu-visible"); });
document.addEventListener("click", (ev) => {
  if (!document.body.classList.contains("is-menu-visible")) return;
  if (ev.target.closest("#menu") || ev.target.closest('a[href="#menu"]')) return;
  document.body.classList.remove("is-menu-visible");
});
document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") document.body.classList.remove("is-menu-visible"); });
$$('#menu a[href^="#"]').forEach((a) => a.addEventListener("click", () => document.body.classList.remove("is-menu-visible")));

/* ------------------------------ marks ---------------------------------- */
const marksToggle = $("#marksToggle");
marksToggle.addEventListener("click", () => {
  const on = document.body.classList.toggle("marks-on");
  marksToggle.setAttribute("aria-pressed", on ? "true" : "false");
  marksToggle.title = on ? "Hide improvisations" : "Reveal improvisations";
});

/* ------------------------------ intro ---------------------------------- */
window.addEventListener("load", () => setTimeout(() => document.body.classList.remove("is-preload"), 100));
