/* Cadence — behaviour. Every visual value follows app.css (wink pack citations in NOTES.md).
   No network calls; fixtures only; localStorage for demo persistence. */
"use strict";

/* ---------- fixtures ---------- */
const RITUALS = [
  { id: "r1", name: "Morning run", cat: "Movement", mins: 30, streak: 12, best: 21, spark: [30, 0, 30, 30, 30, 30, 30] },
  { id: "r2", name: "Read 20 pages", cat: "Mind", mins: 20, streak: 34, best: 34, spark: [20, 20, 20, 20, 20, 20, 0] },
  { id: "r3", name: "Meditate", cat: "Mind", mins: 10, streak: 8, best: 15, spark: [0, 10, 10, 10, 10, 10, 10] },
  { id: "r4", name: "No sugar", cat: "Discipline", mins: 0, streak: 21, best: 21, spark: [15, 15, 0, 15, 15, 15, 15] },
  { id: "r5", name: "Practice guitar", cat: "Craft", mins: 25, streak: 5, best: 12, spark: [25, 0, 25, 25, 25, 25, 0] }
];
const ICONS = {
  r1: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="14" cy="4.6" r="1.8"/><path d="M13.6 7l-2.6 4.6 3.6 2 1.6 4.4"/><path d="M11 11.4l-4.4-.8"/><path d="M13 14l-2.6 5.4"/></svg>',
  r2: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6.6C10.8 5.5 8.9 4.9 6.6 4.9c-.9 0-1.7.1-2.4.3v13c.7-.2 1.5-.3 2.4-.3 2.3 0 4.2.6 5.4 1.7 1.2-1.1 3.1-1.7 5.4-1.7.9 0 1.7.1 2.4.3v-13c-.7-.2-1.5-.3-2.4-.3-2.3 0-4.2.6-5.4 1.7z"/><path d="M12 6.6v13"/></svg>',
  r3: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="7.6" r="2.2"/><path d="M12 10.4c-1 1.9-3.1 3-5.8 3.4 1.5 2.1 3.6 3.3 5.8 3.3s4.3-1.2 5.8-3.3c-2.7-.4-4.8-1.5-5.8-3.4z"/></svg>',
  r4: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4.6c2.6 3 4.5 5.3 4.5 7.9a4.5 4.5 0 01-9 0c0-2.6 1.9-4.9 4.5-7.9z"/><path d="M6 5.4l12 13.2"/></svg>',
  r5: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="8.8" cy="15" r="4.6"/><circle cx="8.8" cy="15" r="1.5"/><path d="M12.1 11.7l6.4-6.4"/><path d="M16.4 5.4l2.2 2.2"/></svg>'
};
const ENTRIES = [
  { date: "Mon 6 Oct", ritual: "Morning run", minutes: 30, notes: "Felt strong — new route by the water." },
  { date: "Sun 5 Oct", ritual: "Read 20 pages", minutes: 20, notes: "Finished chapter seven on the balcony." },
  { date: "Sat 4 Oct", ritual: "Practice guitar", minutes: 25, notes: "Chord changes finally clean." },
  { date: "Fri 3 Oct", ritual: "Meditate", minutes: 10, notes: "Ten quiet minutes before work." },
  { date: "Thu 2 Oct", ritual: "No sugar", minutes: 15, notes: "Held the line all day." },
  { date: "Wed 1 Oct", ritual: "Morning run", minutes: 30, notes: "Rainy but done." },
  { date: "Tue 30 Sep", ritual: "Read 20 pages", minutes: 20, notes: "Slow pages, good pages." },
  { date: "Mon 29 Sep", ritual: "Practice guitar", minutes: 25, notes: "New song, half tempo." }
];
const OLDER = [
  { date: "Sun 28 Sep", ritual: "Meditate", minutes: 10, notes: "Day six of the run streak." },
  { date: "Sat 27 Sep", ritual: "No sugar", minutes: 15, notes: "Harder at the weekend, kept it." },
  { date: "Fri 26 Sep", ritual: "Morning run", minutes: 30, notes: "Legs heavy, mood light." },
  { date: "Thu 25 Sep", ritual: "Read 20 pages", minutes: 20, notes: "Read before the phone today." },
  { date: "Wed 24 Sep", ritual: "Practice guitar", minutes: 25, notes: "Worked the barre chords." },
  { date: "Tue 23 Sep", ritual: "Meditate", minutes: 10, notes: "Short but steady." }
];
const BARS = [{ d: "Mon", v: 45 }, { d: "Tue", v: 30 }, { d: "Wed", v: 60 }, { d: "Thu", v: 25 }, { d: "Fri", v: 50 }, { d: "Sat", v: 0 }, { d: "Sun", v: 35 }];
const HEAT = [1, 2, 0, 3, 2, 1, 0, 2, 3, 4, 3, 2, 1, 1, 0, 2, 3, 4, 3, 2, 0, 1, 2, 2, 3, 4, 3, 1, 0, 2, 3];
const BADGES = [
  { name: "First week", earned: true }, { name: "10 days", earned: true },
  { name: "Early bird", earned: true }, { name: "Century club", earned: true },
  { name: "21 days", earned: false }, { name: "Perfect month", earned: false }
];
const LS_KEY = "cadence.wink.v1";

