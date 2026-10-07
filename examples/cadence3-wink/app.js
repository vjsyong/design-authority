"use strict";
/* =============================================================================
   Cadence — wink 0.2.0 build (examples/cadence3-wink)
   Personal ritual tracker. Vanilla JS, no network: fonts are local, all state
   in localStorage. The 42 spec elements are marked in the DOM:
     data-improvised / data-adapted / data-fallback  (revealed by the ◌ toggle)
   ========================================================================== */

const TODAY = "2026-10-07";                 // fixed fixture day (Wednesday)
const STORE_KEY = "cadence3.wink.v1";
const PAGE_SIZE = 8;
const CATEGORIES = ["Movement", "Mindfulness", "Learning", "Creative", "Home"];
const DFULL = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/* ------------------------------- fixtures -------------------------------- */

const RITUAL_SEED = [
  { id: "r1", name: "Morning run",     category: "Movement",    freq: "Every weekday", minutes: 20, streak: 6,  lastLog: "2026-10-07" },
  { id: "r2", name: "Meditate",        category: "Mindfulness", freq: "Every day",     minutes: 10, streak: 12, lastLog: "2026-10-07" },
  { id: "r3", name: "Read 20 pages",   category: "Learning",    freq: "Every day",     minutes: 25, streak: 2,  lastLog: "2026-10-04" },
  { id: "r4", name: "Guitar practice", category: "Creative",    freq: "Every weekday", minutes: 30, streak: 4,  lastLog: "2026-10-07" },
  { id: "r5", name: "Tidy desk",       category: "Home",        freq: "Every weekday", minutes: 5,  streak: 0,  lastLog: "2026-10-05" }
];

const ENTRY_SEED = [
  { d: "2026-09-24", r: "r1", m: 20 }, { d: "2026-09-25", r: "r1", m: 20 },
  { d: "2026-09-26", r: "r2", m: 10 }, { d: "2026-09-28", r: "r1", m: 21 },
  { d: "2026-09-28", r: "r2", m: 10 }, { d: "2026-09-29", r: "r2", m: 11 },
  { d: "2026-09-30", r: "r4", m: 25 },
  { d: "2026-10-01", r: "r2", m: 10 }, { d: "2026-10-01", r: "r1", m: 20 },
  { d: "2026-10-02", r: "r1", m: 22 }, { d: "2026-10-02", r: "r2", m: 10 },
  { d: "2026-10-03", r: "r2", m: 10 }, { d: "2026-10-03", r: "r4", m: 25 },
  { d: "2026-10-04", r: "r3", m: 25, note: "Chapter 6 — a good one." }, { d: "2026-10-04", r: "r2", m: 10 },
  { d: "2026-10-05", r: "r1", m: 24 }, { d: "2026-10-05", r: "r2", m: 10 },
  { d: "2026-10-05", r: "r4", m: 30 }, { d: "2026-10-05", r: "r5", m: 5 },
  { d: "2026-10-06", r: "r1", m: 20 }, { d: "2026-10-06", r: "r2", m: 12 },
  { d: "2026-10-07", r: "r1", m: 22 }, { d: "2026-10-07", r: "r2", m: 10 },
  { d: "2026-10-07", r: "r4", m: 30 }
];

const RHYTHMS = ["Every day", "Weekdays", "Twice a week"];

/* -------------------------------- state ---------------------------------- */

let state = loadState();
let ui = { view: "today", tab: "charts", page: 1, search: "", wizStep: 1, confirmCtx: null, detailsId: null };

function seedState() {
  return {
    rituals: RITUAL_SEED.map((r) => Object.assign({}, r)),
    entries: ENTRY_SEED.map((e) => Object.assign({}, e)),
    settings: { goal: 30, reminders: true, streakAlerts: false, rhythm: "Every day" },
    onboarded: false
  };
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (raw) {
      const s = JSON.parse(raw);
      if (s && Array.isArray(s.rituals) && Array.isArray(s.entries)) return s;
    }
  } catch (err) { /* fall through to seed */ }
  return seedState();
}
function save() { localStorage.setItem(STORE_KEY, JSON.stringify(state)); }

