---
status: approved
tags: [assets, art, backgrounds, pipeline]
updated: 2026-11-04
---

# Background Generation Guide — Tea & Coffee Capillary Watercolor on Macro Canvas (Pass 3A)

> **Machine-Readable Companion**: [`vault/06 Assets/background_style_spec.json`](background_style_spec.json)  
> **Post-Processing Pipeline Script**: [`scripts/apply_canvas_style.py`](../../scripts/apply_canvas_style.py)  
> **Reference Plates**: [`vault/06 Assets/style_references/`](style_references/)

---

## 1. Visual Direction & Core Philosophy

Our backgrounds use a **high-key, low-contrast analog canvas aesthetic** designed so character sprites, dialogue, and UI pop effortlessly while the environment feels tactile, warm, and handmade across both mobile phone screens and 1080p desktop monitors:

1. **Warm Ivory Macro-Weave Canvas (`#F4EEE1` average)**:
   - Sits **50/50** between bright warm-white cotton (`#FAF8F3`) and unbleached raw linen (`#EEE4CF`).
   - Features a **bold, chunky warp-and-weft fabric grain** large enough to be immediately legible on a small phone screen while crisp at `1920×1080` on desktop.
2. **Low-Contrast Wet-on-Wet Coffee & Tea Stains**:
   - Environments are rendered as delicate, translucent washes of **chamomile tea, Earl Grey tea, and diluted espresso/coffee rings**.
   - Forms emerge organically from **capillary bleeding, water backruns, feathered blooms, and pooled tide marks** soaking into the fabric.
3. **Strictly Zero Linework**:
   - **No pen, pencil, ink outlines, or wireframe polygons.**
   - Architectural edges, tech/crypto motifs, screens, and lighting are suggested **exclusively through wash density and untouched negative-space cutouts** rather than literal drawn lines.

---

## 2. Key Learnings from Iteration (Why We Use a 2-Stage Pipeline)

| Pass | What We Tried | What We Learned |
|------|---------------|-----------------|
| **Pass 1** (`pass1_macro_canvas_source.jpg`) | Prompted for coarse raw linen canvas + tea/coffee washes + sepia draftsmanship. | Great chunky macro canvas weave (very legible on phone), **but** the sepia ink linework and wireframe nodes felt too literal/forced, and the raw linen ground was slightly too dark. |
| **Pass 2A** (`pass2a_capillary_wash_reference.jpg`) | Enforced **strictly zero linework**, brighter white cotton ground, and pure capillary washes + negative-space diamond blooms. | Nailed the soft, low-contrast abstract tea/coffee wash and organic capillary branching, **but** prompting the AI for a brighter white ground caused the generator to smooth out the macro canvas weave. |
| **Pass 3A — Approved** (`pass3a_approved_composite.jpg`) | **Two-Stage Pipeline**: Generate the pure zero-linework capillary wash on a clean white ground (Pass 2A style), then run `scripts/apply_canvas_style.py` to apply the clean standalone canvas texture (`create-flat-evenly-lit-ada66b.png`) at `tone_mix=0.50`, `weave_strength=0.75`, `valley_boost=0.35` and Lanczos-upscale to `1920×1080`. | Combines Pass 2A's soft, linework-free washes with the newly selected clean ivory canvas texture and **keeps the canvas grain scale and ground tone consistent across backgrounds**. |

---

## 3. Stage 1 — Prompting Formula for New Backgrounds

### Master Prompt Template

```text
A wide 16:9 visual novel background illustration of {SCENE_SUBJECT}, created entirely from delicate, ethereal tea and coffee watercolor washes on a clean bright-white ground. Absolutely zero linework, no pen, no pencil, no wireframe polygon outlines, no drawn contours. {STRUCTURAL_WASH_BEHAVIOR}. {NEGATIVE_SPACE_MOTIFS}. Very low contrast, pale chamomile amber and soft Earl Grey sepia washes, highly luminous and airy, fine-art analog stain painting, with capillary bleeding, water backruns, feathered blooms, and pooled tide marks. Pure artwork with no text. Leave canvas weave and final ground tone to the Stage 2 composite.
```

### How to Translate Different Scene Types (Zero-Linework Rules)

When writing `{SCENE_SUBJECT}`, `{STRUCTURAL_WASH_BEHAVIOR}`, and `{NEGATIVE_SPACE_MOTIFS}` after the narrative rewrite, never ask for drawn objects—describe **how water, tea, and negative space suggest the space**:

