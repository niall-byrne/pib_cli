"""Click based CLI interface."""

import click
from pib_cli.cli.interface.builtins import builtin_commands
from pib_cli.cli.interface.custom import custom_commands

cli_interface = click.CommandCollection(sources=[custom_commands])
custom_commands.add_command(builtin_commands)
