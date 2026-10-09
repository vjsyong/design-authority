#!/usr/bin/env python3
"""driftexp — guided blind-review app for the x05 design-drift experiment.

Serves a capability-URL surface (unguessable token + reviewer name) that walks
a human reviewer through narrow 1–5 comparisons and stores every event under
blind-app/data/ (never committed). Stdlib only; noindex on every response.

    python3 app.py --port 8455

Config: data/config.json {"token": "..."} auto-created on first run (printed);
override with X05_BLIND_TOKEN. Review set: data/blindset/set.json (+ img/).
"""
import argparse
import hmac
import json
import os
import re
import secrets
import sys
import threading
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
BLINDSET = os.path.join(DATA, "blindset")
RATINGS = os.path.join(DATA, "ratings.jsonl")
CONFIG = os.path.join(DATA, "config.json")
LOCK = threading.Lock()
IMG_RE = re.compile(r"^[A-Za-z0-9._-]+$")
CTYPES = {".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
          ".woff2": "font/woff2", ".txt": "text/plain; charset=utf-8",
          ".svg": "image/svg+xml", ".png": "image/png", ".html": "text/html; charset=utf-8"}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_config():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(CONFIG):
        cfg = {"token": secrets.token_urlsafe(18), "created": now()}
        with open(CONFIG, "w") as fh:
            json.dump(cfg, fh, indent=1)
    with open(CONFIG) as fh:
        cfg = json.load(fh)
    env = os.environ.get("X05_BLIND_TOKEN")
    if env:
        cfg["token"] = env
    return cfg


def load_set():
    p = os.path.join(BLINDSET, "set.json")
    if not os.path.exists(p):
        return None
    with open(p) as fh:
        return json.load(fh)


def clean_name(raw):
    name = " ".join(str(raw or "").split())
    name = "".join(ch for ch in name if ch.isprintable())
    return name[:80]


def append_event(obj):
    with LOCK:
        os.makedirs(DATA, exist_ok=True)
        with open(RATINGS, "a") as fh:
            fh.write(json.dumps(obj) + "\n")


def answered_state(name, comparisons):
    """Presence of answers per code (last answer wins; append-only log)."""
    answers = {}
    if os.path.exists(RATINGS):
        with open(RATINGS, errors="replace") as fh:
            for line in fh:
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                if ev.get("event") == "answer" and ev.get("name") == name:
                    answers[ev.get("code")] = ev
    done = [c["code"] for c in comparisons if c["code"] in answers]
    codes = set(c["code"] for c in comparisons)
    index = next((i for i, c in enumerate(comparisons) if c["code"] not in answers),
                 len(comparisons))
    return {"answered": [c for c in done if c in codes], "index": index}


class Server(ThreadingHTTPServer):
    daemon_threads = True
    base_path = "/"


