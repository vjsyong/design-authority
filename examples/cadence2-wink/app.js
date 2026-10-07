/* ==========================================================================
   Cadence — rebuilt against the wink Design Authority (packs/wink).
   Vanilla JS SPA. No network calls anywhere: fonts are local, everything
   else is fixtures + localStorage.
   ========================================================================== */

'use strict';

/* ---------------------------------------------------------------- fixtures */

const ICONS = { run: 'i-run', read: 'i-read', meditate: 'i-meditate', sugar: 'i-sugar', guitar: 'i-guitar' };

const FIXTURE_RITUALS = [
  { id: 'run',     name: 'Morning run',    cat: 'Movement',   minutes: 30, icon: 'i-run',      streak: 12, done: true,  spark: [30, 30, 0, 30, 45, 30, 30] },
  { id: 'read',    name: 'Read 20 pages',  cat: 'Mind',       minutes: 20, icon: 'i-read',     streak: 9,  done: true,  spark: [20, 0, 20, 20, 20, 20, 20] },
  { id: 'meditate',name: 'Meditate',       cat: 'Mind',       minutes: 10, icon: 'i-meditate', streak: 14, done: true,  spark: [10, 10, 10, 0, 10, 10, 10] },
  { id: 'sugar',   name: 'No sugar',       cat: 'Discipline', minutes: 0,  icon: 'i-sugar',    streak: 5,  done: false, spark: [1, 1, 0, 1, 1, 1, 1] },
  { id: 'guitar',  name: 'Practice guitar',cat: 'Craft',      minutes: 25, icon: 'i-guitar',   streak: 3,  done: false, spark: [25, 0, 25, 25, 0, 25, 25] }
];

const WEEK_MIN = [
  { day: 'Mon', v: 45 }, { day: 'Tue', v: 30 }, { day: 'Wed', v: 60 }, { day: 'Thu', v: 25 },
  { day: 'Fri', v: 50 }, { day: 'Sat', v: 0 }, { day: 'Sun', v: 35 }
];
const WEEK_TODAY = 'Tue';

/* October heatmap fixture: 31 fixed values (minutes). Oct 1 = Wed in this world. */
const HM_VALUES = [
  0, 18, 30, 22, 40, 12, 0,
  25, 35, 20, 0, 45, 30, 10,
  0, 28, 50, 18, 32, 0, 20,
  42, 25, 0, 15, 38, 22, 30,
  0, 26, 34
];

const FIXTURE_ENTRIES = [
  { d: 'Tue 7 Oct',  iso: '2026-10-07', ritual: 'Morning run',     minutes: 30, note: 'Legs felt heavy, went anyway.',       status: 'Done' },
  { d: 'Tue 7 Oct',  iso: '2026-10-07', ritual: 'Read 20 pages',   minutes: 20, note: 'Chapter four, kitchen table.',        status: 'Done' },
  { d: 'Tue 7 Oct',  iso: '2026-10-07', ritual: 'Meditate',        minutes: 10, note: '',                                    status: 'Done' },
  { d: 'Mon 6 Oct',  iso: '2026-10-06', ritual: 'Practice guitar', minutes: 25, note: 'Barre chords, slowly.',               status: 'Done' },
  { d: 'Mon 6 Oct',  iso: '2026-10-06', ritual: 'No sugar',        minutes: 0,  note: '',                                    status: 'Done' },
  { d: 'Sun 5 Oct',  iso: '2026-10-05', ritual: 'Morning run',     minutes: 30, note: '',                                    status: 'Done' },
  { d: 'Sun 5 Oct',  iso: '2026-10-05', ritual: 'Read 20 pages',   minutes: 20, note: '',                                    status: 'Done' },
  { d: 'Sat 4 Oct',  iso: '2026-10-04', ritual: 'Practice guitar', minutes: 0,  note: 'Strings felt wrong; left it.',        status: 'Skipped' },
  { d: 'Sat 4 Oct',  iso: '2026-10-04', ritual: 'Meditate',        minutes: 10, note: 'Ten quiet minutes.',                  status: 'Done' },
  { d: 'Fri 3 Oct',  iso: '2026-10-03', ritual: 'Morning run',     minutes: 45, note: 'Long loop by the river.',             status: 'Done' },
  { d: 'Fri 3 Oct',  iso: '2026-10-03', ritual: 'No sugar',        minutes: 0,  note: '',                                    status: 'Done' },
  { d: 'Thu 2 Oct',  iso: '2026-10-02', ritual: 'Read 20 pages',   minutes: 20, note: '',                                    status: 'Done' },
  { d: 'Thu 2 Oct',  iso: '2026-10-02', ritual: 'Practice guitar', minutes: 25, note: '',                                    status: 'Done' },
  { d: 'Wed 1 Oct',  iso: '2026-10-01', ritual: 'Meditate',        minutes: 0,  note: 'Fell asleep instead. Tomorrow?',      status: 'Skipped' },
  { d: 'Wed 1 Oct',  iso: '2026-10-01', ritual: 'Morning run',     minutes: 30, note: '',                                    status: 'Done' },
  { d: 'Tue 30 Sep', iso: '2026-09-30', ritual: 'Read 20 pages',   minutes: 20, note: '',                                    status: 'Done' },
  { d: 'Tue 30 Sep', iso: '2026-09-30', ritual: 'No sugar',        minutes: 0,  note: 'Office birthday cake. Watched.',      status: 'Done' },
  { d: 'Mon 29 Sep', iso: '2026-09-29', ritual: 'Morning run',     minutes: 30, note: '',                                    status: 'Done' },
  { d: 'Mon 29 Sep', iso: '2026-09-29', ritual: 'Meditate',        minutes: 10, note: '',                                    status: 'Done' },
  { d: 'Sun 28 Sep', iso: '2026-09-28', ritual: 'Practice guitar', minutes: 25, note: '',                                    status: 'Done' },
  { d: 'Sun 28 Sep', iso: '2026-09-28', ritual: 'Read 20 pages',   minutes: 0,  note: 'Life happened.',                      status: 'Skipped' },
  { d: 'Sat 27 Sep', iso: '2026-09-27', ritual: 'Morning run',     minutes: 30, note: '',                                    status: 'Done' },
  { d: 'Sat 27 Sep', iso: '2026-09-27', ritual: 'No sugar',        minutes: 0,  note: '',                                    status: 'Done' },
  { d: 'Fri 26 Sep', iso: '2026-09-26', ritual: 'Meditate',        minutes: 10, note: 'Park bench, five minutes of it.',     status: 'Done' }
];

