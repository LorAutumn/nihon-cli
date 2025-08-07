"""
Basic Japanese vocabulary database.

This module provides a comprehensive list of 150 basic Japanese words
suitable for beginners, organized by categories and using only
Hiragana and Katakana characters (no Kanji).
"""

from nihon_cli.core.word import Word

# Familie (10 Wörter)
FAMILY_WORDS = [
    Word(japanese="おかあさん", romaji="okaasan", german="Mutter", category="family"),
    Word(japanese="おとうさん", romaji="otousan", german="Vater", category="family"),
    Word(japanese="あに", romaji="ani", german="älterer Bruder", category="family"),
    Word(japanese="あね", romaji="ane", german="ältere Schwester", category="family"),
    Word(japanese="おとうと", romaji="otouto", german="jüngerer Bruder", category="family"),
    Word(japanese="いもうと", romaji="imouto", german="jüngere Schwester", category="family"),
    Word(japanese="おじいさん", romaji="ojiisan", german="Großvater", category="family"),
    Word(japanese="おばあさん", romaji="obaasan", german="Großmutter", category="family"),
    Word(japanese="こども", romaji="kodomo", german="Kind", category="family"),
    Word(japanese="かぞく", romaji="kazoku", german="Familie", category="family"),
]

# Tiere (15 Wörter)
ANIMAL_WORDS = [
    Word(japanese="ねこ", romaji="neko", german="Katze", category="animals"),
    Word(japanese="いぬ", romaji="inu", german="Hund", category="animals"),
    Word(japanese="とり", romaji="tori", german="Vogel", category="animals"),
    Word(japanese="さかな", romaji="sakana", german="Fisch", category="animals"),
    Word(japanese="うま", romaji="uma", german="Pferd", category="animals"),
    Word(japanese="ぶた", romaji="buta", german="Schwein", category="animals"),
    Word(japanese="うし", romaji="ushi", german="Kuh", category="animals"),
    Word(japanese="ひつじ", romaji="hitsuji", german="Schaf", category="animals"),
    Word(japanese="うさぎ", romaji="usagi", german="Hase", category="animals"),
    Word(japanese="ねずみ", romaji="nezumi", german="Maus", category="animals"),
    Word(japanese="ぞう", romaji="zou", german="Elefant", category="animals"),
    Word(japanese="らいおん", romaji="raion", german="Löwe", category="animals"),
    Word(japanese="くま", romaji="kuma", german="Bär", category="animals"),
    Word(japanese="きつね", romaji="kitsune", german="Fuchs", category="animals"),
    Word(japanese="かめ", romaji="kame", german="Schildkröte", category="animals"),
]

# Essen (20 Wörter)
FOOD_WORDS = [
    Word(japanese="ごはん", romaji="gohan", german="Reis/Essen", category="food"),
    Word(japanese="パン", romaji="pan", german="Brot", category="food"),
    Word(japanese="みず", romaji="mizu", german="Wasser", category="food"),
    Word(japanese="おちゃ", romaji="ocha", german="Tee", category="food"),
    Word(japanese="コーヒー", romaji="koohii", german="Kaffee", category="food"),
    Word(japanese="ぎゅうにゅう", romaji="gyuunyuu", german="Milch", category="food"),
    Word(japanese="たまご", romaji="tamago", german="Ei", category="food"),
    Word(japanese="にく", romaji="niku", german="Fleisch", category="food"),
    Word(japanese="やさい", romaji="yasai", german="Gemüse", category="food"),
    Word(japanese="くだもの", romaji="kudamono", german="Obst", category="food"),
    Word(japanese="りんご", romaji="ringo", german="Apfel", category="food"),
    Word(japanese="バナナ", romaji="banana", german="Banane", category="food"),
    Word(japanese="みかん", romaji="mikan", german="Mandarine", category="food"),
    Word(japanese="いちご", romaji="ichigo", german="Erdbeere", category="food"),
    Word(japanese="ケーキ", romaji="keeki", german="Kuchen", category="food"),
    Word(japanese="アイス", romaji="aisu", german="Eis", category="food"),
    Word(japanese="チョコレート", romaji="chokoreeto", german="Schokolade", category="food"),
    Word(japanese="さとう", romaji="satou", german="Zucker", category="food"),
    Word(japanese="しお", romaji="shio", german="Salz", category="food"),
    Word(japanese="スープ", romaji="suupu", german="Suppe", category="food"),
]

