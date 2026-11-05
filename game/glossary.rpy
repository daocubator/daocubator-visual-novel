# Glossary — a collectible dictionary of business / crypto / DeFi / DAO jargon.
# vault: 01 Overview/Game Systems.md (Glossary & Plain Mode)
#
# How terms unlock (progress is persistent — it carries across playthroughs):
#   1. STORY — a term appears in dialogue, a menu choice, or a Lesson popup.
#      say_menu_text_filter wraps matches in {a=gloss:id} links; the character
#      callback unlocks them when the line is actually shown (the filter itself
#      must stay pure: Ren'Py also runs it during prediction and lint).
#   2. LINK — glossary entries link to each other. Following a † link to an
#      undiscovered entry unlocks it. Some terms are ONLY reachable this way.
#
# Entry body markup:  <id>  or  <id|display text>   (converted to {a=gloss:id}).
# `match` = regex fragments (case-insensitive, word-bounded) that find the term
# in story text. Check data + reachability with:  python scripts/check_glossary.py

################################################################################
## Data + pure helpers. scripts/check_glossary.py execs this block standalone,
## so it must not touch renpy / store / persistent.

init -10 python:
    import re as _gre

    GLOSS_CATS = [
        # (id, tab label, color)
        ("biz",    "BUSINESS", "#FFAA55"),
        ("crypto", "CRYPTO",   "#55FFFF"),
        ("defi",   "MONEY",    "#FFFF55"),
        ("dao",    "DAO",      "#FF55FF"),
        ("game",   "STATS",    "#55FF55"),
    ]
    GLOSS_CAT_NAMES = {
        "biz": "Business & Startups", "crypto": "Crypto & Tech",
        "defi": "Money & DeFi", "dao": "DAO & Governance", "game": "Game Stats",
    }

    GLOSSARY = [
        ## ── GAME STATS ────────────────────────────────────────────────────
        dict(id="vibes", term="Vibes", cat="game", match=[r"vibes"],
             text="One of your five stats. Vibes is how the wider community feels about your project: excitement, trust, hype. High Vibes help your <token> price and help you win votes. Low Vibes lead to fights — and sometimes a <fork>."),
        dict(id="security", term="Security", cat="game", match=[r"security"],
             text="One of your five stats. Security is how safe your money and systems are. Low Security makes attacks like <phishing> much easier. You raise it with an <audit>, a <multisig>, and good habits with your <seed_phrase|seed phrase>."),
        dict(id="morale", term="Morale", cat="game", match=[r"morale"],
             text="One of your five stats. Morale is how your core team feels. High Morale means people stay and do good work. Low Morale means people quit — like a <cofounder|co-founder> taking a better job."),

        ## ── DAO & GOVERNANCE ──────────────────────────────────────────────
        dict(id="dao", term="DAO", cat="dao", match=[r"DAOs?"],
             text="Decentralized Autonomous Organization. A group that runs itself with rules written in code on a <blockchain>, instead of with bosses. Members hold <governance_token|governance tokens> and vote on <proposal|proposals>. The group's money sits in a shared <treasury>."),
        dict(id="governance", term="Governance", cat="dao", match=[r"governance"],
             text="How a group makes decisions: who can suggest things, who can vote, and how votes are counted. In a <dao|DAO>, governance happens through <proposal|proposals> and token votes. Bad governance — not hackers — is the most common way DAOs die."),
        dict(id="governance_token", term="Governance Token", cat="dao", match=[r"governance tokens?"],
             text="A <token> that gives you votes. Usually one token = one vote, so people with more tokens have more power. This is why a <whale> can be dangerous: votes can be bought."),
        dict(id="proposal", term="Proposal", cat="dao", match=[r"proposals?"],
             text="A formal suggestion that members vote on, like 'spend 10 ETH on marketing'. In many DAOs a proposal that passes runs automatically as code — so read the code, not just the title. See <timelock|time-locks>."),
        dict(id="turnout", term="Turnout", cat="dao", match=[r"turnout"],
             text="The percent of members who actually vote. Average DAO turnout is only about 6 percent. Low turnout means a small group — or one <whale> — can decide everything. A common fix is <delegation>."),
        dict(id="quorum", term="Quorum", cat="dao", match=[r"quorums?"],
             text="The minimum number of votes needed for a vote to count. A quorum stops a tiny group from passing a <proposal> while nobody else is watching. Too high, though, and nothing ever passes (see <turnout>)."),
        dict(id="delegation", term="Delegation", cat="dao", match=[r"delegat(?:e|es|ed|ing|ion)(?! for a week)", r"liquid democracy"],
             text="Giving your voting power to someone you trust, who votes for you. Also called 'liquid democracy'. It raises <turnout>, but power can collect in a few hands: in many DAOs the top 10 percent of voters control about 76 percent of the votes. That's quiet <capture>."),
        dict(id="veto", term="Veto", cat="dao", match=[r"veto(?:es|ed)?"],
             text="The power to stop a decision alone, even after a vote. A founder veto can save a <dao|DAO> in an emergency — but every time you use it, you prove the group isn't really <decentralization|decentralized>."),
        dict(id="timelock", term="Time-lock", cat="dao", match=[r"time-?locks?"],
             text="A forced waiting time between a vote passing and the result happening — often a few days. It gives people time to read the code and react. A time-lock would have stopped the Beanstalk <flash_loan|flash loan> attack, which passed and ran in a single moment."),
        dict(id="multisig", term="Multisig", cat="dao", match=[r"multi-?sigs?"],
             text="Short for 'multi-signature wallet'. A <wallet> that needs several people to approve each payment — for example 3 out of 5 keyholders. One stolen <private_key|private key> is not enough to take the money."),
        dict(id="attack51", term="51% Attack", cat="dao", match=[r"51%{1,2} attack"],
             text="When one person or group gets more than half of the votes (or, on a blockchain, half the computing power) and can force any decision. In a DAO this usually means a <whale> quietly buying <governance_token|governance tokens> from many wallets. See <capture>."),
        dict(id="capture", term="Governance Capture", cat="dao", match=[r"(?:governance )?capture"],
             text="When one person or group takes control of a DAO's decisions — usually by buying votes, or because nobody else votes. It rarely looks like a robbery. It looks like help. Build Finance DAO lost about 470,000 dollars this way in 2022."),
        dict(id="fork", term="Fork", cat="dao", match=[r"fork(?:s|ed|ing)?"],
             text="A split. Unhappy members copy the code (and sometimes part of the money) and start their own version of the project. The community, the <token> and the <treasury> all get divided."),
        dict(id="decentralization", term="Decentralization", cat="dao", match=[r"decentrali[sz](?:ation|ed|e|ing)"],
             text="Spreading power across many people instead of a few. It is a spectrum, not yes-or-no. More decentralization means more fairness and no single point of failure — but slower decisions and more chances for <capture> when nobody shows up to vote."),
        dict(id="whale", term="Whale", cat="dao", match=[r"whales?"],
             text="Someone who holds a very large amount of a <token>. In a <dao|DAO>, a whale has a lot of votes. A whale can be a helpful investor — or the beginning of a <attack51|51% attack>."),
        dict(id="legal_wrapper", term="Legal Wrapper", cat="dao", match=[r"legal wrappers?", r"Verein"],
             text="A real-world legal company (like a Swiss Verein or a US LLC) that 'wraps' a DAO. If something goes wrong, the company is responsible — not each member personally. Without one, a court may treat your DAO as a <general_partnership|general partnership>."),
        dict(id="general_partnership", term="General Partnership", cat="dao", match=[r"general partnerships?"],
             text="A business type where every partner is personally responsible for ALL of the business's debts. A US court decided the Ooki DAO was one, so its members could be held personally liable — they were even served legal papers through the website's help chat. A <legal_wrapper|legal wrapper> prevents this."),

        ## ── CRYPTO & TECH ─────────────────────────────────────────────────
        dict(id="blockchain", term="Blockchain", cat="crypto", match=[r"blockchains?", r"on-chain"],
             text="A shared record of transactions that thousands of computers keep at the same time, so nobody can secretly change it. Ethereum is a blockchain. <token|Tokens>, <smart_contract|smart contracts> and <dao|DAOs> all live on top of one."),
        dict(id="genesis_block", term="Genesis Block", cat="crypto", match=[r"genesis block"],
             text="The very first block of a <blockchain>. People use it to mean 'the very beginning of something' — which is why Chapter 1 has this name."),
        dict(id="token", term="Token", cat="crypto", match=[r"tokens?"],
             text="A digital item on a <blockchain>. A token can work like money, like a company share, or like a voting card (a <governance_token|governance token>). Your project creates its own — a <native_token|native token> — on launch day, its <tge|TGE>."),
        dict(id="tokenomics", term="Tokenomics", cat="crypto", match=[r"tokenomics"],
             text="Token + economics. The plan for your <token>: how many exist, who gets them, when they <vesting|unlock>, and why anyone would want them."),
        dict(id="tge", term="TGE", cat="crypto", match=[r"token generation events?", r"TGE"],
             text="Token Generation Event: the day a <token> is created and starts trading. A bit like a company's first day on the stock market — but much faster, and with far fewer rules. That's why <regulator|regulators> watch them."),
        dict(id="mint", term="Mint", cat="crypto", match=[r"mint(?:s|ed|ing)?"],
             text="To create new <token|tokens> or NFTs. 'Mint night' is when people can first get them. Minting can also be an attack: whoever controls <governance> may be able to mint a billion new tokens for themselves."),
        dict(id="burn", term="Burn", cat="crypto", match=[r"burn(?:s|ed|ing)?"],
             text="To destroy <token|tokens> on purpose by sending them to an <address> nobody can ever use. A founder burn means giving up some of your own tokens — and the votes that come with them — to show trust."),
        dict(id="eth", term="ETH (Ξ)", cat="crypto", match=[r"ETH", r"ether"],
             text="Ether: the money of the Ethereum <blockchain>. You use it to buy things and to pay <gas>. In this game your <treasury> is counted in ETH — that's the Ξ symbol."),
        dict(id="gas", term="Gas", cat="crypto", match=[r"gas"],
             text="The small fee you pay the network for each transaction on a <blockchain>. How a <wallet> pays gas (how much, and when) can work like a fingerprint — that's how Spectre and Alex spot one person behind many wallets."),
        dict(id="wallet", term="Wallet", cat="crypto", match=[r"wallets?"],
             text="An app or device that holds your <private_key|private keys> and lets you send <token|tokens>. Browser-extension wallets like MetaMask are easy to use but can be hacked. Compare a <hot_wallet|hot wallet> with a <hardware_wallet|hardware wallet>."),
        dict(id="hot_wallet", term="Hot Wallet", cat="crypto", match=[r"hot wallets?"],
             text="A <wallet> that is connected to the internet. Easy to use, easy to hack. Rule of thumb: keep only 5–10 percent of your funds in hot wallets, and the rest in <cold_storage|cold storage>."),
        dict(id="cold_storage", term="Cold Storage", cat="crypto", match=[r"cold storage"],
             text="Keeping crypto keys offline — in a <hardware_wallet|hardware wallet>, or behind a <multisig>. Slower to use, much harder to steal. Anything above about 10,000 dollars belongs here."),
        dict(id="hardware_wallet", term="Hardware Wallet", cat="crypto", match=[r"hardware wallets?", r"hardware screen"],
             text="A small physical device that keeps your <private_key|private keys> offline. Its tiny screen shows what you are REALLY signing, even if your computer is full of <malware>. Always read it. See <hex|raw data>."),
        dict(id="seed_phrase", term="Seed Phrase", cat="crypto", match=[r"seed phrases?", r"recovery phrases?"],
             text="12 or 24 secret words that can rebuild your whole <wallet>. Anyone who sees them can take everything, forever. Never type them into a website, a chat, or a shared document. Ever."),
        dict(id="private_key", term="Private Key", cat="crypto", match=[r"private keys?", r"founder key"],
             text="The secret code that proves you own a <wallet>. Your <seed_phrase|seed phrase> creates it. If someone copies your private key, then on the <blockchain> they ARE you."),
        dict(id="smart_contract", term="Smart Contract", cat="crypto", match=[r"smart contracts?"],
             text="A program that runs on a <blockchain>. It holds money and follows its rules automatically — nobody can stop it once it runs. That's why contracts need an <audit>. Usually written in <solidity|Solidity>."),
        dict(id="solidity", term="Solidity", cat="crypto", match=[r"Solidity"],
             text="The most popular programming language for writing <smart_contract|smart contracts> on Ethereum. 4,000 lines of it is a lot to check alone at 4 a.m."),
        dict(id="bytecode", term="Bytecode", cat="crypto", match=[r"bytecode"],
             text="The machine version of a <smart_contract|smart contract> — what the computer actually runs, after the human-readable <solidity|Solidity> is compiled. Experts read it to find hidden bugs like <reentrancy>."),
        dict(id="reentrancy", term="Reentrancy", cat="crypto", match=[r"reentrancy"],
             text="A famous kind of <smart_contract|smart contract> bug. An attacker's contract calls back into yours before yours finishes updating its records, and takes the money again and again. It caused 'The DAO' hack in 2016."),
        dict(id="audit", term="Audit", cat="crypto", match=[r"audit(?:s|ed|ing|ors?)?"],
             text="An expert review of code (or of money) to find problems before attackers do. A security audit is expensive. A hack is much more expensive. Auditors look for bugs like <reentrancy>."),
        dict(id="address", term="Address", cat="crypto", match=[r"address(?:es)?"],
             text="A long code like 0x4A21…9DEB that identifies a <wallet> or a <smart_contract|contract>. Attackers create addresses that look almost the same as real ones, so check every character. See <hex>."),
        dict(id="hex", term="Hex / Raw Data", cat="crypto", match=[r"hex", r"raw data"],
             text="The raw code of a transaction, written in hexadecimal (0–9 and a–f). Your wallet app shows a friendly summary, but <malware> can fake that summary. The raw data — best read on a <hardware_wallet|hardware wallet> — shows the truth."),
        dict(id="phishing", term="Phishing", cat="crypto", match=[r"phish(?:ing|ed)?"],
             text="Tricking people into giving away secrets or signing something bad, using fake messages, websites or apps. In crypto, one bad signature can lose everything. A sneaky version: <ice_phishing|ice phishing>."),
        dict(id="ice_phishing", term="Ice Phishing", cat="crypto", match=[r"ice phishing"],
             text="A <phishing> attack where you're tricked into giving a <token_approval|token approval>. You never give away your keys — but the attacker can now move your tokens. Badger DAO users lost 121 million dollars this way, through a hacked <front_end|front end>."),
        dict(id="token_approval", term="Token Approval", cat="crypto", match=[r"(?:token )?approvals?"],
             text="Permission you give a <smart_contract|smart contract> to move your <token|tokens> for you. Apps need it to work. But an unlimited approval to a bad contract lets it empty your wallet later, whenever it wants."),
        dict(id="front_end", term="Front End", cat="crypto", match=[r"front[- ]ends?"],
             text="The website or app people use to talk to your <smart_contract|smart contracts>. Even if the contract is perfect, a hacked front end can trick users into signing bad things. It's protected by keys like your <cdn|CDN key>."),
        dict(id="cdn", term="CDN Key", cat="crypto", match=[r"CDN(?: keys?)?"],
             text="A Content Delivery Network serves your website quickly around the world. Its API key works like a password for changing your site. A stolen CDN key lets an attacker quietly add bad code to your <front_end|front end>."),
        dict(id="malware", term="Malware", cat="crypto", match=[r"malware"],
             text="Bad software that runs secretly on your computer. Crypto malware can change what your <wallet> shows you, or swap the <address> you are paying for the attacker's."),
        dict(id="pfp", term="PFP", cat="crypto", match=[r"PFPs?"],
             text="Profile picture. In crypto, many people use an NFT or a cartoon as their PFP and never show their real face or name. Anonymous people are called 'anons'."),

        ## ── MONEY & DEFI ──────────────────────────────────────────────────
        dict(id="defi", term="DeFi", cat="defi", match=[r"DeFi"],
             text="Decentralized Finance: banking-style services — trading, loans, savings — run by <smart_contract|smart contracts> instead of banks. Open and fast, but there is nobody to call when something breaks. Home of the <flash_loan|flash loan>."),
        dict(id="treasury", term="Treasury", cat="defi", match=[r"treasury", r"treasuries"],
             text="The shared money of a group or company. In a <dao|DAO> it sits in a <wallet> (ideally a <multisig>) and members vote on how to spend it. In this game Treasury is also a stat, counted in <eth|ETH>."),
        dict(id="native_token", term="Native Token", cat="defi", match=[r"native(?: tokens?)?"],
             text="The <token> your own project creates. Exciting to hold — but its price falls exactly when your project has problems. A <treasury> full of it can fall into a <death_spiral|death spiral>."),
        dict(id="stablecoin", term="Stablecoin", cat="defi", match=[r"stablecoins?", r"stables"],
             text="A <token> designed to always be worth about 1 US dollar (USDC is one example). Boring — and that's the point: it doesn't crash when your project does. Also called 'stables'. The safe end of a <barbell>."),
        dict(id="barbell", term="Barbell Strategy", cat="defi", match=[r"barbell"],
             text="Splitting money into two very different ends: a big safe part (30–50 percent in <stablecoin|stablecoins>) and a risky part (your <native_token|native token>). The safe end keeps you alive in a bad month. It costs a few <swap_fee|swap fees>."),
        dict(id="swap_fee", term="Swap Fee", cat="defi", match=[r"swap fees?"],
             text="The small fee you pay to trade one <token> for another. A cheap price for safety when you build a <barbell>."),
        dict(id="death_spiral", term="Death Spiral", cat="defi", match=[r"death spirals?", r"spiral"],
             text="A trap: you need cash → you sell your own <token> → its price drops → you must sell even more → repeat. It happens when a <treasury> is mostly <native_token|native token> and a <bear_market|bear market> arrives."),
        dict(id="flash_loan", term="Flash Loan", cat="defi", match=[r"flash[- ]?loans?", r"flash-borrowed"],
             text="A huge loan that is borrowed and paid back inside ONE transaction — a few seconds. No collateral needed. Attackers use flash loans to borrow millions of votes for one moment. A <timelock|time-lock> makes that useless."),
        dict(id="bear_market", term="Bear Market", cat="defi", match=[r"bear markets?"],
             text="A long period when prices keep falling and people are scared. The opposite is a 'bull market'. A plan that only works when prices go up (<number_go_up|number go up>) dies in a bear market."),
        dict(id="candle", term="Candle", cat="defi", match=[r"candles?"],
             text="One bar on a price chart. It shows where the price started, ended, and how high and low it went in that time. 'Remember this candle' means 'remember this price — it won't last'."),
        dict(id="number_go_up", term="Number Go Up", cat="defi", match=[r"number goes? up"],
             text="A crypto joke about believing the <token> price will only ever rise. A strategy built on Number Go Up has no plan for the bad day — see <death_spiral|death spiral>."),
        dict(id="carbon_credit", term="Carbon Credit", cat="defi", match=[r"carbon[- ]credits?"],
             text="A certificate saying one ton of CO₂ was removed or avoided. Companies buy them to 'offset' their pollution. Some are worthless — like credits from old dams that were going to exist anyway. Buying those is <greenwashing>."),
        dict(id="greenwashing", term="Greenwashing", cat="defi", match=[r"greenwash(?:ing|ed)?"],
             text="Making something look good for the planet when it isn't. Tying your project to junk <carbon_credit|carbon credits> can destroy trust overnight. The defence is <due_diligence|due diligence>."),

        ## ── BUSINESS & STARTUPS ───────────────────────────────────────────
        dict(id="equity", term="Equity", cat="biz", match=[r"equity"],
             text="Ownership of a company, split into shares. If you hold 10 percent of the equity, you own 10 percent of the company. Founders should agree on equity early, in writing — see <vesting> and <equal_split|equal split>."),
        dict(id="equal_split", term="Equal Split", cat="biz", match=[r"equal splits?", r"50/50"],
             text="Giving every founder the same share (like 50/50) on day one. It feels fair, but often it's a way to avoid a hard conversation. Later, when people do different amounts of work, it causes fights. Pair any split with <vesting>."),
        dict(id="vesting", term="Vesting", cat="biz", match=[r"(?:un)?vest(?:ing|ed|s)?"],
             text="Earning your <equity> or <token|tokens> slowly over time, not all at once. The standard is 4 years with a 1-year <cliff>. If someone leaves early, the unvested part goes back to the company — no <dead_equity|dead equity>."),
        dict(id="cliff", term="Cliff", cat="biz", match=[r"cliffs?"],
             text="A waiting time before ANY <vesting> starts. With a 1-year cliff, someone who leaves after 11 months gets nothing; after 12 months they get the first quarter. It protects the team from people who leave very early."),
        dict(id="dead_equity", term="Dead Equity", cat="biz", match=[r"dead equity"],
             text="Shares held by someone who no longer works on the project. They still own part of it and can still vote, but add nothing. Investors hate it — it makes a messy <cap_table|cap table>. <vesting|Vesting> prevents it."),
        dict(id="cap_table", term="Cap Table", cat="biz", match=[r"cap tables?"],
             text="Capitalization table: the list of who owns what percent of a company. Investors read it first. A messy cap table — for example, full of <dead_equity|dead equity> — scares them away."),
        dict(id="cofounder", term="Co-founder", cat="biz", match=[r"co-?founders?"],
             text="One of the people who start a company together. Co-founder problems — fights about <equity>, effort, or direction — are one of the top reasons startups fail. Decide the hard things early."),
        dict(id="board_seat", term="Board Seat", cat="biz", match=[r"board seats?"],
             text="A place on the board of directors: the small group that controls a company's biggest decisions. Investors often ask for one in exchange for money. 'No board seat' means 'you get money, not control'."),
        dict(id="runway", term="Runway", cat="biz", match=[r"runway"],
             text="How long your company can survive with the money it has. '18 months of runway' means 18 months until the bank account hits zero — unless you earn or raise more. Missing <payroll> means the runway is over."),
        dict(id="payroll", term="Payroll", cat="biz", match=[r"payroll"],
             text="Paying salaries to the people who work for you, on time, every time. Missing payroll is one of the fastest ways to lose a team — and it's why a <death_spiral|death spiral> hurts so much."),
        dict(id="deferred_salary", term="Deferred Salary", cat="biz", match=[r"deferred salary"],
             text="Working now and getting paid later — or taking less pay now and more <equity> instead. Common in early startups. It's a real cost for that person, and they remember it."),
        dict(id="moat", term="Moat", cat="biz", match=[r"moats?"],
             text="Something that protects a business from competitors, like the water around a castle. Strong brands, loyal communities and patents are moats. 'Momentum is the moat' means 'growing fast will protect us' (it usually won't, alone)."),
        dict(id="standup", term="Standup", cat="biz", match=[r"stand-?ups?"],
             text="A short daily team meeting (often 15 minutes, sometimes literally standing) where everyone shares what they're working on. When someone goes quiet at standups, check on them — see <burnout>."),
        dict(id="postmortem", term="Post-mortem", cat="biz", match=[r"post-?mortems?"],
             text="A careful, honest review after something fails: what went wrong, and why. This whole game is built from real DAO and startup post-mortems. Reading them is the cheapest education there is."),
        dict(id="burnout", term="Burnout", cat="biz", match=[r"burnout"],
             text="Deep physical and mental exhaustion from long-term stress. Founders get it constantly. In this game Burnout is a stat: at 60 or more your judgment gets worse (and the game stops being honest with you), and at 80 you are forced to rest."),
        dict(id="exit", term="Exit", cat="biz", match=[r"exits?"],
             text="How founders and investors finally get their money out — usually by selling the company (an <acquisition>) or by listing it on a stock market. 'We didn't build an exit' means 'we're not building this to sell it'."),
        dict(id="acquisition", term="Acquisition", cat="biz", match=[r"acquisitions?", r"acqui-hires?", r"acquir(?:e|es|ed|ing)"],
             text="When one company buys another. An 'acqui-hire' is buying a company mostly to hire its team; the product often gets shut down. It's one kind of <exit>."),
        dict(id="unicorn", term="Unicorn", cat="biz", match=[r"unicorns?"],
             text="A private startup worth more than 1 billion dollars. Rare, like the animal. Most good companies are not unicorns, and that's fine."),
        dict(id="regulator", term="Regulator", cat="biz", match=[r"regulators?"],
             text="A government agency that makes and enforces the rules for an industry — like the SEC or CFTC in the US. Regulators often ask whether a <token> is really an investment product sold without permission. A <legal_wrapper|legal wrapper> gives them someone to talk to besides your members."),
        dict(id="due_diligence", term="Due Diligence", cat="biz", match=[r"(?:due )?diligence(?:d)?"],
             text="Checking the facts carefully before you agree to a deal. Is the money real? Is the product real? Who is behind it? Skipping diligence is how <greenwashing> deals happen."),
        dict(id="advance", term="Advance", cat="biz", match=[r"advances?"],
             text="Money a label or partner pays you up front. It sounds like a gift, but it's a loan you repay out of your future earnings — see <recoupment>."),
        dict(id="recoupment", term="Recoupment", cat="biz", match=[r"recoup(?:s|ed|able|ables|ment)?"],
             text="When a partner takes back an <advance> from your earnings before you get paid anything. Music labels often recoup at 10–20 cents per dollar you earn, so it can take years — or forever, with <cross_collat|cross-collateralization>."),
        dict(id="deal_360", term="360 Deal", cat="biz", match=[r"360(?: deals?)?"],
             text="A music contract where the label takes a share of everything an artist earns — not only records, but touring and merch too. Often paired with <cross_collat|cross-collateralization>."),
        dict(id="cross_collat", term="Cross-collateralization", cat="biz", match=[r"cross-collateraliz(?:e|es|ed|ation)"],
             text="Using the profit from one project to pay the debt of another. If Album A loses money, the label takes it out of Album B's profits. Artists can stay in debt forever. Ask for it to be removed when you negotiate an <advance>."),
        dict(id="masters", term="Masters", cat="biz", match=[r"masters"],
             text="The original recordings of a song. Whoever owns the masters controls — and earns from — every copy and every stream. Many famous artists don't own theirs; a <deal_360|360 deal> rarely gives them back."),
        dict(id="preorder", term="Pre-order", cat="biz", match=[r"pre-?orders?"],
             text="Selling a product before you make it. If people pay, you know the demand is real — a cheap way to <validation|validate> an idea. It also limits <chargeback|chargebacks>, because you only promise what you can actually ship."),
        dict(id="validation", term="Validation", cat="biz", match=[r"(?:un)?validat(?:e|ed|ion)"],
             text="Proving people really want a product before you spend lots of money making it. Example: a <preorder|pre-order> for one item before you make eight. The opposite is building on hype."),
        dict(id="cut_and_sew", term="Cut-and-sew", cat="biz", match=[r"cut-and-sew"],
             text="Clothing made from scratch: you design the pattern, choose the fabric, and a factory cuts and sews it. Much slower and more expensive than printing a logo on ready-made shirts. Watch your <unit_cost|unit cost>."),
        dict(id="unit_cost", term="Unit Cost", cat="biz", match=[r"unit costs?"],
             text="How much it costs to make and ship ONE item. If you sell below unit cost, every sale loses money — so more sales means bigger losses. See <overfunding>."),
        dict(id="overfunding", term="Overfunding", cat="biz", match=[r"overfund(?:ed|ing)?"],
             text="When a crowdfunding campaign raises far more than its goal. It sounds great, but you promised a price that may not work at a bigger size. Coolest Cooler raised 13 million dollars and still went bankrupt — every sale was below <unit_cost|unit cost>."),
        dict(id="chargeback", term="Chargeback", cat="biz", match=[r"chargebacks?"],
             text="When a customer asks their bank to reverse a card payment. Too many chargebacks — more than about 1 percent — and your <payment_processor|payment processor> can freeze ALL your money, not just the disputed orders."),
        dict(id="payment_processor", term="Payment Processor", cat="biz", match=[r"payment processors?"],
             text="A company like Stripe or PayPal that handles card payments for you. They are a partner with very little patience: too many <chargeback|chargebacks> and they freeze your account."),
    ]

    GLOSS = {e["id"]: e for e in GLOSSARY}
    GLOSS_CAT_COLORS = dict((c[0], c[2]) for c in GLOSS_CATS)
    for _e in GLOSSARY:
        _e["cat_color"] = GLOSS_CAT_COLORS.get(_e["cat"], "#FFFFFF")
        _e["masked"] = _e["term"][0] + "·" * min(len(_e["term"]) - 1, 9)

    ## One big case-insensitive regex; one named group per entry. Entries with
    ## longer patterns go first so "governance token" beats "governance".
    def _gloss_build_re():
        order = sorted(GLOSSARY, key=lambda e: -max(len(p) for p in e["match"]))
        alts = []
        for e in order:
            pats = sorted(e["match"], key=len, reverse=True)
            alts.append("(?P<%s>%s)" % (e["id"], "|".join(pats)))
        return _gre.compile(r"\b(?:" + "|".join(alts) + r")\b", _gre.IGNORECASE)

    GLOSS_RE = _gloss_build_re()

    ## Text tags {..}, escaped braces, and [interpolations] are never matched.
    _GLOSS_TAG_RE = _gre.compile(r"(\{\{|\[\[|\{[^{}]*\}|\[[^\[\]]*\])")
    _GLOSS_KEEP = ("i", "b", "size")   # hyperlink style resets these; re-open inside links

    def gloss_find_ids(s):
        """Glossary ids mentioned in displayed text (tags/interpolation skipped)."""
        found = []
        for k, part in enumerate(_GLOSS_TAG_RE.split(s or "")):
            if k % 2:
                continue
            for m in GLOSS_RE.finditer(part):
                if m.lastgroup not in found:
                    found.append(m.lastgroup)
        return found

    def gloss_link_text(s):
        """Wrap the first mention of each term in {a=gloss:id}. Pure function."""
        if not s:
            return s
        out = []
        linked = set()
        stack = []          # open formatting tags: (name, open_tag)
        in_link = 0
        for k, part in enumerate(_GLOSS_TAG_RE.split(s)):
            if k % 2:
                out.append(part)
                if part.startswith("{") and not part.startswith("{{"):
                    body = part[1:-1]
                    name = body.split("=", 1)[0]
                    if name == "a":
                        in_link += 1
                    elif name == "/a":
                        in_link = max(0, in_link - 1)
                    elif name in _GLOSS_KEEP:
                        stack.append((name, part))
                    elif name.startswith("/") and name[1:] in _GLOSS_KEEP:
                        for i in range(len(stack) - 1, -1, -1):
                            if stack[i][0] == name[1:]:
                                del stack[i]
                                break
                continue
            if in_link or not part:
                out.append(part)
                continue
            pos = 0
            for m in GLOSS_RE.finditer(part):
                gid = m.lastgroup
                if gid in linked:
                    continue
                linked.add(gid)
                reopen = "".join(t for _, t in stack)
                reclose = "".join("{/%s}" % n for n, _ in reversed(stack))
                out.append(part[pos:m.start()])
                out.append("{a=gloss:%s}%s%s%s{/a}" % (gid, reopen, m.group(0), reclose))
                pos = m.end()
            out.append(part[pos:])
        return "".join(out)

    ## Exact inverse of gloss_link_text: the link tag plus the formatting tags
    ## it re-opened. Needed because menu labels are filtered BEFORE the
    ## translation lookup, whose key is the original text.
    _GLOSS_UNLINK_RE = _gre.compile(
        r"\{a=gloss:\w+\}(?:\{(?:i|b|size=[^{}]*)\})*(.*?)(?:\{/(?:i|b|size)\})*\{/a\}")

    def gloss_unlink(s):
        return _GLOSS_UNLINK_RE.sub(r"\1", s or "")

    def gloss_strip_links(s):
        """Menu choices are buttons — hyperlinks can't live inside them. Underline instead."""
        return _gre.sub(r"\{a=gloss:\w+\}(.*?)\{/a\}", r"{u}\1{/u}", s)

    _GLOSS_MARKUP_RE = _gre.compile(r"<(\w+)(?:\|([^<>]+))?>")

    def gloss_body_links(text):
        """(id, display) pairs for each <id|display> link in an entry body."""
        return [(m.group(1), m.group(2) or GLOSS.get(m.group(1), {}).get("term", m.group(1)))
                for m in _GLOSS_MARKUP_RE.finditer(text)]

    def gloss_render_body(text, found):
        """Entry body → Ren'Py text. Undiscovered targets get a † after and magenta."""
        def rep(m):
            gid = m.group(1)
            disp = m.group(2) or GLOSS[gid]["term"]
            if gid in found:
                return "{a=gloss:%s}%s{/a}" % (gid, disp)
            return "{a=gloss:%s}{color=#FF55FF}%s†{/color}{/a}" % (gid, disp)
        return _GLOSS_MARKUP_RE.sub(rep, text)

    GLOSS_RANKS = [
        # (min fraction discovered, title)
        (0.00, "TOURIST"),
        (0.10, "LURKER"),
        (0.25, "ANON"),
        (0.45, "CONTRIBUTOR"),
        (0.65, "CORE CONTRIBUTOR"),
        (0.85, "DELEGATE"),
        (1.00, "DAO ELDER"),
    ]

    def gloss_rank(n_found):
        frac = n_found / float(len(GLOSSARY))
        title = GLOSS_RANKS[0][1]
        for lo, t in GLOSS_RANKS:
            if frac >= lo:
                title = t
        return title

    def gloss_bar(n, total, width=20):
        filled = int(round(width * n / float(total))) if total else 0
        return "█" * filled + "░" * (width - filled)

