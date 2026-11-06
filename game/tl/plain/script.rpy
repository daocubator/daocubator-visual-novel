# Plain mode — core script (intro, chapter close, forced rest)
# vault: 07 Production/Plain Mode Style Guide.md
# (The experience picker's own text is intentionally NOT translated: it's
#  shown before the player has chosen.)

# game/script.rpy:118
translate plain chapter_close_c90f9f98:

    # narrator "{color=#FF5555}Your token dips with the mood. A treasury that IS your token dips with it. (Treasury -15){/color}"
    narrator "{color=#FF5555}People feel worse about the project, so your token price drops. Your treasury is mostly that token, so your treasury drops too. (Treasury -15){/color}"

# game/script.rpy:126
translate plain forced_rest_896351b8:

    # narrator "You don't remember deciding to lie down."
    narrator "You don't remember deciding to lie down. Your body decided for you."

# game/script.rpy:127
translate plain forced_rest_70942272:

    # narrator "Your body files a governance proposal of its own. It passes unanimously."
    narrator "It's like your body made its own governance proposal: \"We rest now.\" Everyone voted yes."
    narrator "{color=#55FF55}TIP:{/color} Your Burnout is very high. Resting lowers it but costs a little money. Not resting saves time but makes you more tired and hurts team Morale."

# game/script.rpy:131
translate plain forced_rest_aff035fa:

    # narrator "The collective survives a week without you. That fact is either humbling or liberating. You choose liberating."
    narrator "The collective is fine for a whole week without you."
    narrator "That could make you feel less important. Or it could make you feel free. You choose free."

# game/script.rpy:134
translate plain forced_rest_322f6bd7:

    # narrator "You reopen the laptop. Somewhere, Vera sighs without knowing why."
    narrator "You open your laptop again and keep working. Somewhere, Vera sighs. She doesn't know why — but she would not be happy."

# game/script.rpy:158
translate plain start_809f9a27:

    # narrator "{color=#55FF55}TIP:{/color} {color=#FFFF55}{u}Yellow words{/u}{/color} are Glossary terms — click one to look it up. New terms unlock as you meet them, and entries link to more entries. Press G any time."
    narrator "{color=#55FF55}TIP:{/color} {color=#FFFF55}{u}Yellow words{/u}{/color} are special words. Click one to see what it means in the Glossary."
    narrator "{color=#55FF55}TIP:{/color} Each new word you meet is saved in your Glossary. Inside the Glossary, words link to other words — follow them to find more. Press G any time to open it."
    narrator "{color=#55FF55}TIP:{/color} At the top of the screen are your five stats: Vibes, Treasury, Security, Morale and Burnout. Click any of them to learn what it means."

# game/script.rpy:160
translate plain legacy_marathon_202e172d:

    # narrator "2025. The age of DAOs has truly begun — again — for the third or fourth time."
    narrator "The year is 2025. DAOs are popular again. A DAO is a group that runs itself with shared rules and shared money, instead of with a boss."
    narrator "This is not the first time DAOs have been popular. It's maybe the third or fourth time."

# game/script.rpy:161
translate plain legacy_marathon_62088c0d:

    # narrator "NounsDAO. MakerDAO. The Aragon crisis. Build Finance. Beanstalk. You watched them all rise, and you read every post-mortem on the way down."
    narrator "NounsDAO. MakerDAO. The Aragon crisis. Build Finance. Beanstalk. These are real DAOs. You watched them grow."
    narrator "Many of them failed. Each time, you read the post-mortem — the report about what went wrong."

# game/script.rpy:162
translate plain legacy_marathon_dda79876:

    # narrator "Roughly 65%% of ventures like the one you're about to start die from the inside. Not the market. The people. The structure. The deferred conversations."
    narrator "About 65 percent of projects like yours fail from the inside."
    narrator "The market is not what kills them. The people do. The way the group is set up. The hard talks that everyone kept putting off."

# game/script.rpy:163
translate plain legacy_marathon_242637e6:

    # narrator "You're going to be different. Everyone says that."
    narrator "You believe you will be different. Everyone believes that."

translate plain strings:

    # game/script.rpy:129
    old "Actually rest. Delegate for a week."
    new "Really rest. Let others do your work for a week."

    # game/script.rpy:132
    old "Rest is for people with runway."
    new "No. Resting is for people with lots of money saved."