/* ------------------------------- helpers --------------------------------- */

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
function pad(n) { return n < 10 ? "0" + n : String(n); }
function dparse(isoStr) {
  const p = isoStr.split("-").map(Number);
  return new Date(p[0], p[1] - 1, p[2], 12);
}
function isoOf(dt) { return dt.getFullYear() + "-" + pad(dt.getMonth() + 1) + "-" + pad(dt.getDate()); }
function fmtDay(isoStr) { const dt = dparse(isoStr); return DFULL[dt.getDay()] + " " + dt.getDate() + " " + MONTHS[dt.getMonth()]; }
function last7() {
  const base = dparse(TODAY).getTime();
  const out = [];
  for (let i = 6; i >= 0; i--) out.push(isoOf(new Date(base - i * 86400000)));
  return out;
}
function minutesFor(isoStr) {
  return state.entries.filter((e) => e.d === isoStr).reduce((a, e) => a + e.m, 0);
}
function loggedToday() { return state.rituals.filter((r) => r.lastLog === TODAY).length; }
function isOnTrack(r) { return r.lastLog >= isoOf(new Date(dparse(TODAY).getTime() - 86400000)); }
function byId(id) { return state.rituals.find((r) => r.id === id) || null; }
function entriesOf(id) { return state.entries.filter((e) => e.r === id); }

/* ------------------------------ rendering -------------------------------- */

function renderAll() {
  renderToday();
  renderHistory();
  renderAchievements();
  renderSettings();
  syncNav();
  applyMarks();
}

function renderToday() {
  const total = state.rituals.length;
  const done = loggedToday();

  /* week banner — improvised composition */
  const week = last7();
  const wkMin = week.reduce((a, d) => a + minutesFor(d), 0);
  const wkSessions = state.entries.filter((e) => week.indexOf(e.d) >= 0).length;
  document.getElementById("wbLead").textContent = wkMin + " minutes across " + wkSessions + " sessions — ahead of last week.";
  document.getElementById("wbSub").textContent =
    (done === total && total > 0) ? "Every ritual logged today. That's the week behaving." :
    "Your steadiest seven days yet. Keep it comfortable.";

  /* ring — pattern/progress (W-18): yellow on parsnip track; ink when complete */
  const R = 59, C = 2 * Math.PI * R;
  const frac = total ? done / total : 0;
  const ringFill = document.getElementById("ringFill");
  ringFill.setAttribute("stroke-dasharray", String(C.toFixed(2)));
  ringFill.setAttribute("stroke-dashoffset", String((C * (1 - frac)).toFixed(2)));
  document.getElementById("ringCount").textContent = done + " of " + total;
  document.getElementById("ringCaption").textContent =
    total === 0 ? "nothing to log yet" : (done === total ? "all done today — nice." : "done today");
  document.querySelector(".ringcard").classList.toggle("is-complete", total > 0 && done === total);

  document.getElementById("listMeta").textContent = total + " rituals · " + done + " logged today";

  /* ritual list */
  const q = ui.search.trim().toLowerCase();
  const list = state.rituals.filter((r) => !q || r.name.toLowerCase().indexOf(q) >= 0 || r.category.toLowerCase().indexOf(q) >= 0);
  const listEl = document.getElementById("ritualList");
  listEl.innerHTML = list.map(ritualCard).join("");
  if (state.rituals.length > 0 && list.length === 0) {
    listEl.innerHTML = '<p class="muted">No rituals match “' + esc(ui.search.trim()) + '”. Try fewer letters.</p>';
  }
  document.getElementById("emptyState").hidden = total !== 0;
  document.getElementById("searchClear").hidden = !ui.search;
}

