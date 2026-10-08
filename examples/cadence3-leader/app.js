'use strict';
/* Cadence — a ritual tracker, stress-built against the leader authority (v0.2.0).
   Fixed fixtures; all mutations persist to localStorage. */

const TODAY = '2026-10-07';
const WEEK_START = '2026-10-05';
const STORE_KEY = 'cadence.v3';

/* Deterministic fixture log (mulberry32 seed 20261007; see NOTES.md). */
const FIXTURE_LOGS = {
 "2026-09-03": {"r1":13,"r2":23,"r3":30,"r4":16},
 "2026-09-04": {"r1":13,"r3":35},
 "2026-09-05": {"r1":11,"r2":24,"r4":18},
 "2026-09-06": {"r2":25,"r4":18,"r5":29},
 "2026-09-07": {"r1":15,"r3":35,"r4":19},
 "2026-09-08": {"r1":15,"r2":23,"r4":19},
 "2026-09-09": {"r1":11,"r2":20,"r3":33},
 "2026-09-10": {"r2":23,"r3":35,"r4":16},
 "2026-09-11": {"r1":13,"r2":21,"r3":34},
 "2026-09-12": {"r1":14,"r2":22,"r4":17},
 "2026-09-13": {"r1":10,"r2":22,"r4":16,"r5":30},
 "2026-09-15": {"r1":12,"r3":31,"r4":18},
 "2026-09-16": {"r1":15,"r2":24,"r4":17},
 "2026-09-17": {"r1":11,"r2":24,"r3":34,"r4":18},
 "2026-09-18": {"r2":23,"r3":30,"r4":20},
 "2026-09-19": {"r1":14,"r2":22,"r4":17},
 "2026-09-21": {"r1":14,"r2":25,"r3":30},
 "2026-09-22": {"r1":12,"r2":23,"r3":30,"r4":20},
 "2026-09-23": {"r1":15,"r3":32,"r4":15},
 "2026-09-24": {"r1":13,"r2":24,"r4":20},
 "2026-09-26": {"r1":14,"r2":21,"r4":15,"r5":25},
 "2026-09-27": {"r1":10,"r2":20,"r5":25},
 "2026-09-28": {"r1":11,"r2":22,"r3":33,"r4":20},
 "2026-09-29": {"r1":14,"r3":30,"r4":19},
 "2026-09-30": {"r1":15,"r2":23,"r3":32,"r4":18},
 "2026-10-01": {"r1":12,"r2":21,"r4":19},
 "2026-10-02": {"r1":15,"r2":24,"r3":34,"r4":15},
 "2026-10-03": {"r1":14,"r2":23},
 "2026-10-04": {"r2":20,"r4":19},
 "2026-10-05": {"r1":14,"r3":35,"r4":17},
 "2026-10-06": {"r1":11,"r2":23,"r3":34,"r4":16},
 "2026-10-07": {"r1":12,"r2":25}
};

const WD = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
const WD_SHORT = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const WORDS = ['zero','one','two','three','four','five','six','seven','eight','nine','ten'];
const w = n => (WORDS[n] || String(n));
const cap = s => s.charAt(0).toUpperCase() + s.slice(1);

const GLYPH_PATTERNS = [
  [6, 9, 12], [12, 6, 9], [9, 12, 6], [6, 12, 6], [12, 9, 6], [9, 6, 12]
];

const WZ_OPTIONS = [
  {id: 'w1', name: 'Twelve-minute walk', cat: 'Body',  freq: 'daily', mins: 12},
  {id: 'w2', name: 'Evening pages',      cat: 'Mind',  freq: 'daily', mins: 12},
  {id: 'w3', name: 'Room reset',         cat: 'Craft', freq: 'daily', mins: 10}
];

/* ---------------- date helpers (UTC, deterministic) ---------------- */
const pad2 = n => String(n).padStart(2, '0');
const dateOf = iso => new Date(iso + 'T00:00:00Z');
const isoOf = d => d.getUTCFullYear() + '-' + pad2(d.getUTCMonth() + 1) + '-' + pad2(d.getUTCDate());
function addDays(iso, n) { const d = dateOf(iso); d.setUTCDate(d.getUTCDate() + n); return isoOf(d); }
const dowMon = iso => (dateOf(iso).getUTCDay() + 6) % 7;   // 0 = Monday
function fmtShort(iso) { const d = dateOf(iso); return d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()].slice(0, 3); }
function fmtLong(iso) { const d = dateOf(iso); return WD[d.getUTCDay()] + ' ' + d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()]; }
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/* ---------------- state ---------------- */
function defaultState() {
  return {
    rituals: [
      {id: 'r1', name: 'Morning stretch', cat: 'Body',  freq: 'daily',    mins: 10, remind: true,  glyph: 0},
      {id: 'r2', name: 'Read 20 pages',  cat: 'Mind',  freq: 'daily',    mins: 20, remind: true,  glyph: 1},
      {id: 'r3', name: 'Evening walk',   cat: 'Body',  freq: 'weekdays', mins: 30, remind: false, glyph: 2},
      {id: 'r4', name: 'Journal',        cat: 'Mind',  freq: 'daily',    mins: 15, remind: true,  glyph: 3},
      {id: 'r5', name: 'Piano practice', cat: 'Craft', freq: 'weekends', mins: 25, remind: false, glyph: 4}
    ],
    logs: JSON.parse(JSON.stringify(FIXTURE_LOGS)),
    notes: {},
    prefs: {remind: true, goal: 45},
    wizardDone: false,
    nextRitualId: 6
  };
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (raw) {
      const o = JSON.parse(raw);
      if (o && Array.isArray(o.rituals) && o.logs && o.prefs) {
        if (!o.notes) o.notes = {};
        if (!o.nextRitualId) o.nextRitualId = 100;
        return o;
      }
    }
  } catch (e) { /* fall back to fixtures */ }
  return defaultState();
}
function saveState() {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(S)); } catch (e) { /* private mode */ }
}

let S = loadState();
let filter = '';
let pagerPage = 0;
let logTarget = null;
let detailsTarget = null;
let removed = null;
let wizard = {step: 1, choice: 'w1'};

