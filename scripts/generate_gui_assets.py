#!/usr/bin/env python3
"""
Generate complete GUI assets for Get Rich Together
strictly following the DAOcubator Design System (research/DAOcubator-design-system):
- Grounds: ink (#140702), char (#1E140E), ground (#241309), panel (#2D1B10), field (#42281E)
- Accents & Light: glow (#FAC443), glow-core (#FFF3C9), ember (#D3710D), clay (#B87444), rust (#834225)
- Structural & Cool: sand (#AE896A), teal (#578C88), verdigris (#3B615F), mark (#1C1A15)
- Text & Rules: flame (#EED4B4), bone (#DDBCAD), ash (#9D908D), rule, rule-strong
- Geometry: Square structure (radius-0); round shapes only for rings, discs, seed dots, and twine knots (radius-full).
- HungPanel motif: panel (#2D1B10) hung on visible sand (#AE896A) twine with round knots inside a field (#42281E) timber frame over a char (#1E140E) wall.
"""

import os
import math
from PIL import Image, ImageDraw, ImageEnhance

# -------------------------------------------------------------------------
# Directories
# -------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GUI_DIR = os.path.join(BASE_DIR, 'game', 'gui')
VAULT_GUI_DIR = os.path.join(BASE_DIR, 'vault', '06 Assets', 'generated_gui')
DESIGN_SYS_IMAGERY = os.path.join(BASE_DIR, 'research', 'DAOcubator-design-system', 'assets', 'Imagery', 'first-constellation.jpg')
BG_CONSTELLATION = os.path.join(BASE_DIR, 'game', 'images', 'bg constellation.png')

os.makedirs(VAULT_GUI_DIR, exist_ok=True)
for sub in ['', 'button', 'overlay', 'phone', 'phone/button', 'phone/overlay',
            'phone/scrollbar', 'phone/slider', 'phone/bar',
            'scrollbar', 'slider', 'bar']:
    os.makedirs(os.path.join(GUI_DIR, sub), exist_ok=True)
    os.makedirs(os.path.join(VAULT_GUI_DIR, sub), exist_ok=True)

# -------------------------------------------------------------------------
# DAOcubator Design System Color Tokens (tokens.json)
# -------------------------------------------------------------------------
INK         = (20, 7, 2, 255)        # #140702 - Default page and slide ground
CHAR        = (30, 20, 14, 255)      # #1E140E - Raised ground: cards, panels, hung-frame wall
GROUND      = (36, 19, 9, 255)       # #241309 - Alternate layer in a stack
PANEL       = (45, 27, 16, 255)      # #2D1B10 - Fill of a panel hung in its frame and of node cards
FIELD       = (66, 40, 30, 255)      # #42281E - Timber: frame rails and table label cells
CLAY        = (184, 116, 68, 255)    # #B87444 - Mid-value workhorse material fill
RUST        = (131, 66, 37, 255)     # #834225 - Deep warm end of a fill or gradient
EMBER       = (211, 113, 13, 255)    # #D3710D - Warm accent: inner ring of a node, secondary fills
GLOW        = (250, 196, 67, 255)    # #FAC443 - The light: rings, panel titles, links, focus ring
GLOW_CORE   = (255, 243, 201, 255)   # #FFF3C9 - Near-white hot core at the centre of a glow
SAND        = (174, 137, 106, 255)   # #AE896A - Twine, table grids and structural hairlines
VERDIGRIS   = (59, 97, 95, 255)      # #3B615F - Cool shadow (decorative fills only)
TEAL        = (87, 140, 136, 255)    # #578C88 - Cool accent
MARK        = (28, 26, 21, 255)      # #1C1A15 - The glossy near-black mark: strokes, pips, counters
FLAME       = (238, 212, 180, 255)   # #EED4B4 - Titles and ledes
BONE        = (221, 188, 173, 255)   # #DDBCAD - Body copy
ASH         = (157, 144, 141, 255)   # #9D908D - Secondary text, captions and control borders
RULE        = (221, 188, 173, 41)    # rgba(221,188,173,0.16) - Quiet dividers and card edges
RULE_STRONG = (221, 188, 173, 77)    # rgba(221,188,173,0.3) - Panel frames and stack dividers

def with_alpha(col, a):
    return (col[0], col[1], col[2], a)