const BADGES_EARNED = [
  { name: 'First week',  icon: 'i-cal',   meta: 'Earned 1 Oct' },
  { name: '10 days',     icon: 'i-flame', meta: 'Earned 6 Oct' },
  { name: 'Early bird',  icon: 'i-sun',   meta: 'Earned 30 Sep' },
  { name: 'Century club',icon: 'i-medal', meta: 'Earned 2 Oct' }
];
const BADGES_LOCKED = [
  { name: '21 days',     icon: 'i-medal', meta: 'Locked · 12 of 21' },
  { name: 'Perfect month', icon: 'i-cal', meta: 'Locked · 17 of 31 days' }
];

const STORAGE_KEY = 'cadence2-wink';
const SAVE_MS = 700;           /* simulated saving state */
const PAGE_SIZE = 8;

/* ------------------------------------------------------------------ state */

let state = null;
let page = 0;
let query = '';
let deletedBuffer = null;      /* last deleted ritual for Undo */

function freshState() {
  return {
    rituals: FIXTURE_RITUALS.map(r => Object.assign({}, r)),
    entries: FIXTURE_ENTRIES.map(e => Object.assign({}, e)),
    settings: { name: 'Sam', goal: 30, dark: false, remAM: true, remPM: true, weekStart: 'monday', category: 'Movement' },
    seenIntro: false
  };
}

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const saved = JSON.parse(raw);
      const s = freshState();
      if (Array.isArray(saved.rituals)) s.rituals = saved.rituals;
      if (Array.isArray(saved.entries)) s.entries = saved.entries;
      Object.assign(s.settings, saved.settings || {});
      s.seenIntro = !!saved.seenIntro;
      return s;
    }
  } catch (e) { /* storage unavailable — run from fixtures */ }
  return freshState();
}

function save() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) { /* ignore */ }
}

/* ------------------------------------------------------------------ utils */

const $ = (sel, root) => (root || document).querySelector(sel);
const $$ = (sel, root) => Array.prototype.slice.call((root || document).querySelectorAll(sel));

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
function svgIcon(id, cls) {
  return '<svg class="ic ' + (cls || '') + '" aria-hidden="true"><use href="#' + id + '"/></svg>';
}

/* ------------------------------------------------------------------ toasts */

function toast(text, opts) {
  opts = opts || {};
  const el = document.createElement('div');
  el.className = 'toast';
  el.setAttribute('role', 'status');
  const span = document.createElement('span');
  span.innerHTML = text;
  el.appendChild(span);
  let timer = null;
  function leave() {
    if (!el.parentNode) return;
    el.classList.add('leaving');
    setTimeout(() => el.remove(), 220);
  }
  if (opts.actionLabel && typeof opts.action === 'function') {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'cta outline small';
    btn.textContent = opts.actionLabel;
    btn.addEventListener('click', () => { clearTimeout(timer); leave(); opts.action(); });
    el.appendChild(btn);
  }
  $('#toasts').appendChild(el);
  timer = setTimeout(leave, opts.timeout || 2800);
}

