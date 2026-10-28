# DAOCUBATOR / "Get Rich Together" — core definitions
# vault: 01 Overview/Game Systems.md · 02 Characters/*  (vault/ is the source of truth)

################################################################################
## Characters (colors match vault character frontmatter / Art Style Guide)

define narrator = Character(None)
define pc  = Character("[player_name]", color="#FFFFFF")
define m   = Character("Maya",    color="#55FFFF", image="maya")
define j   = Character("Jordan",  color="#FF55FF", image="jordan")
define a   = Character("Alex",    color="#FFAA55", image="alex")
define v   = Character("Vera",    color="#AA00AA", image="vera")
define s   = Character("Spectre", color="#00AAAA", image="spectre", what_prefix="{i}", what_suffix="{/i}")
define w   = Character("Atlas",   color="#FFFF55", image="atlas")
define mod = Character("Mod (pixel_pal)", color="#AAAAAA")

################################################################################
## Core stats — the research's five-variable model

default vibes    = 50
default treasury = 100
default security = 40
default morale   = 60
default burnout  = 10
default day      = 1

## Relationships (governance capital, not romance meters)
default rel_maya    = 40
default rel_jordan  = 50
default rel_alex    = 30
default rel_vera    = 20
default rel_spectre = 10
default rel_atlas   = 25

## Flags — vault: Game Systems.md
default venture      = None      # "label" | "streetwear" | "collective"
default equity       = None      # "equal" | "merit" | "vesting"
default wrapper      = None      # "none" | "verein"
default treasury_mix = None      # "mono" | "barbell"
default whale_in     = False
default opsec        = "rushed"  # "rushed" | "hardened"
default timelocks    = False
default veto_used    = False
default apathy       = 0
default mentor       = False
default maya_gone    = False
default alex_loyal   = False
default attack_vector = None     # set at ch4 start: "phish" | "fiftyone" | "spiral"
default player_name  = "Kai"
default pivotal      = []        # run recap: (choice, consequence) strings
default codex_seen   = set()

init python:
    def clamp(x, lo, hi):
        return max(lo, min(hi, x))

    def adjust(vibes=0, treasury=0, security=0, morale=0, burnout=0,
               maya=0, jordan=0, alex=0, vera=0, spectre=0, atlas=0):
        """All stat changes flow through here (clamping + one place for cascade hooks)."""
        st = renpy.store
        st.vibes    = clamp(st.vibes + vibes, 0, 100)
        st.treasury = clamp(st.treasury + treasury, 0, 200)
        st.security = clamp(st.security + security, 0, 100)
        st.morale   = clamp(st.morale + morale, 0, 100)
        st.burnout  = clamp(st.burnout + burnout, 0, 100)
        st.rel_maya    = clamp(st.rel_maya + maya, 0, 100)
        st.rel_jordan  = clamp(st.rel_jordan + jordan, 0, 100)
        st.rel_alex    = clamp(st.rel_alex + alex, 0, 100)
        st.rel_vera    = clamp(st.rel_vera + vera, 0, 100)
        st.rel_spectre = clamp(st.rel_spectre + spectre, 0, 100)
        st.rel_atlas   = clamp(st.rel_atlas + atlas, 0, 100)

    def max_rel():
        st = renpy.store
        return max(st.rel_maya, st.rel_jordan, st.rel_alex,
                   st.rel_vera, st.rel_spectre, st.rel_atlas)

    def mark(text):
        """Record a pivotal choice for the ending recap screen."""
        renpy.store.pivotal.append(text)

################################################################################
## Stats HUD — top bar, PC-98 flavored

screen stats_hud():
    zorder 50
    frame:
        xalign 0.5
        ypos 0
        background Frame("gui/notify.png", gui.notify_frame_borders)
        padding (36, 8)
        hbox:
            spacing 28
            text "DAY [day]" color "#FFFFFF" size 22 yalign 0.5
            ## Each stat opens its glossary entry (glossary.rpy).
            textbutton "VIBES [vibes]" action Function(gloss_hyperlink, "vibes") style "hud_stat" text_color "#FF55FF"
            textbutton "TREASURY [treasury]Ξ" action Function(gloss_hyperlink, "treasury") style "hud_stat" text_color "#FFFF55"
            textbutton "SECURITY [security]" action Function(gloss_hyperlink, "security") style "hud_stat" text_color "#55FF55"
            textbutton "MORALE [morale]" action Function(gloss_hyperlink, "morale") style "hud_stat" text_color "#55FFFF"
            textbutton "BURNOUT [burnout]" action Function(gloss_hyperlink, "burnout") style "hud_stat" text_color ("#FF5555" if burnout >= 60 else "#AAAAAA")

style hud_stat is button
style hud_stat_text is button_text
style hud_stat:
    padding (0, 0)
    background None
