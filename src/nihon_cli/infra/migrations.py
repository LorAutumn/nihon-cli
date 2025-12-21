"""Database migration system for vocabulary feature.

This module provides version-based migrations to evolve the database schema
safely without breaking existing data.
"""

import sqlite3
from pathlib import Path
from typing import List, Type


class Migration:
    """Base class for database migrations."""

    version: int = 0
    description: str = ""

    @classmethod
    def apply(cls, db_path: Path) -> None:
        """Apply this migration to the database.

        Args:
            db_path: Path to the SQLite database file

        Raises:
            sqlite3.Error: If migration fails
        """
        raise NotImplementedError


class Migration001AddWeeklyFields(Migration):
    """Migration to add weekly session fields to vocabulary table."""

    version = 1
    description = "Add vocab_type, opposite_id, base_form, and weekly counter fields"

    @classmethod
    def apply(cls, db_path: Path) -> None:
        """Add new columns to vocabulary table."""
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        cursor = conn.cursor()

        try:
            # Check which columns already exist
            cursor.execute("PRAGMA table_info(vocabulary)")
            existing_columns = {row[1] for row in cursor.fetchall()}

            # Add vocab_type column
            if 'vocab_type' not in existing_columns:
                cursor.execute("""
                    ALTER TABLE vocabulary
                    ADD COLUMN vocab_type TEXT
                    CHECK(vocab_type IN ('noun', 'adjective', 'pattern'))
                """)

            # Add opposite_id column
            if 'opposite_id' not in existing_columns:
                cursor.execute("""
                    ALTER TABLE vocabulary
                    ADD COLUMN opposite_id INTEGER
                    REFERENCES vocabulary(id) ON DELETE SET NULL
                """)

            # Add base_form column
            if 'base_form' not in existing_columns:
                cursor.execute("""
                    ALTER TABLE vocabulary
                    ADD COLUMN base_form TEXT
                """)

            # Add weekly_correct_german column
            if 'weekly_correct_german' not in existing_columns:
                cursor.execute("""
                    ALTER TABLE vocabulary
                    ADD COLUMN weekly_correct_german INTEGER DEFAULT 0
                """)

            # Add weekly_correct_japanese column
            if 'weekly_correct_japanese' not in existing_columns:
                cursor.execute("""
                    ALTER TABLE vocabulary
                    ADD COLUMN weekly_correct_japanese INTEGER DEFAULT 0
                """)

            # Create indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_vocab_type
                ON vocabulary(vocab_type)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_opposite_id
                ON vocabulary(opposite_id)
            """)

            conn.commit()

        except sqlite3.Error as e:
            conn.rollback()
            raise sqlite3.Error(f"Migration 001 failed: {e}") from e
        finally:
            conn.close()


class Migration002CreateWeeklySessions(Migration):
    """Migration to create weekly_sessions and weekly_session_items tables."""

    version = 2
    description = "Create weekly_sessions and weekly_session_items tables"

    @classmethod
    def apply(cls, db_path: Path) -> None:
        """Create new tables for weekly sessions."""
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        cursor = conn.cursor()

        try:
            # Create weekly_sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weekly_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    week_start DATE NOT NULL,
                    week_end DATE NOT NULL,
                    status TEXT CHECK(status IN ('active', 'completed')) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(week_start)
                )
            """)

            # Create weekly_session_items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weekly_session_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL REFERENCES weekly_sessions(id) ON DELETE CASCADE,
                    vocab_id INTEGER NOT NULL REFERENCES vocabulary(id) ON DELETE CASCADE,
                    times_tested_this_week INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(session_id, vocab_id)
                )
            """)

            # Create index for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_weekly_session_status
                ON weekly_sessions(status)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_weekly_session_items_session
                ON weekly_session_items(session_id)
            """)

            conn.commit()

        except sqlite3.Error as e:
            conn.rollback()
            raise sqlite3.Error(f"Migration 002 failed: {e}") from e
        finally:
            conn.close()


class MigrationManager:
    """Manages database migrations with version tracking."""

    def __init__(self, db_path: Path):
        """Initialize the migration manager.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.migrations: List[Type[Migration]] = [
            Migration001AddWeeklyFields,
            Migration002CreateWeeklySessions,
        ]

    def _ensure_schema_version_table(self) -> None:
        """Create schema_version table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        cursor = conn.cursor()

        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    description TEXT
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise sqlite3.Error(f"Failed to create schema_version table: {e}") from e
        finally:
            conn.close()

    def get_current_version(self) -> int:
        """Get the current schema version from the database.

        Returns:
            Current schema version (0 if no migrations applied yet)
        """
        self._ensure_schema_version_table()

        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT MAX(version) FROM schema_version")
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0
        finally:
            conn.close()

    def _record_migration(self, migration: Type[Migration]) -> None:
        """Record a migration in the schema_version table.

        Args:
            migration: The migration class that was applied
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO schema_version (version, description)
                VALUES (?, ?)
            """, (migration.version, migration.description))
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise sqlite3.Error(f"Failed to record migration: {e}") from e
        finally:
            conn.close()

    def run_migrations(self) -> int:
        """Run all pending migrations.

        Returns:
            Number of migrations applied

        Raises:
            sqlite3.Error: If any migration fails
        """
        current_version = self.get_current_version()
        applied_count = 0

        # Apply migrations that haven't been applied yet
        for migration in self.migrations:
            if migration.version > current_version:
                print(f"Applying migration {migration.version}: {migration.description}")
                migration.apply(self.db_path)
                self._record_migration(migration)
                applied_count += 1

        if applied_count > 0:
            print(f"✓ Applied {applied_count} migration(s)")

        return applied_count
