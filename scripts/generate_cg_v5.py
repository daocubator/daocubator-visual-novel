#!/usr/bin/env python3
"""
generate_cg_v5.py
Economical, style-locked 16:9 Outcome CG generator (Episodes 1-4 Disaster & Happy pairs).

Key fixes over v3/v4:
1. 3 SEPARATE high-res character references (Koraba, Xochit, Clara) instead of a 3-in-1 lineup sheet,
   eliminating lineup bias and giving 3x character detail.
2. Approved keeper `cg_ep1_disaster_v3c_raw.jpg` as Image 4 (Scene Style & Palette Anchor).
3. Optional `--layout-ref` (Image 5) to reuse strong existing compositions (e.g. ep3_disaster_full2_v4.png
   or ep4_disaster_512_expB.jpg) while redrawing characters & style to match Images 1-4.
4. Balanced expressiveness: keeps woodcut geometric faces (heavy-lidded almond eyes, carved hatching)
   while using brow angles, head tilt, body lean, and dynamic 3-plane camera blocking for thumbnail impact.
5. `--size 512` ($0.015/img) for cheap iteration; `--size full` ($0.030/img) for 1920x1080 + canvas weave
   + thumbnails + scenario cards.
"""

import argparse
import base64
import io
import json
import os
import sys
from datetime import datetime, timezone
import numpy as np
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SPRITES_V3_DIR = os.path.join(REPO_ROOT, "vault", "06 Assets", "generated_sprites", "v3")
OUT_DIR = os.path.join(REPO_ROOT, "vault", "06 Assets", "generated_cgs", "v3")
V5_OUT_DIR = os.path.join(REPO_ROOT, "vault", "06 Assets", "generated_cgs", "v5")
CANVAS_TEX_PATH = os.path.join(REPO_ROOT, "vault", "06 Assets", "style_references", "create-flat-evenly-lit-ada66b.png")
STYLE_ANCHOR_PATH = os.path.join(REPO_ROOT, "vault", "06 Assets", "style_references", "original_sheet_style_swatch.png")
USAGE_LOG_PATH = os.path.join(REPO_ROOT, "vault", "06 Assets", "generation_usage_log.json")

MODEL = "gemini-3.1-flash-image"
COST_512_USD = 0.015
COST_FULL_USD = 0.030

SHARED_CG_STYLE = (
    "Full-bleed 16:9 cinematic visual novel event CG illustration combining TWO distinct material treatments:\n"
    "1) CHARACTERS: Render Koraba, Xochit, and Clara in the EXACT hand-carved woodcut / folk-engraving style "
    "and geometric facial proportions of Reference Images 1, 2, and 3 (large heavy-lidded half-moon almond eyes, "
    "long thin geometric noses, small mouths, bold black/umber etched contours, coarse parallel woodcut hatching). "
    "All three characters are equal adult human scale (do NOT make Xochit larger just because her reference crop is closer). "
    "Express strong emotion through angled/furrowed brows, head tilt, tense shoulders, and urgent hand gestures—NOT through "
    "realistic comic-book faces, wide-open screaming mouths, or bulging eyes. "
    "Ensure natural human arm, wrist, and 5-fingered hand anatomy with realistic sleeve/cuff perspective (exactly two arms total per character).\n"
    "2) ENVIRONMENT & ATMOSPHERE: Match the exact woodcut-plus-watercolor-wash material balance of Reference Image 4 "
    "(bold carved ink on foreground characters/props, loose wet-on-wet tea/coffee watercolor washes on warm ivory paper in the background).\n"
    "3) DYNAMIC CAMERA & THUMBNAIL READ: Use the 3-plane depth layout (Foreground / Midground / Background at distinct scales) "
    "described in the scene prompt. Characters may be cropped by frame edges, seen in 3/4 view, or over-the-shoulder, "
    "as long as their signature silhouette/costume/prop remains recognizable. One clear focal action, readable at 512x288 thumbnail size. "
    "Fill the 16:9 frame edge-to-edge. ABSOLUTELY NO text, letters, numbers, readable screens, logos, or watermarks."
)

