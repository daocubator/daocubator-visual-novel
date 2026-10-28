#!/usr/bin/env python3
"""
Generate complete high-fidelity GUI assets for Get Rich Together
matching Asya Abdrahman's mixed-media fine-art visual direction:
- Deep midnight obsidian blue glass (#0A1120 / #080D18)
- Distressed gold leaf and PCB circuit filament line work (#D4AF37, #F3E5AB, #9A7E32)
- Cyan tech node highlights (#55FFFF, #00AAAA)
- Crisp 9-slice sliceable geometry for Ren'Py frames, buttons, sliders, and textboxes
"""

import os
import math
import shutil
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance

# -------------------------------------------------------------------------
# Directories
# -------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GUI_DIR = os.path.join(BASE_DIR, 'game', 'gui')
VAULT_GUI_DIR = os.path.join(BASE_DIR, 'vault', '06 Assets', 'generated_gui')
MAIN_MENU_SOURCE = r"C:\Users\kwhyc\.gemini\antigravity\brain\f33b4088-2607-477b-bf17-4d27ec1b08cf\main_menu_art_1791587962829.jpg"

os.makedirs(VAULT_GUI_DIR, exist_ok=True)
for sub in ['', 'button', 'overlay', 'phone', 'phone/button', 'phone/overlay',
            'phone/scrollbar', 'phone/slider', 'phone/bar',
            'scrollbar', 'slider', 'bar']:
    os.makedirs(os.path.join(GUI_DIR, sub), exist_ok=True)
    os.makedirs(os.path.join(VAULT_GUI_DIR, sub), exist_ok=True)

# -------------------------------------------------------------------------
# Color Palette
# -------------------------------------------------------------------------
GOLD_BRIGHT   = (243, 229, 171, 255) # #F3E5AB champagne
GOLD_LEAF     = (212, 175, 55, 255)  # #D4AF37 classic gold
GOLD_ANTIQUE  = (154, 126, 50, 255)  # #9A7E32 dark bronze gold
GOLD_GLOW     = (255, 215, 0, 80)    # soft halo
CYAN_ACCENT   = (85, 255, 255, 255)  # #55FFFF
CYAN_TEAL     = (0, 170, 170, 255)   # #00AAAA

BG_DARK_GLASS = (10, 17, 32, 225)    # deep midnight blue glass
BG_DARKER     = (7, 12, 22, 240)     # darker base
BG_HOVER      = (22, 38, 64, 245)    # active hover fill
BG_SLATE      = (18, 28, 48, 220)

# Helper to save to both GUI_DIR and VAULT_GUI_DIR
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
    if os.path.exists(MAIN_MENU_SOURCE):
        src = Image.open(MAIN_MENU_SOURCE).convert('RGB')
        # Scale to 1920x1080 Lanczos
        main_menu = src.resize((1920, 1080), Image.Resampling.LANCZOS).convert('RGBA')

        # Add left gradient scrim for main menu navigation readability
        scrim = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
        scrim_draw = ImageDraw.Draw(scrim)
        for x in range(750):
            # Alpha ramps from 170 down to 0
            factor = (1.0 - (x / 750.0)) ** 1.5
            alpha = int(170 * factor)
            scrim_draw.line([(x, 0), (x, 1080)], fill=(6, 10, 18, alpha))
        
        main_menu_final = Image.alpha_composite(main_menu, scrim)
        save_asset(main_menu_final, 'main_menu.png')

        # Game Menu: Atmospheric, darker companion with subtle gold circuit framing
        # Start from main_menu art, darken center significantly, enhance blue tone
        game_menu = main_menu.copy().convert('RGB')
        enhancer = ImageEnhance.Brightness(game_menu)
        game_menu = enhancer.enhance(0.38) # dark base
        game_menu = game_menu.convert('RGBA')

        # Add vignette and subtle gold circuit lines
        vignette = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
        v_draw = ImageDraw.Draw(vignette)
        # Gradient from corners
        for x in range(1920):
            # Darken center to ensure high data contrast
            dx = abs(x - 960) / 960.0
            col_a = int(140 * (1.0 - dx * 0.5))
            v_draw.line([(x, 0), (x, 1080)], fill=(5, 9, 16, col_a))
        
        game_menu = Image.alpha_composite(game_menu, vignette)
        
        # Subtle perimeter gold circuit lines on game_menu
        gm_draw = ImageDraw.Draw(game_menu)
        gm_draw.rectangle([20, 20, 1899, 1059], outline=(154, 126, 50, 90), width=1)
        gm_draw.rectangle([24, 24, 1895, 1055], outline=(212, 175, 55, 60), width=1)
        # Corner brackets
        corner_len = 60
        for cx, cy, sign_x, sign_y in [(20, 20, 1, 1), (1899, 20, -1, 1), (20, 1059, 1, -1), (1899, 1059, -1, -1)]:
            gm_draw.line([(cx, cy), (cx + sign_x * corner_len, cy)], fill=(243, 229, 171, 180), width=2)
            gm_draw.line([(cx, cy), (cx, cy + sign_y * corner_len)], fill=(243, 229, 171, 180), width=2)
            gm_draw.ellipse([cx + sign_x * 8 - 3, cy + sign_y * 8 - 3, cx + sign_x * 8 + 3, cy + sign_y * 8 + 3], fill=(243, 229, 171, 200))

        save_asset(game_menu, 'game_menu.png')
        save_asset(game_menu, 'nvl.png')
        save_asset(game_menu, 'phone/nvl.png')
    else:
        print(f"WARNING: {MAIN_MENU_SOURCE} not found!")

