#!/usr/bin/env python3
"""Catch literal-percent bugs in Ren'Py displayed text, across ALL branches.

With config.old_substitutions on (Ren'Py's default), `s % tag_quoting_dict`
is applied to BOTH say statements (sayexports.py) and menu choices
(menuexports.py). A literal `%` there is read as a format code: it either
crashes (e.g. `% o`) OR silently garbles (e.g. `% a` -> a valid %a/ascii
conversion that prints "<TagQuotingDict object ...>"). `renpy lint` catches
neither. The only safe literal percent is `%%`.

Rule: a displayed string is safe iff it contains no lone `%` — i.e. after
removing every `%%` pair, no `%` remains. (This game uses `[...]` for
interpolation and never intentional %-format specs, so every `%` is literal.)

Screen `text` statements do NOT apply `%` formatting, so this only targets
say statements and menu choices — never screen text (e.g. lessons.rpy data).

Translations are covered too. game/tl/<lang>/*.rpy say lines follow the say
rule above. But `new "..."` lines in `translate <lang> strings:` blocks are the
OPPOSITE: menu labels are %-formatted *before* the string-table lookup, so the
`old`/`new` pair holds already-formatted text that is never formatted again.
There a literal percent is a single `%`, and `%%` would display as "%%".
Engine string tables (tl/*/common.rpy) are skipped.

Usage:
  python3 scripts/lint_dialogue.py         # report (exit 1 if problems)
  python3 scripts/lint_dialogue.py --fix   # auto-escape and rewrite
"""
import glob
import os
import re
import sys

SPEAKERS = ["narrator", "pc", "mod", "ashel", "laylay", "xochtl",
            "maya", "jordan", "alex", "vera", "spectre", "atlas",
            "m", "j", "a", "v", "s", "w"]
STR = r'"(?:[^"\\]|\\.)*"'

# A say statement:  <speaker> "..."  [extra]
SAY_RE = re.compile(r'^(\s*)(' + "|".join(SPEAKERS) + r')(\s+)(' + STR + r')(.*)$')
# A menu choice / caption:  "..."[ if cond]:   (string first, line ends in a colon)
MENU_RE = re.compile(r'^(\s*)(' + STR + r')(\s*(?:if\s+.*?)?:)\s*$')
# A translated string:  new "..."
NEW_RE = re.compile(r'^(\s*new\s+)(' + STR + r')()\s*$')

GAME_DIR = os.path.join(os.path.dirname(__file__), "..", "game")


def unsafe(inner):
    """True if the string has a lone % (would crash or garble under % formatting)."""
    return "%" in inner.replace("%%", "")


def escape(inner):
    """Double every % that isn't already part of a %% pair (idempotent)."""
    return re.sub(r'%%|%', lambda m: '%%', inner)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    fix = "--fix" in sys.argv
    problems = 0
    fixed = 0
    paths = sorted(glob.glob(os.path.join(GAME_DIR, "**", "*.rpy"), recursive=True))
    for path in paths:
        if os.path.basename(path) == "common.rpy" and os.sep + "tl" + os.sep in path:
            continue
        lines = open(path, encoding="utf-8").read().split("\n")
        changed = False
        for i, line in enumerate(lines):
            m = SAY_RE.match(line)
            kind = "say"
            if not m:
                m = MENU_RE.match(line)
                kind = "menu"
            if not m:
                m = NEW_RE.match(line)
                kind = "tl-string"
            if not m:
                continue
            # group index of the string literal differs per pattern
            gi = 4 if kind == "say" else 2
            inner = m.group(gi)[1:-1]
            if kind == "tl-string":
                if "%%" not in inner:
                    continue
            elif not unsafe(inner):
                continue
            problems += 1
            rel = os.path.relpath(path, os.path.join(GAME_DIR, ".."))
            if fix:
                if kind == "tl-string":
                    newlit = '"' + inner.replace("%%", "%") + '"'
                else:
                    newlit = '"' + escape(inner) + '"'
                g = list(m.groups())
                g[gi - 1] = newlit
                lines[i] = "".join(x for x in g if x is not None)
                changed = True
                fixed += 1
                print(f"FIXED  {rel}:{i+1}  ({kind})")
            else:
                print(f"BUG    {rel}:{i+1}  ({kind})  {line.strip()[:80]}")
        if fix and changed:
            open(path, "w", encoding="utf-8").write("\n".join(lines))
    if fix:
        print(f"\n{fixed} string(s) escaped.")
        return 0
    if problems:
        print(f"\n{problems} displayed string(s) have a lone % (crash or garble), or a %% in a tl string. Run --fix.")
        return 1
    print("All say + menu strings are percent-safe.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
