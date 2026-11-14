#!/usr/bin/env python3
"""
generate_cg_v4.py
v4 Full-Art 16:9 (1920x1080) Outcome CGs (Episodes 1-4 Disaster and Happy pairs).

What changed from v3, and why:
- v3 ordered a sprite lineup. Its shared style said "knees/hips up, faces and
  props in the upper two-thirds, lower garments to the bottom edge", and every
  scene then blocked the cast as left / center / right, standing, facing out.
  The model obeyed that, and the 3-panel front-facing cast reference sheet
  gave it a lineup to copy. Result: eye-level medium shot, three figures
  equally spaced, all facing the camera, no depth, no motion.
- v4 orders a camera shot. Each scene opens with its own CAMERA block, then
  a DECISIVE MOMENT (one action mid-flight, not a state), then DEPTH
  (foreground / midground / background at very different scales, with at
  least one body cropped by the frame edge). No scene shares another scene's
  camera. The cast reference is now style and face only, never pose or
  framing. Character style, palette, and no-text rules are unchanged, so this
  is a framing fix, not a style restart.

Shot list, one camera per CG so the set stops looking like eight sprites:
- ep1 disaster: low Dutch tilt from crate height, Koraba huge and cropped
- ep1 happy: tight over-shoulder, looking down into the glowing phone
- ep2 disaster: low, over Clara's shoulder, diagonal table, Koraba lunging
- ep2 happy: very low wide stage shot, looking up at the mandala
- ep3 disaster: high, almost top-down over the cacao table, hands from edges
- ep3 happy: tight, just above the table, stamp coming down in foreground
- ep4 disaster: extreme close-up Dutch tilt on Clara's finger leaving the key
- ep4 happy: close three-quarter at desk height, wallet large in foreground

Test rule, from the keeper skill: run ONE CG first with --suffix v4a, compare
it to the v3 keeper side by side, and only then run the rest. Do not change
style and framing in the same run.
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
    "This is ONE cinematic film still, one manga panel, one decisive moment. It is NOT a character lineup, NOT a sprite sheet, and NOT a group portrait.\n"
    "1) CHARACTERS (FOREGROUND): Render Koraba, Xochit, and Clara in the EXACT HIGHLY STYLIZED, flat-plane hand-carved "
    "woodcut / folk-engraving style and non-realistic geometric facial proportions shown in Reference Image 1 "
    "(GIANT oversized heavy-lidded half-moon horizontal almond eyes spanning temple-to-temple, long razor-thin vertical geometric noses, "
    "tiny narrow mouths, sharply tapered narrow chins, long slender cylindrical necks, bold black/umber etched contours, "
    "and coarse parallel woodcut hatching in warm ochre, antique ivory, slate-blue, and terracotta). "
    "Take ONLY face, hair, costume, and carving style from Reference Image 1. Do NOT copy its front-facing pose, its spacing, its lineup, or its eye contact with the camera.\n"
    "2) ENVIRONMENT & ATMOSPHERE (BACKGROUND/MIDGROUND): Render the surrounding setting in the loose, line-free wet-on-wet "
    "tea, coffee, and watercolor stain wash style of Reference Image 2 on warm antique ivory paper (with capillary blooms, "
    "tide rings, and negative-space light pockets, enriched with deeper umber, charcoal, crimson, or golden wash accents for dramatic impact).\n"
    "3) CAMERA & COMPOSITION (CRITICAL, OVERRIDES ANY DEFAULT): Follow the CAMERA block at the start of the scene prompt exactly. "
    "Never default to an eye-level medium shot. Never place all three characters at the same distance, the same height, and the same size. "
    "In every shot, at least one character is cropped by the frame edge, at least one is much larger or much smaller than the others, and at least one is in profile or three-quarter view, looking at another character or at an object, never at the camera. "
    "Build real depth: a large foreground element (a shoulder, a hand, a prop, a crate edge) close to the lens, a midground action, and a smaller background figure or setting. "
    "Use diagonal lines, off-center placement, and empty negative space. Fill the entire 16:9 frame edge-to-edge, full-bleed, no border, no margin strip.\n"
    "4) ACTION: Show one decisive instant mid-flight, a verb happening now, not a state of standing. An object is falling, spilling, being grabbed, being offered, or just slipping away. Bodies lean, reach, recoil, or lunge. Hands are doing the story, not resting at sides.\n"
    "5) CLICKBAIT THUMBNAIL READ (CRITICAL): This image must also work as a 512x288 YouTube thumbnail and scenario card, readable in one second at small size. One huge emotion, one huge object, one clear idea. The main face is large, close, and exaggerated, not small and subtle. The main object is large and unmistakable. Silhouettes must read as dark shapes against a light wash or light shapes against a dark wash. No three equal faces, no three equal ideas, no fine detail as the point of the image. If you shrink this to thumbnail size, a stranger must still get the story instantly.\n"
    "6) OUTCOME POLARITY: Disaster and happy must look like opposites, not two versions of the same warm scene. Disaster is dark, tilted, broken, cold, red and black, faces in shock, horror, or fury, the key object failing, empty, spilling, or being taken away. Happy is bright, upright, open, warm gold, faces in open relief, laughter, or pride, the key object glowing, held up, shared, or succeeding. Push both ends hard, do not meet in the middle.\n"
    "ABSOLUTELY NO text, NO letters, NO numbers, NO readable screens, NO UI labels, NO watermarks."
)

DISASTER_POLARITY = (
    "OUTCOME: DISASTER. Make it obviously bad at thumbnail size. Exaggerated horrified or furious faces, wide eyes, open mouths, recoiling or lunging bodies. "
    "Dark, cold, tilted composition, heavy black and crimson washes, the key object clearly failing: blank, empty, spilling, breaking, or being blocked. "
    "The mood must read as WRONG and URGENT, not tense but tasteful."
)

HAPPY_POLARITY = (
    "OUTCOME: GOOD ENDING. Make it obviously good at thumbnail size. Exaggerated relieved, laughing, or proud faces, open smiles, relaxed open bodies leaning in together. "
    "Bright, upright, warm golden light, the key object clearly succeeding: glowing, held up, shared, or landing. "
    "The mood must read as RELIEF and TRIUMPH, not just calm and warm."
)


CG_CONFIGS = {
    "cg_ep1_disaster": {
        "ep_id": "ep1_keys",
        "mood": "disaster",
        "bg_ref": "bg lisbon_airport.png",
        "prompt": (
            "Scene: Episode 1 Disaster, 'The $60,000 Transfer Is Gone' at Lisbon Airport after midnight.\n"
            "CAMERA: Low angle Dutch tilt, camera down at crate height on the wet terminal floor, looking up. Wide 16:9, diagonal rain-streaked windows slicing the top of frame.\n"
            "DECISIVE MOMENT: Koraba has just lifted his phone and the screen has just gone pale and blank. He is staring at it, frozen mid-lift.\n"
            "DEPTH: FOREGROUND, Koraba huge at left, cropped at the shoulder and waist by the frame edge, kora strap cutting diagonally across his chest, phone thrust close to the lens in his raised hand. MIDGROUND, Xochit behind him and smaller, leaning in toward the phone, both hands pressed to her chest. BACKGROUND, Clara small and far at right near the windows, ledger clutched tight, turned half away, face in profile. Wooden elixir crates loom at left behind a sagging customs barrier tape.\n"
            "Characters: EXACTLY THREE PEOPLE, no fourth person, no coins, no other props crossing the frame. Koraba, dark crown locs, beaded strands, ochre/indigo woven wrap, gourd kora strapped across his shoulder. Xochit, red/gold beaded headband, red/black cheek and chin face paint, diamond fringe earrings, woven huipil. Clara, blonde coiled side bun, slate-blue patterned blazer, red lanyard, closed ledger and a single brass key held against her chest.\n"
            "Atmosphere and Palette: Tense midnight indigo-grey, scorched espresso-umber, and bruised crimson-amber watercolor washes streaking down the tall rain-wet terminal windows behind them, angling toward the stranded crates."
        ),
    },
    "cg_ep1_happy": {
        "ep_id": "ep1_keys",
        "mood": "happy",
        "bg_ref": "bg lisbon_airport.png",
        "prompt": (
            "Scene: Episode 1 Good Outcome, 'The $1 Test Transfer Lands and 2-of-3 Shared Custody' at Lisbon Airport.\n"
            "CAMERA: Tight over-shoulder shot, camera just behind Xochit's shoulder, looking down into the hands. Shallow, intimate, no one faces the camera.\n"
            "DECISIVE MOMENT: The small phone at chest height has just lit up with a soft warm golden star-shaped glow, and all three hands are converging on it at once.\n"
            "DEPTH: FOREGROUND, Xochit seen only from behind: her shoulder and long beaded hair large at the left edge, cropped by the frame, her face never visible. MIDGROUND, Koraba's hand and Clara's hand reaching in from opposite sides, Clara's palm open offering the shared 2-of-3 hardware key token, Koraba's kora neck angling in from the left. BACKGROUND, exactly TWO people shown as complete upper bodies with necks, shoulders, arms and torsos fully attached (never floating heads): Koraba at left and Clara at right, both leaning in over the table in profile, looking down at the phone with relief, their torsos continuing down behind the table edge; Xochit is NOT in the background, she is only the foreground shoulder, dawn light breaking through the terminal glass behind them, open elixir crates soft and out of focus.\n"
            "Characters: EXACTLY THREE PEOPLE and therefore exactly THREE heads in the image in total (Xochit's head is the large back-of-head in the foreground, plus two background heads), no fourth person, no extra hands or arms from other people, no text anywhere. Koraba, left, with his gourd kora instrument. Xochit, right, holding her carved star cacao bowl low in her other hand. Clara, center, in her slate-blue blazer.\n"
            "Atmosphere and Palette: Warm golden dawn chamomile and amber tea washes breaking through the airport terminal glass."
        ),
    },
    "cg_ep2_disaster": {
        "ep_id": "ep2_lisbon",
        "mood": "disaster",
        "bg_ref": "bg showcase_backstage.png",
        "prompt": (
            "Scene: Episode 2 Disaster, 'The Showcase Freezes' backstage at the Lisbon venue.\n"
            "CAMERA: Low shot over Clara's shoulder, looking down the length of a folding production table that cuts diagonally across the whole frame. The table edge is the horizon line.\n"
            "DECISIVE MOMENT: Koraba is lunging across the table to unplug his laptop and pull his finished game offline, his arm fully extended, cable already taut. Clara is blocking him.\n"
            "DEPTH: FOREGROUND, Clara's raised hand and closed ledger, huge at right, blocking the laptop, her blazer shoulder cropped by the frame edge. MIDGROUND, Koraba leaning hard across the table from the left, woven wrap and kora swinging with the lunge, face in three-quarter view and ANGRY, not surprised: brows crushed down hard into a V, eyes narrowed into a glare at Clara's hand and the laptop, teeth bared in a snarl, jaw clenched, neck tendons tight. His eyes must NOT be wide open.  BACKGROUND, Xochit stepping decisively between them, smaller, both hands raised outward to stop the collapse, backstage curtain and cold stage spotlights spilling in above her.\n"
            "Characters: EXACTLY THREE PEOPLE in the whole frame, no fourth person anywhere. Koraba, left, wearing his woven wrap and his kora exactly as in Image 1: a West African kora with a large round polished brown calabash-gourd body with a small rectangular sound-hole cut into it, a very long straight slender wooden neck rising diagonally from it, and many thin strings running from the neck down over a bridge; NOT a banjo, NOT a lute, NOT a guitar, no round drum face. Xochit, center background, in her patterned huipil and red/black face paint. Clara is NOT fully in frame: at the right edge only her raised open hand and a slice of her slate-blue blazer shoulder and sleeve enter the frame, her head and face are out of frame above the top edge; there is no other woman and no one seated or standing behind the laptop. No coins or tokens anywhere. The laptop and table at right are empty of people.\n"
            "Atmosphere and Palette: Harsh cold empty stage spotlights spill through the parted backstage curtain above them against dark charcoal-sepia and tense amber-crimson washes. Coiled cables and road cases crowd the lower frame, out of focus. No readable text on screens."
        ),
    },
    "cg_ep2_happy": {
        "ep_id": "ep2_lisbon",
        "mood": "happy",
        "bg_ref": "bg showcase_stage.png",
        "prompt": (
            "Scene: Episode 2 Good Outcome, 'The Work Speaks for Itself' on the Lisbon Showcase Stage.\n"
            "CAMERA: Very low wide stage shot, camera on the stage floor looking up. The projection screen fills the whole top half of the frame like a sky.\n"
            "DECISIVE MOMENT: Koraba is mid-strum on his kora, head tilted back, playing with joy, while Xochit lifts the anonymous neutral-avatar scroll high and Clara lowers her ledger.\n"
            "DEPTH: FOREGROUND, the stage floor and the bottom curve of Koraba's gourd kora, large at the bottom edge. MIDGROUND, the three in a loose open arc, not a line: Koraba center and largest, playing, Xochit left and a step back holding the scroll up, Clara right and a step back, her supportive hand reaching toward Koraba's shoulder, all in three-quarter view. BACKGROUND, a large circular projection screen glowing with a radiant watercolor mandala and constellation wash, no text, washing them in gold.\n"
            "Characters: EXACTLY THREE PEOPLE, no fourth person, no extra hands or arms from other people, no text anywhere. Koraba, center, playing his gourd kora with joy and pride. Xochit, left, holding up the anonymous neutral-avatar scroll and papers with a warm vindicated smile. Clara, right, lowering her ledger with humble accountability and respect.\n"
            "Atmosphere and Palette: Luminous chamomile gold, warm amber stage light, and soft Earl Grey sepia washes."
        ),
    },
    "cg_ep3_disaster": {
        "ep_id": "ep3_agreements",
        "mood": "disaster",
        "bg_ref": "bg cacao_circle.png",
        "prompt": (
            "Scene: Episode 3 Disaster, 'The Handshake Split Collapses' at the ceremonial cacao circle.\n"
            "CAMERA: Steep high angle, almost top-down, with a strong Dutch tilt of about 20 degrees so the whole table slopes diagonally downhill. Faces seen from above, bodies cropped hard by the frame edges. Extreme foreshortening, the foreground is enormous.\n"
            "DECISIVE MOMENT: A suited arm has just SLAMMED a thick stack of papers with a red wax and ribbon seal onto the altar cloth, the impact knocking the carved cacao bowl over. A huge river of dark cacao is mid-splash and flooding diagonally across the whole table toward the lower-left corner, with big splash droplets in the air. Large round token discs are flying and tumbling through the air in every direction, some far in front of the lens, some still bouncing off the table.\n"
            "DEPTH: FOREGROUND, gigantic: the overturned bowl and the cacao flood at the bottom, and several huge coins tumbling close to the lens, partly cropped by the bottom edge. RIGHT SIDE, one enormous dark-suit arm cropped at the frame edge, its hand slamming down on the papers and grabbing at the coins: people coming to take their money. MIDGROUND, Koraba at left and Xochit at center, slumped and collapsing over the table, reaching listlessly toward the flood, faces slack, hollow-eyed and DRAINED. BACKGROUND, ONE Clara only at the far top edge, small, both hands pressed to her head, drained and defeated, nothing in her hands, no clipboard. No boxes, cubes or extra props on the table.\n"
            "Characters: EXACTLY THREE PEOPLE in the frame plus ONE disembodied dark-suited arm from the right edge grabbing at the papers and coins (a lawsuit taking their money); no other person, no other arm. ALL THREE ARE DEPRESSED, DRAINED AND DEFEATED: slumped shoulders, heavy hollow eyes, slack mouths, grey exhausted faces, nobody angry and nobody screaming. This sad emotion OVERRIDES any generic angry or wide-eyed-horror wording. Koraba, left, in his woven wrap with dark locs, face drained and hollow, eyes down at the table. Xochit, center, in her patterned huipil and red/black face paint, hands reaching for the bowl, face drained and hollow, eyes heavy. Clara, ONE person, far top edge, in her slate-blue blazer, small, holding her head with both hands. NO text, letters or words anywhere: the papers show only blank carved lines, the seal is a plain blob. Every surface is hand-carved woodblock with dense engraved hatching.\n"
            "Atmosphere and Palette: Collision of warm ceremonial ochre with cold slate-charcoal and bruised crimson tea stains. No legible text."
        ),
    },
    "cg_ep3_happy": {
        "ep_id": "ep3_agreements",
        "mood": "happy",
        "bg_ref": "bg cacao_circle.png",
        "prompt": (
            "Scene: Episode 3 Good Outcome, 'The Agreement Holds' at the ceremonial cacao circle.\n"
            "CAMERA: Tight shot just above the table, low and close, looking across the open charter scroll. The scroll fills the bottom third like a landscape.\n"
            "DECISIVE MOMENT: Koraba and Xochit are both mid-signature on the large formal cooperative charter scroll, pens touching paper at the same instant, while Clara is bringing the official four-point-star cooperative stamp down toward the page.\n"
            "DEPTH: FOREGROUND, the star stamp gripped in Clara's hand, huge and close at top center, coming straight down toward the scroll, the hand attached to her sleeve and arm that rises out of frame; Clara's head is cropped out above the top edge so no head appears near the stamp. MIDGROUND, the scroll itself, the steaming star-carved cacao bowl at left, and the sturdy glass treasury reserve jar filled with golden coins and tokens at right. BACKGROUND, only Koraba at left and Xochit at right, leaning in over the table in profile, signing, warm dawn light behind them. No person stands behind the table.\n"
            "Characters: EXACTLY THREE PEOPLE, of whom two heads are visible (Koraba and Xochit) and Clara is only an arm and torso with her head out of frame, no fourth person, no extra hands or arms from other people, no text anywhere. Koraba, left, signing. Xochit, right, signing. Clara, center between them, holding the stamp and shared ledger as an accountable steward.\n"
            "Atmosphere and Palette: Harmonious golden chamomile, warm terracotta, and rich coffee-amber washes with interwoven textile geometry."
        ),
    },
    "cg_ep4_disaster": {
        "ep_id": "ep4_apothecary",
        "mood": "disaster",
        "bg_ref": "bg treasury_fire.png",
        "prompt": (
            "Scene: Episode 4 Disaster, 'One Tired Click Drained the Apothecary' at 1:14 A.M.\n"
            "CAMERA: Extreme close-up, Dutch tilt, camera inches from the laptop. Clara's face and hand fill most of the frame. The doorway is tiny in the distance.\n"
            "DECISIVE MOMENT: Clara's finger has just left the laptop key, a fraction of a second too late. A sinister dark espresso-and-crimson stain current is already swirling upward out of an open treasury vessel on the desk, draining glowing golden tokens away into a dark vortex.\n"
            "DEPTH: FOREGROUND, Clara's hand and the laptop key, huge at bottom center, her face in profile at right, hair slightly disheveled from fatigue, eyes wide in horror, cropped at the top and right edges. MIDGROUND, the treasury vessel and the spiraling vortex of tokens rising from it. BACKGROUND, the upper-left doorway, small and far, where Koraba and Xochit are bursting into the room, tiny and out of focus, arms raised in alarm, trying to stop the click.\n"
            "Characters: EXACTLY THREE PEOPLE, no fourth person. Clara, foreground right, exhausted, in her slate-blue blazer, one finger just lifting off the laptop key, face in horror. Koraba and Xochit, tiny in the background doorway, in their woven wrap and huipil, arms raised. Laptop screen shows only abstract carved shapes, no words or numbers. Every surface is hand-carved woodblock with dense engraved hatching.\n"
            "Atmosphere and Palette: High-contrast sinister crimson hibiscus-tea, scorched espresso-soot, and flickering candle amber washes. No readable UI text."
        ),
    },
    "cg_ep4_happy": {
        "ep_id": "ep4_apothecary",
        "mood": "happy",
        "bg_ref": "bg apothecary.png",
        "prompt": (
            "Scene: Episode 4 Good Outcome, 'The Hex Is Caught in Time' in the Herbal Apothecary.\n"
            "CAMERA: Low angle looking up from the desk surface with a strong Dutch tilt of about 15 degrees, wide-angle and close, so the figures tower over the lens and the room slants. Dynamic, not straight-on, nobody centered.\n"
            "DECISIVE MOMENT: CELEBRATION. Clara has just thrust the small hardware wallet high toward the lens in a triumphant raised fist, mouth open in a laugh. Koraba and Xochit explode with joy beside her, throwing their arms up and grabbing each other in a half hug. On the desk below, a luminous golden timelock ring bursts outward from the treasury vessel, blasting the dark stain away in a ring of light and sparks.\n"
            "DEPTH: FOREGROUND, enormous: Clara's fist and the hardware wallet thrust close to the lens at right, foreshortened, her arm cropped by the frame edge, and the burst of golden light and sparks from the vessel across the bottom. MIDGROUND, Koraba at left and Xochit at center-left caught mid-jump, arms thrown up, faces tilted up laughing, bodies leaning at diagonals. BACKGROUND, Clara's laughing face and shoulders high at right above her fist, with shelves of herbal bottles tilted and blurred behind, golden daylight streaming in. Exactly three people, complete bodies, no floating heads.\n"
            "Characters: EXACTLY THREE PEOPLE, no fourth person, no extra hands or arms from other people, no text anywhere. Clara, center, holding the hardware wallet. Koraba, left. Xochit, right.\n"
            "Atmosphere and Palette: Calm, triumphant golden daylight chamomile, sage-amber, and warm sepia watercolor washes."
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
        "asset": f"{cg_name} (v4 full-art 16:9 CG)",
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
    NOTE v4: this sheet is face and style only. The prompt now explicitly tells
    the model not to copy its pose, spacing, or lineup.
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

        tex_luma = (0.299 * tex_np[:, :, 0] + 0.587 * tex_np[:, :, 1] + 0.114 * tex_np[:, :, 2]) / 255.0
        tex_mean = float(np.mean(tex_luma))
        weave_centered = (tex_luma - tex_mean)[..., None]

        cg_luma = (0.299 * cg_np[:, :, 0] + 0.587 * cg_np[:, :, 1] + 0.114 * cg_np[:, :, 2]) / 255.0
        paper_weight = np.clip((cg_luma - 0.18) / 0.72, 0.0, 1.0)[..., None]

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

    thumb_im = cg_1080.resize((512, 288), Image.Resampling.LANCZOS)
    thumb_out = os.path.join(OUT_DIR, f"{cg_key}_thumb.png")
    thumb_game = os.path.join(REPO_ROOT, "game", "images", f"{cg_key}_thumb.png")
    thumb_im.save(thumb_out)
    thumb_im.save(thumb_game)
    print(f"[SAVED] Thumbnail (512x288) -> {thumb_game}")

    card_w, card_h = 512, 285
    card_rgb = cg_1080.resize((card_w, card_h), Image.Resampling.LANCZOS).convert("RGBA")

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
    polarity = DISASTER_POLARITY if cfg["mood"] == "disaster" else HAPPY_POLARITY
    full_prompt = f"{SHARED_CG_STYLE}\n\n{polarity}\n\n{scene_prompt}"

    cast_ref_path = build_cast_reference_sheet()
    bg_ref_path = os.path.join(REPO_ROOT, "game", "images", cfg["bg_ref"])

    with open(cast_ref_path, "rb") as f:
        cast_b64 = base64.b64encode(f.read()).decode("utf-8")
    with open(bg_ref_path, "rb") as f:
        bg_b64 = base64.b64encode(f.read()).decode("utf-8")

    tag_name = f"{cg_key}_{suffix}" if suffix else cg_key
    print(f"\n==================================================")
    print(f"Generating v4 Full-Art 16:9 CG: {tag_name}")
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
                "in their approved HIGHLY STYLIZED hand-carved woodcut/engraved art style and non-realistic geometric facial proportions. "
                "Use Reference Image 1 ONLY for face, hair, costume, and carving style. Do NOT copy its front-facing pose, its spacing, its lineup, or its eye contact with the camera. "
                "Reference Image 2 shows the approved wet-on-wet tea/coffee watercolor wash background setting on warm ivory canvas.\n\n"
                f"{full_prompt}\n\n"
                "Strict Negative Constraints (DO NOT INCLUDE): "
                "realistic human facial proportions, generic comic/anime faces, text, letters, numbers, typography, UI screens with text, "
                "captions, logos, watermarks, stiff front-facing lineup, eye-level medium shot of three full figures, three figures equally spaced at the same size, all characters facing the camera, centered symmetrical composition, heads cut off, key action hidden in bottom 25% of frame."
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
    parser = argparse.ArgumentParser(description="Generate v4 Full-Art 16:9 Outcome CG")
    parser.add_argument("cg_key", choices=list(CG_CONFIGS.keys()), help="CG slot name to generate")
    parser.add_argument("--prompt", help="Optional custom prompt override")
    parser.add_argument("--suffix", default="", help="Optional suffix for A/B comparison, use v4a for the first test")
    args = parser.parse_args()
    generate_cg(args.cg_key, custom_prompt=args.prompt, suffix=args.suffix)