def save_asset(im, rel_path):
    dest1 = os.path.join(GUI_DIR, rel_path)
    dest2 = os.path.join(VAULT_GUI_DIR, rel_path)
    os.makedirs(os.path.dirname(dest1), exist_ok=True)
    os.makedirs(os.path.dirname(dest2), exist_ok=True)
    im.save(dest1, format='PNG')
    im.save(dest2, format='PNG')
    print(f"Saved: {rel_path} ({im.size}, {im.mode})")


# -------------------------------------------------------------------------
# 1. Main Menu and Game Menu Backgrounds
# -------------------------------------------------------------------------
def generate_menus():
    print("--- Generating Menu Backgrounds ---")
    src_path = BG_CONSTELLATION if os.path.exists(BG_CONSTELLATION) else (
        DESIGN_SYS_IMAGERY if os.path.exists(DESIGN_SYS_IMAGERY) else None
    )

    if src_path:
        src = Image.open(src_path).convert('RGB')
        main_menu = src.resize((1920, 1080), Image.Resampling.LANCZOS).convert('RGBA')

        # Warm ink (#140702) vignette scrim on left for navigation legibility
        scrim = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
        scrim_draw = ImageDraw.Draw(scrim)
        for x in range(780):
            factor = (1.0 - (x / 780.0)) ** 1.4
            alpha = int(195 * factor)
            scrim_draw.line([(x, 0), (x, 1080)], fill=with_alpha(INK, alpha))

        main_menu_final = Image.alpha_composite(main_menu, scrim)
        save_asset(main_menu_final, 'main_menu.png')

        # Game Menu: Warm ink/char ground with field timber rail and sand hairlines
        game_menu = main_menu.copy().convert('RGB')
        game_menu = ImageEnhance.Brightness(game_menu).enhance(0.28).convert('RGBA')

        vignette = Image.new('RGBA', (1920, 1080), with_alpha(INK, 190))
        v_draw = ImageDraw.Draw(vignette)
        # Left navigation column on ground (#241309), content area on char (#1E140E)
        v_draw.rectangle([0, 0, 420, 1080], fill=with_alpha(GROUND, 215))
        v_draw.rectangle([0, 0, 18, 1080], fill=FIELD)
        v_draw.line([(420, 0), (420, 1080)], fill=SAND, width=1)
        # Top header bar divider in sand
        v_draw.rectangle([24, 24, 1895, 1055], outline=RULE_STRONG, width=1)
        # Oblique mark member on the left timber rail
        v_draw.polygon([(0, 148), (38, 136), (38, 152), (0, 164)], fill=MARK)

        game_menu = Image.alpha_composite(game_menu, vignette)
        save_asset(game_menu, 'game_menu.png')
        save_asset(game_menu, 'nvl.png')
        save_asset(game_menu, 'phone/nvl.png')
    else:
        print("WARNING: No menu background source found!")


# -------------------------------------------------------------------------
# 2. Overlays
# -------------------------------------------------------------------------
def generate_overlays():
    print("--- Generating Overlays ---")
    mm_ov = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    save_asset(mm_ov, 'overlay/main_menu.png')
    save_asset(mm_ov, 'phone/overlay/main_menu.png')

    # game_menu overlay: warm ink/char wash
    gm_ov = Image.new('RGBA', (1920, 1080), with_alpha(INK, 185))
    save_asset(gm_ov, 'overlay/game_menu.png')
    save_asset(gm_ov, 'phone/overlay/game_menu.png')

    # confirm modal overlay: deep ink ground
    conf_ov = Image.new('RGBA', (1920, 1080), with_alpha(INK, 224))
    save_asset(conf_ov, 'overlay/confirm.png')


