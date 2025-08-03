"""
Hiragana character database.

This module provides a complete list of Hiragana characters,
including their Romaji transcriptions, based on the Character domain model.
This file maintains backward compatibility by combining basic and advanced characters.
"""

from nihon_cli.core.character import Character
from nihon_cli.data.hiragana_basic import HIRAGANA_BASIC_CHARACTERS
from nihon_cli.data.hiragana_advanced import HIRAGANA_ADVANCED_CHARACTERS

# Combine basic and advanced characters for backward compatibility
HIRAGANA_CHARACTERS: list[Character] = HIRAGANA_BASIC_CHARACTERS + HIRAGANA_ADVANCED_CHARACTERS
