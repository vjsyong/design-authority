/* Cadence — dominion v0.2.0 build (fixed fixtures; no network). */
'use strict';

var DEMO_TODAY = '2026-10-07';
var WEEK_START = '2026-10-05';   /* Monday of the demo week */
var LAST_WEEK = ['2026-09-28', '2026-09-29', '2026-09-30', '2026-10-01',
                 '2026-10-02', '2026-10-03', '2026-10-04'];
var LAST7 = ['2026-10-01', '2026-10-02', '2026-10-03', '2026-10-04',
             '2026-10-05', '2026-10-06', '2026-10-07'];
var KEY = 'cadence3-dominion-v1';
var PAGE_SIZE = 7;

var SEED = {
  version: 1,
  rituals: [
    { id: 'r1', name: 'Morning walk',   category: 'Health',   target: 25, freq: 'Daily',    notes: '' },
    { id: 'r2', name: 'Read 20 pages',  category: 'Learning', target: 20, freq: 'Daily',    notes: '' },
    { id: 'r3', name: 'Practice guitar', category: 'Craft',   target: 30, freq: 'Weekdays', notes: '' },
    { id: 'r4', name: 'Stretch',        category: 'Health',   target: 10, freq: 'Daily',    notes: '' },
    { id: 'r5', name: 'Tidy the desk',  category: 'Home',     target: 15, freq: 'Weekdays', notes: '' }
  ],
  logs: [
    { id: 'e01', date: '2026-10-07', ritualId: 'r1', minutes: 25, status: 'Logged' },
    { id: 'e02', date: '2026-10-07', ritualId: 'r2', minutes: 20, status: 'Logged' },
    { id: 'e03', date: '2026-10-06', ritualId: 'r1', minutes: 25, status: 'Logged' },
    { id: 'e04', date: '2026-10-06', ritualId: 'r3', minutes: 30, status: 'Logged' },
    { id: 'e05', date: '2026-10-05', ritualId: 'r1', minutes: 25, status: 'Logged' },
    { id: 'e06', date: '2026-10-05', ritualId: 'r4', minutes: 10, status: 'Logged' },
    { id: 'e07', date: '2026-10-04', ritualId: 'r2', minutes: 20, status: 'Made up' },
    { id: 'e08', date: '2026-10-03', ritualId: 'r1', minutes: 25, status: 'Logged' },
    { id: 'e09', date: '2026-10-03', ritualId: 'r4', minutes: 10, status: 'Logged' },
    { id: 'e10', date: '2026-10-02', ritualId: 'r2', minutes: 20, status: 'Logged' },
    { id: 'e11', date: '2026-10-01', ritualId: 'r1', minutes: 25, status: 'Logged' },
    { id: 'e12', date: '2026-09-29', ritualId: 'r2', minutes: 20, status: 'Logged' },
    { id: 'e13', date: '2026-09-28', ritualId: 'r1', minutes: 25, status: 'Logged' },
    { id: 'e14', date: '2026-09-28', ritualId: 'r5', minutes: 0,  status: 'Missed' }
  ],
  settings: { goal: 20, reminders: true, quiet: false }
};

var state = null;
var ui = {
  view: 'today',
  ledgerPage: 1,
  ledgerFilter: '',
  logRitual: null,
  editRitual: null,
  editorMode: null,
  detailId: null,
  onbStep: 1,
  lastRemoved: null,
  celebrate: false,
  dialogOpener: null,
  pendingRemove: null
};

/* ---------- helpers ---------- */

function $(sel, root) { return (root || document).querySelector(sel); }
function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

function clone(o) { return JSON.parse(JSON.stringify(o)); }

function fmtDate(iso) {
  var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var p = iso.split('-');
  return String(Number(p[2])) + ' ' + months[Number(p[1]) - 1] + ' ' + p[0];
}

function prevDay(iso) {
  var d = new Date(iso + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() - 1);
  return d.toISOString().slice(0, 10);
}

function fmtDayShort(iso) {
  var p = iso.split('-');
  return String(Number(p[2])) + ' ' + ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][Number(p[1]) - 1];
}

function pad2(n) { return (n < 10 ? '0' : '') + n; }

function byId(id) {
  for (var i = 0; i < state.rituals.length; i++) {
    if (state.rituals[i].id === id) return state.rituals[i];
  }
  return null;
}

