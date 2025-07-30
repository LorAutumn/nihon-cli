"""
Katakana character data for the Nihon CLI application.

This module contains the complete set of Katakana characters
with their romanized representations.
"""

from ..core.character import Character


# Katakana character dataset
# Implementation will be added in Phase 2
KATAKANA_CHARACTERS = [
    # Basic characters will be defined here in Phase 2
    # Example structure:
    # Character(symbol="ア", romaji="a", character_type="katakana"),
    # Character(symbol="カ", romaji="ka", character_type="katakana"),
    # ... more characters
]


def get_katakana_characters():
    """
    Get the complete list of Katakana characters.
    
    Returns:
        list: List of Character objects representing Katakana characters
    """
    return KATAKANA_CHARACTERS