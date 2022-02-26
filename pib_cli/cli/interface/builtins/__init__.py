"""Built in CLI commands."""

import click
from pib_cli.cli.commands import handler, version
from pib_cli.config.locale import _

from .config import config_commands
from .container import container_commands


@click.group(_("@pib"))
def builtins() -> None:
  """PIB built-in commands."""


@builtins.command(_("version"))
def version_builtin() -> None:
  """Display the current CLI version."""

  handler(version.VersionCommand)


builtin_commands: click.Group = builtins
builtin_commands.add_command(config_commands)
builtin_commands.add_command(container_commands)
