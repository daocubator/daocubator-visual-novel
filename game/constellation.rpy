# World Overview ("The First Constellation") & Lessons Codex
# vault: 01 Overview/Story Structure.md · 01 Overview/Game Systems.md · 05 Lessons/Lessons Index.md

init 5 python:
    _LESSON_NUM_CAT = {
        "no_keys_no_cheese": ("#16", "Pillar I · Keys & Sovereignty"),
        "vetting_admins":    ("#17", "Pillar I · Keys & Sovereignty"),
        "test_transaction":  ("#18", "Pillar I · Keys & Sovereignty"),
        "creator_vs_admin":  ("#19", "Pillar II · Collaboration & Co-op"),
        "coop_solidarity":   ("#20", "Pillar II · Collaboration & Co-op"),
        "agreements_law":    ("#21", "Pillar III · Make & Enforce Agreements"),
        "equal_split":       ("#01", "Pillar III · Agreements & Equity"),
        "vesting":           ("#02", "Pillar III · Agreements & Equity"),
        "partnership":       ("#03", "Pillar III · Law & Legal Wrappers"),
        "death_spiral":      ("#04", "Pillar III · Treasury Structure"),
        "recoupment":        ("#05", "Pillar III · Fair Recoupment"),
        "chargeback":        ("#06", "Operations & Fulfillment"),
        "overfunding":       ("#07", "Operations & Fulfillment"),
        "apathy":            ("#08", "Governance & Stewardship"),
        "capture":           ("#09", "Governance & Defense"),
        "flashloan":         ("#10", "Governance & Defense"),
        "credentials":       ("#11", "Pillar I · Keys & OpSec"),
        "verify_hex":        ("#12", "Pillar I · Hardware Verification"),
        "ice_phishing":      ("#13", "Pillar I · Front-End Security"),
        "burnout":           ("#14", "Pillar II · Co-op Sustainability"),
        "greenwash":         ("#15", "Verification & Due Diligence"),
    }

    def get_lesson_meta(lid):
        tup = LESSONS.get(lid, ("LESSON", "", ""))
        num, cat = _LESSON_NUM_CAT.get(lid, ("#--", "Core Lesson"))
        return {
            "number": num,
            "category": cat,
            "title": tup[0],
            "body": tup[1],
            "real_world": tup[2],
        }

    EPISODES = {
        "ep1_keys": {
            "num": "EPISODE I",
            "title": "No Keys, No Cheese",
            "pillar": "PILLAR I · KEYS & SOVEREIGNTY (CRYPTO BASIS)",
            "pillar_short": "Keys & Sovereignty",
            "color": "#E07A5F",
            "pov": "Ash El (The Creator — Acoustic-Electric Folk Instrument)",
            "cast": "Ash El · Lay-Lay · Xochtl",
            "pos": (450, 355),
            "label": "ep1_keys",
            "omg_title": "THE $60,000 SANCTUARY MELTDOWN",
            "omg_hook": (
                "Ash El is stranded at the Lisbon terminal with twelve crates of botanical pressings and his folk guitar. "
                "The Essential Food & Medicine DAO treasury just hit 0.00 NEAR. $60,000 meant for the Brazil sanctuary "
                "was blasted in a single panic transfer to a dead address — and Lay-Lay holds the only remaining admin key."
            ),
            "decisions_preview": [
                "D1 · Key Rotation & Sovereignty: After a plaintext key leak, rotate keys via NEAR account access keys & 2-of-3 multisig — or let Lay-Lay hold sole custody?",
                "D2 · Vetting New Admins: Audit a charismatic nominee's past treasury history and scope permissions — or fast-track them on vibes?",
                "D3 · The $1 Test Transaction: Send a $1 test transaction and verify receipt with Xochtl first — or wire all $60,000 in one blind click?",
            ],
            "lessons": ["no_keys_no_cheese", "vetting_admins", "test_transaction"],
        },
        "ep2_lisbon": {
            "num": "EPISODE II",
            "title": "The Lisbon Refusal",
            "pillar": "PILLAR II · COLLABORATION & CO-OP = WINNING TOGETHER",
            "pillar_short": "Collaboration & Co-op",
            "color": "#2EC4B6",
            "pov": "Xochtl (The Shaman — Ceremonial Cacao Cup) & Ash El",
            "cast": "Xochtl · Ash El · Lay-Lay",
            "pos": (1470, 355),
            "label": "ep2_lisbon",
            "omg_title": "THE SHOWCASE SABOTAGE",
            "omg_hook": (
                "Three hours before the Lisbon Web3 Cultural Showcase, Ash El's interactive game and soundtrack are finished — "
                "and Administrator Lay-Lay freezes his 18,000 USDC payout out of sheer ego and jealousy. "
                "Ash El is ready to delete the repository and walk away forever while the stage lights warm up."
            ),
            "decisions_preview": [
                "D1 · Objective Milestone Escrow: Lock creative bounties in pre-agreed smart-contract escrow — or leave payouts to an admin's personal mood?",
                "D2 · Co-op Solidarity (The Avatar Play): Pull Xochtl's clever neutral-avatar submission to prove bias on-chain — or blow up the collective in public?",
                "D3 · Rotating Stewardship: Restructure the DAO around co-op reciprocity and rotating signers — or crown a new unchecked gatekeeper?",
            ],
            "lessons": ["creator_vs_admin", "coop_solidarity", "burnout"],
        },
        "ep3_agreements": {
            "num": "EPISODE III",
            "title": "Blood, Cacao & Paper",
            "pillar": "PILLAR III · MAKE & ENFORCE AGREEMENTS (LAW & STRUCTURE)",
            "pillar_short": "Make & Enforce Agreements",
            "color": "#F2CC8F",
            "pov": "Ash El & Xochtl (Co-Creators at the Cacao Circle)",
            "cast": "Ash El · Xochtl · Lay-Lay",
            "pos": (450, 755),
            "label": "ep3_agreements",
            "omg_title": "THE SUMMONS & THE DEAD CAP TABLE",
            "omg_hook": (
                "A process server drops a personal liability lawsuit onto the ceremonial cacao altar while a vanished co-founder "
                "who left in Week 2 dumps 33% of the unvested governance tokens on the open market — crashing the treasury "
                "and leaving Ash El and Xochtl personally on the hook for every debt."
            ),
            "decisions_preview": [
                "D1 · Written Vesting & Cliffs: Put a 4-year vesting schedule with a 1-year cliff in writing — or trust a '33/33/33 sacred handshake'?",
                "D2 · Legal Wrapper vs. Counter-Culture Dogma: Form a Co-op LLC / Swiss Verein wrapper — or stay an unwrapped general partnership?",
                "D3 · Treasury Barbell & Recoupment: Split 50% into USDC operational runway with clear recoupment terms — or keep 100% in volatile governance tokens?",
            ],
            "lessons": ["agreements_law", "vesting", "partnership"],
        },
        "ep4_apothecary": {
            "num": "EPISODE IV",
            "title": "The Keys of the Apothecary",
            "pillar": "PERSPECTIVE SHIFT · BEHIND THE ADMINISTRATOR'S LEDGER",
            "pillar_short": "Perspective Shift (Lay-Lay POV)",
            "color": "#9B7EDE",
            "pov": "Lay-Lay (The Administrator — Potions, Herbs & Multisig Keys)",
            "cast": "Lay-Lay · Ash El · Xochtl",
            "pos": (1470, 755),
            "label": "ep4_apothecary",
            "omg_title": "THE APOTHECARY DRAIN AT 1:14 A.M.",
            "omg_hook": (
                "Step into Lay-Lay's candlelit apothecary. Surrounded by amber tinctures, ledger requests, and a whale's "
                "backroom bribe, a single 1:14 a.m. blind-signed transaction hands the entire DAO treasury and governance "
                "keys to a flash-loan attacker while Ash El and Xochtl bang on the door."
            ),
            "decisions_preview": [
                "D1 · Resisting Plutocracy: Reject a whale's private veto side-letter — or trade community sovereignty for fast capital?",
                "D2 · Verifying Hex on Hardware: Pause at 1:14 a.m. to verify hardware calldata hex and run a $1 test batch — or blind-sign a spoofed draining contract?",
                "D3 · Flash-Loan Defense: Enforce a 48-hour timelock and co-op delegation rally — or leave instant execution wide open?",
            ],
            "lessons": ["capture", "verify_hex", "flashloan"],
        },
    }

    EPISODE_ORDER = ["ep1_keys", "ep2_lisbon", "ep3_agreements", "ep4_apothecary"]


