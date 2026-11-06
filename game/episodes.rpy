# Episodic Micro-Dramas — Worst-Case Hook -> Rewind -> 3 Checkpointed Decisions
# vault: 01 Overview/Story Structure.md · 02 Characters/Ash El.md · Lay-Lay.md · Xochtl.md · 05 Lessons/*

################################################################################
## Rewind & Checkpoint Retry Screens and Helpers

screen rewind_overlay(headline="⏪ REWINDING TIMELINE", subline="Dropping back before the disaster..."):
    modal True
    zorder 180
    add "#0D0B09EE"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1280
        background "#1E1915"
        padding (56, 44)
        at rewind_banner_flash
        vbox:
            spacing 18
            xalign 0.5
            text "[headline]" color "#2EC4B6" size 44 xalign 0.5
            text "[subline]" color "#F4EFE6" size 26 xalign 0.5
            null height 8
            text "Change the structure. Protect the keys. Save the collective." color "#F2CC8F" size 21 xalign 0.5
            null height 10
            textbutton "⏪ STEP INTO THE PAST" action Return() style "constellation_confirm_btn" xalign 0.5


label trigger_rewind(headline="⏪ REWINDING TIMELINE", subline="Dropping back before the disaster..."):
    call screen rewind_overlay(headline=headline, subline=subline)
    return


screen bad_ending_rewind_modal(failure_title, failure_summary, lesson_id):
    modal True
    zorder 190
    $ ldata = get_lesson_meta(lesson_id)

    add "#120808EE"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1380
        background "#1F1413"
        padding (48, 38)

        vbox:
            spacing 18
            hbox:
                xfill True
                text "💥 BAD ENDING — TIMELINE COLLAPSED" color "#E07A5F" size 26
                text "[ldata['number']] · [ldata['category']]" color "#F2CC8F" size 22 xalign 1.0

            text "[failure_title]" color "#F4EFE6" size 38
            text "[failure_summary]" color "#E8E2D9" size 23

            frame:
                xfill True
                background "#161210"
                padding (26, 20)
                vbox:
                    spacing 8
                    text "✦ CRYPTO-ETHICS TAKEAWAY: [ldata['title']]" color "#2EC4B6" size 22
                    text "[ldata['body']]" color "#D8D0C5" size 20
                    text "{i}Real-world receipt: [ldata['real_world']]{/i}" color "#BEB5A7" size 18

            null height 8

            hbox:
                spacing 32
                xalign 0.5
                textbutton "⏪ REWIND TO THIS DECISION (INSTANT RETRY)" action Return("retry") style "constellation_confirm_btn"
                textbutton "✦ RETURN TO CONSTELLATION MAP" action Return("map") style "constellation_cancel_btn"


label checkpoint_bad_end(retry_label, failure_title, failure_summary, lesson_id):
    call lesson(lesson_id)
    call screen bad_ending_rewind_modal(failure_title, failure_summary, lesson_id)
    if _return == "map":
        jump world_overview
    $ renpy.jump(retry_label)
    return


screen episode_complete_modal(ep_id, summary_text):
    modal True
    zorder 190
    $ ep = EPISODES[ep_id]

    add "#0B110FEE"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1380
        background "#17211E"
        padding (48, 38)

        vbox:
            spacing 18
            hbox:
                xfill True
                text "✓ DISASTER AVERTED — TIMELINE RESTORED" color "#52B788" size 26
                text "[ep['num']] · [ep['pillar_short']]" color "#F2CC8F" size 22 xalign 1.0

            text "[ep['title']] — Resolved" color "#F4EFE6" size 40
            text "[summary_text]" color "#E8E2D9" size 23

            frame:
                xfill True
                background "#121917"
                padding (26, 20)
                vbox:
                    spacing 10
                    text "✦ LESSONS MASTERED IN THIS EPISODE:" color "#2EC4B6" size 22
                    for lid in ep["lessons"]:
                        $ ldata = get_lesson_meta(lid)
                        text "★ [ldata['number']] — [ldata['title']]: [ldata['body']]" color "#D8D0C5" size 19

            null height 10

            hbox:
                spacing 32
                xalign 0.5
                textbutton "✦ RETURN TO WORLD OVERVIEW CONSTELLATION" action Return("map") style "constellation_confirm_btn"
                textbutton "📖 OPEN LESSONS CODEX" action [ShowMenu("lessons_codex"), Return("map")] style "constellation_cancel_btn"


label complete_episode(ep_id, summary_text):
    python:
        if persistent.episodes_completed is None:
            persistent.episodes_completed = set()
        persistent.episodes_completed.add(ep_id)
        for lid in EPISODES[ep_id]["lessons"]:
            if persistent.lessons_unlocked is None:
                persistent.lessons_unlocked = set()
            persistent.lessons_unlocked.add(lid)
        renpy.save_persistent()
    call screen episode_complete_modal(ep_id, summary_text)
    jump world_overview


################################################################################
## EPISODE 1: "NO KEYS, NO CHEESE"
## Pillar I: Keys & Sovereignty (Crypto Basis)
## POV: Ash El (The Creator — Acoustic-Electric Folk Instrument)
## Lessons: no_keys_no_cheese, vetting_admins, test_transaction
################################################################################

label ep1_keys:
    $ current_episode = "ep1_keys"
    $ current_pov = "Ash El (The Creator)"
    $ vibes = 35
    $ treasury = 60
    $ security = 25
    $ morale = 40
    $ burnout = 30
    show screen stats_hud

    ## --- THE HOOK: WORST-CASE SCENARIO (IN MEDIA RES) ---
    scene bg treasury_fire with fade
    show ashel alarmed at left
    show laylay stern at right
    show xochtl hurt at center

    narrator "{color=#FF6B6B}WORST-CASE OUTCOME — LISBON TERMINAL, 11:42 P.M.{/color}"
    narrator "Twelve crates of pressed botanical juices sit impounded behind customs glass. Rain streaks the terminal window. On your phone, the Essential Food & Medicine DAO treasury reads {b}0.00 NEAR{/b}."
    ashel "Sixty thousand dollars, Lay-Lay! Every festival set I played, every bottle of cold-pressed medicine we sold, every grant Xochtl and I bled for — gone in one transaction?!"
    laylay "Lower your voice, Ash El. I copied the Brazil sanctuary address from the thread as fast as I could. How was I supposed to know the middle digits were poisoned?"
    xochtl "You didn't send a single dollar first to check if my ceremonial cacao cooperative received it. You rushed all sixty thousand into the void."
    ashel "Then sign the emergency recovery reserve so we can at least pay the freight handlers and get the team home!"
    laylay "I can't. The backup admin we voted in last week already revoked the recovery pool — and I hold the only remaining admin key on the main vault. You wanted me to 'handle the boring wallet stuff,' remember?"
    xochtl "We gave away our keys. We let a stranger into the council without checking his past. And we wired sixty thousand dollars blind."
    narrator "In the Discord forum, someone is already typing in all-caps to blockchain validators, weeping and begging for a 'bank reversal' that does not exist in a trustless ledger."

    ## --- THE REWIND ---
    call trigger_rewind(
        headline="⏪ REWINDING 14 DAYS EARLIER",
        subline="POV: Ash El · Essential Food & Medicine Sanctuary Studio"
    )

    scene bg sanctuary with fade
    $ vibes = 65
    $ treasury = 120
    $ security = 45
    $ morale = 75
    $ burnout = 15

    show ashel neutral at left
    show xochtl warm at center
    show laylay smirk at right

    narrator "Fourteen days before the flight. Sunlight filters through dried calendula bundles and acoustic guitar cases in the sanctuary studio."
    narrator "You are {b}Ash El{/b}. Your fingers still hum from recording the dawn folk-dub session, and forty crates of fresh herbal elixirs are ready for the community tour."
    xochtl "Drink your cacao while it's warm, Ash. Before we book the Brazil sanctuary freight, look at the laptop."
    ashel "What am I looking at?"
    xochtl "Someone uploaded a plaintext file named {b}dao_seed_keys_FINAL.txt{/b} into our public Google Drive press-kit folder last night. Two scraper bots already indexed the folder."
    laylay "Ugh, key management is such a headache for artists. Look, Ash — you make the music and the juices. Just transfer the treasury into my personal hardware wallet. I'll be sole custodian and pay invoices for you."

    ## --- DECISION 1: KEY ROTATION & SOVEREIGNTY ---
