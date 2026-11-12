---
status: draft
tags: [assets, art, prompts, review]
created: 2026-11-11
---

# 2026-11 Visual Asset Regeneration — Prompt Review

**Purpose:** Review the asset scope and prompt direction before spending on image generation. No images have been generated from this plan.

## What already exists

- `Asset List.md` and `background_prompts.json` inventory **13 episodic backgrounds**. The same 13 background files and **8 episode CGs** (four good/bad pairs, plus thumbnail variants) are present in both `vault/06 Assets/generated_backgrounds/` and `game/images/`.
- The existing background prompts are from the older saturated mixed-media direction. They should be treated as source material for the scene subjects, not as approved style prompts for this pass.
- `Background Generation Guide.md`, `background_style_spec.json`, `scripts/apply_canvas_style.py`, and `style_references/pass3a_approved_composite.jpg` document the approved two-stage process: generate a light, line-free tea/coffee wash, then apply the standalone macro canvas weave and upscale to 1920×1080.
- The selected texture-only ground is `style_references/create-flat-evenly-lit-ada66b.png`; `scripts/apply_canvas_style.py` now uses it as the shared canvas source. The earlier code-quilted texture is an unused experiment.
- Three new character sheets were added on 2026-11-11. The mapping is **Ash El → Koraba**, **Xochtl → Xochit**, **Lay-Lay → Clara**. Story-facing names and the character profile filenames have been updated; the Ren'Py sprite tags and image filenames remain legacy implementation names for now. Generated visual assets have not been changed.

## Proposed scope

| Set | Count | First pass | Output target |
|---|---:|---|---|
| Episodic backgrounds | 13 | Regenerate all current named backgrounds in the approved Pass 3A style | 16:9; Stage 1 around 1376×768, then composite/upscale to 1920×1080 |
| Core character sprites | 3 | One neutral standing pose per character | Transparent 560×880 PNG, matching current sprite proportions |
| Episode CG illustrations | 8 | Four disaster / resolution pairs | Full bleed 16:9, 1920×1080; composed for the scenario selector and in-game scene |

The existing CG slot names (`cg_ep1_disaster`, `cg_ep1_happy`, etc.) can stay stable while their imagery is replaced. Existing thumbnail slots should be made by crops from the final full-art image, not separately prompted, to preserve visual continuity.

## Shared style direction

### Backgrounds

Use the Pass 3A style as written in `Background Generation Guide.md`: clean bright-white ground, low-contrast pale chamomile / Earl Grey / diluted coffee washes, capillary blooms and tide marks, forms implied through wash density and untouched negative space. **Absolutely no drawn linework, outlines, wireframes, UI text, labels, or watermarks.** Do not ask the image model to simulate the linen texture; `apply_canvas_style.py` supplies the exact shared weave and ground tone after the wash image is reviewed.

Base prompt:

> A wide 16:9 visual novel background illustration of **{scene subject}**, created entirely from delicate, ethereal wet-on-wet tea and coffee watercolor washes on a clean bright-white ground. Absolutely zero linework: no pen, pencil, ink outlines, wireframe polygons, or drawn contours. **{structural wash behavior}**. **{negative-space light and focal motifs}**. Very low contrast, pale chamomile amber, soft Earl Grey sepia, and diluted coffee, highly luminous and airy, with capillary bleeding, water backruns, feathered blooms, and subtle coffee-ring tide marks. Pure background artwork, no text, labels, interface elements, or watermark. Leave canvas weave and final ground tone to the Stage 2 composite.

### Character sprites

Use the matching new character sheet as the image reference. Preserve the sheet's hand-etched black/umber contours, fine hatch and stipple, antique ivory/ochre paper feel, distinct face and silhouette, textile/accessory details, and restrained palette. Render a **single full-body neutral standing character**, front-facing with a relaxed balanced posture, arms and signature object clearly readable, feet included, isolated on transparent background. Keep the outline clean for sprite compositing; no sheet layout, lettering, extra props, scenery, dramatic pose, or expression beyond calm neutral.

