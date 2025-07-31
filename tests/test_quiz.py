# tests/test_quiz.py
"""
Unit tests for the Quiz module.

This file contains tests for the Quiz class, ensuring that character loading,
question handling, and feedback mechanisms work as expected.
"""

import unittest
from unittest.mock import patch, call

from nihon_cli.core.character import Character
from nihon_cli.core.quiz import Quiz
from nihon_cli.data.hiragana import HIRAGANA_CHARACTERS
from nihon_cli.data.katakana import KATAKANA_CHARACTERS


class TestQuiz(unittest.TestCase):
    """Tests for the Quiz class."""

    def setUp(self) -> None:
        """Set up a Quiz instance for testing."""
        self.quiz = Quiz(character_set="hiragana")

    def test_load_characters_hiragana(self) -> None:
        """Test if hiragana characters are loaded correctly."""
        quiz = Quiz(character_set="hiragana")
        self.assertEqual(quiz.characters, HIRAGANA_CHARACTERS)

    def test_load_characters_katakana(self) -> None:
        """Test if katakana characters are loaded correctly."""
        quiz = Quiz(character_set="katakana")
        self.assertEqual(quiz.characters, KATAKANA_CHARACTERS)

    def test_load_characters_mixed(self) -> None:
        """Test if mixed characters are loaded correctly."""
        quiz = Quiz(character_set="mixed")
        expected_chars = HIRAGANA_CHARACTERS + KATAKANA_CHARACTERS
        self.assertEqual(quiz.characters, expected_chars)

    def test_load_characters_invalid(self) -> None:
        """Test if an invalid character set raises a ValueError."""
        with self.assertRaises(ValueError):
            Quiz(character_set="invalid_set") # type: ignore

    @patch("builtins.input", return_value="a")
    @patch("builtins.print")
    def test_ask_question_correct(self, mock_print: unittest.mock.MagicMock, _: unittest.mock.MagicMock) -> None:
        """Test feedback for a correct answer."""
        char = Character(symbol="あ", romaji="a", character_type="hiragana")
        result = self.quiz.ask_question(char)
        self.assertTrue(result)
        self.assertEqual(self.quiz.correct_answers, 1)
        mock_print.assert_called_with("✅ Richtig!")

    @patch("builtins.input", return_value="wrong")
    @patch("builtins.print")
    def test_ask_question_incorrect(self, mock_print: unittest.mock.MagicMock, _: unittest.mock.MagicMock) -> None:
        """Test feedback for an incorrect answer."""
        char = Character(symbol="あ", romaji="a", character_type="hiragana")
        result = self.quiz.ask_question(char)
        self.assertFalse(result)
        self.assertEqual(self.quiz.incorrect_answers, 1)
        mock_print.assert_called_with("❌ Falsch! Die richtige Antwort ist: a")

    def test_get_session_results_no_answers(self) -> None:
        """Test session results when no questions have been answered."""
        result = self.quiz.get_session_results()
        self.assertEqual(result, "Keine Fragen beantwortet.")

    def test_get_session_results_mixed(self) -> None:
        """Test session results with mixed correct and incorrect answers."""
        self.quiz.correct_answers = 7
        self.quiz.incorrect_answers = 3
        result = self.quiz.get_session_results()
        self.assertIn("Ergebnisse: 7 Richtig, 3 Falsch", result)
        self.assertIn("Genauigkeit: 70.00%", result)

    def test_get_session_results_perfect_score(self) -> None:
        """Test session results for a perfect score, checking for the celebration emoji."""
        self.quiz.correct_answers = 10
        self.quiz.incorrect_answers = 0
        result = self.quiz.get_session_results()
        self.assertIn("Ergebnisse: 10 Richtig, 0 Falsch", result)
        self.assertIn("Genauigkeit: 100.00%", result)
        self.assertIn("🎉 Perfekte Punktzahl! Großartige Arbeit!", result)


if __name__ == "__main__":
    unittest.main()