import os, sys, shutil
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load Gemini API key
ROOT = Path('.')
load_dotenv(ROOT / '.env')
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

out_dir = ROOT / 'vault/06 Assets/generated_cgs/v3'
bust_grid = out_dir / 'cast_bust_grid_ref.jpg'
ref_ep1 = out_dir / 'cg_ep1_disaster_v3c_raw.jpg'
artifact_dir = Path(r'C:\Users\kwhyc\.gemini\antigravity\brain\6ec94b55-6958-434a-97e1-f7ca71729f19')

STYLE = """CRITICAL STYLE: Render the image as a high‑contrast EFAM DAO wood‑cut illustration – bold black‑ink cross‑hatching on characters, props and foreground, with a dry‑brush watercolor wash only on the background planes. Use the attached `cast_bust_grid_ref.jpg` as the primary style reference (ink density, line weight, edge‑to‑edge bleed). Enforce deep black ink for all character outlines and structural elements. Limit watercolor to far background only; keep foreground and midground pure wood‑cut ink. Preserve the exact 3‑plane depth layout described below.
"""

EXP_A = STYLE + """
SCENE: Episode 2 Disaster — 'The Payout Freezes, the Stage Empties' (Lisbon Showcase Backstage — Reverse Angle).
- CAMERA: Dramatic low‑angle deep‑focus movie still shot from the edge of the parted backstage curtain looking across the backstage area.
- PLANE 1 — EXTREME FOREGROUND (RIGHT): CLARA in close‑up foreground on the right, standing rigid in the cold blue spill of the stage curtain, clutching the closed leather ledger and clipboard tightly against her slate‑blue blazer, her face turned slightly away in tense, conflicted guilt.
- PLANE 2 — MIDGROUND (CENTER): XOCHIT stepping urgently between Clara and Koraba, leaning over a backstage road case with one hand reaching toward Clara and the other toward Koraba in a desperate plea to stop the split.
- PLANE 3 — BACKGROUND (LEFT): KORABA in the background left beside a backstage equipment rack, slamming shut his laptop lid with one hand and slinging his kora harp over his shoulder to walk out, while in the background centre‑right through the curtain gap, a harsh white‑blue spotlight illuminates an empty microphone stand on an abandoned stage.
- PALETTE & LIGHTING: Moody backstage charcoal‑sepia ink crosshatching, cold slate‑blue spotlight beams, and bruised crimson‑amber tea‑stain washes.
"""

EXP_B = STYLE + """
SCENE: Episode 2 Disaster — 'The Payout Freezes, the Stage Empties' (Lisbon Showcase Backstage).
- PLANE 1 — EXTREME FOREGROUND (LEFT): Low‑angle close‑up of KORABA beside a dark backstage road‑case crate, his face etched with hurt and bitter resolve. His right hand firmly closes the lid of a dark laptop on top of the road case (pulling his game offline), while his left hand holds the wooden neck of his kora harp strapped to his shoulder.
- PLANE 2 — MIDGROUND (CENTER): XOCHIT leaning forward urgently behind the road case between Koraba and Clara, one hand resting on the road case and her other hand reaching out in an anguished plea to stop the split.
- PLANE 3 — DEEP BACKGROUND (RIGHT): CLARA standing isolated in the distance by the parted dark backstage curtain, clutching her closed leather ledger and clipboard tightly to her chest in rigid, conflicted guilt. Beyond her through the curtain gap, a harsh cold spotlight shines down onto an empty, abandoned stage microphone stand.
- PALETTE & LIGHTING: Moody backstage charcoal‑sepia ink crosshatching, cold slate‑blue spotlight beams, and bruised crimson‑amber tea‑stain washes.
"""

def generate(name, prompt):
    contents = [
        types.Part.from_bytes(data=bust_grid.read_bytes(), mime_type='image/jpeg'),
        types.Part.from_bytes(data=ref_ep1.read_bytes(), mime_type='image/jpeg'),
        prompt,
    ]
    resp = client.models.generate_content(
        model='gemini-3.1-flash-image-preview',
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(aspect_ratio='16:9', image_size='512'),
        ),
    )
    out_path = out_dir / f'{name}.jpg'
    for part in resp.candidates[0].content.parts:
        if part.inline_data:
            out_path.write_bytes(part.inline_data.data)
            break
    # Log usage (approx $0.015 per image)
    import generate_cg_v3 as gcg
    gcg.log_usage(name, prompt, 0.015)
    shutil.copy2(out_path, artifact_dir / f'{name}.jpg')
    print(f'Saved {out_path}')

generate('cg_ep2_disaster_512_expA_style', EXP_A)
generate('cg_ep2_disaster_512_expB_style', EXP_B)
