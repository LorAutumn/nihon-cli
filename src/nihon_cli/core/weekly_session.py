"""Domain models for weekly learning sessions.

This module defines the WeeklySession and WeeklySessionItem classes
that represent weekly vocabulary learning cycles (Thursday-Wednesday).
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional

from nihon_cli.core.vocabulary import VocabularyItem


@dataclass
class WeeklySession:
    """Represents a weekly learning session (Thursday-Wednesday cycle).

    Attributes:
        id: Unique identifier for the session
        week_start: Start date of the week (always Thursday)
        week_end: End date of the week (always Wednesday)
        status: Session status ('active' or 'completed')
        created_at: Timestamp when the session was created
        updated_at: Timestamp when the session was last updated
    """

    id: int
    week_start: date
    week_end: date
    status: str  # 'active' or 'completed'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def get_current_week_boundaries() -> tuple[date, date]:
        """Calculate Thursday-Wednesday boundaries for the current week.

        Returns:
            Tuple of (week_start_thursday, week_end_wednesday)

        Examples:
            If today is Monday, returns (last Thursday, this Wednesday)
            If today is Thursday, returns (this Thursday, next Wednesday)
            If today is Friday, returns (last Thursday, this Wednesday)
        """
        today = date.today()

        # weekday() returns 0=Monday, 1=Tuesday, ..., 6=Sunday
        # We want 3=Thursday
        # Calculate days since last Thursday
        days_since_thursday = (today.weekday() - 3) % 7

        week_start = today - timedelta(days=days_since_thursday)
        week_end = week_start + timedelta(days=6)  # Wednesday (6 days after Thursday)

        return week_start, week_end

    def is_current_week(self) -> bool:
        """Check if this session is for the current week.

        Returns:
            True if this session's week_start matches current week's Thursday
        """
        current_start, _ = self.get_current_week_boundaries()
        return self.week_start == current_start

    def is_expired(self) -> bool:
        """Check if the week has ended.

        Returns:
            True if today's date is past the week_end (Wednesday)
        """
        return date.today() > self.week_end

    def __str__(self) -> str:
        """Return a human-readable string representation.

        Returns:
            String showing week range and status
        """
        return f"Week {self.week_start} - {self.week_end} ({self.status})"


@dataclass
class WeeklySessionItem:
    """Represents a vocabulary item within a weekly session.

    This links vocabulary items to specific weekly sessions and tracks
    how many times each item has been tested during the week.

    Attributes:
        id: Unique identifier for this session-item link
        session_id: ID of the weekly session
        vocab_id: ID of the vocabulary item
        times_tested_this_week: Counter for how many times tested
        vocab: Optional VocabularyItem object (populated via join)
    """

    id: int
    session_id: int
    vocab_id: int
    times_tested_this_week: int = 0
    vocab: Optional[VocabularyItem] = None

    def __str__(self) -> str:
        """Return a human-readable string representation.

        Returns:
            String showing vocab info if available
        """
        if self.vocab:
            return f"{self.vocab} (tested {self.times_tested_this_week}x)"
        return f"Vocab ID {self.vocab_id} (tested {self.times_tested_this_week}x)"
