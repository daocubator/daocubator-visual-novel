# Supabase setup for Get Rich Together

The game uses Supabase email one-time codes and a server-side point ledger. The
project URL and anon/publishable key are public client configuration. Never put
a `service_role` key in the game.

## 1. Create the Supabase project

Create a Supabase project, then open the project's **Connect** dialog and copy:

- Project URL
- Publishable key (or legacy anon key)

Put both values in `game/points.rpy`:

```renpy
define SUPABASE_URL = "https://YOUR_PROJECT_REF.supabase.co"
define SUPABASE_ANON_KEY = "YOUR_PUBLISHABLE_OR_ANON_KEY"
```

These values are intentionally shipped in the game. Database permissions and
the Auth JWT protect player data; the service-role key must remain secret and
is not used by the game.

## 2. Configure email codes

In **Authentication → Emails → Email Templates**, edit the **Magic Link**
template to use `{{ .Token }}` so Supabase sends a code the player can type into
Ren'Py instead of a magic link. Supabase defaults to a six-digit email code, and
the game accepts it. Choose a reasonable expiration and rate limit.
For production, open **Authentication → Settings** and configure a transactional
SMTP provider. Supabase's built-in mailer is for testing and has sending
restrictions; it is limited to project team addresses and currently has a low
send rate.

## 3. Create the points table and RPCs

Open **SQL Editor**, paste and run
[`supabase/migrations/202611070001_game_points.sql`](supabase/migrations/202611070001_game_points.sql).
The migration creates a private event ledger and two authenticated RPCs. It
awards 300 points for each of the four scenario clears and 10 points for each
glossary discovery and first exploration. The unique user/milestone key prevents
replays and repeated syncs from awarding points twice.

## 4. Web requests

Ren'Py calls Supabase with `renpy.fetch()`, which works across web, mobile, and
desktop. The browser build follows browser CORS rules, but hosted Supabase Auth
and REST APIs normally accept browser requests without a per-origin dashboard
allowlist. If the web build reports a CORS error, first confirm it uses the
project's HTTPS URL and that the response is coming from the Supabase API; a
JavaScript bridge is not required for this flow.

## 5. Verify the flow

1. Run the game and open **ACCOUNT** from the constellation screen.
2. Enter an email, request a code, then enter the code from the email. The game
   accepts up to eight numeric digits; Supabase defaults to six.
3. Clear a scenario and discover or open a glossary term.
4. Open **ACCOUNT → SYNC POINTS**. The displayed balance should match the
   account's points and should remain unchanged if you sync again.
5. Sign in on another device with the same email and sync there to see the same
   account balance.

Points are game progress, not a redeemable currency. The client reports which
milestones it reached; the database fixes each milestone's value and prevents
duplicates, but a modified game client can still report a milestone manually.
