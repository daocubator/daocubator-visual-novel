# World Overview ("The First Constellation" — Start Screen) & Lessons Codex
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
            "title": "No Keys, No Cheese",
            "pillar": "PILLAR I · KEYS & SOVEREIGNTY (CRYPTO BASIS)",
            "pillar_short": "Keys & Sovereignty",
            "color": "#E07A5F",
            "pov": "Ash El (The Creator)",
            "cast": "Ash El · Lay-Lay · Xochtl",
            "pos": (430, 340),
            "label": "ep1_keys",
            "cg_disaster": "images/cg_ep1_disaster.png",
            "cg_disaster_thumb": "images/cg_ep1_disaster_thumb.png",
            "cg_happy": "images/cg_ep1_happy.png",
            "cg_happy_thumb": "images/cg_ep1_happy_thumb.png",
            "omg_title": "The $60,000 Sanctuary Meltdown",
            "happy_title": "2-of-3 Multisig & Verified Transfer",
            "omg_hook": (
                "Ash El is stranded at the Lisbon airport terminal with twelve crates of botanical juices and his guitar. "
                "The Essential Food & Medicine DAO treasury just hit 0.00 NEAR. $60,000 meant for the Brazil sanctuary "
                "was sent in one rushed click to a fake address — and Lay-Lay holds the only remaining admin key."
            ),
            "decisions_preview": [
                "1 · Key Rotation & Shared Custody: After a secret key is leaked in a shared folder, rotate keys into a 2-of-3 shared wallet — or let one admin hold everything?",
                "2 · Vetting New Admins: Check a charming newcomer's past wallet history first — or hand them full treasury power on good vibes?",
                "3 · The $1 Test Transfer: Send $1 first and confirm on video that Xochtl's partner received it — or wire all $60,000 in one blind click?",
            ],
            "lessons": ["no_keys_no_cheese", "vetting_admins", "test_transaction"],
        },
        "ep2_lisbon": {
            "title": "The Lisbon Refusal",
            "pillar": "PILLAR II · COLLABORATION & CO-OP = WINNING TOGETHER",
            "pillar_short": "Collaboration & Co-op",
            "color": "#2EC4B6",
            "pov": "Xochtl (The Shaman) & Ash El",
            "cast": "Xochtl · Ash El · Lay-Lay",
            "pos": (1490, 340),
            "label": "ep2_lisbon",
            "cg_disaster": "images/cg_ep2_disaster.png",
            "cg_disaster_thumb": "images/cg_ep2_disaster_thumb.png",
            "cg_happy": "images/cg_ep2_happy.png",
            "cg_happy_thumb": "images/cg_ep2_happy_thumb.png",
            "omg_title": "The Showcase Sabotage",
            "happy_title": "Milestone Escrow & Co-op Solidarity",
            "omg_hook": (
                "Three hours before the Lisbon Showcase doors open, Ash El's interactive game and soundtrack are finished — "
                "and Administrator Lay-Lay freezes his 18,000 USDC payment out of jealousy. "
                "Ash El is ready to pull the game offline and walk away forever while the stage lights warm up."
            ),
            "decisions_preview": [
                "1 · Objective Milestone Escrow: Lock creative payouts in automatic smart-contract escrow — or leave payment up to an admin's personal mood?",
                "2 · Co-op Solidarity (The Neutral Avatar Play): Use Xochtl's clever anonymous submission to prove bias with math — or start a public screaming match?",
                "3 · Rotating Stewardship: Share admin duty through rotating signers and funded rest — or crown a new solo boss?",
            ],
            "lessons": ["creator_vs_admin", "coop_solidarity", "burnout"],
        },
        "ep3_agreements": {
            "title": "Blood, Cacao & Paper",
            "pillar": "PILLAR III · MAKE & ENFORCE AGREEMENTS (LAW & STRUCTURE)",
            "pillar_short": "Make & Enforce Agreements",
            "color": "#F2CC8F",
            "pov": "Ash El & Xochtl (Co-Creators)",
            "cast": "Ash El · Xochtl · Lay-Lay",
            "pos": (430, 760),
            "label": "ep3_agreements",
            "cg_disaster": "images/cg_ep3_disaster.png",
            "cg_disaster_thumb": "images/cg_ep3_disaster_thumb.png",
            "cg_happy": "images/cg_ep3_happy.png",
            "cg_happy_thumb": "images/cg_ep3_happy_thumb.png",
            "omg_title": "The Summons & The Dead Cap Table",
            "happy_title": "4-Year Vesting & Co-op Legal Shield",
            "omg_hook": (
                "A court officer drops a personal lawsuit onto the ceremonial cacao altar at the exact moment a former co-founder "
                "who quit in Week 2 sells off 33% of all tokens — crashing the treasury and leaving Ash El and Xochtl "
                "personally responsible for $140,000 in group debts."
            ),
            "decisions_preview": [
                "1 · Written Vesting & Cliffs: Earn founder shares over 4 years with a 1-year cliff — or split 33/33/33 on a Day 1 handshake?",
                "2 · Real-World Legal Wrapper: Register a formal Co-op LLC / Swiss Verein company wrapper — or stay an unprotected partnership?",
                "3 · Stable Reserve & Recoupment: Keep 50% of the treasury in stable USDC cash and pay back upfront creator costs — or bet 100% on your own volatile token?",
            ],
            "lessons": ["agreements_law", "vesting", "partnership"],
        },
        "ep4_apothecary": {
            "title": "The Keys of the Apothecary",
            "pillar": "PERSPECTIVE SHIFT · BEHIND THE ADMINISTRATOR'S LEDGER",
            "pillar_short": "Perspective Shift (Lay-Lay POV)",
            "color": "#9B7EDE",
            "pov": "Lay-Lay (The Administrator)",
            "cast": "Lay-Lay · Ash El · Xochtl",
            "pos": (1490, 760),
            "label": "ep4_apothecary",
            "cg_disaster": "images/cg_ep4_disaster.png",
            "cg_disaster_thumb": "images/cg_ep4_disaster_thumb.png",
            "cg_happy": "images/cg_ep4_happy.png",
            "cg_happy_thumb": "images/cg_ep4_happy_thumb.png",
            "omg_title": "The Apothecary Drain at 1:14 A.M.",
            "happy_title": "Hardware Hex Verified & Timelock Shield",
            "omg_hook": (
                "Step into Lay-Lay's candlelit apothecary. Surrounded by herbal jars, endless invoices, and a wealthy investor's "
                "backroom bribe, one exhausted click at 1:14 a.m. hands the entire DAO treasury to a flash-loan attacker "
                "while Ash El and Xochtl bang on the door."
            ),
            "decisions_preview": [
                "1 · Resisting Whale Capture: Reject a wealthy investor's secret veto deal and cap voting power at 8% — or trade away community control for fast cash?",
                "2 · Checking the Hardware Screen: Pause at 1:14 a.m. to read the hardware wallet's raw code screen — or blind-sign a fake emergency link?",
                "3 · Flash-Loan Defense: Use a 48-hour waiting period (time-lock) to stop a 12-second borrowed-vote attack — or allow instant same-second execution?",
            ],
            "lessons": ["capture", "verify_hex", "flashloan"],
        },
    }

    EPISODE_ORDER = ["ep1_keys", "ep2_lisbon", "ep3_agreements", "ep4_apothecary"]


