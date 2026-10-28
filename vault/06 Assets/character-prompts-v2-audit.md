# Get Rich Together: Character Prompts v2 Audit
All six prompts from character_prompts.json v1.0, plus the Jordan result image. 2026-10-23.

## Verdict

Yes, redo all of them, but do not redo them all in the same way.
The v1 prompts share one very strong template and that is the problem. Every character has the same body instructions, the same hand zone, and the same gold finish. The template gives consistency, then erases identity.

Keep the template for: material, black background, 2:3 waist up framing, direct eye contact, clean hair mass, rim lighting.
Replace, per character, these 6 variables: shape language, hair volume family, torso geometry, hand pair and hand heights, signature prop position, neutral expression and finish blocking.

## Jordan result review: keep or adjust?

Good, and closer than Maya Iteration 3 was at the same stage. Ship the direction, adjust the prompt, do not restart him.

What worked, better than expected:
1. Hair silhouette lands. The cloud is big, round, and instantly readable. It is his logo now.
2. The raised hand fixed the pocket problem. Even though the model turned the other hand into a thumb hook outside the pocket instead of a hand inside it, that compromise is better than the prompt. Keep it and prompt it on purpose next time.
3. The chest emblem is a discovery. You asked for subtle DAO and circuit emblems and got a large circular tree emblem with roots and two small figures under the branches. That is stronger than a DAO logo, it matches the circuit board tree motif from the DAOcubator style guide, and it reads at sprite size. Lock it as his signature emblem.
4. Smile, head tilt, and hood crescent all read. He feels welcoming.

What to adjust in his prompt:
1. Hand gesture: the raised hand is too high, fingers too splayed and stiff, palm turned sideways. It reads as waving hello, not beckoning. Lower it to chest to shoulder height, palm facing viewer, fingers together and slightly curved, wrist straight and relaxed.
2. Smile: warm is right, visible teeth in gold reads a little uncanny and the chin stretches long. Ask for a warm closed mouth smile, lifted cheeks, no visible teeth.
3. Hair detail: the outer silhouette is great, the interior is busy with pierced loops and black holes that compete with the circuit detail. Ask for fewer, larger, smoother curl masses with shallow grooves, no holes through the hair.
4. Style drift: this result is more 2D illustrated than Maya, who is a 3D sculptural render. If the cast must match, add explicit render language: photorealistic 3D sculpture render, solid cast metal with real depth, not 2D illustration, not painting, not anime.
5. Kangaroo pocket: the big symmetrical pocket rectangle dominates the bottom third. Tilt it with the torso twist and shrink it slightly, so the diagonal of his body survives to the bottom edge.
6. Finish blocking did not really happen: he is bright polished everywhere. Keep the illustration shading if you like it, but if you rerun, restate the three tone blocking inside the prompt itself. Satin hoodie, mirror face and raised hand and emblem, dark antique in curl grooves and folds.

## Cast wide collision map, v1

Hands: this is the biggest problem in the whole file.
Alex holds a phone with both hands at waist level. Maya holds a laptop at her hip with one arm down. Jordan has both hands in pockets at waist level. Atlas has one hand across his midsection. Spectre has both gloved hands quietly at waist level. Vera holds her shawl with both hands in front at waist level.
Six characters, six low central hand placements. That one habit makes every sprite share the same lower silhouette.

Hair: four characters are in the swept back family.
Alex slicked back, Atlas swept back, Vera swept back updo, Maya swept behind the ear into a low bun. At gold sprite size, swept back is swept back, no matter what the prompt calls it. Fix by volume and position, not by naming: Alex low and flat and angular, Atlas tall crest, Vera tall fan, Maya low offset coil, Jordan huge round cloud, Spectre no hair at all, just cowl.

Expressions: three characters are described as calm and calculating or calm and confident.
Alex calm calculating composed, Maya sharp calm confident, Atlas calm calculating formidable. Same face, three names. Give each neutral a different mouth and brow: Alex one corner smirk, Maya level assessing brow, Atlas heavy brow and firm mouth looking down, Jordan open welcome, Vera knowing raised brow, Spectre no face.

Finish: every character is polished reflective gold everywhere.
That flattens suits, hoodies, hair, and faces into the same highlight range. Each v2 prompt now assigns mirror, satin, and dark antique zones.

Frame scale: every character gets generous margins and the same size in frame.
Use scale as character: Atlas largest and widest, Spectre hunched and hooded, Jordan hair makes him tall, Vera tall and narrow, Alex and Maya medium and neat. Same height lineup, different widths and heights inside it.

## Per character v2 assignments

Alex, sharp triangles.
Primary shape: two long peaked lapels like blades framing one bright diagonal tie. Hair: low flat angular wedge with a sharp side part and one diagonal sweep, hugging the skull. Hands: phone raised and tilted at chest height in one hand, other hand at waist adjusting a cufflink. Expression: sly smirk, one corner of mouth only. Phone is no longer a small rectangle held by both hands at his belt.

Maya, angular spiral.
As in the Iteration 4 sheet: oversized offset spiral coil bun, one sided collar fin, laptop rotated to a diagonal shield across the lower torso, both hands on the laptop at different heights and corners. Assessing level expression stays hers alone now.

Jordan, round cloud.
As above: huge round curl cloud, welcoming palm at chest height, thumb hook on pocket, tree emblem locked, closed mouth smile.

Atlas, boxy monument.
Primary shape: trench coat built like armor, massive shoulders, widest character in frame, one huge lapel flipped up on one side. New silhouette tool: a short broad sculpted beard wedge framing the jaw, plus a tall swept crest of hair. One hand high gripping his lapel showing rings, other hand low holding a cane angled diagonally across his body, with a pocket watch chain as a second diagonal. Expression: heavy brow, chin high, looking slightly down at the viewer. He is the only character shot from slightly below.
Note: the beard is the one real identity change in v2. It is in his prompt as a single removable sentence. Delete that sentence if Atlas must stay clean shaven, and lean harder on crest, collar, and cane.

Spectre, hooded triangle.
Already the strongest silhouette in v1, so the lightest touch. Make the cowl oversized with a forward leaning pointed peak and an asymmetric drape over one shoulder. Hunched forward, head lowered. One gloved hand up gripping the cowl edge near the void, the other arm low across the body holding a compact keyboard diagonally under the arm. Cloak is the darkest matte gold in the cast so the void and the gloves separate. Bright rim must trace the whole hood peak so he never merges with the black background.

Vera, elegant curves and one long diagonal.
Hair becomes a tall fan shaped updo rising above her head like a crown fan, not another low swept shape. Shawl becomes one long diagonal sash from high shoulder to opposite hip. One huge round brooch at the high shoulder where the shawl pins, not at her waist. High hand holds the shawl at the brooch, low hand holds a closed ornate fan angled diagonally. Add fine sculpted laugh lines and strong cheekbones so mature actually renders. Expression: knowing closed mouth smile, one eyebrow raised.

## How to roll this out

1. Rerun Jordan first with the v2 adjustments only. He is your proof that small prompt deltas fix a result without losing what worked. Compare side by side with this result before touching anyone else.
2. Then rerun Spectre and Vera, they need the least identity work and will show the fastest silhouette gains.
3. Then Alex and Atlas together, because they are the pair most likely to collide, both suited men with swept hair and calculating faces. Generate them in the same session and line them up at 10 percent size.
4. Maya last, using the Iteration 4 prompt, because hers is already a separate deeper pass.
5. Final gate for the cast: one lineup image, all six at same height, pure black fill version next to it. If you cannot name all six from the black version, that character goes back, no matter how pretty the gold version is.
