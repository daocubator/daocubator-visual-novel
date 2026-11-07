# DAOCUBATOR / "Get Rich Together" — Visual Novel Overview

*Generated from the Obsidian vault on 2026-11-04 (git b637b35). The vault is the source of truth — comment freely here; edits get folded back into the vault on each design pass. See vault/07 Production/Sync Workflow.md.*

## Premise

**Get Rich Together (DAOCUBATOR)** is an episodic educational visual novel (Ren'Py, minimalist rustic line-art & analog watercolor aesthetic) about why creative collectives and DAOs fail—and how to build sovereign, cooperative ones that thrive.

Instead of a long, slow build-up, the game opens with an interactive **World Overview ("The First Constellation")** displaying the core categories of lessons and a constellation of playable crisis scenarios. Clicking any glowing constellation node reveals an **"OMG Disaster" worst-case scenario**—and lets you dive directly into the tragedy, **rewind time (`⏪`)**, and guide the characters through **~3 critical choices** where every mistake triggers a fast, darkly funny bad ending with an **instant 1-click checkpoint retry** so you learn by doing without losing momentum.

### Core Cast & Real-World Backbone

Grounded in real-world DAO post-mortems and lived experiences from collectives like *Essential Food and Medicine*, the episodic stories follow three core archetypes across shifting perspectives:
- ****Ash El** (The Creator / Protagonist):** Visionary musician and community builder equipped with his instrument, who brings the labor, art, free health juice programs, and sanctuary trips—learning the hard way that *"no keys, no cheese."*
- ****Lay-Lay** (The Administrator / Antagonist):** Operations and treasury manager associated with potions, herbs, and administrative keys—embodying what happens when non-creators gain un-oversighted control of multi-sig wallets or let awe curdle into jealousy.
- ****Xochtl** (The Co-Creator / Shaman):** Ceremonial cacao practitioner and strategic protector equipped with her cacao cup—bridging ancestral reciprocity, co-op solidarity, and clever on-chain verification.

Alongside them appear the wider ecosystem cast (****Maya****, ****Jordan****, ****Alex****, ****Vera****, ****Spectre****, and ****Atlas****).

### Core Educational Pillars

1. **Keys & Sovereignty (Crypto Basis & OpSec):**
   - Never giving up your agency or keys to an administrator (**No Keys No Cheese**).
   - Rotating keys on-chain (NEAR-native account key rotation & multi-sig rotation) immediately after a plaintext leak (**Credential Hygiene**).
   - Properly vetting incoming DAO administrators before voting them in (**Vetting DAO Administrators**).
   - Always sending a **$1 test transaction** and confirming receipt before wiring bulk funds like $60,000 (**The One Dollar Test Transaction**, **Verify the Hex**).
2. **Collaboration & Co-op = Winning Together:**
   - Preventing administrative gatekeeping and ego trips over creators (**Creator vs Administrator Gatekeeping** — the Lisbon showcase story).
   - Practicing mutual defense, peer verification, and rotating stewardship (**Co-op Solidarity**, **Burnout and Identity Fusion**).
3. **Make & Enforce Agreements (Law & Structure):**
   - Putting founder splits, 4-year vesting cliffs, and deliverables in writing even in counter-culture collectives (**Make and Enforce Agreements**, **The Equal Split Trap**, **Vesting and Dead Equity**).
   - Wrapping the DAO in a real legal entity so members aren't served in the help chat as a general partnership (**The Partnership Trap**).
   - Protecting the treasury with a stablecoin barbell and fair recoupment terms (**Treasury Death Spiral**, **Predatory Recoupment**).

---

## Themes & Pillars

Per the Vimi ("Visual Novel Design") method: settle **premise → theme → characters → outline** before drafting scenes. These are the promises every scene must keep.

### Theme (the argument)

> **Ventures don't die of bad luck. They die of deferred conversations.**

Every catastrophe in the game is preceded, chapters earlier, by a moment where the cheap-but-honest option was available and the player (like real founders) was tempted to skip it: the equity talk, the vesting doc, the treasury diversification, the security review, the "are you okay?" to a burning-out co-founder.

### Sub-themes

1. **Decentralization is a spectrum, not a virtue.** (Maya's thesis; Ch3–5)
2. **Community is an asset that compounds — and a liability that cascades.** (Jordan's arc)
3. **Money always wants something.** (Alex / Atlas; Ch2)
4. **Security is a habit, not a feature.** (Spectre; Ch4)
5. **The founder is a resource that can be drained to zero.** (Burnout stat; solopreneur research)
6. **We have been organizing collectively for a century — web3 didn't invent it.** (Vera's union-history counterpoint)

### Design pillars

- **P1 — Tempting shortcut vs. costly discipline.** Every major choice pair follows the research's Branch A/Branch B format. Shortcuts feel good *now*; the bill arrives 1–2 chapters later, visibly traceable to the choice.
- **P2 — Name the real failure.** Lesson Learned popups cite the actual case study. Education is explicit, never smuggled.
- **P3 — Relationships are governance.** Character trust meters aren't romance points — they are votes, security disclosures, and 3 a.m. warnings you only get if someone likes you.
- **P4 — Fail forward.** Bad endings are the curriculum. Ending screens summarize which decisions led here and which lesson notes to reread. Replay is expected.
- **P5 — Janky-charming PC-98.** 16-color palette, dithering, scanlines. Placeholder art embraces the constraint rather than apologizing for it.

### Tone

Warm satire. We love these people and this scene; we are honest about its absurdities. Discord drama is rendered with documentary accuracy. Never cynical about the *idea* of collective ownership — cynical only about shortcuts.

---

## Story Structure — Episodic Constellation & Rewind Framework

Instead of forcing players through a single long, linear slog before learning a lesson, **Get Rich Together (DAOCUBATOR)** is structured around an interactive **World Overview Constellation** and gripping, digestible **Episodic Micro-Dramas** powered by a **Worst-Case Hook + Rewind + 3 Checkpointed Decisions** loop.

```
flowchart TD
    START([Start Game / Experience Select]) --> CONST[World Overview: The First Constellation<br/>3 Core Pillars · Animated Disaster Nodes]
    CONST -->|Select Node| MODAL[Scenario Overview Modal<br/>OMG Disaster Hook · POV Character · 3 Target Lessons]
    MODAL -->|Exit| CONST
    MODAL -->|Confirm & Dive In| HOOK[Cold Open: Worst-Case Tragedy<br/>Ash El, Lay-Lay & Xochtl in explosive crisis]
    HOOK --> REW[⏪ THE REWIND<br/>Drop into Protagonist POV before disaster strikes]
    REW --> D1{Decision 1}
    D1 -->|Wrong Choice| BAD1[ Bad Ending + Lesson Popup]
    BAD1 -->|⏪ Instant Checkpoint Retry| D1
    D1 -->|Sovereign Choice + Lesson| D2{Decision 2}
    D2 -->|Wrong Choice| BAD2[ Bad Ending + Lesson Popup]
    BAD2 -->|⏪ Instant Checkpoint Retry| D2
    D2 -->|Sovereign Choice + Lesson| D3{Decision 3}
    D3 -->|Wrong Choice| BAD3[ Bad Ending + Lesson Popup]
    BAD3 -->|⏪ Instant Checkpoint Retry| D3
    D3 -->|Sovereign Choice + Lesson| WIN[✨ Crisis Averted!<br/>Constellation Star Ignited]
    WIN --> CONST
```

### 1. The World Overview ("The First Constellation")

Players begin at the **World Overview Constellation**, inspired by Asya's *Primordia / First Constellation* blueprint:
- Shows **3 Core Categories of Lessons**:
  1. **Keys & Sovereignty (Crypto Basis & OpSec)**
  2. **Collaboration & Co-op (Winning Together)**
  3. **Make & Enforce Agreements (Law, Structure & Treasury)**
- Glowing, animated constellation stars orbit each theme.
- Clicking a star opens a **Scenario Overview Modal** showcasing an **"OMG Disaster" Hook** (e.g., *"$60,000 Sent to the Void & Stranded in Brazil"*, *"The Jealous Gatekeeper Freezes the Lisbon Showcase"*, *"Served in the Help Chat"*). Players can exit to keep exploring or confirm to jump straight into fixing the disaster.

### 2. The Episodic Rewind Loop (~5 Minutes per Episode)

Every episode follows a tight 4-beat structure:
1. **The Hook (The Tragedy):** Drops the player directly into the nightmare outcome—**Ash El**, **Lay-Lay**, and **Xochtl** in an explosive fight as the community treasury vanishes or the project shatters.
2. **The Rewind (`⏪`):** Rewinds the timeline to the critical days before disaster strikes.
3. **Three Checkpointed Decisions (`D1 → D2 → D3`):**
   - Each wrong choice immediately triggers a punchy, memorable **Bad Ending**, unlocks the **Lesson Learned** popup, and offers a **1-click Checkpoint Rewind** right back to *that exact decision* (so players learn fast and never have to replay all 3 choices from scratch).
   - Each right choice demonstrates the sovereign solution, unlocks the **Lesson Learned**, and advances to the next decision.
4. **Resolution:** Heals the timeline, lights up the star on the World Overview Constellation, and returns the player to choose their next episode.

### 3. Playable Episodes in the Constellation

| Episode | Constellation Pillar | POV Protagonist | OMG Disaster Hook | 3 Checkpointed Decisions & Lessons |
|---------|----------------------|-----------------|-------------------|------------------------------------|
| Ep 1: No Keys, No Cheese | Keys & Sovereignty | Ash El (The Creator) | Stranded on the Brazil sanctuary trip while $60,000 vanishes into a dead address and Lay-Lay locks the multisig. | D1: Rotate leaked text-file keys on-chain & set 2-of-3 multisig (No Keys No Cheese, Credential Hygiene)<br/>D2: Vet the incoming DAO co-admin before voting (Vetting DAO Administrators)<br/>D3: Send a $1 test transaction before wiring $60,000 (The One Dollar Test Transaction) |
| Ep 2: Frozen Pay, Empty Stage | Collaboration & Co-op | Xochtl & Ash El | Hours before the Lisbon presentation, Lay-Lay freezes Ash El's game payout out of jealousy, threatening to detonate the showcase. | D1: Separate admin ops from subjective creative veto (Creator vs Administrator Gatekeeping)<br/>D2: Submit the deliverable under a neutral avatar to prove bias on-chain (Co-op Solidarity)<br/>D3: Enact rotating stewardship & rest to prevent creator burnout (Burnout and Identity Fusion, Voter Apathy and Delegation) |
| Ep 3: Blood, Cacao & Paper | Make & Enforce Agreements | Ash El & Xochtl | A departing member claims 50% dead equity, a 360 deal traps the masters, and a regulator serves the DAO via Discord chat. | D1: Reject "handshake vibes" for 4-year vesting + 1-year cliff (Make and Enforce Agreements, The Equal Split Trap, Vesting and Dead Equity)<br/>D2: Form a Swiss Verein / Co-op legal wrapper (The Partnership Trap)<br/>D3: Strike 360 cross-collateralization & build a 50% stablecoin barbell (Predatory Recoupment, Treasury Death Spiral) |
| Ep 4: One Tired Click Drained the Apothecary | Perspective Shift (Admin & Defense) | Lay-Lay (The Administrator) | Overwhelmed at 1:14 a.m., Lay-Lay gets baited by a predatory whale and a spoofed wallet popup that drains the apothecary treasury. | D1: Refuse unilateral "weekend yield" temptations & keep co-op multisig transparency (Governance Capture)<br/>D2: Verify raw hex on the hardware screen & run a $1 test batch (Verify the Hex, Ice Phishing)<br/>D3: Use a 48-hour time-lock & community delegation to defeat a flash-loan whale attack (Flash Loans and Time-locks) |

*(Note: The original 5-chapter "90-Day Founder Marathon" remains accessible from the Constellation screen as Legacy Marathon Mode.)*

---

## Game Systems

### 1. World Overview: The First Constellation (`game/constellation.rpy`)

When a player starts the game, they enter **The First Constellation**—an interactive star-map organized around the three core educational pillars:
- **Pillar I: Keys & Sovereignty** (*Crypto Basis & OpSec*)
- **Pillar II: Collaboration & Co-op** (*Winning Together vs. Gatekeeping*)
- **Pillar III: Make & Enforce Agreements** (*Law, Structure & Treasury*)

#### Interactive Constellation Nodes
- Each playable episode orbits its pillar as an **animated, glowing constellation point**.
- **Click to Inspect:** Clicking a node opens the **Scenario Overview Modal**, showing:
  - The **"OMG Disaster" Hook** (the worst-case tragedy at the heart of the episode).
  - The **POV Protagonist** (**Ash El**, **Xochtl**, or **Lay-Lay**) and supporting cast.
  - The **3 Core Lessons** taught in the scenario (with live Codex unlock status).
  - Actions to **Keep Exploring** (close modal) or **Dive In & Rewind the Disaster** (start episode).

### 2. The Rewind & Checkpointed 3-Choice Loop (`game/episodes.rpy`)

To make sessions fast, gripping, and fun to experiment with:
1. **Worst-Case Scenario Cold Open:** Every episode begins at the height of the disaster (e.g., $60,000 lost to a wrong wallet address while Ash El is stranded in Brazil and Lay-Lay locks the multisig).
2. **The Rewind (`⏪`):** A visual and narrative rewind drops the player back in time before the catastrophe.
3. **Three Checkpointed Decisions (`D1 → D2 → D3`):**
   - **Wrong Choice → Instant Bad Ending + Lesson + Checkpoint Retry:** Picking a shortcut or trap immediately plays out the disaster, triggers the **Lesson Learned** popup (`call lesson(...)`), and presents the **Rewind Retry Modal** (`⏪ Rewind to Decision N`). Players retry *that exact choice* immediately without replaying earlier choices.
   - **Sovereign Choice → Payoff + Lesson + Advance:** Picking the wise path plays out the cooperative/sovereign solution, unlocks the **Lesson Learned** popup, adjusts collective stats, and moves to the next decision.
4. **Episode Complete:** Resolving all 3 decisions heals the timeline, marks the episode star as **★ RESOLVED** in `persistent.episodes_completed`, and returns to the Constellation Map.

### 3. Core Stats & Relationships

| Stat | Start | Range | Meaning |
|------|-------|-------|---------|
| Vibes | 50 | 0–100 | Community trust, cultural energy, shared alignment |
| Treasury | 100 | 0–200 | Collective funds in ETH / stablecoin equivalents |
| Security | 40 | 0–100 | Key sovereignty, multi-sig hygiene, and legal armor |
| Morale | 60 | 0–100 | Co-creator solidarity between Ash El, Xochtl, and the team |
| Burnout | 10 | 0–100 | Creator exhaustion (high is dangerous) |

### 4. Lesson Learned Popups & Collectible Glossary

- **21 Lesson Learned Popups (`game/lessons.rpy`):** Every decision teaches a documented real-world failure mode with (1) the core principle, and (2) the historical case study + real numbers.
- **Collectible Glossary (`game/glossary.rpy`):** ~98 terms across five tabs (`BUSINESS`, `CRYPTO`, `MONEY`, `DAO`, `STATS`). Yellow underlined words in dialogue open their definition on click and unlock persistently across runs.
- **Plain Mode (`game/tl/plain/`):** Optional B1-level plain English mode selectable at start or in Preferences.

---

## Ash El — The Creator

**Role:** Visionary creator, musician, and community builder (Primary POV protagonist in Episodic Mode).
**Voice:** Grounded, soulful, passionate about real human impact; speaks in rhythms and tangible truths ("Music, medicine, and people on the ground—that's the actual treasury").
**Gear & Visual Motif:** Equipped with his acoustic-electric folk instrument; loc'd hair pinned with a feather; striped and botanical/geometric patterned tunic with green bead necklaces; warm terracotta and indigo rustic line-art palette.
**Want:** To build sovereign creative sanctuaries (like *Essential Food and Medicine*) that distribute real nourishment—music, art, free health juices, and transformative community trips—without begging gatekeepers.
**Need:** To claim digital and legal sovereignty over his own keys, agreements, and payouts instead of outsourcing the "boring admin stuff" to people who haven't earned that trust.
**Flaw:** Trusts too easily in the name of harmony; wants to focus purely on creating and healing while letting someone else hold the digital keys ("No keys, no cheese").
**Lessons he embodies:** **No Keys No Cheese**, **The One Dollar Test Transaction**, **Creator vs Administrator Gatekeeping**, **Make and Enforce Agreements**

### Real-World Inspiration (Asya's Narrative)

Ash El represents the visionary creators in collectives like *Essential Food and Medicine* who bring all the actual labor, art, music, and community programs (distributing free health juices, organizing sanctuary trips to Brazil and South Dakota, building interactive showcases for Lisbon), only to find themselves stranded or blocked when administrators hoard the multi-sig keys or let awe curdle into jealousy.

### Arc across the Constellation Episodes

- **Episode 1 — "No Keys, No Cheese" (POV: Ash El):** Confronted with the nightmare of being stranded in Brazil while $60,000 vanishes and Lay-Lay holds the keys, Ash El rewinds time to rotate leaked keys on-chain, vet incoming DAO administrators, and enforce the $1 test transaction rule.
- **Episode 2 — "Frozen Pay, Empty Stage" (POV: Xochtl & Ash El):** After working sleepless weeks on a game and music showcase for Lisbon, Ash El faces an administrative payout freeze from a jealous gatekeeper—and learns how co-op solidarity and objective milestone escrow defeat ego trips.
- **Episode 3 — "Blood, Cacao & Paper" (POV: Ash El & Xochtl):** Learns why counter-culture collectives still need written vesting agreements, legal wrappers, and capped recoupment deals.
- **Episode 4 — "One Tired Click Drained the Apothecary" (Co-star):** Holds the line as a co-signer alongside Xochtl when Lay-Lay is tempted by whale money and spoofed transactions.

### Expressions needed

`neutral`, `focused`, `alarmed`, `hurt`, `determined`, `proud`

---

## Lay-Lay — The Administrator

**Role:** DAO Operations & Treasury Administrator / Antagonist-Archetype (also playable POV in Episode 4).
**Voice:** Smooth, bureaucratic dressed as spiritual ("Let me handle the multisig so you creatives can stay in your flow—why are you bringing colonial legal energy into our sanctuary?").
**Gear & Visual Motif:** Associated with administrative power, glass potion vials, and dried herb bundles paired with a digital multisig key ledger; sage green and alchemical violet rustic line-art pattern.
**Want:** Control, status, and the intoxicating leverage of holding the treasury keys for a collective of brilliant creators.
**Need:** Constitutional guardrails, multi-sig accountability, and separation of powers—because un-oversighted crypto-financing corrupts anyone who holds the keys alone.
**Flaw:** Unaccustomed to instant, un-oversighted treasury power; mistakes administrative access for ownership, and lets admiration for superstar creators curdle into jealousy and gatekeeping.
**Lessons she embodies:** **No Keys No Cheese**, **Vetting DAO Administrators**, **Creator vs Administrator Gatekeeping**, **Governance Capture**

### Real-World Inspiration (Asya's Narrative)

Lay-Lay synthesizes the toxic administrative power dynamic from real-world DAO post-mortems:
1. **The Key Hoarder:** Administrators who held all the multi-sig keys while creators like Ash El were on the ground in Brazil or South Dakota, misappropriating funds or funneling money elsewhere because there were no guardrails.
2. **The Jealous Gatekeeper (The "Amy & Edward" Story):** The administrator who became so awed by a creator's output that it curdled into jealousy, refusing to pay for the Lisbon presentation game until the exact same work was covertly submitted under a different avatar—which she approved instantly.

### Arc across the Constellation Episodes

- **Episode 1 — "No Keys, No Cheese":** Offers to take sole custody of the treasury after a text-file key leak and pushes an unvetted co-admin into the DAO.
- **Episode 2 — "Frozen Pay, Empty Stage":** Freezes Ash El's Lisbon showcase payout out of personal ego, only to expose her own bias when Xochtl submits the identical work under an anonymous co-op proposal.
- **Episode 3 — "Blood, Cacao & Paper":** Pushes for "vibes-only handshake splits" and unwrapped governance until legal and financial reality catches up.
- **Episode 4 — "One Tired Click Drained the Apothecary" (POV: Lay-Lay):** Playable perspective episode showing how an overwhelmed administrator gets targeted by whales (Atlas) and phishing attacks—and how choosing transparency and multi-sig discipline saves both her and the collective.

### Expressions needed

`neutral`, `calculating`, `smirk`, `defensive`, `stern`, `alarmed`

---

## Xochtl — The Co-Creator & Shaman

**Role:** Ceremonial space-holder, co-creator, cacao medicine practitioner, and strategic protector of the collective (POV protagonist in Episode 2 & co-protagonist across all episodes).
**Voice:** Warm, perceptive, fiercely protective of creators; blends ancestral ceremonial wisdom with razor-sharp practical discernment ("Ceremony is about intention, hermano—and a smart contract is just an intention written in code. Read the hex before you drink the cup.").
**Gear & Visual Motif:** Associated with cacao ceremonies and steaming ceremonial cups; beaded headband, red-and-black ceremonial face paint stripes across forehead, cheeks, and chin, beaded geometric fringe earrings, rainbow-striped woven huipil/poncho, and geometric wrist cuffs; cacao bronze and turquoise rustic line-art palette.
**Want:** To weave indigenous/communal reciprocity, real medicine, and sovereign technology into a living co-op where creators and caregivers thrive together.
**Need:** To bridge the gap between sacred trust and hard verification—teaching the collective that true ceremony requires clear agreements and verified transactions.
**Flaw:** Will sometimes carry emotional mediation for the whole group until tension boils over.
**Lessons she embodies:** **Co-op Solidarity**, **Creator vs Administrator Gatekeeping**, **The One Dollar Test Transaction**, **Make and Enforce Agreements**

### Real-World Inspiration (Asya's Narrative)

Xochtl embodies the grounded co-creators and community protectors (including the "Jena" archetype in the Lisbon story) who see through ego games and administrative gatekeeping. When Lay-Lay blocks Ash El's payout out of jealousy before Lisbon, Xochtl devises the brilliant co-op jujitsu move: having Ash El submit the exact same work under a neutral avatar so the funds are approved on the spot and the bias is proven beyond argument.

### Arc across the Constellation Episodes

- **Episode 1 — "No Keys, No Cheese":** Holds the second hardware key in the 2-of-3 co-op multisig and coordinates on-the-ground verification in Brazil for the $1 test transaction.
- **Episode 2 — "Frozen Pay, Empty Stage" (POV: Xochtl):** Steps in when Lay-Lay freezes Ash El's payout, orchestrating the covert avatar submission that saves the Lisbon presentation and reforms the DAO's bounty constitution.
- **Episode 3 — "Blood, Cacao & Paper" (POV: Ash El & Xochtl):** Insists that sacred work deserves sacred protection—allying with Vera to paper the 4-year vesting cliff and Swiss Verein legal wrapper.
- **Episode 4 — "One Tired Click Drained the Apothecary":** Anchors the community stewards to outvote Atlas's hostile governance capture.

### Expressions needed

`neutral`, `warm`, `focused`, `stern`, `hurt`, `proud`

---

## The Player — The Founder

Customizable name (default **Kai**). Silent-ish protagonist with attitude expressed through choices. Left a stable job to start a creative collective; carries the **Burnout and Identity Fusion** risk personally — the Burnout stat is *theirs*.

**Want:** build a collective that outlives them.
**Need:** to learn that discipline is care, and that they are not the venture.
**Flaw:** says yes to everything (each yes is a Burnout tick).

### Venture choice (Ch1)

-  **Record label** — unlocks **Predatory Recoupment** content (360 deals, cross-collateralization)
-  **Streetwear brand** — unlocks **Chargeback Death Spiral** + sourcing/tooling content
-  **Artist collective** — unlocks **The Overfunding Paradox** (viral drop overfunds 300%)

### Expressions needed

None in v1 (first-person POV, no self-sprite). Side-image "tired" variant when Burnout ≥ 60 would be a nice v2 touch.

---

## Maya — The Builder

**Role:** Technical co-founder. Smart contracts, tokenomics, infrastructure. (The only character who appears in all three prototypes — she's the load-bearing wall.)
**Voice:** "Ships code, not vibes." Dry, precise, kind underneath.
**Want:** governance that mathematically works.
**Need:** to admit she's running on fumes and let others carry weight.
**Flaw:** contempt for "community theater" isolates her; grinds toward burnout silently.
**Lessons she embodies:** **Vesting and Dead Equity**, **Burnout and Identity Fusion** (mirror of the player's own stat)

### Arc by chapter

- **Ch1:** Recruited first. Insists on talking equity + vesting *now* — the player's response sets the `equity` flag and her baseline trust.
- **Ch2:** Argues for barbell treasury; overruled if player takes whale money without conditions.
- **Ch3:** Her crisis (from startupfounders98's betrayal arc): a competitor offers 3× salary *while* she's burned out. High trust + low player Burnout → honest conversation, she stays. Low trust or `equity == equal` → resignation, and without vesting she leaves as **dead equity**.
- **Ch4:** If present, she's the one who spots the attack. Her absence makes every Ch4 vector worse (−15 Security).
- **Ch5:** Votes with the player only if trust ≥ 60.

### Relationship mechanics

- ≥ 50: warns player about treasury mix before Ch4c can trigger.
- < 30 after Ch3: leaves; `maya_gone` flag.

### Expressions needed

neutral, focused, tired, proud, alarmed

---

## Jordan — The True Believer

**Role:** Community lead. Discord shepherd, meme laureate, keeper of the mission. (dao25's Jordan fused with daoromance's Aiko — idealism + 2:47 a.m. energy.)
**Voice:** "The tech means nothing without the people." Exclamation points, then sudden 3 a.m. doubt.
**Want:** a movement people believe in.
**Need:** to learn that trust systems beat trust vibes — moderation, reputation, hard conversations.
**Flaw:** idealism blinds them to bad actors; takes every community fight personally.
**Lessons they embody:** **Voter Apathy and Delegation**, **Greenwashing Trap** (they champion the eco-partnership in Ch5's optional beat)

### Arc by chapter

- **Ch1:** Second recruit. Their intro scene teaches the troll-farm / quiet-quitter / vocal-non-contributor taxonomy.
- **Ch2:** Leads the community launch; furious if player sells allocation with veto rights attached ("#SellOut trending").
- **Ch3:** Ground zero of Proposal #17. Their handling of factions depends on whether the player invested in community systems in Ch1–2.
- **Ch4:** In 4b (51% attack), Jordan's community defense (pooled small-holder delegation) is the good path — only available if Vibes ≥ 50.
- **Ch5:** Their late-night "was it worth it?" call is the emotional climax before the final vote (lifted from daoromance's best scene).

### Relationship mechanics

- ≥ 60: community defense path in Ch4b succeeds automatically.
- < 30: Death by Democracy apathy counter +1.

### Expressions needed

neutral, hyped, hurt, determined, exhausted

---

## Alex — The Mercenary

**Role:** Treasury / finance. DeFi native, sharp suit, always checking prices. (dao25's Alex fused with daoromance's Drake — competence you can't fully trust.)
**Voice:** "…Or reckless. Depends on your vesting schedule."
**Want:** to prove profit and purpose can coexist.
**Need:** one relationship that isn't transactional.
**Flaw:** ethically flexible under pressure; unclear loyalties until Ch4.
**Lessons they embody:** **Treasury Death Spiral**, **Predatory Recoupment** (they *bring* the 360-deal term sheet, genuinely thinking it's good)

### Arc by chapter

- **Ch1:** Optional third recruit; critiques the player's token allocation draft.
- **Ch2:** The chapter is theirs: treasury mix decision, whale negotiation, and (label route) the recoupment term sheet.
- **Ch3:** Quietly courted by Atlas. Trust ≥ 50 → they disclose it; otherwise it surfaces in Ch4b as a gut-punch.
- **Ch4:** Loyalty resolves. High trust → they leak Atlas's accumulation early (+1 warning turn). Low trust → they've been advising Atlas ("it was just consulting").
- **Ch5:** If loyal, argues against the acquisition; if not, brokers it.

### Relationship mechanics

- ≥ 50 at end of Ch3: `alex_loyal` flag → early warning in Ch4b.
- < 30: they facilitate the whale (Ch4b harder).

### Expressions needed

neutral, smirk, calculating, defensive, sincere

---

## Vera — The Organizer

**Role:** Mentor. Retired union organizer turned angel investor. (dao25's Vera fused with startupfounders98's Eleanor the angel.)
**Voice:** "We were doing 'governance tokens' in 1936. We called them union cards."
**Want:** to see a new generation get collective action right.
**Need:** to accept the new generation will do it *differently*, on-chain and weird.
**Flaw:** patience reads as passivity; she won't save you unless you ask.
**Lessons she embodies:** **The Partnership Trap** (she's seen members held personally liable before), the historical counterpoint to every sub-theme.

### Arc by chapter

- **Ch1:** Met at a mixer; offers the legal-wrapper advice ("$15k for a Swiss Verein is cheap insurance"). Player can dismiss her as boomer noise — that's the **The Partnership Trap** setup.
- **Ch2:** Counteroffer to Atlas's money: smaller check ($20k for 10%, no board seat, monthly dinners) — startupfounders98's angel scene.
- **Ch3:** Trust ≥ 40 unlocks the compromise path on Proposal #17 (voluntary founder token burn) and the "win the battle, lose the war" veto warning.
- **Ch4:** In 4b, teaches pooled delegation ("solidarity is a governance primitive").
- **Ch5:** Delivers the thematic closing argument regardless of ending — tone varies.

### Relationship mechanics

- ≥ 40: Ch3 compromise path; regulator beat in Ch5 softened if `wrapper == none`.
- Taking her Ch2 deal: +20 Vera, `mentor` flag (Morale +1/chapter passive).

### Expressions needed

neutral, wry, stern, warm

---

## Spectre — The Ghost

**Role:** Anonymous security contributor. Hoodie-shadow PFP, camera never on, timezone unknown. (From daoromance, rebuilt as the opsec teacher.)
**Voice:** Encrypted messages, lowercase, no small talk. "your cloudflare key is in a public gist. fix it."
**Want:** to protect things without being known.
**Need:** one context where being known doesn't get them hurt.
**Flaw:** trust issues cut both ways — the team never knows if Spectre is guardian or inside threat, and low-trust players act on that suspicion wrongly.
**Lessons they embody:** **Verify the Hex**, **Ice Phishing**, **Credential Hygiene**

### Arc by chapter

- **Ch1:** First encrypted DM: they found a vulnerability in the token contract *before launch*. Accepting the camera-off call starts the trust track.
- **Ch2:** Pushes back on "ship fast" opsec culture; the `opsec` flag is largely set by whether the player funds their audit ask.
- **Ch3:** Quietly flags Atlas's wallet clusters accumulating. Trust < 40 → the player has no reason to believe them.
- **Ch4:** The star of 4a: the spoofed-transaction set piece (player must actually expand the transaction and compare hex against the whitelist — research's flagship mechanic). If trust ≥ 60 they intercept the front-end attack in time.
- **Ch5:** Optional: reveals a sliver of identity if trust ≥ 80. Never the full face. (Sprite stays hooded in all endings — hard rule.)

### Relationship mechanics

- ≥ 60: pre-attack warning scene before Ch4 (any vector).
- Funding their audit in Ch2: Security +15, Treasury −20, `opsec = hardened`.

### Expressions needed

neutral(hooded), typing-glow, alert, almost-vulnerable

---

## Atlas — The Whale

**Role:** Benefactor-antagonist. Enormous anonymous wealth, protective energy, patient accumulation. (daoromance's Atlas fused with dao25's THE WHALE — the game's ambiguous heavy.)
**Voice:** Generous in public, precise in private. "Consider it a governance tax."
**Want:** control, framed as stewardship. Atlas genuinely believes founders always blow it and adult supervision is a kindness.
**Need:** to be told no by someone who doesn't need their money.
**Flaw:** cannot distinguish helping from owning.
**Lessons they embody:** **Governance Capture**, **Flash Loans and Time-locks**

### Arc by chapter

- **Ch1:** Cameo — a huge early donation to the mint, unexplained. (Foreshadow: the tokens never move. They're waiting.)
- **Ch2:** The offer: 500 ETH. Player's terms (accept / conditions / decline) set `whale_in` and how Ch4b plays.
- **Ch3:** Courting Alex; buying quietly through fresh wallets (Spectre notices).
- **Ch4:** In 4b, executes the capture attempt — via market accumulation if `whale_in`, via flash loan if the player skipped time-locks. Not a cartoon villain: their proposal is professionally written and half the community *likes it*.
- **Ch5:** Depending on outcome: gracious loser, silent partner, or the new owner of everything you built.

### Design rule

Atlas must be *right about something* in every appearance. The tragedy of governance capture is that whales fund the ecosystem — the game is honest about that.

### Expressions needed

neutral, generous, guarded, predatory-calm

---

## Chapter 1 — Genesis Block

**Dramatic question:** Who do you build with, and on what terms?
**Lessons:** **The Equal Split Trap** · **Vesting and Dead Equity** · **The Partnership Trap**

### Scene cards

#### 1.1 Cold open — the resignation
- **Goal:** establish the player quit BigCorp with modest savings to start a creative collective.
- **Choice:** venture type →  label /  streetwear /  collective (`venture` flag).
- **Tone beat:** "NounsDAO. MakerDAO. The Aragon crisis. You've watched them all rise and fall. Now it's your turn."

#### 1.2 Meet **Maya**
- **Conflict:** she's interested but interrogates the player's decentralization philosophy.
- **Choice:** flatter her vs. engage the philosophy (rel±, sets her respect baseline).

#### 1.3 The equity conversation ⚖️ (KEYSTONE)
- Maya forces the talk founders defer. **Choice:** equal 50/50 ("we're friends!") / merit-based / **4-year vesting with 1-year cliff**.
- Equal: Morale +, sets `equity=equal` → Ch3 blows up harder. Vesting: Maya rel ++, Morale − (awkward now, saves you later).
- **Lesson popup:** **The Equal Split Trap** (73% of startups split in month one; 3× unhappier).

#### 1.4 Meet **Jordan**
- Discord is already growing. Troll-farm / quiet-quitter taxonomy comedy beat.
- **Choice:** community-first onboarding vs. "growth now, systems later" (Vibes vs. later apathy counter).

#### 1.5 Meet **Alex** (optional recruit)
- Critiques the token allocation draft. **Choice:** bring them in / keep treasury founder-run (sets whether Ch2 has an advocate or a blind spot).

#### 1.6 Vera at the mixer 
- **Vera** asks one question: "Who's liable when this goes wrong?" Offers the **legal wrapper** ($15k Swiss Verein).
- **Choice:** pay (Treasury −15, `wrapper=verein`) / "we're decentralized, we don't need it" (`wrapper=none`).
- **Lesson popup:** **The Partnership Trap** (Ooki DAO: served via chat box, $634,542 penalty).

#### 1.7 Spectre's DM 
- Encrypted message: vulnerability in the mint contract. **Choice:** camera-off call / text only / ignore (Spectre rel, Security ±10).

#### 1.8 Token design ceremony
- **Choice:** equal founder split / merit / 60% community treasury (Decentralization flavor; feeds Ch3 Proposal #17 rhetoric).
- Atlas cameo: an enormous anonymous mint donation. The tokens don't move. *(foreshadow)*

#### 1.9 Chapter close — Genesis
- Stats recap screen; day counter jumps to 30.

### Open questions
- Should venture type change the co-founder lineup, or only scene flavor? (v1: flavor only)

---

## Chapter 2 — Token Generation Event

**Dramatic question:** Whose money do you take, and what does it cost?
**Lessons:** **Treasury Death Spiral** · **Predatory Recoupment** / **Chargeback Death Spiral** / **The Overfunding Paradox** (by route) · **Credential Hygiene**

### Scene cards

#### 2.1 TGE eve
- Hype montage. Jordan's Discord at 10k members. "Believers and vultures line up alike."

#### 2.2 Treasury composition  (KEYSTONE)
- Maya vs. Alex debate. **Choice:** 90% native token ("aligned!") vs. **barbell: 30–50% stables** (Treasury −10 now from swap fees, `treasury_mix` flag).
- **Lesson popup:** **Treasury Death Spiral**.

#### 2.3 Atlas's offer  (KEYSTONE)
- 500 ETH. "No strings." Drake-whisper beat from Alex: *whales always want something.*
- **Choice:** accept (Treasury +50, `whale_in=true`, Vibes −10) / accept **with conditions** (advisory only, +25, Atlas rel −5) / decline (Vibes +10, Treasury −10, Atlas rel −15).

#### 2.4 Route beat (by `venture`)
- **Label:** Alex brings a distribution term sheet — 360 deal, cross-collateralized advances. Reject/negotiate/sign → **Predatory Recoupment**.
- **Streetwear:** the 8-piece collection vs. single-item pre-order niche → sourcing squeeze, **Chargeback Death Spiral** seeds.
- **Collective:** the drop goes viral, 300% overfunded → **The Overfunding Paradox** (Coolest Cooler beat: unit cost math on screen).

#### 2.5 Spectre's audit ask 
- "your launch is in 72h. i need 20 eth and admin access to audit. or don't. good luck."
- **Choice:** fund it (`opsec=hardened`, Security +15, Treasury −20) / ship fast (`opsec=rushed`, Burnout +10 — you review it yourself at 4 a.m.).

#### 2.6 The shared doc incident 
- A mod pastes the multisig seed phrase into the team Notion "just temporarily."
- **Choice:** blow up publicly (Security +10, Morale −10) / fix quietly (Security +5) / "we'll deal with it after launch" (Security −15).
- **Lesson popup:** **Credential Hygiene** (8ight Finance, $1.75M via Google Doc).

#### 2.7 Vera's counteroffer
- Small check, mentorship, monthly dinners. Take alongside/instead of Atlas → `mentor` flag.

#### 2.8 Launch night 
- Outcome text assembled from flags. Burnout +15 regardless — launches cost you either way.

#### 2.9 Chapter close — first price candle
- If `treasury_mix=mono`: dramatic irony line about how good the chart looks.

---

## Chapter 3 — Governance Wars

**Dramatic question:** Who actually rules — and who's quietly leaving?
**Lessons:** **Voter Apathy and Delegation** · **Burnout and Identity Fusion** · **Vesting and Dead Equity** (payoff)

### Scene cards

#### 3.1 Honeymoon's over
- Turnout on routine proposals: 6.3%. Jordan is answering 400 DMs a day. Apathy counter mechanics introduced.

#### 3.2 Proposal #17 ⚖️ (KEYSTONE)
- "Redistribute founder tokens to the community." 35% support and climbing. Half the arguments are *good*.
- **Choice:** rally votes democratically (Vibes −5, apathy −1) / **use founder veto** (`veto_used=true`, Vibes −15, Security +5 — **Founders Capture** eligibility) / compromise: voluntary 10% founder burn (needs Vera ≥ 40; Vibes +15).
- Vera's line on veto: "You'll win the battle. I've watched a hundred locals win that battle."

#### 3.3 The delegation debate
- Low turnout → delegation proposal. Top-decile-controls-76% stat dramatized as a pie chart on stream.
- **Choice:** open delegation / capped delegation / do nothing (apathy +1).
- **Lesson popup:** **Voter Apathy and Delegation**.

#### 3.4 Maya's 3× offer  (KEYSTONE — from startupfounders98)
- Competitor offers Maya triple salary. She's been quiet for two weeks (the player saw it, if they were looking).
- **Branches:** direct-but-kind → truth; demand answers → defensive; give space → resignation email + (if `equity=equal`, no vesting) **dead equity legal nightmare** (Treasury −20, Burnout +20).
- **Lesson popup:** **Vesting and Dead Equity** — this is where Ch1's keystone pays off, good or bad.

#### 3.5 Spectre's wallet clusters
- Fresh wallets accumulating in coordinated patterns. Believing them requires Spectre ≥ 40; otherwise the player has every reason to shrug. *(Sets up Ch4's "you were warned" trace.)*

#### 3.6 Burnout mirror 
- Forced quiet scene: the player character at 4 a.m., reading their own old launch-day post.
- **Choice:** take the weekend (Burnout −20, one small Treasury/Vibes cost) / push through ("the collective needs me") (Burnout +15).
- If Burnout ≥ 60 after this: consequence-hint corruption begins (see **Game Systems**).

#### 3.7 Alex's quiet dinner
- Atlas is courting Alex. Disclosure only if Alex ≥ 50. Otherwise a black screen: *"Somewhere across town, a dinner you weren't invited to."*

#### 3.8 Chapter close — factions
- Faction map screen: Decentralists / Pragmatists / Opportunists sized by accumulated Vibes/choices.

---

## Chapter 4 — The Attack

**Dramatic question:** Can the thing you built survive contact with an adversary?
**Structure rule:** the game chooses the vector you're *most vulnerable to* (priority: 4a if `opsec=rushed` → 4b if `whale_in` or Atlas rel high with no time-locks → 4c if `treasury_mix=mono` → else 4b at reduced strength). Consequences must trace visibly to earlier shortcuts.

If Spectre ≥ 60: a pre-attack warning scene fires first (one extra preparation choice, any vector).

### 4a — The Phish (opsec vector)
Lessons: **Verify the Hex** · **Ice Phishing**
- **4a.1** Maya's wallet behaves oddly; a routine treasury transaction is queued at 1 a.m.
- **4a.2 SET PIECE :** the signing screen. The player sees a plausible transaction summary. The *correct* move is to click **[EXPAND RAW DATA]** and compare the destination hex against the whitelist, mimicking the Nexus Mutual hack. Fatigued founders (Burnout ≥ 60) see the hexes rendered in a harder-to-read dithered font — diegetic error rate.
  - Sign without checking → Treasury −60, straight to 4.5 triage.
  - Verify and catch it → Security +15, attacker pivots to front end (4a.3).
- **4a.3** Ice phishing: injected approval-harvesting script on the site (Badger DAO). **Choice:** take the front end down now (Vibes −10, correct) / "keep it up, mint is live" (users drained, Vibes −30).

### 4b — The 51% (governance capture vector)
Lessons: **Governance Capture** · **Flash Loans and Time-locks**
- **4b.1** RED ALERT (Maya, if present): one entity controls 45% of governance tokens. Proposal queued: "Treasury Diversification Initiative" — professionally written; hidden drain logic (Beanstalk's Trojan pattern, with a charity distraction proposal).
- **4b.2 KEYSTONE choice:** emergency pause (Security +, Vibes −20, "decentralized until it's inconvenient", fork risk) / **community defense** — pooled small-holder delegation, needs Jordan ≥ 60 or Vibes ≥ 50 (Vera: "solidarity is a governance primitive") / negotiate with Atlas (Treasury −50, "governance tax", Atlas rel +).
- **4b.3** Resolution + `alex_loyal` reveal beat either way.

### 4c — The Spiral (treasury vector)
Lesson: **Treasury Death Spiral**
- **4c.1** Macro crash; native token −70% in a week. Payroll due. If mono-treasury: purchasing power gone exactly when needed.
- **4c.2** **Choice:** sell native into the crash (accelerates spiral, Vibes −20) / emergency raise from Atlas (whale enters late, Ch5 leverage) / cut everything and hibernate (Morale −25, survive small).

### 4.5 — Triage (all vectors converge)
- Casualty accounting: stats, who left, what the community is saying.
- **Lesson popup** for the vector's case study, with real numbers (Build Finance $470k / Beanstalk $181M / Badger $121M / Nexus Mutual $8M).
- Burnout +20. If that pushes ≥ 80 → forced rest scene or **Burnout Crash** risk.

### Open questions
- Should a flawless Ch1–3 run skip Ch4 entirely? Proposal: no — you get 4b at reduced strength and win it, because the *lesson is that attacks come regardless*.

---

## Chapter 5 — Resolution

**Dramatic question:** What was all this *for*?
**Lessons:** synthesis of all; optional **Greenwashing Trap** beat.

### Scene cards

#### 5.1 After the storm
- Day 90. State-of-the-DAO recap assembled from flags — every surviving character gets one line reflecting their arc.

#### 5.2 The regulator letter  (payoff of Ch1.6)
- If `wrapper=verein`: a formality, one wry Vera line. If `wrapper=none`: members are being served personally (Ooki-style, via the Discord webhook of all things). Treasury −20, Vibes −10.

#### 5.3 Optional beat — the green partnership 
- A carbon-credit protocol offers a lucrative "regenerative" partnership; Jordan champions it. The credits are 2011 Chinese hydro dams.
- **Choice:** sign fast / let Spectre & Maya diligence it (catches it; KlimaDAO cited) / decline on instinct.
- **Lesson popup:** **Greenwashing Trap**.

#### 5.4 The acquisition offer  (from startupfounders98)
- BigCorp (or a rival DAO) offers to absorb the collective. Real money for tired people.
- **Choice:** take it → **Acqui-hire** ending immediately / negotiate (better terms, still Acqui-hire, better epilogue) / refuse → continue.

#### 5.5 Jordan's 3 a.m. call ☎️ (emotional climax)
- "Was it worth it?" The player's honest answer here sets the epilogue's emotional key, not the stats.

#### 5.6 The reform vote ️ (KEYSTONE)
- Three constitutional paths: **Full decentralization** (remove founder privileges) / **Balanced governance** (time-locks + quorums + elected council) / **Benevolent leadership** (founders keep guardrails).
- Character votes are computed from relationship values — the player watches their 90 days of relationship choices tally on screen.

#### 5.7 Ending computation
- See **Endings Overview**. Ending screen lists: 3 pivotal choices this run, lessons unlocked, lessons *missed* (tease replays).

#### 5.8 Vera's closing argument
- Plays over every ending, re-keyed by outcome. Draft line: "The tools are new. The work is old. The work was always each other."

---

## Endings Overview

Evaluated in this order (first match wins), after Ch5.6 unless an early-exit ending fired. Bad endings are curriculum (Pillar P4): each ending screen names the 3 pivotal choices and links the missed lessons.

| # | Ending | Trigger | Tone |
|---|--------|---------|------|
| 1 |  Acqui-hire | Chose acquisition in 5.4 | Bittersweet. "Wealthy but incomplete. Not a failure. Not quite a win." |
| 2 |  Burnout Crash | Burnout ≥ 80 at any chapter close (and skipped the rest scene) | The venture survives you. Or doesn't. Solopreneur research payoff — identity ≠ venture. |
| 3 |  Hostile Takeover | Security < 20 or Treasury ≤ 10 | Atlas (or the phisher) owns it. "A cautionary tale studied in governance courses." |
| 4 | ️ Founder's Capture | `veto_used` and final vote = benevolent leadership | You kept control of everything except the point. "Web2 with extra steps." |
| 5 |  Death by Democracy | apathy ≥ 3 and Vibes < 40 | 47 proposals pending. Three months to approve a logo. A ghost town with perfect process. |
| 6 |  Community Split | Vibes < 30 | The fork. Three DAOs, one dream, zero momentum. Default-bad fallback. |
| 7 |  Sustainable Collective | Survived, no golden thresholds, Morale ≥ 40 | The quiet good ending. Small, profitable, humane. You sleep well. |
| 8 |  Collective Prosperity (golden) | Vibes ≥ 60 · Morale ≥ 60 · Security ≥ 50 · Treasury ≥ 80 · Burnout < 50 · final vote = balanced governance | The blueprint others copy. Every co-founder's epilogue is warm. Hard to reach on run one — by design. |

### Epilogue modifiers (stack on any ending)

- `maya_gone` → her epilogue line arrives as a LinkedIn notification.
- Spectre ≥ 80 → one extra scene: the sliver-of-identity reveal.
- `mentor` flag → Vera's closing argument is addressed to the player by name.
- Jordan's 5.5 answer re-keys the final music sting (hopeful vs. elegiac).

### Open questions
- Do we want a secret 9th ending for a flawless golden run + Spectre 80 ("The Handoff" — you leave, and it keeps working without you)? Strong thematic candidate for v2.

---

## Lessons Index

One note = one Lesson Learned popup = one entry in the in-game Codex. Organized by the **Three Constellation Pillars** of the World Overview (plus the Legacy 90-Day Marathon lessons).

### Pillar I: Keys & Sovereignty (Crypto Basis & OpSec)
- **No Keys No Cheese** — Sovereignty, non-custodial vs. custodial keys, 2-of-3 multisigs, and NEAR-style account key rotation after a text-file leak (`no_keys_no_cheese`)
- **Vetting DAO Administrators** — Investigating incoming DAO members/admins and scoping permissions before voting them in (`vetting_admins`)
- **The One Dollar Test Transaction** — Always sending a $1 test transaction and confirming receipt before wiring bulk funds (`test_transaction`)
- **Credential Hygiene** — Never pasting seed phrases or private keys into shared docs (`credentials`)
- **Verify the Hex** — Reading the hardware wallet screen instead of trusting spoofed browser extensions (`verify_hex`)
- **Ice Phishing** — Front-end CDN security and malicious token approvals (`ice_phishing`)

### Pillar II: Collaboration & Co-op (Winning Together vs. Toxic Power)
- **Creator vs Administrator Gatekeeping** — The Lisbon showcase story ("Amy & Edward / Jena"): preventing admin jealousy from freezing creator payouts (`creator_vs_admin`)
- **Co-op Solidarity** — Collaboration & Co-op = Winning Together through peer verification and rotating stewardship (`coop_solidarity`)
- **Burnout and Identity Fusion** — Sustainable pacing and separating personal identity from the venture (`burnout`)
- **Voter Apathy and Delegation** — Why 6.3% turnout and unchecked delegation re-centralize power (`apathy`)
- **Governance Capture** — How whales and insiders quietly buy control of a treasury (`capture`)
- **Flash Loans and Time-locks** — Why instant proposal execution invites flash-borrowed attacks (`flashloan`)

### Pillar III: Make & Enforce Agreements (Law, Structure & Treasury)
- **Make and Enforce Agreements** — Why counter-culture collectives and fast innovators still need written agreements and legal armor (`agreements_law`)
- **The Equal Split Trap** — Why 50/50 handshake splits fail when contributions diverge (`equal_split`)
- **Vesting and Dead Equity** — 4-year vesting, 1-year cliff, and preventing departing founders from holding the cap table hostage (`vesting`)
- **The Partnership Trap** — Unincorporated DAOs as general partnerships (CFTC v. Ooki DAO) vs. Swiss Verein / Co-op LLC wrappers (`partnership`)
- **Treasury Death Spiral** — Why a 90% native-token treasury collapses in a bear market vs. the 50% stablecoin barbell (`death_spiral`)
- **Predatory Recoupment** — 360 deals and cross-collateralization in music/creative contracts (`recoupment`)
- **Chargeback Death Spiral** — Payment processor freeze thresholds and pre-order validation (`chargeback`)
- **The Overfunding Paradox** — Why viral overfunding below unit cost bankrupts projects (`overfunding`)
- **Greenwashing Trap** — Verifying physical assets before financializing them (`greenwash`)

---

## Art Style Guide — Minimalist Rustic Line-Art & Analog Watercolor

### Visual Direction

Moving away from generic, overly saturated cyber-punk and heavy 3D metallic gold renders, **Get Rich Together** uses a **minimalist, high-contrast rustic line-art and analog watercolor** aesthetic:
- **Rustic Ink Line-Art:** Crisp, expressive black and sepia ink contours (`#141210` and `#2B2520`) inspired by woodcut printmaking, botanical illustration, and rotoscoped indie graphic novels (see `research/visual references/5. Efam DAO Esphera texture overlay`).
- **Analog & Watercolor Textures:** Warm, breathable parchment, raw canvas, and organic watercolor washes that are easy on the eyes and translate cleanly into physical merchandise, zines, and screen prints.
- **Flat High-Contrast Backgrounds:** Clean architectural and natural silhouettes over textured paper washes—never cluttered or noisy.

### Core Palette

| Name | Hex | Role & Archetype Mapping |
|------|-----|--------------------------|
| Charcoal Ink | `#141210` | Primary line-art, Constellation night sky, high-contrast outlines |
| Warm Parchment | `#F4EFE6` | Light canvas base, dialogue typography, clean breathing room |
| Sunlit Ochre | `#E8C574` | Sanctuary walls, constellation starlight, Lesson unlocked accents |
| Terracotta Ember | `#E07A5F` | Ash El accent color — creator warmth, acoustic resonance,woven poncho geometry |
| Alchemical Violet | `#9B7EDE` | Lay-Lay primary accent — administrative power, apothecary potion vials |
| Herbal Sage | `#528C6E` | Lay-Lay & Sanctuary secondary accent — medicinal herbs, botanical leaves |
| Cacao Turquoise | `#2EC4B6` | Xochtl primary accent — ceremonial clarity, sacred water, beadwork |
| Cacao Bronze | `#8C533E` | Xochtl secondary accent — ceremonial cacao cup, earth grounding |
| Crimson Alert | `#D64545` | Worst-Case Scenario hooks, Rewind triggers, Bad Ending flashes |

### Character & Asset Mapping

Rather than generic avatars, the core cast is built around unmistakable visual archetypes, signature gear, and color-coded textile patterns:

1. **Ash El (The Creator / Protagonist):**
   - **Gear:** Equipped with his acoustic-electric folk instrument (`charango` / guitar) strapped across his chest, green bead necklaces, and a feather pinned in his locs.
   - **Pattern:** Vertical indigo/cream stripes paired with terracotta & botanical leaf line-art motifs.
2. **Lay-Lay (The Administrator / Antagonist):**
   - **Gear:** Equipped with glass apothecary potion vials, dried herb bundles, and an ornate administrative multisig key & ledger tablet.
   - **Pattern:** Interlocking key-step fretwork in alchemical violet and herbal sage.
3. **Xochtl (The Co-Creator / Shaman):**
   - **Gear:** Holding a steaming ceremonial cacao cup; wearing a geometric beaded headband, red-and-black ceremonial face paint stripes across forehead, cheeks, and chin, and long beaded fringe earrings.
   - **Pattern:** Horizontal rainbow-earth woven huipil stripes and black-and-white geometric zig-zag wrist cuffs.

---

## Asset List

Status legend: ⬜ needed ·  generated & live in `game/images/` · ✅ final

### Core Episodic Cast Sprites (Minimalist Rustic Line-Art & Analog Watercolor, 560×880)

| Character | Archetype & Signature Gear | Color-Coded Pattern | Expressions | Status |
|-----------|----------------------------|---------------------|-------------|--------|
| Ash El (`ashel`) | The Creator / Protagonist — acoustic-electric folk instrument (`charango`/guitar), feather in locs, green bead necklaces | Terracotta `#E07A5F` & Indigo vertical stripes + botanical leaf line-art | `neutral`, `focused`, `alarmed`, `hurt`, `determined`, `proud` |  Rustic line-art & watercolor live |
| Lay-Lay (`laylay`) | The Administrator / Antagonist — glass apothecary potion vials, dried herb bundles, multisig key & ledger tablet | Alchemical Violet `#9B7EDE` & Herbal Sage `#528C6E` interlocking key-fret pattern | `neutral`, `calculating`, `smirk`, `defensive`, `stern`, `alarmed` |  Rustic line-art & watercolor live |
| Xochtl (`xochtl`) | The Co-Creator / Shaman — steaming ceremonial cacao cup, beaded headband, red/black ceremonial face paint stripes, beaded fringe earrings | Cacao Turquoise `#2EC4B6` & Bronze `#8C533E` rainbow-earth woven huipil + zig-zag cuffs | `neutral`, `warm`, `focused`, `stern`, `hurt`, `proud` |  Rustic line-art & watercolor live |

### Ensemble / Legacy Cast Sprites (560×880)

| Character | Expressions | Status |
|-----------|-------------|--------|
| Maya | `neutral`, `focused`, `tired`, `proud`, `alarmed` |  Live in `game/images/` |
| Jordan | `neutral`, `hyped`, `hurt`, `determined`, `exhausted` |  Live in `game/images/` |
| Alex | `neutral`, `smirk`, `calculating`, `defensive`, `sincere` |  Live in `game/images/` |
| Vera | `neutral`, `wry`, `stern`, `warm` |  Live in `game/images/` |
| Spectre | `neutral`, `typing`, `alert`, `vulnerable` |  Live in `game/images/` |
| Atlas | `neutral`, `generous`, `guarded`, `predatory` |  Live in `game/images/` |

### Backgrounds (1920×1080 — Flat High-Contrast & Analog Watercolor Textures)

| BG | Used in | Visual Description | Status |
|----|---------|--------------------|--------|
| `bg constellation` | World Overview | Matte charcoal ink star-chart with organic root-circuit tendrils & glowing constellation nodes (inspired by *The First Constellation*) |  Rustic line-art & analog texture live |
| `bg sanctuary` | Ep 1, Ep 3 | Warm flat sunlit ochre wall, wooden beam shelf, vine plant, woven indigo rug, herbs & instruments (inspired by *Efam DAO Esphera*) |  Rustic line-art & analog texture live |
| `bg treasury_fire` | Cold Open Hooks & Bad Endings | High-contrast crimson & charcoal ink wash with fractured ledger lines and burning embers |  Rustic line-art & analog texture live |
| `bg cacao_circle` | Ep 2 (Lisbon), Ep 3 | Ceremonial cacao table with steaming cups, woven textiles, candle glow, and Lisbon presentation stage |  Rustic line-art & analog texture live |
| `bg apothecary` | Ep 1, Ep 4 (Lay-Lay POV) | Herbal apothecary shelves with potion bottles, dried sage bundles, and a high-contrast hardware wallet signing desk |  Rustic line-art & analog texture live |
| `bg coworking` … `bg signing` | Ensemble & Legacy Chapters | Studio, Discord, Conference, Apartment, Blockchain, Rooftop, Signing, Faction Map |  Live in `game/images/` |

---