label ep1_d1:
    scene bg sanctuary
    show ashel determined at left
    show xochtl neutral at center
    show laylay smirk at right

    narrator "{color=#F2CC8F}DECISION 1 OF 3 — THE LEAKED KEYS & THE CUSTODY TRAP{/color}"
    narrator "A plaintext seed file was exposed in a shared cloud folder, and Lay-Lay is offering to hold 100%% of the funds in her personal wallet so you 'don't have to worry about crypto.'"

    menu:
        "Perform NEAR account key rotation immediately and move the treasury into a 2-of-3 non-custodial DAO multisig (Ash El, Xochtl, Lay-Lay).":
            $ adjust(security=+25, morale=+10, vibes=+5)
            ashel "No. 'No keys, no cheese.' If the creators who build the value don't hold signing sovereignty, we aren't a cooperative — we're employees waiting for permission."
            xochtl "Agreed. On NEAR, we can perform an on-chain {b}key rotation{/b} right now — deleting the leaked full-access key and replacing it with fresh hardware keys in a 2-of-3 {b}non-custodial{/b} {b}multisig{/b}."
            laylay "Fine, fine! Two-of-three it is. Though you're making me do three times the paperwork."
            call lesson("no_keys_no_cheese")

        "Let Lay-Lay hold all the keys in her personal wallet — you're an artist, not a sysadmin.":
            $ adjust(security=-30, morale=-25)
            scene bg treasury_fire with vpunch
            show ashel hurt at left
            show laylay stern at right
            ashel "You're right, Lay-Lay. Take the keys so I can finish mixing the album."
            narrator "Three weeks later, while you're stranded on tour waiting for travel reimbursement, Lay-Lay decides your stage budget is 'unnecessary' and redirects the treasury into her own consulting stipend."
            laylay "My keys, my treasury priorities, Ash. You don't even have a signer slot to propose a vote."
            call checkpoint_bad_end(
                "ep1_d1",
                "Custodial Lockout: 'No Keys, No Cheese'",
                "By handing sole custody of the treasury to an administrator, Ash El surrendered all on-chain sovereignty. When conflict arose, the creators who generated 100% of the DAO's value were locked out of their own funds.",
                "no_keys_no_cheese"
            )

        "Keep the leaked keys in the text file — just rename it to 'recipes_backup.txt' so hackers won't notice.":
            $ adjust(security=-40, treasury=-100)
            scene bg treasury_fire with vpunch
            show ashel alarmed at left
            show xochtl hurt at center
            ashel "Let's just rename the file in Google Drive. Nobody's going to open 'recipes_backup.txt'."
            narrator "Automated sweeper bots don't read filenames — they regex-scan every file for 12-word BIP-39 entropy and Ed25519 private keys. Eleven minutes later, the treasury is swept to Tornado Cash."
            call checkpoint_bad_end(
                "ep1_d1",
                "Plaintext Key Compromise",
                "Private keys stored in cloud text files are harvested automatically by bots within minutes. Once a key is exposed, renaming the file does nothing — only on-chain key rotation or migrating to a fresh multisig saves the funds.",
                "no_keys_no_cheese"
            )

    ## --- DECISION 2: TRUST & VETTING NEW DAO ADMINISTRATORS ---
label ep1_d2:
    scene bg sanctuary with dissolve
    show ashel neutral at left
    show xochtl neutral at center
    show laylay neutral at right

    narrator "Five days later. The new 2-of-3 multisig is live, and the Brazil sanctuary harvest is Seller-confirmed."
    laylay "Since we're scaling fast, I invited a brilliant operations administrator I met at an afterparty — 'Kestrel.' He wants to join our DAO council today with full treasury proposal and execution rights."
    xochtl "Wait. Has anyone checked Kestrel's on-chain history or called the last two collectives he administrated?"
    laylay "Oh, don't be so paranoid, Xochtl! He wore a hand-woven poncho and talked about regenerative mycelial finance for two hours. Look, the council proposal to add his wallet is already queued."

    narrator "{color=#F2CC8F}DECISION 2 OF 3 — TRUST VS. VERIFICATION IN DAO GOVERNANCE{/color}"
    narrator "Lay-Lay wants you to co-sign Kestrel onto the DAO council with full administrative keys right now based on charisma and 'high vibes.'"

    menu:
        "Pause the vote: audit Kestrel's on-chain wallet history, call his past collectives, and grant only scoped trial permissions first.":
            $ adjust(security=+20, vibes=+5, morale=+10)
            ashel "Vibes are for jam sessions, not multisig keys. Let's look up his wallet on the block explorer and message his last DAO before we sign anything."
            xochtl "Look at this transaction graph... Kestrel's address drained a 40,000 USDC community grant from a solar cooperative in Tulum six months ago and ghosted."
            laylay "I... I had no idea. He sounded so aligned at the tea bar."
            ashel "That's why we verify first and scope permissions with function-call keys. Rejecting his council nomination now."
            call lesson("vetting_admins")

        "Sign Kestrel in with full admin keys immediately — questioning him would ruin the sacred trust of the collective.":
            $ adjust(security=-35, treasury=-80)
            scene bg treasury_fire with vpunch
            show ashel hurt at left
            show xochtl hurt at center
            ashel "We're building a trust-based family. I'll co-sign his full admin key."
            narrator "At 3:00 a.m. that Sunday, Kestrel uses his un-scoped council authority to push a batch payout to an offshore mixer and deletes his Telegram account."
            xochtl "Charisma is not an audit, Ash. On-chain permissions don't care how spiritual someone sounded at a party."
            call checkpoint_bad_end(
                "ep1_d2",
                "Unvetted Administrator Rug-Pull",
                "Voting a new administrator into a DAO multisig without auditing their on-chain history and scoping their permissions gave a serial grifter direct access to the community treasury.",
                "vetting_admins"
            )

        "DM Kestrel the backup treasury seed phrase for a '48-hour trial' so he can prove he's trustworthy.":
            $ adjust(security=-45, treasury=-100)
            scene bg treasury_fire with vpunch
            show ashel alarmed at left
            ashel "Here, Kestrel — take the backup seed phrase just for the weekend so we can see how you work."
            narrator "A seed phrase doesn't expire after 48 hours. Kestrel copies the 12 words, waits until the treasury tops up on Monday, and sweeps every token."
            call checkpoint_bad_end(
                "ep1_d2",
                "The 'Trial Seed Phrase' Fallacy",
                "You cannot give someone 'temporary' access to a raw seed phrase. Once shared, a private key is permanently compromised. Trial contributors must only receive revocable, allowance-capped function-call keys.",
                "vetting_admins"
            )

    ## --- DECISION 3: THE $60,000 TRANSFER & THE $1 TEST TRANSACTION ---
