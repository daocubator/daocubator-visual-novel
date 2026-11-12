---
status: draft
tags: [lesson]
category: opsec
appears_in: "Ep1.1"
---

# No Keys, No Cheese (Sovereignty and Key Rotation)

**Principle (popup line 1):** If someone else holds your keys "for convenience," they hold your agency—and if a key touches a text file, rotate it immediately.
**Failure mode:** Two compounding mistakes: (1) storing private keys or seed phrases in unencrypted text files or shared docs where bots and insiders can scrape them, and (2) handing sole custodial control of a DAO treasury to a single administrator because creators "don't want to deal with tech."
**Real case:** **Essential Food & Medicine / Brazil & South Dakota Sanctions & 8ight Finance ($1.75M)** — Creators on the ground were left stranded waiting for payouts while administrators who held all the multi-sig keys froze or misdirected funds. Meanwhile, projects that left keys in plaintext files had treasuries swept in minutes. On account-model chains like NEAR Protocol, native access-key rotation and multi-sig threshold wallets let collectives revoke a leaked key without losing the account or handing custody to a single boss.
**Mitigation:** Never surrender custody to a solo admin; use a threshold multi-sig (e.g. 2-of-3 across creator, co-creator, and admin hardware wallets) and immediately rotate access keys on-chain the moment any key is exposed.
**In the game:** Episode 1, Decision 1 — After a backup key is pasted into a shared text file, Clara offers to hold sole custody on her laptop. Choosing convenience triggers the "No Keys, No Cheese" lockout; rotating the account keys and enforcing a 2-of-3 co-op multisig saves the treasury.
