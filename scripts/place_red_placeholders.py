#!/usr/bin/env python3
"""Place tinted sketch placeholders (set MOOD=disaster|happy) into game/images at every disaster size. Backs up what it replaces."""
import os, shutil, numpy as np
from PIL import Image, ImageDraw
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
V3 = os.path.join(ROOT, "vault", "06 Assets", "generated_cgs", "v3"); IMG = os.path.join(ROOT, "game", "images")
BK = os.path.join(V3, "_backup_game_images_before_red_placeholders"); os.makedirs(BK, exist_ok=True)
import sys
MOOD = os.environ.get("MOOD","disaster")
SRC_D = {"cg_ep1_disaster": ("ep1_keys", "cg_ep1_disaster_s4_sketch_red.jpg"),
       "cg_ep2_disaster": ("ep2_lisbon", "cg_ep2_disaster_t1_sketch_red.jpg"),
       "cg_ep3_disaster": ("ep3_agreements", "cg_ep3_disaster_s5_sketch_red.jpg"),
       "cg_ep4_disaster": ("ep4_apothecary", "cg_ep4_disaster_s1_sketch_red.jpg")}
SRC_H = {"cg_ep1_happy": ("ep1_keys", "cg_ep1_happy_s3_sketch_green.jpg"),
         "cg_ep2_happy": ("ep2_lisbon", "cg_ep2_happy_s1_sketch_green.jpg"),
         "cg_ep3_happy": ("ep3_agreements", "cg_ep3_happy_s2_sketch_green.jpg"),
         "cg_ep4_happy": ("ep4_apothecary", "cg_ep4_happy_s2_sketch_green.jpg")}
SRC = SRC_H if MOOD == "happy" else SRC_D
def backup(name):
    p = os.path.join(IMG, name)
    if os.path.exists(p) and not os.path.exists(os.path.join(BK, name)): shutil.copy2(p, os.path.join(BK, name))
for key, (ep_id, f) in SRC.items():
    full = Image.open(os.path.join(V3, f)).convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
    for name, im in ((f"{key}.png", full), (f"{key}_thumb.png", full.resize((512, 288), Image.Resampling.LANCZOS))):
        backup(name); im.save(os.path.join(IMG, name))
    w, h = 512, 285
    card = full.resize((w, h), Image.Resampling.LANCZOS).convert("RGBA")
    g = np.zeros((h, w, 4), dtype=np.uint8)
    for y in range(h - 90, h):
        t = (y - (h - 90)) / 89.0; g[y, :, :3] = (24, 14, 9); g[y, :, 3] = int(round(215 * t ** 1.35))
    card = Image.alpha_composite(card, Image.fromarray(g))
    m = Image.new("L", (w * 2, h * 2), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), radius=28, fill=255)
    card.putalpha(m.resize((w, h), Image.Resampling.LANCZOS))
    cn = f"scenario_card_{ep_id}_{MOOD}.png"; backup(cn); card.save(os.path.join(IMG, cn)); print("placed", key, cn)
