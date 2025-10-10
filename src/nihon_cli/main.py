# src/nihon_cli/main.py
"""
Main entry point for the Nihon CLI application.
"""

import logging
import sys

from nihon_cli.cli.commands import parse_and_execute
from nihon_cli.infra import init_db


def main() -> None:
    """
    This function is the main entry point for the command-line interface.

    It executes the CLI application and handles top-level exceptions
    to ensure the application exits gracefully.
    """
    try:
        # Initialize the vocabulary database on startup
        init_db()
        
        parse_and_execute()
    except Exception as e:
        logging.critical(f"A critical unhandled error occurred: {e}", exc_info=True)
        print(
            "\nEin kritischer Fehler ist aufgetreten. Die Anwendung wird beendet.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
