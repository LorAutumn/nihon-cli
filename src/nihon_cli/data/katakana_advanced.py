"""
Advanced Katakana character database.

This module provides the advanced Katakana characters including
combination characters (Yōon).
"""

from nihon_cli.core.character import Character

KATAKANA_ADVANCED_CHARACTERS: list[Character] = [
    # Combinations (Yōon)
    Character(symbol="キャ", romaji="kya", character_type="katakana"),
    Character(symbol="キュ", romaji="kyu", character_type="katakana"),
    Character(symbol="キョ", romaji="kyo", character_type="katakana"),
    Character(symbol="シャ", romaji="sha", character_type="katakana"),
    Character(symbol="シュ", romaji="shu", character_type="katakana"),
    Character(symbol="ショ", romaji="sho", character_type="katakana"),
    Character(symbol="チャ", romaji="cha", character_type="katakana"),
    Character(symbol="チュ", romaji="chu", character_type="katakana"),
    Character(symbol="チョ", romaji="cho", character_type="katakana"),
    Character(symbol="ニャ", romaji="nya", character_type="katakana"),
    Character(symbol="ニュ", romaji="nyu", character_type="katakana"),
    Character(symbol="ニョ", romaji="nyo", character_type="katakana"),
    Character(symbol="ヒャ", romaji="hya", character_type="katakana"),
    Character(symbol="ヒュ", romaji="hyu", character_type="katakana"),
    Character(symbol="ヒョ", romaji="hyo", character_type="katakana"),
    Character(symbol="ミャ", romaji="mya", character_type="katakana"),
    Character(symbol="ミュ", romaji="myu", character_type="katakana"),
    Character(symbol="ミョ", romaji="myo", character_type="katakana"),
    Character(symbol="リャ", romaji="rya", character_type="katakana"),
    Character(symbol="リュ", romaji="ryu", character_type="katakana"),
    Character(symbol="リョ", romaji="ryo", character_type="katakana"),
    Character(symbol="ギャ", romaji="gya", character_type="katakana"),
    Character(symbol="ギュ", romaji="gyu", character_type="katakana"),
    Character(symbol="ギョ", romaji="gyo", character_type="katakana"),
    Character(symbol="ジャ", romaji="ja", character_type="katakana"),
    Character(symbol="ジュ", romaji="ju", character_type="katakana"),
    Character(symbol="ジョ", romaji="jo", character_type="katakana"),
    Character(symbol="ビャ", romaji="bya", character_type="katakana"),
    Character(symbol="ビュ", romaji="byu", character_type="katakana"),
    Character(symbol="ビョ", romaji="byo", character_type="katakana"),
    Character(symbol="ピャ", romaji="pya", character_type="katakana"),
    Character(symbol="ピュ", romaji="pyu", character_type="katakana"),
    Character(symbol="ピョ", romaji="pyo", character_type="katakana"),
]