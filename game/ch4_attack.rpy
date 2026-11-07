# Chapter 4 — The Attack (Day 60)
# vault: 03 Chapters/Chapter 4 - The Attack.md
# The vector is EARNED: the game picks what you're most vulnerable to.

label ch4_attack:
    $ ch_open_vibes = vibes
    $ play_bad_music(force=True)

    python:
        if opsec == "rushed":
            attack_vector = "phish"
        elif whale_in or rel_atlas >= 50:
            attack_vector = "fiftyone"
        elif treasury_mix == "mono":
            attack_vector = "spiral"
        else:
            attack_vector = "fiftyone"  # reduced-strength default: attacks come regardless

    scene bg blockchain with fade
    narrator "Day 60. Something is wrong with the chain the way something can be wrong with a house at night — quietly, and in your own walls."

    ## Spectre's earned warning (vault: relationship gate)
    if rel_spectre >= 60:
        show spectre alert at right with dissolve
        s "it's happening. tonight. you have maybe one move before it starts. use it."
        menu:
            "\"Harden the multisig. Rotate everything.\"":
                $ adjust(security=+10)
                s "done. it won't stop them. it will slow them. sometimes that's the whole war."
            "\"Alert the community. All hands.\"":
                $ adjust(vibes=+5, jordan=+5)
                s "loud. risky. but a thousand eyes see more than mine."
        hide spectre with dissolve

    if attack_vector == "phish":
        jump ch4a_phish
    elif attack_vector == "spiral":
        jump ch4c_spiral
    else:
        jump ch4b_fiftyone

################################################################################
label ch4a_phish:
    ## 4a.1 The odd transaction
    scene bg apartment with fade
    narrator "1:14 a.m. A routine treasury payout is queued — vendor invoice, seen a hundred times. Your wallet extension summarizes it cheerfully."
    if maya_gone:
        narrator "Maya would have caught the smell of it. Maya is gone."
    else:
        show maya alarmed at left with dissolve
        m "Something's off. My extension updated itself an hour ago and I didn't approve that."

    ## 4a.2 THE SET PIECE — verify the hex (vault 4a.2)
    scene bg signing with fade
    narrator "SIGN TRANSACTION?\n\nTo: Vendor Payments Ltd [OK]\nAmount: 12.5 ETH [OK]\nGas: normal [OK]"
    narrator "Everything looks fine. It is 1:14 a.m. Your Burnout is [burnout]. The confirm button is very large and very green."
    menu:
        "• SIGN — it's the same invoice as always.":
            $ adjust(treasury=-60, security=-20, vibes=-15)
            $ mark("Signed a spoofed transaction without checking the raw hex")
            narrator "The 'summary' was drawn by malware. The real destination was 0x7C3f…a91E — a fresh wallet, already tumbling your 60 ETH into fog."
            call lesson("verify_hex")
        "› EXPAND RAW DATA — check the hex against the whitelist.":
            if burnout >= 60:
                narrator "You expand the raw data. The hex swims — you're too tired for this.\n\nWhitelist:  {color=#578C88}0x4A21…9DEB{/color}\nDestination: {color=#9D908D}0x4A2l…9DE8{/color}\n\n(Is that an l? An 8? You genuinely cannot tell tonight.)"
            else:
                narrator "You expand the raw data.\n\nWhitelist:  {color=#578C88}0x4A21…9DEB{/color}\nDestination: {color=#D3710D}0x7C3f…a91E{/color}\n\nNot even close."
            menu:
                "REJECT. Kill the queue. Wake everyone up.":
                    $ adjust(security=+15, spectre=+10)
                    $ mark("Caught a spoofed transaction by verifying the raw hex")
                    narrator "Rejected. Somewhere, an attacker's script moves to plan B. The ugly little hardware screen just earned its keep."
                    call lesson("verify_hex")
                "Sign it anyway. It's probably a display bug.":
                    $ adjust(treasury=-60, security=-20, vibes=-15)
                    $ mark("Saw the mismatched hex and signed anyway")
                    narrator "It was not a display bug."
                    call lesson("verify_hex")

    ## 4a.3 Ice phishing — plan B (vault 4a.3)
    scene bg discord with fade
    show jordan hurt at right with dissolve
    j "Three members say the site asked them for weird token approvals tonight. Probably nothing? The mint is LIVE, [player_name]."
    menu:
        "Take the front end down. Now. Mid-mint.":
            $ adjust(vibes=-10, security=+15)
            $ mark("Took the site down mid-mint on a phishing report")
            narrator "You pull the plug on your own party. Post-mortem: injected script, harvesting approvals — a stolen CDN key. Three wallets grazed. It would have been three hundred."
            call lesson("ice_phishing")
        "Keep it up. Don't panic the mint over three reports.":
            $ adjust(vibes=-30, security=-15)
            $ mark("Kept the compromised front end up during the mint")
            narrator "By morning, ninety wallets are drained — your believers' wallets, not the treasury. That's the one loss you can't refund."
            call lesson("ice_phishing")
    jump ch4_triage