label ep1_d3:
    scene bg sanctuary with dissolve
    show ashel determined at left
    show xochtl warm at center
    show laylay neutral at right

    narrator "Departure afternoon. All sixty thousand dollars of community funds are safe in the 2-of-3 multisig. Now it's time to wire the $60,000 settlement to the Brazil sanctuary land trust so the cargo and flight clearances release."
    laylay "Hurry! The freight desk closes in twenty minutes. I pasted the sanctuary's wallet address into the multisig proposal for the full $60,000. Just click 'Approve & Broadcast' so we can run to the gate!"
    xochtl "Hold on. Where did you copy that address from, Lay-Lay?"
    laylay "From the forwarded message in our ops chat! Look, the first four characters match: {b}0x7F4c...{/b} Come on, Ash, sign it — we don't have time to waste!"

    narrator "{color=#F2CC8F}DECISION 3 OF 3 — THE $60,000 WIRE{/color}"
    narrator "Sixty thousand dollars is queued in a single irreversible blockchain transfer under a ticking clock."

    menu:
        "Refuse to rush: send a $1 test transaction first, confirm on video with Xochtl's sanctuary partner that the $1 arrived, then wire the $59,999.":
            $ adjust(security=+25, treasury=+10, morale=+20, vibes=+15)
            ashel "Stop. Nobody wires sixty grand in one blind click. In crypto there is no bank manager, no customer support hotline, and no undo button."
            xochtl "Send a {b}test transaction{/b} of one single dollar first. I have the Brazil land trust treasurer on video right now."
            narrator "You queue a $1.00 transfer to the address Lay-Lay pasted. Thirty seconds pass. On the video call, the sanctuary treasurer shakes her head."
            xochtl "She didn't get the dollar! Look closely at the middle digits of Lay-Lay's address — it's a vanity address-poisoning spoof from the ops chat!"
            laylay "Oh my god... the first four and last four characters matched, but the middle was a hacker's wallet. If we had sent the $60,000..."
            ashel "We would have lost everything and spent the next week crying on forums. Now let's take the verified address directly from the treasurer's signed hardware QR, send a $1 test transaction to confirm, and wire the remaining $59,999."
            narrator "The $1 test lands in four seconds. The $59,999 follows cleanly into the verified recipient slot."
            call lesson("test_transaction")

        "Click 'Approve & Broadcast' on the full $60,000 right now so you don't miss the freight cutoff!":
            $ adjust(treasury=-100, morale=-40, vibes=-30)
            scene bg treasury_fire with vpunch
            show ashel hurt at left
            show laylay alarmed at right
            show xochtl hurt at center
            ashel "We're out of time — broadcasting the full $60,000 now!"
            narrator "The transaction finalizes in 1.2 seconds. Five minutes later, the Brazil sanctuary calls: their wallet balance is still zero. The address in the chat was a vanity-poisoned lookalike."
            narrator "For three days, Lay-Lay posts desperate pleas in validator channels asking how to 'reverse a mistaken wire.' The answer is always the same: immutable ledgers do not have a refund desk."
            call checkpoint_bad_end(
                "ep1_d3",
                "The $60,000 Wrong-Address Disaster",
                "Rushing a bulk transfer without sending a $1 test transaction first sent $60,000 into a poisoned address. On a trustless blockchain, transactions are final and irreversible.",
                "test_transaction"
            )

        "Only check the first 4 characters of the address ('0x7F4c') and send the full $60,000 without a test transfer.":
            $ adjust(treasury=-100, morale=-35)
            scene bg treasury_fire with vpunch
            show ashel alarmed at left
            show laylay alarmed at right
            ashel "First four characters say 0x7F4c — good enough for me. Sending all $60,000!"
            narrator "Attackers use GPU vanity generators to create poison addresses that match the first four and last four hex characters of your frequent recipients. Every cent vanishes instantly."
            call checkpoint_bad_end(
                "ep1_d3",
                "Vanity Address-Poisoning Trap",
                "Checking only the first four characters of a wallet address is never enough. Always verify the full address out-of-band and confirm receipt of a $1 test transaction before sending bulk treasury funds.",
                "test_transaction"
            )

    ## --- EPISODE 1 RESOLUTION ---
    scene bg sanctuary with fade
    show ashel proud at left
    show xochtl proud at center
    show laylay neutral at right

    narrator "At the Lisbon terminal that night, the twelve crates of botanical elixirs clear customs smoothly. The Brazil sanctuary confirms all $60,000 in its vault, and your 2-of-3 hardware keys rest safely at your side."
    xochtl "Keys rotated. Grifters vetted out. One dollar tested before sixty thousand moved."
    ashel "And nobody had to learn the hard way at the airport."

    call complete_episode(
        "ep1_keys",
        "You rotated the leaked keys into a 2-of-3 non-custodial multisig, vetted out a predatory admin nominee, and caught a vanity address-poisoning attack with a $1 test transaction before wiring $60,000."
    )


################################################################################
## EPISODE 2: "THE LISBON REFUSAL"
## Pillar II: Collaboration & Co-op = Winning Together (The "Amy & Edward / Jena" Story)
## POV: Xochtl (The Shaman) & Ash El (The Creator)
## Lessons: creator_vs_admin, coop_solidarity, burnout
################################################################################

