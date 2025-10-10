# src/nihon_cli/cli/commands.py
"""
CLI command definitions for the Nihon CLI application using argparse.
"""

import argparse
import sys
from typing import List, Optional

from nihon_cli.app import NihonCli


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
    query direction based on learning progress.
    
    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'limit' attribute.
    """
    from nihon_cli.core.quiz_vocab import VocabQuiz
    from nihon_cli.infra.repository import VocabRepository
    
    try:
        # Initialize repository and quiz engine
        repository = VocabRepository()
        quiz = VocabQuiz(repository)
        
        # Start learning session
        quiz.start_session(limit=args.limit)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Lernsitzung abgebrochen.")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Unerwarteter Fehler: {e}")
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
    learn_parser.set_defaults(func=handle_vocab_learn_command)

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
