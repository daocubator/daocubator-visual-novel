# Account binding and milestone points.
# Supabase URL and anon key are public client configuration, not service secrets.
define SUPABASE_URL = "https://jcluracmbowqtbasrppv.supabase.co"
define SUPABASE_ANON_KEY = "sb_publishable_GOruiaNRryNw2rCqFWRwAA_dM7F8_iV"

default persistent.game_point_milestones = set()
default persistent.game_point_balance = 0
default persistent.supabase_session = {}
default supabase_email = ""
default supabase_otp = ""
default supabase_code_email = ""
default supabase_status = ""

init -5 python:
    import time as _points_time

    SCENARIO_POINTS = 300
    GLOSSARY_POINTS = 10

    def milestone_points(milestone_id):
        if milestone_id.startswith("scenario:") and milestone_id.endswith(":cleared"):
            ep_id = milestone_id[len("scenario:"):-len(":cleared")]
            if ep_id in EPISODES:
                return SCENARIO_POINTS
        elif milestone_id.startswith("glossary:discovered:"):
            gid = milestone_id[len("glossary:discovered:"):]
            if gid in GLOSS:
                return GLOSSARY_POINTS
        elif milestone_id.startswith("glossary:explored:"):
            gid = milestone_id[len("glossary:explored:"):]
            if gid in GLOSS:
                return GLOSSARY_POINTS
        return 0

    def local_points_total():
        return sum(milestone_points(mid) for mid in persistent.game_point_milestones)

    def award_game_points(milestone_id):
        """Record a milestone locally; an account sync uploads it idempotently."""
        points = milestone_points(milestone_id)
        if not points or milestone_id in persistent.game_point_milestones:
            return False
        persistent.game_point_milestones.add(milestone_id)
        if not _session_user_id():
            persistent.game_point_balance = local_points_total()
        renpy.save_persistent()
        return True

    def supabase_ready():
        return bool(SUPABASE_URL and SUPABASE_ANON_KEY)

    def _supabase_url(path):
        return SUPABASE_URL.rstrip("/") + path

    def _supabase_headers(access_token=None):
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Content-Type": "application/json",
        }
        if access_token:
            headers["Authorization"] = "Bearer " + access_token
        return headers

    def _supabase_fetch(path, method="POST", payload=None, access_token=None, params=None):
        return renpy.fetch(
            _supabase_url(path),
            method=method,
            json=payload,
            params=params,
            headers=_supabase_headers(access_token),
            timeout=12,
            result="json",
        )

    def _session_user_id():
        session = persistent.supabase_session or {}
        return (session.get("user") or {}).get("id")

    def request_supabase_code(email):
        email = (email or "").strip().lower()
        if not supabase_ready():
            store.supabase_status = "Add the Supabase project URL and anon key in game/points.rpy first."
            return
        if not email or "@" not in email:
            store.supabase_status = "Enter a valid email address."
            return
        try:
            _supabase_fetch("/auth/v1/otp", payload={"email": email, "create_user": True})
            store.supabase_email = email
            store.supabase_code_email = email
            store.supabase_status = "Code sent. Check your email and enter the code."
        except Exception as e:
            store.supabase_status = "Could not send code: %s" % str(e)

    def _set_session(data):
        expires_in = int(data.get("expires_in", 3600))
        persistent.supabase_session = {
            "access_token": data.get("access_token"),
            "refresh_token": data.get("refresh_token"),
            "expires_at": int(_points_time.time()) + max(0, expires_in - 60),
            "user": data.get("user") or {},
        }
        renpy.save_persistent()

    def _refresh_supabase_session():
        session = persistent.supabase_session or {}
        refresh_token = session.get("refresh_token")
        if not refresh_token:
            return False
        data = _supabase_fetch(
            "/auth/v1/token",
            payload={"refresh_token": refresh_token},
            params={"grant_type": "refresh_token"},
        )
        _set_session(data)
        return bool((persistent.supabase_session or {}).get("access_token"))

    def _access_token():
        session = persistent.supabase_session or {}
        if not session.get("access_token"):
            return None
        if int(session.get("expires_at", 0)) <= int(_points_time.time()):
            if not _refresh_supabase_session():
                return None
        return (persistent.supabase_session or {}).get("access_token")

    def sync_game_points():
        """Submit this device's unlocked milestones; the database deduplicates per account."""
        if not supabase_ready():
            store.supabase_status = "Add your Supabase project URL and anon key before syncing."
            return
        if not _session_user_id():
            store.supabase_status = "Sign in first to sync points."
            return
        try:
            token = _access_token()
            if not token:
                raise Exception("Your sign-in expired. Request a new email code.")
            data = _supabase_fetch(
                "/rest/v1/rpc/award_game_milestones",
                payload={"p_milestone_ids": sorted(persistent.game_point_milestones)},
                access_token=token,
            )
            store.supabase_status = "Points synced to your account."
            persistent.game_point_balance = int(data.get("points", 0))
            renpy.save_persistent()
        except Exception as e:
            store.supabase_status = "Could not sync points: %s" % str(e)

    def verify_supabase_code(code):
        email = (store.supabase_email or "").strip().lower()
        code = (code or "").strip()
        if not supabase_ready():
            store.supabase_status = "Add the Supabase project URL and anon key in game/points.rpy first."
            return
        if not email or not code:
            store.supabase_status = "Enter the email address and the code from your message."
            return
        try:
            data = _supabase_fetch("/auth/v1/verify", payload={
                "email": email,
                "token": code,
                "type": "email",
            })
            _set_session(data)
            store.supabase_status = "Signed in. Syncing your points…"
            sync_game_points()
        except Exception as e:
            store.supabase_status = "Could not verify code: %s" % str(e)

    def sign_out_supabase():
        session = persistent.supabase_session or {}
        token = session.get("access_token")
        if token and supabase_ready():
            try:
                _supabase_fetch("/auth/v1/logout", method="POST", access_token=token)
            except Exception:
                pass
        persistent.supabase_session = {}
        persistent.game_point_balance = local_points_total()
        renpy.save_persistent()
        store.supabase_status = "Signed out. Your local progress is still on this device."

    def backfill_game_point_milestones():
        """Award points for progress made before this points update."""
        for ep_id in (persistent.episodes_completed or set()):
            award_game_points("scenario:%s:cleared" % ep_id)
        for gid in (persistent.gloss_found or {}).keys():
            award_game_points("glossary:discovered:%s" % gid)
        for gid in (persistent.gloss_read or set()):
            award_game_points("glossary:explored:%s" % gid)

    def account_screen_opened():
        backfill_game_point_milestones()
        if _session_user_id():
            sync_game_points()

    def prompt_supabase_otp():
        code = renpy.input(
            "Enter the code from your email",
            default=store.supabase_otp,
            length=8,
            allow="0123456789",
            copypaste=True,
        )
        store.supabase_otp = (code or "").strip()


