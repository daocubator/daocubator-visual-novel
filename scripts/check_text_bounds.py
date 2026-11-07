#!/usr/bin/env python3
"""Check that all Ren'Py dialogue (`say`) and menu choice strings fit within
their GUI text containers without overflowing vertically or horizontally.

Measures actual pixel word-wrapping using PIL/FreeType (`DejaVuSans.ttf`) after:
  1. Unescaping `%%` -> `%` and `\\"` -> `"`
  2. Applying the glossary filter (`gloss_link_text` from `game/glossary.rpy`,
     which appends the `ˀ` superscript marker to the first mention of each term)
  3. Substituting `[...]` interpolations with realistic worst-case placeholders
  4. Stripping Ren'Py display tags (`{b}`, `{i}`, `{a=...}`, `{color=...}`, etc.)

Checks both:
  - Main script files (`game/*.rpy`)
  - Translation / Plain Mode files (`game/tl/<lang>/*.rpy`)

Usage:
  python scripts/check_text_bounds.py           # check against current gui.rpy & screens.rpy
  python scripts/check_text_bounds.py --verbose # also list 4-line dialogue & multi-line choices
"""

import glob
import os
import re
import sys
import textwrap
from PIL import ImageFont

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GAME_DIR = os.path.join(ROOT_DIR, "game")

SPEAKERS = [
    "narrator", "pc", "mod", "ashel", "laylay", "xochtl",
    "maya", "jordan", "alex", "vera", "spectre", "atlas",
    "m", "j", "a", "v", "s", "w",
]
NARRATOR_SPEAKERS = {"narrator"}
STR_PAT = r'"(?:[^"\\]|\\.)*"'

SAY_RE = re.compile(r'^(\s*)(' + "|".join(SPEAKERS) + r')(\s+)(' + STR_PAT + r')(.*)$')
MENU_RE = re.compile(r'^(\s*)(' + STR_PAT + r')(\s*(?:if\s+.*?)?:)\s*$')
TAG_RE = re.compile(r'\{[^{}]*\}')
INTERP_RE = re.compile(r'\[([^\[\]]+)\]')


def load_glossary_filter():
    """Load `gloss_link_text` from `game/glossary.rpy` standalone init block."""
    gloss_path = os.path.join(GAME_DIR, "glossary.rpy")
    with open(gloss_path, encoding="utf-8") as f:
        src = f.read()
    m = re.search(r"init -10 python:\n((?:    .*\n|\n)+)", src)
    if not m:
        return lambda s: s
    ns = {}
    exec(textwrap.dedent(m.group(1)), ns)
    return ns.get("gloss_link_text", lambda s: s)


def parse_gui_settings():
    """Read current dialogue layout numbers from `game/gui.rpy` and `game/screens.rpy`."""
    gui_path = os.path.join(GAME_DIR, "gui.rpy")
    screens_path = os.path.join(GAME_DIR, "screens.rpy")
    with open(gui_path, encoding="utf-8") as f:
        gui_src = f.read()
    with open(screens_path, encoding="utf-8") as f:
        scr_src = f.read()

    def get_int(name, default):
        m = re.search(rf"^\s*define\s+gui\.{name}\s*=\s*(\d+)", gui_src, re.MULTILINE)
        return int(m.group(1)) if m else default

    dialogue_ypos = get_int("dialogue_ypos", 75)
    # Check if screen say uses a smaller ypos when `who is None`
    m_narr_y = re.search(r'id\s+"what"\s+ypos\s+\(gui\.dialogue_ypos\s+if\s+who\s+is\s+not\s+None\s+else\s+(\d+)\)', scr_src)
    narrator_ypos = int(m_narr_y.group(1)) if m_narr_y else dialogue_ypos

    # Check if style window uses auto-expanding yminimum + Frame
    auto_expand = bool(
        re.search(r"style window:[\s\S]*?yminimum\s+gui\.textbox_height", scr_src)
        and re.search(r'style window:[\s\S]*?Frame\("gui/textbox\.png"', scr_src)
    )

    # Parse choice_button_borders left/right padding
    m_cb = re.search(
        r"^\s*define\s+gui\.choice_button_borders\s*=\s*Borders\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)",
        gui_src,
        re.MULTILINE,
    )
    cb_pad_x = (int(m_cb.group(1)) + int(m_cb.group(3))) if m_cb else 300

    return {
        "text_size": get_int("text_size", 33),
        "textbox_height": get_int("textbox_height", 278),
        "dialogue_xpos": get_int("dialogue_xpos", 240),
        "dialogue_ypos": dialogue_ypos,
        "narrator_ypos": narrator_ypos,
        "dialogue_width": get_int("dialogue_width", 1440),
        "choice_button_width": get_int("choice_button_width", 1360),
        "choice_pad_x": cb_pad_x,
        "auto_expand": auto_expand,
    }


