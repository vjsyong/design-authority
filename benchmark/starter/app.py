#!/usr/bin/env python3
"""Procura — procurement approvals console (benchmark starter application).

The backend is FROZEN. Implement the UI by editing `templates/` and `static/`
only: do not change routes, data shapes, or query parameters.

Deterministic state forcing (used by tests and screenshots):
    /?empty=1                    empty lists (no requests, no activity)
    /?error=1                    persistent connector error state
    /?job=running|done|failed    force the current triage-job state

Run:  ./run.sh            (uses the benchmark python), or
      python app.py --port 8105
"""
import argparse
import os
import random
import sqlite3
from datetime import datetime, timedelta, timezone

from flask import Flask, g, jsonify, redirect, render_template, request, send_from_directory

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "data", "procura.db")

REVIEWERS = ["Dana Whitfield", "Marco Reyes", "Priya Natarajan", "Sam Okafor"]
REQUESTERS = [("Alba Chen", "Design"), ("Ravi Patel", "Engineering"),
              ("Mona Lindqvist", "Operations"), ("Tomas Rivera", "Finance"),
              ("Grace Ho", "Marketing")]
REQUESTS = [
    ("Laptop refresh for the design team (4 units)", "Hardware"),
    ("Standing desks for the ops pod (6 units)", "Hardware"),
    ("Studio monitors for the video review corner", "Hardware"),
    ("Figma organization seats — annual renewal", "Software"),
    ("Analytics platform annual renewal", "Software"),
    ("Security scanner license expansion", "Software"),
    ("Legal review retainer — Q4", "Services"),
    ("Recruiting agency fee — senior designer", "Services"),
    ("Localization vendor pilot (zh-Hant)", "Services"),
    ("Team offsite venue deposit", "Travel"),
    ("Client visit — Singapore flights", "Travel"),
    ("Conference passes and travel — platform summit", "Travel"),
    ("Product launch photography", "Marketing"),
    ("Developer conference sponsorship", "Marketing"),
    ("Brand refresh — typography licensing", "Marketing"),
    ("Meeting room AV upgrade", "Facilities"),
    ("Kitchen restock — quarterly contract", "Facilities"),
    ("Office security audit", "Facilities"),
    ("Data warehouse storage uplift", "Software"),
    ("Contractor onboarding — data engineer", "Services"),
    ("Customer research incentives (40 sessions)", "Marketing"),
    ("Support plan upgrade — priority tier", "Software"),
    ("Prototype fabrication materials", "Hardware"),
    ("Quarterly team dinner", "Facilities"),
]
CATEGORIES = ["Hardware", "Software", "Services", "Travel", "Marketing", "Facilities"]
JOB_DURATION_S = 600  # simulated duration of a running scan

app = Flask(__name__)


# --------------------------------------------------------------------------- #
# time + formatting helpers
# --------------------------------------------------------------------------- #
def now():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.isoformat(timespec="seconds")


def parse_iso(s):
    return datetime.fromisoformat(s)


