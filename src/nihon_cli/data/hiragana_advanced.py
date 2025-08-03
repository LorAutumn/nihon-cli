"""
Advanced Hiragana character database.

This module provides the advanced Hiragana characters including
combination characters (Yōon).
"""

from nihon_cli.core.character import Character

HIRAGANA_ADVANCED_CHARACTERS: list[Character] = [
    # Combinations (Yōon)
    Character(symbol="きゃ", romaji="kya", character_type="hiragana"),
    Character(symbol="きゅ", romaji="kyu", character_type="hiragana"),
    Character(symbol="きょ", romaji="kyo", character_type="hiragana"),
    Character(symbol="しゃ", romaji="sha", character_type="hiragana"),
    Character(symbol="しゅ", romaji="shu", character_type="hiragana"),
    Character(symbol="しょ", romaji="sho", character_type="hiragana"),
    Character(symbol="ちゃ", romaji="cha", character_type="hiragana"),
    Character(symbol="ちゅ", romaji="chu", character_type="hiragana"),
    Character(symbol="ちょ", romaji="cho", character_type="hiragana"),
    Character(symbol="にゃ", romaji="nya", character_type="hiragana"),
    Character(symbol="にゅ", romaji="nyu", character_type="hiragana"),
    Character(symbol="にょ", romaji="nyo", character_type="hiragana"),
    Character(symbol="ひゃ", romaji="hya", character_type="hiragana"),
    Character(symbol="ひゅ", romaji="hyu", character_type="hiragana"),
    Character(symbol="ひょ", romaji="hyo", character_type="hiragana"),
    Character(symbol="みゃ", romaji="mya", character_type="hiragana"),
    Character(symbol="みゅ", romaji="myu", character_type="hiragana"),
    Character(symbol="みょ", romaji="myo", character_type="hiragana"),
    Character(symbol="りゃ", romaji="rya", character_type="hiragana"),
    Character(symbol="りゅ", romaji="ryu", character_type="hiragana"),
    Character(symbol="りょ", romaji="ryo", character_type="hiragana"),
    Character(symbol="ぎゃ", romaji="gya", character_type="hiragana"),
    Character(symbol="ぎゅ", romaji="gyu", character_type="hiragana"),
    Character(symbol="ぎょ", romaji="gyo", character_type="hiragana"),
    Character(symbol="じゃ", romaji="ja", character_type="hiragana"),
    Character(symbol="じゅ", romaji="ju", character_type="hiragana"),
    Character(symbol="じょ", romaji="jo", character_type="hiragana"),
    Character(symbol="びゃ", romaji="bya", character_type="hiragana"),
    Character(symbol="びゅ", romaji="byu", character_type="hiragana"),
    Character(symbol="びょ", romaji="byo", character_type="hiragana"),
    Character(symbol="ぴゃ", romaji="pya", character_type="hiragana"),
    Character(symbol="ぴゅ", romaji="pyu", character_type="hiragana"),
    Character(symbol="ぴょ", romaji="pyo", character_type="hiragana"),
]