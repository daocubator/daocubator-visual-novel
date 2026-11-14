#!/usr/bin/env python3
"""Low-res woodblock-style prompt test. Never touches game/images. Usage: cg_style_test.py cg_ep1_disaster [tag]"""
import base64, io, os, sys, importlib.util, requests
from dotenv import load_dotenv
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("g", os.path.join(HERE, "generate_cg_v3.py")); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

STYLE = (
"Full-bleed 16:9 visual novel event CG, ENTIRE image rendered as ONE hand-carved WOODBLOCK PRINT / folk-engraving, exactly matching the "
"DAO character-prototype illustrations in the reference image (NOT a pen-and-ink comic, NOT a watercolor painting, NOT realistic).\n"
"STYLE RULES: flat-plane geometric figures with elongated faces, GIANT heavy-lidded almond eyes, razor-thin vertical noses, tiny mouths, "
"long slender necks; faces are calm, mask-like and nearly expressionless. Skin, wood, cloth and floor are filled with dense concentric / parallel "
"engraved gouge lines (thumbprint-like spiral hatching, wood-grain ridges) and fine stipple dots. Thick black-umber carved contours. "
"Strict limited palette: near-black umber, golden ochre, tan, ivory paper, plus only small accents (terracotta red, slate blue, sage). "
"Flat color fills, NO gradients, NO soft watercolor washes, NO photographic shading. Background and props (crates, windows, rain, architecture) "
"are ALSO carved woodblock: rain as parallel incised lines, night sky as black ground with stippled stars and spiral halos like the reference's cosmic halos.\n"
"ACTING: show emotion through body posture, hands and props, NOT through realistic facial expression.\n"
"COMPOSITION: edge-to-edge full-bleed, characters interacting (not a lineup, not facing camera), faces/hands/key props in the upper two-thirds, "
"scene continues to the bottom edge, no border or margin. NO text, letters, numbers or readable screens."
)

def main():
    key = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else "woodcut"
    load_dotenv(os.path.join(g.REPO_ROOT, ".env"))
    ref = os.path.join(g.OUT_DIR, "cast_dossier_hero_ref.jpg")
    b64 = base64.b64encode(open(ref, "rb").read()).decode()
    prompt = ("The reference image shows the three approved characters (left Koraba, center Xochit, right Clara) in their final woodblock-print style. "
              "Keep each character's design, costume and face-shape identical, and carry that SAME carved technique into the whole scene.\n\n"
              + STYLE + "\n\n" + g.CG_CONFIGS[key]["prompt"] +
              "\n\nAvoid: realistic faces, comic/anime faces, watercolor bleeding, gradients, text.")
    payload = {"contents": [{"parts": [{"inlineData": {"mimeType": "image/jpeg", "data": b64}}, {"text": prompt}]}],
               "generationConfig": {"responseModalities": ["IMAGE", "TEXT"], "imageConfig": {"aspectRatio": "16:9"}}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent?key={os.environ['GEMINI_API_KEY']}"
    r = requests.post(url, json=payload, timeout=180); r.raise_for_status()
    for p in r.json()["candidates"][0]["content"]["parts"]:
        if "inlineData" in p:
            im = Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert("RGB")
            im.thumbnail((768, 432)); out = os.path.join(g.OUT_DIR, f"{key}_{tag}_test.jpg"); im.save(out, quality=90)
            g.log_usage(f"{key}_{tag}_test", prompt, g.COST_PER_IMAGE_USD); print("saved", out); return
    print("no image", r.text[:500])
main()
