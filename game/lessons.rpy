# Lesson Learned popups + Codex (Easy-to-understand plain English)
# vault: 05 Lessons/* — one LESSONS entry per lesson note; ids = note slugs

define LESSONS = {
    "no_keys_no_cheese": (
        "No keys, no cheese: sovereignty & key rotation",
        "If someone else holds your keys 'for convenience,' they control your money — and if a secret key ever touches a shared text file, replace it immediately.",
        "In the real-world Brazil Sanctuary stranding, administrators held all the wallet keys while creators on the ground were left waiting for funds. On blockchains like NEAR, key rotation and a 2-of-3 multisig (where two out of three partners must approve every payment) let you cancel a leaked private key without giving up shared control.",
    ),
    "vetting_admins": (
        "Trust, but verify: vetting DAO administrators",
        "Never vote a stranger onto your shared wallet or treasury council on 'good vibes' alone — check their past projects and limit their permissions first.",
        "Build Finance & Wonderland (2022): unvetted treasury administrators with histories of drained projects were handed signing power based on charm and hype, leading to insider thefts. Always run due diligence on a newcomer's past DAOs and start with limited, revocable permissions.",
    ),
    "test_transaction": (
        "The $1 test transaction rule",
        "Measure twice, cut once: always send a $1 test transaction and confirm it arrived before wiring the rest of the treasury.",
        "The $60,000 Wrong-Address Disaster: a rushed $60,000 transfer was sent to a fake lookalike wallet address, followed by days of begging online forums for a refund. Blockchains have no undo button. Sending a $1 test transfer and confirming on video with the recipient saves the other $59,999.",
    ),
    "creator_vs_admin": (
        "Creator vs. administrator gatekeeping",
        "When administrators have the power to block payouts on a whim, initial admiration for creators can curdle into jealousy and gatekeeping.",
        "The Lisbon Showcase ('Amy & Edward'): an administrator froze a lead creator's game payout out of jealousy right before the event. When teammate 'Jena' quietly submitted the exact same file under a different username, the admin approved it immediately. Lock creative payouts in objective milestone escrow so personal ego cannot freeze completed work.",
    ),
    "coop_solidarity": (
        "Co-op solidarity: winning together",
        "A true cooperative wins together by backing each other up with clear rules and shared power — not by pitting solo stars against solo bosses.",
        "A century of cooperative history shows that creative groups survive when members protect each other with peer review, objective escrow, and rotating leadership instead of fighting alone.",
    ),
    "agreements_law": (
        "Make & enforce agreements",
        "Counter-culture values and fast innovation are no substitute for written agreements, clear deliverables, and real legal protection.",
        "Handshakes feel warm on day one and turn into lawsuits by day ninety. Even decentralized groups need written vesting cliffs, clear deliverable contracts, and a legal wrapper so one bad breakup doesn't sink the whole sanctuary.",
    ),
    "equal_split": (
        "The equal split trap",
        "People often choose an equal split to avoid a hard conversation, not because it is fair.",
        "73 percent of startups split equity in the first month. Equity means who owns how much of the company. Teams that default to an equal split without talking through each person's role are about 3 times more likely to be unhappy later. (Source: Wasserman, 'The Founder's Dilemmas')",
    ),
    "vesting": (
        "Vesting & dead equity",
        "Always use vesting. Always have a cliff. Always put the founder agreement in writing.",
        "Vesting means you earn your shares or tokens slowly over time. Without it, a co-founder who quits in month two keeps everything. That is 'dead equity': it scares away supporters or lets an early quitter dump tokens on the team still working. The standard fix is 4-year vesting with a 1-year cliff: leave before one year and you get nothing.",
    ),
    "partnership": (
        "The partnership trap",
        "If your DAO has no legal wrapper, YOU are the legal wrapper — and you are personally responsible.",
        "In CFTC v. Ooki DAO, a court ruled that a DAO with no registered legal company form was a general partnership. That means every participating member can be held personally responsible for all debts and lawsuits. A formal legal wrapper (like a Co-op LLC or Swiss Verein) shields individual members' homes and bank accounts.",
    ),
    "death_spiral": (
        "Treasury death spiral",
        "If 90 percent of your treasury is your own token, you are betting you will never have a bad month.",
        "When trouble comes, your native token crashes right when you need cash. Selling it to pay bills makes the price fall even faster. The fix is a barbell strategy: keep 30–50 percent of your treasury in stablecoins (like USDC) that stay worth $1 even when the market dips.",
    ),
    "recoupment": (
        "Predatory recoupment",
        "An advance is a loan — and under bad terms, only 10–20 cents of every dollar you earn goes toward paying it back.",
        "A 360 deal lets a label take a cut of your touring and merch, even though they didn't build them. Cross-collateralization links Album A's debt to Album B's profits so the creator stays in debt forever. Always put fair, transparent recoupment rules in your charter so creators get paid back cleanly.",
    ),
    "chargeback": (
        "Chargeback death spiral",
        "Your payment processor is a partner that accepts only about 1 percent of disputed orders.",
        "A chargeback is when a buyer asks their bank to reverse a card payment. Above about a 1 percent chargeback rate, processors like Stripe or PayPal can freeze your entire account — locking all your money, not just the disputed orders. Giving proactive refunds beats fighting disputes.",
    ),
    "overfunding": (
        "The overfunding paradox",
        "Overfunding is not free money — it is growth you didn't plan for on a fixed-price promise.",
        "Coolest Cooler (2014) asked for $50k and raised $13.2M from 62,000 backers at $185 each — less than the real unit cost to build and ship at that scale. The company went bankrupt, and more than 20,000 backers never received their cooler.",
    ),
    "apathy": (
        "Voter apathy & delegation",
        "A governance system that nobody uses is not a democracy — it is a weak spot that attackers can exploit.",
        "Average DAO voter turnout is only about 6.3 percent. The usual fix is delegation: giving your voting power to someone you trust. Done carelessly, power quietly collects in a few hands, where the top 10 percent of voters control over 75 percent of the votes.",
    ),
    "capture": (
        "Governance capture",
        "If votes can be bought without limits, someone is already working out the price of your treasury.",
        "Build Finance DAO (2022): an attacker quietly collected tokens, passed a harmful proposal when few members were watching, minted over 1 billion new tokens, and drained the treasury (~$470k). Governance capture rarely looks like a robbery at first — it looks like a wealthy investor offering help.",
    ),
    "flashloan": (
        "Flash loans & time-locks",
        "If a governance vote can execute in the same second it passes, one day an attack will execute in the same second too.",
        "Beanstalk (2022, $181M): an attacker used a flash loan — a huge loan borrowed and repaid inside a single transaction — to rent most of the voting power for a few seconds and drain the treasury immediately. A 24–48 hour time-lock delay between a vote passing and the money moving stops flash-loan governance attacks cold.",
    ),
    "credentials": (
        "Credential hygiene",
        "A seed phrase in a shared document is already stolen — you just don't know who has it yet.",
        "8ight Finance lost $1.75M after private keys were pasted into a shared Google Doc and sent over group chat. Keep only 5–10 percent at most in online hot wallets; store treasury funds in offline hardware wallets and a multi-sig.",
    ),
    "verify_hex": (
        "Verify the hex",
        "The small screen on your hardware wallet is the only screen you can trust when signing.",
        "In December 2020, Nexus Mutual's founder lost $8M when a hacked browser wallet showed a fake, friendly transaction summary on the computer monitor. The real, malicious action was visible on the hardware wallet's tiny raw-data (hex) screen the whole time — unchecked.",
    ),
    "ice_phishing": (
        "Ice phishing",
        "Your website (front end) is part of your smart contract's security.",
        "Badger DAO (2021, $121M): attackers stole a Cloudflare CDN key and added a hidden script to the website that tricked users into signing unlimited token approvals. There was no bug in the smart contract itself — protect your website keys just like your wallet keys.",
    ),
    "burnout": (
        "Burnout & sustainable co-ops",
        "You are not the venture. When one person tries to carry creation, administration, and crisis response alone, everyone loses.",
        "Research on founders shows that deep exhaustion ruins decision-making and turns small setbacks into total collapse. Healthy cooperatives prevent burnout by rotating administrative duties, sharing the workload, and building funded rest into every major sprint.",
    ),
    "greenwash": (
        "The greenwashing trap",
        "Verify the real-world project before you turn it into a token — otherwise you risk greenwashing.",
        "KlimaDAO and Toucan bought up the cheapest carbon credits on the market ('sweeping the floor'), which revived old, worthless offsets from 2011-era hydro dams. When scientists and registries rejected those credits, both the token price and community trust collapsed.",
    ),
}

