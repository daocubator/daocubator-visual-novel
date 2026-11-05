# Stage Direction, Static Framing, Speaker Focus & Room Lighting
# Implements the visual novel staging principles from "LEVEL UP Your Visual Novel Sprites!":
#   1. Theater Staging: Automatic speaker focus (active speaker pops, listeners dim) & asymmetric slots
#   2. Static Expression Framing: 27 character expression definitions with zero motion and bottom-anchored framing
#   3. Film Framing Techniques: Waist-up vs. Bust close-ups (1.42x), imposing whale scale, & static camera framing
#   4. Lighting & Framing: Automatic room-lighting tints on 24k gold sprites + Burnout >= 60 desaturation
#   5. Show-Don't-Tell Blocking: Whisper aside framing & dead-equity ghost tint — all static with zero motion or bottom gaps

################################################################################
## 1. Speaker Focus & Environment Lighting State

default _active_speaker = None
default _lab_room_tint_enabled = True
default _lab_speaker_focus_enabled = True
default _lab_override_bg = None

init -5 python:
    import math

    # Map Character `name` (or image tag) to canonical sprite tag
    CHAR_TAG_MAP = {
        "Maya": "maya",
        "Jordan": "jordan",
        "Alex": "alex",
        "Vera": "vera",
        "Spectre": "spectre",
        "Atlas": "atlas",
    }

    ALL_CHAR_TAGS = ("maya", "jordan", "alex", "vera", "spectre", "atlas")

    # Room lighting profiles (r_mul, g_mul, b_mul, bright_offset, contrast_mul)
    # Calibrated specifically for polished 24k gold sculptures so each venue
    # reflects its ambient environment naturally.
    ROOM_LIGHTING = {
        "coworking":  (1.00, 0.99, 0.96,  0.00, 1.00),  # Warm natural daylight studio
        "conference": (1.02, 0.98, 0.92,  0.01, 1.04),  # Crisp stage spotlights
        "apartment":  (0.84, 0.93, 1.08, -0.05, 1.06),  # 2:47 AM cool midnight monitor glow
        "discord":    (0.95, 0.92, 1.08,  0.00, 1.05),  # Neon cyan/magenta server ambiance
        "blockchain": (0.88, 0.98, 1.06, -0.02, 1.10),  # High-contrast cyber node glow
        "rooftop":    (1.06, 0.95, 0.88,  0.03, 1.04),  # Golden hour / dawn rose-gold warmth
        "signing":    (0.90, 1.02, 0.94, -0.03, 1.08),  # Hardware wallet emerald/terminal glow
        "factionmap": (0.96, 0.94, 0.90, -0.02, 1.05),  # War-room tactical table light
    }

    # Expression-specific subtle lighting modifiers (bright_delta, sat_mul, contrast_mul)
    EXPR_LIGHTING = {
        "neutral":     ( 0.00, 1.00, 1.00),
        "hyped":       ( 0.04, 1.08, 1.04),
        "proud":       ( 0.03, 1.05, 1.03),
        "determined":  ( 0.03, 1.05, 1.05),
        "generous":    ( 0.04, 1.06, 1.02),
        "focused":     ( 0.01, 1.02, 1.08),
        "calculating": ( 0.00, 0.98, 1.12),
        "smirk":       ( 0.02, 1.04, 1.06),
        "wry":         ( 0.02, 1.02, 1.05),
        "sincere":     ( 0.03, 1.04, 1.00),
        "warm":        ( 0.04, 1.06, 1.00),
        "tired":       (-0.07, 0.82, 0.95),
        "exhausted":   (-0.09, 0.78, 0.94),
        "hurt":        (-0.06, 0.84, 0.96),
        "vulnerable":  (-0.05, 0.86, 0.96),
        "defensive":   (-0.02, 0.90, 1.10),
        "guarded":     (-0.03, 0.90, 1.12),
        "stern":       (-0.02, 0.92, 1.12),
        "alarmed":     ( 0.05, 1.06, 1.12),
        "alert":       ( 0.04, 1.04, 1.12),
        "predatory":   (-0.04, 0.94, 1.20),
        "typing":      ( 0.02, 1.02, 1.08),
    }

    def get_current_room_bg():
        """Return the active background attribute (e.g., 'apartment', 'conference')."""
        if getattr(store, "_lab_override_bg", None):
            return store._lab_override_bg
        try:
            attrs = renpy.get_attributes("bg", layer="master")
            if attrs:
                return attrs[0]
        except Exception:
            pass
        return "conference"

    def get_showing_characters():
        """Return list of character tags currently visible on the master layer."""
        try:
            tags = renpy.get_showing_tags(layer="master")
            return [c for c in ALL_CHAR_TAGS if c in tags]
        except Exception:
            return []

    def char_focus_light_fn(trans, st, at, char_tag="maya", expr_name="neutral"):
        """Static transform function that applies speaker focus (zoom, brightness,
        saturation) and room + expression lighting with zero motion or bottom gaps."""
        # Determine showing characters (or Stage Lab override)
        showing = getattr(store, "_lab_showing_chars", None)
        if showing is None:
            showing = get_showing_characters()
        multi_stage = len(showing) >= 2
        active = getattr(store, "_active_speaker", None)
        focus_on = getattr(store, "_lab_speaker_focus_enabled", True)

        # Target focus values (no yoffset so bottom edge never lifts off the screen)
        if not focus_on:
            t_zoom, t_bright, t_sat = 1.0, 0.0, 1.0
        elif active == char_tag:
            if multi_stage:
                t_zoom, t_bright, t_sat = 1.035, 0.04, 1.04
            else:
                t_zoom, t_bright, t_sat = 1.0, 0.02, 1.02
        elif active is not None and active != char_tag and multi_stage:
            # Another character is speaking in a multi-character scene -> dim listener
            t_zoom, t_bright, t_sat = 0.965, -0.20, 0.82
        elif active is None and multi_stage:
            # Narrator or player speaking while multiple characters are on stage
            t_zoom, t_bright, t_sat = 0.985, -0.08, 0.92
        else:
            t_zoom, t_bright, t_sat = 1.0, 0.0, 1.0

        # Expression lighting modifier
        eb, es, ec = EXPR_LIGHTING.get(expr_name, (0.0, 1.0, 1.0))

        # Room ambient lighting modifier
        if getattr(store, "_lab_room_tint_enabled", True):
            room = get_current_room_bg()
            rr, rg, rb, r_bright, r_cont = ROOM_LIGHTING.get(room, (1.0, 1.0, 1.0, 0.0, 1.0))
        else:
            rr, rg, rb, r_bright, r_cont = (1.0, 1.0, 1.0, 0.0, 1.0)

        # Spectre typing gets a subtle cyan terminal screen reflection
        if expr_name == "typing":
            rr, rg, rb = rr * 0.88, rg * 1.04, rb * 1.12

        # Burnout >= 60 visual fraying (slight desaturation & contrast, no motion jitter)
        burnout_val = getattr(store, "burnout", 10)
        if burnout_val >= 60:
            es *= 0.86
            r_cont *= 1.06

        final_bright = t_bright + eb + r_bright
        final_sat    = t_sat * es
        final_cont   = ec * r_cont

        tint_hex = "#%02x%02x%02x" % (
             max(0, min(255, int(rr * 255))),
             max(0, min(255, int(rg * 255))),
             max(0, min(255, int(rb * 255))),
        )

        # Overcompensate by +2px at the bottom so window scaling across resolutions
        # never exposes a 1px seam between the sprite and the bottom of the screen.
        trans.zoom = t_zoom
        trans.yoffset = 2
        trans.xoffset = 0
        trans.matrixcolor = (
            TintMatrix(tint_hex)
            * SaturationMatrix(final_sat)
            * ContrastMatrix(final_cont)
            * BrightnessMatrix(final_bright)
        )
        return None

    def char_focus_and_light(char_tag, expr_name="neutral"):
        return Transform(function=renpy.curry(char_focus_light_fn)(char_tag=char_tag, expr_name=expr_name))

