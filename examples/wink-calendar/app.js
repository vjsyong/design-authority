/* Wink Calendar — app.js
   Local storage, month grid, day agenda, create/edit/delete.
   Microcopy follows guideline/voice: second person, question-first,
   plain English, dry wit allowed. */

"use strict";

const STORE_KEY = "wink-calendar-events-v1";

/* ---------- storage ---------- */
function loadEvents() {
  try { return JSON.parse(localStorage.getItem(STORE_KEY)) || []; }
  catch { return []; }
}
function saveEvents(evts) {
  localStorage.setItem(STORE_KEY, JSON.stringify(evts));
}

/* ---------- date helpers (defined before first use) ---------- */
function fmtKey(d) {
  return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
}
const todayKey = () => fmtKey(new Date());
function parseKey(k) {
  const [y, m, d] = k.split("-").map(Number);
  return new Date(y, m - 1, d);
}

/* ---------- state ---------- */
let events = loadEvents();
let viewYear, viewMonth;          // month being shown (0-based month)
let selectedDate = todayKey();    // "YYYY-MM-DD"

const MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const DOWS = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];

/* ---------- els ---------- */
const $ = (id) => document.getElementById(id);
const monthTitle = $("month-title"), monthDows = $("month-dows"),
      monthCells = $("month-cells"), dayLabel = $("day-label"),
      dayTitle = $("day-title"), dayBody = $("day-body"),
      notice = $("notice"), noticeLead = $("notice-lead"), noticeSub = $("notice-sub"),
      scrim = $("scrim"), form = $("event-form"), fieldError = $("field-error"),
      scrimConfirm = $("scrim-confirm"), confText = $("conf-text");

/* ---------- rendering ---------- */
function render() {
  renderMonth();
  renderDay();
}

function renderMonth() {
  monthTitle.textContent = MONTHS[viewMonth] + " " + viewYear;
  monthDows.innerHTML = DOWS.map(d => `<span>${d}</span>`).join("");

  const first = new Date(viewYear, viewMonth, 1);
  const startOffset = first.getDay();                       // Sun=0
  const gridStart = new Date(viewYear, viewMonth, 1 - startOffset);
  const tk = todayKey();

  let html = "";
  for (let i = 0; i < 42; i++) {
    const d = new Date(gridStart.getFullYear(), gridStart.getMonth(), gridStart.getDate() + i);
    const key = fmtKey(d);
    const out = d.getMonth() !== viewMonth;
    const today = key === tk;
    const sel = key === selectedDate;
    const dayEvents = eventsByDay(key);

    let chips = "";
    if (dayEvents.length) {
      chips = dayEvents.slice(0, 3).map(e =>
        `<button type="button" class="chip" draggable="true" data-open="${e.id}" title="${esc(e.title)} — drag to reschedule">` +
        (e.allDay ? "" : `<span class="chip-time">${fmtTime(e.start)}&nbsp;</span>`) +
        esc(e.title) + `</button>`).join("");
      if (dayEvents.length > 3) chips += `<span class="chip-more">+${dayEvents.length - 3} more</span>`;
    }

    html += `<div class="cell${out ? " out" : ""}${today ? " today" : ""}${sel ? " sel" : ""}" data-day="${key}" role="button" tabindex="0" aria-label="${MONTHS[d.getMonth()]} ${d.getDate()}${dayEvents.length ? ", " + dayEvents.length + " events" : ""}">` +
      `<span class="dnum">${d.getDate()}</span>` + chips + `</div>`;
  }
  monthCells.innerHTML = html;
}

function eventsByDay(key) {
  return events
    .filter(e => e.date === key)
    .sort((a, b) => (a.allDay ? 0 : 1) - (b.allDay ? 0 : 1) || (a.start || "").localeCompare(b.start || ""));
}

