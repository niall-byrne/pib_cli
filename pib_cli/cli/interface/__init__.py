"""Click based CLI interface."""

import click
from pib_cli.cli.interface.builtins import builtin_commands
from pib_cli.cli.interface.custom import custom_commands
from pib_cli.config import _

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

custom_commands.add_command(builtin_commands)
cli_interface = click.CommandCollection(
    help=_("Python-In-A-Box CLI."),
    sources=[custom_commands],
    context_settings=CONTEXT_SETTINGS
)
