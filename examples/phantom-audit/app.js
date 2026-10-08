/* phantom-audit app.js
   Console behaviour + audit data. The console parts (chips, ledger, panel,
   filters, demos) are marked improvisations (see console.css header + the
   marks layer); the reviewed system lives in assets/css/main.css. */

/* ============================== DATA ================================== */

const ARTIFACTS = [
  {id: "token-set/type", title: "Type set — Source Sans Pro", cond: "canon",
   note: "One family, three voices: 300 light body, 700 sentence-case h1, 900 tracked caps for heads/labels. Used faithfully on the site.",
   demo: `<h1 style="margin-bottom:0.35em;">Heading one</h1><h2>Heading two · tracked caps</h2><h3>Heading three</h3><p>Body copy runs in Source Sans Pro light (300) at 12pt with generous line-height.</p>`},
  {id: "token-set/colour", title: "Colour — ink, tint, pink-led accents", cond: "deviated",
   note: "Ink #585858 on white; accents are SURFACES (pink #f2849e hover/focus, six tile pastels). The deployment re-inked text to neon pink/green.",
   demo: `<div style="display:flex; flex-wrap:wrap; gap:0.6em;">
     <div><div style="width:3.4em;height:3.4em;border-radius:4px;background:#585858;border:1px solid rgba(88,88,88,.25);"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#585858 ink</p></div>
     <div><div style="width:3.4em;height:3.4em;border-radius:4px;background:#fff;border:1px solid #c9c9c9;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#fff</p></div>
     <div><div style="width:3.4em;height:3.4em;border-radius:4px;background:rgba(144,144,144,0.075);border:1px solid #c9c9c9;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">tint</p></div>
     <div><div style="width:3.4em;height:3.4em;border-radius:4px;background:#f2849e;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">pink accent</p></div>
     <div><div style="width:3.4em;height:3.4em;border-radius:4px;background:#7ecaf6;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#7ecaf6</p></div>
     <div><div style="width:3.4em;height:3.4em;border-radius:4px;background:#8499e7;"></div><p style="font-size:0.65em;margin:0.3em 0 0 0;">#8499e7</p></div>
   </div>`},
  {id: "component/action-button", title: "Button — ink ring, tracked caps", cond: "canon",
   note: "Transparent ground + 2px ink ring (inset shadow); hover flips to pink. The deployment keeps this system intact.",
   demo: `<ul class="actions"><li><button type="button" class="button primary">Primary</button></li><li><button type="button" class="button">Default</button></li><li><button type="button" class="button small">Small</button></li></ul>`},
  {id: "component/field", title: "Field — underline input", cond: "deviated",
   note: "Tint ground, single bottom line (1px #c9c9c9), flat corners, pink underline on focus. Deployment re-inked the text to pink.",
   demo: `<div class="fields"><div class="field half"><input type="text" placeholder="Name" /></div><div class="field half"><input type="email" placeholder="Email" /></div></div>`},
  {id: "component/select", title: "Select", cond: "canon",
   note: "Native select restyled to the field language.",
   demo: `<select><option>— Category —</option><option>Installation</option><option>Game</option><option>Framework</option></select>`},
  {id: "component/checkbox-radio", title: "Checkbox & radio", cond: "deviated",
   note: "Custom marks: checked fills ink. The deployment repainted marks red and labels purple.",
   demo: `<div><input type="checkbox" id="demo-cb" checked /><label for="demo-cb">Consent</label></div><div><input type="radio" id="demo-r1" name="demo-r" checked /><label for="demo-r1">One</label><input type="radio" id="demo-r2" name="demo-r" /><label for="demo-r2">Two</label></div>`},
  {id: "component/actions", title: "Actions row", cond: "canon",
   note: "ul.actions — the standard cluster for buttons in footer/hero blocks.",
   demo: `<ul class="actions"><li><button type="button" class="button primary">Send</button></li><li><button type="button" class="button">Reset</button></li></ul>`},
  {id: "component/table", title: "Table — ruled, 900-weight head", cond: "deviated",
   note: "Deployment defect: an edited comment killed the .table-wrapper scroll rule (G09).",
   demo: `<div class="table-wrapper"><table><thead><tr><th>Name</th><th>Year</th></tr></thead><tbody><tr><td>ILightUUp</td><td>2024</td></tr><tr><td>Tame</td><td>2024</td></tr></tbody></table></div>`},
  {id: "component/tiles", title: "Tiles — project grid", cond: "deviated",
   note: "The portfolio grid; hover system disabled by the deployment (zoom off, veils repainted — G08).",
   demo: `<section class="tiles" style="margin:0;"><article class="style1"><span class="image"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect width='400' height='300' fill='%23e9e9e9'/%3E%3Cpath d='M0 300L400 0M-40 300L360 0M40 300L400 40' stroke='%23d4d4d4' stroke-width='2'/%3E%3C/svg%3E" alt="Placeholder tile" /></span><a href="#system"><h2>ILightUUp</h2><div class="content"><p>Light drives the emergent narrative.</p></div></a></article><article class="style2"><span class="image"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect width='400' height='300' fill='%23ececec'/%3E%3Cpath d='M0 300L400 0M-40 300L360 0' stroke='%23d8d8d8' stroke-width='2'/%3E%3C/svg%3E" alt="Placeholder tile" /></span><a href="#system"><h2>Tame</h2><div class="content"><p>Affection in VR.</p></div></a></article><article class="style6"><span class="image"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect width='400' height='300' fill='%23eaeaea'/%3E%3Cpath d='M0 300L400 0M40 300L400 40' stroke='%23d6d6d6' stroke-width='2'/%3E%3C/svg%3E" alt="Placeholder tile" /></span><a href="#system"><h2>FAFA</h2><div class="content"><p>A plant-based virus attacking AI systems.</p></div></a></article></section>`},
  {id: "component/blockquote", title: "Blockquote", cond: "canon",
   note: "Italic quote with a 4px left rule.",
   demo: `<blockquote>Playful interaction, sensorial interfaces, emergent art — the site's own words for its research.</blockquote>`},
  {id: "component/code-pre", title: "Code & preformatted", cond: "deviated",
   note: "Deployment turned the inline ground into a solid blue block (G03).",
   demo: `<p>Inline <code>tick-until-done</code> and a block:</p><pre><code>i = 0
while (!deck.isInOrder()):
    deck.shuffle()
    i += 1</code></pre>`},
  {id: "component/lists", title: "Lists", cond: "canon",
   note: "Disc lists, alt lists, ordered lists.",
   demo: `<ul><li>Dolor pulvinar etiam.</li><li>Sagittis adipiscing.</li></ul><ul class="alt"><li>Dolor pulvinar etiam.</li><li>Felis enim feugiat.</li></ul>`},
  {id: "component/image", title: "Image treatments", cond: "canon",
   note: ".image.main full-column, .image.fit content width, floats left/right.",
   demo: `<span class="image main" style="margin-bottom:0;"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1000' height='300'%3E%3Crect width='1000' height='300' fill='%23e9e9e9'/%3E%3Cpath d='M0 300L1000 0M-60 300L940 0M60 300L1000 60' stroke='%23d2d2d2' stroke-width='3'/%3E%3C/svg%3E" alt="Placeholder image" /></span>`},
  {id: "component/icon-row", title: "Icons & social row", cond: "canon",
   note: "Circle icon buttons; the site's footer uses these for Instagram / Scholar / GitHub / Email.",
   demo: `<ul class="icons"><li><a href="#system" class="icon brands style2 fa-github"></a></li><li><a href="#system" class="icon brands style2 fa-instagram"></a></li><li><a href="#system" class="icon solid style2 fa-envelope"></a></li><li><a href="#system" class="icon solid style2 fa-book"></a></li></ul>`},
  {id: "layout/header", title: "Header & logo", cond: "deviated",
   note: "Circular symbol + wordmark; deployment drifts the title per page (G22). The review uses it faithfully.",
   demo: `<div class="preview" style="display:flex; align-items:center; gap:0.8em;"><span style="display:inline-flex;width:2.6em;height:2.6em;border:2px solid #585858;border-radius:100%;align-items:center;justify-content:center;font-weight:700;">◔</span><span style="font-weight:700;letter-spacing:0.28em;text-transform:uppercase;font-size:0.85em;">Wordmark</span><span style="margin-left:auto;font-size:0.7em;font-weight:900;letter-spacing:0.28em;text-transform:uppercase;">Menu</span></div>`},
  {id: "layout/menu", title: "Menu overlay", cond: "deviated",
   note: "Fixed 22em panel, ink ground, 0.45s slide — deployment recoloured it neon green (G06).",
   demo: `<button type="button" class="button small" id="demoOpenMenu">Open the real menu ↗</button>`},
  {id: "layout/footer", title: "Footer", cond: "canon",
   note: "Grey ground, contact + follow sections, copyright bar — mirrored at the bottom of this page.",
   demo: `<div class="preview" style="background:#f6f6f6;"><p style="margin:0; font-size:0.8em;"><strong>Get in touch</strong> · zwuch@connect.ust.hk<br><span style="opacity:.6;">Follow — icons row</span></p></div>`},
  {id: "layout/page-intro", title: "Load-in motion", cond: "canon",
   note: "The system's only sanctioned motion: is-preload → fade/scale-in over 0.45s. Deployment adds an autoplay carousel on top (G21).",
   demo: `<button type="button" class="button small" id="demoReplay">Replay the load-in ↻</button>`},
  {id: "component/hr", title: "Horizontal rule", cond: "canon",
   note: "1px rule, 2em margins.",
   demo: `<hr />`},
];

