# Endings — evaluation order mirrors vault/04 Endings/Endings Overview.md
# (Acqui-hire and Burnout Crash exit early from their own scenes.)

default persistent.endings_seen = set()
default epilogue_key = "elegiac"
default final_vote = None

label compute_ending:
    if burnout >= 80:
        jump ending_burnout
    elif security < 20 or treasury <= 10:
        jump ending_takeover
    elif veto_used and final_vote == "benevolent":
        jump ending_capture
    elif apathy >= 3 and vibes < 40:
        jump ending_bureaucracy
    elif vibes < 30:
        jump ending_split
    elif vibes >= 60 and morale >= 60 and security >= 50 and treasury >= 80 and burnout < 50 and final_vote == "balanced":
        jump ending_golden
    else:
        jump ending_sustainable

## Shared closing beat — Vera's argument plays over every ending, re-keyed
label vera_closing(mood):
    scene bg rooftop with fade
    show vera warm at right with dissolve
    if mood == "warm":
        v "The tools are new. The work is old. The work was always each other."
    elif mood == "stern":
        v "The tools are new. The work is old. You skipped the work, founder. The tools noticed."
    else:
        v "The tools are new. The work is old. Next time — and there's always a next time — start with the work."
    hide vera with dissolve
    return

label ending_recap:
    scene bg factionmap with fade
    narrator "—— THIS RUN ——"
    python:
        recap = renpy.store.pivotal[-6:] if len(renpy.store.pivotal) > 6 else renpy.store.pivotal
    $ recap_text = "\n".join("• " + p for p in recap)
    narrator "[recap_text]"
    $ n_seen = len(codex_seen)
    $ n_total = len(LESSONS)
    $ missed = n_total - n_seen
    narrator "Lessons unlocked this run: [n_seen] of [n_total]. ([missed] failure modes remain undiscovered. They remain either way — the question is whether you meet them here or out there.)"
    return

################################################################################

label ending_acquihire:
    $ persistent.endings_seen.add("acquihire")
    $ play_menu_music(force=True)
    scene bg conference with fade
    narrator "ENDING · THE ACQUI-HIRE"
    narrator "The papers sign smoothly. Everyone gets jobs, some get windfalls, and the mission statement gets a redirect notice."
    narrator "Wealthy, but incomplete. Not a failure. Not quite a win. In the reunion group chat, someone posts the old logo every year, and everyone hearts it, and nobody says anything."
    call vera_closing("mixed")
    call ending_recap
    return

label ending_burnout:
    $ persistent.endings_seen.add("burnout")
    $ play_bad_music()
    scene black with fade
    narrator "ENDING · THE BURNOUT CRASH"
    narrator "The collective survives you. That's the good news, and — sit with this — it's also the lesson: it could always survive you. You were the one who couldn't."
    narrator "Months later, rested, you read their announcements like postcards from a country you founded and had to leave. You are not the venture. You never were."
    call lesson("burnout")
    call vera_closing("gentle")
    call ending_recap
    return

label ending_takeover:
    $ persistent.endings_seen.add("takeover")
    $ play_bad_music()
    scene bg blockchain with fade
    narrator "ENDING · THE HOSTILE TAKEOVER"
    narrator "The treasury address updates one last time. Whoever holds the keys now sends a single gg into the governance forum before archiving it."
    narrator "Your collapse becomes a case study — taught, cited, dissected. Founders you'll never meet will make better choices because you documented yours. It's not nothing. It's just not yours."
    call vera_closing("stern")
    call ending_recap
    return

label ending_capture:
    $ persistent.endings_seen.add("capture")
    $ play_bad_music()
    scene bg conference with fade
    narrator "ENDING · FOUNDER'S CAPTURE"
    narrator "You kept control of everything except the point. The votes pass smoothly now — they're yours. The proposals are polite — they're performative. The community is stable — it's an audience."
    narrator "Somewhere in the docs, the word 'decentralized' remains, like a fossil. Web2 with extra steps, and the steps were expensive."
    call vera_closing("stern")
    call ending_recap
    return

label ending_bureaucracy:
    $ persistent.endings_seen.add("bureaucracy")
    $ play_bad_music()
    scene bg discord with fade
    narrator "ENDING · DEATH BY DEMOCRACY"
    narrator "Forty-seven proposals pending. Approving the new logo took three months and a constitutional amendment. Turnout on the amendment: 4.1%%."
    narrator "Nobody attacked you. Nobody had to. The collective became a beautifully-governed ghost town — perfect process, no pulse."
    call vera_closing("stern")
    call ending_recap
    return

label ending_split:
    $ persistent.endings_seen.add("split")
    $ play_bad_music()
    scene bg factionmap with fade
    narrator "ENDING · THE COMMUNITY SPLIT"
    narrator "The fork was inevitable in hindsight, which is the only place anything is inevitable. Three DAOs now share one dream, two grudges, and a fractured treasury."
    narrator "The dream doesn't die in an attack. It dies in a Discord argument about the dream."
    call vera_closing("mixed")
    call ending_recap
    return

label ending_sustainable:
    $ persistent.endings_seen.add("sustainable")
    $ play_menu_music(force=True)
    scene bg coworking with fade
    narrator "ENDING · THE SUSTAINABLE COLLECTIVE"
    narrator "No monument. No unicorn. A working thing: artists paid on time, decisions made in the open, a treasury that survives bad months because you made it boring on purpose."
    narrator "You sleep well. In this industry, that's the rarest exit of all."
    call vera_closing("warm")
    call ending_recap
    return

label ending_golden:
    $ persistent.endings_seen.add("golden")
    $ play_menu_music(force=True)
    scene bg rooftop with fade
    narrator "ENDING · COLLECTIVE PROSPERITY"
    narrator "It works. Not perfectly — resiliently. The constitution has calluses. The treasury has boring parts. The community has factions that argue and stay."
    narrator "Other founders study your governance docs the way you once studied the post-mortems. Someone forks your constitution and credits you in the README. That's the whole trophy. It's enough."
    if rel_spectre >= 80:
        show spectre vulnerable at right with dissolve
        s "before you log off. my name — my real one — is"
        narrator "The message stops there. A typing indicator, forever. Some trust is the reveal."
        hide spectre with dissolve
    call vera_closing("warm")
    call ending_recap
    return
