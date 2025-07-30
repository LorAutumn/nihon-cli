# src/nihon_cli/cli/commands.py
"""
CLI command definitions for the Nihon CLI application.
"""

import click

@click.group()
@click.version_option(version="0.1.0", prog_name="nihon-cli")
def cli():
    """
    Nihon CLI is a tool to help you learn Japanese characters.
    """
    pass

# Add commands in future phases
# For example:
# @cli.command()
# @click.option('--type', default='hiragana', help='Character type to practice (hiragana or katakana).')
# def quiz(type):
#     """Start a new quiz."""
#     click.echo(f"Starting a {type} quiz...")

if __name__ == '__main__':
    cli()