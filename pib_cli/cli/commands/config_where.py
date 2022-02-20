"""ConfigWhereCommand class."""

import click
from pib_cli import config_filename

from .bases import command


class ConfigWhereCommand(command.CommandBase):
  """CLI command to reveal the current PIB CLI configuration's location."""

  def invoke(self) -> None:
    """Invoke the command."""

    click.echo(f"Current Configuration: {config_filename}")
