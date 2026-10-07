import re
import time
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8300"


def get(path):
    with urllib.request.urlopen(BASE + path) as r:
        return r.read().decode(), r.geturl()


def post(path, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(BASE + path, data=body, method="POST")
    with urllib.request.urlopen(req) as r:
        return r.read().decode(), r.geturl()


def check(label, cond):
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        raise SystemExit(1)


html, _ = get("/items")
check("register data-view", 'data-view="register"' in html)
check("register data-item id", 'data-item="1"' in html)
check("status available", 'data-status="available"' in html)
check("status on_loan", 'data-status="on_loan"' in html)
check("status overdue", 'data-status="overdue"' in html)
check("register class", 'class="register"' in html)
check("indicator text", re.search(r'class="indicator"[^>]*>[A-Z]', html) is not None)

html, _ = get("/items/new")
check("form data-view", 'data-view="form"' in html)
check("form-flow", "form-flow" in html)
check("chooser", 'class="chooser"' in html)

html, _ = get("/items/1")
check("detail data-view", 'data-view="detail"' in html)
check("retire action", 'data-action="retire"' in html)
check("retire dialog", 'class="dialog"' in html)
check("retire consequence copy", "permanently" in html.lower())
check("borrower datalist", "<datalist" in html and "member-list" in html)

html, _ = get("/activity")
check("activity data-view", 'data-view="activity"' in html)
check("job-view", "job-view" in html)

# create
_, url = post("/items", {"name": "Smoke wrench", "category": "Hand tools", "note": "test"})
new_id = int(re.search(r"/items/(\d+)", url).group(1))
html, _ = get("/items/%d" % new_id)
check("created item shown", "Smoke wrench" in html)
check("created available", 'data-status="available"' in html)

# edit
html, _ = post("/items/%d/update" % new_id, {"name": "Smoke wrench v2", "category": "Measuring", "note": "edited"})
check("edited name", "Smoke wrench v2" in html)
check("edited category", "Measuring" in html)

# checkout
html, _ = post("/items/%d/checkout" % new_id, {"borrower": "S. Ho", "days": "7"})
check("checkout on_loan", 'data-status="on_loan"' in html and "S. Ho" in html)
check("checkout hides form", "Check out" not in html)

# return
html, _ = post("/items/%d/return" % new_id, {})
check("returned available", 'data-status="available"' in html)

# import flow
_, _ = post("/activity/import", {})
time.sleep(2.5)
html, _ = get("/activity")
check("progressbar present while running", 'role="progressbar"' in html)
m = re.search(r'aria-valuemax="(\d+)"[^>]*aria-valuenow="(\d+)"', html)
check("aria values parse", m is not None)
if m:
    check("aria max 9", m.group(1) == "9")
    check("aria now > 0", int(m.group(2)) > 0)

import json
with urllib.request.urlopen(BASE + "/activity/status") as r:
    data = json.loads(r.read().decode())
check("status json running/complete", data["job"]["state"] in ("running", "complete"))
check("gauge fill width", "gauge__fill" in html)

# retire
_, url = post("/items/%d/retire" % new_id, {})
html, _ = get("/items")
check("retired removed from register", ('data-item="%d"' % new_id) not in html)
check("retire logged", "Retired Smoke wrench v2 permanently." in get("/activity")[0])

print("ALL FLOWS PASS")
