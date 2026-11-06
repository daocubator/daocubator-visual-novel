# Lesson Learned popups + Codex
# vault: 05 Lessons/* — one LESSONS entry per lesson note; ids = note slugs

define LESSONS = {
    "no_keys_no_cheese": (
        "NO KEYS, NO CHEESE: SOVEREIGNTY & KEY ROTATION",
        "If someone else holds your keys 'for convenience,' they hold your agency — and if a key touches a text file, rotate it immediately.",
        "Essential Food & Medicine / Brazil Stranding: when administrators held all the multisig keys, creators on the ground were left stranded waiting for payout. On chains like NEAR, native key rotation and a 2-of-3 multisig let you revoke a leaked private key without giving up sovereignty.",
    ),
    "vetting_admins": (
        "TRUST, BUT VERIFY: VETTING DAO ADMINISTRATORS",
        "Never vote a stranger onto your multisig or treasury council on 'good vibes' alone — verify their history and scope their permissions first.",
        "Build Finance & Wonderland (2022): unvetted treasury administrators with past drained projects were handed signing power on a vibe check, leading to insider drains. Always run due diligence on past DAOs and require a 90-day scoped contributor agreement.",
    ),
    "test_transaction": (
        "THE $1 TEST TRANSACTION RULE",
        "Measure twice, cut once: always send a $1 test transaction and confirm receipt before wiring the real treasury.",
        "The $60,000 Wrong-Address Disaster: a rushed $60,000 transfer was sent to a clipped wallet address, followed by days weeping on forums begging for a 'refund.' Blockchains have no undo button. A $1 test transfer confirmed by the recipient saves the other $59,999.",
    ),
    "creator_vs_admin": (
        "CREATOR VS. ADMINISTRATOR GATEKEEPING",
        "When non-creators hold unilateral payout power over creators, admiration can curdle into jealousy and gatekeeping.",
        "The Lisbon Showcase ('Amy & Edward'): an administrator froze a star creator's game payout out of jealousy right before Lisbon. When teammate 'Jena' covertly submitted the exact same work under a different avatar, the admin approved it instantly. Separate admin ops from subjective creative veto.",
    ),
    "coop_solidarity": (
        "CO-OP SOLIDARITY: WINNING TOGETHER",
        "A true cooperative wins together by sharing both the shield and the harvest — not by pitting solo stars against solo bosses.",
        "A century of cooperative governance shows that collectives survive when creators back each other up with peer validation, objective milestone escrow, and rotating stewardship rather than burning out in isolation.",
    ),
    "agreements_law": (
        "MAKE & ENFORCE AGREEMENTS",
        "Counter-culture values and fast innovation are no substitute for written agreements, clear deliverables, and legal armor.",
        "Handshakes feel spiritual on day one and turn into lawsuits by day ninety. Even decentralized collectives need written vesting cliffs, clear deliverable contracts, and a legal wrapper so one bad breakup doesn't sink the sanctuary.",
    ),
    "equal_split": (
        "THE EQUAL SPLIT TRAP",
        "Equal splits are chosen to avoid a conversation, not to be fair.",
        "73% of startups split equity within the first month of founding. Teams that default to an equal split are ~3x more likely to be unhappy with it later. (Wasserman, 'The Founder's Dilemmas')",
    ),
    "vesting": (
        "VESTING & DEAD EQUITY",
        "Always vesting. Always a cliff. Always a lawyer on the founder agreement.",
        "A co-founder who leaves in month 9 without vesting keeps everything — 'dead equity' that kills investor interest or costs a treasury-sized buyout. Standard fix: 4-year vesting, 1-year cliff. Bonus trap: miss the 30-day IRS 83(b) window and get taxed on paper gains forever.",
    ),
    "partnership": (
        "THE PARTNERSHIP TRAP",
        "If your DAO has no legal wrapper, YOU are the legal wrapper.",
        "CFTC v. Ooki DAO: an unincorporated DAO was ruled a general partnership — members were served through the website's help chat box. Default judgment: $634,542 penalty. Sarcuni v. bZx reached the same theory. A ~$15k legal wrapper is cheap insurance.",
    ),
    "death_spiral": (
        "TREASURY DEATH SPIRAL",
        "A treasury that's 90% your own token is a bet that you'll never have a bad month.",
        "When trouble hits, the native token crashes exactly when cash is needed; selling to raise cash crashes it further. Research fix: the barbell — keep 30–50% in uncorrelated stables and pay the boring swap fees.",
    ),
    "recoupment": (
        "PREDATORY RECOUPMENT",
        "An advance is a loan you repay at 10–20 cents on the dollar.",
        "360 deals take cuts of touring and merch the label didn't build. Cross-collateralization ties Album A's debt to Album B's profits — a permanent debt trap dressed as support.",
    ),
    "chargeback": (
        "CHARGEBACK DEATH SPIRAL",
        "Your payment processor is a partner with a 1% tolerance for your mistakes.",
        "Past roughly a 1% chargeback rate, Stripe/PayPal freeze or terminate the account — locking the WHOLE treasury, not just disputed orders. Proactive refunds beat fighting disputes.",
    ),
    "overfunding": (
        "THE OVERFUNDING PARADOX",
        "Overfunding isn't free money — it's unplanned scale on a fixed-price promise.",
        "Coolest Cooler (2014): $50k goal, $13.2M raised, 62,000 backers at $185 — below true at-scale unit cost. Sold at retail for $499 before fulfilling backers. Bankruptcy; 20,000+ backers never got one.",
    ),
    "apathy": (
        "VOTER APATHY & DELEGATION",
        "A governance system nobody uses is an attack surface, not a democracy.",
        "Average DAO turnout: ~6.3%. The usual fix, delegation, quietly re-centralizes: the top 10% of voters ends up controlling up to 76.2% of voting power — a board of directors with no fiduciary duty.",
    ),
    "capture": (
        "GOVERNANCE CAPTURE",
        "If votes can be bought, someone is pricing your treasury.",
        "Build Finance DAO (2022): an attacker accumulated tokens, passed a malicious mint on a low-turnout retry, minted 1B+ tokens and drained ~160 ETH (~$470k). Capture doesn't look like a heist. It looks like help.",
    ),
    "flashloan": (
        "FLASH LOANS & TIME-LOCKS",
        "Any governance path that executes instantly will eventually execute an attack instantly.",
        "Beanstalk (2022, $181M): a flash-borrowed voting supermajority passed a Trojan proposal and executed it in the same transaction via an emergency path — paired with a charity proposal as the distraction. A non-zero delay between vote and execution would have stopped it cold.",
    ),
    "credentials": (
        "CREDENTIAL HYGIENE",
        "A seed phrase in a shared doc is already stolen — you just don't know by whom yet.",
        "8ight Finance lost $1.75M after private keys were pasted into a shared Google Doc and sent over Facebook group chat. Keep 5–10% max in hot wallets; multi-sig cold storage above ~$10k.",
    ),
    "verify_hex": (
        "VERIFY THE HEX",
        "The hardware wallet's ugly little screen is the only screen that isn't lying to you.",
        "Nexus Mutual's founder lost $8M (370,000 NXM) in Dec 2020 to a compromised MetaMask that spoofed the transaction summary. The true destination was on the hardware wallet screen the whole time — unchecked.",
    ),
    "ice_phishing": (
        "ICE PHISHING",
        "Your front end is part of your smart contract.",
        "Badger DAO (2021, $121M): a stolen Cloudflare API key let attackers inject a script into the site that harvested token approvals from users. No contract bug required. DNS, CDN and API keys are security boundaries.",
    ),
    "burnout": (
        "BURNOUT & IDENTITY FUSION",
        "You are not the venture. If it must die, it should not take you with it.",
        "Solopreneur failure research: identity-venture fusion turns stagnation into personal failure and blocks rational pivots. Exhaustion measurably degrades decisions — which is why this game's hints stop being trustworthy when your Burnout is high.",
    ),
    "greenwash": (
        "THE GREENWASHING TRAP",
        "Verify the physical asset before you financialize it.",
        "KlimaDAO/Toucan: 'sweeping the floor' of cheap carbon credits revived worthless legacy offsets (2011-era hydro dams). Scientists and registries disavowed the pools; price and trust collapsed together.",
    ),
}

default persistent.lessons_unlocked = set()

screen lesson_popup(lid):
    modal True
    zorder 100
    add "#0d0c0ae6"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1240
        background Frame("gui/frame.png", gui.frame_borders)
        padding (48, 38)
        vbox:
            spacing 18
            text "✦ CRYPTO-ETHICS & CO-OP LESSON UNLOCKED ✦" color "#E8C574" size 30 xalign 0.5
            text LESSONS[lid][0] color "#E07A5F" size 32 xalign 0.5
            null height 4
            ## __() translates first (plain mode), then terms get glossary links.
            text gloss_say_filter(__(LESSONS[lid][1])) color "#F4EFE6" size 26
            text gloss_say_filter(__(LESSONS[lid][2])) color "#B8B0A4" size 22
            null height 12
            textbutton "▶ CONTINUE" action Return() xalign 0.5 text_color "#528C6E" text_hover_color "#E8C574"

label lesson(lid):
    $ codex_seen.add(lid)
    if persistent.lessons_unlocked is None:
        $ persistent.lessons_unlocked = set()
    $ persistent.lessons_unlocked.add(lid)
    $ gloss_unlock_text(__(LESSONS[lid][1]), __(LESSONS[lid][2]))
    call screen lesson_popup(lid)
    return
