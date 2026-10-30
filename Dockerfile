# Serves the prebuilt Ren'Py web build (web-build/) with COOP/COEP headers.
# Build web-build/ first (see WEB.md) — it is gitignored and must exist locally.
FROM python:3.12-slim

WORKDIR /app
COPY scripts/serve_web.py scripts/serve_web.py
COPY web-build web-build

ENV HOST=0.0.0.0
# Cloud Run injects PORT (default 8080); serve_web.py reads it.
ENV PORT=8080

CMD ["python3", "scripts/serve_web.py"]