################################################################################
## Transforms for animated / glowing Constellation nodes

transform constellation_star_glow:
    alpha 0.90
    zoom 1.0
    linear 1.5 alpha 1.0 zoom 1.04
    linear 1.5 alpha 0.90 zoom 1.0
    repeat

transform constellation_orb_pulse:
    alpha 0.30
    zoom 0.94
    linear 1.6 alpha 0.70 zoom 1.12
    linear 1.6 alpha 0.30 zoom 0.94
    repeat

transform rewind_banner_flash:
    alpha 0.0
    zoom 1.12
    easein 0.25 alpha 1.0 zoom 1.0


################################################################################
## World Overview Hub Label

label world_overview:
    $ current_episode = None
    $ selected_constellation_node = None
    hide screen stats_hud
    scene bg constellation with dissolve
    call screen constellation_map
    return


################################################################################
## World Overview Screen — "The First Constellation"

screen constellation_map():
    tag menu
    modal True

    add "bg constellation"
    add "#100E0C77"

    ## Top Header Bar — Core Categories of Lessons
    frame:
        xalign 0.5
        ypos 16
        xsize 1840
        background "#181512EE"
        padding (32, 16)
        vbox:
            spacing 8
            hbox:
                xfill True
                vbox:
                    text "✦ THE FIRST CONSTELLATION — WORLD OVERVIEW" color "#F2CC8F" size 30
                    text "Click any glowing constellation node to inspect the disaster scenario, then rewind time and solve it in 3 choices." color "#D8D0C5" size 20
                hbox:
                    spacing 16
                    yalign 0.5
                    $ num_ep_done = len(persistent.episodes_completed or set())
                    $ num_lessons_done = len(persistent.lessons_unlocked or set())
                    frame:
                        background "#26211C"
                        padding (16, 8)
                        text "EPISODES: [num_ep_done]/4" color "#2EC4B6" size 20
                    frame:
                        background "#26211C"
                        padding (16, 8)
                        text "LESSONS: [num_lessons_done]/[len(LESSONS)]" color "#F2CC8F" size 20
                    textbutton "📖 LESSONS CODEX" action ShowMenu("lessons_codex") style "constellation_nav_btn"
                    textbutton "📚 GLOSSARY" action ShowMenu("glossary") style "constellation_nav_btn"

            ## The Core Lesson Pillars bar
            hbox:
                spacing 22
                xalign 0.5
                frame:
                    background "#241B17"
                    padding (18, 6)
                    text "● PILLAR I: KEYS & SOVEREIGNTY (Crypto Basis)" color "#E07A5F" size 18
                frame:
                    background "#162422"
                    padding (18, 6)
                    text "● PILLAR II: COLLABORATION & CO-OP = WINNING TOGETHER" color "#2EC4B6" size 18
                frame:
                    background "#262116"
                    padding (18, 6)
                    text "● PILLAR III: MAKE & ENFORCE AGREEMENTS (Law & Structure)" color "#F2CC8F" size 18
                frame:
                    background "#1F1A29"
                    padding (18, 6)
                    text "● PERSPECTIVE SHIFT: ADMIN & DEFENSE" color "#9B7EDE" size 18

    ## Center Hub Badge ("PRIMORDIA / EFAM CORE")
    frame:
        xalign 0.5
        yalign 0.54
        background "#181512DD"
        padding (26, 18)
        vbox:
            spacing 4
            xalign 0.5
            text "✦ PRIMORDIA ✦" color "#F2CC8F" size 25 xalign 0.5
            text "Essential Food & Medicine" color "#E07A5F" size 19 xalign 0.5
            text "Ash El · Lay-Lay · Xochtl" color "#2EC4B6" size 17 xalign 0.5

    ## Glowing Constellation Nodes for Each Playable Scenario
    for ep_id in EPISODE_ORDER:
        $ ep = EPISODES[ep_id]
        $ nx, ny = ep["pos"]
        $ is_done = ep_id in (persistent.episodes_completed or set())

        ## Pulsing outer aura
        frame:
            xpos nx
            ypos ny
            xanchor 0.5
            yanchor 0.5
            xsize 548
            ysize 244
            background "#2E261F77"
            at constellation_orb_pulse

        ## Interactive Node Card
        button:
            xpos nx
            ypos ny
            xanchor 0.5
            yanchor 0.5
            xsize 530
            padding (24, 18)
            background ("#1A2622F2" if is_done else "#1C1815F2")
            hover_background "#2B241FF8"
            at constellation_star_glow
            action Show("scenario_overview_modal", ep_id=ep_id)

            vbox:
                spacing 6
                hbox:
                    xfill True
                    text "[ep['num']] · [ep['pillar_short']]" color ep["color"] size 18
                    if is_done:
                        text "✓ RESOLVED" color "#52B788" size 18 xalign 1.0
                    else:
                        text "⚠ OMG DISASTER" color "#E07A5F" size 18 xalign 1.0

                text "✦ [ep['title']]" color "#F4EFE6" size 28
                text "Hook: [ep['omg_title']]" color "#F2CC8F" size 19
                text "POV: [ep['pov']]" color "#BEB5A7" size 17

                hbox:
                    spacing 12
                    ypos 4
                    for lid in ep["lessons"]:
                        $ lmeta = get_lesson_meta(lid)
                        $ l_unlocked = lid in (persistent.lessons_unlocked or set())
                        text ("★ " + lmeta["number"] if l_unlocked else "☆ " + lmeta["number"]) color ("#52B788" if l_unlocked else "#888075") size 16
                    text "→ Inspect Scenario" color ep["color"] size 17 xalign 1.0

    ## Bottom Bar
    frame:
        xalign 0.5
        yalign 0.98
        xsize 1840
        background "#181512EE"
        padding (28, 12)
        hbox:
            xfill True
            text "Each scenario starts at the moment of worst-case collapse, then rewinds ⏪ so you can test choices and retry any decision instantly." color "#BEB5A7" size 19 yalign 0.5
            hbox:
                spacing 20
                xalign 1.0
                textbutton "⚙ PREFERENCES" action ShowMenu("preferences") style "constellation_nav_btn"
                textbutton "🏠 MAIN MENU" action MainMenu(confirm=False) style "constellation_nav_btn"

    key "l" action ShowMenu("lessons_codex")
    key "g" action ShowMenu("glossary")