function ritualName(id) {
  var r = byId(id);
  return r ? r.name : '(removed ritual)';
}

function ritualCategory(id) {
  var r = byId(id);
  return r ? r.category : '—';
}

function save() {
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
}

function load() {
  try {
    var raw = localStorage.getItem(KEY);
    if (raw) {
      var parsed = JSON.parse(raw);
      if (parsed && parsed.rituals && parsed.logs) return parsed;
    }
  } catch (e) { /* fall through to seed */ }
  return clone(SEED);
}

/* ---------- derived data ---------- */

function logsOn(date) { return state.logs.filter(function (l) { return l.date === date; }); }

function dayMinutes(date) {
  return logsOn(date).reduce(function (s, l) { return s + l.minutes; }, 0);
}

function streak() {
  var d = DEMO_TODAY, n = 0;
  while (dayMinutes(d) > 0) { n++; d = prevDay(d); }
  return n;
}

function weekSummary() {
  var elapsed = ['2026-10-05', '2026-10-06', '2026-10-07']; /* Mon..today */
  var slots = elapsed.length * state.rituals.length;
  var logged = 0, minutes = 0;
  state.logs.forEach(function (l) {
    if (l.date >= WEEK_START && l.date <= DEMO_TODAY && l.status !== 'Missed') {
      logged++; minutes += l.minutes;
    }
  });
  return { slots: slots, logged: logged, minutes: minutes, streak: streak() };
}

function last7Count(ritualId) {
  var first = LAST7[0];
  var n = 0;
  state.logs.forEach(function (l) {
    if (l.ritualId === ritualId && l.date >= first && l.date <= DEMO_TODAY && l.status !== 'Missed') n++;
  });
  return n;
}

function ritualStatus(ritualId) {
  return last7Count(ritualId) >= 3 ? 'On track' : 'Slipping';
}

function todayDone() {
  var seen = {};
  logsOn(DEMO_TODAY).forEach(function (l) { if (l.status !== 'Missed') seen[l.ritualId] = true; });
  return Object.keys(seen).length;
}

/* ---------- rendering ---------- */

function setView(view) {
  ui.view = view;
  $all('.view').forEach(function (v) { v.hidden = v.getAttribute('data-view') !== view; });
  $all('.nav-link').forEach(function (a) {
    if (a.getAttribute('data-view') === view) a.setAttribute('aria-current', 'page');
    else a.removeAttribute('aria-current');
  });
}

function renderNav() { setView(ui.view); }

function renderToday() {
  /* meter */
  var total = state.rituals.length;
  var done = todayDone();
  var minutesToday = dayMinutes(DEMO_TODAY);
  var target = state.rituals.reduce(function (s, r) { return s + r.target; }, 0);
  var pct = total ? Math.round((done / total) * 100) : 0;
  $('#meter-fill').style.width = pct + '%';
  $('#today-meter').setAttribute('aria-valuemax', String(total));
  $('#today-meter').setAttribute('aria-valuenow', String(done));
  $('#meter-readout').textContent = done + ' of ' + total + ' rituals · ' +
    minutesToday + ' of ' + target + ' minutes';

  /* week band */
  var w = weekSummary();
  $('#week-band-line').textContent = 'This week: ' + w.logged + ' of ' + w.slots +
    ' ritual slots logged · ' + w.minutes + ' minutes · streak ' + w.streak + ' days';

  /* ritual list */
  var list = $('#ritual-list');
  list.innerHTML = '';
  var firstUnlogged = null;
  state.rituals.forEach(function (r) {
    var doneToday = logsOn(DEMO_TODAY).some(function (l) {
      return l.ritualId === r.id && l.status !== 'Missed';
    });
    if (!doneToday && !firstUnlogged) firstUnlogged = r.id;
  });
  state.rituals.forEach(function (r, i) {
    var li = document.createElement('li');
    var st = ritualStatus(r.id);
    li.className = 'r-row';
    li.setAttribute('data-rit', r.id);
    var isPrimary = (r.id === firstUnlogged) && !ui.logRitual;
    li.innerHTML =
      '<span class="ordinal" data-el="19" data-mark="adapted" data-adapted ' +
        'data-note="ordinals stand in for icons (precedent)">' + pad2(i + 1) + '</span>' +
      '<span class="r-main"><span class="rname">' + escapeHtml(r.name) + '</span>' +
        '<span class="r-meta"> — ' + r.target + ' min · ' + r.freq + '</span></span>' +
      '<span class="tag" data-el="34" data-mark="adapted" data-adapted ' +
        'data-note="word label in the ruled register; tags declined as decoration">' +
        escapeHtml(r.category) + '</span>' +
      '<span class="st' + (st === 'Slipping' ? ' attn' : '') + '" data-el="17">' + st + '</span>' +
      '<span class="r-actions">' +
        '<button class="btn ' + (isPrimary ? 'b-slate' : 'b-out') + ' r-log" type="button" ' +
          'data-el="2" data-rid="' + r.id + '">Log</button>' +
        '<button class="btn b-link r-details" type="button" data-rid="' + r.id + '">Details</button>' +
      '</span>';
    list.appendChild(li);
  });

  /* empty state */
  var empty = state.rituals.length === 0;
  $('#empty-state').hidden = !empty;
  list.hidden = empty;

  /* editor + detail */
  renderLogEditor();
  renderDetail();
  $('#ceremony-accent').hidden = !ui.celebrate;
}