function renderDay() {
  const d = parseKey(selectedDate);
  const isToday = selectedDate === todayKey();
  dayLabel.textContent = isToday ? "Today" : (isWeekend(d) ? "This weekend" : "This week");
  dayTitle.textContent = d.getDate() + " " + MONTHS[d.getMonth()];

  const dayEvents = eventsByDay(selectedDate);
  if (!dayEvents.length) {
    dayBody.innerHTML = `<div class="empty">
      <h3>Nothing here yet.</h3>
      <p>Quiet days are underrated — but if you'd like, you can put something on.</p>
      <button type="button" class="cta" data-open-new>Plan something</button>
    </div>`;
    return;
  }

  dayBody.innerHTML = `<div class="agenda">` + dayEvents.map(e =>
    `<div class="agenda-row" draggable="true" data-open="${e.id}" role="button" tabindex="0" title="Drag to another day to reschedule">
      <span class="agenda-time">${e.allDay ? `<span class="badge">All day</span>` : fmtTime(e.start) + "–" + fmtTime(e.end)}</span>
      <span><span class="agenda-title">${esc(e.title)}</span>${e.notes ? `<span class="agenda-notes">${esc(e.notes)}</span>` : ""}</span>
    </div>`).join("") + `</div>`;
}

const isWeekend = d => d.getDay() === 0 || d.getDay() === 6;

/* ---------- time helpers ---------- */
function fmtTime(t) {
  if (!t) return "";
  const [h, m] = t.split(":").map(Number);
  const ampm = h >= 12 ? "pm" : "am";
  const hh = h % 12 || 12;
  return m ? `${hh}:${String(m).padStart(2, "0")}${ampm}` : `${hh}${ampm}`;
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}

/* ---------- inline notice (pattern/inline-notice) ---------- */
let noticeTimer;
function notify(lead, sub) {
  noticeLead.textContent = lead;
  noticeSub.textContent = sub || "";
  notice.hidden = false;
  clearTimeout(noticeTimer);
  noticeTimer = setTimeout(() => { notice.hidden = true; }, 4000);
}

/* ---------- dialog (pattern/dialog-overlay) ---------- */
let editingId = null;
function openDialog(evt) {
  editingId = evt ? evt.id : null;
  $("dlg-title").textContent = evt ? "Edit event" : "New event";
  $("btn-save").textContent = evt ? "Save changes" : "Create event";
  $("btn-delete").hidden = !evt;
  fieldError.hidden = true;

  const f = form;
  f.title.value = evt ? evt.title : "";
  f.date.value = evt ? evt.date : selectedDate;
  f.allday.checked = evt ? !!evt.allDay : false;
  f.start.value = evt && !evt.allDay ? (evt.start || "") : "";
  f.end.value = evt && !evt.allDay ? (evt.end || "") : "";
  f.notes.value = evt ? (evt.notes || "") : "";
  toggleTimes(f.allday.checked);
  f.title.setAttribute("aria-invalid", "false");

  scrim.hidden = false;
  f.title.focus();
}
function closeDialog() { scrim.hidden = true; editingId = null; }

function toggleTimes(allDay) {
  $("time-row").style.display = allDay ? "none" : "flex";
}

/* ---------- destructive confirm (pattern/destructive-confirm) ---------- */
let pendingDeleteId = null;
function askDelete(evt) {
  pendingDeleteId = evt.id;
  confText.textContent = `We'll remove “${evt.title}” from ${parseKey(evt.date).getDate()} ${MONTHS[parseKey(evt.date).getMonth()]}. There's no undo — so take your time deciding.`;
  scrimConfirm.hidden = false;
  $("conf-cancel").focus();   // the destructive action never gets default focus
}
function closeConfirm() { scrimConfirm.hidden = true; pendingDeleteId = null; }

