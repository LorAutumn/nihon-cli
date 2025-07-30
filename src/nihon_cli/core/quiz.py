"""
Quiz logic for Japanese character learning.

This module contains the Quiz class that handles the quiz functionality
including character selection, user input validation, and feedback.
"""

import random
from nihon_cli.core.character import Character
from nihon_cli.data.hiragana import HIRAGANA_CHARACTERS
from nihon_cli.data.katakana import KATAKANA_CHARACTERS


class Quiz:
    """
    Handles quiz functionality for Japanese character learning.

    This class manages quiz sessions, including random character selection,
    user input validation, and providing feedback on answers.
    """

    def __init__(self, character_set: str):
        """
        Initialize a Quiz instance.

        Args:
            character_set (str): The character set to use ('hiragana', 'katakana', or 'mixed')
        """
        self.character_set_name = character_set
        self.characters = self._load_characters(character_set)
        self.correct_answers = 0
        self.incorrect_answers = 0

    def _load_characters(self, character_set: str) -> list[Character]:
        """Loads the specified character set."""
        if character_set == "hiragana":
            return HIRAGANA_CHARACTERS
        elif character_set == "katakana":
            return KATAKANA_CHARACTERS
        elif character_set == "mixed":
            return HIRAGANA_CHARACTERS + KATAKANA_CHARACTERS
        else:
            raise ValueError(
                "Invalid character set. Choose 'hiragana', 'katakana', or 'mixed'."
            )

    def _select_questions(self, count: int = 10) -> list[Character]:
        """Selects a random subset of characters for the quiz."""
        return random.sample(self.characters, min(count, len(self.characters)))

    def run_session(self):
        """
        Run a complete quiz session with 10 random characters.
        """
        print(f"Starte eine neue Quiz-Session für {self.character_set_name}...")
        self.correct_answers = 0
        self.incorrect_answers = 0

        questions = self._select_questions(10)

        for i, character in enumerate(questions, 1):
            print(f"\nFrage {i}/{len(questions)}")
            self.ask_question(character)

        print("\n--- Session-Zusammenfassung ---")
        print(self.get_session_results())

    def ask_question(self, character: Character) -> bool:
        """
        Asks a single question, validates the answer, and provides feedback.

        Args:
            character (Character): The character to ask the user about.

        Returns:
            bool: True if the answer was correct, False otherwise.
        """
        user_input = (
            input(f"Was ist das Romaji für '{character.symbol}'? ").strip().lower()
        )

        if user_input == character.romaji:
            print("Richtig!")
            self.correct_answers += 1
            return True
        else:
            print(f"Falsch! Die richtige Antwort ist: {character.romaji}")
            self.incorrect_answers += 1
            return False

    def get_session_results(self) -> str:
        """
        Returns a formatted string with the results of the current session.
        """
        total = self.correct_answers + self.incorrect_answers
        if total == 0:
            return "Keine Fragen beantwortet."

        accuracy = (self.correct_answers / total) * 100
        return (
            f"Ergebnisse: {self.correct_answers} Richtig, {self.incorrect_answers} Falsch\n"
            f"Genauigkeit: {accuracy:.2f}%"
        )
