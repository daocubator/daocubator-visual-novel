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


# Cloud Run rejects (500) any HTTP/1 response over 32 MiB that carries a
# Content-Length. Files above this size are sent with chunked transfer
# encoding instead, which Cloud Run streams without a size cap.
CHUNKED_THRESHOLD = 16 * 1024 * 1024


class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # required for Transfer-Encoding: chunked
    _chunked = False

    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def do_GET(self):
        path = self.translate_path(self.path)
        self._chunked = os.path.isfile(path) and os.path.getsize(path) > CHUNKED_THRESHOLD
        super().do_GET()

    def do_HEAD(self):
        self._chunked = False
        super().do_HEAD()

    def send_header(self, keyword, value):
        if self._chunked and keyword.lower() == "content-length":
            keyword, value = "Transfer-Encoding", "chunked"
        super().send_header(keyword, value)

    def copyfile(self, source, outputfile):
        if not self._chunked:
            return super().copyfile(source, outputfile)
        while True:
            buf = source.read(1024 * 1024)
            if not buf:
                break
            outputfile.write(b"%x\r\n" % len(buf) + buf + b"\r\n")
        outputfile.write(b"0\r\n\r\n")

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