function ritualCard(r) {
  const logged = r.lastLog === TODAY;
  const newOne = !r.lastLog;
  const slipping = !newOne && !isOnTrack(r);
  const idx = state.rituals.indexOf(r);
  const status = newOne ? "New" : (slipping ? "Slipping" : "On track");
  return '' +
  '<article class="card ritual-card" data-ritual="' + r.id + '">' +
    '<div class="monogram" aria-hidden="true" data-adapted="photo/icon declined — monogram (asset policy)">' + esc(r.name.charAt(0)) + '</div>' +
    '<div>' +
      '<h3 class="ritual-name">' + esc(r.name) + '</h3>' +
      '<p class="ritual-meta">' +
        '<span class="tag" data-adapted="neutral tag — plain text, parsnip/ink (precedent)">' + esc(r.category) + '</span>' +
        '<span class="status ' + (slipping ? "slip" : "") + '" data-adapted="words + tint composition (W-14 route, precedent)">' + status + '</span>' +
        '<span class="streakline" data-improvised="composed readout — numeral + label (W-10)">' + (r.streak > 0 ? r.streak + "-day run" : "not started yet") + '</span>' +
      '</p>' +
      '<p class="ritual-schedule">' + esc(r.freq) + ' · ' + r.minutes + ' minutes' + (r.lastLog ? ' · last logged ' + fmtDay(r.lastLog) : '') + '</p>' +
    '</div>' +
    '<div class="ritual-actions">' +
      '<button class="cta small log-btn"' + (logged ? " disabled" : "") + '>' + (logged ? "Logged" : "Log") + '</button>' +
      '<a href="#" class="tlink details-btn">Details</a>' +
      '<a href="#" class="tlink moveup-btn' + (idx === 0 ? " is-dim" : "") + '" data-adapted="reorder via explicit move actions (precedent)">Move up</a>' +
      '<a href="#" class="tlink movedown-btn' + (idx === state.rituals.length - 1 ? " is-dim" : "") + '" data-adapted="reorder via explicit move actions (precedent)">Move down</a>' +
      '<a href="#" class="tlink delete-btn">Delete</a>' +
    '</div>' +
  '</article>';
}

function renderHistory() {
  renderCharts();
  renderLedger();
  renderLogForm();
}

function renderCharts() {
  const week = last7();
  const vals = week.map(minutesFor);
  const max = Math.max.apply(null, vals.concat([1]));

  /* bar chart — minimal data block: numerals + rules */
  document.getElementById("barsWrap").innerHTML = week.map((d, i) => {
    const h = Math.max(4, Math.round((vals[i] / max) * 118));
    const lab = DFULL[dparse(d).getDay()].charAt(0);
    return '<div class="bar-col"><span class="bar-num">' + vals[i] + '</span>' +
           '<span class="bar-rule" style="height:' + h + 'px"></span>' +
           '<span class="bar-day">' + lab + (d === TODAY ? " ·" : "") + '</span></div>';
  }).join("");
  const bars = document.getElementById("barsWrap");
  bars.removeAttribute("aria-hidden");
  bars.setAttribute("role", "img");
  bars.setAttribute("aria-label", "Minutes per day, last seven days: " + week.map((d, i) => fmtDay(d) + " " + vals[i] + " minutes").join(", "));
  document.getElementById("barTotal").textContent = vals.reduce((a, v) => a + v, 0) + " minutes in seven days.";

  /* heatmap — minimal data block: rules + numerals */
  const first = dparse("2026-10-01");
  const daysInOct = 31;
  const lead = (first.getDay() + 6) % 7;   // Monday-based column of the 1st
  let cells = "";
  for (let i = 0; i < lead; i++) cells += '<span class="heat-cell blank"></span>';
  for (let n = 1; n <= daysInOct; n++) {
    const isoStr = "2026-10-" + pad(n);
    const mins = minutesFor(isoStr);
    let cls = "heat-cell";
    if (mins > 0) cls += " on";
    if (isoStr === TODAY) cls += " today";
    if (isoStr > TODAY) cls += " future";
    cells += '<span class="' + cls + '">' + (mins > 0 ? mins : "") + '</span>';
  }
  const trail = (7 - ((lead + daysInOct) % 7)) % 7;
  for (let i = 0; i < trail; i++) cells += '<span class="heat-cell blank"></span>';
  document.getElementById("heatGrid").innerHTML =
    '<div class="heat-head"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div>' +
    '<div class="heatgrid">' + cells + '</div>';

  /* sparkline — minimal data block: rules + spacing */
  document.getElementById("sparkWrap").innerHTML = week.map((d) => {
    const h = Math.max(4, Math.round((minutesFor(d) / max) * 56));
    return '<span class="spark-rule" style="height:' + h + 'px"></span>';
  }).join("");
  const spark = document.getElementById("sparkWrap");
  spark.removeAttribute("aria-hidden");
  spark.setAttribute("role", "img");
  spark.setAttribute("aria-label", "Trend, last seven days: " + vals.join(", ") + " minutes.");
  document.getElementById("sparkCaption").textContent =
    "Up from " + vals[0] + " to " + vals[vals.length - 1] + " minutes — a steady climb.";
}

