"""
Character domain model for Japanese characters.

This module defines the Character class that represents individual
Japanese characters (Hiragana and Katakana) with their properties.
"""


class Character:
    """
    Represents a Japanese character with its properties.
    
    This class encapsulates the core attributes of a Japanese character
    including the symbol, romanization, and character type.
    """
    
    def __init__(self, symbol: str, romaji: str, character_type: str):
        """
        Initialize a Character instance.
        
        Args:
            symbol (str): The Japanese character symbol
            romaji (str): The romanized representation
            character_type (str): Either 'hiragana' or 'katakana'
        """
        self.symbol = symbol
        self.romaji = romaji
        self.character_type = character_type
    
    def __str__(self) -> str:
        """Return string representation of the character."""
        return f"{self.symbol} ({self.romaji})"
    
    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return f"Character(symbol='{self.symbol}', romaji='{self.romaji}', character_type='{self.character_type}')"