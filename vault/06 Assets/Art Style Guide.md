---
status: draft
tags: [assets, art]
---

> **Current Background Direction (Approved 2026-11-04 — Pass 3A Tea/Coffee Watercolor on Macro Canvas)**:
> - **Human-Readable Guide**: [[Background Generation Guide]] (`vault/06 Assets/Background Generation Guide.md`)
> - **Machine-Readable Spec**: `vault/06 Assets/background_style_spec.json`
> - **Automated Post-Processor**: `scripts/apply_canvas_style.py`
> - **Reference Plates**: `vault/06 Assets/style_references/`
>
> *(The PC-98 notes below are preserved from the earlier prototype phase.)*

# Art Style Guide — PC-98

The look is NEC PC-98 era Japanese PC games: 16-color palette, ordered dithering for gradients, sharp 1px pixel edges, CRT scanline overlay, anime-style portraits with dramatic 90s shading.

## Canonical palette (from dao25's styles.css — the strictest of the three prototypes)

| Name | Hex | Use |
|------|-----|-----|
| black | `#000000` | backgrounds, outlines |
| deep blue | `#000080` | night scenes, UI base |
| blue | `#0000AA` | UI frames |
| cyan | `#00AAAA` | Spectre, tech UI |
| bright cyan | `#55FFFF` | Maya, highlights |
| magenta | `#AA00AA` | Vera, shadows on pink |
| bright magenta | `#FF55FF` | Jordan, accents |
| pink | `#FF55AA` | warm accents |
| orange | `#FFAA55` | Alex, skin tones |
| brown | `#AA5500` | skin shadow, wood |
| yellow | `#FFFF55` | Atlas, treasury/gold |
| red | `#FF5555` | alerts, Burnout |
| green | `#55FF55` | success, Security |
| gray | `#AAAAAA` | body text |
| dark gray | `#555555` | disabled, dither mix |
| white | `#FFFFFF` | names, emphasis |

Ending accents: gold `#FFD700` (golden ending), blood `#AA0000` (takeover).

## Rules

1. **Never exceed the 16 colors** in final art. Gradients = ordered (Bayer) dithering between palette neighbors.
2. Character portraits: 2/3-body, ~500×800 at 1920×1080 stage; left/center/right slots; each character owns one palette accent (see character notes' `color:` frontmatter).
3. Backgrounds: flat perspective, detail via dithered texture, 1920×1080.
4. UI: 2px pixel borders, cream text boxes on deep blue, blinking ▼ advance cursor.
5. Scanline overlay at ~15% opacity, toggleable in prefs.
6. Typography: Press Start 2P (or similar pixel font) for headers, a readable pixel font for body.

## Generation pipeline (future)

Prototypes assumed Retrodiffusion API for pixel portraits — evaluate that vs. hand-pixel vs. SD + palette-quantize post-process. Whatever generates must end in **exact palette quantization + manual dither cleanup**. Placeholders (current): scripted PIL output, see [[Asset List]].