## Attach speaker tracking to the Character objects defined in script.rpy
init 5 python:
    def _wire_speaker_callbacks():
        mapping = [
            ("m", "maya"),
            ("j", "jordan"),
            ("a", "alex"),
            ("v", "vera"),
            ("s", "spectre"),
            ("w", "atlas"),
            ("pc", None),
            ("narrator", None),
            ("mod", None),
        ]
        for var_name, tag in mapping:
            ch = getattr(store, var_name, None)
            if ch is not None and hasattr(ch, "cb_args"):
                new_cb_args = dict(ch.cb_args) if ch.cb_args else {}
                new_cb_args["_speaker_tag"] = tag
                ch.cb_args = new_cb_args

    _wire_speaker_callbacks()

    def direction_all_char_callback(event, interact=True, _speaker_tag=None, **kwargs):
        if event == "begin" and interact:
            store._active_speaker = _speaker_tag

    if direction_all_char_callback not in config.all_character_callbacks:
        config.all_character_callbacks.append(direction_all_char_callback)


################################################################################
## 2. Static Expression Framing
## No rotation (`rotate None`) so Ren'Py never adds `rotate_pad` transparent
## bounding-box padding around the 560x880 sprite, and no motion/bobbing.

transform expr_neutral:
    subpixel True
    yoffset 0 xoffset 0 zoom 1.0

