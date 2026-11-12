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
default supabase_code_loading = False
default supabase_verify_loading = False
default supabase_loading_dots = 0

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
            store.supabase_otp = ""
            store.supabase_status = "Code sent. Check your email and enter the code."
        except Exception as e:
            store.supabase_status = "Could not send code: %s" % str(e)

    def begin_supabase_code_request(email):
        email = (email or "").strip().lower()
        if store.supabase_code_loading:
            return
        if not supabase_ready():
            store.supabase_status = "Add the Supabase project URL and anon key in game/points.rpy first."
            renpy.restart_interaction()
            return
        if not email or "@" not in email:
            store.supabase_status = "Enter a valid email address."
            renpy.restart_interaction()
            return
        store.supabase_status = ""
        store.supabase_code_loading = True
        store.supabase_loading_dots = 0
        renpy.restart_interaction()

    def finish_supabase_code_request(email):
        try:
            request_supabase_code(email)
        finally:
            store.supabase_code_loading = False
            renpy.restart_interaction()

    def begin_supabase_code_verification(code):
        code = (code or "").strip()
        if store.supabase_code_loading or store.supabase_verify_loading:
            return
        if not supabase_ready():
            store.supabase_status = "Add the Supabase project URL and anon key in game/points.rpy first."
            renpy.restart_interaction()
            return
        if not (store.supabase_email or "").strip() or not code:
            store.supabase_status = "Enter the email address and the code from your message."
            renpy.restart_interaction()
            return
        store.supabase_status = ""
        store.supabase_verify_loading = True
        store.supabase_loading_dots = 0
        renpy.restart_interaction()

    def finish_supabase_code_verification(code):
        try:
            verify_supabase_code(code)
        finally:
            store.supabase_verify_loading = False
            renpy.restart_interaction()

    def edit_supabase_email():
        store.supabase_code_email = ""
        store.supabase_otp = ""
        store.supabase_status = ""
        renpy.restart_interaction()

    def activate_account_cta():
        if store.supabase_code_loading or store.supabase_verify_loading:
            return
        if persistent.supabase_session and (persistent.supabase_session.get("user") or {}).get("email"):
            sync_game_points()
        elif store.supabase_code_email and store.supabase_code_email == (store.supabase_email or "").strip().lower():
            begin_supabase_code_verification(store.supabase_otp)
        else:
            begin_supabase_code_request(store.supabase_email)

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

style account_input is input:
    xsize 726
    ysize 36
    yoffset 3
    font gui.sans_font
    color "#EED4B4"
    size 22


style account_disabled_btn is constellation_confirm_btn:
    xsize 320
    insensitive_background "#42281E"

style account_disabled_btn_text is constellation_confirm_btn_text:
    xalign 0.0
    insensitive_color "#9D908D"

style account_request_btn is constellation_confirm_btn:
    xsize 320

style account_request_btn_text is constellation_confirm_btn_text:
    xalign 0.0

style account_verify_btn is constellation_confirm_btn:
    xsize 400

style account_verify_btn_text is constellation_confirm_btn_text:
    xalign 0.0

style account_verify_disabled_btn is account_disabled_btn:
    xsize 400

screen player_account():
    tag menu
    modal True
    on "show" action Function(account_screen_opened)
    dismiss action Return() keysym "mouseup_1"

    $ normalized_account_email = (supabase_email or "").strip().lower()
    $ account_email_locked = supabase_code_loading or supabase_verify_loading or (supabase_code_email and supabase_code_email == normalized_account_email)

    if supabase_code_loading or supabase_verify_loading:
        timer 0.16 repeat True action SetVariable("supabase_loading_dots", (supabase_loading_dots + 1) % 4)
    if supabase_code_loading:
        timer 0.56 action Function(finish_supabase_code_request, supabase_email)
    if supabase_verify_loading:
        timer 0.56 action Function(finish_supabase_code_verification, supabase_otp)

    key ["K_RETURN", "K_KP_ENTER"] action Function(activate_account_cta) capture True

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
                        if account_email_locked:
                            text "[supabase_email]" font gui.sans_font color "#9D908D" size 22 xsize 726 ysize 36 yoffset 3
                        else:
                            input value VariableInputValue("supabase_email") length 254 allow "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@._+-" action Function(activate_account_cta) style "account_input"
                if supabase_code_loading:
                    textbutton "SENDING[supabase_loading_dots * '.']" action NullAction() sensitive False style "account_disabled_btn"
                elif account_email_locked:
                    if supabase_verify_loading:
                        textbutton "CHECK YOUR EMAIL" action NullAction() sensitive False style "account_disabled_btn"
                    else:
                        hbox:
                            spacing 12
                            textbutton "CHECK YOUR EMAIL" action NullAction() sensitive False style "account_disabled_btn"
                            textbutton "EDIT EMAIL" action Function(edit_supabase_email) style "constellation_cancel_btn"
                else:
                    textbutton "SEND EMAIL CODE" action Function(begin_supabase_code_request, supabase_email) style "account_request_btn"
                if supabase_code_email and supabase_code_email == normalized_account_email:
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
                            if supabase_verify_loading:
                                text "[supabase_otp]" font gui.sans_font color "#9D908D" size 22 xsize 726 ysize 36 yoffset 3
                            else:
                                input value VariableInputValue("supabase_otp") length 8 allow "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" action Function(activate_account_cta) style "account_input"
                    if supabase_verify_loading:
                        textbutton "VERIFYING[supabase_loading_dots * '.']" action NullAction() sensitive False style "account_verify_disabled_btn"
                    else:
                        textbutton "VERIFY & SYNC POINTS" action Function(begin_supabase_code_verification, supabase_otp) style "account_verify_btn"

            text "[supabase_status]" font gui.sans_font color "#DDBCAD" size 18
            text "Local points: [local_points_total()]" font gui.mono_font kerning 2.5 color "#9D908D" size 15
