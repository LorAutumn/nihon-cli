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

2. Install with uv (recommended):
```bash
uv sync --dev
```

Or using traditional pip:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Production Installation

```bash
uv add nihon-cli
```

Or using pip:
```bash
pip install nihon-cli
```

## Usage

Once installed, you can use the `nihon` command:

```bash
# Basic usage (implementation coming soon)
nihon --help

# Hiragana learning mode
nihon cli hiragana

# Katakana learning mode  
nihon cli katakana

# Mixed mode
nihon cli hiraganakatakana

# Test mode (5-second intervals)
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

**Current Phase: 1.1 - Project Setup and Basic Structure**

- ✅ Project structure created
- ✅ Setup.py configured for CLI installation
- ✅ Basic module structure established
- ⏳ Core functionality implementation (upcoming phases)

## Development Phases

1. **Phase 1**: Project Setup and Basic Structure
2. **Phase 2**: Domain Models and Data Structures
3. **Phase 3**: Core Logic Implementation
4. **Phase 4**: CLI Interface
5. **Phase 5**: Integration and Main Entry Point
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

- [ ] Complete core functionality implementation
- [ ] Add comprehensive character datasets
- [ ] Implement quiz and timer systems
- [ ] Add CLI command handling
- [ ] Create automated tests
- [ ] Add progress tracking features
- [ ] Implement advanced learning algorithms

---

*This project is currently in early development. Core functionality will be implemented in upcoming phases.*