function renderLogEditor() {
  var ed = $('#log-editor');
  if (!ui.logRitual) { ed.hidden = true; return; }
  ed.hidden = false;
  $('#log-title').textContent = 'Log — ' + ritualName(ui.logRitual);
}

function openLogEditor(rid) {
  ui.logRitual = rid;
  ui.celebrate = false;
  ui.detailId = null;
  $('#log-date').value = DEMO_TODAY;
  var r = byId(rid);
  $('#log-minutes').value = String(r ? r.target : 20);
  $('#save-meter').hidden = true;
  $('#save-readout').textContent = 'Ready.';
  $('#notice-logged').hidden = true;
  renderToday();
  $('#log-editor').scrollIntoView({ block: 'nearest' });
}

function renderDetail() {
  var d = $('#ritual-detail');
  if (!ui.detailId || !byId(ui.detailId)) { d.hidden = true; return; }
  var r = byId(ui.detailId);
  d.hidden = false;
  $('#detail-title').textContent = r.name + ' — details';
  $('#detail-list').innerHTML =
    '<dt>Category</dt><dd>' + escapeHtml(r.category) + '</dd>' +
    '<dt>Frequency</dt><dd>' + escapeHtml(r.freq) + '</dd>' +
    '<dt>Daily target</dt><dd>' + r.target + ' minutes</dd>' +
    '<dt>Status</dt><dd>' + ritualStatus(r.id) + '</dd>' +
    '<dt>Logged, last 7 days</dt><dd>' + last7Count(r.id) + ' times</dd>';
}

