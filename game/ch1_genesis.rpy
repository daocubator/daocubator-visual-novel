# Chapter 1 — Genesis Block (Day 1–7)
# vault: 03 Chapters/Chapter 1 - Genesis Block.md

label ch1_genesis:
    $ ch_open_vibes = vibes

    ## 1.1 Cold open — the resignation
    scene bg coworking with fade
    narrator "Day one. You badge out of BigCorp for the last time, savings account modest, group chat feral."
    pc "Okay. A collective. Actually collectively owned. What are we making?"
    menu:
        "A record label — artists own their masters, together.":
            $ venture = "label"
            $ mark("Founded a record label collective")
            narrator "A label. Contracts, catalogs, and a century of artists getting robbed to learn from."
        "A streetwear brand — drops decided by the community.":
            $ venture = "streetwear"
            $ mark("Founded a streetwear collective")
            narrator "Streetwear. Hype is a supply chain, and supply chains are where dreams meet customs forms."
        "An artist collective — shared studio, shared upside.":
            $ venture = "collective"
            $ mark("Founded an artist collective")
            narrator "An artist collective. The oldest idea here, wearing the newest clothes."

    ## 1.2 Meet Maya
    show maya neutral at right with dissolve
    m "Hey. I heard you're starting something interesting."
    m "Maya. Smart contracts, tokenomics, the whole stack. I've watched too many DAOs die of idealism to be polite about it."
    menu:
        "\"I'd love to have you on board!\"":
            $ adjust(maya=+5)
            show maya focused
            m "Cool. Enthusiasm noted. Now let me interrogate your governance philosophy anyway."
        "\"What's your take on decentralization?\"":
            $ adjust(maya=+12)
            show maya proud
            m "Correct first question."
            m "Decentralization is a spectrum, not a virtue. Pure democracy sounds great until your first 51%% attack. Smart governance is knowing when to decentralize."

    ## 1.3 The equity conversation — KEYSTONE (vault 1.3)
    show maya focused
    m "Before I write a single line: equity. Let's have the awkward conversation now, while we still like each other."
    menu:
        "\"50/50, obviously. We're in this together!\"":
            $ equity = "equal"
            $ adjust(morale=+10, maya=-5)
            $ mark("Chose a 50/50 equal split, no vesting")
            show maya tired
            m "...Sure. Feels fair today. Ask me again the month our contributions diverge."
            call lesson("equal_split")
        "\"Merit-based. We'll size it to contribution as we go.\"":
            $ equity = "merit"
            $ adjust(maya=+5)
            $ mark("Chose merit-based equity, terms loose")
            m "Ambitious. 'As we go' is doing a lot of work in that sentence. Get it in writing."
        "\"Four-year vesting, one-year cliff. For both of us. Papered.\"":
            $ equity = "vesting"
            $ adjust(morale=-5, maya=+15)
            $ mark("Set 4-year vesting with a 1-year cliff on day one")
            show maya proud
            m "You read the post-mortems. Okay. I'm in."
            call lesson("vesting")

    ## 1.4 Meet Jordan
    scene bg discord with fade
    show jordan hyped at right with dissolve
    j "YO. Your server is blowing up! I'm Jordan — community's my thing. Tech means nothing without the people, you know?"
    j "Also, heads up: you already have a troll farm, two quiet quitters, and one guy with a megaphone and empty hands. It's day one. This is normal."
    menu:
        "\"Community first. Build the onboarding and trust systems now.\"":
            $ adjust(jordan=+15, vibes=+10, treasury=-5)
            $ mark("Invested early in community systems")
            show jordan determined
            j "Reputation, progressive trust, actual moderation. It's unglamorous and it's everything. On it."
        "\"Growth now, systems later. Momentum is the moat.\"":
            $ adjust(jordan=-5, vibes=+5)
            $ apathy += 1
            show jordan hurt
            j "Momentum's great until the first fight. Fine — but I'm writing 'I said this' in the channel topic."

    ## 1.5 Meet Alex
    scene bg conference with fade
    show alex calculating at right with dissolve
    a "I've been reading your tokenomics draft. Alex — DeFi background, treasury management."
    a "You're leaving 40%% unallocated? Bold choice. ...Or reckless. Depends on your vesting schedule."
    menu:
        "\"Come run the treasury. Show me how to do it right.\"":
            $ adjust(alex=+10)
            $ mark("Recruited Alex to run the treasury")
            show alex smirk
            a "Smart. I'm expensive, but so is learning treasury management from Twitter threads."
        "\"Thanks, but the community will manage the treasury.\"":
            $ adjust(alex=-5, vibes=+5)
            show alex neutral
            a "Adorable. I'll be nearby when 'the community' meets its first bear market."

    ## 1.6 Vera at the mixer — the legal wrapper (vault 1.6)
    scene bg conference with fade
    show vera wry at right with dissolve
    v "So you're the new collective. I organized unions for thirty years — we were doing 'governance tokens' in 1936. We called them union cards."
    v "One question, founder: when this goes wrong — and something always goes wrong — who is legally holding the bag?"
    menu:
        "\"...Point taken. Set up the legal wrapper. Pay the $15k.\"":
            $ wrapper = "verein"
            $ adjust(treasury=-15, vera=+15, security=+10)
            $ mark("Paid for a legal wrapper (Swiss Verein)")
            show vera warm
            v "Boring, expensive, and correct. You may survive this industry yet."
        "\"We're decentralized. There's no bag and no holder.\"":
            $ wrapper = "none"
            $ adjust(vera=-5)
            show vera stern
            v "Mm. A court once served an entire DAO through the help-desk chat box. But sure. No bag."
            call lesson("partnership")

    ## 1.7 Spectre's DM (vault 1.7)
    scene bg apartment with fade
    narrator "2:47 AM. An encrypted message from an account with a hooded PFP and no history."
    show spectre typing at right with dissolve
    s "found a reentrancy path in your mint contract. you have not launched. this is the good timeline. voice call, camera off, or keep the bug."
    menu:
        "Take the call. Camera off is fine.":
            $ adjust(spectre=+15, security=+10)
            $ mark("Trusted Spectre's anonymous security report")
            show spectre neutral
            s "patched. you listen. that's rarer than the bug."
        "\"Who are you, really?\"":
            $ adjust(spectre=-5, security=+5)
            show spectre alert
            s "someone who reads bytecode for fun. wrong question, but i fixed it anyway. next time ask 'what did you find.'"
        "Ignore it. Anonymous accounts don't get calls.":
            $ adjust(spectre=-10)
            hide spectre with dissolve
            narrator "The account goes quiet. The bug does not."

    ## 1.8 Token design + Atlas foreshadow (vault 1.8)
    scene bg blockchain with fade
    narrator "Token design ceremony. This shapes everything that follows."
    menu:
        "Equal split between founders":
            $ adjust(morale=+5)
            narrator "Clean, simple, and — as Maya mutters — 'a tie waiting for a breaker.'"
        "Merit-weighted by contribution":
            $ adjust(morale=-5, vibes=+5)
            narrator "Fair in theory. The spreadsheet measuring 'contribution' becomes the most political document you own."
        "60%% to the community treasury":
            $ adjust(vibes=+15, treasury=+20)
            $ mark("Gave the community 60% of the token supply")
            narrator "The community cheers. Alex does math quietly, like a person at a funeral."
    narrator "Mint night. Donations trickle in — then one address deposits more than everyone else combined."
    show atlas guarded at right with dissolve
    w "Consider it a vote of confidence. I admire builders."
    hide atlas with dissolve
    narrator "The tokens never move again. They sit there. Waiting. (You will think about this later.)"

    ## 1.9 Chapter close
    scene bg coworking with fade
    narrator "The Genesis Block is complete. Your collective is born."
    narrator "The real challenges are just beginning."
    call chapter_close(30, ch_open_vibes)
    jump ch2_tge
