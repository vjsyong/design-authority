/* wink-notes — the save flow runs the adopted records: pattern/progress
   (step caption, no indeterminate motion) then pattern/inline-notice on
   completion. The toast at the end is a marked improvisation (case 05). */
(function () {
  "use strict";

  var KEY = "wink-notes";
  var notes = null;
  try { notes = JSON.parse(localStorage.getItem(KEY)); } catch (e) { notes = null; }
  if (!notes) {
    /* first visit: a couple of sample rituals so the list, card vessel,
       status words and the per-note actions have their surfaces */
    notes = [
      { text: "Water the ferns", done: false },
      { text: "Evening stretch", done: true }
    ];
  }
  notes = notes.map(function (n) {
    return typeof n === "string" ? { text: n, done: false } : n;
  });

  var list = document.getElementById("noteList");
  var empty = document.getElementById("emptyState");
  var form = document.getElementById("addForm");
  var input = document.getElementById("noteInput");
  var inputError = document.getElementById("inputError");
  var notice = document.getElementById("saveNotice");
  var progress = document.getElementById("saveProgress");
  var fill = document.getElementById("progressFill");
  var caption = document.getElementById("progressCaption");
  var toast = document.getElementById("toast");

  function persist() { localStorage.setItem(KEY, JSON.stringify(notes)); }

  function render() {
    list.innerHTML = "";
    notes.forEach(function (n, i) {
      var li = document.createElement("li");
      li.className = "card";
      var main = document.createElement("div");
      main.className = "note-main";
      var span = document.createElement("span");
      span.className = "note-text" + (n.done ? " done" : "");
      span.textContent = n.text;
      var status = document.createElement("span");
      status.className = "status " + (n.done ? "closed" : "open");
      status.textContent = n.done ? "Done" : "To do";
      var done = document.createElement("button");
      done.type = "button";
      done.className = "mini note-done";
      done.textContent = n.done ? "Reopen" : "Mark done";
      done.addEventListener("click", function () {
        n.done = !n.done;
        persist();
        render();
      });
      var remove = document.createElement("button");
      remove.type = "button";
      remove.className = "mini note-remove";
      remove.textContent = "Remove";
      remove.addEventListener("click", function () {
        notes.splice(i, 1);
        persist();
        render();
      });
      main.appendChild(span);
      main.appendChild(status);
      main.appendChild(done);
      main.appendChild(remove);
      li.appendChild(main);
      list.appendChild(li);
    });
    empty.hidden = notes.length > 0;
  }

  var STEPS = ["Saving, step 1 of 3", "Saving, step 2 of 3", "Saving, step 3 of 3"];

  function save() {
    var value = input.value.trim();
    if (!value) {
      input.classList.add("invalid");
      input.setAttribute("aria-invalid", "true");
      inputError.hidden = false;
      input.focus();
      return;
    }
    notice.hidden = true;
    progress.hidden = false;
    progress.classList.remove("complete");
    var step = 0;

    function tick() {
      caption.textContent = STEPS[Math.min(step, STEPS.length - 1)];
      fill.style.width = Math.round(((step + 1) / STEPS.length) * 100) + "%";
      step += 1;
      if (step < STEPS.length) {
        window.setTimeout(tick, 250);
      } else {
        progress.classList.add("complete");
        notes.push({ text: value, done: false });
        persist();
        input.value = "";
        render();
        window.setTimeout(function () {
          progress.hidden = true;
          fill.style.width = "0";
          progress.classList.remove("complete");
          notice.hidden = false;
          showToast("Saved. Your ritual list is up to date.");
        }, 250);
      }
    }
    tick();
  }

  /* noncanonical: floating toast — improvisation, no wink record (case 05) */
  var toastTimer = null;
  function showToast(message) {
    toast.textContent = message;
    toast.hidden = false;
    if (toastTimer) { window.clearTimeout(toastTimer); }
    toastTimer = window.setTimeout(function () { toast.hidden = true; }, 4000);
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    save();
  });
  input.addEventListener("input", function () {
    input.classList.remove("invalid");
    input.removeAttribute("aria-invalid");
    inputError.hidden = true;
  });
  document.getElementById("clearBtn").addEventListener("click", function () {
    input.value = "";
    input.classList.remove("invalid");
    input.removeAttribute("aria-invalid");
    inputError.hidden = true;
    input.focus();
  });
  document.getElementById("emptyAdd").addEventListener("click", function () {
    input.focus();
  });

  render();
})();