################################################################################
label ch4b_fiftyone:
    ## 4b.1 Red alert
    scene bg blockchain with fade
    if not maya_gone:
        show maya alarmed at left with dissolve
        m "RED ALERT. One entity just crossed 45%% of governance tokens. Eleven wallets, one owner."
    else:
        narrator "The alert comes from a community dashboard, hours late — the person who would have watched it in real time doesn't work here anymore. One entity holds 45%%."
    if alex_loyal:
        show alex sincere at right with dissolve
        a "It's Atlas. I'd know that gas-price signature anywhere. You have maybe a day before the proposal drops. Use it."
        $ adjust(security=+5)
    narrator "The proposal appears at dawn: 'Treasury Diversification Initiative.' Professional. Reasonable. Beautifully formatted."
    if timelocks:
        narrator "Buried in the code: a drain to an address Atlas controls. Your time-locks force a 7-day review — which is why anyone found it at all."
        call lesson("flashloan")
    else:
        narrator "Buried in the code: a drain function. And with no time-locks, it executes the moment it passes. A charming proposal to fund an animal shelter posts an hour later. (The distraction.)"
        call lesson("flashloan")
    show atlas predatory at right with dissolve
    w "Nothing personal, founder. Someone responsible was always going to end up holding the keys. I'd hoped you'd hand them over gently."

    ## 4b.2 KEYSTONE choice
    menu:
        "Emergency pause. Freeze governance. Founder key, one click.":
            $ adjust(security=+15, vibes=-20)
            $ veto_used = True
            $ mark("Emergency-paused governance to stop the whale")
            narrator "The attack stops. So does the pretense. 'Decentralized until it's inconvenient' — the quote-tweet does numbers. A splinter group forks off as 'TrueDAO' by the weekend."
            call lesson("capture")
        "Community defense: pool the small holders, delegate, outvote the whale." if rel_jordan >= 60 or vibes >= 50:
            $ adjust(vibes=+15, jordan=+15, vera=+10)
            $ mark("Beat the 51% attack with pooled community delegation")
            show vera warm at left with dissolve
            v "Solidarity is a governance primitive. Always was."
            narrator "Twelve hundred small wallets delegate to trusted stewards overnight. The proposal fails, 52 against. Atlas's tokens sit there, suddenly just... money."
            call lesson("capture")
        "Negotiate. Ask Atlas the price.":
            $ adjust(treasury=-50, atlas=+10, vibes=-10)
            $ mark("Paid Atlas off — 'a governance tax'")
            w "One hundred ETH and I walk away. Consider it a governance tax. Cheaper than the lesson, which you are also receiving."
            call lesson("capture")
    hide atlas with dissolve
    jump ch4_triage

################################################################################
label ch4c_spiral:
    ## 4c.1 The crash
    scene bg blockchain with fade
    narrator "No attacker this time. Just weather: the market drops 40%% in a week, and your token — being 90%% of your treasury — drops harder."
    if not maya_gone:
        show maya tired at left with dissolve
        m "Treasury purchasing power is down 70%%. Payroll is Thursday. I want it on record that I said the word 'barbell' in this room."
    narrator "The spiral logic is simple and airless: you need cash » you sell your token » the price falls » you need more cash."

    ## 4c.2 The choice
    menu:
        "Sell native into the crash. Payroll is sacred.":
            $ adjust(treasury=-30, vibes=-20, morale=+5)
            $ mark("Sold the native token into the crash to make payroll")
            narrator "Payroll clears. The chart now looks like a ski slope, and the community watched you shove."
            call lesson("death_spiral")
        "Emergency raise from Atlas. Whatever the terms.":
            $ whale_in = True
            $ adjust(treasury=+40, atlas=+15, vibes=-15)
            $ mark("Took Atlas's emergency money mid-crash")
            show atlas generous at right with dissolve
            w "Of course. Happy to help. We can discuss governance... later."
            call lesson("death_spiral")
        "Hibernate. Cut everything. Survive small.":
            $ adjust(morale=-25, burnout=+10, security=+5)
            $ mark("Cut everything and hibernated through the crash")
            narrator "Contributor pay paused. Grants paused. Dreams: paused. But the lights, technically, stay on."
            call lesson("death_spiral")
    jump ch4_triage

################################################################################
label ch4_triage:
    ## 4.5 Triage (vault 4.5)
    scene bg coworking with fade
    $ adjust(burnout=+20)
    narrator "Casualty accounting, morning after: Treasury [treasury] ETH. Vibes [vibes]. Security [security]. Morale [morale]. Burnout [burnout] — crises bill the founder first."
    narrator "The collective is still here. Changed — the way a house is changed by a fire it survived."
    if burnout >= 80:
        call forced_rest
    call chapter_close(90, ch_open_vibes)
    jump ch5_resolution
