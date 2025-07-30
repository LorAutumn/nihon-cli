# src/nihon_cli/core/character.py
"""
Character domain model for Japanese characters.

This module defines the Character class, which serves as a data structure
for representing individual Japanese characters (Hiragana and Katakana)
along with their essential properties.
"""

from dataclasses import dataclass
from typing import Literal

CharacterType = Literal["hiragana", "katakana"]


@dataclass(frozen=True)
class Character:
    """
    Represents a Japanese character with its properties.

    This class encapsulates the core attributes of a Japanese character,
    including the symbol, its romanized representation (romaji), and the
    character type. The class is immutable to ensure data integrity.

    Attributes:
        symbol (str): The Japanese character symbol (e.g., 'あ').
        romaji (str): The romanized representation (e.g., 'a').
        character_type (CharacterType): The type of character, either
                                        'hiragana' or 'katakana'.
    """

    symbol: str
    romaji: str
    character_type: CharacterType

    def __post_init__(self) -> None:
        """
        Validates the character_type after initialization.

        Raises:
            ValueError: If character_type is not 'hiragana' or 'katakana'.
        """
        if self.character_type not in ("hiragana", "katakana"):
            raise ValueError("character_type must be 'hiragana' or 'katakana'")

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the character.

        Returns:
            str: A string in the format "symbol (romaji)".
        """
        return f"{self.symbol} ({self.romaji})"

    def is_hiragana(self) -> bool:
        """
        Checks if the character is a Hiragana character.

        Returns:
            bool: True if the character is Hiragana, False otherwise.
        """
        return self.character_type == "hiragana"

    def is_katakana(self) -> bool:
        """
        Checks if the character is a Katakana character.

        Returns:
            bool: True if the character is Katakana, False otherwise.
        """
        return self.character_type == "katakana"