################################################################################
## Ren'Py wiring: persistence, unlocking, dialogue filter, hyperlink protocol.

default persistent.gloss_found = {}      # id -> "story" | "link"
default persistent.gloss_read = set()    # ids the player has opened
default persistent.gloss_links = True    # preference: link terms in dialogue
default persistent.gloss_sel = None      # last entry viewed (UI state)
default persistent.gloss_cat = "all"     # last category tab (UI state)
default persistent._gloss_fresh = None   # entry just discovered via a link

init python:
    def gloss_unlock(ids, how="story", toast=True):
        """Unlock ids; returns the newly discovered ones (and toasts them)."""
        new = [i for i in ids if i in GLOSS and i not in persistent.gloss_found]
        for i in new:
            persistent.gloss_found[i] = how
        if new and toast:
            renpy.show_screen("gloss_toast", names=[GLOSS[i]["term"] for i in new],
                              n=len(persistent.gloss_found))
        return new

    def gloss_unlock_text(*texts):
        """Unlock every term in `texts`. Returns None ON PURPOSE: it's used as a
        screen action (choice screen `on "show"`), and a non-None return from an
        action ends the interaction — the menu would 'choose' the return value."""
        ids = []
        for t in texts:
            for i in gloss_find_ids(t):
                if i not in ids:
                    ids.append(i)
        gloss_unlock(ids)
        return None

    def gloss_mark_read(gid):
        if gid in persistent.gloss_found and gid not in persistent.gloss_read:
            persistent.gloss_read.add(gid)

    def gloss_select(gid):
        persistent.gloss_sel = gid
        persistent._gloss_fresh = None
        gloss_mark_read(gid)

    def gloss_set_cat(cat):
        """Switch tab; keep the selection if it's in the tab, else select the
        tab's first discovered entry (so it counts as read)."""
        persistent.gloss_cat = cat
        sel = persistent.gloss_sel
        if sel in GLOSS and (cat == "all" or GLOSS[sel]["cat"] == cat):
            return None
        first = next((e["id"] for e in gloss_entries(cat) if e["id"] in persistent.gloss_found), None)
        if first:
            gloss_select(first)
        return None

    def gloss_entries(cat):
        es = [e for e in GLOSSARY if cat == "all" or e["cat"] == cat]
        return sorted(es, key=lambda e: e["term"].lower())

    def gloss_masked(term):
        """Locked entries show first letter + dots — a little hangman hint."""
        return term[0] + "·" * min(len(term) - 1, 9)

    def gloss_count(cat=None):
        es = [e for e in GLOSSARY if cat is None or e["cat"] == cat]
        return len([e for e in es if e["id"] in persistent.gloss_found]), len(es)

    def gloss_link_count():
        return len([1 for v in persistent.gloss_found.values() if v == "link"])

    ## Dialogue + menu text: link terms. Must be pure (also runs in predict/lint).
    def gloss_say_filter(s):
        if not persistent.gloss_links:
            return s
        return gloss_link_text(s)

    config.say_menu_text_filter = gloss_say_filter

    ## Menu choice caption: unlink → translate (plain mode) → underline terms.
    def gloss_choice_raw(caption):
        return __(gloss_unlink(caption))

    def gloss_choice_text(caption):
        return gloss_strip_links(gloss_say_filter(gloss_choice_raw(caption)))

    ## Unlock when a line is actually displayed. `what` is the final text.
    def gloss_character_callback(event, interact=True, what=None, **kwargs):
        if event == "begin" and interact and what:
            gloss_unlock_text(what)

    config.all_character_callbacks.append(gloss_character_callback)

    ## {a=gloss:id} — from dialogue/history/lessons: open the glossary on that
    ## entry. From inside the glossary: follow the link (this is how LINK
    ## unlocks happen).
    def gloss_hyperlink(gid):
        if gid not in GLOSS:
            return None
        in_menu = renpy.context()._menu
        new = gloss_unlock([gid], "link" if in_menu else "story", toast=False)
        persistent.gloss_sel = gid
        persistent._gloss_fresh = gid if new else None
        gloss_mark_read(gid)
        if persistent.gloss_cat not in ("all", GLOSS[gid]["cat"]):
            persistent.gloss_cat = GLOSS[gid]["cat"]
        if in_menu and renpy.get_screen("glossary"):
            renpy.restart_interaction()
        else:
            renpy.run(ShowMenu("glossary"))
        return None

    config.hyperlink_handlers["gloss"] = gloss_hyperlink

