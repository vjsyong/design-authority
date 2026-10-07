/* Cadence — dominion variant. Vanilla JS, no network calls.
   Fixtures + state + simple renderers. Improvised/adapted surfaces are marked
   with data-improvised / data-adapted (see ◌ toggle and NOTES.md). */
(function () {
  'use strict';

  var TODAY = '2026-10-07';
  var TODAY_LABEL = 'Tuesday, 7 October';
  var STORE_KEY = 'cadence-dominion-v1';

  /* ------------------------------ fixtures ------------------------------ */
  var FIX = {
    rituals: [
      { id: 'run', n: 'Morning run', cat: 'Movement', min: 30, streak: 12, status: 'on', done: true, spark: [30, 0, 45, 30, 60, 25, 30] },
      { id: 'read', n: 'Read 20 pages', cat: 'Mind', min: 20, streak: 4, status: 'on', done: false, spark: [20, 0, 20, 20, 0, 20, 20] },
      { id: 'meditate', n: 'Meditate', cat: 'Mind', min: 10, streak: 12, status: 'on', done: true, spark: [10, 12, 10, 10, 10, 0, 10] },
      { id: 'sugar', n: 'No sugar', cat: 'Discipline', min: null, streak: 7, status: 'on', done: true, spark: [1, 1, 1, 0, 1, 1, 1] },
      { id: 'guitar', n: 'Practice guitar', cat: 'Craft', min: 25, streak: 2, status: 'slip', done: false, spark: [0, 25, 0, 0, 25, 0, 0] }
    ],
    week: [45, 30, 60, 25, 50, 0, 35],
    weekDays: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    monthFirst: 3,           // Oct 1, 2026 per the spec's calendar (Wed start; Mon-first grid)
    monthDays: 31,
    heat: { 1: 55, 2: 40, 3: 70, 4: 0, 5: 45, 6: 30, 7: 30 },  // days 1..7 only (fixture)
    entries: {
      1: [
        { d: '07 Oct', r: 'Morning run', m: 30, note: 'Easy pace.' },
        { d: '07 Oct', r: 'Meditate', m: 10, note: '' },
        { d: '07 Oct', r: 'No sugar', m: null, note: 'Stayed clear.' },
        { d: '06 Oct', r: 'Morning run', m: 45, note: 'Windy.' },
        { d: '06 Oct', r: 'Practice guitar', m: 25, note: 'Scales, then one song.' },
        { d: '05 Oct', r: 'Read 20 pages', m: 20, note: '' },
        { d: '04 Oct', r: 'No sugar', m: null, note: 'Movie night, still clear.' },
        { d: '03 Oct', r: 'Meditate', m: 12, note: 'Longer sit.' }
      ],
      2: [
        { d: '02 Oct', r: 'Morning run', m: 50, note: 'Long loop.' },
        { d: '01 Oct', r: 'Practice guitar', m: 30, note: 'New chord.' },
        { d: '30 Sep', r: 'Read 20 pages', m: 25, note: 'Finished a chapter.' },
        { d: '29 Sep', r: 'Meditate', m: 10, note: '' },
        { d: '28 Sep', r: 'Morning run', m: 35, note: '' },
        { d: '27 Sep', r: 'No sugar', m: null, note: '' },
        { d: '26 Sep', r: 'Read 20 pages', m: 20, note: '' },
        { d: '25 Sep', r: 'Meditate', m: 15, note: '' }
      ]
    },
    badges: [
      { n: 'First week', earned: true, sub: 'Earned — 28 September' },
      { n: '10 days', earned: true, sub: 'Earned — 1 October' },
      { n: 'Early bird', earned: true, sub: 'Earned — 3 October' },
      { n: 'Century club', earned: true, sub: 'Earned — 5 October' },
      { n: '21 days', earned: false, sub: 'Reach a 21-day streak' },
      { n: 'Perfect month', earned: false, sub: 'A check every day of one month' }
    ],
    stats: { current: 12, best: 21, total: 240 },
    settings: { name: 'Sam', category: 'Movement', weekStart: 'monday', goal: 30, morning: true, evening: true }
  };

  /* ------------------------------ state ------------------------------ */
  var state = {
    removed: [],       // ritual ids removed by the user
    order: FIX.rituals.map(function (r) { return r.id; }),
    done: {},          // per-ritual checked overrides
    extra: [],         // entries added via the log form
    settings: JSON.parse(JSON.stringify(FIX.settings)),
    dark: false,
    page: 1,
    badgesEmpty: false,
    celebration: null
  };
  var lastDeleted = null;   // {ritual, index}
  var undoAll = null;       // full snapshot for delete-all undo

  function save() {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({
        v: 1, removed: state.removed, order: state.order, done: state.done,
        extra: state.extra, settings: state.settings, dark: state.dark
      }));
    } catch (e) { /* storage unavailable: stay in-memory */ }
  }
  function load() {
    try {
      var raw = localStorage.getItem(STORE_KEY);
      if (!raw) return;
      var s = JSON.parse(raw);
      if (!s || s.v !== 1) return;
      state.removed = s.removed || [];
      state.order = s.order || state.order;
      state.done = s.done || {};
      state.extra = s.extra || [];
      state.settings = Object.assign({}, FIX.settings, s.settings || {});
      state.dark = !!s.dark;
    } catch (e) { /* ignore corrupt state */ }
  }

  function rituals() {
    var list = FIX.rituals.filter(function (r) { return state.removed.indexOf(r.id) === -1; });
    list.sort(function (a, b) { return state.order.indexOf(a.id) - state.order.indexOf(b.id); });
    return list.map(function (r) {
      var done = (r.id in state.done) ? state.done[r.id] : r.done;
      return Object.assign({}, r, { done: done });
    });
  }
  function allEntries() {
    return state.extra.concat(FIX.entries[1], FIX.entries[2]);
  }
  function pageEntries() {
    var base = state.page === 1 ? state.extra.concat(FIX.entries[1]) : FIX.entries[2];
    return base;
  }

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html !== undefined) n.innerHTML = html;
    return n;
  }

  /* ------------------------------ notices (D-13 vessel) ------------------------------ */
  function showNotice(text, opts) {
    opts = opts || {};
    var region = $('#notice-region');
    region.innerHTML = '';
    var n = el('div', 'notice');
    n.setAttribute('data-adapted', 'toast → ruled notice (D-13: no toasts)');
    var p = el('p', null, text);
    n.appendChild(p);
    if (opts.undo) {
      var u = el('button', 'linkish', 'Undo');
      u.setAttribute('data-improvised', 'undo as a link in the ruled notice (not catalogued)');
      u.addEventListener('click', function () {
        opts.undo();
        region.innerHTML = '';
      });
      p.appendChild(u);
    }
    var d = el('button', 'linkish', 'Dismiss');
    d.addEventListener('click', function () { region.innerHTML = ''; });
    p.appendChild(d);
    region.appendChild(n);
  }

  /* ------------------------------ ring + today ------------------------------ */
  var RING_R = 50;
  var RING_C = 2 * Math.PI * RING_R;

  function renderToday() {
    var list = rituals();
    var done = list.filter(function (r) { return r.done; }).length;
    var total = list.length || 5;
    var pct = total ? Math.round(done / total * 100) : 0;

    $('#ring-pct').textContent = pct + '%';
    $('#ring-sub').textContent = done + ' of ' + total;
    var arc = $('#ring-arc');
    arc.setAttribute('stroke-dasharray', (RING_C * (pct / 100)) + ' ' + RING_C);
    $('#ring').setAttribute('aria-label', done + ' of ' + total + ' rituals done, ' + pct + ' percent');
    $('#hero-done').textContent = done + ' of ' + total + ' rituals done';
    $('#hero-done-fr').textContent = done + ' de ' + total + ' rituels faits';
    $('#hero-sub').textContent = (total - done) + ' left today.';

    var ul = $('#ritual-list');
    ul.innerHTML = '';
    list.forEach(function (r, i) {
      ul.appendChild(ritualRow(r, i));
    });
    $('#rituals-empty').hidden = list.length > 0;

    /* greeting / identity */
    $('#today-greeting').textContent = 'Good evening, ' + state.settings.name + '.';
    $('#id-name').textContent = state.settings.name;
    $('#initials').textContent = (state.settings.name || 'S').charAt(0).toUpperCase();
  }

  function ritualRow(r, i) {
    var li = el('li', 'ritual');
    li.draggable = true;
    li.setAttribute('data-ritual', r.id);

    var mark = el('span', 'r-mark', (i + 1 < 10 ? '0' : '') + (i + 1));
    mark.title = 'Drag to reorder';
    if (i === 0) mark.setAttribute('data-adapted', 'icon → ordinal marker (pictograms prohibited, D-22)');
    mark.tabIndex = 0;
    mark.setAttribute('role', 'button');
    mark.setAttribute('aria-label', 'Move ' + r.n + ' up or down with Alt and arrow keys');

    var main = el('div', 'r-main');
    var name = el('span', 'r-name', r.n);
    var meta = el('div', 'r-meta');
    var tag = el('span', 'tag', r.cat);
    if (i === 0) tag.setAttribute('data-improvised', 'small ruled label per D-10 idiom (not catalogued)');
    meta.appendChild(tag);
    if (r.min) meta.appendChild(el('span', 'r-min', r.min + ' min'));
    main.appendChild(name);
    main.appendChild(meta);
    main.tabIndex = 0;
    main.setAttribute('role', 'button');
    main.setAttribute('aria-label', 'Open details for ' + r.n);
    main.addEventListener('click', function () { openDetail(r.id); });
    main.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); openDetail(r.id); }
    });

    var flags = el('div', 'r-flags');
    var chip = el('span', 'chip', r.streak + ' days');
    if (i === 0) chip.setAttribute('data-improvised', 'streak chip invented (not catalogued)');
    var st = el('span', 'st ' + (r.status === 'on' ? 'st-on' : 'st-slip'), r.status === 'on' ? 'On track' : 'Slipping');
    if (i === 0) st.setAttribute('data-improvised', 'status device per D-10 (not in catalogue)');
    flags.appendChild(chip);
    flags.appendChild(st);

    var check = el('button', 'check' + (r.done ? ' is-done' : ''), r.done ? '✓' : '');
    check.type = 'button';
    check.setAttribute('aria-pressed', r.done ? 'true' : 'false');
    check.setAttribute('aria-label', (r.done ? 'Uncheck ' : 'Mark done: ') + r.n);
    check.title = 'Mark done';
    if (i === 0) check.setAttribute('data-improvised', 'check control composed from action + field primitives (not catalogued)');
    check.addEventListener('click', function (ev) {
      ev.stopPropagation();
      toggleCheck(r.id, check);
    });

    li.appendChild(mark);
    li.appendChild(main);
    li.appendChild(flags);
    li.appendChild(check);
    if (i === 0) li.setAttribute('data-improvised', 'celebration = brief reversed colourway, instant settle (motion gated)');

    /* drag reorder */
    li.addEventListener('dragstart', function (ev) {
      ev.dataTransfer.setData('text/plain', r.id);
      ev.dataTransfer.effectAllowed = 'move';
    });
    li.addEventListener('dragover', function (ev) { ev.preventDefault(); ev.dataTransfer.dropEffect = 'move'; });
    li.addEventListener('drop', function (ev) {
      ev.preventDefault();
      var dragId = ev.dataTransfer.getData('text/plain');
      if (dragId && dragId !== r.id) reorder(dragId, r.id);
    });
    mark.addEventListener('keydown', function (ev) {
      if (ev.altKey && (ev.key === 'ArrowUp' || ev.key === 'ArrowDown')) {
        ev.preventDefault();
        move(r.id, ev.key === 'ArrowUp' ? -1 : 1);
      }
    });
    return li;
  }

  function reorder(dragId, beforeId) {
    var o = state.order.filter(function (id) { return id !== dragId; });
    o.splice(o.indexOf(beforeId), 0, dragId);
    state.order = o;
    /* keep any unseen fixture ids positioned safely */
    FIX.rituals.forEach(function (r) { if (state.order.indexOf(r.id) === -1) state.order.push(r.id); });
    save();
    renderToday();
  }
  function move(id, dir) {
    var o = state.order.slice();
    var i = o.indexOf(id);
    var j = i + dir;
    if (j < 0 || j >= o.length) return;
    o.splice(i, 1); o.splice(j, 0, id);
    state.order = o;
    save();
    renderToday();
  }

  function toggleCheck(id, btn) {
    var r = null;
    rituals().forEach(function (x) { if (x.id === id) r = x; });
    if (!r) return;
    var nowDone = !r.done;
    state.done[id] = nowDone;
    save();
    renderToday();
    if (nowDone) celebrate(id);
    if (nowDone) {
      var list = rituals();
      var done = list.filter(function (x) { return x.done; }).length;
      showNotice('Logged ✓. ' + r.n + ' is in for ' + TODAY_LABEL + '. The ring is now ' + done + ' of ' + list.length + '.');
    } else {
      showNotice('Unchecked. ' + r.n + ' is open again.');
    }
  }

  function celebrate(id) {
    var li = $('.ritual[data-ritual="' + id + '"]');
    if (!li) return;
    li.classList.add('celebrate');
    window.setTimeout(function () { li.classList.remove('celebrate'); }, 900);
  }

  /* ------------------------------ detail overlay ------------------------------ */
  function openDetail(id) {
    var r = null;
    rituals().forEach(function (x) { if (x.id === id) r = x; });
    if (!r) return;
    $('#detail-title').textContent = r.n;
    $('#detail-meta').textContent = r.cat + (r.min ? ' · ' + r.min + ' min' : '') + ' · ' + r.streak + '-day streak';
    drawSpark($('#detail-spark'), r.spark);
    var hist = $('#detail-hist');
    hist.innerHTML = '';
    allEntries().filter(function (e) { return e.r === r.n; }).slice(0, 5).forEach(function (e) {
      hist.appendChild(el('li', null, '<span>' + e.d + '</span><span>' + (e.m == null ? '—' : e.m + ' min') + '</span>'));
    });
    if (!hist.children.length) hist.appendChild(el('li', null, '<span>No entries yet.</span><span></span>'));
    $('#detail-delete').onclick = function () {
      closeOv('ov-detail');
      openConfirm('Delete “' + r.n + '”?', 'This removes it from your rituals and its checks stop counting. You can undo once, right after.', 'Delete ritual', function () {
        var list = rituals();
        var idx = list.map(function (x) { return x.id; }).indexOf(r.id);
        state.removed.push(r.id);
        lastDeleted = { ritual: r, index: idx };
        save();
        renderToday();
        showNotice('Deleted. “' + r.n + '” is out of your rituals.', {
          undo: function () {
            state.removed = state.removed.filter(function (x) { return x !== r.id; });
            lastDeleted = null; save(); renderToday();
            showNotice('Restored. “' + r.n + '” is back in place.');
          }
        });
      });
    };
    openOv('ov-detail');
  }

  function drawSpark(holder, series) {
    var W = 220, H = 48, P = 4;
    var max = Math.max.apply(null, series.concat([1]));
    var pts = series.map(function (v, i) {
      var x = P + i * (W - 2 * P) / (series.length - 1);
      var y = H - P - (v / max) * (H - 2 * P);
      return [x, y];
    });
    var svg = '<svg width="' + W + '" height="' + H + '" role="img" aria-label="Trend of the last seven days">' +
      '<line x1="0" y1="' + (H - 0.5) + '" x2="' + W + '" y2="' + (H - 0.5) + '" stroke="#C9C9C9" stroke-width="1"/>' +
      '<polyline points="' + pts.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' ') + '" fill="none" stroke="#000" stroke-width="2"/>' +
      pts.map(function (p) { return '<rect x="' + (p[0] - 2) + '" y="' + (p[1] - 2) + '" width="4" height="4" fill="#000"/>'; }).join('') +
      '</svg>';
    holder.innerHTML = svg;
  }

  /* ------------------------------ history ------------------------------ */
  function renderHistory() {
    /* chart */
    var chart = $('#chart');
    chart.innerHTML = '';
    var max = Math.max.apply(null, FIX.week);
    FIX.week.forEach(function (m) {
      var col = el('div', 'col');
      col.appendChild(el('span', 'val', String(m)));
      var bar = el('span', 'bar');
      bar.style.height = (m / max * 100) + '%';
      col.appendChild(bar);
      chart.appendChild(col);
    });
    var days = $('#chart-days');
    days.innerHTML = '';
    FIX.weekDays.forEach(function (d) { days.appendChild(el('span', 'd', d)); });

    /* heatmap */
    var head = $('#heat-head');
    if (!head.children.length) {
      ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].forEach(function (d) {
        head.appendChild(el('span', null, d.charAt(0)));
      });
    }
    var heat = $('#heat');
    heat.innerHTML = '';
    for (var i = 0; i < FIX.monthFirst; i++) heat.appendChild(el('div', 'hc blank'));
    for (var day = 1; day <= FIX.monthDays; day++) {
      var cell = el('div', 'hc');
      var v = FIX.heat[day];
      var level = 0;
      if (v != null) {
        if (v > 64) level = 4; else if (v > 44) level = 3; else if (v > 24) level = 2; else if (v > 0) level = 1;
        cell.classList.add('h' + level);
      } else {
        cell.classList.add('future');
        cell.classList.add('h0');
      }
      if (day === 7) cell.classList.add('today');
      cell.appendChild(el('span', null, String(day)));
      heat.appendChild(cell);
    }
    renderLedger();
  }

  function renderLedger() {
    var body = $('#entries-body');
    var rows = pageEntries();
    var q = ($('#filter').value || '').trim().toLowerCase();
    var shown = rows.filter(function (e) {
      if (!q) return true;
      return (e.r + ' ' + e.note + ' ' + e.d).toLowerCase().indexOf(q) !== -1;
    });
    body.innerHTML = '';
    shown.forEach(function (e) {
      var tr = el('tr');
      tr.innerHTML = '<td>' + e.d + '</td><td>' + e.r + '</td><td class="num">' + (e.m == null ? '—' : e.m) + '</td><td>' + (e.note || '—') + '</td>';
      body.appendChild(tr);
    });
    $('#filter-readout').textContent = q
      ? 'Showing ' + shown.length + ' of ' + rows.length + ' entries.'
      : 'Showing ' + rows.length + ' entries.';
    $('#entries-empty').hidden = shown.length > 0;
    $('.tbl-wrap').hidden = shown.length === 0;
    $('#pager-readout').textContent = 'Page ' + state.page + ' of 2';
    $('#btn-older').hidden = state.page !== 1;
    $('#btn-newer').hidden = state.page !== 2;
  }

  /* ------------------------------ achievements ------------------------------ */
  function renderAchievements() {
    $('#stat-current').textContent = FIX.stats.current;
    $('#stat-best').textContent = FIX.stats.best;
    $('#stat-total').textContent = FIX.stats.total;

    var grid = $('#badges');
    grid.innerHTML = '';
    FIX.badges.forEach(function (b) {
      var t = el('div', 'badge' + (b.earned ? '' : ' locked'));
      t.appendChild(el('span', 'b-name', b.n));
      t.appendChild(el('span', 'b-state', b.sub));
      grid.appendChild(t);
    });
    grid.hidden = state.badgesEmpty;
    $('#badges-empty').hidden = !state.badgesEmpty;
    $('#btn-empty-demo').setAttribute('aria-pressed', state.badgesEmpty ? 'true' : 'false');
  }

  /* ------------------------------ settings ------------------------------ */
  function renderSettings() {
    $('#set-name').value = state.settings.name;
    $('#set-cat').value = state.settings.category;
    $$('input[name="weekstart"]').forEach(function (r) { r.checked = r.value === state.settings.weekStart; });
    $('#set-goal').value = state.settings.goal;
    $('#goal-readout').textContent = state.settings.goal + ' min';
    $('#set-morning').checked = state.settings.morning;
    $('#set-evening').checked = state.settings.evening;
    $('#set-dark').checked = state.dark;
    document.body.classList.toggle('dark', state.dark);
  }

  /* ------------------------------ overlays ------------------------------ */
  function openOv(id) {
    var ov = document.getElementById(id);
    ov.hidden = false;
    var sheet = $('.sheet', ov);
    if (sheet) {
      sheet.tabIndex = -1;
      sheet.focus({ preventScroll: true });
    }
  }
  function closeOv(id) {
    var ov = document.getElementById(id);
    if (ov) ov.hidden = true;
  }
  function openConfirm(titleText, bodyText, label, onYes) {
    var ov = $('#ov-confirm');
    $('#confirm-title').innerHTML = '<span>' + titleText + '</span><span class="bdiv" aria-hidden="true"></span><span class="fr" lang="fr">' +
      (titleText.indexOf('Delete all data?') === 0 ? 'Supprimer toutes les données ?' : 'Supprimer « ' + titleText.replace(/^Delete “|”\?$/g, '') + ' » ?') + '</span>';
    $('#confirm-body').textContent = bodyText;
    var yes = $('#confirm-yes');
    yes.textContent = label;
    yes.onclick = function () {
      /* destructive: never pre-focused; saving state shown briefly (D-14 + loading) */
      var saving = $('#confirm-saving');
      saving.hidden = false;
      yes.disabled = true;
      window.setTimeout(function () {
        saving.hidden = true;
        yes.disabled = false;
        closeOv('ov-confirm');
        onYes();
      }, 400);
    };
    openOv('ov-confirm');
  }

  /* ------------------------------ export CSV ------------------------------ */
  function exportCsv() {
    var lines = ['date,ritual,minutes,notes'];
    allEntries().forEach(function (e) {
      lines.push([e.d, e.r, e.m == null ? '' : e.m, e.note]
        .map(function (x) { var s = String(x); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; })
        .join(','));
    });
    var blob = new Blob([lines.join('\n')], { type: 'text/csv' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'cadence-entries.csv';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    showNotice('Exported. cadence-entries.csv has all ' + allEntries().length + ' entries.');
  }

  /* ------------------------------ wizard ------------------------------ */
  var wiz = { step: 0, goal: 30, picks: {} };
  var WIZ_STEPS = [
    {
      t: 'Welcome', tf: 'Bienvenue',
      body: function (box) {
        box.appendChild(el('p', null, 'Small rituals, kept daily.'));
        box.appendChild(el('p', null, 'Cadence tracks five rituals and one number: what you actually kept. Everything stays on this device.'));
      }
    },
    {
      t: 'Pick your rituals', tf: 'Choisissez vos rituels',
      body: function (box) {
        FIX.rituals.forEach(function (r) {
          var lab = el('label', 'pick');
          var cb = el('input'); cb.type = 'checkbox'; cb.checked = true; cb.value = r.id;
          if (!box.querySelector('input')) cb.setAttribute('data-improvised', 'platform fallback: native checkbox (fallback/platform-controls)');
          lab.appendChild(cb);
          lab.appendChild(el('span', null, r.n));
          box.appendChild(lab);
        });
      }
    },
    {
      t: 'Set your goal', tf: 'Fixez votre objectif',
      body: function (box) {
        box.appendChild(el('p', null, 'How many minutes a day are you aiming for?'));
        var row = el('div', 'slider-row');
        var input = el('input'); input.type = 'range'; input.min = 10; input.max = 90; input.step = 5; input.value = wiz.goal;
        var out = el('span', 'readout', wiz.goal + ' min');
        input.addEventListener('input', function () { wiz.goal = Number(input.value); out.textContent = wiz.goal + ' min'; });
        input.setAttribute('data-improvised', 'platform fallback: native range (fallback/platform-controls)');
        row.appendChild(input); row.appendChild(out);
        box.appendChild(row);
      }
    }
  ];
  function renderWizard() {
    var s = WIZ_STEPS[wiz.step];
    $('#wiz-title').innerHTML = '<span>' + s.t + '</span><span class="bdiv" aria-hidden="true"></span><span class="fr" lang="fr">' + s.tf + '</span>';
    var box = $('#wiz-body');
    box.innerHTML = '';
    s.body(box);
    $$('#wiz-dots i').forEach(function (d, i) { d.className = i === wiz.step ? 'on' : ''; });
    $('#wiz-back').disabled = wiz.step === 0;
    $('#wiz-next').textContent = wiz.step === WIZ_STEPS.length - 1 ? 'Begin' : 'Next';
  }

  /* ------------------------------ wiring ------------------------------ */
  function switchView(name) {
    $$('.tab').forEach(function (t) {
      var on = t.getAttribute('data-view') === name;
      t.classList.toggle('is-on', on);
      t.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    ['today', 'history', 'achievements', 'settings'].forEach(function (v) {
      document.getElementById('view-' + v).hidden = v !== name;
    });
  }

  function init() {
    load();
    renderToday();
    renderHistory();
    renderAchievements();
    renderSettings();

    /* tabs */
    $$('.tab').forEach(function (t) {
      t.addEventListener('click', function () { switchView(t.getAttribute('data-view')); });
    });
    $('#tabbar').addEventListener('keydown', function (ev) {
      if (ev.key !== 'ArrowRight' && ev.key !== 'ArrowLeft') return;
      var tabs = $$('.tab');
      var i = tabs.indexOf(document.activeElement);
      if (i === -1) return;
      ev.preventDefault();
      var j = (i + (ev.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
      tabs[j].focus(); switchView(tabs[j].getAttribute('data-view'));
    });

    /* marks toggle */
    $('#marks-toggle').addEventListener('click', function () {
      var on = document.body.classList.toggle('show-marks');
      this.setAttribute('aria-pressed', on ? 'true' : 'false');
    });

    /* overlay close: [data-close], scrim, Esc */
    $$('[data-close]').forEach(function (b) {
      b.addEventListener('click', function () {
        var ov = b.closest('.overlay'); if (ov) ov.hidden = true;
      });
    });
    $$('.overlay').forEach(function (ov) {
      ov.addEventListener('click', function (ev) {
        if (ev.target === ov && ov.id !== 'ov-confirm' && ov.id !== 'ov-log') ov.hidden = true;
      });
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key !== 'Escape') return;
      ['ov-wizard', 'ov-log', 'ov-confirm', 'ov-detail'].some(function (id) {
        if (!document.getElementById(id).hidden) { closeOv(id); return true; }
        return false;
      });
    });

    /* log a ritual */
    $('#btn-log').addEventListener('click', function () {
      var sel = $('#log-ritual');
      sel.innerHTML = '';
      rituals().forEach(function (r) { sel.appendChild(new Option(r.n, r.id)); });
      $('#log-saving').hidden = true;
      var sub = $('#log-submit');
      sub.disabled = false; sub.textContent = 'Log';
      $('#log-date').value = TODAY;
      openOv('ov-log');
    });
    $('#min-minus').addEventListener('click', function () {
      var m = $('#log-min'); m.value = Math.max(0, Number(m.value || 0) - 5);
    });
    $('#min-plus').addEventListener('click', function () {
      var m = $('#log-min'); m.value = Math.min(600, Number(m.value || 0) + 5);
    });
    $('#log-submit').addEventListener('click', function () {
      var sub = this;
      var r = null;
      rituals().forEach(function (x) { if (x.id === $('#log-ritual').value) r = x; });
      if (!r) return;
      var date = $('#log-date').value || TODAY;
      var mins = Math.max(0, Number($('#log-min').value || 0));
      sub.disabled = true; sub.textContent = 'Saving…';
      $('#log-saving').hidden = false;
      window.setTimeout(function () {
        $('#log-saving').hidden = true;
        sub.disabled = false; sub.textContent = 'Log';
        var d = new Date(date + 'T12:00:00');
        var label = d.getDate() + ' ' + ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][d.getMonth()];
        if (r.min == null && mins > 0) { /* no-sugar style rituals still log fine */ }
        var entry = { d: label, r: r.n, m: (r.min == null && mins === 0) ? null : mins, note: $('#log-notes').value.trim() };
        state.extra.unshift(entry);
        var note = 'Logged ✓. ' + r.n + ' is in for ' + (date === TODAY ? TODAY_LABEL : label) + '.';
        if (date === TODAY) {
          var before = r.done;
          state.done[r.id] = true;
          if (!before) {
            var list = rituals();
            var done = list.filter(function (x) { return x.done; }).length;
            note += ' The ring is now ' + done + ' of ' + list.length + '.';
          }
        }
        save();
        closeOv('ov-log');
        $('#log-notes').value = '';
        $('#log-min').value = r.min || 30;
        renderToday();
        renderLedger();
        showNotice(note);
      }, 700);
    });

    /* history controls */
    $('#filter').addEventListener('input', renderLedger);
    $('#btn-clear-filter').addEventListener('click', function () { $('#filter').value = ''; renderLedger(); });
    $('#btn-older').addEventListener('click', function () { state.page = 2; renderLedger(); });
    $('#btn-newer').addEventListener('click', function () { state.page = 1; renderLedger(); });
    $('#btn-export').addEventListener('click', exportCsv);
    $('#btn-export-2').addEventListener('click', exportCsv);

    /* achievements demo toggle */
    $('#btn-empty-demo').addEventListener('click', function () {
      state.badgesEmpty = !state.badgesEmpty;
      renderAchievements();
    });
    $('#btn-badges-back').addEventListener('click', function () {
      state.badgesEmpty = false;
      renderAchievements();
    });

    /* settings */
    $('#set-name').addEventListener('input', function () { $('#name-err').hidden = true; });
    $('#set-goal').addEventListener('input', function () { $('#goal-readout').textContent = this.value + ' min'; });
    $('#set-dark').addEventListener('change', function () { document.body.classList.toggle('dark', this.checked); });
    $('#settings-form').addEventListener('submit', function (ev) {
      ev.preventDefault();
      var name = $('#set-name').value.trim();
      if (!name) {
        $('#name-err').hidden = false;
        $('#set-name').focus();
        return;
      }
      var btn = $('#btn-save');
      var saving = $('#set-saving');
      if (!saving) {
        saving = el('div', 'saving');
        saving.id = 'set-saving';
        saving.setAttribute('data-improvised', 'loading = meter compose, no spinner (not catalogued)');
        saving.innerHTML = '<p class="readout">Saving <span class="bdiv" aria-hidden="true"></span> <span class="fr" lang="fr">Enregistrement…</span></p><div class="meter"><i class="sweep"></i></div>';
        saving.hidden = true;
        $('.save-row').parentNode.insertBefore(saving, $('.save-row'));
      }
      btn.disabled = true; btn.textContent = 'Saving…';
      saving.hidden = false;
      window.setTimeout(function () {
        state.settings = {
          name: name,
          category: $('#set-cat').value,
          weekStart: ($$('input[name="weekstart"]').filter(function (r) { return r.checked; })[0] || {}).value || 'monday',
          goal: Number($('#set-goal').value),
          morning: $('#set-morning').checked,
          evening: $('#set-evening').checked
        };
        state.dark = $('#set-dark').checked;
        save();
        btn.disabled = false; btn.textContent = 'Save settings';
        saving.hidden = true;
        renderToday();
        showNotice('Saved. Your settings apply right away.');
      }, 700);
    });
    $('#btn-delete-all').addEventListener('click', function () {
      openConfirm('Delete all data?', 'Your rituals, checks and settings will be reset to the demo fixture. You can undo once, right after.', 'Delete everything', function () {
        undoAll = { removed: state.removed, order: state.order, done: state.done, extra: state.extra, settings: state.settings, dark: state.dark };
        state.removed = []; state.order = FIX.rituals.map(function (r) { return r.id; });
        state.done = {}; state.extra = []; state.settings = JSON.parse(JSON.stringify(FIX.settings)); state.dark = false;
        try { localStorage.removeItem(STORE_KEY); } catch (e) { /* noop */ }
        renderToday(); renderHistory(); renderAchievements(); renderSettings();
        closeOv('ov-detail');
        showNotice('Deleted. Everything is reset to the demo fixture.', {
          undo: function () {
            if (!undoAll) return;
            state.removed = undoAll.removed; state.order = undoAll.order; state.done = undoAll.done;
            state.extra = undoAll.extra; state.settings = undoAll.settings; state.dark = undoAll.dark;
            undoAll = null;
            save(); renderToday(); renderHistory(); renderAchievements(); renderSettings();
            showNotice('Restored. Your data is back.');
          }
        });
      });
    });

    /* wizard */
    $$('[data-open="wizard"]').forEach(function (b) {
      b.addEventListener('click', function () {
        wiz.step = 0; wiz.goal = state.settings.goal;
        renderWizard();
        openOv('ov-wizard');
      });
    });
    $('#wiz-skip').addEventListener('click', function () { closeOv('ov-wizard'); });
    $('#wiz-back').addEventListener('click', function () {
      if (wiz.step > 0) { wiz.step--; renderWizard(); }
    });
    $('#wiz-next').addEventListener('click', function () {
      if (wiz.step < WIZ_STEPS.length - 1) { wiz.step++; renderWizard(); return; }
      state.settings.goal = wiz.goal;
      if (state.removed.length) state.removed = [];   // intro re-seeds anything removed
      save();
      renderSettings(); renderToday();
      closeOv('ov-wizard');
      showNotice('You’re set. Check off a ritual when it’s done — replay this any time from Settings.');
    });
  }

  init();
})();
