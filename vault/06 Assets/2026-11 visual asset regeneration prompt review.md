---
status: draft
tags: [assets, art, prompts, review]
created: 2026-11-11
---

# 2026-11 Visual Asset Regeneration — Prompt Review

**Purpose:** Review the asset scope and prompt direction before spending on image generation. No images have been generated from this plan.

## What already exists

- The previous **13-background prompt list** was inherited from the older chapter-based narrative and mixes legacy settings with a few locations reused by the episodes. The current start flow opens the episode constellation; this regeneration scope covers its hub and four playable episodes. The legacy chapter files remain in the repo but are out of scope.
- The existing background prompts are from the older saturated mixed-media direction. They should be treated as source material for the scene subjects, not as approved style prompts for this pass.
- `Background Generation Guide.md`, `background_style_spec.json`, `scripts/apply_canvas_style.py`, and `style_references/pass3a_approved_composite.jpg` document the approved two-stage process: generate a light, line-free tea/coffee wash, then apply the standalone macro canvas weave and upscale to 1920×1080.
- The selected texture-only ground is `style_references/create-flat-evenly-lit-ada66b.png`; `scripts/apply_canvas_style.py` now uses it as the shared canvas source. The earlier code-quilted texture is an unused experiment.
- Three new character sheets were added on 2026-11-11. The mapping is **Ash El → Koraba**, **Xochtl → Xochit**, **Lay-Lay → Clara**. Story-facing names and the character profile filenames have been updated; the Ren'Py sprite tags and image filenames remain legacy implementation names for now. Generated visual assets have not been changed.

## Proposed scope

| Set | Count | First pass | Output target |
|---|---:|---|---|
| Episode and hub backgrounds | 6 | Regenerate the locations used for hub, episode openings, and ordinary dialogue scenes; outcomes use full-art CGs | 16:9; Stage 1 around 1376×768, then composite/upscale to 1920×1080 |
| Core character sprites | 3 | One neutral standing pose per character | Transparent 560×880 PNG, matching current sprite proportions |
| Follow-up character expressions | 14 | Generate only the non-neutral poses used in the current episode script, per the expression map below | Transparent 560×880 PNGs, matching each neutral character design |
| Episode CG illustrations | 8 | Four disaster / resolution pairs | Full bleed 16:9, 1920×1080; composed for the scenario selector and in-game scene |

The existing CG slot names (`cg_ep1_disaster`, `cg_ep1_happy`, etc.) can stay stable while their imagery is replaced. Existing thumbnail slots should be made by crops from the final full-art image, not separately prompted, to preserve visual continuity.

## Story-beat background and cast cross-check

This table follows the playable scenes in `game/episodes.rpy`. The scenario selector previews the disaster CG, so each episode opens with its location background and character sprites to introduce the cast. Failed choices and successful resolutions switch to the matching full-art CG; the art already contains the characters, so sprites are not layered on top. Ordinary setup and successful decision scenes use the listed background and live sprites.

