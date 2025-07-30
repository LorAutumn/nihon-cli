# src/nihon_cli/main.py
"""
Main entry point for the Nihon CLI application.
"""

from nihon_cli.cli.commands import parse_and_execute

def main():
    """
    This function is the main entry point for the command-line interface.
    It executes the CLI application.
    """
    parse_and_execute()

if __name__ == "__main__":
    main()