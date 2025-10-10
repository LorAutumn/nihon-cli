"""Database initialization and management for the vocabulary feature.

This module handles SQLite database creation and schema management for
storing vocabulary items and their learning progress.
"""

import sqlite3
from pathlib import Path
from typing import Optional


def init_db(db_path: Optional[str] = None) -> Path:
    """Initialize the vocabulary database.
    
    Creates the SQLite database at ~/.nihon-cli/vocab.db if it doesn't exist.
    Also creates the vocabulary table with the required schema and indexes.
    
    Args:
        db_path: Optional custom database path. If None, uses ~/.nihon-cli/vocab.db
        
    Returns:
        Path: The path to the initialized database file
        
    Raises:
        sqlite3.Error: If database creation or schema setup fails
    """
    # Determine database location
    if db_path is None:
        db_dir = Path.home() / ".nihon-cli"
        db_dir.mkdir(parents=True, exist_ok=True)
        db_path = db_dir / "vocab.db"
    else:
        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Connect to database (creates file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create vocabulary table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                japanese_vocab TEXT NOT NULL,
                german_vocab TEXT NOT NULL,
                source_file TEXT,
                upload_tag TEXT,
                correct_german INTEGER DEFAULT 0,
                correct_japanese INTEGER DEFAULT 0,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for performance optimization
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_japanese_vocab 
            ON vocabulary(japanese_vocab)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_completed 
            ON vocabulary(completed)
        """)
        
        # Commit changes
        conn.commit()
        
    except sqlite3.Error as e:
        conn.rollback()
        raise sqlite3.Error(f"Failed to initialize database: {e}") from e
    finally:
        conn.close()
    
    return Path(db_path)