/* ---------------- queries ---------------- */
const applicable = (r, ds) => {
  const d = dateOf(ds).getUTCDay();
  if (r.freq === 'daily') return true;
  if (r.freq === 'weekdays') return d >= 1 && d <= 5;
  return d === 0 || d === 6;
};
const loggedOn = (r, ds) => !!(S.logs[ds] && S.logs[ds][r.id] != null);
const minutesOn = ds => {
  const o = S.logs[ds]; if (!o) return 0;
  let n = 0; for (const k in o) n += o[k];
  return n;
};
const weekSums = () => { const out = []; for (let i = 0; i < 7; i++) out.push(minutesOn(addDays(WEEK_START, i))); return out; };
const last7 = () => { const out = []; for (let i = 6; i >= 0; i--) out.push({date: addDays(TODAY, -i), mins: minutesOn(addDays(TODAY, -i))}); return out; };
function streak() {
  let day = TODAY, n = 0;
  if (minutesOn(TODAY) === 0) day = addDays(TODAY, -1);
  while (minutesOn(day) > 0) { n++; day = addDays(day, -1); }
  return n;
}
function ritualStatus(r) {
  let any = false;
  for (const ds in S.logs) { if (S.logs[ds][r.id] != null) { any = true; break; } }
  if (!any) return 'ontrack';   /* no history yet — nothing to slip */
  let missed = 0;
  for (let i = 1; i <= 7; i++) { const ds = addDays(TODAY, -i); if (applicable(r, ds) && !loggedOn(r, ds)) missed++; }
  return missed >= 2 ? 'slipping' : 'ontrack';
}
const totalLogs = () => { let n = 0; for (const ds in S.logs) n += Object.keys(S.logs[ds]).length; return n; };
const totalMinutes = () => { let n = 0; for (const ds in S.logs) n += minutesOn(ds); return n; };

/* ---------------- marks overlay ---------------- */
const markedSelector = '[data-improvised],[data-adapted],[data-fallback]';
function injectMarkLabels() {
  document.querySelectorAll(markedSelector).forEach(el => {
    const makeLbl = () => {
      const type = el.hasAttribute('data-improvised') ? 'improvised'
                 : el.hasAttribute('data-adapted') ? 'adapted' : 'fallback';
      const note = el.getAttribute('data-note') || '';
      const lbl = document.createElement('span');
      lbl.className = 'mark-lbl';
      lbl.textContent = type + (note ? ' · ' + note : '');
      return lbl;
    };
    if (el.tagName === 'INPUT' || el.tagName === 'SELECT') {
      if (el.nextElementSibling && el.nextElementSibling.classList.contains('mark-lbl')) return;
      if (el.parentElement) el.parentElement.style.position = 'relative';
      el.insertAdjacentElement('afterend', makeLbl());
    } else {
      if (el.querySelector(':scope > .mark-lbl')) return;
      el.appendChild(makeLbl());
    }
  });
}

/* ---------------- render: today ---------------- */
function glyphHTML(r) {
  const pat = GLYPH_PATTERNS[(r.glyph || 0) % GLYPH_PATTERNS.length];
  return '<span class="glyph" data-adapted data-note="icon → rhythm glyph" aria-hidden="true">' +
    pat.map(h => '<i style="height:' + h + 'px"></i>').join('') + '</span>';
}
function renderToday() {
  const appl = S.rituals.filter(r => applicable(r, TODAY)).length;
  const logged = S.rituals.filter(r => applicable(r, TODAY) && loggedOn(r, TODAY)).length;
  const head = document.getElementById('today-headline');
  head.textContent = appl === 0 ? 'Nothing scheduled today.'
    : logged === appl ? cap(w(appl)) + ' of ' + w(appl) + ' — the day is kept.'
    : cap(w(logged)) + ' of ' + w(appl) + ' rituals logged.';

  const pct = appl ? Math.round(100 * logged / appl) : 0;
  const meter = document.getElementById('meter-fill');
  meter.style.width = pct + '%';
  const pb = meter.parentElement;
  pb.setAttribute('aria-valuemin', '0');
  pb.setAttribute('aria-valuemax', '100');
  pb.setAttribute('aria-valuenow', String(pct));
  document.getElementById('meter-readout').textContent =
    logged + ' of ' + appl + ' rituals · ' + minutesOn(TODAY) + ' minutes logged';

  const sums = weekSums();
  const elapsed = dowMon(TODAY) + 1;
  let weekTotal = 0; for (let i = 0; i < elapsed; i++) weekTotal += sums[i];
  document.getElementById('week-notice-text').textContent =
    'Week to date — ' + weekTotal + ' minutes over ' + w(elapsed) + ' days. ' +
    'Today counts ' + minutesOn(TODAY) + '; the streak stands at ' + streak() + '.';

  const q = filter.trim().toLowerCase();
  let list = S.rituals.slice();
  if (q) list = list.filter(r => r.name.toLowerCase().includes(q) || r.cat.toLowerCase().includes(q));

  const listEl = document.getElementById('ritual-list');
  listEl.innerHTML = list.map(r => {
    const st = ritualStatus(r);
    let actions;
    if (!applicable(r, TODAY)) {
      actions = '<span class="rstate off">Not scheduled today</span>';
    } else if (loggedOn(r, TODAY)) {
      actions = '<span class="rstate" data-adapted data-note="celebration → static flip (L-03)">Logged · ' +
                (S.logs[TODAY][r.id]) + ' min</span>';
    } else {
      actions = '<button class="btn b-navy" data-log="' + r.id + '">Log</button>';
    }
    return '<li class="rrow" id="row-' + r.id + '">' +
      glyphHTML(r) +
      '<span class="rname">' + esc(r.name) + '</span>' +
      '<span class="rmeta">' + r.mins + ' min · ' + r.freq + '</span>' +
      '<span class="tag">' + esc(r.cat) + '</span>' +
      (st === 'slipping' ? '<span class="tag attn">Slipping</span>' : '<span class="tag">On track</span>') +
      '<span class="ractions">' + actions +
      '<button class="btn b-txt" data-details="' + r.id + '">Details</button></span>' +
      '</li>';
  }).join('');

  const empty = document.getElementById('empty-state');
  if (list.length === 0) {
    const clearBtn = document.getElementById('empty-clear');
    if (q) {
      document.getElementById('empty-line').textContent = 'Nothing matches \u201C' + filter.trim() + '\u201D. The filter is exact; try fewer words.';
      clearBtn.textContent = 'Clear search';
    } else {
      document.getElementById('empty-line').textContent = 'No rituals yet. The list is yours to fill.';
      clearBtn.textContent = 'Run setup';
    }
    empty.hidden = false;
  } else {
    empty.hidden = true;
  }
  if (document.body.classList.contains('marks-on')) injectMarkLabels();
}

