/* Cadence — app logic. Built against Design Authority pack 'leader' v0.1.0.
   All fixtures local; persistence via localStorage; no network calls. */

(function () {
  'use strict';

  var KEY = 'cadence2-leader-v1';
  var C = 2 * Math.PI * 52; /* ring circumference, r=52 */

  /* ---------------- fixtures ---------------- */
  var F_RITUALS = [
    { id: 'r1', name: 'Morning run', cat: 'Movement', min: 30, streak: 12, done: true, glyph: [14, 7], spark: [30, 30, 0, 45, 30, 30, 30] },
    { id: 'r2', name: 'Read 20 pages', cat: 'Mind', min: 20, streak: 9, done: false, glyph: [7, 7, 7], spark: [20, 20, 20, 20, 0, 20, 20] },
    { id: 'r3', name: 'Meditate', cat: 'Mind', min: 10, streak: 21, done: true, glyph: ['h12'], spark: [10, 0, 10, 10, 10, 10, 10] },
    { id: 'r4', name: 'No sugar', cat: 'Discipline', min: null, streak: 4, done: true, glyph: [6, 14], spark: [1, 1, 0, 1, 1, 1, 1] },
    { id: 'r5', name: 'Practice guitar', cat: 'Craft', min: 25, streak: 7, done: false, glyph: [16, 4], spark: [25, 25, 0, 25, 25, 25, 25] }
  ];
  var MARK_SET = [[14, 7], [7, 7, 7], ['h12'], [6, 14], [16, 4], [10], [4, 10, 4]];

  var F_ENTRIES = [
    { date: 'Tue 7 Oct', rit: 'Meditate', cat: 'Mind', min: 10 },
    { date: 'Tue 7 Oct', rit: 'Morning run', cat: 'Movement', min: 30 },
    { date: 'Mon 6 Oct', rit: 'Read 20 pages', cat: 'Mind', min: 20 },
    { date: 'Mon 6 Oct', rit: 'Practice guitar', cat: 'Craft', min: 25 },
    { date: 'Sun 5 Oct', rit: 'No sugar', cat: 'Discipline', min: null },
    { date: 'Sun 5 Oct', rit: 'Morning run', cat: 'Movement', min: 45 },
    { date: 'Sat 4 Oct', rit: 'Meditate', cat: 'Mind', min: 10 },
    { date: 'Sat 4 Oct', rit: 'Practice guitar', cat: 'Craft', min: 25 },
    { date: 'Fri 3 Oct', rit: 'Morning run', cat: 'Movement', min: 30 },
    { date: 'Fri 3 Oct', rit: 'Read 20 pages', cat: 'Mind', min: 20 },
    { date: 'Thu 2 Oct', rit: 'Morning run', cat: 'Movement', min: 30 },
    { date: 'Thu 2 Oct', rit: 'No sugar', cat: 'Discipline', min: null },
    { date: 'Wed 1 Oct', rit: 'Meditate', cat: 'Mind', min: 10 },
    { date: 'Wed 1 Oct', rit: 'Practice guitar', cat: 'Craft', min: 25 },
    { date: 'Tue 30 Sep', rit: 'Morning run', cat: 'Movement', min: 30 },
    { date: 'Tue 30 Sep', rit: 'Read 20 pages', cat: 'Mind', min: 20 },
    { date: 'Mon 29 Sep', rit: 'Meditate', cat: 'Mind', min: 10 },
    { date: 'Mon 29 Sep', rit: 'No sugar', cat: 'Discipline', min: null },
    { date: 'Sun 28 Sep', rit: 'Morning run', cat: 'Movement', min: 45 },
    { date: 'Sun 28 Sep', rit: 'Practice guitar', cat: 'Craft', min: 25 },
    { date: 'Sat 27 Sep', rit: 'Meditate', cat: 'Mind', min: 10 },
    { date: 'Sat 27 Sep', rit: 'Read 20 pages', cat: 'Mind', min: 20 },
    { date: 'Fri 26 Sep', rit: 'Morning run', cat: 'Movement', min: 30 },
    { date: 'Fri 26 Sep', rit: 'No sugar', cat: 'Discipline', min: null }
  ];

  var ORIG_ENTRIES = JSON.parse(JSON.stringify(F_ENTRIES));
  var WEEK = [45, 30, 60, 25, 50, 0, 35];
  var DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  var HEAT = { 1: 45, 2: 30, 3: 60, 4: 25, 5: 50, 6: 0, 7: 35 };
  var BADGES = [
    { name: 'First week', earned: true, glyph: [10] },
    { name: '10 days', earned: true, glyph: [8, 12] },
    { name: 'Early bird', earned: true, glyph: [6, 10, 14] },
    { name: 'Century club', earned: true, glyph: [10, 10, 10, 10] },
    { name: '21 days', earned: false, glyph: [12, 6] },
    { name: 'Perfect month', earned: false, glyph: [8, 8, 8, 8] }
  ];

  function defaults() {
    return {
      rituals: JSON.parse(JSON.stringify(F_RITUALS)),
      settings: { name: 'Sam', cat: 'Mind', weekStart: 'mon', goal: 30, remAm: true, remPm: false, dark: false }
    };
  }

  /* ---------------- state ---------------- */
  var S = load();
  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return defaults();
      var d = JSON.parse(raw);
      var s = defaults();
      if (Array.isArray(d.rituals)) s.rituals = d.rituals;
      if (d.settings) Object.assign(s.settings, d.settings);
      return s;
    } catch (e) { return defaults(); }
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify({ rituals: S.rituals, settings: S.settings })); } catch (e) {}
  }

  /* ---------------- helpers ---------------- */
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  function glyphHTML(sizes, cls) {
    return '<span class="glyph ' + (cls || '') + '">' + sizes.map(function (g) {
      if (typeof g === 'string' && g.charAt(0) === 'h') {
        var s = parseInt(g.slice(1), 10) - 4;
        return '<i class="hollow" style="width:' + s + 'px;height:' + s + 'px"></i>';
      }
      return '<i style="width:' + g + 'px;height:' + g + 'px"></i>';
    }).join('') + '</span>';
  }

  var noticeTimers = {};
  function notice(viewId, text, action) {
    var slot = $('#slot-' + viewId);
    if (!slot) return null;
    slot.innerHTML = '';
    var el = document.createElement('div');
    el.className = 'notice';
    el.setAttribute('data-adapted', 'toast → ruled notice (component/notice: no toasts in system)');
    var p = document.createElement('p');
    p.textContent = text;
    el.appendChild(p);
    if (action) {
      var b = document.createElement('button');
      b.className = 'btn b-txt sm act';
      b.textContent = action.label;
      b.setAttribute('data-improvised', 'undo = ruled notice + tertiary link');
      b.addEventListener('click', function () { action.fn(); });
      el.appendChild(b);
    }
    slot.appendChild(el);
    clearTimeout(noticeTimers[viewId]);
    noticeTimers[viewId] = setTimeout(function () { slot.innerHTML = ''; }, action ? 6000 : 2800);
    return el;
  }

  function loading(host, label) {
    return new Promise(function (resolve) {
      var el = document.createElement('div');
      el.className = 'loading';
      el.setAttribute('data-improvised', 'spinner → stepped meter (L-16 static register; no motion)');
      el.innerHTML = '<span class="track"><i style="width:25%"></i></span><span class="meta">' + (label || 'Saving') + '</span>';
      host.appendChild(el);
      var fill = $('i', el);
      var steps = [[240, 55], [480, 85], [700, 100]];
      steps.forEach(function (st) { setTimeout(function () { fill.style.width = st[1] + '%'; }, st[0]); });
      setTimeout(function () { resolve(el); }, 760);
    });
  }

  function celebrate() {
    var st = $('#stamp');
    st.classList.add('on');
    setTimeout(function () { st.classList.remove('on'); }, 1600);
  }

  /* ---------------- views ---------------- */
  function showView(name) {
    $$('.view').forEach(function (v) { v.hidden = (v.id !== 'view-' + name); });
    $$('.tab, .tabbar a').forEach(function (t) {
      var on = t.getAttribute('data-view') === name;
      t.classList.toggle('on', on);
      if (on) { t.setAttribute('aria-current', 'page'); } else { t.removeAttribute('aria-current'); }
    });
    window.scrollTo(0, 0);
  }
  $$('.tab, .tabbar a').forEach(function (t) {
    t.addEventListener('click', function (e) { e.preventDefault(); showView(t.getAttribute('data-view')); });
  });

  /* ---------------- today ---------------- */
  function doneCount() { return S.rituals.filter(function (r) { return r.done; }).length; }

  function renderRing() {
    var n = S.rituals.length;
    var d = doneCount();
    var pct = n ? d / n : 0;
    $('#ringArc').setAttribute('stroke-dasharray', (C * pct).toFixed(2) + ' ' + C.toFixed(2));
    $('#ringPct').textContent = Math.round(pct * 100) + '%';
    $('.ringbox svg') && $('#ringSvg').setAttribute('aria-label', 'Today ' + Math.round(pct * 100) + ' percent complete');
    $('#doneReadout').textContent = d + ' of ' + n + ' rituals done';
    var tag = $('#statusTag');
    var on = n > 0 && d / n >= 0.6;
    tag.textContent = on ? 'On track' : 'Slipping';
    tag.classList.toggle('attn', !on);
  }

  function renderList() {
    var ul = $('#ritualList');
    ul.innerHTML = '';
    S.rituals.forEach(function (r, i) {
      var li = document.createElement('li');
      li.className = 'ritual';
      li.draggable = true;
      li.setAttribute('data-id', r.id);
      li.innerHTML =
        '<button class="handle" aria-label="Drag to reorder ' + esc(r.name) + '" data-improvised="native drag; red insertion rule"><i></i><i></i></button>' +
        glyphHTML(r.glyph, 'mark') .replace('class="glyph mark"', 'class="glyph mark" data-improvised="rhythm glyphs (deck L-08) as ritual marks"') +
        '<span class="rbody"><span class="name">' + esc(r.name) + '</span>' +
        '<span class="sub"><span class="tag" data-improvised="tag per deck L-13">' + esc(r.cat) + '</span>' +
        (r.min ? '<span class="meta">' + r.min + ' min</span>' : '') + '</span></span>' +
        '<span class="tags"><span class="tag">' + r.streak + 'D</span></span>' +
        '<button class="check' + (r.done ? ' on' : '') + '" aria-pressed="' + r.done + '" aria-label="' + (r.done ? 'Unmark ' : 'Mark ') + esc(r.name) + ' done">' +
        '<svg viewBox="0 0 14 12" aria-hidden="true"><path d="M1 6.2l4 4L13 1" fill="none" stroke="#fff" stroke-width="2.4"/></svg></button>';
      $('.check', li).addEventListener('click', function (e) { e.stopPropagation(); toggleCheck(r.id); });
      $('.handle', li).addEventListener('click', function (e) { e.stopPropagation(); });
      li.addEventListener('click', function () { openDetail(r.id); });
      li.addEventListener('dragstart', function (e) { dragId = r.id; try { e.dataTransfer.setData('text/plain', r.id); e.dataTransfer.effectAllowed = 'move'; } catch (x) {} });
      li.addEventListener('dragover', function (e) { e.preventDefault(); li.classList.add('dragover'); });
      li.addEventListener('dragleave', function () { li.classList.remove('dragover'); });
      li.addEventListener('drop', function (e) { e.preventDefault(); li.classList.remove('dragover'); var from = ''; try { from = e.dataTransfer.getData('text/plain'); } catch (x) {} reorder(from || dragId, r.id); });
      li.addEventListener('dragend', function () { $$('.ritual.dragover').forEach(function (x) { x.classList.remove('dragover'); }); });
      ul.appendChild(li);
    });
  }
  var dragId = '';

  function reorder(fromId, toId) {
    if (!fromId || !toId || fromId === toId) return;
    var from = S.rituals.findIndex(function (r) { return r.id === fromId; });
    var to = S.rituals.findIndex(function (r) { return r.id === toId; });
    if (from < 0 || to < 0) return;
    var moved = S.rituals.splice(from, 1)[0];
    S.rituals.splice(to, 0, moved);
    save();
    renderList();
  }

  function toggleCheck(id) {
    var r = S.rituals.find(function (x) { return x.id === id; });
    if (!r) return;
    r.done = !r.done;
    save();
    renderRing();
    renderList();
    if (r.done) {
      notice('today', 'Logged ✓ — ' + r.name + (r.min ? ', ' + r.min + ' min' : '') + '.');
      celebrate();
    }
  }

  function renderToday() {
    renderRing();
    renderList();
    var empty = S.rituals.length === 0;
    $('#todayMain').hidden = empty;
    $('#todayEmpty').hidden = !empty;
    if (empty) {
      $('#todayEmpty').innerHTML =
        '<div class="empty" data-improvised="empty state: ruled statement block, one action (deck L-17)">' +
        '<div class="eglyph" data-adapted="illustration → glyph mark (no imagery: deck L-17/L-21)">' + glyphHTML([6, 9, 13, 8]) + '</div>' +
        '<h3>No rituals yet.</h3>' +
        '<p class="pdek">One small thing, kept daily, is enough to begin.</p>' +
        '<button class="btn b-out" id="restoreDemo">Restore demo data</button></div>';
      $('#restoreDemo').addEventListener('click', restoreDemo);
    }
  }

  function restoreDemo() {
    S.rituals = JSON.parse(JSON.stringify(F_RITUALS));
    F_ENTRIES.length = 0;
    ORIG_ENTRIES.forEach(function (e) { F_ENTRIES.push(JSON.parse(JSON.stringify(e))); });
    save();
    renderAll();
    notice('today', 'Demo data restored.');
  }

  /* ---------------- detail panel ---------------- */
  function openDetail(id) {
    var r = S.rituals.find(function (x) { return x.id === id; });
    if (!r) return;
    var host = $('#panelHost');
    host.innerHTML = '';
    var tabRows = F_ENTRIES.filter(function (e) { return e.rit === r.name; }).slice(0, 3);
    var wrap = document.createElement('div');
    wrap.className = 'panel';
    wrap.id = 'detailPanel';
    wrap.setAttribute('data-improvised', 'fallback/ruled-panel: in-flow detail panel (no scrim, no motion)');
    wrap.innerHTML =
      '<div class="phead"><p class="lab">Ritual detail</p><button class="btn b-txt sm act" id="closeDetail">Close</button></div>' +
      '<h2>' + esc(r.name) + '</h2>' +
      '<p class="meta">' + esc(r.cat) + (r.min ? ' · ' + r.min + ' min' : '') + ' · ' + r.streak + '-day streak</p>' +
      '<p class="lab" style="margin-top:18px">Last seven days</p>' +
      '<div class="spark" data-improvised="mini bar trend (no canonical sparkline)">' + sparkHTML(r.spark) + '</div>' +
      '<p class="meta">Minutes logged per day. Today ' + (r.done ? 'is checked.' : 'is open.') + '</p>' +
      '<p class="lab" style="margin-top:18px">History</p>' +
      '<div>' + (tabRows.length ? tabRows.map(function (e) {
        return '<div style="display:flex;justify-content:space-between;border-bottom:1px solid var(--line);padding:7px 0;max-width:420px">' +
          '<span class="meta" style="margin:0">' + esc(e.date) + '</span>' +
          '<span class="meta" style="margin:0">' + (e.min ? e.min + ' min' : 'kept') + '</span></div>';
      }).join('') : '<p class="meta">No entries yet.</p>') + '</div>' +
      '<div class="pact"><button class="btn b-out danger-tx" id="askDelete" data-improvised="destructive: red verb rect per deck L-15 (no canonical pattern)">Delete ritual</button></div>' +
      '<div id="confirmHost"></div>';
    host.appendChild(wrap);
    $('#closeDetail').addEventListener('click', closeDetail);
    $('#askDelete').addEventListener('click', function () {
      var ch = $('#confirmHost');
      ch.innerHTML =
        '<div class="panel confirm" data-improvised="fallback/ruled-panel: inline confirmation (no scrim, no motion)">' +
        '<p class="pdek">Delete "' + esc(r.name) + '"? Its log history is removed.</p>' +
        '<div class="pact"><button class="btn b-red" id="confirmDelete">Delete</button>' +
        '<button class="btn b-out" id="cancelDelete">Keep</button></div></div>';
      $('#confirmDelete').addEventListener('click', function () { doDelete(r.id); });
      $('#cancelDelete').addEventListener('click', function () { ch.innerHTML = ''; });
      $('#cancelDelete').focus();
    });
    wrap.scrollIntoView({ block: 'nearest' });
  }

  function sparkHTML(vals) {
    var max = Math.max.apply(null, vals.concat([1]));
    var maxI = vals.indexOf(max);
    return vals.map(function (v, i) {
      var h = 6 + Math.round((v / max) * 30);
      return '<i class="' + (i === maxI && v > 0 ? 'hi' : '') + '" style="height:' + h + 'px"></i>';
    }).join('');
  }

  function closeDetail() { $('#panelHost').innerHTML = ''; }

  var undoData = null;
  function doDelete(id) {
    var i = S.rituals.findIndex(function (x) { return x.id === id; });
    if (i < 0) return;
    undoData = { ritual: S.rituals[i], index: i };
    S.rituals.splice(i, 1);
    save();
    closeDetail();
    renderAll();
    notice('today', 'Ritual deleted.', { label: 'Undo', fn: function () {
      if (!undoData) return;
      S.rituals.splice(undoData.index, 0, undoData.ritual);
      undoData = null;
      save();
      renderAll();
      notice('today', 'Ritual restored.');
    } });
  }

  /* ---------------- log form ---------------- */
  function openLogForm() {
    var host = $('#panelHost');
    if ($('#logPanel')) { closeLogForm(); return; }
    host.innerHTML = '';
    var opts = S.rituals.map(function (r) { return '<option value="' + r.id + '">' + esc(r.name) + '</option>'; }).join('');
    var form = document.createElement('div');
    form.className = 'panel';
    form.id = 'logPanel';
    form.setAttribute('data-improvised', 'form expands as ruled panel in flow (no dialog canon)');
    form.innerHTML =
      '<div class="phead"><p class="lab">Log a ritual</p><button class="btn b-txt sm act" id="closeLog">Close</button></div>' +
      '<div class="field" id="fRitual"><label for="logRitual">Ritual</label>' +
      '<select id="logRitual"><option value="">Choose…</option>' + opts + '</select>' +
      '<p class="err">Choose a ritual.</p></div>' +
      '<div class="row2">' +
      '<div class="field"><label for="logDate">Date</label><input type="date" id="logDate" value="2026-10-07" data-improvised="fallback/platform-controls: native date, field styling"></div>' +
      '<div class="field" id="fMinutes"><label for="logMinutes">Minutes</label>' +
      '<div class="stepper"><button class="sbtn" id="minMinus" type="button" aria-label="Fewer minutes">−</button>' +
      '<input type="number" id="logMinutes" min="0" step="5" value="30" data-improvised="fallback/platform-controls: native number + stepper buttons">' +
      '<button class="sbtn" id="minPlus" type="button" aria-label="More minutes">+</button></div>' +
      '<p class="err">Enter minutes above zero.</p></div>' +
      '</div>' +
      '<div class="field"><label for="logNotes">Notes</label><textarea id="logNotes" placeholder="How did it go?"></textarea></div>' +
      '<div class="field" data-adapted="photo upload → ritual mark picker (no imagery in system)"><label>Ritual mark</label>' +
      '<div class="markpicker" id="markPicker">' + MARK_SET.map(function (m, i) {
        return '<button type="button" class="markbtn' + (i === 0 ? ' on' : '') + '" data-mark="' + i + '">' + glyphHTML(m) + '</button>';
      }).join('') + '</div></div>' +
      '<div class="pact"><button class="btn b-navy" id="submitLog">Log ritual</button>' +
      '<button class="btn b-out" id="cancelLog">Cancel</button></div>' +
      '<div id="logLoading"></div>';
    host.appendChild(form);
    $('#closeLog').addEventListener('click', closeLogForm);
    $('#cancelLog').addEventListener('click', closeLogForm);
    $('#minMinus').addEventListener('click', function () { stepMin(-5); });
    $('#minPlus').addEventListener('click', function () { stepMin(5); });
    $('#logRitual').addEventListener('change', function () {
      var r = S.rituals.find(function (x) { return x.id === $('#logRitual').value; });
      if (r && r.min) $('#logMinutes').value = r.min;
    });
    $$('.markbtn', form).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('.markbtn', form).forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on');
      });
    });
    $('#submitLog').addEventListener('click', submitLog);
    form.scrollIntoView({ block: 'nearest' });
  }
  function stepMin(d) {
    var inp = $('#logMinutes');
    var v = parseInt(inp.value, 10); if (isNaN(v)) v = 0;
    inp.value = Math.max(0, v + d);
  }
  function closeLogForm() { var p = $('#logPanel'); if (p) p.remove(); }

  function submitLog() {
    var sel = $('#logRitual').value;
    var mins = parseInt($('#logMinutes').value, 10);
    var fR = $('#fRitual'), fM = $('#fMinutes');
    fR.classList.toggle('invalid', !sel);
    fM.classList.toggle('invalid', !(mins > 0));
    if (!sel || !(mins > 0)) return;
    var r = S.rituals.find(function (x) { return x.id === sel; });
    $('#submitLog').disabled = true;
    $('#cancelLog').disabled = true;
    var mark = parseInt($('.markbtn.on').getAttribute('data-mark'), 10);
    loading($('#logLoading')).then(function (el) {
      el.remove();
      if (r) {
        r.done = true;
        r.glyph = MARK_SET[mark];
        F_ENTRIES.unshift({ date: 'Tue 7 Oct', rit: r.name, cat: r.cat, min: mins });
      }
      save();
      closeLogForm();
      renderToday();
      renderHistory();
      notice('today', 'Logged ✓ — ' + (r ? r.name : 'ritual') + ', ' + mins + ' min.');
      celebrate();
    });
  }

  /* ---------------- history ---------------- */
  var page = 1, filterQ = '';

  function renderBars() {
    var max = Math.max.apply(null, WEEK.concat([1]));
    $('#barChart').innerHTML = '<div class="bars">' + WEEK.map(function (v) {
      var h = v === 0 ? 2 : Math.max(4, Math.round((v / max) * 118));
      return '<div class="bar-col"><span class="val">' + v + '</span><span class="bar' + (v === 0 ? ' zero' : '') + '" style="height:' + h + 'px"></span></div>';
    }).join('') + '</div>';
    $('#barDays').innerHTML = DAYS.map(function (d) { return '<span>' + d + '</span>'; }).join('');
  }

  function renderHeat() {
    var rows = [
      { label: 'Sep 28', days: [null, null, null, 1, 2, 3, 4] },
      { label: 'Oct 5', days: [5, 6, 7, 8, 9, 10, 11] },
      { label: 'Oct 12', days: [12, 13, 14, 15, 16, 17, 18] },
      { label: 'Oct 19', days: [19, 20, 21, 22, 23, 24, 25] },
      { label: 'Oct 26', days: [26, 27, 28, 29, 30, 31, null] }
    ];
    var head = '<div class="hrow"><span class="hday"></span>' + ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su'].map(function (d) {
      return '<span class="hday" style="width:24px;flex:0 0 24px;text-align:center;font-size:11px;line-height:24px">' + d + '</span>';
    }).join('') + '</div>';
    function lv(d) {
      if (d === null) return null;
      if (d > 7) return 'lv0';
      var v = HEAT[d] || 0;
      if (v === 0) return 'lv0';
      if (v <= 20) return 'lv1';
      if (v <= 40) return 'lv2';
      if (v <= 55) return 'lv3';
      return 'lv4';
    }
    var body = rows.map(function (row) {
      return '<div class="hrow"><span class="hday">' + row.label + '</span>' + row.days.map(function (d) {
        if (d === null) return '<i class="blank"></i>';
        return '<i class="' + lv(d) + (d === 7 ? ' today' : '') + '" title="' + d + ' Oct ' + (HEAT[d] ? '— ' + HEAT[d] + ' min' : '— no entry') + '"></i>';
      }).join('') + '</div>';
    }).join('');
    $('#heatmap').innerHTML = head + body;
  }

  function visibleEntries() {
    var names = S.rituals.map(function (r) { return r.name; });
    return F_ENTRIES.filter(function (e) { return names.indexOf(e.rit) >= 0; }).filter(function (e) {
      if (!filterQ) return true;
      var t = (e.date + ' ' + e.rit + ' ' + e.cat).toLowerCase();
      return t.indexOf(filterQ) >= 0;
    });
  }

  function renderTable() {
    var rows = visibleEntries();
    var per = 8;
    var pages = Math.max(1, Math.ceil(rows.length / per));
    if (page > pages) page = pages;
    var start = (page - 1) * per;
    var slice = rows.slice(start, start + per);
    var tb = $('#ledgerBody');
    if (!slice.length) {
      tb.innerHTML = '<tr class="emptyrow"><td colspan="4">No entries match.</td></tr>';
    } else {
      tb.innerHTML = slice.map(function (e) {
        return '<tr><td>' + esc(e.date) + '</td><td class="rit">' + esc(e.rit) + '</td>' +
          '<td><span class="tag mute">' + esc(e.cat) + '</span></td>' +
          '<td class="num">' + (e.min ? e.min : '—') + '</td></tr>';
      }).join('');
    }
    $('#pageMeta').textContent = rows.length ? (start + 1) + '–' + Math.min(start + per, rows.length) + ' of ' + rows.length : '0 of 0';
    $('#pageOlder').disabled = page >= pages;
    $('#pageNewer').disabled = page <= 1;
  }

  function renderHistory() {
    renderBars();
    renderHeat();
    renderTable();
  }
  $('#filterInput').addEventListener('input', function () {
    filterQ = this.value.trim().toLowerCase();
    page = 1;
    renderTable();
  });
  $('#pageOlder').addEventListener('click', function () { page++; renderTable(); });
  $('#pageNewer').addEventListener('click', function () { page = Math.max(1, page - 1); renderTable(); });

  function buildCSV(rows) {
    var head = 'Date,Ritual,Category,Minutes';
    var body = rows.map(function (e) {
      return [e.date, e.rit, e.cat, e.min === null ? '' : e.min].map(function (v) {
        return '"' + String(v).replace(/"/g, '""') + '"';
      }).join(',');
    }).join('\n');
    return head + '\n' + body + '\n';
  }
  function downloadCSV() {
    var csv = buildCSV(visibleEntries());
    var blob = new Blob([csv], { type: 'text/csv' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'cadence-log.csv';
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 400);
  }
  $('#exportTable').addEventListener('click', downloadCSV);
  $('#exportSettings').addEventListener('click', downloadCSV);

  /* ---------------- achievements ---------------- */
  function renderAchievements() {
    $('#statTiles').innerHTML = [
      { v: 12, l: 'Current streak' }, { v: 21, l: 'Best streak' }, { v: 240, l: 'Total logged' }
    ].map(function (t) {
      return '<div class="tile" data-improvised="stat tile: display register for big statics (L-04)">' +
        '<div class="tval">' + t.v + '</div><div class="tlab">' + t.l + '</div></div>';
    }).join('');
    $('#badgeGrid').innerHTML = BADGES.map(function (b) {
      return '<div class="badge ' + (b.earned ? '' : 'locked') + '" data-improvised="badge tile composition; no canonical trophy">' +
        glyphHTML(b.glyph) +
        '<div class="bname">' + esc(b.name) + '</div>' +
        '<div class="btag"><span class="tag' + (b.earned ? '' : ' mute') + '">' + (b.earned ? 'Earned' : 'Locked') + '</span></div></div>';
    }).join('');
    $('#badgesEmpty').innerHTML =
      '<div class="empty" data-improvised="empty state: ruled statement block, one action (deck L-17)">' +
      '<div class="eglyph" data-adapted="illustration → glyph mark (no imagery: deck L-17/L-21)">' + glyphHTML([5, 8, 12]) + '</div>' +
      '<h3>No badges yet.</h3>' +
      '<p class="pdek">One kept week earns the first.</p>' +
      '<button class="btn b-out" id="emptyGoToday">Go to Today</button></div>';
    $('#emptyGoToday').addEventListener('click', function () { showView('today'); });
  }
  $('#emptyToggle').addEventListener('change', function () {
    $('#badgeGrid').hidden = this.checked;
    $('#badgesEmpty').hidden = !this.checked;
  });

  /* ---------------- settings ---------------- */
  function renderSettings() {
    var st = S.settings;
    $('#setName').value = st.name;
    $('#setCat').value = st.cat;
    $('#weekMon').checked = st.weekStart === 'mon';
    $('#weekSun').checked = st.weekStart === 'sun';
    $('#goalRange').value = st.goal;
    $('#goalOut').textContent = st.goal;
    $('#remAm').checked = !!st.remAm;
    $('#remPm').checked = !!st.remPm;
    $('#darkToggle').checked = document.documentElement.getAttribute('data-theme') === 'dark';
  }
  $('#goalRange').addEventListener('input', function () { $('#goalOut').textContent = this.value; });
  $('#darkToggle').addEventListener('change', function () {
    document.documentElement.setAttribute('data-theme', this.checked ? 'dark' : '');
    S.settings.dark = this.checked;
    save();
  });
  $('#saveSettings').addEventListener('click', function () {
    var name = $('#setName').value.trim();
    var inv = !name;
    $('#fName').classList.toggle('invalid', inv);
    if (inv) return;
    $('#saveSettings').disabled = true;
    loading($('#settingsPanels'), 'Saving').then(function (el) {
      el.remove();
      var st = S.settings;
      st.name = name;
      st.cat = $('#setCat').value;
      st.weekStart = $('#weekSun').checked ? 'sun' : 'mon';
      st.goal = parseInt($('#goalRange').value, 10);
      st.remAm = $('#remAm').checked;
      st.remPm = $('#remPm').checked;
      save();
      greet();
      $('#saveSettings').disabled = false;
      notice('settings', 'Saved.');
    });
  });
  function greet() {
    $('#greeting').textContent = 'Good evening, ' + S.settings.name + '.';
    $('.avatar').textContent = (S.settings.name.charAt(0) || 'S').toUpperCase();
  }

  $('#deleteAll').addEventListener('click', function () {
    var ch = $('#settingsPanels');
    ch.innerHTML =
      '<div class="panel confirm" data-improvised="fallback/ruled-panel: inline confirmation (no scrim, no motion)">' +
      '<p class="pdek">Delete all data? Every ritual, entry and setting is removed.</p>' +
      '<div class="pact"><button class="btn b-red" id="confirmAll">Delete all</button>' +
      '<button class="btn b-out" id="cancelAll">Keep</button></div></div>';
    $('#confirmAll').addEventListener('click', function () {
      try { localStorage.removeItem(KEY); } catch (e) {}
      S = defaults();
      S.rituals = [];
      F_ENTRIES.length = 0;
      ch.innerHTML = '';
      renderAll();
      notice('settings', 'All data deleted.');
    });
    $('#cancelAll').addEventListener('click', function () { ch.innerHTML = ''; });
    $('#cancelAll').focus();
  });

  /* ---------------- wizard ---------------- */
  var wz = { step: 0 };
  var WZ = [
    { t: 'Small rituals, kept daily.', d: 'Cadence keeps a plain record: what you did, and for how long. That is the whole trick.' },
    { t: 'Pick your rituals.', d: 'Five to start. One check a day keeps each alive.' },
    { t: 'Set your goal.', d: 'A daily floor, not a ceiling.' }
  ];
  function renderWizard() {
    $('#wizStep').textContent = 'Step ' + (wz.step + 1) + ' of 3';
    $('#wizTitle').textContent = WZ[wz.step].t;
    $('#wizDek').textContent = WZ[wz.step].d;
    $$('#wizDots i').forEach(function (d, i) { d.classList.toggle('on', i === wz.step); });
    $('#wizBack').disabled = wz.step === 0;
    $('#wizNext').textContent = wz.step === 2 ? 'Begin' : 'Next';
    var body = $('#wizBody');
    if (wz.step === 1) {
      var src = S.rituals.length ? S.rituals : F_RITUALS;
      body.innerHTML = src.map(function (r) {
        return '<div class="cbrow"><label><input type="checkbox" class="cb" checked> ' + esc(r.name) + '</label></div>';
      }).join('');
    } else if (wz.step === 2) {
      body.innerHTML = '<div class="rng-wrap"><input type="range" class="rng" id="wizGoal" min="5" max="120" step="5" value="' + (S.settings.goal || 30) + '"><span class="rng-readout"><span id="wizGoalOut">' + (S.settings.goal || 30) + '</span> min</span></div>';
      $('#wizGoal').addEventListener('input', function () { $('#wizGoalOut').textContent = this.value; });
    } else { body.innerHTML = ''; }
  }
  function openWizard() { wz.step = 0; renderWizard(); showView('wizard'); }
  function closeWizard() { showView('today'); }
  $('#replayIntro').addEventListener('click', openWizard);
  $('#wizNext').addEventListener('click', function () {
    if (wz.step < 2) { wz.step++; renderWizard(); }
    else { closeWizard(); notice('today', 'You\u2019re set.'); }
  });
  $('#wizBack').addEventListener('click', function () { if (wz.step > 0) { wz.step--; renderWizard(); } });
  $('#wizSkip').addEventListener('click', closeWizard);

  /* ---------------- provenance marks ---------------- */
  $('#marksBtn').addEventListener('click', function () {
    var on = document.body.classList.toggle('show-marks');
    this.setAttribute('aria-pressed', String(on));
  });

  /* ---------------- boot ---------------- */
  $('#openLog').addEventListener('click', openLogForm);

  function renderAll() {
    renderToday();
    renderHistory();
    renderAchievements();
    renderSettings();
  }

  if (S.settings.dark) document.documentElement.setAttribute('data-theme', 'dark');
  greet();
  renderAll();
  showView('today');

  window.__cadence = {
    get state() { return S; },
    save: save,
    render: renderAll,
    showView: showView,
    reorder: reorder,
    csv: function () { return buildCSV(visibleEntries()); },
    setView: showView
  };
})();