# -------------------------------------------------------------------------
# 3. Dialogue Textbox & Namebox (HungPanel Architecture)
# -------------------------------------------------------------------------
def generate_textbox():
    print("--- Generating Textbox & Namebox (HungPanel) ---")
    # Desktop textbox: 1920 x 278
    # Note: screens.rpy uses Frame("gui/textbox.png", Borders(200, 32, 200, 32))
    # Keeping all knots and vertical twine inside x < 200 and x > 1720 ensures
    # 9-slice horizontal stretching never distorts the knots or vertical twine.
    W, H = 1920, 278
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # Outer timber frame (`field` #42281E)
    draw.rectangle([0, 0, W - 1, H - 1], fill=with_alpha(FIELD, 242))
    # Top and bottom subtle structural hairlines
    draw.line([(0, 0), (W - 1, 0)], fill=SAND, width=1)

    # Hung-frame wall (`char` #1E140E) inside the oversized `field` timber frame
    wall_left, wall_top, wall_right, wall_bot = 16, 10, W - 17, H - 11
    draw.rectangle([wall_left, wall_top, wall_right, wall_bot], fill=with_alpha(CHAR, 248))

    # Asymmetric hung `panel` (#2D1B10) with `rule-strong` 1px square border
    p_left, p_top, p_right, p_bot = 176, 24, W - 156, H - 18
    draw.rectangle([p_left, p_top, p_right, p_bot], fill=with_alpha(PANEL, 252), outline=RULE_STRONG, width=1)

    # Sand twine ties (`stroke-thread` = 2px in `sand` #AE896A) with round 10px knots (`radius-full`)
    # Tie A (left, inside x < 200 non-stretched region)
    tie_a_x = 188
    draw.rectangle([tie_a_x - 1, 0, tie_a_x, p_top], fill=SAND)
    draw.ellipse([tie_a_x - 5, p_top - 5, tie_a_x + 5, p_top + 5], fill=SAND)
    # Tail A (bottom dangling twine end)
    draw.line([(tie_a_x + 2, p_bot), (tie_a_x + 5, H - 1)], fill=SAND, width=2)

    # Tie B (right, inside x > 1720 non-stretched region)
    tie_b_x = W - 172
    draw.rectangle([tie_b_x - 1, 0, tie_b_x, p_top], fill=SAND)
    draw.ellipse([tie_b_x - 5, p_top - 5, tie_b_x + 5, p_top + 5], fill=SAND)
    # Tail B (bottom dangling twine end)
    draw.line([(tie_b_x - 2, p_bot), (tie_b_x - 6, H - 1)], fill=SAND, width=2)

    # The Mark (#1C1A15): one glossy near-black element entering obliquely on the left timber/wall margin
    draw.polygon([(0, 68), (112, 44), (112, 58), (0, 82)], fill=MARK)
    # Small detached square status pips in `mark` (#1C1A15) and `sand`
    draw.rectangle([56, 102, 66, 112], fill=MARK, outline=RULE, width=1)
    draw.rectangle([74, 102, 84, 112], fill=MARK, outline=RULE, width=1)

    save_asset(im, 'textbox.png')

    # Phone textbox (1920 x 360, Borders(32, 32, 32, 32))
    H_phone = 360
    im_phone = Image.new('RGBA', (W, H_phone), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(im_phone)
    p_draw.rectangle([0, 0, W - 1, H_phone - 1], fill=with_alpha(FIELD, 245))
    p_draw.line([(0, 0), (W - 1, 0)], fill=SAND, width=2)
    p_draw.rectangle([12, 10, W - 13, H_phone - 11], fill=with_alpha(CHAR, 250))
    p_draw.rectangle([28, 22, W - 29, H_phone - 16], fill=with_alpha(PANEL, 252), outline=RULE_STRONG, width=1)
    save_asset(im_phone, 'phone/textbox.png')

    # Namebox (360 x 48) - Square (`radius-0`), `field` timber plaque with `sand` hairline and `glow` seed dot
    NW, NH = 360, 48
    nb = Image.new('RGBA', (NW, NH), (0, 0, 0, 0))
    n_draw = ImageDraw.Draw(nb)
    n_draw.rectangle([0, 0, NW - 1, NH - 1], fill=FIELD, outline=SAND, width=1)
    # Left warm ember bar + small round glow seed dot (`radius-full`)
    n_draw.rectangle([0, 0, 4, NH - 1], fill=EMBER)
    n_draw.ellipse([12, NH // 2 - 3, 18, NH // 2 + 3], fill=GLOW)
    save_asset(nb, 'namebox.png')


# -------------------------------------------------------------------------
# 4. Choice Buttons (Square `radius-0`, `ash` border idle, `2px glow` focus hover)
# -------------------------------------------------------------------------
def generate_choice_buttons():
    print("--- Generating Choice Buttons ---")
    CW, CH = 1360, 56

    # Choice Idle: raised `char` (#1E140E) with 1px `ash` (#9D908D) control border
    idle = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(idle)
    draw.rectangle([0, 0, CW - 1, CH - 1], fill=with_alpha(CHAR, 242), outline=ASH, width=1)
    # Left timber `field` tab
    draw.rectangle([1, 1, 8, CH - 2], fill=FIELD)

    save_asset(idle, 'button/choice_idle_background.png')
    save_asset(idle, 'phone/button/choice_idle_background.png')

    # Choice Hover: `panel` (#2D1B10) with `2px solid glow` (#FAC443) focus ring
    hover = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hover)
    h_draw.rectangle([0, 0, CW - 1, CH - 1], fill=with_alpha(PANEL, 252), outline=GLOW, width=2)
    h_draw.rectangle([2, 2, 10, CH - 3], fill=EMBER)

    save_asset(hover, 'button/choice_hover_background.png')
    save_asset(hover, 'phone/button/choice_hover_background.png')


# -------------------------------------------------------------------------
# 5. Frames & Modals (frame.png, notify.png, skip.png, bubbles)
# -------------------------------------------------------------------------
def generate_frames():
    print("--- Generating Frames ---")
    # frame.png (900 x 375, 9-slice with Borders(16, 16, 16, 16))
    # Square (`radius-0`): outer `field` timber border, inner `panel` (#2D1B10) with `sand` hairline
    FW, FH = 900, 375
    fr = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fr)
    draw.rectangle([0, 0, FW - 1, FH - 1], fill=with_alpha(FIELD, 245), outline=SAND, width=1)
    draw.rectangle([6, 6, FW - 7, FH - 7], fill=with_alpha(CHAR, 248))
    draw.rectangle([12, 12, FW - 13, FH - 13], fill=with_alpha(PANEL, 252), outline=RULE_STRONG, width=1)

    save_asset(fr, 'frame.png')

    # notify.png (1383 x 64) - Square (`radius-0`), `panel` with `field` left rail & `sand` border
    NW, NH = 1383, 64
    notif = Image.new('RGBA', (NW, NH), (0, 0, 0, 0))
    n_draw = ImageDraw.Draw(notif)
    n_draw.rectangle([0, 0, NW - 1, NH - 1], fill=with_alpha(PANEL, 248), outline=SAND, width=1)
    n_draw.rectangle([1, 1, 8, NH - 2], fill=CLAY)
    save_asset(notif, 'notify.png')

    # skip.png (360 x 64) - Square (`radius-0`), `panel` with `glow` left accent
    SW, SH = 360, 64
    sk = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk)
    s_draw.rectangle([0, 0, SW - 1, SH - 1], fill=with_alpha(PANEL, 248), outline=SAND, width=1)
    s_draw.rectangle([1, 1, 6, SH - 2], fill=GLOW)
    save_asset(sk, 'skip.png')

    # speech bubble / thought bubble (200 x 155, 200 x 133) - Square (`radius-0`)
    for bname, bw, bh in [('bubble.png', 200, 155), ('thoughtbubble.png', 200, 133)]:
        b_im = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        b_draw = ImageDraw.Draw(b_im)
        b_draw.rectangle([2, 2, bw - 3, bh - 3], fill=with_alpha(PANEL, 248), outline=SAND, width=2)
        save_asset(b_im, bname)


