#!/usr/bin/env python3
"""
generate_background_v3.py
Two-stage Pass 3A background generator for 'Get Rich Together':
- Stage 1: Calls gemini-3.1-flash-image (16:9, 1376x768) with the approved Pass 2A
  capillary wash reference plate to produce a strictly line-free wet-on-wet tea/coffee
  watercolor wash on a clean bright-white ground, where all architecture and props read
  purely as loose wet-on-wet stain blooms and negative-space cutouts with zero drawn edges.
- Stage 2: Runs apply_canvas_style.py to composite the wash onto the shared macro-canvas
  ground (create-flat-evenly-lit-ada66b.png) and upscale to 1920x1080 PNG32.
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from apply_canvas_style import apply_pass3a_composite

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PASS2A_REF = os.path.join(REPO_ROOT, "vault", "06 Assets", "style_references", "pass2a_capillary_wash_reference.jpg")
USAGE_LOG_PATH = os.path.join(REPO_ROOT, "vault", "06 Assets", "generation_usage_log.json")
STAGE1_DIR = os.path.join(REPO_ROOT, "vault", "06 Assets", "generated_backgrounds", "v3_stage1")
STAGE2_DIR = os.path.join(REPO_ROOT, "vault", "06 Assets", "generated_backgrounds", "v3_stage2")

COST_PER_IMAGE_USD = 0.030

LOOSE_BLOOM_RULE = (
    "Every architectural feature and room prop must have loose, dissolved, lost-and-found wet-into-wet edges, "
    "reading purely as soft watercolor stain blooms, pooled tea puddles, capillary backruns, and untouched white "
    "negative-space cutouts—never as drawn objects. Zero thin brush outlines, zero dark edge contours around objects, "
    "zero ruled straight lines, and zero fine literal prop detailing."
)

BACKGROUND_PROMPTS = {
    "sanctuary": (
        "A wide 16:9 visual novel background illustration of an airy community sanctuary studio, "
        "created entirely from loose, atmospheric wet-on-wet tea and coffee watercolor stain blooms on a clean bright-white ground. "
        "Absolutely zero linework: no pen, pencil, ink outlines, thin brush contours, wireframe polygons, or drawn object edges. "
        f"{LOOSE_BLOOM_RULE} "
        "Soft horizontal and vertical puddles of pale Earl Grey and chamomile tea bleed wet-into-wet to suggest an overhead timber beam, "
        "feathered botanical stain clusters hanging above, soft gourd-and-curve stain silhouettes of resting folk instruments, "
        "and soft blocky washes of stacked shipment crates to the side, all dissolving into surrounding water blooms and leaving a "
        "wide, quiet, unpainted foreground floor area for three standing character sprites. "
        "Filtered morning daylight, window glow, and airy light pockets between the stain washes are left strictly as untouched "
        "bright warm-white negative-space cutouts with delicate water-drop backruns pushing pale pigment outward. "
        "Very low contrast, pale chamomile amber, soft Earl Grey sepia, and diluted coffee, highly luminous and airy, "
        "with capillary bleeding, water backruns, feathered blooms, and subtle coffee-ring tide marks. "
        "Pure background artwork, no text, labels, people, characters, interface elements, or watermark. "
        "Leave canvas weave and final ground tone to the Stage 2 composite."
    ),
    "constellation": (
        "Uses existing approved pass2a_capillary_wash_reference.jpg composited via apply_canvas_style.py."
    ),
    "lisbon_airport": (
        "A wide 16:9 visual novel background illustration of an international airport terminal and customs waiting area "
        "in Lisbon after midnight, created entirely from loose, atmospheric wet-on-wet tea and coffee watercolor stain blooms "
        "on a clean bright-white ground. Absolutely zero linework: no pen, pencil, ink outlines, thin brush contours, "
        "wireframe polygons, or drawn object edges. "
        f"{LOOSE_BLOOM_RULE} "
        "Tall rain-streaked window bays, vertical capillary water runs, soft barrier silhouettes, and stacked shipment crate masses "
        "to one side emerge purely from bleeding vertical and horizontal puddles of pale Earl Grey, cool sepia, and diluted coffee washes "
        "with feathered tide edges, leaving an open, quiet foreground standing area for three character sprites. "
        "Distant terminal lights through the rain-streaked glass and wet floor reflections appear strictly as untouched bright "
        "warm-white negative-space light pockets and delicate water-drop backruns. "
        "Very low contrast, pale chamomile amber, soft Earl Grey sepia, and diluted coffee, highly luminous and airy, "
        "with capillary bleeding, water backruns, feathered blooms, and subtle coffee-ring tide marks. "
        "Pure background artwork, no text, signage, numbers, people, interface elements, or watermark. "
        "Leave canvas weave and final ground tone to the Stage 2 composite."
    ),
    "cacao_circle": (
        "A wide 16:9 visual novel background illustration of a serene ceremonial cacao gathering space, "
        "created entirely from loose, atmospheric wet-on-wet tea and coffee watercolor stain blooms on a clean bright-white ground. "
        "Absolutely zero linework: no pen, pencil, ink outlines, thin brush contours, wireframe polygons, or drawn object edges. "
        f"{LOOSE_BLOOM_RULE} "
        "A low gathering table, woven textile runner, and soft sanctuary arches emerge purely from bleeding wet-into-wet chamomile, "
        "warm amber, and diluted espresso stain puddles, while overlapping circular coffee-ring tide marks naturally suggest cacao cups "
        "and a central ceremonial bowl without drawn rims, leaving a clear foreground and midground area for three character sprites. "
        "Warm candle glow, rising steam wisps, and ambient daylight pockets are left strictly as untouched bright warm-white "
        "negative-space cutouts with feathered water-bloom halos pushing pigment outward. "
        "Very low contrast, pale chamomile amber, soft Earl Grey sepia, and diluted coffee, highly luminous and airy, "
        "with capillary bleeding, water backruns, feathered blooms, and subtle coffee-ring tide marks. "
        "Pure background artwork, no text, labels, people, interface elements, or watermark. "
        "Leave canvas weave and final ground tone to the Stage 2 composite."
    ),
    "showcase_backstage": (
        "A wide 16:9 visual novel background illustration of a practical backstage production workspace at a Lisbon festival venue, "
        "created entirely from loose, atmospheric wet-on-wet tea and coffee watercolor stain blooms on a clean bright-white ground. "
        "Absolutely zero linework: no pen, pencil, ink outlines, thin brush contours, wireframe polygons, or drawn object edges. "
        f"{LOOSE_BLOOM_RULE} "
        "Tall stage curtain drapes, soft blocky stain masses suggesting road cases and a worktable, and organic capillary water channels "
        "suggesting trailing cables emerge purely from bleeding vertical and curved wet-on-wet Earl Grey and diluted coffee puddles, "
        "keeping a wide open foreground for three character sprites. "
        "The spill of stage light through the curtain gap and the soft glowing rectangle of a laptop screen are left strictly as "
        "untouched bright warm-white negative-space light pockets with feathered water-bloom halos and zero readable screen content. "
        "Very low contrast, pale chamomile amber, soft Earl Grey sepia, and diluted coffee, highly luminous and airy, "
        "with capillary bleeding, water backruns, feathered blooms, and subtle coffee-ring tide marks. "
        "Pure background artwork, no text, labels, people, interface elements, or watermark. "
        "Leave canvas weave and final ground tone to the Stage 2 composite."
    ),
    "showcase_stage": (
        "A wide 16:9 visual novel background illustration of an expansive Lisbon festival performance stage with a broad projection "
        "dome and warming stage lights, created entirely from loose, atmospheric wet-on-wet tea and coffee watercolor stain blooms "
        "on a clean bright-white ground. Absolutely zero linework: no pen, pencil, ink outlines, thin brush contours, wireframe polygons, "
        "or drawn object edges. "
        f"{LOOSE_BLOOM_RULE} "
        "The wide stage plane, soft stain silhouettes of stage instruments, overhead lighting washes, and distant audience blooms "
        "emerge purely from overlapping translucent puddles of chamomile, warm amber, and Earl Grey tea with feathered tide edges, "
        "leaving the center foreground stage open and readable for three character sprites. "
        "Projector beams, stage spotlights, and abstract geometric light blooms across the projection backdrop are left strictly as "
        "untouched bright warm-white negative-space cutouts and glowing water-drop backruns with zero readable text. "
        "Very low contrast, pale chamomile amber, soft Earl Grey sepia, and diluted coffee, highly luminous and airy, "
        "with capillary bleeding, water backruns, feathered blooms, and subtle coffee-ring tide marks. "
        "Pure background artwork, no text, labels, people, interface elements, or watermark. "
        "Leave canvas weave and final ground tone to the Stage 2 composite."
    ),
    "apothecary": (
        "A wide 16:9 visual novel background illustration of a working herbal apothecary and signing desk, "
        "created entirely from loose, atmospheric wet-on-wet tea and coffee watercolor stain blooms on a clean bright-white ground. "
        "Absolutely zero linework: no pen, pencil, ink outlines, thin brush contours, wireframe polygons, or drawn object edges. "
        f"{LOOSE_BLOOM_RULE} "
        "Vertical and horizontal amber, chamomile, and Earl Grey stain washes frame the left and right shelves, while the foreground "
        "signing desk, mortar silhouette, and open ledger form purely through pooled coffee-ring tide marks and bleeding tonal puddles "
        "with dissolved edges, leaving a clean open midground for three character sprites. "
        "Rows of glass apothecary bottles, hanging herb clusters, and warm desk lamp light appear strictly as untouched bright "
        "warm-white negative-space bottle-shaped light pockets and water-drop blooms pushing pigment outward. "
        "Very low contrast, pale chamomile amber, soft Earl Grey sepia, and diluted coffee, highly luminous and airy, "
        "with capillary bleeding, water backruns, feathered blooms, and subtle coffee-ring tide marks. "
        "Pure background artwork, no text, labels, people, interface elements, or watermark. "
        "Leave canvas weave and final ground tone to the Stage 2 composite."
    ),
    "treasury_fire": (
        "A wide 16:9 visual novel background illustration of a sinister, catastrophic symbolic treasury collapse and breach, "
        "created entirely from dramatic, ominous wet-on-wet watercolor stain blooms of crimson hibiscus tea, scorched espresso soot, "
        "burnt umber, rust, and bruised ash-grey on a bright-white ground. "
        "Absolutely zero linework: no pen, pencil, ink outlines, thin brush contours, wireframe polygons, or drawn object edges. "
        f"{LOOSE_BLOOM_RULE} "
        "In the upper two-thirds, a shattered circular vault seal and fractured ledger planes split violently apart as dark, heavy "
        "scorched-espresso and deep crimson-hibiscus stain currents hemorrhage and bleed outward through jagged capillary fault channels "
        "like a drained vessel and spreading blight. Rising clouds of soot-grey backruns, rust-red tide rings, and scorched ember splatters "
        "radiate across the frame with unsettling, disastrous gravity, while jagged negative-space fissure cutouts slash through the dark washes. "
        "Keep the very bottom dialogue area slightly lighter so UI text remains legible, while making the overall atmosphere unmistakably "
        "sinister, ruptured, and catastrophic—not peaceful or warm. "
        "Pure background artwork, no text, labels, people, interface elements, or watermark. "
        "Leave canvas weave and final ground tone to the Stage 2 composite."
    ),
}


def log_usage(bg_name: str, prompt: str, cost: float = COST_PER_IMAGE_USD):
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
        "asset": f"bg {bg_name} (v3 stage1)",
        "model": "gemini-3.1-flash-image",
        "cost_usd": cost,
        "cumulative_spent_usd": log_data["total_spent_usd"],
        "prompt_snippet": prompt[:120] + "..."
    })

    os.makedirs(os.path.dirname(USAGE_LOG_PATH), exist_ok=True)
    with open(USAGE_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

    print(f"[USAGE] Logged generation for bg {bg_name}. Cumulative spend: ${log_data['total_spent_usd']:.3f} ({log_data['total_images']} images)")


def generate_background(bg_name: str, custom_prompt: str = None, deploy: bool = False, suffix: str = ""):
    key = bg_name.lower().strip().replace("bg ", "").replace(".png", "")
    os.makedirs(STAGE1_DIR, exist_ok=True)
    os.makedirs(STAGE2_DIR, exist_ok=True)

    # Special case: constellation uses the approved pass2a_capillary_wash_reference.jpg directly
    if key == "constellation" and not custom_prompt:
        print("\n==================================================")
        print("Compositing approved Pass 2A wash -> bg constellation.png (zero API cost)")
        print("==================================================")
        stage2_path = os.path.join(STAGE2_DIR, "bg constellation.png")
        apply_pass3a_composite(PASS2A_REF, stage2_path)
        if deploy:
            deploy_path = os.path.join(REPO_ROOT, "game", "images", "bg constellation.png")
            apply_pass3a_composite(PASS2A_REF, deploy_path)
            print(f"[DEPLOYED] Saved to {deploy_path}")
        return

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in environment or .env!")
        sys.exit(1)

    prompt = custom_prompt or BACKGROUND_PROMPTS.get(key)
    if not prompt:
        print(f"[ERROR] Unknown background key '{key}'. Available: {list(BACKGROUND_PROMPTS.keys())}")
        sys.exit(1)

    print(f"\n==================================================")
    print(f"Generating Pass 3A Background: bg {key}.png {f'({suffix})' if suffix else ''}")
    print(f"Stage 1 Style Reference: {PASS2A_REF}")
    print(f"Estimated Cost: ${COST_PER_IMAGE_USD:.3f}")
    print(f"==================================================")

    parts = []
    if os.path.exists(PASS2A_REF):
        with open(PASS2A_REF, "rb") as f:
            ref_b64 = base64.b64encode(f.read()).decode("utf-8")
        parts.append({
            "inlineData": {
                "mimeType": "image/jpeg",
                "data": ref_b64
            }
        })

    if key == "treasury_fire":
        instructions = (
            "Reference Image 1 shows the approved Stage-1 wet-on-wet watercolor stain-bloom and capillary backrun technique on a clean bright-white ground "
            "(strictly ZERO drawn pen/ink lines, forms emerging purely from bleeding stain puddles, capillary channels, tide rings, and negative-space cutouts).\n\n"
            "CRITICAL MOOD & PALETTE SHIFT FOR CRISIS BACKDROP:\n"
            "Unlike the peaceful chamomile palette of Reference Image 1, this image is the game's CRISIS & DISASTER backdrop (`bg treasury_fire`). "
            "Use Reference Image 1 ONLY for the wet-on-wet capillary stain-bloom technique and clean white ground, NOT its peaceful mood or pale yellow colors. "
            "Instead, render a sinister, catastrophic, ominous rupture using deep crimson hibiscus / dried-blood red tea stains, scorched dark espresso soot, "
            "burnt umber, rust, and bruised charcoal-ash watercolor blooms bleeding violently across the upper two-thirds of the frame, with jagged negative-space "
            "fissures slashing through the dark stains.\n\n"
            "Task:\n"
            f"{prompt}\n\n"
            "Strict Negative Constraints (DO NOT INCLUDE): "
            "pen lines, pencil sketch, ink outlines, thin brush outlines around objects, wireframe polygons, literal burning buildings, "
            "people, characters, text, typography, signage, UI elements, watermarks."
        )
    else:
        instructions = (
            "Reference Image 1 shows the approved Stage-1 wet-on-wet tea and coffee watercolor wash style on a clean bright-white ground "
            "(very low contrast, pale chamomile amber and soft Earl Grey sepia washes, capillary bleeding, water backruns, feathered blooms, "
            "untouched white negative-space light pockets, and strictly ZERO drawn lines or outlines).\n\n"
            "CRITICAL EDGE-SOFTNESS INSTRUCTION:\n"
            "Look closely at the upper canopy of Reference Image 1: notice how shapes have NO drawn outlines, NO dark brush borders, and NO fine "
            "interior detail lines—forms exist ONLY as soft wet-into-wet watercolor stain blooms, water backruns, and negative-space white cutouts.\n"
            "When depicting the scene below, DO NOT outline props (such as crates, instruments, herbs, furniture, or windows) with thin brown/sepia "
            "brush lines, and DO NOT draw literal interior details (like wood slats, guitar strings, soundholes, or box seams). "
            "Every single prop and architectural element must have loose, dissolved, bleeding wet-into-wet stain edges so the entire scene reads "
            "purely as organic tea and coffee stain blooms.\n\n"
            "Task:\n"
            "Generate a new wide 16:9 Stage-1 background wash in that exact loose wet-on-wet stain-bloom technique (do NOT copy the tree subject "
            "from Reference Image 1; depict the new scene subject below):\n\n"
            f"{prompt}\n\n"
            "Strict Negative Constraints (DO NOT INCLUDE): "
            "pen lines, pencil sketch, ink outlines, thin brush outlines around objects, hard object borders, drawn wood planks or crate slats, "
            "drawn guitar strings or soundholes, architectural drafting lines, wireframe polygons, dark shadows, black fills, "
            "high contrast, saturated colors, people, characters, text, typography, signage, UI elements, watermarks."
        )
    parts.append({"text": instructions})

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
    name_tag = f"{key}_{suffix}" if suffix else key
    stage1_path = os.path.join(STAGE1_DIR, f"{name_tag}_stage1_wash{ext}")
    with open(stage1_path, "wb") as f:
        f.write(img_bytes)
    print(f"[STAGE 1 OK] Saved raw wash -> {stage1_path}")

    log_usage(name_tag, prompt, COST_PER_IMAGE_USD)

    stage2_filename = f"bg {key}_{suffix}.png" if suffix else f"bg {key}.png"
    stage2_path = os.path.join(STAGE2_DIR, stage2_filename)
    print(f"[STAGE 2] Running Pass 3A macro-canvas composite & 1080p upscale...")
    apply_pass3a_composite(stage1_path, stage2_path)

    if deploy:
        deploy_path = os.path.join(REPO_ROOT, "game", "images", f"bg {key}.png")
        apply_pass3a_composite(stage1_path, deploy_path)
        print(f"[DEPLOYED] Saved to {deploy_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Pass 3A Background (Stage 1 Wash + Stage 2 Canvas Composite)")
    parser.add_argument("background", help="Background key (e.g. sanctuary, constellation, lisbon_airport, cacao_circle, showcase_backstage, showcase_stage, apothecary, treasury_fire)")
    parser.add_argument("--prompt", help="Optional custom prompt override")
    parser.add_argument("--suffix", default="", help="Optional filename suffix for A/B test comparison (e.g. v3b)")
    parser.add_argument("--deploy", action="store_true", help="Also write output to game/images/bg <name>.png")
    args = parser.parse_args()
    generate_background(args.background, custom_prompt=args.prompt, deploy=args.deploy, suffix=args.suffix)
