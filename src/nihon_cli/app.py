# src/nihon_cli/app.py
"""
Central application class for the Nihon CLI.

This module provides the NihonCli class, which orchestrates the core
components of the application, such as the quiz, timer, and configuration
management. It serves as the main entry point for running training sessions.
"""

import logging
import os
import sys
from typing import Optional

from nihon_cli.core.quiz import Quiz
from nihon_cli.core.timer import LearningTimer

__version__ = "0.1.0"


class NihonCli:
    """
    The main application class for Nihon CLI.

    This class integrates and manages the training session, including setting up
    the quiz and timer, handling the session loop, and managing application state.
    """

    def __init__(self) -> None:
        """
        Initializes the NihonCli application.
        """
        self.quiz: Optional[Quiz] = None
        self.timer: Optional[LearningTimer] = None
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        logging.info("NihonCli application initialized.")

    def get_version(self) -> str:
        """
        Returns the current version of the application.

        Returns:
            str: The application version string.
        """
        return f"Nihon CLI Version {__version__}"

    def run_training_session(self, character_set: str, test_mode: bool = False, advanced_mode: bool = False) -> None:
        """
        Runs a full training session for the specified character set.

        This is the main method to start a training loop. It sets up the
        necessary components and handles the session flow.

        Args:
            character_set (str): The character set for the quiz ('hiragana', 'katakana', 'mixed', 'words').
            test_mode (bool): If True, runs in a short test mode (5s timer).
            advanced_mode (bool): If True, includes advanced characters (combination characters/Yōon).
                                 Note: For 'words', this parameter is ignored as all words are always included.
        """
        try:
            self._setup_components(character_set, test_mode, advanced_mode)
            self._handle_session_loop()
        except ValueError as e:
            logging.error(f"Configuration error: {e}")
            print(f"Fehler: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\nTraining manually stopped. Goodbye!")
            logging.info("Training session stopped by user.")
            sys.exit(0)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}", exc_info=True)
            print(
                "\nEin unerwarteter Fehler ist aufgetreten. "
                "Weitere Details finden Sie in den Log-Dateien.",
                file=sys.stderr,
            )
            sys.exit(1)

    def _setup_components(self, character_set: str, test_mode: bool, advanced_mode: bool = False) -> None:
        """
        Initializes and configures the core components (Quiz and Timer).

        Args:
            character_set (str): The character set for the quiz.
            test_mode (bool): Flag for test mode.
            advanced_mode (bool): Flag for advanced mode (includes combination characters).
        """
        logging.info(
            f"Setting up components for character set '{character_set}' with test_mode={test_mode}, advanced_mode={advanced_mode}."
        )
        self.quiz = Quiz(character_set, include_advanced=advanced_mode)

        interval = 5 if test_mode else 1500  # 5 seconds for test, 25 minutes for normal
        self.timer = LearningTimer(interval)

    def _clear_terminal(self) -> None:
        """
        Clears the terminal screen.

        This method uses ANSI escape codes for POSIX systems and the 'cls'
        command for Windows, avoiding the use of 'clear' to prevent potential
        command injection risks.
        """
        if os.name == "nt":
            os.system("cls")
        else:
            # Use ANSI escape codes to clear the screen and move the cursor
            # to the top-left, which is safer than calling 'clear'.
            print("\033[H\033[J", end="")

    def _handle_session_loop(self) -> None:
        """
        Manages the continuous loop of quiz sessions and breaks.
        """
        if not self.quiz or not self.timer:
            raise RuntimeError("Components not set up. Call _setup_components first.")

        mode_name = {
            "hiragana": "Hiragana",
            "katakana": "Katakana",
            "mixed": "Hiragana & Katakana",
            "words": "Japanese Vocabulary",
        }.get(self.quiz.character_set_name, "Unknown")

        print(f"Welcome to the {mode_name} training!")
        print("Press Ctrl+C to end the training at any time.")

        while True:
            self._clear_terminal()
            self.quiz.run_session()
            print("\nNext session will begin shortly...")
            self.timer.wait_for_next_session()