/* ---------- state ---------- */
function defaults() {
  return {
    done: { r1: true, r3: true, r4: true },
    order: ["r1", "r2", "r3", "r4", "r5"],
    deleted: [],
    extraEntries: [],
    settings: { name: "Sam", cat: "Movement", weekstart: "monday", goal: 30, remMorning: true, remEvening: false, dark: false },
    introSeen: false,
    showMarks: false
  };
}
let S = load();
function load() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (!raw) return defaults();
    const d = defaults(), p = JSON.parse(raw);
    return { ...d, ...p, settings: { ...d.settings, ...(p.settings || {}) }, done: { ...d.done, ...(p.done || {}) } };
  } catch (e) { return defaults(); }
}
function save() { try { localStorage.setItem(LS_KEY, JSON.stringify(S)); } catch (e) { /* demo: storage optional */ } }

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const active = () => S.order.map((id) => RITUALS.find((r) => r.id === id)).filter((r) => r && !S.deleted.includes(r.id));

/* ---------- today ---------- */
function renderRing() {
  const list = active();
  const total = list.length || 1;
  const done = list.filter((r) => S.done[r.id]).length;
  const pct = Math.round((done / total) * 100);
  const C = 427.26;
  $("ringFill").style.strokeDashoffset = String(C * (1 - (list.length ? pct : 0) / 100));
  $("ringPct").textContent = (list.length ? pct : 0) + "%";
  $("ringSub").textContent = done + " of " + list.length + " done";
  $("heroDone").textContent = done + " of " + list.length + " rituals done";
  $("ringWrap").querySelector("svg").setAttribute("aria-label", done + " of " + list.length + " rituals done");
  renderStatus(done, list.length);
}
function renderStatus(done, total) {
  const pill = $("statusPill");
  const slipping = total > 0 && done / total < 0.6;
  pill.textContent = slipping ? "Slipping" : "On track";
  if (slipping) { pill.style.background = "var(--yellow)"; pill.style.boxShadow = "inset 0 0 0 1px var(--ink)"; }
  else { pill.style.background = "var(--parsnip)"; pill.style.boxShadow = "inset 0 0 0 1px var(--border)"; }
}
function renderList() {
  const ul = $("ritList");
  const list = active();
  $("emptyToday").hidden = list.length > 0;
  ul.innerHTML = list.map((r) => `
    <li class="ritrow" data-rid="${r.id}" draggable="true">
      <span class="draghandle" data-improvised="drag to reorder: undefined" title="Drag to reorder" aria-hidden="true">
        <svg width="14" height="18" viewBox="0 0 14 18" fill="currentColor"><circle cx="4" cy="4" r="1.4"/><circle cx="10" cy="4" r="1.4"/><circle cx="4" cy="9" r="1.4"/><circle cx="10" cy="9" r="1.4"/><circle cx="4" cy="14" r="1.4"/><circle cx="10" cy="14" r="1.4"/></svg>
      </span>
      <span class="ritoicon" data-improvised="icon glyphs: undefined">${ICONS[r.id] || ""}</span>
      <span>
        <span class="rename">${esc(r.name)}</span>
        <span class="meta">
          <span class="chip tag" data-improvised="neutral tag variant: undefined">${esc(r.cat)}</span>
          <span class="caption">${r.mins ? r.mins + " min" : "daily"}</span>
        </span>
      </span>
      <span class="chips">
        <span class="chip streak" data-improvised="streak chip: undefined"><b>${r.streak}d</b></span>
      </span>
      <button class="check ${S.done[r.id] ? "on" : ""}" data-improvised="check-off moment: undefined" aria-label="${S.done[r.id] ? "Uncheck" : "Check off"} ${esc(r.name)}" aria-pressed="${!!S.done[r.id]}">
        <svg viewBox="0 0 24 24" fill="none" stroke="#231E15" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg>
      </button>
    </li>`).join("");
}

