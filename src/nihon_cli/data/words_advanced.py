"""
Advanced Japanese vocabulary database.

This module provides a list of 50 advanced Japanese words
for intermediate beginners, featuring longer words, more complex concepts,
and specialized categories. Uses only Hiragana and Katakana characters.
"""

from nihon_cli.core.word import Word

# Schule (10 Wörter)
SCHOOL_WORDS = [
    Word(japanese="がっこう", romaji="gakkou", german="Schule", category="school"),
    Word(japanese="せんせい", romaji="sensei", german="Lehrer", category="school"),
    Word(japanese="がくせい", romaji="gakusei", german="Schüler/Student", category="school"),
    Word(japanese="きょうしつ", romaji="kyoushitsu", german="Klassenzimmer", category="school"),
    Word(japanese="しゅくだい", romaji="shukudai", german="Hausaufgaben", category="school"),
    Word(japanese="べんきょう", romaji="benkyou", german="Lernen", category="school"),
    Word(japanese="しけん", romaji="shiken", german="Prüfung", category="school"),
    Word(japanese="えんぴつ", romaji="enpitsu", german="Bleistift", category="school"),
    Word(japanese="ノート", romaji="nooto", german="Notizbuch", category="school"),
    Word(japanese="じしょ", romaji="jisho", german="Wörterbuch", category="school"),
]

# Verkehrsmittel (10 Wörter)
TRANSPORTATION_WORDS = [
    Word(japanese="でんしゃ", romaji="densha", german="Zug", category="transportation"),
    Word(japanese="バス", romaji="basu", german="Bus", category="transportation"),
    Word(japanese="タクシー", romaji="takushii", german="Taxi", category="transportation"),
    Word(japanese="じてんしゃ", romaji="jitensha", german="Fahrrad", category="transportation"),
    Word(japanese="くるま", romaji="kuruma", german="Auto", category="transportation"),
    Word(japanese="ひこうき", romaji="hikouki", german="Flugzeug", category="transportation"),
    Word(japanese="ふね", romaji="fune", german="Schiff", category="transportation"),
    Word(japanese="ちかてつ", romaji="chikatetsu", german="U-Bahn", category="transportation"),
    Word(japanese="えき", romaji="eki", german="Bahnhof", category="transportation"),
    Word(japanese="くうこう", romaji="kuukou", german="Flughafen", category="transportation"),
]

# Natur (10 Wörter)
NATURE_WORDS = [
    Word(japanese="しぜん", romaji="shizen", german="Natur", category="nature"),
    Word(japanese="やま", romaji="yama", german="Berg", category="nature"),
    Word(japanese="うみ", romaji="umi", german="Meer", category="nature"),
    Word(japanese="かわ", romaji="kawa", german="Fluss", category="nature"),
    Word(japanese="もり", romaji="mori", german="Wald", category="nature"),
    Word(japanese="はな", romaji="hana", german="Blume", category="nature"),
    Word(japanese="き", romaji="ki", german="Baum", category="nature"),
    Word(japanese="そら", romaji="sora", german="Himmel", category="nature"),
    Word(japanese="ほし", romaji="hoshi", german="Stern", category="nature"),
    Word(japanese="たいよう", romaji="taiyou", german="Sonne", category="nature"),
]

# Gefühle (10 Wörter)
EMOTION_WORDS = [
    Word(japanese="きもち", romaji="kimochi", german="Gefühl", category="emotions"),
    Word(japanese="うれしい", romaji="ureshii", german="glücklich", category="emotions"),
    Word(japanese="かなしい", romaji="kanashii", german="traurig", category="emotions"),
    Word(japanese="おこる", romaji="okoru", german="wütend werden", category="emotions"),
    Word(japanese="こわい", romaji="kowai", german="ängstlich", category="emotions"),
    Word(japanese="たのしい", romaji="tanoshii", german="lustig/unterhaltsam", category="emotions"),
    Word(japanese="つまらない", romaji="tsumaranai", german="langweilig", category="emotions"),
    Word(japanese="びっくり", romaji="bikkuri", german="überrascht", category="emotions"),
    Word(japanese="しんぱい", romaji="shinpai", german="Sorge", category="emotions"),
    Word(japanese="あんしん", romaji="anshin", german="Erleichterung", category="emotions"),
]

# Aktivitäten (10 Wörter)
ACTIVITY_WORDS = [
    Word(japanese="スポーツ", romaji="supootsu", german="Sport", category="activities"),
    Word(japanese="おんがく", romaji="ongaku", german="Musik", category="activities"),
    Word(japanese="えいが", romaji="eiga", german="Film", category="activities"),
    Word(japanese="りょこう", romaji="ryokou", german="Reise", category="activities"),
    Word(japanese="かいもの", romaji="kaimono", german="Einkaufen", category="activities"),
    Word(japanese="りょうり", romaji="ryouri", german="Kochen", category="activities"),
    Word(japanese="そうじ", romaji="souji", german="Putzen", category="activities"),
    Word(japanese="せんたく", romaji="sentaku", german="Wäsche waschen", category="activities"),
    Word(japanese="ゲーム", romaji="geemu", german="Spiel", category="activities"),
    Word(japanese="パーティー", romaji="paatii", german="Party", category="activities"),
]

# Alle erweiterten Wörter kombinieren (50 Wörter)
WORDS_ADVANCED = (
    SCHOOL_WORDS +
    TRANSPORTATION_WORDS +
    NATURE_WORDS +
    EMOTION_WORDS +
    ACTIVITY_WORDS
)