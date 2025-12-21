"""Domain model for vocabulary items.

This module defines the VocabularyItem class that represents a single
vocabulary entry with all its metadata and learning progress.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class VocabularyItem:
    """Represents a single vocabulary item with all metadata.
    
    Attributes:
        id: Unique identifier for the vocabulary item
        japanese_vocab: List of Japanese vocabulary words/phrases
        german_vocab: List of German translations
        source_file: Name of the source file from which this was imported
        upload_tag: User-defined tag for organizing vocabulary
        correct_german: Counter for correct answers in Japanese→German direction (0-5)
        correct_japanese: Counter for correct answers in German→Japanese direction (0-5)
        completed: Whether this vocabulary item has been fully learned
        created_at: Timestamp when the item was created
        updated_at: Timestamp when the item was last updated
    """
    
    id: int
    japanese_vocab: List[str]
    german_vocab: List[str]
    source_file: Optional[str]
    upload_tag: Optional[str]
    correct_german: int = 0
    correct_japanese: int = 0
    completed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # New fields for weekly sessions
    vocab_type: Optional[str] = None  # 'noun', 'adjective', 'pattern'
    opposite_id: Optional[int] = None  # Link to opposite adjective
    base_form: Optional[str] = None  # Base form for conjugated words
    weekly_correct_german: int = 0  # Weekly counter for JP→DE
    weekly_correct_japanese: int = 0  # Weekly counter for DE→JP
    
    @property
    def current_direction(self) -> str:
        """Determine the current query direction based on progress.
        
        The learning algorithm first focuses on Japanese→German until
        the user has answered correctly 5 times, then switches to
        German→Japanese direction.
        
        Returns:
            str: Either "jp_to_de" or "de_to_jp"
        """
        if self.correct_german < 5:
            return "jp_to_de"
        return "de_to_jp"
    
    @property
    def is_ready_for_completion(self) -> bool:
        """Check if the vocabulary item can be marked as completed.
        
        A vocabulary item is ready for completion when the user has
        answered correctly 5 times in both directions.
        
        Returns:
            bool: True if both counters are >= 5, False otherwise
        """
        return self.correct_german >= 5 and self.correct_japanese >= 5
    
    @property
    def progress_percentage(self) -> float:
        """Calculate the overall learning progress as a percentage.

        Returns:
            float: Progress percentage (0.0 to 100.0)
        """
        total_required = 10  # 5 correct in each direction
        total_achieved = self.correct_german + self.correct_japanese
        return min(100.0, (total_achieved / total_required) * 100)

    @property
    def weekly_direction(self) -> str:
        """Determine the current query direction based on weekly progress.

        The weekly learning algorithm first focuses on Japanese→German until
        the user has answered correctly 2 times, then switches to
        German→Japanese direction.

        Returns:
            str: Either "jp_to_de" or "de_to_jp"
        """
        if self.weekly_correct_german < 2:
            return "jp_to_de"
        return "de_to_jp"

    @property
    def weekly_progress_score(self) -> int:
        """Calculate weekly progress score for prioritization.

        Lower scores indicate items that need more practice this week
        and should be prioritized in quiz selection.

        Returns:
            int: Total weekly correct answers (german + japanese)
        """
        return self.weekly_correct_german + self.weekly_correct_japanese

    def __str__(self) -> str:
        """Return a human-readable string representation.
        
        Returns:
            str: Formatted string showing Japanese and German vocabulary
        """
        jp_str = ", ".join(self.japanese_vocab)
        de_str = ", ".join(self.german_vocab)
        return f"{jp_str} → {de_str}"