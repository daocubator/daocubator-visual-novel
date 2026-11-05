# Standalone Director's Stage Lab — Get Rich Together Visual Effects Sandbox
# Boots directly into the interactive Stage Lab (zero menus, zero JumpOutExceptions).
# Shares `images/` and `gui/` with the main game via directory junctions.

define narrator = Character(None)
define pc  = Character("[player_name]", color="#FFFFFF")
define m   = Character("Maya",    color="#55FFFF", image="maya")
define j   = Character("Jordan",  color="#FF55FF", image="jordan")
define a   = Character("Alex",    color="#FFAA55", image="alex")
define v   = Character("Vera",    color="#AA00AA", image="vera")
define s   = Character("Spectre", color="#00AAAA", image="spectre", what_prefix="{i}", what_suffix="{/i}")
define w   = Character("Atlas",   color="#FFFF55", image="atlas")
define mod = Character("Mod (pixel_pal)", color="#AAAAAA")

default player_name = "Kai"
default burnout = 15

## Minimal glossary stubs so shared `screens.rpy` works cleanly standalone
init -10 python:
    def gloss_unlock_text(*args):
        return None
    def gloss_choice_raw(caption):
        return caption
    def gloss_choice_text(caption):
        return caption

style gloss_tab is button
style gloss_tab_text is button_text
style gloss_tab:
    background Frame("gui/button/idle_background.png", gui.button_borders)
    selected_background Frame("gui/button/hover_background.png", gui.button_borders)
    hover_background Frame("gui/button/hover_background.png", gui.button_borders)
    padding (14, 8)
style gloss_tab_text:
    size 20
    color "#94A3B8"
    selected_color "#FFE57F"
    hover_color "#FFFFFF"

################################################################################
## Skip the Main Menu and boot straight into the Stage Lab loop!

label main_menu:
    return

label start:
    scene black
    jump lab_loop

label lab_loop:
    $ _in_lab_jukebox = False
    camera at cam_reset
    scene black
    $ _lab_override_bg = lab_bg
    if lab_tab == "blocking":
        $ _lab_showing_chars = [lab_left_char, lab_right_char] + ([lab_center_char] if lab_trio_mode else [])
    else:
        $ _lab_showing_chars = [lab_char]
    call screen stage_lab
    $ _picked_beat = _return
    $ _lab_override_bg = None
    $ _lab_showing_chars = None
    if _picked_beat:
        $ renpy.jump("lab_jukebox_" + _picked_beat)
    jump lab_loop


################################################################################
## Stage Lab State & Helpers

default lab_tab = "emotes"          # "emotes" | "blocking" | "lighting" | "jukebox"
default lab_char = "maya"           # active solo character in Tab 1
default lab_expr = "neutral"        # active expression in Tab 1
default lab_special = "none"        # "none" | "shadow" | "glitch" | "whisper" | "ghost"
default lab_slot = "stage_right"    # "stage_right" | "stage_center" | "closeup_right" | "imposing_center" | "lurk_right"
default lab_bg = "conference"       # background id
default lab_cam = "reset"           # "reset" | "push_in" | "intimate" | "dutch" | "red_alert"
default lab_left_char = "maya"
default lab_left_expr = "focused"
default lab_right_char = "alex"
default lab_right_expr = "calculating"
default lab_center_char = "atlas"
default lab_center_expr = "predatory"
default lab_trio_mode = False
default lab_flip_left = True
default lab_blocking_preset = "standard"  # "standard" | "closeup" | "whale" | "whisper"
default lab_ui_minimized = False
default lab_anim_nonce = 0
default _in_lab_jukebox = False

