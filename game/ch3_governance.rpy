# Chapter 3 — Governance Wars (Day 47)
# vault: 03 Chapters/Chapter 3 - Governance Wars.md

label ch3_governance:
    $ ch_open_vibes = vibes

    ## 3.1 Honeymoon's over
    scene bg discord with fade
    show jordan exhausted at right with dissolve
    j "Turnout on the last three proposals: six point three percent. I'm answering four hundred DMs a day and the megaphone guy has opinions about the logo."
    narrator "Democracy, it turns out, is a chore. Chores get skipped."

    ## 3.2 Proposal #17 — KEYSTONE (vault 3.2)
    scene bg conference with fade
    show maya alarmed at left with dissolve
    m "Proposal #17 just went up: 'Redistribute founder tokens to the community.' Thirty-five percent support and climbing."
    m "Here's the uncomfortable part: half their arguments are good."
    if rel_vera >= 40:
        show vera stern at right with dissolve
        v "Before you touch that veto, founder: I watched a hundred union locals win that exact battle and lose everything after. There's a third path if you're brave enough to look weak."
    menu:
        "Rally votes. Beat it democratically, in the open.":
            $ adjust(vibes=-5, jordan=+10)
            $ apathy = max(0, apathy - 1)
            $ mark("Beat Proposal #17 democratically")
            narrator "Vote: 48 for, 47 against, 5 abstain. You win by a coin flip's width. Factions crystallize overnight."
        "Use the founder veto. This ends now.":
            $ veto_used = True
            $ adjust(vibes=-15, security=+5, vera=-10)
            $ mark("Vetoed Proposal #17 with founder powers")
            narrator "The proposal dies instantly. So does something less visible. 'Decentralized*' — the asterisk is yours now."
        "Compromise: voluntary 10%% founder burn to the community." if rel_vera >= 40:
            $ adjust(vibes=+15, treasury=-10, vera=+10, maya=-5)
            $ mark("Voluntarily burned 10% of founder tokens")
            v "Losing a little on purpose so you can't lose everything by force. That's the oldest trick organized people have."

    ## 3.3 The delegation debate (vault 3.3)
    scene bg factionmap with fade
    narrator "Turnout keeps falling. Someone proposes delegation — 'liquid democracy.' Someone else livestreams a pie chart: in comparable DAOs, the top 10%% of voters hold 76.2%% of the power."
    menu:
        "Open delegation. Participation over purity.":
            $ adjust(vibes=+5)
            $ mark("Adopted open delegation")
            narrator "Turnout doubles. So does the influence of exactly eleven people."
            call lesson("apathy")
        "Capped, rotating delegation with time-locks on big proposals.":
            $ timelocks = True
            $ adjust(security=+10, vibes=+5)
            $ mark("Adopted capped delegation + proposal time-locks")
            narrator "Clunky. Slower. Attack-resistant. Maya calls it 'beautifully boring.'"
            call lesson("apathy")
        "Table it. We have shipping to do.":
            $ apathy += 1
            $ adjust(burnout=+5)
            narrator "The governance forum quietly becomes a museum."

    ## 3.4 Maya's 3× offer — KEYSTONE (vault 3.4)
    scene bg coworking with fade
    narrator "Maya's been quiet for two weeks. Commits at 3 a.m., camera off at standups. You noticed. (Didn't you?)"
    show maya tired at right with dissolve
    m "...A competitor offered me three times my salary. I told them I'd think about it. I've been thinking about it for two weeks."
    menu:
        "\"What do you need — not to stay. Just, what do you need?\"":
            if rel_maya >= 50 and burnout < 60:
                $ adjust(maya=+15, morale=+10)
                $ mark("Talked Maya through her burnout — she stayed")
                show maya proud
                m "...I need to not be the only adult about infrastructure. And a real vacation. That's it. That's the whole ransom."
                narrator "She stays. It costs you a hire and two weeks of her silence. Cheap."
            else:
                $ adjust(maya=+5, morale=-5)
                m "I appreciate the words. But you're running on fumes too — you can't refill me from an empty tank."
                narrator "She agrees to 'transition slowly.' You both know what that means."
                $ maya_gone = True
                $ mark("Maya left — the conversation came too late")
        "\"Three times? That's a betrayal of everything we—\"":
            $ adjust(maya=-20, morale=-10, burnout=+10)
            $ maya_gone = True
            $ mark("Called Maya's offer a betrayal — she resigned")
            show maya alarmed
            m "A betrayal? [player_name], I deferred salary for eight months. Read the resignation email whenever you're ready."
        "Give her space. She'll work it out.":
            $ maya_gone = True
            $ adjust(burnout=+10)
            $ mark("Gave Maya 'space' — got a resignation email")
            narrator "Two weeks of space later: a resignation email, timestamped 3:04 a.m. 'Please have your lawyer contact mine regarding equity separation.'"
    if maya_gone:
        hide maya with dissolve
        if equity == "vesting":
            narrator "The vesting agreement does its quiet work: her unvested tokens return to the treasury. Sad, clean, survivable."
            $ adjust(treasury=+10)
            call lesson("vesting")
        else:
            narrator "No vesting. She leaves with every token — dead equity on your cap table, a veto-sized ghost in every future vote. The lawyers begin to circle."
            $ adjust(treasury=-20, burnout=+15)
            call lesson("vesting")

    ## 3.5 Spectre's wallet clusters (vault 3.5)
    scene bg apartment with fade
    show spectre alert at right with dissolve
    s "eleven fresh wallets. coordinated buys, drip pattern, same gas habits. someone is accumulating quietly. guess who i think it is."
    if rel_spectre >= 40:
        $ adjust(security=+5)
        pc "I believe you. Start logging everything."
        s "already was."
        $ mark("Believed Spectre's whale-accumulation warning")
    else:
        pc "Eleven wallets is a Tuesday. You have literally no evidence."
        show spectre neutral
        s "no. i have a pattern. you have a preference. we'll compare notes in two weeks."

    ## 3.6 Burnout mirror (vault 3.6)
    scene bg apartment with fade
    narrator "4:11 a.m. You're re-reading your own launch-day post. 'We're going to do this sustainably.' The author seems nice. You don't recognize them."
    menu:
        "Take the weekend. Actually off. Phone in a drawer.":
            $ adjust(burnout=-20, vibes=-3)
            $ mark("Took a real weekend off")
            narrator "Two proposals pass without you. The sky does not fall. This is the most threatening thing you've learned all month."
            call lesson("burnout")
        "Push through. The collective needs you.":
            $ adjust(burnout=+15)
            narrator "The collective needs you. You need sleep. Only one of those needs has a Discord channel."
            call lesson("burnout")
    if burnout >= 60:
        narrator "{color=#D3710D}Your judgment is fraying at the edges. From here on, don't fully trust your own read on consequences — that's not a metaphor, it's a mechanic.{/color}"

    ## 3.7 Alex's quiet dinner (vault 3.7)
    if rel_alex >= 50:
        scene bg conference with fade
        show alex sincere at right with dissolve
        a "Full disclosure: Atlas bought me dinner. Offered me 'an advisory role.' I said I'd pass it by you — that's me, passing it by you."
        $ alex_loyal = True
        $ adjust(alex=+10)
        $ mark("Alex disclosed Atlas's approach — loyalty confirmed")
        pc "Thank you for telling me."
        a "Loyalty's a treasury asset too. I did the math on it."
    else:
        scene black with fade
        narrator "Somewhere across town, a dinner you weren't invited to."

    ## 3.8 Chapter close — factions
    scene bg factionmap with fade
    narrator "The map hardens: Decentralists. Pragmatists. Opportunists. Everyone's sure they're in the first two."
    call chapter_close(60, ch_open_vibes)
    jump ch4_attack