const GAPS = [
  {id: "G01", title: "Body & form text re-inked to neon pink (#ff6bbc)", cat: "system", sev: "warning", fw: "precedent",
   ref: "main.css L122 (css-diff)",
   detail: "Every body/input/select/textarea inherits the neon pink. Pink-on-white measures ~2.1:1 — well below AA for text. The banner across it is the template's own pink accent (#f2849e, hover/focus roles only). Pathway: the declined precedent carries the reading-ink rule; the pink ambition routes to the accent candidate.",
   links: ["precedent:precedent/declined-neon-reading-ink", "candidate:candidate/pink-accent-system", "adapt:AD1"]},
  {id: "G02", title: "Links green (#6bff2c) over a blue dotted underline", cat: "system", sev: "warning", fw: "precedent",
   ref: "main.css L151-2", detail: "Link contrast ~1.3:1; two accents stack (green text + blue underline) where the system uses one ink + 50% ink dotted underline. Pathway: within the accent candidate, one accent carries link hover/underline — not two on the text itself.",
   links: ["precedent:precedent/declined-neon-reading-ink", "candidate:candidate/pink-accent-system", "adapt:AD1"]},
  {id: "G03", title: "Inline code painted as a solid blue block", cat: "system", sev: "warning", fw: "pathway",
   ref: "main.css L273", detail: "Inline code gained a fully opaque blue ground (rgba(46,90,249,.986)) — a reading surface in the middle of body copy. The system's code ground is the 7.5% grey tint.", links: ["adapt:AD1"]},
  {id: "G04", title: "Checkbox/radio labels purple (#8833e3)", cat: "system", sev: "info", fw: "pathway",
   ref: "main.css L2231", detail: "Form labels are the loudest text in the form; the system keeps labels in ink. Folds into the accent candidate's role map.", links: ["candidate:candidate/pink-accent-system"]},
  {id: "G05", title: "Checked mark fills red (#f51616)", cat: "system", sev: "info", fw: "pathway",
   ref: "main.css L2273", detail: "A red check reads as an error state. System: checked = ink fill.", links: ["candidate:candidate/pink-accent-system"]},
  {id: "G06", title: "Menu panel neon green (#3ef900) with black text", cat: "system", sev: "warning", fw: "pathway",
   ref: "main.css L3005", detail: "The signature surface recoloured to pure neon; also re-inks the panel to black over green rather than white over ink. If a coloured menu is wanted, it belongs in the accent candidate (surface role).",
   links: ["candidate:candidate/pink-accent-system", "adapt:AD1"]},
  {id: "G07", title: "Radius family flattened — 4px → 0px across 7 rules", cat: "system", sev: "error", fw: "defect",
   ref: "main.css L1845,2254,2283,2293,2314,2321,2597", detail: "Buttons, form controls, boxes, images and tiles all squared. The 4px family IS the system's softness (a candidate path exists to re-open the radius decision — but 0px fractures button/field language). Restore, or open a radius candidate.", links: ["adapt:AD5"]},
  {id: "G08", title: "Tile hover system disabled (zoom off; veils repainted)", cat: "system", sev: "warning", fw: "defect",
   ref: "main.css L2709-2741", detail: "Tile hover = the portfolio's interactive heart: pastel veil + copy panel + zoom. Deployment set scale(1.1→1) and swapped pastels for near-transparent fills / one full pink veil — hover feedback is now near-invisible or overpowering depending on state.", links: []},
  {id: "G09", title: "Table scroll wrapper rule is dead (comment edit)", cat: "craft", sev: "error", fw: "defect",
   ref: "main.css L2373-2378 (Table)", detail: "Deleting the /* */ markers left the bare word “Table” in the stylesheet, so the next rule parses as the selector “Table .table-wrapper” — matches nothing. Wide tables lose their horizontal scroll on small screens. Fix: restore the comment; the rule revives.",
   links: ["adapt:AD5"]},
  {id: "G10", title: "Orphan CSS: .imagemain (5%×1%, unused) + .publication colour patch", cat: "system", sev: "info", fw: "note",
   ref: "css-diff tail", detail: ".imagemain is dead code; .publication { color: black } is a page-local patch fighting the global pink — a symptom of G01, not a separate system decision.", links: ["adapt:AD5"]},
  {id: "G11", title: "A second <!DOCTYPE html><html><head> nested inside <body>", cat: "craft", sev: "error", fw: "defect",
   ref: "index.html L58-67", detail: "A whole document skeleton sits mid-content (with its own title/CSS links) — browsers cope, but it is invalid structure and it was clearly meant to hold a heading. Remove the block; keep the text.", links: ["adapt:AD5"]},
  {id: "G12", title: "Stray closers and mid-body markup: orphan </h1>, empty <span class=image main> wrapping sections", cat: "craft", sev: "error", fw: "defect",
   ref: "index.html L54-68, L91, L204", detail: "Commented-out headings leave an orphan </h1>; content sections are wrapped in an image container by accident. Tidy to the template's section pattern.", links: ["adapt:AD5"]},
  {id: "G13", title: "Broken title tag: <title>…</S></title>", cat: "craft", sev: "error", fw: "defect",
   ref: "publication.html L9", detail: "An “</S>” inside the title. One-character fix.", links: []},
  {id: "G14", title: "Every subpage still shows the stock lorem menu", cat: "craft", sev: "warning", fw: "normalise",
   ref: "light/tame/fafa/Unlogical/email/publication.html", detail: "Home has her real menu; every other page has “Ipsum veroeros / Tempus etiam / Consequat dolor / Elements”. Navigation contradicts itself across the site.", links: ["adapt:AD4"]},
  {id: "G15", title: "elements.html is byte-identical to the stock template demo", cat: "content", sev: "warning", fw: "normalise",
   ref: "elements.html (diff w/ upstream = empty)", detail: "Linked from the menu as “Game, Design & Development Log”, it still says “Phantom” and “Elements — Phantom by HTML5 UP”, with lorem content throughout. Either feed it or unlink it.", links: ["adapt:AD4"]},
  {id: "G16", title: "Font Awesome loaded twice (bundled + CDN beta on home only)", cat: "craft", sev: "warning", fw: "defect",
   ref: "index.html L13", detail: "The template bundles FA; the homepage also pulls a 6.0.0-beta CDN stylesheet. Icons come from whichever wins; subpages differ from home. Keep the bundled set (as this review does).", links: ["adapt:AD5"]},
  {id: "G17", title: "Per-page <style> blocks and inline styles bypass the system", cat: "craft", sev: "warning", fw: "normalise",
   ref: "light.html L16-35; index.html inline styles", detail: "Floats, pixel widths and colours live inline on individual pages (e.g. .image1 odd/even floats, width:700px images, inline pink h1). The system has classes for these patterns; inline forks are unmaintainable and unmarked.", links: []},
  {id: "G18", title: "Duplicate id=\"main\" on the homepage", cat: "craft", sev: "warning", fw: "defect",
   ref: "index.html L52 + L77", detail: "Two elements share id=main (a leftover nested block). Invalid; breaks anchor/anchor-adjacent code.", links: []},
  {id: "G19", title: "Every image has alt=\"\"", cat: "content", sev: "warning", fw: "note",
   ref: "all pages", detail: "Decorative-only assumption applied to content images (project photos, installation shots). Give content images real alt text; keep empty alt for true decoration.", links: []},
  {id: "G20", title: "No favicon, meta description or share cards", cat: "content", sev: "info", fw: "note",
   ref: "all pages", detail: "Tabs and shared links show defaults. This review adds description+title as a baseline example.", links: []},
  {id: "G21", title: "Autoplaying carousel with no controls and dead prev/next code", cat: "pattern", sev: "warning", fw: "improvise",
   ref: "index.html L261-305", detail: "4s autoplay, no pause, no arrows, desc fields empty, showPrev/showNext half-wired. The template defines no carousel — this is a genuine system gap. Pathway: the carousel candidate (controlled, no autoplay by default) + a real gap record.", links: ["candidate:candidate/carousel", "adapt:AD3"]},
  {id: "G22", title: "Logo/title drift across pages", cat: "content", sev: "info", fw: "normalise",
   ref: "index (Zhen Wu YoYo 圳) / generic+publication (About Zhen) / light (Back to main) / elements (Phantom)", detail: "Four different wordmarks. One brand line, site-wide.", links: ["adapt:AD4"]},
  {id: "G23", title: "Lorem ipsum survives in the “Sea, sense” tile", cat: "content", sev: "info", fw: "note",
   ref: "index.html L163", detail: "“Sed nisl arcu euismod sit amet nisi…” — placeholder copy on a live tile.", links: ["adapt:AD6"]},
  {id: "G24", title: "generic.html serves as About AND four project destinations", cat: "content", sev: "warning", fw: "improvise",
   ref: "generic.html (linked from About, Gallery, Sea sense, Orchid, SoundMorphTPU)", detail: "The template's generic page is reused so project tiles rarely lead anywhere specific. A project-detail composition is genuinely undefined by the template — improvised here, marked, filed.", links: ["gaprec:project-detail", "adapt:AD2"]},
  {id: "G25", title: "Empty carousel captions; “la la la” copyright; contact form commented out on home", cat: "content", sev: "info", fw: "note",
   ref: "index.html L246, L264-271, L216-231", detail: "Small finishing passes: captions written, copyright real, home contact block either restored (form) or the email section kept deliberately.", links: ["adapt:AD6"]},
  {id: "G26", title: "CJK characters fall back to system fonts (圳, 小圳的主页)", cat: "pattern", sev: "warning", fw: "improvise",
   ref: "index.html logo + comments; main.css has no CJK stack", detail: "The wordmark mixes “Zhen Wu YoYo 圳” with a Latin-only font stack — the 圳 renders in whatever the OS picks, differently on every platform. A mixed-script typography policy is genuinely undefined by the template; improvised here (marked) and filed.", links: ["gaprec:cjk-typography", "adapt:AD2"]},
  {id: "G27", title: "No active/current-page state in the menu", cat: "pattern", sev: "info", fw: "improvise",
   ref: "all pages (stock menu links identical everywhere)", detail: "Nothing marks where you are. A small current-section mark is undefined by the template; the review improvises one for its own anchor menu (see Marks), marked + filed.", links: ["gaprec:current-section-mark"]},
];

