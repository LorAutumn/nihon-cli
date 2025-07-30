"""
Hiragana character data for the Nihon CLI application.

This module contains the complete set of Hiragana characters
with their romanized representations.
"""

from ..core.character import Character


# Hiragana character dataset
# Implementation will be added in Phase 2
HIRAGANA_CHARACTERS = [
    # Basic characters will be defined here in Phase 2
    # Example structure:
    # Character(symbol="あ", romaji="a", character_type="hiragana"),
    # Character(symbol="か", romaji="ka", character_type="hiragana"),
    # ... more characters
]


def get_hiragana_characters():
    """
    Get the complete list of Hiragana characters.
    
    Returns:
        list: List of Character objects representing Hiragana characters
    """
    return HIRAGANA_CHARACTERS