DISASTER_POLARITY = (
    "MOOD: DISASTER. Dark, tilted, urgent, cold midnight indigo, charcoal, and bruised crimson tea washes. "
    "Characters show shock, grief, tension, or conflict through furrowed brows, recoiling/lunging posture, and urgent hands."
)

HAPPY_POLARITY = (
    "MOOD: GOOD ENDING. Bright, open, warm golden chamomile and amber washes. "
    "Characters show relief, pride, and solidarity through relaxed brows, warm eye contact, and open cooperative gestures."
)

CG_CONFIGS = {
    "cg_ep1_happy": {
        "ep_id": "ep1_keys",
        "mood": "happy",
        "prompt": (
            "Scene: Episode 1 Good Outcome — 'The $1 Test Transfer Lands & 2-of-3 Shared Custody' at Lisbon Airport.\n"
            "CAMERA: Dynamic low-angle diagonal shot from just above the wooden elixir crate looking slightly up at the trio gathered in a close, celebratory huddle, with warm golden dawn sunbeams streaming through tall airport terminal glass behind them.\n"
            "DECISIVE MOMENT: A small smartphone rests flat and solidly on top of the closed wooden elixir crate, its screen emitting a warm golden star-shaped glow upward onto their faces (no text). All three lean in together with genuine, relieved smiles, rendered with strongly stylized, angular, hand-carved wooden mask facial planes, bold woodcut ink hatching, and sculptural brow and cheekbone ridges (not generic smooth comic faces).\n"
            "DEPTH: FOREGROUND, the corner of the sturdy wooden elixir crate with the glowing phone resting flat on its surface. "
            "MIDGROUND LEFT, Koraba (dark crown locs, woven wrap, his single straight-necked round gourd kora strapped diagonally across his back with the straight neck and round gourd body cleanly aligned in one continuous unbroken line) leaning forward over the crate with a joyful, relieved smile, one hand resting on the crate. "
            "MIDGROUND CENTER, Clara (blonde coiled side bun, slate-blue blazer, red lanyard) leaning in with a warm, relieved smile, extending the brass hardware key forward over the glowing phone. "
            "MIDGROUND RIGHT, Xochit (red/gold beaded headband, red/black face paint, diamond earrings, patterned huipil) leaning in with a proud, warm smile, cradling her star-carved cacao bowl."
        ),
    },
    "cg_ep2_disaster": {
        "ep_id": "ep2_lisbon",
        "mood": "disaster",
        "prompt": (
            "Scene: Episode 2 Disaster — 'The Showcase Freezes' backstage at the Lisbon venue.\n"
            "CAMERA: Low over-the-shoulder shot from behind Clara's right shoulder, looking down a diagonal folding production table.\n"
            "DECISIVE MOMENT: Koraba defiantly raises his arm high as he yanks a thick instrument/amplifier jack cable completely out of the amplifier on the table to end the show, while Clara blocks with a raised hand and closed ledger.\n"
            "DEPTH: FOREGROUND RIGHT, Clara's slate-blue blazer shoulder, back of her head, raised blocking hand, and closed ledger, cropped at the right frame edge. "
            "MIDGROUND LEFT, Koraba leaning across the table, locking defiant eye contact directly onto Clara with brows furrowed in bitter resolve; his right arm is raised high holding the unplugged instrument cable end he just yanked from the amplifier on the table, and his left hand rests on the table (only two arms total), with his straight-necked round gourd kora strapped across his back. "
            "BACKGROUND CENTER, Xochit stepping between them, looking directly toward Clara (foreground right) with a concerned, pleading-yet-frustrated expression—directing her frustration at Clara, not Koraba—harsh cold stage spotlights spilling through parted backstage curtains behind her."
        ),
    },
    "cg_ep2_happy": {
        "ep_id": "ep2_lisbon",
        "mood": "happy",
        "prompt": (
            "Scene: Episode 2 Good Outcome — 'The Work Speaks for Itself' on the Lisbon Showcase Stage.\n"
            "CAMERA: Extreme low-angle worm's-eye shot from the pit looking steeply UP at the stage, making the trio tower larger-than-life against a massive glowing circular golden watercolor mandala and star constellation projection screen (no text).\n"
            "DECISIVE MOMENT: Koraba, towering at center stage, leans back in a sweeping, triumphant performance pose—head tilted up with a radiant, joyful smile (preserving his chiseled, carved woodcut-mask facial structure and hatching), one knee bent on a stage riser, raising and strumming his single straight-necked round gourd kora high across his chest; Xochit on the left beams with a proud, warm smile (keeping her carved woodcut-mask facial features) as she thrusts the unrolled neutral-avatar scroll high into the golden spotlight; Clara on the right steps up beside them with a warm, celebratory smile, lowering her closed ledger and raising a hand in solidarity.\n"
            "DEPTH: 4TH FOREGROUND LAYER (bottom edge), only the dark silhouettes of the tops of the audience's heads barely visible along the very bottom rim of the frame. "
            "STAGE HERO CENTER, Koraba towering and rim-lit against the glowing golden mandala. "
            "STAGE LEFT, Xochit in dramatic 3/4 low-angle view raising the scroll. "
            "STAGE RIGHT, Clara in 3/4 low-angle view with her ledger lowered at her side. "
            "Golden stage wash, dramatic backlighting and long stage shadows, NO duplicate instruments."
        ),
    },
    "cg_ep3_disaster": {
        "ep_id": "ep3_agreements",
        "mood": "disaster",
        "prompt": (
            "Scene: Episode 3 Disaster — 'The Handshake Split Collapses' at the ceremonial cacao circle.\n"
            "CAMERA: Steep high-angle Dutch-tilt shot looking down across the ceremonial cacao table.\n"
            "DECISIVE MOMENT: A dark-suited arm from the right edge slams a thick stack of papers with a red wax seal onto the table, overturning the carved cacao bowl; dark cacao spills toward the bottom-left and round token discs scatter through the air.\n"
            "DEPTH: FOREGROUND, the overturning cacao bowl, spilling cacao river, scattering token discs, and the suited arm slamming the blank-lined summons papers (NO text or letters on papers or cuff). "
            "MIDGROUND, Koraba (left, his straight-necked kora resting behind him against his chair, clear of his hands) hunched forward in grief with one hand gripping his forehead and the other bracing on the empty table, brows sharply furrowed; "
            "Xochit (center) recoiling backward in shock with one hand clutching her chest and the other raised defensively toward the suited arm, brows furrowed. "
            "BACKGROUND TOP, Clara small, hands pressed to her head in defeat."
        ),
    },
    "cg_ep3_happy": {
        "ep_id": "ep3_agreements",
        "mood": "happy",
        "prompt": (
            "Scene: Episode 3 Good Outcome — 'The Agreement Holds' at the ceremonial cacao circle.\n"
            "CAMERA: Steep overhead bird's-eye shot looking straight down onto the round ceremonial cacao table, creating a dynamic radial composition.\n"
            "DECISIVE MOMENT: At the center of the table, the unrolled cooperative charter scroll (blank decorative lines only, NO readable text) is being stamped with the four-point-star cooperative stamp by Clara's hand from the left, while Koraba's hand (top-right) and Xochit's hand (bottom-right) sign with pens from opposite angles, forming a tight, unified triangle of action.\n"
            "DEPTH: TABLETOP CENTER, the charter scroll, the four-point-star stamp, the steaming star-carved cacao bowl (top-left), and the glass treasury reserve jar filled with golden tokens (bottom-left). "
            "AROUND THE TABLE EDGE, Clara, Koraba (with his straight-necked round gourd kora strapped cleanly across his back, the straight neck and round gourd body cleanly aligned in one continuous unbroken line), and Xochit lean in from three sides, their smiling faces (rendered with strongly stylized, angular, hand-carved wooden mask facial planes and bold woodcut ink hatching) looking down warmly at the signed charter. Warm dawn chamomile gold wash."
        ),
    },
    "cg_ep4_disaster": {
        "ep_id": "ep4_apothecary",
        "mood": "disaster",
        "prompt": (
            "Scene: Episode 4 Disaster — 'One Tired Click Drained the Apothecary' at 1:14 A.M.\n"
            "CAMERA: Dramatic close-to-midground shot inside the candlelit herbal apothecary.\n"
            "DECISIVE MOMENT: Exhausted Clara recoils in horror as her hand leaves the laptop keyboard; a sinister dark espresso-and-crimson vortex swirls upward from the laptop/open treasury chest, draining glowing golden tokens.\n"
            "DEPTH: FOREGROUND LEFT, Clara in 3/4 profile at her desk, exhausted, eyes wide with furrowed brows, hand pulling back from the laptop. "
            "MIDGROUND CENTER, the single glowing laptop (only one laptop in the entire scene) and open wooden treasury chest with the dark crimson vortex of golden tokens rising. "
            "BACKGROUND RIGHT, Xochit leaning across the counter in alarm and Koraba bursting through the rain-streaked doorway with his straight-necked gourd kora strapped on his back."
        ),
    },
    "cg_ep4_happy": {
        "ep_id": "ep4_apothecary",
        "mood": "happy",
        "prompt": (
            "Scene: Episode 4 Good Outcome — 'The Hex Is Caught in Time' in the Herbal Apothecary.\n"
            "CAMERA: Dramatic, tilted low-angle Dutch-angle shot from desk level right behind the glowing treasury vessel, looking steeply up at the trio framed by towering apothecary shelves and warm golden sunbeams streaming through the tall window.\n"
            "DECISIVE MOMENT: Clara raises a small hardware wallet device into the light for Koraba and Xochit to verify together, while a luminous golden timelock shield ring around the treasury vessel on the desk deflects a dark outer ink stain. All three share relieved, triumphant smiles, rendered with strongly stylized, angular, hand-carved wooden mask facial planes and bold woodcut ink hatching.\n"
            "DEPTH: FOREGROUND, the carved treasury vessel encircled by a blazing golden timelock shield ring on the angled desk, deflecting a dark stain. "
            "MIDGROUND, Clara (right, holding the hardware wallet up with her two hands—only two arms total—beaming with relief), Xochit (center, pointing triumphantly at the device with a proud smile), and Koraba (left, leaning in with a relieved smile, his straight-necked round gourd kora resting intact against the apothecary shelf behind him). "
            "BACKGROUND, tall apothecary shelves of herbal bottles bathed in warm golden daylight."
        ),
    },
}