transform expr_hyped:
    subpixel True
    yoffset 0 xoffset 0 zoom 1.02

transform expr_proud:
    subpixel True
    yoffset 0 xoffset 0 zoom 1.025

transform expr_determined:
    subpixel True
    yoffset 0 xoffset 0 zoom 1.025

transform expr_generous:
    subpixel True
    yoffset 0 xoffset 0 zoom 1.03

transform expr_focused:
    subpixel True
    yoffset 0 xoffset -6 zoom 1.03

transform expr_calculating:
    subpixel True
    yoffset 0 xoffset -8 zoom 1.04

transform expr_smirk:
    subpixel True
    yoffset 0 xoffset 8 zoom 1.015

transform expr_wry:
    subpixel True
    yoffset 0 xoffset 4 zoom 1.015

transform expr_tired:
    subpixel True
    yoffset 16 xoffset 0 zoom 0.98

transform expr_exhausted:
    subpixel True
    yoffset 24 xoffset 0 zoom 0.96

transform expr_hurt:
    subpixel True
    yoffset 12 xoffset 10 zoom 0.97

transform expr_vulnerable:
    subpixel True
    yoffset 8 xoffset -8 zoom 0.98

transform expr_defensive:
    subpixel True
    yoffset 2 xoffset 12 zoom 0.98

transform expr_guarded:
    subpixel True
    yoffset 2 xoffset 10 zoom 0.985

transform expr_stern:
    subpixel True
    yoffset 0 xoffset 0 zoom 1.02

transform expr_alarmed:
    subpixel True
    yoffset 0 xoffset 0 zoom 1.025

transform expr_alert:
    subpixel True
    yoffset 0 xoffset 0 zoom 1.02

transform expr_sincere:
    subpixel True
    yoffset 0 xoffset -6 zoom 1.025

transform expr_warm:
    subpixel True
    yoffset 0 xoffset 0 zoom 1.025

transform expr_predatory:
    subpixel True
    yoffset 18 xoffset -10 zoom 1.08

transform expr_typing:
    subpixel True
    yoffset 0 xoffset 0 zoom 1.0


################################################################################
## 3. Bind All 27 Character Expression Images to Their Framing + Lighting Rig