init python:
    LAB_CHAR_EXPRESSIONS = {
        "maya":    ["neutral", "focused", "tired", "proud", "alarmed"],
        "jordan":  ["neutral", "hyped", "hurt", "determined", "exhausted"],
        "alex":    ["neutral", "smirk", "calculating", "defensive", "sincere"],
        "vera":    ["neutral", "wry", "stern", "warm"],
        "spectre": ["neutral", "typing", "alert", "vulnerable"],
        "atlas":   ["neutral", "generous", "guarded", "predatory"],
    }

    LAB_CHAR_COLORS = {
        "maya":    "#55FFFF",
        "jordan":  "#FF55FF",
        "alex":    "#FFAA55",
        "vera":    "#AA00AA",
        "spectre": "#00AAAA",
        "atlas":   "#FFFF55",
    }

    LAB_EXPR_NOTES = {
        "neutral":     "Calm breathing loop (2.4s ease) + baseline gold specular.",
        "hyped":       "Double-hop entrance (-28px -> -14px) + fast upbeat pulse & warm specular boost.",
        "proud":       "Confident chest-up rise (-14px, 1.03x zoom) + bright golden sheen.",
        "determined":  "Forward-stepping resolve (-12px, 1.035x zoom) + crisp contrast.",
        "generous":    "Open, expansive posture (1.035x zoom) + warm gold glow.",
        "focused":     "Deliberate lean-in toward camera (1.04x zoom, xoffset -8) + sharp contrast.",
        "calculating": "Slow analytical lean-in (1.05x zoom, -0.8 deg tilt) + high-contrast specular.",
        "smirk":       "Sly sideways shift & head tilt (-1.8 deg rotate, xoffset +12).",
        "wry":         "Knowing asymmetric tilt (+1.5 deg rotate) + subtle warm glint.",
        "tired":       "Sigh inhale (-6px) -> heavy downward slump (+22px, 0.97x zoom) + desaturated gold.",
        "exhausted":   "Deep slump (+30px, 0.955x zoom, +1.6 deg droop) + dimmed metallic tone.",
        "hurt":        "Sharp flinch backward (xoffset +20, yoffset +12, 0.96x zoom) + muted shadow tint.",
        "vulnerable":  "Guarded step inward (0.98x zoom, -0.8 deg tilt) + softened contrast.",
        "defensive":   "Stiff step back (xoffset +16, 0.975x zoom) + cold metallic edge.",
        "guarded":     "Closed, watchful recoil (0.985x zoom) + high-contrast shadows.",
        "stern":       "Rigid, unyielding rise (-8px, 1.025x zoom) + steely contrast.",
        "alarmed":     "Startle jolt + rapid horizontal shiver (+/-14px) + electric highlight.",
        "alert":       "Sudden snap-to-attention jolt (+/-10px) + heightened contrast.",
        "sincere":     "Gentle open step closer (1.03x zoom) + warm rose-gold tint.",
        "warm":        "Soft welcoming lean (1.03x zoom, -0.5 deg) + rich amber glow.",
        "predatory":   "Slow, looming creep forward (0.95s ease to 1.09x zoom, +22px) + deep shadow contrast.",
        "typing":      "Hologram alpha glitch + rapid keyboard-typing micro-tremor + cyan terminal glow.",
    }

    LAB_BGS = [
        ("conference", "Conference Stage"),
        ("apartment",  "2:47 AM Apartment"),
        ("discord",    "Discord Server"),
        ("blockchain", "Blockchain Nodes"),
        ("coworking",  "Coworking Space"),
        ("rooftop",    "Dawn Rooftop"),
        ("signing",    "Wallet Signing UI"),
        ("factionmap", "Faction War Map"),
    ]

    LAB_JUKEBOX_BEATS = [
        ("ch1_spectre", "Ch1.7 · Spectre's 2:47 AM Encrypted DM",     "Terminal glitch entrance + apartment midnight blue monitor glow."),
        ("ch1_atlas",   "Ch1.8 · Atlas Mint-Night Shadow Reveal",      "Atlas materializes from a pitch-black silhouette into polished gold."),
        ("ch2_debate",  "Ch2.2 · Maya vs. Alex Treasury Debate",       "2-character inward flip + automatic speaker-focus zoom & listener dimming."),
        ("ch2_whisper", "Ch2.3 · Atlas's 500 ETH & Alex's Aside",      "Alex slides in and leans close to whisper while Atlas dims in the background."),
        ("ch2_viral",   "Ch2.4 · Viral Drop: Hyped vs. Alarmed",       "Jordan's excited double-hop vs. Maya's alarmed jolt & screen punch."),
        ("ch3_maya",    "Ch3.4 · Maya's 3x Offer & Dead-Equity Ghost", "Intimate 1.42x bust close-up + 'veto-sized ghost' resignation exit."),
        ("ch4_attack",  "Ch4b · 51% Attack: RED ALERT & Whale",        "Red Alert camera pulse + imposing 1.18x center-stage Atlas takeover."),
        ("ch5_jordan",  "Ch5.5 · Jordan's 3:00 AM Rooftop/Apt Call",   "Exhausted slump in 2:47 AM lighting -> warm determined close-up."),
    ]

    def lab_select_char(c):
        store.lab_char = c
        exprs = LAB_CHAR_EXPRESSIONS.get(c, ["neutral"])
        if store.lab_expr not in exprs:
            store.lab_expr = "neutral"
        store.lab_special = "none"
        store._active_speaker = c
        store.lab_anim_nonce += 1

    def lab_select_expr(e):
        store.lab_expr = e
        store.lab_special = "none"
        store.lab_anim_nonce += 1

    def lab_select_special(sp):
        store.lab_special = sp
        store.lab_anim_nonce += 1

    def lab_replay():
        store.lab_anim_nonce += 1

    def lab_set_bg(bg_id):
        store.lab_bg = bg_id
        store._lab_override_bg = bg_id

    def lab_set_tab(t):
        store.lab_tab = t
        if t == "blocking":
            store._lab_showing_chars = [store.lab_left_char, store.lab_right_char] + ([store.lab_center_char] if store.lab_trio_mode else [])
            store._active_speaker = store.lab_left_char
        else:
            store._lab_showing_chars = [store.lab_char]
            store._active_speaker = store.lab_char
        store.lab_anim_nonce += 1

    def lab_get_expr_transform(expr_name):
        return getattr(store, "expr_" + expr_name, store.expr_neutral)

    def lab_get_cam_transform():
        c = store.lab_cam
        if c == "push_in":
            return store.cam_push_in
        elif c == "intimate":
            return store.cam_intimate
        elif c == "dutch":
            return store.cam_dutch_spiral
        elif c == "red_alert":
            return store.cam_red_alert
        return store.cam_reset

    def lab_get_slot_transform():
        sp = store.lab_special
        if sp == "shadow":
            return store.enter_shadow(0.5 if store.lab_slot in ("stage_center", "imposing_center") else 0.80)
        elif sp == "glitch":
            return store.enter_glitch(0.5 if store.lab_slot in ("stage_center", "imposing_center") else 0.84)
        elif sp == "whisper":
            return store.enter_whisper_left
        elif sp == "ghost":
            return store.exit_ghost
        return getattr(store, store.lab_slot, store.stage_right)

    def lab_build_char_displayable(char_tag, expr_name, slot_trans):
        """Construct the live animated character displayable for the Stage Lab."""
        img_path = "images/%s %s.png" % (char_tag, expr_name)
        expr_t = lab_get_expr_transform(expr_name)
        light_t = char_focus_and_light(char_tag, expr_name)
        return At(img_path, expr_t, light_t, slot_trans)

