"""
Character domain model for Japanese characters.

This module defines the Character class that represents individual
Japanese characters (Hiragana and Katakana) with their properties.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Character:
    """
    Represents a Japanese character with its properties.

    This class encapsulates the core attributes of a Japanese character
    including the symbol, romanization, and character type.
    It is immutable to ensure data integrity.

    Attributes:
        symbol (str): The Japanese character symbol.
        romaji (str): The romanized representation.
        character_type (str): Either 'hiragana' or 'katakana'.
    """
    symbol: str
    romaji: str
    character_type: str

    def __post_init__(self):
        """Validate the character_type after initialization."""
        if self.character_type not in ['hiragana', 'katakana']:
            raise ValueError("character_type must be 'hiragana' or 'katakana'")

    def __str__(self) -> str:
        """Return a user-friendly string representation of the character."""
        return f"{self.symbol} ({self.romaji})"

    def is_hiragana(self) -> bool:
        """Check if the character is a Hiragana character."""
        return self.character_type == 'hiragana'

    def is_katakana(self) -> bool:
        """Check if the character is a Katakana character."""
        return self.character_type == 'katakana'