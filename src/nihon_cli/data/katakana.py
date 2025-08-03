"""
Katakana character database.

This module provides a complete list of Katakana characters,
including their Romaji transcriptions, based on the Character domain model.
This file maintains backward compatibility by combining basic and advanced characters.
"""

from nihon_cli.core.character import Character
from nihon_cli.data.katakana_basic import KATAKANA_BASIC_CHARACTERS
from nihon_cli.data.katakana_advanced import KATAKANA_ADVANCED_CHARACTERS

# Combine basic and advanced characters for backward compatibility
KATAKANA_CHARACTERS: list[Character] = KATAKANA_BASIC_CHARACTERS + KATAKANA_ADVANCED_CHARACTERS