1. **Interior Spaces (Co-working studios, apartments, conference halls)**
   - *Structural Wash Behavior*: `"Walls, tables, ceiling beams, and room depth emerge softly from layered horizontal and vertical wet-on-wet Earl Grey and diluted espresso washes with feathered tide edges and capillary wicking."`
   - *Negative-Space Motifs*: `"Sunlight through paned windows, laptop screens, and desk lamps are left as untouched bright warm-white canvas negative-space shapes with soft water-bloom halos pushing pigment outward."`
2. **Exterior / Urban / Rooftop Scenes**
   - *Structural Wash Behavior*: `"Distant skyline silhouettes, rooftop planters, and architectural ledges form through overlapping translucent washes of chamomile tea, raw umber, and pale coffee-stain rings soaking into the weave."`
   - *Negative-Space Motifs*: `"Open dawn sky, horizon glow, and distant city lights appear as expansive unpainted off-white canvas negative space and delicate water-drop backruns."`
3. **Symbolic / Network / Blockchain / Governance Spaces**
   - *Structural Wash Behavior*: `"Core pathways and branching structures feature delicate capillary bleeding and water channels that naturally evoke organic circuit traces soaking into the fabric weave."`
   - *Negative-Space Motifs*: `"Floating geometric crystal nodes, token constellations, or dashboard clusters are rendered strictly as soft negative-space diamond and polygon light pockets emerging from watercolor blooms—zero wireframe outlines."`
4. **Close-Up / Interface Set Pieces (Signing screens, terminals, chat logs)**
   - *Structural Wash Behavior*: `"Foreground focal panels are suggested by overlapping rectangular tea washes and pooled coffee-ring edges without hard drawn borders."`
   - *Negative-Space Motifs*: `"Message rows, hex blocks, or confirmation prompts appear as clean negative-space light strips and glowing water-drop cutouts suspended inside a pale amber wash."`

### Mandatory Do's & Don'ts Checklist

- **DO** repeat `"Absolutely zero linework, no pen, no pencil, no wireframe polygon outlines"` in every prompt—image models naturally default to ink outlines on architecture and tech motifs unless explicitly forbidden.
- **DO** inspect the Stage-1 image before post-processing: if the model sneaks in hard wireframe lines or placeholder text, re-roll or pass the image back with `"remove all drawn lines/text, render strictly as soft negative-space water blooms"`.
- **DON'T** prompt Stage 1 for canvas weave or a finished linen texture. Keep its ground bright and clean so the washes remain clean; Stage 2 (`scripts/apply_canvas_style.py`) supplies the exact warm-ivory tone and macro weave relief from the shared reference.

---

## 4. Stage 2 — Automated Macro-Canvas Composite & 1080p Upscale

Once you have an approved Stage-1 wash image (typically generated at `1376×768` 16:9), run [`scripts/apply_canvas_style.py`](../../scripts/apply_canvas_style.py) to apply the Pass 3A canvas weave and output the final `1920×1080` PNG32:

```bash
/opt/homebrew/bin/python3 scripts/apply_canvas_style.py \
  path/to/stage1_wash.jpg \
  "game/images/bg scene_name.png"
```

### What `scripts/apply_canvas_style.py` Does Under the Hood
1. **Standalone Weave Ground**: Applies the selected clean texture-only [`create-flat-evenly-lit-ada66b.png`](style_references/create-flat-evenly-lit-ada66b.png). The older Pass 1 tree image remains a historical source/reference; it is no longer the active texture input.
2. **50/50 Ground Tone Calibration (`tone_mix = 0.50`)**: Mixes pure warm-white (`rgb(250, 248, 243)`) 50/50 with the standalone texture's linen mean for a consistent warm-ivory ground (`~#F4EEE1`).
3. **Macro Thread Relief (`weave_strength = 0.75`)**: Applies 75% of the standalone texture's warp/weft thread relief across the entire frame.
4. **Capillary Valley Absorption (`valley_boost = 0.35`)**: Deepens pigment absorption by 35% inside the thread valleys (`dg < 0`) proportional to stain density, making the tea/coffee wash sit physically inside the woven fabric.
5. **1080p Desktop Upscale**: Resamples to `1920×1080` with `Lanczos` filtering and a subtle thread-detail unsharp mask (`0x0.75+0.45+0.008`), outputting a lossless 32-bit RGBA PNG.
