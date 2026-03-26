"""Quiz engine for weekly vocabulary learning sessions.

This module provides the WeeklySessionQuiz class that manages interactive
vocabulary learning sessions with weekly progress tracking and adjective
opposite pairing.
"""

from typing import List

from nihon_cli.core.answer_checker import AnswerChecker, AnswerCheckResult
from nihon_cli.core.vocabulary import VocabularyItem
from nihon_cli.infra.repository import VocabRepository
from nihon_cli.infra.weekly_session_repository import WeeklySessionRepository
from nihon_cli.ui.formatting import draw_box, COLOR_GREEN, COLOR_RED, COLOR_RESET


class WeeklySessionQuiz:
    """Manages weekly vocabulary learning sessions.

    The quiz engine handles:
    - Loading items prioritized by weekly progress
    - Building quiz sequences with adjective-opposite pairing
    - Adaptive query direction (2x rule: JP→DE then DE→JP)
    - Base form display in feedback
    - Session statistics tracking
    """

    def __init__(
        self,
        vocab_repository: VocabRepository,
        session_repository: WeeklySessionRepository
    ):
        """Initialize the weekly quiz engine.

        Args:
            vocab_repository: VocabRepository instance for vocab operations
            session_repository: WeeklySessionRepository for session operations
        """
        self.vocab_repo = vocab_repository
        self.session_repo = session_repository
        self.answer_checker = AnswerChecker()
        self.session_stats = {
            'correct': 0,
            'incorrect': 0
        }
        self.questions_asked = 0

    def run_session(self, session_id: int) -> int:
        """Run a weekly quiz session (up to 10 items).

        Args:
            session_id: ID of the weekly session

        Returns:
            Number of questions asked in this session
        """
        # Load items prioritized by weekly progress
        items = self.session_repo.get_session_items(
            session_id,
            prioritize_by_progress=True
        )

        if not items:
            print("\n🎉 Keine Vokabeln zum Lernen verfügbar!")
            print("Alle Vokabeln sind abgeschlossen oder es wurden noch keine hinzugefügt.")
            return 0

        # Build quiz sequence with adjective-opposite pairing (max 10 items)
        quiz_sequence = self._build_quiz_sequence(items, max_items=10)

        if not quiz_sequence:
            print("\n✅ Alle Vokabeln dieser Woche wurden ausreichend geübt!")
            return 0

        # Reset statistics
        self.session_stats = {
            'correct': 0,
            'incorrect': 0
        }
        self.questions_asked = 0

        # Display session header
        session_info = (
            f"Typ: Wöchentliche Lernsitzung\n"
            f"Vokabeln: {len(quiz_sequence)}"
        )
        print("\n" + draw_box(session_info, title="📚 Weekly Session"))

        # Run the quiz loop
        self._run_quiz_loop(quiz_sequence)

        # Display summary
        self._display_summary()

        return self.questions_asked

    def _build_quiz_sequence(
        self,
        items: List[VocabularyItem],
        max_items: int = 10
    ) -> List[VocabularyItem]:
        """Build quiz sequence with adjective-opposite pairing.

        Algorithm:
        - Iterate through items
        - If adjective with opposite_id:
          - Add item to sequence
          - Load opposite and add immediately after (if room available and in session)
          - Mark opposite as "processed" to avoid duplicates
        - Else: Add item normally
        - Stop when max_items limit is reached

        Args:
            items: List of vocabulary items
            max_items: Maximum number of items in the quiz sequence

        Returns:
            List of items in quiz order with opposites paired (max max_items)
        """
        sequence = []
        processed_ids = set()

        # Create set of all IDs in this session for validation
        session_item_ids = {item.id for item in items}

        for item in items:
            # Stop if we've reached the limit
            if len(sequence) >= max_items:
                break

            if item.id in processed_ids:
                continue

            sequence.append(item)
            processed_ids.add(item.id)

            # Check for opposite adjective (only add if we still have room and it's in session)
            if item.vocab_type == 'adjective' and item.opposite_id and len(sequence) < max_items:
                # Only add opposite if it's part of this session
                if item.opposite_id in session_item_ids:
                    opposite = self.vocab_repo.get_adjective_opposite(item.id)
                    if opposite and opposite.id not in processed_ids:
                        sequence.append(opposite)
                        processed_ids.add(opposite.id)

        return sequence

    def _run_quiz_loop(self, items: List[VocabularyItem]) -> None:
        """Execute the main quiz loop for all vocabulary items.

        Uses weekly_direction property (2x rule) for direction determination.

        Args:
            items: List of vocabulary items to quiz
        """
        total = len(items)

        for index, item in enumerate(items, 1):
            # Use weekly direction (2x rule)
            direction = item.weekly_direction

            # Display question
            self._display_question(item, index, total, direction)

            # Get user input
            try:
                user_answer = input("\n> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️  Lernsitzung abgebrochen.")
                return

            # Increment questions asked counter
            self.questions_asked += 1

            # Check answer
            if direction == "jp_to_de":
                correct_answers = item.german_vocab
            else:  # de_to_jp
                correct_answers = item.japanese_vocab

            result = self.answer_checker.check(user_answer, correct_answers, direction)
            is_correct = result.accepted

            # Update weekly progress
            self.vocab_repo.update_weekly_progress(item.id, direction, is_correct)

            # Update local item for accurate feedback
            if is_correct:
                if direction == "jp_to_de":
                    item.weekly_correct_german += 1
                else:
                    item.weekly_correct_japanese += 1
                self.session_stats['correct'] += 1
            else:
                self.session_stats['incorrect'] += 1

            # Display feedback with base form
            self._display_feedback(result, user_answer, correct_answers, item)

            print()  # Empty line for spacing

    def _display_question(
        self,
        item: VocabularyItem,
        current: int,
        total: int,
        direction: str
    ) -> None:
        """Display a vocabulary question to the user.

        Args:
            item: The vocabulary item to quiz
            current: Current question number
            total: Total number of questions
            direction: Query direction ("jp_to_de" or "de_to_jp")
        """
        direction_symbol = "🇯🇵 → 🇩🇪" if direction == "jp_to_de" else "🇩🇪 → 🇯🇵"

        if direction == "jp_to_de":
            question_text = ", ".join(item.japanese_vocab)
            content = f"{direction_symbol}\n\nWas bedeutet '{question_text}'?"
        else:
            question_text = ", ".join(item.german_vocab)
            content = f"{direction_symbol}\n\nWie sagt man '{question_text}' auf Japanisch?"

        title = f"Frage {current}/{total}"
        print("\n" + draw_box(content, title=title))

    def _display_feedback(
        self,
        result: AnswerCheckResult,
        user_answer: str,
        correct_answers: List[str],
        item: VocabularyItem
    ) -> None:
        """Display feedback after an answer with base form if available.

        Args:
            result: The answer check result
            user_answer: The user's answer
            correct_answers: List of correct answers
            item: The vocabulary item
        """
        if result.accepted:
            if result.method == "semantic":
                feedback = f"{COLOR_GREEN}✅ Richtig! ({result.feedback}){COLOR_RESET}"
                feedback += f"\nErwartete Antwort: {', '.join(correct_answers)}"
            else:
                feedback = f"{COLOR_GREEN}✅ Richtig!{COLOR_RESET}"

            # Show base form if available
            if item.base_form:
                feedback += f"\nGrundform: {item.base_form}"

            # Show weekly progress (use 2+ instead of /5)
            feedback += f"\n\nWöchentlicher Fortschritt: DE {item.weekly_correct_german}/2+ | JP {item.weekly_correct_japanese}/2+"

            print(feedback)
        else:
            answers_str = ", ".join(correct_answers)
            user_line = f"Antwort: {user_answer}"
            correct_line = f"Lösung:  {answers_str}"

            # Add base form to solution if available
            if item.base_form:
                correct_line += f"\nGrundform: {item.base_form}"

            feedback_line = f"{COLOR_RED}❌ Falsch!{COLOR_RESET}"
            print(f"{user_line}\n{correct_line}\n{feedback_line}")

    def _display_summary(self) -> None:
        """Display a summary of the learning session."""
        total = self.session_stats['correct'] + self.session_stats['incorrect']

        if total == 0:
            return

        accuracy = (self.session_stats['correct'] / total * 100)

        summary_content = (
            f"Richtig:        {COLOR_GREEN}{self.session_stats['correct']}{COLOR_RESET}\n"
            f"Falsch:         {COLOR_RED}{self.session_stats['incorrect']}{COLOR_RESET}\n"
            f"Genauigkeit:    {accuracy:.1f}%"
        )

        print("\n" + draw_box(summary_content, title="📊 Sitzungs-Zusammenfassung"))