| Episode | Story beat | Background or CG | Characters on screen |
|---|---|---|---|
| 1 · No Keys, No Cheese | Disaster hook: stranded with the lost transfer at Lisbon Airport | `bg lisbon_airport.png` | Koraba, Xochit, Clara sprites |
| 1 | Rewind and sanctuary setup: leaked keys, shipment preparation | `bg sanctuary.png` | Koraba, Xochit, Clara sprites |
| 1 | Decision 1: leaked-key rotation / custody | Good path: `bg sanctuary.png`; failures: `cg_ep1_disaster.png` | All three on either path |
| 1 | Decision 2: vet the proposed new administrator | Good path: `bg sanctuary.png`; failures: `cg_ep1_disaster.png` | All three on either path |
| 1 | Decision 3: test the Brazil transfer before sending $60,000 | Good path: `bg sanctuary.png`; failures: `cg_ep1_disaster.png` | All three on either path |
| 1 | Resolution: verified funds and cleared crates at the airport | Happy CG: `cg_ep1_happy.png` | Koraba, Xochit, Clara in the art |
| 2 · Frozen Pay, Empty Stage | Disaster hook: payment freeze backstage before the Lisbon Showcase opens | `bg showcase_backstage.png` | Koraba, Xochit, Clara sprites |
| 2 | Rewind and early team setup: preparing the showcase over cacao | `bg cacao_circle.png` | Koraba, Xochit, Clara sprites |
| 2 | Decision 1: objective escrow for the creative work | Good path: `bg cacao_circle.png`; failures: `cg_ep2_disaster.png` | All three on either path |
| 2 | Decision 2: prove bias with the neutral-avatar submission, two days before the event | Good path: `bg showcase_backstage.png`; failures: `cg_ep2_disaster.png` | All three on either path |
| 2 | Decision 3: rotate stewardship and prevent burnout before the event | Good path: `bg showcase_backstage.png`; failures: `cg_ep2_disaster.png` | All three on either path |
| 2 | Resolution: game succeeds and the team celebrates at the showcase | Happy CG: `cg_ep2_happy.png` | Koraba, Xochit, Clara in the art |
| 3 · Blood, Cacao & Paper | Disaster hook: lawsuit and token crash hit the cacao ceremony | `bg cacao_circle.png` | Koraba, Xochit, Clara sprites |
| 3 | Rewind and founding circle: draft the cooperative agreement | `bg cacao_circle.png` | Koraba, Xochit, Clara sprites |
| 3 | Decision 1: written vesting and cliffs | Good path: `bg cacao_circle.png`; failures: `cg_ep3_disaster.png` | All three on either path |
| 3 | Decision 2: register the legal wrapper | Good path: `bg cacao_circle.png`; failures: `cg_ep3_disaster.png` | All three on either path |
| 3 | Decision 3: treasury reserve and creator expense repayment | Good path: `bg cacao_circle.png`; failure: `cg_ep3_disaster.png` | All three on either path |
| 3 | Resolution: agreements protect the cooperative six months later | Happy CG: `cg_ep3_happy.png` | Koraba, Xochit, Clara in the art |
| 4 · One Tired Click Drained the Apothecary | Disaster hook: the treasury is drained inside Clara's apothecary | `bg apothecary.png` | Koraba, Xochit, Clara sprites |
| 4 | Rewind and POV setup: Clara faces the admin workload | `bg apothecary.png` | Koraba, Xochit, Clara sprites |
| 4 | Decision 1: reject the whale's secret control deal | Good path: `bg apothecary.png`; failure: `cg_ep4_disaster.png` | All three on either path |
| 4 | Decision 2: inspect the hardware wallet's raw transaction data | Good path: `bg apothecary.png`; failure: `cg_ep4_disaster.png` | Good path: Clara + Xochit sprites; failure CG: all three |
| 4 | Decision 3: add time-lock and snapshot-voting defenses | Good path: `bg apothecary.png`; failure: `cg_ep4_disaster.png` | All three on either path |
| 4 | Resolution: shared responsibility and safe operations in the apothecary | Happy CG: `cg_ep4_happy.png` | Koraba, Xochit, Clara in the art |

This mapping uses all eight episode CG slots for failed choices and successful resolutions, in addition to their existing use in the constellation selector and completion card. Background generation is now scoped to six assets: the playable hub, sanctuary studio, Lisbon airport, cacao circle, showcase backstage workspace, and apothecary. Dedicated showcase-stage and treasury-fire backgrounds are not needed because the outcome CGs carry those dramatic beats.

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

This list is reconciled against the four playable episodes in `game/episodes.rpy` and the active hub in `game/constellation.rpy`. It excludes old chapter-only locations and scenes carried by full-art CGs. The episode openings use backgrounds and character sprites; each failed choice and successful resolution uses its matching CG.

| Output | Subject and scene-specific wash notes |
|---|---|
| `bg constellation.png` | The playable episode hub: an expansive branching tree/root network with softly suggested star/node blooms, following the approved reference's organic stain behavior. Keep clear central and edge areas for the overlaid episode nodes and UI. |
| `bg sanctuary.png` | Episode 1's community sanctuary studio: herbs, instruments, woven rug, packing crates and wood beams, with filtered daylight and enough open floor for three sprites. This is the rewind location before the Brazil shipment. |
| `bg lisbon_airport.png` | Episode 1's opening hook at Lisbon Airport after midnight: rain-streaked terminal glass, customs barrier and sealed crates of herbal elixirs, with open standing space for the three sprites. Keep the phone and treasury failure to dialogue; no legible background text. |
| `bg cacao_circle.png` | Episodes 2 and 3: a ceremonial cacao gathering table with cups, woven cloth, candles, and space for the team to prepare the Lisbon showcase or discuss written agreements. Rounded pooled tea rings suggest cups; retain an open character area around the table. |
| `bg showcase_backstage.png` | Episode 2's Lisbon venue work area: folding table, laptop, cables, road cases, and a curtain or open doorway with soft stage light beyond. Make it feel like a practical production workspace where the team can inspect Koraba's build and discuss the payment dispute; leave a clear foreground for three sprites, with no readable screens or text. |
| `bg apothecary.png` | Episode 4's working herbal apothecary: shelves of bottles, dried herbs, mortar, ledger and a clear signing desk. Use vertical amber/sepia shelf washes, soft bottle-shaped light pockets, and open foreground for three sprites. |

