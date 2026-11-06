# DAOCUBATOR / "Get Rich Together" — core definitions
# vault: 01 Overview/Game Systems.md · 02 Characters/*  (vault/ is the source of truth)

################################################################################
## Characters (colors match vault character frontmatter / Art Style Guide)

define narrator = Character(None)
define pc  = Character("[player_name]", color="#FFFFFF")
define ashel  = Character("Ash El",  color="#E07A5F", image="ashel")
define laylay = Character("Lay-Lay", color="#9B7EDE", image="laylay")
define xochtl = Character("Xochtl",  color="#2EC4B6", image="xochtl")
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

## Episodic Constellation state — vault: 01 Overview/Story Structure.md
default persistent.episodes_completed = set()
default current_episode = None
default current_pov = "Ash El"
default selected_constellation_node = None

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
## Top HUD Bar — POV, Glossary Footnote Hint, Lessons & Constellation Navigation

init python:
    def _ensure_single_narrative():
        try:
            if _preferences.language is not None:
                _preferences.language = None
        except Exception:
            pass
    config.start_callbacks.append(_ensure_single_narrative)
    config.after_load_callbacks.append(_ensure_single_narrative)

screen stats_hud():
    zorder 50
    frame:
        xalign 0.5
        ypos 0
        background Frame("gui/notify.png", gui.notify_frame_borders)
        padding (32, 8)
        hbox:
            spacing 28
            if current_episode:
                text "POV: [current_pov]" color "#E07A5F" size 21 yalign 0.5
            else:
                text "DAY [day]" color "#F4EFE6" size 21 yalign 0.5
            text "·" color "#6E655C" size 21 yalign 0.5
            text "Click any {color=#FFFF55}{u}term(?){/u}{/color} to learn more" color "#BEB5A7" size 19 yalign 0.5
            textbutton "(?) GLOSSARY" action ShowMenu("glossary") style "hud_stat" text_color "#FFFF55"
            textbutton "★ LESSONS" action ShowMenu("lessons_codex") style "hud_stat" text_color "#2EC4B6"
            textbutton "✦ CONSTELLATION" action Jump("world_overview") style "hud_stat" text_color "#F2CC8F"

style hud_stat is button
style hud_stat_text is button_text
style hud_stat:
    padding (0, 0)
    background None
style hud_stat_text:
    size 21
    hover_underline True

################################################################################
## Chapter close bookkeeping (legacy chapters compatibility)

label chapter_close(new_day, vibes_at_open):
    $ day = new_day
    return

label forced_rest:
    return

################################################################################
## Main menu — start the theme (Soft Circuit Reverie for Nimpet, by staRpauSe)
## and keep it playing into the game. The Episode Constellation is the Start Screen.

label main_menu:
    $ _ensure_single_narrative()
    if not renpy.music.get_playing(channel='music'):
        play music "audio/Soft-Circuit-Reverie-for-Nimpet-by-staRpauSe.mp3" loop
    call screen main_menu
    return

################################################################################
## Start

label start:
    $ _ensure_single_narrative()
    $ pivotal = []
    $ current_episode = None
    jump world_overview

label legacy_marathon:
    $ current_episode = None
    scene bg blockchain with fade
    show screen stats_hud
    narrator "The year is 2025. DAOs — groups that run themselves with shared rules and a shared treasury on a blockchain instead of a boss — are popular again."
    narrator "NounsDAO. MakerDAO. The Aragon crisis. Build Finance. Beanstalk. You watched them grow, and when they failed, you read every post-mortem report about what went wrong."
    narrator "About 65%% of projects like yours fail from the inside — not because of the market, but because of the people, the structure, and the hard conversations everyone kept putting off."
    narrator "You believe you will be different. Everyone believes that."
    python:
        player_name = renpy.input("What do they call you, founder?", default="Kai", length=20).strip() or "Kai"
    jump ch1_genesis