const ADAPTATIONS = [
  {id: "AD1", ladder: "candidate", title: "The pink accent, promoted properly",
   body: "Her experiment is legible: the template's own accent is pink — she pushed it everywhere at once. The system's response is not a scolding: it's a promotion bar. Draft one accent, map it to non-reading roles (hover, focus underline, markers), prove contrast, then sign off. The live check below runs the numbers on her values and a darker candidate.",
   demo: "aa", links: ["candidate:candidate/pink-accent-system", "precedent:precedent/declined-neon-reading-ink", "gap:G01", "gap:G02"]},
  {id: "AD2", ladder: "improvised", title: "Project-detail composition (undefined → marked)",
   body: "The template has no project page; the deployment reuses generic.html. Here the review improvises one in character — heading, meta row, full-width image, body, back-link — marked as an improvisation, filed as a gap record. This is the system's standard answer where it is silent: build, mark, file.",
   demo: "project", links: ["gaprec:project-detail", "gap:G24"]},
  {id: "AD3", ladder: "gap + candidate", title: "Carousel: controlled, not autoplaying",
   body: "G21's autoplay carousel is the clearest system gap. The candidate composition: image frame + caption + small ink buttons for prev/next + position readout; no autoplay by default; static fallback. Try it below — the same markup the candidate would specify.",
   demo: "carousel", links: ["candidate:candidate/carousel", "gap:G21"]},
  {id: "AD4", ladder: "normalise", title: "One menu, one wordmark, everywhere",
   body: "Normalisation, not invention: her real navigation list (Home, About, Gallery, Publication, Log) applied to every page, one wordmark, current-section marked. Before/after below.",
   demo: "menu-normal", links: ["gap:G14", "gap:G15", "gap:G22"]},
  {id: "AD5", ladder: "defect", title: "Craft repairs (no design content)",
   body: "Three of the craft defects, fixed on the spot — no authority needed: the nested document skeleton, the comment damage that killed the table wrapper, the duplicated icon kit. Before/after source below.",
   demo: "defects", links: ["gap:G09", "gap:G11", "gap:G12", "gap:G16"]},
  {id: "AD6", ladder: "gap (owner task)", title: "Content scaffolding — prose is her job",
   body: "The system can't write the portfolio, and shouldn't: it scaffolds. Placeholder copy becomes named work, captions get written, the copyright becomes real. Examples of the pass, from the ledger.",
   demo: "content", links: ["gap:G23", "gap:G25"]},
];

