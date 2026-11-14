# Episodic Micro-Dramas — Worst-Case Hook -> Rewind -> 3 Checkpointed Decisions
# Written in clear, accessible, easy-to-understand English ("I'm new to this" narrative).
# vault: 01 Overview/Story Structure.md · 02 Characters/Koraba.md · Clara.md · Xochit.md · 05 Lessons/*

################################################################################
## Rewind & Checkpoint Retry Screens and Helpers

default _outcome_cg_active = False

screen rewind_overlay(headline="« REWINDING TIMELINE", subline="Dropping back before the disaster..."):
    modal True
    zorder 180
    add "#140702EE"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1280
        background Frame("gui/frame.png", gui.frame_borders)
        padding (56, 44)
        at rewind_banner_flash
        vbox:
            spacing 18
            xalign 0.5
            text "[headline]" font gui.mono_font kerning 5.2 color "#FAC443" size 26 xalign 0.5
            text "[subline]" font gui.serif_font axis {"weight": 300, "opticalsize": 48} color "#EED4B4" size 38 xalign 0.5
            null height 8
            text "Change the structure. Protect the keys. Save the collective." font gui.sans_font color "#DDBCAD" size 22 xalign 0.5
            null height 10
            textbutton "« STEP INTO THE PAST" action Return() style "constellation_confirm_btn" xalign 0.5


label trigger_rewind(headline="« REWINDING TIMELINE", subline="Dropping back before the disaster..."):
    call screen rewind_overlay(headline=headline, subline=subline)
    return


screen bad_ending_rewind_modal(failure_title, failure_summary, lesson_id):
    modal True
    zorder 190
    $ ldata = get_lesson_meta(lesson_id)

    # Keep the episode's full-art disaster CG visible behind the outcome panel.
    add "#14070255"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1380
        background Frame("gui/frame.png", gui.frame_borders)
        padding (48, 38)

        vbox:
            spacing 18
            hbox:
                xfill True
                text "BAD ENDING — TIMELINE COLLAPSED" font gui.mono_font kerning 3.6 color "#D3710D" size 18
                text "[ldata['number']]" font gui.mono_font kerning 3.2 color "#B87444" size 16 xalign 1.0

            text "[failure_title]" font gui.serif_font axis {"weight": 300, "opticalsize": 48} color "#EED4B4" size 38
            text "[failure_summary]" font gui.sans_font color "#DDBCAD" size 23 line_spacing 5

            frame:
                xfill True
                background "#241309"
                padding (26, 20)
                vbox:
                    spacing 8
                    text "LESSON TAKEAWAY · [ldata['title'].upper()]" font gui.mono_font kerning 3.2 color "#578C88" size 16
                    text "[ldata['body']]" font gui.serif_font axis {"weight": 300, "opticalsize": 36} color "#EED4B4" size 22 line_spacing 5
                    text "Real-world case study: [ldata['real_world']]" font gui.sans_font color "#9D908D" size 18 line_spacing 4

            null height 8

            hbox:
                spacing 32
                xalign 0.5
                textbutton "TRY AGAIN ›" action Return("retry") style "constellation_confirm_btn"
                textbutton "QUIT SCENARIO" action Return("map") style "constellation_cancel_btn"


label checkpoint_bad_end(retry_label, failure_title, failure_summary, lesson_id):
    $ play_bad_music()
    $ _outcome_cg_active = True
    call lesson(lesson_id)
    call screen bad_ending_rewind_modal(failure_title, failure_summary, lesson_id)
    $ _outcome_cg_active = False
    if _return == "map":
        jump world_overview
    $ renpy.jump(retry_label)
    return


transform cg_modal_scale:
    size (560, 315)
    fit "contain"


screen episode_complete_modal(ep_id, summary_text):
    modal True
    zorder 190
    $ ep = EPISODES[ep_id]

    add "#140702EA"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1420
        background Frame("gui/frame.png", gui.frame_borders)
        padding (42, 30)

        vbox:
            spacing 14
            hbox:
                xfill True
                text "• DISASTER AVERTED — GOOD ENDING UNLOCKED" font gui.mono_font kerning 3.6 color "#578C88" size 18

            hbox:
                spacing 28
                frame:
                    background "#1E140E"
                    padding (6, 6)
                    add ep["cg_happy"] at cg_modal_scale
                vbox:
                    spacing 10
                    xfill True
                    text "[ep['title']] — Resolved" font gui.serif_font axis {"weight": 300, "opticalsize": 48} color "#EED4B4" size 36
                    text "• [ep['happy_title'].upper()]" font gui.mono_font kerning 3.2 color "#578C88" size 16
                    text "[summary_text]" font gui.sans_font color "#DDBCAD" size 20 line_spacing 5

            frame:
                xfill True
                background "#241309"
                padding (22, 16)
                vbox:
                    spacing 8
                    text "LESSONS MASTERED IN THIS STORY" font gui.mono_font kerning 3.2 color "#578C88" size 16
                    for lid in ep["lessons"]:
                        $ ldata = get_lesson_meta(lid)
                        text "• [ldata['number']] — [ldata['title']]: [ldata['body']]" font gui.sans_font color "#DDBCAD" size 18

            null height 6

            hbox:
                spacing 32
                xalign 0.5
                textbutton "RETURN TO CONSTELLATION ›" action Return("map") style "constellation_confirm_btn"
                textbutton "OPEN LESSONS CODEX" action [ShowMenu("lessons_codex"), Return("map")] style "constellation_cancel_btn"


init python:
    def reset_scenario_statuses():
        """Mark every scenario uncleared again.

        Points live in persistent.game_point_milestones and are never touched here,
        so the player keeps their balance, and award_game_points() is idempotent,
        so replaying earns nothing new. Lessons stay unlocked.
        """
        persistent.episodes_completed = set()
        renpy.save_persistent()
        renpy.restart_interaction()


label complete_episode(ep_id, summary_text):
    $ play_menu_music()
    python:
        if persistent.episodes_completed is None:
            persistent.episodes_completed = set()
        first_clear = ep_id not in persistent.episodes_completed
        persistent.episodes_completed.add(ep_id)
        if first_clear:
            award_game_points("scenario:%s:cleared" % ep_id)
        for lid in EPISODES[ep_id]["lessons"]:
            if persistent.lessons_unlocked is None:
                persistent.lessons_unlocked = set()
            persistent.lessons_unlocked.add(lid)
        renpy.save_persistent()
        if persistent.supabase_session and _session_user_id():
            sync_game_points()
    call screen episode_complete_modal(ep_id, summary_text)
    jump world_overview