default persistent.lessons_unlocked = set()

screen lesson_popup(lid):
    modal True
    zorder 100
    add "#140702E0"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1240
        background Frame("gui/frame.png", gui.frame_borders)
        padding (48, 38)
        vbox:
            spacing 16
            text "CRYPTO-ETHICS & CO-OP LESSON UNLOCKED" font gui.mono_font kerning 3.2 color "#B87444" size 16 xalign 0.5
            text LESSONS[lid][0] font gui.serif_font axis {"weight": 300, "opticalsize": 48} color "#EED4B4" size 38 xalign 0.5
            null height 4
            frame:
                xfill True
                background "#241309"
                padding (24, 18)
                text gloss_say_filter(LESSONS[lid][1]) font gui.serif_font axis {"weight": 300, "opticalsize": 36} color "#EED4B4" size 26 line_spacing 6
            text gloss_say_filter(LESSONS[lid][2]) font gui.sans_font color "#DDBCAD" size 21 line_spacing 5
            null height 8
            textbutton "CONTINUE ›" action Return() xalign 0.5 style "constellation_confirm_btn"

label lesson(lid):
    $ codex_seen.add(lid)
    if persistent.lessons_unlocked is None:
        $ persistent.lessons_unlocked = set()
    $ persistent.lessons_unlocked.add(lid)
    $ gloss_unlock_text(LESSONS[lid][1], LESSONS[lid][2])
    call screen lesson_popup(lid)
    return
