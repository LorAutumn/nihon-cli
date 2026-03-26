"""Quiz engine for vocabulary learning sessions.

This module provides the VocabQuiz class that manages interactive
vocabulary learning sessions with adaptive query direction.
"""

import random
from typing import List, Optional

from nihon_cli.core.answer_checker import AnswerChecker, AnswerCheckResult
from nihon_cli.core.vocabulary import VocabularyItem
from nihon_cli.infra.repository import VocabRepository
from nihon_cli.ui.formatting import draw_box, COLOR_GREEN, COLOR_RED, COLOR_RESET


class VocabQuiz:
    """Manages vocabulary learning sessions with adaptive query direction.
    
    The quiz engine handles the complete learning session flow:
    - Loading random incomplete vocabulary items
    - Determining query direction based on progress
    - Validating user answers
    - Updating progress in the database
    - Providing session statistics
    """
    
    def __init__(self, repository: VocabRepository):
        """Initialize the quiz engine.
        
        Args:
            repository: VocabRepository instance for database operations
        """
        self.repository = repository
        self.answer_checker = AnswerChecker()
        self.current_session: List[VocabularyItem] = []
        self.session_stats = {
            'correct': 0,
            'incorrect': 0,
            'completed_items': 0
        }
        self.questions_asked = 0
    
    def run_session(self, limit: int = 15) -> int:
        """Run a single learning session.
        
        Loads random incomplete vocabulary items from the database and
        begins an interactive quiz session.
        
        Args:
            limit: Maximum number of vocabulary items to include (default: 15)
            
        Returns:
            int: Number of questions asked in this session
        """
        # Load vocabulary items
        self.current_session = self.repository.get_incomplete_vocabulary(limit)
        
        if not self.current_session:
            print("\n🎉 Keine Vokabeln zum Lernen verfügbar!")
            print("Alle Vokabeln sind abgeschlossen oder es wurden noch keine hochgeladen.")
            return 0
        
        # Shuffle for variety
        random.shuffle(self.current_session)
        
        # Reset statistics
        self.session_stats = {
            'correct': 0,
            'incorrect': 0,
            'completed_items': 0
        }
        self.questions_asked = 0
        
        # Display session header
        session_info = (
            f"Typ: Vokabeltraining\n"
            f"Vokabeln: {len(self.current_session)}"
        )
        print("\n" + draw_box(session_info, title="📚 Vokabel-Lernsitzung"))
        
        # Run the quiz loop
        self._run_quiz_loop()
        
        # Display summary
        self._display_summary()
        
        return self.questions_asked
    
    def start_session(self, limit: int = 15) -> None:
        """Start a new learning session (legacy method for compatibility).
        
        Loads random incomplete vocabulary items from the database and
        begins an interactive quiz session.
        
        Args:
            limit: Maximum number of vocabulary items to include (default: 15)
        """
        self.run_session(limit)
    
    def _run_quiz_loop(self) -> None:
        """Execute the main quiz loop for all vocabulary items."""
        total = len(self.current_session)
        
        for index, item in enumerate(self.current_session, 1):
            # Determine query direction
            direction = item.current_direction
            
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

            # Update progress
            self._update_progress(item, direction, is_correct)

            # Display feedback
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
    
    def _update_progress(
        self, 
        item: VocabularyItem, 
        direction: str, 
        correct: bool
    ) -> None:
        """Update the learning progress in the database.
        
        Args:
            item: The vocabulary item that was quizzed
            direction: The query direction used
            correct: Whether the answer was correct
        """
        if correct:
            # Update progress counter
            self.repository.update_progress(item.id, direction, True)
            self.session_stats['correct'] += 1
            
            # Update local item for accurate feedback
            if direction == "jp_to_de":
                item.correct_german += 1
            else:
                item.correct_japanese += 1
            
            # Check if item is now completed
            if item.is_ready_for_completion:
                self.repository.mark_completed(item.id)
                self.session_stats['completed_items'] += 1
                item.completed = True
        else:
            self.session_stats['incorrect'] += 1
    
    def _display_feedback(
        self,
        result: AnswerCheckResult,
        user_answer: str,
        correct_answers: List[str],
        item: VocabularyItem
    ) -> None:
        """Display feedback after an answer.

        Args:
            result: The answer check result
            user_answer: The user's answer
            correct_answers: List of correct answers
            item: The vocabulary item
        """
        if result.accepted:
            if result.method in ("semantic", "typo"):
                feedback = f"{COLOR_GREEN}✅ Richtig! ({result.feedback}){COLOR_RESET}"
            else:
                feedback = f"{COLOR_GREEN}✅ Richtig!{COLOR_RESET}"
            if item.completed:
                feedback += f"\n{COLOR_GREEN}🎉 Vokabel abgeschlossen!{COLOR_RESET}"
            else:
                feedback += f"\n\nFortschritt: DE {item.correct_german}/5 | JP {item.correct_japanese}/5"
            print(feedback)
        else:
            answers_str = ", ".join(correct_answers)
            user_line = f"Antwort: {user_answer}"
            correct_line = f"Lösung:  {answers_str}"
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
            f"Genauigkeit:    {accuracy:.1f}%\n"
            f"Abgeschlossen:  {COLOR_GREEN}{self.session_stats['completed_items']}{COLOR_RESET} 🎉"
        )
        
        print("\n" + draw_box(summary_content, title="📊 Sitzungs-Zusammenfassung"))