## Overlay shown while a Jukebox scene is playing so you can jump back any time
screen stage_lab_jukebox_hud():
    zorder 250
    if _in_lab_jukebox:
        key "d" action Jump("lab_loop")
        key "D" action Jump("lab_loop")
        key "K_ESCAPE" action Jump("lab_loop")
        frame:
            xalign 0.02
            ypos 18
            background Frame("gui/notify.png", gui.notify_frame_borders)
            padding (24, 12)
            hbox:
                spacing 20
                text "◆ JUKEBOX SCENE PREVIEW ◆" color "#FFFF55" size 22 yalign 0.5
                textbutton "◀ RETURN TO STAGE LAB (D / ESC)" action Jump("lab_loop") text_color "#55FF55" text_hover_color "#FFFFFF" text_size 22

init python:
    if "stage_lab_jukebox_hud" not in config.overlay_screens:
        config.overlay_screens.append("stage_lab_jukebox_hud")


################################################################################
## The Interactive Stage Lab Screen

screen stage_lab():
    modal True
    zorder 220

    key "h" action ToggleVariable("lab_ui_minimized")
    key "H" action ToggleVariable("lab_ui_minimized")
    key "r" action Function(lab_replay)
    key "R" action Function(lab_replay)

    ## ── 1. FULL 1920x1080 LIVE PREVIEW STAGE ────────────────────────────────
    fixed:
        xsize 1920
        ysize 1080
        at lab_get_cam_transform()

        add ("images/bg %s.png" % lab_bg)

        ## Keyed by `lab_anim_nonce` so clicking Replay or switching emotes restarts one-shot animations cleanly
        for _nonce in [lab_anim_nonce]:
            if lab_tab == "blocking":
                ## Left character
                $ _l_slot = (
                    closeup_left if lab_blocking_preset == "closeup"
                    else enter_whisper_left if lab_blocking_preset == "whisper"
                    else (stage_left_flip if lab_flip_left else stage_left)
                )
                add lab_build_char_displayable(lab_left_char, lab_left_expr, _l_slot)

                ## Optional Center character (Trio or Whale power preset)
                if lab_trio_mode or lab_blocking_preset == "whale":
                    $ _c_slot = imposing_center if lab_blocking_preset == "whale" else stage_center
                    add lab_build_char_displayable(lab_center_char, lab_center_expr, _c_slot)

                ## Right character
                $ _r_slot = closeup_right if lab_blocking_preset == "closeup" else stage_right
                add lab_build_char_displayable(lab_right_char, lab_right_expr, _r_slot)
            else:
                ## Solo character preview (Tabs 1, 3, 4)
                add lab_build_char_displayable(lab_char, lab_expr, lab_get_slot_transform())

    ## ── 2. SAMPLE DIALOGUE PREVIEW BAR (BOTTOM) ─────────────────────────────
    if not lab_ui_minimized:
        frame:
            xalign 0.5
            yalign 1.0
            xsize 1920
            ysize 210
            background "#070b14dd"
            padding (48, 20)
            vbox:
                spacing 8
                if lab_tab == "emotes":
                    $ _cname = lab_char.capitalize()
                    $ _ccol = LAB_CHAR_COLORS.get(lab_char, "#FFFF55")
                    hbox:
                        spacing 18
                        text "[_cname]  ·  expression: [lab_expr]" color _ccol size 30
                        if lab_special != "none":
                            text "+ special: [lab_special]" color "#55FF55" size 26 yalign 0.5
                    text LAB_EXPR_NOTES.get(lab_expr, "") color "#F8FAFC" size 25 substitute False
                    text "Tip: Press (R) or click '↻ REPLAY' to re-trigger the entrance/emote animation. Press (H) to hide panels." color "#94A3B8" size 20
                elif lab_tab == "blocking":
                    hbox:
                        spacing 24
                        text "ACTIVE SPEAKER: " + (_active_speaker.upper() if _active_speaker else "NARRATOR / NONE") color "#FFFF55" size 28
                        text ("(Speaker Focus: ON — speaker zooms to 1.035x, listeners dim to 0.965x)" if _lab_speaker_focus_enabled else "(Speaker Focus: OFF — flat unlit staging)") color "#55FFFF" size 22 yalign 0.5
                    text "Click the 'SPEAK' buttons in the panel above to watch focus shift smoothly between characters." color "#F8FAFC" size 24
                elif lab_tab == "lighting":
                    hbox:
                        spacing 24
                        text "ROOM: [lab_bg!u]   ·   CAMERA: [lab_cam!u]   ·   BURNOUT: [burnout]" color "#FFFF55" size 28
                        text ("(Room Lighting Tint: ON)" if _lab_room_tint_enabled else "(Room Lighting Tint: OFF — raw studio gold)") color "#55FF55" size 22 yalign 0.5
                    text "Compare how the 24k gold reflections adapt to 2:47 AM Apartment (cool blue), Rooftop (dawn warm), and Blockchain (high-contrast cyber)." color "#F8FAFC" size 23
                else:
                    text "SCENE BEAT JUKEBOX — Click any scene card above to watch the choreographed dialogue & camera direction live." color "#FFFF55" size 26
                    text "During any Jukebox scene, click '◀ RETURN TO STAGE LAB' at the top-left (or press D / ESC) to jump right back here." color "#94A3B8" size 22

    ## ── 3. TOP CONTROL DECK ─────────────────────────────────────────────────
    if lab_ui_minimized:
        frame:
            xalign 0.02
            ypos 16
            background Frame("gui/notify.png", gui.notify_frame_borders)
            padding (20, 10)
            hbox:
                spacing 16
                textbutton "◆ SHOW STAGE LAB CONTROLS (H)" action SetVariable("lab_ui_minimized", False) text_color "#FFFF55" text_hover_color "#FFFFFF" text_size 22
                textbutton "↻ REPLAY (R)" action Function(lab_replay) text_color "#55FF55" text_hover_color "#FFFFFF" text_size 22
    else:
        frame:
            xalign 0.02
            ypos 14
            xsize 1280
            background "#090e1aee"
            padding (24, 18)
            vbox:
                spacing 12

                ## Header + Mode Tabs
                hbox:
                    spacing 12
                    text "◆ DIRECTOR'S STAGE LAB ◆" color "#FFFF55" size 26 yalign 0.5
                    null width 10
                    textbutton "1. EMOTES (27)" action Function(lab_set_tab, "emotes") selected (lab_tab == "emotes") style "gloss_tab"
                    textbutton "2. BLOCKING & FOCUS" action Function(lab_set_tab, "blocking") selected (lab_tab == "blocking") style "gloss_tab"
                    textbutton "3. LIGHT & CAMERA" action Function(lab_set_tab, "lighting") selected (lab_tab == "lighting") style "gloss_tab"
                hbox:
                    spacing 12
                    textbutton "4. SCENE BEAT JUKEBOX (8)" action Function(lab_set_tab, "jukebox") selected (lab_tab == "jukebox") style "gloss_tab"
                    textbutton "↻ REPLAY (R)" action Function(lab_replay) style "gloss_tab" text_color "#55FF55"
                    textbutton "HIDE UI (H)" action SetVariable("lab_ui_minimized", True) style "gloss_tab" text_color "#55FFFF"
                    textbutton "✕ QUIT LAB" action Quit(confirm=False) style "gloss_tab" text_color "#FF5555"

                ## ── TAB 1: EMOTES & ENTRANCES ───────────────────────────────
                if lab_tab == "emotes":
                    hbox:
                        spacing 8
                        text "CHARACTER:" color "#AAAAAA" size 20 yalign 0.5
                        for c in ("maya", "jordan", "alex", "vera", "spectre", "atlas"):
                            textbutton c.upper():
                                action Function(lab_select_char, c)
                                selected (lab_char == c)
                                style "gloss_tab"
                                text_color LAB_CHAR_COLORS[c]

                    hbox:
                        spacing 8
                        text "EXPRESSION:" color "#AAAAAA" size 20 yalign 0.5
                        for e in LAB_CHAR_EXPRESSIONS[lab_char]:
                            textbutton e.upper():
                                action Function(lab_select_expr, e)
                                selected (lab_expr == e and lab_special == "none")
                                style "gloss_tab"

                    hbox:
                        spacing 8
                        text "SPECIAL ENTRANCE/EXIT:" color "#AAAAAA" size 20 yalign 0.5
                        textbutton "NONE" action Function(lab_select_special, "none") selected (lab_special == "none") style "gloss_tab"
                        textbutton "SHADOW EMERGE (Atlas)" action Function(lab_select_special, "shadow") selected (lab_special == "shadow") style "gloss_tab"
                        textbutton "TERMINAL GLITCH (Spectre)" action Function(lab_select_special, "glitch") selected (lab_special == "glitch") style "gloss_tab"
                        textbutton "WHISPER ASIDE (Alex)" action Function(lab_select_special, "whisper") selected (lab_special == "whisper") style "gloss_tab"
                        textbutton "GHOST EXIT (Maya)" action Function(lab_select_special, "ghost") selected (lab_special == "ghost") style "gloss_tab"

                    hbox:
                        spacing 8
                        text "SHOT / SLOT:" color "#AAAAAA" size 20 yalign 0.5
                        textbutton "RIGHT (0.82)" action [SetVariable("lab_slot", "stage_right"), Function(lab_replay)] selected (lab_slot == "stage_right") style "gloss_tab"
                        textbutton "CENTER (0.50)" action [SetVariable("lab_slot", "stage_center"), Function(lab_replay)] selected (lab_slot == "stage_center") style "gloss_tab"
                        textbutton "BUST CLOSE-UP (1.42x)" action [SetVariable("lab_slot", "closeup_right"), Function(lab_replay)] selected (lab_slot == "closeup_right") style "gloss_tab"
                        textbutton "IMPOSING WHALE (1.18x)" action [SetVariable("lab_slot", "imposing_center"), Function(lab_replay)] selected (lab_slot == "imposing_center") style "gloss_tab"
                        textbutton "EDGE LURK (0.94)" action [SetVariable("lab_slot", "lurk_right"), Function(lab_replay)] selected (lab_slot == "lurk_right") style "gloss_tab"

                ## ── TAB 2: BLOCKING & SPEAKER FOCUS ─────────────────────────
                elif lab_tab == "blocking":
                    hbox:
                        spacing 10
                        text "WHO IS SPEAKING?" color "#FFFF55" size 20 yalign 0.5
                        textbutton ("◀ SPEAK: " + lab_left_char.upper()) action SetVariable("_active_speaker", lab_left_char) selected (_active_speaker == lab_left_char) style "gloss_tab" text_color "#55FF55"
                        if lab_trio_mode or lab_blocking_preset == "whale":
                            textbutton ("▲ SPEAK: " + lab_center_char.upper()) action SetVariable("_active_speaker", lab_center_char) selected (_active_speaker == lab_center_char) style "gloss_tab" text_color "#FFFF55"
                        textbutton ("SPEAK: " + lab_right_char.upper() + " ▶") action SetVariable("_active_speaker", lab_right_char) selected (_active_speaker == lab_right_char) style "gloss_tab" text_color "#55FF55"
                        textbutton "NARRATOR (DIM BOTH)" action SetVariable("_active_speaker", None) selected (_active_speaker is None) style "gloss_tab"
                        textbutton ("FOCUS: " + ("ON" if _lab_speaker_focus_enabled else "OFF")) action ToggleVariable("_lab_speaker_focus_enabled") selected _lab_speaker_focus_enabled style "gloss_tab"

                    hbox:
                        spacing 10
                        text "BLOCKING PRESET:" color "#AAAAAA" size 20 yalign 0.5
                        textbutton "STANDARD DUO" action [SetVariable("lab_blocking_preset", "standard"), SetVariable("lab_trio_mode", False), Function(lab_replay)] selected (lab_blocking_preset == "standard" and not lab_trio_mode) style "gloss_tab"
                        textbutton "BUST CLOSE-UP DUO" action [SetVariable("lab_blocking_preset", "closeup"), SetVariable("lab_trio_mode", False), Function(lab_replay)] selected (lab_blocking_preset == "closeup") style "gloss_tab"
                        textbutton "WHALE DOMINANCE (3-CHAR)" action [SetVariable("lab_blocking_preset", "whale"), SetVariable("lab_trio_mode", True), SetVariable("_active_speaker", "atlas"), Function(lab_replay)] selected (lab_blocking_preset == "whale") style "gloss_tab"
                        textbutton "ALEX WHISPER ASIDE" action [SetVariable("lab_blocking_preset", "whisper"), SetVariable("lab_left_char", "alex"), SetVariable("lab_left_expr", "smirk"), SetVariable("lab_right_char", "atlas"), SetVariable("lab_right_expr", "generous"), SetVariable("_active_speaker", "alex"), Function(lab_replay)] selected (lab_blocking_preset == "whisper") style "gloss_tab"

                    hbox:
                        spacing 10
                        text "STAGE LEFT:" color "#AAAAAA" size 20 yalign 0.5
                        textbutton ("FLIP INWARD (xzoom -1): " + ("ON" if lab_flip_left else "OFF")) action ToggleVariable("lab_flip_left") selected lab_flip_left style "gloss_tab" text_color "#55FFFF"
                        for c in ("maya", "jordan", "alex", "vera"):
                            textbutton c.upper() action [SetVariable("lab_left_char", c), SetVariable("lab_left_expr", "neutral"), Function(lab_replay)] selected (lab_left_char == c) style "gloss_tab"
                        text "  STAGE RIGHT:" color "#AAAAAA" size 20 yalign 0.5
                        for c in ("alex", "atlas", "vera", "spectre"):
                            textbutton c.upper() action [SetVariable("lab_right_char", c), SetVariable("lab_right_expr", "neutral"), Function(lab_replay)] selected (lab_right_char == c) style "gloss_tab"

                ## ── TAB 3: LIGHTING, CAMERA & BURNOUT ───────────────────────
                elif lab_tab == "lighting":
                    hbox:
                        spacing 8
                        text "ROOM BG:" color "#AAAAAA" size 20 yalign 0.5
                        for bg_id, bg_label in LAB_BGS[:4]:
                            textbutton bg_label action Function(lab_set_bg, bg_id) selected (lab_bg == bg_id) style "gloss_tab"
                    hbox:
                        spacing 8
                        text "        " size 20
                        for bg_id, bg_label in LAB_BGS[4:]:
                            textbutton bg_label action Function(lab_set_bg, bg_id) selected (lab_bg == bg_id) style "gloss_tab"
                        textbutton ("GOLD ROOM TINT: " + ("ON" if _lab_room_tint_enabled else "OFF (RAW)")) action ToggleVariable("_lab_room_tint_enabled") selected _lab_room_tint_enabled style "gloss_tab" text_color "#55FF55"

                    hbox:
                        spacing 8
                        text "CAMERA RIG:" color "#AAAAAA" size 20 yalign 0.5
                        textbutton "1.0x RESET" action SetVariable("lab_cam", "reset") selected (lab_cam == "reset") style "gloss_tab"
                        textbutton "PUSH-IN (1.08x)" action SetVariable("lab_cam", "push_in") selected (lab_cam == "push_in") style "gloss_tab"
                        textbutton "INTIMATE (1.15x)" action SetVariable("lab_cam", "intimate") selected (lab_cam == "intimate") style "gloss_tab"
                        textbutton "DUTCH SPIRAL (-1.8°)" action SetVariable("lab_cam", "dutch") selected (lab_cam == "dutch") style "gloss_tab"
                        textbutton "RED ALERT PULSE" action SetVariable("lab_cam", "red_alert") selected (lab_cam == "red_alert") style "gloss_tab"

                    hbox:
                        spacing 10
                        text "BURNOUT MECHANIC:" color "#AAAAAA" size 20 yalign 0.5
                        textbutton "BURNOUT 10 (CLEAR)" action SetVariable("burnout", 10) selected (burnout < 60) style "gloss_tab" text_color "#55FF55"
                        textbutton "BURNOUT 75 (FRAYING TREMOR & DESATURATION)" action SetVariable("burnout", 75) selected (burnout >= 60) style "gloss_tab" text_color "#FF5555"

                ## ── TAB 4: SCENE BEAT JUKEBOX ───────────────────────────────
                elif lab_tab == "jukebox":
                    vpgrid:
                        cols 2
                        spacing 8
                        ysize 230
                        for beat_id, beat_title, beat_desc in LAB_JUKEBOX_BEATS:
                            button:
                                xsize 600
                                padding (14, 10)
                                background Frame("gui/button/slot_idle_background.png", gui.slot_button_borders)
                                hover_background Frame("gui/button/slot_hover_background.png", gui.slot_button_borders)
                                ## Pure Return(beat_id) inside `call screen stage_lab` — NEVER throws JumpOutException!
                                action Return(beat_id)
                                vbox:
                                    spacing 3
                                    text "▶ " + beat_title color "#FFE57F" size 20 substitute False
                                    text beat_desc color "#CBD5E1" size 16 substitute False