/* --------------------------------------------------------------- overlays */

const overlayStack = [];

function openOverlay(id, trigger) {
  const el = document.getElementById(id);
  if (!el || !el.hidden) return;
  el.hidden = false;
  overlayStack.push({ el: el, trigger: trigger || document.activeElement });
  const focusable = $('[data-close], button, input, select, textarea', el);
  if (focusable) focusable.focus();
}
function closeOverlay(id) {
  const el = document.getElementById(id);
  if (!el || el.hidden) return;
  el.hidden = true;
  for (let i = overlayStack.length - 1; i >= 0; i--) {
    if (overlayStack[i].el === el) {
      const t = overlayStack[i].trigger;
      overlayStack.splice(i, 1);
      if (t && t.focus) t.focus();
      break;
    }
  }
}
function closeTopOverlay() {
  const top = overlayStack[overlayStack.length - 1];
  if (top) closeOverlay(top.el.id);
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeTopOverlay(); });

document.addEventListener('click', e => {
  const closer = e.target.closest('[data-close]');
  if (closer) { const ov = closer.closest('.overlay'); if (ov && ov.id !== 'overlay-wizard') closeOverlay(ov.id); }
});

/* confirm dialog — W-16 primitives: rounded dialog, consequence sentence,
   confirm = ink pill with the concrete verb, cancel = outline pill, never pre-focused */
let confirmYesHandler = null;
function openConfirm(opts) {
  $('#confirmTitle').textContent = opts.title;
  $('#confirmCopy').textContent = opts.copy;
  const yes = $('#confirmYes');
  yes.textContent = opts.confirmLabel;
  confirmYesHandler = opts.onYes;
  openOverlay('overlay-confirm');
  $('#confirmNo').focus(); /* destructive is never the default focus */
}
$('#confirmYes').addEventListener('click', () => {
  closeOverlay('overlay-confirm');
  const fn = confirmYesHandler; confirmYesHandler = null;
  if (fn) fn();
});
$('#confirmNo').addEventListener('click', () => closeOverlay('overlay-confirm'));

/* --------------------------------------------------------------- views/nav */

function goto(view) {
  $$('.view').forEach(sec => { sec.hidden = sec.id !== 'view-' + view; });
  $$('[data-goto]').forEach(btn => {
    if (btn.dataset.goto === view) btn.setAttribute('aria-current', 'page');
    else btn.removeAttribute('aria-current');
  });
  document.body.dataset.view = view;
  window.scrollTo(0, 0);
}
$$('[data-goto]').forEach(btn => btn.addEventListener('click', () => goto(btn.dataset.goto)));

/* --------------------------------------------------------------- the ring */

const RING_C = 2 * Math.PI * 60;

function renderRing() {
  const total = state.rituals.length || 1;
  const done = state.rituals.filter(r => r.done).length;
  const p = done / total;
  const arc = $('#ringArc');
  arc.style.strokeDasharray = (p * RING_C).toFixed(1) + ' ' + RING_C.toFixed(1);
  arc.classList.toggle('complete', p >= 1);
  $('#ringCount').textContent = done + ' of ' + total;
  $('#heroReadout').textContent = done + ' of ' + total + ' rituals done';
  $('#ringSvg').setAttribute('aria-label', done + ' of ' + total + ' rituals done today');
  const pill = $('#statusPill');
  const onTrack = done >= 3;
  pill.textContent = onTrack ? 'On track' : 'Slipping';
  pill.className = 'pill ' + (onTrack ? 'positive' : 'attention');
}
$('#ringSvg');

/* ------------------------------------------------------------ celebrations */

function celebrate(x, y) {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const colors = ['#FFE01B', '#241C15', '#E7B75F'];
  for (let i = 0; i < 10; i++) {
    const dot = document.createElement('span');
    dot.className = 'burst-dot';
    const angle = (-90 + (i - 4.5) * 20) * Math.PI / 180;
    const dist = 44 + (i % 3) * 16;
    dot.style.left = (x - 4) + 'px';
    dot.style.top = (y - 4) + 'px';
    dot.style.background = colors[i % colors.length];
    dot.style.setProperty('--dx', (Math.cos(angle) * dist).toFixed(1) + 'px');
    dot.style.setProperty('--dy', (Math.sin(angle) * dist).toFixed(1) + 'px');
    dot.style.animationDelay = (i * 12) + 'ms';
    document.body.appendChild(dot);
    setTimeout(() => dot.remove(), 1000);
  }
  const wrap = $('.ring-wrap');
  wrap.classList.remove('celebrate');
  void wrap.offsetWidth;
  wrap.classList.add('celebrate');
}

