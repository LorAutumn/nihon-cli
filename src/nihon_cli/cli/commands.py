# src/nihon_cli/cli/commands.py
"""
CLI command definitions for the Nihon CLI application using argparse.
"""

import argparse
import sys
from typing import List, Optional

from nihon_cli.app import NihonCli
from nihon_cli.infra.config import save_config


def handle_hiragana_command(args: argparse.Namespace) -> None:
    """
    Handler for the Hiragana training command.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'test' and 'advanced' attributes.
    """
    cli_app = NihonCli()
    cli_app.run_training_session("hiragana", args.test, args.advanced)


def handle_katakana_command(args: argparse.Namespace) -> None:
    """
    Handler for the Katakana training command.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'test' and 'advanced' attributes.
    """
    cli_app = NihonCli()
    cli_app.run_training_session("katakana", args.test, args.advanced)


def handle_mixed_command(args: argparse.Namespace) -> None:
    """
    Handler for the mixed training command.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'test' and 'advanced' attributes.
    """
    cli_app = NihonCli()
    cli_app.run_training_session("mixed", args.test, args.advanced)


def handle_words_command(args: argparse.Namespace) -> None:
    """
    Handler for the words training command.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'test' attribute.
    """
    cli_app = NihonCli()
    cli_app.run_training_session("words", args.test)


def handle_vocab_upload_command(args: argparse.Namespace) -> None:
    """
    Handler for the 'vocab upload' command.
    
    Parses a Markdown file containing vocabulary tables and imports
    the vocabulary items into the database.
    
    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'file' and 'tag' attributes.
    """
    from pathlib import Path
    from nihon_cli.core.parser import MarkdownVocabParser
    from nihon_cli.infra.repository import VocabRepository
    
    file_path = Path(args.file)
    upload_tag = args.tag or file_path.stem
    
    try:
        # Parse the Markdown file
        parser = MarkdownVocabParser()
        items = parser.parse(file_path)
        
        # Update items with the upload tag
        for item in items:
            item.upload_tag = upload_tag
        
        # Insert into database
        repo = VocabRepository()
        inserted, skipped = repo.add_vocabulary_batch(
            items,
            file_path.name,
            upload_tag
        )
        
        # Display results
        print(f"✓ {inserted} Vokabeln erfolgreich importiert!")
        if skipped > 0:
            print(f"  ({skipped} Duplikate übersprungen)")
        
    except FileNotFoundError as e:
        print(f"✗ Fehler: Datei nicht gefunden - {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Fehler: Ungültiges Format - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unerwarteter Fehler: {e}")
        sys.exit(1)


def handle_vocab_learn_command(args: argparse.Namespace) -> None:
    """
    Handler for the 'vocab learn' command.
    
    Starts an interactive vocabulary learning session with adaptive
    query direction based on learning progress and timer-based intervals.
    
    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'limit' and 'test' attributes.
    """
    from nihon_cli.core.quiz_vocab import VocabQuiz
    from nihon_cli.core.timer import LearningTimer
    from nihon_cli.infra.repository import VocabRepository
    
    try:
        # Initialize repository and quiz engine
        repository = VocabRepository()
        quiz = VocabQuiz(repository)
        
        # Determine timer interval based on test mode
        interval_seconds = 5 if args.test else 1500
        
        # Start endless loop with timer
        while True:
            # Run quiz session
            questions_asked = quiz.run_session(limit=args.limit)
            
            # Only start timer if questions were actually asked
            if questions_asked > 0:
                # Initialize timer for next session
                timer = LearningTimer(interval_seconds)
                timer.wait_for_next_session()
            else:
                # No questions available, exit loop
                break
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Lernsitzung abgebrochen.")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Unerwarteter Fehler: {e}")
        sys.exit(1)


def handle_config_set_command(key: str, value: str) -> None:
    """
    Handler for the 'config set' command.
    
    Saves a configuration key-value pair to the config file.
    
    Args:
        key: The configuration key to set
        value: The configuration value to set
    """
    try:
        save_config(key, value)
        print(f"✓ Konfiguration gespeichert: {key} = {value}")
    except Exception as e:
        print(f"✗ Fehler beim Speichern der Konfiguration: {e}")
        sys.exit(1)