################################################################################
## STORY 1: "NO KEYS, NO CHEESE"
## Pillar I: Keys & Sovereignty (Crypto Basis)
## POV: Koraba (The Creator — Acoustic-Electric Folk Instrument)
## Lessons: no_keys_no_cheese, vetting_admins, test_transaction
################################################################################

label ep1_keys:
    $ current_episode = "ep1_keys"
    $ current_pov = "Koraba (The Creator)"
    $ play_bad_music(force=True)

    ## --- THE HOOK: WORST-CASE SCENARIO (IN MEDIA RES) ---
    ## Lineup 1 (ep1_keys): Xochit (left) · Koraba (center) · Clara (right)
    scene bg lisbon_airport with fade
    show xochtl hurt at left
    show ashel alarmed at center_right
    show laylay stern at right

    narrator "Lisbon Airport Terminal, 11:42 p.m. Twelve crates of pressed herbal juices sit locked behind airport customs glass. Rain streaks the window. On your phone, the Essential Food & Medicine DAO treasury reads {b}0.00 NEAR{/b}."
    ashel "Sixty thousand dollars, Clara! Every concert I played, every bottle of herbal medicine we sold, every grant Xochit and I worked for — gone in one click?!"
    laylay "Lower your voice, Koraba. I copied the Brazil sanctuary's wallet address from our group chat as fast as I could. How was I supposed to know a scammer swapped the middle letters?"
    xochtl "You didn't send a single dollar first to check if my cacao cooperative actually received it. You sent all sixty thousand dollars at once to a fake address."
    show ashel alarmed at center_right
    ashel "Then open our backup reserve so we can at least pay the shipping crew and get everyone home!"
    laylay "I can't. That charming new admin we voted into the group last week already emptied the backup pool. And I hold the only remaining private key to the main wallet. You told me to 'handle the boring tech stuff,' remember?"
    show ashel hurt at center_left
    xochtl "We gave away our keys. We let a stranger into our treasury without checking his past. And we wired sixty thousand dollars blind."
    narrator "In the Discord chat, someone is typing in all-caps to blockchain support channels, begging for a bank refund that does not exist on a blockchain."

    ## --- THE REWIND ---
    call trigger_rewind(
        headline="« REWINDING 14 DAYS EARLIER",
        subline="POV: Koraba · Essential Food & Medicine Sanctuary Studio"
    )

    scene bg sanctuary with fade
    show xochtl warm at left
    show ashel neutral at center_left
    show laylay smirk at right

    narrator "Fourteen days before the flight. Warm sunlight shines through dried herbs and guitar cases in the sanctuary studio."
    narrator "You are {b}Koraba{/b}. You just finished recording a morning folk song, and forty crates of fresh herbal elixirs are packed for the community tour."
    xochtl "Drink your warm cacao, Koraba. Before we pay for the Brazil shipment, look at the laptop."
    show ashel focused at center_left
    ashel "What happened?"

    ## --- DECISION 1: KEY ROTATION & SOVEREIGNTY ---
label ep1_d1:
    scene bg sanctuary
    show xochtl neutral at left
    show ashel determined at center_left
    show laylay smirk at right

    xochtl "Someone uploaded a plain text file named {b}dao_seed_keys_FINAL.txt{/b} into our public Google Drive press folder last night. That file has our wallet's secret recovery words — our seed phrase. Automated bots have already scanned the folder."
    show ashel focused at center_right
    laylay "Ugh, managing crypto keys is too complicated for artists. Look, Koraba — you focus on the music and the juices. Just move all the group's money into my personal wallet. I'll hold the keys by myself and pay bills for you."

    menu:
        "Use key rotation right now to cancel the leaked key, and move the treasury into a 2-of-3 shared multisig wallet (Koraba, Xochit, and Clara).":
            show ashel determined at center_right
            ashel "No. 'No keys, no cheese.' If the creators who build the project don't hold keys to the wallet, we aren't a cooperative — we're just begging an administrator for our own money."
            show ashel proud at center_left
            xochtl "Exactly. On the NEAR blockchain, we can do a {b}key rotation{/b} right now. That deletes the leaked private key and replaces it with three fresh hardware keys in a 2-of-3 {b}non-custodial{/b} {b}multisig{/b} — where any two of us must sign to approve a payment."
            show ashel neutral at center_right
            laylay "Fine, fine! Two-out-of-three it is. Though you're making me wait for your signatures on every invoice."
            call lesson("no_keys_no_cheese")

        "Let Clara hold all the money in her personal wallet — you're an artist, not a tech admin.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "You're right, Clara. Take all the keys so I can finish mixing the album."
            narrator "Three weeks later, while you're stranded on tour waiting for travel money, Clara decides your music budget is 'unnecessary' and pays herself a bonus instead."
            laylay "My keys, my rules, Koraba. You don't even have a key on the wallet to vote against me."
            call checkpoint_bad_end(
                "ep1_d1",
                "Locked Out of Your Own Treasury: 'No Keys, No Cheese'",
                "By letting one administrator hold the only key to the treasury, Koraba gave up all control. When a disagreement happened, the creators who made all the value were locked out of their own funds.",
                "no_keys_no_cheese"
            )

        "Leave the secret keys in Google Drive — just rename the file to 'recipes_backup.txt' so hackers won't look inside.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "Let's just rename the file in Google Drive. Nobody will open 'recipes_backup.txt'."
            narrator "Hacker bots don't care what a file is named — they automatically scan every word inside shared folders for 12-word seed phrases and private keys. Eleven minutes later, your entire treasury is stolen."
            call checkpoint_bad_end(
                "ep1_d1",
                "Leaked Keys Stolen by Bots",
                "Secret keys stored in cloud text files are stolen automatically by bots within minutes. Renaming the file does nothing — only rotating the keys on-chain or moving funds to a brand-new multisig wallet saves your money.",
                "no_keys_no_cheese"
            )

    ## --- DECISION 2: TRUST & VETTING NEW DAO ADMINISTRATORS ---