################################################################################
## Scenario Overview Modal — Previews the OMG Disaster & confirms dive-in

screen scenario_overview_modal(ep_id):
    modal True
    zorder 150
    $ ep = EPISODES[ep_id]
    $ is_done = ep_id in (persistent.episodes_completed or set())

    add "#0B0908E0"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1440
        background "#1B1714"
        padding (48, 38)

        vbox:
            spacing 18

            hbox:
                xfill True
                text "[ep['num']] · [ep['pillar']]" color ep["color"] size 22
                if is_done:
                    text "✓ SCENARIO RESOLVED" color "#52B788" size 22 xalign 1.0
                else:
                    text "⚠ UNRESOLVED DISASTER" color "#E07A5F" size 22 xalign 1.0

            text "[ep['title']]" color "#F4EFE6" size 42

            hbox:
                spacing 36
                text "{b}POV Character:{/b} [ep['pov']]" color "#2EC4B6" size 21
                text "{b}Core Cast:{/b} [ep['cast']]" color "#D8D0C5" size 21

            ## The Worst-Case Scenario Hook Box
            frame:
                xfill True
                background "#2A1816"
                padding (26, 20)
                vbox:
                    spacing 8
                    text "💥 THE WORST-CASE DISASTER HOOK: [ep['omg_title']]" color "#E07A5F" size 23
                    text "[ep['omg_hook']]" color "#F4EFE6" size 22

            ## The 3 Rewind Decisions & Crypto-Ethics Lessons
            frame:
                xfill True
                background "#221E1A"
                padding (26, 18)
                vbox:
                    spacing 8
                    text "⏪ THE REWIND CHALLENGE (3 CHECKPOINTED DECISIONS):" color "#F2CC8F" size 21
                    for d_text in ep["decisions_preview"]:
                        text "• [d_text]" color "#D8D0C5" size 19

            ## Lessons taught in this scenario
            hbox:
                spacing 14
                text "Core Lessons:" color "#BEB5A7" size 19 yalign 0.5
                for lid in ep["lessons"]:
                    $ lmeta = get_lesson_meta(lid)
                    $ l_unlocked = lid in (persistent.lessons_unlocked or set())
                    frame:
                        background ("#1A2E26" if l_unlocked else "#28231E")
                        padding (14, 6)
                        text ("[lmeta['number']]: [lmeta['title']]") color ("#52B788" if l_unlocked else "#F2CC8F") size 17

            null height 6

            ## Action Buttons: Confirm Dive-In or Exit to Keep Exploring
            hbox:
                spacing 36
                xalign 0.5
                textbutton "▶ DIVE IN & REWIND DISASTER" action [Hide("scenario_overview_modal"), Jump(ep["label"])] style "constellation_confirm_btn"
                textbutton "✕ KEEP EXPLORING CONSTELLATION" action Hide("scenario_overview_modal") style "constellation_cancel_btn"