/* ========================== CONSOLE HELPERS =========================== */

const $ = (s, r) => (r || document).querySelector(s);
const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const IMP = 'data-improvised data-mk="console kit"';

function chip(kind, text) {
  return '<span class="chip chip--' + kind + '" ' + IMP + '>' + esc(text) + "</span>";
}

/* ----------------------------- panel ---------------------------------- */
const panel = $("#panel"), panelTitle = $("#panelTitle"), panelId = $("#panelId"), panelBody = $("#panelBody");

function openPanel(kind, id) {
  let title = "", sub = "", body = "";
  if (kind === "artifact") {
    const a = ARTIFACTS.find((x) => x.id === id); if (!a) return;
    title = a.title; sub = a.id;
    body = '<div class="kv"><b>Authority record</b><p>' + esc(a.note) + "</p></div>" +
      '<div class="kv"><b>Condition on the reviewed site</b><p>' + (a.cond === "canon" ? "Used as the system defines it." : "Overridden by the deployment — see the Gaps ledger.") + "</p></div>" +
      '<div class="kv"><b>Source</b><p><code>' + esc("packs/phantom · " + a.id) + "</code></p></div>" +
      '<div class="kv"><b>Live demo</b><div class="demo">' + a.demo + "</div></div>";
  } else if (kind === "gap") {
    const g = GAPS.find((x) => x.id === id); if (!g) return;
    title = g.title; sub = g.id + " · " + g.cat + " · " + g.sev;
    body = '<div class="kv"><b>Evidence</b><p><code>' + esc(g.ref) + "</code></p></div>" +
      '<div class="kv"><b>What this is</b><p>' + esc(g.detail) + "</p></div>" +
      '<div class="kv"><b>Pathway</b><p>' + chip(g.fw === "precedent" ? "candidate" : g.fw === "defect" ? "defect" : g.fw === "improvise" ? "improv" : "gap", g.fw) + "</p></div>" +
      (g.links.length ? '<div class="kv"><b>System artefacts</b><p>' + g.links.map(linkBtn).join(" ") + "</p></div>" : "");
  } else if (kind === "adapt") {
    const a = ADAPTATIONS.find((x) => x.id === id); if (!a) return;
    title = a.title; sub = a.id + " · " + a.ladder;
    body = '<div class="kv"><b>Why</b><p>' + esc(a.body) + "</p></div>" +
      '<div class="kv"><b>Artefacts</b><p>' + a.links.map(linkBtn).join(" ") + "</p></div>";
  } else if (kind === "gaprec") {
    title = ({ "project-detail": "gap record — project-detail composition",
                "cjk-typography": "gap record — mixed-script (CJK) typography",
                "current-section-mark": "gap record — current-section mark" })[id] || ("gap record — " + id);
    sub = "filed by this review · _evidence/gaps.jsonl";
    body = '<div class="kv"><b>What is needed</b><p>' + ({
      "project-detail": "A project-detail composition: heading, meta, media, body, back-link — genuinely undefined by the template.",
      "cjk-typography": "A typographic policy for Chinese/English mixed runs (font stack, size nudges, spacing) — undefined by a Latin-only system.",
      "current-section-mark": "A small current-section indicator for menu rows — template marks nothing.",
    })[id] + "</p></div>" +
    '<div class="kv"><b>Handling</b><p>Built in character, marked in the DOM, recorded here — never canon. Promote via a candidate if two consumers need it.</p></div>' +
    '<div class="kv"><b>Precedent check</b><p><code>da precedent-check --ask \"theme the menu\" → outside (neon re-ink is styling, not a pattern)</code></p></div>';
  }
  panelTitle.textContent = title;
  panelId.textContent = sub;
  panelBody.innerHTML = body;
  panel.hidden = false;
  bindPanelLinks();
}

