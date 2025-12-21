"""Repository for weekly session database operations.

This module provides the WeeklySessionRepository class for managing
weekly learning sessions and their associated vocabulary items.
"""

import sqlite3
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

from nihon_cli.core.vocabulary import VocabularyItem
from nihon_cli.core.weekly_session import WeeklySession, WeeklySessionItem
from nihon_cli.infra.database import init_db


class WeeklySessionRepository:
    """Repository for weekly session database operations.

    Handles all database interactions for weekly sessions and their
    relationships with vocabulary items.
    """

    def __init__(self):
        """Initialize the repository with a database connection."""
        self.db_path = init_db()

    @contextmanager
    def _get_connection(self):
        """Context manager for safe database connections.

        Yields:
            sqlite3.Connection: Database connection with row factory set

        Raises:
            sqlite3.Error: If database operations fail
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_current_week_session(self) -> Optional[WeeklySession]:
        """Get the active session for the current week.

        Returns:
            WeeklySession if one exists for current week, None otherwise
        """
        week_start, week_end = WeeklySession.get_current_week_boundaries()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM weekly_sessions
                WHERE week_start = ? AND week_end = ?
                """,
                (week_start, week_end)
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_weekly_session(row)

    def create_new_session(self, vocab_ids: List[int]) -> WeeklySession:
        """Create a new weekly session with specified vocabulary items.

        Args:
            vocab_ids: List of vocabulary IDs to include in this session

        Returns:
            Newly created WeeklySession

        Raises:
            ValueError: If vocab_ids is empty, contains invalid IDs, or session already exists
            sqlite3.Error: If database operations fail
        """
        if not vocab_ids:
            raise ValueError("vocab_ids cannot be empty")

        week_start, week_end = WeeklySession.get_current_week_boundaries()

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Validate that all vocab_ids exist in the vocabulary table
            placeholders = ','.join('?' * len(vocab_ids))
            cursor.execute(
                f"SELECT id FROM vocabulary WHERE id IN ({placeholders})",
                vocab_ids
            )
            valid_ids = {row[0] for row in cursor.fetchall()}
            invalid_ids = set(vocab_ids) - valid_ids

            if invalid_ids:
                raise ValueError(f"Invalid vocabulary IDs: {sorted(invalid_ids)}")

            # Check if session for this week already exists
            cursor.execute(
                "SELECT id, status FROM weekly_sessions WHERE week_start = ?",
                (week_start,)
            )
            existing = cursor.fetchone()
            if existing:
                raise ValueError(
                    f"Session for week {week_start} already exists "
                    f"(ID: {existing[0]}, Status: {existing[1]})"
                )

            # Create the session
            cursor.execute(
                """
                INSERT INTO weekly_sessions (week_start, week_end, status)
                VALUES (?, ?, 'active')
                """,
                (week_start, week_end)
            )
            session_id = cursor.lastrowid

            # Link vocabulary items to session
            for vocab_id in vocab_ids:
                cursor.execute(
                    """
                    INSERT INTO weekly_session_items (session_id, vocab_id)
                    VALUES (?, ?)
                    """,
                    (session_id, vocab_id)
                )

            # Fetch and return the created session
            cursor.execute(
                "SELECT * FROM weekly_sessions WHERE id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
            return self._row_to_weekly_session(row)

    def get_session_items(
        self,
        session_id: int,
        prioritize_by_progress: bool = True
    ) -> List[VocabularyItem]:
        """Get vocabulary items for a session.

        Args:
            session_id: ID of the weekly session
            prioritize_by_progress: If True, order by weekly_progress_score ASC

        Returns:
            List of VocabularyItem objects
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            if prioritize_by_progress:
                # Order by weekly progress (lower scores first)
                cursor.execute(
                    """
                    SELECT v.* FROM vocabulary v
                    INNER JOIN weekly_session_items wsi ON v.id = wsi.vocab_id
                    WHERE wsi.session_id = ?
                    ORDER BY (v.weekly_correct_german + v.weekly_correct_japanese) ASC
                    """,
                    (session_id,)
                )
            else:
                cursor.execute(
                    """
                    SELECT v.* FROM vocabulary v
                    INNER JOIN weekly_session_items wsi ON v.id = wsi.vocab_id
                    WHERE wsi.session_id = ?
                    """,
                    (session_id,)
                )

            rows = cursor.fetchall()
            return [self._row_to_vocabulary_item(row) for row in rows]

    def check_week_expired(self, session_id: int) -> bool:
        """Check if a session's week has expired.

        Args:
            session_id: ID of the weekly session

        Returns:
            True if week has expired, False otherwise
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT week_end FROM weekly_sessions WHERE id = ?",
                (session_id,)
            )
            row = cursor.fetchone()

            if row is None:
                return True

            week_end = date.fromisoformat(row['week_end'])
            return date.today() > week_end

    def complete_session(self, session_id: int) -> None:
        """Mark a session as completed.

        Args:
            session_id: ID of the weekly session to complete
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE weekly_sessions
                SET status = 'completed',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (session_id,)
            )

    def get_session_statistics(self, session_id: int) -> Dict:
        """Get statistics for a weekly session.

        Args:
            session_id: ID of the weekly session

        Returns:
            Dictionary containing session statistics
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Total items in session
            cursor.execute(
                """
                SELECT COUNT(*) FROM weekly_session_items
                WHERE session_id = ?
                """,
                (session_id,)
            )
            total_items = cursor.fetchone()[0]

            # Items with 2+ correct in JP→DE
            cursor.execute(
                """
                SELECT COUNT(*) FROM vocabulary v
                INNER JOIN weekly_session_items wsi ON v.id = wsi.vocab_id
                WHERE wsi.session_id = ? AND v.weekly_correct_german >= 2
                """,
                (session_id,)
            )
            items_2plus_german = cursor.fetchone()[0]

            # Items with 2+ correct in DE→JP
            cursor.execute(
                """
                SELECT COUNT(*) FROM vocabulary v
                INNER JOIN weekly_session_items wsi ON v.id = wsi.vocab_id
                WHERE wsi.session_id = ? AND v.weekly_correct_japanese >= 2
                """,
                (session_id,)
            )
            items_2plus_japanese = cursor.fetchone()[0]

            # Average weekly progress
            cursor.execute(
                """
                SELECT AVG(v.weekly_correct_german + v.weekly_correct_japanese)
                FROM vocabulary v
                INNER JOIN weekly_session_items wsi ON v.id = wsi.vocab_id
                WHERE wsi.session_id = ?
                """,
                (session_id,)
            )
            avg_progress = cursor.fetchone()[0] or 0

            return {
                'total_items': total_items,
                'items_2plus_german': items_2plus_german,
                'items_2plus_japanese': items_2plus_japanese,
                'avg_progress': avg_progress
            }

    def add_items_to_session(
        self,
        session_id: int,
        vocab_ids: List[int]
    ) -> int:
        """Add vocabulary items to an existing session.

        Args:
            session_id: ID of the weekly session
            vocab_ids: List of vocabulary IDs to add

        Returns:
            Number of items added (excluding duplicates)

        Raises:
            ValueError: If vocab_ids is empty or contains invalid IDs
        """
        if not vocab_ids:
            raise ValueError("vocab_ids cannot be empty")

        added_count = 0

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Validate that all vocab_ids exist in the vocabulary table
            placeholders = ','.join('?' * len(vocab_ids))
            cursor.execute(
                f"SELECT id FROM vocabulary WHERE id IN ({placeholders})",
                vocab_ids
            )
            valid_ids = {row[0] for row in cursor.fetchall()}
            invalid_ids = set(vocab_ids) - valid_ids

            if invalid_ids:
                raise ValueError(f"Invalid vocabulary IDs: {sorted(invalid_ids)}")

            for vocab_id in vocab_ids:
                try:
                    cursor.execute(
                        """
                        INSERT INTO weekly_session_items (session_id, vocab_id)
                        VALUES (?, ?)
                        """,
                        (session_id, vocab_id)
                    )
                    added_count += 1
                except sqlite3.IntegrityError:
                    # Item already in session, skip
                    continue

        return added_count

    @staticmethod
    def _row_to_weekly_session(row: sqlite3.Row) -> WeeklySession:
        """Convert a database row to a WeeklySession object.

        Args:
            row: SQLite row object

        Returns:
            WeeklySession object
        """
        return WeeklySession(
            id=row['id'],
            week_start=date.fromisoformat(row['week_start']),
            week_end=date.fromisoformat(row['week_end']),
            status=row['status']
        )

    @staticmethod
    def _row_to_vocabulary_item(row: sqlite3.Row) -> VocabularyItem:
        """Convert a database row to a VocabularyItem object.

        Args:
            row: SQLite row object

        Returns:
            VocabularyItem object
        """
        # Parse comma-separated strings back to lists
        japanese_vocab = [v.strip() for v in row['japanese_vocab'].split(',')]
        german_vocab = [v.strip() for v in row['german_vocab'].split(',')]

        # Helper function to safely get column value
        def safe_get(key, default=None):
            try:
                return row[key] if row[key] is not None else default
            except (IndexError, KeyError):
                return default

        return VocabularyItem(
            id=row['id'],
            japanese_vocab=japanese_vocab,
            german_vocab=german_vocab,
            source_file=row['source_file'],
            upload_tag=row['upload_tag'],
            correct_german=row['correct_german'],
            correct_japanese=row['correct_japanese'],
            completed=bool(row['completed']),
            vocab_type=safe_get('vocab_type'),
            opposite_id=safe_get('opposite_id'),
            base_form=safe_get('base_form'),
            weekly_correct_german=safe_get('weekly_correct_german', 0),
            weekly_correct_japanese=safe_get('weekly_correct_japanese', 0)
        )
