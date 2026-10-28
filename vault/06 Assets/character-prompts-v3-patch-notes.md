# Character Prompts v2.3 Patch Notes
2026-10-24. File: character_prompts_v2.json, version bumped 2.2 to 2.3, JSON validated.

## What changed

One rule for the whole patch: one face sentence added per character, right after the eyes and expression line, nothing else moved. Spectre intentionally unchanged.

### Jordan: Variant B locked, gender neutral
Pronouns stay they and their, zero his, zero her in the checked prompt.
New sentence: Androgynous face, neither masculine nor feminine, round full face, width close to length, full cheeks, soft jaw curve, medium width chin, straight medium eyebrows, round open eyes, wide friendly mouth, lips not emphasized, no long eyelashes, neck of medium thickness, shoulders broader than their hips.
This is the direct counter to the v2.2 result: soft jaw and round face are kept, because those were already Jordan, but lip emphasis, lash emphasis, and slender neck and shoulders are explicitly countered, and gender is named as androgynous instead of left blank for the model to fill.
Hair sentence from v2.2 is untouched. Tree emblem, hand pair, and hoodie are untouched.
Gender split stays 2 male, 2 female, 2 unspecified.

### Alex: long narrow rectangle
New sentence: Long narrow rectangular face, forehead and jaw about the same width, high sharp cheekbones, narrow pointed chin, slim straight nose, narrow eyes.
Pronouns unchanged: his only.

### Maya: heart shaped
New sentence: Heart shaped face, wide forehead tapering to a pointed chin, high sharp cheekbones, narrow jaw.
Pronouns unchanged: her only.

### Atlas: square broad
New sentence: Square broad face, jaw as wide as his forehead, broad flat chin, heavy brow ridge, deep set eyes, broad nose, thick neck, senior lines around his eyes and mouth.
Pronouns unchanged: his only. Beard wedge sentence from v2 remains.

### Vera: long oval
New sentence: Long oval face, longer than wide with soft curves, soft rounded chin.
This sits alongside her existing sculpted cheekbones and laugh lines, which were already in the prompt and were not duplicated.
Pronouns unchanged: her only.

### Spectre: no change, on purpose
No face sentence added. Face type remains: deep black void inside the cowl, zero facial features visible. Giving Spectre a face outline would remove the cast's strongest contrast.

## Verification run
JSON validated with python json.tool.
Face phrase present for Alex, Maya, Atlas, Jordan, Vera: yes for all five.
Jordan pronoun check: his 0, her 0, their 6.
Spectre pronoun check: his 0, her 0, their 0.
No em dashes in any prompt.
Word counts after patch: Alex 320, Maya 331, Atlas 365, Vera 323, Spectre 280, Jordan 415. Jordan is the longest, which is a known risk from the v2 rewrite, but the new face sentence sits early, right after expression and before hair, so it carries more weight than a late detail would.