def img_part(path: str, max_dim: int = None) -> dict:
    im = Image.open(path).convert("RGB")
    if max_dim:
        im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=92)
    return {"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(buf.getvalue()).decode("utf-8")}}


def log_usage(tag_name: str, prompt: str, cost: float):
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
        "asset": f"{tag_name} (v5 CG)",
        "model": MODEL,
        "cost_usd": cost,
        "cumulative_spent_usd": log_data["total_spent_usd"],
        "prompt_snippet": prompt[:120] + "...",
    })
    os.makedirs(os.path.dirname(USAGE_LOG_PATH), exist_ok=True)
    with open(USAGE_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)
    print(f"[USAGE] {tag_name}: ${cost:.3f} | Cumulative: ${log_data['total_spent_usd']:.3f} ({log_data['total_images']} imgs)")


def apply_subtle_canvas_to_cg(raw_path: str, out_1080_path: str) -> Image.Image:
    with Image.open(raw_path) as raw_im:
        cg_1080 = raw_im.convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
    cg_np = np.asarray(cg_1080, dtype=np.float32)

    if os.path.exists(CANVAS_TEX_PATH):
        with Image.open(CANVAS_TEX_PATH) as tex_im:
            tex_1080 = tex_im.convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
        tex_np = np.asarray(tex_1080, dtype=np.float32)
        tex_luma = (0.299 * tex_np[:, :, 0] + 0.587 * tex_np[:, :, 1] + 0.114 * tex_np[:, :, 2]) / 255.0
        weave_centered = (tex_luma - float(np.mean(tex_luma)))[..., None]
        cg_luma = (0.299 * cg_np[:, :, 0] + 0.587 * cg_np[:, :, 1] + 0.114 * cg_np[:, :, 2]) / 255.0
        paper_weight = np.clip((cg_luma - 0.18) / 0.72, 0.0, 1.0)[..., None]
        ground_blend = cg_np * (1.0 - 0.22 * paper_weight) + tex_np * (0.22 * paper_weight)
        out_np = np.clip(ground_blend * (1.0 + weave_centered * (0.48 * paper_weight)), 0.0, 255.0).astype(np.uint8)
        final_im = Image.fromarray(out_np)
    else:
        final_im = cg_1080

    final_im = final_im.filter(ImageFilter.UnsharpMask(radius=0.7, percent=35, threshold=2))
    final_im.save(out_1080_path, format="PNG")
    return final_im