def setup_argument_parser() -> argparse.ArgumentParser:
    """
    Creates and configures the argument parser for the CLI.

    This function sets up all commands, sub-commands, and arguments
    for the application. Using argparse is a security best practice as it
    prevents command injection vulnerabilities by design.

    Returns:
        argparse.ArgumentParser: The configured parser instance.
    """
    parser = argparse.ArgumentParser(
        prog="nihon-cli",
        description="A Python-based CLI tool for learning Japanese characters (Hiragana and Katakana) with automated learning intervals.",
        epilog="Use 'nihon-cli <command> --help' for more information on a specific command.",
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Select a training mode", required=True
    )

    # Subparser for 'hiragana'
    hiragana_parser = subparsers.add_parser(
        "hiragana", help="Start a Hiragana character training session"
    )
    hiragana_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of the standard 25-minute intervals",
    )
    hiragana_parser.add_argument(
        "--advanced",
        action="store_true",
        help="Include advanced combination characters (Yōon) in addition to basic characters",
    )
    hiragana_parser.set_defaults(func=handle_hiragana_command)

    # Subparser for 'katakana'
    katakana_parser = subparsers.add_parser(
        "katakana", help="Start a Katakana character training session"
    )
    katakana_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of the standard 25-minute intervals",
    )
    katakana_parser.add_argument(
        "--advanced",
        action="store_true",
        help="Include advanced combination characters (Yōon) in addition to basic characters",
    )
    katakana_parser.set_defaults(func=handle_katakana_command)

    # Subparser for 'mixed'
    mixed_parser = subparsers.add_parser(
        "mixed", help="Start a mixed Hiragana and Katakana character training session"
    )
    mixed_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of the standard 25-minute intervals",
    )
    mixed_parser.add_argument(
        "--advanced",
        action="store_true",
        help="Include advanced combination characters (Yōon) in addition to basic characters",
    )
    mixed_parser.set_defaults(func=handle_mixed_command)

    # Subparser for 'words'
    words_parser = subparsers.add_parser(
        "words", help="Start a Japanese vocabulary training session"
    )
    words_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of the standard 25-minute intervals",
    )
    words_parser.set_defaults(func=handle_words_command)

    # Subparser for 'vocab'
    vocab_parser = subparsers.add_parser(
        "vocab", help="Vocabulary learning and management"
    )
    vocab_subparsers = vocab_parser.add_subparsers(
        dest="vocab_command", help="Vocabulary sub-commands"
    )

    # vocab upload subcommand
    upload_parser = vocab_subparsers.add_parser(
        "upload",
        help="Upload vocabulary from a Markdown file"
    )
    upload_parser.add_argument(
        "file",
        type=str,
        help="Path to the Markdown file containing vocabulary table"
    )
    upload_parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag for this upload (default: filename without extension)"
    )
    upload_parser.set_defaults(func=handle_vocab_upload_command)

    # vocab learn subcommand
    learn_parser = vocab_subparsers.add_parser(
        "learn",
        help="Start an interactive vocabulary learning session"
    )
    learn_parser.add_argument(
        "--limit",
        type=int,
        default=15,
        help="Number of vocabulary items per session (default: 15)"
    )
    learn_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of the standard 25-minute intervals"
    )
    learn_parser.set_defaults(func=handle_vocab_learn_command)

    # Subparser for 'config'
    config_parser = subparsers.add_parser(
        "config", help="Configuration management"
    )
    config_subparsers = config_parser.add_subparsers(
        dest="config_command", help="Configuration sub-commands"
    )

    # config set subcommand
    set_parser = config_subparsers.add_parser(
        "set",
        help="Set a configuration value"
    )
    set_parser.add_argument(
        "key",
        type=str,
        help="Configuration key to set"
    )
    set_parser.add_argument(
        "value",
        type=str,
        help="Configuration value to set"
    )
    set_parser.set_defaults(func=lambda args: handle_config_set_command(args.key, args.value))

    return parser


def parse_and_execute(args: Optional[List[str]] = None) -> None:
    """
    Parses command-line arguments and executes the corresponding action.

    Args:
        args (Optional[List[str]], optional): A list of strings to parse.
                                              If None, sys.argv[1:] is used.
                                              Defaults to None.
    """
    parser = setup_argument_parser()

    # If no arguments are provided (e.g., just 'nihon'), show help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return

    parsed_args = parser.parse_args(args)

    if hasattr(parsed_args, "func"):
        parsed_args.func(parsed_args)
    else:
        # Fallback if a command is called without a function
        # (should not happen with required=True)
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    parse_and_execute()
