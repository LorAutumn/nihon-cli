# src/nihon_cli/core/quiz.py
"""
Quiz logic for Japanese character learning.

This module contains the Quiz class, which orchestrates the quiz functionality,
including character selection, user input validation, and session feedback.
"""

import random
from typing import List

from nihon_cli.core.character import Character, CharacterType
from nihon_cli.data.hiragana import HIRAGANA_CHARACTERS
from nihon_cli.data.katakana import KATAKANA_CHARACTERS
from nihon_cli.ui.formatting import (
    draw_box,
    format_correct_answer,
    format_incorrect_answer,
    format_question,
    format_quiz_session,
)


class Quiz:
    """
    Handles quiz functionality for Japanese character learning.

    This class manages quiz sessions, including random character selection,
    user input validation, and providing feedback on answers.
    """

    def __init__(self, character_set: CharacterType) -> None:
        """
        Initializes a Quiz instance.

        Args:
            character_set (CharacterType): The character set to use, which can be
                                           'hiragana', 'katakana', or 'mixed'.
        """
        self.character_set_name: CharacterType = character_set
        self.characters: List[Character] = self._load_characters(character_set)
        self.correct_answers: int = 0
        self.incorrect_answers: int = 0

    def _load_characters(self, character_set: CharacterType) -> List[Character]:
        """
        Loads the specified character set.

        Args:
            character_set (CharacterType): The name of the character set to load.

        Returns:
            List[Character]: A list of Character objects.

        Raises:
            ValueError: If an invalid character set name is provided.
        """
        if character_set == "hiragana":
            return HIRAGANA_CHARACTERS
        elif character_set == "katakana":
            return KATAKANA_CHARACTERS
        elif character_set == "mixed":
            return HIRAGANA_CHARACTERS + KATAKANA_CHARACTERS
        else:
            # This case should ideally not be reached if inputs are validated upstream.
            raise ValueError(
                "Invalid character set. Choose 'hiragana', 'katakana', or 'mixed'."
            )

    def _select_questions(self, count: int = 10) -> List[Character]:
        """
        Selects a random subset of characters for the quiz.

        This method prevents errors by ensuring the number of requested
        questions does not exceed the number of available characters.

        Args:
            count (int): The desired number of questions. Defaults to 10.

        Returns:
            List[Character]: A list of characters to be used as questions.
        """
        return random.sample(self.characters, min(count, len(self.characters)))

    def run_session(self) -> None:
        """
        Runs a complete quiz session with a default of 10 random characters.
        """
        questions = self._select_questions(10)
        session_info = {
            "type": self.character_set_name,
            "questions": len(questions),
        }
        print(format_quiz_session(session_info))

        self.correct_answers = 0
        self.incorrect_answers = 0

        for i, character in enumerate(questions, 1):
            self.ask_question(character, i, len(questions))

        print("\n")
        print(draw_box(self.get_session_results(), title="Session-Zusammenfassung"))

    def ask_question(self, character: Character, question_number: int, total_questions: int) -> bool:
        """
        Asks a single question, validates the answer, and provides feedback.

        The user's input is sanitized by stripping whitespace and converting to
        lowercase to ensure a fair comparison.

        Args:
            character (Character): The character to ask the user about.
            question_number (int): The current question number.
            total_questions (int): The total number of questions in the quiz.

        Returns:
            bool: True if the answer was correct, False otherwise.
        """
        question_text = f"Was ist das Romaji für '{character.symbol}'?"
        print("\n" + format_question(question_text, question_number, total_questions))
        
        user_input = input("Antwort: ").strip().lower()

        if user_input == character.romaji:
            print(format_correct_answer())
            self.correct_answers += 1
            return True
        else:
            print(format_incorrect_answer(user_input, character.romaji))
            self.incorrect_answers += 1
            return False

    def get_session_results(self) -> str:
        """
        Returns a formatted string with the results of the current session.

        Calculates the accuracy and provides a summary of correct and
        incorrect answers.

        Returns:
            str: A summary of the session results.
        """
        total = self.correct_answers + self.incorrect_answers
        if total == 0:
            return "Keine Fragen beantwortet."

        accuracy = (self.correct_answers / total) * 100
        return (
            f"Ergebnisse: {self.correct_answers} Richtig, {self.incorrect_answers} Falsch\n"
            f"Genauigkeit: {accuracy:.2f}%"
        )