/* ------------------------------------------------------------ ritual list */

function renderRituals() {
  const list = $('#ritualList');
  list.innerHTML = '';
  state.rituals.forEach(r => {
    const li = document.createElement('li');
    li.className = 'ritual-row' + (r.done ? ' done' : '');
    li.dataset.id = r.id;
    li.draggable = true;
    li.tabIndex = 0;
    li.setAttribute('role', 'button');
    li.setAttribute('aria-label', r.name + ' — open details');
    li.innerHTML =
      '<span class="handle" title="Drag to reorder" data-improvised="drag to reorder: no reorder canon; handle + drop tint">' + svgIcon('i-drag') + '</span>' +
      '<span class="icon-well" data-improvised="ritual icons: no icon canon — drawn to palette">' + svgIcon(r.icon) + '</span>' +
      '<span class="ritual-main"><span class="ritual-name">' + esc(r.name) + '</span>' +
      '<span class="pill neutral" data-adapted="category tag: badge form, neutral parsnip fill (yellow reserved — W-06/W-21)">' + esc(r.cat) + '</span></span>' +
      '<span class="chip">' + svgIcon('i-flame') + esc(r.streak) + '</span>' +
      '<button class="check" type="button" aria-pressed="' + (r.done ? 'true' : 'false') + '" aria-label="Mark ' + esc(r.name) + ' ' + (r.done ? 'not done' : 'done') + '">' + svgIcon('i-check') + '</button>';
    list.appendChild(li);
  });
}

/* check-off: ring + toast + celebration (spec) */
$('#ritualList').addEventListener('click', e => {
  const row = e.target.closest('.ritual-row');
  if (!row) return;
  const r = state.rituals.find(x => x.id === row.dataset.id);
  if (!r) return;
  if (e.target.closest('.check')) {
    const checkEl = e.target.closest('.check');
    const rect = checkEl.getBoundingClientRect();
    r.done = !r.done;
    save();
    renderRituals();
    renderRing();
    if (r.done) {
      celebrate(rect.left + rect.width / 2, rect.top + rect.height / 2);
      const fresh = $('.ritual-row[data-id="' + r.id + '"] .check');
      if (fresh) fresh.classList.add('pop');
      toast('Logged &#10003; &mdash; ' + esc(r.name) + (r.minutes ? ', ' + r.minutes + ' min' : '') + '.');
    }
    return;
  }
  if (e.target.closest('.handle')) return;
  openDetail(r.id);
});

/* drag to reorder (marked: no reorder canon) */
let dragArmed = false;
let dragJustEnded = false;
$('#ritualList').addEventListener('pointerdown', e => {
  dragArmed = !!e.target.closest('.handle');
});
$('#ritualList').addEventListener('dragstart', e => {
  const row = e.target.closest('.ritual-row');
  if (!row || !dragArmed) { e.preventDefault(); return; }
  row.classList.add('dragging');
  e.dataTransfer.setData('text/plain', row.dataset.id);
  e.dataTransfer.effectAllowed = 'move';
});
$('#ritualList').addEventListener('dragover', e => {
  const row = e.target.closest('.ritual-row');
  if (!row) return;
  e.preventDefault();
  $$('.ritual-row.drop-target', $('#ritualList')).forEach(x => x.classList.remove('drop-target'));
  row.classList.add('drop-target');
});
$('#ritualList').addEventListener('drop', e => {
  e.preventDefault();
  const row = e.target.closest('.ritual-row');
  const id = e.dataTransfer.getData('text/plain');
  if (!row || !id) return;
  const from = state.rituals.findIndex(x => x.id === id);
  const to = state.rituals.findIndex(x => x.id === row.dataset.id);
  if (from < 0 || to < 0 || from === to) return;
  const item = state.rituals.splice(from, 1)[0];
  state.rituals.splice(to, 0, item);
  save();
  renderRituals();
  renderRing();
});
$('#ritualList').addEventListener('dragend', e => {
  const row = e.target.closest('.ritual-row');
  if (row) row.classList.remove('dragging');
  $$('.ritual-row.drop-target', $('#ritualList')).forEach(x => x.classList.remove('drop-target'));
  dragJustEnded = true;
  setTimeout(() => { dragJustEnded = false; }, 80);
});
$('#ritualList').addEventListener('keydown', e => {
  const row = e.target.closest('.ritual-row');
  if (!row) return;
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openDetail(row.dataset.id); }
});

/* ------------------------------------------------------------ detail overlay */