label ep1_d2:
    scene bg sanctuary with dissolve
    show xochtl neutral at left
    show ashel neutral at center_right
    show laylay neutral at right

    narrator "Five days later. Your new 2-of-3 shared wallet is safe and working smoothly."
    laylay "Since we're growing fast, I invited a wonderful operations manager I met at a festival party — 'Kestrel.' He wants to join our DAO council today with full power to move treasury money."
    show ashel focused at center_left
    xochtl "Wait. Has anyone checked Kestrel's past wallet history or spoken to the last two groups he worked with?"
    show ashel neutral at center_right
    laylay "Oh, don't be so suspicious, Xochit! He wore a hand-woven poncho and talked about earth-friendly finance for two hours. The vibes were amazing! Here, sign the proposal to give him full admin keys."

    menu:
        "Pause the vote: check Kestrel's past wallet transactions, call his previous groups, and only offer limited trial permissions first.":
            show ashel determined at center_right
            ashel "Good vibes are great for music jams, not for treasury keys. Let's check his wallet history on the blockchain and call his last group before we sign anything."
            show ashel alarmed at center_left
            xochtl "Look at this public transaction record... Kestrel's wallet emptied a $40,000 community grant from a solar cooperative six months ago and disappeared."
            laylay "I... I had no idea. He sounded so kind at the tea bar."
            show ashel determined at center_right
            ashel "That's why we do due diligence first and only give limited permissions to new contributors. I'm rejecting his nomination right now."
            call lesson("vetting_admins")

        "Give Kestrel full admin keys right away — questioning him would hurt the friendly mood of the group.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "We're building a family based on trust. I'll sign his full admin key."
            narrator "At 3:00 a.m. that Sunday, Kestrel uses his new admin power to empty your reserve pool into an anonymous wallet and deletes his chat account."
            xochtl "Charm is not a background check, Koraba. Blockchain wallets don't care how spiritual someone sounded at a party."
            call checkpoint_bad_end(
                "ep1_d2",
                "Robbed by an Unchecked Administrator",
                "Giving a newcomer full wallet permissions without checking their past history handed your community's money straight to a repeat scammer.",
                "vetting_admins"
            )

        "Send Kestrel the backup wallet seed phrase in a private message for a '48-hour trial' to see if he's honest.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "Here, Kestrel — take our backup seed phrase just for the weekend so we can see how you work."
            narrator "A seed phrase cannot be 'borrowed for a weekend.' Anyone who sees those 12 secret words owns the wallet forever. On Monday morning, Kestrel takes every cent."
            call checkpoint_bad_end(
                "ep1_d2",
                "There Is No Such Thing as a 'Trial Seed Phrase'",
                "Once you share a raw seed phrase or private key, that person has permanent access forever. New contributors should only ever get limited, revocable permissions.",
                "vetting_admins"
            )

    ## --- DECISION 3: THE $60,000 TRANSFER & THE $1 TEST TRANSACTION ---
label ep1_d3:
    scene bg sanctuary with dissolve
    show xochtl warm at left
    show ashel determined at center_right
    show laylay neutral at right

    narrator "Departure afternoon. All sixty thousand dollars of community funds are safe in your 2-of-3 shared wallet. Now it's time to send the $60,000 payment to the Brazil sanctuary so the cargo and flights clear."
    laylay "Hurry! The shipping desk closes in twenty minutes. I pasted the sanctuary's wallet address into the payment window for the full $60,000. Click 'Approve' right now so we don't miss the plane!"
    show ashel focused at center_left
    xochtl "Hold on. Where did you copy that wallet address from, Clara?"
    show ashel determined at center_right
    laylay "From a message forwarded in our group chat! Look, the first four letters match: {b}0x7F4c...{/b} Come on, Koraba, sign it — we're out of time!"

    menu:
        "Refuse to rush: send a $1 test transaction first, confirm on a video call that the $1 arrived safely, and only then send the remaining $59,999.":
            show ashel determined at center_right
            ashel "Stop. Nobody sends sixty thousand dollars in one blind click. On a blockchain there is no bank manager and no undo button."
            show ashel focused at center_left
            xochtl "Send a {b}test transaction{/b} of one single dollar first. I have our Brazil sanctuary treasurer on a live video call right now."
            narrator "You send $1.00 to the address Clara pasted. Thirty seconds pass. On the video call, the sanctuary treasurer shakes her head — nothing arrived."
            xochtl "She didn't get the dollar! Look closely at the middle letters of Clara's address — a scammer posted a fake lookalike address in the chat!"
            show ashel alarmed at center_right
            laylay "Oh my goodness... the first four and last four letters matched, but the middle belonged to a thief. If we had sent all $60,000..."
            show ashel determined at center_left
            ashel "We would have lost everything. Now let's scan the real address directly from the treasurer's verified screen, send a $1 test transaction to be 100%% sure, and then wire the remaining $59,999."
            narrator "The $1 test arrives in four seconds. The $59,999 follows safely into the real sanctuary wallet."
            call lesson("test_transaction")

        "Click 'Approve' on the full $60,000 right now so you don't miss the shipping deadline!":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "We're out of time — sending all $60,000 now!"
            narrator "The payment finishes in one second. Five minutes later, the Brazil sanctuary calls: their wallet is still empty. The address in the chat was a fake lookalike planted by a scammer."
            narrator "For three days, Clara posts desperate messages in online forums asking how to 'cancel a mistaken crypto transfer.' There is no cancel button."
            call checkpoint_bad_end(
                "ep1_d3",
                "The $60,000 Wrong-Address Disaster",
                "Rushing a huge payment without sending a $1 test transaction first sent $60,000 straight to a scammer's lookalike address. Blockchain transfers are permanent.",
                "test_transaction"
            )

        "Only check the first 4 letters of the address ('0x7F4c') and send all $60,000 without a test transfer.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "The first four letters say 0x7F4c — that's good enough for me. Sending all $60,000!"
            narrator "Scammers use computer programs to create fake addresses that match the first four and last four letters of real wallets. Every cent disappears."
            call checkpoint_bad_end(
                "ep1_d3",
                "Fooled by a Lookalike Address",
                "Checking only the first four letters of a wallet address is never safe. Always check the full address and send a $1 test transaction before moving large sums.",
                "test_transaction"
            )

    ## --- EPISODE 1 RESOLUTION ---
    $ play_menu_music(force=True)
    scene expression EPISODES[current_episode]["cg_happy"] with fade

    narrator "At the Lisbon airport that night, all twelve crates of herbal elixirs clear customs smoothly. The Brazil sanctuary confirms all $60,000 in its account, and your 2-of-3 shared wallet keys rest safely at your side."
    xochtl "Leaked keys replaced. Scammers filtered out. One dollar tested before sixty thousand moved."
    ashel "And our community's work is safe."

    call complete_episode(
        "ep1_keys",
        "You replaced the leaked keys with a 2-of-3 shared multisig wallet, checked a newcomer's past before handing over admin power, and caught a fake address with a $1 test transaction before wiring $60,000."
    )


