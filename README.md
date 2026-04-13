# Nihon CLI

A Python-based CLI tool for learning Japanese characters (Hiragana and Katakana) with automated learning intervals.

## Overview

Nihon CLI is designed to help users learn Japanese characters through interactive quiz sessions with timed intervals. The application uses a spaced repetition approach with 25-minute learning intervals to optimize retention.

## Features

-   **Interactive Quiz Sessions**: Learn Hiragana and Katakana characters through randomized quizzes
-   **Automated Learning Intervals**: 25-minute standard intervals with 5-second test mode
-   **Character Sets**: Support for Hiragana, Katakana, and mixed character sets
-   **Basic and Advanced Characters**: Choose between basic characters or include advanced combination characters (Yōon)
-   **Simple CLI Interface**: Easy-to-use command-line interface
-   **Kanji Learning**: Import kanji from images (OCR) and learn them with spaced repetition
-   **Flash Cards**: Always-on-top floating window for passive katakana and kanji review

## Installation

You can install Nihon CLI using either `pip` or `uvx`.

### Using `uvx` (Recommended)

`uvx` allows you to run the CLI tool in a temporary virtual environment without polluting your global Python installation.

```bash
# Run the tool directly using uvx
uvx nihon-cli --help
```

### Using `pip`

#### Development Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd nihon-cli
```

2. Install the package in editable mode:

```bash
pip install -e .
```

#### Production Installation

You can install the package directly from GitHub:

```bash
pip install git+https://github.com/your-username/nihon-cli.git
```

### Uninstallation

To uninstall the package, run the following command:

```bash
pip uninstall nihon-cli
```

## Running Locally for Development

When working with the local source code (for development or testing), you need to use the `--from .` flag with `uvx` to run the tool from the current directory instead of looking for a published package.

**Important**: The command `uvx nihon-cli --help` will fail when running from local source because `uvx` tries to find a published package. Use the commands below instead:

```bash
# Display the main help message
uvx --from . nihon-cli --help

# Display help for a specific command
uvx --from . nihon-cli hiragana --help

# Start a Hiragana training session (basic characters only)
uvx --from . nihon-cli hiragana

# Start a Katakana training session (basic characters only)
uvx --from . nihon-cli katakana

# Start a mixed Hiragana and Katakana training session (basic characters only)
uvx --from . nihon-cli mixed

# Start a Hiragana training session with advanced characters (includes combination characters/Yōon)
uvx --from . nihon-cli hiragana --advanced

# Start a Katakana training session with advanced characters
uvx --from . nihon-cli katakana --advanced

# Start a mixed training session with advanced characters
uvx --from . nihon-cli mixed --advanced

# Run a training session in test mode (5-second intervals)
uvx --from . nihon-cli hiragana --test

# Combine test mode with advanced characters
uvx --from . nihon-cli hiragana --test --advanced
```

The `--from .` flag tells `uvx` to install and run the package from the current directory, allowing you to test your local changes without needing to publish the package first.

## Usage

### With `uvx`

You can run all commands by prefixing them with `uvx`:

```bash
# Display the main help message
uvx nihon-cli --help

# Display help for a specific command
uvx nihon-cli hiragana --help

# Start a Hiragana training session (basic characters only)
uvx nihon-cli hiragana

# Start a Katakana training session (basic characters only)
uvx nihon-cli katakana

# Start a mixed Hiragana and Katakana training session (basic characters only)
uvx nihon-cli mixed

# Start a Hiragana training session with advanced characters (includes combination characters/Yōon)
uvx nihon-cli hiragana --advanced

# Start a Katakana training session with advanced characters
uvx nihon-cli katakana --advanced

# Start a mixed training session with advanced characters
uvx nihon-cli mixed --advanced

# Run a training session in test mode (5-second intervals)
uvx nihon-cli hiragana --test

# Combine test mode with advanced characters
uvx nihon-cli hiragana --test --advanced
```

### With `pip`

If you installed the package with `pip`, you can use the `nihon-cli` command directly:

```bash
# Display the main help message
nihon-cli --help

# Display help for a specific command
nihon-cli hiragana --help

# Start a Hiragana training session (basic characters only)
nihon-cli hiragana

# Start a Katakana training session (basic characters only)
nihon-cli katakana

# Start a mixed Hiragana and Katakana training session (basic characters only)
nihon-cli mixed

# Start a Hiragana training session with advanced characters (includes combination characters/Yōon)
nihon-cli hiragana --advanced

# Start a Katakana training session with advanced characters
nihon-cli katakana --advanced

# Start a mixed training session with advanced characters
nihon-cli mixed --advanced

# Run a training session in test mode (5-second intervals)
nihon-cli hiragana --test

# Combine test mode with advanced characters
nihon-cli hiragana --test --advanced
```

## Available Commands

This section provides a complete reference of all available `uvx` commands and their functionality.

### Core Training Commands

#### `hiragana`

Starts a pure Hiragana character training session.

```bash
# Basic usage
uvx nihon-cli hiragana

# With options
uvx nihon-cli hiragana --test --advanced
```

**Available Options:**

-   `--test`: Run in 5-second test mode
-   `--advanced`: Include advanced combination characters (Yōon)

#### `katakana`

Starts a pure Katakana character training session.

```bash
# Basic usage
uvx nihon-cli katakana

# With options
uvx nihon-cli katakana --test --advanced
```

**Available Options:**

-   `--test`: Run in 5-second test mode
-   `--advanced`: Include advanced combination characters (Yōon)

#### `mixed`

Starts a mixed Hiragana and Katakana character training session.

```bash
# Basic usage
uvx nihon-cli mixed

