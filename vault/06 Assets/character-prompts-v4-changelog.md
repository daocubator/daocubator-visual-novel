# Character Prompts v4 Changelog
2026-10-24. New file: character_prompts_v4.json, version 4.0, built from character_prompts_v2.json v2.3. JSON validated.

## The one rule that governs v4

Jordan is unchanged. His v2.3 prompt is copied verbatim into v4, word for word, because it is the locked keeper paired with jordan-keeper-v23.jpg. Every other character was edited for the Jordan learnings, not rewritten from scratch. If a future v4 result for Jordan drifts, compare it against the keeper pair and change one trait at a time, do not touch the rest of his prompt.

## Jordan learnings, applied to the whole cast

1. Hair by outer edge, not mood. Smooth closed contours was removed from every prompt. Each hair family now names its outer edge: Alex sharp diagonal line close to the skull, Maya spiral coil, Jordan bumpy curl edge (unchanged keeper wording), Atlas tall wave crest with a flat point beard wedge, Vera fan arc, Spectre pointed cowl peak instead of hair.
2. Presentation anchored in words. Every character with a face now has jaw, brow, neck, and shoulder language in the prompt itself, not just pronouns. Jordan stays explicitly androgynous, neither masculine nor feminine, so the model does not fill a vacuum again. Spectre gets the opposite explicit anchor: no gendered body cues, no face.
3. Hands split and specified. Every hand pair is at two different heights, doing two different jobs, with side, height, palm direction, and finger shape named where it matters. Atlas cane is now clarified to run diagonally down and outward, not across his chest, which is the exact kind of cross body ambiguity that gave Jordan the tray hand in v2.
4. One focal emblem, with a stop rule. Alex tie only, Maya circuit patches only, Jordan tree emblem only, Atlas watch chain only as a diagonal detail, Spectre sleeve tracings only, Vera brooch only. Each prompt also forbids other badges, patches, or all over print. This is the direct fix for Jordan v2, where one emblem scattered into badges and a full print.
5. Style war language removed. Photorealistic 3D sculpture render, not 2D illustration was deleted from all five non Jordan prompts. It failed on Jordan, because style follows the reference image and the tool, not text. V4 keeps material language, seamless monolithic solid gold, mirror and satin and dark antique finishes, and puts style control in the workflow note instead: use the same reference and settings that produced the keeper for that character.
6. Prompt length trimmed, except the keeper. Word counts: Alex 320 to 293, Maya 331 to 303, Atlas 365 to 356, Spectre 280 to 274, Vera 323 to 301. Jordan stays at 415, because trimming a keeper prompt to save words would be exactly the mistake v2 made.
7. Generation workflow in the file. V4 carries a top level workflow: same reference and settings as the keeper, one trait change at a time, compare silhouette, hair edge, face, hand pair, focal emblem, and framing against the keeper, and if a trait fails on a text only run, rerun the identical prompt with the keeper image as reference before editing words again.

## Per character, what actually changed from v2.3

Alex: hair edge rewritten to a sharp diagonal line, tie named as the only bright focal detail, phone hand finger wrap named, style war language removed, finish language shortened.
Maya: bun edge rewritten to a spiral coil, circuit patches named as the only emblem detail, style war language removed, finish language shortened. Laptop diagonal, collar fin, and heart face are unchanged.
Jordan: nothing. Verbatim v2.3 prompt, verified by string comparison in the build script.
Atlas: crest edge rewritten to a tall wave, beard edge named as a flat point, cane direction clarified to down and outward not across the chest, watch chain named as the only diagonal detail, style war language removed.
Spectre: no gendered body cues and no face added explicitly, cowl grip thumb named, sleeve tracings named as the only emblem detail, style war language removed.
Vera: updo edge rewritten to a fan arc, brooch named as the only emblem with shawl embroidery called texture only, fan grip named by its base, style war language removed.

## Verification run
JSON validated with python json.tool.
Face phrase present for Alex, Maya, Jordan, Atlas, Vera: yes for all five. Spectre void phrase present: yes.
Jordan pronoun check: his 0, her 0, their 6, and Jordan prompt identical to v2.3: yes.
No em dashes in any prompt. No smooth closed contours phrase in any prompt. No not 2D phrase in any prompt.
Gender split unchanged: 2 male (Alex, Atlas), 2 female (Maya, Vera), 2 unspecified (Jordan gender neutral, Spectre anonymous).
Face shapes unchanged from v2.3: Alex long rectangle, Maya heart, Jordan round full, Atlas square monumental, Spectre no face, Vera long oval mature.