style hud_stat_text:
    size 22
    hover_underline True

################################################################################
## Chapter close bookkeeping — cascade rule + burnout gate
## vault: Game Systems.md (token price ∝ Vibes × Security)

label chapter_close(new_day, vibes_at_open):
    if treasury_mix == "mono" and vibes < vibes_at_open:
        $ adjust(treasury=-15)
        narrator "{color=#FF5555}Your token dips with the mood. A treasury that IS your token dips with it. (Treasury -15){/color}"
    if burnout >= 80:
        call forced_rest
    $ day = new_day
    return

label forced_rest:
    scene bg apartment with fade
    narrator "You don't remember deciding to lie down."
    narrator "Your body files a governance proposal of its own. It passes unanimously."
    menu:
        "Actually rest. Delegate for a week.":
            $ adjust(burnout=-30, treasury=-5)
            narrator "The collective survives a week without you. That fact is either humbling or liberating. You choose liberating."
        "Rest is for people with runway.":
            $ adjust(burnout=+10, morale=-10)
            narrator "You reopen the laptop. Somewhere, Vera sighs without knowing why."
    return

################################################################################
## Main menu — start the theme (Soft Circuit Reverie for Nimpet, by staRpauSe)
## and keep it playing into the game.

label main_menu:
    if not renpy.music.get_playing(channel='music'):
        play music "audio/Soft-Circuit-Reverie-for-Nimpet-by-staRpauSe.mp3" loop
    call screen main_menu
    return

################################################################################
## Start

label start:
    $ pivotal = []
    scene bg blockchain with fade

    ## Experience picker — vault: 01 Overview/Game Systems.md (Plain Mode)
    ## "plain" is a Ren'Py language: game/tl/plain/ holds the ELI5/ESL script.
    call screen experience_select
    $ renpy.change_language("plain" if _return == "plain" else None)
    show screen stats_hud

    narrator "{color=#55FF55}TIP:{/color} {color=#FFFF55}{u}Yellow words{/u}{/color} are Glossary terms — click one to look it up. New terms unlock as you meet them, and entries link to more entries. Press G any time."

    narrator "2025. The age of DAOs has truly begun — again — for the third or fourth time."
    narrator "NounsDAO. MakerDAO. The Aragon crisis. Build Finance. Beanstalk. You watched them all rise, and you read every post-mortem on the way down."
    narrator "Roughly 65%% of ventures like the one you're about to start die from the inside. Not the market. The people. The structure. The deferred conversations."
    narrator "You're going to be different. Everyone says that."
    python:
        player_name = renpy.input("What do they call you, founder?", default="Kai", length=20).strip() or "Kai"
    jump ch1_genesis

################################################################################
## Experience picker (shown at Start). Returns "plain" or "classic".

screen experience_select():
    modal True
    add "#000000dd"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1560
        background Frame("gui/frame.png", gui.frame_borders)
        padding (50, 40)
        vbox:
            spacing 26
            text "◆ BEFORE YOU FOUND ANYTHING ◆" color "#FFFF55" size 34 xalign 0.5
            text _("How well do you know business, startups and crypto?") color "#FFFFFF" size 30 xalign 0.5
            hbox:
                spacing 40
                xalign 0.5
                button:
                    style "xp_card"
                    action Return("plain")
                    default_focus (_preferences.language == "plain")
                    vbox:
                        spacing 14
                        text _("I'M NEW TO THIS") style "xp_card_title" color "#55FF55"
                        text _("Plain, simple English. Short sentences, fewer idioms. Words are explained as you go, and you get tips before big choices.") style "xp_card_body"
                        text _("Good if English is not your first language, or if 'multisig' and 'cap table' mean nothing to you yet.") style "xp_card_note"
                button:
                    style "xp_card"
                    action Return("classic")
                    default_focus (_preferences.language != "plain")
                    vbox:
                        spacing 14
                        text _("I SPEAK FOUNDER") style "xp_card_title" color "#FF55FF"
                        text _("The original script: fast, dense, and full of in-jokes and jargon. Assumes you know your vesting cliff from your death spiral.") style "xp_card_body"
                        text _("Good if you've been in a startup, a DAO, or a Discord that should have been a DAO.") style "xp_card_note"
            text _("Both versions have the same story, choices and endings. Switch any time in Preferences → Story Text.") color "#AAAAAA" size 22 xalign 0.5

style xp_card is button
style xp_card:
    xsize 700
    padding (36, 32)
    background Frame("gui/button/slot_idle_background.png", gui.slot_button_borders)
    hover_background Frame("gui/button/slot_hover_background.png", gui.slot_button_borders)
style xp_card_title is text:
    size 34
style xp_card_body is text:
    size 25
    color "#FFFFFF"
style xp_card_note is text:
    size 21
    color "#AAAAAA"
