"""
generate_gold_character.py
Generates 3D solid polished 24k gold character sprites using Google Gemini Image API (gemini-3.1-flash-image).

Features:
1. Loads GEMINI_API_KEY from .env or system environment.
2. Uses approved Alex golden sprite as visual style reference for consistent 24k molten metallic finish.
3. Contains calibrated prompts for all characters (Alex, Maya, Jordan, Atlas, Spectre, Vera).
4. Tracks usage and cost ($0.03/image) in vault/06 Assets/generation_usage_log.json.
5. Automatically runs the raw render through process_gold_sprite.py to produce:
   - 560x880 Ren'Py transparent sprite (arm voids keyed out, garments 100% solid)
   - In-game conference stage composite preview
   - High-contrast magenta verification image
"""

import os
import sys
import json
import base64
import argparse
from datetime import datetime
import requests
from dotenv import load_dotenv
import cv2
import numpy as np

# Import post-processing pipeline
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from process_gold_sprite import process_sprite

# Default Style Reference Image Paths (Maya is the primary gold standard benchmark)
DEFAULT_STYLE_REFS = [
    os.path.join("vault", "06 Assets", "gold_bust_prototypes", "maya_approved_gold_reference_keeper.jpg"),
    os.path.join("vault", "06 Assets", "gold_bust_prototypes", "maya_neutral_gold_raw.jpg"),
    os.path.join("vault", "06 Assets", "gold_bust_prototypes", "alex neutral gold waistup (560x880).png"),
    os.path.join(
        os.path.expanduser("~"),
        ".gemini",
        "antigravity",
        "brain",
        "71b44432-bdf1-4c93-a234-76d434c42254",
        "alex_neutral_direct_eye_contact_v1_1792794378105.jpg"
    )
]

def get_default_style_ref(character: str = None) -> str:
    if character and character.lower().strip() == "alex":
        alex_ref = os.path.join("vault", "06 Assets", "gold_bust_prototypes", "alex_v4_2_approved_keeper.jpg")
        if os.path.exists(alex_ref):
            return alex_ref
    if character and character.lower().strip() == "atlas":
        atlas_ref = os.path.join("vault", "06 Assets", "gold_bust_prototypes", "atlas_clean_reference_keeper.jpg")
        if os.path.exists(atlas_ref):
            return atlas_ref
    if character and character.lower().strip() == "vera":
        vera_ref = os.path.join("vault", "06 Assets", "gold_bust_prototypes", "vera_v4_approved_keeper.jpg")
        if os.path.exists(vera_ref):
            return vera_ref
    for p in DEFAULT_STYLE_REFS:
        if os.path.exists(p):
            return p
    return DEFAULT_STYLE_REFS[-1]

PROMPTS_V4_PATH = os.path.join("vault", "06 Assets", "character_prompts_v4.json")
PROMPTS_V3_PATH = os.path.join("vault", "06 Assets", "character_prompts_v3.json")
PROMPTS_V2_PATH = os.path.join("vault", "06 Assets", "character_prompts_v2.json")
PROMPTS_JSON_PATH = os.path.join("vault", "06 Assets", "character_prompts.json")

def get_active_prompts_path() -> str:
    for p in [PROMPTS_V4_PATH, PROMPTS_V3_PATH, PROMPTS_V2_PATH, PROMPTS_JSON_PATH]:
        if os.path.exists(p):
            return p
    return PROMPTS_JSON_PATH