# -------------------------------------------------------------------------
# 6. Save/Load Slots and Navigation Buttons
# -------------------------------------------------------------------------
def generate_buttons():
    print("--- Generating Buttons ---")
    # Slot Buttons (414 x 309) - Square (`radius-0`)
    SW, SH = 414, 309

    # Slot Idle: `char` (#1E140E) with 1px `ash` control border
    s_idle = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
    d_idle = ImageDraw.Draw(s_idle)
    d_idle.rectangle([0, 0, SW - 1, SH - 1], fill=with_alpha(CHAR, 238), outline=ASH, width=1)
    d_idle.rectangle([1, 1, SW - 2, 6], fill=FIELD)
    save_asset(s_idle, 'button/slot_idle_background.png')
    save_asset(s_idle, 'phone/button/slot_idle_background.png')

    # Slot Hover: `panel` (#2D1B10) with 2px `glow` (#FAC443) focus ring
    s_hover = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
    d_hover = ImageDraw.Draw(s_hover)
    d_hover.rectangle([0, 0, SW - 1, SH - 1], fill=with_alpha(PANEL, 250), outline=GLOW, width=2)
    d_hover.rectangle([2, 2, SW - 3, 7], fill=CLAY)
    save_asset(s_hover, 'button/slot_hover_background.png')
    save_asset(s_hover, 'phone/button/slot_hover_background.png')

    # General Button (450 x 49) - Square (`radius-0`)
    BW, BH = 450, 49
    b_idle = Image.new('RGBA', (BW, BH), (0, 0, 0, 0))
    bi_draw = ImageDraw.Draw(b_idle)
    bi_draw.rectangle([0, 0, BW - 1, BH - 1], fill=with_alpha(CHAR, 230), outline=ASH, width=1)
    save_asset(b_idle, 'button/idle_background.png')

    b_hover = Image.new('RGBA', (BW, BH), (0, 0, 0, 0))
    bh_draw = ImageDraw.Draw(b_hover)
    bh_draw.rectangle([0, 0, BW - 1, BH - 1], fill=with_alpha(PANEL, 248), outline=GLOW, width=2)
    save_asset(b_hover, 'button/hover_background.png')

    # Phone buttons (450 x 64)
    BH_p = 64
    bp_idle = Image.new('RGBA', (BW, BH_p), (0, 0, 0, 0))
    ImageDraw.Draw(bp_idle).rectangle([0, 0, BW - 1, BH_p - 1], fill=with_alpha(CHAR, 230), outline=ASH, width=1)
    save_asset(bp_idle, 'phone/button/idle_background.png')

    bp_hover = Image.new('RGBA', (BW, BH_p), (0, 0, 0, 0))
    ImageDraw.Draw(bp_hover).rectangle([0, 0, BW - 1, BH_p - 1], fill=with_alpha(PANEL, 248), outline=GLOW, width=2)
    save_asset(bp_hover, 'phone/button/hover_background.png')

    # Quick menu buttons (150 x 45) - Square (`radius-0`)
    QW, QH = 150, 45
    q_idle = Image.new('RGBA', (QW, QH), (0, 0, 0, 0))
    ImageDraw.Draw(q_idle).rectangle([0, 0, QW - 1, QH - 1], fill=with_alpha(CHAR, 225), outline=ASH, width=1)
    save_asset(q_idle, 'button/quick_idle_background.png')

    q_hover = Image.new('RGBA', (QW, QH), (0, 0, 0, 0))
    ImageDraw.Draw(q_hover).rectangle([0, 0, QW - 1, QH - 1], fill=with_alpha(PANEL, 248), outline=GLOW, width=2)
    save_asset(q_hover, 'button/quick_hover_background.png')

    # Checkboxes (square `radius-0`) & Radios (round `radius-full` node ring)
    for h, sub in [(49, 'button'), (64, 'phone/button')]:
        mid = h // 2
        # Check Idle (square `mark` / `char` with `ash` border)
        chk_i = Image.new('RGBA', (27, h), (0, 0, 0, 0))
        ImageDraw.Draw(chk_i).rectangle([4, mid - 9, 22, mid + 9], fill=CHAR, outline=ASH, width=1)
        save_asset(chk_i, f'{sub}/check_foreground.png')

        # Check Selected (square `panel` with `glow` border and inner `glow` mark)
        chk_s = Image.new('RGBA', (27, h), (0, 0, 0, 0))
        cs_draw = ImageDraw.Draw(chk_s)
        cs_draw.rectangle([4, mid - 9, 22, mid + 9], fill=PANEL, outline=GLOW, width=2)
        cs_draw.rectangle([9, mid - 4, 17, mid + 4], fill=GLOW)
        save_asset(chk_s, f'{sub}/check_selected_foreground.png')

        # Radio Idle (round `radius-full` ring with `ash` border on `ink`)
        rad_i = Image.new('RGBA', (27, h), (0, 0, 0, 0))
        ImageDraw.Draw(rad_i).ellipse([4, mid - 9, 22, mid + 9], fill=INK, outline=ASH, width=1)
        save_asset(rad_i, f'{sub}/radio_foreground.png')

        # Radio Selected (double ring motif: `glow` outer, `ember` inner, `glow-core` seed dot)
        rad_s = Image.new('RGBA', (27, h), (0, 0, 0, 0))
        rs_draw = ImageDraw.Draw(rad_s)
        rs_draw.ellipse([4, mid - 9, 22, mid + 9], fill=INK, outline=GLOW, width=2)
        rs_draw.ellipse([7, mid - 6, 19, mid + 6], outline=EMBER, width=1)
        rs_draw.ellipse([10, mid - 3, 16, mid + 3], fill=GLOW)
        save_asset(rad_s, f'{sub}/radio_selected_foreground.png')