################################################################################
## STORY 2: "FROZEN PAY, EMPTY STAGE"
## Pillar II: Collaboration & Co-op = Winning Together (The "Amy & Edward / Jena" Story)
## POV: Xochit (The Shaman) & Koraba (The Creator)
## Lessons: creator_vs_admin, coop_solidarity, burnout
################################################################################

label ep2_lisbon:
    $ current_episode = "ep2_lisbon"
    $ current_pov = "Xochit & Koraba"
    $ play_bad_music(force=True)

    ## --- THE HOOK: WORST-CASE SCENARIO (IN MEDIA RES) ---
    ## Lineup 2 (ep2_lisbon): Koraba (left) · Xochit (center) · Clara (right)
    scene bg showcase_backstage with fade
    show ashel alarmed at left
    show xochtl focused at center_right
    show laylay stern at right

    narrator "Backstage at the Lisbon Showcase, three hours before doors open. Projectors warm up across the main hall. Koraba hasn't slept in two days — he built the entire interactive showcase game, recorded the original folk-electronic soundtrack, and delivered everything on time."
    ashel "The game is ready on stage, Clara! Why did you just block my 18,000 USDC payment?!"
    laylay "Because I think your ego has gotten way too big, Koraba. Everyone at the festival keeps calling this 'Koraba's masterpiece' as if my admin work doesn't matter. I'm freezing your pay until you act more humble."
    show xochtl focused at center_left
    ashel "I paid the sound crew out of my own pocket! If you freeze my pay after I already delivered the work, I'm deleting the game off the stage computers right now!"
    show xochtl stern at center_right
    xochtl "Stop — both of you! If Koraba deletes the game and Clara locks the money, our whole cooperative falls apart on stage in three hours!"

    ## --- THE REWIND ---
    call trigger_rewind(
        headline="« REWINDING 10 DAYS EARLIER",
        subline="POV: Xochit & Koraba · Preparing the Lisbon Showcase Game"
    )

    scene bg cacao_circle with fade
    show ashel neutral at left
    show xochtl warm at center_left
    show laylay smirk at right

    narrator "Ten days before the Lisbon event. You are {b}Xochit{/b}, pouring warm ceremonial cacao for the team while Koraba tunes his instrument and tests the interactive game scenes."
    show xochtl focused at center_right
    narrator "You notice a quiet change in {b}Clara{/b}: at first she admired how quickly Koraba created the music, art, and code. Now that admiration is turning into jealousy."

    ## --- DECISION 1: OBJECTIVE ESCROW VS. SUBJECTIVE GATEKEEPING ---
label ep2_d1:
    scene bg cacao_circle
    show ashel neutral at left
    show xochtl focused at center_right
    show laylay smirk at right

    laylay "About the 18,000 USDC budget for Koraba's Lisbon game — let's not lock it into an automatic agreement. Just leave the money in my admin queue, and I'll decide how much Koraba deserves after I see how I feel in Lisbon."

    menu:
        "Lock the 18,000 USDC in an objective smart-contract escrow that pays out automatically when the playable game and music files are delivered.":
            show xochtl stern at center_right
            xochtl "When creators pour their heart into a project, their pay cannot depend on an administrator's mood on delivery day. We're locking the budget in {b}escrow{/b} — a neutral smart contract that releases payment automatically when the agreed work is delivered."
            show xochtl warm at center_left
            ashel "The playable game passes testing, the music files are uploaded, and the payment releases fairly. Simple and clear."
            show xochtl focused at center_right
            laylay "Hmph. You act like you don't trust me! Fine, put the main 12,000 USDC in automatic escrow — though the final 6,000 USDC bonus module still goes through my admin approval button."
            call lesson("creator_vs_admin")

        "Let Clara decide the payment after delivery based on 'how humble Koraba's attitude feels.'":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            xochtl "Let's just trust Clara to decide the payout in Lisbon."
            narrator "On showcase morning, jealous of the crowd cheering for Koraba's music, Clara claims his attitude is 'unaligned' and refuses to pay him a cent. Koraba walks out and the event collapses."
            call checkpoint_bad_end(
                "ep2_d1",
                "Admin Gatekeeping Freezes Creator Pay",
                "Leaving a creator's payment up to an administrator's personal feelings allowed jealousy to block payment for finished work. Always lock creative budgets in objective milestone escrow.",
                "creator_vs_admin"
            )

        "Ask Koraba to build the entire game and soundtrack for free 'for exposure' so nobody argues over money.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            xochtl "What if you just build the whole Lisbon showcase for free, Koraba?"
            ashel "I can't pay the sound engineers or my rent with 'exposure,' Xochit. While the administrators take steady paychecks, the artists work for nothing?"
            narrator "Exhausted and broke, Koraba burns out four days before Lisbon, leaving an unfinished game and a broken team."
            call checkpoint_bad_end(
                "ep2_d1",
                "Creator Burnout from Unpaid Labor",
                "Expecting creators to work for free while administrators control the money destroys team morale and causes severe burnout.",
                "creator_vs_admin"
            )

    ## --- DECISION 2: THE "AMY & EDWARD / JENA" AVATAR PLAY (CO-OP SOLIDARITY) ---