function linkBtn(l) {
  const [kind, id] = l.split(":", 2);
  const label = kind === "adapt" ? "adaptation " + id : kind === "gaprec" ? "gap record" : id;
  return '<button type="button" class="button small" data-open="' + kind + ":" + id + '" ' + IMP + ">" + esc(label) + "</button>";
}

function bindPanelLinks() {
  $$("[data-open]", panelBody).forEach((b) => b.addEventListener("click", () => {
    const [k, id] = b.getAttribute("data-open").split(":", 2);
    openPanel(k, id);
  }));
}

$("#panelClose").addEventListener("click", () => { panel.hidden = true; });

/* --------------------------- system cards ------------------------------ */
$("#systemCards").innerHTML = ARTIFACTS.map((a) =>
  '<li><div class="card-inner" data-open="artifact:' + a.id + '" ' + IMP + ">" +
  "<h3>" + esc(a.title) + "</h3>" +
  '<span class="id">' + esc(a.id) + "</span> " +
  (a.cond === "deviated" ? chip("candidate", "deviated on site") : chip("canon", "canon")) +
  '<div class="mini">' + "</div>" +
  '<div class="demo"><div class="demo-label">live system demo</div>' + a.demo + "</div>" +
  "</div></li>").join("");

$$("[data-open]", $("#systemCards")).forEach((b) => b.addEventListener("click", (ev) => {
  if (ev.target.closest("a, button, input, select, label, .button")) return;  /* let demo controls work */
  const [k, id] = b.getAttribute("data-open").split(":", 2);
  openPanel(k, id);
}));

