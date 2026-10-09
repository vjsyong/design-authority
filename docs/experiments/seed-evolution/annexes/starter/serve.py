#!/usr/bin/env python3
"""Tiny static dev server for the Bookmarks app.

    python3 serve.py --port 8090

Serves the project directory on 127.0.0.1 and answers /healthz with 200.
"""
import argparse
import http.server
import socketserver


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")
            return
        return super().do_GET()

    def log_message(self, fmt, *args):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8090, help="any free port (8080 is often busy on this machine)")
    ap.add_argument("--bind", default="127.0.0.1")
    args = ap.parse_args()
    with socketserver.ThreadingTCPServer((args.bind, args.port), Handler) as httpd:
        httpd.allow_reuse_address = True
        print("serving on http://%s:%d" % (args.bind, args.port), flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
