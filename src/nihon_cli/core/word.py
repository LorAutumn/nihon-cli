# src/nihon_cli/core/word.py
"""
Word domain model for Japanese vocabulary.

This module defines the Word class, which serves as a data structure
for representing Japanese vocabulary words with their essential properties
for language learning.
"""

from dataclasses import dataclass
from typing import Literal

# Common word categories for Japanese language learning
WordCategory = Literal[
    "family", "animals", "food", "colors", "numbers", "body_parts",
    "clothing", "weather", "time", "household", "verbs", "adjectives",
    "greetings", "school", "transportation", "nature", "emotions",
    "activities", "places", "objects"
]


@dataclass(frozen=True)
class Word:
    """
    Represents a Japanese vocabulary word with its properties.

    This class encapsulates the core attributes of a Japanese word,
    including the Japanese writing (Hiragana/Katakana only), its romanized
    representation (romaji), German translation, and category for learning
    organization. The class is immutable to ensure data integrity.

    Attributes:
        japanese (str): The Japanese word in Hiragana/Katakana (e.g., 'ねこ').
        romaji (str): The romanized representation (e.g., 'neko').
        german (str): The German translation (e.g., 'Katze').
        category (WordCategory): The learning category (e.g., 'animals').
    """

    japanese: str
    romaji: str
    german: str
    category: WordCategory

    def __post_init__(self) -> None:
        """
        Validates the word attributes after initialization.

        Raises:
            ValueError: If any required field is empty or if category is invalid.
        """
        if not self.japanese.strip():
            raise ValueError("Japanese word cannot be empty")
        if not self.romaji.strip():
            raise ValueError("Romaji cannot be empty")
        if not self.german.strip():
            raise ValueError("German translation cannot be empty")

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the word.

        Returns:
            str: A string in the format "japanese (romaji) - german".
        """
        return f"{self.japanese} ({self.romaji}) - {self.german}"

    def get_display_text(self) -> str:
        """
        Returns the Japanese text for display purposes.

        Returns:
            str: The Japanese word in Hiragana/Katakana.
        """
        return self.japanese

    def get_answer_text(self) -> str:
        """
        Returns the German translation for answer checking.

        Returns:
            str: The German translation.
        """
        return self.german

    def matches_category(self, category: WordCategory) -> bool:
        """
        Checks if the word belongs to a specific category.

        Args:
            category (WordCategory): The category to check against.

        Returns:
            bool: True if the word belongs to the specified category.
        """
        return self.category == category