label ep2_d2:
    scene bg showcase_backstage with dissolve
    show ashel hurt at left
    show xochtl neutral at center_left
    show laylay stern at right

    narrator "Two days before the Lisbon showcase, you meet in the venue's backstage production room. The main escrow paid out cleanly, but Clara just rejected Koraba's final 6,000 USDC game module in the admin portal — claiming the code and art are 'low quality and unusable.'"
    ashel "She didn't even open the file! Look at the server log — zero downloads from her computer. She clicked 'Reject' thirty seconds after seeing my name on the upload because people at the welcome dinner praised my music!"
    show xochtl focused at center_left
    xochtl "I see it, Koraba. Her admiration turned into jealousy, and now she's blocking anything with your name on it. But if we scream at her in public chat, she'll act like the victim and lock the whole wallet."
    ashel "Then how do we prove to the council that she's rejecting me out of pure personal bias AND get the finished work approved?"

    menu:
        "Use Xochit's 'Neutral Avatar' plan: quietly resubmit Koraba's exact same game file under an anonymous teammate username ('solstice_dev_09') with Koraba's wallet address attached.":
            show xochtl warm at center_left
            xochtl "Don't change a single line of code, Koraba. Hand me the file. I'm submitting your exact same build under a neutral contributor handle — {b}solstice_dev_09{/b} — with your payout address underneath."
            narrator "Twenty minutes later, Clara posts a glowing message in the council channel."
            show xochtl focused at center_right
            laylay "Everyone look at {b}solstice_dev_09{/b}'s upload! I just approved it for the full 6,000 USDC! See, Koraba? THIS is what clean, humble game design looks like — unlike the mess you uploaded!"
            show xochtl stern at center_right
            xochtl "Look at the digital file fingerprint on the blockchain, Clara. Byte for byte, {b}solstice_dev_09{/b} is the exact same file Koraba submitted two hours ago. And you just approved and paid for it."
            laylay "Wait — what?! That's... you tricked me!"
            show xochtl proud at center_left
            ashel "No, Xochit proved to the whole group that my work was spotless and your rejection was 100%% personal jealousy. And the 6,000 USDC just arrived in my wallet."
            call lesson("coop_solidarity")

        "Start a public shouting match in the festival chat group and threaten to smash the stage equipment.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "I'm going to call Clara out in the main festival chat right now!"
            laylay "Look how angry and unstable Koraba is acting, everyone! Clearly I was right to hold back the money."
            narrator "Festival sponsors pull out within an hour, and outsiders side with Clara's calm messages over Koraba's public outburst."
            call checkpoint_bad_end(
                "ep2_d2",
                "Public Outburst Plays Into the Gatekeeper's Hands",
                "Fighting unfair gatekeeping with an angry public meltdown lets the administrator paint the creator as 'unstable.' Clever teamwork and clear proof win where anger fails.",
                "coop_solidarity"
            )

        "Stay quiet, give up the 6,000 USDC, and let Clara take stage credit for Koraba's game.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            xochtl "Just let the money go, Koraba. Keep the peace."
            narrator "At the Lisbon showcase, Clara takes the stage microphone for forty minutes as 'Lead Visionary' while Koraba sits unpaid in the back row. On Monday, Koraba quits the collective forever."
            call checkpoint_bad_end(
                "ep2_d2",
                "Silence Rewards the Gatekeeper",
                "Allowing an administrator to withhold creator pay and steal credit drives away the very people who build the group's real value.",
                "coop_solidarity"
            )

    ## --- DECISION 3: RESTRUCTURING FOR CO-OP RECIPROCITY & PREVENTING BURNOUT ---
label ep2_d3:
    scene bg showcase_backstage with dissolve
    show ashel proud at left
    show xochtl warm at center_left
    show laylay defensive at right

    narrator "Still in the venue's backstage production room, the file proof is open on the laptop. The whole council now sees how one person holding unchecked admin power nearly ruined the Lisbon showcase."
    ashel "My payment arrived and the game is ready for the main stage tonight. But if we keep the exact same setup, this same fight will happen again next month."
    show xochtl focused at center_right
    xochtl "How should we redesign our roles so our cooperative truly wins together?"

    menu:
        "Set up rotating admin signers elected by the group, peer review for creative work, and paid rest breaks after big projects so nobody burns out.":
            show xochtl proud at center_right
            xochtl "No more permanent gatekeepers. Admin signers will rotate every three months by team vote, creative work will be reviewed fairly by fellow builders, and every major project includes paid rest."
            show xochtl warm at center_left
            ashel "Now that's a cooperative where I can pour my heart into the music without burning out."
            show xochtl warm at center_right
            laylay "Rotating signers... and shared peer review. Honestly, holding all the admin pressure alone was turning me into someone I didn't even like. I'm in."
            call lesson("burnout")

        "Fire Clara and make Koraba do 100%% of the music, coding, accounting, and admin paperwork alone.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "Give me every key, every spreadsheet, every tax form, and every creative project!"
            narrator "After three weeks of trying to write music, press herbal juices, pay invoices, and manage legal paperwork alone at 4:00 a.m., Koraba collapses from complete burnout."
            call checkpoint_bad_end(
                "ep2_d3",
                "Solo-Boss Burnout Collapse",
                "Forcing the lead creator to also do 100% of the administration alone guarantees exhaustion and burnout. A cooperative needs both creators and administrators working in balance.",
                "burnout"
            )

        "Keep the exact same rules and just hope Clara 'promises to be nicer next time.'":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            laylay "I promise I'll totally be nicer at the next event!"
            narrator "Because the rules didn't change, the very next project runs into the exact same payment freeze, and half the team quits to start a rival fork."
            call checkpoint_bad_end(
                "ep2_d3",
                "Wishes Don't Fix Broken Rules",
                "Relying on personal promises instead of fixing the group's rules leaves everyone open to the exact same abuse next month.",
                "creator_vs_admin"
            )

    ## --- EPISODE 2 RESOLUTION ---
    $ play_menu_music(force=True)
    scene expression EPISODES[current_episode]["cg_happy"] with fade

    narrator "That night on the Lisbon showcase stage, the interactive game brings the crowd to its feet. Koraba's live strings echo across the projection dome, Xochit welcomes two hundred new cooperative members, and the escrow payment settles automatically."
    xochtl "When creators are backed by fair agreements and teamwork, we all win together."

    call complete_episode(
        "ep2_lisbon",
        "You protected creator pay with automatic milestone escrow, used Xochit's anonymous submission to prove and defeat admin bias peacefully, and set up rotating cooperative leadership."
    )


################################################################################
## STORY 3: "BLOOD, CACAO & PAPER"
## Pillar III: Make & Enforce Agreements (Importance of Law/Legal for Innovators)
## POV: Koraba & Xochit
## Lessons: agreements_law, vesting, partnership
################################################################################

