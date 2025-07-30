"""
Katakana character database.

This module provides a complete list of Katakana characters,
including their Romaji transcriptions, based on the Character domain model.
"""

from src.nihon_cli.core.character import Character

KATAKANA_CHARACTERS: list[Character] = [
    # Basic Katakana (Gojūon)
    Character(symbol='ア', romaji='a', character_type='katakana'),
    Character(symbol='イ', romaji='i', character_type='katakana'),
    Character(symbol='ウ', romaji='u', character_type='katakana'),
    Character(symbol='エ', romaji='e', character_type='katakana'),
    Character(symbol='オ', romaji='o', character_type='katakana'),

    Character(symbol='カ', romaji='ka', character_type='katakana'),
    Character(symbol='キ', romaji='ki', character_type='katakana'),
    Character(symbol='ク', romaji='ku', character_type='katakana'),
    Character(symbol='ケ', romaji='ke', character_type='katakana'),
    Character(symbol='コ', romaji='ko', character_type='katakana'),

    Character(symbol='サ', romaji='sa', character_type='katakana'),
    Character(symbol='シ', romaji='shi', character_type='katakana'),
    Character(symbol='ス', romaji='su', character_type='katakana'),
    Character(symbol='セ', romaji='se', character_type='katakana'),
    Character(symbol='ソ', romaji='so', character_type='katakana'),

    Character(symbol='タ', romaji='ta', character_type='katakana'),
    Character(symbol='チ', romaji='chi', character_type='katakana'),
    Character(symbol='ツ', romaji='tsu', character_type='katakana'),
    Character(symbol='テ', romaji='te', character_type='katakana'),
    Character(symbol='ト', romaji='to', character_type='katakana'),

    Character(symbol='ナ', romaji='na', character_type='katakana'),
    Character(symbol='ニ', romaji='ni', character_type='katakana'),
    Character(symbol='ヌ', romaji='nu', character_type='katakana'),
    Character(symbol='ネ', romaji='ne', character_type='katakana'),
    Character(symbol='ノ', romaji='no', character_type='katakana'),

    Character(symbol='ハ', romaji='ha', character_type='katakana'),
    Character(symbol='ヒ', romaji='hi', character_type='katakana'),
    Character(symbol='フ', romaji='fu', character_type='katakana'),
    Character(symbol='ヘ', romaji='he', character_type='katakana'),
    Character(symbol='ホ', romaji='ho', character_type='katakana'),

    Character(symbol='マ', romaji='ma', character_type='katakana'),
    Character(symbol='ミ', romaji='mi', character_type='katakana'),
    Character(symbol='ム', romaji='mu', character_type='katakana'),
    Character(symbol='メ', romaji='me', character_type='katakana'),
    Character(symbol='モ', romaji='mo', character_type='katakana'),

    Character(symbol='ヤ', romaji='ya', character_type='katakana'),
    Character(symbol='ユ', romaji='yu', character_type='katakana'),
    Character(symbol='ヨ', romaji='yo', character_type='katakana'),

    Character(symbol='ラ', romaji='ra', character_type='katakana'),
    Character(symbol='リ', romaji='ri', character_type='katakana'),
    Character(symbol='ル', romaji='ru', character_type='katakana'),
    Character(symbol='レ', romaji='re', character_type='katakana'),
    Character(symbol='ロ', romaji='ro', character_type='katakana'),

    Character(symbol='ワ', romaji='wa', character_type='katakana'),
    Character(symbol='ヲ', romaji='wo', character_type='katakana'),

    # Special Characters
    Character(symbol='ン', romaji='n', character_type='katakana'),
    Character(symbol='ッ', romaji='tsu', character_type='katakana'), # Small tsu

    # Dakuten and Handakuten
    Character(symbol='ガ', romaji='ga', character_type='katakana'),
    Character(symbol='ギ', romaji='gi', character_type='katakana'),
    Character(symbol='グ', romaji='gu', character_type='katakana'),
    Character(symbol='ゲ', romaji='ge', character_type='katakana'),
    Character(symbol='ゴ', romaji='go', character_type='katakana'),

    Character(symbol='ザ', romaji='za', character_type='katakana'),
    Character(symbol='ジ', romaji='ji', character_type='katakana'),
    Character(symbol='ズ', romaji='zu', character_type='katakana'),
    Character(symbol='ゼ', romaji='ze', character_type='katakana'),
    Character(symbol='ゾ', romaji='zo', character_type='katakana'),

    Character(symbol='ダ', romaji='da', character_type='katakana'),
    Character(symbol='ヂ', romaji='ji', character_type='katakana'),
    Character(symbol='ヅ', romaji='zu', character_type='katakana'),
    Character(symbol='デ', romaji='de', character_type='katakana'),
    Character(symbol='ド', romaji='do', character_type='katakana'),

    Character(symbol='バ', romaji='ba', character_type='katakana'),
    Character(symbol='ビ', romaji='bi', character_type='katakana'),
    Character(symbol='ブ', romaji='bu', character_type='katakana'),
    Character(symbol='ベ', romaji='be', character_type='katakana'),
    Character(symbol='ボ', romaji='bo', character_type='katakana'),

    Character(symbol='パ', romaji='pa', character_type='katakana'),
    Character(symbol='ピ', romaji='pi', character_type='katakana'),
    Character(symbol='プ', romaji='pu', character_type='katakana'),
    Character(symbol='ペ', romaji='pe', character_type='katakana'),
    Character(symbol='ポ', romaji='po', character_type='katakana'),

    # Combinations (Yōon)
    Character(symbol='キャ', romaji='kya', character_type='katakana'),
    Character(symbol='キュ', romaji='kyu', character_type='katakana'),
    Character(symbol='キョ', romaji='kyo', character_type='katakana'),

    Character(symbol='シャ', romaji='sha', character_type='katakana'),
    Character(symbol='シュ', romaji='shu', character_type='katakana'),
    Character(symbol='ショ', romaji='sho', character_type='katakana'),

    Character(symbol='チャ', romaji='cha', character_type='katakana'),
    Character(symbol='チュ', romaji='chu', character_type='katakana'),
    Character(symbol='チョ', romaji='cho', character_type='katakana'),

    Character(symbol='ニャ', romaji='nya', character_type='katakana'),
    Character(symbol='ニュ', romaji='nyu', character_type='katakana'),
    Character(symbol='ニョ', romaji='nyo', character_type='katakana'),

    Character(symbol='ヒャ', romaji='hya', character_type='katakana'),
    Character(symbol='ヒュ', romaji='hyu', character_type='katakana'),
    Character(symbol='ヒョ', romaji='hyo', character_type='katakana'),

    Character(symbol='ミャ', romaji='mya', character_type='katakana'),
    Character(symbol='ミュ', romaji='myu', character_type='katakana'),
    Character(symbol='ミョ', romaji='myo', character_type='katakana'),

    Character(symbol='リャ', romaji='rya', character_type='katakana'),
    Character(symbol='リュ', romaji='ryu', character_type='katakana'),
    Character(symbol='リョ', romaji='ryo', character_type='katakana'),

    Character(symbol='ギャ', romaji='gya', character_type='katakana'),
    Character(symbol='ギュ', romaji='gyu', character_type='katakana'),
    Character(symbol='ギョ', romaji='gyo', character_type='katakana'),

    Character(symbol='ジャ', romaji='ja', character_type='katakana'),
    Character(symbol='ジュ', romaji='ju', character_type='katakana'),
    Character(symbol='ジョ', romaji='jo', character_type='katakana'),

    Character(symbol='ビャ', romaji='bya', character_type='katakana'),
    Character(symbol='ビュ', romaji='byu', character_type='katakana'),
    Character(symbol='ビョ', romaji='byo', character_type='katakana'),

    Character(symbol='ピャ', romaji='pya', character_type='katakana'),
    Character(symbol='ピュ', romaji='pyu', character_type='katakana'),
    Character(symbol='ピョ', romaji='pyo', character_type='katakana'),
]