# Nihon CLI

A Python-based CLI tool for learning Japanese characters (Hiragana and Katakana) with automated learning intervals.

## Overview

Nihon CLI is designed to help users learn Japanese characters through interactive quiz sessions with timed intervals. The application uses a spaced repetition approach with 25-minute learning intervals to optimize retention.

## Features (Planned)

- **Interactive Quiz Sessions**: Learn Hiragana and Katakana characters through randomized quizzes
- **Automated Learning Intervals**: 25-minute standard intervals with 5-second test mode
- **Character Sets**: Support for Hiragana, Katakana, and mixed character sets
- **Simple CLI Interface**: Easy-to-use command-line interface
- **No External Dependencies**: Uses only Python standard library

## Installation

### Development Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd nihon-cli
```

2. Install the package in editable mode:
```bash
uv pip install -e .
```

### Production Installation

(Coming soon)

## Usage

Once installed, you can use the `nihon` command:

```bash
# Display the main help message
nihon --help

# Display help for the training commands
nihon cli --help

# Start a Hiragana training session
nihon cli hiragana

# Start a Katakana training session
nihon cli katakana

# Start a mixed Hiragana and Katakana training session
nihon cli mixed

# Run a training session in test mode (5-second intervals)
nihon cli hiragana --test
```

## Project Structure

```
nihon-cli/
├── src/
│   ├── nihon_cli/
│   │   ├── __init__.py
│   │   ├── main.py              # CLI Entry Point
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── character.py     # Character Domain Model
│   │   │   ├── quiz.py          # Quiz Logic
│   │   │   └── timer.py         # Learning Timer
│   │   ├── data/
│   │   │   ├── __init__.py
│   │   │   ├── hiragana.py      # Hiragana Character Data
│   │   │   └── katakana.py      # Katakana Character Data
│   │   └── cli/
│   │       ├── __init__.py
│   │       └── commands.py      # CLI Command Handler
├── tests/
├── setup.py
└── README.md
```

## Development Status

**Current Phase: 5.2 - Entry Points and Installation**

- ✅ Project structure created
- ✅ Setup.py configured for CLI installation
- ✅ Core functionality implemented
- ✅ CLI interface finalized
- ✅ Entry points and installation finalized
- ⏳ Final testing and refinement (upcoming)

## Development Phases

1. **Phase 1**: Project Setup and Basic Structure (Completed)
2. **Phase 2**: Domain Models and Data Structures (Completed)
3. **Phase 3**: Core Logic Implementation (Completed)
4. **Phase 4**: CLI Interface (Completed)
5. **Phase 5**: Integration and Main Entry Point (In Progress)
6. **Phase 6**: Testing and Refinement

## Requirements

- Python 3.8 or higher
- No external dependencies (uses only standard library)

## Contributing

This project follows Python best practices:

- **PEP 8**: Python style guide compliance
- **Type Hints**: For better code clarity
- **Docstrings**: Comprehensive documentation
- **Domain-Driven Design**: Clean, modular architecture

## License

MIT License (to be added)

## Roadmap

- [x] Complete core functionality implementation
- [x] Add comprehensive character datasets
- [x] Implement quiz and timer systems
- [x] Add CLI command handling
- [ ] Create automated tests
- [ ] Add progress tracking features
- [ ] Implement advanced learning algorithms

---

*This project is currently in early development. Core functionality will be implemented in upcoming phases.*