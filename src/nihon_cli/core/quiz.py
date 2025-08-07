# src/nihon_cli/core/quiz.py
"""
Quiz logic for Japanese character learning.

This module contains the Quiz class, which orchestrates the quiz functionality,
including character selection, user input validation, and session feedback.
"""

import random
from typing import List, Union

from nihon_cli.core.character import Character, CharacterType
from nihon_cli.core.word import Word
from nihon_cli.data.hiragana_basic import HIRAGANA_BASIC_CHARACTERS
from nihon_cli.data.hiragana_advanced import HIRAGANA_ADVANCED_CHARACTERS
from nihon_cli.data.katakana_basic import KATAKANA_BASIC_CHARACTERS
from nihon_cli.data.katakana_advanced import KATAKANA_ADVANCED_CHARACTERS
from nihon_cli.data.words import get_words
from nihon_cli.ui.formatting import (
    draw_box,
    format_correct_answer,
    format_incorrect_answer,
    format_question,
    format_quiz_session,
    format_word_correct_answer,
    format_word_incorrect_answer,
)


class Quiz:
    """
    Handles quiz functionality for Japanese character learning.

    This class manages quiz sessions, including random character selection,
    user input validation, and providing feedback on answers.
    """

    def __init__(self, character_set: str, include_advanced: bool = False) -> None:
        """
        Initializes a Quiz instance.

        Args:
            character_set (str): The character set to use, which can be
                                'hiragana', 'katakana', 'mixed', or 'words'.
            include_advanced (bool): If True, includes advanced characters (combination characters/Yōon).
                                    For 'words', this parameter is ignored as all words are always included.
        """
        self.character_set_name: str = character_set
        self.include_advanced: bool = include_advanced
        self.items: List[Union[Character, Word]] = self._load_items(character_set, include_advanced)
        self.correct_answers: int = 0
        self.incorrect_answers: int = 0

    def _load_items(self, character_set: str, include_advanced: bool = False) -> List[Union[Character, Word]]:
        """
        Loads the specified character set or word set.

        Args:
            character_set (str): The name of the character set to load.
            include_advanced (bool): If True, includes advanced characters (combination characters/Yōon).
                                    For 'words', this parameter is ignored as all words are always included.

        Returns:
            List[Union[Character, Word]]: A list of Character or Word objects.

        Raises:
            ValueError: If an invalid character set name is provided.
        """
        if character_set == "hiragana":
            if include_advanced:
                return HIRAGANA_BASIC_CHARACTERS + HIRAGANA_ADVANCED_CHARACTERS
            else:
                return HIRAGANA_BASIC_CHARACTERS
        elif character_set == "katakana":
            if include_advanced:
                return KATAKANA_BASIC_CHARACTERS + KATAKANA_ADVANCED_CHARACTERS
            else:
                return KATAKANA_BASIC_CHARACTERS
        elif character_set == "mixed":
            if include_advanced:
                return (HIRAGANA_BASIC_CHARACTERS + HIRAGANA_ADVANCED_CHARACTERS +
                        KATAKANA_BASIC_CHARACTERS + KATAKANA_ADVANCED_CHARACTERS)
            else:
                return HIRAGANA_BASIC_CHARACTERS + KATAKANA_BASIC_CHARACTERS
        elif character_set == "words":
            return self._load_words()
        else:
            # This case should ideally not be reached if inputs are validated upstream.
            raise ValueError(
                "Invalid character set. Choose 'hiragana', 'katakana', 'mixed', or 'words'."
            )

    def _load_words(self) -> List[Word]:
        """
        Loads all Japanese vocabulary words (basic + advanced combined).

        Returns:
            List[Word]: A list of all Word objects.
        """
        return get_words(include_advanced=True)  # Always load all words

    def _select_questions(self, count: int = 10) -> List[Union[Character, Word]]:
        """
        Selects a random subset of characters or words for the quiz.

        This method prevents errors by ensuring the number of requested
        questions does not exceed the number of available items.

        Args:
            count (int): The desired number of questions. Defaults to 10.

        Returns:
            List[Union[Character, Word]]: A list of characters or words to be used as questions.
        """
        return random.sample(self.items, min(count, len(self.items)))

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

        for i, item in enumerate(questions, 1):
            self.ask_question(item, i, len(questions))

        print("\n")
        print(draw_box(self.get_session_results(), title="Session-Zusammenfassung"))

    def ask_question(self, item: Union[Character, Word], question_number: int, total_questions: int) -> bool:
        """
        Asks a single question, validates the answer, and provides feedback.

        The user's input is sanitized by stripping whitespace and converting to
        lowercase to ensure a fair comparison.

        Args:
            item (Union[Character, Word]): The character or word to ask the user about.
            question_number (int): The current question number.
            total_questions (int): The total number of questions in the quiz.

        Returns:
            bool: True if the answer was correct, False otherwise.
        """
        if isinstance(item, Character):
            question_text = f"Was ist das Romaji für '{item.symbol}'?"
            print("\n" + format_question(question_text, question_number, total_questions))
            
            user_input = input("> ").strip().lower()

            if user_input == item.romaji:
                print(format_correct_answer())
                self.correct_answers += 1
                return True
            else:
                print(format_incorrect_answer(user_input, item.romaji, character=item))
                self.incorrect_answers += 1
                return False
        elif isinstance(item, Word):
            question_text = f"Was ist das Romaji für '{item.japanese}'?"
            print("\n" + format_question(question_text, question_number, total_questions))
            
            user_input = input("> ").strip().lower()

            if user_input == item.romaji.lower():
                print(format_word_correct_answer(item))
                self.correct_answers += 1
                return True
            else:
                print(format_word_incorrect_answer(user_input, item))
                self.incorrect_answers += 1
                return False
        else:
            raise ValueError(f"Unsupported item type: {type(item)}")

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