- **Koraba** — use `Koraba_ The Bridge Keeper Dossier.png`: musician/healer/bridge keeper; dark locs, layered blue/ochre wrap, beads, string instrument (kora), grounded ceremonial presence. Avoid turning the halo motifs from the sheet into literal floating props.
- **Xochit** — use `Xochit_ Ceremonial Weaver Character Sheet.png`: ceremonial weaver/messenger; long dark braids, geometric beaded headband and statement earrings, red/black face paint, richly patterned textile layers, ceremonial cacao bowl. Preserve the face paint and textile motifs as identity anchors.
- **Clara** — use `Clara_ The Registrar Character Sheet.png`: registrar/administrator; blonde hair in a structured bun, tailored patterned office clothes, lanyard, clipboard or ledger; composed, organized bearing. Preserve the orbit/ring and star motif as subtle graphic design language, not floating UI.

### Full-art CGs

Combine the material treatment of the approved background (washed tea/coffee watercolor visibly absorbed into coarse ivory canvas) with the character sheets' expressive etched/crosshatched figures, readable faces, and recognizable outfits. Compared with a quiet background, CGs may use deeper umber, charcoal, crimson, blue, and gold accents for thumbnail impact. Use a decisive manga/anime/visual-novel panel composition, clear foreground-midground depth, dramatic gesture and eye-lines, and one instantly legible conflict or triumph. Fill the frame edge-to-edge. Place faces, hands, and the key action in the **upper two-thirds**; keep the bottom third lower-detail and lighter so dialogue can remain legible over the image. No typography, captions, logos, or fake interface text. Avoid tiny detail that disappears at thumbnail scale.

## Background prompt subjects

Append the corresponding subject and composition notes to the shared background base prompt above. Keep each environment open enough for character sprites unless noted otherwise.

| Output | Subject and scene-specific wash notes |
|---|---|
| `bg apartment.png` | A founder's small apartment at 3 AM: desk, laptop glow, mug, rain-softened city window. Suggest intimate room depth with horizontal/vertical Earl Grey washes; leave the laptop and window glow as pale negative space. Quiet and tired, not ominous-black. |
| `bg apothecary.png` | A working herbal apothecary: shelves of bottles, dried herbs, mortar, ledger and a clear signing desk. Use vertical amber/sepia shelf washes, soft bottle-shaped light pockets, open foreground for characters. |
| `bg blockchain.png` | An abstract chain / treasury space: branching pathways and connected blocks suggested by capillary channels and stain blooms; leave several diamond node-shaped light pockets. No literal code or wireframe. |
| `bg cacao_circle.png` | A Lisbon gathering table prepared for cacao: cups, woven cloth, candles and a small presentation space. Rounded pooled tea rings suggest cups; warm light remains unpainted; leave character space around the table. |
| `bg conference.png` | A public conference hall and pitch stage: distant seats, broad screen-shaped light pocket, stage wash and open speaker area. Warmly formal, with low-contrast audience silhouettes only as soft washes. |
| `bg constellation.png` | A world overview: expansive branching tree/root network with softly suggested star/node blooms, following the approved reference's organic stain behavior. Keep the center clear enough for overlaid map nodes. |
| `bg coworking.png` | A shared creative studio with long worktable, laptops, chairs, plants and window light. Use broad pale room-depth washes; keep the central foreground open for three sprites. |
| `bg discord.png` | A digital community space at night suggested abstractly through stacked message-like pale rectangles, clustered avatar-like circles and a channel rail, all as soft negative-space forms within faint cool sepia/grey washes. No legible text, logos, or hard UI borders. |
| `bg factionmap.png` | A governance map with three loosely connected communities, voting clusters and branching delegation flows. Suggest circles and flows with wash blooms and pale cutouts, not drawn diagrams or text. Keep the center quiet enough for recap UI. |
| `bg rooftop.png` | A rooftop terrace at dawn: low city skyline, planters, rail and wide glowing horizon. Warm chamomile/amber blooms surround an open pale sky; keep standing space at the bottom. |
| `bg sanctuary.png` | A sunlit community sanctuary studio with herbs, instruments, woven rug and wood beams. Filtered daylight as negative space, gentle ochre and tea stains, enough open floor for a three-person group. |
| `bg signing.png` | A close-up signing set piece: hardware wallet beside a laptop, with two contrasting transaction-summary and raw-data areas implied as soft rectangular light pockets. No readable digits, buttons, text, or hard borders; focal devices emerge from pooled washes. |
| `bg treasury_fire.png` | A disaster transition background: fractured ledger-like wash planes, scattered ember blooms and a failing treasury suggested by a darkening center, while retaining the same light ivory canvas and overall low contrast. Keep the lower dialogue area pale and quiet. |