def build_thumb_and_scenario_card(cg_1080: Image.Image, cg_key: str, ver_suffix: str = ""):
    cfg = CG_CONFIGS[cg_key]
    thumb_im = cg_1080.resize((512, 288), Image.Resampling.LANCZOS)
    thumb_game = os.path.join(REPO_ROOT, "game", "images", f"{cg_key}_thumb.png")
    thumb_im.save(os.path.join(V5_OUT_DIR, f"{cg_key}{ver_suffix}_thumb.png"))
    thumb_im.save(thumb_game)

    card_w, card_h = 512, 285
    card_rgb = cg_1080.resize((card_w, card_h), Image.Resampling.LANCZOS).convert("RGBA")
    grad_np = np.zeros((card_h, card_w, 4), dtype=np.uint8)
    for y in range(card_h - 90, card_h):
        t = (y - (card_h - 90)) / 89.0
        grad_np[y, :, :3] = [24, 14, 9]
        grad_np[y, :, 3] = int(round(215 * (t ** 1.35)))
    card_rgba = Image.alpha_composite(card_rgb, Image.fromarray(grad_np))

    mask = Image.new("L", (card_w * 2, card_h * 2), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, card_w * 2 - 1, card_h * 2 - 1), radius=28, fill=255)
    card_rgba.putalpha(mask.resize((card_w, card_h), Image.Resampling.LANCZOS))

    card_name = f"scenario_card_{cfg['ep_id']}_{cfg['mood']}.png"
    card_v5_name = f"scenario_card_{cfg['ep_id']}_{cfg['mood']}{ver_suffix}.png"
    card_rgba.save(os.path.join(V5_OUT_DIR, card_v5_name))
    card_rgba.save(os.path.join(REPO_ROOT, "game", "images", card_name))
    print(f"[SAVED] {cg_key} -> game/images/ (1080p, thumb, scenario_card)")


