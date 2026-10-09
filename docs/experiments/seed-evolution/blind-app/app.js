/* driftexp — guided blind review (x05). Completely guided flow: one narrow
   1-5 question per screen, autosave, resume by name. Vanilla JS, no deps. */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var viewEls = { welcome: "view-welcome", run: "view-run", done: "view-done" };
  var SCALE = { 1: "very unlikely", 2: "unlikely", 3: "unsure", 4: "likely", 5: "very likely" };
  var DEFAULT_Q = "How likely are these two interfaces to belong to the same design system?";
  var KIND_LABEL = { pair: "Whole screens",
                     primary: "Close-up: primary action",
                     card: "Close-up: bookmark card" };
  var S = { meta: null, set: null, name: "", i: 0, rating: 0,
            answered: {}, local: {}, last: null };

  function api(path, opts) {
    opts = opts || {};
    var init = { method: opts.method || "GET", headers: {} };
    if (opts.body) {
      init.headers["Content-Type"] = "application/json";
      init.body = JSON.stringify(opts.body);
    }
    return fetch(path, init).then(function (r) {
      return r.json().then(function (j) {
        if (!r.ok) { throw new Error(j.error || ("HTTP " + r.status)); }
        return j;
      });
    });
  }

  function show(view) {
    Object.keys(viewEls).forEach(function (k) {
      $(viewEls[k]).classList.toggle("hidden", k !== view);
    });
  }

  function fail(el, msg) {
    var box = $(el);
    box.textContent = msg;
    box.classList.remove("hidden");
    setTimeout(function () { box.classList.add("hidden"); }, 6000);
  }

  function storageKey(suffix) { return "driftexp." + suffix + "." + (S.name || "").toLowerCase(); }

  function loadLocal() {
    try { S.local = JSON.parse(localStorage.getItem(storageKey("answers")) || "{}") || {}; }
    catch (e) { S.local = {}; }
  }
  function saveLocal() {
    try { localStorage.setItem(storageKey("answers"), JSON.stringify(S.local)); } catch (e) {}
  }

  function countAnswered() {
    var n = 0;
    S.set.comparisons.forEach(function (c) { if (S.answered[c.code]) { n++; } });
    return n;
  }

  function setProgress() {
    var total = S.set.comparisons.length;
    var done = countAnswered();
    var pct = total ? Math.round((done / total) * 100) : 0;
    var bar = $("progressBar");
    bar.setAttribute("aria-valuenow", String(pct));
    $("progressFill").style.width = pct + "%";
    $("progressBadge").textContent = done + " / " + total + " answered";
  }

  function setRating(v) {
    S.rating = v;
    var btns = $("rating").querySelectorAll("button");
    for (var i = 0; i < btns.length; i++) {
      var on = parseInt(btns[i].getAttribute("data-v"), 10) === v;
      btns[i].classList.toggle("primary", on);
      btns[i].setAttribute("aria-pressed", on ? "true" : "false");
    }
    $("ratingHint").textContent = v ? v + " — " + SCALE[v] : "Pick a number";
  }

  function render() {
    var c = S.set.comparisons[S.i];
    var total = S.set.comparisons.length;
    $("q-counter").textContent = "Comparison " + (S.i + 1) + " of " + total;
    $("q-text").textContent = c.prompt || DEFAULT_Q;
    $("q-kind").textContent = KIND_LABEL[c.kind] || "";
    $("shot-a").src = "img/" + c.left;
    $("shot-b").src = "img/" + c.right;
    var mine = S.local[c.code] || {};
    setRating(mine.rating || 0);
    $("noteInput").value = mine.note || "";
    setProgress();
    for (var k = 1; k <= 2; k++) {  /* prefetch the next pair */
      var nx = S.set.comparisons[S.i + k];
      if (nx) { [nx.left, nx.right].forEach(function (f) { var im = new Image(); im.src = "img/" + f; }); }
    }
  }

  function current() { return S.set.comparisons[S.i]; }

  function next() {
    var c = current();
    if (!S.rating) { fail("runErr", "Pick a rating from 1 to 5 first."); return; }
    api("api/answer", { method: "POST", body: { name: S.name, code: c.code,
        rating: S.rating, note: $("noteInput").value.trim() } })
      .then(function (res) {
        S.answered[c.code] = true;
        S.local[c.code] = { rating: S.rating, note: $("noteInput").value.trim() };
        saveLocal();
        if (res.index >= S.set.comparisons.length) { finish(); return; }
        S.i = res.index;
        render();
      })
      .catch(function (e) { fail("runErr", "Could not save: " + e.message); });
  }

  function back() {
    if (S.i > 0) { S.i--; render(); }
  }

  function finish() {
    show("done");
    $("progressBadge").textContent = "complete";
  }

  function start() {
    var name = $("nameInput").value.trim();
    if (!name) { fail("welcomeErr", "Please enter your name."); return; }
    S.name = name;
    try { localStorage.setItem("driftexp.name", name); } catch (e) {}
    api("api/hello", { method: "POST", body: { name: name } })
      .then(function (st) {
        return api("api/set").then(function (set) {
          S.set = set;
          S.answered = {};
          (st.answered || []).forEach(function (code) { S.answered[code] = true; });
          loadLocal();
          if (!set.comparisons.length) { fail("welcomeErr", "The review set is empty."); return; }
          if (st.index >= set.comparisons.length) { finish(); return; }
          S.i = st.index;
          show("run");
          render();
        });
      })
      .catch(function (e) { fail("welcomeErr", "Could not start: " + e.message); });
  }

  function sendComment() {
    api("api/comment", { method: "POST",
        body: { name: S.name, text: $("commentInput").value } })
      .then(function () { $("commentSent").classList.remove("hidden"); })
      .catch(function (e) { fail("welcomeErr", "Could not save comment: " + e.message); });
  }

  /* ------------------------------------------------------------- wiring */
  function boot() {
    api("api/meta").then(function (meta) {
      S.meta = meta;
      if (meta.title) { document.title = meta.title; $("hdr-title").textContent = meta.title; }
      if (meta.blurb) { $("hdr-desc").textContent = meta.blurb; }
      if (meta.placeholder) { $("placeholderNote").classList.remove("hidden"); }
      if (meta.count) {
        $("welcome-meta").textContent = meta.count + " comparisons · roughly " +
          Math.max(5, Math.round(meta.count * 0.5)) + "–" +
          Math.round(meta.count * 1.2) + " minutes · no right answers";
      }
      try {
        var saved = localStorage.getItem("driftexp.name");
        if (saved) { $("nameInput").value = saved; }
      } catch (e) {}
      if (!meta.ready) {
        fail("welcomeErr", "The review set has not been generated yet.");
        $("btnStart").disabled = true;
      }
    }).catch(function (e) { fail("welcomeErr", "Could not load: " + e.message); });

    $("btnStart").addEventListener("click", start);
    $("btnNext").addEventListener("click", next);
    $("btnBack").addEventListener("click", back);
    $("btnComment").addEventListener("click", sendComment);

    $("rating").addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-v]");
      if (b) { setRating(parseInt(b.getAttribute("data-v"), 10)); }
    });
    $("nameInput").addEventListener("keydown", function (ev) {
      if (ev.key === "Enter") { start(); }
    });

    document.addEventListener("keydown", function (ev) {
      if ($("view-run").classList.contains("hidden")) { return; }
      if (ev.target === $("noteInput")) {
        if (ev.key === "Enter") { next(); }
        return;
      }
      if (ev.key >= "1" && ev.key <= "5") { setRating(parseInt(ev.key, 10)); }
      else if (ev.key === "ArrowLeft" && S.rating > 1) { setRating(S.rating - 1); }
      else if (ev.key === "ArrowRight" && S.rating < 5) { setRating(S.rating + 1); }
      else if (ev.key === "Enter") { next(); }
    });
  }

  window.addEventListener("DOMContentLoaded", boot);
})();