################################################################################
## Screens

## Toast: "◆ NEW TERM ◆" — top-right, under the HUD.
screen gloss_toast(names, n):
    zorder 200
    tag gloss_toast
    timer 3.0 action Hide("gloss_toast")
    frame at gloss_toast_appear:
        xalign 1.0
        ypos 70
        background Frame("gui/notify.png", gui.notify_frame_borders)
        padding (32, 14)
        vbox:
            spacing 4
            text ("◆ NEW TERM ◆" if len(names) == 1 else "◆ %d NEW TERMS ◆" % len(names)) color "#FFFF55" size 22
            text ", ".join(names) color "#FFFFFF" size 24 substitute False
            text "GLOSSARY %d/%d  ·  press G" % (n, len(GLOSSARY)) color "#AAAAAA" size 18

transform gloss_toast_appear:
    on show:
        alpha 0.0 xoffset 20
        easein 0.25 alpha 1.0 xoffset -20
    on hide:
        linear 0.4 alpha 0.0

## The glossary itself — a game-menu screen.
screen glossary():
    tag menu

    $ cat = persistent.gloss_cat
    $ entries = gloss_entries(cat)
    $ cur = persistent.gloss_sel
    if cur not in GLOSS:
        $ cur = next((e["id"] for e in entries if e["id"] in persistent.gloss_found), None)
    $ n_found, n_total = gloss_count()
    ## Open the list scrolled to the selected entry (applies when the screen opens).
    $ sel_idx = next((i for i, e in enumerate(entries) if e["id"] == cur), 0)

    on "show" action Function(gloss_mark_read, cur)

    use game_menu(_("Glossary")):

        vbox:
            spacing 14

            ## Progress header
            hbox:
                spacing 24
                text "[n_found]/[n_total] TERMS" color "#FFFF55" size 26
                text gloss_bar(n_found, n_total) color "#55FFFF" size 22 yalign 0.5
                text "RANK: " + gloss_rank(n_found) color "#FF55FF" size 26
                text "† via links: %d" % gloss_link_count() color "#AAAAAA" size 22 yalign 0.5

            ## Category tabs
            hbox:
                spacing 6
                textbutton "ALL":
                    action Function(gloss_set_cat, "all")
                    selected cat == "all"
                    style "gloss_tab"
                for cid, clabel, ccol in GLOSS_CATS:
                    $ cf, ct = gloss_count(cid)
                    textbutton "%s %d/%d" % (clabel, cf, ct):
                        action Function(gloss_set_cat, cid)
                        selected cat == cid
                        style "gloss_tab"
                        text_color ccol

            hbox:
                spacing 24

                ## Term list
                frame:
                    background Frame("gui/button/slot_idle_background.png", gui.slot_button_borders)
                    xsize 470
                    ysize 640
                    padding (14, 14)
                    vpgrid:
                        id "gloss_vp"
                        cols 1
                        spacing 2
                        scrollbars "vertical"
                        vscrollbar_unscrollable "hide"
                        mousewheel "change"
                        draggable True
                        yinitial (sel_idx / float(max(1, len(entries) - 1)))
                        for e in entries:
                            $ eid = e["id"]
                            if eid in persistent.gloss_found:
                                textbutton (e["term"] + ("  {color=#FFFF55}NEW{/color}" if eid not in persistent.gloss_read and eid != cur else "")):
                                    style "gloss_item"
                                    text_color e["cat_color"]
                                    selected cur == eid
                                    action Function(gloss_select, eid)
                            else:
                                textbutton e["masked"]:
                                    style "gloss_item"
                                    text_color "#555555"
                                    selected cur == eid
                                    action Function(gloss_select, eid)

                ## Entry detail
                frame:
                    background Frame("gui/frame.png", gui.frame_borders)
                    xsize 880
                    ysize 640
                    padding (36, 28)
                    if cur is None:
                        vbox:
                            spacing 16
                            text "Nothing discovered yet." color "#FFFFFF" size 30
                            text "Words in {color=#FFFF55}yellow{/color} in the story are glossary terms. Click one to look it up. Every term you meet is added here — and entries link to more entries." color "#AAAAAA" size 24
                    elif cur in persistent.gloss_found:
                        $ e = GLOSS[cur]
                        $ ccol = e["cat_color"]
                        viewport:
                            id "gloss_detail_vp"
                            scrollbars "vertical"
                            vscrollbar_unscrollable "hide"
                            mousewheel "change"
                            draggable True
                            vbox:
                                spacing 16
                                if persistent._gloss_fresh == cur:
                                    text "★ NEW DISCOVERY ★" color "#FFFF55" size 26
                                text e["term"] color ccol size 44 substitute False
                                text "%s  ·  %s" % (GLOSS_CAT_NAMES[e["cat"]].upper(), "found by following a link" if persistent.gloss_found[cur] == "link" else "found in the story") color "#AAAAAA" size 20
                                null height 4
                                text gloss_render_body(e["text"], persistent.gloss_found) color "#FFFFFF" size 28 substitute False
                                null height 8
                                text "{color=#FF55FF}†{/color} = not discovered yet. Follow it to unlock." color "#777777" size 18
                    else:
                        $ e = GLOSS[cur]
                        vbox:
                            spacing 16
                            text "† UNDISCOVERED †" color "#FF55FF" size 36
                            text gloss_masked(e["term"]) color "#555555" size 44 substitute False
                            text "Category: " + GLOSS_CAT_NAMES[e["cat"]] color "#AAAAAA" size 22
                            text "Keep playing to meet this term in the story — or find a {color=#FF55FF}† link{/color} to it inside another entry." color "#FFFFFF" size 26

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

style gloss_item is button
style gloss_item_text is button_text
style gloss_item:
    xfill True
    ysize 38
    padding (10, 4)
    selected_background "#0000AA"
    hover_background "#000060"
style gloss_item_text:
    size 24
    yalign 0.5
    hover_color "#FFFFFF"
    selected_color "#FFFFFF"