## Character neutral prompt review

Use one common sprite prompt from the style direction, swapping in each character's sheet and description. Proposed prompt endings: **Koraba** “neutral expression, calm attentive eyes, hands resting naturally near the kora”; **Xochit** “neutral expression, warm steady gaze, holding the cacao bowl securely at waist height”; **Clara** “neutral expression, composed gaze, holding a closed ledger against her side and clipboard in the other hand.”

If the image tool cannot make a clean transparent background with the reference image, generate on flat warm white and remove the background locally after selection. Do not generate expression variants in this pass.

## Character expression generation scope

Audited `show` statements in `game/episodes.rpy` against image definitions in `game/direction.rpy`. The active story calls **17** distinct character poses: the three neutral poses plus **14** non-neutral follow-up poses. These are explicit at the story setup and decision beats. The failure and resolution CG scenes contain their own character art, so they do not call for additional sprite expressions. The code uses legacy image tags (`ashel` = Koraba, `xochtl` = Xochit, `laylay` = Clara); retain those filenames or update the image definitions when replacing the artwork.

| Character | Expression | Used story beats |
|---|---|---|
| **Koraba** (`ashel`) | `neutral` | Episode 1 sanctuary rewind and administrator-vetting scene; Episode 2 showcase planning and escrow decision; Episode 3 founding circle and all agreement decisions; Episode 4 Clara's rewind setup. |
| **Koraba** (`ashel`) | `alarmed` | The disaster hook at the start of each of the four episodes. |
| **Koraba** (`ashel`) | `determined` | Episode 1 key-rotation and test-transfer decisions; Episode 4 flash-loan defense. |
| **Koraba** (`ashel`) | `hurt` | Episode 2, after Clara rejects the final game module and during the bias dispute. |
| **Koraba** (`ashel`) | `proud` | Episode 2, after the neutral-avatar proof and during cooperative restructuring. |
| **Koraba** (`ashel`) | `focused` | Episode 4, evaluating Atlas's offer of voting control. |
| **Xochit** (`xochtl`) | `neutral` | Episode 1 key custody and vetting; Episode 2 bias-proof decision; Episode 4 rewind into Clara's POV. |
| **Xochit** (`xochtl`) | `hurt` | Episode 1 transfer-loss hook; Episode 3 lawsuit/token-crash hook; Episode 4 drained-apothecary hook. |
| **Xochit** (`xochtl`) | `warm` | Episode 1 sanctuary welcome and test transfer; Episode 2 cacao planning and cooperative restructuring; Episode 3 treasury agreement. |
| **Xochit** (`xochtl`) | `focused` | Episode 2 payment/escrow conflict; Episode 3 vesting decision; Episode 4 hardware verification and flash-loan defense. |
| **Xochit** (`xochtl`) | `stern` | Episode 3 legal-wrapper decision; Episode 4 governance-capture decision. |
| **Clara** (`laylay`) | `neutral` | Episode 1 vetting and transfer decisions; Episode 3 founding circle and treasury-safety agreement. |
| **Clara** (`laylay`) | `stern` | Episode 1 airport hook; Episode 2 payment-freeze hook and bias dispute; Episode 4 governance-capture and flash-loan scenes. |
| **Clara** (`laylay`) | `smirk` | Episode 1 sanctuary rewind/key-custody scene; Episode 2 showcase-planning and escrow decision. |
| **Clara** (`laylay`) | `defensive` | Episode 2, after bias is exposed and the group considers shared stewardship. |
| **Clara** (`laylay`) | `alarmed` | Episode 3 lawsuit/token-crash hook and Episode 4 drained-apothecary hook. |
| **Clara** (`laylay`) | `calculating` | Episode 3 legal-wrapper decision; Episode 4 rewind and hardware-wallet verification. |

**Not in the current generation list:** Xochit's `proud` image is defined in code and exists as an older sprite, but no current episode scene calls it. Generate it only if a future scene uses it. All 17 poses currently called by the episode script have matching legacy PNG files in `game/images/`; those are the files the new sheet-based art would replace.

**Code check:** Expression changes are already assigned with `show <legacy-tag> <expression>` statements at the relevant scene and decision beats. The 17 listed calls are wired; no expression-generation work requires story-script edits unless the desired emotion or timing changes.

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

