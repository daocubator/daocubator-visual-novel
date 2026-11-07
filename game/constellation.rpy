# World Overview ("The First Constellation" — Start Screen) & Lessons Codex
# vault: 01 Overview/Story Structure.md · 01 Overview/Game Systems.md · 05 Lessons/Lessons Index.md

init 5 python:
    _LESSON_NUMBERS = {
        "no_keys_no_cheese": "#16",
        "vetting_admins":    "#17",
        "test_transaction":  "#18",
        "creator_vs_admin":  "#19",
        "coop_solidarity":   "#20",
        "agreements_law":    "#21",
        "equal_split":       "#01",
        "vesting":           "#02",
        "partnership":       "#03",
        "death_spiral":      "#04",
        "recoupment":        "#05",
        "chargeback":        "#06",
        "overfunding":       "#07",
        "apathy":            "#08",
        "capture":           "#09",
        "flashloan":         "#10",
        "credentials":       "#11",
        "verify_hex":        "#12",
        "ice_phishing":      "#13",
        "burnout":           "#14",
        "greenwash":         "#15",
    }

    def get_lesson_meta(lid):
        tup = LESSONS.get(lid, ("LESSON", "", ""))
        num = _LESSON_NUMBERS.get(lid, "#--")
        return {
            "number": num,
            "title": tup[0],
            "body": tup[1],
            "real_world": tup[2],
        }

    EPISODES = {
        "ep1_keys": {
            "title": "No Keys, No Cheese",
            "color": "#D3710D",
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
            "title": "Frozen Pay, Empty Stage",
            "color": "#578C88",
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
            "color": "#FAC443",
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
            "title": "One Tired Click Drained the Apothecary",
            "color": "#C2AEC7",
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

transform constellation_card_float(delay=0.0):
    pause delay
    yoffset 0
    ease 2.4 yoffset -7
    ease 2.4 yoffset 0
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
    add "#1407027A"

    ## Top Header Bar — Game Title & Navigation
    frame:
        xalign 0.5
        ypos 12
        xsize 1860
        background "#1E140EF2"
        padding (28, 12)
        vbox:
            spacing 8
            hbox:
                xfill True
                vbox:
                    spacing 2
                    text "Get Rich Together — The First Constellation" font gui.serif_font axis {"weight": 300, "opticalsize": 48} color "#EED4B4" size 30
                    text "Click any story node below to witness the collapse, then rewind time and solve it." font gui.sans_font color "#DDBCAD" size 18
                hbox:
                    spacing 12
                    xalign 1.0
                    yalign 0.5
                    $ num_lessons_done = len(persistent.lessons_unlocked or set())
                    frame:
                        background "#241309"
                        padding (14, 6)
                        text "LESSONS · [num_lessons_done]/[len(LESSONS)]" font gui.mono_font kerning 3.2 color "#FAC443" size 16
                    textbutton "LESSONS CODEX" action ShowMenu("lessons_codex") style "constellation_nav_btn"
                    textbutton "GLOSSARY" action ShowMenu("glossary") style "constellation_nav_btn"

    ## Center Hub Badge ("Primordia / EFAM Core") — NodeCard / Hub Label
    frame:
        xalign 0.5
        yalign 0.53
        background "#1E140EE8"
        padding (28, 18)
        vbox:
            spacing 4
            xalign 0.5
            text "Primordia" font gui.serif_font axis {"weight": 300, "opticalsize": 28} color "#FAC443" size 28 xalign 0.5
            text "ESSENTIAL FOOD & MEDICINE" font gui.mono_font kerning 3.0 color "#EED4B4" size 15 xalign 0.5
            text "Ash El · Lay-Lay · Xochtl" font gui.sans_font color "#578C88" size 16 xalign 0.5

    ## Story cards with click-through thumbnail art (Disaster CG -> Happy CG)
    for ep_id in EPISODE_ORDER:
        $ ep = EPISODES[ep_id]
        $ nx, ny = ep["pos"]
        $ float_delay = EPISODE_ORDER.index(ep_id) * 0.55
        $ is_done = ep_id in (persistent.episodes_completed or set())
        $ cg_thumb = ep["cg_happy_thumb"] if is_done else ep["cg_disaster_thumb"]
        ## Completed stories get a soft sage aura and a clear green border.
        frame:
            xpos nx
            ypos ny
            xanchor 0.5
            yanchor 0.5
            xsize 536
            ysize 244
            background ("#528C6E55" if is_done else "#83422522")
            at constellation_card_float(float_delay)

        ## Keep the thumbnail and story title as the card's only content.
        button:
            xpos nx
            ypos ny
            xanchor 0.5
            yanchor 0.5
            xsize 520
            ysize 230
            padding (4, 4)
            background ("#528C6E" if is_done else "#8C533E")
            hover_background ("#528C6E" if is_done else "#8C533E")
            at constellation_card_float(float_delay)
            action Show("scenario_overview_modal", ep_id=ep_id)

            vbox:
                spacing 0
                add cg_thumb xsize 512
                frame:
                    xfill True
                    ysize 54
                    background "#140702E8"
                    padding (12, 4)
                    text "[ep['title']]" font gui.serif_font axis {"weight": 400, "opticalsize": 42} color "#EED4B4" size 34 yalign 0.5

    ## Bottom Bar — Natural Glossary Footnote Explanation + System Menu Controls
    frame:
        xalign 0.5
        yalign 0.99
        xsize 1860
        background "#1E140EF2"
        padding (24, 10)
        hbox:
            xfill True
            hbox:
                spacing 12
                yalign 0.5
                text "In stories, click any highlighted {color=#FAC443}{u}word{/u}˚{/color} to open its Glossary definition." font gui.sans_font color "#DDBCAD" size 18 yalign 0.5
            hbox:
                spacing 14
                xalign 1.0
                yalign 0.5
                textbutton "LOAD" action ShowMenu("load") style "constellation_nav_btn"
                textbutton "PREFERENCES" action ShowMenu("preferences") style "constellation_nav_btn"
                textbutton "ABOUT" action ShowMenu("about") style "constellation_nav_btn"
                if renpy.variant("pc"):
                    textbutton "QUIT" action Quit(confirm=not main_menu) style "constellation_nav_btn"

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

    ## Clicking or tapping outside the modal card dismisses the overlay
    button:
        xfill True
        yfill True
        background "#140702E0"
        action Hide("scenario_overview_modal")

    key "game_menu" action Hide("scenario_overview_modal")

    ## Modal card filled with dimmed scenario CG background
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1350
        ysize 432
        padding (0, 0)
        background "#1E140E"

        ## Scenario CG (happy if good ending unlocked, otherwise disaster) + dark dimming overlay
        add cg_img at cg_modal_bg
        add "#140702D8"

        ## Absorb clicks inside the modal card so they don't trigger the outside backdrop button
        button:
            xfill True
            yfill True
            background None
            mouse "default"
            action NullAction()

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 16

            vbox:
                xalign 0.5
                spacing 6
                text "[ep['title']]" font gui.serif_font axis {"weight": 300, "opticalsize": 48} color "#EED4B4" size 44 xalign 0.5 outlines [(2, "#140702CC", 0, 0)]

            text "[ep['omg_hook']]" font gui.sans_font color "#DDBCAD" size 23 xsize 1160 xalign 0.5 text_align 0.5 line_spacing 6 outlines [(2, "#140702CC", 0, 0)]

            vbox:
                xalign 0.5
                spacing 12

                if is_done:
                    text "• TIMELINE RESTORED — GOOD ENDING UNLOCKED" font gui.mono_font kerning 4.0 color "#578C88" size 20 xalign 0.5 outlines [(2, "#140702CC", 0, 0)]

                hbox:
                    spacing 28
                    xalign 0.5
                    textbutton ("REPLAY STORY ›" if is_done else "ENTER STORY ›") action [Hide("scenario_overview_modal"), Start(ep["label"]) if main_menu else Jump(ep["label"])] style "constellation_confirm_btn"
                    textbutton "BACK" action Hide("scenario_overview_modal") style "constellation_cancel_btn"


################################################################################
## Lessons Codex Screen — Browse all 21 lessons in LESSONS

default selected_codex_lesson = "no_keys_no_cheese"

screen lessons_codex():
    tag menu
    modal True

    key "K_ESCAPE" action Return()

    add "#140702"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1780
        ysize 980
        background "#1E140E"
        padding (40, 32)

        vbox:
            spacing 18
            hbox:
                xfill True
                vbox:
                    spacing 4
                    text "CRYPTO-ETHICS & COOPERATIVE FIELD NOTES" font gui.mono_font kerning 3.0 color "#B87444" size 15
                    text "Lessons Codex" font gui.serif_font axis {"weight": 300, "opticalsize": 48} color "#EED4B4" size 36
                    text "Every disaster teaches a real-world rule." font gui.sans_font color "#9D908D" size 19
                textbutton "× RETURN" action Return() style "constellation_confirm_btn" xalign 1.0 yalign 0.5

            hbox:
                spacing 30
                ysize 800

                ## Left column: scrollable list of all lessons
                frame:
                    xsize 680
                    yfill True
                    background "#241309"
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
                                    background ("#42281E" if selected_codex_lesson == lid else "#2D1B10")
                                    hover_background "#42281E"
                                    action SetScreenVariable("selected_codex_lesson", lid)
                                    hbox:
                                        spacing 12
                                        text ("•" if is_un else "·") font gui.mono_font color ("#FAC443" if is_un else "#9D908D") size 22 yalign 0.5
                                        vbox:
                                            spacing 2
                                            text "[lmeta['number']] · [lmeta['title']]" font gui.sans_font color ("#EED4B4" if selected_codex_lesson == lid else "#DDBCAD") size 18

                ## Right column: detail view of selected lesson
                $ cur_l = get_lesson_meta(selected_codex_lesson)
                $ cur_un = selected_codex_lesson in (persistent.lessons_unlocked or set())
                frame:
                    xfill True
                    yfill True
                    background "#2D1B10"
                    padding (36, 30)
                    vbox:
                        spacing 18
                        hbox:
                            xfill True
                            text "[cur_l['number']]" font gui.mono_font kerning 3.2 color "#B87444" size 16
                            text ("• UNLOCKED IN PLAY" if cur_un else "· PREVIEW MODE") font gui.mono_font kerning 3.2 color ("#FAC443" if cur_un else "#9D908D") size 16 xalign 1.0
                        text "[cur_l['title']]" font gui.serif_font axis {"weight": 300, "opticalsize": 48} color "#EED4B4" size 38
                        frame:
                            xfill True
                            background "#241309"
                            padding (26, 22)
                            text "[cur_l['body']]" font gui.serif_font axis {"weight": 300, "opticalsize": 36} color "#EED4B4" size 26 line_spacing 6
                        frame:
                            xfill True
                            background "#1E140E"
                            padding (22, 16)
                            vbox:
                                spacing 6
                                text "REAL-WORLD CASE STUDY & RECEIPTS" font gui.mono_font kerning 3.0 color "#578C88" size 15
                                text "[cur_l['real_world']]" font gui.sans_font color "#DDBCAD" size 20


################################################################################
## Styles for Constellation & Modals

style constellation_nav_btn is button:
    background "#2D1B10"
    hover_background "#42281E"
    padding (16, 6)

style constellation_nav_btn_text is button_text:
    font gui.mono_font
    kerning 3.2
    color "#DDBCAD"
    hover_color "#FAC443"
    size 16

style constellation_confirm_btn is button:
    background "#FAC443"
    hover_background "#FFF3C9"
    padding (32, 14)

style constellation_confirm_btn_text is button_text:
    font gui.mono_font
    kerning 4.0
    color "#140702"
    hover_color "#140702"
    size 20

style constellation_cancel_btn is button:
    background "#2D1B10"
    hover_background "#42281E"
    padding (26, 14)

style constellation_cancel_btn_text is button_text:
    font gui.mono_font
    kerning 3.6
    color "#DDBCAD"
    hover_color "#FAC443"
    size 18