label ep2_lisbon:
    $ current_episode = "ep2_lisbon"
    $ current_pov = "Xochtl & Ash El"
    $ vibes = 40
    $ treasury = 95
    $ security = 65
    $ morale = 30
    $ burnout = 65
    show screen stats_hud

    ## --- THE HOOK: WORST-CASE SCENARIO (IN MEDIA RES) ---
    scene bg treasury_fire with fade
    show ashel alarmed at left
    show xochtl focused at center
    show laylay stern at right

    narrator "{color=#FF6B6B}WORST-CASE OUTCOME — LISBON SHOWCASE BACKSTAGE, 3 HOURS TO DOORS{/color}"
    narrator "Projectors hum across the main hall in Lisbon. Ash El hasn't slept in forty hours. He built the entire interactive DAO showcase game, composed the acoustic-electronic score, and shipped every asset on time."
    ashel "The build is live on stage, Lay-Lay! Why did you just reject my 18,000 USDC milestone payout in the multisig?!"
    laylay "Because I think your ego has gotten out of control, Ash El. Everyone at the conference keeps calling this 'Ash El's masterpiece' as if administration doesn't even exist. Consider the payout frozen until I feel your attitude is more humble."
    ashel "I paid the sound engineers out of my own pocket! If you freeze the bounty after I already delivered the game, I'm pulling the repository offline right now!"
    xochtl "Stop — both of you! If Ash deletes the build and Lay-Lay locks the treasury, the entire collective dies on stage in three hours!"

    ## --- THE REWIND ---
    call trigger_rewind(
        headline="⏪ REWINDING 10 DAYS EARLIER",
        subline="POV: Xochtl & Ash El · Preparing the Lisbon Showcase Game"
    )

    scene bg cacao_circle with fade
    $ vibes = 70
    $ treasury = 110
    $ security = 65
    $ morale = 70
    $ burnout = 25

    show xochtl warm at left
    show ashel neutral at center
    show laylay smirk at right

    narrator "Ten days before the Lisbon presentation. You are {b}Xochtl{/b}, pouring ceremonial cacao for the build team while Ash El tunes his instrument and compiles the interactive showcase scenes."
    narrator "You can already see the subtle shift in {b}Lay-Lay{/b}'s eyes: at first she was awed by how fast Ash El created the music, code, and visual world. Now that awe is curdling into quiet resentment."
    laylay "Regarding the 18,000 USDC budget for the Lisbon game — let's not bother locking it into a milestone smart contract. I'll just disburse whatever I feel Ash El deserves after I review the vibes in Lisbon."

    ## --- DECISION 1: OBJECTIVE ESCROW VS. SUBJECTIVE GATEKEEPING ---
label ep2_d1:
    scene bg cacao_circle
    show xochtl focused at left
    show ashel neutral at center
    show laylay smirk at right

    narrator "{color=#F2CC8F}DECISION 1 OF 3 — PROTECTING CREATORS FROM ADMINISTRATIVE WHIM{/color}"
    narrator "Lay-Lay wants complete subjective discretion over whether and how much Ash El gets paid after he finishes building the Lisbon game."

    menu:
        "Lock the 18,000 USDC in an objective smart-contract escrow tied to verifiable deliverables (playable build + audio assets), not personal feelings.":
            $ adjust(security=+15, morale=+15, burnout=-10)
            xochtl "When creators pour their labor into a collective, their livelihood cannot depend on an administrator's mood on delivery day. We're locking the bounty in {b}escrow{/b} with objective milestone criteria."
            ashel "Playable build passes QA, audio stems uploaded, payout releases automatically. Clean and fair."
            laylay "Hmph. You act like I wouldn't be fair! Fine, put the base bounty in escrow — though the final 6,000 USDC integration bounty still goes through my admin review queue."
            call lesson("creator_vs_admin")

        "Agree to let Lay-Lay decide the payout amount after delivery based on 'how humble Ash El's energy feels.'":
            $ adjust(morale=-35, burnout=+30)
            scene bg treasury_fire with vpunch
            show ashel hurt at left
            show laylay stern at right
            xochtl "Let's trust Lay-Lay's judgment after the showcase."
            narrator "On showcase morning, jealous of the crowd cheering Ash El's demo, Lay-Lay declares his work 'spiritually unaligned' and refuses to pay him a cent. Ash El walks out and the showcase collapses."
            call checkpoint_bad_end(
                "ep2_d1",
                "Administrative Gatekeeping & Refusal to Pay",
                "Leaving creator compensation to an administrator's subjective mood allowed jealousy and ego to block payment for completed work. Always use objective milestone escrow.",
                "creator_vs_admin"
            )

        "Tell Ash El to work for free 'for exposure' so there's no money to argue over.":
            $ adjust(morale=-40, burnout=+45)
            scene bg treasury_fire with vpunch
            show ashel hurt at left
            xochtl "What if you just build the whole Lisbon game for free, Ash?"
            ashel "I can't pay the audio devs or my rent with 'exposure,' Xochtl. While the admins collect stipends, the creators starve?"
            narrator "Ash El burns out four days before Lisbon, leaving an unfinished prototype and a shattered collective."
            call checkpoint_bad_end(
                "ep2_d1",
                "Creator Exploitation & Collapse",
                "Expecting creators to donate all the labor while administrators control the treasury destroys morale and guarantees burnout.",
                "creator_vs_admin"
            )

    ## --- DECISION 2: THE "AMY & EDWARD / JENA" AVATAR PLAY (CO-OP SOLIDARITY) ---
label ep2_d2:
    scene bg cacao_circle with dissolve
    show xochtl neutral at left
    show ashel hurt at center
    show laylay stern at right

    narrator "Two days before the Lisbon presentation. The base escrow cleared, but Lay-Lay just rejected Ash El's final 6,000 USDC Lisbon game module in the governance portal — claiming the code and art are 'substandard and unusable.'"
    ashel "She didn't even open the build! Look at the server logs — zero downloads from her IP. She rejected it thirty seconds after seeing my name on the pull request because people at the pre-party praised my music!"
    xochtl "I see it, Ash. It's not about the work — her awe turned into jealousy, and now she's gatekeeping your name. If we scream at her in public Discord, she'll play the victim and freeze the multisig."
    ashel "Then how do we prove to the whole DAO council that she's blocking me out of pure personal bias AND get the work paid?"

    narrator "{color=#F2CC8F}DECISION 2 OF 3 — EXPOSING ADMINISTRATIVE BIAS WITH CO-OP SOLIDARITY{/color}"
    narrator "Lay-Lay rejected Ash El's finished Lisbon game module sight-unseen solely because his name was attached to it."

    menu:
        "Use Xochtl's 'Neutral Avatar' strategy: covertly resubmit Ash El's exact same game build under a fresh contributor handle ('solstice_dev_09') and route the payout directly to Ash.":
            $ adjust(vibes=+20, morale=+25, burnout=-15, security=+10)
            xochtl "Don't touch a single line of code, Ash. Give me the archive. I'm creating a neutral contributor profile — {b}solstice_dev_09{/b} — with your hardware payout address underneath, and submitting the exact same build to Lay-Lay's queue."
            narrator "Twenty minutes later, Lay-Lay's notification chimes in the council channel."
            laylay "Everyone look at {b}solstice_dev_09{/b}'s submission! Approved instantly for the full 6,000 USDC! See, Ash El? THIS is what professional, ego-free game design looks like — unlike the garbage you submitted!"
            xochtl "Check the SHA-256 hash on-chain, Lay-Lay. Byte for byte, {b}solstice_dev_09{/b} is the exact same file Ash El uploaded two hours ago. And you just signed his payout."
            laylay "Wait — what?! That's... you tricked me!"
            ashel "No, Xochtl proved on-chain that my work was flawless and your rejection was 100%% personal gatekeeping. And the 6,000 USDC just landed in my wallet."
            call lesson("coop_solidarity")

        "Start a screaming match in the public conference Telegram and threaten to smash the stage laptops.":
            $ adjust(vibes=-35, morale=-30)
            scene bg treasury_fire with vpunch
            show ashel alarmed at left
            show laylay smirk at right
            ashel "I'm going to blast Lay-Lay in the main conference chat right now!"
            laylay "Look how unstable Ash El is being, everyone! Clearly I was right to withhold treasury funds for safety."
            narrator "Sponsors pull out within an hour, and the council sides with Lay-Lay's calm administrative spin over Ash El's public meltdown."
            call checkpoint_bad_end(
                "ep2_d2",
                "Public Meltdown Plays Into the Gatekeeper's Hands",
                "Fighting petty administrative gatekeeping with an unstrategic public outburst lets the administrator frame the creator as 'unstable.' Co-op solidarity and verifiable receipts win where rage fails.",
                "coop_solidarity"
            )

        "Swallow the injustice, forfeit the 6,000 USDC, and let Lay-Lay take stage credit for Ash El's game.":
            $ adjust(morale=-40, burnout=+35)
            scene bg treasury_fire with vpunch
            show ashel hurt at left
            show xochtl hurt at center
            xochtl "Just let the money go, Ash. Keep the peace."
            narrator "At the Lisbon showcase, Lay-Lay takes the microphone for forty minutes as 'Visionary Producer' while Ash El sits unpaid in the back row. By Monday, Ash El quits the DAO forever."
            call checkpoint_bad_end(
                "ep2_d2",
                "Appeasing the Gatekeeper Destroys the Creator",
                "Rewarding administrative jealousy with silence teaches gatekeepers they can withhold creator pay with impunity, driving away the people who actually build the collective's value.",
                "coop_solidarity"
            )

    ## --- DECISION 3: RESTRUCTURING FOR CO-OP RECIPROCITY & PREVENTING BURNOUT ---
