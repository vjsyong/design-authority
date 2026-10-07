/* Cadence — leader-variant demo. Vanilla, single page, no network calls.
   Authority: pack 'leader' 0.1.0. Undefined needs are improvised in character,
   marked with data-improvised, and reported as gaps (see NOTES.md). */
(function () {
  'use strict';

  window.__cadenceDiag = { exports: 0, saves: 0 };

  /* ---------------- fixtures ---------------- */
  var RITUALS_DEFAULT = [
    { id: 'run',      name: 'Morning run',     cat: 'Movement',   min: 30, streak: 12, best: 21 },
    { id: 'read',     name: 'Read 20 pages',   cat: 'Mind',       min: 20, streak: 9,  best: 14 },
    { id: 'meditate', name: 'Meditate',        cat: 'Mind',       min: 10, streak: 21, best: 21 },
    { id: 'nosugar',  name: 'No sugar',        cat: 'Discipline', min: 0,  streak: 5,  best: 11 },
    { id: 'guitar',   name: 'Practice guitar', cat: 'Craft',      min: 25, streak: 7,  best: 9 }
  ];
  var DEFAULT_CHECKS = { run: false, read: true, meditate: true, nosugar: true, guitar: false };

  var WEEK_MINUTES = [45, 30, 60, 25, 50, 0, 35]; /* Mon..Sun */
  var DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  var HEAT = [45, 0, 30, 60, 20, 0, 60,
              45, 0, 25, 40, 0, 15, 60,
              30, 0, 45, 20, 0, 35, 55,
              0, 25, 45, 0, 30, 60, 0,
              40, 20, 0]; /* 1..31 Oct */

  var FIXTURE_ENTRIES = [
    { date: '7 Oct',  ritual: 'Read 20 pages',   min: 20, note: 'Finished the chapter on patience.' },
    { date: '7 Oct',  ritual: 'Meditate',        min: 10, note: 'Ten minutes before the call.' },
    { date: '6 Oct',  ritual: 'Morning run',     min: 30, note: 'Cold start, steady finish.' },
    { date: '6 Oct',  ritual: 'No sugar',        min: 0,  note: 'Kept it simple.' },
    { date: '5 Oct',  ritual: 'Practice guitar', min: 25, note: 'Chords, slowly.' },
    { date: '5 Oct',  ritual: 'Meditate',        min: 10, note: 'Late, but done.' },
    { date: '4 Oct',  ritual: 'Morning run',     min: 30, note: 'Rain. Treadmill instead.' },
    { date: '4 Oct',  ritual: 'Read 20 pages',   min: 20, note: 'Two chapters left.' },
    { date: '3 Oct',  ritual: 'No sugar',        min: 0,  note: 'Skipped dessert without a fuss.' },
    { date: '3 Oct',  ritual: 'Meditate',        min: 10, note: 'Quiet house, good focus.' },
    { date: '2 Oct',  ritual: 'Practice guitar', min: 25, note: 'Metronome at 80.' },
    { date: '2 Oct',  ritual: 'Morning run',     min: 30, note: 'Second wind at minute eight.' },
    { date: '1 Oct',  ritual: 'Read 20 pages',   min: 20, note: 'Read on the balcony.' },
    { date: '30 Sep', ritual: 'No sugar',        min: 0,  note: 'Fruit instead.' },
    { date: '30 Sep', ritual: 'Meditate',        min: 10, note: 'Counted to forty.' },
    { date: '29 Sep', ritual: 'Morning run',     min: 30, note: 'Hills. Slow.' },
    { date: '28 Sep', ritual: 'Practice guitar', min: 25, note: 'New chord shape.' },
    { date: '28 Sep', ritual: 'Read 20 pages',   min: 20, note: 'Borrowed book, good one.' },
    { date: '27 Sep', ritual: 'Meditate',        min: 10, note: 'Sat by the window.' },
    { date: '26 Sep', ritual: 'No sugar',        min: 0,  note: 'Easy day.' },
    { date: '26 Sep', ritual: 'Morning run',     min: 30, note: 'Felt strong.' },
    { date: '25 Sep', ritual: 'Read 20 pages',   min: 20, note: 'Reread a favourite page.' },
    { date: '24 Sep', ritual: 'Practice guitar', min: 25, note: 'Short session. Still counts.' },
    { date: '23 Sep', ritual: 'Meditate',        min: 10, note: 'Started again.' }
  ];

  var BADGES = [
    { name: 'First week',  meta: 'Seven days kept',     earned: true,  glyph: [12, 8] },
    { name: '10 days',     meta: 'Ten days kept',       earned: true,  glyph: [14] },
    { name: 'Early bird',  meta: 'Logged before 08:00', earned: true,  glyph: [8, 12] },
    { name: 'Century club',meta: '100 rituals logged',  earned: true,  glyph: [10, 14, 6] },
    { name: '21 days',     meta: '18 days to go',       earned: false, glyph: [12, 8] },
    { name: 'Perfect month', meta: '30 of 31 days',     earned: false, glyph: [14] }
  ];

  var CATGLYPH = { Movement: 'g-movement', Mind: 'g-mind', Craft: 'g-craft', Discipline: 'g-discipline' };
  var GLYPH_COUNT = { Movement: 1, Mind: 2, Craft: 3, Discipline: 1 };
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  var LS = 'cadence-leader-v1';
  var RING_C = 2 * Math.PI * 56;
  var PAGE = 8;

  /* ---------------- helpers ---------------- */
  function $(sel) { return document.querySelector(sel); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function fmtDate(v) {
    var p = String(v).split('-');
    if (p.length !== 3) { return v; }
    return parseInt(p[2], 10) + ' ' + MONTHS[parseInt(p[1], 10) - 1];
  }

  /* ---------------- state ---------------- */
  function defaults() {
    return {
      rituals: clone(RITUALS_DEFAULT),
      checked: Object.assign({}, DEFAULT_CHECKS),
      added: [],
      photos: {},
      badgesEmpty: false,
      settings: { name: 'Sam', cat: 'Mind', week: 'monday', goal: 30, remAM: true, remPM: true, dark: false }
    };
  }
  function loadState() {
    try {
      var raw = localStorage.getItem(LS);
      if (!raw) { return defaults(); }
      var s = JSON.parse(raw);
      if (!s || !Array.isArray(s.rituals) || !s.settings) { return defaults(); }
      return s;
    } catch (e) { return defaults(); }
  }
  function saveState() {
    try { localStorage.setItem(LS, JSON.stringify(state)); } catch (e) { /* storage off */ }
  }
  var state = loadState();

  function allEntries() { return state.added.concat(FIXTURE_ENTRIES); }

  /* ---------------- toast + celebration ---------------- */
  function toast(msg) {
    var t = document.createElement('div');
    t.className = 'toast';
    t.setAttribute('data-improvised', 'no toast canon; ruled readout');
    t.innerHTML = '<span class="sq" aria-hidden="true"></span><span></span>';
    t.lastChild.textContent = msg;
    $('#toast-region').appendChild(t);
    setTimeout(function () {
      t.classList.add('off');
      setTimeout(function () { t.remove(); }, 180);
    }, 2400);
  }

  var celTimer = null;
  function celebrate() {
    var c = $('#celebrate');
    c.classList.remove('on');
    void c.offsetWidth;
    c.classList.add('on');
    clearTimeout(celTimer);
    celTimer = setTimeout(function () { c.classList.remove('on'); }, 1200);
  }

  /* ---------------- render: today ---------------- */
  function renderRituals() {
    var list = $('#ritual-list');
    list.innerHTML = '';
    state.rituals.forEach(function (r) {
      var li = document.createElement('li');
      li.className = 'ritual' + (state.checked[r.id] ? ' done' : '');
      li.draggable = true;
      li.setAttribute('data-id', r.id);
      var n = GLYPH_COUNT[r.cat] || 1;
      var ii = '';
      for (var k = 0; k < n; k++) { ii += '<i></i>'; }
      li.innerHTML =
        '<span class="glyph ' + CATGLYPH[r.cat] + '" aria-hidden="true" data-improvised="no icon canon; rhythm glyph squares">' + ii + '</span>' +
        '<div class="rmain">' +
          '<button type="button" class="rname">' + esc(r.name) + '</button>' +
          '<div class="rmeta">' +
            '<span class="tag sm" data-improvised="no tag canon in pack; sheet L-13">' + esc(r.cat) + '</span>' +
            '<span class="meta">' + (r.min ? r.min + ' min' : 'no minutes') + '</span>' +
            '<span class="tag sm hair">' + r.streak + '-day</span>' +
          '</div>' +
        '</div>' +
        '<label class="cbx"><input type="checkbox" data-ritual="' + r.id + '"' + (state.checked[r.id] ? ' checked' : '') +
          ' aria-label="Toggle ' + esc(r.name) + ' done"><span class="box" aria-hidden="true"></span></label>' +
        '<span class="drag" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></span>';
      list.appendChild(li);
    });
    var hasAny = state.rituals.length > 0;
    $('#empty-rituals').hidden = hasAny;
    list.hidden = !hasAny;
  }

  function renderRing() {
    var total = state.rituals.length;
    var done = 0, mins = 0;
    state.rituals.forEach(function (r) {
      if (state.checked[r.id]) { done++; mins += r.min || 0; }
    });
    var pct = total ? done / total : 0;
    var arc = $('#ring-progress');
    arc.style.strokeDasharray = RING_C.toFixed(2);
    arc.style.strokeDashoffset = (RING_C * (1 - pct)).toFixed(2);
    $('#ring-count').textContent = done + ' of ' + total;
    $('#done-n').textContent = done;
    $('#total-n').textContent = total;
    $('#ring-wrap').setAttribute('aria-label', done + ' of ' + total + ' rituals done today');
    var goal = state.settings.goal;
    $('#today-min').textContent = mins + ' min logged today · goal ' + goal + ' min';
    var tag = $('#status-tag');
    if (goal > 0 && mins >= goal) {
      tag.textContent = 'On track';
      tag.classList.remove('red');
    } else {
      tag.textContent = 'Slipping';
      tag.classList.add('red');
    }
  }

  /* ---------------- render: history ---------------- */
  function renderBars() {
    var el = $('#bars');
    var w = 640, h = 170, base = 140, slot = w / 7, bw = 44, max = 60;
    var p = ['<svg viewBox="0 0 640 170" width="640" height="170" role="img" aria-label="Minutes logged each day this week">'];
    p.push('<line class="baseline" x1="8" y1="140" x2="632" y2="140"></line>');
    WEEK_MINUTES.forEach(function (v, i) {
      var x = i * slot + (slot - bw) / 2;
      var bh = Math.round(v / max * 110);
      var y = base - bh;
      if (v > 0) { p.push('<rect class="bar" x="' + x + '" y="' + y + '" width="' + bw + '" height="' + bh + '"></rect>'); }
      if (i === 1) { p.push('<rect class="cap" x="' + x + '" y="' + (y - 4) + '" width="' + bw + '" height="4"></rect>'); }
      p.push('<text x="' + (x + bw / 2) + '" y="' + (y - 8) + '" text-anchor="middle">' + v + '</text>');
      p.push('<text class="' + (i === 1 ? 'today' : '') + '" x="' + (x + bw / 2) + '" y="157" text-anchor="middle">' +
             DAY_NAMES[i].toUpperCase() + (i === 1 ? ' · TODAY' : '') + '</text>');
    });
    p.push('</svg>');
    el.innerHTML = p.join('');
  }

  function renderHeatmap() {
    var el = $('#heatmap');
    el.innerHTML = '';
    DAY_NAMES.forEach(function (d) {
      var s = document.createElement('span');
      s.className = 'hd';
      s.textContent = d;
      el.appendChild(s);
    });
    var blanks = (new Date(2026, 9, 1).getDay() + 6) % 7;
    for (var b = 0; b < blanks; b++) {
      var blank = document.createElement('div');
      blank.className = 'c blank';
      el.appendChild(blank);
    }
    HEAT.forEach(function (v, i) {
      var level = v === 0 ? 0 : (v <= 25 ? 1 : (v <= 50 ? 2 : 3));
      var c = document.createElement('div');
      c.className = 'c' + (level ? ' l' + level : '') + (i === 6 ? ' today' : '');
      c.title = (i + 1) + ' Oct · ' + v + ' min';
      el.appendChild(c);
    });
  }

  var page = 0;
  function renderLedger() {
    var q = ($('#filter').value || '').trim().toLowerCase();
    var all = allEntries();
    var rows;
    if (q) {
      rows = all.filter(function (e) {
        return (e.date + ' ' + e.ritual + ' ' + e.note).toLowerCase().indexOf(q) >= 0;
      });
    } else {
      rows = all.slice(page * PAGE, page * PAGE + PAGE);
    }
    var body = $('#ledger-body');
    body.innerHTML = '';
    if (rows.length === 0) {
      body.innerHTML = '<tr><td class="note" colspan="4">No entries match that filter.</td></tr>';
    }
    rows.forEach(function (e) {
      var tr = document.createElement('tr');
      tr.innerHTML = '<td class="n">' + esc(e.date) + '</td>' +
        '<td class="rname">' + esc(e.ritual) + '</td>' +
        '<td class="n">' + (e.min ? e.min : '—') + '</td>' +
        '<td class="note">' + esc(e.note) + '</td>';
      body.appendChild(tr);
    });
    var total = all.length;
    var lastPage = Math.max(0, Math.ceil(total / PAGE) - 1);
    if (q) {
      $('#page-meta').textContent = rows.length + ' of ' + total + ' entries match';
    } else {
      $('#page-meta').textContent = 'Showing ' + (total ? page * PAGE + 1 : 0) + '–' +
        Math.min((page + 1) * PAGE, total) + ' of ' + total;
    }
    $('#page-newer').disabled = q ? true : page <= 0;
    $('#page-older').disabled = q ? true : page >= lastPage;
  }

  /* ---------------- render: achievements ---------------- */
  function renderBadges() {
    var grid = $('#badge-grid');
    var empty = $('#badge-empty');
    grid.innerHTML = '';
    if (state.badgesEmpty) {
      grid.hidden = true;
      empty.hidden = false;
      return;
    }
    grid.hidden = false;
    empty.hidden = true;
    BADGES.forEach(function (b) {
      var d = document.createElement('div');
      d.className = 'badge' + (b.earned ? '' : ' locked');
      d.setAttribute('data-improvised', 'no badge canon; tag language');
      var mark = '<div class="bmark">' + b.glyph.map(function (g) {
        return '<i style="width:' + g + 'px;height:' + g + 'px"></i>';
      }).join('') + '</div>';
      var st = b.earned ? '<span class="tag sm">Earned</span>' : '<span class="tag sm hair">Locked</span>';
      d.innerHTML = mark + '<div class="bname">' + esc(b.name) + '</div>' +
        '<div class="bmeta meta">' + esc(b.meta) + '</div>' +
        '<div style="margin-top:10px">' + st + '</div>';
      grid.appendChild(d);
    });
  }

  function renderAll() {
    renderRituals();
    renderRing();
    renderLedger();
    renderBadges();
  }

  /* ---------------- sparkline (detail) ---------------- */
  function renderSpark(mount) {
    var max = 60, base = 40, bw = 16, slot = 36;
    var p = ['<svg viewBox="0 0 252 44" width="252" height="44" role="img" aria-label="Minutes over the last seven days">'];
    p.push('<line class="spline" x1="0" y1="40" x2="252" y2="40"></line>');
    WEEK_MINUTES.forEach(function (v, i) {
      var bh = Math.round(v / max * 30);
      if (v > 0) {
        p.push('<rect class="spbar" x="' + (i * slot) + '" y="' + (base - bh) + '" width="' + bw + '" height="' + bh + '"></rect>');
      }
    });
    p.push('</svg>');
    mount.innerHTML = p.join('');
  }

  /* ---------------- panels ---------------- */
  var slot = $('#panel-slot');
  var currentPanel = null;
  function closePanel() {
    if (currentPanel) { currentPanel.remove(); currentPanel = null; }
  }
  function mountPanel(el) {
    slot.appendChild(el);
    currentPanel = el;
    var h = el.querySelector('h2');
    if (h) { h.focus(); }
    el.addEventListener('click', function (ev) {
      if (ev.target.closest('[data-close]')) { closePanel(); }
    });
  }

  function openLog() {
    closePanel();
    if (!state.rituals.length) { toast('No rituals on the list'); return; }
    var el = document.createElement('section');
    el.className = 'panel';
    var opts = state.rituals.map(function (r) {
      return '<option value="' + esc(r.id) + '">' + esc(r.name) + '</option>';
    }).join('');
    el.innerHTML =
      '<div class="panel-head"><div><p class="slabel">Log</p><h2 class="h-display" tabindex="-1">Log a ritual</h2></div>' +
      '<button type="button" class="btn link" data-close>Close</button></div>' +
      '<div class="field" data-improvised="fallback/selection; native field styling"><label for="log-ritual">Ritual</label><select id="log-ritual">' + opts + '</select></div>' +
      '<div class="field" data-improvised="fallback/selection; native field styling"><label for="log-date">Date</label><input id="log-date" type="date" value="2026-10-07"><p class="err" id="log-date-err" hidden>Pick a date for the entry.</p></div>' +
      '<div class="field" data-improvised="no stepper canon; field-styled number"><label for="log-min">Minutes</label>' +
      '<div class="step-ctl"><button type="button" class="btn secondary" id="min-dec" aria-label="Fewer minutes">−</button>' +
      '<input id="log-min" type="number" min="1" max="600" value="30">' +
      '<button type="button" class="btn secondary" id="min-inc" aria-label="More minutes">+</button></div>' +
      '<p class="err" id="log-min-err" hidden>Enter between 1 and 600 minutes.</p></div>' +
      '<div class="field" data-improvised="field styling extended; no canon"><label for="log-notes">Notes</label><textarea id="log-notes" rows="3" placeholder="Optional"></textarea></div>' +
      '<div class="panel-actions"><button type="button" class="btn primary" id="log-submit">Log ritual</button>' +
      '<button type="button" class="btn link" data-close>Cancel</button></div>';
    mountPanel(el);
    var min = $('#log-min');
    $('#min-dec').addEventListener('click', function () {
      min.value = Math.max(1, (parseInt(min.value, 10) || 1) - 5);
    });
    $('#min-inc').addEventListener('click', function () {
      min.value = Math.min(600, (parseInt(min.value, 10) || 0) + 5);
    });
    $('#log-submit').addEventListener('click', function () {
      var dateV = $('#log-date').value;
      var minV = parseInt($('#log-min').value, 10);
      var ok = true;
      $('#log-date-err').hidden = true;
      $('#log-min-err').hidden = true;
      if (!dateV) { $('#log-date-err').hidden = false; ok = false; }
      if (!(minV >= 1 && minV <= 600)) { $('#log-min-err').hidden = false; ok = false; }
      if (!ok) { return; }
      var id = $('#log-ritual').value;
      var ritual = state.rituals.filter(function (r) { return r.id === id; })[0];
      if (!ritual) { toast('Pick a ritual'); return; }
      state.added.unshift({
        date: fmtDate(dateV),
        ritual: ritual.name,
        min: minV,
        note: ($('#log-notes').value || '').trim()
      });
      saveState();
      renderLedger();
      toast('Logged ✓');
      closePanel();
    });
  }

  function openDetail(id) {
    closePanel();
    var r = state.rituals.filter(function (x) { return x.id === id; })[0];
    if (!r) { return; }
    var el = document.createElement('section');
    el.className = 'panel';
    el.setAttribute('data-improvised', 'fallback/ruled-panel: in-flow, no scrim');
    var entries = allEntries().filter(function (e) { return e.ritual === r.name; }).slice(0, 5);
    var hist = entries.map(function (e) {
      return '<li><span class="hd-date">' + esc(e.date) + '</span><span class="hd-note">' + esc(e.note || 'Logged.') + '</span></li>';
    }).join('') || '<li><span class="hd-note">No entries yet.</span></li>';
    el.innerHTML =
      '<div class="panel-head"><div><p class="slabel">Ritual</p><h2 class="h-display" tabindex="-1">' + esc(r.name) + '</h2></div>' +
      '<button type="button" class="btn link" data-close>Close</button></div>' +
      '<div class="detail-meta"><span class="tag sm" data-improvised="no tag canon in pack; sheet L-13">' + esc(r.cat) + '</span>' +
      '<span class="meta">Current ' + r.streak + ' · Best ' + r.best + '</span></div>' +
      '<div class="spark" id="detail-spark" data-improvised="no chart canon; mini columns"></div>' +
      '<p class="meta-caps" style="margin-top:12px">Recent entries</p><ul class="hist">' + hist + '</ul>' +
      '<hr class="rule-hair">' +
      '<div class="field"><label for="detail-rename">Name</label><input id="detail-rename" type="text" value="' + esc(r.name) + '">' +
      '<p class="err" id="rename-err" hidden>A ritual needs a name.</p></div>' +
      '<div class="field" data-improvised="no upload canon; field-styled input"><label for="detail-photo">Photo</label>' +
      '<input id="detail-photo" type="file" accept="image/*">' +
      '<p class="hint" id="detail-photo-name">No photo chosen.</p>' +
      '<div class="frame" id="detail-frame"><img id="detail-photo-img" alt="Chosen ritual photo"></div></div>' +
      '<div class="panel-actions" id="detail-actions" data-improvised="destructive pattern from sheet; not in pack">' +
      '<button type="button" class="btn danger" id="detail-delete">Delete</button></div>' +
      '<div class="confirm" id="detail-confirm" hidden data-improvised="fallback/ruled-panel: in-flow, no scrim">' +
      '<p class="ct" tabindex="-1" id="detail-ct">Delete "' + esc(r.name) + '"?</p>' +
      '<p class="cb">It leaves the ritual list permanently. Its logged entries stay in history.</p>' +
      '<button type="button" class="btn danger" id="confirm-yes">Delete</button> ' +
      '<button type="button" class="btn secondary" id="confirm-no">Cancel</button></div>';
    mountPanel(el);
    renderSpark($('#detail-spark'));

    var rn = $('#detail-rename');
    rn.addEventListener('change', function () {
      var v = rn.value.trim();
      if (!v) {
        $('#rename-err').hidden = false;
        rn.value = r.name;
        return;
      }
      $('#rename-err').hidden = true;
      r.name = v;
      el.querySelector('h2').textContent = v;
      saveState();
      renderRituals();
    });

    var ph = $('#detail-photo');
    ph.addEventListener('change', function () {
      var f = ph.files && ph.files[0];
      if (!f) { return; }
      state.photos[r.id] = f.name;
      saveState();
      $('#detail-photo-name').textContent = f.name + ' · kept locally';
      $('#detail-photo-img').src = URL.createObjectURL(f);
      $('#detail-frame').classList.add('on');
    });
    if (state.photos[r.id]) {
      $('#detail-photo-name').textContent = state.photos[r.id] + ' · kept locally';
    }

    var actions = $('#detail-actions');
    var conf = $('#detail-confirm');
    $('#detail-delete').addEventListener('click', function () {
      actions.hidden = true;
      conf.hidden = false;
      $('#detail-ct').focus();
    });
    $('#confirm-no').addEventListener('click', function () {
      conf.hidden = true;
      actions.hidden = false;
    });
    $('#confirm-yes').addEventListener('click', function () {
      var idx = state.rituals.map(function (x) { return x.id; }).indexOf(r.id);
      state.rituals.splice(idx, 1);
      saveState();
      renderRituals();
      renderRing();
      closePanel();
      showUndo(r, idx);
    });
  }

  function showUndo(r, idx) {
    var mount = $('#undo-slot');
    mount.innerHTML = '';
    var n = document.createElement('div');
    n.className = 'notice';
    n.setAttribute('data-improvised', 'no undo canon; ruled notice');
    n.innerHTML = '<span></span><div class="rowlink">' +
      '<button type="button" class="btn link" id="undo-yes">Undo</button>' +
      '<button type="button" class="btn link" id="undo-no">Dismiss</button></div>';
    n.firstChild.textContent = r.name + ' deleted.';
    mount.appendChild(n);
    $('#undo-yes').addEventListener('click', function () {
      state.rituals.splice(Math.min(idx, state.rituals.length), 0, r);
      saveState();
      renderRituals();
      renderRing();
      mount.innerHTML = '';
    });
    $('#undo-no').addEventListener('click', function () { mount.innerHTML = ''; });
  }

  /* ---------------- onboarding wizard ---------------- */
  var introStep = 0;
  function openIntro() {
    closePanel();
    var el = document.createElement('section');
    el.className = 'panel';
    el.setAttribute('data-improvised', 'no wizard canon; ruled panel, step squares');
    el.innerHTML =
      '<div class="panel-head"><div><p class="slabel">Intro</p><h2 class="h-display" tabindex="-1" id="intro-title"></h2></div></div>' +
      '<div class="step-squares" id="intro-squares" aria-hidden="true"><i class="on"></i><i></i><i></i></div>' +
      '<div id="intro-body"></div>' +
      '<div class="panel-actions">' +
      '<button type="button" class="btn secondary" id="intro-back">Back</button>' +
      '<button type="button" class="btn primary" id="intro-next">Next</button>' +
      '<button type="button" class="btn link" id="intro-skip">Skip</button></div>';
    mountPanel(el);
    introStep = 0;
    renderIntro();
    $('#intro-skip').addEventListener('click', closePanel);
    $('#intro-back').addEventListener('click', function () {
      if (introStep > 0) { introStep--; renderIntro(); }
    });
    $('#intro-next').addEventListener('click', function () {
      if (introStep < 2) { introStep++; renderIntro(); return; }
      var g = document.getElementById('intro-goal');
      if (g) {
        state.settings.goal = parseInt(g.value, 10);
        $('#set-goal').value = state.settings.goal;
        $('#goal-read').textContent = state.settings.goal + ' min daily';
        saveState();
        renderRing();
      }
      var picks = document.querySelectorAll('#intro-body input[data-pick]');
      if (picks.length) {
        picks.forEach(function (p) { ensureRitual(p.getAttribute('data-pick'), p.checked); });
        saveState();
        renderAll();
      }
      closePanel();
    });
  }

  function ensureRitual(id, keep) {
    var idx = state.rituals.map(function (x) { return x.id; }).indexOf(id);
    var def = RITUALS_DEFAULT.filter(function (d) { return d.id === id; })[0];
    if (!def) { return; }
    if (!keep && idx >= 0) {
      state.rituals.splice(idx, 1);
    } else if (keep && idx < 0) {
      var di = RITUALS_DEFAULT.indexOf(def);
      state.rituals.splice(Math.min(di, state.rituals.length), 0, clone(def));
    }
  }

  function renderIntro() {
    var titles = ['Small rituals, kept daily.', 'Pick your rituals', 'Set your goal'];
    $('#intro-title').textContent = titles[introStep];
    var sq = $('#intro-squares').children;
    for (var i = 0; i < sq.length; i++) { sq[i].className = i <= introStep ? 'on' : ''; }
    var body = $('#intro-body');
    if (introStep === 0) {
      body.innerHTML = '<p class="stand" style="margin-top:0">Cadence tracks five small practices a day, and nothing more.</p>';
    } else if (introStep === 1) {
      body.innerHTML = '<ul class="intro-picks">' + state.rituals.map(function (r) {
        return '<li><label class="cbx" data-improvised="fallback/platform-controls; field styling">' +
          '<input type="checkbox" checked data-pick="' + esc(r.id) + '"><span class="box" aria-hidden="true"></span>' +
          '<span class="serif" style="font-size:15px">' + esc(r.name) + '</span></label>' +
          '<span class="meta">' + esc(r.cat) + ' · ' + (r.min ? r.min + ' min' : '—') + '</span></li>';
      }).join('') + '</ul><p class="hint">Uncheck what you will not keep.</p>';
    } else {
      body.innerHTML = '<div class="field" data-improvised="fallback/platform-controls; field styling">' +
        '<label for="intro-goal">Daily goal</label>' +
        '<input id="intro-goal" type="range" min="0" max="120" step="5" value="' + state.settings.goal + '"></div>' +
        '<p class="goal-read" id="intro-goal-read">' + state.settings.goal + ' min daily</p>';
      $('#intro-goal').addEventListener('input', function () {
        $('#intro-goal-read').textContent = this.value + ' min daily';
      });
    }
    $('#intro-next').textContent = introStep === 2 ? 'Done' : 'Next';
    $('#intro-back').disabled = introStep === 0;
  }

  /* ---------------- export ---------------- */
  function csvq(s) { return '"' + String(s).replace(/"/g, '""') + '"'; }
  function exportCsv() {
    var lines = ['date,ritual,minutes,notes'];
    allEntries().forEach(function (e) {
      lines.push([e.date, e.ritual, String(e.min), e.note].map(csvq).join(','));
    });
    var blob = new Blob([lines.join('\r\n')], { type: 'text/csv' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'cadence-entries.csv';
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    window.__cadenceDiag.exports++;
  }

  /* ---------------- settings ---------------- */
  function syncSettingsUI() {
    var s = state.settings;
    $('#set-name').value = s.name;
    $('#avatar-initial').textContent = (s.name || '?').trim().charAt(0).toUpperCase() || '?';
    $('#set-cat').value = s.cat;
    document.querySelectorAll('input[name=weekstart]').forEach(function (r) {
      r.checked = (r.value === s.week);
    });
    $('#set-goal').value = s.goal;
    $('#goal-read').textContent = s.goal + ' min daily';
    $('#rem-am').checked = s.remAM;
    $('#rem-pm').checked = s.remPM;
    $('#set-dark').checked = s.dark;
    document.body.classList.toggle('dark', !!s.dark);
    $('#greeting').textContent = 'Good evening, ' + s.name + '.';
  }

  $('#save-settings').addEventListener('click', function () {
    var btn = this;
    var name = $('#set-name').value.trim();
    if (!name) {
      $('#name-err').hidden = false;
      $('#set-name').focus();
      return;
    }
    $('#name-err').hidden = true;
    var saving = $('#saving');
    var meter = $('#save-meter');
    btn.disabled = true;
    saving.hidden = false;
    var step = 0;
    var iv = setInterval(function () {
      step++;
      meter.style.width = (step * 25) + '%';
      if (step >= 4) { clearInterval(iv); }
    }, 170);
    setTimeout(function () {
      saving.hidden = true;
      meter.style.width = '0';
      btn.disabled = false;
      state.settings.name = name;
      state.settings.cat = $('#set-cat').value;
      var wk = document.querySelector('input[name=weekstart]:checked');
      state.settings.week = wk ? wk.value : 'monday';
      state.settings.goal = parseInt($('#set-goal').value, 10) || 0;
      state.settings.remAM = $('#rem-am').checked;
      state.settings.remPM = $('#rem-pm').checked;
      saveState();
      syncSettingsUI();
      renderRing();
      toast('Saved');
      window.__cadenceDiag.saves++;
    }, 700);
  });

  $('#set-dark').addEventListener('change', function () {
    state.settings.dark = this.checked;
    document.body.classList.toggle('dark', this.checked);
    saveState();
  });

  $('#set-goal').addEventListener('input', function () {
    $('#goal-read').textContent = this.value + ' min daily';
  });

  $('#export-history').addEventListener('click', exportCsv);
  $('#export-settings').addEventListener('click', exportCsv);
  $('#replay-intro').addEventListener('click', openIntro);

  $('#delete-all').addEventListener('click', function () {
    $('#danger-confirm').hidden = false;
    $('#danger-ct').focus();
  });
  $('#danger-no').addEventListener('click', function () {
    $('#danger-confirm').hidden = true;
  });
  $('#danger-yes').addEventListener('click', function () {
    try { localStorage.removeItem(LS); } catch (e) { /* ignore */ }
    state = defaults();
    saveState();
    $('#danger-confirm').hidden = true;
    syncSettingsUI();
    renderAll();
    toast('Data cleared');
  });

  /* ---------------- nav, marks, list events ---------------- */
  $('#tabs').addEventListener('click', function (ev) {
    var b = ev.target.closest('.tab');
    if (!b) { return; }
    var name = b.getAttribute('data-view');
    ['today', 'history', 'achievements', 'settings'].forEach(function (v) {
      document.getElementById('view-' + v).hidden = (v !== name);
    });
    document.querySelectorAll('.tab').forEach(function (t) {
      var on = t.getAttribute('data-view') === name;
      t.classList.toggle('on', on);
      if (on) { t.setAttribute('aria-current', 'page'); } else { t.removeAttribute('aria-current'); }
    });
    closePanel();
  });

  $('#marks-toggle').addEventListener('click', function () {
    var on = document.body.classList.toggle('show-marks');
    this.setAttribute('aria-pressed', on ? 'true' : 'false');
  });

  $('#ritual-list').addEventListener('click', function (ev) {
    var b = ev.target.closest('.rname');
    if (b) {
      var li = b.closest('.ritual');
      openDetail(li.getAttribute('data-id'));
    }
  });

  $('#ritual-list').addEventListener('change', function (ev) {
    var cb = ev.target.closest('input[data-ritual]');
    if (!cb) { return; }
    var id = cb.getAttribute('data-ritual');
    state.checked[id] = cb.checked;
    saveState();
    var li = cb.closest('.ritual');
    if (li) { li.classList.toggle('done', cb.checked); }
    renderRing();
    if (cb.checked) {
      celebrate();
      toast('Logged ✓');
    }
  });

  /* drag to reorder */
  var dragId = null;
  $('#ritual-list').addEventListener('dragstart', function (ev) {
    var li = ev.target.closest('.ritual');
    if (!li) { return; }
    dragId = li.getAttribute('data-id');
    li.classList.add('dragging');
    ev.dataTransfer.effectAllowed = 'move';
    try { ev.dataTransfer.setData('text/plain', dragId); } catch (e) { /* ignore */ }
  });
  $('#ritual-list').addEventListener('dragover', function (ev) {
    var over = ev.target.closest('.ritual');
    if (!over || !dragId) { return; }
    ev.preventDefault();
    var dragging = document.querySelector('.ritual.dragging');
    if (!dragging || over === dragging) { return; }
    var rect = over.getBoundingClientRect();
    var after = (ev.clientY - rect.top) > rect.height / 2;
    over.parentNode.insertBefore(dragging, after ? over.nextSibling : over);
  });
  $('#ritual-list').addEventListener('drop', function (ev) { ev.preventDefault(); });
  $('#ritual-list').addEventListener('dragend', function () {
    var dragging = document.querySelector('.ritual.dragging');
    if (dragging) { dragging.classList.remove('dragging'); }
    var ids = [].map.call(document.querySelectorAll('#ritual-list .ritual'), function (li) {
      return li.getAttribute('data-id');
    });
    state.rituals.sort(function (a, b) { return ids.indexOf(a.id) - ids.indexOf(b.id); });
    saveState();
    dragId = null;
  });

  /* filter + pagination */
  $('#filter').addEventListener('input', function () {
    page = 0;
    renderLedger();
  });
  $('#page-newer').addEventListener('click', function () {
    page = Math.max(0, page - 1);
    renderLedger();
  });
  $('#page-older').addEventListener('click', function () {
    page = Math.min(Math.ceil(allEntries().length / PAGE) - 1, page + 1);
    renderLedger();
  });

  $('#restore-rituals').addEventListener('click', function () {
    state.rituals = clone(RITUALS_DEFAULT);
    state.checked = Object.assign({}, DEFAULT_CHECKS);
    saveState();
    renderAll();
  });

  $('#badge-demo').addEventListener('change', function () {
    state.badgesEmpty = this.checked;
    saveState();
    renderBadges();
  });
  $('#badge-empty-back').addEventListener('click', function () {
    state.badgesEmpty = false;
    $('#badge-demo').checked = false;
    saveState();
    renderBadges();
  });

  $('#open-log').addEventListener('click', openLog);

  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') { closePanel(); }
  });

  /* ---------------- init ---------------- */
  syncSettingsUI();
  renderRituals();
  renderRing();
  renderBars();
  renderHeatmap();
  renderLedger();
  renderBadges();
  window.__cadenceReady = true;
})();