def prepare_displayed_text(raw_inner, gloss_link_fn, is_tl_string=False):
    """Simulate Ren'Py's text pipeline from raw string literal to visible glyphs."""
    s = raw_inner.replace('\\"', '"').replace("\\'", "'").replace("\\n", "\n")
    if not is_tl_string:
        s = s.replace("%%", "%")
    s = gloss_link_fn(s)
    # Replace [var] interpolations with a representative 10-char string
    s = INTERP_RE.sub("AetherLabs", s)
    # Strip Ren'Py text tags {b}, {a=...}, etc.
    s = TAG_RE.sub("", s)
    s = s.replace("{{", "{").replace("[[", "[")
    return s


def wrap_text_pixels(text, font, max_width):
    """Wrap `text` into lines using pixel widths from `font` (matching Ren'Py greedy/tex wrap)."""
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            cand = w if not cur else (cur + " " + w)
            # Slight 1.02x safety factor for bold/kerning variance
            if font.getlength(cand) * 1.02 <= max_width:
                cur = cand
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    verbose = "--verbose" in sys.argv

    gloss_link_fn = load_glossary_filter()
    gui = parse_gui_settings()

    font_path = os.path.join(GAME_DIR, "fonts", "Karla-Variable.woff2")
    font_desktop = ImageFont.truetype(font_path, gui["text_size"])
    line_bbox = font_desktop.getbbox("Ag")
    line_height = int(round((line_bbox[3] - line_bbox[1]) * 1.35))  # ~42px at size 33

    # Visible bottom border of textbox.png is at y = H - 14 (264 for 278px height)
    visible_bottom_y = gui["textbox_height"] - 14
    avail_spk = visible_bottom_y - gui["dialogue_ypos"]
    avail_narr = visible_bottom_y - gui["narrator_ypos"]
    max_lines_spk = avail_spk // line_height
    max_lines_narr = avail_narr // line_height

    # Choice button inner width
    choice_inner_width = gui["choice_button_width"] - gui["choice_pad_x"]

    print(
        f"GUI Config: dialogue_xpos={gui['dialogue_xpos']}, "
        f"dialogue_ypos={gui['dialogue_ypos']} (narrator={gui['narrator_ypos']}), "
        f"dialogue_width={gui['dialogue_width']}px, "
        f"text_size={gui['text_size']}px (~{line_height}px/line)"
    )
    print(
        f"Base textbox budget (before auto-expand): "
        f"speaker={max_lines_spk} lines ({avail_spk}px), "
        f"narrator={max_lines_narr} lines ({avail_narr}px), "
        f"auto_expand_frame={gui['auto_expand']}\n"
    )

    paths = sorted(glob.glob(os.path.join(GAME_DIR, "**", "*.rpy"), recursive=True))
    prose_overflows = []
    explicit_multiline = []
    near_overflows = []
    long_choices = []
    total_say = 0
    total_menu = 0

    for path in paths:
        if os.path.basename(path) == "common.rpy" and (os.sep + "tl" + os.sep) in path:
            continue
        rel = os.path.relpath(path, ROOT_DIR)
        raw_lines = open(path, encoding="utf-8").read().splitlines()
        for idx, line in enumerate(raw_lines, 1):
            m_say = SAY_RE.match(line)
            if m_say:
                total_say += 1
                spk = m_say.group(2)
                inner = m_say.group(4)[1:-1]
                disp = prepare_displayed_text(inner, gloss_link_fn)
                wrapped = wrap_text_pixels(disp, font_desktop, gui["dialogue_width"])
                n_lines = len(wrapped)
                req_h = n_lines * line_height
                max_safe = max_lines_narr if spk in NARRATOR_SPEAKERS else max_lines_spk

                if n_lines > max_safe:
                    if "\n" in disp and gui["auto_expand"]:
                        explicit_multiline.append((n_lines, req_h, len(disp), rel, idx, spk, disp, wrapped))
                    else:
                        prose_overflows.append((n_lines, req_h, len(disp), rel, idx, spk, disp, wrapped))
                elif n_lines == max_safe:
                    near_overflows.append((n_lines, req_h, len(disp), rel, idx, spk, disp, wrapped))
                continue

            m_menu = MENU_RE.match(line)
            if m_menu:
                total_menu += 1
                inner = m_menu.group(2)[1:-1]
                disp = prepare_displayed_text(inner, gloss_link_fn)
                wrapped = wrap_text_pixels(disp, font_desktop, choice_inner_width)
                if len(wrapped) > 3:
                    long_choices.append((len(wrapped), len(disp), rel, idx, disp))

    prose_overflows.sort(key=lambda x: (-x[0], -x[2]))
    explicit_multiline.sort(key=lambda x: (-x[0], -x[2]))
    near_overflows.sort(key=lambda x: (-x[0], -x[2]))

    print(f"Scanned {total_say} dialogue lines and {total_menu} menu choices across {len(paths)} files.")
    print(f"  Prose overflows (> base height): {len(prose_overflows)}")
    print(f"  Explicit multi-line blocks (handled by auto-expand Frame): {len(explicit_multiline)}")
    print(f"  At base limit: {len(near_overflows)}")
    print(f"  Menu choices > 3 lines: {len(long_choices)}")

    if prose_overflows:
        print("\nOVERFLOWING PROSE DIALOGUE LINES:")
        for n_lines, req_h, n_chars, rel, idx, spk, disp, wrapped in prose_overflows:
            print(f"  [{n_lines} lines / ~{req_h}px / {n_chars} chars] {rel}:{idx} ({spk})")
            print(f"      {disp[:110]}{'...' if len(disp) > 110 else ''}")

    if verbose and explicit_multiline:
        print("\nEXPLICIT MULTI-LINE BLOCKS (auto-expanded by Frame):")
        for n_lines, req_h, n_chars, rel, idx, spk, disp, wrapped in explicit_multiline:
            flat = disp.replace("\n", " \\n ")
            print(f"  [{n_lines} lines / ~{req_h}px] {rel}:{idx} ({spk}): {flat[:100]}...")

    if verbose and near_overflows:
        print("\nAT-LIMIT DIALOGUE LINES:")
        for n_lines, req_h, n_chars, rel, idx, spk, disp, wrapped in near_overflows[:20]:
            print(f"  [{n_lines} lines / ~{req_h}px / {n_chars} chars] {rel}:{idx} ({spk})")
            print(f"      {disp[:110]}{'...' if len(disp) > 110 else ''}")

    if long_choices:
        print("\nLONG MENU CHOICES (> 2 lines):")
        for n_lines, n_chars, rel, idx, disp in long_choices:
            print(f"  [{n_lines} lines / {n_chars} chars] {rel}:{idx}: {disp}")

    return 1 if (prose_overflows or long_choices) else 0


if __name__ == "__main__":
    sys.exit(main())