# Farben (10 Wörter)
COLOR_WORDS = [
    Word(japanese="あか", romaji="aka", german="rot", category="colors"),
    Word(japanese="あお", romaji="ao", german="blau", category="colors"),
    Word(japanese="きいろ", romaji="kiiro", german="gelb", category="colors"),
    Word(japanese="みどり", romaji="midori", german="grün", category="colors"),
    Word(japanese="しろ", romaji="shiro", german="weiß", category="colors"),
    Word(japanese="くろ", romaji="kuro", german="schwarz", category="colors"),
    Word(japanese="ちゃいろ", romaji="chairo", german="braun", category="colors"),
    Word(japanese="むらさき", romaji="murasaki", german="lila", category="colors"),
    Word(japanese="ピンク", romaji="pinku", german="rosa", category="colors"),
    Word(japanese="オレンジ", romaji="orenji", german="orange", category="colors"),
]

# Zahlen 1-10 (10 Wörter)
NUMBER_WORDS = [
    Word(japanese="いち", romaji="ichi", german="eins", category="numbers"),
    Word(japanese="に", romaji="ni", german="zwei", category="numbers"),
    Word(japanese="さん", romaji="san", german="drei", category="numbers"),
    Word(japanese="よん", romaji="yon", german="vier", category="numbers"),
    Word(japanese="ご", romaji="go", german="fünf", category="numbers"),
    Word(japanese="ろく", romaji="roku", german="sechs", category="numbers"),
    Word(japanese="なな", romaji="nana", german="sieben", category="numbers"),
    Word(japanese="はち", romaji="hachi", german="acht", category="numbers"),
    Word(japanese="きゅう", romaji="kyuu", german="neun", category="numbers"),
    Word(japanese="じゅう", romaji="juu", german="zehn", category="numbers"),
]

# Körperteile (10 Wörter)
BODY_PARTS_WORDS = [
    Word(japanese="あたま", romaji="atama", german="Kopf", category="body_parts"),
    Word(japanese="かお", romaji="kao", german="Gesicht", category="body_parts"),
    Word(japanese="め", romaji="me", german="Auge", category="body_parts"),
    Word(japanese="はな", romaji="hana", german="Nase", category="body_parts"),
    Word(japanese="くち", romaji="kuchi", german="Mund", category="body_parts"),
    Word(japanese="みみ", romaji="mimi", german="Ohr", category="body_parts"),
    Word(japanese="て", romaji="te", german="Hand", category="body_parts"),
    Word(japanese="あし", romaji="ashi", german="Fuß/Bein", category="body_parts"),
    Word(japanese="からだ", romaji="karada", german="Körper", category="body_parts"),
    Word(japanese="こころ", romaji="kokoro", german="Herz", category="body_parts"),
]

# Kleidung (10 Wörter)
CLOTHING_WORDS = [
    Word(japanese="ふく", romaji="fuku", german="Kleidung", category="clothing"),
    Word(japanese="シャツ", romaji="shatsu", german="Hemd", category="clothing"),
    Word(japanese="ズボン", romaji="zubon", german="Hose", category="clothing"),
    Word(japanese="スカート", romaji="sukaato", german="Rock", category="clothing"),
    Word(japanese="くつ", romaji="kutsu", german="Schuhe", category="clothing"),
    Word(japanese="くつした", romaji="kutsushita", german="Socken", category="clothing"),
    Word(japanese="ぼうし", romaji="boushi", german="Hut", category="clothing"),
    Word(japanese="めがね", romaji="megane", german="Brille", category="clothing"),
    Word(japanese="とけい", romaji="tokei", german="Uhr", category="clothing"),
    Word(japanese="かばん", romaji="kaban", german="Tasche", category="clothing"),
]