/* ---------- history ---------- */
function renderBars() {
  const max = 60;
  $("bars").innerHTML = BARS.map((b, i) => `
    <div class="barcol ${i === 1 ? "today" : ""}">
      <div class="barval">${b.v ? b.v : "—"}</div>
      <div class="bartrack"><div class="barfill" style="height:${Math.round((b.v / max) * 100)}%"></div></div>
      <div class="barlbl">${b.d}</div>
    </div>`).join("");
}
function renderHeat() {
  $("heatGrid").innerHTML = HEAT.map((v, i) => `<div class="heatcell ${v ? "h" + v : ""}" title="Day ${i + 1}">${i + 1}</div>`).join("");
}
function allEntries() { return [...S.extraEntries, ...ENTRIES, ...OLDER]; }
let pageSize = 8;
function renderTable() {
  const q = $("entrySearch").value.trim().toLowerCase();
  const rows = allEntries().filter((e) => !q || (e.date + " " + e.ritual + " " + e.notes).toLowerCase().includes(q));
  const shown = rows.slice(0, pageSize);
  $("entryBody").innerHTML = shown.length
    ? shown.map((e) => `<tr><td>${esc(e.date)}</td><td>${esc(e.ritual)}</td><td class="num">${e.minutes}</td><td>${esc(e.notes)}</td></tr>`).join("")
    : `<tr><td colspan="4" class="caption" style="padding:18px">No entries match — try another word?</td></tr>`;
  const allShown = shown.length >= rows.length;
  $("olderBtn").style.visibility = allShown && rows.length ? "hidden" : "visible";
  $("pageInfo").textContent = rows.length ? `Showing ${shown.length} of ${rows.length}` : "No matches";
}

/* ---------- achievements ---------- */
function renderBadges() {
  $("badgeGrid").innerHTML = BADGES.map((b) => b.earned
    ? `<div class="badge"><span class="dot">✓</span>${esc(b.name)}</div>`
    : `<div class="badge locked" data-improvised="locked badge variant: undefined"><span class="dot">·</span>${esc(b.name)}</div>`).join("");
}

/* ---------- overlays ---------- */
function openScrim(id) { $(id).hidden = false; }
function closeScrim(id) { $(id).hidden = true; }
document.querySelectorAll(".scrim").forEach((s) => {
  s.addEventListener("click", (e) => { if (e.target === s) s.hidden = true; });
});
document.addEventListener("keydown", (e) => {
  if (e.key !== "Escape") return;
  const open = [...document.querySelectorAll(".scrim")].filter((s) => !s.hidden);
  if (open.length) open[open.length - 1].hidden = true;
});

let toastTimer = null;
function showToast(msg, ms) {
  $("toastMsg").textContent = msg;
  const t = $("toast");
  t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), ms || 2400);
}
function showConfirm(title, msg, verb, onYes) {
  $("cfTitle").textContent = title;
  $("cfMsg").textContent = msg;
  $("cfConfirm").textContent = verb;   /* never pre-focused (source-layer destructive-pattern note) */
  $("cfConfirm").onclick = () => { closeScrim("confirmModal"); onYes(); };
  openScrim("confirmModal");
}

