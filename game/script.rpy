# DAOCUBATOR / "Get Rich Together" — core definitions
# vault: 01 Overview/Game Systems.md · 02 Characters/*  (vault/ is the source of truth)

################################################################################
## Characters (DAOcubator Design System color tokens)

define narrator = Character(None)
define pc  = Character("[player_name]", color="#EED4B4")
define ashel  = Character("Koraba",  color="#D3710D", image="ashel")
define laylay = Character("Clara", color="#C2AEC7", image="laylay")
define xochtl = Character("Xochit",  color="#578C88", image="xochtl")
define m   = Character("Maya",    color="#578C88", image="maya")
define j   = Character("Jordan",  color="#D3710D", image="jordan")
define a   = Character("Alex",    color="#B87444", image="alex")
define v   = Character("Vera",    color="#C2AEC7", image="vera")
define s   = Character("Spectre", color="#8C8CA3", image="spectre")
define w   = Character("Atlas",   color="#FAC443", image="atlas")
define mod = Character("Mod (pixel_pal)", color="#9D908D")

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
default current_pov = "Koraba"
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

    MENU_MUSIC = [
        "audio/(menu)-Glitch-N-Paper-by-DJ-KWHYC.mp3",
        "audio/(menu)-Off-Kilter-Hustle-by-DJ-KWHYC.mp3",
    ]

    BAD_MUSIC = [
        "audio/(bad)-Subtle-Ruin-by-DJ-KWHYC.mp3",
        "audio/(bad)-Red-Ink-Panic-by-DJ-KWHYC.mp3",
        "audio/(bad)-Bankrupt-Breakdown.mp3",
        "audio/(bad)-Point-of-No-Return-by-DJ-KWHYC.mp3",
    ]

    def play_menu_music(force=False):
        """Randomly play one of the (menu) tracks for default, main menu, and good outcomes."""
        current = renpy.music.get_playing(channel="music")
        if force or current not in MENU_MUSIC:
            track = renpy.random.choice(MENU_MUSIC)
            config.main_menu_music = track
            renpy.music.play(track, channel="music", loop=True, fadeout=0.5, fadein=0.5)

    def play_bad_music(force=False):
        """Randomly play one of the (bad) tracks when entering an episode where things are going bad."""
        current = renpy.music.get_playing(channel="music")
        if force or current not in BAD_MUSIC:
            track = renpy.random.choice(BAD_MUSIC)
            renpy.music.play(track, channel="music", loop=True, fadeout=0.5, fadein=0.5)

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
    pass

################################################################################
## Chapter close bookkeeping (legacy chapters compatibility)

label chapter_close(new_day, vibes_at_open):
    $ day = new_day
    return

label forced_rest:
    return

################################################################################
## Main menu — randomly play one of the DJ KWHYC (menu) tracks
## and keep it playing into the game. The Episode Constellation is the Start Screen.

label main_menu:
    $ _ensure_single_narrative()
    $ play_menu_music()
    call screen main_menu
    return

################################################################################
## Start

label start:
    $ _ensure_single_narrative()
    $ pivotal = []
    $ current_episode = None
    $ play_menu_music()
    jump world_overview

label legacy_marathon:
    $ current_episode = None
    $ play_menu_music()
    scene bg blockchain with fade
    narrator "The year is 2025. DAOs — groups that run themselves with shared rules and a shared treasury on a blockchain instead of a boss — are popular again."
    narrator "NounsDAO. MakerDAO. The Aragon crisis. Build Finance. Beanstalk. You watched them grow, and when they failed, you read every post-mortem report about what went wrong."
    narrator "About 65%% of projects like yours fail from the inside — not because of the market, but because of the people, the structure, and the hard conversations everyone kept putting off."
    narrator "You believe you will be different. Everyone believes that."
    python:
        player_name = renpy.input("What do they call you, founder?", default="Kai", length=20).strip() or "Kai"
    jump ch1_genesis