# Wetter (10 Wörter)
WEATHER_WORDS = [
    Word(japanese="てんき", romaji="tenki", german="Wetter", category="weather"),
    Word(japanese="はれ", romaji="hare", german="sonnig", category="weather"),
    Word(japanese="くもり", romaji="kumori", german="bewölkt", category="weather"),
    Word(japanese="あめ", romaji="ame", german="Regen", category="weather"),
    Word(japanese="ゆき", romaji="yuki", german="Schnee", category="weather"),
    Word(japanese="かぜ", romaji="kaze", german="Wind", category="weather"),
    Word(japanese="あつい", romaji="atsui", german="heiß", category="weather"),
    Word(japanese="さむい", romaji="samui", german="kalt", category="weather"),
    Word(japanese="あたたかい", romaji="atatakai", german="warm", category="weather"),
    Word(japanese="すずしい", romaji="suzushii", german="kühl", category="weather"),
]

# Zeit (15 Wörter)
TIME_WORDS = [
    Word(japanese="じかん", romaji="jikan", german="Zeit", category="time"),
    Word(japanese="あさ", romaji="asa", german="Morgen", category="time"),
    Word(japanese="ひる", romaji="hiru", german="Mittag", category="time"),
    Word(japanese="ばん", romaji="ban", german="Abend", category="time"),
    Word(japanese="よる", romaji="yoru", german="Nacht", category="time"),
    Word(japanese="きょう", romaji="kyou", german="heute", category="time"),
    Word(japanese="あした", romaji="ashita", german="morgen", category="time"),
    Word(japanese="きのう", romaji="kinou", german="gestern", category="time"),
    Word(japanese="いま", romaji="ima", german="jetzt", category="time"),
    Word(japanese="まえ", romaji="mae", german="vorher", category="time"),
    Word(japanese="あと", romaji="ato", german="nachher", category="time"),
    Word(japanese="はやい", romaji="hayai", german="früh/schnell", category="time"),
    Word(japanese="おそい", romaji="osoi", german="spät/langsam", category="time"),
    Word(japanese="ようび", romaji="youbi", german="Wochentag", category="time"),
    Word(japanese="つき", romaji="tsuki", german="Monat/Mond", category="time"),
]

# Haushalt (15 Wörter)
HOUSEHOLD_WORDS = [
    Word(japanese="いえ", romaji="ie", german="Haus", category="household"),
    Word(japanese="へや", romaji="heya", german="Zimmer", category="household"),
    Word(japanese="だいどころ", romaji="daidokoro", german="Küche", category="household"),
    Word(japanese="おふろ", romaji="ofuro", german="Bad", category="household"),
    Word(japanese="トイレ", romaji="toire", german="Toilette", category="household"),
    Word(japanese="ベッド", romaji="beddo", german="Bett", category="household"),
    Word(japanese="つくえ", romaji="tsukue", german="Tisch", category="household"),
    Word(japanese="いす", romaji="isu", german="Stuhl", category="household"),
    Word(japanese="でんき", romaji="denki", german="Licht/Strom", category="household"),
    Word(japanese="テレビ", romaji="terebi", german="Fernseher", category="household"),
    Word(japanese="でんわ", romaji="denwa", german="Telefon", category="household"),
    Word(japanese="ほん", romaji="hon", german="Buch", category="household"),
    Word(japanese="かみ", romaji="kami", german="Papier", category="household"),
    Word(japanese="ペン", romaji="pen", german="Stift", category="household"),
    Word(japanese="まど", romaji="mado", german="Fenster", category="household"),
]

