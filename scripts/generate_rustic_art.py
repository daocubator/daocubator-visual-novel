#!/usr/bin/env python3
"""
generate_rustic_art.py
Generates minimalist, high-contrast rustic ink line-art & analog watercolor
character sprites (2x supersampled for crisp print/merch-grade ink lines) and
flat/textured backgrounds for Get Rich Together:
- Characters (560x880 RGBA):
  * Ash El (ashel): The Creator / Protagonist — locs with feather, striped &
    botanical-geometric tunic, green bead necklaces, equipped with his instrument.
  * Lay-Lay (laylay): The Administrator / Antagonist — sage & alchemical-violet
    key-fret tunic, glass potion vials, dried herb bundles, and multisig key ledger.
  * Xochtl (xochtl): The Co-Creator / Shaman — beaded headband, ceremonial red/black
    face paint stripes, beaded diamond fringe earrings, rainbow-striped woven huipil,
    zig-zag cuffs, holding a steaming ceremonial cacao cup.
- Backgrounds (1920x1080 RGB):
  * bg constellation.png (The First Constellation — organic root-circuit star map)
  * bg sanctuary.png (Essential Food & Medicine ochre sanctuary room)
  * bg treasury_fire.png (Worst-Case Scenario high-contrast crimson/charcoal fracture)
  * bg cacao_circle.png (Ceremonial cacao circle & Lisbon showcase stage)
  * bg apothecary.png (Herbal apothecary & multisig admin signing desk)
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG_DIR = os.path.join(ROOT, "game", "images")
VAULT_SPRITES_DIR = os.path.join(ROOT, "vault", "06 Assets", "generated_sprites")
VAULT_BG_DIR = os.path.join(ROOT, "vault", "06 Assets", "generated_backgrounds")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(VAULT_SPRITES_DIR, exist_ok=True)
os.makedirs(VAULT_BG_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Rustic Line-Art & Analog Watercolor Palette
# ---------------------------------------------------------------------------
INK = (22, 18, 16, 255)           # #161210 deep rustic charcoal ink
INK_SOFT = (54, 44, 38, 255)      # #362C26 sepia-charcoal secondary line
PARCHMENT = (244, 239, 230, 255)  # #F4EFE6 warm paper
CREAM = (236, 226, 208, 255)      # #ECE2D0 warm linen

# Ash El palette
ASHEL_SKIN = (106, 68, 48, 255)
ASHEL_SKIN_SHADOW = (80, 50, 34, 255)
ASHEL_SKIN_HIGHLIGHT = (126, 84, 60, 255)
TERRACOTTA = (214, 98, 64, 255)   # #D66240
INDIGO_STRIPE = (46, 74, 112, 255)
BEAD_GREEN = (64, 138, 82, 255)
WOOD_AMBER = (182, 116, 58, 255)
WOOD_DARK = (108, 62, 32, 255)

# Xochtl palette
XOCHTL_SKIN = (218, 168, 134, 255)
XOCHTL_SKIN_SHADOW = (186, 134, 102, 255)
XOCHTL_BLUSH = (212, 128, 108, 255)
FACE_RED = (198, 48, 44, 255)
TURQUOISE = (46, 164, 150, 255)
CACAO_BRONZE = (138, 82, 58, 255)
HUIPIL_BLACK = (28, 26, 30, 255)

# Lay-Lay palette
LAYLAY_SKIN = (168, 118, 88, 255)
LAYLAY_SKIN_SHADOW = (136, 90, 64, 255)
SAGE_GREEN = (78, 128, 98, 255)
ALCHEMICAL_VIOLET = (118, 86, 152, 255)
POTION_CYAN = (92, 198, 188, 255)
POTION_AMBER = (228, 174, 68, 255)


def apply_watercolor_paper_grain(img: Image.Image, strength: float = 0.042, seed: int = 42) -> Image.Image:
    """Applies subtle analog paper & watercolor pigment granulation to non-transparent pixels."""
    arr = np.array(img).astype(np.float32)
    rng = np.random.default_rng(seed)
    h, w = arr.shape[:2]
    fine = rng.normal(0.0, 1.0, (h, w)).astype(np.float32)
    coarse_small = rng.normal(0.0, 1.0, (max(1, h // 14), max(1, w // 14))).astype(np.float32)
    coarse_img = Image.fromarray((coarse_small * 40 + 128).clip(0, 255).astype(np.uint8)).resize((w, h), Image.Resampling.BILINEAR)
    coarse = (np.array(coarse_img).astype(np.float32) - 128.0) / 40.0

    grain = (0.40 * fine + 0.60 * coarse) * (255.0 * strength)
    if arr.shape[2] == 4:
        mask = (arr[:, :, 3:4] > 10).astype(np.float32)
        arr[:, :, :3] = np.clip(arr[:, :, :3] + grain[:, :, None] * mask, 0, 255)
    else:
        arr[:, :, :3] = np.clip(arr[:, :, :3] + grain[:, :, None], 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def draw_ink_poly(draw: ImageDraw.ImageDraw, pts, fill, outline=INK, width=7):
    draw.polygon(pts, fill=fill)
    if outline and width > 0:
        draw.line(list(pts) + [pts[0]], fill=outline, width=width, joint="curve")


def draw_eyes_and_mouth_2x(draw: ImageDraw.ImageDraw, cx: int, cy: int, expr: str, skin_shadow, lip_color):
    """Draws expressive 2x-supersampled rustic ink line-art eyes, eyebrows, nose, and mouth."""
    ex_l, ex_r = cx - 84, cx + 84
    ey = cy - 18

    brow_l_dy, brow_r_dy = 0, 0
    eye_open = 21
    mouth_style = "neutral"
    look_dx = 0

    if expr in ("focused", "determined"):
        brow_l_dy, brow_r_dy = 10, 10
        mouth_style = "firm" if expr == "focused" else "determined"
    elif expr == "alarmed":
        brow_l_dy, brow_r_dy = -16, -16
        eye_open = 28
        mouth_style = "open_o"
    elif expr == "hurt":
        brow_l_dy, brow_r_dy = -12, 12
        eye_open = 18
        mouth_style = "sad"
    elif expr in ("proud", "warm"):
        brow_l_dy, brow_r_dy = -6, -6
        eye_open = 20
        mouth_style = "warm_smile"
    elif expr == "calculating":
        brow_l_dy, brow_r_dy = 8, -10
        eye_open = 17
        look_dx = 6
        mouth_style = "smirk"
    elif expr == "smirk":
        brow_l_dy, brow_r_dy = 4, -12
        mouth_style = "smirk"
    elif expr == "defensive":
        brow_l_dy, brow_r_dy = -8, 10
        look_dx = -8
        mouth_style = "frown"
    elif expr == "stern":
        brow_l_dy, brow_r_dy = 12, 12
        eye_open = 17
        mouth_style = "stern"

    # Subtle watercolor eye-socket shading
    for ex in (ex_l, ex_r):
        draw.ellipse([ex - 42, ey - 28, ex + 42, ey + 24], fill=skin_shadow)

    # Eyebrows (tapered rustic ink brush strokes)
    draw.polygon([
        (ex_l - 46, ey - 40 - brow_l_dy),
        (ex_l - 4, ey - 54 + brow_l_dy // 2),
        (ex_l + 42, ey - 38 + brow_l_dy),
        (ex_l + 38, ey - 28 + brow_l_dy),
        (ex_l - 4, ey - 42 + brow_l_dy // 2),
        (ex_l - 44, ey - 32 - brow_l_dy),
    ], fill=INK)
    draw.polygon([
        (ex_r - 42, ey - 38 + brow_r_dy),
        (ex_r + 4, ey - 54 + brow_r_dy // 2),
        (ex_r + 46, ey - 40 - brow_r_dy),
        (ex_r + 44, ey - 32 - brow_r_dy),
        (ex_r + 4, ey - 42 + brow_r_dy // 2),
        (ex_r - 38, ey - 28 + brow_r_dy),
    ], fill=INK)

    # Eyes
    for ex in (ex_l, ex_r):
        draw.ellipse([ex - 36, ey - eye_open, ex + 36, ey + eye_open], fill=PARCHMENT, outline=INK, width=6)
        ix = ex + look_dx
        draw.ellipse([ix - 17, ey - 17, ix + 17, ey + 17], fill=(36, 24, 18, 255), outline=INK, width=3)
        draw.ellipse([ix - 8, ey - 8, ix + 8, ey + 8], fill=INK)
        draw.ellipse([ix - 9, ey - 11, ix - 1, ey - 3], fill=PARCHMENT)
        # Upper lash line
        draw.arc([ex - 40, ey - eye_open - 4, ex + 40, ey + eye_open], 182, 358, fill=INK, width=10)
        # Eyelid crease
        draw.arc([ex - 34, ey - eye_open - 14, ex + 34, ey + eye_open - 10], 195, 345, fill=INK_SOFT, width=4)

    # Nose bridge, shadow & nostrils
    draw.polygon([(cx - 4, ey + 8), (cx - 18, cy + 56), (cx + 4, cy + 64), (cx + 8, ey + 14)], fill=skin_shadow)
    draw.line([(cx - 5, ey + 6), (cx - 16, cy + 56), (cx + 12, cy + 62)], fill=INK, width=7, joint="curve")
    draw.arc([cx - 28, cy + 44, cx + 28, cy + 70], 10, 170, fill=INK, width=6)

    # Mouth
    my = cy + 120
    if mouth_style == "warm_smile":
        draw.chord([cx - 52, my - 20, cx + 52, my + 32], 0, 180, fill=lip_color, outline=INK, width=6)
        draw.arc([cx - 56, my - 24, cx + 56, my + 28], 10, 170, fill=INK, width=8)
    elif mouth_style == "determined":
        draw.polygon([(cx - 52, my + 4), (cx, my - 8), (cx + 52, my - 2), (cx, my + 18)], fill=lip_color)
        draw.line([(cx - 54, my + 6), (cx, my - 2), (cx + 54, my - 4)], fill=INK, width=8)
    elif mouth_style == "smirk":
        draw.polygon([(cx - 44, my + 8), (cx + 8, my + 4), (cx + 56, my - 16), (cx + 12, my + 20)], fill=lip_color)
        draw.line([(cx - 48, my + 8), (cx + 8, my + 6), (cx + 56, my - 16)], fill=INK, width=8)
    elif mouth_style == "open_o":
        draw.ellipse([cx - 32, my - 16, cx + 32, my + 32], fill=(44, 18, 18, 255), outline=INK, width=8)
    elif mouth_style in ("sad", "frown"):
        draw.arc([cx - 48, my, cx + 48, my + 44], 195, 345, fill=INK, width=8)
        draw.line([(cx - 32, my + 24), (cx + 32, my + 24)], fill=lip_color, width=6)
    elif mouth_style in ("stern", "firm"):
        draw.polygon([(cx - 48, my), (cx, my - 8), (cx + 48, my), (cx, my + 14)], fill=lip_color)
        draw.line([(cx - 52, my + 2), (cx + 52, my + 2)], fill=INK, width=8)
    else:
        draw.polygon([(cx - 48, my), (cx, my - 10), (cx + 48, my), (cx, my + 16)], fill=lip_color)
        draw.line([(cx - 50, my), (cx, my + 4), (cx + 50, my - 2)], fill=INK, width=8)


# ---------------------------------------------------------------------------
# 1. ASH EL — The Creator / Protagonist (Equipped with his Instrument)
# ---------------------------------------------------------------------------
def generate_ashel_sprite(expr: str) -> Image.Image:
    W, H = 1120, 1760
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = W // 2

    # 1. Feather & Locs (Crown of hair inspired by Efam DAO Esphera reference)
    feather_pts = [(cx - 30, 220), (cx - 190, 68), (cx - 250, 52), (cx - 164, 116), (cx - 50, 240)]
    draw_ink_poly(d, feather_pts, fill=CREAM, outline=INK, width=6)
    d.line([(cx - 36, 228), (cx - 236, 60)], fill=TERRACOTTA, width=6)

    locs = [
        (cx - 150, 250, cx - 50, 440),
        (cx - 100, 190, cx + 20, 400),
        (cx - 20, 200, cx + 110, 410),
        (cx + 50, 240, cx + 160, 450),
        (cx - 184, 320, cx - 110, 580),
        (cx + 110, 330, cx + 176, 570),
    ]
    for x0, y0, x1, y1 in locs:
        d.rounded_rectangle([x0, y0, x1, y1], radius=36, fill=INK, outline=INK_SOFT, width=4)
    d.line([(cx - 156, 380), (cx - 176, 620)], fill=INK, width=20)
    d.line([(cx + 152, 390), (cx + 170, 600)], fill=INK, width=18)

    # 2. Neck & Tunic Torso
    d.rectangle([cx - 72, 740, cx + 72, 910], fill=ASHEL_SKIN_SHADOW, outline=INK, width=8)

    torso_pts = [
        (184, H), (144, 1300), (192, 936), (cx - 104, 860),
        (cx, 904), (cx + 104, 860), (W - 192, 936), (W - 144, 1300), (W - 184, H)
    ]
    draw_ink_poly(d, torso_pts, fill=CREAM, outline=INK, width=10)

    for sx in range(216, cx + 20, 44):
        d.line([(sx, 910), (sx, H)], fill=INDIGO_STRIPE, width=8)

    sash_poly = [
        (cx - 170, 1190), (cx + 250, 904), (W - 192, 936),
        (W - 148, 1300), (W - 184, H), (cx - 90, H)
    ]
    draw_ink_poly(d, sash_poly, fill=(34, 62, 54, 255), outline=INK, width=8)

    for py in range(1020, H - 60, 136):
        for px in range(cx - 50, W - 230, 136):
            d.ellipse([px - 44, py - 44, px + 44, py + 44], fill=INDIGO_STRIPE, outline=CREAM, width=4)
            d.ellipse([px - 20, py - 20, px + 20, py + 20], fill=TERRACOTTA, outline=INK, width=4)
            d.polygon([(px, py - 52), (px + 16, py - 72), (px, py - 88), (px - 16, py - 72)], fill=BEAD_GREEN, outline=INK, width=4)

    d.line([(cx - 170, 1190), (cx + 250, 904)], fill=TERRACOTTA, width=20)
    d.line([(cx - 170, 1190), (cx + 250, 904)], fill=INK, width=4)

    # Green Bead Necklaces
    for r_off in (0, 28, 56):
        d.arc([cx - 164 - r_off // 2, 810, cx + 164 + r_off // 2, 1370 + r_off], 0, 180, fill=BEAD_GREEN, width=16)
        d.arc([cx - 164 - r_off // 2, 810, cx + 164 + r_off // 2, 1370 + r_off], 0, 180, fill=INK, width=4)

    # 3. Head & Face
    head_pts = [
        (cx - 140, 430), (cx - 144, 630), (cx - 104, 764),
        (cx, 812), (cx + 104, 764), (cx + 144, 630), (cx + 140, 430),
        (cx + 90, 330), (cx - 90, 330)
    ]
    draw_ink_poly(d, head_pts, fill=ASHEL_SKIN, outline=INK, width=10)

    d.pieslice([cx - 172, 530, cx - 120, 650], 90, 270, fill=ASHEL_SKIN, outline=INK, width=8)
    d.pieslice([cx + 120, 530, cx + 172, 650], 270, 90, fill=ASHEL_SKIN, outline=INK, width=8)

    # Mustache & Chin Beard
    d.arc([cx - 108, 660, cx + 108, 816], 15, 165, fill=INK, width=28)
    d.polygon([(cx - 68, 652), (cx, 636), (cx + 68, 652), (cx + 56, 672), (cx, 660), (cx - 56, 672)], fill=INK)
    d.rectangle([cx - 16, 710, cx + 16, 796], fill=INK)

    draw_eyes_and_mouth_2x(d, cx, 550, expr, ASHEL_SKIN_SHADOW, (138, 72, 62, 255))

    # 4. Signature Gear: Ash El's Acoustic-Electric Folk Instrument
    neck_pts = [(230, 1070), (270, 1016), (660, 1290), (620, 1344)]
    draw_ink_poly(d, neck_pts, fill=WOOD_DARK, outline=INK, width=8)
    headstock_pts = [(150, 1010), (204, 948), (276, 1012), (224, 1072)]
    draw_ink_poly(d, headstock_pts, fill=TERRACOTTA, outline=INK, width=8)
    for peg_x, peg_y in [(164, 964), (192, 940), (148, 1028), (176, 1052)]:
        d.ellipse([peg_x - 10, peg_y - 10, peg_x + 10, peg_y + 10], fill=PARCHMENT, outline=INK, width=4)

    d.ellipse([490, 1160, 890, 1540], fill=WOOD_AMBER, outline=INK, width=10)
    d.ellipse([630, 1250, 970, 1630], fill=WOOD_AMBER, outline=INK, width=10)
    d.ellipse([510, 1180, 870, 1520], fill=WOOD_AMBER)

    sh_x, sh_y = 670, 1356
    d.ellipse([sh_x - 84, sh_y - 84, sh_x + 84, sh_y + 84], outline=TERRACOTTA, width=12)
    d.ellipse([sh_x - 68, sh_y - 68, sh_x + 68, sh_y + 68], fill=INK, outline=CREAM, width=4)
    d.rectangle([770, 1390, 804, 1496], fill=WOOD_DARK, outline=INK, width=6)
    for s_off in (-16, -6, 4, 14):
        d.line([(244, 1040 + s_off), (784, 1440 + s_off)], fill=PARCHMENT, width=4)

    d.ellipse([320, 1090, 424, 1190], fill=ASHEL_SKIN, outline=INK, width=8)
    d.polygon([(700, 1490), (820, 1420), (910, 1530), (790, 1610)], fill=ASHEL_SKIN, outline=INK, width=8)
    d.line([(810, 1544), (884, 1484)], fill=TERRACOTTA, width=16)
    d.line([(820, 1556), (894, 1496)], fill=TURQUOISE, width=10)

    im_small = im.resize((560, 880), Image.Resampling.LANCZOS)
    return apply_watercolor_paper_grain(im_small, strength=0.038, seed=11)


# ---------------------------------------------------------------------------
# 2. XOCHTL — The Co-Creator / Shaman (Cacao Ceremonies & Cups)
# ---------------------------------------------------------------------------
def generate_xochtl_sprite(expr: str) -> Image.Image:
    W, H = 1120, 1760
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = W // 2

    hair_back = [
        (cx - 190, 380), (cx - 250, 760), (cx - 230, 1120),
        (cx + 230, 1120), (cx + 250, 760), (cx + 190, 380),
        (cx + 120, 260), (cx - 120, 260)
    ]
    draw_ink_poly(d, hair_back, fill=INK, outline=INK, width=8)

    torso_pts = [
        (136, H), (112, 1280), (176, 916), (cx - 108, 850),
        (cx, 896), (cx + 108, 850), (W - 176, 916), (W - 112, 1280), (W - 136, H)
    ]
    draw_ink_poly(d, torso_pts, fill=HUIPIL_BLACK, outline=INK, width=10)

    stripe_palette = [TERRACOTTA, POTION_AMBER, TURQUOISE, ALCHEMICAL_VIOLET]
    for band_y in (990, 1150, 1330, 1520, 1670):
        for idx, col in enumerate(stripe_palette):
            y_pos = band_y + idx * 12
            margin = 152 if y_pos > 1100 else 196
            d.line([(margin, y_pos), (W - margin, y_pos)], fill=col, width=10)
        d.line([(margin, band_y - 4), (W - margin, band_y - 4)], fill=INK, width=4)
        d.line([(margin, band_y + 48), (W - margin, band_y + 48)], fill=INK, width=4)

    d.rectangle([cx - 64, 740, cx + 64, 890], fill=XOCHTL_SKIN_SHADOW, outline=INK, width=8)

    # Beaded Geometric Chest Necklace / Pectoral
    d.polygon([(cx - 96, 870), (cx + 96, 870), (cx + 76, 1230), (cx, 1300), (cx - 76, 1230)], fill=INK, outline=PARCHMENT, width=6)
    d.polygon([(cx, 930), (cx + 56, 1040), (cx, 1150), (cx - 56, 1040)], fill=TURQUOISE, outline=PARCHMENT, width=4)
    d.polygon([(cx, 976), (cx + 30, 1040), (cx, 1104), (cx - 30, 1040)], fill=TERRACOTTA, outline=INK, width=4)
    d.ellipse([cx - 12, 1028, cx + 12, 1052], fill=POTION_AMBER)

    head_pts = [
        (cx - 136, 420), (cx - 136, 620), (cx - 92, 756),
        (cx, 804), (cx + 92, 756), (cx + 136, 620), (cx + 136, 420),
        (cx + 90, 320), (cx - 90, 320)
    ]
    draw_ink_poly(d, head_pts, fill=XOCHTL_SKIN, outline=INK, width=10)

    # Ceremonial Red & Black Face Paint Stripes
    d.polygon([(cx - 128, 424), (cx, 400), (cx + 128, 424), (cx + 132, 464), (cx, 440), (cx - 132, 464)], fill=FACE_RED, outline=INK, width=6)
    d.polygon([(cx - 134, 592), (cx, 564), (cx + 134, 592), (cx + 132, 632), (cx, 596), (cx - 132, 632)], fill=FACE_RED, outline=INK, width=6)
    d.line([(cx - 132, 612), (cx - 36, 588)], fill=INK, width=6)
    d.line([(cx + 36, 588), (cx + 132, 612)], fill=INK, width=6)
    d.rectangle([cx - 16, 688, cx + 16, 800], fill=FACE_RED, outline=INK, width=6)

    # Beaded Headband
    d.polygon([(cx - 144, 384), (cx, 356), (cx + 144, 384), (cx + 140, 416), (cx, 388), (cx - 140, 416)], fill=INK, outline=INK, width=6)
    for bx in range(cx - 112, cx + 120, 48):
        d.polygon([(bx, 372), (bx + 20, 386), (bx, 400), (bx - 20, 386)], fill=TURQUOISE if (bx // 48) % 2 == 0 else TERRACOTTA, outline=PARCHMENT, width=2)

    # Beaded Diamond Fringe Earrings
    for side_sign in (-1, 1):
        ex = cx + side_sign * 156
        ey = 690
        d.polygon([(ex, ey - 56), (ex + 44, ey), (ex, ey + 56), (ex - 44, ey)], fill=FACE_RED, outline=PARCHMENT, width=6)
        d.polygon([(ex, ey - 56), (ex + 44, ey), (ex, ey + 56), (ex - 44, ey)], outline=INK, width=4)
        d.polygon([(ex, ey - 16), (ex + 16, ey), (ex, ey + 16), (ex - 16, ey)], fill=POTION_AMBER, outline=INK, width=4)
        for fx in range(ex - 28, ex + 32, 10):
            d.line([(fx, ey + 48), (fx - side_sign * 8, ey + 230)], fill=FACE_RED, width=6)
            d.line([(fx, ey + 48), (fx - side_sign * 8, ey + 230)], fill=INK, width=2)

    draw_eyes_and_mouth_2x(d, cx, 544, expr, XOCHTL_SKIN_SHADOW, FACE_RED)

    # 4. Signature Gear: Steaming Ceremonial Cacao Cup + Geometric Wrist Cuffs
    cup_y = 1330
    for side_sign in (-1, 1):
        cuff_x = cx + side_sign * 192
        cuff_pts = [
            (cuff_x - 64, cup_y + 36), (cuff_x + 64, cup_y + 16),
            (cuff_x + 72, cup_y + 124), (cuff_x - 56, cup_y + 144)
        ]
        draw_ink_poly(d, cuff_pts, fill=PARCHMENT, outline=INK, width=8)
        for cy_off in (48, 76, 104):
            d.line([(cuff_x - 52, cup_y + cy_off), (cuff_x, cup_y + cy_off - 16), (cuff_x + 52, cup_y + cy_off)], fill=INK, width=8)

    d.ellipse([cx - 164, cup_y - 4, cx - 36, cup_y + 112], fill=XOCHTL_SKIN, outline=INK, width=8)
    d.ellipse([cx + 36, cup_y - 4, cx + 164, cup_y + 112], fill=XOCHTL_SKIN, outline=INK, width=8)

    cup_pts = [
        (cx - 104, cup_y - 84), (cx + 104, cup_y - 84),
        (cx + 76, cup_y + 76), (cx - 76, cup_y + 76)
    ]
    draw_ink_poly(d, cup_pts, fill=CACAO_BRONZE, outline=INK, width=10)
    d.ellipse([cx - 104, cup_y - 104, cx + 104, cup_y - 60], fill=(62, 32, 22, 255), outline=INK, width=8)
    d.line([(cx - 92, cup_y - 28), (cx + 92, cup_y - 28)], fill=TURQUOISE, width=12)
    for gx in range(cx - 64, cx + 72, 32):
        d.polygon([(gx, cup_y - 44), (gx + 14, cup_y - 28), (gx, cup_y - 12), (gx - 14, cup_y - 28)], fill=PARCHMENT, outline=INK, width=4)

    steam_paths = [
        [(cx - 36, cup_y - 116), (cx - 60, cup_y - 190), (cx - 16, cup_y - 260), (cx - 44, cup_y - 330)],
        [(cx + 8, cup_y - 124), (cx + 44, cup_y - 204), (cx - 4, cup_y - 284), (cx + 28, cup_y - 360)],
        [(cx + 48, cup_y - 112), (cx + 72, cup_y - 176), (cx + 36, cup_y - 240)],
    ]
    for sp in steam_paths:
        d.line(sp, fill=PARCHMENT, width=8, joint="curve")
        d.line(sp, fill=TURQUOISE, width=4, joint="curve")

    im_small = im.resize((560, 880), Image.Resampling.LANCZOS)
    return apply_watercolor_paper_grain(im_small, strength=0.038, seed=22)


# ---------------------------------------------------------------------------
# 3. LAY-LAY — The Administrator / Antagonist (Admin Power, Potions & Herbs)
# ---------------------------------------------------------------------------
def generate_laylay_sprite(expr: str) -> Image.Image:
    W, H = 1120, 1760
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = W // 2

    d.ellipse([cx - 168, 236, cx + 168, 550], fill=INK, outline=INK, width=8)
    d.ellipse([cx - 104, 164, cx + 104, 324], fill=INK, outline=INK, width=8)
    d.line([(cx - 176, 264), (cx + 184, 208)], fill=POTION_AMBER, width=12)
    d.ellipse([cx - 208, 244, cx - 160, 292], fill=ALCHEMICAL_VIOLET, outline=INK, width=6)

    for angle, leaf_col in [(-25, SAGE_GREEN), (-5, BEAD_GREEN), (15, SAGE_GREEN)]:
        lx = cx + 136 + int(56 * math.cos(math.radians(angle)))
        ly = 390 + int(56 * math.sin(math.radians(angle)))
        d.polygon([(cx + 116, 420), (lx, ly - 16), (lx + 32, ly), (lx, ly + 16)], fill=leaf_col, outline=INK, width=6)

    d.rectangle([cx - 64, 740, cx + 64, 900], fill=LAYLAY_SKIN_SHADOW, outline=INK, width=8)

    torso_pts = [
        (164, H), (132, 1290), (184, 924), (cx - 100, 856),
        (cx, 904), (cx + 100, 856), (W - 184, 924), (W - 132, 1290), (W - 164, H)
    ]
    draw_ink_poly(d, torso_pts, fill=ALCHEMICAL_VIOLET, outline=INK, width=10)

    cape_pts = [
        (164, H), (132, 1290), (184, 924), (cx - 100, 856),
        (cx + 70, 904), (cx - 50, H)
    ]
    draw_ink_poly(d, cape_pts, fill=SAGE_GREEN, outline=INK, width=8)

    for ky in range(940, H - 40, 96):
        kx = cx + 44 - int((ky - 940) * 0.12)
        d.rectangle([kx - 28, ky, kx + 28, ky + 56], fill=CREAM, outline=INK, width=6)
        d.rectangle([kx - 12, ky + 16, kx + 12, ky + 40], fill=ALCHEMICAL_VIOLET, outline=INK, width=4)

    d.polygon([(cx, 868), (cx + 48, 924), (cx, 980), (cx - 48, 924)], fill=POTION_AMBER, outline=INK, width=8)
    d.ellipse([cx - 14, 904, cx + 14, 932], fill=INK)
    d.line([(cx, 932), (cx, 964)], fill=INK, width=8)

    head_pts = [
        (cx - 132, 420), (cx - 132, 616), (cx - 88, 752),
        (cx, 800), (cx + 88, 752), (cx + 132, 616), (cx + 132, 420),
        (cx + 88, 324), (cx - 88, 324)
    ]
    draw_ink_poly(d, head_pts, fill=LAYLAY_SKIN, outline=INK, width=10)

    draw_eyes_and_mouth_2x(d, cx, 544, expr, LAYLAY_SKIN_SHADOW, (108, 46, 82, 255))

    # 4. Signature Gear: Bandolier with Potions, Dried Herbs & Multisig Key Ledger
    d.line([(216, 930), (780, 1580)], fill=WOOD_DARK, width=36)
    d.line([(216, 930), (780, 1580)], fill=INK, width=6)

    vials = [
        (330, 1070, POTION_CYAN),
        (430, 1176, POTION_AMBER),
        (530, 1284, FACE_RED),
    ]
    for vx, vy, pcol in vials:
        d.rectangle([vx - 14, vy - 52, vx + 14, vy - 28], fill=WOOD_AMBER, outline=INK, width=6)
        d.ellipse([vx - 40, vy - 28, vx + 40, vy + 52], fill=PARCHMENT, outline=INK, width=8)
        d.pieslice([vx - 32, vy - 20, vx + 32, vy + 44], 0, 180, fill=pcol, outline=INK, width=4)
        d.ellipse([vx - 16, vy - 8, vx - 4, vy + 4], fill=PARCHMENT)

    herb_x, herb_y = 330, 1450
    for h_angle, h_col in [(-35, SAGE_GREEN), (-20, BEAD_GREEN), (-5, ALCHEMICAL_VIOLET), (10, SAGE_GREEN), (25, POTION_AMBER)]:
        rad = math.radians(h_angle - 90)
        hx1 = herb_x + int(170 * math.cos(rad))
        hy1 = herb_y + int(170 * math.sin(rad))
        d.line([(herb_x, herb_y + 60), (hx1, hy1)], fill=INK, width=10)
        d.ellipse([hx1 - 24, hy1 - 36, hx1 + 24, hy1 + 36], fill=h_col, outline=INK, width=6)
    d.rectangle([herb_x - 44, herb_y - 12, herb_x + 44, herb_y + 36], fill=TERRACOTTA, outline=INK, width=6)
    d.ellipse([herb_x - 60, herb_y + 8, herb_x + 56, herb_y + 104], fill=LAYLAY_SKIN, outline=INK, width=8)

    tab_x, tab_y = 756, 1300
    tab_pts = [
        (tab_x - 124, tab_y - 136), (tab_x + 112, tab_y - 168),
        (tab_x + 136, tab_y + 132), (tab_x - 100, tab_y + 164)
    ]
    draw_ink_poly(d, tab_pts, fill=INK, outline=POTION_AMBER, width=8)
    scr_pts = [
        (tab_x - 96, tab_y - 104), (tab_x + 88, tab_y - 130),
        (tab_x + 108, tab_y + 96), (tab_x - 76, tab_y + 124)
    ]
    draw_ink_poly(d, scr_pts, fill=(28, 36, 42, 255), outline=POTION_CYAN, width=4)
    d.ellipse([tab_x - 32, tab_y - 72, tab_x + 32, tab_y - 8], outline=POTION_AMBER, width=8)
    d.line([(tab_x, tab_y - 8), (tab_x + 8, tab_y + 72)], fill=POTION_AMBER, width=8)
    d.line([(tab_x + 4, tab_y + 40), (tab_x + 32, tab_y + 36)], fill=POTION_AMBER, width=8)
    d.line([(tab_x + 8, tab_y + 64), (tab_x + 36, tab_y + 60)], fill=POTION_AMBER, width=8)

    d.ellipse([tab_x + 44, tab_y - 20, tab_x + 152, tab_y + 88], fill=LAYLAY_SKIN, outline=INK, width=8)

    im_small = im.resize((560, 880), Image.Resampling.LANCZOS)
    return apply_watercolor_paper_grain(im_small, strength=0.038, seed=33)


# ---------------------------------------------------------------------------
# 4. BACKGROUNDS (1920x1080 Minimalist Flat + Analog Watercolor & Rustic Line-Art)
# ---------------------------------------------------------------------------
def generate_bg_constellation() -> Image.Image:
    W, H = 1920, 1080
    im = Image.new("RGBA", (W, H), (17, 18, 22, 255))
    cx, cy = 960, 560
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(520, 20, -20):
        alpha = int(32 * ((1.0 - r / 520.0) ** 2))
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(228, 184, 96, alpha))
    im = Image.alpha_composite(im, glow)
    d = ImageDraw.Draw(im)

    d.rectangle([28, 28, W - 29, H - 29], outline=(146, 122, 74, 110), width=2)
    d.rectangle([36, 36, W - 37, H - 37], outline=(146, 122, 74, 55), width=1)

    targets = [
        (410, 340, (224, 122, 95)),   # Terracotta - Keys & Sovereignty
        (410, 740, (46, 196, 182)),   # Turquoise - Collaboration & Co-op
        (1510, 340, (232, 197, 116)), # Ochre - Make & Enforce Agreements
        (1510, 740, (155, 126, 222)), # Violet - Perspective Shift: Admin & Defense
    ]

    rng = random.Random(77)
    for tx, ty, col in targets:
        d.line([(cx, cy), (tx, ty)], fill=(218, 192, 138, 180), width=3)
        dx, dy = tx - cx, ty - cy
        length = math.hypot(dx, dy)
        ux, uy = dx / length, dy / length
        px, py = -uy, ux
        for step in (0.28, 0.44, 0.60, 0.76):
            bx = cx + dx * step
            by = cy + dy * step
            for side in (-1, 1):
                reach = rng.uniform(55, 115)
                along = rng.uniform(45, 95)
                mid_x = bx + ux * (along * 0.5) + px * side * (reach * 0.4)
                mid_y = by + uy * (along * 0.5) + py * side * (reach * 0.4)
                end_x = bx + ux * along + px * side * reach
                end_y = by + uy * along + py * side * reach
                d.line([(bx, by), (mid_x, mid_y), (end_x, end_y)], fill=(196, 172, 122, 135), width=2, joint="curve")
                d.ellipse([end_x - 6, end_y - 6, end_x + 6, end_y + 6], fill=(*col, 90))
                d.ellipse([end_x - 3, end_y - 3, end_x + 3, end_y + 3], fill=(250, 240, 210, 235))

    d.ellipse([cx - 118, cy - 118, cx + 118, cy + 118], fill=(22, 23, 28, 245), outline=(232, 197, 116, 230), width=4)
    d.ellipse([cx - 106, cy - 106, cx + 106, cy + 106], outline=(232, 197, 116, 95), width=2)

    for _ in range(120):
        sx = rng.randint(60, W - 60)
        sy = rng.randint(60, H - 60)
        sr = rng.choice([1, 1, 2, 3])
        sa = rng.randint(50, 160)
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(244, 239, 230, sa))

    return apply_watercolor_paper_grain(im.convert("RGB"), strength=0.025, seed=99)


def generate_bg_sanctuary() -> Image.Image:
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), (238, 198, 124))
    d = ImageDraw.Draw(im)

    for y in range(0, 700, 4):
        t = y / 700.0
        r = int(242 * (1 - t) + 228 * t)
        g = int(204 * (1 - t) + 182 * t)
        b = int(132 * (1 - t) + 108 * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    d.polygon([(0, 210), (W, 218), (W, 298), (0, 290)], fill=(156, 98, 56), outline=INK[:3], width=5)
    d.line([(0, 265), (W, 272)], fill=(118, 70, 36), width=4)
    for bx in (740, 1010, 1380):
        d.rectangle([bx, 292, bx + 22, 435], fill=(218, 214, 206), outline=INK[:3], width=3)
        d.ellipse([bx + 6, 310, bx + 16, 320], fill=INK[:3])
        d.ellipse([bx + 6, 412, bx + 16, 422], fill=INK[:3])

    d.chord([440, 185, 640, 235], 0, 180, fill=(138, 168, 192), outline=INK[:3], width=4)
    d.pieslice([740, 165, 910, 255], 180, 360, fill=BEAD_GREEN[:3], outline=INK[:3], width=4)
    d.rectangle([940, 158, 1095, 214], fill=(118, 124, 134), outline=INK[:3], width=4)
    d.rectangle([1160, 170, 1340, 216], fill=(228, 152, 84), outline=INK[:3], width=3)
    d.chord([1145, 188, 1355, 240], 0, 180, fill=(144, 172, 192), outline=INK[:3], width=4)
    leaves = [
        (1350, 140, 48, 28), (1410, 95, 56, 32), (1485, 130, 52, 30),
        (1440, 175, 44, 26), (1545, 165, 50, 28), (1595, 195, 42, 24)
    ]
    for lx, ly, lw, lh in leaves:
        d.line([(1390, 210), (lx, ly)], fill=INK[:3], width=4)
        d.ellipse([lx - lw, ly - lh, lx + lw, ly + lh], fill=BEAD_GREEN[:3], outline=INK[:3], width=4)
        d.line([(lx - lw + 10, ly), (lx + lw - 10, ly)], fill=INK[:3], width=2)

    d.polygon([(0, 700), (W, 700), (W, H), (0, H)], fill=(42, 68, 112), outline=INK[:3], width=5)
    for rx in range(80, W, 140):
        d.polygon([(rx, 700), (rx + 45, 700), (rx - 60, H), (rx - 105, H)], fill=(68, 106, 154), outline=INK[:3], width=2)
        d.line([(rx + 65, 700), (rx - 40, H)], fill=TERRACOTTA[:3], width=3)

    d.polygon([(830, 690), (895, 690), (885, 785), (840, 785)], fill=(252, 218, 92), outline=INK[:3], width=4)
    d.ellipse([830, 680, 895, 702], fill=(255, 248, 200), outline=INK[:3], width=3)
    for i in range(-8, 9):
        ang = math.radians(i * 7 + 90)
        ex = 760 + int(165 * math.cos(ang))
        ey = 810 + int(135 * math.sin(ang))
        d.polygon([(760, 810), (ex - 16, ey - 10), (ex, ey + 15), (ex + 16, ey - 10)], fill=(154, 178, 96), outline=INK[:3], width=3)

    return apply_watercolor_paper_grain(im, strength=0.04, seed=44)


def generate_bg_treasury_fire() -> Image.Image:
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), (24, 18, 20))
    d = ImageDraw.Draw(im)

    for i in range(0, W + 400, 16):
        t = i / float(W + 400)
        col = (
            int(42 + 128 * math.sin(t * math.pi)),
            int(20 + 24 * math.sin(t * math.pi)),
            int(24 + 18 * math.cos(t * math.pi)),
        )
        d.line([(i - 300, 0), (i + 100, H)], fill=col, width=18)

    cx, cy = W // 2, H // 2 - 40
    for a0, a1, r_off in [(10, 82, 0), (95, 168, 18), (185, 260, -12), (275, 348, 10)]:
        r = 310 + r_off
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=(236, 226, 208), width=6)
        d.arc([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14], a0, a1, fill=TERRACOTTA[:3], width=3)

    cracks = [
        [(cx, cy), (cx - 180, cy - 140), (cx - 420, cy - 90), (cx - 780, cy - 280)],
        [(cx, cy), (cx + 210, cy - 110), (cx + 520, cy - 220), (cx + 860, cy - 180)],
        [(cx, cy), (cx - 140, cy + 160), (cx - 490, cy + 290)],
        [(cx, cy), (cx + 190, cy + 150), (cx + 560, cy + 310)],
    ]
    for c in cracks:
        d.line(c, fill=INK[:3], width=9)
        d.line(c, fill=(244, 184, 120), width=3)

    return apply_watercolor_paper_grain(im, strength=0.05, seed=55)


def generate_bg_cacao_circle() -> Image.Image:
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), (234, 222, 202))
    d = ImageDraw.Draw(im)

    d.rectangle([140, 80, 620, 660], fill=(218, 146, 114), outline=INK[:3], width=5)
    d.rectangle([680, 60, 1240, 660], fill=(42, 54, 62), outline=INK[:3], width=6)
    d.rectangle([1300, 80, 1780, 660], fill=(138, 168, 144), outline=INK[:3], width=5)

    scx, scy = 960, 360
    for r in (60, 120, 180, 240):
        d.ellipse([scx - r, scy - r, scx + r, scy + r], outline=(232, 197, 116), width=3)
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        d.line([(scx + int(65 * math.cos(rad)), scy + int(65 * math.sin(rad))),
                (scx + int(235 * math.cos(rad)), scy + int(235 * math.sin(rad)))], fill=(46, 164, 150), width=2)

    d.polygon([(0, 680), (W, 680), (W, H), (0, H)], fill=(124, 76, 48), outline=INK[:3], width=6)
    d.polygon([(640, 680), (1280, 680), (1420, H), (500, H)], fill=TERRACOTTA[:3], outline=INK[:3], width=5)
    for ry in range(720, H, 55):
        d.line([(580, ry), (1340, ry)], fill=PARCHMENT[:3], width=4)

    for cup_x in (760, 960, 1160):
        d.polygon([(cup_x - 36, 735), (cup_x + 36, 735), (cup_x + 26, 795), (cup_x - 26, 795)],
                  fill=CACAO_BRONZE[:3], outline=INK[:3], width=4)
        d.ellipse([cup_x - 36, 726, cup_x + 36, 744], fill=INK[:3], outline=PARCHMENT[:3], width=2)

    return apply_watercolor_paper_grain(im, strength=0.04, seed=66)


def generate_bg_apothecary() -> Image.Image:
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), (224, 218, 204))
    d = ImageDraw.Draw(im)

    d.rectangle([0, 0, W, 58], fill=WOOD_DARK[:3], outline=INK[:3], width=5)
    for hx in range(220, W - 180, 260):
        d.line([(hx, 58), (hx, 130)], fill=INK[:3], width=4)
        d.polygon([(hx, 120), (hx - 42, 230), (hx, 255), (hx + 42, 230)], fill=SAGE_GREEN[:3], outline=INK[:3], width=4)
        d.rectangle([hx - 14, 118, hx + 14, 136], fill=TERRACOTTA[:3], outline=INK[:3], width=3)

    for sx0, sx1 in [(110, 680), (1240, 1810)]:
        for sy in (340, 520):
            d.rectangle([sx0, sy, sx1, sy + 24], fill=WOOD_AMBER[:3], outline=INK[:3], width=4)
            for bx in range(sx0 + 45, sx1 - 45, 95):
                col = POTION_CYAN[:3] if (bx + sy) % 3 == 0 else (ALCHEMICAL_VIOLET[:3] if (bx + sy) % 2 == 0 else POTION_AMBER[:3])
                d.ellipse([bx - 24, sy - 56, bx + 24, sy - 2], fill=PARCHMENT[:3], outline=INK[:3], width=4)
                d.pieslice([bx - 20, sy - 50, bx + 20, sy - 6], 0, 180, fill=col, outline=INK[:3], width=2)
                d.rectangle([bx - 8, sy - 74, bx + 8, sy - 54], fill=WOOD_DARK[:3], outline=INK[:3], width=3)

    d.rounded_rectangle([740, 160, 1180, 640], radius=180, fill=(38, 46, 56), outline=INK[:3], width=6)
    d.ellipse([860, 280, 1060, 480], outline=(232, 197, 116), width=4)
    d.polygon([(960, 310), (1025, 425), (895, 425)], outline=POTION_CYAN[:3], width=4)

    d.polygon([(0, 670), (W, 670), (W, H), (0, H)], fill=(96, 62, 42), outline=INK[:3], width=6)

    return apply_watercolor_paper_grain(im, strength=0.04, seed=77)


def generate_gui_chrome():
    """Restyle main_menu.png, game_menu.png, textbox.png, frame.png, namebox.png, notify.png
    into the minimalist high-contrast rustic line-art & analog watercolor aesthetic."""
    gui_dir = os.path.join(ROOT, "game", "gui")
    W, H = 1920, 1080

    # 1. main_menu.png — Minimalist rustic constellation & three-archetype emblem on warm charcoal paper
    mm = generate_bg_constellation().convert("RGBA")
    d = ImageDraw.Draw(mm)
    # Subtle botanical/circuit line-art framing on the right side for the title screen
    cx, cy = 1140, 540
    for r in (280, 220, 155):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(232, 197, 116, 175), width=3)
    # Three archetype emblems (Guitar / Cacao Cup / Apothecary Vial) at 120-degree intervals
    for deg, col in [(270, TERRACOTTA[:3]), (30, TURQUOISE[:3]), (150, ALCHEMICAL_VIOLET[:3])]:
        rad = math.radians(deg)
        nx = cx + int(220 * math.cos(rad))
        ny = cy + int(220 * math.sin(rad))
        d.line([(cx, cy), (nx, ny)], fill=(218, 192, 138, 180), width=3)
        d.ellipse([nx - 26, ny - 26, nx + 26, ny + 26], fill=(22, 20, 18, 245), outline=(*col, 240), width=4)
        d.ellipse([nx - 8, ny - 8, nx + 8, ny + 8], fill=(244, 239, 230, 255))
    mm_rgb = mm.convert("RGB")
    mm_rgb.save(os.path.join(gui_dir, "main_menu.png"), format="PNG")

    # 2. game_menu.png & nvl.png — Clean muted parchment-charcoal wash
    gm = Image.new("RGB", (W, H), (22, 19, 17))
    gd = ImageDraw.Draw(gm)
    gd.rectangle([28, 28, W - 29, H - 29], outline=(184, 158, 114), width=2)
    gd.rectangle([38, 38, W - 39, H - 39], outline=(112, 96, 72), width=1)
    gm = apply_watercolor_paper_grain(gm, strength=0.025, seed=88)
    gm.save(os.path.join(gui_dir, "game_menu.png"), format="PNG")
    gm.save(os.path.join(gui_dir, "nvl.png"), format="PNG")
    phone_nvl = os.path.join(gui_dir, "phone", "nvl.png")
    if os.path.exists(os.path.dirname(phone_nvl)):
        gm.save(phone_nvl, format="PNG")

    # 3. textbox.png — High-contrast matte charcoal dialogue box with rustic terracotta/ochre double-ink border
    tb = Image.new("RGBA", (1920, 278), (0, 0, 0, 0))
    td = ImageDraw.Draw(tb)
    td.rounded_rectangle([180, 12, 1740, 264], radius=10, fill=(22, 19, 17, 238), outline=(224, 122, 95, 230), width=3)
    td.rounded_rectangle([188, 20, 1732, 256], radius=6, outline=(242, 204, 143, 120), width=1)
    tb.save(os.path.join(gui_dir, "textbox.png"), format="PNG")

    # 4. frame.png — Clean rustic line-art modal frame
    fr = Image.new("RGBA", (300, 300), (24, 20, 18, 242))
    fd = ImageDraw.Draw(fr)
    fd.rectangle([2, 2, 297, 297], outline=(224, 122, 95, 235), width=3)
    fd.rectangle([8, 8, 291, 291], outline=(242, 204, 143, 130), width=1)
    fr.save(os.path.join(gui_dir, "frame.png"), format="PNG")

    # 5. notify.png — Top HUD bar & notification pill
    nf = Image.new("RGBA", (400, 60), (22, 19, 17, 235))
    nd = ImageDraw.Draw(nf)
    nd.rectangle([1, 1, 398, 58], outline=(232, 197, 116, 190), width=2)
    nf.save(os.path.join(gui_dir, "notify.png"), format="PNG")
    print("[SAVED] Restyled GUI chrome (main_menu, game_menu, textbox, frame, notify)")


def save_both(im: Image.Image, filename: str, is_bg: bool = False):
    p1 = os.path.join(IMG_DIR, filename)
    p2 = os.path.join(VAULT_BG_DIR if is_bg else VAULT_SPRITES_DIR, filename)
    im.save(p1, format="PNG")
    im.save(p2, format="PNG")
    stage_lab_dir = os.path.join(ROOT, "stage-lab", "game", "images")
    if os.path.exists(stage_lab_dir):
        im.save(os.path.join(stage_lab_dir, filename), format="PNG")
    print(f"[SAVED] {filename} ({im.size}, {im.mode})")


def main():
    print("=== Generating 2x-Supersampled Rustic Line-Art & Analog Watercolor Assets ===")

    for expr in ("neutral", "focused", "alarmed", "hurt", "determined", "proud"):
        im = generate_ashel_sprite(expr)
        save_both(im, f"ashel {expr}.png", is_bg=False)

    for expr in ("neutral", "warm", "focused", "stern", "hurt", "proud"):
        im = generate_xochtl_sprite(expr)
        save_both(im, f"xochtl {expr}.png", is_bg=False)

    for expr in ("neutral", "calculating", "smirk", "defensive", "stern", "alarmed"):
        im = generate_laylay_sprite(expr)
        save_both(im, f"laylay {expr}.png", is_bg=False)

    save_both(generate_bg_constellation(), "bg constellation.png", is_bg=True)
    save_both(generate_bg_sanctuary(), "bg sanctuary.png", is_bg=True)
    save_both(generate_bg_treasury_fire(), "bg treasury_fire.png", is_bg=True)
    save_both(generate_bg_cacao_circle(), "bg cacao_circle.png", is_bg=True)
    save_both(generate_bg_apothecary(), "bg apothecary.png", is_bg=True)
    generate_gui_chrome()

    print("=== All Rustic Line-Art & Analog Watercolor Assets Generated! ===")


if __name__ == "__main__":
    main()
