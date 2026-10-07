/* Cadence — interaction layer.
   Vanilla JS. No network calls. localStorage persistence for check-offs + settings.
   Doctrine notes: notices are ruled boxes (no toasts), dialogs are instant (no motion),
   saving states are words + pewter de-emphasis (no spinners). */
(() => {
'use strict';

const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const LS_KEY = 'cadence2.state.v1';
const TODAY = '2026-10-07';

/* ---------------- fixtures ---------------- */

const RITUALS = [
  { id: 'run',    name: 'Morning run',     cat: 'Movement',   min: 30, streak: 6,  hist: [30, 30, 0, 30, 30, 25, 30], recent: [['6 Oct', 30], ['5 Oct', 30], ['4 Oct', 30], ['3 Oct', 30], ['2 Oct', 30]] },
  { id: 'read',   name: 'Read 20 pages',   cat: 'Mind',       min: 20, streak: 3,  hist: [20, 20, 20, 0, 20, 20, 20], recent: [['6 Oct', 20], ['5 Oct', 20], ['4 Oct', 0], ['3 Oct', 20], ['1 Oct', 20]] },
  { id: 'med',    name: 'Meditate',        cat: 'Mind',       min: 10, streak: 12, hist: [10, 10, 10, 10, 10, 10, 10], recent: [['6 Oct', 10], ['4 Oct', 10], ['2 Oct', 10], ['30 Sep', 10], ['29 Sep', 10]] },
  { id: 'sugar',  name: 'No sugar',        cat: 'Discipline', min: 0,  streak: 4,  hist: [0, 0, 0, 0, 0, 0, 0], recent: [['6 Oct', 0], ['5 Oct', 0], ['4 Oct', 0], ['2 Oct', 0], ['1 Oct', 0]] },
  { id: 'guitar', name: 'Practice guitar', cat: 'Craft',      min: 25, streak: 2,  hist: [25, 0, 25, 25, 0, 25, 25], recent: [['5 Oct', 25], ['4 Oct', 25], ['3 Oct', 25], ['30 Sep', 25], ['28 Sep', 25]] },
];

const WEEK = [
  { d: 'Mon', v: 45 }, { d: 'Tue', v: 30 }, { d: 'Wed', v: 60 }, { d: 'Thu', v: 25 },
  { d: 'Fri', v: 50 }, { d: 'Sat', v: 0 },  { d: 'Sun', v: 35 },
];

const HEAT = { 1: 10, 2: 0, 3: 25, 4: 45, 5: 30, 6: 20, 7: 60 };

const ENTRIES = [
  ['7 Oct', 'Morning run', 'Movement', 30], ['7 Oct', 'Read 20 pages', 'Mind', 20], ['7 Oct', 'Meditate', 'Mind', 10],
  ['6 Oct', 'Morning run', 'Movement', 30], ['6 Oct', 'Meditate', 'Mind', 10],
  ['5 Oct', 'Read 20 pages', 'Mind', 20], ['5 Oct', 'Practice guitar', 'Craft', 25],
  ['4 Oct', 'Morning run', 'Movement', 30], ['4 Oct', 'Meditate', 'Mind', 10],
  ['3 Oct', 'Morning run', 'Movement', 30], ['3 Oct', 'Read 20 pages', 'Mind', 20],
  ['2 Oct', 'Morning run', 'Movement', 30], ['2 Oct', 'No sugar', 'Discipline', 0],
  ['1 Oct', 'Read 20 pages', 'Mind', 20], ['1 Oct', 'Meditate', 'Mind', 10],
  ['30 Sep', 'Morning run', 'Movement', 30], ['30 Sep', 'Practice guitar', 'Craft', 25],
  ['29 Sep', 'Morning run', 'Movement', 30], ['29 Sep', 'Meditate', 'Mind', 10],
  ['28 Sep', 'Read 20 pages', 'Mind', 20], ['28 Sep', 'Morning run', 'Movement', 30],
  ['27 Sep', 'Meditate', 'Mind', 10], ['27 Sep', 'Practice guitar', 'Craft', 25],
  ['26 Sep', 'Morning run', 'Movement', 30], ['26 Sep', 'Read 20 pages', 'Mind', 20],
  ['25 Sep', 'Morning run', 'Movement', 30], ['25 Sep', 'No sugar', 'Discipline', 0],
];
let entries = ENTRIES.slice();

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
function fmtDate(iso) {
  const [, m, d] = iso.split('-');
  return `${Number(d)} ${MONTHS[Number(m) - 1]}`;
}

/* ---------------- state ---------------- */

const defaults = () => ({
  checked: ['run', 'read', 'med'],
  order: RITUALS.map(r => r.id),
  deleted: [],
  settings: { name: 'Sam', cat: 'Mind', week: 'mon', goal: 30, remAm: true, remPm: false, dark: false },
  introSeen: false,
});

let state = load();
function load() {
  try {
    const raw = JSON.parse(localStorage.getItem(LS_KEY));
    if (raw && raw.settings) return Object.assign(defaults(), raw);
  } catch (e) { /* storage unavailable — run unpersisted */ }
  return defaults();
}
function save() {
  try { localStorage.setItem(LS_KEY, JSON.stringify(state)); } catch (e) { /* ignore */ }
}

const byId = id => RITUALS.find(r => r.id === id);
const visible = () => state.order.filter(id => !state.deleted.includes(id)).map(byId).filter(Boolean);
const doneCount = () => visible().filter(r => state.checked.includes(r.id)).length;

/* ---------------- notices · D-13 (ruled boxes; no toasts; no motion) ---------------- */

const noticeTimers = {};
function showNotice(view, html, opts = {}) {
  const slot = $(`.notice-slot[data-slot="${view}"]`);
  if (!slot) return;
  clearTimeout(noticeTimers[view]);
  slot.innerHTML = `<div class="notice${opts.ceremony ? ' ceremony' : ''}" role="status">
      <i class="n-acc" aria-hidden="true"></i><p>${html}</p>
      ${opts.undo ? '<button class="link" type="button" id="undo-btn">Undo · Rétablir</button>' : ''}
    </div>`;
  if (opts.undo) {
    $('#undo-btn').addEventListener('click', () => {
      clearTimeout(noticeTimers[view]); slot.innerHTML = '';
      opts.undo();
    });
  }
  if (opts.ceremony) {
    /* ceremony beat: the identity red accent, brief and static — no motion. */
    setTimeout(() => {
      const n = slot.querySelector('.notice');
      if (n) n.classList.remove('ceremony');
    }, 1800);
  }
  noticeTimers[view] = setTimeout(() => { slot.innerHTML = ''; }, opts.stay || 4200);
}

/* ---------------- overlays · D-18 (instant, square sheet, scrim 55%) ---------------- */

let lastFocus = null;
function openOvl(id) {
  lastFocus = document.activeElement;
  $('#' + id).hidden = false;
  const d = $('#' + id + ' .dlg');
  if (d) d.focus();
}
function closeOvl(id) { $('#' + id).hidden = true; if (lastFocus && lastFocus.focus) lastFocus.focus(); }

/* saving state: words + pewter de-emphasis; ~750 ms (no spinner — motion gated) */
function withSaving(btn, savingLabel, done) {
  const origText = btn.textContent;
  const origClass = btn.className;
  btn.disabled = true;
  btn.classList.remove('b-slate', 'b-out');
  btn.classList.add('b-out', 'saving');
  btn.textContent = savingLabel;
  setTimeout(() => {
    btn.className = origClass;
    btn.textContent = origText;
    btn.disabled = false;
    done();
  }, 750);
}

/* ---------------- today ---------------- */

function renderToday() {
  const vis = visible();
  const t = vis.length;
  const n = doneCount();
  const pct = t ? Math.round(n / t * 100) : 0;

  $('#hero-count').textContent = `${n} of ${t} rituals done · ${pct}%`;
  $('#hero-count-fr').textContent =
    `${n} rituel${n > 1 ? 's' : ''} sur ${t} fait${n > 1 ? 's' : ''} · ${pct} %`;
  $('#hero-fill').style.width = pct + '%';
  $('#hero-meter').setAttribute('aria-valuenow', pct);

  const list = $('#ritual-list');
  list.innerHTML = vis.map((r, i) => `
    <li class="ritual" data-id="${r.id}">
      <span class="ri-mark" data-adapted="ritual icon → ordinal marker (pictograms prohibited)">${String(i + 1).padStart(2, '0')}</span>
      <span class="ri-name">${r.name}</span>
      <span class="tag">${r.cat}</span>
      <span class="chip">${r.streak}-day streak</span>
      <label class="check"><input type="checkbox" data-fallback="platform checkbox as check control + field styling (fallback/platform-controls)"
        aria-label="Mark ${r.name} done" ${state.checked.includes(r.id) ? 'checked' : ''}></label>
    </li>`).join('');

  $('#today-empty').hidden = t !== 0;
  list.hidden = t === 0;
  buildMarks();
}

function onCheck(id, box) {
  const r = byId(id);
  if (box.checked) {
    if (!state.checked.includes(id)) state.checked.push(id);
  } else {
    state.checked = state.checked.filter(x => x !== id);
  }
  save();
  renderToday();
  const t = visible().length;
  const n = doneCount();
  if (box.checked) {
    let msg = `Logged ✓ — ${r.name} recorded.${r.min ? ' ' + r.min + ' min.' : ''} | Consigné ✓ — ${r.name} enregistré.`;
    if (t > 0 && n === t) msg += ' All rituals done today. · Tous les rituels du jour sont faits.';
    showNotice('today', msg, { ceremony: true });
  } else {
    showNotice('today', `Unchecked — ${r.name} removed from today. | Décoché — ${r.name} retiré du jour.`);
  }
}

/* ---------------- ritual detail ---------------- */

let detailId = null;

function openDetail(id) {
  detailId = id;
  const r = byId(id);
  const idx = visible().findIndex(x => x.id === id);
  const marker = String(idx + 1).padStart(2, '0');
  const isChecked = state.checked.includes(id);

  $('#detail-title').textContent = r.name;
  $('#detail-body').innerHTML = `
    <div class="det-top">
      <span class="ri-mark" data-adapted="ritual icon → ordinal marker (pictograms prohibited)">${marker}</span>
      <span class="tag">${r.cat}</span>
      <span class="chip">${r.min ? 'Default ' + r.min + ' min · ' : ''}${r.streak}-day streak · série de ${r.streak} jours</span>
      <span class="status">${isChecked ? 'Logged · Consigné' : 'Not logged · Non consigné'}</span>
    </div>
    <h3 class="det-h">Last 7 days · 7 derniers jours</h3>
    <div class="spark" data-improvised="mini-bar trend; sparkline undefined in pack">
      ${r.hist.map(v => `<i style="height:${v === 0 ? 2 : Math.max(5, Math.round(v / 30 * 46))}px"></i>`).join('')}
    </div>
    <p class="spark-cap">${r.min === 0 ? 'A yes/no ritual — no minutes. · Rituel oui/non — sans minutes.' : r.hist.join(' · ') + ' min'}</p>
    <h3 class="det-h">Recent entries · Entrées récentes</h3>
    <ul class="mini">
      ${r.recent.map(([d, m]) => `<li><span>${d}</span><span>${r.name}</span><span class="num">${m === 0 ? '—' : m + ' min'}</span></li>`).join('')}
    </ul>
    <div class="marker-block" data-adapted="photo upload → marker statement (imagery prohibited)">
      <span class="ri-mark">${marker}</span>
      <p><strong>Marker · Marqueur.</strong> Rituals are marked by their number and initials — photos are not part of this system.</p>
    </div>`;

  $('#detail-up').disabled = idx <= 0;
  $('#detail-down').disabled = idx >= visible().length - 1;
  openOvl('ovl-detail');
  buildMarks();
}

function moveRitual(id, dir) {
  const order = state.order.filter(x => !state.deleted.includes(x));
  const i = order.indexOf(id);
  const j = i + dir;
  if (i < 0 || j < 0 || j >= order.length) return;
  [order[i], order[j]] = [order[j], order[i]];
  state.order = order.concat(state.order.filter(x => state.deleted.includes(x)));
  save();
  renderToday();
  openDetail(id);
}

function deleteRitual(id) {
  const r = byId(id);
  const wasChecked = state.checked.includes(id);
  state.deleted.push(id);
  state.checked = state.checked.filter(x => x !== id);
  save();
  closeOvl('ovl-detail');
  renderToday();
  showNotice('today', `Deleted — ${r.name} removed from the list. | Supprimé — ${r.name} retiré de la liste.`, {
    undo: () => {
      state.deleted = state.deleted.filter(x => x !== id);
      if (wasChecked && !state.checked.includes(id)) state.checked.push(id);
      save();
      renderToday();
      showNotice('today', `Restored ✓ — ${r.name} is back. | Rétabli ✓ — ${r.name} est de retour.`, { ceremony: true });
    },
  });
}

/* ---------------- confirm (recipe/retire-confirm) ---------------- */

let confirmOnOk = null;
function openConfirm({ title, body, ok, onOk }) {
  $('#cf-title').textContent = title;
  $('#cf-body').textContent = body;
  $('#cf-ok').textContent = ok;
  confirmOnOk = onOk;
  openOvl('ovl-confirm'); /* focus lands on the sheet, never on the confirm button */
}

/* ---------------- log form ---------------- */

function populateLogSelect() {
  $('#log-ritual').innerHTML = visible()
    .map(r => `<option value="${r.id}">${r.name}${r.min ? ' — ' + r.min + ' min' : ''}</option>`).join('');
}

function openLog() {
  if (!visible().length) {
    showNotice('today', 'No rituals to log right now. Restore one first. · Aucun rituel à consigner pour le moment.');
    return;
  }
  populateLogSelect();
  clearLogErrors();
  const first = byId($('#log-ritual').value);
  if (first && first.min > 0) $('#log-min').value = first.min;
  openOvl('ovl-log');
}

function clearLogErrors() {
  $('#log-min-err').hidden = true;
  $('#log-min').classList.remove('invalid');
}

/* ---------------- history ---------------- */

function renderBars() {
  const bars = $('#bars');
  const MAXH = 150, max = 60;
  bars.innerHTML =
    WEEK.map(d => `
      <div class="bcol-top">
        <span class="bval">${d.v}</span>
        <div class="btrack"><i style="height:${Math.round(d.v / max * MAXH)}px"></i></div>
      </div>`).join('') +
    '<div class="axis" aria-hidden="true"></div>' +
    WEEK.map(d => `<div class="bcol-lab">${d.d}</div>`).join('');
}

function renderHeat() {
  const heat = $('#heat');
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  let html = days.map(d => `<div class="hw">${d}</div>`).join('');
  /* leading cells: 28–30 Sep, context only */
  ['28', '29', '30'].forEach(d => { html += `<div class="hc out">${d}</div>`; });
  for (let d = 1; d <= 31; d++) {
    const v = HEAT[d];
    if (v === undefined || v === 0) { html += `<div class="hc">${d}</div>`; continue; }
    const cls = v < 15 ? ' l1' : v < 30 ? ' l2' : ' l3';
    html += `<div class="hc has${cls}" title="${d} Oct — ${v} min">${d}</div>`;
  }
  heat.innerHTML = html;
}

let entryFilter = '';
let entryPage = 0;
const PER_PAGE = 8;

function filteredEntries() {
  const f = entryFilter.toLowerCase();
  return entries.filter(e => !f || (e[0] + ' ' + e[1] + ' ' + e[2]).toLowerCase().includes(f));
}

function renderEntries() {
  const f = filteredEntries();
  const pages = Math.max(1, Math.ceil(f.length / PER_PAGE));
  entryPage = Math.min(entryPage, pages - 1);
  const slice = f.slice(entryPage * PER_PAGE, entryPage * PER_PAGE + PER_PAGE);

  $('#entries-body').innerHTML = slice.length
    ? slice.map(e => `<tr><td>${e[0]}</td><td>${e[1]}</td><td>${e[2]}</td><td class="num">${e[3] === 0 ? '—' : e[3]}</td><td>Logged · Consigné</td></tr>`).join('')
    : '<tr><td colspan="5">No matching entries. · Aucune entrée correspondante.</td></tr>';

  const a = f.length ? entryPage * PER_PAGE + 1 : 0;
  const b = Math.min(f.length, (entryPage + 1) * PER_PAGE);
  $('#page-readout').textContent = `Showing ${a}–${b} of ${f.length} entries · Entrées ${a}–${b} sur ${f.length}`;
  $('#page-newer').disabled = entryPage === 0;
  $('#page-older').disabled = entryPage >= pages - 1;
}

function exportCSV() {
  const rows = [['Date', 'Ritual', 'Category', 'Minutes', 'Status'],
    ...entries.map(e => [e[0], e[1], e[2], String(e[3]), 'Logged'])];
  const csv = rows.map(r => r.map(c => `"${c.replace(/"/g, '""')}"`).join(',')).join('\r\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'cadence-entries.csv';
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

/* ---------------- settings ---------------- */

function syncSettings() {
  const s = state.settings;
  $('#s-name').value = s.name;
  $('#s-cat').value = s.cat;
  $$('input[name="weekstart"]').forEach(r => { r.checked = r.value === s.week; });
  $('#s-goal').value = s.goal;
  $('#goal-out').textContent = s.goal + ' min';
  $('#rem-am').checked = s.remAm;
  $('#rem-pm').checked = s.remPm;
  $('#s-dark').checked = s.dark;
  document.body.classList.toggle('dark', s.dark);
}

/* ---------------- wizard ---------------- */

let wizStep = 0;
function renderWizard() {
  $$('#wiz-body .wiz-step').forEach(el => { el.hidden = Number(el.dataset.step) !== wizStep; });
  $$('#wiz-dots .dot').forEach((d, i) => d.classList.toggle('is-on', i === wizStep));
  $('#wiz-count').textContent = `Step ${wizStep + 1} of 3 · Étape ${wizStep + 1} de 3`;
  $('#wiz-back').disabled = wizStep === 0;
  $('#wiz-next').textContent = wizStep === 2 ? 'Start · Commencer' : 'Next · Suivant';
}
function openWizard(step) { wizStep = step || 0; renderWizard(); openOvl('ovl-intro'); }
function finishWizard() { state.introSeen = true; save(); closeOvl('ovl-intro'); }

/* ---------------- marks · ◌ (improvised: dashed amber outlines + labels) ---------------- */

function buildMarks() {
  let n = 0, imp = 0, ad = 0, fb = 0;
  $$('[data-improvised],[data-adapted],[data-fallback]').forEach(el => {
    n++;
    let kind = 'improvised', note = el.dataset.improvised;
    if (el.dataset.adapted) { kind = 'adapted'; note = el.dataset.adapted; ad++; }
    else if (el.dataset.fallback) { kind = 'fallback'; note = el.dataset.fallback; fb++; }
    else imp++;
    const label = `${kind} · ${note}`;
    const isForm = ['INPUT', 'SELECT', 'TEXTAREA'].includes(el.tagName);
    const host = isForm ? (el.closest('.field') || el.closest('label') || el.parentElement) : el;
    host.classList.add('mk');
    host.dataset.mk = label;
  });
  const b = $('#marks');
  b.dataset.count = n;
  b.title = `Marks: ${n} elements — improvised ${imp} · adapted ${ad} · fallback ${fb}`;
}

/* ---------------- wiring ---------------- */

$$('.tab').forEach(tab => tab.addEventListener('click', () => {
  const v = tab.dataset.view;
  $$('.tab').forEach(x => {
    const on = x === tab;
    x.classList.toggle('is-on', on);
    x.setAttribute('aria-selected', on ? 'true' : 'false');
  });
  $$('.view').forEach(sec => { sec.hidden = sec.id !== 'view-' + v; });
  if (v === 'history') renderEntries();
  window.scrollTo(0, 0);
}));

$('#ritual-list').addEventListener('click', e => {
  if (e.target.closest('.check')) return;
  const li = e.target.closest('.ritual');
  if (li) openDetail(li.dataset.id);
});
$('#ritual-list').addEventListener('change', e => {
  const box = e.target.closest('input[type="checkbox"]');
  if (box) onCheck(box.closest('.ritual').dataset.id, box);
});

/* Today */
$('#log-open').addEventListener('click', openLog);
$('#empty-restore').addEventListener('click', () => {
  state.deleted = [];
  save();
  renderToday();
  showNotice('today', 'Restored ✓ — All rituals are back. | Rétabli ✓ — tous les rituels sont de retour.', { ceremony: true });
});

/* Detail dialog */
$('#detail-close').addEventListener('click', () => closeOvl('ovl-detail'));
$('#detail-up').addEventListener('click', () => moveRitual(detailId, -1));
$('#detail-down').addEventListener('click', () => moveRitual(detailId, 1));
$('#detail-del').addEventListener('click', () => {
  const r = byId(detailId);
  openConfirm({
    title: 'Delete this ritual? · Supprimer ce rituel ?',
    body: `This removes “${r.name}” and its history from this device. This can’t be undone. · Cette action supprime « ${r.name} » et son historique de cet appareil. Elle est irréversible.`,
    ok: 'Delete ritual · Supprimer',
    onOk: () => deleteRitual(detailId),
  });
});

/* Confirm dialog */
$('#cf-cancel').addEventListener('click', () => closeOvl('ovl-confirm'));
$('#cf-ok').addEventListener('click', () => {
  const fn = confirmOnOk;
  confirmOnOk = null;
  closeOvl('ovl-confirm');
  if (fn) fn();
});

/* Scrim closes (except the wizard, which asks for a choice) */
$$('.scrim[data-close]').forEach(s => s.addEventListener('click', () => {
  closeOvl('ovl-' + s.dataset.close);
}));

/* Log form */
$('#log-ritual').addEventListener('change', () => {
  const r = byId($('#log-ritual').value);
  if (r && r.min > 0) $('#log-min').value = r.min;
});
$('#log-minus').addEventListener('click', () => { $('#log-min').value = Math.max(0, Number($('#log-min').value || 0) - 5); });
$('#log-plus').addEventListener('click', () => { $('#log-min').value = Math.min(240, Number($('#log-min').value || 0) + 5); });
$('#log-min').addEventListener('input', clearLogErrors);
$('#log-cancel').addEventListener('click', () => { closeOvl('ovl-log'); clearLogErrors(); });
$('#log-form').addEventListener('submit', e => {
  e.preventDefault();
  const v = Number($('#log-min').value);
  if (!(v >= 1 && v <= 240)) {
    $('#log-min-err').hidden = false;
    $('#log-min').classList.add('invalid');
    return;
  }
  clearLogErrors();
  const id = $('#log-ritual').value;
  const date = $('#log-date').value;
  withSaving($('#log-save'), 'Saving… · Enregistrement…', () => {
    const r = byId(id);
    closeOvl('ovl-log');
    /* the logged entry joins the register */
    entries.unshift([fmtDate(date), r.name, r.cat, v]);
    entryPage = 0;
    if (!$('#view-history').hidden) renderEntries();
    let ringChanged = false;
    if (date === TODAY && !state.checked.includes(id)) {
      state.checked.push(id);
      ringChanged = true;
      save();
    }
    renderToday();
    showNotice('today',
      `Logged ✓ — ${r.name}, ${v} min. Entry recorded.${ringChanged ? ' Today’s progress updated.' : ''} | Consigné ✓ — ${r.name}, ${v} min.`,
      { ceremony: true });
  });
});

/* History */
$('#entry-search').addEventListener('input', e => {
  entryFilter = e.target.value.trim();
  entryPage = 0;
  renderEntries();
});
$('#page-newer').addEventListener('click', () => { entryPage--; renderEntries(); });
$('#page-older').addEventListener('click', () => { entryPage++; renderEntries(); });
$('#h-export').addEventListener('click', () => {
  exportCSV();
  showNotice('history', 'Exported ✓ — cadence-entries.csv saved to your downloads. | Exporté ✓ — fichier enregistré dans vos téléchargements.');
});

/* Achievements */
$('#empty-demo').addEventListener('change', e => {
  const empty = e.target.checked;
  $('#badge-grid').hidden = empty;
  $('#ach-empty').hidden = !empty;
});
$('#ach-empty-go').addEventListener('click', () => {
  $$('.tab').find(t => t.dataset.view === 'today').click();
  openLog();
});

/* Settings */
$('#s-goal').addEventListener('input', e => { $('#goal-out').textContent = e.target.value + ' min'; });
$('#s-dark').addEventListener('change', e => {
  state.settings.dark = e.target.checked;
  document.body.classList.toggle('dark', e.target.checked);
  save();
});
$('#s-name').addEventListener('input', () => {
  $('#s-name-err').hidden = true;
  $('#s-name').classList.remove('invalid');
});
$('#s-save').addEventListener('click', () => {
  const name = $('#s-name').value.trim();
  if (!name) {
    $('#s-name-err').hidden = false;
    $('#s-name').classList.add('invalid');
    return;
  }
  withSaving($('#s-save'), 'Saving… · Enregistrement…', () => {
    state.settings.name = name;
    state.settings.cat = $('#s-cat').value;
    state.settings.week = $$('input[name="weekstart"]').find(r => r.checked).value;
    state.settings.goal = Number($('#s-goal').value);
    state.settings.remAm = $('#rem-am').checked;
    state.settings.remPm = $('#rem-pm').checked;
    state.settings.dark = $('#s-dark').checked;
    save();
    showNotice('settings', 'Saved ✓ — Preferences saved. | Enregistré ✓ — préférences enregistrées.');
  });
});
$('#s-export').addEventListener('click', () => {
  exportCSV();
  showNotice('settings', 'Exported ✓ — cadence-entries.csv saved to your downloads. | Exporté ✓ — fichier enregistré dans vos téléchargements.');
});
$('#s-replay').addEventListener('click', () => openWizard(0));
$('#s-delete').addEventListener('click', () => {
  openConfirm({
    title: 'Delete all data? · Supprimer toutes les données ?',
    body: 'This removes every ritual, entry and setting from this device. This can’t be undone. · Cette action supprime tous les rituels, entrées et réglages de cet appareil. Elle est irréversible.',
    ok: 'Delete all · Tout supprimer',
    onOk: () => {
      try { localStorage.removeItem(LS_KEY); } catch (e) { /* ignore */ }
      state = defaults();
      state.introSeen = true;
      save();
      syncSettings();
      renderToday();
      showNotice('settings', 'Deleted ✓ — All data removed. | Supprimé ✓ — toutes les données supprimées.');
    },
  });
});

/* Wizard */
$('#wiz-next').addEventListener('click', () => { wizStep < 2 ? openWizard(wizStep + 1) : finishWizard(); });
$('#wiz-back').addEventListener('click', () => { if (wizStep > 0) openWizard(wizStep - 1); });
$('#wiz-skip').addEventListener('click', finishWizard);

/* Marks toggle */
$('#marks').addEventListener('click', () => {
  const on = document.body.classList.toggle('show-marks');
  $('#marks').setAttribute('aria-pressed', on ? 'true' : 'false');
  $('#marks').textContent = on ? '◌ ' + ($('#marks').dataset.count || '') : '◌';
});

/* ---------------- init ---------------- */

state.checked = state.checked.filter(id => RITUALS.some(r => r.id === id));
renderToday();
renderBars();
renderHeat();
renderEntries();
syncSettings();
buildMarks();
if (!state.introSeen) openWizard(0);

})();
