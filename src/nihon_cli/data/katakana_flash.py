"""
Katakana flash card data with hiragana readings and example words.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class FlashCard:
    katakana: str
    hiragana: str
    example_word: str
    example_reading: str
    example_meaning: str


KATAKANA_FLASH_CARDS: list[FlashCard] = [
    FlashCard("ア", "あ", "アメリカ", "あめりか", "Amerika"),
    FlashCard("イ", "い", "イギリス", "いぎりす", "England"),
    FlashCard("ウ", "う", "ウイルス", "ういるす", "Virus"),
    FlashCard("エ", "え", "エレベーター", "えれべーたー", "Aufzug"),
    FlashCard("オ", "お", "オレンジ", "おれんじ", "Orange"),
    FlashCard("カ", "か", "カメラ", "かめら", "Kamera"),
    FlashCard("キ", "き", "キロ", "きろ", "Kilo"),
    FlashCard("ク", "く", "クラス", "くらす", "Klasse"),
    FlashCard("ケ", "け", "ケーキ", "けーき", "Kuchen"),
    FlashCard("コ", "こ", "コーヒー", "こーひー", "Kaffee"),
    FlashCard("サ", "さ", "サラダ", "さらだ", "Salat"),
    FlashCard("シ", "し", "シャツ", "しゃつ", "Hemd"),
    FlashCard("ス", "す", "スポーツ", "すぽーつ", "Sport"),
    FlashCard("セ", "せ", "セーター", "せーたー", "Pullover"),
    FlashCard("ソ", "そ", "ソファー", "そふぁー", "Sofa"),
    FlashCard("タ", "た", "タクシー", "たくしー", "Taxi"),
    FlashCard("チ", "ち", "チーズ", "ちーず", "Kaese"),
    FlashCard("ツ", "つ", "ツアー", "つあー", "Tour"),
    FlashCard("テ", "て", "テレビ", "てれび", "Fernseher"),
    FlashCard("ト", "と", "トイレ", "といれ", "Toilette"),
    FlashCard("ナ", "な", "ナイフ", "ないふ", "Messer"),
    FlashCard("ニ", "に", "ニュース", "にゅーす", "Nachrichten"),
    FlashCard("ヌ", "ぬ", "カヌー", "かぬー", "Kanu"),
    FlashCard("ネ", "ね", "ネクタイ", "ねくたい", "Krawatte"),
    FlashCard("ノ", "の", "ノート", "のーと", "Notizbuch"),
    FlashCard("ハ", "は", "ハンバーガー", "はんばーがー", "Hamburger"),
    FlashCard("ヒ", "ひ", "ヒーター", "ひーたー", "Heizung"),
    FlashCard("フ", "ふ", "フランス", "ふらんす", "Frankreich"),
    FlashCard("ヘ", "へ", "ヘリコプター", "へりこぷたー", "Hubschrauber"),
    FlashCard("ホ", "ほ", "ホテル", "ほてる", "Hotel"),
    FlashCard("マ", "ま", "マスク", "ますく", "Maske"),
    FlashCard("ミ", "み", "ミルク", "みるく", "Milch"),
    FlashCard("ム", "む", "ムード", "むーど", "Stimmung"),
    FlashCard("メ", "め", "メニュー", "めにゅー", "Speisekarte"),
    FlashCard("モ", "も", "モデル", "もでる", "Modell"),
    FlashCard("ヤ", "や", "ヤング", "やんぐ", "jung"),
    FlashCard("ユ", "ゆ", "ユニフォーム", "ゆにふぉーむ", "Uniform"),
    FlashCard("ヨ", "よ", "ヨーロッパ", "よーろっぱ", "Europa"),
    FlashCard("ラ", "ら", "ラーメン", "らーめん", "Ramen"),
    FlashCard("リ", "り", "リモコン", "りもこん", "Fernbedienung"),
    FlashCard("ル", "る", "ルール", "るーる", "Regel"),
    FlashCard("レ", "れ", "レストラン", "れすとらん", "Restaurant"),
    FlashCard("ロ", "ろ", "ロボット", "ろぼっと", "Roboter"),
    FlashCard("ワ", "わ", "ワイン", "わいん", "Wein"),
    FlashCard("ヲ", "を", "ヲタク", "をたく", "Otaku"),
    FlashCard("ン", "ん", "パン", "ぱん", "Brot"),
    FlashCard("ガ", "が", "ガラス", "がらす", "Glas"),
    FlashCard("ギ", "ぎ", "ギター", "ぎたー", "Gitarre"),
    FlashCard("グ", "ぐ", "グループ", "ぐるーぷ", "Gruppe"),
    FlashCard("ゲ", "げ", "ゲーム", "げーむ", "Spiel"),
    FlashCard("ゴ", "ご", "ゴルフ", "ごるふ", "Golf"),
    FlashCard("ザ", "ざ", "デザート", "でざーと", "Dessert"),
    FlashCard("ジ", "じ", "ジュース", "じゅーす", "Saft"),
    FlashCard("ズ", "ず", "チーズ", "ちーず", "Kaese"),
    FlashCard("ゼ", "ぜ", "ゼロ", "ぜろ", "Null"),
    FlashCard("ゾ", "ぞ", "ゾーン", "ぞーん", "Zone"),
    FlashCard("ダ", "だ", "ダンス", "だんす", "Tanz"),
    FlashCard("デ", "で", "デパート", "でぱーと", "Kaufhaus"),
    FlashCard("ド", "ど", "ドイツ", "どいつ", "Deutschland"),
    FlashCard("バ", "ば", "バス", "ばす", "Bus"),
    FlashCard("ビ", "び", "ビール", "びーる", "Bier"),
    FlashCard("ブ", "ぶ", "ブラジル", "ぶらじる", "Brasilien"),
    FlashCard("ベ", "べ", "ベッド", "べっど", "Bett"),
    FlashCard("ボ", "ぼ", "ボール", "ぼーる", "Ball"),
    FlashCard("パ", "ぱ", "パーティー", "ぱーてぃー", "Party"),
    FlashCard("ピ", "ぴ", "ピアノ", "ぴあの", "Klavier"),
    FlashCard("プ", "ぷ", "プール", "ぷーる", "Schwimmbad"),
    FlashCard("ペ", "ぺ", "ペン", "ぺん", "Stift"),
    FlashCard("ポ", "ぽ", "ポスト", "ぽすと", "Briefkasten"),
]