################################################################################
## Lessons Codex Screen — Browse all 21 lessons in LESSONS

default selected_codex_lesson = "no_keys_no_cheese"

screen lessons_codex():
    tag menu
    modal True

    add "#12100E"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1780
        ysize 980
        background "#1B1714"
        padding (40, 32)

        vbox:
            spacing 18
            hbox:
                xfill True
                vbox:
                    text "📖 CRYPTO-ETHICS & CO-OP LESSONS CODEX" color "#F2CC8F" size 34
                    text "Every disaster teaches a structural rule. Review unlocked lessons or inspect any lesson below." color "#BEB5A7" size 20
                textbutton "✕ RETURN" action Return() style "constellation_cancel_btn" xalign 1.0 yalign 0.5

            hbox:
                spacing 30
                ysize 820

                ## Left column: scrollable list of all lessons
                frame:
                    xsize 680
                    yfill True
                    background "#14110F"
                    padding (18, 18)
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        vbox:
                            spacing 8
                            for lid in LESSONS.keys():
                                $ lmeta = get_lesson_meta(lid)
                                $ is_un = lid in (persistent.lessons_unlocked or set())
                                button:
                                    xfill True
                                    padding (14, 10)
                                    background ("#2D251E" if selected_codex_lesson == lid else "#1C1815")
                                    hover_background "#382E25"
                                    action SetScreenVariable("selected_codex_lesson", lid)
                                    hbox:
                                        spacing 12
                                        text ("★" if is_un else "☆") color ("#52B788" if is_un else "#777067") size 20 yalign 0.5
                                        vbox:
                                            text "[lmeta['number']] · [lmeta['title']]" color ("#F4EFE6" if selected_codex_lesson == lid else "#D8D0C5") size 18
                                            text "[lmeta['category']]" color "#E07A5F" size 15

                ## Right column: detail view of selected lesson
                $ cur_l = get_lesson_meta(selected_codex_lesson)
                $ cur_un = selected_codex_lesson in (persistent.lessons_unlocked or set())
                frame:
                    xfill True
                    yfill True
                    background "#221D19"
                    padding (36, 30)
                    vbox:
                        spacing 18
                        hbox:
                            xfill True
                            text "[cur_l['number']] · [cur_l['category']]" color "#F2CC8F" size 22
                            text ("✓ EXPERIENCED IN PLAY" if cur_un else "☆ PREVIEW MODE") color ("#52B788" if cur_un else "#BEB5A7") size 20 xalign 1.0
                        text "[cur_l['title']]" color "#F4EFE6" size 36
                        frame:
                            xfill True
                            background "#171411"
                            padding (26, 22)
                            text "[cur_l['body']]" color "#E8E2D9" size 24 line_spacing 6
                        frame:
                            xfill True
                            background "#1C2926"
                            padding (22, 16)
                            vbox:
                                spacing 6
                                text "REAL-WORLD PRECEDENT & RECEIPTS:" color "#2EC4B6" size 18
                                text "[cur_l['real_world']]" color "#D8D0C5" size 21


################################################################################
## Styles for Constellation & Modals

style constellation_nav_btn is button:
    background "#2B241E"
    hover_background "#3E332A"
    padding (18, 8)

style constellation_nav_btn_text is button_text:
    color "#F4EFE6"
    hover_color "#F2CC8F"
    size 19

style constellation_confirm_btn is button:
    background "#2EC4B6"
    hover_background "#45DFD0"
    padding (32, 16)

style constellation_confirm_btn_text is button_text:
    color "#12100E"
    hover_color "#000000"
    size 25

style constellation_cancel_btn is button:
    background "#2E2722"
    hover_background "#463B33"
    padding (28, 16)

style constellation_cancel_btn_text is button_text:
    color "#D8D0C5"
    hover_color "#FFFFFF"
    size 23