# -------------------------------------------------------------------------
# 7. Sliders, Scrollbars & Bars (Square `radius-0` tracks)
# -------------------------------------------------------------------------
def generate_bars():
    print("--- Generating Bars, Sliders & Scrollbars ---")
    for h, sub in [(38, 'slider'), (54, 'phone/slider')]:
        mid = h // 2
        # Idle Bar
        sb_i = Image.new('RGBA', (525, h), (0, 0, 0, 0))
        ImageDraw.Draw(sb_i).rectangle([2, mid - 6, 522, mid + 6], fill=CHAR, outline=ASH, width=1)
        save_asset(sb_i, f'{sub}/horizontal_idle_bar.png')

        # Hover Bar
        sb_h = Image.new('RGBA', (525, h), (0, 0, 0, 0))
        ImageDraw.Draw(sb_h).rectangle([2, mid - 6, 522, mid + 6], fill=PANEL, outline=SAND, width=1)
        save_asset(sb_h, f'{sub}/horizontal_hover_bar.png')

    # Horizontal Slider Thumbs (Square `radius-0`)
    th_i = Image.new('RGBA', (15, 38), (0, 0, 0, 0))
    ImageDraw.Draw(th_i).rectangle([1, 4, 13, 33], fill=CLAY, outline=FLAME, width=1)
    save_asset(th_i, 'slider/horizontal_idle_thumb.png')

    th_h = Image.new('RGBA', (15, 38), (0, 0, 0, 0))
    ImageDraw.Draw(th_h).rectangle([1, 2, 13, 35], fill=GLOW, outline=GLOW_CORE, width=1)
    save_asset(th_h, 'slider/horizontal_hover_thumb.png')

    th_ip = Image.new('RGBA', (22, 54), (0, 0, 0, 0))
    ImageDraw.Draw(th_ip).rectangle([2, 5, 19, 48], fill=CLAY, outline=FLAME, width=1)
    save_asset(th_ip, 'phone/slider/horizontal_idle_thumb.png')

    th_hp = Image.new('RGBA', (22, 54), (0, 0, 0, 0))
    ImageDraw.Draw(th_hp).rectangle([2, 3, 19, 50], fill=GLOW, outline=GLOW_CORE, width=1)
    save_asset(th_hp, 'phone/slider/horizontal_hover_thumb.png')

    # Vertical Slider Bars & Thumbs
    vb_i = Image.new('RGBA', (38, 525), (0, 0, 0, 0))
    ImageDraw.Draw(vb_i).rectangle([13, 2, 25, 522], fill=CHAR, outline=ASH, width=1)
    save_asset(vb_i, 'slider/vertical_idle_bar.png')

    vb_h = Image.new('RGBA', (38, 525), (0, 0, 0, 0))
    ImageDraw.Draw(vb_h).rectangle([13, 2, 25, 522], fill=PANEL, outline=SAND, width=1)
    save_asset(vb_h, 'slider/vertical_hover_bar.png')

    vth_i = Image.new('RGBA', (38, 15), (0, 0, 0, 0))
    ImageDraw.Draw(vth_i).rectangle([4, 1, 33, 13], fill=CLAY, outline=FLAME, width=1)
    save_asset(vth_i, 'slider/vertical_idle_thumb.png')

    vth_h = Image.new('RGBA', (38, 15), (0, 0, 0, 0))
    ImageDraw.Draw(vth_h).rectangle([2, 1, 35, 13], fill=GLOW, outline=GLOW_CORE, width=1)
    save_asset(vth_h, 'slider/vertical_hover_thumb.png')

    # Scrollbars (1050 x 18 horizontal, 18 x 1050 vertical)
    for sub in ['scrollbar', 'phone/scrollbar']:
        # Horizontal
        hsc_b = Image.new('RGBA', (1050, 18), (0, 0, 0, 0))
        ImageDraw.Draw(hsc_b).rectangle([0, 3, 1049, 14], fill=CHAR, outline=SAND, width=1)
        save_asset(hsc_b, f'{sub}/horizontal_idle_bar.png')
        save_asset(hsc_b, f'{sub}/horizontal_hover_bar.png')

        hsc_th = Image.new('RGBA', (1050, 18), (0, 0, 0, 0))
        ImageDraw.Draw(hsc_th).rectangle([2, 4, 1047, 13], fill=CLAY)
        save_asset(hsc_th, f'{sub}/horizontal_idle_thumb.png')

        hsc_thh = Image.new('RGBA', (1050, 18), (0, 0, 0, 0))
        ImageDraw.Draw(hsc_thh).rectangle([2, 3, 1047, 14], fill=GLOW)
        save_asset(hsc_thh, f'{sub}/horizontal_hover_thumb.png')

        # Vertical
        vsc_b = Image.new('RGBA', (18, 1050), (0, 0, 0, 0))
        ImageDraw.Draw(vsc_b).rectangle([3, 0, 14, 1049], fill=CHAR, outline=SAND, width=1)
        save_asset(vsc_b, f'{sub}/vertical_idle_bar.png')
        save_asset(vsc_b, f'{sub}/vertical_hover_bar.png')

        vsc_th = Image.new('RGBA', (18, 1050), (0, 0, 0, 0))
        ImageDraw.Draw(vsc_th).rectangle([4, 2, 13, 1047], fill=CLAY)
        save_asset(vsc_th, f'{sub}/vertical_idle_thumb.png')

        vsc_thh = Image.new('RGBA', (18, 1050), (0, 0, 0, 0))
        ImageDraw.Draw(vsc_thh).rectangle([3, 2, 14, 1047], fill=GLOW)
        save_asset(vsc_thh, f'{sub}/vertical_hover_thumb.png')

    # Progress Bar left / right (525 x 38) - Square (`radius-0`)
    for sub in ['bar', 'phone/bar']:
        # left = filled portion (`clay` fill with `glow` border)
        b_left = Image.new('RGBA', (525, 38), (0, 0, 0, 0))
        ImageDraw.Draw(b_left).rectangle([2, 4, 522, 33], fill=CLAY, outline=GLOW, width=1)
        save_asset(b_left, f'{sub}/left.png')

        # right = empty track (`char` fill with `ash` border)
        b_right = Image.new('RGBA', (525, 38), (0, 0, 0, 0))
        ImageDraw.Draw(b_right).rectangle([2, 4, 522, 33], fill=CHAR, outline=ASH, width=1)
        save_asset(b_right, f'{sub}/right.png')

        # top / bottom vertical
        b_top = Image.new('RGBA', (38, 525), (0, 0, 0, 0))
        ImageDraw.Draw(b_top).rectangle([4, 2, 33, 522], fill=CLAY, outline=GLOW, width=1)
        save_asset(b_top, f'{sub}/top.png')

        b_bot = Image.new('RGBA', (38, 525), (0, 0, 0, 0))
        ImageDraw.Draw(b_bot).rectangle([4, 2, 33, 522], fill=CHAR, outline=ASH, width=1)
        save_asset(b_bot, f'{sub}/bottom.png')


