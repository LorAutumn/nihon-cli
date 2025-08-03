# Changelog - Nihon CLI

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