function renderLedger() {
  const sorted = state.entries.slice().sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : 0));
  const visible = sorted.slice(0, ui.page * PAGE_SIZE);
  document.getElementById("ledgerBody").innerHTML = visible.map((e) => {
    const r = byId(e.r);
    return '<tr><td>' + fmtDay(e.d) + '</td><td>' + esc(r ? r.name : "—") + '</td><td>' + e.m + '</td>' +
           '<td class="note-cell">' + (e.note ? esc(e.note) : "—") + '</td></tr>';
  }).join("");
  document.getElementById("pageReadout").textContent = "Showing " + visible.length + " of " + sorted.length;
  document.getElementById("loadOlder").hidden = visible.length >= sorted.length;
}

function renderLogForm() {
  const sel = document.getElementById("logRitual");
  const cur = sel.value;
  sel.innerHTML = state.rituals.map((r) => '<option value="' + r.id + '">' + esc(r.name) + '</option>').join("");
  if (cur && byId(cur)) sel.value = cur;
}

function renderAchievements() {
  const week = last7();
  const allMin = state.entries.reduce((a, e) => a + e.m, 0);
  const top = state.rituals.slice().sort((a, b) => b.streak - a.streak)[0];
  document.getElementById("streakBig").textContent = top && top.streak > 0 ? top.streak : "0";
  document.getElementById("streakSub").textContent = top && top.streak > 0
    ? top.name + ", going since 26 September."
    : "Nothing to show yet — give it a week.";

  const done = loggedToday();
  const total = state.rituals.length;
  const cards = [
    { t: "First steps",       l: "Log your very first session.",                     ok: state.entries.length > 0, badge: "Earned 24 Sep" },
    { t: "Seven straight",    l: "Seven days in a row on one ritual.",               ok: state.rituals.some((r) => r.streak >= 7), badge: "Earned 5 Oct" },
    { t: "Twenty sessions",   l: "Twenty entries in the ledger.",                    ok: state.entries.length >= 20, badge: "Earned 6 Oct" },
    { t: "Full house",        l: "Every ritual logged in a single day.",             ok: total > 0 && done === total, badge: "Earned today", locked: done + " of " + total + " today" },
    { t: "Comeback",          l: "Log again after a slipped day.",                   ok: false, locked: "Keep going" },
    { t: "Five hundred minutes", l: "Five hundred minutes in one month.",            ok: allMin >= 500, badge: "Earned", locked: allMin + " of 500 minutes" }
  ];
  document.getElementById("achGrid").innerHTML = cards.map((c) =>
    '<article class="card ach-card" data-improvised="composed: card + badge + numerals">' +
      '<h3 class="ach-title">' + c.t + '</h3>' +
      '<p class="ach-line">' + c.l + '</p>' +
      (c.ok ? '<span class="badge">' + c.badge + '</span>'
            : '<span class="ach-locked">' + c.locked + '</span>') +
    '</article>').join("");
}

function renderSettings() {
  document.getElementById("goalOut").textContent = state.settings.goal + " minutes a day — enough, not heroic.";
  document.getElementById("rhythmOut").textContent = "Checking in: " + state.settings.rhythm.toLowerCase() + ".";
  document.getElementById("dataReadout").textContent =
    state.rituals.length + " rituals · " + state.entries.length + " entries logged.";
}

function syncNav() {
  document.querySelectorAll(".nav-link").forEach((el) => {
    el.classList.toggle("is-active", el.getAttribute("data-view") === ui.view);
  });
  ["today", "history", "achievements", "settings"].forEach((v) => {
    const el = document.getElementById("view-" + v);
    if (el) el.hidden = v !== ui.view;
  });
}

/* ------------------------------- notices --------------------------------- */

function showNotice(html) {
  const el = document.getElementById("todayNotice");
  el.setAttribute("aria-live", "polite");
  el.innerHTML = html;
  el.hidden = false;
}

/* ------------------------------- actions --------------------------------- */

function logRitual(id, btn) {
  const r = byId(id);
  if (!r || r.lastLog === TODAY) return;
  if (btn) { btn.textContent = "Saving…"; btn.disabled = true; }
  setTimeout(() => {
    state.entries.push({ d: TODAY, r: r.id, m: r.minutes, note: "" });
    r.lastLog = TODAY;
    r.streak += 1;
    save();
    renderAll();
    const done = loggedToday(), total = state.rituals.length;
    showNotice(done === total
      ? "<b>Logged.</b> All " + total + " done today — that's the day closed, gently."
      : "<b>Logged.</b> That's " + done + " of " + total + " today.");
  }, 320);
}