# MAYA (5)
image maya neutral     = At("images/maya neutral.png",     expr_neutral,     char_focus_and_light("maya", "neutral"))
image maya focused     = At("images/maya focused.png",     expr_focused,     char_focus_and_light("maya", "focused"))
image maya tired       = At("images/maya tired.png",       expr_tired,       char_focus_and_light("maya", "tired"))
image maya proud       = At("images/maya proud.png",       expr_proud,       char_focus_and_light("maya", "proud"))
image maya alarmed     = At("images/maya alarmed.png",     expr_alarmed,     char_focus_and_light("maya", "alarmed"))

# JORDAN (5)
image jordan neutral    = At("images/jordan neutral.png",    expr_neutral,    char_focus_and_light("jordan", "neutral"))
image jordan hyped      = At("images/jordan hyped.png",      expr_hyped,      char_focus_and_light("jordan", "hyped"))
image jordan hurt       = At("images/jordan hurt.png",       expr_hurt,       char_focus_and_light("jordan", "hurt"))
image jordan determined = At("images/jordan determined.png", expr_determined, char_focus_and_light("jordan", "determined"))
image jordan exhausted  = At("images/jordan exhausted.png",  expr_exhausted,  char_focus_and_light("jordan", "exhausted"))

# ALEX (5)
image alex neutral     = At("images/alex neutral.png",     expr_neutral,     char_focus_and_light("alex", "neutral"))
image alex smirk       = At("images/alex smirk.png",       expr_smirk,       char_focus_and_light("alex", "smirk"))
image alex calculating = At("images/alex calculating.png", expr_calculating, char_focus_and_light("alex", "calculating"))
image alex defensive   = At("images/alex defensive.png",   expr_defensive,   char_focus_and_light("alex", "defensive"))
image alex sincere     = At("images/alex sincere.png",     expr_sincere,     char_focus_and_light("alex", "sincere"))

# VERA (4)
image vera neutral     = At("images/vera neutral.png",     expr_neutral,     char_focus_and_light("vera", "neutral"))
image vera wry         = At("images/vera wry.png",         expr_wry,         char_focus_and_light("vera", "wry"))
image vera stern       = At("images/vera stern.png",       expr_stern,       char_focus_and_light("vera", "stern"))
image vera warm        = At("images/vera warm.png",        expr_warm,        char_focus_and_light("vera", "warm"))

# SPECTRE (4)
image spectre neutral    = At("images/spectre neutral.png",    expr_neutral,    char_focus_and_light("spectre", "neutral"))
image spectre typing     = At("images/spectre typing.png",     expr_typing,     char_focus_and_light("spectre", "typing"))
image spectre alert      = At("images/spectre alert.png",      expr_alert,      char_focus_and_light("spectre", "alert"))
image spectre vulnerable = At("images/spectre vulnerable.png", expr_vulnerable, char_focus_and_light("spectre", "vulnerable"))

# ATLAS (4)
image atlas neutral   = At("images/atlas neutral.png",   expr_neutral,   char_focus_and_light("atlas", "neutral"))
image atlas generous  = At("images/atlas generous.png",  expr_generous,  char_focus_and_light("atlas", "generous"))
image atlas guarded   = At("images/atlas guarded.png",   expr_guarded,   char_focus_and_light("atlas", "guarded"))
image atlas predatory = At("images/atlas predatory.png", expr_predatory, char_focus_and_light("atlas", "predatory"))


################################################################################
## 4. Theater Blocking Slots & Shot Sizes (Static, Bottom-Anchored)
## Also overrides built-in `right`, `left`, and `center` so all chapter scripts
## automatically use the theatrical Rule-of-Thirds framing with stage-left inward flip.

init 10:
    transform right:
        subpixel True
        xalign 0.82 yalign 1.0
        xzoom 1.0 zoom 1.0 yoffset 0 xoffset 0 alpha 1.0

    transform left:
        subpixel True
        xalign 0.18 yalign 1.0
        xzoom -1.0 zoom 1.0 yoffset 0 xoffset 0 alpha 1.0

    transform center:
        subpixel True
        xalign 0.50 yalign 1.0
        xzoom 1.0 zoom 1.0 yoffset 0 xoffset 0 alpha 1.0