################################################################################
## Jukebox Scene Preview Labels (Self-Contained 15-Second Set Pieces)

label lab_jukebox_ch1_spectre:
    $ _in_lab_jukebox = True
    $ burnout = 15
    scene bg apartment with fade
    narrator "2:47 AM. An encrypted message from an account with a hooded PFP and no history."
    show spectre typing at enter_glitch(0.84) with dissolve
    s "found a reentrancy path in your mint contract. you have not launched. this is the good timeline. voice call, camera off, or keep the bug."
    show spectre alert
    s "someone who reads bytecode for fun. next time ask 'what did you find.'"
    show spectre neutral
    s "patched. you listen. that's rarer than the bug."
    jump lab_loop

label lab_jukebox_ch1_atlas:
    $ _in_lab_jukebox = True
    $ burnout = 15
    scene bg blockchain with fade
    narrator "Mint night. Donations trickle in — then one address deposits more than everyone else combined."
    camera at cam_push_in
    show atlas guarded at enter_shadow(0.78) with dissolve
    w "Consider it a vote of confidence. I admire builders."
    hide atlas with dissolve
    camera at cam_reset
    narrator "The tokens never move again. They sit there. Waiting."
    jump lab_loop

label lab_jukebox_ch2_debate:
    $ _in_lab_jukebox = True
    $ burnout = 20
    scene bg conference with fade
    show maya focused at stage_left_flip
    show alex calculating at stage_right
    with dissolve
    a "Treasury allocation. Option one: hold 90%% in our own token. Number goes up, we all win, maximum alignment."
    m "Option two: the barbell. 30 to 50 percent in boring stables. We pay swap fees now and get to exist during our first bad month."
    show maya tired
    m "Cool. So if we go 90%% native, our rainy-day fund is made of rain."
    show alex smirk
    a "And if we go barbell, we pay the boring tax. Pick your poison, founder."
    jump lab_loop

