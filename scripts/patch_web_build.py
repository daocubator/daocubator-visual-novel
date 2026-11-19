#!/usr/bin/env python3
"""Post-process a Ren'Py web build: add the mobile "Install" button.

Ren'Py regenerates index.html from the SDK template on every web_build and has
no hook for a custom template, so run this after each build:

    python3 scripts/patch_web_build.py web-build

Idempotent: copies scripts/web/install-prompt.js into the build and adds a
<script> tag for it to index.html if it isn't there yet.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "web", "install-prompt.js")
TAG = '<script src="install-prompt.js"></script>'


def main(dest):
    index = os.path.join(dest, "index.html")
    if not os.path.isfile(index):
        sys.exit(f"{index} not found - build the web version first")

    shutil.copy(SRC, os.path.join(dest, "install-prompt.js"))

    with open(index, encoding="utf-8") as f:
        html = f.read()
    if TAG not in html:
        if "</body>" not in html:
            sys.exit("index.html has no </body> - Ren'Py template changed?")
        html = html.replace("</body>", f"  {TAG}\n</body>", 1)
        with open(index, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
    print(f"patched {index} (install button)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "web-build"))