label ep3_agreements:
    $ current_episode = "ep3_agreements"
    $ current_pov = "Koraba & Xochit"
    $ play_bad_music(force=True)

    ## --- THE HOOK: WORST-CASE SCENARIO (IN MEDIA RES) ---
    ## Lineup 3 (ep3_agreements): Clara (left) · Xochit (center) · Koraba (right)
    scene bg cacao_circle with fade
    show laylay alarmed at left
    show xochtl hurt at center_right
    show ashel alarmed at right

    narrator "A court officer walks past the incense burner and drops a thick legal lawsuit onto the ceremonial cacao table. At the exact same moment, your phone buzzes: your group's token price just crashed 78%%."
    ashel "What is happening?! That early co-founder who quit in Week Two after making three slides — how did he just sell off thirty-three percent of all our tokens?!"
    laylay "Because we did an equal 33%% handshake split on Day One with no written vesting agreement! He kept all those tokens the second he walked out the door."
    show xochtl hurt at center_left
    xochtl "And why does this court lawsuit list my personal home address and Koraba's personal bank account?!"
    laylay "The stage company whose sound rig broke at our festival is suing the DAO for $140,000. Because we refused to register a legal company wrapper — calling contracts 'old-world paper' — the court ruled our group is an unwrapped general partnership. Every one of us is personally responsible for the whole debt!"

    ## --- THE REWIND ---
    call trigger_rewind(
        headline="« REWINDING TO DAY 3 — THE FOUNDING CACAO CIRCLE",
        subline="POV: Koraba & Xochit · Writing the Cooperative's Agreements"
    )

    scene bg cacao_circle with fade
    show laylay neutral at left
    show xochtl warm at center_left
    show ashel neutral at right

    narrator "Day 3 of the project. Warm steam rises from clay cacao cups. Everyone is excited — music, herbal medicine, and big dreams are flowing fast."
    narrator "{b}Xochit{/b} places a clean three-page founder agreement and cooperative charter beside the cacao pot while {b}Clara{/b} opens the notebook."
    show xochtl warm at center_right
    ashel "The music feels great and everyone trusts each other right now. Do we really need written contracts and lawyers in a creative sanctuary?"
    show xochtl focused at center_right
    xochtl "Listen closely, Koraba. How we write down our ownership, our legal protection, and our money rules today decides whether this sanctuary survives its first storm."

    ## --- DECISION 1: WRITTEN VESTING & CLIFFS VS. HANDSHAKE SPLITS ---
label ep3_d1:
    scene bg cacao_circle
    show laylay neutral at left
    show xochtl focused at center_right
    show ashel neutral at right

    xochtl "First: how will we divide ownership shares and voting tokens among the co-founders?"

    menu:
        "Sign a written 4-year vesting agreement with a 1-year cliff — founders earn their shares gradually by staying and doing the work.":
            $ equity = "vesting"
            ashel "Real commitment is proven over time. If someone quits in month two, they shouldn't walk away with a third of the sanctuary's future."
            show xochtl focused at center_right
            xochtl "We'll use four-year {b}vesting{/b} with a one-year {b}cliff{/b}. That means you earn your share over four years, and if anyone leaves before the first year is up, their unearned shares stay with the group — no {b}dead equity{/b} on our {b}cap table{/b}."
            show xochtl warm at center_left
            laylay "Smart and clear. Written in plain English and enforced automatically by the token contract."
            call lesson("vesting")

        "Do a 'Sacred 33/33/33 Handshake Split' with all tokens unlocked on Day 1 — written contracts feel too corporate!":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "No cliffs, no paperwork! Equal unlocked shares for everyone right now!"
            narrator "Two weeks later, an early co-founder loses interest, stops showing up, and sells his entire 33%% token share on the open market — crashing the treasury and leaving the working team with dead equity."
            call checkpoint_bad_end(
                "ep3_d1",
                "The Day-One Handshake Split & Token Dump",
                "Giving co-founders 100% of their shares on Day 1 without a 4-year vesting schedule and 1-year cliff lets early quitters walk away with a huge piece of the project and dump it on the people doing the work.",
                "vesting"
            )

        "Promise to 'figure out who owns what in a year or two' after the project makes money.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "Let's not talk about ownership numbers now — we'll sort it out once we're rich!"
            narrator "The day the first $100,000 grant arrives, three founders remember three totally different verbal promises. The group tears itself apart in bitter arguments."
            call checkpoint_bad_end(
                "ep3_d1",
                "Putting Off the Agreement Causes War",
                "Avoiding written ownership agreements early on guarantees an explosive fight the moment real money arrives.",
                "agreements_law"
            )

    ## --- DECISION 2: LEGAL WRAPPER VS. UNWRAPPED GENERAL PARTNERSHIP ---
label ep3_d2:
    scene bg cacao_circle with dissolve
    show laylay neutral at left
    show xochtl stern at center_right
    show ashel neutral at right

    narrator "Next, Xochit slides the second document across the table: registration papers for a {b}Cooperative LLC / Swiss Verein legal wrapper{/b}."
    xochtl "Right now, we are renting real-world event halls, shipping herbal drinks across borders, and voting on payments. Without a registered company — a {b}legal wrapper{/b} — courts treat our group as a {b}general partnership{/b}."
    ashel "Wait — doesn't calling ourselves a 'DAO' on the internet automatically protect our personal bank accounts?"
    show xochtl stern at center_left
    laylay "Not at all. In the Ooki DAO court case, the judge ruled that an unregistered DAO is a general partnership. That means any member who voted can be held personally responsible for 100%% of the group's lawsuits and debts."

    menu:
        "Register a formal Co-op LLC / Swiss Verein legal wrapper and written operating agreement before signing leases or moving money.":
            $ wrapper = "verein"
            show xochtl focused at center_right
            xochtl "Innovators moving fast need stronger legal armor, not weaker armor. Wrapping our DAO in a real cooperative company means the company signs contracts — so no artist or healer can lose their home over a business dispute."
            ashel "Blood, cacao, and paper. Our ceremony sets our heart; our legal wrapper protects our people in the real world."
            show xochtl warm at center_left
            laylay "Filed and stamped. Now the cooperative entity holds the liability, not our personal bank accounts."
            call lesson("partnership")

        "Refuse all legal companies — 'Code is Law, and government paperwork is for the old world!'":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "We don't register with any government! Code is law!"
            narrator "Six months later, a shipping company sues the group over a damaged festival crate. Because the DAO has no legal wrapper, the judge rules it a general partnership and freezes Koraba and Xochit's personal bank accounts."
            call checkpoint_bad_end(
                "ep3_d2",
                "Unlimited Personal Liability (The Ooki DAO Trap)",
                "A DAO with no legal company wrapper is treated by courts as a general partnership, leaving every active member personally on the hook for lawsuits and debts.",
                "partnership"
            )

        "Have Koraba put his personal name and credit card on every venue lease to save registration fees.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "I'll just sign all the festival contracts under my own name to save $2,000."
            narrator "When a festival sponsor fails to pay a $50,000 bill, debt collectors come straight after Koraba's personal guitars and apartment."
            call checkpoint_bad_end(
                "ep3_d2",
                "Never Sign Group Debts in Your Personal Name",
                "Putting one creator's personal name on group contracts leaves that person carrying 100% of the legal risk alone. Always sign through a shared legal wrapper.",
                "agreements_law"
            )

    ## --- DECISION 3: ENFORCEABLE RECOUPMENT & BARBELL TREASURY DISCIPLINE ---
