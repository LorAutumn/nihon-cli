"""Repository for vocabulary database operations.

This module provides the VocabRepository class for managing vocabulary
items in the SQLite database, including batch inserts and duplicate handling.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional

from nihon_cli.core.vocabulary import VocabularyItem
from nihon_cli.infra.database import init_db


class VocabRepository:
    """Repository for vocabulary database operations.
    
    Handles all database interactions for vocabulary items, including
    batch inserts with duplicate detection and transaction management.
    """
    
    def __init__(self):
        """Initialize the repository with a database connection.
        
        The database path is loaded from the configuration file if available,
        otherwise the default location ~/.nihon-cli/vocab.db is used.
        """
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
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def add_vocabulary_batch(
        self, 
        items: List[VocabularyItem], 
        source_file: str, 
        tag: str
    ) -> tuple[int, int]:
        """Add a batch of vocabulary items to the database.
        
        Uses a transaction to efficiently insert multiple vocabulary items.
        Duplicates (based on japanese_vocab) are skipped to avoid redundancy.
        
        Args:
            items: List of VocabularyItem objects to insert
            source_file: Name of the source file
            tag: User-defined tag for organizing vocabulary
            
        Returns:
            Tuple of (inserted_count, skipped_count)
            
        Raises:
            sqlite3.Error: If database operations fail
            ValueError: If items list is empty
        """
        if not items:
            raise ValueError("Items list cannot be empty")
        
        inserted_count = 0
        skipped_count = 0
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            for item in items:
                # Convert lists to comma-separated strings for storage
                japanese_str = ", ".join(item.japanese_vocab)
                german_str = ", ".join(item.german_vocab)
                
                # Check if this vocabulary already exists
                cursor.execute(
                    "SELECT id FROM vocabulary WHERE japanese_vocab = ?",
                    (japanese_str,)
                )
                
                if cursor.fetchone() is not None:
                    skipped_count += 1
                    continue
                
                # Insert new vocabulary item
                try:
                    cursor.execute(
                        """
                        INSERT INTO vocabulary (
                            japanese_vocab,
                            german_vocab,
                            source_file,
                            upload_tag,
                            correct_german,
                            correct_japanese,
                            completed
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            japanese_str,
                            german_str,
                            source_file,
                            tag,
                            item.correct_german,
                            item.correct_japanese,
                            item.completed
                        )
                    )
                    inserted_count += 1
                except sqlite3.IntegrityError:
                    # Handle any constraint violations
                    skipped_count += 1
                    continue
        
        return inserted_count, skipped_count
    
    def get_vocabulary_by_id(self, vocab_id: int) -> Optional[VocabularyItem]:
        """Retrieve a vocabulary item by its ID.
        
        Args:
            vocab_id: The ID of the vocabulary item to retrieve
            
        Returns:
            VocabularyItem if found, None otherwise
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM vocabulary WHERE id = ?",
                (vocab_id,)
            )
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            return self._row_to_vocabulary_item(row)
    
    def get_incomplete_vocabulary(
        self, 
        limit: int = 15,
        tag: Optional[str] = None
    ) -> List[VocabularyItem]:
        """Retrieve incomplete vocabulary items for learning.
        
        Args:
            limit: Maximum number of items to retrieve
            tag: Optional tag filter
            
        Returns:
            List of VocabularyItem objects that are not yet completed
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if tag:
                cursor.execute(
                    """
                    SELECT * FROM vocabulary 
                    WHERE completed = FALSE AND upload_tag = ?
                    ORDER BY RANDOM()
                    LIMIT ?
                    """,
                    (tag, limit)
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM vocabulary 
                    WHERE completed = FALSE
                    ORDER BY RANDOM()
                    LIMIT ?
                    """,
                    (limit,)
                )
            
            rows = cursor.fetchall()
            return [self._row_to_vocabulary_item(row) for row in rows]
    
    def update_progress(
        self, 
        vocab_id: int, 
        direction: str, 
        correct: bool
    ) -> None:
        """Update the learning progress for a vocabulary item.
        
        Args:
            vocab_id: ID of the vocabulary item
            direction: Either "jp_to_de" or "de_to_jp"
            correct: Whether the answer was correct
            
        Raises:
            ValueError: If direction is invalid
        """
        if direction not in ("jp_to_de", "de_to_jp"):
            raise ValueError(f"Invalid direction: {direction}")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if correct:
                if direction == "jp_to_de":
                    cursor.execute(
                        """
                        UPDATE vocabulary 
                        SET correct_german = correct_german + 1,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """,
                        (vocab_id,)
                    )
                else:  # de_to_jp
                    cursor.execute(
                        """
                        UPDATE vocabulary 
                        SET correct_japanese = correct_japanese + 1,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """,
                        (vocab_id,)
                    )
    
    def mark_completed(self, vocab_id: int) -> None:
        """Mark a vocabulary item as completed.
        
        Args:
            vocab_id: ID of the vocabulary item to mark as completed
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE vocabulary 
                SET completed = TRUE,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (vocab_id,)
            )
    
    def get_statistics(self) -> dict:
        """Get statistics about vocabulary learning progress.
        
        Returns:
            Dictionary containing various statistics
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Total vocabulary count
            cursor.execute("SELECT COUNT(*) FROM vocabulary")
            total = cursor.fetchone()[0]
            
            # Completed count
            cursor.execute("SELECT COUNT(*) FROM vocabulary WHERE completed = TRUE")
            completed = cursor.fetchone()[0]
            
            # In progress count
            in_progress = total - completed
            
            return {
                'total': total,
                'completed': completed,
                'in_progress': in_progress,
                'completion_percentage': (completed / total * 100) if total > 0 else 0
            }
    
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
        
        return VocabularyItem(
            id=row['id'],
            japanese_vocab=japanese_vocab,
            german_vocab=german_vocab,
            source_file=row['source_file'],
            upload_tag=row['upload_tag'],
            correct_german=row['correct_german'],
            correct_japanese=row['correct_japanese'],
            completed=bool(row['completed'])
        )