/* ---------------- render: history ---------------- */
function renderHistory() {
  const sums = weekSums();
  const maxV = Math.max.apply(null, sums.concat([1]));
  const todayIdx = dowMon(TODAY);
  let area = '', days = '';
  for (let i = 0; i < 7; i++) {
    const ds = addDays(WEEK_START, i);
    const v = sums[i];
    const past = i <= todayIdx;
    const isToday = i === todayIdx;
    const h = past ? Math.max(4, Math.round(4 + 112 * v / maxV)) : 2;
    area += '<div class="barcol"><span class="vlab">' + (past ? v : '\u00B7') + '</span>' +
            '<span class="bar' + (isToday ? ' today' : '') + (past ? '' : ' future') + '" data-value="' + v + '" style="height:' + h + 'px"></span></div>';
    days += '<span>' + WD_SHORT[i].slice(0, 3) + ' ' + dateOf(ds).getUTCDate() + '</span>';
  }
  document.getElementById('chart-area').innerHTML = area;
  document.getElementById('chart-days').innerHTML = days;
  let weekTotal = 0, loggedDays = 0;
  for (let i = 0; i <= todayIdx; i++) { weekTotal += sums[i]; if (sums[i] > 0) loggedDays++; }
  document.getElementById('bar-note').textContent =
    weekTotal + ' minutes logged so far this week (' + loggedDays + ' of ' + (todayIdx + 1) + ' days with a log). Today is the red bar.';

  /* month grid */
  let head = '';
  for (const l of ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']) head += '<span>' + l + '</span>';
  document.getElementById('mgrid-head').innerHTML = head;
  let cells = '';
  let cursor = '2026-09-28';
  const end = '2026-11-01';
  while (cursor <= end) {
    const d = dateOf(cursor);
    const outside = d.getUTCMonth() !== 9;
    const m = minutesOn(cursor);
    let cls = 'mcell';
    if (outside) cls += ' outside';
    else if (cursor === TODAY) cls += ' todayc';
    else if (m === 0) cls += ' emptyc';
    else if (m <= 39) cls += ' i1';
    else if (m <= 69) cls += ' i2';
    else cls += ' i3';
    const title = fmtLong(cursor) + ' — ' + (m ? m + ' minutes' : 'no log');
    cells += '<span class="' + cls + '" data-date="' + cursor + '" data-min="' + m + '" title="' + title + '"></span>';
    cursor = addDays(cursor, 1);
  }
  document.getElementById('month-grid').innerHTML = cells;

  /* sparkline */
  const l7 = last7();
  const sMax = Math.max.apply(null, l7.map(x => x.mins).concat([1]));
  document.getElementById('spark-main').innerHTML = l7.map(x => {
    const h = x.mins ? Math.max(3, Math.round(24 * x.mins / sMax)) : 2;
    return '<i class="' + (x.mins ? '' : 'zero') + '" style="height:' + h + 'px" data-value="' + x.mins + '" title="' + fmtShort(x.date) + ' — ' + x.mins + ' min"></i>';
  }).join('');
  let sTotal = 0; l7.forEach(x => sTotal += x.mins);
  document.getElementById('spark-readout').textContent = sTotal + ' minutes over the last seven days.';

  /* ledger */
  const entries = [];
  Object.keys(S.logs).sort().reverse().forEach(ds => {
    const o = S.logs[ds];
    S.rituals.forEach(r => { if (o[r.id] != null) entries.push({ds: ds, r: r, mins: o[r.id], notes: S.notes[ds + '|' + r.id] || ''}); });
  });
  document.getElementById('ledger-sub').textContent = entries.length + ' entries, newest first.';
  const PAGE = 8;
  const pages = Math.max(1, Math.ceil(entries.length / PAGE));
  if (pagerPage > pages - 1) pagerPage = pages - 1;
  const slice = entries.slice(pagerPage * PAGE, pagerPage * PAGE + PAGE);
  document.getElementById('ledger-body').innerHTML = slice.map(e =>
    '<tr><td data-l="Date">' + fmtShort(e.ds) + ' ' + dateOf(e.ds).getUTCFullYear() + '</td>' +
    '<td class="rname-cell" data-l="Ritual">' + esc(e.r.name) + '</td>' +
    '<td class="num" data-l="Minutes">' + e.mins + '</td>' +
    '<td data-l="Notes">' + (e.notes ? esc(e.notes) : '\u2014') + '</td></tr>').join('');
  document.getElementById('pg-readout').textContent = 'Page ' + (pagerPage + 1) + ' of ' + pages;
  document.getElementById('pg-newer').disabled = pagerPage === 0;
  document.getElementById('pg-older').disabled = pagerPage >= pages - 1;
}

/* ---------------- render: achievements ---------------- */
function renderAchievements() {
  const st = streak();
  document.getElementById('streak-num').textContent = st;
  const anchor = minutesOn(TODAY) > 0 ? TODAY : addDays(TODAY, -1);
  const start = addDays(anchor, -(st - 1));
  document.getElementById('streak-note').textContent =
    st > 0 ? 'The run began ' + fmtLong(start) + ' and holds through today.' : 'No run yet — one log starts it.';
  const tl = totalLogs();
  const badges = [
    {label: '7 Days',   earned: st >= 7,  note: st >= 7 ? 'Earned ' + fmtShort(addDays(TODAY, -(st - 7))) + '.' : st + ' of 7.'},
    {label: '30 Days',  earned: st >= 30, note: st >= 30 ? 'Earned.' : st + ' of 30.'},
    {label: '150 Logs', earned: tl >= 150, note: tl >= 150 ? 'Earned.' : tl + ' of 150.'}
  ];
  document.getElementById('badges').innerHTML = badges.map(b =>
    '<div class="badge' + (b.earned ? ' earned' : '') + '" data-improvised data-note="no badge canon">' +
    '<span class="b-stamp">' + b.label + '</span><span class="b-note">' + b.note + '</span></div>').join('');
}

/* ---------------- render: settings ---------------- */
function renderSettings() {
  document.getElementById('pref-remind').checked = !!S.prefs.remind;
  document.getElementById('pref-goal').value = S.prefs.goal;
  document.getElementById('goal-readout').textContent = S.prefs.goal + ' min';
  document.getElementById('order-list').innerHTML = S.rituals.map((r, i) =>
    '<li>' + glyphHTML(r) + '<span class="rname">' + esc(r.name) + '</span>' +
    '<span class="mv">' +
    '<button class="btn b-txt" data-move="-1" data-id="' + r.id + '"' + (i === 0 ? ' disabled' : '') + '>Move up</button>' +
    '<button class="btn b-txt" data-move="1" data-id="' + r.id + '"' + (i === S.rituals.length - 1 ? ' disabled' : '') + '>Move down</button>' +
    '</span></li>').join('');
  document.getElementById('marks-list').innerHTML = S.rituals.map(r =>
    '<li>' + glyphHTML(r) + '<span class="rname">' + esc(r.name) + '</span>' +
    '<button class="btn b-txt" data-mark="' + r.id + '">Next mark</button></li>').join('');
}

function renderAll() {
  renderToday();
  renderHistory();
  renderAchievements();
  renderSettings();
  if (document.body.classList.contains('marks-on')) injectMarkLabels();
}

/* ---------------- notices ---------------- */
function showNotice(label, text) {
  document.getElementById('log-notice-lab').textContent = label;
  document.getElementById('log-notice-text').textContent = text;
  document.getElementById('log-notice').hidden = false;
}
function showSetup(text) {
  document.getElementById('setup-notice-text').textContent = text;
  document.getElementById('setup-notice').hidden = false;
}

/* ---------------- log flow ---------------- */
function openLog(id) {
  const r = S.rituals.find(x => x.id === id);
  if (!r) return;
  logTarget = r;
  document.getElementById('log-title').textContent = 'Log — ' + r.name;
  document.getElementById('log-sub').textContent = r.mins + ' min target · ' + r.freq + '.';
  document.getElementById('log-date').value = TODAY;
  document.getElementById('log-mins').value = r.mins;
  document.getElementById('log-notes').value = '';
  document.getElementById('save-readout').textContent = '';
  const save = document.getElementById('log-save');
  save.disabled = false;
  save.textContent = 'Save log';
  document.getElementById('log-cancel').textContent = 'Cancel';
  document.getElementById('log-panel').hidden = false;
}
function initLog() {
  document.getElementById('log-save').addEventListener('click', () => {
    if (!logTarget) return;
    const ds = document.getElementById('log-date').value || TODAY;
    const minsInput = document.getElementById('log-mins');
    const errEl = document.getElementById('log-mins-err');
    const m = parseInt(minsInput.value, 10);
    if (!m || m < 1) {
      errEl.hidden = false;
      minsInput.setAttribute('aria-invalid', 'true');
      return;
    }
    errEl.hidden = true;
    minsInput.removeAttribute('aria-invalid');
    const notes = document.getElementById('log-notes').value.trim();
    const rt = document.getElementById('save-readout');
    rt.textContent = 'Saving…';
    document.getElementById('log-save').disabled = true;
    const r = logTarget;
    window.setTimeout(() => {
      S.logs[ds] = S.logs[ds] || {};
      S.logs[ds][r.id] = m;
      if (notes) S.notes[ds + '|' + r.id] = notes; else delete S.notes[ds + '|' + r.id];
      saveState();
      rt.textContent = 'Saved · ' + m + ' min';
      document.getElementById('log-save').textContent = 'Saved';
      document.getElementById('log-cancel').textContent = 'Close';
      showNotice('Logged', r.name + ', ' + m + ' minutes on ' + fmtShort(ds) +
        '. The streak stands at ' + streak() + ' days.');
      renderAll();
    }, 700);
  });
  document.getElementById('log-cancel').addEventListener('click', () => {
    document.getElementById('log-panel').hidden = true;
    logTarget = null;
  });
}

/* ---------------- details flow ---------------- */
function openDetails(id) {
  const r = S.rituals.find(x => x.id === id);
  if (!r) return;
  detailsTarget = r;
  document.getElementById('details-title').textContent = r.name;
  document.getElementById('confirm-zone').hidden = true;
  document.getElementById('remove-start').hidden = false;
  renderDetailsBody();
  document.getElementById('details-panel').hidden = false;
}
function renderDetailsBody() {
  const r = detailsTarget;
  if (!r) return;
  let count = 0, mins = 0;
  for (const ds in S.logs) { if (S.logs[ds][r.id] != null) { count++; mins += S.logs[ds][r.id]; } }
  const spark = [];
  for (let i = 6; i >= 0; i--) { const ds = addDays(TODAY, -i); spark.push({d: ds, v: (S.logs[ds] && S.logs[ds][r.id]) || 0}); }
  const mx = Math.max.apply(null, spark.map(s => s.v).concat([1]));
  const bars = spark.map(s => '<i class="' + (s.v ? '' : 'zero') + '" style="height:' + (s.v ? Math.max(3, Math.round(24 * s.v / mx)) : 2) + 'px" data-value="' + s.v + '" title="' + fmtShort(s.d) + ' — ' + s.v + ' min"></i>').join('');
  document.getElementById('details-body').innerHTML =
    '<div class="drow"><span class="dk">Category</span><span class="dv"><span class="tag" id="d-cat-tag">' + esc(r.cat) + '</span></span>' +
      '<span class="dedit" data-fallback data-note="platform select"><select id="d-cat" aria-label="Category">' +
      ['Body', 'Mind', 'Craft'].map(c => '<option' + (c === r.cat ? ' selected' : '') + '>' + c + '</option>').join('') +
      '</select></span></div>' +
    '<div class="drow"><span class="dk">Frequency</span><span class="dv" id="d-freq-v">' + r.freq + '</span>' +
      '<span class="dedit radio-set" data-fallback data-note="platform radios">' +
      [['daily', 'Daily'], ['weekdays', 'Weekdays'], ['weekends', 'Weekends']].map(o =>
        '<label class="radio-row"><input type="radio" name="d-freq" value="' + o[0] + '"' + (r.freq === o[0] ? ' checked' : '') + '> ' + o[1] + '</label>').join('') +
      '</span></div>' +
    '<div class="drow"><span class="dk">Reminders</span><span class="dv" id="d-rem-v">' + (r.remind ? 'On' : 'Off') + '</span>' +
      '<span class="dedit" data-fallback data-note="platform checkbox"><label class="check-row"><input type="checkbox" id="d-rem"' + (r.remind ? ' checked' : '') + '> Remind me about this ritual</label></span></div>' +
    '<div class="drow"><span class="dk">Target</span><span class="dv">' + r.mins + ' min · ' + r.freq + '</span></div>' +
    '<div class="drow"><span class="dk">Record</span><span class="dv">' + count + ' logs · ' + mins + ' minutes</span></div>' +
    '<div class="drow"><span class="dk">Last seven days</span><span class="spark">' + bars + '</span></div>';

  const sel = document.getElementById('d-cat');
  if (sel) sel.addEventListener('change', () => {
    r.cat = sel.value; saveState(); afterDetailEdit('Category set to ' + sel.value + '.');
  });
  document.querySelectorAll('#details-body .radio-set input').forEach(inp => inp.addEventListener('change', () => {
    r.freq = inp.value; saveState(); afterDetailEdit('Frequency set to ' + inp.value + '.');
  }));
  const rem = document.getElementById('d-rem');
  if (rem) rem.addEventListener('change', () => {
    r.remind = rem.checked; saveState(); afterDetailEdit('Reminders ' + (rem.checked ? 'on' : 'off') + '.');
  });
  if (document.body.classList.contains('marks-on')) injectMarkLabels();
}
function afterDetailEdit(msg) {
  renderAll();
  renderDetailsBody();
  showNotice('Updated', msg);
}
function initDetails() {
  document.getElementById('details-close').addEventListener('click', () => {
    document.getElementById('details-panel').hidden = true;
    detailsTarget = null;
  });
  document.getElementById('remove-start').addEventListener('click', () => {
    document.getElementById('confirm-zone').hidden = false;
    document.getElementById('remove-start').hidden = true;
  });
  document.getElementById('confirm-keep').addEventListener('click', () => {
    document.getElementById('confirm-zone').hidden = true;
    document.getElementById('remove-start').hidden = false;
  });
  document.getElementById('confirm-remove').addEventListener('click', () => {
    if (!detailsTarget) return;
    const r = detailsTarget;
    const idx = S.rituals.indexOf(r);
    removed = {ritual: r, index: idx};
    S.rituals.splice(idx, 1);
    saveState();
    document.getElementById('details-panel').hidden = true;
    detailsTarget = null;
    document.getElementById('undo-text').textContent = r.name + ' removed. Its log was set aside with it.';
    document.getElementById('undo-notice').hidden = false;
    showNotice('Removed', r.name + ' left the list. Undo below restores it.');
    renderAll();
  });
  document.getElementById('undo-btn').addEventListener('click', () => {
    if (!removed) return;
    const at = Math.min(removed.index, S.rituals.length);
    S.rituals.splice(at, 0, removed.ritual);
    document.getElementById('undo-notice').hidden = true;
    showNotice('Restored', removed.ritual.name + ' is back on the list.');
    removed = null;
    saveState();
    renderAll();
  });
}

/* ---------------- wizard (fallback: in-flow steps) ---------------- */
function openWizard() {
  wizard = {step: 1, choice: 'w1'};
  document.getElementById('wizard-panel').hidden = false;
  renderWizard();
}
function renderWizard() {
  document.getElementById('wizard-steplab').textContent = 'Step ' + wizard.step + ' of 3';
  const titleEl = document.getElementById('wizard-title');
  const bodyEl = document.getElementById('wizard-body');
  const actEl = document.getElementById('wizard-actions');
  if (wizard.step === 1) {
    titleEl.textContent = 'A quiet tracker for small rituals.';
    bodyEl.innerHTML = '<p>Cadence keeps one page a day: what you did, how long, and how the week is going.</p>' +
      '<p>No noise, no trophies — just the count, kept honestly.</p>';
    actEl.innerHTML = '<button class="btn b-txt" id="wz-skip">Skip setup</button>' +
      '<button class="btn b-navy" id="wz-next">Next</button>';
  } else if (wizard.step === 2) {
    titleEl.textContent = 'Choose a first ritual.';
    bodyEl.innerHTML = '<div class="radio-set">' + WZ_OPTIONS.map(o =>
      '<label class="radio-row"><input type="radio" name="wz-ritual" value="' + o.id + '"' + (wizard.choice === o.id ? ' checked' : '') + '> ' +
      esc(o.name) + ' · ' + o.mins + ' min</label>').join('') + '</div>';
    actEl.innerHTML = '<button class="btn b-txt" id="wz-back">Back</button>' +
      '<button class="btn b-navy" id="wz-next">Next</button>';
  } else {
    titleEl.textContent = 'Set a daily goal.';
    bodyEl.innerHTML = '<p>A target for the day, in minutes.</p>' +
      '<div class="srow"><input type="range" id="wz-goal" min="10" max="120" step="5" value="' + S.prefs.goal + '">' +
      '<span class="readout" id="wz-goal-readout">' + S.prefs.goal + ' min</span></div>';
    actEl.innerHTML = '<button class="btn b-txt" id="wz-back">Back</button>' +
      '<button class="btn b-navy" id="wz-finish">Finish setup</button>';
  }
  const skip = document.getElementById('wz-skip');
  if (skip) skip.addEventListener('click', () => {
    S.wizardDone = true; saveState();
    document.getElementById('wizard-panel').hidden = true;
    showSetup('Setup skipped. The fixture rituals stay in place.');
    renderAll();
  });
  const next = document.getElementById('wz-next');
  if (next) next.addEventListener('click', () => {
    if (wizard.step === 2) {
      const sel = document.querySelector('input[name="wz-ritual"]:checked');
      if (sel) wizard.choice = sel.value;
    }
    wizard.step++; renderWizard();
  });
  const back = document.getElementById('wz-back');
  if (back) back.addEventListener('click', () => { wizard.step--; renderWizard(); });
  const goal = document.getElementById('wz-goal');
  if (goal) goal.addEventListener('input', () => {
    document.getElementById('wz-goal-readout').textContent = goal.value + ' min';
  });
  const finish = document.getElementById('wz-finish');
  if (finish) finish.addEventListener('click', () => {
    const opt = WZ_OPTIONS.find(o => o.id === wizard.choice) || WZ_OPTIONS[0];
    S.prefs.goal = parseInt(document.getElementById('wz-goal').value, 10) || S.prefs.goal;
    if (!S.rituals.some(r => r.name === opt.name)) {
      S.rituals.push({id: 'r' + S.nextRitualId, name: opt.name, cat: opt.cat, freq: opt.freq,
                      mins: opt.mins, remind: true, glyph: S.rituals.length % GLYPH_PATTERNS.length});
      S.nextRitualId++;
    }
    S.wizardDone = true;
    saveState();
    document.getElementById('wizard-panel').hidden = true;
    showSetup(opt.name + ' is on your list.');
    renderAll();
  });
}

/* ---------------- view switching ---------------- */
function showView(name) {
  document.querySelectorAll('.view').forEach(v => { v.hidden = v.id !== 'view-' + name; });
  document.querySelectorAll('.tab').forEach(t => {
    const on = t.dataset.view === name;
    t.classList.toggle('on', on);
    if (on) t.setAttribute('aria-current', 'page'); else t.removeAttribute('aria-current');
  });
  if (name === 'today') renderToday();
}

/* ---------------- wiring ---------------- */
function init() {
  document.getElementById('tabs').addEventListener('click', e => {
    const b = e.target.closest('.tab');
    if (b) showView(b.dataset.view);
  });
  document.getElementById('search').addEventListener('input', e => { filter = e.target.value; renderToday(); });
  document.getElementById('empty-clear').addEventListener('click', () => {
    if (filter.trim()) {
      filter = '';
      document.getElementById('search').value = '';
      renderToday();
    } else {
      showView('today');
      openWizard();
    }
  });
  document.getElementById('ritual-list').addEventListener('click', e => {
    const logBtn = e.target.closest('[data-log]');
    if (logBtn) { openLog(logBtn.dataset.log); return; }
    const detBtn = e.target.closest('[data-details]');
    if (detBtn) { openDetails(detBtn.dataset.details); return; }
  });
  document.getElementById('order-list').addEventListener('click', e => {
    const b = e.target.closest('[data-move]');
    if (!b) return;
    const i = S.rituals.findIndex(r => r.id === b.dataset.id);
    const j = i + parseInt(b.dataset.move, 10);
    if (i < 0 || j < 0 || j >= S.rituals.length) return;
    const t = S.rituals[i]; S.rituals[i] = S.rituals[j]; S.rituals[j] = t;
    saveState(); renderAll();
  });
  document.getElementById('marks-list').addEventListener('click', e => {
    const b = e.target.closest('[data-mark]');
    if (!b) return;
    const r = S.rituals.find(x => x.id === b.dataset.mark);
    if (!r) return;
    r.glyph = ((r.glyph || 0) + 1) % GLYPH_PATTERNS.length;
    saveState(); renderAll();
  });
  document.getElementById('pg-newer').addEventListener('click', () => { pagerPage--; renderHistory(); });
  document.getElementById('pg-older').addEventListener('click', () => { pagerPage++; renderHistory(); });
  document.getElementById('pref-remind').addEventListener('change', e => { S.prefs.remind = e.target.checked; saveState(); });
  document.getElementById('pref-goal').addEventListener('input', e => {
    S.prefs.goal = parseInt(e.target.value, 10);
    document.getElementById('goal-readout').textContent = S.prefs.goal + ' min';
    saveState();
  });
  document.getElementById('export-csv').addEventListener('click', () => {
    const rows = [['date', 'ritual', 'minutes', 'notes']];
    Object.keys(S.logs).sort().forEach(ds => {
      S.rituals.forEach(r => {
        const m = S.logs[ds][r.id];
        if (m != null) rows.push([ds, r.name, m, S.notes[ds + '|' + r.id] || '']);
      });
    });
    const csv = rows.map(row => row.map(v => {
      const s = String(v);
      return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
    }).join(',')).join('\n');
    const blob = new Blob([csv], {type: 'text/csv'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'cadence-log.csv';
    document.body.appendChild(a); a.click(); a.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  document.getElementById('run-setup').addEventListener('click', () => {
    showView('today');
    openWizard();
  });
  document.getElementById('reset-demo').addEventListener('click', () => {
    try { localStorage.removeItem(STORE_KEY); } catch (e) { /* ignore */ }
    location.reload();
  });
  const mt = document.getElementById('marks-toggle');
  mt.addEventListener('click', () => {
    const on = document.body.classList.toggle('marks-on');
    mt.setAttribute('aria-pressed', String(on));
    if (on) injectMarkLabels();
  });

  initLog();
  initDetails();

  renderAll();
  if (!S.wizardDone) openWizard();

  window.__cadence = {
    state: () => S,
    weekSums: weekSums,
    last7: last7,
    streak: streak,
    totalLogs: totalLogs,
    totalMinutes: totalMinutes,
    minutesOn: minutesOn,
    showView: showView,
    render: renderAll,
    fmtShort: fmtShort
  };
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
else init();

/* ============ lens: provenance inspector (marks layer companion) ============
   With marks on, clicking a dashed node opens its decision record:
   outcome - authority record - precedents - fallback - candidate - gap -
   independent verification. Registry: PROV in provenance.js (generated by
   _evidence/make_provenance_js.py). */
(function () {
  var provPanel, provKindEl, provRowEl, provBody, provFoot, provLastNode = null;

  function escHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function kindOf(node) {
    var attrs = ["improvised", "adapted", "fallback"];
    for (var i = 0; i < attrs.length; i++) {
      if (node.hasAttribute("data-" + attrs[i])) return attrs[i];
    }
    return "improvised";
  }

  document.body.insertAdjacentHTML("beforeend",
    '<aside id="provPanel" role="region" aria-label="Decision provenance" hidden>' +
    '<header class="prov-head"><span class="prov-kind" id="provKind">improvised</span>' +
    '<span class="prov-rowtag" id="provRow">ask</span>' +
    '<button id="provClose" class="prov-close" aria-label="Close provenance">\u2715</button></header>' +
    '<div class="prov-body" id="provBody"></div>' +
    '<footer class="prov-foot" id="provFoot"></footer></aside>');
  provPanel = document.getElementById("provPanel");
  provKindEl = document.getElementById("provKind");
  provRowEl = document.getElementById("provRow");
  provBody = document.getElementById("provBody");
  provFoot = document.getElementById("provFoot");

  /* ---- independent verification results (fetched, not bundled) ---- */
  var verifData = null, verifTried = false;
  function loadVerification() {
    if (verifData || verifTried) return;
    verifTried = true;
    fetch("_evidence/verification/leader-verification.json")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { verifData = d; if (d && provLastNode && !provPanel.hidden) openProv(provLastNode); })
      .catch(function () {});
  }
  function verificationBlock(node) {
    var h = '<p class="prov-sec">independent verification</p>';
    h += '<p class="prov-line prov-src">tools/da_verify.py \u2014 file, DOM, computed-style and behavioural evidence; claims are not evidence. These results ship inside the artifact \u2014 re-run the verifier to confirm.</p>';
    if (!verifData) {
      if (!verifTried) loadVerification();
      h += '<p class="prov-line prov-src">' + (verifTried ? "results not published for this serve" : "loading\u2026") + '</p>';
      return h;
    }
    var s = verifData.summary || {};
    var bad = s.VIOLATION || 0;
    h += '<p class="prov-line">this build: <b>' + (s.PASS || 0) + '</b> verified' +
         (bad ? ' \u00b7 <b class="prov-viol">' + bad + ' violations</b>' : ' \u00b7 no violations') +
         (s.REVIEW_REQUIRED ? ' \u00b7 ' + s.REVIEW_REQUIRED + ' open to human review' : '') + '</p>';
    if (verifData.covers) {
      h += '<p class="prov-line prov-src">covers ' +
           Object.keys(verifData.covers).map(function (k) { return k + "@" + verifData.covers[k]; }).join(' \u00b7 ') + '</p>';
    }
    var matched = (verifData.checks || []).filter(function (c) {
      if (!c.selector) return false;
      try {
        return node.matches(c.selector) || node.querySelectorAll(c.selector).length > 0;
      } catch (e) { return false; }
    }).slice(0, 6);
    if (matched.length) {
      h += '<ul class="prov-list">';
      matched.forEach(function (c) {
        var icon = ({ PASS: "\u2713", VIOLATION: "\u2715", UNVERIFIABLE: "?", REVIEW_REQUIRED: "\u25cc" })[c.status] || "\u00b7";
        var cls = c.status === "VIOLATION" ? "prov-viol" : (c.status === "PASS" ? "prov-pass" : "prov-src");
        h += '<li><span class="' + cls + '">' + icon + " " + escHtml(c.status) + "</span> \u2014 " + escHtml(c.title || c.id) +
             (c.observed && c.observed.length ? ' <span class="prov-src">(' + escHtml(String(c.observed[0]).slice(0, 90)) + ")</span>" : "") + "</li>";
      });
      h += "</ul>";
    } else {
      h += '<p class="prov-line prov-src">no direct check targets this element</p>';
    }
    return h;
  }

  function closeProv() { if (provPanel && !provPanel.hidden) provPanel.hidden = true; }
  function chip(t) { return '<span class="prov-chip">' + escHtml(t) + '</span>'; }
  function pid(t) { return '<span class="prov-id">' + escHtml(t) + '</span>'; }

  function recFor(node) {
    var holder = node.closest("[data-note]") || node;
    var note = holder.getAttribute("data-note");
    var key = note && PROV.byNote ? PROV.byNote[note] : null;
    return { key: note, rec: key ? PROV.rows[key] : null, note: note };
  }

  function openProv(node) {
    if (typeof PROV === "undefined") return;
    provLastNode = node;
    var found = recFor(node);
    var rec = found.rec;
    var kind = kindOf(node);

    provKindEl.textContent = kind;
    provRowEl.textContent = rec ? ("ask #" + rec.n) : "no record";

    var h = "";
    if (!rec) {
      h = '<p class="prov-line">' + (found.key ? "No registry entry for " + pid(found.key) + "." : "This node is not keyed to a decision record.") + "</p>";
    } else {
      h += '<p class="prov-ask">' + escHtml(rec.ask) + "</p>";
      if (found.note) h += '<p class="prov-note">the label says: \u201c' + escHtml(found.note) + '\u201d</p>';

      h += '<p class="prov-sec">decision</p><p class="prov-line"><span class="prov-outcome">' + escHtml(rec.outcome) + "</span>";
      if (rec.resolution) h += " resolved by " + pid(rec.resolution);
      else if (rec.closest) h += " closest: " + pid(rec.closest);
      h += "</p>";

      if (rec.built) h += '<p class="prov-line prov-built">' + escHtml(rec.built) + "</p>";

      var art = rec.resolution && PROV.artifacts[rec.resolution];
      if (art) {
        h += '<p class="prov-sec">authority record</p>';
        h += '<p class="prov-line"><b>' + escHtml(art.title) + "</b> " + pid(art.id) + "</p>";
        if (art.summary) h += '<p class="prov-line">' + escHtml(art.summary) + "</p>";
        if (art.source_path) h += '<p class="prov-line prov-src">provenance: ' + escHtml(art.source_path) + "</p>";
        if (art.compiled_from && art.compiled_from.length) {
          h += '<p class="prov-line">compiled from ' + art.compiled_from.map(chip).join(" ") + "</p>";
        }
      }

      (rec.precedents || []).forEach(function (p) {
        var live = PROV.precedents[p];
        var dead = PROV.retired && PROV.retired[p];
        h += '<p class="prov-sec">precedent</p>';
        if (live) {
          h += '<p class="prov-line"><b>' + escHtml(live.title) + "</b> " + pid(p) + "</p>";
          if (live.reason) h += '<p class="prov-line">' + escHtml(live.reason) + "</p>";
          if (live.try && live.try.length) {
            h += '<p class="prov-line">try-list followed:</p><ul class="prov-list">' +
                 live.try.map(function (t) { return "<li>" + escHtml(t) + "</li>"; }).join("") + "</ul>";
          }
          if (live.citation) h += '<p class="prov-line prov-src">' + escHtml(live.citation) + "</p>";
        } else if (dead) {
          h += '<p class="prov-line"><b>' + escHtml(dead.title) + "</b> " + chip(dead.now) + "</p>";
          h += '<p class="prov-line">' + escHtml(dead.note) + "</p>";
        } else {
          h += '<p class="prov-line">' + pid(p) + "</p>";
        }
        var v = rec.precedent_verdicts && rec.precedent_verdicts[p];
        if (v) h += '<p class="prov-line">scope verdict: ' + chip(v + " - not governed; proceed as marked improvisation") + "</p>";
      });
      if (!(rec.precedents || []).length && rec.precedents_raw && rec.precedents_raw !== "\u2014") {
        h += '<p class="prov-sec">precedent</p><p class="prov-line">' + escHtml(rec.precedents_raw) + "</p>";
      }

      if (rec.outcome === "FALLBACK") {
        var fb = PROV.fallbacks[rec.resolution];
        if (fb) {
          h += '<p class="prov-sec">fallback record</p>';
          h += '<p class="prov-line"><b>' + escHtml(fb.title) + "</b> " + pid(fb.id) + "</p>";
          if (fb.statement) h += '<p class="prov-line">' + escHtml(fb.statement) + "</p>";
          if (fb.constraints && fb.constraints.length) {
            h += '<ul class="prov-list">' + fb.constraints.map(function (c) { return "<li>" + escHtml(c) + "</li>"; }).join("") + "</ul>";
          }
        }
      }

      if (rec.candidate && PROV.candidates[rec.candidate]) {
        var c = PROV.candidates[rec.candidate];
        h += '<p class="prov-sec">candidate \u2014 provisional, not authority</p>';
        h += '<p class="prov-line"><b>' + escHtml(c.title) + "</b> " + pid(c.id) + " " + chip("provisional") + "</p>";
        if (c.summary) h += '<p class="prov-line">' + escHtml(c.summary) + "</p>";
        if (c.promote_when && c.promote_when.length) {
          h += '<p class="prov-line">promote when:</p><ul class="prov-list">' +
               c.promote_when.map(function (t) { return "<li>" + escHtml(t) + "</li>"; }).join("") + "</ul>";
        }
      }

      if (rec.gap && PROV.gaps[rec.gap]) {
        var g = PROV.gaps[rec.gap];
        h += '<p class="prov-sec">gap filed</p>';
        h += '<p class="prov-line">' + pid(g.id) + " " + chip(g.status || "open") + "</p>";
        if (g.need) h += '<p class="prov-line">' + escHtml(g.need) + "</p>";
        var ctx = g.context || {};
        if (ctx.searched && ctx.searched.length) h += '<p class="prov-line prov-src">searched: ' + ctx.searched.map(chip).join(" ") + "</p>";
        if (ctx.note) h += '<p class="prov-line">' + escHtml(ctx.note) + "</p>";
      }

      h += verificationBlock(node);
    }
    provBody.innerHTML = h;

    var f = ['<a href="NOTES.md" target="_blank" rel="noopener">NOTES.md</a>'];
    if (rec && rec.resolve_line) f.push('<a href="_evidence/resolves.jsonl" target="_blank" rel="noopener">resolves.jsonl \u00b7 line ' + rec.resolve_line + "</a>");
    if (rec && rec.gap) f.push('<a href=".design-authority/gaps.jsonl" target="_blank" rel="noopener">gaps.jsonl</a>');
    if (verifData) f.push('<a href="_evidence/verification/leader-verification.json" target="_blank" rel="noopener">verification JSON</a>');
    provFoot.innerHTML = "evidence: " + f.join(" \u00b7 ");
    provPanel.hidden = false;
  }

  /* capture-phase: with marks on, a click on a marked node opens its record
     instead of performing the node's action; everything else passes through */
  document.addEventListener("click", function (ev) {
    if (!document.body.classList.contains("marks-on")) return;
    var t = ev.target;
    if (!t || !t.closest) return;
    if (t.closest("#provPanel")) return;
    var node = t.closest("[data-note],[data-improvised],[data-adapted],[data-fallback]");
    if (!node) return;
    ev.preventDefault();
    ev.stopPropagation();
    openProv(node);
  }, true);

  document.getElementById("provClose").addEventListener("click", closeProv);
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" && !provPanel.hidden) closeProv();
  });
  document.addEventListener("close", function (ev) {
    if (ev.target && ev.target.tagName === "DIALOG" && provPanel.parentNode === ev.target) {
      document.body.appendChild(provPanel);
    }
  }, true);

  /* #lens deep link - enable the marks layer on load (retries while the app boots) */
  if (/lens/i.test(location.hash || "")) {
    var lensTries = 6;
    (function lensBoot() {
      var mt = document.getElementById("marks-toggle");
      if (mt && !document.body.classList.contains("marks-on")) mt.click();
      if (--lensTries > 0 && !document.body.classList.contains("marks-on")) {
        setTimeout(lensBoot, 350);
      }
    })();
  }
})();
