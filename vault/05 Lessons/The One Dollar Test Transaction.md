---
status: draft
tags: [lesson]
category: opsec
appears_in: "Ep1.3"
---

# The One Dollar Test Transaction

**Principle (popup line 1):** Measure twice, cut once: always send a $1 test transaction and confirm receipt before wiring the real treasury.
**Failure mode:** Rushing a massive transfer under time pressure, copy-pasting a truncated or poisoned wallet address, and blasting the entire treasury in a single irreversible transaction.
**Real case:** **The $60,000 Wrong-Address Disaster** — A collective member rushed a $60,000 transfer to the wrong wallet address and spent days weeping on forums begging for a "refund" as if a blockchain were a traditional bank. On-chain transfers have no customer service desk and no undo button.
**Mitigation:** Send a $1 (or 0.001 ETH / 1 USDC) test transaction first, wait for the human recipient on the other end to confirm it arrived in their live wallet, verify the first and last 6 characters of the address on a hardware screen, and only then send the bulk amount.
**In the game:** Episode 1, Decision 3 — Under deadline pressure to fund the Brazil sanctuary trip, Lay-Lay pastes an address with a clipped character. Sending the full $60,000 at once vaporizes the funds forever; sending a $1 test transaction first catches the dead address and saves $59,999.