################################################################################
## Transforms for animated / glowing Constellation nodes

transform constellation_star_glow:
    alpha 0.94
    zoom 1.0
    linear 1.6 alpha 1.0 zoom 1.02
    linear 1.6 alpha 0.94 zoom 1.0
    repeat

transform constellation_orb_pulse:
    alpha 0.25
    zoom 0.97
    linear 1.8 alpha 0.55 zoom 1.04
    linear 1.8 alpha 0.25 zoom 0.97
    repeat

transform rewind_banner_flash:
    alpha 0.0
    zoom 1.10
    easein 0.25 alpha 1.0 zoom 1.0

transform cg_modal_bg:
    size (1350, 432)
    fit "cover"


################################################################################
## World Overview Hub Label

label world_overview:
    $ _ensure_single_narrative()
    $ current_episode = None
    $ selected_constellation_node = None
    $ play_menu_music()
    hide screen stats_hud
    scene bg constellation with dissolve
    call screen constellation_map
    return


################################################################################
## World Overview Screen — "The First Constellation" (Start Screen & Episode Hub)

screen constellation_map():
    tag menu
    modal True

    add "bg constellation"
    add "#100E0C66"

    ## Top Header Bar — Game Title, Progress & Core Pillars
    frame:
        xalign 0.5
        ypos 12
        xsize 1860
        background "#181512F2"
        padding (28, 12)
        vbox:
            spacing 8
            hbox:
                xfill True
                vbox:
                    text "✦ GET RICH TOGETHER — THE FIRST CONSTELLATION" color "#F2CC8F" size 28
                    text "Click any story node below to witness the collapse, then rewind time and solve it in 3 decisions." color "#D8D0C5" size 18
                hbox:
                    spacing 12
                    xalign 1.0
                    yalign 0.5
                    $ num_ep_done = len(persistent.episodes_completed or set())
                    $ num_lessons_done = len(persistent.lessons_unlocked or set())
                    frame:
                        background "#26211C"
                        padding (14, 6)
                        text "RESOLVED: [num_ep_done]/4" color "#52B788" size 18
                    frame:
                        background "#26211C"
                        padding (14, 6)
                        text "LESSONS: [num_lessons_done]/[len(LESSONS)]" color "#F2CC8F" size 18
                    textbutton "★ LESSONS CODEX" action ShowMenu("lessons_codex") style "constellation_nav_btn"
                    textbutton "ˀ GLOSSARY" action ShowMenu("glossary") style "constellation_nav_btn"

            ## The Core Lesson Pillars bar — sized to fit cleanly inside 1860px
            hbox:
                spacing 14
                xalign 0.5
                frame:
                    background "#241B17"
                    padding (14, 4)
                    text "● PILLAR I: KEYS & SOVEREIGNTY" color "#E07A5F" size 16
                frame:
                    background "#162422"
                    padding (14, 4)
                    text "● PILLAR II: COLLABORATION & CO-OP = WINNING TOGETHER" color "#2EC4B6" size 16
                frame:
                    background "#262116"
                    padding (14, 4)
                    text "● PILLAR III: MAKE & ENFORCE AGREEMENTS" color "#F2CC8F" size 16
                frame:
                    background "#1F1A29"
                    padding (14, 4)
                    text "● PERSPECTIVE SHIFT: ADMIN & DEFENSE" color "#9B7EDE" size 16

    ## Center Hub Badge ("PRIMORDIA / EFAM CORE")
    frame:
        xalign 0.5
        yalign 0.53
        background "#181512E8"
        padding (26, 18)
        vbox:
            spacing 4
            xalign 0.5
            text "✦ PRIMORDIA ✦" color "#F2CC8F" size 25 xalign 0.5
            text "Essential Food & Medicine" color "#E07A5F" size 19 xalign 0.5
            text "Ash El · Lay-Lay · Xochtl" color "#2EC4B6" size 17 xalign 0.5

    ## Glowing Constellation Nodes with Event CG Thumbnails (Disaster CG -> Happy CG)
    for ep_id in EPISODE_ORDER:
        $ ep = EPISODES[ep_id]
        $ nx, ny = ep["pos"]
        $ is_done = ep_id in (persistent.episodes_completed or set())
        $ cg_thumb = ep["cg_happy_thumb"] if is_done else ep["cg_disaster_thumb"]
        $ sub_hook = ep["happy_title"] if is_done else ep["omg_title"]

        ## Pulsing outer aura
        frame:
            xpos nx
            ypos ny
            xanchor 0.5
            yanchor 0.5
            xsize 536
            ysize 326
            background ("#1E352B66" if is_done else "#2E261F66")
            at constellation_orb_pulse

        ## Interactive Node Card with Cutscene Event CG Thumbnail
        button:
            xpos nx
            ypos ny
            xanchor 0.5
            yanchor 0.5
            xsize 520
            padding (20, 14)
            background ("#17241FF4" if is_done else "#1C1815F4")
            hover_background "#2B241FF8"
            at constellation_star_glow
            action Show("scenario_overview_modal", ep_id=ep_id)

            vbox:
                spacing 6
                ## Cutscene Event CG Thumbnail (switches from Disaster CG to Happy CG when completed)
                add cg_thumb xalign 0.5

                hbox:
                    xfill True
                    text "[ep['pillar_short']]" color ep["color"] size 17
                    if is_done:
                        text "✓ TIMELINE RESTORED" color "#52B788" size 16 xalign 1.0
                    else:
                        text "→ Inspect Scenario" color ep["color"] size 16 xalign 1.0

                text "✦ [ep['title']]" color "#F4EFE6" size 26
                text "[sub_hook]  ·  POV: [ep['pov']]" color "#D8D0C5" size 16

                hbox:
                    spacing 14
                    for lid in ep["lessons"]:
                        $ lmeta = get_lesson_meta(lid)
                        $ l_unlocked = lid in (persistent.lessons_unlocked or set())
                        text ("★ " + lmeta["number"] + " " + lmeta["title"][:18] + ("…" if len(lmeta["title"]) > 18 else "") if l_unlocked else "☆ Lesson " + lmeta["number"]) color ("#52B788" if l_unlocked else "#888075") size 15

    ## Bottom Bar — Natural Glossary Footnote Explanation + System Menu Controls
    frame:
        xalign 0.5
        yalign 0.99
        xsize 1860
        background "#181512F2"
        padding (24, 10)
        hbox:
            xfill True
            hbox:
                spacing 12
                yalign 0.5
                text "✦ In stories, click any highlighted {color=#FFFF55}{u}word{/u}ˀ{/color} to open its Glossary definition." color "#D8D0C5" size 18 yalign 0.5
            hbox:
                spacing 14
                xalign 1.0
                yalign 0.5
                textbutton "📂 LOAD" action ShowMenu("load") style "constellation_nav_btn"
                textbutton "⚙ PREFERENCES" action ShowMenu("preferences") style "constellation_nav_btn"
                textbutton "ℹ ABOUT" action ShowMenu("about") style "constellation_nav_btn"
                if renpy.variant("pc"):
                    textbutton "✕ QUIT" action Quit(confirm=not main_menu) style "constellation_nav_btn"

    key "l" action ShowMenu("lessons_codex")
    key "g" action ShowMenu("glossary")