def generate_one(cg_key: str, size: str = "512", layout_ref: str = None, suffix: str = ""):
    load_dotenv(os.path.join(REPO_ROOT, ".env"))
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("[ERROR] GEMINI_API_KEY not found in .env")

    cfg = CG_CONFIGS[cg_key]
    polarity = DISASTER_POLARITY if cfg["mood"] == "disaster" else HAPPY_POLARITY

    parts = [
        {"text": "CHARACTER REFERENCE 1 — KORABA (STRICTLY copy his exact face, heavy-lidded almond eyes, dark crown locs, woven wrap, and straight-necked gourd kora; do NOT alter his face or add accessories):"},
        img_part(os.path.join(SPRITES_V3_DIR, "koraba_v3e_neutral_raw.jpg"), 1024),
        {"text": "CHARACTER REFERENCE 2 — XOCHIT (STRICTLY copy her exact face, heavy-lidded almond eyes, red/black face paint, red/gold beaded headband, diamond earrings, and patterned huipil; do NOT alter her face):"},
        img_part(os.path.join(SPRITES_V3_DIR, "xochit_v3d_neutral_raw.jpg"), 1024),
        {"text": "CHARACTER REFERENCE 3 — CLARA (STRICTLY copy her exact face, heavy-lidded almond eyes, blonde coiled side bun, slate-blue blazer, and red lanyard; NO glasses, NO unprompted accessories):"},
        img_part(os.path.join(SPRITES_V3_DIR, "clara_v3c_neutral_raw.jpg"), 1024),
        {"text": "STYLE & PALETTE REFERENCE ONLY (match this woodcut hatching weight and watercolor tea-wash background texture; do NOT copy its camera angle or character positions):"},
        img_part(STYLE_ANCHOR_PATH, 1024),
    ]

    if layout_ref:
        parts.append({
            "text": (
                "COMPOSITION & LAYOUT REFERENCE ONLY (keep ONLY the camera angle, perspective, and prop placement; "
                "DO NOT copy any faces, hairstyles, glasses, or clothing from this image—replace every character with Koraba, Xochit, and Clara from Character References 1-3):"
            )
        })
        parts.append(img_part(layout_ref, 1024))

    parts.append({"text": f"{SHARED_CG_STYLE}\n\n{polarity}\n\n{cfg['prompt']}"})

    img_cfg = {"aspectRatio": "16:9"}
    if size == "512":
        img_cfg["imageSize"] = "512"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key}"
    resp = requests.post(
        url,
        json={"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE", "TEXT"], "imageConfig": img_cfg}},
        timeout=180,
    )
    if resp.status_code != 200:
        sys.exit(f"[ERROR] {resp.status_code}: {resp.text[:400]}")

    img_bytes = None
    for p in resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in p:
            img_bytes = base64.b64decode(p["inlineData"]["data"])
            break
    if not img_bytes:
        sys.exit(f"[ERROR] No image returned: {resp.text[:400]}")

    os.makedirs(V5_OUT_DIR, exist_ok=True)
    base_tag = f"{cg_key}_{size}" + (f"_{suffix}" if suffix else "")
    tag = base_tag
    ver_suffix = ""
    raw_path = os.path.join(V5_OUT_DIR, f"{tag}_raw.jpg")
    if os.path.exists(raw_path):
        idx = 2
        while os.path.exists(os.path.join(V5_OUT_DIR, f"{base_tag}_v{idx}_raw.jpg")):
            idx += 1
        ver_suffix = f"_v{idx}"
        tag = f"{base_tag}{ver_suffix}"
        raw_path = os.path.join(V5_OUT_DIR, f"{tag}_raw.jpg")
    with open(raw_path, "wb") as f:
        f.write(img_bytes)

    cost = COST_512_USD if size == "512" else COST_FULL_USD
    log_usage(tag, cfg["prompt"], cost)
    print(f"[REVIEW] {raw_path}")

    if size == "full":
        out_1080 = os.path.join(V5_OUT_DIR, f"{cg_key}{ver_suffix}.png")
        cg_1080 = apply_subtle_canvas_to_cg(raw_path, out_1080)
        cg_1080.save(os.path.join(REPO_ROOT, "game", "images", f"{cg_key}.png"))
        build_thumb_and_scenario_card(cg_1080, cg_key, ver_suffix=ver_suffix)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate v5 Full-Art 16:9 Outcome CGs")
    parser.add_argument("cg_keys", nargs="+", choices=list(CG_CONFIGS.keys()) + ["all"], help="CG key(s) or 'all'")
    parser.add_argument("--size", choices=["512", "full"], default="512", help="512 ($0.015) for draft, full ($0.030) for 1080p final")
    parser.add_argument("--layout-ref", help="Optional path to a composition/layout reference image (Image 5)")
    parser.add_argument("--suffix", default="", help="Optional filename suffix")
    args = parser.parse_args()

    keys = list(CG_CONFIGS.keys()) if "all" in args.cg_keys else args.cg_keys
    for k in keys:
        generate_one(k, size=args.size, layout_ref=args.layout_ref, suffix=args.suffix)