label ep3_d3:
    scene bg cacao_circle with dissolve
    show laylay neutral at left
    show xochtl warm at center_right
    show ashel neutral at right

    narrator "Xochit turns to the final page of the agreement: {b}Treasury Safety & Paying Back Creator Expenses{/b}."
    xochtl "Koraba has already spent $12,000 of his own savings on studio gear and herbal bottles, and our community token just launched. How should we manage the group's money?"

    menu:
        "Write two clear rules into the charter: keep 50%% of the treasury in stable USDC cash (a barbell strategy) and pay back verified creator expenses automatically.":
            $ treasury_mix = "barbell"
            ashel "Putting fair {b}recoupment{/b} and a 50%% {b}stablecoin{/b} {b}barbell{/b} reserve in writing means nobody has to beg to be paid back for supplies, and a crypto market crash won't wipe out our rent money."
            show xochtl proud at center_right
            xochtl "Clear written agreements don't hurt the magic — they keep resentment out of the circle so the magic can last."
            show xochtl warm at center_left
            laylay "Agreement signed by all three of us and built directly into our shared wallet rules."
            call lesson("agreements_law")

        "Keep 100%% of the group's money in our own volatile token and leave expense payback to 'future good vibes.'":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            ashel "Let's keep 100%% of our money in our own token — trading any for stable cash looks weak!"
            narrator "When the crypto market dips, your token drops 85%% in a {b}death spiral{/b}. The group cannot pay shipping bills or pay Koraba back for the studio gear he bought."
            call checkpoint_bad_end(
                "ep3_d3",
                "Treasury Death Spiral & Unpaid Expenses",
                "Keeping 100% of your treasury in your own volatile token means your cash disappears right when the market dips, leaving creators unpaid for expenses they fronted.",
                "agreements_law"
            )

    ## --- EPISODE 3 RESOLUTION ---
    $ play_menu_music(force=True)
    scene expression EPISODES[current_episode]["cg_happy"] with fade

    narrator "Six months later, when an early speculator quits and a festival vendor disputes a bill, your written 1-year vesting cliff, Co-op legal wrapper, and 50%% USDC cash reserve protect everyone without a single crisis."
    xochtl "The cacao grounded our spirit. The written agreements protected our home."

    call complete_episode(
        "ep3_agreements",
        "You protected the group with a written 4-year vesting agreement and 1-year cliff, formed a real Co-op legal wrapper to shield members from personal lawsuits, and kept 50% of the treasury in stable USDC cash."
    )


################################################################################
## STORY 4: "ONE TIRED CLICK DRAINED THE APOTHECARY"
## Perspective Shift: Behind the Administrator's Ledger
## POV: Clara (The Administrator — Potions, Herbs & Multisig Keys)
## Lessons: capture, verify_hex, flashloan
################################################################################

label ep4_apothecary:
    $ current_episode = "ep4_apothecary"
    $ current_pov = "Clara (The Administrator)"
    $ play_bad_music(force=True)

    ## --- THE HOOK: WORST-CASE SCENARIO (IN MEDIA RES) ---
    ## Lineup 4 (ep4_apothecary): Koraba (left) · Clara (center) · Xochit (right)
    scene bg apothecary with fade
    show ashel alarmed at left
    show laylay alarmed at center_left
    show xochtl hurt at right

    narrator "Inside Clara's apothecary at 1:18 a.m., glass potion vials lie shattered across the floor. On her computer screen, a red alert flashes: {b}PROPOSAL EXECUTED — 100%% OF TREASURY TRANSFERRED TO 0xDEAD...BEEF{/b}."
    ashel "Clara, open the door! What did you just sign on our shared wallet?!"
    show laylay alarmed at center_left
    laylay "I didn't mean to! It was 1:14 in the morning, a popup said our wallet session was expiring, and the wealthy investor Atlas was pressuring me to rush his vote through!"
    xochtl "You gave Atlas a secret veto deal, turned off the 48-hour safety delay, and clicked 'Approve' on your hardware wallet without reading its screen?!"
    show laylay defensive at center_right
    laylay "Everyone thinks being the administrator is easy power — they don't see the fifty messages an hour, the rich investors offering bribes, and the phishing traps waiting for one tired mistake at 1:00 a.m.!"

    ## --- THE REWIND ---
    call trigger_rewind(
        headline="« REWINDING 48 HOURS EARLIER",
        subline="POV: Clara · Inside the Candlelit Apothecary"
    )

    scene bg apothecary with fade
    show ashel neutral at left
    show laylay calculating at center_left
    show xochtl neutral at right

    narrator "Forty-eight hours earlier. You are {b}Clara{/b}. Rows of dried lavender, glass potion bottles, and accounting ledgers line your desk beside your {b}hardware wallet{/b}."
    narrator "For the first time, you feel the heavy pressure on the administrator's shoulders: while Koraba and Xochit prepare the ceremony, your inbox is overflowing with thirty-two unpaid bills, tax forms, and a private voice message from {b}Atlas{/b}, a wealthy crypto {b}whale{/b}."

    ## --- DECISION 1: RESISTING PLUTOCRATIC CAPTURE ---
