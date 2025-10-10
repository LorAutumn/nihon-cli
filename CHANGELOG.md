# Changelog - Nihon CLI

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-10-10

### ✨ Added

-   **Vocabulary Learning System**: Complete vocabulary management and learning feature
    -   `vocab upload` command to import vocabulary from Markdown files
    -   `vocab learn` command for interactive vocabulary learning sessions
    -   Adaptive query direction (Japanese→German, then German→Japanese)
    -   Progress tracking with 5 correct answers required per direction
    -   Session statistics with accuracy and completion metrics
-   **Markdown Parser**: [`MarkdownVocabParser`](src/nihon_cli/core/parser.py:14) for parsing vocabulary tables
    -   Supports comma-separated multiple meanings
    -   Validates table format with proper error handling
    -   UTF-8 encoding support for Japanese characters
-   **Database Infrastructure**: SQLite-based vocabulary storage
    -   [`VocabRepository`](src/nihon_cli/infra/repository.py:16) for database operations
    -   Batch insert with duplicate detection
    -   Progress tracking and completion status management
    -   Statistics API for learning progress overview
-   **Domain Models**: [`VocabularyItem`](src/nihon_cli/core/vocabulary.py:13) dataclass with learning metadata
    -   Adaptive direction logic based on progress counters
    -   Progress percentage calculation
    -   Completion readiness detection

### 🔧 Changed

-   **CLI Structure**: Extended command hierarchy with vocabulary subcommands
    -   Added `vocab` parent command with `upload` and `learn` subcommands
    -   Enhanced [`commands.py`](src/nihon_cli/cli/commands.py:1) with vocabulary handlers
-   **Project Version**: Bumped to 1.2.0 in [`pyproject.toml`](pyproject.toml:7)
-   **Infrastructure Layer**: New `infra` package for data persistence
    -   [`database.py`](src/nihon_cli/infra/database.py:1) for schema initialization
    -   [`repository.py`](src/nihon_cli/infra/repository.py:1) for data access patterns

### 🐛 Fixed

### 🏗️ Technical Details

-   **Database Schema**: SQLite database at `~/.nihon-cli/vocab.db`
    -   Vocabulary table with progress counters and completion status
    -   Indexes on `japanese_vocab` and `completed` for query optimization
    -   Automatic timestamp tracking for created_at and updated_at
-   **Learning Algorithm**: Spaced repetition approach
    -   5 correct answers required per direction (JP→DE, DE→JP)
    -   Adaptive query direction based on progress
    -   Random selection of incomplete vocabulary items
-   **Architecture**: Clean separation of concerns
    -   Core domain models in [`core/vocabulary.py`](src/nihon_cli/core/vocabulary.py:1)
    -   Quiz engine in [`core/quiz_vocab.py`](src/nihon_cli/core/quiz_vocab.py:1)
    -   Infrastructure layer for persistence
    -   CLI handlers for user interaction
-   **Data Format**: Markdown table format for vocabulary import
    -   Expected columns: `Japanisch` and `Deutsch`
    -   Supports multiple meanings separated by commas
    -   Tag-based organization for vocabulary sets

## [1.1.0] - 2025-08-03

### 💥 BREAKING CHANGES

-   **CLI Structure**: Changed command structure from `nihon cli <mode>` to `nihon-cli <mode>`
    -   Old: `nihon cli hiragana`
    -   New: `nihon-cli hiragana`

### ✨ Added

-   **Advanced Character Support**: Added `--advanced` flag to all quiz modes (hiragana, katakana, mixed)
    -   Includes combination characters (Yōon) such as きゃ, しゅ, ちょ, etc.
    -   Basic mode remains default for gradual learning progression
-   **Flexible Character Sets**: Users can now choose between basic and advanced character training

### 🔧 Changed

-   **Character Data Restructure**: Split character data into modular files
    -   `hiragana_basic.py` - Basic Hiragana characters (Gojūon, special chars, Dakuten/Handakuten)
    -   `hiragana_advanced.py` - Advanced Hiragana characters (Yōon combinations)
    -   `katakana_basic.py` - Basic Katakana characters
    -   `katakana_advanced.py` - Advanced Katakana characters
    -   Original `hiragana.py` and `katakana.py` maintain backward compatibility
-   **Documentation**: Comprehensive README update with new command structure and features

### 🐛 Fixed

-   **UI Formatting**: Fixed box drawing width calculation in formatting module

### 🏗️ Technical Details

-   **Backward Compatibility**: All existing character imports continue to work
-   **Quiz Engine**: Enhanced to support basic/advanced character selection
-   **CLI Parser**: Streamlined argument parsing with direct command structure

## [1.0.0] - 2025-01-30

### ✅ Added

-   Vollständiges Hiragana/Katakana-Training
-   CLI-Interface mit argparse
-   Timer-System mit 25-Min/5-Sek Modi
-   Quiz-Engine mit 10 zufälligen Zeichen
-   Terminal-Clearing zwischen Sessions
-   PEP 8 konforme Code-Qualität
-   Umfassende Sicherheitsprüfung
-   uvx-Kompatibilität
-   Vollständige Dokumentation

### 🏗️ Technical

-   Domain-Driven Design
-   Character Domain Model
-   208 japanische Zeichen (104 Hiragana + 104 Katakana)
-   Cross-Platform-Kompatibilität
-   Nur Standard-Python-Bibliotheken

### 📦 Deployment

-   pip-Installation: `pip install -e .`
-   uvx-Nutzung: `uvx nihon-cli cli hiragana --test`
-   Entry Points konfiguriert
-   Moderne pyproject.toml-Konfiguration