function moveRitual(id, dir) {
  const i = state.rituals.findIndex((r) => r.id === id);
  const j = i + dir;
  if (i < 0 || j < 0 || j >= state.rituals.length) return;
  const t = state.rituals[i]; state.rituals[i] = state.rituals[j]; state.rituals[j] = t;
  save(); renderAll();
}

function addRitual(name, category, freq) {
  const r = {
    id: "r" + Date.now().toString(36),
    name: name, category: category, freq: freq, minutes: 15,
    streak: 0, lastLog: null   // "New" until the first log — honest, not smug
  };
  state.rituals.push(r);
  save(); renderAll();
  showNotice('<b>Added.</b> “' + esc(name) + '” is on the list — see you at the starting line.');
  return r;
}

function deleteRitual(id) {
  const r = byId(id);
  if (!r) return;
  state.rituals = state.rituals.filter((x) => x.id !== id);
  state.entries = state.entries.filter((e) => e.r !== id);
  save(); renderAll();
  document.querySelector("#listHeading").setAttribute("tabindex", "-1");
  document.querySelector("#listHeading").focus();
  showNotice('<b>Deleted.</b> “' + esc(r.name) + '” is gone for good — no undo, by design.');
}

/* ------------------------------- dialogs --------------------------------- */

const confirmDialog = document.getElementById("confirmDialog");
const detailsDialog = document.getElementById("detailsDialog");
const wizardDialog = document.getElementById("wizardDialog");
const addDialog = document.getElementById("addDialog");

function openConfirm(ctx) {
  ui.confirmCtx = ctx;
  document.getElementById("confirmTitle").textContent = ctx.title;
  document.getElementById("confirmBody").textContent = ctx.body;
  document.getElementById("confirmDelete").textContent = ctx.confirmLabel;
  confirmDialog.showModal();
  document.getElementById("confirmTitle").focus();   // destructive NEVER gets default focus
}
document.getElementById("confirmCancel").addEventListener("click", () => confirmDialog.close());
document.getElementById("confirmDelete").addEventListener("click", () => {
  const ctx = ui.confirmCtx;
  confirmDialog.close();
  if (ctx && ctx.onConfirm) ctx.onConfirm();
});

function openDetails(id) {
  const r = byId(id);
  if (!r) return;
  ui.detailsId = id;
  const idx = state.rituals.indexOf(r);
  document.getElementById("detailsTitle").textContent = r.name;
  document.getElementById("detailsBody").innerHTML =
    '<div class="detail-row"><b>Category</b><span class="tag" data-adapted="neutral tag — plain text, parsnip/ink (precedent)">' + esc(r.category) + '</span></div>' +
    '<div class="detail-row"><b>Status</b><span>' + (!r.lastLog ? "New — no log yet" : (isOnTrack(r) ? "On track" : "Slipping")) + ' — words first, as canon asks.</span></div>' +
    '<div class="detail-row"><b>Streak</b><span data-improvised="composed readout — numeral + label (W-10)">' + (r.streak > 0 ? r.streak + "-day run" : "Not started yet") + '</span></div>' +
    '<div class="detail-row"><b>Schedule</b><span>' + esc(r.freq) + ' · ' + r.minutes + ' minutes</span></div>' +
    '<div class="detail-row"><b>Logged</b><span>' + entriesOf(r.id).length + ' entries</span></div>' +
    '<div class="detail-row"><b>Why</b><span>Six weeks from now, this row is how it adds up.</span></div>';
  document.getElementById("detailsUp").classList.toggle("is-dim", idx === 0);
  document.getElementById("detailsDown").classList.toggle("is-dim", idx === state.rituals.length - 1);
  detailsDialog.showModal();
  document.getElementById("detailsTitle").focus();
}
document.getElementById("detailsClose").addEventListener("click", () => detailsDialog.close());
document.getElementById("detailsUp").addEventListener("click", () => {
  if (ui.detailsId) { moveRitual(ui.detailsId, -1); openDetailsAgain(); }
});
document.getElementById("detailsDown").addEventListener("click", () => {
  if (ui.detailsId) { moveRitual(ui.detailsId, 1); openDetailsAgain(); }
});
function openDetailsAgain() {   // keep the dialog open, refresh edge states
  const r = byId(ui.detailsId);
  if (!r) { detailsDialog.close(); return; }
  const idx = state.rituals.indexOf(r);
  document.getElementById("detailsUp").classList.toggle("is-dim", idx === 0);
  document.getElementById("detailsDown").classList.toggle("is-dim", idx === state.rituals.length - 1);
}
document.getElementById("detailsDelete").addEventListener("click", () => {
  const r = byId(ui.detailsId);
  detailsDialog.close();
  if (r) openConfirm({
    title: 'Delete “' + r.name + '”?',
    body: "This removes the ritual and its " + entriesOf(r.id).length + " logged entries for good. There's no undo — only momentum.",
    confirmLabel: "Delete ritual",
    onConfirm: () => deleteRitual(r.id)
  });
});

