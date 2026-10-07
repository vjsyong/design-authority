# Procura — procurement approvals console (starter)

A small internal tool for an operations team: employees raise purchase
requests, reviewers approve or reject them, and a background "AI triage scan"
pre-classifies incoming requests.

**The backend is frozen.** Implement the UI by editing `templates/` and
`static/` only. Do not change `app.py`, routes, data shapes, or query
parameters; every route below must keep working.

## Run

```bash
./run.sh                    # http://127.0.0.1:8105
./run.sh --port 8106        # custom port
```

## Routes

| Route | What it is |
|---|---|
| `/` | Dashboard: pending count/amount, approved-30d total, rejected count, background jobs strip, recent activity |
| `/requests` | Requests list: filters (`status`, `category`, `q`), pagination (`page`, 10/page), bulk action form (`POST /requests/bulk` with repeated `ids` + `action=approve\|reject`) |
| `/requests/<id>` | Request detail: fields, approval history (steps), approve/reject forms, assign-reviewer form |
| `/jobs` | Background jobs: run a scan (`POST /jobs/triage/start`), running job with progress, history |
| `/api/jobs` | Live JSON for jobs (poll it for progress) |
| `/settings` | Notification + auto-approve settings (`POST /settings`) |
| `/healthz` | Liveness JSON |

Deterministic state forcing (used by tests; keep working):
`/?empty=1`, `/?error=1`, `/?job=running|done|failed`.

Data lives in `data/procura.db` (seeded automatically on first run).