# -------------------------------------------------------------------------
# 8. Window Icon (250 x 250) - NodeCard Double Ring Motif
# -------------------------------------------------------------------------
def generate_window_icon():
    print("--- Generating Window Icon ---")
    IW, IH = 250, 250
    icon = Image.new('RGBA', (IW, IH), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(icon)
    # Double ring (`glow` outer, `ember` inner) on `ink` (#140702) ground
    i_draw.ellipse([6, 6, IW - 7, IH - 7], fill=INK, outline=GLOW, width=3)
    i_draw.ellipse([16, 16, IW - 17, IH - 17], outline=EMBER, width=2)

    # Aperture arch motif inside the node ring (from Cover/preview.html)
    mid_x, mid_y = IW // 2, IH // 2
    i_draw.pieslice([mid_x - 42, mid_y - 48, mid_x + 42, mid_y + 36], start=180, end=360, fill=GLOW)
    i_draw.rectangle([mid_x - 42, mid_y - 6, mid_x + 42, mid_y + 52], fill=GLOW)
    i_draw.pieslice([mid_x - 16, mid_y + 4, mid_x + 16, mid_y + 36], start=180, end=360, fill=GLOW_CORE)
    i_draw.rectangle([mid_x - 16, mid_y + 20, mid_x + 16, mid_y + 52], fill=GLOW_CORE)

    save_asset(icon, 'window_icon.png')


if __name__ == '__main__':
    generate_menus()
    generate_overlays()
    generate_textbox()
    generate_choice_buttons()
    generate_frames()
    generate_buttons()
    generate_bars()
    generate_window_icon()
    print("All DAOcubator design-system GUI assets generated and deployed successfully!")