## Asymmetric Rule-of-Thirds Stage Slots
transform stage_right:
    subpixel True
    xalign 0.82 yalign 1.0
    xzoom 1.0 zoom 1.0 yoffset 0 xoffset 0 alpha 1.0

transform stage_left:
    subpixel True
    xalign 0.18 yalign 1.0
    xzoom 1.0 zoom 1.0 yoffset 0 xoffset 0 alpha 1.0

## Flips a 3/4 character horizontally on stage left so they face inward toward stage right
transform stage_left_flip:
    subpixel True
    xalign 0.18 yalign 1.0
    xzoom -1.0 zoom 1.0 yoffset 0 xoffset 0 alpha 1.0

transform stage_center:
    subpixel True
    xalign 0.50 yalign 1.0
    xzoom 1.0 zoom 1.0 yoffset 0 xoffset 0 alpha 1.0

## Close-Up Bust Framing (crops the 560x880 waist-up render into a tight 1.42x bust shot)
transform closeup_right:
    subpixel True
    xalign 0.80 yalign 1.0
    zoom 1.42 yoffset 260 xoffset 0

transform closeup_left:
    subpixel True
    xalign 0.20 yalign 1.0
    xzoom -1.0 zoom 1.42 yoffset 260 xoffset 0

transform closeup_center:
    subpixel True
    xalign 0.50 yalign 1.0
    zoom 1.42 yoffset 260 xoffset 0

## Power & Isolation Framing
transform imposing_center:
    subpixel True
    xalign 0.52 yalign 1.0
    zoom 1.18 yoffset 90 xoffset 0

transform imposing_right:
    subpixel True
    xalign 0.82 yalign 1.0
    zoom 1.16 yoffset 85 xoffset 0

transform lurk_right:
    subpixel True
    xalign 0.94 yalign 1.0
    zoom 0.93 yoffset 20 xoffset 0

## Bespoke Story Framing (Static — No Motion)
transform enter_shadow(x_pos=0.82):
    subpixel True
    xalign x_pos yalign 1.0
    alpha 1.0 zoom 1.0 yoffset 0 xoffset 0

transform enter_glitch(x_pos=0.86):
    subpixel True
    xalign x_pos yalign 1.0
    alpha 1.0 zoom 1.0 yoffset 0 xoffset 0

transform enter_whisper_left:
    subpixel True
    xalign 0.28 yalign 1.0
    xzoom -1.0 alpha 1.0 zoom 1.06 yoffset 14 xoffset 0

transform exit_ghost:
    subpixel True
    xoffset 35 yoffset 0 alpha 0.32 matrixcolor (SaturationMatrix(0.0) * BrightnessMatrix(0.15))


################################################################################
## 5. Static Camera Framing (for `camera at ...` or Stage Lab container)
## Positive yoffset keeps zoomed-in frames anchored to the bottom of the screen
## so camera zoom never lifts the stage or creates bottom gaps.

transform cam_reset:
    subpixel True
    xalign 0.5 yalign 0.5
    zoom 1.0 xoffset 0 yoffset 0 matrixcolor IdentityMatrix()

transform cam_push_in:
    subpixel True
    xalign 0.5 yalign 0.5
    zoom 1.08 xoffset 0 yoffset 40 matrixcolor IdentityMatrix()

transform cam_intimate:
    subpixel True
    xalign 0.5 yalign 0.5
    zoom 1.15 xoffset 0 yoffset 75 matrixcolor IdentityMatrix()

transform cam_dutch_spiral:
    subpixel True
    xalign 0.5 yalign 0.5
    zoom 1.09 xoffset 0 yoffset 45 matrixcolor (ContrastMatrix(1.08) * SaturationMatrix(0.88))

transform cam_red_alert:
    subpixel True
    xalign 0.5 yalign 0.5
    zoom 1.05 xoffset 0 yoffset 25 matrixcolor (TintMatrix("#ffdede") * ContrastMatrix(1.10))