label lab_jukebox_ch2_whisper:
    $ _in_lab_jukebox = True
    $ burnout = 20
    scene bg conference with fade
    show atlas generous at imposing_right with dissolve
    w "Five hundred ETH. No strings. Builders should build, not beg."
    show alex smirk at enter_whisper_left with dissolve
    a "{size=-8}(Whales always want something. Sometimes the something is later.){/size}"
    show alex calculating at stage_left_flip with dissolve
    show atlas guarded
    w "...Conditions. How disciplined of you. Agreed — for now."
    jump lab_loop

label lab_jukebox_ch2_viral:
    $ _in_lab_jukebox = True
    $ burnout = 25
    scene bg discord with fade
    show jordan hyped at stage_right with dissolve
    j "THE DROP WENT VIRAL. We're at 300%% of goal and climbing! This is the best thing that has ever happened to us!"
    show maya alarmed at stage_left_flip with dissolve
    m "Unit cost at promised price: negative fifteen per unit at this scale. Every new backer buys us a bigger hole. This is the worst thing that has ever happened to us."
    show jordan hurt
    j "...Wait. Negative fifteen?"
    jump lab_loop

label lab_jukebox_ch3_maya:
    $ _in_lab_jukebox = True
    $ burnout = 45
    scene bg coworking with fade
    camera at cam_intimate
    show maya tired at closeup_right with dissolve
    m "...A competitor offered me three times my salary. I told them I'd think about it. I've been thinking about it for two weeks."
    show maya alarmed
    m "A betrayal? [player_name], I deferred salary for eight months. Read the resignation email whenever you're ready."
    show maya tired at exit_ghost with dissolve
    narrator "No vesting. She leaves with every token — dead equity on your cap table, a veto-sized ghost in every future vote."
    camera at cam_reset
    jump lab_loop