/* wizard — pattern/dialog-overlay composes the vessel; step controls are native fallbacks */
function openWizard() {
  ui.wizStep = 1;
  document.getElementById("wizChecks").innerHTML = state.rituals.map((r) =>
    '<label class="checkline" data-fallback="native checkbox — fallback/platform-controls">' +
    '<input type="checkbox" value="' + r.id + '" checked> ' + esc(r.name) + '</label>').join("");
  document.getElementById("wizRadios").innerHTML = RHYTHMS.map((rh) =>
    '<label class="checkline" data-fallback="native radio — fallback/platform-controls">' +
    '<input type="radio" name="wizrhythm" value="' + rh + '"' + (state.settings.rhythm === rh ? " checked" : "") + '> ' + rh + '</label>').join("");
  document.getElementById("wizGoal").value = state.settings.goal;
  document.getElementById("wizGoalOut").textContent = state.settings.goal + " minutes.";
  setWizStep(1);
  wizardDialog.showModal();
  document.getElementById("wizTitle").focus();
  applyMarks();
}
function setWizStep(n) {
  ui.wizStep = n;
  for (let i = 1; i <= 3; i++) document.getElementById("wizStep" + i).hidden = i !== n;
  document.getElementById("wizProgressText").textContent = "Step " + n + " of 3";
  document.getElementById("wizProgressBar").style.width = (n * 33.4) + "%";
  document.getElementById("wizBack").hidden = n === 1;
  document.getElementById("wizNext").textContent = n === 3 ? "Start tracking" : "Next";
}
document.getElementById("wizBack").addEventListener("click", () => setWizStep(ui.wizStep - 1));
document.getElementById("wizNext").addEventListener("click", () => {
  if (ui.wizStep < 3) { setWizStep(ui.wizStep + 1); return; }
  const picks = Array.prototype.slice.call(document.querySelectorAll("#wizChecks input:checked")).map((i) => i.value);
  const rhythm = (document.querySelector("#wizRadios input:checked") || {}).value || state.settings.rhythm;
  state.rituals = state.rituals.filter((r) => picks.indexOf(r.id) >= 0);
  state.settings.rhythm = rhythm;
  state.settings.goal = parseInt(document.getElementById("wizGoal").value, 10);
  state.onboarded = true;
  save(); renderAll(); wizardDialog.close();
  if (state.rituals.length === 0) { showView("today"); showNotice("<b>You're set.</b> Add a ritual whenever you're ready — the page will wait."); }
  else showNotice("<b>You're set.</b> " + state.rituals.length + " rituals, one gentle week.");
});
document.getElementById("wizSkip").addEventListener("click", () => {
  state.onboarded = true; save(); wizardDialog.close();
});

/* add ritual dialog */
function openAdd() {
  document.getElementById("addName").value = "";
  document.getElementById("addNameError").hidden = true;
  document.getElementById("addName").closest(".field").classList.remove("invalid");
  const cat = document.getElementById("addCategory");
  cat.innerHTML = CATEGORIES.map((c) => '<option>' + c + '</option>').join("");
  addDialog.showModal();
  document.getElementById("addTitle").focus();
}
document.getElementById("addCancel").addEventListener("click", () => addDialog.close());
document.getElementById("addForm").addEventListener("submit", (ev) => {
  ev.preventDefault();
  const nameEl = document.getElementById("addName");
  const name = nameEl.value.trim();
  if (!name) {
    document.getElementById("addNameError").hidden = false;
    nameEl.closest(".field").classList.add("invalid");
    nameEl.focus();
    return;
  }
  const freq = (document.querySelector("#addFreq input:checked") || {}).value || "Every day";
  const cat = document.getElementById("addCategory").value;
  addRitual(name, cat, freq);
  addDialog.close();
});
document.getElementById("addPhoto").addEventListener("change", (ev) => {
  const f = ev.target.files && ev.target.files[0];
  const note = ev.target.closest(".field").querySelector(".readout");
  note.textContent = f ? f.name + " attached — the monogram stays (asset policy)." : "wink shows a monogram instead — asset policy, not shyness.";
});