label ep2_d3:
    scene bg cacao_circle with dissolve
    show xochtl warm at left
    show ashel proud at center
    show laylay defensive at right

    narrator "With the SHA-256 hash receipt on-chain, the entire DAO council sees how unchecked administrative power nearly sabotaged the Lisbon showcase."
    ashel "The money is in my wallet and the game is ready for the main stage tonight. But if we leave the admin structure the way it is, this exact fight will happen again next month."
    xochtl "How do we restructure the collective so Collaboration & Co-op truly means winning together?"

    narrator "{color=#F2CC8F}DECISION 3 OF 3 — DESIGNING CO-OP RECIPROCITY{/color}"

    menu:
        "Establish rotating administrative signers, peer-reviewed creative bounties, and mandatory rest/sabbatical stipends so creators and stewards share power transparently.":
            $ adjust(morale=+20, burnout=-20, vibes=+15, security=+10)
            xochtl "No more permanent administrative monarchs. Admin signers rotate every quarter by contributor vote, creative milestones are peer-reviewed by fellow builders, and every crunch sprint includes funded rest."
            ashel "Now that's a cooperative I can pour my soul and music into without burning out."
            laylay "Rotating signers... and transparent peer review. Okay. Honestly, holding the veto alone was turning me into someone I didn't even like."
            call lesson("burnout")

        "Fire Lay-Lay and make Ash El the sole unchecked dictator of both creation and treasury administration.":
            $ adjust(burnout=+45, security=-25)
            scene bg treasury_fire with vpunch
            show ashel alarmed at center
            ashel "Give me every key, every spreadsheet, every tax filing, and every creative sprint!"
            narrator "Within three weeks of trying to write music, press herbal juices, run accounting, and sign every invoice alone at 4:00 a.m., Ash El collapses from catastrophic founder burnout."
            call checkpoint_bad_end(
                "ep2_d3",
                "Solo-Dictator Burnout Collapse",
                "Replacing an unchecked administrator by forcing the lead artist to do 100% of both creation and administration alone guarantees rapid burnout and single-point-of-failure risk.",
                "burnout"
            )

        "Keep the exact same top-down admin hierarchy and hope Lay-Lay 'promises to be nicer next time.'":
            $ adjust(morale=-30, security=-20)
            scene bg treasury_fire with vpunch
            show laylay smirk at right
            laylay "I promise I'll totally be nicer next conference!"
            narrator "Without structural change, the very next grant cycle repeats the exact same gatekeeping freeze, and half the builders fork away."
            call checkpoint_bad_end(
                "ep2_d3",
                "Unchanged Structure Repeats the Crisis",
                "Relying on personal promises instead of changing governance rules leaves the collective vulnerable to the exact same administrative abuse on the next payout cycle.",
                "creator_vs_admin"
            )

    ## --- EPISODE 2 RESOLUTION ---
    scene bg sanctuary with fade
    show xochtl proud at left
    show ashel proud at center
    show laylay neutral at right

    narrator "That evening in Lisbon, the interactive showcase brings the hall to its feet. Ash El's live folk-electronic strings weave through the projection dome, Xochtl welcomes two hundred new co-op patrons, and the milestone escrow settles automatically on-chain."
    xochtl "When creators are protected by objective agreements and co-op solidarity, nobody has to beg for what they earned."

    call complete_episode(
        "ep2_lisbon",
        "You protected creator payouts with objective escrow, used Xochtl's neutral-avatar hash proof to defeat administrative gatekeeping without a destructive public brawl, and instituted rotating co-op stewardship."
    )


################################################################################
## EPISODE 3: "BLOOD, CACAO & PAPER"
## Pillar III: Make & Enforce Agreements (Importance of Law/Legal for Innovators)
## POV: Ash El & Xochtl
## Lessons: agreements_law, vesting, partnership
################################################################################

