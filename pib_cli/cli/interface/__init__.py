"""Click based CLI interface."""

import click
from pib_cli.cli.interface.builtins import builtin_commands
from pib_cli.cli.interface.external import external_commands

cli_interface = click.CommandCollection(sources=[external_commands])
external_commands.add_command(builtin_commands)