function sparklineSVG(values) {
  const W = 440, H = 64, P = 8;
  const max = Math.max.apply(null, values.concat([1]));
  const n = values.length;
  const pts = values.map((v, i) => {
    const x = P + i * ((W - 2 * P) / (n - 1));
    const y = H - P - (v / max) * (H - 2 * P);
    return [x.toFixed(1), y.toFixed(1)];
  });
  const last = pts[pts.length - 1];
  return '<svg class="sparkline" viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none" aria-hidden="true">' +
    '<polyline points="' + pts.map(p => p[0] + ',' + p[1]).join(' ') + '"/>' +
    '<circle cx="' + last[0] + '" cy="' + last[1] + '" r="4"/></svg>';
}

function openDetail(id) {
  if (dragJustEnded) return;
  const r = state.rituals.find(x => x.id === id);
  if (!r) return;
  const recent = state.entries.filter(e => e.ritual === r.name).slice(0, 3);
  const body = $('#detailBody');
  body.innerHTML =
    '<div class="detail-head"><span class="icon-well" data-improvised="ritual icons: no icon canon — drawn to palette">' + svgIcon(r.icon) + '</span>' +
    '<h3 class="detail-name" id="detailTitle">' + esc(r.name) + '</h3></div>' +
    '<div class="detail-sub"><span class="pill neutral">' + esc(r.cat) + '</span>' +
    '<span class="chip">' + svgIcon('i-flame') + esc(r.streak) + ' days</span></div>' +
    '<div class="detail-streak"><span class="streak-num">' + r.streak + '</span><span class="streak-label">day streak</span></div>' +
    '<div class="spark-card" data-improvised="sparkline: ink line, 7-day trend (no chart canon)"><span class="label">Last 7 days</span>' + sparklineSVG(r.spark) + '</div>' +
    '<p class="label" style="margin-bottom:2px">Recent entries</p>' +
    '<ul class="mini-list">' + (recent.length ? recent.map(e =>
      '<li><span>' + esc(e.d) + ' &middot; ' + esc(e.note || 'No note') + '</span><span class="ml-meta">' + (e.minutes ? e.minutes + ' min' : '—') + '</span></li>'
    ).join('') : '<li><span>Nothing logged yet. First one today?</span><span class="ml-meta">—</span></li>') + '</ul>' +
    '<div class="dialog-actions">' +
    '<button class="cta outline danger" type="button" id="detailDelete" data-improvised="destructive: outline pill in error ink; routes to confirm dialog (W-16)">Delete ritual</button>' +
    '<button class="cta outline" type="button" data-close>Close</button>' +
    '</div>';
  openOverlay('overlay-detail');
  const del = $('#detailDelete');
  if (del) del.addEventListener('click', () => {
    openConfirm({
      title: 'Delete \u201C' + r.name + '\u201D?',
      copy: 'It leaves your list and its ' + r.streak + '-day streak resets. You can undo this for a few seconds after.',
      confirmLabel: 'Delete ritual',
      onYes: () => {
        const idx = state.rituals.findIndex(x => x.id === r.id);
        deletedBuffer = { ritual: r, index: idx };
        state.rituals.splice(idx, 1);
        save();
        closeOverlay('overlay-detail');
        renderRituals();
        renderRing();
        toast('Deleted \u201C' + esc(r.name) + '\u201D.', {
          actionLabel: 'Undo', timeout: 6000,
          action: () => {
            if (!deletedBuffer) return;
            state.rituals.splice(deletedBuffer.index, 0, deletedBuffer.ritual);
            deletedBuffer = null;
            save();
            renderRituals();
            renderRing();
            toast('Restored &#10003; &mdash; \u201C' + esc(r.name) + '\u201D.');
          }
        });
      }
    });
  });
}

/* legacy helper kept for clarity: overlay openers */
$('#openLog').addEventListener('click', () => openLogForm());
$('#openNew').addEventListener('click', () => openOverlay('overlay-new'));

/* --------------------------------------------------------------- log form */

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function openLogForm() {
  const sel = $('#logRitual');
  sel.innerHTML = state.rituals.map(r =>
    '<option value="' + r.id + '">' + esc(r.name) + (r.minutes ? ' · ' + r.minutes + ' min' : '') + '</option>').join('');
  const first = state.rituals[0];
  $('#logMinutes').value = first ? (first.minutes || 0) : 30;
  $('#logDate').value = '2026-10-07';
  $('#logNotes').value = '';
  openOverlay('overlay-log');
}
$('#logRitual').addEventListener('change', () => {
  const r = state.rituals.find(x => x.id === $('#logRitual').value);
  if (r) $('#logMinutes').value = r.minutes || 0;
});
$$('.stepper-btn').forEach(btn => btn.addEventListener('click', () => {
  const input = $('#logMinutes');
  const step = parseInt(btn.dataset.step, 10);
  const v = (parseInt(input.value, 10) || 0) + step;
  input.value = Math.max(0, Math.min(240, v));
}));

