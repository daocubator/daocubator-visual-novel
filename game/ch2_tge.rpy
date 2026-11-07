# Chapter 2 — Token Generation Event (Day 30)
# vault: 03 Chapters/Chapter 2 - Token Generation Event.md

label ch2_tge:
    $ ch_open_vibes = vibes

    ## 2.1 TGE eve
    scene bg discord with fade
    show jordan hyped at right with dissolve
    j "Ten. Thousand. Members. The believers are here, [player_name]!"
    narrator "So are the vultures. From a distance, they cheer identically."

    ## 2.2 Treasury composition — KEYSTONE (vault 2.2)
    scene bg conference with fade
    show maya focused at left
    show alex calculating at right
    with dissolve
    a "Treasury allocation. Option one: hold 90%% in our own token. Number goes up, we all win, maximum alignment."
    m "Option two: the barbell. 30 to 50 percent in boring stables. We pay swap fees now and get to exist during our first bad month."
    menu:
        "\"Ninety percent native. We bet on ourselves.\"":
            $ treasury_mix = "mono"
            $ adjust(alex=+5, morale=+5)
            $ mark("Kept the treasury 90% in the native token")
            show maya tired
            m "Cool. So our rainy-day fund is made of rain."
        "\"Barbell it. Half stables. Pay the boring tax.\"":
            $ treasury_mix = "barbell"
            $ adjust(treasury=-10, maya=+10)
            $ mark("Diversified the treasury (barbell strategy)")
            show maya proud
            m "Thank you. Screenshot this moment for the postmortem we now won't need."
            call lesson("death_spiral")

    ## 2.3 Atlas's offer — KEYSTONE (vault 2.3)
    scene bg conference with fade
    show atlas generous at right with dissolve
    w "Five hundred ETH. No strings. Builders should build, not beg."
    show alex smirk at left with dissolve
    a "{size=-8}(Whales always want something. Sometimes the something is later.){/size}"
    menu:
        "Take it. 500 ETH buys years of runway.":
            $ whale_in = True
            $ adjust(treasury=+50, atlas=+20, vibes=-10)
            $ mark("Took Atlas's 500 ETH, no conditions")
            w "Wonderful. You won't even notice me."
            narrator "The community notices. '#WhaleDAO' trends for a day and a half."
        "Take it — with conditions. Advisory only. No governance weight.":
            $ whale_in = True
            $ adjust(treasury=+25, atlas=-5, vibes=+5)
            $ mark("Took whale money with governance conditions")
            show atlas guarded
            w "...Conditions. How disciplined of you. Agreed — for now."
        "Decline. Politely. Expensively.":
            $ adjust(treasury=-10, atlas=-15, vibes=+10)
            $ mark("Declined the whale's 500 ETH")
            show atlas guarded
            w "Pride is a luxury good. Enjoy it while the treasury lasts."

    ## 2.4 Route beat (vault 2.4 — one lesson by venture)
    if venture == "label":
        scene bg conference with fade
        show alex sincere at right with dissolve
        a "Big distributor wants our whole catalog. Advance up front. It's a 360 — they take touring and merch too, and the advances cross-collateralize across releases."
        a "I think it's good money. Genuinely."
        menu:
            "Sign it. Advances now, details later.":
                $ adjust(treasury=+30, vibes=-10, morale=-10)
                $ mark("Signed the 360 deal, cross-collateralized")
                narrator "The artists do the math three months later. The math does not love them back."
                call lesson("recoupment")
            "Negotiate: capped recoupables, no cross-collateralization.":
                $ adjust(treasury=+10, alex=+10, vibes=+5)
                $ mark("Negotiated the label deal to capped recoupables")
                a "They pushed back. Then they signed. Huh. You can just... ask."
                call lesson("recoupment")
            "Walk away. We distribute ourselves.":
                $ adjust(treasury=-5, vibes=+5, burnout=+10)
                narrator "Independence: all of the freedom, all of the shipping labels."
    elif venture == "streetwear":
        scene bg coworking with fade
        show jordan hyped at right with dissolve
        j "Everyone's asking for a FULL COLLECTION. Eight pieces! Cut-and-sew! We'd look so real!"
        menu:
            "Do the eight-piece collection. Look real.":
                $ adjust(treasury=-30, burnout=+10)
                $ mark("Launched an 8-piece collection on unvalidated demand")
                narrator "Pattern makers. Size grading. Fabric minimums. A six-month launch quietly becomes eighteen."
                call lesson("chargeback")
            "One item, pre-order only. Validate first.":
                $ adjust(treasury=+15, vibes=+5)
                $ mark("Ran a single-item pre-order drop")
                j "One perfect hoodie. Okay. Boring... but the spreadsheet agrees with you."
                call lesson("chargeback")
    else:
        scene bg discord with fade
        show jordan hyped at right with dissolve
        j "THE DROP WENT VIRAL. We're at 300%% of goal and climbing! This is the best thing that has ever happened to us!"
        show maya alarmed at left with dissolve
        m "Unit cost at promised price: negative fifteen per unit at this scale. Every new backer buys us a bigger hole. This is the worst thing that has ever happened to us."
        menu:
            "Cap it. Close the drop, fulfill what we promised.":
                $ adjust(treasury=+20, vibes=-5, maya=+10)
                $ mark("Capped the viral drop at fulfillable scale")
                m "Capped. We'll disappoint thousands of strangers instead of betraying hundreds of believers. Correct trade."
                call lesson("overfunding")
            "Ride it! We'll figure out fulfillment!":
                $ adjust(treasury=+40, burnout=+15, morale=-10)
                $ mark("Let the overfunded drop run uncapped")
                narrator "The number is beautiful. The number is a promise you haven't priced."
                call lesson("overfunding")

    ## 2.5 Spectre's audit ask (vault 2.5)
    scene bg apartment with fade
    show spectre typing at right with dissolve
    s "launch in 72h. i need 20 eth and admin access to audit properly. or don't. good luck either way."
    menu:
        "Fund the audit. Give scoped access.":
            $ opsec = "hardened"
            $ adjust(treasury=-20, security=+15, spectre=+15)
            $ mark("Funded a pre-launch security audit")
            show spectre neutral
            s "three criticals, patched. you'll never know which headlines you skipped. that's the job."
        "No time, no budget. We review it ourselves tonight.":
            $ opsec = "rushed"
            $ adjust(burnout=+10, spectre=-5)
            $ mark("Skipped the security audit to make the launch date")
            narrator "You review 4,000 lines of Solidity at 4 a.m. with the confidence of the sleep-deprived."

    ## 2.6 The shared doc incident (vault 2.6)
    scene bg discord with fade
    show jordan hurt at right with dissolve
    j "Um. pixel_pal pasted the multisig seed phrase into the team Notion. 'Just temporarily.' It's been six hours."
    menu:
        "Blow it up publicly. Zero-tolerance, new rules today.":
            $ adjust(security=+10, morale=-10)
            narrator "pixel_pal apologizes in four channels. Everyone learns. Nobody relaxes for a week."
            call lesson("credentials")
        "Fix it quietly: rotate keys, DM them kindly, write the policy.":
            $ adjust(security=+8, morale=+5, jordan=+5)
            $ mark("Rotated keys and wrote a secrets policy without a public flogging")
            narrator "Keys rotated. Policy posted. pixel_pal becomes your most paranoid — best — mod."
            call lesson("credentials")
        "\"After launch. Add it to the list.\"":
            $ adjust(security=-15)
            $ mark("Left the seed phrase in Notion until 'after launch'")
            narrator "The list is long. The list is where security goes to die."

    ## 2.7 Vera's counteroffer (vault 2.7)
    scene bg conference with fade
    show vera warm at right with dissolve
    v "My counteroffer to your whale: twenty ETH for a sliver, no board seat — and dinner once a month where you tell me the truth."
    menu:
        "Take the dinners. (And the truth-telling.)":
            $ mentor = True
            $ adjust(treasury=+10, vera=+20, morale=+5)
            $ mark("Took Vera's mentorship deal")
            v "Good. First truth: you look exhausted already. Write that down."
        "Pass. We're covered on capital.":
            $ adjust(vera=-5)
            v "Capital, yes. Perspective — we'll see."

    ## 2.8 Launch night (vault 2.8)
    scene bg blockchain with fade
    narrator "LAUNCH. The token goes live. Governance activates. Someone makes a shrine to the block number."
    $ adjust(burnout=+15, vibes=+10)
    narrator "You are, officially, a real DAO now. Burnout +15 — launches cost you either way. Nobody warns founders about the mornings after."

    ## 2.9 Chapter close
    if treasury_mix == "mono":
        narrator "The chart is beautiful tonight. 90%% of your treasury agrees with itself. (Remember this candle.)"
    call chapter_close(47, ch_open_vibes)
    jump ch3_governance
