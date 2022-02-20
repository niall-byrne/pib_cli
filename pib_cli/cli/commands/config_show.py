"""ConfigShowCommand class."""

import click
from pib_cli.support import user_configuration

from .bases import command


class ConfigShowCommand(command.CommandBase):
  """CLI command to report the PIB CLI version."""

  def invoke(self) -> None:
    """Invoke the command."""

    config = user_configuration.UserConfiguration()
    click.echo(config.get_raw_file())
