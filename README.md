# Nihon CLI

A Python-based CLI tool for learning Japanese characters (Hiragana and Katakana) with automated learning intervals.

## Overview

Nihon CLI is designed to help users learn Japanese characters through interactive quiz sessions with timed intervals. The application uses a spaced repetition approach with 25-minute learning intervals to optimize retention.

## Features

- **Interactive Quiz Sessions**: Learn Hiragana and Katakana characters through randomized quizzes.
- **Visual Feedback**: Emojis provide instant feedback on your answers (✅ for correct, ❌ for incorrect).
- **Automated Learning Intervals**: 25-minute standard intervals, configurable and with a 5-second test mode.
- **Character Sets**: Support for Hiragana, Katakana, and mixed character sets.
- **Configuration**: Customize behavior with a `config.json` file (`--no-sound`, notification types).
- **Audio Notifications**: Sound alerts at the end of a learning interval.
- **Notification Types**: Choose between different system notification styles.
- **Simple CLI Interface**: Easy-to-use command-line interface.
- **No External Dependencies**: Uses only the Python standard library.

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

## Usage

### With `uvx`

You can run all commands by prefixing them with `uvx`:

```bash
# Display the main help message
uvx nihon-cli --help

# Display help for the training commands
uvx nihon-cli cli --help

# Start a Hiragana training session
uvx nihon-cli cli hiragana

# Start a Katakana training session
uvx nihon-cli cli katakana

# Start a mixed Hiragana and Katakana training session
uvx nihon-cli cli mixed

# Run a training session in test mode (5-second intervals)
uvx nihon-cli cli hiragana --test

# Disable audio notifications for a session
uvx nihon-cli cli hiragana --no-sound

# Set a specific notification type
uvx nihon-cli cli hiragana --notification-type "mac"
```

## Visual Feedback

Nihon CLI uses emojis to provide immediate visual feedback during quiz sessions, making the learning process more intuitive and engaging.

- **✅ Correct Answer**: Displayed when you provide the correct Romaji for a character.
- **❌ Incorrect Answer**: Displayed when your answer is wrong, along with the correct answer.
- **🎉 Perfect Score**: A special celebration for achieving 100% accuracy in a session.

### Example Output

```
Was ist das Romaji für 'あ'? a
✅ Richtig!

Was ist das Romaji für 'い'? u
❌ Falsch! Die richtige Antwort ist: i
```

### With `pip`

If you installed the package with `pip`, you can use the `nihon` command directly:

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

# Disable audio notifications for a session
nihon cli hiragana --no-sound

# Set a specific notification type
nihon cli hiragana --notification-type "mac"
```

## Configuration

Nihon CLI can be configured using a `config.json` file located in `~/.config/nihon-cli/`. The CLI flags will always override the settings in the configuration file.

The following options are available:

| Key                 | Type    | Description                                                                 | Default | CLI Flag                  |
|---------------------|---------|-----------------------------------------------------------------------------|---------|---------------------------|
| `enable_sound`      | boolean | Enable or disable audio notifications at the end of an interval.            | `true`  | `--no-sound`              |
| `notification_type` | string  | Sets the notification type. Options: `bell`, `sound`, `desktop`.            | `bell`  | `--notification-type`     |

### Example `config.json`

```json
{
  "enable_sound": false,
  "notification_type": "desktop"
}
```

To create the configuration file, you can manually create the directory and file at `~/.config/nihon-cli/config.json`.

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