/* menu / intro demo buttons inside cards */
const demoMenu = $("#demoOpenMenu");
if (demoMenu) demoMenu.addEventListener("click", () => { document.body.classList.add("is-menu-visible"); });
const demoReplay = $("#demoReplay");
if (demoReplay) demoReplay.addEventListener("click", () => {
  const w = $("#wrapper");
  w.classList.add("is-preload");
  setTimeout(() => { w.classList.remove("is-preload"); }, 80);
});

/* ------------------------------ gaps ----------------------------------- */
let activeFilter = "all";
const FAMS = [["all", "All", GAPS.length], ["system", "System", GAPS.filter((g) => g.cat === "system").length],
              ["craft", "Craft", GAPS.filter((g) => g.cat === "craft").length],
              ["content", "Content", GAPS.filter((g) => g.cat === "content").length],
              ["pattern", "Patterns", GAPS.filter((g) => g.cat === "pattern").length]];
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
    const [k, id] = tr.getAttribute("data-open").split(":", 2);
    openPanel(k, id);
  }));
}
$$("#gapFilters [data-f]").forEach((b) => b.addEventListener("click", () => {
  activeFilter = b.getAttribute("data-f");
  $$("#gapFilters [data-f]").forEach((x) => x.removeAttribute("data-active"));
  b.setAttribute("data-active", "1");
  renderGaps();
}));
renderGaps();