function savingButton(btn, done) {
  if (!btn.dataset.label) btn.dataset.label = $('.btn-label', btn) ? $('.btn-label', btn).textContent : btn.textContent;
  if (!done) {
    btn.classList.add('is-saving');
    btn.innerHTML = '<span class="spinner"></span><span class="btn-label">Saving\u2026</span>';
  } else {
    btn.classList.remove('is-saving');
    btn.innerHTML = '<span class="btn-label">' + btn.dataset.label + '</span>';
  }
}

$('#logForm').addEventListener('submit', e => {
  e.preventDefault();
  const btn = $('#logSave');
  const r = state.rituals.find(x => x.id === $('#logRitual').value);
  const mins = parseInt($('#logMinutes').value, 10) || 0;
  const iso = $('#logDate').value || '2026-10-07';
  const note = $('#logNotes').value.trim();
  savingButton(btn, false);
  setTimeout(() => {                       /* simulated saving state (~700 ms) */
    savingButton(btn, true);
    const d = parseInt(iso.slice(8, 10), 10);
    const m = parseInt(iso.slice(5, 7), 10);
    state.entries.unshift({
      d: d + ' ' + MONTHS[m - 1], iso: iso, ritual: r ? r.name : 'Ritual', minutes: mins, note: note, status: 'Done'
    });
    save();
    renderEntries();
    closeOverlay('overlay-log');
    toast('Logged &#10003; &mdash; ' + esc(r ? r.name : 'ritual') + (mins ? ', ' + mins + ' min' : '') + '.');
  }, SAVE_MS);
});

/* -------------------------------------------------------------- new ritual */

$('#newPhoto').addEventListener('change', e => {
  const file = e.target.files && e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    const prev = $('#newPhotoPreview');
    prev.hidden = false;
    prev.innerHTML = '<img alt="Ritual photo preview" src="' + reader.result + '">';
  };
  reader.readAsDataURL(file);
});

$('#newForm').addEventListener('submit', e => {
  e.preventDefault();
  const field = $('#newNameField');
  const input = $('#newName');
  const err = $('#newNameError');
  const name = input.value.trim();
  if (!name) { /* field error state (W-12: border + message in #BF4055) */
    field.classList.add('invalid');
    err.hidden = false;
    input.setAttribute('aria-invalid', 'true');
    input.focus();
    return;
  }
  field.classList.remove('invalid');
  err.hidden = true;
  input.removeAttribute('aria-invalid');
  const cat = $('#newCategory').value;
  const icon = cat === 'Movement' ? 'i-run' : cat === 'Craft' ? 'i-guitar' : cat === 'Discipline' ? 'i-sugar' : 'i-read';
  const btn = $('#newSave');
  savingButton(btn, false);
  setTimeout(() => {
    savingButton(btn, true);
    state.rituals.push({
      id: 'r' + Date.now(), name: name, cat: cat, minutes: 15, icon: icon,
      streak: 0, done: false, spark: [0, 0, 0, 0, 0, 0, 0]
    });
    save();
    renderRituals();
    renderRing();
    closeOverlay('overlay-new');
    input.value = '';
    $('#newPhotoPreview').hidden = true;
    toast('Added &#10003; &mdash; \u201C' + esc(name) + '\u201D is on the list.');
  }, SAVE_MS);
});

/* ----------------------------------------------------------------- history */

function barLevel(v) { return v === 0 ? 0 : v < 60 ? 1 : 2; }

function renderBars() {
  const max = 60;
  $('#barChart').innerHTML = WEEK_MIN.map(d =>
    '<div class="bar-col' + (d.day === WEEK_TODAY ? ' today' : '') + '">' +
    '<span class="bar-val">' + (d.v || '') + '</span>' +
    '<div class="bar' + (d.v === 0 ? ' zero' : '') + (d.day === WEEK_TODAY ? ' today' : '') + '" style="height:' + Math.round((d.v / max) * 100) + '%" title="' + d.day + ' · ' + d.v + ' min"></div>' +
    '<span class="bar-day">' + d.day + '</span>' +
    '</div>').join('');
}

function renderHeatmap() {
  const heads = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
  let html = heads.map(h => '<span class="hm-head">' + h + '</span>').join('');
  const startCol = 2; /* Oct 1 lands on Wednesday in this fixture world */
  for (let i = 0; i < startCol; i++) html += '<span class="hm-blank"></span>';
  HM_VALUES.forEach((v, i) => {
    const day = i + 1;
    const lv = v === 0 ? 0 : v < 20 ? 1 : v < 40 ? 2 : v < 55 ? 3 : 4;
    html += '<span class="hm-cell' + (lv ? ' lv' + lv : '') + (day === 7 ? ' today' : '') + '" title="' + day + ' Oct · ' + (v ? v + ' min' : 'nothing logged') + '"></span>';
  });
  $('#heatmap').innerHTML = html;
}

