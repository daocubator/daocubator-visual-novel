# Web build — DAOCUBATOR / "Get Rich Together"

A browser (WASM) build so collaborators can **play in a browser with no Ren'Py install**.
The build output (`web-build/`) is gitignored — it's ~48 MB of WASM/data blobs; regenerate it with the steps below.

## Prerequisites (one-time): install Ren'Py web support

The SDK at `~/renpy-8.5.0-sdk` doesn't ship web support by default. Install it once:

```bash
curl -s "http://update.renpy.org/8.5.0/renpy-8.5.0-web.update.gz" -o /tmp/web.update.gz
gzip -dc /tmp/web.update.gz | tar xf - -C ~/renpy-8.5.0-sdk web/
```

The web runtime version must **exactly match** the SDK (`renpy.sh --version` → 8.5.0 here).
The launcher checks `web/hash.txt`; a mismatched runtime (e.g. 8.5.3 on an 8.5.0 SDK) fails
with `TypeError: expected str ... not NoneType` in `build_web`.

On Windows (no `renpy.sh`), run the SDK's bundled Python:
`~/renpy-8.5.0-sdk/lib/py3-windows-x86_64/python.exe ~/renpy-8.5.0-sdk/renpy.py ~/renpy-8.5.0-sdk/launcher web_build "<abs project path>" --dest "<abs project path>/web-build"`.
Stop `serve_web.py` first — it holds `web-build/` open and the build can't replace it.

## Build

```bash
~/renpy-8.5.0-sdk/renpy.sh ~/renpy-8.5.0-sdk/launcher web_build . --dest ./web-build
```

Produces `web-build/` (index.html + renpy.wasm + renpy.data + game.zip + icons).
The browser build's source artwork lives at the project root: `web-presplash.jpg`
for the loading screen and `web-icon.png` for the page/PWA icons. Update those
files before rebuilding; changing only `web-build/` won't affect the GitHub Pages
workflow, which builds from the project source on each run.

## Play locally

Ren'Py web requires cross-origin isolation (COOP/COEP headers), which a plain
`python -m http.server` does NOT set. Use the wrapper:

```bash
python3 scripts/serve_web.py 8055      # serves ./web-build with COOP/COEP
# open http://127.0.0.1:8055/index.html
```

First load is slow (~1–2 min): the browser downloads + unpacks the WASM runtime,
the placeholder images, and the music track, then compiles the script. It's cached
after the first load. Click **Start** to play.

## Hosting for collaborators

**GitHub Pages (automatic):** `.github/workflows/pages.yml` rebuilds the web version on every
push to `main` with a fresh Ren'Py 8.5.0 SDK + matching web runtime and publishes it to Pages.
One-time setup: repo Settings → Pages → Source: "GitHub Actions". Re-run by hand from the
Actions tab ("Run workflow"). Bump `RENPY_VERSION` there when the SDK is upgraded.

Other options for a Ren'Py web build:
- **itch.io** — upload `web-build/` as an HTML project, tick "SharedArrayBuffer support". Easiest; handles the COOP/COEP headers.
- **Any static host that lets you set headers** — the page needs
  `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`.
  (GitHub Pages can't set these directly; the build's bundled service worker works around it on most browsers, but itch.io is the path of least resistance.)

## What ships

`game/options.rpy` excludes `vault/`, `research/`, `prototypes/`, `scripts/`, `build/`,
root `*.md`/`*.txt`/`*.zip` and `game/saves/` from every distribution. Before that, the
public web `game.zip` contained the whole repo (design docs, research PDFs, the dev's
persistent file) — and a stale `web-build.zip` from the previous build.

## Note on automated testing

The Claude desktop app's built-in browser CAN drive the web build: `.claude/launch.json`
defines a `web-build` server (serve_web.py on :8055). Ren'Py focuses buttons on mouse-move,
so hover before clicking; the first click on the canvas only gives it focus.

Automated click-through of the desktop app (or a web tab that isn't visible) doesn't work in a
headless/background sandbox: when the window/tab isn't the OS-foreground surface, the
engine's event loop is throttled and injected input isn't processed. Verify dialogue/logic
statically instead — `python3 scripts/lint_dialogue.py` + `renpy.sh . lint` — and click
through a real, focused browser/desktop window for interactive confirmation.