/* --------------------------- adaptations ------------------------------- */
const DEMOS = {
  aa: function () {
    const pairs = [["#ff6bbc", "experiment: pink text"], ["#6bff2c", "experiment: link green"], ["#3ef900", "experiment: menu green"], ["#b03b72", "candidate: darker pink"], ["#f2849e", "system: pink accent"], ["#585858", "system: ink"]];
    return pairs.map(([hex, label]) => {
      const r = contrast(hex, "#ffffff");
      const pass = r >= 4.5 ? "AA ✓" : r >= 3 ? "large-only" : "fails";
      return '<div class="aa"><span class="sw" style="background:' + hex + '"></span><span class="ratio">' + r.toFixed(2) + " : 1 on white</span>" +
        chip(r >= 4.5 ? "canon" : "defect", pass) + ' <span class="muted" style="font-size:0.8em; margin-left:0.6em;">' + esc(label) + "</span></div>";
    }).join("") + '<p class="muted" style="font-size:0.85em;">Text roles need ≥ 4.5 : 1. The experiment values fail for text — but as SURFACES (hover/focus/veils) colour is exempt; that is exactly the role split the candidate asks the owner to sign off.</p>';
  },
  project: function () {
    return '<div class="demo"><div class="demo-label">improvised project-detail composition — marked, filed</div>' +
      '<div ' + IMP + ' data-mk="project-detail improvisation"><h2 style="letter-spacing:0.2em; font-size:1em;">Tame — affection in VR</h2>' +
      '<p class="muted" style="font-size:0.8em;">2024 · installation · with collaborators · demo</p>' +
      '<span class="image main" style="margin-bottom:1em;"><img src="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'1000\' height=\'260\'%3E%3Crect width=\'1000\' height=\'260\' fill=\'%23eaeaea\'/%3E%3Cpath d=\'M0 260L1000 0M-50 260L950 0\' stroke=\'%23d5d5d5\' stroke-width=\'3\'/%3E%3C/svg%3E" alt="Project image placeholder" /></span>' +
      '<p>Two sentences of real project prose would sit here — built as a first-class page instead of a generic.html reuse.</p>' +
      '<ul class="actions"><li><a href="#adaptations" class="button small">Back to review</a></li></ul></div></div>';
  },
  carousel: function () {
    const frames = ["ILightUUp — installation view (sample)", "Sea, Sense and Melody — detail (sample)", "Tame — prototype still (sample)"];
    return '<div class="car" id="carDemo" data-improvised data-mk="carousel candidate preview">' +
      '<div class="frame" id="carFrame">' + esc(frames[0]) + "</div>" +
      '<div class="ctrl"><button type="button" class="button small" id="carPrev">← Prev</button>' +
      '<span class="pos" id="carPos">1 / 3</span>' +
      '<button type="button" class="button small" id="carNext">Next →</button></div></div>' +
      '<p class="muted" style="font-size:0.85em; margin-top:0.6em;">No autoplay by default; arrow buttons in the ink-ring language; a position readout instead of dots. The deployment version rotates every 4s with no controls.</p>';
  },
  "menu-normal": function () {
    const before = ["Ipsum veroeros", "Tempus etiam", "Consequat dolor", "Elements"];
    const after = ["Home", "About", "Gallery", "Publication", "Game, Design & Development Log → (rebuilt or unlinked)"];
    return '<div class="ba"><div><div class="ba-label">before — stock lorem menus</div><div class="demo"><ul class="alt" style="margin:0;">' +
      before.map((x) => "<li>" + x + "</li>").join("") + '</ul></div></div><div><div class="ba-label">after — one real menu, site-wide</div><div class="demo"><ul class="alt" style="margin:0;">' +
      after.map((x) => "<li>" + x + "</li>").join("") + "</ul></div></div></div>";
  },
  defects: function () {
    return '<div class="ba">' +
      '<div><div class="ba-label">before — nested skeleton in body</div><pre><code>&lt;p&gt;Hello~ welcome…&lt;/p&gt;\n&lt;html lang="en"&gt;\n  &lt;head&gt;…&lt;/head&gt;\n  &lt;body&gt;&lt;/body&gt;\n&lt;/html&gt;</code></pre></div>' +
      '<div><div class="ba-label">after — the heading it meant to be</div><pre><code>&lt;h2&gt;Page of — YoYo Zhen&lt;/h2&gt;\n&lt;p&gt;Hello~ welcome…&lt;/p&gt;</code></pre></div>' +
      '<div><div class="ba-label">before — comment damage kills a rule</div><pre><code>Table\n\n.table-wrapper {\n  overflow-x: auto;\n}</code></pre></div>' +
      '<div><div class="ba-label">after — the comment restored</div><pre><code>/* Table */\n\n.table-wrapper {\n  overflow-x: auto;\n}</code></pre></div>' +
      '<div><div class="ba-label">before — two icon kits</div><pre><code>&lt;link … fontawesome-all (bundled)&gt;\n&lt;link … font-awesome/6.0.0-beta3 (CDN)&gt;</code></pre></div>' +
      '<div><div class="ba-label">after — the bundled kit only (as this review does)</div><pre><code>&lt;link … fontawesome-all.min.css&gt;</code></pre></div>' +
      "</div>";
  },
  content: function () {
    return '<div class="ba"><div><div class="ba-label">before</div><div class="demo"><p style="margin:0; font-size:0.85em;">“Sed nisl arcu euismod sit amet nisi lorem etiam dolor veroeros et feugiat.” — Sea, sense tile</p><p style="margin:0.6em 0 0 0; font-size:0.85em;">desc: "" (×4 carousel slides) · © la la la</p></div></div>' +
      '<div><div class="ba-label">after (scaffolded)</div><div class="demo"><p style="margin:0; font-size:0.85em;">“Tidal play — a harbour installation that listens to the water and answers in light.” — Sea, sense tile</p>' +
      '<p style="margin:0.6em 0 0 0; font-size:0.85em;">one real caption per slide · © 2026 Zhen Wu</p></div></div></div>' +
      '<p class="muted" style="font-size:0.85em; margin-top:0.5em;">Scaffold copy shown for shape, not as her voice — the owner writes the real words.</p>';
  },
};

$("#adaptList").innerHTML = ADAPTATIONS.map((a) => {
  const d = DEMOS[a.demo] ? DEMOS[a.demo]() : "";
  const demoHtml = typeof d === "string" ? d : "";
  return '<section class="adapt" id="' + a.id + '">' +
    "<h3>" + esc(a.title) + " " + chip(a.ladder.indexOf("candidate") >= 0 ? "candidate" : a.ladder === "defect" ? "defect" : a.ladder === "improvised" ? "improv" : "gap", a.ladder) + "</h3>" +
    '<p style="font-size:0.9em;">' + esc(a.body) + "</p>" +
    '<div class="demo"><div class="demo-label">live — ' + esc(a.demo) + "</div>" + demoHtml + "</div>" +
    '<p style="font-size:0.8em;" class="muted">artefacts: ' + a.links.map(linkBtn).join(" ") + "</p>" +
    "</section>";
}).join("");

$$("#adaptList [data-open]").forEach((b) => b.addEventListener("click", () => {
  const [k, id] = b.getAttribute("data-open").split(":", 2);
  openPanel(k, id);
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
window.addEventListener("load", () => setTimeout(() => document.body.classList.remove("is-preload"), 60));
