"""Quiz engine for vocabulary learning sessions.

This module provides the VocabQuiz class that manages interactive
vocabulary learning sessions with adaptive query direction.
"""

import random
from typing import List, Optional

from nihon_cli.core.vocabulary import VocabularyItem
from nihon_cli.infra.repository import VocabRepository


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
        self.current_session: List[VocabularyItem] = []
        self.session_stats = {
            'correct': 0,
            'incorrect': 0,
            'completed_items': 0
        }
    
    def start_session(self, limit: int = 15) -> None:
        """Start a new learning session.
        
        Loads random incomplete vocabulary items from the database and
        begins an interactive quiz session.
        
        Args:
            limit: Maximum number of vocabulary items to include (default: 15)
        """
        # Load vocabulary items
        self.current_session = self.repository.get_incomplete_vocabulary(limit)
        
        if not self.current_session:
            print("\n🎉 Keine Vokabeln zum Lernen verfügbar!")
            print("Alle Vokabeln sind abgeschlossen oder es wurden noch keine hochgeladen.")
            return
        
        # Shuffle for variety
        random.shuffle(self.current_session)
        
        # Reset statistics
        self.session_stats = {
            'correct': 0,
            'incorrect': 0,
            'completed_items': 0
        }
        
        # Display session header
        print("\n" + "=" * 60)
        print(f"📚 Vokabel-Lernsitzung gestartet")
        print(f"   {len(self.current_session)} Vokabeln geladen")
        print("=" * 60)
        
        # Run the quiz loop
        self._run_quiz_loop()
        
        # Display summary
        self._display_summary()
    
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
            
            # Check answer
            if direction == "jp_to_de":
                correct_answers = item.german_vocab
            else:  # de_to_jp
                correct_answers = item.japanese_vocab
            
            is_correct = self._check_answer(user_answer, correct_answers)
            
            # Update progress
            self._update_progress(item, direction, is_correct)
            
            # Display feedback
            self._display_feedback(is_correct, user_answer, correct_answers, item)
            
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
        
        print(f"\n[{current}/{total}] {direction_symbol}")
        
        if direction == "jp_to_de":
            question_text = ", ".join(item.japanese_vocab)
            print(f"Was bedeutet '{question_text}'?")
        else:
            question_text = ", ".join(item.german_vocab)
            print(f"Wie sagt man '{question_text}' auf Japanisch?")
    
    def _check_answer(self, user_input: str, correct_answers: List[str]) -> bool:
        """Check if the user's answer is correct.
        
        The check is case-insensitive and accepts any of the possible
        correct answers (for vocabulary with multiple meanings).
        
        Args:
            user_input: The user's answer
            correct_answers: List of acceptable correct answers
            
        Returns:
            True if the answer is correct, False otherwise
        """
        user_input_normalized = user_input.strip().lower()
        
        return any(
            user_input_normalized == answer.strip().lower()
            for answer in correct_answers
        )
    
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
        is_correct: bool, 
        user_answer: str, 
        correct_answers: List[str],
        item: VocabularyItem
    ) -> None:
        """Display feedback after an answer.
        
        Args:
            is_correct: Whether the answer was correct
            user_answer: The user's answer
            correct_answers: List of correct answers
            item: The vocabulary item
        """
        if is_correct:
            print(f"✓ Richtig!")
            if item.completed:
                print(f"🎉 Vokabel abgeschlossen!")
            else:
                print(f"   Fortschritt: DE {item.correct_german}/5 | JP {item.correct_japanese}/5")
        else:
            print(f"✗ Falsch!")
            print(f"   Deine Antwort: {user_answer}")
            answers_str = ", ".join(correct_answers)
            print(f"   Korrekt wäre: {answers_str}")
    
    def _display_summary(self) -> None:
        """Display a summary of the learning session."""
        total = self.session_stats['correct'] + self.session_stats['incorrect']
        
        if total == 0:
            return
        
        accuracy = (self.session_stats['correct'] / total * 100)
        
        print("\n" + "=" * 60)
        print("📊 Sitzungs-Zusammenfassung")
        print("=" * 60)
        print(f"Richtig:              {self.session_stats['correct']}")
        print(f"Falsch:               {self.session_stats['incorrect']}")
        print(f"Genauigkeit:          {accuracy:.1f}%")
        print(f"Abgeschlossene:       {self.session_stats['completed_items']}")
        print("=" * 60)