label ep3_agreements:
    $ current_episode = "ep3_agreements"
    $ current_pov = "Ash El & Xochtl"
    $ vibes = 35
    $ treasury = 45
    $ security = 30
    $ morale = 35
    $ burnout = 50
    show screen stats_hud

    ## --- THE HOOK: WORST-CASE SCENARIO (IN MEDIA RES) ---
    scene bg treasury_fire with fade
    show ashel alarmed at left
    show xochtl hurt at center
    show laylay alarmed at right

    narrator "{color=#FF6B6B}WORST-CASE OUTCOME — THE CACAO ALTAR SUMMONS{/color}"
    narrator "A uniformed process server steps past the incense burner and drops a thick manila summons onto the ceremonial cloth. At the same moment, your phone buzzes with a liquidity alert: the DAO token just crashed 78%%."
    ashel "What is happening?! That early co-founder who left in Week Two after making three slides — how did he just dump thirty-three percent of the entire token supply on the market?!"
    laylay "Because we gave every founder an instant 33%% handshake split on Day One with zero written vesting cliff! He owned those tokens free and clear the second he walked out the door."
    xochtl "And what is this court summons with my personal home address and Ash El's bank account listed as defendants?!"
    laylay "The vendor whose stage rig shorted out in South Dakota is suing the DAO for $140,000. Because we refused to form a legal wrapper — calling contracts 'Babylon paper' — the court classified our DAO as an unwrapped general partnership. Every one of us is personally liable!"

    ## --- THE REWIND ---
    call trigger_rewind(
        headline="⏪ REWINDING TO DAY 3 — THE FOUNDING CACAO CIRCLE",
        subline="POV: Ash El & Xochtl · Writing the Collective's Charter"
    )

    scene bg cacao_circle with fade
    $ vibes = 75
    $ treasury = 110
    $ security = 50
    $ morale = 80
    $ burnout = 15

    show ashel neutral at left
    show xochtl warm at center
    show laylay neutral at right

    narrator "Day 3 of the collective. Steam rises from earthen cacao cups. The energy in the circle is electric — music, medicine, and community dreams flowing fast."
    narrator "{b}Xochtl{/b} sets a clean three-page founder covenant and co-op charter beside the cacao pot while {b}Lay-Lay{/b} opens the governance ledger."
    ashel "Man, the music is flowing and everyone loves each other right now. Do we really need lawyers and contracts in a counter-culture sanctuary?"
    xochtl "Listen carefully, Ash. How we structure our equity, our legal wrapper, and our treasury today determines whether this sanctuary survives its first storm."

    ## --- DECISION 1: WRITTEN VESTING & CLIFFS VS. HANDSHAKE SPLITS ---
label ep3_d1:
    scene bg cacao_circle
    show ashel neutral at left
    show xochtl focused at center
    show laylay neutral at right

    narrator "{color=#F2CC8F}DECISION 1 OF 3 — THE FOUNDER CAP TABLE & VESTING AGREEMENT{/color}"
    narrator "How do you allocate founder governance tokens and equity among the founding circle?"

    menu:
        "Sign a written 4-year vesting agreement with a 1-year cliff tied to active contribution — nobody gets unlocked tokens until they stay and build.":
            $ equity = "vesting"
            $ adjust(security=+20, morale=+10, treasury=+10)
            ashel "True ceremony respects commitment over time. If someone leaves in month two, they shouldn't walk away with a third of the sanctuary's future."
            xochtl "Four-year {b}vesting{/b} with a one-year {b}cliff{/b}, written in plain language and enforced by a token-lock smart contract."
            laylay "Smart. When someone ghosts early, their unvested tokens return automatically to the cooperative contributor pool."
            call lesson("vesting")

        "Do a 'Sacred 33/33/33 Handshake Split' with all tokens unlocked on Day 1 — written vesting feels too corporate!":
            $ adjust(treasury=-60, morale=-35)
            scene bg treasury_fire with vpunch
            show ashel alarmed at left
            show laylay stern at right
            ashel "No cliffs, no paperwork! Equal unlocked tokens for everyone right now!"
            narrator "Two weeks later, an early co-founder loses interest, vanishes from work channels, and market-dumps his entire 33%% allocation into the liquidity pool — draining the treasury and leaving the builders with a dead cap table."
            call checkpoint_bad_end(
                "ep3_d1",
                "The Handshake Split & Dead-Equity Dump",
                "Giving co-founders unlocked equity on Day 1 without a 4-year vesting schedule and 1-year cliff lets early quitters walk away with a massive share of the collective and dump on the people doing the work.",
                "vesting"
            )

        "Promise to 'figure out who owns what in a year or two' after the project gets rich.":
            $ adjust(morale=-40, vibes=-30)
            scene bg treasury_fire with vpunch
            show ashel hurt at left
            show xochtl hurt at center
            ashel "Let's not talk about numbers now — we'll split everything once the treasury hits a million dollars!"
            narrator "The moment the first $100,000 grant arrives, three founders remember three completely different verbal promises. The collective implodes in bitter accusations and lawyer threats."
            call checkpoint_bad_end(
                "ep3_d1",
                "Deferred Agreements Breed War",
                "Avoiding written equity agreements when there is nothing to fight over guarantees an explosive war the moment real money arrives.",
                "agreements_law"
            )

    ## --- DECISION 2: LEGAL WRAPPER VS. UNWRAPPED GENERAL PARTNERSHIP ---
label ep3_d2:
    scene bg cacao_circle with dissolve
    show ashel neutral at left
    show xochtl stern at center
    show laylay calculating at right

    narrator "Next, Xochtl slides the second document across the cedar table: articles for a **Limited Cooperative Association (Co-op LLC) / Swiss Verein legal wrapper**."
    xochtl "Right now, we are signing real-world venue leases, shipping herbal goods across borders, and voting on treasury payouts. Without a legal wrapper, courts don't see a 'mystical collective' — they see an unincorporated {b}general partnership{/b}."
    ashel "Wait — doesn't putting 'DAO' in our name automatically protect our personal bank accounts?"
    laylay "Ask the members of Ooki DAO after the CFTC sued them. Without a wrapper, every single person who voted in governance can be held personally, jointly, and severally liable for 100%% of the collective's debts or lawsuits."

    narrator "{color=#F2CC8F}DECISION 2 OF 3 — REAL-WORLD LAW & LEGAL WRAPPERS{/color}"

    menu:
        "Establish a formal Co-op LLC / Swiss Verein legal wrapper and written operating agreement before signing contracts or moving funds.":
            $ wrapper = "verein"
            $ adjust(security=+25, treasury=-5, morale=+15)
            xochtl "Counter-culture innovators moving fast need stronger armor, not weaker armor. We wrap the DAO in a real cooperative legal entity so no artist or healer loses their home over a venue dispute."
            ashel "Blood, cacao, and paper. The ceremony sets our intention; the legal wrapper protects our people in the courts."
            laylay "Filed and stamped. Now the entity signs leases and holds liability — not our personal savings accounts."
            call lesson("partnership")

        "Refuse all legal wrappers — 'Code is Law, and paper contracts are for the old world!'":
            $ adjust(security=-40, treasury=-70)
            scene bg treasury_fire with vpunch
            show ashel alarmed at left
            show xochtl hurt at center
            show laylay alarmed at right
            ashel "We don't register with any jurisdiction! Code is law!"
            narrator "Six months later, a freight contractor files suit over a damaged festival shipment. Because the DAO has no legal wrapper, the judge rules it a general partnership and freezes Ash El and Xochtl's personal bank accounts."
            call checkpoint_bad_end(
                "ep3_d2",
                "Unlimited Personal Liability (The Ooki DAO Trap)",
                "An unwrapped DAO operating in the real world defaults to a general partnership, exposing every active participant and voter to unlimited personal liability.",
                "partnership"
            )

        "Have Ash El sign every venue lease and vendor contract under his personal Social Security Number to save filing fees.":
            $ adjust(security=-35, burnout=+35)
            scene bg treasury_fire with vpunch
            show ashel hurt at left
            ashel "I'll just put my own name and credit card on all the festival contracts to save $2,000."
            narrator "When a sponsor defaults on a $50,000 invoice, the creditors come straight after Ash El's personal instruments and apartment while the DAO treasury sits legally disconnected."
            call checkpoint_bad_end(
                "ep3_d2",
                "Personal Guarantor Ruin",
                "Never put an individual creator's personal identity on the hook for collective liabilities. Always contract through a properly capitalized legal wrapper.",
                "agreements_law"
            )

    ## --- DECISION 3: ENFORCEABLE RECOUPMENT & BARBELL TREASURY DISCIPLINE ---