/* ---------- log form ---------- */
function openLog() {
  const sel = $("logRitual");
  const list = active();
  sel.innerHTML = list.map((r) => `<option value="${r.id}">${esc(r.name)}</option>`).join("")
    || `<option value="">No rituals yet</option>`;
  $("minsErr").hidden = true;
  $("minsField").classList.remove("invalid");
  openScrim("logModal");
}
$("openLog").addEventListener("click", openLog);
$("emptyAdd").addEventListener("click", openLog);
$("logCancel").addEventListener("click", () => closeScrim("logModal"));
$("minsMinus").addEventListener("click", () => { const i = $("logMins"); i.value = Math.max(1, (+i.value || 1) - 5); });
$("minsPlus").addEventListener("click", () => { const i = $("logMins"); i.value = Math.min(300, (+i.value || 0) + 5); });
$("logForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const mins = +$("logMins").value;
  if (!mins || mins < 1) {
    $("minsField").classList.add("invalid");
    $("minsErr").hidden = false;
    return;
  }
  const rid = $("logRitual").value;
  const rec = RITUALS.find((r) => r.id === rid);
  $("logSpinner").hidden = false;                    /* ~700ms simulated save */
  $("logSubmit").disabled = true;
  setTimeout(() => {
    $("logSpinner").hidden = true;
    $("logSubmit").disabled = false;
    if (rec) {
      S.extraEntries.unshift({ date: "Tue 7 Oct", ritual: rec.name, minutes: mins, notes: $("logNotes").value || "Logged from Today." });
      save(); renderTable();
    }
    closeScrim("logModal");
    $("logNotes").value = "";
    showToast("Logged ✓");
  }, 700);
});

/* ---------- ritual detail ---------- */
let detailId = null;
function openDetail(id) {
  const r = RITUALS.find((x) => x.id === id);
  if (!r) return;
  detailId = id;
  $("detIcon").innerHTML = ICONS[id];
  $("detIcon").setAttribute("data-improvised", "icon glyphs: undefined");
  $("detTitle").textContent = r.name;
  $("detTag").textContent = r.cat;
  $("detStreak").textContent = r.streak;
  $("detBest").textContent = r.best;
  $("photoName").textContent = "";
  /* sparkline (element 14) */
  const w = 170, h = 44, max = Math.max(...r.spark, 1);
  const pts = r.spark.map((v, i) => `${(i / (r.spark.length - 1)) * (w - 8) + 4},${h - 6 - (v / max) * (h - 14)}`).join(" ");
  const last = r.spark[r.spark.length - 1];
  $("detSpark").innerHTML = `<svg width="100%" height="46" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-label="Last 7 days trend">
      <polyline points="${pts}" fill="none" stroke="#231E15" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>
      <circle cx="${w - 4}" cy="${h - 6 - (last / max) * (h - 14)}" r="4" fill="#FFE01B" stroke="#231E15" stroke-width="1.2"/>
    </svg>`;
  /* mini history */
  const hist = allEntries().filter((e) => e.ritual === r.name).slice(0, 3);
  $("detHist").innerHTML = hist.length
    ? hist.map((e) => `<div class="mh"><span>${esc(e.date)}</span><span>${e.minutes} min — ${esc(e.notes)}</span></div>`).join("")
    : `<div class="mh"><span class="muted">No entries yet — first one counts double.</span></div>`;
  openScrim("detailModal");
}
$("detClose").addEventListener("click", () => closeScrim("detailModal"));
$("photoBtn").addEventListener("click", () => $("photoInput").click());
$("photoInput").addEventListener("change", () => {
  const f = $("photoInput").files && $("photoInput").files[0];
  $("photoName").textContent = f ? f.name + " attached (demo only)" : "";
});
$("detDelete").addEventListener("click", () => {
  const r = RITUALS.find((x) => x.id === detailId);
  if (!r) return;
  closeScrim("detailModal");
  showConfirm(`Delete “${r.name}”?`, "It leaves your list and its history isn’t restored.", "Delete ritual", () => {
    S.deleted.push(r.id);
    delete S.done[r.id];
    save(); renderList(); renderRing(); renderTable();
    $("undoMsg").textContent = `“${r.name}” deleted.`;
    $("undoBar").hidden = false;
    clearTimeout(undoTimer);
    undoTimer = setTimeout(() => { $("undoBar").hidden = true; }, 8000);
  });
});
let undoTimer = null;
$("undoBtn").addEventListener("click", () => {
  const id = S.deleted.pop();
  if (id) { save(); renderList(); renderRing(); }
  $("undoBar").hidden = true;
});
$("ritList").addEventListener("click", (e) => {
  const row = e.target.closest(".ritrow");
  if (!row) return;
  const id = row.getAttribute("data-rid");
  if (e.target.closest(".check")) {
    S.done[id] = !S.done[id];
    save(); renderRing(); renderList();
    if (S.done[id]) {
      showToast("Logged ✓");
      const nb = document.querySelector(`.ritrow[data-rid="${id}"] .check`);
      if (nb) nb.classList.add("pop");   /* brief celebration moment (element 40) */
    }
    return;
  }
  openDetail(id);
});