## Character neutral prompt review

Use one common sprite prompt from the style direction, swapping in each character's sheet and description. Proposed prompt endings: **Koraba** “neutral expression, calm attentive eyes, hands resting naturally near the kora”; **Xochit** “neutral expression, warm steady gaze, holding the cacao bowl securely at waist height”; **Clara** “neutral expression, composed gaze, holding a closed ledger against her side and clipboard in the other hand.”

If the image tool cannot make a clean transparent background with the reference image, generate on flat warm white and remove the background locally after selection. Do not generate expression variants in this pass.

## Eight CG prompt concepts

Use the shared full-art CG direction above and one scene-specific paragraph per illustration. Character references: Koraba dossier, Xochit sheet, and Clara sheet. All names below reflect the proposed story rename.

1. **Episode 1 disaster — “The $60,000 transfer is gone.”** At a rain-streaked Lisbon airport after midnight, Koraba stands stunned beside sealed crates of herbal elixirs, one hand gripping his instrument strap and the other holding a phone with a blank pale screen; Xochit faces him in alarm and grief; Clara stands apart clutching the ledger and key, unable to undo the transfer. Angle the airport glass and crate stack toward the characters; convey betrayal, helplessness, and the empty treasury without readable text.
2. **Episode 1 good outcome — “The test transfer lands.”** At the same airport, the three gather around a small phone showing one calm confirmation-shaped light; Koraba and Xochit exchange relieved eye contact while Clara offers the shared key forward. Let the crates and departure lights recede behind them; show shared custody and relief as a team achievement, not a solo victory.
3. **Episode 2 disaster — “The showcase freezes.”** Backstage minutes before the Lisbon doors open, exhausted Koraba reaches toward the stage computer to pull his finished game while Clara blocks the payment with a ledger; Xochit steps decisively between them with an open hand. Bright empty stage lights loom above, creating urgency and a sharp triangle of conflicting eye-lines.
4. **Episode 2 good outcome — “The work speaks for itself.”** In the warm spill of the saved Lisbon stage, Koraba's game is running and the crew is ready; Xochit reveals the neutral submission that exposes the bias, while Clara lowers the ledger and recognizes the harm. Frame the three in one linked gesture of accountability and solidarity, with celebratory stage light behind them and no readable screen content.
5. **Episode 3 disaster — “The handshake split collapses.”** At a cacao ceremony table, a court summons lands across the cloth as a former founder's token sell-off is suggested by a cascade of falling token-like discs; Koraba and Xochit reach toward the papers and spilled cacao, Clara watches the consequences close in. Make the collision of sacred gathering and cold legal/financial shock the visual hook; no legible legal text.
6. **Episode 3 good outcome — “The agreement holds.”** Koraba and Xochit sign a clear, formal co-op agreement beside the cacao bowl while a patient reserve jar and shared ledger sit within reach; Clara stands with them as accountable administrator. Use paper folds and interwoven textile shapes to suggest durable commitments, with dawn-like light and an assured three-person composition.
7. **Episode 4 disaster — “One tired click drains the apothecary.”** In Clara's candlelit apothecary at 1:14 AM, her finger hovers over a misleading signing control on a pale screen as a dark stain-like current pulls tokens from an open treasury vessel; Koraba and Xochit pound urgently at the door behind her. Show her fatigue and the irreversible instant in her face and hand; avoid readable UI or text.
8. **Episode 4 good outcome — “The hex is caught in time.”** Clara turns the hardware wallet toward Koraba and Xochit; all three verify the transaction together as a malicious dark wash is stopped at a clear boundary. A timelock/guardian motif can appear as a ring of pale light around the shared treasury vessel. Convey alert teamwork and earned relief, with the threat still visible but contained.

## Open review points before generation

- Confirm whether all 13 existing backgrounds should be regenerated in this pass, including the symbolic map and the one-off signing set piece. The current inventory suggests yes.
- Confirm whether CGs should use **Koraba / Xochit / Clara** naming and visual designs exclusively, or whether returning ensemble characters (for example Vera, Spectre, or Atlas) should appear in any of the eight CGs. The scene drafts currently focus on the three new core designs.
- Approve or revise the eight scene moments and emotional framing. After approval, expand any scene into final generation-ready prompts and generate only the selected assets.

