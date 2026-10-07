/* app.js — progressive enhancement only.
   With JavaScript off the app is fully usable: forms submit normally, the
   activity screen refreshes via <meta http-equiv="refresh"> while a job runs,
   and the retire action falls back to an inline warning + submit button.
   Nothing here is required for a flow to complete. */
(function () {
  "use strict";

  /* ---- Retire confirmation (recipe/retire-confirm + component/dialog) ---- */
  var retireTrigger = document.querySelector('[data-action="retire"]');
  var retireDialog = document.getElementById("retire-dialog");
  if (retireTrigger && retireDialog && typeof retireDialog.showModal === "function") {
    retireTrigger.addEventListener("click", function () {
      retireDialog.showModal();
    });
    var cancelButton = retireDialog.querySelector("[data-cancel]");
    if (cancelButton) {
      cancelButton.addEventListener("click", function () {
        retireDialog.close();
      });
    }
  }

  /* ---- Live import progress (recipe/import-progress + component/meter) ---- */
  var root = document.querySelector("[data-activity-job]");
  if (!root) { return; }

  /* JS takes over from the no-JS meta refresh. */
  var metaRefresh = document.querySelector('meta[http-equiv="refresh"]');
  if (metaRefresh && metaRefresh.parentNode) {
    metaRefresh.parentNode.removeChild(metaRefresh);
  }

  var stateEl = root.querySelector("[data-job-state]");
  if (!stateEl) { return; }

  var meter = root.querySelector('[role="progressbar"]');
  var fill = meter ? meter.querySelector("i") : null;
  var readout = root.querySelector("[data-job-readout]");
  var message = root.querySelector("[data-job-message]");
  var button = root.querySelector("[data-job-button]");
  var logBody = document.querySelector("[data-job-log]");
  var inFlight = false;

  function tone(state) {
    if (state === "running") { return "overdue"; }
    if (state === "complete") { return "loan"; }
    if (state === "failed") { return "overdue"; }
    return "available";
  }

  function label(state) {
    if (state === "running") { return "Running"; }
    if (state === "complete") { return "Complete"; }
    if (state === "failed") { return "Failed"; }
    return "Idle";
  }

  function renderLog(entries) {
    if (!logBody) { return; }
    var signature = entries.length
      ? entries[0].at + "\u0000" + entries[0].message + "\u0000" + entries.length
      : "empty";
    if (logBody.getAttribute("data-signature") === signature) { return; }
    logBody.setAttribute("data-signature", signature);
    logBody.textContent = "";
    if (!entries.length) {
      var empty = document.createElement("tr");
      var cell = document.createElement("td");
      cell.className = "row-empty";
      cell.colSpan = 2;
      cell.textContent = "Nothing logged yet.";
      empty.appendChild(cell);
      logBody.appendChild(empty);
      return;
    }
    entries.forEach(function (entry) {
      var tr = document.createElement("tr");
      var when = document.createElement("td");
      var what = document.createElement("td");
      when.className = "meta";
      when.textContent = entry.at;
      what.textContent = entry.message;
      tr.appendChild(when);
      tr.appendChild(what);
      logBody.appendChild(tr);
    });
  }

  function render(data) {
    var job = data.job;
    stateEl.textContent = label(job.state);
    stateEl.className = "status " + tone(job.state);
    stateEl.setAttribute("data-job-state", job.state);

    if (meter) {
      meter.setAttribute("aria-valuenow", job.done);
      meter.setAttribute("aria-valuemax", job.total);
      meter.setAttribute("aria-valuetext", job.done + " of " + job.total + " steps");
      meter.setAttribute("data-job-done", job.done);
      meter.setAttribute("data-job-total", job.total);
      meter.classList.toggle("complete", job.state === "complete");
      meter.classList.toggle("running", job.state === "running");
    }
    if (fill) {
      fill.style.setProperty("--value", Math.floor((job.done / job.total) * 100) + "%");
    }
    if (readout) {
      readout.textContent = job.done + " of " + job.total + " steps";
    }
    if (message) {
      message.textContent = job.message || "Not started.";
    }
    if (button) {
      button.disabled = job.state === "running";
      button.textContent = job.state === "running"
        ? "Importing…"
        : (job.state === "complete" ? "Run import again" : "Start import");
    }
    renderLog(data.entries || []);
    return job.state;
  }

  function poll() {
    if (inFlight) { return; }
    inFlight = true;
    fetch("/activity/status", { headers: { Accept: "application/json" } })
      .then(function (response) { return response.json(); })
      .then(function (data) {
        inFlight = false;
        if (render(data) === "running") {
          window.setTimeout(poll, 1200);
        }
      })
      .catch(function () {
        inFlight = false;
        window.setTimeout(poll, 2000);
      });
  }

  if (stateEl.getAttribute("data-job-state") === "running") {
    window.setTimeout(poll, 800);
  }
})();