function renderHistory() {
  /* bars — last complete week */
  var values = LAST_WEEK.map(dayMinutes);
  var max = Math.max.apply(null, values.concat([1]));
  var cols = $('#bar-cols');
  cols.innerHTML = '';
  values.forEach(function (v) {
    var col = document.createElement('div');
    col.className = 'bcol';
    var bar = document.createElement('div');
    bar.className = 'bar' + (v === 0 ? ' zero' : '');
    bar.style.height = (v === 0 ? 0 : Math.max(3, Math.round(v / max * 130))) + 'px';
    col.innerHTML = '<span class="bval">' + v + '</span>';
    col.appendChild(bar);
    cols.appendChild(col);
  });
  var days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  var drow = $('#bar-days');
  if (!drow) {
    drow = document.createElement('div');
    drow.className = 'days';
    drow.id = 'bar-days';
    $('#bars .bars').insertAdjacentElement('afterend', drow);
  }
  drow.innerHTML = days.map(function (d) { return '<span class="day">' + d + '</span>'; }).join('');

  /* heatmap — October 2026 */
  var grid = $('#heat-grid');
  grid.innerHTML = '';
  ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].forEach(function (wd) {
    var h = document.createElement('div');
    h.className = 'hcell wd';
    h.textContent = wd;
    grid.appendChild(h);
  });
  for (var b = 0; b < 3; b++) {
    var blank = document.createElement('div');
    blank.className = 'hcell blank';
    grid.appendChild(blank);
  }
  for (var day = 1; day <= 31; day++) {
    var iso = '2026-10-' + pad2(day);
    var cell = document.createElement('div');
    var m = dayMinutes(iso);
    var future = iso > DEMO_TODAY;
    var level = future ? 0 : (m === 0 ? 0 : m <= 20 ? 1 : m <= 45 ? 2 : 3);
    cell.className = 'hcell l' + level + (future ? ' future' : '') +
                     (iso === DEMO_TODAY ? ' today' : '');
    cell.textContent = String(day);
    cell.title = fmtDate(iso) + ' — ' + (future ? 'outside the demo fixture' : m + ' minutes');
    grid.appendChild(cell);
  }

  /* sparkline — last 7 days */
  var vals = LAST7.map(dayMinutes);
  var vmax = Math.max.apply(null, vals.concat([1]));
  var pts = vals.map(function (v, i) {
    var x = 12 + i * 112.7;
    var y = 104 - (v / vmax) * 88;
    return { x: x, y: y };
  });
  var svg = $('#spark-svg');
  var parts = ['<line x1="0" y1="104" x2="700" y2="104" stroke="#C9C9C9" stroke-width="1"></line>'];
  parts.push('<polyline fill="none" stroke="#000000" stroke-width="2" points="' +
    pts.map(function (p) { return p.x.toFixed(1) + ',' + p.y.toFixed(1); }).join(' ') + '"></polyline>');
  pts.forEach(function (p) {
    parts.push('<rect x="' + (p.x - 2).toFixed(1) + '" y="' + (p.y - 2).toFixed(1) +
               '" width="4" height="4" fill="#000000"></rect>');
  });
  svg.innerHTML = parts.join('');
  $('#spark-labels').textContent = vals.join(' · ') + ' minutes';
  $('#spark-labels').title = '(' + fmtDayShort(LAST7[0]) + ' → ' + fmtDayShort(DEMO_TODAY) + ')';

  renderLedger();
}

function renderLedger() {
  var f = ui.ledgerFilter.trim().toLowerCase();
  var rows = state.logs.slice().sort(function (a, b) { return b.date.localeCompare(a.date); });
  if (f) {
    rows = rows.filter(function (l) {
      return (ritualName(l.ritualId) + ' ' + ritualCategory(l.ritualId)).toLowerCase().indexOf(f) !== -1;
    });
  }
  var pages = Math.max(1, Math.ceil(rows.length / PAGE_SIZE));
  if (ui.ledgerPage > pages) ui.ledgerPage = pages;
  var slice = rows.slice((ui.ledgerPage - 1) * PAGE_SIZE, ui.ledgerPage * PAGE_SIZE);
  var tbody = $('#ledger-rows');
  tbody.innerHTML = '';
  slice.forEach(function (l) {
    var tr = document.createElement('tr');
    var cls = l.status === 'Missed' ? ' attn' : l.status === 'Made up' ? ' dim' : '';
    tr.innerHTML =
      '<td>' + fmtDate(l.date) + '</td>' +
      '<td>' + escapeHtml(ritualName(l.ritualId)) + '</td>' +
      '<td>' + l.minutes + '</td>' +
      '<td><span class="st' + cls + '">' + escapeHtml(l.status) + '</span></td>';
    tbody.appendChild(tr);
  });
  $('#page-readout').textContent = 'Page ' + ui.ledgerPage + ' of ' + pages;
  $('#page-prev').disabled = ui.ledgerPage <= 1;
  $('#page-next').disabled = ui.ledgerPage >= pages;
}

function renderAchievements() {
  var s = streak();
  $('#streak-value').textContent = String(s);
  $('#streak-sub').textContent = s === 1 ? 'day in a row' : 'days in a row';
  var seven = LAST7.filter(function (d) { return dayMinutes(d) > 0; }).length;
  $('#tile7-num').textContent = String(seven);
  $('#tile7-meta').textContent = seven + ' of 7 days';
  $('#tile-entries-num').textContent = String(state.logs.length);
  var lw = LAST_WEEK.reduce(function (a, d) { return a + dayMinutes(d); }, 0);
  $('#tile-week-num').textContent = String(lw);
}

