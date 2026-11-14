#!/usr/bin/env python3
"""
generate_sprite_v3.py
Generates v3 hand-etched woodcut/engraved character neutral sprites (Koraba, Xochit, Clara)
from the 2026-11-11 EFAM DAO character sheets, removes the flat white background while
preserving 100% of interior ivory/ochre paper tones, and outputs 560x880 RGBA PNGs +
in-game stage previews over the new Pass 3A backgrounds.
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime, timezone
import cv2
import numpy as np
import requests
from dotenv import load_dotenv
from PIL import Image

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SHEETS_DIR = os.path.join(REPO_ROOT, "vault", "06 Assets", "2026-11-11 character designs (EFAM DAO)")
OUT_DIR = os.path.join(REPO_ROOT, "vault", "06 Assets", "generated_sprites", "v3")
USAGE_LOG_PATH = os.path.join(REPO_ROOT, "vault", "06 Assets", "generation_usage_log.json")

COST_PER_IMAGE_USD = 0.030

CHARACTER_CONFIGS = {
    "koraba": {
        "legacy_tag": "ashel",
        "sheet_file": "Koraba_ The Bridge Keeper Dossier.png",
        "preview_bg": "bg sanctuary.png",
        "prompt": (
            "Three-quarter-length (knees-up) standing character sprite of Koraba (The Bridge Keeper, musician and healer), "
            "strictly replicating the HIGHLY STYLIZED, flat-plane hand-carved woodcut / folk-icon art style and exact non-realistic "
            "geometric facial proportions of the character on Reference Image 1. "
            "EXTREME STYLIZED WOODCUT FACIAL GEOMETRY (CRITICAL — DO NOT HUMANIZE OR USE REALISTIC PROPORTIONS): "
            "Must preserve the exact elongated, angular African-mask / woodcut icon face from the reference sheet: "
            "1) Oversized, wide horizontal almond eyes spanning from temple to temple with heavy half-moon upper eyelids and concentric carved under-eye arcs; "
            "2) Very long, razor-thin vertical geometric nose bridge running straight down the face; "
            "3) Tiny, narrow, compact mouth set low above a sharply tapered narrow geometric chin; "
            "4) White ceremonial stippled dots along the brow arch, nose bridge, and cheekbones, with bold parallel vertical woodcut gouge lines carving the cheeks and long slender cylindrical neck. "
            "SUBTLE 2/3 PROFILE & DROPPED-SHOULDER POSTURE: Standing with his body and head turned at a subtle, natural 2/3 angle "
            "(20 to 30 degrees—enough to feel natural and alive while keeping both oversized stylized almond eyes and the iconic woodcut "
            "face geometry 100% intact), with his closer shoulder dropped noticeably lower in a relaxed contrapposto stance, and his eyes "
            "looking naturally off-camera along his 2/3 turn toward his companions on stage (NOT staring at the viewer). "
            "ASYMMETRIC SPLIT HANDS & KORA: Holding his gourd-bodied kora string instrument diagonally across his torso, upper hand raised "
            "to chest height gently fretting the wooden kora neck, lower hand resting on the curved gourd resonator at waist level. "
            "Appearance & Attire: Dark locs tied at the crown with bead-adorned strands draping over his angled shoulders, layered woven "
            "sleeveless tunic and asymmetrically draped indigo/ochre wrap/shawl with coarse linear and zig-zag woodcut patterns, beaded necklaces and bracelets. "
            "IMPORTANT ISOLATION RULES: Do NOT include the circular halo/mandala behind his head, floor rugs, bottles, herbs, flutes, "
            "drums, text, or labels. Render ONLY the single standing character with a bold hand-etched dark black/umber outer contour line, "
            "completely isolated on a pure, flat, uniform bright white background (#FFFFFF) with generous empty white margins."
        ),
    },
    "xochit": {
        "legacy_tag": "xochtl",
        "sheet_file": "Xochit_ Ceremonial Weaver Character Sheet.png",
        "preview_bg": "bg cacao_circle.png",
        "prompt": (
            "Three-quarter-length (knees-up) standing character sprite of Xochit (The Ceremonial Weaver, ceremonialist and messenger), "
            "strictly replicating the HIGHLY STYLIZED, flat-plane hand-carved woodcut / folk-engraving art style and exact non-realistic "
            "geometric mask-like facial proportions of the character on Reference Image 1. "
            "EXTREME STYLIZED WOODCUT FACIAL GEOMETRY (CRITICAL — DO NOT HUMANIZE OR USE GENERIC AI/COMIC FACIAL PROPORTIONS): "
            "Must look like it was carved by the exact same woodcut artist as Reference Image 1, preserving her iconic stylized geometric face: "
            "1) GIANT, oversized heavy-lidded horizontal almond eyes that span nearly the ENTIRE width of her face from temple to temple, "
            "with thick, drooping half-moon upper eyelids and bold concentric carved under-eye arcs; "
            "2) A very long, razor-thin, straight vertical geometric nose bridge with flat woodcut planes and a tiny septum ring; "
            "3) A tiny, petite, narrow pursed mouth (no wider than the nose tip) set low above a sharply tapered, narrow V-shaped geometric chin; "
            "4) A long, slender, columnar cylindrical neck carved with vertical parallel woodcut striations; "
            "5) Bold horizontal red-and-black face-paint stripes across her flat geometric cheeks and a vertical red stripe down her nose bridge and chin, "
            "with coarse parallel diagonal woodcut hatching across her cheeks. "
            "SUBTLE 2/3 PROFILE & DROPPED-SHOULDER POSTURE: Standing with her torso and head turned at a subtle, natural 2/3 angle "
            "(20 to 30 degrees—preserving both of her giant temple-to-temple heavy-lidded almond eyes and her iconic triangular woodcut face "
            "while avoiding a stiff straight-on pose), with one shoulder dropped lower in a relaxed, natural posture and her eyes looking "
            "naturally off-camera along her 2/3 turn toward her companions on stage (NOT looking at the viewer). "
            "ASYMMETRIC SPLIT HANDS & CACAO BOWL: One hand cradling the base of her carved ceremonial cacao bowl (marked with a four-point star motif) "
            "at solar-plexus height, while her other hand is raised slightly higher near the rim in a natural ceremonial gesture. "
            "Appearance & Attire: Long dark wavy/braided hair flowing over her shoulders, geometric red-and-gold beaded headband, huge diamond-shaped "
            "beaded fringe statement earrings, layered beaded necklaces, and richly patterned woven poncho/huipil with diamond and step-fret woodcut motifs. "
            "IMPORTANT ISOLATION RULES: Do NOT include the circular cosmic halo behind her head, background baskets, flowers, bottles, "
            "text, or labels. Render ONLY the single standing character with a bold hand-etched dark black/umber outer contour line, "
            "completely isolated on a pure, flat, uniform bright white background (#FFFFFF) with generous empty white margins."
        ),
    },
    "clara": {
        "legacy_tag": "laylay",
        "sheet_file": "Clara_ The Registrar Character Sheet.png",
        "preview_bg": "bg apothecary.png",
        "prompt": (
            "Three-quarter-length (knees-up) standing character sprite of Clara (The Registrar, administrator and archivist), "
            "strictly replicating the HIGHLY STYLIZED, flat-plane hand-carved woodcut / folk-engraving art style and exact non-realistic "
            "geometric facial proportions of the character on Reference Image 1. "
            "EXTREME STYLIZED WOODCUT FACIAL GEOMETRY (CRITICAL — DO NOT HUMANIZE OR USE GENERIC AI/COMIC FACIAL PROPORTIONS): "
            "Must look like it was carved by the exact same woodcut artist as Reference Image 1, preserving her iconic stylized geometric face: "
            "1) GIANT, oversized heavy-lidded horizontal almond eyes that span nearly the ENTIRE width of her face from temple to temple, "
            "with thick, heavy half-moon upper eyelids and bold concentric carved under-eye arcs; "
            "2) A very long, razor-thin, straight vertical geometric nose bridge running down the center of the face; "
            "3) A tiny, petite, narrow pursed mouth set low above a sharply tapered, narrow pointed geometric chin; "
            "4) An ultra-long, slender, cylindrical columnar neck carved with vertical parallel woodcut hatching and a vertical dotted center line; "
            "5) Flat geometric cheek planes carved with coarse parallel vertical/diagonal woodcut lines. "
            "SUBTLE 2/3 PROFILE & DROPPED-SHOULDER POSTURE: Standing with her torso and head turned at a subtle, natural 2/3 angle "
            "(20 to 30 degrees—preserving both of her giant temple-to-temple heavy-lidded almond eyes and her iconic narrow woodcut face "
            "while avoiding a stiff straight-on pose), with one shoulder dropped lower in a relaxed, natural contrapposto posture and her eyes "
            "looking naturally off-camera along her 2/3 turn toward her colleagues on stage (NOT looking at the viewer). "
            "ASYMMETRIC SPLIT HANDS & PROPS: One arm bent to hold her wooden clipboard (bearing a four-point star emblem) angled across her chest, "
            "while her other hand is raised slightly higher holding a fountain pen poised near the clipboard. "
            "Appearance & Attire: Blonde hair styled in a neat parted woodcut updo with a large coiled side bun behind one ear, round pearl stud earrings, "
            "tailored slate-blue blazer with engraved orbit/spiral sleeve and lapel patterns and a four-point star lapel pin over a crisp collared shirt, "
            "red lanyard with ID keycard badge, and matching tailored trousers/skirt with fine linear woodcut hatching. "
            "IMPORTANT ISOLATION RULES: Do NOT include the circular bookshelf halo/arch behind her head, desks, lamps, mugs, stacks of "
            "binders, text, or labels. Render ONLY the single standing character with a bold hand-etched dark black/umber outer contour line, "
            "completely isolated on a pure, flat, uniform bright white background (#FFFFFF) with generous empty white margins."
        ),
    },
}


def log_usage(char_name: str, prompt: str, cost: float = COST_PER_IMAGE_USD):
    log_data = {"total_spent_usd": 0.0, "total_images": 0, "generations": []}
    if os.path.exists(USAGE_LOG_PATH):
        try:
            with open(USAGE_LOG_PATH, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        except Exception:
            pass

    log_data["total_images"] += 1
    log_data["total_spent_usd"] = round(log_data["total_spent_usd"] + cost, 4)
    log_data["generations"].append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "asset": f"sprite {char_name} neutral (v3)",
        "model": "gemini-3.1-flash-image",
        "cost_usd": cost,
        "cumulative_spent_usd": log_data["total_spent_usd"],
        "prompt_snippet": prompt[:120] + "..."
    })

    os.makedirs(os.path.dirname(USAGE_LOG_PATH), exist_ok=True)
    with open(USAGE_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

    print(f"[USAGE] Logged generation for {char_name}. Cumulative spend: ${log_data['total_spent_usd']:.3f} ({log_data['total_images']} images)")


def extract_clean_cutout(raw_path: str) -> Image.Image:
    """
    Removes the flat white exterior background using exterior flood-fill + dark contour
    barrier so 100% of the interior antique ivory/ochre tones remain completely solid.
    Also punches out any bright-white enclosed background voids (e.g., between legs or
    between kora neck and shoulder) that are purely flat white (#FAFAFA+).
    """
    img_bgr = cv2.imread(raw_path)
    if img_bgr is None:
        raise RuntimeError(f"Could not read {raw_path}")
    h, w, _ = img_bgr.shape
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    b, g, r = cv2.split(img_bgr)
    sat = np.maximum(np.maximum(r, g), b).astype(np.int16) - np.minimum(np.minimum(r, g), b).astype(np.int16)

    # Pure background pixels are very bright neutral white (#F0F0F0+), unlike warm ivory/ochre textiles
    warmth = r.astype(np.int16) - b.astype(np.int16)
    is_bg_candidate = ((gray >= 236) & (sat <= 14) & (warmth <= 10)).astype(np.uint8)

    # Connected components of background candidates
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(is_bg_candidate, connectivity=8)

    # Any component touching the image border is exterior background
    border_labels = set()
    border_labels.update(np.unique(labels[0, :]))
    border_labels.update(np.unique(labels[h - 1, :]))
    border_labels.update(np.unique(labels[:, 0]))
    border_labels.update(np.unique(labels[:, w - 1]))
    border_labels.discard(0)

    bg_mask = np.isin(labels, list(border_labels)).astype(np.uint8) * 255

    # Only punch out enclosed interior voids if they are either:
    # (a) pure paper-white limb/arm pass-throughs (p85_g >= 248, p25_w <= 4, area >= 120) outside the torso center, OR
    # (b) small hair-curl / loc gaps surrounded by dark hair (mean ring gray < 95).
    for lbl in range(1, num_labels):
        if lbl in border_labels:
            continue
        area = stats[lbl, cv2.CC_STAT_AREA]
        cx = stats[lbl, cv2.CC_STAT_LEFT] + stats[lbl, cv2.CC_STAT_WIDTH] * 0.5
        cy = stats[lbl, cv2.CC_STAT_TOP] + stats[lbl, cv2.CC_STAT_HEIGHT] * 0.5
        comp_mask = (labels == lbl)
        ring = cv2.dilate(comp_mask.astype(np.uint8), np.ones((7, 7), np.uint8)) - comp_mask.astype(np.uint8)
        ring_bool = (ring > 0) & (bg_mask == 0)
        ring_gray = float(np.mean(gray[ring_bool])) if ring_bool.sum() > 0 else 255.0

        # Case (b): gap between dark hair/locs in upper head region (outside central eyes)
        if cy < h * 0.30 and not (w * 0.40 <= cx <= w * 0.60 and h * 0.12 <= cy <= h * 0.24):
            if area >= 10 and ring_gray < 95.0:
                bg_mask[comp_mask] = 255
                continue

        # Case (a): pure-white enclosed background pass-through void (between arms, instrument neck, hair, etc.)
        if area >= 15 and not (w * 0.36 <= cx <= w * 0.58 and h * 0.14 <= cy <= h * 0.22):
            p85_g = float(np.percentile(gray[comp_mask], 85))
            p25_w = float(np.percentile(warmth[comp_mask], 25))
            if p85_g >= 246.0 and p25_w <= 8.0 and ring_gray < 225.0:
                bg_mask[comp_mask] = 255
                hole_dil = cv2.dilate(comp_mask.astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=1)
                bg_mask[(hole_dil > 0) & (gray >= 200) & (warmth <= 15)] = 255

    # Secondary pass strictly for small holes inside dark outer hair curls (cy < 0.29, outside earrings/shoulders)
    hair_hole_cand = ((gray >= 195) & (bg_mask == 0)).astype(np.uint8)
    zone_mask = np.zeros((h, w), dtype=np.uint8)
    zone_mask[:int(h * 0.29), :int(w * 0.36)] = 1
    zone_mask[:int(h * 0.29), int(w * 0.64):] = 1
    hair_hole_cand = hair_hole_cand & zone_mask
    nh, lh, sh_stats, _ = cv2.connectedComponentsWithStats(hair_hole_cand, connectivity=8)
    for lbl in range(1, nh):
        area = sh_stats[lbl, cv2.CC_STAT_AREA]
        if 4 <= area <= 2200:
            comp_mask = (lh == lbl)
            ring = cv2.dilate(comp_mask.astype(np.uint8), np.ones((7, 7), np.uint8)) - comp_mask.astype(np.uint8)
            ring_bool = (ring > 0) & (bg_mask == 0)
            if ring_bool.sum() > 0 and float(np.mean(gray[ring_bool])) < 145.0 and float(np.percentile(gray[comp_mask], 85)) >= 215.0:
                bg_mask[comp_mask] = 255
                hole_dil = cv2.dilate(comp_mask.astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=1)
                bg_mask[(hole_dil > 0) & (zone_mask > 0) & (gray >= 150)] = 255

    fg_mask = cv2.bitwise_not(bg_mask)

    # Choke outer boundary by 1px to remove white halo anti-aliasing along dark ink outline
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fg_choked = cv2.erode(fg_mask, kernel, iterations=1)
    alpha = cv2.GaussianBlur(fg_choked, (3, 3), 0)

    rgba = np.dstack([img_rgb, alpha])
    return Image.fromarray(rgba)


def build_sprite_and_previews(rgba_cutout: Image.Image, char_key: str, suffix: str = ""):
    cfg = CHARACTER_CONFIGS[char_key]
    tag_name = f"{char_key}_{suffix}" if suffix else char_key

    # Find tight bounding box of non-transparent pixels
    alpha_np = np.array(rgba_cutout)[:, :, 3]
    ys, xs = np.where(alpha_np > 16)
    if len(xs) == 0 or len(ys) == 0:
        raise RuntimeError("Cutout is empty!")
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    tight = rgba_cutout.crop((x0, y0, x1 + 1, y1 + 1))

    target_w, target_h = 560, 880

    # 1. Full-body 560x880 sprite (fits full standing figure with small top/bottom margin)
    fb_canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    avail_w, avail_h = target_w - 24, target_h - 16
    scale_fb = min(avail_w / tight.width, avail_h / tight.height)
    fb_w = int(round(tight.width * scale_fb))
    fb_h = int(round(tight.height * scale_fb))
    fb_resized = tight.resize((fb_w, fb_h), Image.Resampling.LANCZOS)
    fb_x = (target_w - fb_w) // 2
    fb_y = target_h - fb_h  # Bottom-anchored
    fb_canvas.alpha_composite(fb_resized, (fb_x, fb_y))

    fb_path = os.path.join(OUT_DIR, f"{tag_name}_neutral_fullbody_560x880.png")
    fb_canvas.save(fb_path)
    print(f"[SAVED] Full-body 560x880 sprite -> {fb_path}")

    # 2. Three-quarter / knees-up 560x880 sprite (crops bottom 22% of legs so head/torso/prop
    #    fill the upper 600px above the 278px dialogue box, matching existing Ren'Py sprite scale)
    crop_h = int(round(tight.height * 0.78))
    tight_3q = tight.crop((0, 0, tight.width, crop_h))
    wq_canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    scale_wq = min((target_w - 16) / tight_3q.width, (target_h - 20) / tight_3q.height)
    wq_w = int(round(tight_3q.width * scale_wq))
    wq_h = int(round(tight_3q.height * scale_wq))
    wq_resized = tight_3q.resize((wq_w, wq_h), Image.Resampling.LANCZOS)
    wq_x = (target_w - wq_w) // 2
    wq_y = target_h - wq_h  # Bottom-anchored to y=880
    wq_canvas.alpha_composite(wq_resized, (wq_x, wq_y))

    wq_path = os.path.join(OUT_DIR, f"{tag_name}_neutral_3q_560x880.png")
    wq_canvas.save(wq_path)
    print(f"[SAVED] 3/4-length 560x880 sprite -> {wq_path}")

    # 3. Scale D (Approved Default: Normalized by anatomical skull-to-chin height and eye level
    #    so Koraba's upward-pointing crown locs don't shrink his head/torso relative to Xochit & Clara)
    scale_d_params = {
        "koraba": (0.76, 1055),
        "xochit": (0.98, 990),
        "clara": (0.92, 985),
    }
    crop_ratio_d, target_hd = scale_d_params.get(char_key, (0.92, 1010))
    crop_d = tight.crop((0, 0, tight.width, int(round(tight.height * crop_ratio_d))))
    scale_d = target_hd / crop_d.height
    wd = int(round(crop_d.width * scale_d))
    im_d = crop_d.resize((wd, target_hd), Image.Resampling.LANCZOS)
    canvas_d = Image.new("RGBA", (max(700, wd + 20), target_hd), (0, 0, 0, 0))
    canvas_d.alpha_composite(im_d, ((canvas_d.width - wd) // 2, 0))

    sd_path = os.path.join(OUT_DIR, f"{tag_name}_neutral_scaleD.png")
    canvas_d.save(sd_path)
    print(f"[SAVED] Scale D (1010px tall) sprite -> {sd_path}")

    # 4. Stage previews over the character's home background + textbox.png
    bg_path = os.path.join(REPO_ROOT, "game", "images", cfg["preview_bg"])
    tb_path = os.path.join(REPO_ROOT, "game", "gui", "textbox.png")
    if os.path.exists(bg_path):
        bg = Image.open(bg_path).convert("RGBA")
        tb = Image.open(tb_path).convert("RGBA") if os.path.exists(tb_path) else None

        for label, sprite_im in [("scaleD", canvas_d), ("fullbody", fb_canvas), ("3q", wq_canvas)]:
            stage = bg.copy()
            # Center slot: xalign 0.5, yalign 1.0
            sx = (1920 - sprite_im.width) // 2
            sy = 1080 - sprite_im.height
            stage.alpha_composite(sprite_im, (sx, sy))
            if tb is not None:
                stage.alpha_composite(tb, (0, 1080 - tb.height))
            prev_path = os.path.join(OUT_DIR, f"{tag_name}_stage_preview_{label}.png")
            stage.save(prev_path)
            print(f"[SAVED] Stage preview ({label}) -> {prev_path}")


def generate_character_sprite(char_name: str, custom_prompt: str = None, suffix: str = ""):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in environment or .env!")
        sys.exit(1)

    key = char_name.lower().strip()
    if key not in CHARACTER_CONFIGS:
        print(f"[ERROR] Unknown character '{key}'. Available: {list(CHARACTER_CONFIGS.keys())}")
        sys.exit(1)

    cfg = CHARACTER_CONFIGS[key]
    prompt = custom_prompt or cfg["prompt"]
    sheet_path = os.path.join(SHEETS_DIR, cfg["sheet_file"])
    if not os.path.exists(sheet_path):
        print(f"[ERROR] Character sheet not found: {sheet_path}")
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)

    # Crop the left 53% of the character sheet (which contains the main illustrated woodcut
    # portrait and the 4 turnaround illustrations, excluding the photo inset and text blocks)
    # so the model focuses 100% on the woodcut art style and character design!
    with Image.open(sheet_path) as sheet_im:
        sw, sh = sheet_im.size
        # Tight crop around the stylized woodcut portrait face/torso and turnaround row (excluding DAO logo & background margins)
        art_crop = sheet_im.crop((int(sw * 0.06), int(sh * 0.05), int(sw * 0.50), int(sh * 0.99)))
        crop_ref_path = os.path.join(OUT_DIR, f"{key}_sheet_art_crop.png")
        art_crop.save(crop_ref_path)

    with open(crop_ref_path, "rb") as f:
        ref_b64 = base64.b64encode(f.read()).decode("utf-8")

    print(f"\n==================================================")
    print(f"Generating v3 Neutral Sprite: {key.capitalize()} (maps to {cfg['legacy_tag']})")
    print(f"Reference Sheet Crop: {crop_ref_path}")
    print(f"Estimated Cost: ${COST_PER_IMAGE_USD:.3f}")
    print(f"==================================================")

    parts = [
        {
            "inlineData": {
                "mimeType": "image/png",
                "data": ref_b64,
            }
        },
        {
            "text": (
                "Reference Image 1 shows the approved HIGHLY STYLIZED hand-carved woodcut/engraved character design and turnaround illustrations. "
                "CRITICAL STYLE LOCK: You MUST preserve the exact stylized, non-realistic woodcut facial geometry of Reference Image 1 "
                "(giant temple-to-temple heavy-lidded almond eyes, long razor-thin geometric nose, tiny narrow mouth, sharply tapered narrow chin, "
                "long slender cylindrical neck, and coarse parallel woodcut hatching). Do NOT replace the stylized face with realistic human or generic comic facial proportions!\n\n"
                "Task:\n"
                f"{prompt}\n\n"
                "Strict Negative Constraints (DO NOT INCLUDE): "
                "realistic human facial proportions, small realistic eyes, wide mouth, realistic round cheeks, generic AI illustration face, "
                "comic book anatomy, smooth airbrushed shading, dead-on symmetrical front-facing view, squared level shoulders, stiff mannequin posture, "
                "sitting pose, cross-legged pose, floating halo behind head, circular background mandala, floor rug, extra props on the ground, "
                "multiple figures, turnaround sheet layout, text, typography, labels, watermarks, photorealism, 3D rendering, gradients on background."
            )
        }
    ]

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
            "imageConfig": {
                "aspectRatio": "3:4"
            }
        }
    }

    response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=120)
    if response.status_code != 200:
        print(f"[WARN] Request with imageConfig returned {response.status_code}, retrying without imageConfig...")
        payload_fallback = {"contents": [{"parts": parts}]}
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload_fallback, timeout=120)
        if response.status_code != 200:
            print(f"[ERROR] API request failed ({response.status_code}): {response.text}")
            sys.exit(1)

    res_json = response.json()
    candidates = res_json.get("candidates", [])
    if not candidates:
        print(f"[ERROR] No candidates returned: {res_json}")
        sys.exit(1)

    img_bytes = None
    mime_out = "image/jpeg"
    for p in candidates[0].get("content", {}).get("parts", []):
        if "inlineData" in p:
            img_bytes = base64.b64decode(p["inlineData"]["data"])
            mime_out = p["inlineData"].get("mimeType", "image/jpeg")
            break

    if not img_bytes:
        print(f"[ERROR] No image returned in response parts: {candidates[0]}")
        sys.exit(1)

    ext = ".png" if "png" in mime_out.lower() else ".jpg"
    tag_name = f"{key}_{suffix}" if suffix else key
    raw_path = os.path.join(OUT_DIR, f"{tag_name}_neutral_raw{ext}")
    with open(raw_path, "wb") as f:
        f.write(img_bytes)
    print(f"[RAW OK] Saved raw render -> {raw_path}")

    log_usage(tag_name, prompt, COST_PER_IMAGE_USD)

    rgba_cutout = extract_clean_cutout(raw_path)
    build_sprite_and_previews(rgba_cutout, key, suffix=suffix)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate v3 character neutral sprite")
    parser.add_argument("character", choices=["koraba", "xochit", "clara"], help="Character to generate")
    parser.add_argument("--prompt", help="Optional custom prompt override")
    parser.add_argument("--suffix", default="", help="Optional suffix for A/B comparison")
    args = parser.parse_args()
    generate_character_sprite(args.character, custom_prompt=args.prompt, suffix=args.suffix)