label ep3_d3:
    scene bg cacao_circle with dissolve
    show ashel neutral at left
    show xochtl warm at center
    show laylay neutral at right

    narrator "Xochtl turns to the final page of the charter: **Treasury Reserve & Creator Recoupment Rules**."
    xochtl "Ash El has already fronted $12,000 of his own studio gear and herbal inventory, and our community token just launched. How do we write the treasury rules into the charter?"

    narrator "{color=#F2CC8F}DECISION 3 OF 3 — WRITTEN RECOUPMENT & TREASURY DIVERSIFICATION{/color}"

    menu:
        "Enforce a written charter rule: diversify 50%% of treasury into USDC stablecoin runway and schedule automatic milestone recoupment for verified creator expenses.":
            $ treasury_mix = "barbell"
            $ adjust(security=+20, treasury=+15, morale=+20, vibes=+10)
            ashel "When we put recoupment and a 50%% USDC {b}barbell{/b} reserve in writing, nobody has to beg to be paid back for fronting supplies, and a crypto market dip won't wipe out our rent."
            xochtl "Clear agreements don't kill the magic — they keep resentment out of the sanctuary so the magic can survive."
            laylay "Charter ratified and mirrored in the multisig spending policies."
            call lesson("agreements_law")

        "Keep 100%% of the treasury in our volatile governance token and leave expense reimbursement to 'informal future vibes.'":
            $ adjust(treasury=-75, morale=-35)
            scene bg treasury_fire with vpunch
            show ashel hurt at left
            show xochtl hurt at center
            ashel "Keep 100%% in our own token — selling any for USDC looks bearish!"
            narrator "When the broader market dips 60%%, your mono-token treasury loses 85%% of its purchasing power overnight. The collective can't pay freight bills or reimburse Ash El's fronted gear."
            call checkpoint_bad_end(
                "ep3_d3",
                "Mono-Token Treasury Death Spiral & Unpaid Recoupment",
                "Holding 100% of a DAO's treasury in its own volatile token means your runway vanishes precisely when sentiment dips, leaving upfront creator expenses unpaid.",
                "agreements_law"
            )

    ## --- EPISODE 3 RESOLUTION ---
    scene bg cacao_circle with fade
    show ashel proud at left
    show xochtl proud at center
    show laylay neutral at right

    narrator "Six months later, when an early speculator tries to walk away with unvested tokens and a festival vendor disputes a freight invoice, your written 1-year cliff, Co-op legal wrapper, and 50%% USDC reserve handle both in a single afternoon."
    xochtl "The cacao grounded our spirit. The paper and smart contracts protected our house."

    call complete_episode(
        "ep3_agreements",
        "You instituted a written 4-year vesting schedule with a 1-year cliff, shielded the collective inside a formal legal wrapper, and enforced a 50% USDC barbell reserve with clear creator recoupment."
    )


################################################################################
## EPISODE 4: "THE KEYS OF THE APOTHECARY"
## Perspective Shift: Behind the Administrator's Ledger
## POV: Lay-Lay (The Administrator — Potions, Herbs & Multisig Keys)
## Lessons: capture, verify_hex, flashloan
################################################################################

label ep4_apothecary:
    $ current_episode = "ep4_apothecary"
    $ current_pov = "Lay-Lay (The Administrator)"
    $ vibes = 45
    $ treasury = 110
    $ security = 35
    $ morale = 45
    $ burnout = 55
    show screen stats_hud

    ## --- THE HOOK: WORST-CASE SCENARIO (IN MEDIA RES) ---
    scene bg treasury_fire with fade
    show laylay alarmed at center
    show ashel alarmed at left
    show xochtl hurt at right

    narrator "{color=#FF6B6B}WORST-CASE OUTCOME — LAY-LAY'S APOTHECARY, 1:18 A.M.{/color}"
    narrator "Amber apothecary vials lie shattered across the floorboards. On Lay-Lay's monitor, a single red banner blinks: {b}GOVERNANCE EXECUTED — 100%% OF TREASURY TRANSFERRED TO 0xDEAD...BEEF{/b}."
    ashel "Lay-Lay, open the door! What did you just sign on the multisig?!"
    laylay "I didn't mean to! It was 1:14 in the morning, the bot said our Discord verification was expiring, and Atlas was pressuring me to fast-track his whale proposal without a timelock!"
    xochtl "You gave Atlas a backroom veto, disabled the 48-hour timelock, and blind-signed a malicious contract on your hardware wallet without reading the hex?!"
    laylay "Everyone thinks being the administrator is pure power — they don't see the fifty notifications an hour, the whales offering bribes, and the phishing traps waiting for one tired click!"

    ## --- THE REWIND ---
    call trigger_rewind(
        headline="⏪ REWINDING 48 HOURS EARLIER",
        subline="POV: Lay-Lay · Inside the Candlelit Apothecary"
    )

    scene bg apothecary with fade
    $ vibes = 65
    $ treasury = 125
    $ security = 55
    $ morale = 70
    $ burnout = 30

    show laylay calculating at center
    show ashel neutral at left
    show xochtl neutral at right

    narrator "Forty-eight hours earlier. You are {b}Lay-Lay{/b}. Rows of dried lavender, glass tincture bottles, and ledger notebooks line your apothecary desk alongside your hardware wallet."
    narrator "For the first time, you feel the weight from the other side of the table: while Ash El and Xochtl prepare the ceremony, your inbox overflows with thirty-two invoices, tax filings, and a private voice note from {b}Atlas{/b}, an outside crypto whale."
    laylay "Listen to this message Atlas just sent me: he wants to inject 80 ETH into the apothecary treasury today — on one condition."
    ashel "What condition?"
    laylay "He wants 35%% of the governance supply and a private administrative side-letter so he and I can fast-track proposals without waiting for the co-op circle to vote."

    ## --- DECISION 1: RESISTING PLUTOCRATIC CAPTURE ---