# Verben (15 Wörter)
VERB_WORDS = [
    Word(japanese="たべる", romaji="taberu", german="essen", category="verbs"),
    Word(japanese="のむ", romaji="nomu", german="trinken", category="verbs"),
    Word(japanese="みる", romaji="miru", german="sehen", category="verbs"),
    Word(japanese="きく", romaji="kiku", german="hören", category="verbs"),
    Word(japanese="はなす", romaji="hanasu", german="sprechen", category="verbs"),
    Word(japanese="よむ", romaji="yomu", german="lesen", category="verbs"),
    Word(japanese="かく", romaji="kaku", german="schreiben", category="verbs"),
    Word(japanese="あるく", romaji="aruku", german="gehen", category="verbs"),
    Word(japanese="はしる", romaji="hashiru", german="laufen", category="verbs"),
    Word(japanese="ねる", romaji="neru", german="schlafen", category="verbs"),
    Word(japanese="おきる", romaji="okiru", german="aufwachen", category="verbs"),
    Word(japanese="くる", romaji="kuru", german="kommen", category="verbs"),
    Word(japanese="いく", romaji="iku", german="gehen", category="verbs"),
    Word(japanese="かう", romaji="kau", german="kaufen", category="verbs"),
    Word(japanese="つくる", romaji="tsukuru", german="machen", category="verbs"),
]

# Adjektive (10 Wörter)
ADJECTIVE_WORDS = [
    Word(japanese="おおきい", romaji="ookii", german="groß", category="adjectives"),
    Word(japanese="ちいさい", romaji="chiisai", german="klein", category="adjectives"),
    Word(japanese="たかい", romaji="takai", german="hoch/teuer", category="adjectives"),
    Word(japanese="やすい", romaji="yasui", german="billig", category="adjectives"),
    Word(japanese="あたらしい", romaji="atarashii", german="neu", category="adjectives"),
    Word(japanese="ふるい", romaji="furui", german="alt", category="adjectives"),
    Word(japanese="いい", romaji="ii", german="gut", category="adjectives"),
    Word(japanese="わるい", romaji="warui", german="schlecht", category="adjectives"),
    Word(japanese="きれい", romaji="kirei", german="schön", category="adjectives"),
    Word(japanese="げんき", romaji="genki", german="gesund/munter", category="adjectives"),
]

# Grüße (10 Wörter)
GREETING_WORDS = [
    Word(japanese="おはよう", romaji="ohayou", german="Guten Morgen", category="greetings"),
    Word(japanese="こんにちは", romaji="konnichiwa", german="Guten Tag", category="greetings"),
    Word(japanese="こんばんは", romaji="konbanwa", german="Guten Abend", category="greetings"),
    Word(japanese="さようなら", romaji="sayounara", german="Auf Wiedersehen", category="greetings"),
    Word(japanese="ありがとう", romaji="arigatou", german="Danke", category="greetings"),
    Word(japanese="すみません", romaji="sumimasen", german="Entschuldigung", category="greetings"),
    Word(japanese="はじめまして", romaji="hajimemashite", german="Freut mich", category="greetings"),
    Word(japanese="おなまえは", romaji="onamae wa", german="Wie heißen Sie?", category="greetings"),
    Word(japanese="はい", romaji="hai", german="ja", category="greetings"),
    Word(japanese="いいえ", romaji="iie", german="nein", category="greetings"),
]

# Alle Grundwörter kombinieren (150 Wörter)
WORDS_BASIC = (
    FAMILY_WORDS +
    ANIMAL_WORDS +
    FOOD_WORDS +
    COLOR_WORDS +
    NUMBER_WORDS +
    BODY_PARTS_WORDS +
    CLOTHING_WORDS +
    WEATHER_WORDS +
    TIME_WORDS +
    HOUSEHOLD_WORDS +
    VERB_WORDS +
    ADJECTIVE_WORDS +
    GREETING_WORDS
)