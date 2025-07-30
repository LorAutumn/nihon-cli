# Security Policy

## Supported Versions

This project is in active development. Security updates will be applied to the latest version available on the `main` branch.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take all security vulnerabilities seriously. If you discover a security issue, please report it to us by creating a GitHub issue. We appreciate your efforts to disclose your findings responsibly.

Please include the following information in your report:

- A description of the vulnerability and its potential impact.
- Steps to reproduce the issue.
- Any proof-of-concept code.

We will acknowledge your report within 48 hours and will work to address the issue promptly.

## Security Best Practices

The Nihon CLI application is designed with security in mind. Below are the key principles and practices followed in this project:

### 1. Input Validation

- **Command-Line Arguments**: All command-line arguments are parsed using Python's `argparse` library. This is a standard, secure method that prevents command injection by design, as arguments are treated as data, not executable code.
- **User Input**: The only direct user input during runtime is the quiz answer. This input is sanitized using `.strip().lower()` and is only used for string comparison against known correct answers. It is never executed, evaluated, or used in file paths.

### 2. No Shell Command Execution with User Input

- The application avoids using `os.system()` or `subprocess.run()` with user-provided input.
- The `_clear_terminal` function in `app.py` uses a safe, static command (`cls`) on Windows and ANSI escape codes on POSIX systems, avoiding shell injection risks.

### 3. No File System Access

- The application does not perform any file system reads or writes during runtime.
- Character data is compiled into Python modules (`hiragana.py`, `katakana.py`) and imported, which is a safe alternative to reading data from files at runtime and eliminates the risk of path traversal vulnerabilities.

### 4. No Sensitive Data Logging

- The application's logging is configured to record application state and errors for debugging purposes.
- No personally identifiable information or sensitive user inputs (like quiz answers) are logged.

### 5. Secure Exception Handling

- Top-level exception handlers in `main.py` and `app.py` are configured to catch unexpected errors.
- To prevent information disclosure, generic error messages are shown to the user, while detailed exception information is logged for developers.

### 6. Denial-of-Service (DoS) Prevention

- The main quiz loop is hard-coded to a fixed number of questions (10), preventing infinite loops.
- The `random.sample` function is used safely by ensuring the number of requested items does not exceed the available items, preventing potential crashes.

## Summary of Addressed Security Issues (Phase 6.2)

- **Information Disclosure**: Corrected exception handling to avoid leaking raw error messages to the user.
- **Insecure `os.system` usage**: Replaced a potentially unsafe call to `os.system("clear")` with a safer ANSI escape sequence to clear the terminal on POSIX systems.
- **Redundant Logging Configuration**: Removed a duplicate `logging.basicConfig` call to ensure a single, consistent logging setup.

By following these practices, we aim to provide a safe and reliable tool for learning Japanese.