---
status: draft
tags: [overview, systems]
---

# Game Systems

## 1. World Overview: The First Constellation (`game/constellation.rpy`)

When a player starts the game, they enter **The First Constellation**—an interactive star-map organized around the three core educational pillars:
- **Pillar I: Keys & Sovereignty** (*Crypto Basis & OpSec*)
- **Pillar II: Collaboration & Co-op** (*Winning Together vs. Gatekeeping*)
- **Pillar III: Make & Enforce Agreements** (*Law, Structure & Treasury*)

### Interactive Constellation Nodes
- Each playable episode orbits its pillar as an **animated, glowing constellation point**.
- **Click to Inspect:** Clicking a node opens the **Scenario Overview Modal**, showing:
  - The **"OMG Disaster" Hook** (the worst-case tragedy at the heart of the episode).
  - The **POV Protagonist** ([[Ash El]], [[Xochtl]], or [[Lay-Lay]]) and supporting cast.
  - The **3 Core Lessons** taught in the scenario (with live Codex unlock status).
  - Actions to **Keep Exploring** (close modal) or **Dive In & Rewind the Disaster** (start episode).

## 2. The Rewind & Checkpointed 3-Choice Loop (`game/episodes.rpy`)

To make sessions fast, gripping, and fun to experiment with:
1. **Worst-Case Scenario Cold Open:** Every episode begins at the height of the disaster (e.g., $60,000 lost to a wrong wallet address while Ash El is stranded in Brazil and Lay-Lay locks the multisig).
2. **The Rewind (`⏪`):** A visual and narrative rewind drops the player back in time before the catastrophe.
3. **Three Checkpointed Decisions (`D1 → D2 → D3`):**
   - **Wrong Choice → Instant Bad Ending + Lesson + Checkpoint Retry:** Picking a shortcut or trap immediately plays out the disaster, triggers the **Lesson Learned** popup (`call lesson(...)`), and presents the **Rewind Retry Modal** (`⏪ Rewind to Decision N`). Players retry *that exact choice* immediately without replaying earlier choices.
   - **Sovereign Choice → Payoff + Lesson + Advance:** Picking the wise path plays out the cooperative/sovereign solution, unlocks the **Lesson Learned** popup, adjusts collective stats, and moves to the next decision.
4. **Episode Complete:** Resolving all 3 decisions heals the timeline, marks the episode star as **★ RESOLVED** in `persistent.episodes_completed`, and returns to the Constellation Map.

## 3. Core Stats & Relationships

| Stat | Start | Range | Meaning |
|------|-------|-------|---------|
| **Vibes** | 50 | 0–100 | Community trust, cultural energy, shared alignment |
| **Treasury** | 100 | 0–200 | Collective funds in ETH / stablecoin equivalents |
| **Security** | 40 | 0–100 | Key sovereignty, multi-sig hygiene, and legal armor |
| **Morale** | 60 | 0–100 | Co-creator solidarity between Ash El, Xochtl, and the team |
| **Burnout** | 10 | 0–100 | Creator exhaustion (high is dangerous) |

## 4. Lesson Learned Popups & Collectible Glossary

- **21 Lesson Learned Popups (`game/lessons.rpy`):** Every decision teaches a documented real-world failure mode with (1) the core principle, and (2) the historical case study + real numbers.
- **Collectible Glossary (`game/glossary.rpy`):** ~98 terms across five tabs (`BUSINESS`, `CRYPTO`, `MONEY`, `DAO`, `STATS`). Yellow underlined words in dialogue open their definition on click and unlock persistently across runs.
- **Plain Mode (`game/tl/plain/`):** Optional B1-level plain English mode selectable at start or in Preferences.
