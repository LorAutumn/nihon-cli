# src/nihon_cli/cli/commands.py
"""
CLI command definitions for the Nihon CLI application using argparse.
"""

import argparse
import sys
import os
from src.nihon_cli.core.quiz import Quiz
from src.nihon_cli.core.timer import LearningTimer

def _clear_terminal():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def _run_learning_loop(quiz_type: str, is_test_mode: bool):
    """
    Führt eine kontinuierliche Lernschleife aus Quiz-Sessions und Pausen durch.

    Args:
        quiz_type (str): Der Typ des Quiz ('hiragana', 'katakana', 'mixed').
        is_test_mode (bool): Ob der Testmodus aktiv ist.
    """
    interval = 5 if is_test_mode else 1500
    quiz = Quiz(quiz_type)
    timer = LearningTimer(interval)

    mode_name = {
        "hiragana": "Hiragana",
        "katakana": "Katakana",
        "mixed": "Hiragana & Katakana"
    }.get(quiz_type, "Unbekannt")

    print(f"Willkommen zum {mode_name}-Training!")
    print("Drücke Ctrl+C, um das Training jederzeit zu beenden.")
    
    try:
        while True:
            _clear_terminal()
            quiz.run_session()
            print("\nNächste Session beginnt bald...")
            timer.wait_for_next_session()
            
    except KeyboardInterrupt:
        print("\n\nTraining manuell beendet. Auf Wiedersehen!")
        sys.exit(0)
    except Exception as e:
        print(f"\nEin unerwarteter Fehler ist aufgetreten: {e}")
        print("Das Programm wird beendet.")
        sys.exit(1)

def handle_hiragana_command(args):
    """Handler für das Hiragana-Trainingskommando."""
    _run_learning_loop("hiragana", args.test)

def handle_katakana_command(args):
    """Handler für das Katakana-Trainingskommando."""
    _run_learning_loop("katakana", args.test)

def handle_mixed_command(args):
    """Handler für das gemischte Trainingskommando."""
    _run_learning_loop("mixed", args.test)

def setup_argument_parser():
    """Erstellt und konfiguriert den Argument-Parser für die CLI."""
    parser = argparse.ArgumentParser(
        prog="nihon",
        description="Nihon CLI ist ein Werkzeug, um japanische Schriftzeichen zu lernen.",
        epilog="Benutze 'nihon cli <kommando> --help' für mehr Informationen über ein spezifisches Kommando."
    )
    
    subparsers = parser.add_subparsers(dest="main_command", help="Verfügbare Hauptkommandos")

    # Subparser für das 'cli' Kommando
    cli_parser = subparsers.add_parser("cli", help="Startet das Schriftzeichen-Training.")
    cli_subparsers = cli_parser.add_subparsers(dest="command", help="Wähle einen Trainingsmodus", required=True)

    # Subparser für 'hiragana'
    hiragana_parser = cli_subparsers.add_parser("hiragana", help="Startet ein reines Hiragana-Training.")
    hiragana_parser.add_argument("--test", action="store_true", help="Führt das Training im 5-Sekunden-Testmodus aus.")
    hiragana_parser.set_defaults(func=handle_hiragana_command)

    # Subparser für 'katakana'
    katakana_parser = cli_subparsers.add_parser("katakana", help="Startet ein reines Katakana-Training.")
    katakana_parser.add_argument("--test", action="store_true", help="Führt das Training im 5-Sekunden-Testmodus aus.")
    katakana_parser.set_defaults(func=handle_katakana_command)

    # Subparser für 'mixed'
    mixed_parser = cli_subparsers.add_parser("mixed", help="Startet ein gemischtes Hiragana- und Katakana-Training.")
    mixed_parser.add_argument("--test", action="store_true", help="Führt das Training im 5-Sekunden-Testmodus aus.")
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
    
    if hasattr(parsed_args, 'func'):
        parsed_args.func(parsed_args)
    else:
        # Fallback, falls ein Kommando ohne Funktion aufgerufen wird (sollte nicht passieren mit required=True)
        parser.print_help(sys.stderr)

if __name__ == '__main__':
    parse_and_execute()