class Handler(BaseHTTPRequestHandler):
    server_version = "driftexp"

    # ------------------------------------------------------------- helpers
    def _base(self):
        return self.server.base_path

    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("X-Robots-Tag", "noindex, nofollow, noarchive")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            try:
                self.wfile.write(body)
            except BrokenPipeError:
                pass

    def do_HEAD(self):
        return self.do_GET()

    def _json(self, obj, code=200):
        self._send(code, "application/json", json.dumps(obj).encode())

    def _file(self, path, ctype=None, code=200):
        if not os.path.isfile(path):
            return self._json({"error": "not found"}, 404)
        if ctype is None:
            ctype = CTYPES.get(os.path.splitext(path)[1], "application/octet-stream")
        with open(path, "rb") as fh:
            self._send(code, ctype, fh.read())

    def _notfound(self):
        """Styled 404 for page requests; JSON for API paths. Follows the
        recorded component/page-state anatomy (icon, code, h2, sentence,
        meta ref); the ref is logged so screenshots can be traced. Actions
        deliberately omitted (no safe public destination)."""
        if "/api/" in self.path:
            return self._json({"error": "not found"}, 404)
        ref = secrets.token_hex(2)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
        sys.stderr.write("driftexp notfound ref=%s path=%s\n"
                         % (ref, self.path[:200]))
        with open(os.path.join(HERE, "notfound.html")) as fh:
            html = fh.read().replace("{{REF}}", ref).replace("{{TS}}", ts)
        self._send(404, "text/html; charset=utf-8", html.encode())

    def _read_body(self):
        try:
            length = min(int(self.headers.get("Content-Length") or 0), 65536)
        except ValueError:
            length = 0
        raw = self.rfile.read(length) if length else b""
        try:
            return json.loads(raw.decode() or "{}")
        except ValueError:
            return None

    def log_message(self, format, *args):
        sys.stderr.write("driftexp %s %s\n" % (now(), format % args))

    # ----------------------------------------------------------------- GET
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        base = self._base()
        if path == "/robots.txt":
            return self._send(200, "text/plain; charset=utf-8",
                              b"User-agent: *\nDisallow: /\n")
        if path.startswith("/assets/"):
            norm = os.path.normpath(path)
            if ".." in path or not norm.startswith("/assets/"):
                return self._notfound()
            return self._file(os.path.join(HERE, norm.lstrip("/")))
        if path in ("/", ""):
            return self._notfound()
        if path == base:
            self.send_response(301)
            self.send_header("Location", base + "/")
            self.send_header("X-Robots-Tag", "noindex, nofollow, noarchive")
            self.end_headers()
            return
        if not path.startswith(base + "/"):
            return self._notfound()
        rel = path[len(base) + 1:]
        if rel == "":
            return self._file(os.path.join(HERE, "index.html"))
        if rel in ("styles.css", "app.js"):
            return self._file(os.path.join(HERE, rel))
        if rel.startswith("assets/"):
            norm = os.path.normpath(rel)
            if norm.startswith(".."):
                return self._notfound()
            return self._file(os.path.join(HERE, norm))
        if rel.startswith("img/"):
            name = rel[len("img/"):]
            if not IMG_RE.match(name) or ".." in name:
                return self._notfound()
            return self._file(os.path.join(BLINDSET, "img", name))
        if rel == "api/meta":
            s = load_set() or {}
            comps = s.get("comparisons", [])
            return self._json({
                "title": s.get("title", "Design drift review"),
                "blurb": s.get("blurb", ""),
                "count": len(comps),
                "placeholder": bool(s.get("placeholder")),
                "ready": bool(s),
            })
        if rel == "api/state":
            q = urllib.parse.parse_qs(parsed.query)
            name = clean_name((q.get("name") or [""])[0])
            if not name:
                return self._json({"error": "name required"}, 400)
            s = load_set() or {}
            return self._json(answered_state(name, s.get("comparisons", [])))
        if rel == "api/set":
            s = load_set()
            if not s:
                return self._json({"error": "no review set"}, 404)
            # serve only reviewer-facing fields
            pub = {"title": s.get("title"), "blurb": s.get("blurb", ""),
                   "placeholder": bool(s.get("placeholder")),
                   "comparisons": [{"code": c["code"], "prompt": c.get("prompt", ""),
                                    "left": c["left"], "right": c["right"],
                                    "scale": c.get("scale", 5)}
                                   for c in s.get("comparisons", [])]}
            return self._json(pub)
        return self._notfound()

    # ---------------------------------------------------------------- POST
    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        base = self._base()
        if not path.startswith(base + "/"):
            return self._json({"error": "not found"}, 404)
        rel = path[len(base) + 1:]
        body = self._read_body()
        if body is None:
            return self._json({"error": "bad json"}, 400)
        name = clean_name(body.get("name"))
        if not name:
            return self._json({"error": "name required"}, 400)

        if rel == "api/hello":
            seen = any(
                ev.get("event") == "started" and ev.get("name") == name
                for ev in _iter_events()) if os.path.exists(RATINGS) else False
            if not seen:
                append_event({"event": "started", "name": name, "ts": now()})
            s = load_set() or {}
            st = answered_state(name, s.get("comparisons", []))
            return self._json({"ok": True, **st})

        if rel == "api/answer":
            s = load_set() or {}
            codes = {c["code"] for c in s.get("comparisons", [])}
            code = str(body.get("code") or "")
            try:
                rating = int(body.get("rating"))
            except (TypeError, ValueError):
                rating = 0
            if code not in codes:
                return self._json({"error": "unknown comparison"}, 400)
            if rating < 1 or rating > 5:
                return self._json({"error": "rating must be 1-5"}, 400)
            note = " ".join(str(body.get("note") or "").split())[:500]
            append_event({"event": "answer", "name": name, "code": code,
                          "rating": rating, "note": note, "ts": now()})
            st = answered_state(name, s.get("comparisons", []))
            return self._json({"ok": True, "answered_count": len(st["answered"]),
                               "index": st["index"]})

        if rel == "api/comment":
            text = " ".join(str(body.get("text") or "").split())[:4000]
            append_event({"event": "comment", "name": name, "text": text,
                          "ts": now()})
            return self._json({"ok": True})

        return self._json({"error": "not found"}, 404)


def _iter_events():
    with open(RATINGS, errors="replace") as fh:
        for line in fh:
            try:
                yield json.loads(line)
            except ValueError:
                continue


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8455)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--base-path", default=None,
                    help="capability path prefix (default: /r/<config token>)")
    args = ap.parse_args(argv)

    cfg = load_config()
    base = args.base_path or ("/r/" + cfg["token"])
    srv = Server((args.host, args.port), Handler)
    srv.base_path = base
    s = load_set()
    state = "ready (%d comparisons)" % len(s.get("comparisons", [])) if s else \
        "NO REVIEW SET — run tools/make_placeholders.py (or the real generator)"
    print("driftexp starting\n  local : http://%s:%d%s/\n  public: https://driftexp.seanyong.xyz%s/\n  set   : %s"
          % (args.host, args.port, base, base, state), flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    sys.exit(main())