/* ----------------------------- log entry form ---------------------------- */

document.getElementById("logForm").addEventListener("submit", (ev) => {
  ev.preventDefault();
  const minutes = parseInt(document.getElementById("logMinutes").value, 10);
  const field = document.getElementById("logMinutesField");
  const err = document.getElementById("logError");
  if (!state.rituals.length) {
    showNotice("<b>Add a ritual first</b> — there's nothing to log against yet.");
    return;
  }
  if (!minutes || minutes <= 0) {
    err.hidden = false;
    field.classList.add("invalid");
    document.getElementById("logMinutes").focus();
    return;
  }
  err.hidden = true;
  field.classList.remove("invalid");

  const submit = document.getElementById("logSubmit");
  const saving = document.getElementById("savingNote");
  const payload = {
    d: document.getElementById("logDate").value || TODAY,
    r: document.getElementById("logRitual").value,
    m: minutes,
    note: document.getElementById("logNote").value.trim()
  };
  submit.disabled = true;
  submit.textContent = "Saving…";
  saving.hidden = false;
  setTimeout(() => {
    state.entries.push(payload);
    const r = byId(payload.r);
    if (r && payload.d === TODAY && r.lastLog !== TODAY) { r.lastLog = TODAY; r.streak += 1; }
    save(); renderAll();
    submit.disabled = false;
    submit.textContent = "Add entry";
    saving.hidden = true;
    document.getElementById("logMinutes").value = "";
    document.getElementById("logNote").value = "";
    const week = last7();
    showNotice("<b>Entry saved.</b> " + week.reduce((a, d) => a + minutesFor(d), 0) + " minutes this week — keep it comfortable.");
  }, 420);
});

/* ------------------------------- CSV export ------------------------------ */