label ep4_d1:
    scene bg apothecary
    show ashel focused at left
    show laylay stern at center_left
    show xochtl stern at right

    laylay "Listen to this offer Atlas just sent me: he wants to put 80 ETH into our apothecary treasury today — on one condition."
    ashel "What condition?"
    show laylay calculating at center_left
    laylay "He wants 35%% of all our voting tokens and a secret side-agreement so he and I can push proposals through without waiting for the rest of the cooperative to vote."

    menu:
        "Reject the secret deal: limit any single investor to 8%% voting power and keep all terms 100%% public to the cooperative.":
            show laylay stern at center_right
            laylay "My job as administrator is to guard this apothecary, not sell control of it in a backroom deal. We can welcome outside supporters, but no single {b}whale{/b} gets more than 8%% voting power, and every agreement stays public."
            xochtl "Thank you, Clara. Handing a wealthy outsider a massive voting block always looks like easy money until they take over the group — that's {b}governance capture{/b}."
            show laylay neutral at center_left
            ashel "Eight percent limit, public rules only. The sanctuary stays in the community's hands."
            call lesson("capture")

        "Accept Atlas's secret deal — let the whale and administrator run everything quietly behind the scenes.":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            laylay "Deal. Between his 35%% vote and my admin key, we'll run the group quietly."
            narrator "Two weeks later, Atlas uses his 35%% voting block to cancel the sanctuary budget, vote all the treasury money to his own fund, and fire Koraba, Xochit, and finally you."
            call checkpoint_bad_end(
                "ep4_d1",
                "Governance Capture by a Wealthy Whale",
                "Selling a huge chunk of voting power to one wealthy investor in exchange for fast money lets them outvote the community and empty the treasury.",
                "capture"
            )

    ## --- DECISION 2: VERIFYING HARDWARE CALLDATA HEX AT 1:14 A.M. ---
label ep4_d2:
    scene bg apothecary with dissolve
    show laylay calculating at center_right
    show xochtl focused at right

    narrator "Night two in the apothecary. It is 1:14 a.m. You just finished bottling herbal orders and logging thirty-two contributor payments. Your eyes are burning with fatigue."
    narrator "Suddenly, an urgent direct message pops up from an account using the exact logo of your wallet app: {b}'URGENT: Wallet Sync Error. Click here and sign now or tomorrow's Brazil Sanctuary payment will fail!'{/b}"
    narrator "You click the link. Your computer screen shows a friendly button saying 'Re-Sync Wallet.' However, when you look down at the tiny screen on your physical {b}hardware wallet{/b}, the raw data ({b}hex{/b}) says `{b}setApprovalForAll{/b}` — giving an unknown contract permission to take every token in the vault!"

    menu:
        "Stop immediately: trust the hardware wallet's tiny screen, close the fake link, and wait until morning to verify with the team.":
            show laylay alarmed at center_right
            laylay "Wait a second... my computer monitor says 'Re-Sync,' but my hardware wallet's tiny screen says `{b}setApprovalForAll{/b}`! That's a {b}phishing{/b} trap trying to trick me into giving away unlimited {b}token approval{/b}!"
            xochtl "Great catch, Clara! Hacked websites and fake links can lie on your computer screen, but the small screen on your hardware wallet shows what the transaction really does."
            show laylay stern at center_right
            laylay "New apothecary rule: never sign transactions after midnight, never click links in direct messages, and always read the hardware wallet screen before pressing confirm."
            call lesson("verify_hex")

        "Click 'Approve' on the hardware wallet without reading its tiny screen — you're tired and don't want the morning payment to be late!":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            laylay "I'm too tired to read the tiny screen — clicking approve!"
            narrator "The fake link was a phishing trap. The moment you press the button on your hardware wallet, the attacker's contract takes every dollar in the apothecary vault."
            call checkpoint_bad_end(
                "ep4_d2",
                "1:14 a.m. Blind-Signing Phishing Drain",
                "Computer screens and browser popups can be faked by scammers; only the physical hardware wallet screen shows the real transaction code (hex). Never sign in a rush late at night.",
                "verify_hex"
            )

    ## --- DECISION 3: DEFENDING AGAINST FLASH-LOAN GOVERNANCE CAPTURE ---
label ep4_d3:
    scene bg apothecary with dissolve
    show ashel determined at left
    show laylay stern at center_left
    show xochtl focused at right

    narrator "Morning sunlight fills the apothecary. Furious that you rejected his private deal, an attacker uses a {b}flash loan{/b} — borrowing $2,000,000 worth of voting tokens for just a few seconds — and submits {b}Proposal #44: 'Send 100%% of Apothecary Treasury to External Account.'{/b}"
    ashel "Clara! How did that attacker get forty percent of the votes in twelve seconds?!"
    show laylay stern at center_right
    xochtl "He didn't buy those tokens — he borrowed them for a single transaction using a flash loan! How did you set up our voting rules, Clara?!"

    menu:
        "Use a mandatory 48-hour time-lock waiting period and past-snapshot voting so borrowed flash-loan tokens cannot execute an instant theft.":
            $ timelocks = True
            show laylay smirk at center_right
            laylay "He thought our votes ran in the exact same second like the Beanstalk hack! I turned on a 48-hour {b}timelock{/b} waiting period and snapshot voting. Tokens borrowed today have zero voting power on a vote counted from last week's snapshot!"
            show laylay neutral at center_left
            ashel "And with 48 hours to react, our real community members show up in force — hitting 72%% {b}quorum{/b} to cancel Proposal #44 completely."
            show laylay neutral at center_right
            xochtl "When administration acts as a shield for the community instead of a boss over it, no whale or flash loan can break us."
            call lesson("flashloan")

        "Allow votes to run in the exact same second they pass with no waiting period (no time-lock) so things 'move fast.'":
            scene expression EPISODES[current_episode]["cg_disaster"] with vpunch
            laylay "We turned off time-locks so votes run in the exact same second!"
            narrator "Just like the real-world $181M Beanstalk hack, the attacker borrows the voting tokens, passes Proposal #44, steals the entire treasury, and pays back the flash loan inside a single 12-second blockchain block."
            call checkpoint_bad_end(
                "ep4_d3",
                "Drained in 12 Seconds by a Flash-Loan Vote",
                "Without a 24–48 hour time-lock delay between a vote passing and the money moving, an attacker can borrow millions of votes for a few seconds via a flash loan and empty the treasury immediately.",
                "flashloan"
            )

    ## --- EPISODE 4 RESOLUTION ---
    $ play_menu_music(force=True)
    scene expression EPISODES[current_episode]["cg_happy"] with fade

    narrator "Morning sunlight warms the amber apothecary jars. Koraba sets a fresh bottle of ginger elixir beside Clara's hardware wallet, and Xochit pours three warm cups of cacao."
    laylay "I used to think holding the admin keys meant holding power over you two. Now I get it: holding keys in a cooperative means holding the shield so we can build safely together."

    call complete_episode(
        "ep4_apothecary",
        "Stepping into Clara's shoes, you rejected a wealthy whale's secret takeover deal, caught a 1:14 a.m. phishing trap by reading the hardware wallet's tiny screen, and stopped a flash-loan attack with a 48-hour time-lock."
    )