/* ---------- events: submit / delete ---------- */
function submitForm(ev) {
  ev.preventDefault();
  const f = form;
  const title = f.title.value.trim();
  const date = f.date.value;
  if (!title) {
    fieldError.textContent = "Give it a name — even “mystery meeting” works.";
    fieldError.hidden = false;
    f.title.setAttribute("aria-invalid", "true");
    f.title.focus();
    return;
  }
  if (!date) {
    fieldError.textContent = "Pick a day for it.";
    fieldError.hidden = false;
    f.date.setAttribute("aria-invalid", "true");
    f.date.focus();
    return;
  }
  if (f.end.value && f.start.value && f.end.value <= f.start.value) {
    fieldError.textContent = "It ends before it starts — that's a brave schedule.";
    fieldError.hidden = false;
    f.end.setAttribute("aria-invalid", "true");
    f.end.focus();
    return;
  }

  const allDay = f.allday.checked;
  const data = {
    title, date,
    start: allDay ? "" : (f.start.value || "09:00"),
    end: allDay ? "" : (f.end.value || f.start.value || "09:00"),
    allDay,
    notes: f.notes.value.trim(),
  };

  if (editingId) {
    const i = events.findIndex(e => e.id === editingId);
    if (i > -1) events[i] = { ...events[i], ...data, updatedAt: Date.now() };
    notify("Saved.", `“${title}” is updated.`);
  } else {
    events.push({ id: "ev_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), ...data, createdAt: Date.now() });
    notify("Done — it's on the calendar.", `“${title}” is set for ${parseKey(date).getDate()} ${MONTHS[parseKey(date).getMonth()]}.`);
  }
  saveEvents(events);
  selectedDate = date;
  closeDialog();
  render();
}

function doDelete() {
  const evt = events.find(e => e.id === pendingDeleteId);
  events = events.filter(e => e.id !== pendingDeleteId);
  saveEvents(events);
  closeConfirm();
  if (evt) notify("Deleted.", `“${evt.title}” is gone. The day is quieter for it.`);
  render();
}

/* ---------- navigation ---------- */
function shiftMonth(delta) {
  let m = viewMonth + delta, y = viewYear;
  if (m < 0) { m = 11; y--; }
  if (m > 11) { m = 0; y++; }
  viewMonth = m; viewYear = y;
  render();
}

/* ---------- wiring ---------- */
$("nav-prev").addEventListener("click", () => shiftMonth(-1));
$("nav-next").addEventListener("click", () => shiftMonth(1));
$("nav-today").addEventListener("click", () => {
  const t = new Date();
  viewYear = t.getFullYear(); viewMonth = t.getMonth();
  selectedDate = todayKey();
  render();
});
$("btn-new").addEventListener("click", () => openDialog(null));

monthCells.addEventListener("click", (e) => {
  const chip = e.target.closest("[data-open]");
  if (chip) {
    const evt = events.find(x => x.id === chip.dataset.open);
    if (evt) { openDialog(evt); return; }
  }
  const cell = e.target.closest("[data-day]");
  if (cell) { selectedDate = cell.dataset.day; render(); }
});
monthCells.addEventListener("keydown", (e) => {
  if (e.key !== "Enter" && e.key !== " ") return;
  const cell = e.target.closest("[data-day]");
  if (cell) { e.preventDefault(); selectedDate = cell.dataset.day; render(); }
});
monthCells.addEventListener("dblclick", (e) => {
  const cell = e.target.closest("[data-day]");
  if (cell) { selectedDate = cell.dataset.day; openDialog(null); }
});

/* ---------- drag to reschedule (improvisation — UNRECORDED, gap filed) ----
   Native HTML5 DnD, no framework (authority house rule: plain HTML/CSS/JS).
   Drag a chip (month) or agenda row (day panel) onto another day to move the
   event there, keeping its time. Drop target = the 2px ink inset-ring state. */
let justDragged = false;
document.addEventListener("dragstart", (e) => {
  const src = e.target.closest ? e.target.closest("[data-open]") : null;
  if (!src) return;
  justDragged = true;
  e.dataTransfer.setData("text/event-id", src.dataset.open);
  e.dataTransfer.effectAllowed = "move";
  src.classList.add("dragging");
});
document.addEventListener("dragend", (e) => {
  const src = e.target.closest ? e.target.closest("[data-open]") : null;
  if (src) src.classList.remove("dragging");
  // clear any lingering drop-target highlight
  document.querySelectorAll(".cell.drop-target").forEach(c => c.classList.remove("drop-target"));
});

function onCellDragOver(e, cell) {
  // only allow when actually dragging one of our events
  if (!e.dataTransfer.types.includes("text/event-id")) return;
  e.preventDefault();               // required to make the cell a drop target
  e.dataTransfer.dropEffect = "move";
  cell.classList.add("drop-target");
}
function onCellDragLeave(cell) {
  cell.classList.remove("drop-target");
}
function onCellDrop(e, cell) {
  e.preventDefault();
  cell.classList.remove("drop-target");
  const id = e.dataTransfer.getData("text/event-id");
  const evt = events.find(x => x.id === id);
  const newDay = cell.dataset.day;
  if (!evt || !newDay || evt.date === newDay) return;  // no-op if same day
  const from = evt.date;
  evt.date = newDay;
  evt.updatedAt = Date.now();
  saveEvents(events);
  selectedDate = newDay;
  const d = parseKey(newDay);
  notify("Rescheduled.", `“${evt.title}” moved to ${d.getDate()} ${MONTHS[d.getMonth()]}.`);
  render();
}
// wire per-cell drag handlers (cells are re-created on every render)
monthCells.addEventListener("dragover", (e) => {
  const cell = e.target.closest("[data-day]");
  if (cell) onCellDragOver(e, cell);
});
monthCells.addEventListener("dragleave", (e) => {
  const cell = e.target.closest("[data-day]");
  if (cell) onCellDragLeave(cell);
});
monthCells.addEventListener("drop", (e) => {
  const cell = e.target.closest("[data-day]");
  if (cell) onCellDrop(e, cell);
});
// a finished drag must not also fire as a click (open/selection)
monthCells.addEventListener("click", (e) => {
  if (justDragged) { justDragged = false; e.stopPropagation(); e.preventDefault(); }
}, true);
dayBody.addEventListener("click", (e) => {
  if (justDragged) { justDragged = false; e.stopPropagation(); e.preventDefault(); }
}, true);

dayBody.addEventListener("click", (e) => {
  if (e.target.closest("[data-open-new]")) { openDialog(null); return; }
  const row = e.target.closest("[data-open]");
  if (row) {
    const evt = events.find(x => x.id === row.dataset.open);
    if (evt) openDialog(evt);
  }
});

form.addEventListener("submit", submitForm);
form.addEventListener("input", (e) => {
  if (e.target.name === "allday") toggleTimes(e.target.checked);
  if (e.target === f_el()) fieldError.hidden = true;
});
function f_el() { return form.title; }
form.title.addEventListener("input", () => fieldError.hidden = true);
form.date.addEventListener("input", () => fieldError.hidden = true);
form.end.addEventListener("input", () => fieldError.hidden = true);

$("btn-cancel").addEventListener("click", closeDialog);
$("btn-delete").addEventListener("click", () => {
  const evt = events.find(x => x.id === editingId);
  if (evt) { closeDialog(); askDelete(evt); }
});
$("conf-cancel").addEventListener("click", closeConfirm);
$("conf-confirm").addEventListener("click", doDelete);

/* click on the scrim itself (not the dialog) closes */
scrim.addEventListener("mousedown", (e) => { if (e.target === scrim) closeDialog(); });
scrimConfirm.addEventListener("mousedown", (e) => { if (e.target === scrimConfirm) closeConfirm(); });
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    if (!scrimConfirm.hidden) closeConfirm();
    else if (!scrim.hidden) closeDialog();
  }
});

/* ---------- init ---------- */
(function init() {
  const t = new Date();
  viewYear = t.getFullYear(); viewMonth = t.getMonth();
  render();
})();