const newerBtn = document.createElement('button');
newerBtn.type = 'button';
newerBtn.className = 'link';
newerBtn.id = 'newerBtn';
newerBtn.hidden = true;
newerBtn.innerHTML = '&#8592; Newer';
newerBtn.dataset.improvised = 'pagination: \u2018Newer entries\u2019 link (no pagination canon)';

function statusPill(status) {
  const cls = status === 'Skipped' ? 'attention' : 'neutral';
  return '<span class="pill ' + cls + '">' + esc(status) + '</span>';
}

function renderEntries() {
  const foot = $('.table-foot');
  if (!newerBtn.parentNode) foot.insertBefore(newerBtn, $('#entriesRange'));
  let rows = state.entries;
  if (query) {
    const q = query.toLowerCase();
    rows = rows.filter(e => (e.d + ' ' + e.ritual + ' ' + e.note + ' ' + e.status).toLowerCase().indexOf(q) !== -1);
    newerBtn.hidden = true;
    $('#olderBtn').hidden = true;
    $('#entriesRange').textContent = rows.length + (rows.length === 1 ? ' match' : ' matches');
  } else {
    const pages = Math.max(1, Math.ceil(rows.length / PAGE_SIZE));
    if (page >= pages) page = pages - 1;
    const start = page * PAGE_SIZE;
    rows = rows.slice(start, start + PAGE_SIZE);
    newerBtn.hidden = page === 0;
    $('#olderBtn').hidden = page >= pages - 1;
    $('#entriesRange').textContent = (start + 1) + '\u2013' + (start + rows.length) + ' of ' + state.entries.length;
  }
  $('#entriesBody').innerHTML = rows.length ? rows.map(e =>
    '<tr><td>' + esc(e.d) + '</td><td>' + esc(e.ritual) + '</td><td>' + (e.minutes ? esc(e.minutes) + ' min' : '&mdash;') + '</td>' +
    '<td class="notes">' + (e.note ? esc(e.note) : '&mdash;') + '</td><td>' + statusPill(e.status) + '</td></tr>').join('')
    : '<tr><td colspan="5">Nothing matches yet &mdash; try a different word?</td></tr>';
}

$('#entriesSearch').addEventListener('input', e => { query = e.target.value; page = 0; renderEntries(); });
$('#olderBtn').addEventListener('click', () => { page++; renderEntries(); });
newerBtn.addEventListener('click', () => { page = Math.max(0, page - 1); renderEntries(); });

/* ------------------------------------------------------------------ badges */

function renderBadges() {
  const tile = (b, locked) =>
    '<div class="badge-tile' + (locked ? ' locked' : '') + '">' +
    '<span class="medal' + (locked ? ' locked' : '') + '">' + svgIcon(locked ? 'i-lock' : b.icon) + '</span>' +
    '<span class="bt-name">' + esc(b.name) + '</span><span class="bt-meta">' + esc(b.meta) + '</span></div>';
  $('#badgeGrid').innerHTML =
    BADGES_EARNED.map(b => tile(b, false)).join('') +
    BADGES_LOCKED.map(b => tile(b, true)).join('');
}

$('#emptyToggle').addEventListener('click', () => {
  const on = $('#emptyPanel').hidden;
  $('#emptyPanel').hidden = !on;
  $('#badgeGrid').hidden = on;
  $('#emptyToggle').setAttribute('aria-pressed', on ? 'true' : 'false');
  $('#emptyToggle').textContent = on ? 'demo: badges' : 'demo: empty state';
});

/* ---------------------------------------------------------------- settings */

function applySettings() {
  const s = state.settings;
  $('#greetName').textContent = s.name || 'Sam';
  $('#setName').value = s.name || 'Sam';
  $('#setCategory').value = s.category;
  $('#setGoal').value = s.goal;
  $('#goalOut').textContent = s.goal + ' min';
  $('#remAM').checked = !!s.remAM;
  $('#remPM').checked = !!s.remPM;
  $('#darkToggle').checked = !!s.dark;
  document.body.classList.toggle('dark', !!s.dark);
  const radios = $$('input[name="weekStart"]');
  radios.forEach(r => { r.checked = r.value === s.weekStart; });
}

$('#setGoal').addEventListener('input', () => { $('#goalOut').textContent = $('#setGoal').value + ' min'; });
$('#wizGoal').addEventListener('input', () => { $('#wizGoalOut').textContent = $('#wizGoal').value + ' min'; });
$('#darkToggle').addEventListener('change', () => {
  state.settings.dark = $('#darkToggle').checked;
  document.body.classList.toggle('dark', state.settings.dark);
  save();
});