document.getElementById("exportCsv").addEventListener("click", () => {
  const rows = [["Day", "Ritual", "Category", "Minutes", "Note"]];
  state.entries.slice().sort((a, b) => (a.d < b.d ? -1 : 1)).forEach((e) => {
    const r = byId(e.r) || { name: "", category: "" };
    rows.push([e.d, r.name, r.category, String(e.m), e.note || ""]);
  });
  const csv = rows.map((row) => row.map((c) => '"' + String(c).replace(/"/g, '""') + '"').join(",")).join("\n");
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
  const a = document.createElement("a");
  a.href = url;
  a.download = "cadence-entries.csv";
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
});

/* ------------------------------ marks toggle ----------------------------- */

const MARKS_ATTRS = ["improvised", "adapted", "fallback"];
const MK_CLASSES = ["mk-0", "mk-1", "mk-2", "mk-3"];
function applyMarks() {
  const on = document.body.classList.contains("marks-on");
  let i = 0;
  document.querySelectorAll("[data-improvised],[data-adapted],[data-fallback]").forEach((el) => {
    if (on) {
      const kind = MARKS_ATTRS.find((k) => el.hasAttribute("data-" + k));
      const note = el.getAttribute("data-" + kind) || "";
      el.setAttribute("data-mark-label", kind);
      MK_CLASSES.forEach((c) => el.classList.remove(c));
      el.classList.add("mk-" + (i++ % 4));   // cycle corners so adjacent labels don't collide
      if (note) el.setAttribute("title", kind + " — " + note);
    } else {
      el.removeAttribute("data-mark-label");
      MK_CLASSES.forEach((c) => el.classList.remove(c));
      el.removeAttribute("title");
    }
  });
}
document.getElementById("marksToggle").addEventListener("click", (ev) => {
  const on = document.body.classList.toggle("marks-on");
  ev.currentTarget.setAttribute("aria-pressed", on ? "true" : "false");
  ev.currentTarget.textContent = on ? "◉" : "◌";
  applyMarks();
});

/* ------------------------------- wiring ---------------------------------- */

function showView(name) {
  ui.view = name;
  syncNav();
}

document.querySelectorAll(".nav-link").forEach((el) => {
  el.addEventListener("click", () => showView(el.getAttribute("data-view")));
});
document.getElementById("addRitualBtn").addEventListener("click", openAdd);
document.getElementById("emptyAddBtn").addEventListener("click", openAdd);

/* tabs */
document.getElementById("tabCharts").addEventListener("click", () => setTab("charts"));
document.getElementById("tabEntries").addEventListener("click", () => setTab("entries"));
function setTab(t) {
  ui.tab = t;
  const isCharts = t === "charts";
  document.getElementById("tabCharts").classList.toggle("is-active", isCharts);
  document.getElementById("tabEntries").classList.toggle("is-active", !isCharts);
  document.getElementById("tabCharts").setAttribute("aria-selected", isCharts ? "true" : "false");
  document.getElementById("tabEntries").setAttribute("aria-selected", isCharts ? "false" : "true");
  document.getElementById("panelCharts").hidden = !isCharts;
  document.getElementById("panelEntries").hidden = isCharts;
}

/* search */
document.getElementById("ritualSearch").addEventListener("input", (ev) => {
  ui.search = ev.target.value;
  renderToday();
});
document.getElementById("searchClear").addEventListener("click", () => {
  ui.search = "";
  document.getElementById("ritualSearch").value = "";
  renderToday();
});

/* delegated list actions */
document.getElementById("ritualList").addEventListener("click", (ev) => {
  const card = ev.target.closest(".ritual-card");
  if (!card) return;
  const id = card.getAttribute("data-ritual");
  const r = byId(id);
  if (!r) return;
  if (ev.target.closest(".log-btn")) { logRitual(id, ev.target.closest(".log-btn")); return; }
  if (ev.target.closest(".details-btn")) { ev.preventDefault(); openDetails(id); return; }
  if (ev.target.closest(".moveup-btn")) { ev.preventDefault(); moveRitual(id, -1); return; }
  if (ev.target.closest(".movedown-btn")) { ev.preventDefault(); moveRitual(id, 1); return; }
  if (ev.target.closest(".delete-btn")) {
    ev.preventDefault();
    openConfirm({
      title: 'Delete “' + r.name + '”?',
      body: "This removes the ritual and its " + entriesOf(r.id).length + " logged entries for good. There's no undo — only momentum.",
      confirmLabel: "Delete ritual",
      onConfirm: () => deleteRitual(r.id)
    });
  }
});

/* ledger pager */
document.getElementById("loadOlder").addEventListener("click", () => { ui.page += 1; renderLedger(); });

/* settings controls */
document.getElementById("goalSlider").addEventListener("input", (ev) => {
  state.settings.goal = parseInt(ev.target.value, 10);
  save();
  document.getElementById("goalOut").textContent = state.settings.goal + " minutes a day — enough, not heroic.";
});
document.getElementById("remindersToggle").addEventListener("change", (ev) => {
  state.settings.reminders = ev.target.checked; save();
});
document.getElementById("streakAlerts").addEventListener("change", (ev) => {
  state.settings.streakAlerts = ev.target.checked; save();
});
document.getElementById("wizGoal").addEventListener("input", (ev) => {
  document.getElementById("wizGoalOut").textContent = ev.target.value + " minutes.";
});
document.getElementById("replayOnboarding").addEventListener("click", (ev) => { ev.preventDefault(); openWizard(); });
document.getElementById("resetDemo").addEventListener("click", (ev) => {
  ev.preventDefault();
  openConfirm({
    title: "Reset the demo?",
    body: "This puts every ritual, entry and setting back to how the demo shipped.",
    confirmLabel: "Reset demo",
    onConfirm: () => { localStorage.removeItem(STORE_KEY); window.location.reload(); }
  });
});

/* scrim-click dismissal (dialog-overlay a11y: Esc + scrim baseline) */
[confirmDialog, detailsDialog, wizardDialog, addDialog].forEach((dlg) => {
  dlg.addEventListener("click", (ev) => { if (ev.target === dlg) dlg.close(); });
});

/* ------------------------------- boot ------------------------------------ */

renderAll();
if (!state.onboarded) setTimeout(openWizard, 120);