# -------------------------------------------------------------------------
# 2. Overlays
# -------------------------------------------------------------------------
def generate_overlays():
    print("--- Generating Overlays ---")
    # main_menu overlay: soft dark gradient
    mm_ov = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    save_asset(mm_ov, 'overlay/main_menu.png')
    save_asset(mm_ov, 'phone/overlay/main_menu.png')

    # game_menu overlay: rich dark glass tint
    gm_ov = Image.new('RGBA', (1920, 1080), (6, 11, 20, 175))
    save_asset(gm_ov, 'overlay/game_menu.png')
    save_asset(gm_ov, 'phone/overlay/game_menu.png')

    # confirm modal overlay: deeper backdrop
    conf_ov = Image.new('RGBA', (1920, 1080), (4, 7, 14, 215))
    save_asset(conf_ov, 'overlay/confirm.png')

# -------------------------------------------------------------------------
# 3. Dialogue Textbox & Namebox
# -------------------------------------------------------------------------
def generate_textbox():
    print("--- Generating Textbox & Namebox ---")
    # Standard desktop textbox: 1920 x 277
    W, H = 1920, 277
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # Base background gradient (y=0 to H)
    for y in range(H):
        t = y / float(H)
        # Deep midnight blue glass: top 220 alpha, bottom 245 alpha
        r = int(10 * (1 - t) + 6 * t)
        g = int(17 * (1 - t) + 10 * t)
        b = int(32 * (1 - t) + 20 * t)
        a = int(218 * (1 - t) + 248 * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b, a))

    # Top border gold line
    draw.line([(0, 0), (W, 0)], fill=GOLD_ANTIQUE, width=1)
    draw.line([(0, 1), (W, 1)], fill=GOLD_LEAF, width=1)
    draw.line([(0, 2), (W, 2)], fill=GOLD_BRIGHT, width=1)
    draw.line([(0, 3), (W, 3)], fill=(212, 175, 55, 90), width=1)

    # Decorative gold PCB circuit traces along top edge
    # Left side circuit trace
    draw.line([(60, 14), (240, 14)], fill=GOLD_ANTIQUE, width=1)
    draw.line([(240, 14), (254, 28)], fill=GOLD_ANTIQUE, width=1)
    draw.line([(254, 28), (420, 28)], fill=GOLD_ANTIQUE, width=1)
    # Node circles
    draw.ellipse([58, 12, 64, 18], fill=GOLD_BRIGHT)
    draw.ellipse([418, 26, 424, 32], fill=GOLD_BRIGHT)

    # Right side circuit trace
    draw.line([(W - 60, 14), (W - 240, 14)], fill=GOLD_ANTIQUE, width=1)
    # Far left side circuit trace (confined to margins, away from namebox at x=360)
    draw.line([(40, 14), (180, 14)], fill=GOLD_ANTIQUE, width=1)
    draw.line([(180, 14), (194, 28)], fill=GOLD_ANTIQUE, width=1)
    draw.line([(194, 28), (250, 28)], fill=GOLD_ANTIQUE, width=1)
    draw.ellipse([38, 12, 44, 18], fill=GOLD_BRIGHT)
    draw.ellipse([248, 26, 254, 32], fill=GOLD_BRIGHT)

    # Far right side circuit trace
    draw.line([(W - 40, 14), (W - 180, 14)], fill=GOLD_ANTIQUE, width=1)
    draw.line([(W - 180, 14), (W - 194, 28)], fill=GOLD_ANTIQUE, width=1)
    draw.line([(W - 194, 28), (W - 250, 28)], fill=GOLD_ANTIQUE, width=1)
    draw.ellipse([W - 44, 12, W - 38, 18], fill=GOLD_BRIGHT)
    draw.ellipse([W - 254, 26, W - 248, 32], fill=GOLD_BRIGHT)

    # Soft glowing cyan sub-trace
    draw.line([(60, 28), (140, 28)], fill=(85, 255, 255, 120), width=1)
    draw.line([(W - 140, 28), (W - 60, 28)], fill=(85, 255, 255, 120), width=1)

    save_asset(im, 'textbox.png')

    # Phone textbox (1920 x 360)
    H_phone = 360
    im_phone = Image.new('RGBA', (W, H_phone), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(im_phone)
    for y in range(H_phone):
        t = y / float(H_phone)
        r = int(10 * (1 - t) + 6 * t)
        g = int(17 * (1 - t) + 10 * t)
        b = int(32 * (1 - t) + 20 * t)
        a = int(225 * (1 - t) + 250 * t)
        p_draw.line([(0, y), (W, y)], fill=(r, g, b, a))
    p_draw.line([(0, 0), (W, 0)], fill=GOLD_ANTIQUE, width=1)
    p_draw.line([(0, 1), (W, 1)], fill=GOLD_LEAF, width=2)
    p_draw.line([(0, 3), (W, 3)], fill=GOLD_BRIGHT, width=1)
    save_asset(im_phone, 'phone/textbox.png')

    # Namebox (450 x 54)
    # Raised gold plaque with chamfered corners, clean interior (no dots)
    NW, NH = 450, 54
    nb = Image.new('RGBA', (NW, NH), (0, 0, 0, 0))
    n_draw = ImageDraw.Draw(nb)

    # Polygon with chamfered top corners
    pts = [(8, 0), (NW - 9, 0), (NW - 1, 8), (NW - 1, NH - 1), (0, NH - 1), (0, 8)]
    n_draw.polygon(pts, fill=(12, 21, 38, 240))
    # Crisp gold borders
    n_draw.line([(8, 0), (NW - 9, 0)], fill=GOLD_BRIGHT, width=2)
    n_draw.line([(NW - 9, 0), (NW - 1, 8)], fill=GOLD_LEAF, width=2)
    n_draw.line([(NW - 1, 8), (NW - 1, NH - 1)], fill=GOLD_ANTIQUE, width=1)
    n_draw.line([(NW - 1, NH - 1), (0, NH - 1)], fill=GOLD_ANTIQUE, width=1)
    n_draw.line([(0, NH - 1), (0, 8)], fill=GOLD_ANTIQUE, width=1)
    n_draw.line([(0, 8), (8, 0)], fill=GOLD_LEAF, width=2)

    save_asset(nb, 'namebox.png')

# -------------------------------------------------------------------------
# 4. Choice Buttons
# -------------------------------------------------------------------------
def generate_choice_buttons():
    print("--- Generating Choice Buttons ---")
    CW, CH = 1185, 52

    # Choice Idle
    idle = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(idle)
    # 45-degree chamfers on all 4 corners: 6px
    c = 7
    poly = [(c, 0), (CW - 1 - c, 0), (CW - 1, c), (CW - 1, CH - 1 - c),
            (CW - 1 - c, CH - 1), (c, CH - 1), (0, CH - 1 - c), (0, c)]
    draw.polygon(poly, fill=(11, 20, 36, 225))
    # Antique gold border
    draw.polygon(poly, outline=GOLD_ANTIQUE, width=1)
    # Left and right circuit brackets
    draw.line([(24, 12), (14, 12), (14, CH - 13), (24, CH - 13)], fill=GOLD_LEAF, width=1)
    draw.line([(CW - 25, 12), (CW - 15, 12), (CW - 15, CH - 13), (CW - 25, CH - 13)], fill=GOLD_LEAF, width=1)
    # Small gold nodes
    draw.ellipse([27, CH // 2 - 2, 31, CH // 2 + 2], fill=GOLD_LEAF)
    draw.ellipse([CW - 32, CH // 2 - 2, CW - 28, CH // 2 + 2], fill=GOLD_LEAF)

    save_asset(idle, 'button/choice_idle_background.png')
    save_asset(idle, 'phone/button/choice_idle_background.png')

    # Choice Hover (glowing gold & navy with cyan accent)
    hover = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hover)
    h_draw.polygon(poly, fill=(22, 38, 66, 250))
    # Double gold border with bright highlight
    h_draw.polygon(poly, outline=GOLD_BRIGHT, width=2)
    # Radiant brackets
    h_draw.line([(26, 10), (12, 10), (12, CH - 11), (26, CH - 11)], fill=GOLD_BRIGHT, width=2)
    h_draw.line([(CW - 27, 10), (CW - 13, 10), (CW - 13, CH - 11), (CW - 27, CH - 11)], fill=GOLD_BRIGHT, width=2)
    # Glowing diamond on left and right
    mid_y = CH // 2
    h_draw.polygon([(30, mid_y - 4), (34, mid_y), (30, mid_y + 4), (26, mid_y)], fill=(255, 215, 0, 255))
    h_draw.polygon([(CW - 31, mid_y - 4), (CW - 27, mid_y), (CW - 31, mid_y + 4), (CW - 35, mid_y)], fill=(255, 215, 0, 255))
    # Subtle cyan node accents
    h_draw.point((42, mid_y), fill=CYAN_ACCENT)
    h_draw.point((CW - 43, mid_y), fill=CYAN_ACCENT)

    save_asset(hover, 'button/choice_hover_background.png')
    save_asset(hover, 'phone/button/choice_hover_background.png')

# -------------------------------------------------------------------------
# 5. Frames & Modals (frame.png, notify.png, skip.png, bubbles)
# -------------------------------------------------------------------------
def generate_frames():
    print("--- Generating Frames ---")
    # frame.png (900 x 375, 9-slice)
    FW, FH = 900, 375
    fr = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fr)
    c = 10
    poly = [(c, 0), (FW - 1 - c, 0), (FW - 1, c), (FW - 1, FH - 1 - c),
            (FW - 1 - c, FH - 1), (c, FH - 1), (0, FH - 1 - c), (0, c)]
    draw.polygon(poly, fill=(10, 16, 29, 235))
    draw.polygon(poly, outline=GOLD_ANTIQUE, width=1)
    # Inner border
    inner_poly = [(c + 3, 3), (FW - 4 - c, 3), (FW - 4, c + 3), (FW - 4, FH - 4 - c),
                  (FW - 4 - c, FH - 4), (c + 3, FH - 4), (3, FH - 4 - c), (3, c + 3)]
    draw.polygon(inner_poly, outline=GOLD_LEAF, width=1)

    # 4 Corner PCB pads with nodes
    for cx, cy, sx, sy in [(14, 14, 1, 1), (FW - 15, 14, -1, 1), (14, FH - 15, 1, -1), (FW - 15, FH - 15, -1, -1)]:
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=GOLD_BRIGHT)
        draw.line([(cx, cy), (cx + sx * 16, cy)], fill=GOLD_ANTIQUE, width=1)
        draw.line([(cx, cy), (cx, cy + sy * 16)], fill=GOLD_ANTIQUE, width=1)

    save_asset(fr, 'frame.png')

    # notify.png (1383 x 64)
    # Clean chamfered dark glass banner with gold border — NO interior crossing lines
    NW, NH = 1383, 64
    notif = Image.new('RGBA', (NW, NH), (0, 0, 0, 0))
    n_draw = ImageDraw.Draw(notif)
    c = 8
    poly = [(c, 0), (NW - 1 - c, 0), (NW - 1, c), (NW - 1, NH - 1 - c),
            (NW - 1 - c, NH - 1), (c, NH - 1), (0, NH - 1 - c), (0, c)]
    n_draw.polygon(poly, fill=(12, 22, 38, 240))
    n_draw.polygon(poly, outline=GOLD_LEAF, width=1)
    # Subtle inner corner bevel highlight (strictly at the outer edge, no crossing lines)
    n_draw.line([(c, 1), (c + 8, 1)], fill=GOLD_BRIGHT, width=1)
    n_draw.line([(NW - 1 - c - 8, 1), (NW - 1 - c, 1)], fill=GOLD_BRIGHT, width=1)
    save_asset(notif, 'notify.png')

    # skip.png (360 x 64)
    SW, SH = 360, 64
    sk = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk)
    poly = [(c, 0), (SW - 1 - c, 0), (SW - 1, c), (SW - 1, SH - 1 - c),
            (SW - 1 - c, SH - 1), (c, SH - 1), (0, SH - 1 - c), (0, c)]
    s_draw.polygon(poly, fill=(14, 24, 42, 245))
    s_draw.polygon(poly, outline=GOLD_BRIGHT, width=1)
    save_asset(sk, 'skip.png')

    # speech bubble / thought bubble (200 x 155, 200 x 133)
    for bname, bw, bh in [('bubble.png', 200, 155), ('thoughtbubble.png', 200, 133)]:
        b_im = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        b_draw = ImageDraw.Draw(b_im)
        b_draw.rounded_rectangle([4, 4, bw - 5, bh - 5], radius=12, fill=(12, 21, 36, 235), outline=GOLD_LEAF, width=2)
        save_asset(b_im, bname)

# -------------------------------------------------------------------------
# 6. Save/Load Slots and Navigation Buttons
# -------------------------------------------------------------------------
def generate_buttons():
    print("--- Generating Buttons ---")
    # Slot Buttons (414 x 309)
    # Clean 9-slice card: NO dividing lines, NO interior dots across content
    SW, SH = 414, 309
    c = 8
    poly = [(c, 0), (SW - 1 - c, 0), (SW - 1, c), (SW - 1, SH - 1 - c),
            (SW - 1 - c, SH - 1), (c, SH - 1), (0, SH - 1 - c), (0, c)]
    
    # Slot Idle
    s_idle = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
    d_idle = ImageDraw.Draw(s_idle)
    d_idle.polygon(poly, fill=(9, 15, 26, 220))
    d_idle.polygon(poly, outline=GOLD_ANTIQUE, width=1)
    save_asset(s_idle, 'button/slot_idle_background.png')
    save_asset(s_idle, 'phone/button/slot_idle_background.png')

    # Slot Hover
    s_hover = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
    d_hover = ImageDraw.Draw(s_hover)
    d_hover.polygon(poly, fill=(18, 30, 52, 245))
    d_hover.polygon(poly, outline=GOLD_BRIGHT, width=2)
    save_asset(s_hover, 'button/slot_hover_background.png')
    save_asset(s_hover, 'phone/button/slot_hover_background.png')

    # General Button (450 x 49)
    BW, BH = 450, 49
    b_poly = [(6, 0), (BW - 7, 0), (BW - 1, 6), (BW - 1, BH - 7),
              (BW - 7, BH - 1), (6, BH - 1), (0, BH - 7), (0, 6)]
    
    b_idle = Image.new('RGBA', (BW, BH), (0, 0, 0, 0))
    bi_draw = ImageDraw.Draw(b_idle)
    bi_draw.polygon(b_poly, fill=(10, 18, 32, 210))
    bi_draw.polygon(b_poly, outline=GOLD_ANTIQUE, width=1)
    save_asset(b_idle, 'button/idle_background.png')

    b_hover = Image.new('RGBA', (BW, BH), (0, 0, 0, 0))
    bh_draw = ImageDraw.Draw(b_hover)
    bh_draw.polygon(b_poly, fill=(20, 35, 60, 240))
    bh_draw.polygon(b_poly, outline=GOLD_BRIGHT, width=2)
    save_asset(b_hover, 'button/hover_background.png')

    # Phone buttons (450 x 64)
    BH_p = 64
    bp_poly = [(6, 0), (BW - 7, 0), (BW - 1, 6), (BW - 1, BH_p - 7),
               (BW - 7, BH_p - 1), (6, BH_p - 1), (0, BH_p - 7), (0, 6)]
    bp_idle = Image.new('RGBA', (BW, BH_p), (0, 0, 0, 0))
    ImageDraw.Draw(bp_idle).polygon(bp_poly, fill=(10, 18, 32, 210), outline=GOLD_ANTIQUE, width=1)
    save_asset(bp_idle, 'phone/button/idle_background.png')

    bp_hover = Image.new('RGBA', (BW, BH_p), (0, 0, 0, 0))
    ImageDraw.Draw(bp_hover).polygon(bp_poly, fill=(20, 35, 60, 240), outline=GOLD_BRIGHT, width=2)
    save_asset(bp_hover, 'phone/button/hover_background.png')

    # Quick menu buttons (150 x 45)
    QW, QH = 150, 45
    q_idle = Image.new('RGBA', (QW, QH), (0, 0, 0, 0))
    ImageDraw.Draw(q_idle).rounded_rectangle([2, 2, QW - 3, QH - 3], radius=4, fill=(8, 14, 25, 190), outline=GOLD_ANTIQUE, width=1)
    save_asset(q_idle, 'button/quick_idle_background.png')

    q_hover = Image.new('RGBA', (QW, QH), (0, 0, 0, 0))
    ImageDraw.Draw(q_hover).rounded_rectangle([2, 2, QW - 3, QH - 3], radius=4, fill=(18, 32, 54, 240), outline=GOLD_BRIGHT, width=1)
    save_asset(q_hover, 'button/quick_hover_background.png')

    # Checkboxes & Radios (27 x 49 desktop, 27 x 64 phone)
    for h, sub in [(49, 'button'), (64, 'phone/button')]:
        mid = h // 2
        # Check Idle
        chk_i = Image.new('RGBA', (27, h), (0, 0, 0, 0))
        ImageDraw.Draw(chk_i).rectangle([4, mid - 9, 22, mid + 9], fill=(10, 17, 30, 230), outline=GOLD_ANTIQUE, width=1)
        save_asset(chk_i, f'{sub}/check_foreground.png')

        # Check Selected
        chk_s = Image.new('RGBA', (27, h), (0, 0, 0, 0))
        cs_draw = ImageDraw.Draw(chk_s)
        cs_draw.rectangle([4, mid - 9, 22, mid + 9], fill=(16, 28, 50, 240), outline=GOLD_BRIGHT, width=2)
        # Gold checkmark
        cs_draw.line([(8, mid), (12, mid + 4), (18, mid - 4)], fill=GOLD_BRIGHT, width=2)
        save_asset(chk_s, f'{sub}/check_selected_foreground.png')

        # Radio Idle
        rad_i = Image.new('RGBA', (27, h), (0, 0, 0, 0))
        ImageDraw.Draw(rad_i).ellipse([4, mid - 9, 22, mid + 9], fill=(10, 17, 30, 230), outline=GOLD_ANTIQUE, width=1)
        save_asset(rad_i, f'{sub}/radio_foreground.png')

        # Radio Selected
        rad_s = Image.new('RGBA', (27, h), (0, 0, 0, 0))
        rs_draw = ImageDraw.Draw(rad_s)
        rs_draw.ellipse([4, mid - 9, 22, mid + 9], fill=(16, 28, 50, 240), outline=GOLD_BRIGHT, width=2)
        rs_draw.ellipse([9, mid - 4, 17, mid + 4], fill=GOLD_BRIGHT)
        save_asset(rad_s, f'{sub}/radio_selected_foreground.png')

# -------------------------------------------------------------------------
# 7. Sliders, Scrollbars & Bars
# -------------------------------------------------------------------------
def generate_bars():
    print("--- Generating Bars, Sliders & Scrollbars ---")
    # Horizontal Slider Bars (525 x 38 desktop, 525 x 54 phone)
    for h, sub in [(38, 'slider'), (54, 'phone/slider')]:
        mid = h // 2
        # Idle Bar
        sb_i = Image.new('RGBA', (525, h), (0, 0, 0, 0))
        ImageDraw.Draw(sb_i).rounded_rectangle([2, mid - 6, 522, mid + 6], radius=3, fill=(12, 20, 36, 230), outline=GOLD_ANTIQUE, width=1)
        save_asset(sb_i, f'{sub}/horizontal_idle_bar.png')

        # Hover Bar (glowing gold accent)
        sb_h = Image.new('RGBA', (525, h), (0, 0, 0, 0))
        ImageDraw.Draw(sb_h).rounded_rectangle([2, mid - 6, 522, mid + 6], radius=3, fill=(18, 30, 52, 240), outline=GOLD_LEAF, width=1)
        save_asset(sb_h, f'{sub}/horizontal_hover_bar.png')

    # Horizontal Slider Thumbs
    # Desktop: 15 x 38; Phone: 22 x 54
    th_i = Image.new('RGBA', (15, 38), (0, 0, 0, 0))
    ImageDraw.Draw(th_i).rounded_rectangle([1, 4, 13, 33], radius=4, fill=GOLD_LEAF, outline=GOLD_BRIGHT, width=1)
    save_asset(th_i, 'slider/horizontal_idle_thumb.png')

    th_h = Image.new('RGBA', (15, 38), (0, 0, 0, 0))
    ImageDraw.Draw(th_h).rounded_rectangle([1, 2, 13, 35], radius=4, fill=GOLD_BRIGHT, outline=(255, 255, 255, 255), width=1)
    save_asset(th_h, 'slider/horizontal_hover_thumb.png')

    th_ip = Image.new('RGBA', (22, 54), (0, 0, 0, 0))
    ImageDraw.Draw(th_ip).rounded_rectangle([2, 5, 19, 48], radius=5, fill=GOLD_LEAF, outline=GOLD_BRIGHT, width=1)
    save_asset(th_ip, 'phone/slider/horizontal_idle_thumb.png')

    th_hp = Image.new('RGBA', (22, 54), (0, 0, 0, 0))
    ImageDraw.Draw(th_hp).rounded_rectangle([2, 3, 19, 50], radius=5, fill=GOLD_BRIGHT, outline=(255, 255, 255, 255), width=1)
    save_asset(th_hp, 'phone/slider/horizontal_hover_thumb.png')

    # Vertical Slider Bars & Thumbs
    vb_i = Image.new('RGBA', (38, 525), (0, 0, 0, 0))
    ImageDraw.Draw(vb_i).rounded_rectangle([13, 2, 25, 522], radius=3, fill=(12, 20, 36, 230), outline=GOLD_ANTIQUE, width=1)
    save_asset(vb_i, 'slider/vertical_idle_bar.png')

    vb_h = Image.new('RGBA', (38, 525), (0, 0, 0, 0))
    ImageDraw.Draw(vb_h).rounded_rectangle([13, 2, 25, 522], radius=3, fill=(18, 30, 52, 240), outline=GOLD_LEAF, width=1)
    save_asset(vb_h, 'slider/vertical_hover_bar.png')

    vth_i = Image.new('RGBA', (38, 15), (0, 0, 0, 0))
    ImageDraw.Draw(vth_i).rounded_rectangle([4, 1, 33, 13], radius=4, fill=GOLD_LEAF, outline=GOLD_BRIGHT, width=1)
    save_asset(vth_i, 'slider/vertical_idle_thumb.png')

    vth_h = Image.new('RGBA', (38, 15), (0, 0, 0, 0))
    ImageDraw.Draw(vth_h).rounded_rectangle([2, 1, 35, 13], radius=4, fill=GOLD_BRIGHT, outline=(255, 255, 255, 255), width=1)
    save_asset(vth_h, 'slider/vertical_hover_thumb.png')

    # Scrollbars (1050 x 18 horizontal, 18 x 1050 vertical)
    for sub in ['scrollbar', 'phone/scrollbar']:
        # Horizontal
        hsc_b = Image.new('RGBA', (1050, 18), (0, 0, 0, 0))
        ImageDraw.Draw(hsc_b).rectangle([0, 3, 1049, 14], fill=(9, 15, 27, 210), outline=GOLD_ANTIQUE, width=1)
        save_asset(hsc_b, f'{sub}/horizontal_idle_bar.png')
        save_asset(hsc_b, f'{sub}/horizontal_hover_bar.png')

        hsc_th = Image.new('RGBA', (1050, 18), (0, 0, 0, 0))
        ImageDraw.Draw(hsc_th).rounded_rectangle([2, 4, 1047, 13], radius=3, fill=GOLD_ANTIQUE)
        save_asset(hsc_th, f'{sub}/horizontal_idle_thumb.png')

        hsc_thh = Image.new('RGBA', (1050, 18), (0, 0, 0, 0))
        ImageDraw.Draw(hsc_thh).rounded_rectangle([2, 3, 1047, 14], radius=3, fill=GOLD_BRIGHT)
        save_asset(hsc_thh, f'{sub}/horizontal_hover_thumb.png')

        # Vertical
        vsc_b = Image.new('RGBA', (18, 1050), (0, 0, 0, 0))
        ImageDraw.Draw(vsc_b).rectangle([3, 0, 14, 1049], fill=(9, 15, 27, 210), outline=GOLD_ANTIQUE, width=1)
        save_asset(vsc_b, f'{sub}/vertical_idle_bar.png')
        save_asset(vsc_b, f'{sub}/vertical_hover_bar.png')

        vsc_th = Image.new('RGBA', (18, 1050), (0, 0, 0, 0))
        ImageDraw.Draw(vsc_th).rounded_rectangle([4, 2, 13, 1047], radius=3, fill=GOLD_ANTIQUE)
        save_asset(vsc_th, f'{sub}/vertical_idle_thumb.png')

        vsc_thh = Image.new('RGBA', (18, 1050), (0, 0, 0, 0))
        ImageDraw.Draw(vsc_thh).rounded_rectangle([3, 2, 14, 1047], radius=3, fill=GOLD_BRIGHT)
        save_asset(vsc_thh, f'{sub}/vertical_hover_thumb.png')

    # Progress Bar left / right (525 x 38)
    for sub in ['bar', 'phone/bar']:
        # left = filled portion (warm gold gradient)
        b_left = Image.new('RGBA', (525, 38), (0, 0, 0, 0))
        bld = ImageDraw.Draw(b_left)
        bld.rounded_rectangle([2, 4, 522, 33], radius=4, fill=GOLD_LEAF, outline=GOLD_BRIGHT, width=1)
        save_asset(b_left, f'{sub}/left.png')

        # right = empty track
        b_right = Image.new('RGBA', (525, 38), (0, 0, 0, 0))
        brd = ImageDraw.Draw(b_right)
        brd.rounded_rectangle([2, 4, 522, 33], radius=4, fill=(10, 17, 30, 220), outline=GOLD_ANTIQUE, width=1)
        save_asset(b_right, f'{sub}/right.png')

        # top / bottom vertical
        b_top = Image.new('RGBA', (38, 525), (0, 0, 0, 0))
        ImageDraw.Draw(b_top).rounded_rectangle([4, 2, 33, 522], radius=4, fill=GOLD_LEAF, outline=GOLD_BRIGHT, width=1)
        save_asset(b_top, f'{sub}/top.png')

        b_bot = Image.new('RGBA', (38, 525), (0, 0, 0, 0))
        ImageDraw.Draw(b_bot).rounded_rectangle([4, 2, 33, 522], radius=4, fill=(10, 17, 30, 220), outline=GOLD_ANTIQUE, width=1)
        save_asset(b_bot, f'{sub}/bottom.png')

# -------------------------------------------------------------------------
# 8. Window Icon (250 x 250)
# -------------------------------------------------------------------------
def generate_window_icon():
    print("--- Generating Window Icon ---")
    IW, IH = 250, 250
    icon = Image.new('RGBA', (IW, IH), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(icon)
    # Circular medallion background
    i_draw.ellipse([6, 6, IW - 7, IH - 7], fill=(8, 14, 26, 255), outline=GOLD_BRIGHT, width=3)
    i_draw.ellipse([14, 14, IW - 15, IH - 15], outline=GOLD_ANTIQUE, width=1)

    # Stylized Tree / Ethereum diamond in center
    mid_x, mid_y = IW // 2, IH // 2
    # Diamond top & bottom
    d_pts_top = [(mid_x, mid_y - 65), (mid_x + 45, mid_y - 10), (mid_x, mid_y + 15), (mid_x - 45, mid_y - 10)]
    i_draw.polygon(d_pts_top, fill=(212, 175, 55, 230), outline=GOLD_BRIGHT, width=2)
    d_pts_bot = [(mid_x, mid_y + 25), (mid_x + 45, mid_y), (mid_x, mid_y + 70), (mid_x - 45, mid_y)]
    i_draw.polygon(d_pts_bot, fill=(154, 126, 50, 200), outline=GOLD_BRIGHT, width=2)
    # Center node
    i_draw.ellipse([mid_x - 7, mid_y - 7, mid_x + 7, mid_y + 7], fill=GOLD_BRIGHT)

    # Branching circuit traces
    for angle in [30, 60, 120, 150, 210, 240, 300, 330]:
        rad = math.radians(angle)
        x1 = mid_x + int(55 * math.cos(rad))
        y1 = mid_y + int(55 * math.sin(rad))
        x2 = mid_x + int(95 * math.cos(rad))
        y2 = mid_y + int(95 * math.sin(rad))
        i_draw.line([(x1, y1), (x2, y2)], fill=GOLD_LEAF, width=2)
        i_draw.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=GOLD_BRIGHT)

    save_asset(icon, 'window_icon.png')

# -------------------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------------------
if __name__ == '__main__':
    generate_menus()
    generate_overlays()
    generate_textbox()
    generate_choice_buttons()
    generate_frames()
    generate_buttons()
    generate_bars()
    generate_window_icon()
    print("All GUI assets generated and deployed successfully!")
