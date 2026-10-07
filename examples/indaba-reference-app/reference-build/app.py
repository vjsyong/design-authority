#!/usr/bin/env python3
"""Depot — small equipment-lending register (reference app for the Orbit spike).

Deliberately trivial backend: JSON files under ./data, Flask rendering, no auth.
The interface layer (templates + static/orbit.css) is what the experiment exercises.

Run:  python3 app.py [--port 8300]
"""
import argparse
import json
import os
import threading
import time
from datetime import date, datetime, timedelta

from flask import Flask, redirect, render_template, request, url_for

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
app = Flask(__name__)

STATUS_LABELS = {"available": "Available", "on_loan": "On loan", "overdue": "Overdue"}
CATEGORIES = ["Hand tools", "Power tools", "Measuring", "Safety"]


# ---------- storage ----------
def load(name, default):
    path = os.path.join(DATA, name)
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    return default


def save(name, obj):
    with open(os.path.join(DATA, name), "w") as fh:
        json.dump(obj, fh, indent=1)


def db_items():
    return load("items.json", {"items": [], "next_id": 1})


def db_members():
    return load("members.json", {"members": []})


def db_activity():
    return load("activity.json", {"entries": []})


def log_activity(message):
    db = db_activity()
    db["entries"].insert(0, {
        "at": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        "message": message,
    })
    save("activity.json", db)


def find_item(db, iid):
    for it in db["items"]:
        if it["id"] == iid:
            return it
    return None


def effective_status(it):
    """Overdue is derived from the due date while an item is out."""
    if it.get("status") == "on_loan" and it.get("due"):
        try:
            if date.fromisoformat(it["due"]) < date.today():
                return "overdue"
        except ValueError:
            pass
    return it.get("status", "available")


# ---------- import job (simulated, for the activity screen) ----------
JOB = {"state": "idle", "done": 0, "total": 9, "message": "", "started": None}
JOB_LOCK = threading.Lock()

IMPORT_STEPS = [
    "Reading members.csv", "Validating rows", "Matching equipment names",
    "Updating categories", "Reconciling loan dates", "Checking duplications",
    "Writing items", "Rebuilding index", "Done",
]


def run_import():
    with JOB_LOCK:
        JOB.update(state="running", done=0, total=len(IMPORT_STEPS), started=time.time())
    for i, step in enumerate(IMPORT_STEPS):
        time.sleep(1.2)
        with JOB_LOCK:
            JOB["done"] = i + 1
            JOB["message"] = step
            if step == "Done":
                JOB["state"] = "complete"
    log_activity("Import finished: 9 of 9 steps.")


# ---------- routes ----------
@app.route("/healthz")
def healthz():
    return "ok"


@app.route("/")
def index():
    return redirect(url_for("items_view"))


@app.route("/items")
def items_view():
    db = db_items()
    rows = [dict(it, status=effective_status(it)) for it in db["items"]
            if it.get("status") != "retired"]
    return render_template("items.html", items=rows, status_labels=STATUS_LABELS)


@app.route("/items/new")
def item_new():
    return render_template("item_form.html", item=None, categories=CATEGORIES)


@app.route("/items", methods=["POST"])
def item_create():
    db = db_items()
    it = {
        "id": db["next_id"],
        "name": (request.form.get("name") or "").strip() or "Untitled item",
        "category": request.form.get("category") or CATEGORIES[0],
        "note": (request.form.get("note") or "").strip(),
        "status": "available",
        "borrower": None,
        "due": None,
    }
    db["items"].append(it)
    db["next_id"] += 1
    save("items.json", db)
    log_activity("Added item: %s." % it["name"])
    return redirect(url_for("item_detail", iid=it["id"]))


@app.route("/items/<int:iid>")
def item_detail(iid):
    db = db_items()
    it = find_item(db, iid)
    if not it:
        return "Not found", 404
    it = dict(it, status=effective_status(it))
    return render_template("item_detail.html", item=it,
                           members=db_members()["members"], status_labels=STATUS_LABELS)


@app.route("/items/<int:iid>/update", methods=["POST"])
def item_update(iid):
    db = db_items()
    it = find_item(db, iid)
    if not it:
        return "Not found", 404
    it["name"] = (request.form.get("name") or it["name"]).strip()
    it["category"] = request.form.get("category") or it["category"]
    it["note"] = (request.form.get("note") or "").strip()
    save("items.json", db)
    log_activity("Updated item: %s." % it["name"])
    return redirect(url_for("item_detail", iid=iid))


@app.route("/items/<int:iid>/checkout", methods=["POST"])
def item_checkout(iid):
    db = db_items()
    it = find_item(db, iid)
    if not it:
        return "Not found", 404
    borrower = (request.form.get("borrower") or "").strip()
    days = request.form.get("days") or "14"
    try:
        due = (date.today() + timedelta(days=int(days))).isoformat()
    except ValueError:
        due = (date.today() + timedelta(days=14)).isoformat()
    it["status"] = "on_loan"
    it["borrower"] = borrower or "unassigned"
    it["due"] = due
    save("items.json", db)
    log_activity("Checked out %s to %s (due %s)." % (it["name"], it["borrower"], due))
    return redirect(url_for("item_detail", iid=iid))


@app.route("/items/<int:iid>/return", methods=["POST"])
def item_return(iid):
    db = db_items()
    it = find_item(db, iid)
    if not it:
        return "Not found", 404
    it["status"] = "available"
    it["borrower"] = None
    it["due"] = None
    save("items.json", db)
    log_activity("Returned %s." % it["name"])
    return redirect(url_for("item_detail", iid=iid))


@app.route("/items/<int:iid>/retire", methods=["POST"])
def item_retire(iid):
    db = db_items()
    it = find_item(db, iid)
    if not it:
        return "Not found", 404
    it["status"] = "retired"
    save("items.json", db)
    log_activity("Retired %s permanently." % it["name"])
    return redirect(url_for("items_view"))


@app.route("/activity")
def activity_view():
    with JOB_LOCK:
        job = dict(JOB)
    return render_template("activity.html", job=job, entries=db_activity()["entries"])


@app.route("/activity/status")
def activity_status():
    """Read-only JSON snapshot so the activity screen can follow progress in place."""
    with JOB_LOCK:
        job = dict(JOB)
    return {"job": job, "entries": db_activity()["entries"]}


@app.route("/activity/import", methods=["POST"])
def activity_import():
    with JOB_LOCK:
        if JOB["state"] != "running":
            threading.Thread(target=run_import, daemon=True).start()
    return redirect(url_for("activity_view"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8300)
    args = ap.parse_args()
    app.run(host="127.0.0.1", port=args.port, debug=False)
