#!/usr/bin/env python3
"""v4 low-res test: role-labelled refs (3 subject, 1 style, 1 composition sketch). Never touches game/images.
Usage: cg_v4_test.py cg_ep1_disaster [tag]   -> writes <key>_<tag>_sketch.jpg and <key>_<tag>_v4.jpg in generated_cgs/v3"""
import base64, io, os, sys, importlib.util, requests
from dotenv import load_dotenv
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("g", os.path.join(HERE, "generate_cg_v4.py")); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
A = os.path.join(g.REPO_ROOT, "vault", "06 Assets"); D = os.path.join(A, "2026-11-11 character designs (EFAM DAO)")
MODEL = "gemini-3.1-flash-image"

CAMERA = {
 "cg_ep1_disaster": ("Extreme LOW-ANGLE DUTCH-TILT shot, camera on the wet floor looking up. Koraba fills the left foreground, huge, cropped at the chest, "
   "his hand raised in the near foreground holding the blank phone toward camera, kora strap diagonal across frame. Xochit mid-ground right, turned away "
   "from him and bent forward, one hand on a crate, other at her mouth. Clara tiny and far, a small silhouette deep in the rain-streaked terminal window "
   "at the top-right vanishing point, back half-turned, key clutched. Crates stacked as strong diagonal leading lines. Big scale contrast, strong depth, no lineup."),
}

def b64(p, thumb=None):
    im = Image.open(p).convert("RGB")
    if thumb: im.thumbnail(thumb)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=92); return base64.b64encode(buf.getvalue()).decode()
def img(data): return {"inlineData": {"mimeType": "image/jpeg", "data": data}}
def call(parts, size=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={os.environ['GEMINI_API_KEY']}"
    r = requests.post(url, json={"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE", "TEXT"], "imageConfig": ({"aspectRatio": "16:9", "imageSize": size} if size else {"aspectRatio": "16:9"})}}, timeout=180)
    r.raise_for_status()
    for p in r.json()["candidates"][0]["content"]["parts"]:
        if "inlineData" in p: return Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert("RGB")
    raise SystemExit("no image: " + r.text[:400])

def main():
    key = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else "t1"
    load_dotenv(os.path.join(g.REPO_ROOT, ".env")); cfg = g.CG_CONFIGS[key]
    scene = cfg["prompt"]
    # 1) composition sketch
    SK = os.environ.get("REUSE_SKETCH")
    if SK: sk_path = SK; sk = None
    else:
      sk = call([{"text": "Draw an ABSTRACT blocking diagram, 16:9: flat solid dark-gray and mid-gray SILHOUETTE SHAPES only on a pale ground, no faces, no features, no shading, no texture, no realism, no text. Figures are simple blocky cut-out shapes, props are plain boxes. Camera and staging only. Draw the people named, each with their own hands attached to their own arms. Include exactly the one extra dark-suited arm from the right edge if the scene names it, and no other disembodied arms or people. No cracks on the table. "
        "It must clearly show this exact camera angle and layout:\n" + "\n".join(l for l in scene.split("\n") if l.startswith(("CAMERA","DEPTH","DECISIVE","Characters"))) }], "512")
      sk.thumbnail((768, 432)); sk_path = os.path.join(g.OUT_DIR, f"{key}_{tag}_sketch.jpg"); sk.save(sk_path, quality=90)
    if os.environ.get('SKETCH_ONLY'): print('sketch', sk_path); return
    # 2) final with role-labelled refs
    kor = os.path.join(D, "Koraba_ The Bridge Keeper Dossier.png"); xo = os.path.join(D, "Xochit_ Ceremonial Weaver Character Sheet.png"); cl = os.path.join(D, "Clara_ The Registrar Character Sheet.png")
    def crop(p, box): im = Image.open(p).convert("RGB").crop(box); b = io.BytesIO(); im.save(b, "JPEG", quality=92); return base64.b64encode(b.getvalue()).decode()
    parts = [img(crop(kor, (0,0,790,745))), img(crop(xo, (0,0,790,735))), img(crop(cl, (0,0,725,745))),
             img(b64(os.path.join(g.OUT_DIR, "cg_ep1_disaster_t2_v4.jpg"))), img(b64(sk_path)),
      {"text": ("Image 1 = SUBJECT: Koraba. Image 2 = SUBJECT: Xochit. Image 3 = SUBJECT: Clara. Keep each one's face shape, hair, costume and props exactly. "
        "Image 4 = STYLE reference for a full SCENE: hand-carved woodblock print, concentric gouge-line hatching, stipple, flat limited palette, carved rain/sky/props, "
        "geometric woodcut faces, acting through posture and hands. Match this technique for every surface, including background. "
        "Image 5 = COMPOSITION reference: copy its camera angle, tilt, figure placement, scale contrast and depth exactly; it is only a silhouette diagram: ignore its shapes as art and redraw every figure from Images 1-3 in the Image 4 style. "
        "CRITICAL STYLE: high-contrast EFAM DAO WOODCUT illustration; bold deep-black carved ink outlines and engraved cross-hatching on characters, props and the whole foreground/midground; a dry-brush watercolor wash ONLY on the far background plane. Keep three clear depth planes. Characters keep the elongated geometric woodcut faces of Images 1-3, never realistic faces. "
        "Characters are NOT in a lineup and NOT facing camera.\n\nFull-bleed 16:9, no border, no text/letters/labels on any prop.\n\n" + scene +
        "\n\n" + (g.DISASTER_POLARITY if cfg["mood"]=="disaster" else g.HAPPY_POLARITY) + " Express it through the carved woodcut face geometry: the emotion the scene names (anger = crushed V brows, narrowed glaring eyes, bared teeth; shock = wide eyes), strong brows and posture, not realistic faces. The scene must also read as a 512x288 thumbnail: one huge emotion, one huge object.")}]
    SIZE = os.environ.get("IMG_SIZE"); out = call(parts, SIZE)
    if not SIZE: out.thumbnail((768, 432))
    op = os.path.join(g.OUT_DIR, f"{key}_{tag}_v4" + (".png" if SIZE else ".jpg")); out.save(op); print(out.size)
    g.log_usage(f"{key}_{tag}_v4", scene, 2 * g.COST_PER_IMAGE_USD); print("saved", op)
main()
