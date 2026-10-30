#!/usr/bin/env python3
"""Serve the Ren'Py web build with the COOP/COEP headers it requires.

Ren'Py web (WASM + SharedArrayBuffer) only runs when the page is served
cross-origin-isolated. Python's plain http.server doesn't set those headers,
so this wrapper adds them.

Usage: python3 scripts/serve_web.py [port]   (default 8042, dir ./web-build)

Cloud Run: set PORT (Cloud Run injects it) and HOST=0.0.0.0 via env vars.
"""
import http.server
import mimetypes
import os
import sys

mimetypes.add_type("application/wasm", ".wasm")

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8042))
HOST = os.environ.get("HOST", "127.0.0.1")
ROOT = os.path.join(os.path.dirname(__file__), "..", "web-build")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        # Revalidate so a new deploy is picked up, but allow 304s for the
        # large wasm/data/image payloads instead of forcing a full re-download.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


if __name__ == "__main__":
    os.chdir(ROOT)
    httpd = http.server.ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"serving {ROOT} at http://{HOST}:{PORT}/  (COOP/COEP enabled)")
    httpd.serve_forever()