# With options
uvx nihon-cli mixed --test --advanced
```

**Available Options:**

-   `--test`: Run in 5-second test mode
-   `--advanced`: Include advanced combination characters (Yōon)

#### `words`

Starts a Japanese vocabulary training session.

```bash
# Basic usage
uvx nihon-cli words

# With test mode
uvx nihon-cli words --test
```

**Available Options:**

-   `--test`: Run in 5-second test mode

**Note:** The `--advanced` option is not available for the `words` command as all vocabulary is included by default.

### Kanji Commands

#### `kanji import`

Imports kanji from image files using OCR (requires OpenAI API key).

```bash
# Import kanji from a single image
nihon-cli kanji import path/to/image.HEIC

# Import from multiple images at once
nihon-cli kanji import img1.HEIC img2.HEIC img3.HEIC

# With a custom tag
nihon-cli kanji import *.HEIC --tag "lektion1"
```

**Available Options:**

-   `--tag`: Optional tag for organizing imports (default: `kanji_<date>`)

#### `kanji learn`

Starts an interactive kanji learning session with box logic (5x correct = completed).

```bash
# Start learning
nihon-cli kanji learn

# With test mode (5-second intervals)
nihon-cli kanji learn --test

# Limit kanji per session
nihon-cli kanji learn --limit 10
```

**Available Options:**

-   `--test`: Run in 5-second test mode
-   `--limit`: Number of kanji per session (default: 15)

#### `kanji list`

Shows all imported kanji with their learning progress.

```bash
nihon-cli kanji list
```

### Flash Card Commands

#### `flash katakana`

Opens a floating always-on-top window that cycles through katakana characters with readings and example words.

```bash
nihon-cli flash katakana
```

#### `flash kanji`

Opens a floating always-on-top window that cycles through unlearned kanji from the database.

```bash
nihon-cli flash kanji
```

**Window Features:**

-   Always-on-top, freely resizable
-   Configurable interval (1-15s, default 4s)
-   Example words and readings toggleable via hover menu (top right)
-   Click or Space/Arrow Right to skip to next card

### Command Options Reference

-   `--test`: Runs the training in a 5-second test mode instead of the standard 25-minute intervals
-   `--advanced`: Includes advanced characters (combination characters/Yōon) in addition to basic characters (available for `hiragana`, `katakana`, and `mixed` commands only)

### Character Sets

-   **Basic Characters**: Includes Gojūon (basic syllabary), special characters (ん, っ), and Dakuten/Handakuten characters (が, ざ, だ, ば, ぱ, etc.)
-   **Advanced Characters**: Includes combination characters (Yōon) such as きゃ, しゅ, ちょ, etc.

By default, only basic characters are included. Use the `--advanced` flag to include combination characters for a more comprehensive learning experience.

## Project Structure

```
nihon-cli/
├── src/
│   ├── nihon_cli/
│   │   ├── __init__.py
│   │   ├── main.py              # CLI Entry Point
│   │   ├── app.py               # Main Application Logic
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── character.py     # Character Domain Model
│   │   │   ├── kanji.py         # Kanji Domain Model
│   │   │   ├── quiz.py          # Quiz Logic
│   │   │   ├── quiz_kanji.py    # Kanji Quiz Engine
│   │   │   ├── flash.py         # Flash Card Window
│   │   │   └── timer.py         # Learning Timer
│   │   ├── data/
│   │   │   ├── __init__.py
│   │   │   ├── hiragana.py      # Complete Hiragana Character Data
│   │   │   ├── hiragana_basic.py    # Basic Hiragana Characters
│   │   │   ├── hiragana_advanced.py # Advanced Hiragana Characters (Yōon)
│   │   │   ├── katakana.py      # Complete Katakana Character Data
│   │   │   ├── katakana_basic.py    # Basic Katakana Characters
│   │   │   ├── katakana_advanced.py # Advanced Katakana Characters (Yōon)
│   │   │   └── katakana_flash.py   # Katakana Flash Card Data
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   └── commands.py      # CLI Command Handler
│   │   └── ui/
│   │       └── formatting.py   # UI Formatting Utilities
├── tests/
├── pyproject.toml
└── README.md
```

## Development Status

**Current Phase: Completed - Full Feature Implementation**

-   ✅ Project structure created
-   ✅ Core functionality implemented
-   ✅ CLI interface with direct command structure
-   ✅ Basic and advanced character support
-   ✅ Entry points and installation configured
-   ✅ Character data restructured for flexibility
-   ✅ Advanced mode implementation completed

## Development Phases

1. **Phase 1**: Project Setup and Basic Structure (Completed)
2. **Phase 2**: Domain Models and Data Structures (Completed)
3. **Phase 3**: Core Logic Implementation (Completed)
4. **Phase 4**: CLI Interface (Completed)
5. **Phase 5**: Integration and Main Entry Point (In Progress)
6. **Phase 6**: Testing and Refinement

## Requirements

-   Python 3.8 or higher
-   No external dependencies (uses only standard library)

## Contributing

This project follows Python best practices:

-   **PEP 8**: Python style guide compliance
-   **Type Hints**: For better code clarity
-   **Docstrings**: Comprehensive documentation
-   **Domain-Driven Design**: Clean, modular architecture

## License

MIT License (to be added)

## Roadmap

-   [x] Complete core functionality implementation
-   [x] Add comprehensive character datasets
-   [x] Implement quiz and timer systems
-   [x] Add CLI command handling
-   [x] Kanji learning mode with OCR import and box logic
-   [x] Flash card window for passive katakana and kanji review
-   [ ] Create automated tests
-   [ ] Add progress tracking features
-   [ ] Implement advanced learning algorithms

---

_This project is currently in early development. Core functionality will be implemented in upcoming phases._