################################################################################
## Scenario Overview Modal — Previews the Event CG, Scenario & 3 Decisions

screen scenario_overview_modal(ep_id):
    modal True
    zorder 150
    $ ep = EPISODES[ep_id]
    $ is_done = ep_id in (persistent.episodes_completed or set())
    $ cg_img = ep["cg_happy"] if is_done else ep["cg_disaster"]
    $ subtitle_text = ep["pillar_short"].upper()

    ## Clicking or tapping outside the modal card dismisses the overlay
    button:
        xfill True
        yfill True
        background "#0B0908E8"
        action Hide("scenario_overview_modal")

    key "game_menu" action Hide("scenario_overview_modal")

    ## Modal card filled with dimmed scenario CG background
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1350
        ysize 432
        padding (0, 0)
        background "#1B1714"

        ## Scenario CG (happy if good ending unlocked, otherwise disaster) + dark dimming overlay
        add cg_img at cg_modal_bg
        add "#120F0DD4"

        ## Absorb clicks inside the modal card so they don't trigger the outside backdrop button
        button:
            xfill True
            yfill True
            background None
            action NullAction()

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 16

            vbox:
                xalign 0.5
                spacing 4
                text "[ep['title']]" color "#F4EFE6" size 42 xalign 0.5 bold True outlines [(2, "#000000AA", 0, 0)]
                text "[subtitle_text]" color ep["color"] size 20 xalign 0.5 bold True outlines [(1, "#000000AA", 0, 0)]

            text "[ep['omg_hook']]" color "#F4EFE6" size 23 xsize 1160 xalign 0.5 text_align 0.5 line_spacing 6 outlines [(2, "#000000CC", 0, 0)]

            vbox:
                xalign 0.5
                spacing 10

                if is_done:
                    text "GOOD ENDING UNLOCKED" color "#52B788" size 26 xalign 0.5 bold True outlines [(2, "#000000CC", 0, 0)]

                hbox:
                    spacing 28
                    xalign 0.5
                    textbutton ("Replay Story" if is_done else "Enter Story") action [Hide("scenario_overview_modal"), Start(ep["label"]) if main_menu else Jump(ep["label"])] style "constellation_confirm_btn"
                    textbutton "Back" action Hide("scenario_overview_modal") style "constellation_cancel_btn"


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
                    text "★ CRYPTO-ETHICS & CO-OP LESSONS CODEX" color "#F2CC8F" size 34
                    text "Every disaster teaches a real-world rule. Review unlocked lessons or inspect any lesson below." color "#BEB5A7" size 20
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
                            text ("✓ UNLOCKED IN PLAY" if cur_un else "☆ PREVIEW MODE") color ("#52B788" if cur_un else "#BEB5A7") size 20 xalign 1.0
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
                                text "REAL-WORLD CASE STUDY & RECEIPTS:" color "#2EC4B6" size 18
                                text "[cur_l['real_world']]" color "#D8D0C5" size 21


################################################################################
## Styles for Constellation & Modals

style constellation_nav_btn is button:
    background "#2B241E"
    hover_background "#3E332A"
    padding (16, 6)

style constellation_nav_btn_text is button_text:
    color "#F4EFE6"
    hover_color "#F2CC8F"
    size 18

style constellation_confirm_btn is button:
    background "#2EC4B6"
    hover_background "#45DFD0"
    padding (32, 14)

style constellation_confirm_btn_text is button_text:
    color "#12100E"
    hover_color "#000000"
    size 24

style constellation_cancel_btn is button:
    background "#2E2722"
    hover_background "#463B33"
    padding (26, 14)

style constellation_cancel_btn_text is button_text:
    color "#D8D0C5"
    hover_color "#FFFFFF"
    size 22