function renderSettings() {
  /* admin list */
  var admin = $('#ritual-admin');
  admin.innerHTML = '';
  state.rituals.forEach(function (r, i) {
    var li = document.createElement('li');
    var st = ritualStatus(r.id);
    li.innerHTML =
      '<span class="ordinal">' + pad2(i + 1) + '</span>' +
      '<span class="grow"><span class="rname">' + escapeHtml(r.name) + '</span> ' +
        '<span class="r-meta">— ' + r.target + ' min · ' + r.freq + '</span></span>' +
      '<span class="tag">' + escapeHtml(r.category) + '</span>' +
      '<span class="st' + (st === 'Slipping' ? ' attn' : '') + '">' + st + '</span>' +
      '<button class="btn b-out admin-edit" type="button" data-rid="' + r.id + '">Edit</button>';
    admin.appendChild(li);
  });
  if (state.rituals.length === 0) {
    var li = document.createElement('li');
    li.innerHTML = '<span class="meta">No rituals. Add one to begin.</span>';
    admin.appendChild(li);
  }

  /* editor */
  var ed = $('#ritual-editor');
  if (ui.editRitual === null) {
    ed.hidden = true;
  } else {
    ed.hidden = false;
    var adding = ui.editorMode === 'add';
    $('#editor-title').textContent = adding ? 'Add a ritual' : 'Edit ritual';
    $('#editor-order').hidden = adding;
    $('#remove-ritual').hidden = adding;
    var r = adding ? null : byId(ui.editRitual);
    $('#ritual-name').value = r ? r.name : '';
    $('#ritual-category').value = r ? r.category : 'Health';
    $('#ritual-notes').value = r ? (r.notes || '') : '';
    var freq = r ? r.freq : 'Daily';
    $all('input[name="freq"]').forEach(function (x) { x.checked = x.value === freq; });
    $('#name-error').hidden = true;
    $('#field-name').classList.remove('invalid');
  }

  /* goal + toggles */
  $('#goal-slider').value = String(state.settings.goal);
  $('#goal-readout').textContent = state.settings.goal + ' minutes';
  $('#reminders-check').checked = !!state.settings.reminders;
  $('#quiet-toggle').checked = !!state.settings.quiet;
  $('#dark-toggle').checked = false;

  /* onboarding */
  for (var i = 1; i <= 3; i++) $('#onb-panel-' + i).hidden = (i !== ui.onbStep);
  $('#onb-readout').textContent = 'Step ' + ui.onbStep + ' of 3';
  $('#onb-back').hidden = ui.onbStep === 1;
  $('#onb-next').hidden = ui.onbStep === 3;
  $('#onb-finish').hidden = ui.onbStep !== 3;
}