/* drag to reorder (element 35, improvised) */
let dragId = null;
$("ritList").addEventListener("dragstart", (e) => {
  const row = e.target.closest(".ritrow");
  if (!row) return;
  dragId = row.getAttribute("data-rid");
  row.classList.add("dragging");
  e.dataTransfer.effectAllowed = "move";
});
$("ritList").addEventListener("dragend", (e) => {
  const row = e.target.closest(".ritrow");
  if (row) row.classList.remove("dragging");
  document.querySelectorAll(".ritrow.dragover").forEach((r) => r.classList.remove("dragover"));
});
$("ritList").addEventListener("dragover", (e) => {
  const row = e.target.closest(".ritrow");
  if (!row || !dragId || row.getAttribute("data-rid") === dragId) return;
  e.preventDefault();
  document.querySelectorAll(".ritrow.dragover").forEach((r) => r.classList.remove("dragover"));
  row.classList.add("dragover");
});
$("ritList").addEventListener("drop", (e) => {
  const row = e.target.closest(".ritrow");
  if (!row || !dragId) return;
  e.preventDefault();
  const to = row.getAttribute("data-rid");
  const from = S.order.indexOf(dragId);
  const dest = S.order.indexOf(to);
  if (from > -1 && dest > -1 && from !== dest) {
    S.order.splice(from, 1);
    S.order.splice(dest, 0, dragId);
    save(); renderList();
  }
  dragId = null;
});

/* ---------- views / tabs ---------- */
function setView(v) {
  ["today", "history", "achievements", "settings"].forEach((name) => {
    $("view-" + name).hidden = name !== v;
  });
  document.querySelectorAll(".navitem").forEach((b) => b.classList.toggle("on", b.getAttribute("data-view") === v));
}
document.querySelectorAll(".navitem").forEach((b) => b.addEventListener("click", () => setView(b.getAttribute("data-view"))));
/* bottom bar mirrors the tabs (element 30: nav bar -> bottom on mobile) */
$("tabsBottom").innerHTML = ["today", "history", "achievements", "settings"]
  .map((v) => `<button class="navitem" data-view="${v}">${v[0].toUpperCase() + v.slice(1)}</button>`).join("");
document.querySelectorAll("#tabsBottom .navitem").forEach((b) => b.addEventListener("click", () => setView(b.getAttribute("data-view"))));

/* ---------- achievements extras ---------- */
$("demoToggle").addEventListener("change", () => {
  const on = $("demoToggle").checked;
  $("badgeGrid").hidden = on;
  $("emptyAch").hidden = !on;
});
$("emptyAchBtn").addEventListener("click", openLog);