@app.template_filter("ago")
def ago(ts):
    secs = (now() - parse_iso(ts)).total_seconds()
    if secs < 3600:
        return "%dm ago" % max(1, int(secs // 60))
    if secs < 86400:
        return "%dh ago" % int(secs // 3600)
    return "%dd ago" % int(secs // 86400)


@app.template_filter("money")
def money(v):
    return "$%s" % format(int(v or 0), ",")


@app.template_filter("dt")
def dt(ts):
    return parse_iso(ts).strftime("%Y-%m-%d %H:%M UTC")


# --------------------------------------------------------------------------- #
# database
# --------------------------------------------------------------------------- #
SCHEMA = """
create table if not exists requesters (id integer primary key, name text, dept text);
create table if not exists categories (id integer primary key, name text);
create table if not exists requests (
  id integer primary key, title text, requester_id integer, category_id integer,
  amount integer, status text, created_at text, updated_at text,
  reviewer text, note text);
create table if not exists steps (
  id integer primary key, request_id integer, actor text, action text, ts text, note text);
create table if not exists jobs (
  id integer primary key, kind text, state text, started_at text, finished_at text,
  total integer, note text);
create table if not exists settings (key text primary key, value text);
"""


def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def _close_db(exc):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.executescript(SCHEMA)
    if con.execute("select count(*) from requests").fetchone()[0] == 0:
        seed(con)
        con.commit()
    con.close()


def seed(con):
    rng = random.Random(7)
    t0 = now()
    for i, (name, dept) in enumerate(REQUESTERS, 1):
        con.execute("insert into requesters values (?,?,?)", (i, name, dept))
    for i, name in enumerate(CATEGORIES, 1):
        con.execute("insert into categories values (?,?)", (i, name))

    for i, (title, cat) in enumerate(REQUESTS, 1):
        requester_id = (i - 1) % len(REQUESTERS) + 1
        cat_id = CATEGORIES.index(cat) + 1
        status = "pending" if i <= 9 else ("approved" if i <= 18 else
                                           ("rejected" if i <= 22 else "approved"))
        days = rng.randint(0, 6) if status == "pending" else rng.randint(3, 21)
        created = t0 - timedelta(days=days, hours=rng.randint(0, 12))
        amount = rng.randrange(250, 45000)
        reviewer = REVIEWERS[i % len(REVIEWERS)]
        note = "Exceeds department budget guidance" if status == "rejected" else None
        updated = created + timedelta(hours=rng.randint(6, 40))
        con.execute(
            "insert into requests values (?,?,?,?,?,?,?,?,?,?)",
            (i, title, requester_id, cat_id, amount, status, iso(created), iso(updated),
             reviewer if status != "pending" else None, note))
        requester = REQUESTERS[requester_id - 1][0]
        con.execute("insert into steps values (?,?,?,?,?,?)",
                    (None, i, requester, "submitted", iso(created), None))
        if status in ("approved", "rejected"):
            con.execute("insert into steps values (?,?,?,?,?,?)",
                        (None, i, reviewer, "reviewed", iso(created + timedelta(hours=4)), None))
            con.execute("insert into steps values (?,?,?,?,?,?)",
                        (None, i, reviewer,
                         "approved" if status == "approved" else "rejected",
                         iso(updated), note))
        else:
            con.execute("insert into steps values (?,?,?,?,?,?)",
                        (None, i, reviewer, "assigned", iso(created + timedelta(hours=2)), None))

    con.execute("insert into steps values (?,?,?,?,?,?)",
                (None, 1, "system", "reminder sent", iso(t0 - timedelta(hours=3)), None))
    con.execute("insert into steps values (?,?,?,?,?,?)",
                (None, 2, "system", "reminder sent", iso(t0 - timedelta(hours=8)), None))

    con.execute("insert into jobs values (?,?,?,?,?,?,?)",
                (1, "AI triage scan", "done", iso(t0 - timedelta(hours=7)),
                 iso(t0 - timedelta(hours=6, minutes=42)), 420, None))
    con.execute("insert into jobs values (?,?,?,?,?,?,?)",
                (2, "AI triage scan", "failed", iso(t0 - timedelta(days=2)),
                 iso(t0 - timedelta(days=2, hours=-1)), 300, "IMAP connection lost"))
    con.execute("insert into jobs values (?,?,?,?,?,?,?)",
                (3, "AI triage scan", "done", iso(t0 - timedelta(days=4)),
                 iso(t0 - timedelta(days=4, hours=-1)), 385, None))

    for k, v in (("notify_email", "on"), ("digest", "daily"),
                 ("auto_approve_threshold", "500"), ("connector_name", "Finance ERP")):
        con.execute("insert into settings values (?,?)", (k, v))


def setting(key, default=None):
    row = db().execute("select value from settings where key=?", (key,)).fetchone()
    return row["value"] if row else default


# --------------------------------------------------------------------------- #
# jobs (simulated async work)
# --------------------------------------------------------------------------- #
def job_view(row):
    total = row["total"] or 0
    state = row["state"]
    started = parse_iso(row["started_at"]) if row["started_at"] else None
    if state == "running" and started:
        elapsed = (now() - started).total_seconds()
        scanned = min(total, max(0, int(total * elapsed / JOB_DURATION_S)))
    elif state == "done":
        scanned = total
    else:
        scanned = int(total * 0.35)
    return {"id": row["id"], "kind": row["kind"], "state": state,
            "scanned": scanned, "total": total,
            "percent": round(100 * scanned / total) if total else 0,
            "note": row["note"], "started_at": row["started_at"],
            "finished_at": row["finished_at"]}


def forced_job(which):
    t0 = now()
    specs = {
        "running": ("running", 189, 420, t0 - timedelta(minutes=4), None),
        "done": ("done", 420, 420, t0 - timedelta(minutes=40), None),
        "failed": ("failed", 147, 420, t0 - timedelta(hours=3), "IMAP connection lost"),
    }
    state, scanned, total, started, note = specs[which]
    return {"id": 99, "kind": "AI triage scan", "state": state, "scanned": scanned,
            "total": total, "percent": round(100 * scanned / total),
            "note": note, "started_at": iso(started),
            "finished_at": iso(t0 - timedelta(minutes=35)) if state != "running" else None}


def effective_jobs():
    forced = request.args.get("job")
    if forced in ("running", "done", "failed"):
        job = forced_job(forced)
        rows = db().execute("select * from jobs order by started_at desc").fetchall()
        history = [job_view(r) for r in rows if r["state"] != "running"][:3]
        active = job if job["state"] == "running" else None
        return ([job] + history), active
    rows = db().execute("select * from jobs order by started_at desc").fetchall()
    views = [job_view(r) for r in rows]
    active = next((v for v in views if v["state"] == "running"), None)
    history = [v for v in views if v["state"] != "running"][:3]
    return (([active] if active else []) + history), active


# --------------------------------------------------------------------------- #
# pages
# --------------------------------------------------------------------------- #
@app.route("/")
def dashboard():
    con = db()
    empty = request.args.get("empty") == "1"
    error = request.args.get("error") == "1"
    stats = {"pending_count": 0, "pending_amount": 0, "approved_amount": 0,
             "rejected_count": 0}
    recent = []
    if not empty:
        stats["pending_count"] = con.execute(
            "select count(*) c from requests where status='pending'").fetchone()["c"]
        stats["pending_amount"] = con.execute(
            "select coalesce(sum(amount),0) s from requests where status='pending'").fetchone()["s"]
        stats["approved_amount"] = con.execute(
            "select coalesce(sum(amount),0) s from requests where status='approved' "
            "and updated_at > ?", (iso(now() - timedelta(days=30)),)).fetchone()["s"]
        stats["rejected_count"] = con.execute(
            "select count(*) c from requests where status='rejected'").fetchone()["c"]
        recent = con.execute(
            "select s.*, r.title from steps s join requests r on r.id=s.request_id "
            "order by s.ts desc limit 8").fetchall()
    jobs, active_job = ([], None) if empty else effective_jobs()
    return render_template("dashboard.html", stats=stats, recent=recent, jobs=jobs,
                           active_job=active_job, empty=empty, error=error,
                           connector_name=setting("connector_name", "Finance ERP"))


@app.route("/requests")
def requests_list():
    con = db()
    empty = request.args.get("empty") == "1"
    status = request.args.get("status", "")
    category = request.args.get("category", "")
    q = request.args.get("q", "").strip()
    page = max(1, request.args.get("page", 1, type=int))
    per = 10
    where, args = [], []
    if not empty:
        if status in ("pending", "approved", "rejected"):
            where.append("r.status=?"); args.append(status)
        if category in CATEGORIES:
            where.append("c.name=?"); args.append(category)
        if q:
            where.append("r.title like ?"); args.append("%" + q + "%")
    clause = ("where " + " and ".join(where)) if where else ""
    total = con.execute("select count(*) c from requests r join categories c on c.id=r.category_id "
                        + clause, args).fetchone()["c"] if not empty else 0
    rows = con.execute(
        "select r.*, c.name cat, q.name requester from requests r "
        "join categories c on c.id=r.category_id "
        "join requesters q on q.id=r.requester_id " + clause +
        " order by r.created_at desc limit ? offset ?",
        args + [per, (page - 1) * per]).fetchall() if not empty else []
    pages = max(1, (total + per - 1) // per)
    return render_template("requests.html", requests=rows, total=total, page=page,
                           pages=pages, status=status, category=category, q=q,
                           categories=CATEGORIES, empty=empty)


@app.route("/requests/<int:req_id>")
def request_detail(req_id):
    con = db()
    row = con.execute(
        "select r.*, c.name cat, q.name requester, q.dept from requests r "
        "join categories c on c.id=r.category_id "
        "join requesters q on q.id=r.requester_id where r.id=?",
        (req_id,)).fetchone()
    if row is None:
        return "request not found", 404
    steps = con.execute("select * from steps where request_id=? order by ts",
                        (req_id,)).fetchall()
    return render_template("request_detail.html", r=row, steps=steps,
                           reviewers=REVIEWERS)


@app.route("/requests/<int:req_id>/approve", methods=["POST"])
def approve(req_id):
    return _decide(req_id, "approved")


@app.route("/requests/<int:req_id>/reject", methods=["POST"])
def reject(req_id):
    return _decide(req_id, "rejected")


def _decide(req_id, decision):
    con = db()
    note = request.form.get("reason") or None
    row = con.execute("select * from requests where id=?", (req_id,)).fetchone()
    if row is None:
        return "request not found", 404
    if row["status"] == "pending":
        actor = request.form.get("actor") or "You"
        con.execute("update requests set status=?, updated_at=?, note=? where id=?",
                    (decision, iso(now()), note, req_id))
        con.execute("insert into steps values (?,?,?,?,?,?)",
                    (None, req_id, actor, decision, iso(now()), note))
        con.commit()
    back = request.form.get("back") or request.referrer or "/requests"
    return redirect(back + ("&" if "?" in back else "?") +
                    "flash=%s&name=%s" % (decision, req_id))


@app.route("/requests/bulk", methods=["POST"])
def bulk():
    con = db()
    action = request.form.get("action", "")
    ids = request.form.getlist("ids")
    changed = 0
    if action in ("approve", "reject") and ids:
        decision = "approved" if action == "approve" else "rejected"
        for rid in ids:
            if not str(rid).isdigit():
                continue
            row = con.execute("select * from requests where id=? and status='pending'",
                              (int(rid),)).fetchone()
            if row:
                con.execute("update requests set status=?, updated_at=? where id=?",
                            (decision, iso(now()), int(rid)))
                con.execute("insert into steps values (?,?,?,?,?,?)",
                            (None, int(rid), "You", decision, iso(now()), None))
                changed += 1
        con.commit()
    back = request.form.get("back") or "/requests"
    return redirect(back + ("&" if "?" in back else "?") +
                    "flash=bulk-%s&count=%d" % (action or "noop", changed))


@app.route("/requests/<int:req_id>/assign", methods=["POST"])
def assign(req_id):
    con = db()
    reviewer = request.form.get("reviewer")
    if reviewer in REVIEWERS:
        con.execute("update requests set reviewer=?, updated_at=? where id=?",
                    (reviewer, iso(now()), req_id))
        con.execute("insert into steps values (?,?,?,?,?,?)",
                    (None, req_id, "You", "assigned " + reviewer, iso(now()), None))
        con.commit()
    return redirect(request.form.get("back") or "/requests/%d" % req_id)


@app.route("/jobs")
def jobs_page():
    jobs, active = effective_jobs()
    return render_template("jobs.html", jobs=jobs, active_job=active)


@app.route("/jobs/triage/start", methods=["POST"])
def start_job():
    con = db()
    running = con.execute("select count(*) c from jobs where state='running'").fetchone()["c"]
    if not running:
        con.execute("insert into jobs values (?,?,?,?,?,?,?)",
                    (None, "AI triage scan", "running", iso(now()), None, 420, None))
        con.commit()
    return redirect("/jobs")


@app.route("/api/jobs")
def api_jobs():
    jobs, active = effective_jobs()
    return jsonify({"active": active, "recent": [j for j in jobs if j["state"] != "running"],
                    "jobs": jobs})


@app.route("/settings", methods=["GET", "POST"])
def settings():
    con = db()
    if request.method == "POST":
        for key in ("notify_email", "digest", "auto_approve_threshold"):
            if key in request.form:
                con.execute("insert into settings values (?,?) "
                            "on conflict(key) do update set value=excluded.value",
                            (key, request.form[key]))
            elif key == "notify_email":
                con.execute("insert into settings values (?,?) "
                            "on conflict(key) do update set value=excluded.value",
                            (key, "off"))
        con.commit()
        return redirect("/settings?flash=saved")
    return render_template("settings.html",
                           notify_email=setting("notify_email") == "on",
                           digest=setting("digest"), threshold=setting("auto_approve_threshold"))


@app.route("/healthz")
def healthz():
    return jsonify({"ok": True, "app": "procura"})


@app.route("/design/<path:filename>")
def design_assets(filename):
    """Serve the vendored design system package read-only (if present)."""
    return send_from_directory(os.path.join(HERE, "design"), filename)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8105)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    init_db()
    app.run(host=args.host, port=args.port, debug=False)


init_db()

if __name__ == "__main__":
    main()