def load_character_prompt(character: str, expression: str = "neutral") -> tuple[str, str]:
    """Returns (prompt_text, global_negative)"""
    char_key = character.lower().strip()
    active_path = get_active_prompts_path()

    if os.path.exists(active_path):
        try:
            with open(active_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            negative = data.get("_global_negative", "")
            chars = data.get("characters", {})
            char_data = chars.get(char_key)
            if isinstance(char_data, dict):
                prompt = char_data.get(expression) or char_data.get("neutral")
                if prompt:
                    print(f"[PROMPT] Loaded '{char_key}' ({expression}) from {active_path}")
                    return prompt, negative
            elif isinstance(char_data, str):
                print(f"[PROMPT] Loaded '{char_key}' from {active_path}")
                return char_data, negative
        except Exception as e:
            print(f"[WARN] Error loading {active_path}: {e}")

    # Fallback to in-script dictionary if needed
    fallback = CHARACTER_PROMPTS.get(char_key, "")
    print(f"[PROMPT] Using in-script fallback prompt for '{char_key}'")
    return fallback, ""

# Calibrated Fallback Prompts for Neutral Gold Sprites (Waist-Up, Dynamic 3/4 Dropped Shoulder, Direct Eye Contact, Black Background)
CHARACTER_PROMPTS = {
    "alex": (
        "Waist-up character portrait sprite of a handsome young business executive named Alex, standing in a dynamic 3/4 angled body pose "
        "with one shoulder closer to the camera and lower in a relaxed dropped-shoulder pose (natural asymmetric contrapposto stance, confident and lively, "
        "not stiff or squared-on). His head is turned at a natural 3/4 angle naturally aligned with his body, while his eyes are locked directly onto the "
        "viewer / camera making calm, calculating, composed direct eye contact with the player. He wears an impeccably tailored three-piece suit, dress shirt, "
        "and tie, holding a modern golden smartphone in his hands at waist level, comfortably contained within the canvas. Cleanly sculpted slicked-back modern hair "
        "with smooth continuous contours, no loose strands. The entire character, suit, hair, skin, hands, and phone are sculpted from a single monolithic "
        "solid polished reflective 24-karat yellow gold metal, matching the style and material of the reference image, with gleaming mirror-like specular highlights "
        "and warm amber reflections. Sharp studio rim lighting. Framed waist-up with generous margins on all borders. Absolute solid pitch-black background "
        "(#000000) with no floor, clean silhouette edges. Vertical 2:3 visual novel character portrait aspect ratio."
    ),
    "maya": (
        "Waist-up character portrait sprite of a sharp, brilliant female software architect named Maya, standing in a dynamic 3/4 angled body pose "
        "with one shoulder closer to the camera than the other in an expressive dropped shoulder pose (natural contrapposto stance, asymmetric and lively, "
        "not stiff, not squared-on). Her head is turned at a natural 3/4 angle naturally aligned with her body, while her eyes are locked directly on the "
        "viewer / camera, making sharp, calm, confident direct eye contact with the player through her modern slim-frame glasses. She holds a sleek modern "
        "golden ultra-thin laptop tucked vertically under her arm against her ribs/hip, with her other arm resting naturally with the dropped shoulder, "
        "comfortably contained inside the canvas with generous margins on all sides (zero edge clipping). She has a sleek, cleanly sculpted low bun swept "
        "neatly behind her ear sculpted from smooth solid gold with continuous clean sculptural mass, no loose hanging strands, no floating wisps, no detached "
        "hair loops, ensuring a pristine smooth silhouette around her head, neck, and shoulders. She wears an athletic zip-up tech startup jacket with subtle "
        "circuit relief tracings over a casual crewneck. Entire figure, glasses, hair, jacket, laptop, and hands are crafted from seamless monolithic "
        "solid polished reflective 24-karat yellow gold metal, matching the molten metallic gold material of the reference image, with bright mirror-like "
        "specular highlights and crisp studio edge rim lighting. Framed comfortably waist-up with generous margins. Centered against an absolute pure solid "
        "pitch-black background (#000000) with no floor, no shadows, pristine clean edges. Vertical 2:3 visual novel character portrait aspect ratio."
    ),
    "jordan": (
        "Waist-up character portrait sprite of an energetic, charismatic young community organizer named Jordan, standing in a dynamic 3/4 angled body pose "
        "with one shoulder closer to the camera and lower in a relaxed dropped-shoulder stance (natural asymmetric contrapposto posture, relaxed and alive, "
        "not stiff, not squared-on). Their head is turned at a natural 3/4 angle naturally aligned with their body, while their eyes are locked directly onto the "
        "viewer / camera, making warm, engaging, confident direct eye contact with the player. They have stylish textured curly hair sculpted as a single solid "
        "continuous sculptural mass with smooth, closed outer contours—absolutely no loose dangling strands, no wire wisps, and no floating loops. They wear an "
        "oversized streetwear hoodie with the hood resting comfortably down around the neck, featuring subtle embossed DAO and circuit emblems in gold relief, "
        "with their hands resting naturally in their front pockets / at waist level, fully contained within the frame with generous margins. Entire figure, "
        "sculpted curls, hoodie fabric folds, and hands are sculpted from seamless monolithic solid polished 24-karat yellow gold metal, matching the molten "
        "metallic gold material of the reference image, with gleaming specular highlights and deep warm reflections. Crisp studio rim lighting. Framed "
        "waist-up with generous margins. Isolated on a uniform solid pitch-black background (#000000), no floor, no shadows, clean silhouette edges. "
        "Vertical 2:3 visual novel character portrait aspect ratio."
    ),
    "atlas": (
        "Waist-up character portrait sprite of an authoritative, imposing senior investor named Atlas, standing in a commanding dynamic 3/4 angled body pose "
        "with one shoulder closer to the camera and lower in a natural dropped-shoulder stance (imposing contrapposto posture, commanding and lively, not stiff "
        "or squared-on). His head is held high and turned at a natural 3/4 angle in harmony with his body, while his eyes are locked directly onto the viewer / "
        "camera, delivering a calm, calculating, formidable direct gaze to the player. Distinguished swept-back hair sculpted as a continuous solid sculptural "
        "mass with smooth closed contours, sharp sculpted jawline. Wearing a luxury double-breasted wool trench coat with structured lapels and a gold silk lapel "
        "drape over a tailored suit, with one hand resting across his midsection / coat button showing sculpted rings on his fingers, fully contained within "
        "the frame with generous margins. The entire figure, hair, heavy coat, and hands are rendered as a solid monolithic polished reflective 24-karat yellow "
        "gold sculpture, matching the molten metallic gold material of the reference image, with dramatic specular edge lighting and deep amber occlusions. "
        "Framed waist-up with generous margins. Pure solid pitch-black background (#000000), no ground, clean sharp edges. Vertical 2:3 visual novel character "
        "portrait aspect ratio."
    ),
    "spectre": (
        "Waist-up character portrait sprite of an enigmatic, completely anonymous developer named Spectre, standing in a dynamic 3/4 angled silhouette posture "
        "facing towards the player with one shoulder slightly forward in a relaxed dropped-shoulder stance. Wearing an oversized tactical technical hooded "
        "cloak with the deep cowl pulled forward. The interior of the hood is a deep, impenetrable black hollow void with zero facial features visible "
        "(faceless anonymous shadow void). Only the sculpted fabric of the deep hood, high structured cowl collar, tactical jacket sleeves with embossed "
        "circuit relief tracings, and metallic gloved hands held quietly at waist level are sculpted from seamless solid polished reflective 24-karat yellow gold "
        "metal, matching the molten metallic gold material of the reference image, contrasting sharply with the pitch-black void beneath the cowl. Crisp "
        "studio edge rim lighting along the golden contours. Framed waist-up with generous margins on all sides, zero edge clipping. Solid uniform pitch-black "
        "background (#000000), no floor, clean silhouette cutout. Vertical 2:3 visual novel character portrait aspect ratio."
    ),
    "vera": (
        "Waist-up character portrait sprite of an elegant, poised mature woman named Vera, standing with regal dynamic 3/4 angled body posture and one "
        "shoulder closer to the camera in a graceful dropped-shoulder stance (asymmetric, composed, and lively, not stiff or squared-on). Her head is turned "
        "at a natural 3/4 angle in harmony with her body, while her eyes look warmly and perceptively directly into the camera / viewer, maintaining direct "
        "eye contact with the player. Sophisticated swept-back hair sculpted into an elegant updo as a single continuous solid gold sculptural mass with smooth "
        "closed contours, zero dangling wisps or loose strands. Wearing an architectural wrap dress with an embroidered textured shawl draped gracefully over "
        "her shoulders, pinned with a prominent gear/handshake geometric brooch, her hands resting gracefully in front holding the edge of the shawl at waist "
        "level, comfortably contained within the canvas with generous margins. The entire figure, hair, textured shawl, brooch, wrap dress, and hands are made "
        "of solid monolithic polished reflective 24-karat yellow gold metal, matching the molten metallic gold material of the reference image, with gleaming "
        "specular highlights and rich amber shadow occlusions. Studio rim lighting. Framed waist-up with generous margins. Uniform solid pitch-black "
        "background (#000000), no floor, clean silhouette edges. Vertical 2:3 visual novel character portrait aspect ratio."
    ),
}

COST_PER_IMAGE_USD = 0.030
USAGE_LOG_PATH = os.path.join("vault", "06 Assets", "generation_usage_log.json")

def log_usage(character: str, prompt: str, cost: float = COST_PER_IMAGE_USD):
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
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "character": character,
        "model": "gemini-3.1-flash-image",
        "cost_usd": cost,
        "cumulative_spent_usd": log_data["total_spent_usd"],
        "prompt_snippet": prompt[:120] + "..."
    })

    os.makedirs(os.path.dirname(USAGE_LOG_PATH), exist_ok=True)
    with open(USAGE_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

    print(f"[USAGE] Logged generation for {character}. Cumulative spend: ${log_data['total_spent_usd']:.3f} ({log_data['total_images']} images)")

def generate_sprite(character: str, custom_prompt: str = None, expression: str = "neutral", style_ref_path: str = None, single_ref: bool = False):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in environment or .env!")
        sys.exit(1)

    char_key = character.lower().strip()
    loaded_prompt, global_negative = load_character_prompt(char_key, expression)
    prompt = custom_prompt or loaded_prompt
    if not prompt:
        print(f"[ERROR] No prompt found for '{character}' (expression: '{expression}'). Check {PROMPTS_V2_PATH}")
        sys.exit(1)

    ref_path = style_ref_path or get_default_style_ref(char_key)

    print(f"\n==================================================")
    print(f"Generating 3D Gold Sprite: {char_key.capitalize()} ({expression.capitalize()})")
    print(f"Model: gemini-3.1-flash-image")
    print(f"Style Reference: {ref_path}")
    print(f"Estimated Cost: ${COST_PER_IMAGE_USD:.3f}")
    print(f"==================================================")

    parts = []
    # 1. Check for original character sprite to use as Pose Reference
    char_orig_paths = [
        os.path.join("vault", "06 Assets", "original_sprites_backup", f"{char_key} neutral.png"),
        os.path.join("game", "images", f"{char_key} neutral.png")
    ]
    char_orig_path = None
    if not single_ref:
        for p in char_orig_paths:
            if os.path.exists(p):
                char_orig_path = p
                break

    # If original sprite exists, composite on solid black for clean input
    if char_orig_path:
        orig_img = cv2.imread(char_orig_path, cv2.IMREAD_UNCHANGED)
        if orig_img is not None:
            if orig_img.shape[2] == 4:
                b, g, r, a = cv2.split(orig_img)
                alpha_f = a.astype(float) / 255.0
                comp = np.zeros_like(orig_img[:, :, :3])
                for c in range(3):
                    comp[:, :, c] = (orig_img[:, :, c].astype(float) * alpha_f).astype(np.uint8)
            else:
                comp = orig_img
            _, buf = cv2.imencode(".jpg", comp)
            char_b64 = base64.b64encode(buf).decode("utf-8")
            parts.append({
                "inlineData": {
                    "mimeType": "image/jpeg",
                    "data": char_b64
                }
            })

    # 2. Attach style reference for 3D gold material & rim lighting
    if ref_path and os.path.exists(ref_path):
        mime = "image/png" if ref_path.lower().endswith(".png") else "image/jpeg"
        with open(ref_path, "rb") as f:
            ref_b64 = base64.b64encode(f.read()).decode("utf-8")
        parts.append({
            "inlineData": {
                "mimeType": mime,
                "data": ref_b64
            }
        })

    bg_guidance = ""
    if "MAGENTA" in prompt or "#FF00FF" in prompt:
        bg_guidance = (
            "\n\nCRITICAL BACKGROUND INSTRUCTION:\n"
            "Generate this character completely isolated against a uniform, flat, solid bright vibrant MAGENTA background (#FF00FF / chroma key magenta backdrop).\n"
            "DO NOT use a black or dark background. Even though Image 2 may be on black, the new output background MUST be pure flat solid magenta (#FF00FF), perfectly uniform across the entire canvas with no floor, no ground shadows, and crisp silhouette edges for chroma keying."
        )

    if char_orig_path and ref_path and os.path.exists(ref_path):
        instructions = (
            "You are an expert 3D character sculptor and concept artist.\n"
            "Image 1 shows the character in their original visual novel design, pose, and framing. (Use Image 1 ONLY for the character's facial features, pose, and proportions—DO NOT copy its 2D illustration or drawing style).\n"
            "Image 2 shows the approved 3D solid polished 24-karat gold sculpture art style.\n\n"
            "Task:\n"
            f"Create a new waist-up visual novel character sprite of {char_key.capitalize()} sculpted entirely out of solid polished "
            "reflective 24-karat yellow gold as a real physical 3D metallic sculpture, translating Image 1 into the exact molten metallic material, specular highlights, and surface finish of Image 2.\n\n"
            f"{prompt}{bg_guidance}"
        )
    elif ref_path and os.path.exists(ref_path):
        instructions = (
            "You are an expert 3D character sculptor and concept artist.\n"
            "The reference image shows the approved 3D solid polished 24-karat gold character sculpture, facial features, princess tiara crown, and attire.\n\n"
            "Task:\n"
            f"Create an updated waist-up visual novel character sprite of {char_key.capitalize()} sculpted entirely out of solid polished "
            "reflective 24-karat yellow gold metal, strictly matching the style, face, princess tiara crown, and material finish of the reference image.\n\n"
            f"{prompt}{bg_guidance}"
        )
    else:
        instructions = f"{prompt}{bg_guidance}"

    # Ensure strong anti-illustration negative constraints
    anti_2d = "2D illustration, drawing, painting, anime, manga, comic, cel-shaded, ink outlines, sketch, fabric texture, cloth texture, satin cloth, matte sweatshirt, flat shading, soft shading"
    if global_negative:
        instructions += f"\n\nStrict negative constraints (AVOID COMPLETELY): {global_negative}, {anti_2d}"
    else:
        instructions += f"\n\nStrict negative constraints (AVOID COMPLETELY): {anti_2d}"

    parts.append({"text": instructions})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": parts}]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=90)
    if response.status_code != 200:
        print(f"[ERROR] API request failed with status {response.status_code}: {response.text}")
        sys.exit(1)

    res_json = response.json()
    candidates = res_json.get("candidates", [])
    if not candidates:
        print(f"[ERROR] No candidates returned: {res_json}")
        sys.exit(1)

    res_parts = candidates[0].get("content", {}).get("parts", [])
    img_bytes = None
    for p in res_parts:
        if "inlineData" in p:
            img_bytes = base64.b64decode(p["inlineData"]["data"])
            break

    if not img_bytes:
        print(f"[ERROR] No image bytes found in response: {res_parts}")
        sys.exit(1)

    # Save raw render
    out_dir = os.path.join("vault", "06 Assets", "gold_bust_prototypes")
    os.makedirs(out_dir, exist_ok=True)
    raw_path = os.path.join(out_dir, f"{char_key}_neutral_gold_raw.jpg")
    with open(raw_path, "wb") as f:
        f.write(img_bytes)
    print(f"[OK] Saved raw render: {raw_path}")

    # Log usage
    log_usage(char_key, prompt, COST_PER_IMAGE_USD)

    # Post-process into Ren'Py sprite (560x880) + stage preview + check image
    sprite_path = os.path.join(out_dir, f"{char_key} neutral gold waistup (560x880).png")
    preview_path = os.path.join(out_dir, f"{char_key}_gold_waistup_stage_preview.png")
    check_path = os.path.join(out_dir, f"{char_key}_transparency_check.png")

    print(f"Processing cutout & stage preview with process_gold_sprite.py...")
    process_sprite(
        src_path=raw_path,
        out_sprite_path=sprite_path,
        stage_preview_path=preview_path,
        magenta_check_path=check_path
    )
    print(f"\n[DONE] {char_key.capitalize()} neutral sprite created and verified!")
    print(f"Preview: {preview_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate 3D Gold Character Sprite via Gemini Image API")
    parser.add_argument("character", choices=["alex", "maya", "jordan", "atlas", "spectre", "vera", "all"], help="Character to generate")
    parser.add_argument("--expression", default="neutral", help="Expression variant in character_prompts.json (default: neutral)")
    parser.add_argument("--prompt", help="Optional custom prompt override")
    parser.add_argument("--style-ref", help="Optional path to custom style reference image (defaults to Maya or Alex gold render)")
    parser.add_argument("--single-ref", action="store_true", help="Use only the 3D gold keeper reference without attaching the legacy 2D sprite")

    args = parser.parse_args()

    if args.character == "all":
        for c in ["maya", "jordan", "atlas", "spectre", "vera"]:
            generate_sprite(c, expression=args.expression, style_ref_path=args.style_ref)
    else:
        generate_sprite(args.character, custom_prompt=args.prompt, expression=args.expression, style_ref_path=args.style_ref, single_ref=args.single_ref)
