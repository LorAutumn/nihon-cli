# src/nihon_cli/cli/commands.py
"""
CLI command definitions for the Nihon CLI application using argparse.
"""

import argparse
import sys
from nihon_cli.app import NihonCli


def handle_hiragana_command(args):
    """Handler für das Hiragana-Trainingskommando."""
    cli_app = NihonCli()
    cli_app.run_training_session("hiragana", args.test)


def handle_katakana_command(args):
    """Handler für das Katakana-Trainingskommando."""
    cli_app = NihonCli()
    cli_app.run_training_session("katakana", args.test)


def handle_mixed_command(args):
    """Handler für das gemischte Trainingskommando."""
    cli_app = NihonCli()
    cli_app.run_training_session("mixed", args.test)


def setup_argument_parser():
    """Erstellt und konfiguriert den Argument-Parser für die CLI."""
    parser = argparse.ArgumentParser(
        prog="nihon",
        description="Nihon CLI ist ein Werkzeug, um japanische Schriftzeichen zu lernen.",
        epilog="Benutze 'nihon cli <kommando> --help' für mehr Informationen über ein spezifisches Kommando.",
    )

    subparsers = parser.add_subparsers(
        dest="main_command", help="Verfügbare Hauptkommandos"
    )

    # Subparser für das 'cli' Kommando
    cli_parser = subparsers.add_parser(
        "cli", help="Startet das Schriftzeichen-Training."
    )
    cli_subparsers = cli_parser.add_subparsers(
        dest="command", help="Wähle einen Trainingsmodus", required=True
    )

    # Subparser für 'hiragana'
    hiragana_parser = cli_subparsers.add_parser(
        "hiragana", help="Startet ein reines Hiragana-Training."
    )
    hiragana_parser.add_argument(
        "--test",
        action="store_true",
        help="Führt das Training im 5-Sekunden-Testmodus aus.",
    )
    hiragana_parser.set_defaults(func=handle_hiragana_command)

    # Subparser für 'katakana'
    katakana_parser = cli_subparsers.add_parser(
        "katakana", help="Startet ein reines Katakana-Training."
    )
    katakana_parser.add_argument(
        "--test",
        action="store_true",
        help="Führt das Training im 5-Sekunden-Testmodus aus.",
    )
    katakana_parser.set_defaults(func=handle_katakana_command)

    # Subparser für 'mixed'
    mixed_parser = cli_subparsers.add_parser(
        "mixed", help="Startet ein gemischtes Hiragana- und Katakana-Training."
    )
    mixed_parser.add_argument(
        "--test",
        action="store_true",
        help="Führt das Training im 5-Sekunden-Testmodus aus.",
    )
    mixed_parser.set_defaults(func=handle_mixed_command)

    return parser


def parse_and_execute(args=None):
    """Parst die Kommandozeilenargumente und führt die entsprechende Aktion aus."""
    parser = setup_argument_parser()

    # Wenn keine Argumente übergeben werden (z.B. nur 'nihon'), zeige die Hilfe
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return

    parsed_args = parser.parse_args(args)

    if hasattr(parsed_args, "func"):
        parsed_args.func(parsed_args)
    else:
        # Fallback, falls ein Kommando ohne Funktion aufgerufen wird (sollte nicht passieren mit required=True)
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    parse_and_execute()
