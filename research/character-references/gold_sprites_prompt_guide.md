# 3D Gold Character Sprites: Midjourney & Generator Prompt Guide

This guide contains calibrated prompts for generating all 6 visual novel characters in the approved **3D solid polished 24k gold sculpture** style.

---

## Technical Specifications
- **Style:** Monolithic solid polished reflective 24-karat gold 3D sculpture with specular edge highlights, warm amber occlusion shadows, and subtle photogrammetric 3D scan contours.
- **Framing:** Waist-up character portrait (hips/beltline to top of head).
- **Stance & Eye Direction:** 3/4 dynamic body posture, but **eyes and gaze turned directly toward the camera/viewer** to maintain player eye contact during visual novel dialogue.
- **Background:** Solid uniform pitch-black background (`#000000`), no floor, no shadows on ground, clean silhouette boundary for automated alpha keying.
- **Aspect Ratio:** `--ar 2:3` (scaled and anchored to $560 \times 880$ via [`scripts/process_gold_sprite.py`](file:///c:/Users/kwhyc/Workspace/Get%20Rich%20Together/scripts/process_gold_sprite.py)).

---

## Automated Post-Processing Pipeline
To convert any raw generated render into a live Ren'Py sprite:
```pwsh
python scripts/process_gold_sprite.py "<path_to_raw_image.jpg>" "game/images/<character> neutral.png" --preview "vault/06 Assets/gold_bust_prototypes/<character>_stage_preview.png" --check "vault/06 Assets/gold_bust_prototypes/<character>_magenta_check.png"
```
*Note: The script automatically keys out the outer background AND genuine arm-to-body pass-through voids while protecting 100% of internal clothing creases, lapels, buttons, and cuffs.*

---

## Live Configuration (JSON)
All active prompts are stored in:
👉 [`vault/06 Assets/character_prompts.json`](file:///c:/Users/kwhyc/Workspace/Get%20Rich%20Together/vault/06%20Assets/character_prompts.json)

The generator script [`scripts/generate_gold_character.py`](file:///c:/Users/kwhyc/Workspace/Get%20Rich%20Together/scripts/generate_gold_character.py) reads directly from this JSON file. Any edits made there will automatically apply on the next generation run.

---

## Character Prompts

### 1. Alex — Neutral (The Mercenary / Treasury Lead)
```text
Waist-up character portrait sprite of a handsome young business executive named Alex, standing in a dynamic 3/4 angled body pose with one shoulder closer to the camera and lower in a relaxed dropped-shoulder pose (natural asymmetric contrapposto stance, confident and lively, not stiff or squared-on). His head is turned at a natural 3/4 angle naturally aligned with his body, while his eyes are locked directly onto the viewer / camera making calm, calculating, composed direct eye contact with the player. He wears an impeccably tailored three-piece suit, dress shirt, and tie, holding a modern golden smartphone in his hands at waist level, comfortably contained within the canvas. Cleanly sculpted slicked-back modern hair with smooth continuous contours, no loose strands. The entire character, suit, hair, skin, hands, and phone are sculpted from a single monolithic solid polished reflective 24-karat yellow gold metal, matching the style and material of the reference image, with gleaming mirror-like specular highlights and warm amber reflections. Sharp studio rim lighting. Framed waist-up with generous margins on all borders. Absolute solid pitch-black background (#000000) with no floor, clean silhouette edges. --ar 2:3 --v 6.1 --style raw
```

---

### 2. Maya — Neutral (The Builder / Tech Lead)
```text
Waist-up character portrait sprite of a sharp, brilliant female software architect named Maya, standing in a dynamic 3/4 angled body pose with one shoulder closer to the camera than the other in an expressive dropped shoulder pose (natural contrapposto stance, asymmetric and lively, not stiff, not squared-on). Her head is turned at a natural 3/4 angle naturally aligned with her body, while her eyes are locked directly on the viewer / camera, making sharp, calm, confident direct eye contact with the player through her modern slim-frame glasses. She holds a sleek modern golden ultra-thin laptop tucked vertically under her arm against her ribs/hip, with her other arm resting naturally with the dropped shoulder, comfortably contained inside the canvas with generous margins on all sides (zero edge clipping). She has a sleek, cleanly sculpted low bun swept neatly behind her ear sculpted from smooth solid gold with continuous clean sculptural mass, no loose hanging strands, no floating wisps, no detached hair loops, ensuring a pristine smooth silhouette around her head, neck, and shoulders. She wears an athletic zip-up tech startup jacket with subtle circuit relief tracings over a casual crewneck. Entire figure, glasses, hair, jacket, laptop, and hands are crafted from seamless monolithic solid polished reflective 24-karat yellow gold metal, matching the molten metallic gold material of the reference image, with bright mirror-like specular highlights and crisp studio edge rim lighting. Framed comfortably waist-up with generous margins. Centered against an absolute pure solid pitch-black background (#000000) with no floor, no shadows, pristine clean edges. --ar 2:3 --v 6.1 --style raw
```

---

### 3. Jordan — Neutral (The True Believer / Community Lead)
```text
Waist-up character portrait sprite of an energetic, charismatic young community organizer named Jordan, standing in a dynamic 3/4 angled body pose with one shoulder closer to the camera and lower in a relaxed dropped-shoulder stance (natural asymmetric contrapposto posture, relaxed and alive, not stiff, not squared-on). Their head is turned at a natural 3/4 angle naturally aligned with their body, while their eyes are locked directly onto the viewer / camera, making warm, engaging, confident direct eye contact with the player. They have stylish textured curly hair sculpted as a single solid continuous sculptural mass with smooth, closed outer contours—absolutely no loose dangling strands, no wire wisps, and no floating loops. They wear an oversized streetwear hoodie with the hood resting comfortably down around the neck, featuring subtle embossed DAO and circuit emblems in gold relief, with their hands resting naturally in their front pockets / at waist level, fully contained within the frame with generous margins. Entire figure, sculpted curls, hoodie fabric folds, and hands are sculpted from seamless monolithic solid polished 24-karat yellow gold metal, matching the molten metallic gold material of the reference image, with gleaming specular highlights and deep warm reflections. Crisp studio rim lighting. Framed waist-up with generous margins. Isolated on a uniform solid pitch-black background (#000000), no floor, no shadows, clean silhouette edges. --ar 2:3 --v 6.1 --style raw
```

---

### 4. Atlas — Neutral (The Whale / Heavy Capital)
```text
Waist-up character portrait sprite of an authoritative, imposing senior investor named Atlas, standing in a commanding dynamic 3/4 angled body pose with one shoulder closer to the camera and lower in a natural dropped-shoulder stance (imposing contrapposto posture, commanding and lively, not stiff or squared-on). His head is held high and turned at a natural 3/4 angle in harmony with his body, while his eyes are locked directly onto the viewer / camera, delivering a calm, calculating, formidable direct gaze to the player. Distinguished swept-back hair sculpted as a continuous solid sculptural mass with smooth closed contours, sharp sculpted jawline. Wearing a luxury double-breasted wool trench coat with structured lapels and a gold silk lapel drape over a tailored suit, with one hand resting across his midsection / coat button showing sculpted rings on his fingers, fully contained within the frame with generous margins. The entire figure, hair, heavy coat, and hands are rendered as a solid monolithic polished reflective 24-karat yellow gold sculpture, matching the molten metallic gold material of the reference image, with dramatic specular edge lighting and deep amber occlusions. Framed waist-up with generous margins. Pure solid pitch-black background (#000000), no ground, clean sharp edges. --ar 2:3 --v 6.1 --style raw
```

---

### 5. Spectre — Neutral (The Ghost / Anonymous Founder)
```text
Waist-up character portrait sprite of an enigmatic, completely anonymous developer named Spectre, standing in a dynamic 3/4 angled silhouette posture facing towards the player with one shoulder slightly forward in a relaxed dropped-shoulder stance. Wearing an oversized tactical technical hooded cloak with the deep cowl pulled forward. The interior of the hood is a deep, impenetrable black hollow void with zero facial features visible (faceless anonymous shadow void). Only the sculpted fabric of the deep hood, high structured cowl collar, tactical jacket sleeves with embossed circuit relief tracings, and metallic gloved hands held quietly at waist level are sculpted from seamless solid polished reflective 24-karat yellow gold metal, matching the molten metallic gold material of the reference image, contrasting sharply with the pitch-black void beneath the cowl. Crisp studio edge rim lighting along the golden contours. Framed waist-up with generous margins on all sides, zero edge clipping. Solid uniform pitch-black background (#000000), no floor, clean silhouette cutout. --ar 2:3 --v 6.1 --style raw
```

---

### 6. Vera — Neutral (The Organizer / Experienced Mentor)
```text
Waist-up character portrait sprite of an elegant, poised mature woman named Vera, standing with regal dynamic 3/4 angled body posture and one shoulder closer to the camera in a graceful dropped-shoulder stance (asymmetric, composed, and lively, not stiff or squared-on). Her head is turned at a natural 3/4 angle in harmony with her body, while her eyes look warmly and perceptively directly into the camera / viewer, maintaining direct eye contact with the player. Sophisticated swept-back hair sculpted into an elegant updo as a single continuous solid gold sculptural mass with smooth closed contours, zero dangling wisps or loose strands. Wearing an architectural wrap dress with an embroidered textured shawl draped gracefully over her shoulders, pinned with a prominent gear/handshake geometric brooch, her hands resting gracefully in front holding the edge of the shawl at waist level, comfortably contained within the canvas with generous margins. The entire figure, hair, textured shawl, brooch, wrap dress, and hands are made of solid monolithic polished reflective 24-karat yellow gold metal, matching the molten metallic gold material of the reference image, with gleaming specular highlights and rich amber shadow occlusions. Studio rim lighting. Framed waist-up with generous margins. Uniform solid pitch-black background (#000000), no floor, clean silhouette edges. --ar 2:3 --v 6.1 --style raw
```
