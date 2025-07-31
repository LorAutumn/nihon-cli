# src/nihon_cli/cli/commands.py
"""
CLI command definitions for the Nihon CLI application using argparse.
"""

import argparse
import sys
from typing import List, Optional

from nihon_cli.app import NihonCli
from nihon_cli.core.config import Config


def handle_hiragana_command(args: argparse.Namespace, config: Config) -> None:
    """
    Handler for the Hiragana training command.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        config (Config): The application configuration object.
    """
    if "no_sound" in args and args.no_sound:
        config.enable_sound = False

    if "notification_type" in args and args.notification_type:
        config.notification_type = args.notification_type

    cli_app = NihonCli(config)
    cli_app.run_training_session("hiragana", args.test)


def handle_katakana_command(args: argparse.Namespace, config: Config) -> None:
    """
    Handler for the Katakana training command.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        config (Config): The application configuration object.
    """
    if "no_sound" in args and args.no_sound:
        config.enable_sound = False

    if "notification_type" in args and args.notification_type:
        config.notification_type = args.notification_type

    cli_app = NihonCli(config)
    cli_app.run_training_session("katakana", args.test)


def handle_mixed_command(args: argparse.Namespace, config: Config) -> None:
    """
    Handler for the mixed training command.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        config (Config): The application configuration object.
    """
    if "no_sound" in args and args.no_sound:
        config.enable_sound = False

    if "notification_type" in args and args.notification_type:
        config.notification_type = args.notification_type

    cli_app = NihonCli(config)
    cli_app.run_training_session("mixed", args.test)


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
        prog="nihon",
        description="Nihon CLI is a tool to learn Japanese characters.",
        epilog="Use 'nihon cli <command> --help' for more information on a specific command.",
    )

    subparsers = parser.add_subparsers(
        dest="main_command", help="Available main commands"
    )

    # Subparser for the 'cli' command
    cli_parser = subparsers.add_parser("cli", help="Starts the character training.")
    cli_subparsers = cli_parser.add_subparsers(
        dest="command", help="Select a training mode", required=True
    )

    # Subparser for 'hiragana'
    hiragana_parser = cli_subparsers.add_parser(
        "hiragana", help="Starts a pure Hiragana training."
    )
    hiragana_parser.add_argument(
        "--test",
        action="store_true",
        help="Runs the training in a 5-second test mode.",
    )
    hiragana_parser.add_argument(
        "--no-sound",
        action="store_true",
        help="Disables audio notifications.",
    )
    hiragana_parser.add_argument(
        "--notification-type",
        choices=["bell", "sound", "desktop"],
        help="Sets the notification type (overrides config).",
    )
    hiragana_parser.set_defaults(func=handle_hiragana_command)

    # Subparser for 'katakana'
    katakana_parser = cli_subparsers.add_parser(
        "katakana", help="Starts a pure Katakana training."
    )
    katakana_parser.add_argument(
        "--test",
        action="store_true",
        help="Runs the training in a 5-second test mode.",
    )
    katakana_parser.add_argument(
        "--no-sound",
        action="store_true",
        help="Disables audio notifications.",
    )
    katakana_parser.add_argument(
        "--notification-type",
        choices=["bell", "sound", "desktop"],
        help="Sets the notification type (overrides config).",
    )
    katakana_parser.set_defaults(func=handle_katakana_command)

    # Subparser for 'mixed'
    mixed_parser = cli_subparsers.add_parser(
        "mixed", help="Starts a mixed Hiragana and Katakana training."
    )
    mixed_parser.add_argument(
        "--test",
        action="store_true",
        help="Runs the training in a 5-second test mode.",
    )
    mixed_parser.add_argument(
        "--no-sound",
        action="store_true",
        help="Disables audio notifications.",
    )
    mixed_parser.add_argument(
        "--notification-type",
        choices=["bell", "sound", "desktop"],
        help="Sets the notification type (overrides config).",
    )
    mixed_parser.set_defaults(func=handle_mixed_command)

    return parser


def parse_and_execute(args: Optional[List[str]] = None) -> None:
    """
    Parses command-line arguments and executes the corresponding action.

    Args:
        args (Optional[List[str]], optional): A list of strings to parse.
                                              If None, sys.argv[1:] is used.
                                              Defaults to None.
    """
    config = Config()
    parser = setup_argument_parser()

    # If no arguments are provided (e.g., just 'nihon'), show help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return

    parsed_args = parser.parse_args(args)

    if hasattr(parsed_args, "func"):
        parsed_args.func(parsed_args, config)
    else:
        # Fallback if a command is called without a function
        # (should not happen with required=True)
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    parse_and_execute()