style account_input is input:
    xsize 726
    ysize 36
    yoffset 3
    font gui.sans_font
    color "#EED4B4"
    size 22


screen player_account():
    tag menu
    modal True
    on "show" action Function(account_screen_opened)
    dismiss action Return()

    add "bg constellation"
    add "#140702D9"

    frame:
        modal True
        xalign 0.5
        yalign 0.5
        xsize 1180
        background Frame("gui/frame.png", gui.frame_borders)
        padding (48, 38)
        vbox:
            spacing 22
            hbox:
                xfill True
                vbox:
                    spacing 4
                    text "PLAYER ACCOUNT" font gui.mono_font kerning 4.0 color "#FAC443" size 18
                    text "Points & progress" font gui.serif_font axis {"weight": 300, "opticalsize": 48} color "#EED4B4" size 38 xoffset -2
                textbutton "× CLOSE" action Return() style "constellation_cancel_btn" xalign 1.0 yalign 0.5

            if persistent.supabase_session and (persistent.supabase_session.get("user") or {}).get("email"):
                $ account_email = persistent.supabase_session["user"].get("email", "")
                text "SIGNED IN AS  [account_email]" font gui.mono_font kerning 2.5 color "#578C88" size 17
                text "[persistent.game_point_balance] POINTS" font gui.serif_font axis {"weight": 300, "opticalsize": 48} color "#FAC443" size 46
                text "This device has [len(persistent.game_point_milestones)] recorded milestones. Sync to add them to your account; each milestone can only score once per account." font gui.sans_font color "#DDBCAD" size 20 line_spacing 4
                hbox:
                    spacing 14
                    textbutton "SYNC POINTS" action Function(sync_game_points) style "constellation_confirm_btn"
                    textbutton "SIGN OUT" action Function(sign_out_supabase) style "constellation_cancel_btn"
            else:
                text "Sign in with an email code to save points to your account and carry them between devices." font gui.sans_font color "#DDBCAD" size 21 line_spacing 4
                text "EMAIL ADDRESS" font gui.mono_font kerning 3.0 color "#B87444" size 15
                frame:
                    xsize 760
                    ysize 58
                    background "#834225"
                    padding (3, 3)
                    frame:
                        xsize 754
                        ysize 52
                        background "#2D1B10"
                        padding (14, 8)
                        input value VariableInputValue("supabase_email") length 254 allow "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@._+-" style "account_input"
                textbutton "SEND EMAIL CODE" action Function(request_supabase_code, supabase_email) style "constellation_confirm_btn"
                if supabase_code_email and supabase_code_email == (supabase_email or "").strip().lower():
                    text "EMAIL CODE" font gui.mono_font kerning 3.0 color "#B87444" size 15
                    frame:
                        xsize 760
                        ysize 58
                        background "#834225"
                        padding (3, 3)
                        frame:
                            xsize 754
                            ysize 52
                            background "#2D1B10"
                            padding (14, 8)
                            if renpy.variant("web"):
                                button:
                                    xsize 726
                                    ysize 36
                                    padding (0, 0)
                                    background None
                                    hover_background None
                                    action Function(prompt_supabase_otp)
                                    text (supabase_otp if supabase_otp else "Click to enter the email code") font gui.sans_font color ("#EED4B4" if supabase_otp else "#9D908D") size 22 xalign 0.0 yalign 0.5
                            else:
                                input value VariableInputValue("supabase_otp") length 8 allow "0123456789" style "account_input"
                    textbutton "VERIFY & SYNC POINTS" action Function(verify_supabase_code, supabase_otp) style "constellation_confirm_btn"

            text "[supabase_status]" font gui.sans_font color "#DDBCAD" size 18
            text "Local points: [local_points_total()]" font gui.mono_font kerning 2.5 color "#9D908D" size 15