label ep4_d1:
    scene bg apothecary
    show laylay stern at center
    show ashel focused at left
    show xochtl stern at right

    narrator "{color=#F2CC8F}DECISION 1 OF 3 — THE WHALE'S BACKROOM DEAL{/color}"
    narrator "The whale offers massive liquidity if you quietly hand him 35%% governance control and a private administrative fast-track."

    menu:
        "Reject the secret side-letter: cap any single whale at 8%% voting power and require full public co-op disclosure.":
            $ adjust(security=+20, morale=+15, vibes=+5)
            laylay "My job as administrator is to guard the apothecary, not sell its keys to the highest bidder. We'll allow capped patronage tokens up to 8%% in the public round — zero backroom vetoes."
            xochtl "Thank you, Lay-Lay. Unchecked whale capital always looks like a gift until the first governance vote."
            ashel "Eight percent cap, public terms only. The sanctuary stays ours."
            call lesson("capture")

        "Accept the whale's backroom deal — run the DAO behind the scenes while the artists 'just make art.'":
            $ adjust(security=-35, morale=-40)
            scene bg treasury_fire with vpunch
            show laylay alarmed at center
            show ashel hurt at left
            laylay "Deal. Between his 35%% stake and my admin key, we'll steer everything quietly."
            narrator "Two weeks later, the whale uses his 35%% voting bloc to liquidate the community sanctuary budget and vote himself a 100%% treasury yield buyout, firing Ash El, Xochtl, and finally you."
            call checkpoint_bad_end(
                "ep4_d1",
                "Plutocratic Whale Capture",
                "Selling uncapped governance control to a single whale in exchange for fast capital turns a cooperative into a plutocracy that immediately liquidates the creators.",
                "capture"
            )

    ## --- DECISION 2: VERIFYING HARDWARE CALLDATA HEX AT 1:14 A.M. ---
label ep4_d2:
    scene bg apothecary with dissolve
    show laylay calculating at center
    show xochtl focused at right

    narrator "Night two in the apothecary. It is 1:14 a.m. You've just finished bottling herbal orders and logging thirty-two contributor reimbursements. Your eyes burn."
    narrator "Suddenly, an urgent DM pings from a bot with the exact avatar of your governance portal: {b}'URGENT: Multisig Session Desync. Click here and sign to keep the Brazil Sanctuary payout from failing at dawn.'{/b}"
    narrator "You click the link. Your browser wallet pops up a signature request. On your hardware wallet's tiny screen, however, the raw hex doesn't say {b}confirmBatch(){/b} — it reads selector {b}0xa22cb465 (setApprovalForAll){/b} on the treasury vault."

    narrator "{color=#F2CC8F}DECISION 2 OF 3 — THE 1:14 A.M. HARDWARE SIGNATURE{/color}"
    narrator "You are exhausted, the popup claims urgent deadline pressure, and your hardware screen shows raw hex `{b}0xa22cb465{/b}` instead of a standard multisig batch."

    menu:
        "Stop immediately: read the hardware wallet hex screen, recognize the spoofed approval selector, close the tab, and verify via a $1 test batch in the morning.":
            $ adjust(security=+25, burnout=-10, morale=+10)
            laylay "Wait a second... selector {b}0xa22cb465{/b} is {b}setApprovalForAll{/b}! A real multisig confirmation never asks for unlimited token approval from a DM link."
            xochtl "Good catch on the hardware screen, Lay-Lay! Ninety percent of administrators click through at 1:14 a.m. because they read the pretty website UI instead of the device hex."
            laylay "New apothecary rule: no signing transactions after midnight, never click DM links, and always verify the contract address and calldata hex on the hardware device."
            call lesson("verify_hex")

        "Click 'Confirm' on the hardware wallet without reading the hex — you're tired and don't want the dawn payout to be late!":
            $ adjust(security=-50, treasury=-110)
            scene bg treasury_fire with vpunch
            show laylay alarmed at center
            laylay "I'm too tired to read hex bytes — approving!"
            narrator "The spoofed drainer contract immediately sweeps every token the apothecary multisig holds permission over. By 1:16 a.m., the vault is empty."
            call checkpoint_bad_end(
                "ep4_d2",
                "1:14 a.m. Blind-Signing Phishing Drain",
                "Browser UIs can be spoofed; only the hardware wallet screen shows the true contract address and calldata hex. Never blind-sign under late-night urgency.",
                "verify_hex"
            )

    ## --- DECISION 3: DEFENDING AGAINST FLASH-LOAN GOVERNANCE CAPTURE ---
label ep4_d3:
    scene bg apothecary with dissolve
    show laylay stern at left
    show xochtl focused at center
    show ashel determined at right

    narrator "Morning breaks over the apothecary. Having failed to buy you off in private, a hostile arbitrageur borrows $2,000,000 of governance tokens in a single-block {b}flash loan{/b} and submits {b}Proposal #44: 'Transfer 100%% of Apothecary Reserve to External Yield Vault.'{/b}"
    ashel "Lay-Lay! Where did that whale wallet get forty percent voting power in twelve seconds?!"
    xochtl "He didn't buy it — he rented it for one block with a flash loan! How is our governance contract configured?!"

    narrator "{color=#F2CC8F}DECISION 3 OF 3 — STOPPING THE FLASH-LOAN GOVERNANCE ATTACK{/color}"

    menu:
        "Trigger the 48-hour governance timelock, require snapshot voting from prior blocks, and rally Ash El & Xochtl's community delegates to veto the attack.":
            $ timelocks = True
            $ adjust(security=+25, morale=+20, vibes=+20)
            laylay "He thought our governance executed in the same block like Beanstalk! I configured a mandatory 48-hour {b}timelock{/b} and historical block-snapshot voting. His flash-loaned tokens have zero weight on last week's snapshot!"
            ashel "And within twenty minutes, our real community holders rally 72%% quorum to crush Proposal #44."
            xochtl "When administration serves as the shield for the collective rather than its master, no whale or flash loan can break us."
            call lesson("flashloan")

        "Allow instant same-block execution with no timelock so proposals 'move at the speed of crypto.'":
            $ adjust(security=-50, treasury=-120)
            scene bg treasury_fire with vpunch
            show laylay alarmed at left
            show ashel alarmed at right
            laylay "We turned off timelocks so votes execute instantly in the same block!"
            narrator "Just like the $182M Beanstalk exploit, the attacker borrows the vote, passes Proposal #44, drains the entire treasury, and repays the flash loan inside a single 12-second block."
            call checkpoint_bad_end(
                "ep4_d3",
                "Same-Block Flash-Loan Governance Drain",
                "Without historical block snapshots and a 24–48 hour execution timelock, an attacker can borrow a majority vote via a flash loan and drain the treasury in a single block.",
                "flashloan"
            )

    ## --- EPISODE 4 RESOLUTION ---
    scene bg apothecary with fade
    show laylay neutral at center
    show ashel proud at left
    show xochtl proud at right

    narrator "Sunlight warms the amber apothecary jars. Ash El sets a fresh bottle of cold-pressed ginger elixir beside Lay-Lay's hardware ledger, and Xochtl pours three cups of ceremonial cacao."
    laylay "I used to think holding the keys meant holding power over you two. Now I understand: holding keys in a cooperative means holding the shield while we build together."

    call complete_episode(
        "ep4_apothecary",
        "Stepping into Lay-Lay's shoes, you rejected Whale Atlas's plutocratic side-letter, caught a 1:14 a.m. blind-signing phishing attack on the hardware hex screen, and defeated a flash-loan governance exploit with a 48-hour timelock."
    )