/* ---------- settings ---------- */
function fillSettings() {
  $("setName").value = S.settings.name;
  $("setCat").value = S.settings.cat;
  document.querySelectorAll('input[name="weekstart"]').forEach((r) => { r.checked = r.value === S.settings.weekstart; });
  $("goalSlider").value = S.settings.goal; $("goalVal").textContent = S.settings.goal + " min";
  $("remMorning").checked = S.settings.remMorning;
  $("remEvening").checked = S.settings.remEvening;
  $("darkToggle").checked = S.settings.dark;
  document.body.classList.toggle("dark", !!S.settings.dark);
}
$("goalSlider").addEventListener("input", () => { $("goalVal").textContent = $("goalSlider").value + " min"; });
$("darkToggle").addEventListener("change", () => {
  S.settings.dark = $("darkToggle").checked;
  document.body.classList.toggle("dark", S.settings.dark);
  save();
});
$("saveBtn").addEventListener("click", () => {
  const name = $("setName").value.trim();
  if (!name) { $("nameField").classList.add("invalid"); $("nameErr").hidden = false; return; }
  $("nameField").classList.remove("invalid"); $("nameErr").hidden = true;
  $("saveSpinner").hidden = false;                    /* ~700ms simulated save */
  $("saveBtn").disabled = true;
  setTimeout(() => {
    S.settings.name = name;
    S.settings.cat = $("setCat").value;
    S.settings.weekstart = document.querySelector('input[name="weekstart"]:checked').value;
    S.settings.goal = +$("goalSlider").value;
    S.settings.remMorning = $("remMorning").checked;
    S.settings.remEvening = $("remEvening").checked;
    save();
    $("saveSpinner").hidden = true;
    $("saveBtn").disabled = false;
    applyName();
    showToast("Saved");
  }, 700);
});
function applyName() {
  $("greeting").innerHTML = "Good evening, <em>" + esc(S.settings.name) + "</em>.";
  $("avatar").textContent = (S.settings.name[0] || "S").toUpperCase();
}

/* export CSV (element 38) */
function exportCSV() {
  const rows = [["date", "ritual", "minutes", "notes"], ...allEntries().map((e) => [e.date, e.ritual, e.minutes, e.notes])];
  const csv = rows.map((r) => r.map((c) => `"${String(c).replace(/"/g, '""')}"`).join(",")).join("\n");
  const blob = new Blob([csv], { type: "text/csv" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "cadence-export.csv";
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  showToast("Exported ✓");
}
$("exportHist").addEventListener("click", exportCSV);
$("exportSet").addEventListener("click", exportCSV);
$("entrySearch").addEventListener("input", () => { pageSize = 8; renderTable(); });
$("olderBtn").addEventListener("click", () => { pageSize = 99; renderTable(); });

/* delete all data */
$("deleteAll").addEventListener("click", () => {
  showConfirm("Delete everything?", "All rituals, logs and settings are wiped from this browser. It can’t be undone.", "Delete everything", () => {
    localStorage.removeItem(LS_KEY);
    S = defaults();
    prefill();
    save();
    applyName();
    showToast("Deleted ✓");
    setView("today");
  });
});

/* ---------- onboarding wizard (element 37) ---------- */
let wzStep = 0;
function renderWizard() {
  [1, 2, 3].forEach((n) => $("wz" + n).classList.toggle("on", n === wzStep + 1));
  $("wzBack").style.visibility = wzStep === 0 ? "hidden" : "visible";
  $("wzNext").textContent = wzStep === 2 ? "Start keeping" : "Next";
  [...$("wzDots").children].forEach((d, i) => d.classList.toggle("on", i === wzStep));
}
$("wzNext").addEventListener("click", () => {
  if (wzStep < 2) { wzStep++; renderWizard(); return; }
  S.settings.goal = +$("wzGoal").value;
  S.introSeen = true; save(); fillSettings();
  closeScrim("wizardModal");
});
$("wzBack").addEventListener("click", () => { if (wzStep > 0) { wzStep--; renderWizard(); } });
$("wzSkip").addEventListener("click", () => { S.introSeen = true; save(); closeScrim("wizardModal"); });
$("wzGoal").addEventListener("input", () => { $("wzGoalVal").textContent = $("wzGoal").value + " min"; });
$("replayBtn").addEventListener("click", () => { wzStep = 0; renderWizard(); openScrim("wizardModal"); });

/* ---------- ◌ marks toggle (required) ---------- */
$("marksBtn").addEventListener("click", () => {
  S.showMarks = !S.showMarks;
  document.body.classList.toggle("show-marks", S.showMarks);
  $("marksBtn").setAttribute("aria-pressed", String(S.showMarks));
  save();
});

/* ---------- boot ---------- */
function prefill() {
  renderList(); renderRing(); renderBars(); renderHeat(); renderTable(); renderBadges();
  fillSettings(); applyName();
  document.body.classList.toggle("show-marks", !!S.showMarks);
  $("marksBtn").setAttribute("aria-pressed", String(!!S.showMarks));
}
prefill();
setView("today");
if (!S.introSeen) { wzStep = 0; renderWizard(); openScrim("wizardModal"); }
