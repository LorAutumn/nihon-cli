# src/nihon_cli/main.py
"""
Main entry point for the Nihon CLI application.
"""

import sys
from nihon_cli.cli.commands import parse_and_execute

def main():
    """
    This function is the main entry point for the command-line interface.
    It executes the CLI application and handles top-level exceptions.
    """
    try:
        parse_and_execute()
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()