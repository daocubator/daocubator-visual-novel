---
status: draft
tags: [assets]
---

# Asset List

**Finding from prototype rip:** the three web prototypes contain **zero bitmap assets** — everything was CSS/emoji, with pixel art *specified* (Retrodiffusion prompts in code) but never generated. So there was nothing to extract except palettes, prompts, and layouts (captured in [[Art Style Guide]] and [[Prototype Archaeology]]). Everything below must be generated.

Status legend: ⬜ needed · 🟨 placeholder generated (scripted PIL, in `game/images/`) · ✅ final

## Character sprites (per [[Art Style Guide]] §2)

| Character | Expressions | Status |
|-----------|-------------|--------|
| Maya | neutral, focused, tired, proud, alarmed | 🎨 neutral live (standing in for 5 expressions) |
| Jordan | neutral, hyped, hurt, determined, exhausted | 🎨 neutral live (standing in for 5 expressions) |
| Alex | neutral, smirk, calculating, defensive, sincere | 🎨 neutral live (standing in for 5 expressions) |
| Vera | neutral, wry, stern, warm | 🎨 neutral live (standing in for 4 expressions) |
| Spectre | hooded-neutral, typing-glow, alert, almost-vulnerable | 🎨 neutral live (standing in for 4 expressions) |
| Atlas | neutral, generous, guarded, predatory-calm | 🎨 neutral live (standing in for 4 expressions) |

= 28 final sprite images (6 bases × expressions).

## Backgrounds (1920×1080)

| BG | Used in | Status |
|----|---------|--------|
| coworking space | Ch1 | 🎨 mixed media (v1 generated) |
| discord server (stylized) | Ch1–5 | 🎨 mixed media (v1 generated) |
| conference hall | Ch2, Ch5 | 🎨 mixed media (v1 generated) |
| late-night apartment | Ch3, Ch5 | 🎨 mixed media (v1 generated) |
| blockchain abstract (nodes, cyan/magenta) | TGE, Ch4 | 🎨 mixed media (v1 generated) |
| rooftop (dawn) | Ch5 endings | 🎨 mixed media (v1 generated) |
| wallet/signing UI close-up | Ch4a set piece | 🎨 mixed media (v1 generated) |
| faction map / governance dashboard | Ch3.8 | 🎨 mixed media (v1 generated) |

## UI / GUI

- Title screen key visual (Tree of life × token geometry × cherry blossoms) 🎨 mixed media (v1 generated)
- Textbox, namebox, choice buttons, frame (Asya mixed-media gold leaf & dark glass skin) 🎨 mixed media live in `game/gui/`
- Lesson Learned popup frame · Codex / Glossary screens · Stats HUD banner 🎨 gold-trimmed dark glass live
- Sliders, scrollbars, checkboxes, radio buttons, slot cards, window icon 🎨 complete in `game/gui/`
- Ending cards ×8 ⬜

## Audio (all ⬜, v1 ships silent or with CC0 chiptune)

- Music: title, daily-life loop, tension loop, attack stinger, elegiac ending, hopeful ending, "Late Night Multisig" (Jordan's 3 a.m. scenes — name mandatory, from daoromance)
- SFX: text blip, choice confirm, lesson popup chime, alert klaxon, coin, heartbeat (burnout)

## CG / special illustrations (v2 wishlist)

Launch night crowd · the signing-screen hex diff · faction map splash · per-ending card art