label lab_jukebox_ch4_attack:
    $ _in_lab_jukebox = True
    $ burnout = 65
    scene bg blockchain with fade
    camera at cam_red_alert
    show maya alarmed at stage_left_flip with dissolve
    m "RED ALERT. One entity just crossed 45%% of governance tokens. Eleven wallets, one owner."
    show alex sincere at stage_right with dissolve
    a "It's Atlas. I'd know that gas-price signature anywhere. You have maybe a day before the proposal drops."
    hide maya with dissolve
    hide alex with dissolve
    show atlas predatory at imposing_center with dissolve
    w "Nothing personal, founder. Someone responsible was always going to end up holding the keys. I'd hoped you'd hand them over gently."
    camera at cam_reset
    jump lab_loop

label lab_jukebox_ch5_jordan:
    $ _in_lab_jukebox = True
    $ burnout = 40
    scene bg apartment with fade
    camera at cam_intimate
    show jordan exhausted at closeup_right with dissolve
    j "Can't sleep. Ninety days, [player_name]. The hack- attempt- thing, the factions, the... everything. Just tell me straight: was it worth it?"
    pc "Yes. Not because it worked — because of who we became running it."
    show jordan determined
    j "...Yeah. Okay. Yeah. Same time tomorrow, founder."
    camera at cam_reset
    jump lab_loop