$('#settingsForm').addEventListener('submit', e => {
  e.preventDefault();
  const btn = $('#saveSettings');
  savingButton(btn, false);
  setTimeout(() => {                       /* simulated saving state (~700 ms) */
    savingButton(btn, true);
    const s = state.settings;
    s.name = $('#setName').value.trim() || 'Sam';
    s.category = $('#setCategory').value;
    s.goal = parseInt($('#setGoal').value, 10);
    s.remAM = $('#remAM').checked;
    s.remPM = $('#remPM').checked;
    s.dark = $('#darkToggle').checked;
    const week = $$('input[name="weekStart"]').find(r => r.checked);
    s.weekStart = week ? week.value : 'monday';
    save();
    applySettings();
    toast('Saved &#10003;');
  }, SAVE_MS);
});

$('#replayIntro').addEventListener('click', () => openWizard(0));

/* --------------------------------------------------------------- csv export */

function exportCSV() {
  const head = ['date', 'ritual', 'minutes', 'notes', 'status'];
  const lines = [head.join(',')];
  state.entries.forEach(e => {
    lines.push([e.d, e.ritual, e.minutes, e.note, e.status].map(v => {
      const s = String(v == null ? '' : v);
      return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
    }).join(','));
  });
  const blob = new Blob([lines.join('\n')], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'cadence-entries.csv';
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
  toast('Exported &#10003; &mdash; cadence-entries.csv.');
}
$('#exportHistory').addEventListener('click', exportCSV);
$('#exportSettings').addEventListener('click', exportCSV);

/* ------------------------------------------------------------- delete all */

$('#deleteAll').addEventListener('click', () => {
  openConfirm({
    title: 'Delete all your data?',
    copy: 'Rituals, history and streaks all go. This one can\u2019t be undone.',
    confirmLabel: 'Delete everything',
    onYes: () => {
      try { localStorage.removeItem(STORAGE_KEY); } catch (e) { /* ignore */ }
      state = freshState();
      deletedBuffer = null;
      page = 0; query = '';
      $('#entriesSearch').value = '';
      applySettings();
      renderAll();
      toast('All clear &#10003; &mdash; starting fresh.');
    }
  });
});

/* ---------------------------------------------------------------- wizard */

let wizStep = 0;
function openWizard(step) {
  wizStep = step;
  renderWizard();
  openOverlay('overlay-wizard');
  const next = $('#wizNext');
  if (next) next.focus();
}
function renderWizard() {
  $$('.wiz-step').forEach(s => { s.hidden = parseInt(s.dataset.step, 10) !== wizStep; });
  $$('.wiz-dot').forEach((d, i) => {
    d.className = 'wiz-dot' + (i === wizStep ? ' on' : i < wizStep ? ' done' : '');
  });
  $('#wizBack').hidden = wizStep === 0;
  $('#wizNext').textContent = wizStep === 2 ? 'Get started' : 'Next';
}
function wizardFinish(fromGoal) {
  state.seenIntro = true;
  if (fromGoal) state.settings.goal = parseInt($('#wizGoal').value, 10);
  save();
  applySettings();
  closeOverlay('overlay-wizard');
  toast('You\u2019re set &#10003; &mdash; small rituals, kept daily.');
}
$('#wizNext').addEventListener('click', () => {
  if (wizStep < 2) { wizStep++; renderWizard(); } else wizardFinish(true);
});
$('#wizBack').addEventListener('click', () => { if (wizStep > 0) { wizStep--; renderWizard(); } });
$('#wizSkip').addEventListener('click', () => wizardFinish(false));

/* wizard step dots + ritual checkboxes */
(function initWizard() {
  const dots = $('#wizDots');
  dots.innerHTML = '<span class="wiz-dot on"></span><span class="wiz-dot"></span><span class="wiz-dot"></span>';
  $('#wizChecks').innerHTML = FIXTURE_RITUALS.map(r =>
    '<label><input type="checkbox" checked> ' + esc(r.name) + '</label>').join('');
})();

/* ----------------------------------------------------------- marks toggle */

$('#marksToggle').addEventListener('click', () => {
  const on = document.body.classList.toggle('show-marks');
  $('#marksToggle').setAttribute('aria-pressed', on ? 'true' : 'false');
});

/* ------------------------------------------------------------------- boot */

function renderAll() {
  renderRituals();
  renderRing();
  renderBars();
  renderHeatmap();
  renderEntries();
  renderBadges();
}

function boot() {
  state = load();
  applySettings();
  renderAll();
  if (!state.seenIntro) openWizard(0);   /* first visit: wizard opens (also via Replay intro) */
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
else boot();
