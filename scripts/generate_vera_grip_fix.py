import os, sys, json, base64, requests, datetime
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("[ERROR] GEMINI_API_KEY not found!")
    sys.exit(1)

USAGE_LOG_PATH = os.path.join("vault", "06 Assets", "generation_usage_log.json")
COST_PER_IMAGE_USD = 0.030

def log_usage(character: str, prompt_snippet: str):
    log_data = {"total_spent_usd": 0.0, "total_images": 0, "generations": []}
    if os.path.exists(USAGE_LOG_PATH):
        try:
            with open(USAGE_LOG_PATH, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        except Exception:
            pass

    log_data["total_spent_usd"] = round(log_data.get("total_spent_usd", 0.0) + COST_PER_IMAGE_USD, 3)
    log_data["total_images"] = log_data.get("total_images", 0) + 1
    log_data["generations"].append({
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "character": character,
        "model": "gemini-3.1-flash-image",
        "cost_usd": COST_PER_IMAGE_USD,
        "cumulative_spent_usd": log_data["total_spent_usd"],
        "prompt_snippet": prompt_snippet[:120] + "..."
    })

    with open(USAGE_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

    print(f"[USAGE] Cumulative spend: ${log_data['total_spent_usd']:.3f} ({log_data['total_images']} images)")

img1_path = "vault/06 Assets/gold_bust_prototypes/vera_inpainted_no_hand.jpg"
img2_path = "vault/06 Assets/gold_bust_prototypes/hand_grip_ref.jpg"

parts = []
# Image 1: Vera without flat hand
with open(img1_path, "rb") as f:
    b64_1 = base64.b64encode(f.read()).decode("utf-8")
parts.append({
    "inlineData": {
        "mimeType": "image/jpeg",
        "data": b64_1
    }
})

# Image 2: Hand grip reference
with open(img2_path, "rb") as f:
    b64_2 = base64.b64encode(f.read()).decode("utf-8")
parts.append({
    "inlineData": {
        "mimeType": "image/jpeg",
        "data": b64_2
    }
})

instructions = (
    "You are an expert 3D character sculptor and concept artist.\n"
    "Image 1 shows Vera's approved character design, face, knowing smile, princess tiara crown, wrap dress, and gear brooch.\n"
    "Image 2 shows the exact hand grip pose required for Vera's lower hand: an elegant hand sculpted from 24-karat gold with fingers curled firmly around the cylindrical handle of a closed gold folding fan.\n\n"
    "Task:\n"
    "Create an updated waist-up visual novel character sprite of Vera sculpted entirely out of solid polished reflective 24-karat yellow gold metal.\n"
    "- STRICTLY PRESERVE Vera's face, facial features, knowing smirk, direct gaze, princess tiara crown, architectural wrap dress, and gear brooch from Image 1.\n"
    "- CRITICAL LOWER HAND POSE: Vera's lower hand at waist height MUST hold a closed ornate gold folding fan with the natural, fingers-curled grip from Image 2. Her fingers (index, middle, ring, pinky) must be curved and wrapped completely around the cylindrical handle like holding a baton or wand, with her thumb locked across the curled fingers. The fan handle passes directly through her closed grip, and the closed ribbed fan extends outward.\n"
    "- ABSOLUTELY NO OPEN HAND, NO FLAT SPLAYED FINGERS RESTING OVER FAN SLATS, NO HOVERING PALM, NO CLAW HAND. The hand MUST be an anatomically correct closed hand encircling the fan handle.\n\n"
    "CRITICAL BACKGROUND INSTRUCTION:\n"
    "Generate this character completely isolated against a uniform, flat, solid bright vibrant MAGENTA background (#FF00FF / chroma key magenta backdrop), perfectly uniform across the entire canvas with no floor, no ground shadows, and crisp silhouette edges for chroma keying.\n\n"
    "Strict negative constraints (AVOID COMPLETELY): open hand, flat fingers, fingers splayed over fan slats, hand hovering over fan, palm resting flat on fan, uncurled fingers, claw hand, fan glued to palm, impossible hand grip, flat palm, straight fingers, fan headdress, giant fan hair, 2D illustration, drawing, painting, sketch."
)

parts.append({"text": instructions})

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent?key={api_key}"
headers = {"Content-Type": "application/json"}
payload = {"contents": [{"parts": parts}]}

print("Sending request to Gemini 3.1 Flash Image...")
response = requests.post(url, headers=headers, json=payload, timeout=90)
if response.status_code != 200:
    print(f"[ERROR] API failed {response.status_code}: {response.text}")
    sys.exit(1)

res_json = response.json()
img_b64 = res_json["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
raw_out = "vault/06 Assets/gold_bust_prototypes/vera_neutral_gold_raw.jpg"
with open(raw_out, "wb") as f:
    f.write(base64.b64decode(img_b64))

print(f"[OK] Saved raw render: {raw_out}")
log_usage("vera", "Vera neutral with dual-reference: inpainted keeper + dedicated hand grip ref")

# Run processing
import subprocess
proc_cmd = [
    "python", "scripts/process_gold_sprite.py",
    raw_out,
    "vault/06 Assets/gold_bust_prototypes/vera neutral gold waistup (560x880).png",
    "--stage-preview", "vault/06 Assets/gold_bust_prototypes/vera_gold_waistup_stage_preview.png",
    "--check-path", "vault/06 Assets/gold_bust_prototypes/vera_transparency_check.png"
]
subprocess.run(proc_cmd, check=True)
print("[DONE] Vera sprite processed!")