function renderAll() {
  renderToday();
  renderHistory();
  renderAchievements();
  renderSettings();
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

/* ---------- interactions ---------- */

function openDialog(rid) {
  var r = byId(rid);
  if (!r) return;
  ui.pendingRemove = rid;
  var n = state.logs.filter(function (l) { return l.ritualId === rid; }).length;
  $('#confirm-body').textContent = 'Removing “' + r.name + '” hides it from Today. Its ' +
    n + ' log ' + (n === 1 ? 'entry stays' : 'entries stay') + ' in the journal. ' +
    'You can undo this right after.';
  ui.dialogOpener = document.activeElement;
  $('#dialog-scrim').hidden = false;
  $('#confirm-dialog').focus();
}

function closeDialog() {
  $('#dialog-scrim').hidden = true;
  ui.pendingRemove = null;
  if (ui.dialogOpener && ui.dialogOpener.focus) ui.dialogOpener.focus();
  ui.dialogOpener = null;
}

function confirmRemove() {
  var rid = ui.pendingRemove;
  if (!rid) { closeDialog(); return; }
  var idx = state.rituals.findIndex(function (r) { return r.id === rid; });
  if (idx === -1) { closeDialog(); return; }
  var ritual = state.rituals[idx];
  state.rituals.splice(idx, 1);
  save();
  closeDialog();
  ui.lastRemoved = { ritual: ritual, index: idx };
  ui.editRitual = null;
  $('#notice-removed').hidden = false;
  $('#notice-removed-text').textContent = 'Ritual removed — “' + ritual.name +
    '” is gone from Today. Log entries are kept.';
  renderAll();
}

function buildCsv() {
  var rows = [['date', 'ritual', 'category', 'minutes', 'status']];
  state.logs.slice().sort(function (a, b) { return b.date.localeCompare(a.date); })
    .forEach(function (l) {
      rows.push([l.date, ritualName(l.ritualId), ritualCategory(l.ritualId),
                 String(l.minutes), l.status]);
    });
  return rows.map(function (r) {
    return r.map(function (c) { return '"' + c.replace(/"/g, '""') + '"'; }).join(',');
  }).join('\n') + '\n';
}

function exportCsv() {
  var text = buildCsv();
  window.__lastExport = text;
  try {
    var blob = new Blob([text], { type: 'text/csv' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'cadence-dominion.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } catch (e) { /* the text is still exposed on window.__lastExport */ }
}

function wire() {
  /* nav */
  $all('.nav-link').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      setView(a.getAttribute('data-view'));
    });
  });

  /* today: ritual list (event delegation) */
  $('#ritual-list').addEventListener('click', function (e) {
    var logBtn = e.target.closest('.r-log');
    if (logBtn) { openLogEditor(logBtn.getAttribute('data-rid')); return; }
    var det = e.target.closest('.r-details');
    if (det) {
      var rid = det.getAttribute('data-rid');
      ui.detailId = ui.detailId === rid ? null : rid;
      renderToday();
    }
  });

  /* log editor */
  $('#log-minus').addEventListener('click', function () {
    var inp = $('#log-minutes');
    inp.value = String(Math.max(1, Number(inp.value || 0) - 5));
  });
  $('#log-plus').addEventListener('click', function () {
    var inp = $('#log-minutes');
    inp.value = String(Math.min(240, Number(inp.value || 0) + 5));
  });
  $('#log-save').addEventListener('click', function () {
    var rid = ui.logRitual;
    if (!rid) return;
    var minutes = Math.max(1, Number($('#log-minutes').value || 1));
    var date = $('#log-date').value || DEMO_TODAY;
    var btn = $('#log-save');
    btn.disabled = true;
    $('#save-meter').hidden = false;
    $('#save-fill').style.width = '0%';
    $('#save-readout').textContent = 'Saving · 0 of 1 steps';
    window.setTimeout(function () {
      state.logs.unshift({ id: 'u' + Date.now(), date: date, ritualId: rid,
                           minutes: minutes, status: 'Logged' });
      save();
      btn.disabled = false;
      $('#save-fill').style.width = '100%';
      $('#save-readout').textContent = 'Saved · 1 of 1 steps';
      var nt = $('#notice-logged');
      nt.hidden = false;
      $('#notice-logged-text').textContent = 'Logged — ' + minutes + ' minutes for ' +
        ritualName(rid) + ' on ' + fmtDate(date) + '. Totals updated.';
      ui.celebrate = true;
      renderToday();
      renderHistory();
      renderAchievements();
    }, 350);
  });
  $('#log-cancel').addEventListener('click', function () {
    ui.logRitual = null;
    ui.celebrate = false;
    renderToday();
  });

  /* history */
  $('#page-prev').addEventListener('click', function () {
    ui.ledgerPage = Math.max(1, ui.ledgerPage - 1);
    renderLedger();
  });
  $('#page-next').addEventListener('click', function () {
    ui.ledgerPage = ui.ledgerPage + 1;
    renderLedger();
  });
  $('#ledger-search').addEventListener('input', function () {
    ui.ledgerFilter = $('#ledger-search').value;
    ui.ledgerPage = 1;
    renderLedger();
  });

  /* settings: admin list + add */
  $('#ritual-admin').addEventListener('click', function (e) {
    var b = e.target.closest('.admin-edit');
    if (!b) return;
    ui.editRitual = b.getAttribute('data-rid');
    ui.editorMode = 'edit';
    renderSettings();
    $('#ritual-editor').scrollIntoView({ block: 'nearest' });
  });
  $('#admin-add').addEventListener('click', function () {
    ui.editRitual = '';
    ui.editorMode = 'add';
    renderSettings();
  });
  $('#empty-add').addEventListener('click', function () {
    setView('settings');
    ui.editRitual = '';
    ui.editorMode = 'add';
    renderSettings();
  });

  /* settings: editor */
  $('#editor-cancel').addEventListener('click', function () {
    ui.editRitual = null;
    renderSettings();
  });
  $('#editor-save').addEventListener('click', function () {
    var name = $('#ritual-name').value.trim();
    if (!name) {
      $('#name-error').hidden = false;
      $('#field-name').classList.add('invalid');
      return;
    }
    var category = $('#ritual-category').value;
    var notes = $('#ritual-notes').value;
    var freq = 'Daily';
    $all('input[name="freq"]').forEach(function (x) { if (x.checked) freq = x.value; });
    if (ui.editorMode === 'add') {
      state.rituals.push({ id: 'r' + Date.now(), name: name, category: category,
                           target: 20, freq: freq, notes: notes });
    } else {
      var r = byId(ui.editRitual);
      if (r) { r.name = name; r.category = category; r.freq = freq; r.notes = notes; }
    }
    save();
    ui.editRitual = null;
    $('#notice-generic').hidden = false;
    $('#notice-generic-text').textContent = 'Ritual saved — “' + name + '” appears in Today.';
    renderAll();
  });
  $('#move-up').addEventListener('click', function () {
    var idx = state.rituals.findIndex(function (r) { return r.id === ui.editRitual; });
    if (idx > 0) {
      var tmp = state.rituals[idx - 1];
      state.rituals[idx - 1] = state.rituals[idx];
      state.rituals[idx] = tmp;
      save(); renderAll();
    }
  });
  $('#move-down').addEventListener('click', function () {
    var idx = state.rituals.findIndex(function (r) { return r.id === ui.editRitual; });
    if (idx !== -1 && idx < state.rituals.length - 1) {
      var tmp = state.rituals[idx + 1];
      state.rituals[idx + 1] = state.rituals[idx];
      state.rituals[idx] = tmp;
      save(); renderAll();
    }
  });
  $('#remove-ritual').addEventListener('click', function () {
    if (ui.editRitual) openDialog(ui.editRitual);
  });

  /* settings: controls */
  $('#goal-slider').addEventListener('input', function () {
    state.settings.goal = Number($('#goal-slider').value);
    $('#goal-readout').textContent = state.settings.goal + ' minutes';
    save();
  });
  $('#reminders-check').addEventListener('change', function () {
    state.settings.reminders = $('#reminders-check').checked;
    save();
  });
  $('#quiet-toggle').addEventListener('change', function () {
    state.settings.quiet = $('#quiet-toggle').checked;
    save();
  });
  $('#export-csv').addEventListener('click', exportCsv);

  /* onboarding */
  $('#onb-next').addEventListener('click', function () {
    ui.onbStep = Math.min(3, ui.onbStep + 1);
    renderSettings();
  });
  $('#onb-back').addEventListener('click', function () {
    ui.onbStep = Math.max(1, ui.onbStep - 1);
    renderSettings();
  });
  $('#onb-finish').addEventListener('click', function () {
    $('#notice-generic').hidden = false;
    $('#notice-generic-text').textContent =
      'Getting started complete. Log your first ritual from Today.';
    renderSettings();
  });

  /* notices */
  $all('.notice-dismiss').forEach(function (b) {
    b.addEventListener('click', function () {
      $('#' + b.getAttribute('data-dismiss')).hidden = true;
    });
  });
  $('#undo-btn').addEventListener('click', function () {
    if (!ui.lastRemoved) return;
    var lr = ui.lastRemoved;
    state.rituals.splice(lr.index, 0, lr.ritual);
    save();
    ui.lastRemoved = null;
    $('#notice-removed-text').textContent = 'Restored — “' + lr.ritual.name + '” is back in Today.';
    renderAll();
  });

  /* dialog */
  $('#confirm-cancel').addEventListener('click', closeDialog);
  $('#confirm-remove').addEventListener('click', confirmRemove);
  $('#dialog-scrim').addEventListener('click', function (e) {
    if (e.target === $('#dialog-scrim')) closeDialog();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !$('#dialog-scrim').hidden) closeDialog();
  });

  /* marks toggle */
  $('#marks-toggle').addEventListener('click', function () {
    var on = document.body.classList.toggle('marks-on');
    $('#marks-toggle').setAttribute('aria-pressed', on ? 'true' : 'false');
  });
}

/* ---------- boot ---------- */

state = load();
wire();
setView(ui.view);
renderAll();

/* expose a small hook for the review harness */
window.cadence = {
  state: function () { return state; },
  ui: function () { return ui; },
  demoToday: DEMO_TODAY,
  reset: function () { try { localStorage.removeItem(KEY); } catch (e) {} }
};
