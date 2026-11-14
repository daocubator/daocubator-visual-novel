#!/usr/bin/env python3
"""
generate_cg_v3.py
Generates v3 Full-Art 16:9 (1920x1080) Outcome CGs (Episodes 1-4 Disaster & Happy pairs)
combining the approved EFAM DAO stylized woodcut characters (Koraba, Xochit, Clara)
with the Pass 3A tea/coffee watercolor wash + macro-canvas world.
Also outputs the 16:9 thumbnail (*_thumb.png) and Constellation scenario card (scenario_card_*.png).
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
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SPRITES_V3_DIR = os.path.join(REPO_ROOT, "vault", "06 Assets", "generated_sprites", "v3")
OUT_DIR = os.path.join(REPO_ROOT, "vault", "06 Assets", "generated_cgs", "v3")
CANVAS_TEX_PATH = os.path.join(REPO_ROOT, "vault", "06 Assets", "style_references", "create-flat-evenly-lit-ada66b.png")
USAGE_LOG_PATH = os.path.join(REPO_ROOT, "vault", "06 Assets", "generation_usage_log.json")

COST_PER_IMAGE_USD = 0.030

SHARED_CG_STYLE = (
    "Full-bleed 16:9 visual novel event CG illustration combining TWO distinct material treatments:\n"
    "1) CHARACTERS (FOREGROUND): Render Koraba, Xochit, and Clara in the EXACT HIGHLY STYLIZED, flat-plane hand-carved "
    "woodcut / folk-engraving style and non-realistic geometric facial proportions shown in Reference Image 1 "
    "(GIANT oversized heavy-lidded half-moon horizontal almond eyes spanning temple-to-temple, long razor-thin vertical geometric noses, "
    "tiny narrow mouths, sharply tapered narrow chins, long slender cylindrical necks, bold black/umber etched contours, "
    "and coarse parallel woodcut hatching in warm ochre, antique ivory, slate-blue, and terracotta).\n"
    "2) ENVIRONMENT & ATMOSPHERE (BACKGROUND/MIDGROUND): Render the surrounding setting in the loose, line-free wet-on-wet "
    "tea, coffee, and watercolor stain wash style of Reference Image 2 on warm antique ivory paper (with capillary blooms, "
    "tide rings, and negative-space light pockets, enriched with deeper umber, charcoal, crimson, or golden wash accents for dramatic impact).\n"
    "3) COMPOSITION & FRAMING RULES (CRITICAL): Decisive visual-novel event panel composition filling the ENTIRE 16:9 frame edge-to-edge "
    "from top to bottom (100% full-bleed artwork). Frame the characters from the knees/hips up so their lower garments, crates, tables, "
    "and floor extend continuously all the way to the very bottom edge of the 16:9 canvas (ABSOLUTELY NO horizontal cutoff line, "
    "NO border line, and NO empty margin strip at the bottom of the image!), while keeping faces, hands, and key props in the upper two-thirds. "
    "Characters must interact dynamically with each other and the scene (NOT standing in stiff symmetrical lineup and NOT staring at the camera). "
    "ABSOLUTELY NO text, NO letters, NO numbers, NO readable screens, NO UI labels, NO watermarks."
)

CG_CONFIGS = {
    "cg_ep1_disaster": {
        "ep_id": "ep1_keys",
        "mood": "disaster",
        "bg_ref": "bg lisbon_airport.png",
        "prompt": (
            "Scene: Episode 1 Disaster — 'The $60,000 Transfer Is Gone' at Lisbon Airport after midnight.\n"
            "Action & Staging (Upper Two-Thirds): In a rain-streaked airport customs terminal at night, "
            "Koraba (center-left, dark crown locs, beaded strands, ochre/indigo woven wrap, kora instrument strapped across his shoulder) "
            "stands stunned beside wooden shipping crates of herbal elixirs behind a customs barrier tape, one hand gripping his kora strap "
            "and the other holding up a small dark phone with a blank pale empty screen (NO text or numbers on the phone). "
            "Xochit (center-right, red/gold beaded headband, red/black cheek & chin face paint, diamond fringe earrings, woven huipil) "
            "turns toward Koraba with her hands raised to her chest in shock and grief. "
            "Clara (right, blonde coiled side bun, slate-blue patterned blazer, red lanyard) stands slightly apart clutching a closed ledger "
            "and a single brass/hardware key tightly against her chest, looking away in helpless guilt unable to undo the lost transfer. "
            "Atmosphere & Palette: Tense midnight indigo-grey, scorched espresso-umber, and bruised crimson-amber watercolor washes "
            "streaking down the tall rain-wet terminal windows behind them, angling toward the stranded crates."
        ),
    },
    "cg_ep1_happy": {
        "ep_id": "ep1_keys",
        "mood": "happy",
        "bg_ref": "bg lisbon_airport.png",
        "prompt": (
            "Scene: Episode 1 Good Outcome — 'The $1 Test Transfer Lands & 2-of-3 Shared Custody' at Lisbon Airport.\n"
            "Action & Staging (Upper Two-Thirds): At the Lisbon airport customs area, all three gather closely in a warm, relieved circle "
            "around a small phone held at chest height emitting a soft, warm golden star-shaped confirmation glow (NO text or numbers). "
            "Koraba (left, with his gourd kora instrument) and Xochit (right, holding her carved star cacao bowl) exchange warm, relieved "
            "eye contact across the glowing phone, while Clara (center, in her slate-blue blazer) extends her hand forward offering the "
            "shared 2-of-3 hardware key token in a gesture of cooperative trust. "
            "Behind them, the wooden herbal elixir crates sit open and cleared through customs as warm golden dawn chamomile and amber tea washes "
            "break through the airport terminal glass."
        ),
    },
    "cg_ep2_disaster": {
        "ep_id": "ep2_lisbon",
        "mood": "disaster",
        "bg_ref": "bg showcase_backstage.png",
        "prompt": (
            "Scene: Episode 2 Disaster — 'The Showcase Freezes' backstage at the Lisbon venue.\n"
            "Action & Staging (Upper Two-Thirds): Backstage minutes before the Lisbon Showcase doors open, a dramatic triangle of conflict: "
            "Exhausted Koraba (left, wearing his woven wrap and kora) reaches angrily toward a laptop on a folding production table to unplug "
            "and pull his finished game offline. Clara (right, in her slate-blue blazer) blocks the table with a closed ledger and raised hand, "
            "freezing his payout. Xochit (center, in her patterned huipil and red/black face paint) steps decisively between Koraba and Clara "
            "with both hands raised outward to stop the collapse. "
            "Atmosphere & Palette: Harsh, cold empty stage spotlights spill through the parted backstage curtain above them against dark "
            "charcoal-sepia and tense amber-crimson washes; coiled cables and road cases in the lower frame. No readable text on screens."
        ),
    },
    "cg_ep2_happy": {
        "ep_id": "ep2_lisbon",
        "mood": "happy",
        "bg_ref": "bg showcase_stage.png",
        "prompt": (
            "Scene: Episode 2 Good Outcome — 'The Work Speaks for Itself' on the Lisbon Showcase Stage.\n"
            "Action & Staging (Upper Two-Thirds): In the warm, luminous golden spill of the saved Lisbon Showcase stage, "
            "a large circular projection screen behind them glows with a radiant watercolor mandala/constellation wash (no text). "
            "In the foreground, Koraba (center, playing his gourd kora with joy and pride), Xochit (left, holding up the anonymous neutral-avatar "
            "scroll/papers with a warm, vindicated smile), and Clara (right, lowering her ledger with an expression of humble accountability "
            "and respect, offering a supportive hand toward Koraba's shoulder) stand united in a linked gesture of cooperative solidarity. "
            "Atmosphere & Palette: Luminous chamomile gold, warm amber stage light, and soft Earl Grey sepia washes."
        ),
    },
    "cg_ep3_disaster": {
        "ep_id": "ep3_agreements",
        "mood": "disaster",
        "bg_ref": "bg cacao_circle.png",
        "prompt": (
            "Scene: Episode 3 Disaster — 'The Handshake Split Collapses' at the ceremonial cacao circle.\n"
            "Action & Staging (Upper Two-Thirds): Around the ceremonial cacao gathering table, the sacred circle is shattered by legal and financial shock: "
            "A stack of heavy legal summons papers with a red wax/ribbon seal slams down across the woven altar cloth, knocking over the carved "
            "cacao bowl as dark cacao spills across the table and a cascade of falling circular token discs scatters downward like dead leaves. "
            "Koraba (left) and Xochit (center) reach out in alarm toward the spilled cacao bowl and scattered papers, while Clara (right) "
            "holds her head/ledger in dismay as the consequences close in. "
            "Atmosphere & Palette: Collision of warm ceremonial ochre with cold slate-charcoal and bruised crimson tea stains; no legible text."
        ),
    },
    "cg_ep3_happy": {
        "ep_id": "ep3_agreements",
        "mood": "happy",
        "bg_ref": "bg cacao_circle.png",
        "prompt": (
            "Scene: Episode 3 Good Outcome — 'The Agreement Holds' at the ceremonial cacao circle.\n"
            "Action & Staging (Upper Two-Thirds): Gathered around the ceremonial cacao table in warm dawn light, "
            "Koraba (left) and Xochit (right) sign a large, formal cooperative charter scroll laid open beside the steaming star-carved cacao bowl "
            "and a sturdy glass treasury reserve jar filled with golden coins/tokens. Clara (center, between them) holds the official four-point-star "
            "cooperative stamp/seal and shared ledger as an accountable steward. "
            "Atmosphere & Palette: Harmonious golden chamomile, warm terracotta, and rich coffee-amber washes with interwoven textile geometry."
        ),
    },
    "cg_ep4_disaster": {
        "ep_id": "ep4_apothecary",
        "mood": "disaster",
        "bg_ref": "bg treasury_fire.png",
        "prompt": (
            "Scene: Episode 4 Disaster — 'One Tired Click Drained the Apothecary' at 1:14 A.M.\n"
            "Action & Staging (Upper Two-Thirds): Inside Clara's candlelit herbal apothecary late at night, "
            "exhausted Clara (foreground right, hair slightly disheveled from fatigue, eyes wide in horror) recoils as her finger leaves "
            "a laptop key—a sinister dark espresso-and-crimson stain current swirls upward out of an open treasury vessel on the desk, "
            "draining glowing golden tokens away into a dark vortex. "
            "In the upper-left midground doorway behind her, Koraba and Xochit burst into the room with urgent, alarmed gestures trying to stop the click. "
            "Atmosphere & Palette: High-contrast sinister crimson hibiscus-tea, scorched espresso-soot, and flickering candle amber washes; no readable UI text."
        ),
    },
    "cg_ep4_happy": {
        "ep_id": "ep4_apothecary",
        "mood": "happy",
        "bg_ref": "bg apothecary.png",
        "prompt": (
            "Scene: Episode 4 Good Outcome — 'The Hex Is Caught in Time' in the Herbal Apothecary.\n"
            "Action & Staging (Upper Two-Thirds): At the apothecary signing desk surrounded by shelves of herbal elixir bottles and dried herbs, "
            "Clara (center) holds up a small hardware wallet device angled toward Koraba (left) and Xochit (right) so all three inspect and verify "
            "it together as a team. Around the shared treasury vessel on the desk, a luminous golden protective ring (timelock shield motif) "
            "blocks and dissolves a dark outer stain at a crisp boundary. "
            "Atmosphere & Palette: Calm, triumphant golden daylight chamomile, sage-amber, and warm sepia watercolor washes."
        ),
    },
}


def log_usage(cg_name: str, prompt: str, cost: float = COST_PER_IMAGE_USD):
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
        "asset": f"{cg_name} (v3 full-art 16:9 CG)",
        "model": "gemini-3.1-flash-image",
        "cost_usd": cost,
        "cumulative_spent_usd": log_data["total_spent_usd"],
        "prompt_snippet": prompt[:120] + "..."
    })

    os.makedirs(os.path.dirname(USAGE_LOG_PATH), exist_ok=True)
    with open(USAGE_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

    print(f"[USAGE] Logged generation for {cg_name}. Cumulative spend: ${log_data['total_spent_usd']:.3f} ({log_data['total_images']} images)")


def build_cast_reference_sheet() -> str:
    """
    Combines the upper-body portraits of the approved stylized woodcut sprites
    (Koraba v3e, Xochit v3d, Clara v3c) into one clean 3-panel reference image
    so Gemini locks onto all three characters' exact stylized EFAM DAO woodcut designs.
    """
    os.makedirs(OUT_DIR, exist_ok=True)
    ref_path = os.path.join(OUT_DIR, "cast_stylized_woodcut_ref.jpg")
    if os.path.exists(ref_path):
        return ref_path

    panels = [
        ("Koraba", os.path.join(SPRITES_V3_DIR, "koraba_v3e_neutral_raw.jpg"), (0, 0, 896, 780)),
        ("Xochit", os.path.join(SPRITES_V3_DIR, "xochit_v3d_neutral_raw.jpg"), (0, 0, 896, 960)),
        ("Clara", os.path.join(SPRITES_V3_DIR, "clara_v3c_neutral_raw.jpg"), (0, 0, 896, 760)),
    ]
    canvas = Image.new("RGB", (1350, 600), (255, 255, 255))
    for idx, (_, p, crop_box) in enumerate(panels):
        im = Image.open(p).convert("RGB").crop(crop_box)
        im.thumbnail((440, 580), Image.Resampling.LANCZOS)
        x = idx * 450 + (450 - im.width) // 2
        y = (600 - im.height) // 2
        canvas.paste(im, (x, y))

    canvas.save(ref_path, quality=95)
    return ref_path


def apply_subtle_canvas_to_cg(raw_path: str, out_1080_path: str):
    """
    Upscales the 16:9 CG to 1920x1080 and applies a subtle macro-canvas weave
    from create-flat-evenly-lit-ada66b.png that embeds into the paper/wash tones
    while preserving 100% of the crisp dark woodcut ink lines on the characters.
    """
    with Image.open(raw_path) as raw_im:
        cg_1080 = raw_im.convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)

    cg_np = np.asarray(cg_1080, dtype=np.float32)

    if os.path.exists(CANVAS_TEX_PATH):
        with Image.open(CANVAS_TEX_PATH) as tex_im:
            tex_1080 = tex_im.convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
        tex_np = np.asarray(tex_1080, dtype=np.float32)

        # Extract high-frequency canvas weave
        tex_luma = (0.299 * tex_np[:, :, 0] + 0.587 * tex_np[:, :, 1] + 0.114 * tex_np[:, :, 2]) / 255.0
        tex_mean = float(np.mean(tex_luma))
        weave_centered = (tex_luma - tex_mean)[..., None]

        # Weight the canvas weave by pixel brightness so bright paper/wash areas show the full
        # coarse linen texture while dark woodcut ink contours stay 100% crisp and dark!
        cg_luma = (0.299 * cg_np[:, :, 0] + 0.587 * cg_np[:, :, 1] + 0.114 * cg_np[:, :, 2]) / 255.0
        paper_weight = np.clip((cg_luma - 0.18) / 0.72, 0.0, 1.0)[..., None]

        # Warm paper ground blend on lightest areas + physical weave modulation
        ground_blend = cg_np * (1.0 - 0.22 * paper_weight) + tex_np * (0.22 * paper_weight)
        weave_factor = 1.0 + weave_centered * (0.48 * paper_weight)
        out_np = np.clip(ground_blend * weave_factor, 0.0, 255.0).astype(np.uint8)
        final_im = Image.fromarray(out_np)
    else:
        final_im = cg_1080

    final_im = final_im.filter(ImageFilter.UnsharpMask(radius=0.7, percent=35, threshold=2))
    final_im.save(out_1080_path, format="PNG")
    return final_im


def build_thumb_and_scenario_card(cg_1080: Image.Image, cg_key: str):
    cfg = CG_CONFIGS[cg_key]
    ep_id = cfg["ep_id"]
    mood = cfg["mood"]

    # 1. 16:9 Thumbnail (512x288)
    thumb_im = cg_1080.resize((512, 288), Image.Resampling.LANCZOS)
    thumb_out = os.path.join(OUT_DIR, f"{cg_key}_thumb.png")
    thumb_game = os.path.join(REPO_ROOT, "game", "images", f"{cg_key}_thumb.png")
    thumb_im.save(thumb_out)
    thumb_im.save(thumb_game)
    print(f"[SAVED] Thumbnail (512x288) -> {thumb_game}")

    # 2. 16:9 Constellation Scenario Card (512x285 RGBA with rounded corners & bottom title wash)
    card_w, card_h = 512, 285
    card_rgb = cg_1080.resize((card_w, card_h), Image.Resampling.LANCZOS).convert("RGBA")

    # Dark warm gradient wash in the bottom 82px so the episode title text on the Constellation screen is 100% legible
    grad = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    grad_np = np.zeros((card_h, card_w, 4), dtype=np.uint8)
    for y in range(card_h - 90, card_h):
        t = (y - (card_h - 90)) / 89.0
        alpha = int(round(215 * (t ** 1.35)))
        grad_np[y, :, 0] = 24
        grad_np[y, :, 1] = 14
        grad_np[y, :, 2] = 9
        grad_np[y, :, 3] = alpha
    grad = Image.fromarray(grad_np)
    card_rgba = Image.alpha_composite(card_rgb, grad)

    # Rounded corner alpha mask (radius=14) matching existing scenario_card_*.png
    mask = Image.new("L", (card_w * 2, card_h * 2), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, card_w * 2 - 1, card_h * 2 - 1), radius=28, fill=255)
    mask = mask.resize((card_w, card_h), Image.Resampling.LANCZOS)
    card_rgba.putalpha(mask)

    card_name = f"scenario_card_{ep_id}_{mood}.png"
    card_out = os.path.join(OUT_DIR, card_name)
    card_game = os.path.join(REPO_ROOT, "game", "images", card_name)
    card_rgba.save(card_out)
    card_rgba.save(card_game)
    print(f"[SAVED] Scenario Card (512x285) -> {card_game}")

    # 3. Stage preview with dialogue box at the bottom so we can verify upper-two-thirds framing
    tb_path = os.path.join(REPO_ROOT, "game", "gui", "textbox.png")
    if os.path.exists(tb_path):
        tb = Image.open(tb_path).convert("RGBA")
        stage = cg_1080.convert("RGBA")
        stage.alpha_composite(tb, (0, 1080 - tb.height))
        prev_path = os.path.join(OUT_DIR, f"{cg_key}_stage_preview.png")
        stage.save(prev_path)
        print(f"[SAVED] Stage Preview (with textbox) -> {prev_path}")


def generate_cg(cg_key: str, custom_prompt: str = None, suffix: str = ""):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in environment or .env!")
        sys.exit(1)

    if cg_key not in CG_CONFIGS:
        print(f"[ERROR] Unknown CG '{cg_key}'. Available: {list(CG_CONFIGS.keys())}")
        sys.exit(1)

    cfg = CG_CONFIGS[cg_key]
    scene_prompt = custom_prompt or cfg["prompt"]
    full_prompt = f"{SHARED_CG_STYLE}\n\n{scene_prompt}"

    cast_ref_path = build_cast_reference_sheet()
    bg_ref_path = os.path.join(REPO_ROOT, "game", "images", cfg["bg_ref"])

    with open(cast_ref_path, "rb") as f:
        cast_b64 = base64.b64encode(f.read()).decode("utf-8")
    with open(bg_ref_path, "rb") as f:
        bg_b64 = base64.b64encode(f.read()).decode("utf-8")

    tag_name = f"{cg_key}_{suffix}" if suffix else cg_key
    print(f"\n==================================================")
    print(f"Generating v3 Full-Art 16:9 CG: {tag_name}")
    print(f"Cast Reference: {cast_ref_path}")
    print(f"Background Reference: {bg_ref_path}")
    print(f"Estimated Cost: ${COST_PER_IMAGE_USD:.3f}")
    print(f"==================================================")

    parts = [
        {
            "inlineData": {
                "mimeType": "image/jpeg",
                "data": cast_b64,
            }
        },
        {
            "inlineData": {
                "mimeType": "image/png",
                "data": bg_b64,
            }
        },
        {
            "text": (
                "Reference Image 1 shows the THREE core characters (left: Koraba, center: Xochit, right: Clara) "
                "in their approved HIGHLY STYLIZED hand-carved woodcut/engraved art style and non-realistic geometric facial proportions.\n"
                "Reference Image 2 shows the approved wet-on-wet tea/coffee watercolor wash background setting on warm ivory canvas.\n\n"
                f"{full_prompt}\n\n"
                "Strict Negative Constraints (DO NOT INCLUDE): "
                "realistic human facial proportions, generic comic/anime faces, text, letters, numbers, typography, UI screens with text, "
                "captions, logos, watermarks, stiff front-facing lineup, heads cut off, key action hidden in bottom 25% of frame."
            )
        }
    ]

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
            "imageConfig": {
                "aspectRatio": "16:9"
            }
        }
    }

    response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=120)
    if response.status_code != 200:
        print(f"[ERROR] API request failed ({response.status_code}): {response.text}")
        sys.exit(1)

    res_json = response.json()
    candidates = res_json.get("candidates", [])
    if not candidates:
        print(f"[ERROR] No candidates returned: {res_json}")
        sys.exit(1)

    img_bytes = None
    for p in candidates[0].get("content", {}).get("parts", []):
        if "inlineData" in p:
            img_bytes = base64.b64decode(p["inlineData"]["data"])
            break

    if not img_bytes:
        print(f"[ERROR] No image returned in response parts: {candidates[0]}")
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)
    raw_path = os.path.join(OUT_DIR, f"{tag_name}_raw.jpg")
    with open(raw_path, "wb") as f:
        f.write(img_bytes)
    print(f"[RAW OK] Saved raw 16:9 CG -> {raw_path}")

    log_usage(tag_name, scene_prompt, COST_PER_IMAGE_USD)

    out_1080_archive = os.path.join(OUT_DIR, f"{tag_name}.png")
    cg_1080 = apply_subtle_canvas_to_cg(raw_path, out_1080_archive)
    out_1080_game = os.path.join(REPO_ROOT, "game", "images", f"{cg_key}.png")
    cg_1080.save(out_1080_game)
    print(f"[SAVED] Full-window 1920x1080 CG -> {out_1080_game}")

    build_thumb_and_scenario_card(cg_1080, cg_key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate v3 Full-Art 16:9 Outcome CG")
    parser.add_argument("cg_key", choices=list(CG_CONFIGS.keys()), help="CG slot name to generate")
    parser.add_argument("--prompt", help="Optional custom prompt override")
    parser.add_argument("--suffix", default="", help="Optional suffix for A/B comparison")
    args = parser.parse_args()
    generate_cg(args.cg_key, custom_prompt=args.prompt, suffix=args.suffix)
